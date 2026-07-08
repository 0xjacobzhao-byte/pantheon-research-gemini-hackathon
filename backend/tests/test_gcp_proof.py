"""Tests for the GCP Cloud Run proof endpoint."""

from __future__ import annotations

import json

import pytest

from app.gcp_proof import get_gcp_proof


def test_gcp_proof_returns_dict():
    proof = get_gcp_proof()
    assert isinstance(proof, dict)


def test_gcp_proof_schema_version():
    proof = get_gcp_proof()
    assert proof["schema_version"] == "gcp-proof-v1"


def test_gcp_proof_no_secrets():
    proof = get_gcp_proof()
    proof_str = json.dumps(proof)
    for pattern in ("AIza", "sk-proj-", "ghp_", "xoxb-", "postgres://user:"):
        assert pattern not in proof_str


def test_gcp_proof_no_external_calls():
    proof = get_gcp_proof()
    assert proof["proof_endpoint_external_calls"] is False


def test_gcp_proof_cloud_provider():
    proof = get_gcp_proof()
    assert proof["cloud_provider"] == "Google Cloud"
    assert proof["deployment_platform"] == "Cloud Run"


def test_gcp_proof_detects_non_cloud_run(monkeypatch):
    monkeypatch.delenv("K_SERVICE", raising=False)
    proof = get_gcp_proof()
    assert proof["deployment_detected"] is False


def test_gcp_proof_detects_cloud_run(monkeypatch):
    monkeypatch.setenv("K_SERVICE", "pantheon-gemini")
    monkeypatch.setenv("K_REVISION", "pantheon-gemini-00001")
    proof = get_gcp_proof()
    assert proof["deployment_detected"] is True
    assert proof["service_name"] == "pantheon-gemini"


def test_gcp_proof_attestation():
    proof = get_gcp_proof()
    att = proof["attestation"]
    assert att["proof_endpoint_external_calls"] is False
    assert att["credential_values_returned"] is False
