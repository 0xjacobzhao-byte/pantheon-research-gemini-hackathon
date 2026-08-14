# Production Reference

> These are sanitized representative production references copied from the
> private Pantheon Research production repository for judge verification.
>
> **They are not the complete production codebase.**
>
> Secrets, provider configuration, operational security details, customer data,
> and proprietary strategy logic have been removed.

Snapshot date: **2026-08-14**.

---

## Why this directory exists

The rest of this repository is a runnable Gemini vertical slice. That proves the
Gemini integration works, but it does not prove Pantheon is more than an LLM
wrapper — a judge would have to take that on trust.

These five files are the evidence for the claims that are otherwise unverifiable
from outside. Each was selected because it makes a specific architectural claim
**checkable**, and because it could be published without releasing strategy IP.

Files were chosen for evidential value, not volume. This is deliberately a small
set.

---

## What is here

| File | Proves | Lines | Deps |
|---|---|---|---|
| [`evidence_tier.py`](evidence_tier.py) | Evidence governance — source-backed research is graded and kept structurally distinct from AI priors | 767 | stdlib only |
| [`advice_policy.py`](advice_policy.py) | The advice-vs-execution boundary — AI may state views, may not operate a trade | 446 | stdlib only |
| [`overlayComparison.ts`](overlayComparison.ts) | The multi-model comparison contract — disagreement is surfaced, not averaged | 467 | none (deps stubbed) |
| [`freshness_policy.py`](freshness_policy.py) | Data-freshness governance — stale data is labelled per module, never silently served | 271 | stdlib only |
| [`valuation_outlier_review_service.py`](valuation_outlier_review_service.py) | Human review — outliers reach a human, and the reader changes nothing | 165 | stdlib only |

None of these files opens a network connection, reads a credential, touches a
database, or executes a trade.

---

## What each one demonstrates

### `evidence_tier.py` — evidence governance

Deterministic, pure post-processing that maps source-pack metadata and factor
mix to one of five graded evidence tiers.

The hard rules encoded here are the point:

- Tier is computed from **source-pack metadata only**. The LLM payload is never
  re-graded by the model that produced it.
- Weak tiers **force** the allowed modifier to zero. A tier can never unlock a
  conclusion the evidence does not support.
- `NO_USABLE_EVIDENCE` maps to `insufficient_evidence` — the system is allowed
  to refuse to conclude.
- No BUY/SELL/HOLD vocabulary may appear in any tier label or reason.

Supports: README §8, "Two explicitly separated lanes".

### `advice_policy.py` — the AI boundary

The authoritative advice-versus-execution rule, in code:

```text
ADVICE     = ALLOWED
EXECUTION  = NOT AUTHORIZED
```

Pantheon **is expected to** state investment opinions, ratings, direction, entry
attractiveness, risk/reward, and invalidation conditions. Refusing to state a
view because it is actionable would be refusing to do the job.

Pantheon must **not** place orders, submit broker instructions, modify or cancel
orders, sign transactions, execute automatic trades — or claim to have done any
of those things. The refused classes are enumerated and each is justified as
execution rather than advice, including personalized position sizing, which is
refused deliberately so the model layer cannot publish a magnitude the
deterministic layer withholds.

The Agent has no order path, no broker credential, and no signing key.

Supports: README §9 and §16.

### `overlayComparison.ts` — multi-model comparison

The client contract for the five-provider comparison surface. What it carries
matters more than the fetch:

- Every provider reports its own state — a failed or skipped provider stays
  **visible** rather than being dropped, because a silently absent provider
  reads as agreement.
- `MajorDivergence` is a first-class field, not an error path.
- `AnalysisLane` separates `evidence_backed` from `model_inferred`.
- `MultiComparisonStatus` can be `NOT_COMPARABLE` — when providers answered
  different questions, the correct output is a refusal to compare, not a
  fabricated agreement score.

Supports: README §8, "Disagreement is surfaced, not averaged away".

### `freshness_policy.py` — data governance

The per-module TTL registry. Every research module declares how fresh its data
is *supposed* to be, and actual age is measured against that declaration rather
than a global default — a monthly fixed-income framework and an intraday crypto
framework share no useful default.

Two thresholds, not one: `SOFT_STALE` is still served but **labelled**, and the
label reaches the user; `HARD_STALE` has failed its own freshness contract.
`stale_root_cause` makes a stale module an explained condition rather than an
anonymous gap.

Supports: README §7.

### `valuation_outlier_review_service.py` — human review

A strictly read-only reader that surfaces pre-computed outlier flags to the
operator review dashboard. No DB, no provider HTTP, no LLM, no network, no model
recomputation.

The caveats are carried in the payload itself: the dashboard changes no rating,
no fair value, no recommendation; outliers are descriptive triggers for human
review, not assertions that the model is wrong; and a data gap is never bearish.

Supports: README §9, human-review escalation.

---

## A note on internal path references

These files retain occasional references to sibling modules and contract
documents by their **private-repository path** — for example
`backend_gateway/services/...`, `docs/equities_llm_overlay/...`, or Sphinx-style
`:mod:` cross-references.

Those paths are **not resolvable in this repository** and are left in place
deliberately: they show where each contract is actually enforced, and rewriting
them would misrepresent the source. They describe application source-tree
layout, not infrastructure, and expose no credential, endpoint, or operational
topology.

---

## What was removed

| File | Removed |
|---|---|
| `freshness_policy.py` | Upstream provider names and routing, credential environment-variable names, hosting and database topology, internal recovery-runbook paths, internal PR references, live coverage statistics |
| `overlayComparison.ts` | Deployment-target references; two internal imports replaced with local declarations so the file reads standalone |
| `evidence_tier.py` | Nothing — published unchanged below the provenance header |
| `advice_policy.py` | Nothing — published unchanged below the provenance header |
| `valuation_outlier_review_service.py` | Nothing — published unchanged below the provenance header. The calibration-pack **artifact** it reads is not published; only the reader is. |

---

## What is deliberately not here

The following were considered and **rejected** for publication:

| Not published | Why |
|---|---|
| Macro / BTC / ETH / Equity / FICC scoring engines | Proprietary strategy IP — the core commercial asset |
| Full valuation and fair-value models | Proprietary strategy IP |
| Private provider adapters and routing | Provider contract terms, credential surface, operational topology |
| Broker execution implementation | Execution attack surface; nothing about it aids judging |
| Production Agent Treasury admin implementation | Payment-authorization attack surface |
| Full Alembic migration history | Reveals production schema and data topology |
| Internal production runbooks | Operational security |
| Signal-alert evaluator | Requires database session and internal anti-spam heuristics; the governance value is already carried by `freshness_policy.py` |
| Model-inferred lane validator | Would require publishing the pydantic schema chain behind it; `evidence_tier.py` already evidences lane discipline at lower cost |
| Any customer or user data | Never publishable |

---

## Licensing note

This repository is Apache-2.0. Everything in this directory is a **deliberate
public release decision**, reviewed for secrets, customer data, operational
topology, and strategy IP before publication.

Anything not present here remains proprietary and closed-source in the
[private production repository](https://github.com/0xjacobzhao-byte/Pantheon-Research).
