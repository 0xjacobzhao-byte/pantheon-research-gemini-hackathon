# Project Story — Pantheon Research

## Inspiration

Modern investors are not short of data. They are short of **governed,
explainable, decision-ready intelligence**.

A single investment decision can require macro liquidity, rates, credit,
earnings, valuation, crypto flows, on-chain data, derivatives positioning,
technical structure, news, sentiment, portfolio exposure, and execution risk.
Large institutions handle this with analyst teams, data engineers, risk
committees, internal research systems, and trading desks. Individual investors,
family offices, and smaller advisory teams usually stitch together dashboards,
spreadsheets, chatbots, broker screens, and manual notes.

Pantheon Research started from one question:

> What would an AI-native investment research operating system look like if it
> combined institutional-style investment frameworks, governed data,
> deterministic signal engines, multi-model AI reasoning, forward validation,
> and human review — **without letting AI execute trades?**

The core thesis:

```text
Wrong Strategy × AI = Faster Loss
Right Strategy × AI = Compounded Discipline
```

**AI should not replace the investor. AI should compound the investor's
discipline.**

---

## What It Does

Pantheon Research is a live, human-in-the-loop, cross-asset investment research
operating system. Not a demo, and not a financial chatbot — a research stack
with **seven layers**:

1. **External data sources** — macro/rates, equities, crypto/DeFi, social and
   alternative data, positioning, derivatives, and market-structure inputs.
2. **Governed data platform** — raw inputs are never passed straight to an AI.
   They flow through scheduled ingestion, provider-health checks, validation,
   normalization, PostgreSQL canonical observations, product and derived
   snapshots, evidence artifacts, TTL/freshness checks, and explicit
   data-quality labelling.
3. **Strategy / research engines** — deterministic engines across Global Macro,
   US/CN/HK/SG equities, BTC, ETH, DeFi, Fixed Income, FX, Commodities,
   Technical Analysis, Narrative/capital-flow, and backtest/validation.
4. **Deterministic + multi-model AI layer** — deterministic engines compute
   valuations, factor regressions, signals, and hard stops. The LLM layer then
   interprets governed evidence packs through source-pack building, prompt
   construction, schema validation, and overlay comparison.
5. **Information layer** — the live Pantheon dashboard across every cross-asset
   module.
6. **Signal + agent layer** — Telegram, user feeds, research alerts, LLM signal
   channels, and human-review gates.
7. **Trading layer** — deliberately separated. Execution is manual today. There
   is no live autonomous trading.

### The hackathon layer

For this submission, the new work is the **Gemini Analyst / Risk-Review layer**.
Gemini reads structured evidence packs and produces qualitative overlays:
business quality, moat, pricing power, capital allocation, red flags, missing
evidence, confidence score, and human-review triggers.

Gemini does not place trades. It does not override deterministic ratings. It
does not manage assets. It acts as a governed analyst layer inside a larger
investment-intelligence operating system.

The workflow:

```text
Data → Canonical Snapshot → Strategy Engine → Signal
     → Gemini / Multi-Model Overlay → Human Review → Manual Execution
```

**Scope boundary:** Pantheon Research existed before this hackathon. What was
built during the submission period — with commit, transaction, and endpoint
evidence — is documented in [`SUBMISSION_SCOPE.md`](SUBMISSION_SCOPE.md).

---

## How We Built It

Pantheon is framework-first, data-governed, and DB-first.

The architecture starts with **deterministic investment frameworks**. Each
framework defines what matters, how evidence is scored, what invalidates a
conclusion, and when the system must refuse to conclude.

The **data layer** turns raw market inputs into governed database artifacts.
Pantheon does not ask an LLM to "look at the market" from scratch. Scheduled
jobs produce canonical PostgreSQL observations, provider scores, product
snapshots, ingest runs, derived snapshots, and evidence artifacts. Research
engines read those stored artifacts rather than refetching at runtime.

The **AI layer** sits on top of that governed evidence. Pantheon uses a
**five-model LLM research overlay**:

| Provider | Role |
|---|---|
| **Claude** | Qualitative overlay & risk reasoning |
| **ChatGPT** | Qualitative overlay & comparison |
| **Gemini** | Qualitative overlay (Google Cloud integration) |
| **DeepSeek** | Qualitative overlay (production lane) |
| **Qwen** | Qualitative overlay (Alibaba DashScope) |

The LLM workflow is: **Source Pack Builder → Prompt Builder → Schema Validator →
Overlay Comparison → Human Review Gate.**

It produces qualitative overlays, confidence labels, red flags, missing
evidence, disagreement detection, and review triggers. It does **not** directly
mutate deterministic scores, and it does **not** execute trades.

### The Gemini build

| Component | Detail |
|---|---|
| Backend | FastAPI / Python |
| Frontend | React · TypeScript · Vite |
| AI | Google Gemini API — **`gemini-2.5-flash`** |
| Google Cloud | Cloud Run · Artifact Registry · Secret Manager · Cloud Logging |
| Evidence | Structured JSON evidence packs, SHA-256 provenance hashes, redacted live-call evidence |
| Safety | Fail-closed Gemini integration with explicit error states |
| Deployment | Live Cloud Run service with proof endpoints and a verified live Gemini API call |

Implementation: [`backend/app/gemini_overlay.py`](../backend/app/gemini_overlay.py).

### Deployment

- **Primary production:** Vercel frontend + Railway FastAPI backend + PostgreSQL
  — the only canonical writer.
- **Google Cloud:** the Gemini service on Cloud Run, as an isolated shadow /
  proof deployment. Cloud SQL is **not** configured.

The shadow deployment was not built to look complicated. It was built to test
portability, cost, reliability, and provider integration under real deployment
constraints. Only one environment is ever the canonical production writer.

---

## Challenges We Ran Into

The hard part was never calling an LLM. It was building a system where AI could
be useful, auditable, and safe inside a real investment research workflow.

1. **Making AI part of a full research operating system.** A raw LLM answer is
   not research. Strategy frameworks, data governance, signal outputs,
   validation clocks, and human-review gates had to exist around the model.
2. **Data governance before AI reasoning.** Market data can be stale, missing,
   delayed, revised, or provider-inconsistent. Freshness, provider health,
   degradation, and gaps had to be labelled before anything downstream could
   trust the output.
3. **Fail-closed model behavior.** The Gemini layer must never return a fake
   success. Missing credentials, API failures, and parse errors map to explicit
   states: `BLOCKED_BY_MISSING_CREDENTIAL`, `API_ERROR`, `PARSE_ERROR`.
4. **Separating signal from execution.** The most dangerous shortcut in
   investment systems is turning a signal directly into a trade. Research,
   signal, review, paper-trade validation, broker integration, and execution are
   deliberately separate concerns.
5. **Backtesting and forward validation.** A backtest is not enough. Pantheon
   captures outcomes and matures decisions forward over time, so immature
   evidence is not marketed as proven alpha.
6. **Multi-model disagreement.** Five models do not always agree. Pantheon
   treats disagreement as useful information — a review trigger, not an error to
   hide.
7. **Multi-cloud deployment complexity.** Cloud Run made containerized
   deployment and secret management relatively efficient; a traditional
   ECS/Docker/Nginx/RDS path required considerably more work. That contrast
   became useful evidence about integration difficulty and operating cost.
8. **The honest hackathon boundary.** Pantheon existed before this hackathon.
   The submission-period work is the Gemini Analyst / Risk-Review layer, the
   Google Cloud deployment, the proof endpoints, the Circle payment proof, and
   the evidence package. That boundary is documented rather than blurred.

---

## Accomplishments We're Proud Of

- A live cross-asset research platform spanning macro, equities, crypto, DeFi,
  FICC, technical analysis, narrative, and Research Ops.
- Deterministic research engines that produce regimes, valuations, ratings, risk
  states, and signals **before** any LLM interpretation.
- A governed data platform with canonical PostgreSQL snapshots, provider-health
  checks, freshness labels, and explicit data-quality states.
- A five-model AI research overlay with disagreement detection.
- The Gemini Analyst / Risk-Review layer, deployed on Google Cloud Run with
  Secret Manager, Artifact Registry, and Cloud Logging, with a **verified live
  `gemini-2.5-flash` API call**.
- Proof endpoints judges can inspect without exposing any secret.
- A **Circle Agent Wallet on-chain USDC payment** on Base mainnet, independently
  verifiable from public chain data alone.
- Backtest and forward-validation infrastructure that separates evidence from
  marketing claims.
- A strict human-in-the-loop boundary with no live autonomous trading.

---

## What We Learned

**AI in finance should be a governance system, not a magic oracle.**

A useful AI investment system needs frameworks before prompts, data quality
before conclusions, deterministic scores before LLM interpretation, signal
separation before execution, backtests *plus* forward validation before
performance claims, and human review before capital risk.

**Model comparison beats model worship.** Gemini is powerful because it turns
structured evidence into readable, explainable research quickly. Its output
becomes *trustworthy* when it is compared against other models, checked against
deterministic signals, tied to evidence hashes, and passed through human review.

**Cloud deployment is part of product truth.** A local demo is not enough.
Judges, users, and future customers need to see that the system runs, secrets
are handled properly, evidence is reproducible, logs exist, costs are
measurable, and the product does not overclaim what AI is doing.

**The real opportunity is not "AI trading."** It is AI-native investment
intelligence: a governed system that helps humans process more evidence, more
consistently, across more markets.

---

## Business Model

Free research → Pantheon Pro → Research Credits → premium research/playbooks →
skills marketplace → advanced data/API → B2B/enterprise licensing.

**Actual hackathon-period results: $0 revenue, 0 verified external users, 0
paying users, net loss of $926.12.** No traction is claimed.

Full cash-basis P&L and the separation of actuals from projections:
[`business_model_and_pnl.md`](business_model_and_pnl.md).

---

## What's Next

1. **Expand Gemini overlays** beyond judge demo tickers to broader equity and
   cross-asset coverage.
2. **Portfolio-aware intelligence** — connect research to user portfolios,
   watchlists, exposure, and risk constraints.
3. **Strengthen forward validation** — continue signal-outcome capture and
   prospective maturation before making any performance claim.
4. **Develop the agent layer** — governed two-way conversation, memory, tool
   routing, signal-triggered reports, and cost-aware execution.
5. **Harden signal delivery** — Telegram, user feed, alerts, weekly reports, and
   human-review workflows, with execution still separate.
6. **Evaluate production cloud strategy** across integration difficulty,
   reliability, cost, and operational burden.
7. **Keep trading manual until validated.** Paper-trader harnesses and broker
   integration are on the roadmap; live autonomous trading remains off.
8. **Build toward B2B / B2B2C distribution** — investment-intelligence
   infrastructure for serious investors, advisors, family offices, wealth
   managers, and institutions.

Pantheon's goal is to become the governed intelligence layer between market
noise and human investment judgment.
