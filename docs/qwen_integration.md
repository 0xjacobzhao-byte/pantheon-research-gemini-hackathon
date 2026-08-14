# Qwen Integration — Comparison Provider

> **Scope.** Qwen is a **secondary comparison provider** in this submission. The
> primary hackathon AI layer is **Gemini** — see
> [README § Gemini](../README.md#gemini--the-hackathon-ai-layer) and
> [`gemini_production_evidence.md`](gemini_production_evidence.md).
>
> This page documents the Qwen integration specifically, because a comparison
> lane is only meaningful if it is real and independently implemented.

## Overview

Pantheon integrates **Qwen** via Alibaba Cloud's DashScope API in
OpenAI-compatible mode. In production Qwen is one of **five** research providers
(Claude · ChatGPT · Gemini · DeepSeek · Qwen); in this public demo it runs
alongside DeepSeek as an independent comparison lane against the Gemini analyst
overlay, under the same fail-closed contract.

## API Details

| Property     | Value                                                        |
|--------------|-------------------------------------------------------------|
| Base URL     | `https://dashscope-intl.aliyuncs.com/compatible-mode/v1`   |
| Endpoint     | `POST /chat/completions`                                    |
| Auth         | Bearer token (`DASHSCOPE_API_KEY`)                         |
| Model        | `qwen-plus` (configurable via `QWEN_MODEL` env var)        |
| Format       | OpenAI-compatible JSON                                      |

## Authentication

The DashScope API key is passed as a Bearer token in the `Authorization` header:

```
Authorization: Bearer <DASHSCOPE_API_KEY>
```

The key is loaded from the `DASHSCOPE_API_KEY` environment variable. No keys are hardcoded in the repository.

## Request Format

The backend builds a prompt from the equity evidence data and sends it as a chat completion request:

```json
{
  "model": "qwen-plus",
  "messages": [
    {
      "role": "user",
      "content": "You are a senior equity research analyst. Based on the following quantitative evidence, produce a structured qualitative overlay..."
    }
  ],
  "temperature": 0.7
}
```

## Response Parsing

The response follows the OpenAI chat completions format. The `content` field from `choices[0].message.content` is parsed as JSON into a structured `OverlayAssessment` with these fields:

| Field                  | Type        | Description                                    |
|------------------------|-------------|------------------------------------------------|
| `takeaway`             | string      | One-paragraph summary                          |
| `business_quality`     | string      | Assessment of business quality                |
| `moat`                 | string      | Assessment of moat & competitive advantage     |
| `pricing_power`        | string      | Assessment of pricing power                   |
| `capital_allocation`   | string      | Assessment of management & capital allocation  |
| `red_flags`            | string      | Identified red flags & risks                   |
| `confidence`           | float (0–1) | Model confidence                               |
| `missing_evidence`     | list[str]   | Evidence gaps identified by the model          |

## Credential Handling

- **Default mode is offline** — no API key required. The app uses bundled sample data in `data/`.
- If `DEMO_MODE=offline` (default), pre-generated sample outputs are loaded from `data/sample_qwen_output_{ticker}.json`
- If `DEMO_MODE=live` and `DASHSCOPE_API_KEY` is not set, the overlay returns `BLOCKED_BY_MISSING_CREDENTIAL` status
- The frontend truthfully renders this status — it does not fake results

## Configuration Endpoint

The `GET /api/qwen-config` endpoint returns the current Qwen/DashScope configuration:

```json
{
  "provider": "Alibaba Cloud DashScope (Model Studio)",
  "base_url": "https://dashscope-intl.aliyuncs.com/compatible-mode/v1",
  "model": "qwen-plus",
  "integration_type": "OpenAI-compatible chat completions",
  "prompt_version": "qwen-overlay-v1.1",
  "output_schema_version": "overlay-assessment-1.0",
  "credential_configured": false,
  "demo_mode": "offline"
}
```

## Alternative Base URLs

The following official Alibaba Cloud MaaS endpoints are also supported:

- `https://dashscope-intl.aliyuncs.com/compatible-mode/v1` (default, international)
- `https://token-plan.ap-southeast-1.maas.aliyuncs.com/compatible-mode/v1` (Singapore region MaaS)

## Code Reference

- Integration: `backend/app/qwen_overlay.py`
- Models: `backend/app/models.py`
- Sample data: `data/sample_qwen_output_ma.json`, `data/sample_qwen_output_nvda.json`
