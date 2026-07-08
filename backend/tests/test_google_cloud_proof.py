"""Tests for Google Cloud proof endpoint — secret-free, correct schema."""

from __future__ import annotations

import os
import json

from app.google_cloud_proof import get_google_cloud_proof


def test_returns_dict():
    result = get_google_cloud_proof()
    assert isinstance(result, dict)


def test_schema_version():
    result = get_google_cloud_proof()
    assert result["schema_version"] == "google-cloud-proof-v1"


def test_status_ok():
    result = get_google_cloud_proof()
    assert result["status"] == "ok"


def test_cloud_provider_google():
    result = get_google_cloud_proof()
    assert result["cloud_provider"] == "Google Cloud"


def test_runtime_cloud_run():
    result = get_google_cloud_proof()
    assert result["runtime"] == "Cloud Run"


def test_no_secrets_in_response():
    """No real API keys, tokens, or database URLs in the response."""
    result = get_google_cloud_proof()
    proof_str = json.dumps(result)
    for pattern in ("AIza", "sk-proj-", "ghp_", "xoxb-", "postgres://user:"):
        assert pattern not in proof_str, f"Secret pattern found in response: {pattern}"


def test_artifact_registry_true():
    result = get_google_cloud_proof()
    assert result["artifact_registry"] is True


def test_cloud_sql_full_production_clone_verified_false():
    """full_production_clone_verified must be False unless real verification exists."""
    result = get_google_cloud_proof()
    assert result["cloud_sql"]["full_production_clone_verified"] is False


def test_cloud_sql_role():
    result = get_google_cloud_proof()
    assert result["cloud_sql"]["role"] == "selected evidence mirror"


def test_no_external_calls():
    result = get_google_cloud_proof()
    assert result["proof_endpoint_external_calls"] is False


def test_safe_claims_present():
    result = get_google_cloud_proof()
    claims = result["safe_claims"]
    assert any("Cloud Run" in c for c in claims)
    assert any("Artifact Registry" in c for c in claims)
    assert any("Secret Manager" in c for c in claims)
    assert any("Gemini" in c for c in claims)


def test_non_claims_no_autonomous_trading():
    result = get_google_cloud_proof()
    non_claims = result["non_claims"]
    assert any("autonomous trading" in nc.lower() for nc in non_claims)


def test_non_claims_no_investment_advice():
    result = get_google_cloud_proof()
    non_claims = result["non_claims"]
    assert any("investment advice" in nc.lower() for nc in non_claims)


def test_non_claims_no_alpha():
    result = get_google_cloud_proof()
    non_claims = result["non_claims"]
    assert any("alpha" in nc.lower() for nc in non_claims)


def test_gemini_provider():
    result = get_google_cloud_proof()
    assert result["gemini"]["provider"] == "Gemini API"


def test_detects_cloud_run_when_env_set(monkeypatch):
    monkeypatch.setenv("K_SERVICE", "pantheon-gemini")
    monkeypatch.setenv("K_REVISION", "pantheon-gemini-00001-abc")
    result = get_google_cloud_proof()
    assert result["runtime_detected"] is True
    assert result["service"] == "pantheon-gemini"


def test_detects_non_cloud_run(monkeypatch):
    monkeypatch.delenv("K_SERVICE", raising=False)
    monkeypatch.delenv("K_REVISION", raising=False)
    result = get_google_cloud_proof()
    assert result["runtime_detected"] is False
    assert result["service"] == "pantheon-gemini"  # fallback name


def test_gemini_credential_detection(monkeypatch):
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)
    result = get_google_cloud_proof()
    assert result["gemini"]["credential_configured"] is False

    monkeypatch.setenv("GEMINI_API_KEY", "AIzaSyDummy12345")
    result = get_google_cloud_proof()
    assert result["gemini"]["credential_configured"] is True
