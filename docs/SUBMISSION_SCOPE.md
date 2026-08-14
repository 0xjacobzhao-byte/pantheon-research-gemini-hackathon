# Submission Scope — What Pre-Existed and What Was Built

> **Pantheon Research existed before this hackathon.** This document draws that
> line explicitly, because a submission that blurs it is not worth judging.

Snapshot date: **2026-08-14**. Every claim below is anchored to a commit, an
on-chain transaction, or a live endpoint — not to narrative.

---

## 1. The short version

| | |
|---|---|
| **Pre-existing** | The Pantheon Research product, brand, live site, private production repository, governed data platform, deterministic research engines, and the multi-provider LLM research lane. |
| **Built during the submission period** | The Gemini Analyst / Risk-Review layer, its Google Cloud deployment and proof surface, the judge-facing public repository, the Circle Agent Wallet on-chain payment proof, and this submission evidence package. |

Pantheon is not a hackathon project with a product bolted on, and this submission
does not claim it is. It is a pre-existing research operating system with a
**new, independently verifiable Gemini + Google Cloud layer** and a **new Circle
agentic-payment rail** built on top during the submission window.

---

## 2. Pre-existing Pantheon foundation

None of the following was created for this hackathon. All of it predates the
submission period and is reused as permitted infrastructure.

| Foundation | State before the submission period |
|---|---|
| Pantheon Research concept, product definition, and brand | Established; live at [pantheon-research.com](https://pantheon-research.com) |
| Private production repository | Established, with production history far exceeding the submission window |
| Versioned investment frameworks (Macro, Equities, BTC, ETH, DeFi, FICC, TA, Narrative) | Established and in production |
| Governed data platform — canonical observations, provider routing, freshness/TTL, data-quality labelling, evidence artifacts | Established and in production |
| Deterministic research and signal engines | Established and in production |
| Multi-provider LLM research overlay (Claude · ChatGPT · DeepSeek · Qwen) | Established; **Gemini was added to this existing lane** |
| Evidence-backed vs. model-inferred lane separation | Established and in production |
| Production deployment substrate (Vercel frontend + Railway backend + PostgreSQL) | Established and in production |
| Backtest and forward-validation infrastructure | Established and in production |
| Telegram / report delivery surfaces | Established and in production |

**Reuse disclosure.** The legal entity, the existing audience, the existing
production infrastructure, and generic data-pipeline / deployment / UI
frameworks and code are reused. That reuse is disclosed here rather than
disguised.

---

## 3. Work added or materially advanced during the submission period

Each row is evidenced. Nothing here is asserted without a commit, a transaction,
or a live endpoint behind it.

### 3.1 Gemini Analyst / Risk-Review layer — 2026-07-08

| Item | Evidence |
|---|---|
| Gemini overlay backend, proof endpoint, offline samples, UI panel | commit `bf61c43` |
| Gemini submission materials and verification pack | commits `947e8a2`, `63b5971` |
| Fail-closed Gemini API path (`BLOCKED_BY_MISSING_CREDENTIAL` / `API_ERROR` / `PARSE_ERROR`) | [`backend/app/gemini_overlay.py`](../backend/app/gemini_overlay.py) |
| Structured evidence-pack → Gemini workflow with SHA-256 provenance | [`backend/app/evidence_pack.py`](../backend/app/evidence_pack.py) |
| Gemini proof endpoint (secret-free, no external calls) | [`backend/app/gemini_proof.py`](../backend/app/gemini_proof.py) |

### 3.2 Google Cloud deployment — 2026-07-08

| Item | Evidence |
|---|---|
| Cloud Run deployment infrastructure and deploy script | commit `d9c64c2` |
| Cloud Run service live and verified | commits `a348c0f`, `fb89511`, `e6f5927` |
| Google Cloud proof endpoint + Secret Manager binding | commit `f9422db` |
| Live Gemini API call verified on Google Cloud | commit `d031d14`, [`data/gemini_live_call_redacted.json`](../data/gemini_live_call_redacted.json) |
| Artifact Registry, Secret Manager, Cloud Logging | [live proof endpoint](https://pantheon-gemini-549837878368.asia-southeast1.run.app/api/proof/google-cloud) |

Google Cloud resources for this service (service account, secret, artifact
image) were created **2026-07-08** — inside the submission period.

### 3.3 Judge-facing public repository — 2026-07-08 onward

This repository itself is submission-period work: a sanitized, runnable,
security-reviewed slice that lets a judge verify the Gemini integration without
private access.

### 3.4 Circle Agent Wallet on-chain payment proof — 2026-08-11 → 2026-08-13

| Item | Evidence |
|---|---|
| Agent Treasury design, Stage 0/1 testnet controls (no money) | private PRs `#1870`, `#1871` |
| Stage 2 gated mainnet enablement + policy versioning | private PR `#1873` |
| Stage 2 on-chain proof verifier | private PR `#1874` |
| Stage 2 audit closeout and risk acceptance | private PRs `#1879`–`#1883` |
| **Mainnet USDC payment executed and independently verified** | tx [`0x699bbb9d…eac6e3`](https://basescan.org/tx/0x699bbb9ddb03f9a98525749374fb976a9cd7ef6319414d1cb5e422d810eac6e3), Base block `49907662`, 2026-08-13T07:04:31Z |
| Public Circle evidence package | commit `ad90800`, [`docs/circle_agentic_economy_evidence.md`](circle_agentic_economy_evidence.md) |

### 3.5 Submission evidence package — 2026-08-13 / 2026-08-14

[`PRODUCT_EVIDENCE_INDEX.md`](PRODUCT_EVIDENCE_INDEX.md),
[`production_reference/`](../production_reference/), this document, and the
reconciliation of the public documentation set against production truth.

---

## 4. What this submission does *not* claim

- ❌ That the Pantheon platform was built during the hackathon. It was not.
- ❌ That the research engines, data platform, or frameworks are new work.
- ❌ That the four non-Gemini LLM providers were integrated for this submission.
- ❌ That production trading, autonomous execution, or realized alpha exists.
- ❌ That any revenue, user, or profit figure was achieved. Revenue is **$0**;
  verified external users are **0**; paying users are **0**. See
  [`business_model_and_pnl.md`](business_model_and_pnl.md).

---

## 5. Attribution of the AI layer

Gemini is a **new provider added to a pre-existing four-model research lane**
(Claude · ChatGPT · DeepSeek · Qwen), making the resulting stack five-model,
plus a new Google Cloud deployment and proof surface. The lane it joined —
schema validation, evidence tiering, overlay comparison, human-review gating —
pre-existed. That is stated plainly so a judge can weight the Gemini
contribution correctly rather than over- or under-crediting it.

What is genuinely new and independently verifiable by a judge, without private
access:

1. A live Gemini `gemini-2.5-flash` integration on Google Cloud Run with
   Secret Manager, Artifact Registry, and Cloud Logging.
2. A fail-closed Gemini path with three distinct, tested failure states.
3. A mainnet Circle Agent Wallet USDC payment, verifiable from public chain data
   alone.
4. This repository — runnable end-to-end with no credentials.

---

## 6. Related documents

- [`README.md`](../README.md) — product and architecture
- [`PRODUCT_EVIDENCE_INDEX.md`](PRODUCT_EVIDENCE_INDEX.md) — claim → evidence map
- [`gemini_production_evidence.md`](gemini_production_evidence.md) — Gemini/GCP verification
- [`circle_agentic_economy_evidence.md`](circle_agentic_economy_evidence.md) — Circle proof and limitations
- [`business_model_and_pnl.md`](business_model_and_pnl.md) — actual hackathon-period P&L
