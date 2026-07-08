"""Fail-closed guarantees for the Gemini overlay.

A missing credential must BLOCK (never a hollow SUCCESS); a non-JSON model
response must surface as PARSE_ERROR; offline mode must serve bundled samples.
"""

import os
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app import gemini_overlay
from app.models import OverlayStatus
from app.sample_loader import load_evidence


@pytest.mark.asyncio
async def test_gemini_missing_credential_fails_closed(monkeypatch):
    monkeypatch.setenv("DEMO_MODE", "live")
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)
    monkeypatch.delenv("GOOGLE_API_KEY", raising=False)

    overlay = await gemini_overlay.run_gemini_overlay(load_evidence("MA"))
    assert overlay.status == OverlayStatus.BLOCKED_BY_MISSING_CREDENTIAL
    assert overlay.assessment is None
    assert overlay.error_message and "blocked" in overlay.error_message.lower()


def test_gemini_invalid_json_raises_parse_error():
    with pytest.raises(ValueError):
        gemini_overlay._parse_json_response("definitely not json {")


def test_gemini_fenced_json_still_parses():
    out = gemini_overlay._parse_json_response('```json\n{"takeaway": "ok"}\n```')
    assert out["takeaway"] == "ok"


@pytest.mark.asyncio
async def test_gemini_offline_sample_works(monkeypatch):
    monkeypatch.setenv("DEMO_MODE", "offline")
    overlay = await gemini_overlay.run_gemini_overlay(load_evidence("NVDA"))
    assert overlay.status == OverlayStatus.OFFLINE_SAMPLE
    assert overlay.assessment is not None
    assert overlay.takeaway
    assert overlay.prompt_version and overlay.output_schema_version


@pytest.mark.asyncio
async def test_gemini_offline_sample_ma(monkeypatch):
    monkeypatch.setenv("DEMO_MODE", "offline")
    overlay = await gemini_overlay.run_gemini_overlay(load_evidence("MA"))
    assert overlay.status == OverlayStatus.OFFLINE_SAMPLE
    assert overlay.assessment is not None
    assert overlay.takeaway


def test_gemini_missing_sample_is_error():
    overlay = gemini_overlay._load_sample_overlay("ZZZZ")
    assert overlay.status == OverlayStatus.API_ERROR
    assert overlay.assessment is None


def test_gemini_overlay_carries_prompt_and_schema_version():
    overlay = gemini_overlay._load_sample_overlay("MA")
    assert overlay.prompt_version == gemini_overlay.PROMPT_VERSION
    assert overlay.output_schema_version == gemini_overlay.OUTPUT_SCHEMA_VERSION


def test_gemini_check_credential(monkeypatch):
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)
    monkeypatch.delenv("GOOGLE_API_KEY", raising=False)
    assert gemini_overlay._check_credential() is False

    monkeypatch.setenv("GEMINI_API_KEY", "test-key")
    assert gemini_overlay._check_credential() is True
