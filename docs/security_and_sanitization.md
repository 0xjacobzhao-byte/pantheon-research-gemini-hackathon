# Security & Sanitization

How this public repository is kept safe to publish and honest to judges.

Snapshot date: **2026-08-14**.

---

## 1. What is public

This repository is a **sanitized, judge-runnable verification slice** of the
Pantheon Research production system:

| Area | What is here |
|---|---|
| `backend/` | FastAPI app: Gemini overlay + proof endpoints, Qwen/DeepSeek comparison overlays, evidence-pack provenance hashing, comparison engine, Research-Ops / data-quality slice, module snapshots, ticker profiles, validation timeline |
| `frontend/` | React + TypeScript demo UI: Gemini integration panel, overlay comparison, data quality, module grid, provider health, mini panels |
| `production_reference/` | Five **sanitized production source files** copied from the private repo for judge verification |
| `data/` | Sanitized sample evidence packs and clearly-labelled redacted traces |
| `docs/`, `scripts/`, `assets/` | Judge-facing documentation, the smoke script, architecture diagrams |

---

## 2. What remains private

The [private production repository](https://github.com/0xjacobzhao-byte/Pantheon-Research)
is closed-source and contains the complete system. **Never published:**

- Proprietary strategy formulas, thresholds, weights, and scoring engines
  (Macro / Equity / BTC / ETH / DeFi / FICC)
- Full valuation and fair-value models
- Private provider adapters, routing, and model-registry configuration
- Broker execution implementation
- Production Agent Treasury admin implementation
- Full Alembic migration history (reveals production schema and data topology)
- Internal production runbooks and operational security topology
- The production database, its rows, and the full research universe
- Any customer or user data

**Judges may request temporary read-only access** if competition rules allow.

---

## 3. `production_reference/` sanitization policy

Five files were selected because each makes a specific architectural claim
**checkable**, and because each could be published without releasing strategy IP.

Every file carries a provenance header naming its private source and snapshot
date. **None opens a network connection, reads a credential, touches a database,
or executes a trade.**

| File | Sanitization applied |
|---|---|
| `evidence_tier.py` | Published unchanged below the header — pure stdlib, deterministic, grades *evidence quality* not securities |
| `advice_policy.py` | Published unchanged below the header — stdlib only; publishing the AI boundary is the point |
| `overlayComparison.ts` | Deployment-target references removed; two internal imports replaced with local declarations so the file reads standalone |
| `freshness_policy.py` | **Substantially sanitized** — upstream provider names and routing, credential environment-variable names, hosting/database topology, internal runbook paths, internal PR references, and live coverage statistics all removed |
| `valuation_outlier_review_service.py` | Published unchanged below the header; the calibration-pack **artifact** it reads is **not** published — only the reader |

Selection criteria and the full rejection list (with reasons) are documented in
[`production_reference/README.md`](../production_reference/README.md).

Publishing these files is a **deliberate Apache-2.0 release decision**, reviewed
for secrets, customer data, operational topology, and strategy IP.

---

## 4. What sample data is included

| Path | Contents |
|---|---|
| `data/sample_equity_evidence_{ma,nvda}.json` | Sanitized quantitative evidence packs |
| `data/gemini_samples/*.json` | Bundled Gemini overlays served as `OFFLINE_SAMPLE` |
| `data/sample_{qwen,deepseek}_output_*.json` | Bundled comparison-provider overlays |
| `data/redacted_traces/*` | Clearly-labelled redacted illustrative traces |
| `data/judge_proof_bundle.json`, `data/ticker_profiles.json` | Public-safe demo fixtures |

The Gemini sample fixtures record the model that **actually produced them**
(`gemini-2.0-flash`) and carry a `model_note` disclosing that the live path uses
`gemini-2.5-flash`. A historical capture is provenance — relabelling it to match
current docs would falsify evidence, so it was not relabelled.

---

## 5. What credentials are excluded

**Never included:** API keys, access tokens, cookies, private keys, seed phrases
or mnemonics, database credentials or connection strings, cloud service-account
credentials, `.env` files, production environment files, database dumps, user
records, admin tokens, broker/trading credentials, Circle credentials or OTP/CLI
session data, internal RPC URLs, or private provider contracts.

Only `.env.example` is committed, and **every value in it is empty**.

---

## 6. Offline-mode behavior

- **Default mode is offline** — the full demo runs with **no secrets**.
- Provider overlays return `OFFLINE_SAMPLE` from bundled data; no live call is
  claimed when none was made.
- Live mode is gated behind `DEMO_MODE=live` plus provider keys supplied via
  environment variables that **no endpoint ever returns**.
- Fail-closed states are explicit and distinct: `BLOCKED_BY_MISSING_CREDENTIAL`
  (no key), `API_ERROR` (upstream failure), `PARSE_ERROR` (non-JSON model
  output). **Never a hollow SUCCESS.**
- Proof endpoints (`/api/proof/gemini`, `/api/proof/google-cloud`,
  `/api/proof/gcp`) make **no external calls** and report credential state as
  **booleans only**.

---

## 7. Production / public separation

| Lane | Role | Writes |
|---|---|---|
| Vercel + Railway | Primary production path | Railway is the **only** canonical writer |
| Google Cloud Run (`pantheon-gemini`) | Live Gemini verification lane | **None** — no canonical writes, no Cloud SQL, no production scheduler |
| Local Docker Compose | Offline judge demo | **None** — no credentials required |

The Gemini lane is a real deployed environment, but it has **no path to
production data or the production portfolio**. See the deployment diagram in
[README § Deployment Architecture](../README.md#deployment-architecture).

---

## 8. Secret-scan methodology

Before every push, scan the working tree for high-signal patterns:

```bash
grep -rEn --binary-files=without-match \
  --exclude-dir=.git --exclude-dir=node_modules --exclude-dir=.venv \
  --exclude-dir=dist --exclude='*.example' \
  'sk-[A-Za-z0-9]{20,}|AKIA[0-9A-Z]{16}|LTAI[A-Za-z0-9]{12,}|-----BEGIN [A-Z ]*PRIVATE KEY-----|postgres(ql)?://[^[:space:]]+:[^[:space:]]+@|ghp_[A-Za-z0-9]{30,}|xox[baprs]-[A-Za-z0-9-]+|AIza[A-Za-z0-9_-]{30,}' .

# No real .env may be tracked
git ls-files | grep -E '(^|/)\.env$' && echo "FAIL" || echo "OK: no committed .env"
```

CI additionally runs a `secret-scan-lite` job on every push and PR to `main`.
Full-history scanning is performed with `gitleaks` before submission milestones.

**Known benign matches.** Two patterns recur and are *not* secrets: a literal
`AIzaSyDummy12345` test fixture asserting credential-*detection* logic, and the
public USDC token contract address on Base (`0x8335…2913`). Scanner regexes in
the test suite and in `judge_smoke.sh` also match their own patterns by design.

---

## 9. Financial safety boundary

- **No autonomous trade execution.** The product produces research artifacts; it
  does not place orders. There is no order path, no broker credential, and no
  signing key anywhere in this repository or its deployments.
- **No performance, return, AUM, revenue, or user claims.** Hackathon-period
  revenue is **$0.00**, verified external users **0**, paying users **0**.
- **LLM output is informational research, not investment advice.**
- **Missing or unusable data fails closed**; humans retain final judgment.
- The Circle payment rail is **structurally separate** from any order path, and
  payment is **not an agent-invocable tool** — prompt injection has no path to
  money.

---

## 10. Related documents

- [`SUBMISSION_SCOPE.md`](SUBMISSION_SCOPE.md) — pre-existing vs hackathon work
- [`PRODUCT_EVIDENCE_INDEX.md`](PRODUCT_EVIDENCE_INDEX.md) — claim → evidence map
- [`data_safety.md`](data_safety.md) — data exclusion policy
- [`safe_claims.md`](safe_claims.md) — the claims / non-claims ledger
- [`production_reference/README.md`](../production_reference/README.md) — what was published and what was rejected
