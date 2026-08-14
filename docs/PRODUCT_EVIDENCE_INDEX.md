# Product Evidence Index

> The canonical map from **claim → evidence**. A judge should be able to verify
> this submission from this one page without exploring dozens of files.

Snapshot date: **2026-08-14**.

**Status vocabulary:** `LIVE` (in production) · `PROOF` (verified deployment or
transaction, not a production writer) · `BETA` (controlled rollout) ·
`INTERNAL` (operator-gated) · `STAGED` (built, fail-closed, not enabled).

**Legend:** ✅ verifiable by a judge with no credentials · 🔒 requires private
access · 🌐 requires the live product.

---

## A. Core product and architecture

| Capability | Status | Public evidence | Live evidence | Representative source | Limitations |
|---|---|---|---|---|---|
| **Live product** | LIVE | [README §1](../README.md#1-what-pantheon-research-is) | ✅ [pantheon-research.com](https://pantheon-research.com) | 🔒 private repo | Public surfaces are free; Pro delivery is controlled beta |
| **Seven-layer architecture** | LIVE | [README §5](../README.md#5-high-level-architecture) · [architecture_diagram.md](architecture_diagram.md) | 🌐 dashboard | 🔒 private repo | Layer 7 (execution) is staged and fail-closed, not live |
| **Submission scope boundary** | — | ✅ [SUBMISSION_SCOPE.md](SUBMISSION_SCOPE.md) | — | commit history | Pantheon predates the hackathon; boundary is documented, not hidden |
| **Public/private repo split** | — | ✅ [README §3](../README.md#3-repository-scope) | — | [`production_reference/`](../production_reference/) | Public repo is a sanitized slice, not the production codebase |

---

## B. Gemini and Google Cloud

| Capability | Status | Public evidence | Live evidence | Representative source | Limitations |
|---|---|---|---|---|---|
| **Gemini API integration** | PROOF | [gemini_production_evidence.md](gemini_production_evidence.md) | ✅ [`/api/proof/gemini`](https://pantheon-gemini-549837878368.asia-southeast1.run.app/api/proof/gemini) | [`backend/app/gemini_overlay.py`](../backend/app/gemini_overlay.py) | `gemini-2.5-flash`; local demo defaults to offline samples |
| **Gemini structured output** | PROOF | [gemini samples](../data/gemini_samples/) | ✅ [`/api/overlay/gemini/NVDA`](https://pantheon-gemini-549837878368.asia-southeast1.run.app/api/overlay/gemini/NVDA) | [`backend/app/gemini_overlay.py`](../backend/app/gemini_overlay.py) | JSON response mode; schema `overlay-assessment-1.0` |
| **Gemini fail-closed behavior** | PROOF | [gemini_production_evidence.md](gemini_production_evidence.md#fail-closed-behavior-live-mode) | ✅ run `./scripts/judge_smoke.sh` | [`backend/tests/test_gemini_overlay.py`](../backend/tests/test_gemini_overlay.py) | Three distinct states; never a hollow SUCCESS |
| **Live Gemini API call verified** | PROOF | ✅ [`data/gemini_live_call_redacted.json`](../data/gemini_live_call_redacted.json) | ✅ Cloud Run live mode | commit `d031d14` | Redacted artifact; key never published |
| **Google Cloud Run deployment** | PROOF | [gemini_production_evidence.md](gemini_production_evidence.md#google-cloud-run-deployment-live) | ✅ [`/api/proof/google-cloud`](https://pantheon-gemini-549837878368.asia-southeast1.run.app/api/proof/google-cloud) | [`scripts/deploy_gcp.sh`](../scripts/deploy_gcp.sh) | Shadow / proof deployment — **not** the production writer |
| **Artifact Registry** | PROOF | proof endpoint `artifact_registry: true` | ✅ same endpoint | [`backend/Dockerfile`](../backend/Dockerfile) | Image storage only |
| **Secret Manager** | PROOF | proof endpoint `secret_manager_used: true` | ✅ same endpoint | [`scripts/deploy_gcp.sh`](../scripts/deploy_gcp.sh) | Key bound via `--set-secrets`; never in the repo |
| **Cloud Logging** | PROOF | proof endpoint `cloud_logging_used: true` | ✅ same endpoint | — | Automatic Cloud Run request logging |
| **Cloud SQL** | NOT USED | proof endpoint `cloud_sql.configured: false` | ✅ same endpoint | — | **Explicitly not claimed** — no production DB migration |

---

## C. Multi-model AI and evidence governance

| Capability | Status | Public evidence | Live evidence | Representative source | Limitations |
|---|---|---|---|---|---|
| **Five-model stack** (Claude · ChatGPT · Gemini · DeepSeek · Qwen) | LIVE | [README §8](../README.md#8-deterministic-research--multi-model-ai) | 🌐 AI Analyst Consensus | ✅ [`production_reference/overlayComparison.ts`](../production_reference/overlayComparison.ts) | Four providers pre-existed; **Gemini is the hackathon addition** |
| **Multi-model comparison** | LIVE | ✅ [`/api/comparison/{ticker}`](../backend/app/comparison.py) (local) | 🌐 Ticker Profile | ✅ [`production_reference/overlayComparison.ts`](../production_reference/overlayComparison.ts) | Public demo compares a subset; production compares five |
| **Disagreement surfaced, not averaged** | LIVE | [README §8](../README.md#8-deterministic-research--multi-model-ai) | 🌐 model-comparison panel | ✅ `overlayComparison.ts` — `MajorDivergence`, `AgreementSummary` | Divergence is a review trigger, not an error state |
| **Evidence provenance** | LIVE | ✅ [`/api/evidence/{ticker}`](../backend/app/evidence_pack.py) — SHA-256 | 🌐 evidence panel | [`backend/app/evidence_pack.py`](../backend/app/evidence_pack.py) | Hash binds pack to overlay output |
| **Evidence-backed vs AI-prior separation** | LIVE | [README §8](../README.md#two-explicitly-separated-lanes) | 🌐 lane labels on overlays | ✅ [`production_reference/evidence_tier.py`](../production_reference/evidence_tier.py) | Five graded tiers; an AI prior can never present as source-backed |
| **Schema validation before serving** | LIVE | [architecture.md](architecture.md) | — | ✅ `evidence_tier.py` (post-validation contract) | Payload validated before tiering; tier never re-grades the LLM |
| **Data quality / freshness governance** | LIVE | ✅ [`/api/data-quality`](../backend/app/data_quality.py) (local) | 🌐 Research Ops | ✅ [`production_reference/freshness_policy.py`](../production_reference/freshness_policy.py) | Soft/hard TTL per module; paused modules excluded from confidence |
| **Provider health** | LIVE | ✅ [`/api/provider-health`](../backend/app/provider_health.py) (local) | 🌐 Research Ops | 🔒 private repo | Operator-gated in production |

---

## D. Research surfaces

| Capability | Status | Public evidence | Live evidence | Representative source | Limitations |
|---|---|---|---|---|---|
| **Ticker Profile** | LIVE | [module_snapshots.md](module_snapshots.md) | 🌐 live product (GOOGL and broad universe) | 🔒 private repo | Local demo serves **MA / NVDA only** — not faked to match screenshots |
| **Equity Decisions** | LIVE | [README §10](../README.md#10-product-surfaces) | 🌐 live product | 🔒 private repo | Research context; not investment advice |
| **AI Analyst Consensus** | LIVE (cache-only) | [README §10](../README.md#10-product-surfaces) | 🌐 live product | ✅ `overlayComparison.ts` | Cache-only — overlays are not regenerated per page view |
| **LLM Research Summary** | LIVE | [README §10](../README.md#10-product-surfaces) | 🌐 live product | ✅ `overlayComparison.ts` (summary contract) | Labelled by support level: evidence-backed / mixed / AI-prior |
| **Macro framework** | LIVE | ✅ [`/api/modules`](../backend/app/mini_panels.py) (local) | 🌐 live product | 🔒 private repo | Regime classification; proprietary scoring not published |
| **BTC framework** | LIVE | ✅ [`/api/modules`](../backend/app/mini_panels.py) (local) | 🌐 live product | 🔒 private repo | Most mature public validation track |
| **Human / valuation review** | INTERNAL | — | 🌐 Research Ops (operator) | ✅ [`production_reference/valuation_outlier_review_service.py`](../production_reference/valuation_outlier_review_service.py) | Read-only; changes no rating, FV, or recommendation |

---

## E. Signal, agent, and delivery

| Capability | Status | Public evidence | Live evidence | Representative source | Limitations |
|---|---|---|---|---|---|
| **Signal / alert delivery** | INTERNAL (dry-run default) | [README §10](../README.md#10-product-surfaces) | — | ✅ [`production_reference/freshness_policy.py`](../production_reference/freshness_policy.py) (alert-module TTL registry) | Fail-closed; dry-run by default |
| **Telegram Agent** | BETA | [README §10](../README.md#10-product-surfaces) | 🌐 account linking in product | ✅ [`production_reference/advice_policy.py`](../production_reference/advice_policy.py) | Pro-gated per-user delivery; controlled beta |
| **Weekly automated reports** | BETA | [README §10](../README.md#10-product-surfaces) | 🌐 email delivery | 🔒 private repo | Controlled beta, fail-closed by default |
| **Advice vs execution boundary** | LIVE | ✅ [README §9](../README.md#9-what-ai-actually-does) | — | ✅ [`production_reference/advice_policy.py`](../production_reference/advice_policy.py) | Advice ALLOWED, execution NOT AUTHORIZED — enforced in code |
| **Human-in-the-loop boundary** | LIVE | ✅ [README §16](../README.md#16-safety--non-claims) · [safe_claims.md](safe_claims.md) | — | ✅ `advice_policy.py` · `valuation_outlier_review_service.py` | No order path, no broker credential, no signing key |

---

## F. Validation

| Capability | Status | Public evidence | Live evidence | Representative source | Limitations |
|---|---|---|---|---|---|
| **Backtest infrastructure** | LIVE | [validation_methodology.md](validation_methodology.md) | 🌐 framework pages | 🔒 private repo | A backtest alone supports **no** performance claim |
| **Forward validation** | LIVE | [validation_methodology.md](validation_methodology.md) · [README §13](../README.md#13-validation) | 🌐 validation surfaces | [`backend/app/validation_timeline.py`](../backend/app/validation_timeline.py) | Maturity varies by market; equities still accumulating samples |
| **Matured outcomes** | PARTIAL | [README §13](../README.md#13-validation) | 🌐 BTC track | 🔒 private repo | **No validated-alpha claim is made anywhere in this submission** |
| **Point-in-time discipline** | LIVE | [validation_methodology.md](validation_methodology.md) | — | 🔒 private repo | Reconstructed history carries declared survivorship limitations |

---

## G. Commercial and agentic economy

| Capability | Status | Public evidence | Live evidence | Representative source | Limitations |
|---|---|---|---|---|---|
| **Circle Agent Wallet payment** | PROOF | ✅ [circle_agentic_economy_evidence.md](circle_agentic_economy_evidence.md) · [redacted artifact](../data/circle_agentic_payment_proof_redacted.json) | ✅ [BaseScan tx](https://basescan.org/tx/0x699bbb9ddb03f9a98525749374fb976a9cd7ef6319414d1cb5e422d810eac6e3) | — | Founder-funded, operator-mediated, **not autonomous**; read the ERC-20 Transfer log, not top-level From/To |
| **Circle spending policy** | PROOF | [circle evidence §4](circle_agentic_economy_evidence.md) | — | — | Operator-observed CLI read-back, **not** cryptographically proven |
| **Production Agent Treasury** | STAGED | [circle evidence §5](circle_agentic_economy_evidence.md) | — | 🔒 private repo | Exists separately; **the final proof did not exercise it** |
| **P&L evidence** | — | ✅ [business_model_and_pnl.md](business_model_and_pnl.md) | — | — | Revenue **$0**, users **0**, paying users **0**, net **−$926.12** |
| **Business model** | — | ✅ [README §15](../README.md#15-business-model) · [business_model_and_pnl.md](business_model_and_pnl.md) | — | — | Projections are clearly separated from actuals |

---

## H. Deployment

| Capability | Status | Public evidence | Live evidence | Representative source | Limitations |
|---|---|---|---|---|---|
| **Primary production** (Vercel + Railway) | LIVE | [README §14](../README.md#14-deployment-architecture) | ✅ [pantheon-research.com](https://pantheon-research.com) | 🔒 private repo | The **only** canonical writer |
| **GCP Gemini shadow** | PROOF | [gemini_production_evidence.md](gemini_production_evidence.md) | ✅ [Cloud Run health](https://pantheon-gemini-549837878368.asia-southeast1.run.app/health) | [`scripts/deploy_gcp.sh`](../scripts/deploy_gcp.sh) | Fail-closed OFF for writes and schedulers |

**Not claimed:** three simultaneous production writers, active-active
replication, automatic cross-cloud failover, or a full production database clone.

---

## I. How to verify without private access

Everything marked ✅ above requires no credentials. The shortest complete path:

```bash
# 1. Live Gemini + Google Cloud proof (no clone needed)
curl -s https://pantheon-gemini-549837878368.asia-southeast1.run.app/api/proof/gemini      | jq
curl -s https://pantheon-gemini-549837878368.asia-southeast1.run.app/api/proof/google-cloud | jq
curl -s https://pantheon-gemini-549837878368.asia-southeast1.run.app/api/overlay/gemini/NVDA | jq

# 2. Local end-to-end, offline, no API keys
git clone https://github.com/0xjacobzhao-byte/pantheon-research-gemini-hackathon
cd pantheon-research-gemini-hackathon
docker compose up --build
./scripts/judge_smoke.sh

# 3. Circle payment — public chain data only, no Pantheon dependency
curl -s -X POST <ANY_BASE_RPC_URL> -H 'Content-Type: application/json' -d '{
  "jsonrpc":"2.0","id":1,"method":"eth_getTransactionReceipt",
  "params":["0x699bbb9ddb03f9a98525749374fb976a9cd7ef6319414d1cb5e422d810eac6e3"]
}' | jq '{status: .result.status, block: .result.blockNumber}'
```

Then read [`production_reference/`](../production_reference/) for representative
production source, and [`SUBMISSION_SCOPE.md`](SUBMISSION_SCOPE.md) for what was
built when.

---

## J. Screenshots

Judge-facing product screenshots are published in the
[Devpost gallery](https://devpost.com/software/pantheon-research-qzn50k). The
naming contract and intended ordering for this repository are in
[`assets/submission/README.md`](../assets/submission/README.md).
