# Architecture Diagram

## Request flow (dual-LLM overlay)

```
                         ┌───────────────────────────────────────────┐
                         │  Frontend — React + TS + Vite              │
                         │  OverlayComparisonPanel · DataQualityPanel │
                         └───────────────┬───────────────────────────┘
                                         │  /api/* (Nginx reverse proxy)
                         ┌───────────────▼───────────────────────────┐
                         │  Backend — Dockerized FastAPI              │
                         │                                            │
                         │  sample_loader ──► evidence_pack           │
                         │        │            (sha256 content hash)  │
                         │        ▼                                   │
                         │  ┌───────────────┐   ┌──────────────────┐  │
                         │  │ qwen_overlay  │   │ deepseek_overlay │  │
                         │  │ (fail-closed) │   │  (fail-closed)   │  │
                         │  └──────┬────────┘   └────────┬─────────┘  │
                         │         └───────┬─────────────┘            │
                         │                 ▼                          │
                         │        comparison.py                       │
                         │  data_state · agreement · divergence ·     │
                         │  evidence gaps · human-review gate         │
                         └───────┬───────────────────────┬───────────┘
                                 │                        │
                    ┌────────────▼─────────┐   ┌──────────▼───────────┐
                    │ Alibaba Cloud        │   │ DeepSeek API         │
                    │ DashScope (Qwen)     │   │ (OpenAI-compatible)  │
                    │ dashscope-intl…/v1   │   │                      │
                    └──────────────────────┘   └──────────────────────┘
```

## Four-layer research framework

```
Strategy ──► Information ──► Signal ──► Trading
   │             │             │           │
 thesis &     evidence      dual-LLM     human-in-the-loop
 universe     pack + hash   overlay +    decision gate
                            comparison   (LLMs never trade)
```

A rendered SVG version is at [`../assets/architecture_diagram.svg`](../assets/architecture_diagram.svg).
