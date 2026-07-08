# Project Story — Pantheon Research Gemini Hackathon

## Inspiration

Investment research is drowning in data but starving for insight. Analysts spend 80% of their time collecting and formatting evidence, leaving only 20% for actual judgment. We asked: **what if Gemini could convert structured quantitative evidence into explainable, professional-grade research overlays in seconds — while keeping a human firmly in the loop?**

The inspiration is not to replace the analyst. It is to give every analyst a tireless, disciplined research partner that never fabricates conclusions, never hides uncertainty, and never executes trades.

$$
\mathrm{Wrong\ Strategy} \times \mathrm{AI} = \mathrm{Faster\ Loss}
$$

$$
\mathrm{Right\ Strategy} \times \mathrm{AI} = \mathrm{Compounded\ Discipline}
$$

## What It Does

Pantheon Research is a **framework-first, data-governed, human-in-the-loop investment research operating system**. The Gemini Hackathon submission adds a **Gemini-powered Analyst / Risk-Review layer** that:

1. **Ingests** structured quantitative evidence packs (P/E, P/B, ROIC, FCF, margins, growth rates)
2. **Generates** structured qualitative overlays via Google Gemini: business quality, moat, pricing power, capital allocation, red flags, confidence score, missing evidence
3. **Compares** Gemini's output against Qwen and DeepSeek overlays for divergence detection
4. **Flags** human review when models disagree or evidence is incomplete
5. **Never** executes trades, fabricates results, or returns fake success

## How We Built It

- **Backend:** FastAPI (Python) with fail-closed Gemini API integration
- **Frontend:** React + TypeScript + Vite with dedicated GeminiOverlayPanel component
- **Evidence Layer:** JSON evidence packs with SHA-256 content hashing for provenance
- **Fail-Closed Design:** Missing key → `BLOCKED_BY_MISSING_CREDENTIAL`; API error → `API_ERROR`; non-JSON → `PARSE_ERROR`. Never a hollow SUCCESS.
- **Offline-First:** Bundled sample overlays let the entire demo run with zero API keys

## Gemini Integration

Gemini is the **primary AI analyst layer** for this hackathon submission:

- **API:** Google Generative Language API v1beta (`generateContent`)
- **Model:** `gemini-2.0-flash` with JSON response mode
- **Prompt Engineering:** Structured prompt requesting specific financial assessment fields
- **Fail-Closed:** Three explicit failure modes, never fake success
- **Implementation:** [`backend/app/gemini_overlay.py`](../backend/app/gemini_overlay.py)

### Google Cloud Product Used

**Google Gemini API** (Generative Language API) — the core AI service powering the qualitative research overlay.

We also use **Google AI Studio** for prompt prototyping and model evaluation during development.

## Challenges

1. **Fail-Closed Guarantee:** Ensuring the system never returns fabricated results required careful error handling across network failures, auth errors, and malformed model outputs
2. **Evidence Provenance:** Threading SHA-256 content hashes through every comparison so judges can verify data integrity
3. **Honest Positioning:** Clearly distinguishing what the system does (research overlays) from what it does not do (execute trades, generate alpha)
4. **Multi-Provider Comparison:** Making Qwen and DeepSeek overlays compatible with Gemini output for apples-to-apples divergence analysis

## What We Learned

- **AI is a research amplifier, not a decision maker.** The most valuable output is not a buy/sell signal — it is a structured, explainable assessment that a human can act on (or reject).
- **Fail-closed is more important than fail-fast.** A system that returns a clear "I cannot assess this" is infinitely more valuable than one that returns a confident but fabricated answer.
- **Evidence provenance matters.** Hashing evidence packs and threading the hash through every downstream output creates an auditable chain of custody.

## Business Model

See [docs/business_model_and_pnl.md](business_model_and_pnl.md) for detailed projections.

- **Pro individual subscription:** $49–$99/month for individual investors
- **Premium AI research reports:** Per-report pricing for deep-dive analysis
- **Signal alerts:** Tiered alert subscriptions
- **B2B research tools:** API access for hedge funds, family offices, RIAs
- **Enterprise / white-label:** Custom deployments for institutional clients

## What's Next

1. **Live Gemini integration testing** with broader ticker universe
2. **Multi-language overlays** (Chinese, Japanese) for Asian market coverage
3. **Forward validation framework** — track overlay predictions against actual outcomes over 6–12 month windows
4. **Institutional API tier** with SLA-backed uptime and dedicated model routing
5. **Mobile-first research dashboard** extending the Gemini overlay to iOS/Android
