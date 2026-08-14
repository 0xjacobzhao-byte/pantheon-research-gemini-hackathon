# Strategy Stack — Frameworks, Not Prompts

Pantheon's strategy layer is a library of **versioned investment frameworks**.
Each framework encodes what matters in a domain, what invalidates a view, and
the risk constraints that govern exposure.

> **Design principle:** a framework must be able to **refuse to conclude**. When
> evidence is missing or a hard stop is hit, the correct output is "no view" —
> not a confident guess.

This is the central claim of the architecture: **investment logic is defined by
frameworks that existed before any model ran, not by improvised LLM prompts.**
Deterministic engines compute regimes, scores and signal candidates *first*; the
five-model AI layer then interprets that governed output. A model never
originates a view, and never mutates a deterministic score.

This document describes **architecture and method**, which is sufficient to
evaluate rigor. Full formulas, thresholds, indicator weights, and framework
version history remain in the private production repository.

---

## Cross-asset framework map

| Domain | Core method | Primary output | Fail-closed / invalidation principle |
|---|---|---|---|
| **Global Macro** | Tiered indicators (liquidity, real rates, credit, growth, inflation, volatility) rolled into a quadrant regime | Regime classification, hard stops, exposure context | Hard stops override the regime. Every downstream engine inherits macro permission rather than re-deriving one. |
| **US / CN / HK / SG Equities** | Stage-gated evaluation: kill-fast screening → quality and cash engine → valuation triangulation → macro permission → risk clustering | Company research, valuation, model comparison | A name that fails any gate exits the funnel; weak candidates fail cheaply. Missing fundamentals produce `NOT_RATED`, never an inferred rating. |
| **Narrative / Capital Flow** | Theme lifecycle, crowding, participation and reflexivity behind a liquidity gate | Thematic and event-context research | Sizing is capped and payoff-asymmetric by construction — narrative exposure is treated as optionality, never conviction. |
| **Technical Analysis** | State-first: market regime → normalized indicator features → dynamic weights → synthesis | Multi-asset scans, regime and signal overlays | Execution risk and portfolio risk budget are computed separately from the signal, so a strong signal can never override a risk limit. |
| **Bitcoin** | Multi-horizon: long-cycle bottom model + primary directional framework + short-horizon risk radar | Cycle and risk stance | When horizons disagree the framework **states which horizon governs** rather than averaging them. |
| **Ethereum** | Multi-quadrant valuation — settlement/security, monetary utility, network effect, revenue floor — weighted by regime | Valuation stance with kill switches | A broken quadrant trips a kill switch and suspends the view outright. |
| **DeFi** | Protocol risk scoring, organic-yield analysis, liquidity and exit mechanics, counterparty and centralization checks | Yield / risk verdicts | `DATA_GAP` is a first-class verdict alongside eligible / watch / avoid — never a silent omission, and never bearish by default. |
| **Fixed Income · FX · Commodities** | Layered: macro → valuation → carry → positioning → market structure → execution | Cross-asset allocation and carry views | Views must remain consistent with the prevailing macro regime; an inconsistent view is withheld rather than published. |
| **Prediction Markets** *(where applicable)* | Event probability, liquidity depth, and payoff structure | Probabilistic event intelligence | Thin liquidity invalidates the signal — an illiquid market produces no tradable read. |
| **Backtest / Forward Validation** | Point-in-time reconstruction, prospective signal capture, outcome maturation | Validation state per module | Immature evidence is reported as immature. Only **matured forward outcomes** may support a performance claim. |

---

## How the layers compose

```text
Governed evidence (layer 2)
   → Deterministic framework computes regime / score / signal candidate (layer 3)
   → Framework asserts its own invalidation conditions
   → Five-model AI layer interprets the governed output (layer 4)
   → Disagreement and evidence gaps surface as review tasks
   → Human review gate (layer 6)
   → Human decision
```

Three properties make this different from prompting a model about a market:

1. **The framework runs first and independently.** Its output exists whether or
   not any model is available. Provider outage degrades interpretation, not the
   research itself.
2. **The framework declares its own kill conditions.** Invalidation is part of
   the framework definition, not a post-hoc caveat added to a model answer.
3. **The model cannot promote its own conclusion.** Evidence tier is computed
   from source-pack metadata only — see
   [`production_reference/evidence_tier.py`](../production_reference/evidence_tier.py).

---

## Validation discipline

A framework is not credible because it is elaborate. Pantheon separates:

| Stage | Evidential weight |
|---|---|
| Historical backtest | Weakest — a strategy run over stored history |
| Reconstructed history | Carries **declared survivorship limitations** |
| Point-in-time evidence | Data as it was observable at decision time |
| Forward validation | Signals captured prospectively, before outcomes exist |
| **Matured outcomes** | **The only stage that supports a performance claim** |

Where a framework has been falsified in internal research, it is **retired
rather than retuned**. Method detail:
[`validation_methodology.md`](validation_methodology.md).

---

## What stays private

Not published here, and deliberately so:

- Full formulas, thresholds, indicator weights, and scoring functions
- Framework version numbers and version history
- Regime and gate multipliers, TTL constants
- Production strategy implementations and the research universe
- Provider routing and model-registry configuration

These are the commercial asset. This document describes the *architecture* they
implement — enough to judge rigor without releasing the IP. Judges may request
temporary read-only access to the private production repository if competition
rules allow.
