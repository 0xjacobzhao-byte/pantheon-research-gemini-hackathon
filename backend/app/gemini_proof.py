"""Gemini proof endpoint — secret-free metadata.

This endpoint makes NO external calls. It reports credential state as a boolean,
never returns key values, and is safe for public-facing demo use.
"""

from __future__ import annotations

import os

from .gemini_overlay import (
    GEMINI_BASE_URL,
    GEMINI_MODEL,
    PROMPT_VERSION,
    OUTPUT_SCHEMA_VERSION,
    _check_credential,
)


def get_gemini_proof() -> dict:
    """Return Gemini proof metadata (no secrets, no external calls)."""
    credential_configured = _check_credential()
    demo_mode = os.environ.get("DEMO_MODE", "offline")

    return {
        "schema_version": "gemini-proof-v1",
        "project": "Pantheon Research Gemini Analyst",
        "status": "ok",
        "provider": "Google Gemini API",
        "credential_configured": credential_configured,
        "demo_mode": demo_mode,
        "model": GEMINI_MODEL,
        "base_url": GEMINI_BASE_URL,
        "prompt_version": PROMPT_VERSION,
        "output_schema_version": OUTPUT_SCHEMA_VERSION,
        "actual_call_implementation": "backend/app/gemini_overlay.py",
        "proof_endpoint_external_calls": False,
        "safe_claims": [
            "Gemini overlay uses Google Generative Language API (v1beta).",
            "Actual Gemini API call implementation is in backend/app/gemini_overlay.py.",
            "Default mode is offline — bundled samples serve the demo with no API key.",
            "Live mode requires DEMO_MODE=live and GEMINI_API_KEY or GOOGLE_API_KEY.",
            "Fail-closed: missing key -> BLOCKED_BY_MISSING_CREDENTIAL, "
            "API error -> API_ERROR, bad JSON -> PARSE_ERROR.",
            "This proof endpoint makes no external calls and returns no secrets.",
        ],
        "non_claims": [
            "Not claiming autonomous trading or model-generated alpha.",
            "Not exposing private production strategy code.",
            "Not claiming investment performance or returns.",
            "Pantheon Research existed before the hackathon; the Gemini-powered "
            "analyst / risk-review layer is the new hackathon work.",
        ],
        "attestation": {
            "proof_endpoint_external_calls": False,
            "credential_values_returned": False,
            "secrets_policy": "booleans only; no key, token, or URL returned",
        },
    }
