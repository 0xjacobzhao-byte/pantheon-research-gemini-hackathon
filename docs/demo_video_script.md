# Demo Video Script — Pantheon Research Gemini Hackathon

> **Target length:** 2:30–2:50
> **Tone:** Professional, concise, product-focused. No alpha claims. No autonomous trading claims.

---

## Footage Plan

### 0:00–0:15 — Title / README

**Screen:** GitHub repo README, scrolled to the top.

**Voiceover:**
> "Pantheon Research — Gemini-powered investment research overlay for human-in-the-loop financial decision intelligence. Built for the Gemini Hackathon."

---

### 0:15–0:45 — Local Web App Running

**Screen:** Terminal running `docker compose up --build`, then browser opening `http://localhost:5173`.

**Voiceover:**
> "The entire demo runs locally with Docker. No API keys required in offline mode. The frontend loads the Gemini integration panel, module snapshots, and the analysis interface."

**Actions:**
- Show the frontend homepage loading
- Scroll past the Gemini Integration proof banner
- Show the architecture layers (Strategy → Information → Signal → Trading)

---

### 0:45–1:30 — Gemini Overlay for NVDA

**Screen:** Click "NVDA" ticker, then "Run Analysis."

**Voiceover:**
> "Let's analyze NVIDIA. The backend loads a structured evidence pack with P/E, ROIC, margins, and growth data. Then Gemini generates a qualitative overlay — business quality, moat, pricing power, capital allocation, red flags, and a confidence score."

**Actions:**
- Click NVDA
- Click Run Analysis
- Scroll to the **Gemini Analyst Overlay** section
- Highlight the takeaway, assessment fields, confidence bar, and missing evidence
- Pause on the confidence score and red flags

---

### 1:30–1:55 — Evidence Pack / Human Review / Safety

**Screen:** Scroll to Evidence Pack section, then to Qwen vs DeepSeek comparison.

**Voiceover:**
> "Every evidence pack is hashed with SHA-256 for provenance. The Qwen and DeepSeek overlays provide secondary comparison context. When models disagree, the system flags human review. LLMs never execute trades — a human portfolio manager always makes the final decision."

**Actions:**
- Show evidence pack with hash
- Show divergence section in comparison panel
- Show human review banner if present

---

### 1:55–2:15 — Gemini Proof Endpoint

**Screen:** Terminal with curl command.

```bash
curl -s http://localhost:8000/api/proof/gemini | jq
```

**Voiceover:**
> "The Gemini proof endpoint returns secret-free metadata — model, credential state, safe claims, and non-claims. It makes no external calls and returns no secrets."

**Actions:**
- Run the curl command
- Highlight `schema_version`, `provider`, `model`, `credential_configured`, `proof_endpoint_external_calls: false`

---

### 2:15–2:35 — GitHub Code

**Screen:** GitHub repo, navigating to key files.

**Voiceover:**
> "The Gemini API call is implemented in `backend/app/gemini_overlay.py` — fail-closed by design with three explicit error modes. Evidence docs and production evidence are in the `docs/` folder."

**Actions:**
- Show `backend/app/gemini_overlay.py` — scroll through the fail-closed statuses
- Show `data/gemini_samples/` directory
- Show `docs/gemini_production_evidence.md`

---

### 2:35–2:50 — Business Model / Closing

**Screen:** `docs/business_model_and_pnl.md` scrolled to P&L table.

**Voiceover:**
> "Pantheon Research targets $5M to $10M ARR in five years through subscription SaaS and B2B API access. The business model is research tooling — not trading performance. Gemini amplifies human judgment; it doesn't replace it."

**Actions:**
- Show P&L projection table
- Fade to repo URL and license

---

## Key Rules

- **Do NOT claim** autonomous trading or model-generated alpha
- **Do NOT claim** investment performance or returns
- **Do NOT show** any API keys, tokens, or credentials on screen
- **Do NOT claim** the entire Pantheon Research platform was built during the hackathon
- **DO emphasize** human-in-the-loop, fail-closed design, and evidence provenance
- **DO show** actual product running (not just slides)
