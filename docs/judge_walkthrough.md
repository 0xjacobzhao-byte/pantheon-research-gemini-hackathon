# Judge Walkthrough

A 10-minute path through this repository for a human judge or an AI reviewer.
Everything here runs **offline with no secrets**; live mode is optional.

---

## 1. What to inspect first

| Priority | File | Why it matters |
|----------|------|----------------|
| 1 | [`backend/app/gemini_overlay.py`](../backend/app/gemini_overlay.py) | Gemini API integration (fail-closed). Missing key → `BLOCKED_BY_MISSING_CREDENTIAL`, bad JSON → `PARSE_ERROR`. |
| 2 | [`backend/app/qwen_overlay.py`](../backend/app/qwen_overlay.py) | Qwen Cloud (DashScope) integration. Same fail-closed contract. |
| 3 | [`backend/app/comparison.py`](../backend/app/comparison.py) | Dual-model comparison engine: `data_state` derivation, agreement scoring, divergence, human-review gate. |
| 4 | [`frontend/src/components/equity/OverlayComparisonPanel.tsx`](../frontend/src/components/equity/OverlayComparisonPanel.tsx) | Product-grade Qwen-vs-DeepSeek UI with fail-closed states. |
| 5 | [`backend/app/evidence_pack.py`](../backend/app/evidence_pack.py) | Provenance-committed evidence pack (content hash). |
| 6 | [`backend/app/data_quality.py`](../backend/app/data_quality.py) | Public-safe Research-Ops / governance slice. |
| 7 | [`backend/app/sample_modules.py`](../backend/app/sample_modules.py) | Module snapshot grid — full multi-asset scope (Macro/TA/FICC/Equity) with honest per-module state. See [`module_snapshots.md`](module_snapshots.md). |

## 2. How to run locally (offline, no secrets)

```bash
git clone https://github.com/0xjacobzhao-byte/pantheon-research-gemini-hackathon
cd pantheon-research-gemini-hackathon
docker compose up --build
# Frontend: http://localhost:5173   Backend: http://localhost:8000/docs
```

Or without Docker:

```bash
cd backend && pip install -r requirements.txt && uvicorn main:app --port 8000
# in another shell:
cd frontend && npm ci && npm run dev
```

## 3. How to run the judge smoke test

```bash
# with the backend running on :8000
./scripts/judge_smoke.sh
```

It exercises health, the evidence-pack hash, both overlays, the comparison
`data_state`, the data-quality panel, and the Gemini proof/overlay endpoints —
all offline, no secrets (`ALL GREEN`).

## 4. How to inspect the Qwen integration code

- Base URL, model, auth: [`backend/app/qwen_overlay.py`](../backend/app/qwen_overlay.py) (`QWEN_BASE_URL`, `QWEN_MODEL`).
- OpenAI-compatible chat completion call via `httpx`, bounded retry/backoff.
- Fail-closed statuses in [`backend/app/models.py`](../backend/app/models.py) (`OverlayStatus`).
- Tests: [`backend/tests/test_qwen_fail_closed.py`](../backend/tests/test_qwen_fail_closed.py).

## 5. How to inspect the product UI

- Component: [`OverlayComparisonPanel.tsx`](../frontend/src/components/equity/OverlayComparisonPanel.tsx)
  (provider cards, agreement, divergences, evidence gaps, human-review gate,
  `data_state` badge, latency/model metadata, fail-closed states).
- Governance panel: [`DataQualityPanel.tsx`](../frontend/src/components/DataQualityPanel.tsx).
- Component tests (jsdom): [`OverlayComparisonPanel.test.tsx`](../frontend/src/components/equity/OverlayComparisonPanel.test.tsx).

## 6. What is included vs excluded

**Included (sanitized vertical slice):** Gemini overlay + proof, dual-LLM
(Qwen/DeepSeek) overlay + comparison engine, evidence pack with content hash,
mini Research-Ops / data quality, forward-validation methodology, redacted
traces, product UI, tests, CI.

**Excluded (stays in the private production repo):** provider credentials, the
production database and its data, the full admin plane, broker/trading logic,
proprietary raw datasets, the multi-asset (crypto/macro/FICC) engines, and the
production research universe.

## 7. Safe claims and non-claims

**Safe claims**
- Qwen is called live via Alibaba Cloud DashScope when live mode is enabled.
- No secrets are committed or returned; proof endpoints make no external calls.
- Offline mode runs the full flow with bundled samples.
- LLMs never execute trades — every signal passes a human-review gate.

**Non-claims**
- No alpha/performance claim — forward validation is required first
  (see [`docs/validation_methodology.md`](validation_methodology.md)).
- This repo is not the full production system.
