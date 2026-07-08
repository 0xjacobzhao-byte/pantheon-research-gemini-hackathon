# Pantheon Research — Gemini Hackathon

> Gemini-powered investment research overlay for human-in-the-loop financial decision intelligence.

A sanitized, judge-facing vertical slice of the private Pantheon Research production system — with a **Gemini-powered Analyst / Risk-Review layer** built during the hackathon period. Not an API wrapper. Not an autonomous trading system.

> **Judges:** start with the [3-Minute Judge Path](#3-minute-judge-path) below, then read [docs/gemini_production_evidence.md](docs/gemini_production_evidence.md) for reproducible verification.

---

## One-Line Pitch

Pantheon Research uses Google Gemini to convert structured quantitative evidence packs into explainable financial research overlays — helping human analysts make better-informed decisions, faster.

---

## Submission Links

| | |
|---|---|
| 💻 GitHub Repo | https://github.com/0xjacobzhao-byte/pantheon-research-gemini-hackathon |
| 🌐 Live Product | https://pantheon-research.com |
| ☁️ Google Cloud Run | https://pantheon-gemini-549837878368.asia-southeast1.run.app |
| 📄 Product-Running Evidence | [docs/gemini_production_evidence.md](docs/gemini_production_evidence.md) |
| 📈 Business Model / P&L | [docs/business_model_and_pnl.md](docs/business_model_and_pnl.md) |
| 📖 Project Story | [docs/project_story.md](docs/project_story.md) |

---

## 3-Minute Judge Path

1. **Run the local demo:**
   ```bash
   docker compose up --build          # frontend :5173 · backend :8000
   ./scripts/judge_smoke.sh           # end-to-end smoke test (offline, no secrets)
   ```

2. **Verify Gemini proof:**
   ```bash
   curl -s http://localhost:8000/api/proof/gemini | jq
   ```

3. **Verify Gemini overlay:**
   ```bash
   curl -s http://localhost:8000/api/overlay/gemini/NVDA | jq
   ```

4. **Verify Google Cloud deployment (live):**
   ```bash
   curl -s https://pantheon-gemini-549837878368.asia-southeast1.run.app/api/proof/google-cloud | jq
   ```

5. **Inspect Gemini API implementation:**
   [`backend/app/gemini_overlay.py`](backend/app/gemini_overlay.py)

6. **Read evidence docs:**
   [`docs/gemini_production_evidence.md`](docs/gemini_production_evidence.md)

---

## Repository Scope

The underlying **Pantheon Research platform existed before the hackathon**. The submitted Gemini-specific feature layer — **Gemini Analyst / Gemini Risk Review** — was developed during the hackathon period.

The complete production codebase lives in the private Pantheon Research repository:

https://github.com/0xjacobzhao-byte/Pantheon-Research

It remains closed-source to protect proprietary trading-strategy IP, provider integrations, operational runbooks, and production data infrastructure. Gemini Hackathon judges may request temporary private access from Jacob Zhao if needed.

---

## Quick Start

```bash
git clone https://github.com/0xjacobzhao-byte/pantheon-research-gemini-hackathon
cd pantheon-research-gemini-hackathon
docker compose up --build          # frontend :5173 · backend :8000
./scripts/judge_smoke.sh           # end-to-end smoke test (offline, no secrets)
```

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

---

## Gemini Integration

| Property | Value |
|----------|-------|
| Provider | Google Gemini API (Generative Language API v1beta) |
| Model | `gemini-2.5-flash` (configurable via `GEMINI_MODEL`) |
| Auth | API key (`GEMINI_API_KEY` or `GOOGLE_API_KEY`) |
| Protocol | REST generateContent with JSON response mode |
| Default Mode | **Offline** — bundled samples, no API key required |

### Fail-Closed Design

| Condition | Status | Behavior |
|-----------|--------|----------|
| No API key | `BLOCKED_BY_MISSING_CREDENTIAL` | No call made, no fake result |
| API error | `API_ERROR` | Retry with backoff, then report |
| Non-JSON response | `PARSE_ERROR` | Report immediately, no retry |
| Offline mode | `OFFLINE_SAMPLE` | Bundled samples from `data/gemini_samples/` |

**Gemini never returns a fake SUCCESS.** Every failure mode maps to an explicit, distinct status.

### Live Mode

Set `DEMO_MODE=live` + `GEMINI_API_KEY` (or `GOOGLE_API_KEY`) for live Gemini API calls. Without credentials, the demo runs end-to-end using bundled offline samples.

---

## Product Demo Flow

1. **Select Ticker** — Choose MA (Mastercard) or NVDA (NVIDIA)
2. **Load Evidence Pack** — Backend loads structured quantitative metrics from `data/`
3. **Gemini Analyst Overlay** — Gemini generates a structured qualitative assessment with takeaway, business quality, moat, pricing power, capital allocation, red flags, confidence score, and missing evidence
4. **Qwen vs DeepSeek Comparison** — Two additional models provide independent overlays for secondary comparison context
5. **Human Review Gate** — Low agreement or major divergences flag human review; LLMs never execute trades

---

## API Endpoints

<details>
<summary><b>Key Gemini endpoints</b></summary>

| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/overlay/gemini/{ticker}` | Gemini qualitative overlay |
| GET | `/api/proof/gemini` | Gemini proof (secret-free, no external calls) |
| GET | `/api/proof/google-cloud` | Google Cloud deployment proof (secret-free) |
| GET | `/api/proof/gcp` | GCP Cloud Run metadata proof |

</details>

<details>
<summary><b>Full endpoint reference</b></summary>

| Method | Path | Description |
|--------|------|-------------|
| GET | `/` | Root info |
| GET | `/health` | Health check |
| **Gemini** | | |
| GET | `/api/overlay/gemini/{ticker}` | Gemini qualitative overlay |
| GET | `/api/proof/gemini` | Gemini proof (secret-free) |
| **Core** | | |
| GET | `/api/project` | Project metadata |
| GET | `/api/evidence/{ticker}` | Evidence pack + provenance |
| GET | `/api/overlay/qwen/{ticker}` | Qwen overlay (secondary) |
| GET | `/api/overlay/deepseek/{ticker}` | DeepSeek overlay (secondary) |
| GET | `/api/comparison/{ticker}` | Dual-provider comparison |
| **Platform** | | |
| GET | `/api/proof/alibaba-cloud` | Deployment proof |
| GET | `/api/data-quality` | Research-Ops governance |
| GET | `/api/modules` | Module snapshot grid |
| GET | `/api/provider-health` | Provider health |

</details>

---

## Business Model & P&L

See [docs/business_model_and_pnl.md](docs/business_model_and_pnl.md) for pricing model, 5-year projections, and path to profitability. No realized profit is claimed for this hackathon submission.

---

## Safety / Human-in-the-Loop

- **LLMs do not execute trades.** A human remains the portfolio manager.
- **Gemini outputs are research overlays**, not trade signals, not alpha, not investment advice.
- **Every signal passes a human-review gate.** Low agreement or major divergences flag mandatory human review.
- **Pantheon Research is not an autonomous trading bot.** It is a framework-first, data-governed, human-in-the-loop AI research operating system.

---

## Architecture

```
Strategy ──▶ Information ──▶ Signal ──▶ Trading
```

| Layer | Role |
|-------|------|
| **Strategy** | Investment thesis and universe selection |
| **Information** | Evidence pack: quantitative metrics, fundamentals, market data |
| **Signal** | Gemini Analyst overlay + Qwen/DeepSeek comparison overlays |
| **Trading** | Human-in-the-loop decision gate (LLMs never execute trades) |

---

## Tests

```bash
cd backend && python -m pytest            # 126 backend tests
cd frontend && npm test -- --run          # 11 frontend tests
cd frontend && npm run build              # production build
```

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | FastAPI · Python 3.11–3.12 |
| Frontend | React 18 · TypeScript · Vite 6 |
| LLM (Gemini) | Google Gemini API (Generative Language API v1beta) |
| LLM (Qwen) | Alibaba Cloud DashScope (secondary comparison) |
| LLM (DeepSeek) | DeepSeek API (secondary comparison) |
| Database | PostgreSQL — production only |
| Deploy (local) | Docker Compose |
| Deploy (cloud) | Google Cloud Run · Artifact Registry · Secret Manager · Cloud Logging |
| Tests | pytest (backend) · vitest + Testing Library (frontend) |

---

## Author & License

**Jacob Zhao** — [0xjacobzhao-byte](https://github.com/0xjacobzhao-byte)

**License:** Apache-2.0 — see [LICENSE](LICENSE)

No API keys, private user data, live trading credentials, production secrets, or private financial records are included in this repository.
