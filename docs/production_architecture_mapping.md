# Production Architecture Mapping

This public repo is a **sanitized, reproducible vertical slice** of the private
production Pantheon Research system. It is deliberately small enough to run from
scratch in minutes, while faithfully mirroring the real **Gemini analyst
integration** (the hackathon layer) and its multi-model comparison context. This
document maps each public file to its production counterpart and states what is
intentionally excluded and why.

## System at a glance

| Layer | Production (private) | This public repo |
| --- | --- | --- |
| Frontend | React + Vite SPA on **Vercel** (`pantheon-research.vercel.app`), ~40 route modules | React + Vite SPA, single Ticker-Profile comparison view |
| Backend | FastAPI on **Railway**, ~200 routers (equities, macro, BTC/ETH, FICC, research-ops) | FastAPI, the overlay + proof endpoints only |
| Database | **Railway Postgres** (`product_snapshots` + ~60 tables), 1,300+ equity overlays | none required — bundled sample JSON (offline) |
| LLM overlay | **Five providers** — Claude · ChatGPT · Gemini · DeepSeek · Qwen (Alibaba DashScope) — batch-generated, schema-validated, DB-persisted | **Gemini** (hackathon analyst layer) + Qwen and DeepSeek comparison lanes, request-time, offline samples by default |
| Gemini deployment | Integrated in the production overlay lane | Independently deployed on **Google Cloud Run** with Artifact Registry, Secret Manager, Cloud Logging — live proof endpoints |

## File-by-file mapping

| Public file | Production counterpart | Notes |
| --- | --- | --- |
| `backend/app/gemini_overlay.py` | Gemini provider client + overlay service in the production five-model lane | **The hackathon layer.** Same `generateContent` call against the Generative Language API v1beta with JSON response mode, same `GEMINI_API_KEY` / `GOOGLE_API_KEY` resolution, same fail-closed status set. Production adds evidence-pack construction, prompt-versioning, and DB persistence. |
| `backend/app/gemini_proof.py`, `google_cloud_proof.py` | — (public-only) | Secret-free proof surface built for judge verification; makes no external calls and returns booleans only. |
| `backend/app/qwen_overlay.py` | `backend_gateway/providers/qwen_client.py` + `services/equity_qwen_overlay.py` | Same DashScope OpenAI-compatible call (`dashscope-intl.aliyuncs.com/compatible-mode/v1`), same env-var resolution (`DASHSCOPE_API_KEY` / `QWEN_API_KEY`), same fail-closed + `PARSE_ERROR` handling. |
| `backend/app/deepseek_overlay.py` | `backend_gateway/providers/deepseek_client.py` | Symmetric DeepSeek path. |
| `backend/app/comparison.py` | `backend_gateway/services/equity_overlay_comparison.py` | Public repo uses tone/Jaccard heuristics; production compares persisted factor verdicts (`moat_pricing_power`, `red_flags`, …) across providers and emits `data_state` (`HEALTHY_REAL_DATA`, `QWEN_NOT_GENERATED`, …). |
| `frontend/.../OverlayComparison*` | `frontend/components/equity/OverlayComparisonPanel.tsx` | Production panel renders unconditionally inside the Ticker Profile cockpit and fetches `/api/equity/overlay-comparison/{market}/{ticker}`. |
| `backend/tests/*` | `backend_gateway/tests/test_overlay_comparison.py` + `test_qwen_cloud_provider.py` | Public repo: overlay proof / fail-closed / data-state / evidence-pack / comparison coverage. |

## Intentionally excluded (and why)

- **Proprietary data pipelines** (market-data ingestion, evidence-pack builders,
  provider routing, scoring models) — the moat, and not needed to demonstrate the
  Qwen integration.
- **Production database + real overlay rows** — would require credentials and
  leak proprietary research. Replaced by realistic bundled samples.
- **Secrets / infra config** — no `.env`, no connection strings, no keys. Only
  `.env.example` with placeholders.
- **The other ~40 frontend modules and ~200 routers** — out of scope for a
  judging demo; they don't change the Qwen story.

## What is faithfully preserved

- **The Gemini call path** — `generateContent` with JSON response mode, the same
  credential resolution, and the same three fail-closed statuses used in
  production.
- The DashScope OpenAI-compatible call path and credential resolution for the
  Qwen comparison lane.
- The multi-provider comparison model with explicit, non-`SUCCESS` states for
  missing or failed generations, and the human-review gate on low agreement.
