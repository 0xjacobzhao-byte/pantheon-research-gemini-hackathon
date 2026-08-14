# Architecture — Public Demo Slice

> **Scope note.** This document describes the internal architecture of **this
> repository** — the runnable, judge-facing vertical slice. It is *not* the
> production Pantheon architecture.
>
> For the production system — the **seven layers** and the **five-model**
> research overlay (Claude · ChatGPT · Gemini · DeepSeek · Qwen) — see
> [README §5](../README.md#5-high-level-architecture) and
> [`architecture_diagram.md`](architecture_diagram.md). For representative
> production source, see [`production_reference/`](../production_reference/).

## Overview

This application implements a **Gemini-primary equity qualitative overlay with
secondary multi-provider comparison**. It takes a quantitative equity evidence
pack and produces structured qualitative analysis from Gemini (the hackathon
analyst layer), alongside independent overlays from Qwen Cloud and DeepSeek,
then renders them for comparison with agreement scoring, tone classification,
and divergence detection.

The demo slice carries three providers because those are the three whose
overlays can be generated without private production credentials. Production
runs five.

## System Diagram

```
┌─────────────────────────────────────────────────────────┐
│                     Frontend (React)                     │
│  ┌─────────────┐  ┌──────────────┐  ┌────────────────┐ │
│  │ Ticker      │  │ Evidence     │  │ Side-by-Side    │ │
│  │ Selector    │  │ Panel        │  │ Comparison Grid │ │
│  └─────────────┘  └──────────────┘  └────────────────┘ │
│         │                                    │           │
│         └────────────┬───────────────────────┘           │
│                      │ /api/*                            │
└──────────────────────┼──────────────────────────────────┘
                       │
┌──────────────────────┼──────────────────────────────────┐
│                Backend (FastAPI)                          │
│                      │                                   │
│  ┌───────────────────▼──────────────────────┐            │
│  │           main.py (FastAPI)               │            │
│  │  GET  /                                    │            │
│  │  GET  /health                              │            │
│  │  GET  /api/project                         │            │
│  │  GET  /api/evidence/{ticker}              │            │
│  │  GET  /api/overlay/qwen/{ticker}          │            │
│  │  GET  /api/overlay/deepseek/{ticker}     │            │
│  │  GET  /api/comparison/{ticker}           │            │
│  │  GET  /api/demo-flow                      │            │
│  │  GET  /api/alibaba/proof                   │            │
│  │  GET  /api/alibaba/qwen-config            │            │
│  └───┬───────┬──────────┬───────────────────┘            │
│      │       │          │                               │
│  ┌───▼──┐ ┌──▼───┐ ┌───▼────────────┐                  │
│  │Sample│ │Qwen  │ │DeepSeek         │                  │
│  │Loader│ │Overlay│ │Overlay          │                  │
│  │      │ │      │ │                 │                  │
│  │data/ │ │httpx │ │httpx            │                  │
│  └──────┘ └──┬───┘ └──┬──────────────┘                  │
│              │        │                                   │
│  ┌──────────▼────────▼──────────┐                        │
│  │      comparison.py            │                        │
│  │  Tone · Divergence · Score    │                        │
│  └───────────────────────────────┘                        │
└──────────────┼────────┼───────────────────────────────────┘
               │        │
    ┌──────────▼──┐  ┌──▼──────────────┐
    │  Qwen Cloud  │  │   DeepSeek API   │
    │ (DashScope)  │  │  (OpenAI-comp.)  │
    │ Alibaba Cloud│  │                  │
    └──────────────┘  └──────────────────┘
```

## Demo-Slice Layers

The demo slice collapses the production seven layers into four, because it
ships bundled evidence rather than a governed data platform:

```
Strategy → Information → Signal → Trading
```

1. **Strategy** — Investment thesis and universe selection
2. **Information** — Evidence pack: quantitative metrics, fundamentals, market data
3. **Signal** — Gemini analyst overlay + Qwen/DeepSeek comparison overlays
4. **Trading** — Human-in-the-loop decision gate (LLMs never execute trades)

**Production maps these onto seven layers** — external data sources, a governed
data platform, strategy/research engines, the deterministic + multi-model AI
layer, the information layer, the signal/agent layer, and a separated
trading/execution boundary. See
[README §5](../README.md#5-high-level-architecture).

## Component Responsibilities

### Backend (`backend/`)

| Module                  | Responsibility                                         |
|-------------------------|--------------------------------------------------------|
| `main.py`               | FastAPI app, route definitions, CORS                  |
| `app/models.py`         | Pydantic models: EquityEvidence, OverlayAssessment, QualitativeOverlay, ComparisonResult |
| `app/sample_loader.py`  | Load sample JSON data from `data/`                     |
| `app/qwen_overlay.py`    | Qwen Cloud (DashScope) API integration                 |
| `app/deepseek_overlay.py`| DeepSeek API integration                              |
| `app/comparison.py`     | Tone classification, divergence detection, agreement scoring, full comparison |
| `app/alibaba_cloud_proof.py` | Alibaba Cloud deployment proof endpoints           |

### Frontend (`frontend/`)

| File            | Responsibility                                          |
|-----------------|---------------------------------------------------------|
| `main.tsx`      | React entry point                                       |
| `App.tsx`       | Main app: ticker selector, evidence panel, comparison   |
| `api.ts`        | Typed API client for backend calls                      |
| `style.css`     | Dark theme styling                                       |

## Data Flow

1. User selects a ticker (MA or NVDA)
2. Frontend calls `GET /api/comparison/{ticker}`
3. Backend loads evidence from `data/sample_equity_evidence_{ticker}.json`
4. Backend concurrently calls:
   - `run_qwen_overlay()` → Qwen Cloud `POST /chat/completions` (if `DEMO_MODE != offline`)
   - `run_deepseek_overlay()` → DeepSeek `POST /chat/completions` (if `DEMO_MODE != offline`)
5. If `DEMO_MODE=offline` (default), loads pre-generated sample outputs from `data/`
6. Backend runs comparison logic:
   - **Tone classification** — keyword-based analysis classifies each overlay's tone
   - **Divergence detection** — Jaccard similarity across assessment fields flags major/moderate divergences
   - **Agreement scoring** — weighted score from divergence penalties, tone distance, confidence proximity
   - **Evidence gaps** — merged, deduplicated list from both providers
7. Backend returns `ComparisonResult` with both overlays and comparison metadata
8. Frontend renders side-by-side comparison with badges, scores, and divergence details

## Comparison Fields

Each overlay produces these structured assessment fields:

| Field                  | Description                                    |
|------------------------|------------------------------------------------|
| `business_quality`     | Assessment of overall business quality         |
| `moat`                 | Assessment of moat & competitive advantage     |
| `pricing_power`        | Assessment of pricing power                    |
| `capital_allocation`   | Assessment of management & capital allocation  |
| `red_flags`            | Identified red flags & risks                    |
| `confidence`           | Model confidence (0–1)                         |
| `missing_evidence`     | List of evidence gaps identified by the model  |

## Comparison Output

```json
{
  "ticker": "MA",
  "agreement_score": 0.78,
  "agreement_level": "HIGH",
  "qwen_tone": "conservative_positive",
  "deepseek_tone": "positive",
  "divergences": [],
  "evidence_gaps": [],
  "human_review_required": false
}
```

## Concurrency

Both LLM calls are executed concurrently using `asyncio.gather()`, reducing total latency to the slower of the two providers rather than the sum.

## Error Handling

- Missing credentials → `BLOCKED_BY_MISSING_CREDENTIAL` status (truthful, not faked)
- API errors → `API_ERROR` status with error message
- Offline mode → `OFFLINE_SAMPLE` status
- All statuses are rendered in the frontend with colored badges
- Human review is flagged when agreement is LOW, major divergences exist, or either provider returns a non-SUCCESS status
