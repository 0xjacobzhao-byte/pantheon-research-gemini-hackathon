#!/usr/bin/env python3
"""Optional live Gemini smoke test — redacted artifact.

Requires:
  DEMO_MODE=live
  GEMINI_API_KEY or GOOGLE_API_KEY set in environment.

Produces:
  data/gemini_live_call_redacted.json

If key is not available, exits gracefully with SKIPPED_MISSING_GEMINI_KEY.
"""

from __future__ import annotations

import asyncio
import json
import os
import sys
import time
from pathlib import Path

# Add backend to path so we can import the overlay module
BACKEND_DIR = Path(__file__).resolve().parent.parent / "backend"
sys.path.insert(0, str(BACKEND_DIR))

from app.gemini_overlay import run_gemini_overlay, _check_credential, GEMINI_MODEL
from app.evidence_loader import load_evidence


REDACTED_OUTPUT = Path(__file__).resolve().parent.parent / "data" / "gemini_live_call_redacted.json"


async def main() -> None:
    # Check prerequisites
    demo_mode = os.environ.get("DEMO_MODE", "offline")
    if demo_mode != "live":
        print("SKIPPED: DEMO_MODE is not 'live'. Set DEMO_MODE=live to run live smoke.")
        sys.exit(0)

    if not _check_credential():
        print("SKIPPED_MISSING_GEMINI_KEY")
        print("No GEMINI_API_KEY or GOOGLE_API_KEY found in environment.")
        print("Live Gemini smoke skipped — offline mode and code path are still valid.")
        sys.exit(0)

    print("Running live Gemini overlay for NVDA...")
    start = time.monotonic()

    try:
        evidence = load_evidence("NVDA")
    except Exception as exc:
        print(f"ERROR loading evidence: {exc}")
        sys.exit(1)

    overlay = await run_gemini_overlay(evidence, demo_mode=False)
    latency_ms = int((time.monotonic() - start) * 1000)

    # Build redacted artifact
    artifact = {
        "schema_version": "gemini-live-smoke-v1",
        "provider": "Google Gemini API",
        "model": GEMINI_MODEL,
        "ticker": "NVDA",
        "status": overlay.status.value if hasattr(overlay.status, "value") else str(overlay.status),
        "latency_ms": overlay.latency_ms or latency_ms,
        "attempts": overlay.attempts,
        "redacted": True,
        "no_secrets": True,
        "note": "All secrets redacted. Only provider, model, ticker, status, and latency stored.",
    }

    if overlay.takeaway:
        artifact["takeaway_preview"] = overlay.takeaway[:200] + ("..." if len(overlay.takeaway) > 200 else "")

    if overlay.assessment:
        artifact["assessment_available"] = True
    else:
        artifact["assessment_available"] = False

    if overlay.error_message:
        artifact["error_message"] = overlay.error_message

    # Write artifact
    REDACTED_OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    REDACTED_OUTPUT.write_text(json.dumps(artifact, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Artifact written to: {REDACTED_OUTPUT}")
    print(f"Status: {artifact['status']}")
    print(f"Latency: {artifact['latency_ms']}ms")


if __name__ == "__main__":
    asyncio.run(main())
