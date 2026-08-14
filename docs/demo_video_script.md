# Demo Video Script — Pantheon Research

> **Target length: 2:40–2:50.** Hard ceiling 3:00. Judges should not need to
> watch past three minutes to see everything that matters.
>
> **Priority: the live product first.** The local demo appears only as a
> reproducibility note near the end. Showing a localhost demo for two minutes
> when a live cross-asset product exists undersells the submission.

**Tone:** professional, concise, product-focused. No alpha claims. No autonomous
trading claims.

---

## Shot list

| Time | Segment | Screen |
|---|---|---|
| 0:00–0:15 | Pantheon / the problem | Live product landing + hero line |
| 0:15–0:40 | Seven-layer architecture | Architecture diagram |
| 0:40–1:15 | Live GOOGL Ticker Profile / Equity Decision | Live product |
| 1:15–1:45 | AI Analyst Consensus + Gemini detail | Live product |
| 1:45–2:05 | Macro / BTC / validation | Live product |
| 2:05–2:25 | Telegram Agent / automated reports | Telegram + email |
| 2:25–2:40 | Gemini / GCP public proof | Browser + terminal |
| 2:40–2:50 | Circle proof + close | BaseScan + repo |

Pacing is a guide, not a metronome — borrow 3–5 seconds between adjacent
segments wherever the footage reads better.

---

### 0:00–0:15 — Pantheon / the problem

**Screen:** [pantheon-research.com](https://pantheon-research.com), top of page.

> "Investors aren't short of data. They're short of governed, explainable,
> decision-ready intelligence. Pantheon Research is an AI-native cross-asset
> research operating system — macro, equities, crypto, and FICC in one governed
> stack."

On-screen text:
```text
Wrong Strategy × AI = Faster Loss
Right Strategy × AI = Compounded Discipline
```

---

### 0:15–0:40 — Seven-layer architecture

**Screen:** the architecture diagram, panning across layers.

> "Seven layers. External data flows into a governed data platform — canonical
> observations, provider health, freshness and quality labels. Deterministic
> research engines compute scores and signals *before* any AI runs. Then a
> five-model AI layer interprets that governed evidence. Signals reach a human
> review gate. Execution sits behind an independent boundary — Pantheon has no
> order path."

Emphasize on screen: **layer 7 is not reachable from layer 4.**

---

### 0:40–1:15 — Live GOOGL Ticker Profile / Equity Decision

**Screen:** live product → GOOGL Ticker Profile → Equity Decision.

> "This is live production, not a demo fixture. A Ticker Profile pulls governed
> fundamentals, valuation, price target and fair value, technical structure, and
> event context — every field carrying provenance and freshness."

**Actions:**
- Open GOOGL Ticker Profile
- Scroll through fundamentals → valuation → price target / fair value
- Pause on a **data-quality or freshness label**
- Show the technical signal timeline

---

### 1:15–1:45 — AI Analyst Consensus + Gemini

**Screen:** AI Analyst Consensus panel → Gemini overlay detail.

> "Five models — Claude, ChatGPT, Gemini, DeepSeek, and Qwen — each read the
> same governed evidence pack and produce an independent structured overlay.
> Gemini, built for this hackathon, returns business quality, moat, pricing
> power, capital allocation, red flags, missing evidence, and a confidence
> score. Where the models disagree, Pantheon shows the disagreement instead of
> averaging it away — and that becomes a human-review trigger."

**Actions:**
- Show the consensus panel with all five providers
- Open the Gemini overlay detail
- **Highlight a divergence and the evidence-backed vs. AI-prior lane label**

---

### 1:45–2:05 — Macro / BTC / validation

**Screen:** Macro framework → BTC framework → validation surface.

> "The same governance runs cross-asset. Macro regime classification, the
> Bitcoin cycle framework, and forward validation — signals captured
> prospectively and allowed to mature. Pantheon does not claim validated alpha
> where maturity doesn't support it."

---

### 2:05–2:25 — Telegram Agent / automated reports

**Screen:** Telegram agent conversation → automated research report email.

> "Research reaches the user through a Telegram agent and automated reports. The
> agent will give you a view — direction, risk, invalidation. What it will never
> do is place an order. Advice is allowed; execution is not authorized, and
> that boundary is enforced in code."

---

### 2:25–2:40 — Gemini / GCP public proof

**Screen:** split — browser on the proof endpoint, terminal running curl.

```bash
curl -s https://pantheon-gemini-549837878368.asia-southeast1.run.app/api/proof/google-cloud | jq
```

> "The Gemini layer is deployed on Google Cloud Run with Artifact Registry,
> Secret Manager, and Cloud Logging. The proof endpoints return no secrets and
> make no external calls. Everything a judge needs is verifiable from a browser."

**Highlight:** `model: gemini-2.5-flash` · `secret_manager_used: true` ·
`artifact_registry: true` · `cloud_logging_used: true`

Brief note on screen: *"Full stack also runs locally — `docker compose up`, no
API keys required."*

---

### 2:40–2:50 — Circle proof + close

**Screen:** BaseScan transaction, ERC-20 Tokens Transferred row highlighted.

> "And a Circle Agent Wallet payment settled on Base mainnet — founder-funded,
> operator-mediated, independently verifiable on-chain. Pantheon Research: AI
> should not replace the investor. It should compound the investor's discipline."

**On-screen close:**
```text
pantheon-research.com
github.com/0xjacobzhao-byte/pantheon-research-gemini-hackathon
```

---

## Recording notes

- **Ticker scope.** The live product covers GOOGL and a broad universe. The
  local demo ships evidence packs for **MA and NVDA only** — do not imply the
  local demo serves GOOGL.
- **Circle framing.** Say "founder-funded" and "operator-mediated." Do not imply
  autonomy or a recurring treasury.
- **Beta surfaces.** Telegram and email delivery are controlled beta — say so or
  don't dwell on them.

## Key rules

- **Do NOT claim** autonomous trading or model-generated alpha
- **Do NOT claim** investment performance, returns, revenue, or users
- **Do NOT claim** the Pantheon platform was built during the hackathon
- **Do NOT show** any API key, token, credential, or private URL on screen
- **DO emphasize** human-in-the-loop, fail-closed design, evidence provenance,
  and model disagreement
- **DO show** the actual live product, not slides
