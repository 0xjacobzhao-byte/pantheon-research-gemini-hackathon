# Business Model & P&L — Pantheon Research

> **No realized profit is claimed for this hackathon submission unless actual revenue evidence is attached.**
> This document provides a conservative P&L model and path-to-profitability projection.

---

## Pricing Model

| Tier | Description | Price Range |
|------|-------------|-------------|
| **Pro Individual** | Monthly subscription for individual investors: Gemini overlays, evidence packs, signal alerts | $49–$99/month |
| **Premium Reports** | Per-report deep-dive AI research with Gemini + multi-model comparison | $29–$99/report |
| **Signal Alerts** | Tiered alert subscriptions for overlay changes and divergence flags | $9–$29/month |
| **B2B Research API** | API access for hedge funds, family offices, RIAs | $500–$5,000/month |
| **Enterprise / White-Label** | Custom deployments, dedicated model routing, SLA | $10,000–$50,000+/month |

---

## Five-Year Goal

- **$5M–$10M ARR** by Year 5
- **Tiny share** of the large fintech / investment research tooling market
- **Target market:** Individual investors, RIAs, family offices, small-to-mid hedge funds

### TAM Estimate

The global investment research and analytics market is estimated at $30B+ (2025). Pantheon Research targets a niche within AI-assisted qualitative research overlays — a subset estimated at $1B–$3B and growing rapidly with LLM adoption.

---

## P&L Projection (Conservative)

| Year | Revenue | COGS (LLM + Data + Infra) | Gross Margin | OpEx | Net Income |
|------|---------|---------------------------|--------------|------|------------|
| **Year 1** | $50K–$150K | $30K–$80K | ~50% | $80K–$120K | **-$60K to -$50K** |
| **Year 2** | $300K–$800K | $120K–$300K | ~55% | $200K–$350K | **-$70K to +$150K** |
| **Year 3** | $1.5M–$3M | $500K–$1M | ~60% | $800K–$1.5M | **+$200K to +$500K** |
| **Year 4** | $3M–$6M | $900K–$1.8M | ~65% | $1.5M–$2.5M | **+$600K to +$1.7M** |
| **Year 5** | $5M–$10M | $1.5M–$3M | ~65% | $2.5M–$4M | **+$1M to +$3M** |

*All figures are projections. No revenue has been realized as of this hackathon submission.*

---

## Cost Model

### LLM Costs

- **Controlled through cached evidence packs:** Each evidence pack is loaded once and hashed; multiple overlay calls reuse the same pack
- **Selective calls:** Gemini is called per-ticker on demand, not batch-scanned continuously
- **Model routing:** Lightweight models (gemini-2.0-flash) for standard overlays; heavier models reserved for premium deep-dives
- **Estimated per-overlay cost:** $0.001–$0.01 per Gemini call at current pricing

### Data Costs

- **DB-first architecture:** Quantitative evidence is stored in PostgreSQL and served without repeated external API calls
- **Provider routing:** Multiple data providers with cost-tiered fallback (free → low-cost → premium)
- **Offline samples:** The demo runs entirely on bundled data with zero external data cost

### Infrastructure Costs

- **Containerized deployment:** Docker Compose for local, single-ECS for production
- **Modular services:** Backend and frontend scale independently
- **Estimated monthly infra cost:** $50–$200/month for early-stage deployment

---

## Path to Profitability

1. **Year 1:** Validate product-market fit with 100–500 Pro subscribers. Focus on Gemini overlay quality and user feedback. Negative or breakeven.
2. **Year 2:** Launch B2B API tier. Acquire 5–20 institutional clients. Approach breakeven.
3. **Year 3:** Scale to 2,000+ Pro subscribers and 50+ B2B clients. Achieve profitability.
4. **Year 4–5:** Expand to Asian markets (Chinese, Japanese overlays). Enterprise white-label deployments. Sustainable growth.

---

## Business Sustainability

- **Recurring revenue model:** Subscription-based with high retention potential (research tools become workflow-embedded)
- **Low marginal cost:** LLM API costs are tiny per user; evidence packs are reusable
- **Moat through data governance:** Evidence provenance hashing, fail-closed design, and human-in-the-loop create trust that pure LLM wrappers cannot replicate
- **No dependency on trading performance:** Revenue comes from research tooling, not investment returns

---

## How the Business Operates with AI

- **AI as research analyst:** Gemini generates structured qualitative assessments from quantitative evidence
- **AI as comparison engine:** Multiple LLM providers (Gemini, Qwen, DeepSeek) produce independent overlays for divergence detection
- **AI as quality gate:** Fail-closed design ensures the system never fabricates results; human review is flagged when models disagree
- **Human as decision maker:** The final investment decision always rests with a human portfolio manager

---

## Disclaimers

- No realized profit, revenue, or customer metrics are claimed for this hackathon submission
- All P&L figures are projections based on conservative market assumptions
- Actual results will depend on market adoption, pricing validation, and competitive dynamics
- Pantheon Research does not execute trades, manage assets, or provide investment advice
