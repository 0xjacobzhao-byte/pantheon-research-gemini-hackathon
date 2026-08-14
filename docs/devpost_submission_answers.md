# Devpost Submission Answers

> Reconciled against the **live Devpost submission** and current product truth
> as of **2026-08-14**.
>
> Live submission: https://devpost.com/software/pantheon-research-qzn50k

---

## Tagline

> Pantheon Research is an institutional cross-asset command center using
> quantitative frameworks to turn market noise into actionable intelligence
> across Macro, Equities, Crypto, and FICC.

---

## Project Story

Full narrative: [`project_story.md`](project_story.md).

**Short version:** Pantheon Research is a live, human-in-the-loop, cross-asset
investment research operating system with seven layers — external data, a
governed data platform, deterministic research engines, a deterministic +
five-model AI layer, the information layer, the signal/agent layer, and a
separated trading boundary. For this hackathon we built the **Gemini Analyst /
Risk-Review layer**, deployed it on Google Cloud Run, and added a **Circle Agent
Wallet on-chain payment proof**. Gemini does not execute trades, does not
override deterministic ratings, and does not manage assets.

**Scope boundary:** Pantheon existed before the hackathon. See
[`SUBMISSION_SCOPE.md`](SUBMISSION_SCOPE.md).

---

## Built With

```
gemini · google-cloud · claude · chatgpt · deepseek · qwen · circle
python · fastapi · postgresql · react · typescript · vite · docker
vercel · railway · human-in-the-loop · codex · hermes · openclaw
```

---

## How the Project Uses AI to Impact Money & Financial Access

Pantheon uses AI to democratize access to professional-grade investment
research. Individual investors, family offices, and small advisory teams lack
the analyst teams, data engineers, and risk committees that large institutions
deploy. Pantheon converts governed financial evidence into explainable
qualitative assessments — business quality, moat, pricing power, capital
allocation, red flags, evidence gaps — across macro, equities, crypto, and FICC.

Critically, the system is **fail-closed and human-in-the-loop**: it never
fabricates results, never hides uncertainty, and never executes trades. It
amplifies human judgment rather than replacing it — professional research
methodology without the risks of autonomous AI trading.

---

## What AI Actually Does (AI-Native Operations)

AI performs **research-operation decisions**:

evidence synthesis · factor classification · risk identification · evidence-gap
detection · model disagreement detection · confidence assessment ·
verification-task generation · human-review escalation · research summarization
· agent routing and tool selection · personalized research explanation

And explicitly **not** capital decisions:

```text
AI research decisions  ≠  capital-allocation / trading decisions
```

The boundary is enforced in code, not policy prose — see
[`../production_reference/advice_policy.py`](../production_reference/advice_policy.py).
Advice is ALLOWED; execution is NOT AUTHORIZED. Pantheon has no order path, no
broker credential, and no signing key.

---

## Which LLMs Are Used, and How Gemini Is Used

Pantheon runs a **five-model** research overlay behind one schema-validated
pipeline:

| LLM | Role |
|---|---|
| **Google Gemini 2.5 Flash** | Hackathon analyst layer — structured qualitative overlays from evidence packs |
| **Claude** | Qualitative overlay & risk reasoning |
| **ChatGPT** | Qualitative overlay & comparison |
| **DeepSeek** | Qualitative overlay (production lane) |
| **Qwen** (Alibaba DashScope) | Qualitative overlay |

Gemini is called via `POST {base_url}/models/{model}:generateContent` with:

- `contents` — the evidence pack formatted as a structured prompt
- `generationConfig.temperature` — 0.7
- `generationConfig.responseMimeType` — `application/json`

Implementation: [`../backend/app/gemini_overlay.py`](../backend/app/gemini_overlay.py)

**Fail-closed:** missing key → `BLOCKED_BY_MISSING_CREDENTIAL`; API error →
`API_ERROR`; non-JSON → `PARSE_ERROR`. Never a hollow SUCCESS.

---

## Which Google Cloud Products Were Used and How

| Product | How used |
|---|---|
| **Google Gemini API** (Generative Language API v1beta) | Primary AI service for qualitative research overlays. Model `gemini-2.5-flash`, REST `generateContent`, JSON response mode. |
| **Google Cloud Run** | Backend deployed as a managed container in `asia-southeast1`, auto-scaling 0–3 instances, 1 Gi memory, 1 CPU. Live: https://pantheon-gemini-549837878368.asia-southeast1.run.app |
| **Google Artifact Registry** | Container image storage. |
| **Google Secret Manager** | `GEMINI_API_KEY` stored and bound to Cloud Run via `--set-secrets`, with a least-privilege custom service account. |
| **Google Cloud Logging** | Automatic request/response logging for the Cloud Run service. |
| **Google AI Studio** | Prompt prototyping and model evaluation during development. |
| **Cloud SQL** | **Not used** in this deployment. Explicitly not claimed. |

The Cloud Run service is a **shadow / proof** deployment, not the canonical
production writer. Primary production is Vercel + Railway.

---

## Circle Agentic Economy

| | |
|---|---|
| Circle product | Circle Agent Stack — Agent Wallets |
| Agent wallet | `0xaae4fab28919e5d0275fed67fca2100e0eb454bc` |
| Chain / token | Base mainnet (`8453`) · USDC |
| Amount | 0.100000 USDC |
| Transaction | `0x699bbb9ddb03f9a98525749374fb976a9cd7ef6319414d1cb5e422d810eac6e3` |
| Block | `49907662` |

**Limitations, stated plainly:** founder-funded, operator-mediated,
policy-limited, **not autonomous**. No user capital, no trading, no Pro
entitlement. The production signed-in Treasury approval flow was **not**
demonstrated by this proof, and no recipient allowlist was machine-enforced.

Full evidence: [`circle_agentic_economy_evidence.md`](circle_agentic_economy_evidence.md).

> The wallet is an **ERC-4337 smart account** — verify via the ERC-20 `Transfer`
> log, not the outer transaction's From/To.

---

## Business Model

Free research → Pantheon Pro → Research Credits → premium research/playbooks →
skills marketplace → advanced data/API → B2B/enterprise licensing.

Only free research is live; Pro is a controlled beta with billing gated off.
Everything else is roadmap.

---

## Actual Hackathon-Period Financials

| Line item | Actual (USD) |
|---|---:|
| **Revenue** | **$0.00** |
| COGS | $316.85 |
| Sales & Marketing | $33.69 |
| R&D | $560.58 |
| G&A | $15.00 |
| **Total Expenses** | **$926.12** |
| **Profit / (Loss)** | **−$926.12** |

| Metric | Actual |
|---|---:|
| Revenue | **$0** |
| Verified external users | **0** |
| Paying users | **0** |

**No realized profit, revenue, or traction is claimed.** Full detail and the
clear separation of actuals from projections:
[`business_model_and_pnl.md`](business_model_and_pnl.md).

---

## Business Model Sustainability and Viability

1. Research-tooling revenue is **decoupled from market performance** — income
   comes from subscriptions, not trading results.
2. **Marginal costs are low and predictable** — evidence packs are built once,
   hashed, and reused across five providers; overlays are cached.
3. **Defensibility is governance, not model access.** Anyone can call an LLM.
   Evidence provenance, fail-closed states, lane separation, forward validation,
   and human-review gating are the hard parts.
4. **Multiple revenue tiers** reduce concentration risk.

Five-year target $5M–$10M ARR against a $1B–$3B niche TAM, targeting <1% share,
with projected profitability in Year 3 — **all projections, none realized.**

---

## Extent to Which AI Is Live in Production

- **Live:** AI generates real qualitative overlays from governed evidence packs
  in the production research surface, across five providers.
- **Not done by AI:** trade execution, investment decisions, asset management,
  capital movement, or mutation of deterministic ratings.
- **Fail-closed by design:** missing credentials, API errors, and parse failures
  each produce explicit states — never fabricated results.
- **Public demo default is offline:** the judge demo runs end-to-end with
  bundled samples and no API keys.

---

## Links

| Field | Value |
|---|---|
| Live product | https://pantheon-research.com |
| Public repo | https://github.com/0xjacobzhao-byte/pantheon-research-gemini-hackathon |
| Cloud Run service | https://pantheon-gemini-549837878368.asia-southeast1.run.app |
| Google Cloud proof | https://pantheon-gemini-549837878368.asia-southeast1.run.app/api/proof/google-cloud |
| Gemini proof | https://pantheon-gemini-549837878368.asia-southeast1.run.app/api/proof/gemini |
| Gemini overlay | https://pantheon-gemini-549837878368.asia-southeast1.run.app/api/overlay/gemini/NVDA |
| Product-running evidence | [`gemini_production_evidence.md`](gemini_production_evidence.md) |
| Evidence index | [`PRODUCT_EVIDENCE_INDEX.md`](PRODUCT_EVIDENCE_INDEX.md) |
| Submission scope | [`SUBMISSION_SCOPE.md`](SUBMISSION_SCOPE.md) |
| P&L evidence | [`business_model_and_pnl.md`](business_model_and_pnl.md) |
| Circle proof | https://basescan.org/tx/0x699bbb9ddb03f9a98525749374fb976a9cd7ef6319414d1cb5e422d810eac6e3 |
| Redacted live Gemini call | [`../data/gemini_live_call_redacted.json`](../data/gemini_live_call_redacted.json) |

> ⚠️ **The private repository is not judge-accessible.** If the Devpost "Try it
> out" section links https://github.com/0xjacobzhao-byte/Pantheon-Research,
> judges will hit a 404. Link the **public** repo there.

---

## Submitter Details

| Field | Value |
|---|---|
| Submitter type | Individual |
| Country | Singapore |
| Hackathon | Build with Gemini XPRIZE |

---

## Pre-Existing Work Disclosure

Pantheon Research (brand, product, data infrastructure, private production
repository, and existing audience) pre-existed this hackathon and is reused as
permitted. The work added during the submission period is the Gemini Analyst /
Risk-Review layer, the Google Cloud deployment and proof surface, this public
judge-facing repository, the Circle Agent Wallet on-chain payment proof, and the
submission evidence package.

Full boundary with commit, transaction, and endpoint evidence:
[`SUBMISSION_SCOPE.md`](SUBMISSION_SCOPE.md).

---

## Demo Video

See [`demo_video_script.md`](demo_video_script.md). Target length: **2:40–2:50**
(under the 3-minute limit).
