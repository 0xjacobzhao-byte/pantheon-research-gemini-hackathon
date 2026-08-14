"""Sanitized production reference.
Source: private Pantheon Research production repository.
Snapshot date: 2026-08-14.
Secrets, provider-specific configuration, operational details, and proprietary
strategy logic removed where applicable.

Published unchanged: this module is pure, deterministic, standard-library-only
post-processing with no credentials, no network, no database, and no
alpha-generating logic. It grades *evidence quality*, not securities.

---

Evidence-tier computation.

Pure, deterministic post-processing applied to a validated
``QualitativeOverlayV0`` after ``validate_overlay_payload`` and after
``_enforce_v1_2_rules``. Maps the source-pack metadata + factor mix to one of
five graded tiers so the frontend can render a useful qualitative brief for
non-US markets without weakening source discipline.

Contract: ``docs/equities_llm_overlay/V1_6_EVIDENCE_TIERING_CONTRACT.md``.

Hard rules:

- Tier is computed from source-pack metadata + factor mix only.  The LLM
  payload is never re-graded.
- ``SOURCE_BACKED_BASIC``, ``SOURCE_LIMITED_BRIEF``, ``NO_USABLE_EVIDENCE``
  ALWAYS force ``allowed_modifier=0``.  Tier never unlocks a forbidden
  modifier value.
- ``NO_USABLE_EVIDENCE`` maps to ``status=insufficient_evidence``; every
  other tier maps to a ``status`` already valid in the V1.4 schema.
- No BUY/SELL/HOLD vocabulary may appear in any tier label / reason.
- Tier is purely informational — it does NOT mutate ``aggregate_overlay``
  or ``status`` except in the ``NO_USABLE_EVIDENCE`` case.
"""
from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Any, Dict, Literal, Optional


EvidenceTier = Literal[
    "SOURCE_BACKED_STRONG",
    "SOURCE_BACKED_MODERATE",
    "SOURCE_BACKED_BASIC",
    "SOURCE_LIMITED_BRIEF",
    "NO_USABLE_EVIDENCE",
]
BriefQuality = Literal["full", "compact", "summary_only", "empty"]
SourceDepth = Literal["multi_source", "single_source", "anchor_only", "none"]


_TIER_LABEL: dict[str, str] = {
    "SOURCE_BACKED_STRONG": "Strong source-backed brief",
    "SOURCE_BACKED_MODERATE": "Moderate source-backed brief",
    "SOURCE_BACKED_BASIC": "Basic source-backed brief",
    "SOURCE_LIMITED_BRIEF": "Source-limited qualitative brief",
    "NO_USABLE_EVIDENCE": "No usable evidence",
}

_TIER_BRIEF_QUALITY: dict[str, str] = {
    "SOURCE_BACKED_STRONG": "full",
    "SOURCE_BACKED_MODERATE": "full",
    "SOURCE_BACKED_BASIC": "compact",
    "SOURCE_LIMITED_BRIEF": "summary_only",
    "NO_USABLE_EVIDENCE": "empty",
}

# Per-market awareness-only context. Surfaced as ``market_source_limitations``
# so the user understands why the tier capped where it did.
_MARKET_SOURCE_LIMITATIONS: dict[str, list[str]] = {
    "US": [
        "US V1.4 packs auto-ingest SEC EDGAR 10-K excerpts and 8-K EX-99.1 earnings commentary.",
    ],
    "HK": [
        "HK V1.5 packs use curated annual-report excerpts plus the HKEXnews title-search anchor.",
        "HK V1.5 does not auto-ingest transcripts or earnings-commentary releases.",
    ],
    "CN": [
        "CN V1.5 packs use curated Top-30 paraphrases plus CNINFO and Eastmoney search anchors.",
        "CN V1.5 does not auto-ingest filings; search anchors are not citable as primary evidence.",
    ],
    "SG": [
        "SG V1.5 BANK / REIT packs use operator-curated annual-results citations.",
        "SG V1.5 BLUE_CHIP packs cap at deterministic scan metrics — no curated annual fixture.",
    ],
}

# Forbidden vocabulary mirror — duplicated to avoid circular import with schema.
_WORD_FORBIDDEN = ("BUY", "SELL", "HOLD", "SIZING")
_PHRASE_FORBIDDEN = (
    "PRICE TARGET",
    "TARGET PRICE",
    "POSITION SIZE",
    "PANTHEON SCORE",
    "COMPOSITE SCORE",
    "INVESTMENT RATING",
)


def _safe_str(value: Optional[str], *, max_len: int = 240) -> str:
    text = (value or "").strip()
    if not text:
        return ""
    upper = " ".join(text.upper().split())
    for token in _WORD_FORBIDDEN:
        if f" {token} " in f" {upper} ":
            return ""
    for phrase in _PHRASE_FORBIDDEN:
        if phrase in upper:
            return ""
    return text[:max_len]


@dataclass(frozen=True)
class EvidenceTierBlock:
    evidence_tier: EvidenceTier
    evidence_tier_label: str
    evidence_tier_reason: str
    brief_quality: BriefQuality
    source_depth: SourceDepth
    can_render_qualitative_brief: bool
    hard_insufficient_reason: Optional[str]
    missing_evidence_fields: list[str]
    market_source_limitations: list[str]
    # V2.1 — deterministic validator / demoter + source-depth diagnostics.
    evidence_tier_raw_model: Optional[str] = None
    evidence_tier_validated: Optional[str] = None
    evidence_tier_demoted: Optional[bool] = None
    evidence_tier_demote_reason: Optional[str] = None
    source_depth_score: Optional[float] = None
    source_depth_components: Optional[Dict[str, Any]] = None
    factor_support_count: Optional[int] = None

    def to_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        # JSON-friendly: keep None for hard_insufficient_reason when unset.
        return d


# V2.1 — source-depth score map. Deterministic mapping from tier to a
# 0.0-1.0 score so the frontend / research memo can render a numeric
# proxy for tier without re-interpreting the label.
_TIER_SOURCE_DEPTH_SCORE: dict[str, float] = {
    "NO_USABLE_EVIDENCE": 0.0,
    "SOURCE_LIMITED_BRIEF": 0.25,
    "SOURCE_BACKED_BASIC": 0.55,
    "SOURCE_BACKED_MODERATE": 0.75,
    "SOURCE_BACKED_STRONG": 0.90,
}


def _count_factor_traits(factors: Optional[dict]) -> dict[str, int]:
    """Return per-trait counters across the 5 factor groups."""
    out = {
        "total": 0,
        "non_insufficient": 0,
        "evidence_strong": 0,
        "evidence_moderate": 0,
        "evidence_weak": 0,
        "evidence_insufficient": 0,
        "inference_direct": 0,
        "inference_inferred": 0,
        "inference_missing": 0,
        "with_source_refs": 0,
        "basis_filing_direct": 0,
        "basis_earnings_direct": 0,
        "basis_financial_direct": 0,
        "basis_pantheon_only": 0,
        "basis_inference_only": 0,
        "basis_missing": 0,
    }
    if not isinstance(factors, dict):
        return out
    for fname in (
        "moat_pricing_power",
        "pricing_power",
        "management_capital_allocation",
        "business_quality",
        "red_flags",
    ):
        f = factors.get(fname)
        if not isinstance(f, dict):
            continue
        out["total"] += 1
        verdict = f.get("verdict")
        if verdict and verdict != "insufficient_evidence":
            out["non_insufficient"] += 1
        eq = f.get("evidence_quality")
        if eq == "strong":
            out["evidence_strong"] += 1
        elif eq == "moderate":
            out["evidence_moderate"] += 1
        elif eq == "weak":
            out["evidence_weak"] += 1
        elif eq == "insufficient":
            out["evidence_insufficient"] += 1
        il = f.get("inference_level")
        if il == "direct":
            out["inference_direct"] += 1
        elif il == "inferred":
            out["inference_inferred"] += 1
        elif il == "missing":
            out["inference_missing"] += 1
        refs = f.get("source_refs") or []
        if isinstance(refs, list) and refs:
            out["with_source_refs"] += 1
        basis = f.get("evidence_basis")
        if basis == "filing_direct":
            out["basis_filing_direct"] += 1
        elif basis == "earnings_commentary_direct":
            out["basis_earnings_direct"] += 1
        elif basis == "financial_metric_direct":
            out["basis_financial_direct"] += 1
        elif basis == "pantheon_context_only":
            out["basis_pantheon_only"] += 1
        elif basis == "inference_only":
            out["basis_inference_only"] += 1
        elif basis == "missing":
            out["basis_missing"] += 1
    return out


def _is_v1_5_market_pack(source_pack_version: Optional[str]) -> bool:
    if not source_pack_version:
        return False
    return source_pack_version.startswith("qual_source_pack_hk_v1.5") or \
        source_pack_version.startswith("qual_source_pack_cn_v1.5") or \
        source_pack_version.startswith("qual_source_pack_sg_v1.5")


def _is_v1_4_us_pack(source_pack_version: Optional[str]) -> bool:
    if not source_pack_version:
        return False
    return source_pack_version.startswith("qual_source_pack_v1.4") or \
        source_pack_version.startswith("qual_source_pack_v1.2") or \
        source_pack_version.startswith("qual_source_pack_v1.1")


def _source_depth_from_overlay(
    *,
    source_pack_version: Optional[str],
    filing_citation_quality: Optional[str],
    filing_sections_present: int,
    transcript_citation_quality: Optional[str],
    earnings_citation_quality: Optional[str],
    source_pack_evidence_ready: Optional[bool],
    coverage_score: Optional[float],
) -> SourceDepth:
    has_filing = (
        filing_citation_quality in {"high", "medium"}
        and filing_sections_present > 0
    )
    has_transcript = transcript_citation_quality in {"high", "medium"}
    has_earnings = earnings_citation_quality in {"high", "medium"}
    distinct_sources = sum(1 for v in (has_filing, has_transcript, has_earnings) if v)
    if distinct_sources >= 2:
        return "multi_source"
    if distinct_sources == 1:
        return "single_source"
    # No primary filing/transcript/earnings source.
    if source_pack_evidence_ready or (coverage_score or 0.0) >= 0.20:
        return "anchor_only"
    return "none"


def compute_evidence_tier(
    *,
    market: Optional[str],
    status: Optional[str],
    aggregate_overlay: Optional[str],
    factors: Optional[dict],
    source_pack_version: Optional[str],
    source_pack_coverage_score: Optional[float],
    source_pack_evidence_ready: Optional[bool],
    source_pack_missing_fields: Optional[list[str]] = None,
    filing_evidence_citation_quality: Optional[str] = None,
    filing_evidence_sections_present: Optional[list[str]] = None,
    filing_evidence_source_refs: Optional[list[str]] = None,
    transcript_evidence_citation_quality: Optional[str] = None,
    earnings_commentary_citation_quality: Optional[str] = None,
    # V2.1 — HKEXnews / CNINFO announcement-index summary inputs.
    filing_evidence_announcement_index_count: Optional[int] = None,
    filing_evidence_announcement_categories: Optional[list[str]] = None,
    filing_evidence_exchange: Optional[str] = None,
    filing_evidence_issuer_mapping_confidence: Optional[str] = None,
) -> EvidenceTierBlock:
    """Deterministic tier assignment.

    The function takes overlay fields plus source-pack-derived fields and
    returns a non-LLM-graded tier block.  Safe to call on persisted pre-V1.6
    snapshots — missing fields default to legacy behaviour.
    """
    mkt = (market or "").upper()
    market_limitations = list(_MARKET_SOURCE_LIMITATIONS.get(mkt, []))
    traits = _count_factor_traits(factors)
    filing_sections_n = len(filing_evidence_sections_present or [])
    filing_refs_n = len(filing_evidence_source_refs or [])
    missing = list((source_pack_missing_fields or [])[:24])

    # Hard-empty fast path: identity unresolved or no pack at all.
    if status in {"provider_not_configured", "skipped_market_not_supported"}:
        return EvidenceTierBlock(
            evidence_tier="NO_USABLE_EVIDENCE",
            evidence_tier_label=_TIER_LABEL["NO_USABLE_EVIDENCE"],
            evidence_tier_reason=_safe_str(f"{status} — provider stack unavailable for tier computation"),
            brief_quality="empty",
            source_depth="none",
            can_render_qualitative_brief=False,
            hard_insufficient_reason=str(status),
            missing_evidence_fields=missing,
            market_source_limitations=market_limitations,
        )

    if not source_pack_version:
        # No source pack stamped. A packless row is NOT source-backed, so it must
        # never reach SOURCE_BACKED_MODERATE or retain a positive modifier — that
        # was a fail-open that rewarded legacy V0/V1 snapshots (and any row that
        # dropped its pack metadata) with a moderate, modifier-carrying tier.
        # Surface a renderable-but-degraded SOURCE_LIMITED_BRIEF when status=ok
        # (the caller's ``apply_evidence_tier_to_overlay_dict`` forces
        # ``allowed_modifier=0`` for every non-STRONG/MODERATE tier), else
        # NO_USABLE_EVIDENCE.
        if status == "ok" and aggregate_overlay and aggregate_overlay != "insufficient_evidence":
            return EvidenceTierBlock(
                evidence_tier="SOURCE_LIMITED_BRIEF",
                evidence_tier_label=_TIER_LABEL["SOURCE_LIMITED_BRIEF"],
                evidence_tier_reason=_safe_str("Packless snapshot — surfaced as source-limited brief (no source pack metadata; modifier forced to 0)"),
                brief_quality="summary_only",
                source_depth="single_source",
                can_render_qualitative_brief=True,
                hard_insufficient_reason=None,
                missing_evidence_fields=missing,
                market_source_limitations=market_limitations,
            )
        return EvidenceTierBlock(
            evidence_tier="NO_USABLE_EVIDENCE",
            evidence_tier_label=_TIER_LABEL["NO_USABLE_EVIDENCE"],
            evidence_tier_reason=_safe_str("Legacy snapshot without source pack metadata"),
            brief_quality="empty",
            source_depth="none",
            can_render_qualitative_brief=False,
            hard_insufficient_reason="legacy_pack_metadata_absent",
            missing_evidence_fields=missing,
            market_source_limitations=market_limitations,
        )

    source_depth = _source_depth_from_overlay(
        source_pack_version=source_pack_version,
        filing_citation_quality=filing_evidence_citation_quality,
        filing_sections_present=filing_sections_n,
        transcript_citation_quality=transcript_evidence_citation_quality,
        earnings_citation_quality=earnings_commentary_citation_quality,
        source_pack_evidence_ready=source_pack_evidence_ready,
        coverage_score=source_pack_coverage_score,
    )
    coverage = float(source_pack_coverage_score or 0.0)
    evidence_ready = bool(source_pack_evidence_ready)

    # NO_USABLE_EVIDENCE: pack is functionally empty.
    if (
        coverage < 0.20
        and source_depth == "none"
        and traits["total"] == 0
    ):
        return EvidenceTierBlock(
            evidence_tier="NO_USABLE_EVIDENCE",
            evidence_tier_label=_TIER_LABEL["NO_USABLE_EVIDENCE"],
            evidence_tier_reason=_safe_str(
                f"Pack coverage {coverage:.2f} below 0.20 and no factor groups validated"
            ),
            brief_quality="empty",
            source_depth="none",
            can_render_qualitative_brief=False,
            hard_insufficient_reason="pack_below_minimum_coverage",
            missing_evidence_fields=missing,
            market_source_limitations=market_limitations,
        )

    # Strong / Moderate are reserved for V1.4 US packs (or any pack with
    # multi-source evidence reaching SEC-grade depth).
    if _is_v1_4_us_pack(source_pack_version):
        if (
            traits["non_insufficient"] >= 2
            and traits["evidence_strong"] >= 2
            and traits["with_source_refs"] >= 2
            and source_depth in {"multi_source", "single_source"}
        ):
            return EvidenceTierBlock(
                evidence_tier="SOURCE_BACKED_STRONG",
                evidence_tier_label=_TIER_LABEL["SOURCE_BACKED_STRONG"],
                evidence_tier_reason=_safe_str(
                    f"V1.4 pack with {traits['evidence_strong']} strong factor groups and {source_depth} evidence"
                ),
                brief_quality="full",
                source_depth=source_depth,
                can_render_qualitative_brief=True,
                hard_insufficient_reason=None,
                missing_evidence_fields=missing,
                market_source_limitations=market_limitations,
            )
        if (
            traits["non_insufficient"] >= 1
            and (traits["evidence_strong"] + traits["evidence_moderate"]) >= 2
            and traits["with_source_refs"] >= 1
        ):
            return EvidenceTierBlock(
                evidence_tier="SOURCE_BACKED_MODERATE",
                evidence_tier_label=_TIER_LABEL["SOURCE_BACKED_MODERATE"],
                evidence_tier_reason=_safe_str(
                    f"V1.4 pack with {traits['evidence_strong'] + traits['evidence_moderate']} strong+moderate factor groups"
                ),
                brief_quality="full",
                source_depth=source_depth,
                can_render_qualitative_brief=True,
                hard_insufficient_reason=None,
                missing_evidence_fields=missing,
                market_source_limitations=market_limitations,
            )
        # V1.4 pack but LLM fail-closed: still BASIC because pack is rich.
        if evidence_ready and coverage >= 0.55:
            return EvidenceTierBlock(
                evidence_tier="SOURCE_BACKED_BASIC",
                evidence_tier_label=_TIER_LABEL["SOURCE_BACKED_BASIC"],
                evidence_tier_reason=_safe_str(
                    f"V1.4 pack at coverage {coverage:.2f} — model fail-closed on factor verdicts"
                ),
                brief_quality="compact",
                source_depth=source_depth,
                can_render_qualitative_brief=True,
                hard_insufficient_reason=None,
                missing_evidence_fields=missing,
                market_source_limitations=market_limitations,
            )

    # V1.5 HK / CN / SG packs.
    #
    # Historically (V1.6 contract) capped at BASIC because no transcripts /
    # 8-K equivalent existed. V2.1 narrows that cap: HK / CN packs may now
    # reach SOURCE_BACKED_MODERATE when (a) the V2.0 HKEXnews / CNINFO
    # announcement index covers ≥ 2 distinct announcement categories AND
    # (b) the issuer-mapping is unambiguous AND (c) the LLM independently
    # cites ≥ 2 factor groups with source_refs AND (d) factor evidence
    # quality is strong/moderate on ≥ 2 groups. STRONG remains reserved
    # for US V1.4 packs (or future HK/CN document-text auto-ingest).
    if _is_v1_5_market_pack(source_pack_version):
        announcement_categories = list(
            filing_evidence_announcement_categories or []
        )
        announcement_categories_n = len(
            {str(c).strip().lower() for c in announcement_categories if str(c).strip()}
        )
        issuer_mapping_high = (
            (filing_evidence_issuer_mapping_confidence or "").lower() == "high"
        )
        strong_or_moderate = traits["evidence_strong"] + traits["evidence_moderate"]
        factor_with_refs = traits["with_source_refs"]
        v2_1_moderate_eligible = (
            mkt in {"HK", "CN"}
            and evidence_ready
            and coverage >= 0.55
            and issuer_mapping_high
            and announcement_categories_n >= 2
            and factor_with_refs >= 2
            and strong_or_moderate >= 2
        )
        # HK requires the curated filing citation quality; CN allows
        # metadata-only when factor refs and direct bases are strong.
        if v2_1_moderate_eligible:
            if mkt == "HK" and filing_evidence_citation_quality not in {"high", "medium"}:
                v2_1_moderate_eligible = False
            elif mkt == "CN" and not (
                factor_with_refs >= 3
                and (traits["basis_filing_direct"] + traits["basis_financial_direct"]) >= 2
            ):
                v2_1_moderate_eligible = False
        if v2_1_moderate_eligible:
            return EvidenceTierBlock(
                evidence_tier="SOURCE_BACKED_MODERATE",
                evidence_tier_label=_TIER_LABEL["SOURCE_BACKED_MODERATE"],
                evidence_tier_reason=_safe_str(
                    f"{mkt} V1.5 pack at coverage {coverage:.2f} with multi-category announcement index "
                    f"({announcement_categories_n} categories) and {factor_with_refs} factor groups with source_refs"
                ),
                brief_quality="full",
                source_depth=source_depth if source_depth != "none" else "single_source",
                can_render_qualitative_brief=True,
                hard_insufficient_reason=None,
                missing_evidence_fields=missing,
                market_source_limitations=market_limitations,
            )
        if (
            evidence_ready
            and coverage >= 0.55
            and (
                filing_evidence_citation_quality in {"high", "medium"}
                or filing_refs_n >= 1
                or source_depth in {"multi_source", "single_source"}
            )
        ):
            return EvidenceTierBlock(
                evidence_tier="SOURCE_BACKED_BASIC",
                evidence_tier_label=_TIER_LABEL["SOURCE_BACKED_BASIC"],
                evidence_tier_reason=_safe_str(
                    f"{mkt} V1.5 pack at coverage {coverage:.2f} with curated brief + market-regulator filing anchor"
                ),
                brief_quality="compact",
                source_depth=source_depth,
                can_render_qualitative_brief=True,
                hard_insufficient_reason=None,
                missing_evidence_fields=missing,
                market_source_limitations=market_limitations,
            )
        # SOURCE_LIMITED: still substantive enough for a brief but below BASIC.
        if (
            evidence_ready
            or coverage >= 0.20
            or filing_refs_n >= 1
            or source_depth != "none"
        ):
            return EvidenceTierBlock(
                evidence_tier="SOURCE_LIMITED_BRIEF",
                evidence_tier_label=_TIER_LABEL["SOURCE_LIMITED_BRIEF"],
                evidence_tier_reason=_safe_str(
                    f"{mkt} V1.5 thin pack at coverage {coverage:.2f} — curated brief only, no filing excerpts"
                ),
                brief_quality="summary_only",
                source_depth=source_depth,
                can_render_qualitative_brief=True,
                hard_insufficient_reason=None,
                missing_evidence_fields=missing,
                market_source_limitations=market_limitations,
            )
        return EvidenceTierBlock(
            evidence_tier="NO_USABLE_EVIDENCE",
            evidence_tier_label=_TIER_LABEL["NO_USABLE_EVIDENCE"],
            evidence_tier_reason=_safe_str(
                f"{mkt} V1.5 pack coverage {coverage:.2f} below brief threshold"
            ),
            brief_quality="empty",
            source_depth="none",
            can_render_qualitative_brief=False,
            hard_insufficient_reason="market_pack_below_brief_threshold",
            missing_evidence_fields=missing,
            market_source_limitations=market_limitations,
        )

    # Unknown / future pack version — treat conservatively.
    if evidence_ready and coverage >= 0.55 and source_depth in {"multi_source", "single_source"}:
        return EvidenceTierBlock(
            evidence_tier="SOURCE_BACKED_BASIC",
            evidence_tier_label=_TIER_LABEL["SOURCE_BACKED_BASIC"],
            evidence_tier_reason=_safe_str(
                f"Unrecognised pack {source_pack_version} at coverage {coverage:.2f}, source_depth={source_depth}"
            ),
            brief_quality="compact",
            source_depth=source_depth,
            can_render_qualitative_brief=True,
            hard_insufficient_reason=None,
            missing_evidence_fields=missing,
            market_source_limitations=market_limitations,
        )
    if coverage >= 0.20 or source_depth != "none":
        return EvidenceTierBlock(
            evidence_tier="SOURCE_LIMITED_BRIEF",
            evidence_tier_label=_TIER_LABEL["SOURCE_LIMITED_BRIEF"],
            evidence_tier_reason=_safe_str(
                f"Unrecognised pack {source_pack_version} at coverage {coverage:.2f}"
            ),
            brief_quality="summary_only",
            source_depth=source_depth,
            can_render_qualitative_brief=True,
            hard_insufficient_reason=None,
            missing_evidence_fields=missing,
            market_source_limitations=market_limitations,
        )
    return EvidenceTierBlock(
        evidence_tier="NO_USABLE_EVIDENCE",
        evidence_tier_label=_TIER_LABEL["NO_USABLE_EVIDENCE"],
        evidence_tier_reason=_safe_str(
            f"Unrecognised pack {source_pack_version} below brief threshold"
        ),
        brief_quality="empty",
        source_depth="none",
        can_render_qualitative_brief=False,
        hard_insufficient_reason="unrecognised_pack_below_threshold",
        missing_evidence_fields=missing,
        market_source_limitations=market_limitations,
    )


def apply_evidence_tier_to_overlay_dict(overlay_dict: Dict[str, Any]) -> Dict[str, Any]:
    """Mutate a serialised overlay dict to include the V1.6 evidence-tier block.

    Safe to call on pre-V1.6 snapshots — never raises, always returns a dict.
    Enforces ``allowed_modifier=0`` for non-STRONG/MODERATE tiers.
    Sets ``status=insufficient_evidence`` only when tier=``NO_USABLE_EVIDENCE``.

    V2.1 — also populates the deterministic validator/demoter trail:
    ``evidence_tier_validated`` always equals ``evidence_tier``;
    ``evidence_tier_demoted`` is True only when MODERATE eligibility was
    close to triggering EXCEPT one prerequisite failed; ``source_depth_score``
    derives from the final tier; ``source_depth_components`` is a diagnostic
    breakdown that drives the rule.
    """
    if not isinstance(overlay_dict, dict):
        return overlay_dict
    tier = compute_evidence_tier(
        market=overlay_dict.get("market"),
        status=overlay_dict.get("status"),
        aggregate_overlay=overlay_dict.get("aggregate_overlay"),
        factors=overlay_dict.get("factors"),
        source_pack_version=overlay_dict.get("source_pack_version"),
        source_pack_coverage_score=overlay_dict.get("source_pack_coverage_score"),
        source_pack_evidence_ready=overlay_dict.get("source_pack_evidence_ready"),
        source_pack_missing_fields=overlay_dict.get("source_pack_missing_fields"),
        filing_evidence_citation_quality=overlay_dict.get("filing_evidence_citation_quality"),
        filing_evidence_sections_present=overlay_dict.get("filing_evidence_sections_present"),
        filing_evidence_source_refs=overlay_dict.get("filing_evidence_source_refs"),
        transcript_evidence_citation_quality=overlay_dict.get("transcript_evidence_citation_quality"),
        earnings_commentary_citation_quality=overlay_dict.get("earnings_commentary_citation_quality"),
        filing_evidence_announcement_index_count=overlay_dict.get(
            "filing_evidence_announcement_index_count"
        ),
        filing_evidence_announcement_categories=overlay_dict.get(
            "filing_evidence_announcement_categories"
        ),
        filing_evidence_exchange=overlay_dict.get("filing_evidence_exchange"),
        filing_evidence_issuer_mapping_confidence=overlay_dict.get(
            "filing_evidence_issuer_mapping_confidence"
        ),
    )
    # V2.1 — enrichment trail. The rule is deterministic so
    # evidence_tier_raw_model has no model channel; the validator is the
    # rule itself.
    enriched = _enrich_v2_1(overlay_dict, tier)
    overlay_dict.update(enriched)
    # Hard rule: non-STRONG/MODERATE tiers MUST keep modifier=0.
    if tier.evidence_tier not in {"SOURCE_BACKED_STRONG", "SOURCE_BACKED_MODERATE"}:
        overlay_dict["allowed_modifier"] = 0
    # Hard rule: NO_USABLE_EVIDENCE maps to insufficient_evidence status when
    # the legacy status would otherwise look "ok" (don't override schema_invalid
    # or other terminal fail-closed states).
    if tier.evidence_tier == "NO_USABLE_EVIDENCE":
        if overlay_dict.get("status") == "ok":
            overlay_dict["status"] = "insufficient_evidence"
        if overlay_dict.get("aggregate_overlay") != "insufficient_evidence":
            overlay_dict["aggregate_overlay"] = "insufficient_evidence"
    # V1.6 contract: SOURCE_BACKED_* and SOURCE_LIMITED_BRIEF mean the LLM
    # produced a validated response and the source pack is non-empty.  Lift
    # status back to ``ok`` when the legacy V0 zero-evidence demoter has set it
    # to ``insufficient_evidence`` — the tier is the product-level signal now.
    # Never override hard fail-closed terminal states.
    if tier.evidence_tier in {
        "SOURCE_BACKED_STRONG", "SOURCE_BACKED_MODERATE",
        "SOURCE_BACKED_BASIC", "SOURCE_LIMITED_BRIEF",
    }:
        if overlay_dict.get("status") == "insufficient_evidence":
            overlay_dict["status"] = "ok"
    return overlay_dict


def _enrich_v2_1(
    overlay_dict: Dict[str, Any],
    tier: EvidenceTierBlock,
) -> Dict[str, Any]:
    """Compute V2.1 validator / demoter / source-depth diagnostic fields.

    Reads input from the overlay dict so a single pass over
    ``compute_evidence_tier`` + this enrichment covers every persisted
    snapshot at read time.
    """
    market = (overlay_dict.get("market") or "").upper()
    coverage = float(overlay_dict.get("source_pack_coverage_score") or 0.0)
    evidence_ready = bool(overlay_dict.get("source_pack_evidence_ready"))
    traits = _count_factor_traits(overlay_dict.get("factors"))
    categories = list(
        overlay_dict.get("filing_evidence_announcement_categories") or []
    )
    categories_n = len(
        {str(c).strip().lower() for c in categories if str(c).strip()}
    )
    issuer_mapping = (
        overlay_dict.get("filing_evidence_issuer_mapping_confidence") or ""
    ).lower()
    filing_citation = (
        overlay_dict.get("filing_evidence_citation_quality") or ""
    ).lower()
    factor_support = int(traits.get("with_source_refs", 0))
    strong_plus_moderate = int(
        traits.get("evidence_strong", 0) + traits.get("evidence_moderate", 0)
    )

    # Demotion detection: MODERATE was *almost* eligible but one prereq
    # failed. Only set demoted=True when at least three of the five
    # prereqs are met; otherwise the gate did not consider MODERATE at
    # all and no demotion is recorded.
    prereq_status = {
        "evidence_ready": evidence_ready,
        "coverage_ok": coverage >= 0.55,
        "issuer_mapping_high": issuer_mapping == "high",
        "categories_ge_2": categories_n >= 2,
        "factor_refs_ge_2": factor_support >= 2,
        "strong_moderate_ge_2": strong_plus_moderate >= 2,
    }
    if market == "HK":
        prereq_status["hk_filing_citation_high_or_medium"] = (
            filing_citation in {"high", "medium"}
        )
    elif market == "CN":
        prereq_status["cn_factor_refs_ge_3"] = factor_support >= 3
        prereq_status["cn_direct_basis_ge_2"] = int(
            traits.get("basis_filing_direct", 0)
            + traits.get("basis_financial_direct", 0)
        ) >= 2

    n_met = sum(1 for v in prereq_status.values() if v)
    n_total = len(prereq_status)
    almost_moderate = (
        market in {"HK", "CN"}
        and tier.evidence_tier
        in {"SOURCE_BACKED_BASIC", "SOURCE_LIMITED_BRIEF"}
        and n_met >= max(3, n_total - 2)
        and tier.evidence_tier != "SOURCE_BACKED_MODERATE"
    )
    demote_reason: Optional[str] = None
    if almost_moderate:
        unmet = [k for k, v in prereq_status.items() if not v]
        demote_reason = (
            "MODERATE prereqs failed: " + ", ".join(unmet[:4])
        )[:240]

    components = {
        "coverage_score": coverage,
        "evidence_ready": evidence_ready,
        "announcement_categories_n": categories_n,
        "announcement_categories": categories[:8],
        "issuer_mapping_confidence": (
            overlay_dict.get("filing_evidence_issuer_mapping_confidence")
        ),
        "filing_citation_quality": (
            overlay_dict.get("filing_evidence_citation_quality")
        ),
        "filing_source_refs_count": len(
            overlay_dict.get("filing_evidence_source_refs") or []
        ),
        "factor_with_source_refs": factor_support,
        "factor_evidence_strong": int(traits.get("evidence_strong", 0)),
        "factor_evidence_moderate": int(traits.get("evidence_moderate", 0)),
        "factor_basis_filing_direct": int(traits.get("basis_filing_direct", 0)),
        "factor_basis_financial_direct": int(
            traits.get("basis_financial_direct", 0)
        ),
        "tier_prereq_status": prereq_status,
    }

    base = tier.to_dict()
    base.update({
        "evidence_tier_raw_model": None,
        "evidence_tier_validated": tier.evidence_tier,
        "evidence_tier_demoted": bool(almost_moderate),
        "evidence_tier_demote_reason": demote_reason,
        "source_depth_score": _TIER_SOURCE_DEPTH_SCORE.get(
            tier.evidence_tier, 0.0
        ),
        "source_depth_components": components,
        "factor_support_count": factor_support,
    })
    return base


__all__ = [
    "EvidenceTier",
    "BriefQuality",
    "SourceDepth",
    "EvidenceTierBlock",
    "compute_evidence_tier",
    "apply_evidence_tier_to_overlay_dict",
]
