"""Google Gemini qualitative overlay integration (fail-closed).

Default mode: offline sample, no API key required.
Live mode: call Gemini only when DEMO_MODE=live and GEMINI_API_KEY or GOOGLE_API_KEY is set.
Missing key -> BLOCKED_BY_MISSING_CREDENTIAL.
API failure -> API_ERROR.
Invalid/non-JSON model response -> PARSE_ERROR.
Never return fake SUCCESS. Never return secrets.
"""

from __future__ import annotations

import asyncio
import json
import os
import time
from pathlib import Path
from typing import Optional

import httpx

from .models import (
    EquityEvidence,
    LLMProvider,
    OverlayAssessment,
    OverlayStatus,
    QualitativeOverlay,
    TokenUsage,
)

GEMINI_BASE_URL = os.environ.get(
    "GEMINI_BASE_URL",
    "https://generativelanguage.googleapis.com/v1beta",
)
GEMINI_MODEL = os.environ.get("GEMINI_MODEL", "gemini-2.0-flash")

PROMPT_VERSION = "gemini-overlay-v1.0"
OUTPUT_SCHEMA_VERSION = "overlay-assessment-1.0"

MAX_ATTEMPTS = int(os.environ.get("GEMINI_MAX_ATTEMPTS", "3"))
BACKOFF_BASE_SECONDS = float(os.environ.get("GEMINI_BACKOFF_BASE_SECONDS", "0.5"))

DATA_DIR = Path(__file__).resolve().parent.parent.parent / "data"


def _check_credential() -> bool:
    return bool(os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY"))


def _api_key() -> Optional[str]:
    return os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")


def _build_prompt(evidence: EquityEvidence) -> str:
    metrics = []
    if evidence.pe_ratio is not None:
        metrics.append(f"P/E (TTM): {evidence.pe_ratio}")
    if evidence.pb_ratio is not None:
        metrics.append(f"P/B: {evidence.pb_ratio}")
    if evidence.roic_pct is not None:
        metrics.append(f"ROIC: {evidence.roic_pct}%")
    if evidence.fcf_ttm_usd is not None:
        metrics.append(f"FCF (TTM): ${evidence.fcf_ttm_usd:,.0f}")
    if evidence.revenue_growth_yoy_pct is not None:
        metrics.append(f"Revenue Growth YoY: {evidence.revenue_growth_yoy_pct}%")
    if evidence.gross_margin_pct is not None:
        metrics.append(f"Gross Margin: {evidence.gross_margin_pct}%")
    if evidence.net_margin_pct is not None:
        metrics.append(f"Net Margin: {evidence.net_margin_pct}%")
    if evidence.debt_to_equity is not None:
        metrics.append(f"D/E: {evidence.debt_to_equity}")

    return f"""You are a senior equity research analyst. Based on the following quantitative evidence, produce a structured qualitative overlay for {evidence.company_name} ({evidence.ticker}).

Company: {evidence.company_name}
Ticker: {evidence.ticker}
Exchange: {evidence.exchange}
Sector: {evidence.sector}
Industry: {evidence.industry}
Market Cap: ${evidence.market_cap_usd:,.0f}
Summary: {evidence.summary}

Key Metrics:
{chr(10).join(metrics)}

Respond as JSON with these exact fields:
- takeaway: one-paragraph summary
- business_quality: assessment text
- moat: assessment text
- pricing_power: assessment text
- capital_allocation: assessment text
- red_flags: assessment text
- confidence: float 0-1
- missing_evidence: list of strings
- risk_summary: brief risk summary
- human_review_notes: notes for human reviewer

Use professional financial language. Be concise but specific."""


def _blocked_overlay(ticker: str) -> QualitativeOverlay:
    return QualitativeOverlay(
        provider=LLMProvider.GEMINI,
        model=GEMINI_MODEL,
        ticker=ticker,
        status=OverlayStatus.BLOCKED_BY_MISSING_CREDENTIAL,
        error_message="GEMINI_API_KEY is not set — live Gemini call blocked (fail-closed).",
        prompt_version=PROMPT_VERSION,
        output_schema_version=OUTPUT_SCHEMA_VERSION,
    )


def _usage_from_response(data: dict) -> Optional[TokenUsage]:
    usage = data.get("usageMetadata")
    if not isinstance(usage, dict):
        return None
    return TokenUsage(
        prompt_tokens=usage.get("promptTokenCount"),
        completion_tokens=usage.get("candidatesTokenCount"),
        total_tokens=usage.get("totalTokenCount"),
        estimated_cost_usd=None,
    )


async def run_gemini_overlay(
    evidence: EquityEvidence, demo_mode: bool = False
) -> QualitativeOverlay:
    """Run the Gemini qualitative overlay (fail-closed)."""
    if demo_mode or os.environ.get("DEMO_MODE", "offline") == "offline":
        return _load_sample_overlay(evidence.ticker)

    if not _check_credential():
        return _blocked_overlay(evidence.ticker)

    prompt = _build_prompt(evidence)
    api_key = _api_key()
    start = time.monotonic()
    last_error: Optional[str] = None

    for attempt in range(1, MAX_ATTEMPTS + 1):
        try:
            async with httpx.AsyncClient(timeout=60.0) as client:
                resp = await client.post(
                    f"{GEMINI_BASE_URL}/models/{GEMINI_MODEL}:generateContent",
                    headers={"Content-Type": "application/json"},
                    params={"key": api_key},
                    json={
                        "contents": [{"parts": [{"text": prompt}]}],
                        "generationConfig": {
                            "temperature": 0.7,
                            "responseMimeType": "application/json",
                        },
                    },
                )
                resp.raise_for_status()

            data = resp.json()
            # Gemini returns text in candidates[0].content.parts[0].text
            candidates = data.get("candidates", [])
            if not candidates:
                raise ValueError("No candidates in Gemini response")
            parts = candidates[0].get("content", {}).get("parts", [])
            if not parts:
                raise ValueError("No parts in Gemini response candidate")
            raw = parts[0].get("text", "")
            latency_ms = int((time.monotonic() - start) * 1000)

            try:
                parsed = _parse_json_response(raw)
            except ValueError as parse_exc:
                return QualitativeOverlay(
                    provider=LLMProvider.GEMINI,
                    model=GEMINI_MODEL,
                    ticker=evidence.ticker,
                    status=OverlayStatus.PARSE_ERROR,
                    error_message=f"Invalid JSON from model: {parse_exc}",
                    latency_ms=latency_ms,
                    attempts=attempt,
                    prompt_version=PROMPT_VERSION,
                    output_schema_version=OUTPUT_SCHEMA_VERSION,
                )

            assessment = OverlayAssessment(
                business_quality=parsed.get("business_quality", ""),
                moat=parsed.get("moat", ""),
                pricing_power=parsed.get("pricing_power", ""),
                capital_allocation=parsed.get("capital_allocation", ""),
                red_flags=parsed.get("red_flags", ""),
                confidence=float(parsed.get("confidence", 0.5)),
                missing_evidence=parsed.get("missing_evidence", []),
            )

            return QualitativeOverlay(
                provider=LLMProvider.GEMINI,
                model=GEMINI_MODEL,
                ticker=evidence.ticker,
                status=OverlayStatus.SUCCESS,
                takeaway=parsed.get("takeaway", ""),
                assessment=assessment,
                latency_ms=latency_ms,
                attempts=attempt,
                prompt_version=PROMPT_VERSION,
                output_schema_version=OUTPUT_SCHEMA_VERSION,
                usage=_usage_from_response(data),
            )

        except Exception as exc:  # noqa: BLE001
            last_error = str(exc)
            if attempt < MAX_ATTEMPTS:
                await asyncio.sleep(BACKOFF_BASE_SECONDS * (2 ** (attempt - 1)))
                continue

    latency_ms = int((time.monotonic() - start) * 1000)
    return QualitativeOverlay(
        provider=LLMProvider.GEMINI,
        model=GEMINI_MODEL,
        ticker=evidence.ticker,
        status=OverlayStatus.API_ERROR,
        error_message=last_error or "Unknown upstream error",
        latency_ms=latency_ms,
        attempts=MAX_ATTEMPTS,
        prompt_version=PROMPT_VERSION,
        output_schema_version=OUTPUT_SCHEMA_VERSION,
    )


def _parse_json_response(raw: str) -> dict:
    """Parse a JSON response from the LLM, handling markdown fences."""
    text = raw.strip()
    if text.startswith("```"):
        lines = text.split("\n")
        lines = [l for l in lines if not l.strip().startswith("```")]
        text = "\n".join(lines)
    try:
        return json.loads(text)
    except json.JSONDecodeError as exc:
        raise ValueError(str(exc)) from exc


def _load_sample_overlay(ticker: str) -> QualitativeOverlay:
    """Load a pre-generated Gemini sample overlay from data/gemini_samples/."""
    filepath = DATA_DIR / "gemini_samples" / f"{ticker.lower()}_gemini_overlay.json"
    if not filepath.exists():
        return QualitativeOverlay(
            provider=LLMProvider.GEMINI,
            model=GEMINI_MODEL,
            ticker=ticker,
            status=OverlayStatus.API_ERROR,
            error_message=f"No bundled Gemini sample for ticker: {ticker}",
            prompt_version=PROMPT_VERSION,
            output_schema_version=OUTPUT_SCHEMA_VERSION,
        )
    with open(filepath, encoding="utf-8") as f:
        data = json.load(f)

    assessment = OverlayAssessment(**data.get("assessment", {}))
    return QualitativeOverlay(
        provider=LLMProvider.GEMINI,
        model=data.get("model", GEMINI_MODEL),
        ticker=data.get("ticker", ticker),
        status=OverlayStatus.OFFLINE_SAMPLE,
        takeaway=data.get("takeaway", ""),
        assessment=assessment,
        prompt_version=PROMPT_VERSION,
        output_schema_version=OUTPUT_SCHEMA_VERSION,
    )
