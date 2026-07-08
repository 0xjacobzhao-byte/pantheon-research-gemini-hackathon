"""Google Cloud Run deployment proof endpoint — secret-free.

Reports Cloud Run deployment metadata without exposing any secrets.
Safe for public-facing demo use.
"""

from __future__ import annotations

import os
import socket
from datetime import datetime, timezone


def get_gcp_proof() -> dict:
    """Return GCP Cloud Run deployment proof (no secrets, no external calls)."""
    # Cloud Run metadata (injected by platform)
    service = os.environ.get("K_SERVICE", "unknown")
    revision = os.environ.get("K_REVISION", "unknown")
    configuration = os.environ.get("K_CONFIGURATION", "unknown")
    port = os.environ.get("PORT", "unknown")
    region = os.environ.get("GOOGLE_CLOUD_REGION", "unknown")
    project = os.environ.get("GOOGLE_CLOUD_PROJECT", "unknown")

    # Detect if running on Cloud Run
    is_cloud_run = bool(os.environ.get("K_SERVICE"))

    # Hostname for container identification
    try:
        hostname = socket.gethostname()
    except Exception:
        hostname = "unknown"

    return {
        "schema_version": "gcp-proof-v1",
        "project": "Pantheon Research — Gemini Hackathon",
        "status": "ok",
        "cloud_provider": "Google Cloud",
        "deployment_platform": "Cloud Run",
        "deployment_detected": is_cloud_run,
        "service_name": service,
        "revision": revision,
        "configuration": configuration,
        "port": port,
        "hostname": hostname,
        "region": region,
        "gcp_project": project,
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "proof_endpoint_external_calls": False,
        "secrets_policy": "no keys, tokens, or URLs returned",
        "safe_claims": [
            "Backend deployed to Google Cloud Run (asia-southeast1).",
            "Container image stored in Google Artifact Registry.",
            "Gemini API key stored in Google Secret Manager (if configured).",
            "Cloud Run auto-scales from 0 to N instances based on traffic.",
            "This proof endpoint makes no external calls and returns no secrets.",
        ],
        "non_claims": [
            "Not claiming autonomous trading or model-generated alpha.",
            "Not claiming full production database migration.",
            "Not claiming investment performance or returns.",
            "Pantheon Research existed before the hackathon; the Gemini-powered "
            "analyst / risk-review layer is the new hackathon work.",
        ],
        "attestation": {
            "proof_endpoint_external_calls": False,
            "credential_values_returned": False,
            "cloud_run_metadata_detected": is_cloud_run,
        },
    }
