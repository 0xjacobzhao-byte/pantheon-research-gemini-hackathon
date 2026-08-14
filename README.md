<div align="center">

# Pantheon Research

### Governed AI-native cross-asset investment research operating system

**Transforming governed market evidence into explainable research, signals,
model comparison, validation, and human-reviewed decisions.**

> **AI should not replace the investor. AI should compound the investor's discipline.**

```text
Wrong Strategy × AI = Faster Loss
Right Strategy × AI = Compounded Discipline
```

**[Live Product](https://pantheon-research.com)** ·
**[Devpost](https://devpost.com/software/pantheon-research-qzn50k)** ·
**[Gemini Cloud Run](https://pantheon-gemini-549837878368.asia-southeast1.run.app/health)** ·
**[Gemini Proof](https://pantheon-gemini-549837878368.asia-southeast1.run.app/api/proof/gemini)** ·
**[Circle Proof](https://basescan.org/tx/0x699bbb9ddb03f9a98525749374fb976a9cd7ef6319414d1cb5e422d810eac6e3)** ·
**[Architecture](#5-high-level-architecture)**

</div>

---

## Judge Quick Path

Eight steps, shortest path to verifying this submission. Steps 1–4 need nothing
but a browser.

| # | Step | Where |
|---|---|---|
| 1 | **Open the live product** | [pantheon-research.com](https://pantheon-research.com) |
| 2 | **Understand the seven-layer architecture** | [§5 below](#5-high-level-architecture) |
| 3 | **Inspect the Gemini analyst workflow** | [§11 below](#11-gemini-hackathon-integration) · [`backend/app/gemini_overlay.py`](backend/app/gemini_overlay.py) |
| 4 | **Verify the live Gemini / Google Cloud proof** | [`/api/proof/google-cloud`](https://pantheon-gemini-549837878368.asia-southeast1.run.app/api/proof/google-cloud) · [`/api/proof/gemini`](https://pantheon-gemini-549837878368.asia-southeast1.run.app/api/proof/gemini) |
| 5 | **Inspect representative production code** | [`production_reference/`](production_reference/) |
| 6 | **Verify the Circle Agent Wallet transaction** | [BaseScan](https://basescan.org/tx/0x699bbb9ddb03f9a98525749374fb976a9cd7ef6319414d1cb5e422d810eac6e3) — read the *ERC-20 Tokens Transferred* row, [why](#12-circle-agentic-economy) |
| 7 | **Review the public evidence index** | [`docs/PRODUCT_EVIDENCE_INDEX.md`](docs/PRODUCT_EVIDENCE_INDEX.md) |
| 8 | **Run the local judge demo** *(optional)* | [§17 below](#17-run-locally) — no API keys required |

**What was built during this hackathon vs. what pre-existed:**
[`docs/SUBMISSION_SCOPE.md`](docs/SUBMISSION_SCOPE.md). Read it before judging
scope — Pantheon predates this hackathon and says so.

---

## 1. What Pantheon Research Is

Pantheon Research is a **cross-asset research operating system** for investors,
analysts, and allocators who need disciplined, explainable decision support
across macro, equities, digital assets, and FICC — instead of a dozen
disconnected tools stitched together by hand.

The problem is not a lack of financial information. **The problem is the absence
of structured, governed, and explainable decision intelligence.** Raw data is
not a view, and a raw model opinion is not research. Pantheon sits between the
two.

Pantheon is deliberately **not**:

- ❌ a finance chatbot
- ❌ a raw-model opinion feed
- ❌ a collection of unrelated dashboards
- ❌ an automatic signal-to-order bot

**The Pantheon thesis:**

1. **Framework first.** Investment discipline precedes AI. Frameworks define what matters, what invalidates a view, and when the system must refuse to conclude.
2. **Data governed.** Every observation carries provenance, freshness, quality, and provider state — missing or stale data is labelled, never silently guessed.
3. **Deterministic before probabilistic.** Scores, regimes, and signals are computed deterministically and reproducibly before any AI interpretation.
4. **Signal is not a trade.** Research output, signal delivery, portfolio judgment, and execution are separate architectural concerns.
5. **Human remains portfolio manager.** AI compounds discipline; it does not remove accountability.

---

## 2. What Was Built During This Hackathon

**Pantheon Research existed before this hackathon.** Full boundary with commit,
transaction, and endpoint evidence: [`docs/SUBMISSION_SCOPE.md`](docs/SUBMISSION_SCOPE.md).

**Pre-existing:** the product, brand, live site, private production repository,
governed data platform, deterministic research engines, and the multi-provider
LLM research lane (Claude · ChatGPT · DeepSeek · Qwen).

**Built during the submission period:**

- **Gemini Analyst / Risk-Review layer** — evidence-pack workflow, fail-closed API path, structured overlay output *(2026-07-08)*
- **Google Cloud deployment** — Cloud Run, Artifact Registry, Secret Manager, Cloud Logging, live proof endpoints, verified live `gemini-2.5-flash` call *(2026-07-08)*
- **This judge-facing public repository** — runnable with no credentials
- **Circle Agent Wallet on-chain payment proof** — mainnet USDC, independently verifiable *(2026-08-11 → 2026-08-13)*
- **Submission evidence package** — evidence index, production references, documentation reconciliation

Gemini was added to a **pre-existing four-model lane** (Claude · ChatGPT ·
DeepSeek · Qwen), making the resulting stack five-model. That is stated so the
contribution can be weighted correctly rather than over- or under-credited.

---

## 3. Repository Scope

| | |
|---|---|
| **This public repo** | Sanitized submission / judge snapshot. Runnable Gemini vertical slice + representative production references. |
| **Private repo** | [Pantheon-Research](https://github.com/0xjacobzhao-byte/Pantheon-Research) — complete proprietary production source of truth. |

The private repository remains closed to protect proprietary strategy IP,
provider integrations, operational runbooks, and production data infrastructure.
Judges may request temporary private access from Jacob Zhao if competition rules
allow.

Everything under [`production_reference/`](production_reference/) is a
**deliberate public release decision** under Apache-2.0 — reviewed for secrets,
customer data, operational topology, and strategy IP before publication.

---

## 4. Submission Links

| | |
|---|---|
| 🌐 Live Product | https://pantheon-research.com |
| 📝 Devpost | https://devpost.com/software/pantheon-research-qzn50k |
| 💻 Public Repo | https://github.com/0xjacobzhao-byte/pantheon-research-gemini-hackathon |
| ☁️ Google Cloud Run | https://pantheon-gemini-549837878368.asia-southeast1.run.app |
| 🧭 Submission Scope | [docs/SUBMISSION_SCOPE.md](docs/SUBMISSION_SCOPE.md) |
| 🔎 Evidence Index | [docs/PRODUCT_EVIDENCE_INDEX.md](docs/PRODUCT_EVIDENCE_INDEX.md) |
| 📄 Gemini / GCP Evidence | [docs/gemini_production_evidence.md](docs/gemini_production_evidence.md) |
| 🔵 Circle Evidence | [docs/circle_agentic_economy_evidence.md](docs/circle_agentic_economy_evidence.md) |
| 📈 Business Model / P&L | [docs/business_model_and_pnl.md](docs/business_model_and_pnl.md) |
| 📖 Project Story | [docs/project_story.md](docs/project_story.md) |

---

## 5. High-Level Architecture

Pantheon spans **seven layers**:

| # | Layer | Role |
|---|---|---|
| 1 | **External Data Sources** | Macro/rates, equities, crypto/DeFi, social/alt data, positioning and market-structure feeds |
| 2 | **Governed Data Platform** | Ingestion scheduling, provider health, validation/normalization, canonical observations, derived and product snapshots, evidence artifacts, TTL/freshness, data-quality labelling |
| 3 | **Strategy / Research Engines** | Macro, Equity (US/CN/HK/SG), Crypto, DeFi, FICC, Technical Analysis, Narrative, Backtest/Validation |
| 4 | **Deterministic + Multi-Model AI Layer** | Deterministic value/risk models, factor regressions, signal engines — alongside a five-model LLM overlay (Source Pack → Prompt → Schema Validation → Overlay Comparison) |
| 5 | **Information Layer** | The Pantheon dashboard across all cross-asset modules |
| 6 | **Signal + Agent Layer** | User feed, research alerts, Telegram, LLM-assisted channels — behind a human-review gate |
| 7 | **Staged Trading / Execution Boundary** | An independently gated execution plane; manual today, no live autonomous trading |

End-to-end flow:

```text
Providers
  → Canonical Observations
  → Product Snapshots & Evidence Packs
  → Deterministic Research Engines
  → Gemini / Multi-Model Research
  → Signals & Human Review
  → Human Decision
  → Independently Gated Execution
```

The critical property: **layer 7 is not reachable from layer 4.** AI output
enters the signal layer as research, passes a human-review gate, and a human
makes the allocation decision. There is no code path from a model output to an
order.

---

## 6. Research Stack

| Domain | Primary Output | Status |
|---|---|---|
| Global Macro | Regime classification, exposure context | LIVE |
| US / CN / HK / SG Equities | Company research, valuation, model comparison | LIVE |
| Narrative / Capital Flow | Thematic and event-context research | LIVE |
| Technical Analysis | Multi-asset scans, regime and signal overlays | LIVE |
| Bitcoin | Cycle and risk stance | LIVE |
| Ethereum | Valuation stance with kill switches | LIVE |
| DeFi | Yield / risk verdicts | LIVE |
| Fixed Income · FX · Commodities | Cross-asset allocation and carry views | LIVE |
| Backtest / Forward Validation | Point-in-time validation infrastructure | LIVE |

Research surfaces are live; forward-return **validation maturity varies by
market** and is tracked separately — see [§13](#13-validation). Proprietary
scoring formulas are not published.

---

## 7. Governed Data Platform

Pantheon is database-first: research reads governed, point-in-time observations,
not ad-hoc API calls at request time.

```text
Providers / APIs / Filings / On-chain / Social
  → Ingestion + Provider Routing
  → Validation + Normalization
  → Canonical Observations
  → Derived Snapshots + Product Snapshots
  → Evidence Artifacts
  → Research Engines + Model Context
  → Dashboard / Alerts / APIs
```

| Capability | What it does | Why it matters |
|---|---|---|
| Canonical observations | Single normalized record per governed data point | One source of truth; reproducible research |
| Provider routing & fallback | Selects and fails over between providers | Resilience without silent gaps |
| Freshness / TTL policy | Soft and hard staleness thresholds per module | Stale data is labelled, never silently served |
| Data-quality labels | Marks quality and degradation per field | Fail-closed governance, never a silent guess |
| Derived & product snapshots | Pre-computed, frontline-ready payloads | Fast, consistent surfaces for engines and UI |
| Evidence artifacts | Structured, hashable evidence packs | Provenance a model output can be verified against |
| Provider health & Research Ops | Live view of provider config, coverage, per-ticker state | Operational trust in the research surface |

**Representative source:** [`production_reference/freshness_policy.py`](production_reference/freshness_policy.py)
— the real TTL / cadence / staleness registry.

---

## 8. Deterministic Research + Multi-Model AI

Pantheon draws a strict boundary between deterministic computation and LLM
interpretation.

**Deterministic engines own:** normalized inputs, scores, regimes, valuation
outputs, hard stops, signal candidates, reproducibility, audit trails.

**AI research modules own:** qualitative interpretation, contradiction
detection, model comparison, evidence-gap discovery, research synthesis, risk
explanation, verification-task generation.

Five LLM providers sit behind one common, schema-validated overlay pipeline. No
single vendor is a permanent architectural dependency.

| Provider | Role in the research overlay | Boundary |
|---|---|---|
| **Claude** | Qualitative overlay & risk reasoning | Reads governed evidence; never trades |
| **ChatGPT** | Qualitative overlay & comparison | Reads governed evidence; never trades |
| **Gemini** | Qualitative overlay (Google Cloud integration) | Reads governed evidence; never trades |
| **DeepSeek** | Qualitative overlay (production lane) | Reads governed evidence; never trades |
| **Qwen** | Qualitative overlay (Alibaba DashScope) | Reads governed evidence; never trades |

### Two explicitly separated lanes

| Lane | Meaning |
|---|---|
| **Evidence-backed** | Graded by an evidence tier computed from source-pack provenance |
| **Model-inferred / AI-prior** | Explicitly labelled model priors — never source-backed |

An AI prior can **never** masquerade as source-backed. Tier is computed from
source-pack metadata and factor mix only — the LLM payload is never re-graded by
the model that produced it.

**Disagreement is surfaced, not averaged away.** Model comparison reports
provider-level agreement, divergence, and evidence discipline as first-class
output. Where models disagree, that becomes a human-review trigger rather than a
number to smooth over.

**Representative source:**
[`production_reference/evidence_tier.py`](production_reference/evidence_tier.py) ·
[`production_reference/overlayComparison.ts`](production_reference/overlayComparison.ts)

### Why this is not an LLM wrapper

| Capability | Pantheon implementation |
|---|---|
| Evidence provenance | Source packs bound to content hashes / references |
| Fail-closed states | Missing, stale, blocked, parse, and provider failures stay visible — never a hollow success |
| Schema validation | Structured model outputs validated before serving |
| Multi-model comparison | Provider-level agreement and divergence, not a single opinion |
| Evidence hierarchy | Source-backed research kept separate from AI-prior |
| Human review | Disagreements and missing evidence generate review tasks |
| Research Ops | Coverage, provider health, queues, audit trail |
| Signal separation | AI research does not execute trades |

---

## 9. What AI Actually Does

Pantheon uses AI to perform **research-operation decisions** — not capital
decisions. Concretely, the AI layer performs:

- **Evidence synthesis** — turning governed source packs into structured research
- **Factor classification** — mapping evidence to defined research factors
- **Risk identification** — surfacing red flags and downside conditions
- **Evidence-gap detection** — naming what is missing rather than filling it in
- **Model disagreement detection** — comparing providers and reporting divergence
- **Confidence assessment** — grading how well-supported a conclusion is
- **Verification-task generation** — emitting the checks a human should run
- **Human-review escalation** — routing low-agreement or thin-evidence cases to review
- **Research summarization** — condensing multi-source research into readable briefs
- **Agent routing / tool-selection assistance** — choosing which governed tool answers a request
- **Personalized research explanation** — adapting explanation to the reader's context

And then, explicitly:

```text
AI research decisions
        ≠
capital-allocation / trading decisions
```

**AI decides what the research says. A human decides what the portfolio does.**

The boundary is enforced in code, not in policy prose. Pantheon's agent layer
permits investment *advice* — views, ratings, direction, risk/reward — and
refuses *execution*: order-lifecycle instructions, leverage instructions,
personalized position sizing, and any claim to have transmitted an instruction
to a venue. Pantheon has no order path, no broker credential, and no signing
key.

**Representative source:** [`production_reference/advice_policy.py`](production_reference/advice_policy.py)
— the actual advice-versus-execution boundary.

---

## 10. Product Surfaces

| Surface | Status |
|---|---|
| Web dashboard — multi-asset research cockpit | LIVE |
| PWA / mobile — installable progressive web app | LIVE |
| Ticker Profile & Equity Decisions | LIVE |
| AI Analyst Consensus / model-comparison cockpit | LIVE (cache-only) |
| LLM Research Summary | LIVE |
| Macro framework | LIVE |
| BTC framework | LIVE |
| Research Ops & data-quality control plane | INTERNAL (operator-gated) |
| Signal Alert Layer | INTERNAL (dry-run default) |
| Telegram Agent & signal delivery | BETA (controlled) |
| Email / weekly automated reports | BETA (controlled) |
| Watchlists / research records | LIVE |
| WeChat Mini Program | BETA (launch-candidate) |
| Trading Gateway | STAGED · fail-closed |

Billing is gated off by default; every real-delivery and execution path is
fail-closed behind environment kill-switches.

---

## 11. Gemini Hackathon Integration

Gemini is the **AI layer built during this submission period**, integrated into
the pre-existing multi-model lane and deployed independently on Google Cloud.

| Property | Value |
|---|---|
| Provider | Google Gemini API (Generative Language API v1beta) |
| Model | `gemini-2.5-flash` (configurable via `GEMINI_MODEL`) |
| Auth | API key via Secret Manager (`GEMINI_API_KEY` / `GOOGLE_API_KEY`) |
| Protocol | REST `generateContent` with JSON response mode |
| Runtime | Google Cloud Run (`asia-southeast1`, scale 0–3, 1 Gi, 1 CPU) |
| Image storage | Google Artifact Registry |
| Secrets | Google Secret Manager, bound via `--set-secrets` |
| Logging | Google Cloud Logging |
| Default local mode | **Offline** — bundled samples, no API key required |

### Workflow

```text
Governed Evidence Pack
  → Gemini
  → Structured Analyst / Risk Overlay
  → Multi-Model Comparison
  → Human Review
```

### Fail-closed design

| Condition | Status | Behavior |
|---|---|---|
| No API key | `BLOCKED_BY_MISSING_CREDENTIAL` | No call made, no fake result |
| API error | `API_ERROR` | Retry with backoff, then report |
| Non-JSON response | `PARSE_ERROR` | Report immediately, no retry |
| Offline mode | `OFFLINE_SAMPLE` | Bundled samples from `data/gemini_samples/` |

**Gemini never returns a fake SUCCESS.** Every failure mode maps to an explicit,
distinct, tested status.

### Live evidence

```bash
curl -s https://pantheon-gemini-549837878368.asia-southeast1.run.app/api/proof/gemini | jq
curl -s https://pantheon-gemini-549837878368.asia-southeast1.run.app/api/proof/google-cloud | jq
curl -s https://pantheon-gemini-549837878368.asia-southeast1.run.app/api/overlay/gemini/NVDA | jq
```

Implementation: [`backend/app/gemini_overlay.py`](backend/app/gemini_overlay.py) ·
Full evidence: [`docs/gemini_production_evidence.md`](docs/gemini_production_evidence.md)

---

## 12. Circle Agentic Economy

Pantheon completed a bounded **Circle Agent Wallet** on-chain payment proof:
founder-funded, operator-mediated, policy-limited, and independently verified on
Base mainnet.

| | |
|---|---|
| Circle product | Circle Agent Stack — Agent Wallets |
| Agent wallet | `0xaae4fab28919e5d0275fed67fca2100e0eb454bc` |
| Chain / token | Base mainnet (`8453`) · USDC |
| Amount | **0.100000 USDC** |
| Transaction | [`0x699bbb9ddb03f9a98525749374fb976a9cd7ef6319414d1cb5e422d810eac6e3`](https://basescan.org/tx/0x699bbb9ddb03f9a98525749374fb976a9cd7ef6319414d1cb5e422d810eac6e3) |
| Block | `49907662` · receipt status `0x1` |
| Circle policy caps | per-tx 1 · daily 2 · weekly 5 · monthly 10 USDC |

> **Verifying:** the wallet is an **ERC-4337 smart account**, so the outer
> transaction's `from` is a bundler and its `to` is the EntryPoint contract. Read
> the **"ERC-20 Tokens Transferred"** row on BaseScan, not the top-level
> From/To. Gas was sponsored by Circle — the wallet held 0 ETH before and after.

**Limitations, stated plainly.** The payment was **founder-funded**,
**operator-mediated**, **policy-limited**, and **not autonomous**. It involved
**no user capital**, **no trading**, and **no Pro entitlement**. Pantheon's
production Agent Treasury (policy engine, single-use human approval gate,
server-side proof verifier, append-only ledger) exists separately in the private
system, but **this final proof did not complete the production signed-in
approval flow**, and the Pantheon cloud proof verifier did not execute or verify
this payment. **No recipient allowlist was machine-enforced** — the recipient is
operator-attested as Pantheon-controlled, with risk bounded instead by funding
the wallet with exactly the proof amount.

Payment is **not an agent-invocable tool**, so prompt injection has no path to
money.

Full detail and independent verification instructions:
[`docs/circle_agentic_economy_evidence.md`](docs/circle_agentic_economy_evidence.md)

---

## 13. Validation

Pantheon distinguishes four different things that are often conflated:

| Term | What it means here |
|---|---|
| **Historical backtest** | A strategy run over stored history. Cheapest and weakest evidence. |
| **Reconstructed history** | History rebuilt from current-cohort data. Carries **survivorship limitations** — a declared constraint, not a solved problem. |
| **Point-in-time evidence** | Data as it was actually observable at decision time, with vintage discipline. |
| **Forward validation** | Signals captured prospectively, before outcomes exist. |
| **Matured outcomes** | Forward signals whose evaluation window has actually closed. |

**Only matured forward outcomes support a performance claim.** Pantheon captures
signals prospectively and lets them mature rather than marketing immature
evidence as proven alpha. Validation maturity varies by market; BTC is the most
mature public track, and equity markets are research-context while forward
samples accumulate.

**No validated-alpha claim is made anywhere in this submission.** Where a
framework has been falsified in internal research, it is retired rather than
retuned.

---

## 14. Deployment Architecture

Pantheon uses **one codebase and several deployment substrates**. GitHub is the
single source of code — the clouds do not each hold their own copy.

| Environment | Role | Data role | Writes |
|---|---|---|---|
| **Vercel** | Production frontend (`pantheon-research.com`) | — | — |
| **Railway** | Production backend — **canonical writer** | Canonical PostgreSQL | **Enabled** |
| **GCP Cloud Run** | **Gemini shadow / proof** | Isolated shadow role | Fail-closed OFF |

**Only one environment is ever the canonical production writer.** Vercel +
Railway is the primary production path. Google Cloud runs an isolated
**shadow / proof** deployment used to validate portability, regional
deployment, provider-specific AI integration, cost, latency, and observability.

Each deployment is stamped with non-secret runtime markers. The application
enforces roles in code, fail-closed: canonical writes are permitted **only** when
the deployment is stamped as production writer with a canonical database role. On
a stamped shadow, every background worker is forced off as defence in depth.

**Not claimed:** three simultaneous production writers, active-active
replication, automatic cross-cloud failover, or a full production database clone.
Cloud SQL is **not** configured for the Gemini Cloud Run service.

---

## 15. Business Model

| Stage | Offering |
|---|---|
| 1 | **Free research** — open cross-asset research surfaces |
| 2 | **Pantheon Pro** — subscription research and signal delivery |
| 3 | **Research Credits** — metered consumption for heavier workloads |
| 4 | **Premium research / playbooks** — deep-dive research products |
| 5 | **Skills marketplace** — third-party research skills |
| 6 | **Advanced data / API** — programmatic research access |
| 7 | **B2B / enterprise licensing** — institutional deployments |

### Actual hackathon-period results

| Metric | Actual |
|---|---|
| Revenue | **$0** |
| Verified external users | **0** |
| Paying users | **0** |
| Net result | **−$926.12** |

No traction is claimed. Full cash-basis P&L and the separation of actual results
from projections: [`docs/business_model_and_pnl.md`](docs/business_model_and_pnl.md).

---

## 16. Safety / Non-Claims

Pantheon Research is a research and decision-support system, **not financial
advice**. This submission explicitly does **not** claim:

- ❌ **No autonomous trading** — execution is manual and independently gated
- ❌ **No model-generated alpha** — LLMs produce research overlays, not signals with proven edge
- ❌ **No proven investment performance** — no validated-alpha claim is made
- ❌ **No user-capital movement** — Pantheon never moves user funds
- ❌ **No Gemini-controlled trading** — Gemini reads evidence and writes research
- ❌ **No Circle-controlled trading** — the payment rail is structurally separate from any order path
- ❌ **No AI override of deterministic ratings** — LLM output never mutates a deterministic score

**AI produces research intelligence. Humans remain responsible for investment
decisions.**

---

## 17. Run Locally

The full judge demo runs **with no API keys**.

```bash
git clone https://github.com/0xjacobzhao-byte/pantheon-research-gemini-hackathon
cd pantheon-research-gemini-hackathon
docker compose up --build          # frontend :5173 · backend :8000
./scripts/judge_smoke.sh           # end-to-end smoke test (offline, no secrets)
```

Then:

```bash
curl -s http://localhost:8000/api/proof/gemini | jq
curl -s http://localhost:8000/api/overlay/gemini/NVDA | jq
```

> **Ticker scope.** The local demo ships bundled evidence packs for **MA** and
> **NVDA** only. Production screenshots and the live product use **GOOGL** and a
> far broader universe. The local demo is deliberately **not** faked to match
> those screenshots — it serves exactly the two tickers it has governed offline
> evidence for. For GOOGL, use the live product.

<details>
<summary><b>Manual setup (no Docker)</b></summary>

**Backend** (Python 3.11–3.12):
```bash
cd backend && python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

**Frontend** (Node.js 18+):
```bash
cd frontend && npm install && npm run dev
```

| Service | URL |
|---------|-----|
| Frontend | http://localhost:5173 |
| Backend API | http://localhost:8000 |
| API Docs (Swagger) | http://localhost:8000/docs |

</details>

<details>
<summary><b>Full endpoint reference</b></summary>

| Method | Path | Description |
|--------|------|-------------|
| GET | `/health` | Health check |
| **Gemini** | | |
| GET | `/api/overlay/gemini/{ticker}` | Gemini qualitative overlay |
| GET | `/api/proof/gemini` | Gemini proof (secret-free, no external calls) |
| GET | `/api/proof/google-cloud` | Google Cloud deployment proof (secret-free) |
| GET | `/api/proof/gcp` | GCP Cloud Run metadata proof |
| **Core** | | |
| GET | `/api/project` | Project metadata |
| GET | `/api/evidence/{ticker}` | Evidence pack + provenance |
| GET | `/api/overlay/qwen/{ticker}` | Qwen overlay (secondary) |
| GET | `/api/overlay/deepseek/{ticker}` | DeepSeek overlay (secondary) |
| GET | `/api/comparison/{ticker}` | Multi-provider comparison |
| **Platform** | | |
| GET | `/api/data-quality` | Research-Ops governance |
| GET | `/api/modules` | Module snapshot grid |
| GET | `/api/provider-health` | Provider health |

</details>

### Tests

```bash
cd backend && python -m pytest            # backend tests
cd frontend && npm test -- --run          # frontend tests
cd frontend && npm run build              # production build
```

---

## 18. Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | FastAPI · Python 3.11–3.12 |
| Frontend | React 18 · TypeScript · Vite 6 |
| LLM (Gemini) | Google Gemini API — `gemini-2.5-flash` |
| LLM (others) | Claude · ChatGPT · DeepSeek · Qwen (Alibaba DashScope) |
| Database | PostgreSQL — production only |
| Payments | Circle Agent Wallets (Base mainnet, USDC) |
| Deploy (local) | Docker Compose |
| Deploy (production) | Vercel · Railway |
| Deploy (Gemini proof) | Google Cloud Run · Artifact Registry · Secret Manager · Cloud Logging |
| Tests | pytest (backend) · vitest + Testing Library (frontend) |

---

## Author & License

**Jacob Zhao** — [0xjacobzhao-byte](https://github.com/0xjacobzhao-byte) · Singapore

**License:** Apache-2.0 — see [LICENSE](LICENSE)

No API keys, private user data, live trading credentials, production secrets, or
private financial records are included in this repository.

<div align="center">
<sub><b>Build the framework first. Let AI compound the discipline.</b></sub>
</div>
