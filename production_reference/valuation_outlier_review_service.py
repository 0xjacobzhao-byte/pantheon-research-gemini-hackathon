"""Sanitized production reference.
Source: private Pantheon Research production repository.
Snapshot date: 2026-08-14.
Secrets, provider-specific configuration, operational details, and proprietary
strategy logic removed where applicable.

Published unchanged: standard-library-only, read-only, no credentials, no
network, no database, and no model recomputation. The calibration-pack artifact
this module reads is **not** published — only the reader is. It demonstrates the
human-review surface: how an outlier reaches a human without the system
silently acting on it.

---

Valuation Outlier Review — read-only calibration-pack reader.

Serves the committed calibration-pack artifact
(``artifacts/valuation_outlier_calibration_pack_<date>.json``) to the admin
Research-Ops dashboard. STRICTLY READ-ONLY:

  * No DB read/write, no provider HTTP, no LLM, no network.
  * No model recomputation — the flags / classification / recommended_action are the
    audit's pre-computed advisory labels, surfaced verbatim.
  * DATA_GAP is never bearish and never maps to AVOID; this module only *describes*.

The dashboard is research/admin review tooling — it changes NO model output.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Optional

# repo_root/backend_gateway/services/<this> → parents[2] == repo root
_REPO_ROOT = Path(__file__).resolve().parents[2]
_ARTIFACTS = _REPO_ROOT / "artifacts"
_PACK_GLOB = "valuation_outlier_calibration_pack_*.json"

CAVEATS = [
    "Review dashboard only. Does not change ratings, FV, or recommendations.",
    "Outliers are descriptive triggers for human review, not assertions the model is wrong.",
    "DATA_GAP is never bearish and never maps to AVOID; unknown/no-data remains NOT_RATED.",
    "Not investment advice.",
]


def _latest_pack_path() -> Optional[Path]:
    """Newest calibration-pack JSON, or None.

    Ordered by embedded ``YYYYMMDD`` date suffix first, then file mtime as the tiebreak so
    same-day packs resolve to the most recently generated one regardless of the descriptive
    name suffix (alphabetical name order does NOT track recency — e.g. ``post_us_adr_pe``
    sorts before ``post_us_specialist`` but is newer)."""
    import re
    if not _ARTIFACTS.is_dir():
        return None
    packs = list(_ARTIFACTS.glob(_PACK_GLOB))
    if not packs:
        return None

    def _key(p: Path):
        m = re.search(r"(\d{8})", p.name)
        date = m.group(1) if m else "00000000"
        try:
            mtime = p.stat().st_mtime
        except OSError:
            mtime = 0.0
        return (date, mtime)

    return max(packs, key=_key)


def _load_pack() -> Optional[dict]:
    path = _latest_pack_path()
    if path is None:
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:  # noqa: BLE001 — corrupt/partial artifact → treat as unavailable
        return None


def _unavailable() -> dict:
    return {
        "available": False,
        "reason": "Calibration-pack artifact not found or unreadable.",
        "caveats": CAVEATS,
        "summary": {"total": 0},
        "records": [],
        "filtered_count": 0,
    }


def _matches(
    rec: dict,
    *,
    market: Optional[str],
    classification: Optional[str],
    flag: Optional[str],
    sector: Optional[str],
    manual_review_only: bool,
    specialist_gap_only: bool,
    stale_analyst_only: bool,
    min_abs_spread: Optional[float],
) -> bool:
    if market and (rec.get("market") or "").upper() != market.upper():
        return False
    if classification and (rec.get("classification") or "") != classification:
        return False
    if flag and flag not in (rec.get("flags") or []):
        return False
    if sector and (rec.get("risk_model") or "").lower() != sector.lower():
        return False
    if manual_review_only and not rec.get("manual_review"):
        return False
    if specialist_gap_only and not rec.get("specialist_gap"):
        return False
    if stale_analyst_only and not rec.get("analyst_stale_flag"):
        return False
    if min_abs_spread is not None:
        spread = rec.get("analyst_vs_fv_spread_pp")
        if spread is None or abs(spread) < min_abs_spread:
            return False
    return True


def get_valuation_outliers(
    *,
    market: Optional[str] = None,
    classification: Optional[str] = None,
    flag: Optional[str] = None,
    sector: Optional[str] = None,
    manual_review_only: bool = False,
    specialist_gap_only: bool = False,
    stale_analyst_only: bool = False,
    min_abs_spread: Optional[float] = None,
    limit: int = 500,
    counts_only: bool = False,
) -> dict[str, Any]:
    """Return the calibration pack (summary + filtered records). Read-only.

    Missing/unreadable artifact degrades gracefully to ``available: False`` (never
    raises) so the dashboard renders an honest empty state rather than a 500.
    """
    pack = _load_pack()
    if pack is None:
        return _unavailable()

    records = pack.get("records") or []
    filtered = [
        r for r in records
        if _matches(
            r, market=market, classification=classification, flag=flag, sector=sector,
            manual_review_only=manual_review_only, specialist_gap_only=specialist_gap_only,
            stale_analyst_only=stale_analyst_only, min_abs_spread=min_abs_spread,
        )
    ]

    out: dict[str, Any] = {
        "available": True,
        "_schema": pack.get("_schema"),
        "generated_for_date": pack.get("generated_for_date"),
        "data_as_of": pack.get("data_as_of"),
        "source": pack.get("source"),
        "caveats": pack.get("caveats") or CAVEATS,
        "classifications": pack.get("classifications"),
        "flags": pack.get("flags"),
        "summary": pack.get("summary") or {},
        "top_manual_review": pack.get("top_manual_review") or [],
        "top_data_gap_driven": pack.get("top_data_gap_driven") or [],
        "special_focus": pack.get("special_focus") or [],
        "filtered_count": len(filtered),
        "records": [] if counts_only else filtered[: max(1, limit)],
    }
    return out


__all__ = ["get_valuation_outliers", "CAVEATS"]
