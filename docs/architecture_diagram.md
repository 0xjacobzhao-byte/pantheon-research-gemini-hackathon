# Architecture Diagram

> **Scope.** This page shows the **request flow inside this public demo repo**.
> For the production seven-layer architecture and the deployment topology, see
> the two canonical diagrams in the
> [root README](../README.md#architecture).

---

## Gemini analyst request flow

The hackathon path: a governed evidence pack feeds **two independent paths** —
the Gemini analyst overlay, and a Qwen-vs-DeepSeek comparison engine. **Gemini's
output is not an input to the comparator** — `run_comparison()` only ever
receives Qwen and DeepSeek. Both paths are fail-closed and both stop at a human
review gate, but they are structurally separate, not merged into one score.

```text
                    ┌──────────────────────────────────────────┐
                    │  Governed Evidence Pack                   │
                    │  quantitative metrics + provenance        │
                    │  SHA-256 content hash                     │
                    └────────────┬────────────────┬────────────┘
                                 │                │
                    ┌────────────▼───────┐   ┌────▼───────────────────────┐
                    │ ★ GEMINI            │   │  Qwen overlay │ DeepSeek   │
                    │ Analyst/Risk Review │   │  (comparison lanes)        │
                    │ gemini-2.5-flash    │   │  fail-closed, both         │
                    │ fail-closed:        │   └────┬───────────────┬──────┘
                    │  no key  → BLOCKED_ │        │               │
                    │   BY_MISSING_       │        ▼               ▼
                    │   CREDENTIAL        │   ┌─────────────────────────┐
                    │  API error → API_   │   │  comparison.py           │
                    │   ERROR             │   │  agreement · divergence  │
                    │  bad JSON → PARSE_  │   │  tone · data_state       │
                    │   ERROR             │   │  (Qwen vs DeepSeek only) │
                    └──────────┬──────────┘   └────────────┬────────────┘
                               │                            │
                               ▼                            ▼
                    ┌──────────────────────┐   ┌──────────────────────────┐
                    │  Structured Output    │   │  Comparison Result        │
                    │  business quality ·   │   │  agreement level ·        │
                    │  moat · pricing power │   │  tone badges ·            │
                    │  · red flags ·        │   │  divergences ·            │
                    │  confidence ·         │   │  human_review_required    │
                    │  missing evidence     │   └────────────┬─────────────┘
                    └──────────┬────────────┘                │
                               ▼                              ▼
                    ┌──────────────────────┐   ┌──────────────────────────┐
                    │  GeminiOverlayPanel   │   │  OverlayComparisonPanel   │
                    │  (frontend, standalone)│   │  (frontend)               │
                    └──────────┬────────────┘   └────────────┬─────────────┘
                               │                              │
                               └──────────────┬───────────────┘
                                              ▼
                                    Human review — LLMs never trade
```

**Gemini is the primary hackathon analyst layer, displayed standalone.** Qwen
and DeepSeek run the same fail-closed contract as an independent **comparison
engine** — a single provider cannot disagree with itself, which is what makes
divergence detection between them meaningful. Gemini is not folded into that
comparator; its fail-closed states and structured output are visible on their
own.

In production the same evidence pack feeds a **five-provider** comparison
(Claude · ChatGPT · Gemini · DeepSeek · Qwen) with all five participating in one
comparator. This public demo's comparator is smaller — Qwen and DeepSeek, the
two providers it could stand up without private production credentials — with
Gemini shown as a standalone parallel overlay rather than wired into it.

---

## Component flow

```text
Frontend — React + TS + Vite
  GeminiOverlayPanel · OverlayComparisonPanel · DataQualityPanel
        │  /api/*
        ▼
Backend — FastAPI
  sample_loader ──► evidence_pack  (sha256 content hash)
        │
        ├──► gemini_overlay.py    ★ hackathon layer, fail-closed
        ├──► qwen_overlay.py         comparison lane, fail-closed
        └──► deepseek_overlay.py     comparison lane, fail-closed
        │
        ▼
  comparison.py
  data_state · agreement · divergence · evidence gaps · human-review gate
```

---

## Four-layer demo framing

```text
Strategy ──► Information ──► Signal ──► Trading
   │             │             │           │
 thesis &     evidence      Gemini      human-in-the-loop
 universe     pack + hash   overlay +   decision gate
                            comparison  (LLMs never trade)
```

The demo slice collapses production's seven layers into four because it ships
bundled evidence rather than a governed data platform. The production mapping is
in [README § Architecture](../README.md#architecture).

A rendered SVG of the demo component flow is at
[`../assets/architecture_diagram.svg`](../assets/architecture_diagram.svg).
