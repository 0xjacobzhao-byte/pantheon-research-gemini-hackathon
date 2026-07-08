# Product-Running Evidence — Gemini Hackathon

> This document provides reproducible evidence that the Pantheon Research Gemini Analyst product runs correctly.

## What Runs Locally

| Component | Command | URL |
|-----------|---------|-----|
| Backend (FastAPI) | `cd backend && uvicorn main:app --port 8000` | http://localhost:8000 |
| Frontend (React + Vite) | `cd frontend && npm run dev` | http://localhost:5173 |
| Full Stack (Docker) | `docker compose up --build` | frontend :5173 · backend :8000 |

## Gemini Proof Endpoint

Returns secret-free metadata confirming Gemini integration configuration. **Makes no external calls.**

```bash
curl -s http://localhost:8000/api/proof/gemini | jq
```

Expected output includes:
- `schema_version`: `"gemini-proof-v1"`
- `provider`: `"Google Gemini API"`
- `model`: `"gemini-2.0-flash"`
- `credential_configured`: `true` or `false`
- `proof_endpoint_external_calls`: `false`

## Gemini Overlay Endpoint

Returns a structured qualitative overlay for a given ticker. In offline mode (default), serves bundled samples.

```bash
curl -s http://localhost:8000/api/overlay/gemini/NVDA | jq
curl -s http://localhost:8000/api/overlay/gemini/MA | jq
```

Expected output includes:
- `provider`: `"gemini"`
- `status`: `"OFFLINE_SAMPLE"` (offline) or `"SUCCESS"` (live with key)
- `takeaway`: one-paragraph assessment
- `assessment.business_quality`, `moat`, `pricing_power`, `capital_allocation`, `red_flags`
- `assessment.confidence`: 0–1 float
- `assessment.missing_evidence`: list of identified gaps

## Offline Sample Mode (Default)

No API key required. Bundled samples in `data/gemini_samples/`:
- `nvda_gemini_overlay.json` — NVIDIA assessment
- `ma_gemini_overlay.json` — Mastercard assessment

## Live Mode

Set environment variables for live Gemini API calls:

```bash
export DEMO_MODE=live
export GEMINI_API_KEY=<your-key>   # or GOOGLE_API_KEY
```

Then the overlay endpoint calls the Google Generative Language API directly.

### Fail-Closed Behavior (Live Mode)

| Condition | Status | Evidence |
|-----------|--------|----------|
| No API key | `BLOCKED_BY_MISSING_CREDENTIAL` | `test_gemini_missing_credential_fails_closed` |
| API error | `API_ERROR` | Retry with backoff, then report |
| Non-JSON response | `PARSE_ERROR` | `test_gemini_invalid_json_raises_parse_error` |

## Phase 1 Test Results

```
Backend tests:  100 passed
Frontend tests: 11 passed (including 2 Gemini-specific)
Frontend build: success (tsc + vite)
Secret scan:    clean (no API keys, tokens, or credentials)
```

### Gemini-Specific Tests (16 tests)

| Test | Status |
|------|--------|
| `test_gemini_missing_credential_fails_closed` | PASS |
| `test_gemini_invalid_json_raises_parse_error` | PASS |
| `test_gemini_fenced_json_still_parses` | PASS |
| `test_gemini_offline_sample_works` | PASS |
| `test_gemini_offline_sample_ma` | PASS |
| `test_gemini_missing_sample_is_error` | PASS |
| `test_gemini_overlay_carries_prompt_and_schema_version` | PASS |
| `test_gemini_check_credential` | PASS |
| `test_gemini_proof_returns_correct_schema` | PASS |
| `test_gemini_proof_no_secrets` | PASS |
| `test_gemini_proof_credential_detected` | PASS |
| `test_gemini_proof_google_api_key_detected` | PASS |
| `test_gemini_proof_demo_mode` | PASS |
| `test_gemini_proof_safe_claims_present` | PASS |
| `test_gemini_proof_implementation_path` | PASS |
| `test_gemini_proof_attestation` | PASS |

## Reproducible Smoke Test

```bash
# Start the backend
cd backend && uvicorn main:app --port 8000 &

# Run smoke checks
curl -s http://localhost:8000/health | jq
curl -s http://localhost:8000/api/proof/gemini | jq
curl -s http://localhost:8000/api/overlay/gemini/NVDA | jq
curl -s http://localhost:8000/api/overlay/gemini/MA | jq
```

## Implementation Files

| File | Purpose |
|------|---------|
| [`backend/app/gemini_overlay.py`](../backend/app/gemini_overlay.py) | Gemini API call implementation |
| [`backend/app/gemini_proof.py`](../backend/app/gemini_proof.py) | Secret-free proof endpoint |
| [`backend/tests/test_gemini_overlay.py`](../backend/tests/test_gemini_overlay.py) | Overlay fail-closed tests |
| [`backend/tests/test_gemini_proof.py`](../backend/tests/test_gemini_proof.py) | Proof endpoint tests |
| [`data/gemini_samples/`](../data/gemini_samples/) | Bundled offline samples |
| [`frontend/src/components/GeminiOverlayPanel.tsx`](../frontend/src/components/GeminiOverlayPanel.tsx) | UI panel component |

## Safe Claims

- Gemini overlay uses Google Generative Language API (v1beta)
- Actual Gemini API call is in `backend/app/gemini_overlay.py`
- Default mode is offline — no API key required for demo
- Fail-closed: three explicit failure modes, never fake success
- Proof endpoint makes no external calls and returns no secrets
- 100 backend tests pass, 11 frontend tests pass

## Non-Claims

- Not claiming autonomous trading or model-generated alpha
- Not claiming investment performance or returns
- Not exposing private production strategy code
- Pantheon Research existed before the hackathon; the Gemini-powered analyst layer is the new hackathon work


## Google Cloud Run Deployment (Live)

**Service URL:** https://pantheon-gemini-rgxoubvsiq-as.a.run.app

**Deployed:** 2026-07-08, asia-southeast1 region

**Infrastructure:**
- Google Cloud Run (managed, auto-scaling 0-3 instances)
- Google Artifact Registry (container image storage)
- Google Secret Manager (available for Gemini API key)
- Cloud Logging (request/response logging)

**Endpoints verified (all HTTP 200):**
- `GET /health` — healthy, offline mode, tickers: MA, NVDA
- `GET /api/proof/gemini` — schema_version: gemini-proof-v1, no secrets
- `GET /api/proof/gcp` — deployment_detected: true, Cloud Run metadata confirmed
- `GET /api/overlay/gemini/NVDA` — OFFLINE_SAMPLE with full 7-field assessment
- `GET /api/evidence/NVDA` — evidence pack with SHA-256 provenance hash
- `GET /api/comparison/MA` — dual-provider comparison, MEDIUM agreement

**Reproduce:**
```bash
curl -s https://pantheon-gemini-rgxoubvsiq-as.a.run.app/health | jq
curl -s https://pantheon-gemini-rgxoubvsiq-as.a.run.app/api/proof/gemini | jq
curl -s https://pantheon-gemini-rgxoubvsiq-as.a.run.app/api/proof/gcp | jq
curl -s https://pantheon-gemini-rgxoubvsiq-as.a.run.app/api/overlay/gemini/NVDA | jq
```

**No secrets exposed:** verified via grep scan on all proof and overlay responses.
