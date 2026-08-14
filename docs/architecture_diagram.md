# Architecture Diagram

> **Scope.** This page shows the **request flow inside this public demo repo**.
> For the production seven-layer architecture and the deployment topology, see
> the two canonical diagrams in the
> [root README](../README.md#architecture).

---

## Gemini analyst request flow

The hackathon path: a governed evidence pack becomes a structured, schema-validated
analyst overlay, is compared against other providers, and stops at a human review
gate.

```text
                    ┌──────────────────────────────────────────┐
                    │  Governed Evidence Pack                   │
                    │  quantitative metrics + provenance        │
                    │  SHA-256 content hash                     │
                    └────────────────────┬─────────────────────┘
                                         │
                                         ▼
                    ┌──────────────────────────────────────────┐
                    │  ★ GEMINI — Analyst / Risk Review         │
                    │  gemini-2.5-flash · JSON response mode    │
                    │  fail-closed:                             │
                    │    no key   → BLOCKED_BY_MISSING_CREDENTIAL│
                    │    API error→ API_ERROR                    │
                    │    bad JSON → PARSE_ERROR                  │
                    └────────────────────┬─────────────────────┘
                                         │
                                         ▼
                    ┌──────────────────────────────────────────┐
                    │  Structured Output                        │
                    │  business quality · moat · pricing power  │
                    │  capital allocation · red flags           │
                    │  confidence · missing evidence            │
                    └────────────────────┬─────────────────────┘
                                         │
                                         ▼
                    ┌──────────────────────────────────────────┐
                    │  Multi-Model Comparison                   │
                    │  agreement · divergence · tone            │
                    │  evidence discipline · data_state         │
                    └───────┬──────────────────────────┬───────┘
                            │                          │
              secondary ────┤                          │
              comparison    ▼                          ▼
              lanes  ┌───────────────┐        ┌────────────────┐
                     │ Qwen overlay  │        │ DeepSeek       │
                     │ (DashScope)   │        │ overlay        │
                     │ fail-closed   │        │ fail-closed    │
                     └───────────────┘        └────────────────┘
                            │                          │
                            └────────────┬─────────────┘
                                         ▼
                    ┌──────────────────────────────────────────┐
                    │  HUMAN REVIEW GATE                        │
                    │  low agreement or major divergence        │
                    │  → mandatory human review                 │
                    └────────────────────┬─────────────────────┘
                                         ▼
                              Human decision — LLMs never trade
```

**Gemini is the primary hackathon analyst layer.** Qwen and DeepSeek run the
same fail-closed contract as **secondary comparison lanes**, which is what makes
divergence detection meaningful — a single provider cannot disagree with itself.

In production the same pipeline runs **five** providers (Claude · ChatGPT ·
Gemini · DeepSeek · Qwen). This public demo ships the three whose overlays can be
served without private production credentials.

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
