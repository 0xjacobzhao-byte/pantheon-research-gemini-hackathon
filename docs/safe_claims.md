# Safe Claims & Non-Claims

A single, explicit ledger of what this repository **does** and **does not**
claim — so judges (human or AI) never have to guess, and nothing here is an
overclaim.

## Safe claims (defensible, verifiable)

1. **Gemini is the hackathon analyst layer, and it runs live.** The
   `gemini-2.5-flash` integration is implemented in
   [`backend/app/gemini_overlay.py`](../backend/app/gemini_overlay.py) and is
   deployed on **Google Cloud Run** with Artifact Registry, Secret Manager, and
   Cloud Logging. A real live call was captured
   ([`data/gemini_live_call_redacted.json`](../data/gemini_live_call_redacted.json)),
   and the secret-free proof endpoints make **no external calls**:
   [`/api/proof/gemini`](https://pantheon-gemini-549837878368.asia-southeast1.run.app/api/proof/gemini)
   · [`/api/proof/google-cloud`](https://pantheon-gemini-549837878368.asia-southeast1.run.app/api/proof/google-cloud).
2. **Gemini is fail-closed.** Missing key → `BLOCKED_BY_MISSING_CREDENTIAL`;
   upstream failure → `API_ERROR`; non-JSON output → `PARSE_ERROR`. Never a
   hollow `SUCCESS`.
3. **Qwen and DeepSeek are called live** as **secondary comparison lanes** when
   live mode is enabled (`DEMO_MODE=live` + provider key), under the same
   fail-closed contract —
   [`qwen_overlay.py`](../backend/app/qwen_overlay.py) (Alibaba DashScope) and
   [`deepseek_overlay.py`](../backend/app/deepseek_overlay.py). The offline
   default runs on bundled samples and makes no external calls.
4. **Multi-model comparison is real.** Independent providers assess the same
   evidence pack; agreement / divergence / tone are computed, not assumed. Low
   agreement or major divergence routes to human review. Production runs five
   providers (Claude · ChatGPT · Gemini · DeepSeek · Qwen).
5. **Evidence is provenance-committed.** Each evidence pack is bound to a
   `sha256` content hash threaded through every comparison.
6. **The system is multi-asset.** Macro, Technical, FICC (FI/FX/Commodity), and
   Equity modules exist in production; the public repo surfaces their scope via a
   context-only module grid ([`module_snapshots.md`](module_snapshots.md)).
7. **Offline mode is fully functional** with bundled samples and **no secrets**.

## Non-claims (explicitly NOT asserted)

1. **No autonomous trading.** LLMs never execute trades; every signal passes a
   human-review gate.
2. **No alpha / performance claim.** The overlay is a tracked research signal, not
   an oracle; forward validation is required first
   ([`validation_methodology.md`](validation_methodology.md)).
3. **The context-only module cards are not live nowcasts.** Macro/TA/FICC cards
   are illustrative bundled snapshots; they carry no fair-value bands and no
   trading signals.
4. **No proprietary internals are published.** Market-data pipelines, scoring
   models, provider routing, the production database and its rows, the full
   universe, and the admin plane stay in the private repo.
5. **Live production numbers are withheld**, not fabricated — see
   [`qwen_coverage_report.md`](qwen_coverage_report.md).

## How to verify each claim

| Claim | Verify |
|-------|--------|
| Gemini runs on Google Cloud | [`/api/proof/google-cloud`](https://pantheon-gemini-549837878368.asia-southeast1.run.app/api/proof/google-cloud) → `secret_manager_used`, `artifact_registry`, `cloud_logging_used` |
| Gemini model + fail-closed | [`/api/proof/gemini`](https://pantheon-gemini-549837878368.asia-southeast1.run.app/api/proof/gemini) · `backend/tests/test_gemini_overlay.py` |
| Multi-model + fail-closed | `./scripts/judge_smoke.sh` · `backend/tests/test_qwen_fail_closed.py` |
| Evidence hashing | `GET /api/evidence/NVDA` → `provenance.evidence_hash` |
| Multi-asset scope | `GET /api/modules` · [`module_snapshots.md`](module_snapshots.md) |
| No secrets | CI `secret-scan-lite` job · [`security_and_sanitization.md`](security_and_sanitization.md) |

## Primary implementation files

| Provider | Implementation |
|---|---|
| **Gemini** (hackathon layer) | [`backend/app/gemini_overlay.py`](../backend/app/gemini_overlay.py) · [`gemini_proof.py`](../backend/app/gemini_proof.py) |
| Qwen (comparison) | [`backend/app/qwen_overlay.py`](../backend/app/qwen_overlay.py) |
| DeepSeek (comparison) | [`backend/app/deepseek_overlay.py`](../backend/app/deepseek_overlay.py) |
