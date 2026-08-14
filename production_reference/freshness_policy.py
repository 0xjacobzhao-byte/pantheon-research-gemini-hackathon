"""Sanitized production reference.
Source: private Pantheon Research production repository.
Snapshot date: 2026-08-14.
Secrets, provider-specific configuration, operational details, and proprietary
strategy logic removed where applicable.

Removed for publication: upstream provider names and routing, credential
environment-variable names, hosting/database topology, internal recovery-runbook
paths, and internal PR references. The freshness contract itself — cadence, TTL
thresholds, scheduler lanes, and the classification function — is published
unchanged.

---

Alert-module freshness policy registry.

Maps each upstream research module to its expected refresh cadence, TTL
thresholds, and calendar awareness. Used by the scheduler to determine lane
assignment, and by the freshness check to contextualize staleness.

Why this exists: a research system that serves stale data without saying so is
worse than one that refuses to answer. Every module declares, up front, how
fresh its data is *supposed* to be. Actual age is then measured against that
declaration rather than against a global default, because a monthly fixed-income
framework and an intraday crypto framework have nothing useful in common.

Two thresholds, not one:

  * ``soft_ttl_hours`` — past this, data is ``SOFT_STALE``: still served, but
    labelled, and the label reaches the user.
  * ``hard_ttl_hours`` — past this, data is ``HARD_STALE``: it has failed its
    own freshness contract.

``stale_root_cause`` records *why* a module is known to be stale, so a stale
module is an explained condition rather than an anonymous gap.

Paused modules are excluded from the confidence computation so they cannot
permanently drag the confidence label below its honest level. They remain in the
registry for observability and are shown as "Paused" in Research Ops.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

FRESHNESS_POLICY_VERSION = "v1.2"


@dataclass(frozen=True)
class AlertModulePolicy:
    module_key: str
    cadence: str
    soft_ttl_hours: float
    hard_ttl_hours: float
    scheduler_lane: str
    calendar_aware: bool
    market_hours: Optional[str]
    stale_root_cause: Optional[str]
    paused: bool = False
    pause_reason: Optional[str] = None


ALERT_MODULE_POLICIES: dict[str, AlertModulePolicy] = {
    "macro": AlertModulePolicy(
        module_key="macro",
        cadence="daily",
        soft_ttl_hours=12,
        hard_ttl_hours=26,
        scheduler_lane="market_state",
        calendar_aware=True,
        market_hours="US",
        stale_root_cause=None,
    ),
    "us-stock": AlertModulePolicy(
        module_key="us-stock",
        cadence="daily",
        soft_ttl_hours=18,
        hard_ttl_hours=26,
        scheduler_lane="market_state",
        calendar_aware=True,
        market_hours="US",
        stale_root_cause=None,
    ),
    "cn-stock": AlertModulePolicy(
        module_key="cn-stock",
        cadence="weekly",
        soft_ttl_hours=144,
        hard_ttl_hours=192,
        scheduler_lane="market_state",
        calendar_aware=True,
        market_hours="CN",
        stale_root_cause=None,
    ),
    "hk-stock": AlertModulePolicy(
        module_key="hk-stock",
        cadence="weekly",
        soft_ttl_hours=144,
        hard_ttl_hours=192,
        scheduler_lane="market_state",
        calendar_aware=True,
        market_hours="HK",
        # ACTIVE: a governed provider bridge feeds current HK OHLCV and
        # fundamentals into the canonical store; the scan reads that bridge as
        # the primary HK price source. (Provider identity and routing detail
        # removed for publication.)
        stale_root_cause=None,
    ),
    "sg-stock": AlertModulePolicy(
        module_key="sg-stock",
        cadence="weekly",
        soft_ttl_hours=144,
        hard_ttl_hours=192,
        scheduler_lane="market_state",
        calendar_aware=True,
        market_hours="SG",
        # ACTIVE: a governed provider path writes current SG data directly into
        # product snapshots in the canonical store — no operator-local artifact
        # sits anywhere on the serving path. (Provider identity and hosting
        # detail removed for publication.)
        stale_root_cause=None,
    ),
    "btc": AlertModulePolicy(
        module_key="btc",
        cadence="intraday",
        soft_ttl_hours=4,
        hard_ttl_hours=8,
        scheduler_lane="market_state",
        calendar_aware=False,
        market_hours=None,
        stale_root_cause=None,
    ),
    "eth": AlertModulePolicy(
        module_key="eth",
        cadence="intraday",
        # 10min soft / 20min hard — 2/4× the 5min refresh cadence. A 5min soft
        # TTL == the exact interval and flapped FRESH↔SOFT_STALE between cycles.
        soft_ttl_hours=0.167,
        hard_ttl_hours=0.333,
        scheduler_lane="market_state",
        calendar_aware=False,
        market_hours=None,
        # ACTIVE: the hybrid pipeline fails closed rather than serving a stored
        # golden fixture as if it were current — a fixture presented as live data
        # is exactly the silent-guess failure this registry exists to prevent.
        stale_root_cause=None,
    ),
    "defi": AlertModulePolicy(
        module_key="defi",
        cadence="daily",
        soft_ttl_hours=1,
        hard_ttl_hours=3,
        scheduler_lane="market_state",
        calendar_aware=False,
        market_hours=None,
        stale_root_cause=None,
    ),
    "fi": AlertModulePolicy(
        module_key="fi",
        cadence="monthly",
        soft_ttl_hours=672,
        hard_ttl_hours=1080,
        scheduler_lane="maintenance",
        calendar_aware=False,
        market_hours=None,
        stale_root_cause=None,
    ),
    "forex": AlertModulePolicy(
        module_key="forex",
        cadence="monthly",
        soft_ttl_hours=672,
        hard_ttl_hours=1080,
        scheduler_lane="maintenance",
        calendar_aware=False,
        market_hours=None,
        stale_root_cause=None,
    ),
    "commodity": AlertModulePolicy(
        module_key="commodity",
        cadence="daily",
        soft_ttl_hours=6,
        hard_ttl_hours=26,
        scheduler_lane="market_state",
        calendar_aware=True,
        market_hours="US",
        stale_root_cause=None,
    ),
    "ta": AlertModulePolicy(
        module_key="ta",
        cadence="weekly",
        soft_ttl_hours=144,
        hard_ttl_hours=192,
        scheduler_lane="maintenance",
        calendar_aware=True,
        market_hours="US",
        # ACTIVE: the cloud data profile is confirmed present in the production
        # environment, and the write guard threshold is aligned to the asset
        # coverage that profile actually provides — a guard calibrated to
        # coverage the provider does not serve blocks every legitimate write.
        # (Profile name, credential variables, and hosting detail removed for
        # publication.)
        stale_root_cause=None,
    ),
}


SCHEDULER_LANES = {
    "system_trust": {
        "description": "System health and data quality monitoring",
        "poll_interval_seconds": 300,
        "modules": [],
    },
    "market_state": {
        "description": "Market data evaluation (macro, stocks, crypto, commodities)",
        "poll_interval_seconds": 900,
        "modules": [k for k, v in ALERT_MODULE_POLICIES.items() if v.scheduler_lane == "market_state"],
    },
    "input_change_trigger": {
        "description": "Event-driven: fire when upstream data changes",
        "poll_interval_seconds": 0,
        "modules": [],
    },
    "maintenance": {
        "description": "Low-frequency modules (weekly/monthly data, TA scans)",
        "poll_interval_seconds": 3600,
        "modules": [k for k, v in ALERT_MODULE_POLICIES.items() if v.scheduler_lane == "maintenance"],
    },
}


def get_module_policy(module_key: str) -> Optional[AlertModulePolicy]:
    return ALERT_MODULE_POLICIES.get(module_key)


def get_known_stale_modules() -> list[dict]:
    return [
        {
            "module": p.module_key,
            "root_cause": p.stale_root_cause,
            "cadence": p.cadence,
            "hard_ttl_hours": p.hard_ttl_hours,
        }
        for p in ALERT_MODULE_POLICIES.values()
        if p.stale_root_cause is not None
    ]


def get_active_module_keys() -> list[str]:
    """Module keys that participate in confidence computation (excludes paused)."""
    return [k for k, p in ALERT_MODULE_POLICIES.items() if not p.paused]


def get_paused_modules() -> list[dict]:
    """Paused modules with their reasons — for observability, not confidence."""
    return [
        {
            "module": p.module_key,
            "pause_reason": p.pause_reason,
            "stale_root_cause": p.stale_root_cause,
        }
        for p in ALERT_MODULE_POLICIES.values()
        if p.paused
    ]


def is_module_paused(module_key: str) -> bool:
    policy = ALERT_MODULE_POLICIES.get(module_key)
    return policy.paused if policy else False


def classify_module_freshness(module_key: str, age_hours: float) -> str:
    """Classify a module's freshness status based on its policy TTL."""
    policy = ALERT_MODULE_POLICIES.get(module_key)
    if policy is None:
        return "UNKNOWN"
    if age_hours <= policy.soft_ttl_hours:
        return "FRESH"
    elif age_hours <= policy.hard_ttl_hours:
        return "SOFT_STALE"
    else:
        return "HARD_STALE"
