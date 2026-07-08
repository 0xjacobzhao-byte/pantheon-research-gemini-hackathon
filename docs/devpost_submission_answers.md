# Devpost Submission Answers — Gemini Hackathon

> Draft answers for the Devpost submission form. Conservative language, no overclaiming.

---

## Project Story

See [docs/project_story.md](project_story.md) for the full narrative.

**Short version:** Pantheon Research is a framework-first, data-governed, human-in-the-loop investment research operating system. For the Gemini Hackathon, we built a Gemini-powered Analyst / Risk-Review layer that converts structured quantitative evidence into explainable qualitative research overlays. Gemini does not execute trades — humans remain final decision-makers.

---

## Built With Tags

```
Gemini API, Google AI Studio, Google Cloud, Python, FastAPI, React, TypeScript,
Vite, PostgreSQL, Docker, Financial Technology, Investment Research, Public Markets,
Equities, Macro, Crypto, FICC, Data Quality, Model Comparison, Human-in-the-loop AI,
Structured Outputs, Evidence Provenance, Risk Analysis, Business Intelligence
```

---

## How the Project Uses AI to Impact the World in Money & Financial Access

Pantheon Research uses Google Gemini to democratize access to professional-grade investment research. Individual investors and small funds typically lack the analyst teams that large institutions deploy. Gemini levels the playing field by converting structured financial evidence into explainable qualitative assessments — business quality, moat analysis, pricing power, capital allocation, red flags — in seconds.

Critically, the system is **fail-closed and human-in-the-loop**: it never fabricates results, never hides uncertainty, and never executes trades. It amplifies human judgment rather than replacing it, making professional research methodology accessible without the risks of autonomous AI trading.

---

## Underlying Business Model

Subscription SaaS + API access:
- Pro individual: $49–$99/month
- Premium reports: $29–$99/report
- B2B API: $500–$5,000/month
- Enterprise white-label: $10,000–$50,000+/month

See [docs/business_model_and_pnl.md](business_model_and_pnl.md) for details.

---

## How Business Operations Will Be Sustained

- **Recurring subscription revenue** with high retention (research tools become workflow-embedded)
- **Low marginal cost per user** (LLM API costs are $0.001–$0.01 per overlay call)
- **Tiered pricing** from individual to enterprise creates natural growth ladder
- **No dependency on trading performance** — revenue comes from research tooling, not investment returns

---

## Which AI Tools Were Leveraged

- **Google Gemini API** (primary): Powers the qualitative research overlay — converts evidence packs into structured financial assessments
- **Google AI Studio**: Used for prompt prototyping and model evaluation during development
- **Qwen / Alibaba Cloud DashScope** (secondary): Comparison model for divergence analysis
- **DeepSeek API** (secondary): Independent comparison model

---

## Business Model Sustainability and Viability

The business model is sustainable because:
1. Research tooling revenue is **decoupled from market performance** — we earn from subscriptions, not from trading results
2. **Marginal costs are low and predictable** — LLM API pricing is per-call with caching
3. **Evidence-first architecture creates defensibility** — provenance hashing and fail-closed design build trust that pure LLM wrappers cannot replicate
4. **Multiple revenue tiers** reduce concentration risk

---

## Five-Year Goal, TAM, Market Share, P&L, Path to Profitability

- **Five-year revenue target:** $5M–$10M ARR
- **TAM:** $1B–$3B (AI-assisted qualitative investment research overlay niche)
- **Target market share:** <1% of niche (realistic, conservative)
- **Path to profitability:** Year 3 with 2,000+ Pro subscribers and 50+ B2B clients
- **See:** [docs/business_model_and_pnl.md](business_model_and_pnl.md)

---

## How the Business Operates with AI

1. User selects a stock ticker
2. Backend loads a structured evidence pack (P/E, P/B, ROIC, FCF, margins, growth)
3. Gemini generates a qualitative overlay: business quality, moat, pricing power, capital allocation, red flags, confidence, missing evidence
4. System compares against Qwen/DeepSeek for divergence detection
5. Human review is flagged if models disagree significantly
6. **Human makes the final decision** — Gemini never executes trades

---

## Extent to Which AI Is Live in Production and Executes Key Decisions

- **AI is live in the research overlay:** Gemini generates real qualitative assessments from evidence packs
- **AI does NOT execute trades or make investment decisions:** Every output is a research overlay reviewed by a human
- **AI does NOT manage assets or provide investment advice**
- **Fail-closed by design:** Missing credentials, API errors, and parse failures each produce explicit error states — never fabricated results
- **Default mode is offline:** The demo runs end-to-end with bundled samples and no API keys

---

## Which Google Cloud Product Was Used and How

**Google Gemini API** (Generative Language API v1beta):
- Used as the primary AI service for generating qualitative research overlays
- Called via REST `generateContent` endpoint with JSON response mode
- Model: `gemini-2.0-flash`
- Implementation: [`backend/app/gemini_overlay.py`](../backend/app/gemini_overlay.py)

**Google AI Studio:**
- Used for prompt engineering and model evaluation during development

---

## Which LLMs Are Used and How Gemini API Is Used

| LLM | Role | How Used |
|-----|------|----------|
| **Google Gemini 2.0 Flash** | Primary analyst | Generates structured qualitative overlays from evidence packs via REST API |
| **Qwen (Alibaba DashScope)** | Secondary comparison | Independent overlay for divergence detection |
| **DeepSeek** | Secondary comparison | Independent overlay for divergence detection |

Gemini API is called via `POST {base_url}/models/{model}:generateContent` with:
- `contents`: evidence pack formatted as a structured prompt
- `generationConfig.temperature`: 0.7
- `generationConfig.responseMimeType`: `application/json`

---

## GitHub Repo URL

```
https://github.com/0xjacobzhao-byte/pantheon-research-gemini-hackathon
```

---

## Product-Running Evidence URL

```
docs/gemini_production_evidence.md
```

(Will be: `https://github.com/0xjacobzhao-byte/pantheon-research-gemini-hackathon/blob/main/docs/gemini_production_evidence.md`)

---

## Profit/P&L Evidence URL

```
docs/business_model_and_pnl.md
```

(Will be: `https://github.com/0xjacobzhao-byte/pantheon-research-gemini-hackathon/blob/main/docs/business_model_and_pnl.md`)

**Note:** No realized profit is claimed. This document provides conservative projections.

---

## Submitter Type

```
Individual
```

---

## Country

```
Singapore
```

---

## Start Date

Use the date Gemini-specific module development started (hackathon period), not the original Pantheon Research platform start date.

**Suggested wording:** "Gemini Analyst module development began during the Gemini Hackathon period."

---

## Demo Video

See [docs/demo_video_script.md](demo_video_script.md) for the footage plan and script.
