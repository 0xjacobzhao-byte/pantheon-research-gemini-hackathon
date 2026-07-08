"""Gemini proof endpoint tests — secret-free, no external calls."""

import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.gemini_proof import get_gemini_proof


def test_gemini_proof_returns_correct_schema():
    proof = get_gemini_proof()
    assert proof["schema_version"] == "gemini-proof-v1"
    assert proof["project"] == "Pantheon Research Gemini Analyst"
    assert proof["status"] == "ok"
    assert proof["provider"] == "Google Gemini API"


def test_gemini_proof_no_secrets(monkeypatch):
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)
    monkeypatch.delenv("GOOGLE_API_KEY", raising=False)
    proof = get_gemini_proof()
    assert proof["credential_configured"] is False
    assert proof["proof_endpoint_external_calls"] is False
    # Ensure no key values leaked
    proof_str = str(proof)
    assert "AIza" not in proof_str


def test_gemini_proof_credential_detected(monkeypatch):
    monkeypatch.setenv("GEMINI_API_KEY", "test-key")
    proof = get_gemini_proof()
    assert proof["credential_configured"] is True


def test_gemini_proof_google_api_key_detected(monkeypatch):
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)
    monkeypatch.setenv("GOOGLE_API_KEY", "test-key")
    proof = get_gemini_proof()
    assert proof["credential_configured"] is True


def test_gemini_proof_demo_mode(monkeypatch):
    monkeypatch.setenv("DEMO_MODE", "offline")
    proof = get_gemini_proof()
    assert proof["demo_mode"] == "offline"


def test_gemini_proof_safe_claims_present():
    proof = get_gemini_proof()
    assert len(proof["safe_claims"]) > 0
    assert len(proof["non_claims"]) > 0


def test_gemini_proof_implementation_path():
    proof = get_gemini_proof()
    assert proof["actual_call_implementation"] == "backend/app/gemini_overlay.py"


def test_gemini_proof_attestation():
    proof = get_gemini_proof()
    att = proof["attestation"]
    assert att["proof_endpoint_external_calls"] is False
    assert att["credential_values_returned"] is False
