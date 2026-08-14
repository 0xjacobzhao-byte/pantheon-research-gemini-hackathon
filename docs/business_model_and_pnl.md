# Business Model & P&L — Pantheon Research

> **This document leads with actual results.** Projections appear only in §4,
> clearly labelled, and are **not** offered as evidence of performance.

Snapshot date: **2026-08-14**.

---

## 1. Actual hackathon-period P&L — cash basis

This is the submitted financial evidence. It is what actually happened.

| Line item | Actual (USD) |
|---|---:|
| **Revenue** | **$0.00** |
| Cost of Goods Sold (LLM + data + infrastructure) | $316.85 |
| Sales & Marketing | $33.69 |
| Research & Development | $560.58 |
| General & Administrative | $15.00 |
| **Total Expenses** | **$926.12** |
| **Profit / (Loss)** | **−$926.12** |

### Actual traction

| Metric | Actual |
|---|---:|
| Revenue | **$0** |
| Verified external users | **0** |
| Paying users | **0** |
| Customers | **0** |

**No traction is claimed.** There is no user base, no revenue, and no paying
customer to report. The product is live and free; commercialization has not
started.

### What these numbers are

- **Cash basis** — money actually spent during the hackathon period.
- **COGS** is real infrastructure and model spend for a running system: LLM API
  calls across five providers, market-data access, and hosting.
- **R&D** is the largest line, which is what a pre-revenue research system
  should look like.
- **No founder salary is capitalized or imputed.** Founder time is unpaid and
  does not appear in these figures.
- **No revenue is deferred, accrued, or projected into this table.**

### What these numbers are not

- ❌ Not a profit claim. The submitted result is a **loss**.
- ❌ Not a projection. §4 is the projection; this section is not.
- ❌ Not audited financial statements.

---

## 2. Business model

Pantheon monetizes **research tooling**, not investment performance. Revenue is
structurally decoupled from whether any signal was right.

| Stage | Offering | Status |
|---|---|---|
| 1 | **Free research** — open cross-asset research surfaces | LIVE |
| 2 | **Pantheon Pro** — subscription research and signal delivery | BETA (controlled) |
| 3 | **Research Credits** — metered consumption for heavier workloads | PLANNED |
| 4 | **Premium research / playbooks** — deep-dive research products | PLANNED |
| 5 | **Skills marketplace** — third-party research skills | PLANNED |
| 6 | **Advanced data / API** — programmatic research access | PLANNED |
| 7 | **B2B / enterprise licensing** — institutional deployments | PLANNED |

Only stage 1 is live and free. Stage 2 is a controlled beta with billing gated
off by default. Stages 3–7 are roadmap and have generated **$0**.

---

## 3. How the business operates with AI

- **AI as research analyst** — five LLM providers generate structured
  qualitative assessments from governed evidence packs.
- **AI as comparison engine** — providers produce independent overlays;
  divergence is surfaced as a review trigger.
- **AI as quality gate** — fail-closed design means missing credentials, API
  errors, and parse failures each produce explicit states, never a fabricated
  result.
- **AI as research operator** — evidence-gap detection, confidence assessment,
  verification-task generation, and human-review escalation.
- **Human as decision maker** — the investment decision always rests with a
  human. See [`../production_reference/advice_policy.py`](../production_reference/advice_policy.py)
  for the enforced boundary.

### Cost structure

- **DB-first architecture.** Research reads governed PostgreSQL observations
  rather than re-fetching from providers at request time, so read volume does
  not scale linearly with usage.
- **Cached evidence packs.** Each pack is built once and hashed; multiple
  provider overlays reuse the same pack.
- **Selective model calls.** Overlays are generated per-ticker on demand and
  cached, not continuously batch-scanned.
- **Model routing.** Lighter models (e.g. `gemini-2.5-flash`) serve standard
  overlays; heavier models are reserved for premium deep-dives.
- **Scale-to-zero proof deployments.** The Google Cloud Run Gemini service
  scales to zero when idle.

---

## 4. Projections — explicitly not evidence

> ⚠️ **Everything below this line is a forward-looking projection.**
> It is **not** realized performance, and it is **not** the profit evidence for
> this submission. The submitted financial result is §1: **a loss of $926.12 on
> $0 revenue.**

### Indicative pricing (not yet validated by a paying customer)

| Tier | Price range |
|---|---|
| Pro Individual | $49–$99 / month |
| Premium Reports | $29–$99 / report |
| Signal Alerts | $9–$29 / month |
| B2B Research API | $500–$5,000 / month |
| Enterprise / White-Label | $10,000–$50,000+ / month |

**No customer has paid any of these prices.** They are untested.

### Five-year projection

| Year | Revenue | COGS | OpEx | Net Income |
|---|---|---|---|---|
| 1 | $50K–$150K | $30K–$80K | $80K–$120K | −$60K to −$50K |
| 2 | $300K–$800K | $120K–$300K | $200K–$350K | −$70K to +$150K |
| 3 | $1.5M–$3M | $500K–$1M | $800K–$1.5M | +$200K to +$500K |
| 4 | $3M–$6M | $900K–$1.8M | $1.5M–$2.5M | +$600K to +$1.7M |
| 5 | $5M–$10M | $1.5M–$3M | $2.5M–$4M | +$1M to +$3M |

- **Five-year target:** $5M–$10M ARR
- **TAM:** $1B–$3B (AI-assisted qualitative investment research niche within a
  $30B+ global investment research and analytics market)
- **Target share:** <1% of the niche
- **Projected path to profitability:** Year 3

All figures above are unvalidated assumptions.

---

## 5. Why the model is defensible

- **Recurring revenue** with high retention potential — research tools become
  workflow-embedded.
- **Low marginal cost per user** — evidence packs are reusable across providers
  and users; model spend is per-call and cacheable.
- **Moat through governance, not model access.** Anyone can call an LLM.
  Evidence provenance, fail-closed states, lane separation, forward validation,
  and human-review gating are the parts that take years and are the reason a
  serious investor would trust the output.
- **No dependency on trading performance.** Revenue comes from research tooling.
  Pantheon does not need to be right about a stock to be paid.

---

## 6. Disclaimers

- Revenue during the hackathon period is **$0.00**; the result is a **loss of
  $926.12**.
- Verified external users: **0**. Paying users: **0**.
- All §4 figures are projections based on unvalidated assumptions.
- Actual results will depend on market adoption, pricing validation, and
  competitive dynamics.
- Pantheon Research does not execute trades, manage assets, or provide
  investment advice.
