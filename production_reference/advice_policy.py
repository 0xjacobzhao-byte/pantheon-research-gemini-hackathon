"""Sanitized production reference.
Source: private Pantheon Research production repository.
Snapshot date: 2026-08-14.
Secrets, provider-specific configuration, operational details, and proprietary
strategy logic removed where applicable.

Published unchanged: standard-library-only, no credentials, no network, no
database. This is the executable form of the claim in README §9 — that AI
research decisions are structurally separated from capital-allocation
decisions. It is published precisely so that boundary can be audited rather
than taken on trust.

---

Pantheon Agent — the authoritative advice-versus-execution boundary.

This module replaces the product rule that used to govern every outbound answer.

The rule that was removed
-------------------------

Until now the outbound gate treated *any* wording that could be read as a trade
instruction as prohibited, and withheld the whole answer when it found one. The
gate defaulted to DENY: an unqualified ``buy``/``sell``/``加仓`` anywhere in a
reply blocked it unless one of ~20 exemptions fired. A subscriber who asked "is
BTC a good buy now?" could therefore receive::

    I had the evidence, but that draft contained wording that could read as a
    trade instruction, so it was withheld.

That is a product defect, not a safety control. Pantheon Research exists to
produce investment views; refusing to state one because it is actionable is
refusing to do the job.

The rule that replaces it
-------------------------

::

    ADVICE     = ALLOWED
    EXECUTION  = NOT AUTHORIZED

Pantheon **is expected to** state investment opinions, trading recommendations,
BUY / HOLD / SELL, LONG / FLAT / SHORT, buy / wait / reduce / avoid, entry
attractiveness, risk/reward, position-direction recommendations, conditions for
adding or reducing exposure, and invalidation conditions. None of that is
withheld, in any language, in any grammatical person, framed or unframed.

Pantheon must **not** place orders, submit broker instructions, modify or cancel
orders, sign transactions, or execute automatic trades — and must not claim to
have done any of those things. The Agent has no order path, no broker credential
and no signing key, and nothing here adds one.

What is still refused, and why each one is execution rather than advice
----------------------------------------------------------------------

``execution_claim``
    The reply asserts Pantheon transmitted or will transmit an instruction to a
    venue on the reader's behalf ("I've placed the order", "I'll submit that
    trade for you"). Always false, and the single most damaging sentence the
    product could emit.

``order_lifecycle_instruction``
    An operational venue instruction — place / submit / cancel / amend / route an
    order, set a stop-loss *order* at a level, 下单 / 挂单 / 撤单. Telling a reader
    *what to think about an asset* is research; telling them *what to type into a
    broker* is operating the trade.

``leverage_instruction``
    Instructing the reader to apply leverage. Not a directional view, and the one
    class of "advice" whose downside is unbounded.

``personal_sizing_instruction``
    A personalized allocation or position size ("increase your allocation to
    40%", "把仓位提到五成", "target allocation: 40% BTC"). Deliberately still
    refused, and deliberately consistent with :mod:`canonical_facts`, whose rule
    2 is that no size ever leaves the canonical layer: allowing the *model* to
    state sizing the *deterministic* layer refuses to publish would make the two
    halves of the product disagree. Direction is advice; magnitude is not
    published.

Scope note
----------

:func:`find_execution_directive` is used in two places with two different
consequences, and that split is intentional:

* :mod:`outbound_policy` withholds the whole reply — the last resort, reserved
  for text that must never be delivered at all;
* :mod:`execution_sanitizer` removes the offending **sentence** and delivers the
  rest, which is what keeps a single stray clause from costing the reader an
  otherwise correct answer.
"""

from __future__ import annotations

import re
from typing import Final, Optional

# ── Advice vocabulary: explicitly, permanently allowed ──────────────────────
#
# Kept as data rather than as a comment because the regression corpus asserts
# every one of these is deliverable. If a future change starts blocking one of
# them, that test fails and names the term.
ALLOWED_ADVICE_TERMS: Final[tuple[str, ...]] = (
    "buy",
    "sell",
    "hold",
    "wait",
    "reduce",
    "trim",
    "add",
    "accumulate",
    "avoid",
    "long",
    "short",
    "flat",
    "overweight",
    "underweight",
    "买入",
    "卖出",
    "持有",
    "观望",
    "减仓",
    "加仓",
    "回避",
    "做多",
    "做空",
)

# ── Execution: refused ──────────────────────────────────────────────────────

#: Pantheon claiming it transmitted, or will transmit, an instruction to a venue.
#: First person is required — "the fund placed a large order" is market reporting.
_EXECUTION_CLAIM = re.compile(
    # The contracted forms are spelled out because they carry no space: "I've
    # placed the order" is the single most damaging sentence here and an
    # apostrophe is all that separated it from the uncontracted form the pattern
    # already caught.
    r"\b(?:i|we)(?:['’](?:ve|ll|m))?\s+"
    r"(?:have\s+|has\s+|had\s+|just\s+|already\s+)?"
    r"(?:will\s+|can\s+|am\s+going\s+to\s+|going\s+to\s+)?"
    r"(?:placed?|submitted?|executed?|routed?|filled?|cancelled?|canceled?|"
    r"amended?|signed?|broadcast(?:ed)?|sent)\s+"
    r"(?:the\s+|a\s+|an\s+|your\s+|my\s+|this\s+|that\s+)?"
    r"(?:buy\s+|sell\s+|market\s+|limit\s+|stop\s+)?"
    r"(?:order|trade|transaction|tx|swap|position)s?\b"
    r"|\b(?:order|trade|transaction)\s+(?:has\s+been\s+|was\s+)?"
    r"(?:placed|submitted|executed|filled|routed|sent|confirmed)\b"
    r"|\b(?:i|we)(?:['’](?:ve|ll|m))?\s+(?:will\s+|can\s+)?"
    r"(?:buy|sell|short|long)\s+(?:it|them|this|that|the\s+\w+)\s+for\s+you\b"
    r"|我(?:已经|已|会|将|可以)?(?:帮|替|为)(?:你|您)"
    r"(?:下单|下了单|买入|卖出|平仓|建仓|执行|撤单)"
    r"|(?:订单|委托|交易)(?:已经|已)(?:提交|下达|执行|成交|发送)",
    re.I,
)

#: An operational venue instruction aimed at the reader.
#:
#: The stop-loss branch requires the ORDER noun or an explicit placement verb —
#: "invalidation below 92,000" and "the level that would void this view" are
#: research and must survive, while "place a stop-loss order at 92,000" is
#: operating the trade.
_ORDER_LIFECYCLE = re.compile(
    r"\b(?:place|placing|submit|submitting|cancel|cancell?ing|amend|amending|"
    r"modify|modifying|replace|replacing|route|routing|pull|execute|executing)\s+"
    r"(?:(?:a|an|the|your|my|our|this|that|all|any)\s+)?"
    r"(?:[A-Za-z0-9][\w.-]*\s+){0,3}orders?\b"
    r"|\b(?:market|limit|stop|stop[- ]limit|iceberg|twap|vwap|oco|"
    r"trailing[- ]stop)\s+orders?\b"
    r"|\b(?:set|place|put|enter)\s+(?:(?:a|an|the|your)\s+)?"
    r"(?:stop[- ]loss|take[- ]profit|stop)\s+order\b"
    # "Execute a trade" with no order noun. Narrow on purpose: `trade` as a NOUN
    # after an execution verb is an instruction, while "trade volume", "trade
    # flow" and "the trade is crowded" are ordinary market vocabulary.
    r"|\bexecut(?:e|es|ing)\s+(?:(?:a|an|the|this|that|your|my)\s+)?"
    r"(?:[A-Za-z0-9][\w.-]*\s+){0,2}trades?\b"
    # A second-person execution LEVEL. Deliberately not the whole
    # ``entry_exit_price`` rule, which stays sanitizer-only: an analyst target
    # price and an invalidation level are research and must stay deliverable,
    # while "set your stop loss at 60,000" is telling the reader what to place.
    r"|\b(?:set|move|place|put|shift)\s+(?:(?:a|an|the|your|my)\s+)?"
    r"(?:[A-Za-z0-9][\w.-]*\s+){0,2}"
    r"(?:stop[- ]?loss|stop|take[- ]?profit)\s*"
    r"(?:at|to|near|around|@|:)\s*[$¥€£]?\s*[\d,]"
    r"|\btake\s+profits?\s+(?:at|near|around|@)\s*[$¥€£]?\s*[\d,]"
    r"|下单|挂单|撤单|撤销委托|委托单|市价单|限价单|止损单|条件单|报单",
    re.I,
)

#: Leverage applied at the reader's account.
_LEVERAGE = re.compile(
    r"\b(?:us(?:e|es|ed|ing)|apply|applying|add|adding|increase|increasing|"
    r"take\s+on|taking\s+on|run|running|maximi[sz]e|maximi[sz]ing|dial\s+up)\s+"
    r"(?:(?:up\s+to\s+)?\d+(?:\.\d+)?x\s+|more\s+|maximum\s+|full\s+|extra\s+)?"
    r"leverage\b"
    r"|\b\d+(?:\.\d+)?x\s+leverage\b"
    r"|(?:加|上|开|用|使用|放大|提高|调高|调至|调到)\s*杠杆"
    r"|杠杆\s*(?:加|提|调|放)\s*(?:到|至)"
    r"|\d+\s*倍杠杆"
    r"|梭哈",
    re.I,
)

#: A personalized allocation or position size. Direction is advice; magnitude is
#: not published — the same rule the deterministic canonical layer already obeys.
_PERSONAL_SIZING = re.compile(
    r"\b\d+(?:\.\d+)?%\s*(?:of\s+)?(?:your|the\s+reader's|his|her|their)\s+"
    r"(?:portfolio|capital|book|account|net\s+worth|allocation|position)"
    r"|\b(?:increase|raise|lift|cut|reduce|lower|set|move|take)\s+"
    r"(?:(?:your|the|its|their)\s+)?"
    r"(?:[A-Za-z0-9][\w.-]*\s+){0,2}"
    r"(?:allocation|exposure|position\s+size|weighting?)\s+"
    r"(?:to|at|up\s+to|down\s+to)\s+[~<>]?\s*\d"
    r"|\bposition\s+siz(?:e|ing)\s+(?:should|must|of|at|to)\b"
    r"|\b(?:allocate|allocating|commit|committing|deploy|deploying)\s+"
    r"(?:up\s+to\s+)?\d+(?:\.\d+)?%"
    r"|\ballocate\s+(?:\w+\s+){0,2}(?:of\s+)?(?:your|their|his|her)\s+"
    r"(?:portfolio|capital|book)"
    r"|(?:你的|您的)\s*(?:仓位|敞口|配置|持仓)\s*(?:提|调|加|降|设)"
    r"|仓位\s*(?:提高|提升|加|升|降|减|调|放)\s*(?:到|至)"
    r"|(?:提高|提升|降低|减少|增加)\s*(?:你的|您的)?\s*仓位\s*(?:到|至)"
    r"|(?:配置|投入|押上|投)\s*\d+(?:\.\d+)?\s*[%成]"
    # A specific quantity IS a position size, however casually it is phrased.
    # "buy 500 shares" and "add 2 BTC" name a size just as much as "40% of your
    # portfolio" does, and the canonical layer publishes neither.
    r"|\b(?:buy|sell|short|add|acquire|accumulate|offload|dump)\s+"
    r"(?:me\s+)?\d[\d,.]*\s*"
    r"(?:shares?|units?|coins?|contracts?|lots?|btc|eth|sol|k\b|m\b)"
    r"|(?:买入|卖出|加|减|增持|减持)\s*\d[\d,.]*\s*"
    r"(?:股|手|张|个|枚|万|亿)"
    # All-in is a 100% position size stated as an idiom.
    r"|\bgo(?:es|ing)?\s+all[-\s]?in\b"
    r"|\b(?:put|invest|commit|deploy|allocate|move)\s+"
    r"(?:all\s+(?:of\s+)?(?:your|their|his|her)\s+|everything\s+)"
    r"(?:money\s+|cash\s+|capital\s+)?(?:in|into|to)\b"
    # A fraction of the reader's capital is a size even with no percent sign.
    r"|\b(?:all|half|most|a\s+(?:third|quarter))\s+(?:of\s+)?"
    r"(?:your|their|his|her|the\s+reader's)\s+"
    r"(?:cash|money|capital|portfolio|savings|net\s+worth|book|account)"
    # "Target a 50% BTC allocation" puts the magnitude between the verb and the
    # noun, which the adjacency-anchored framework rule cannot reach.
    r"|\btarget(?:s|ing)?\s+(?:a|an)?\s*\d+(?:\.\d+)?%\s*"
    r"(?:[A-Za-z0-9][\w.-]*\s+){0,2}(?:allocation|exposure|weight(?:ing)?)"
    # CN: sizing expressed as a target level rather than as a verb.
    r"|(?:加仓|减仓|建仓|调仓)\s*(?:到|至)\s*[\d一二三四五六七八九十半]+\s*[成%]"
    r"|仓位\s*(?:加满|打满|拉满|清空)"
    r"|(?:把|将)\s*仓位\s*(?:加|提|调|升|降)",
    re.I,
)

#: Nominal framework sizing, with no verb and no second person. A production turn
#: rendered "推荐敞口17.5%" and "推荐敞口从25%降至17.5%" to the reader: that is a
#: personalized allocation however impersonally it is phrased, and the canonical
#: payload's own ``recommended_exposure`` is exactly where it came from.
#:
#: Kept under its historical rule name because operator runbooks and the audit
#: vocabulary key on it. Unconditional at the sentence level: a third-party
#: subject does not make a recommended allocation percentage research.
_FRAMEWORK_SIZING = re.compile(
    r"(?:推荐|建议|目标)\s*(?:的)?\s*(?:敞口|仓位|配置|持仓|头寸|杠杆)"
    r"|(?:模型|框架)\s*(?:的)?\s*(?:敞口|仓位|配置|持仓|头寸|杠杆)"
    r"[^\d%\n]{0,4}[-+]?\d+(?:\.\d+)?\s*[%成]"
    r"|(?:敞口|仓位|配置|持仓|头寸)\s*(?:从|由)\s*[-+]?\d*\.?\d+"
    r"|\b(?:recommended|suggested|target|model(?:led|ed)?|framework|proposed|"
    r"ideal|optimal)\s+"
    r"(?:portfolio\s+)?(?:exposure|allocation|weight(?:ing)?s?)\b",
    re.I,
)

#: The same rule at the OUTBOUND tier, one word narrower — ``model`` rather than
#: ``model(?:led|ed)?``.
#:
#: This is load-bearing, not tidying. The renderer emits Pantheon's own canonical
#: line as ``Modelled exposure direction: LONG``, and that wording was chosen
#: precisely because it is not nominal sizing: "Model exposure" IS the sizing
#: shape, "Modelled exposure direction" is a labelled enum. Widening the outbound
#: pattern to the sanitizer's form blocks the deterministic divergence line the
#: product is required to state — every BTC and ETH answer with a
#: direction/position disagreement.
_FRAMEWORK_SIZING_OUTBOUND = re.compile(
    r"(?:推荐|建议|目标)\s*(?:的)?\s*(?:敞口|仓位|配置|持仓|头寸|杠杆)"
    r"|(?:模型|框架)\s*(?:的)?\s*(?:敞口|仓位|配置|持仓|头寸|杠杆)"
    r"[^\d%\n]{0,4}[-+]?\d+(?:\.\d+)?\s*[%成]"
    r"|(?:敞口|仓位|配置|持仓|头寸)\s*(?:从|由)\s*[-+]?\d*\.?\d+"
    r"|\b(?:recommended|suggested|target|model|framework|proposed|ideal|optimal)"
    r"\s+(?:portfolio\s+)?(?:exposure|allocation|weight(?:ing)?s?)\b",
    re.I,
)

#: A concrete execution price — an entry, an exit, a stop or a take-profit level
#: stated as a number to act on. Removed from narrative but NOT grounds for
#: withholding an answer, which is the whole reason the two tiers below exist:
#: one stray level in a paragraph should cost the sentence, never the reply.
#:
#: Invalidation conditions legitimately name levels and are exempted by
#: :data:`_EXECUTION_EXEMPT`, so "if GLI breaks 0.2 this view is void" survives
#: while "enter at $58,200" does not.
_ENTRY_EXIT_PRICE = re.compile(
    r"\b(?:entry|entries|exit|add|scale\s+in|scale\s+out|fill)\s*"
    r"(?:price|level|zone)?\s*(?:at|near|around|@|:)\s*"
    r"[$¥€£]?\s*\d"
    r"|\b(?:stop[- ]loss|stop|take[- ]profit|target\s+price|limit)\s*"
    r"(?:at|near|around|@|:|of)\s*[$¥€£]?\s*\d"
    r"|(?:买入价|买入点|入场价|入场点|加仓价|卖出价|离场价|止损位|止盈位|"
    r"目标价位)\s*(?:设|放|定|在|为|是|：|:)?\s*[$¥€£]?\s*\d"
    r"|(?:止损|止盈|入场|离场|买入|卖出)\s*(?:设|放|定)?在\s*[$¥€£]?\s*\d",
    re.I,
)

#: Rules that WITHHOLD a whole reply. Names are stable, appear in operator audit
#: records and in the block reason, and are unchanged from the previous policy
#: wherever the control itself survived — so an existing runbook keyed on
#: ``order_instruction`` or ``framework_sizing`` still resolves.
OUTBOUND_RULES: Final[tuple[tuple[str, re.Pattern[str]], ...]] = (
    ("execution_claim", _EXECUTION_CLAIM),
    ("order_instruction", _ORDER_LIFECYCLE),
    ("leverage_instruction", _LEVERAGE),
    ("framework_sizing", _FRAMEWORK_SIZING_OUTBOUND),
    ("personal_allocation", _PERSONAL_SIZING),
)

#: Rules applied per SENTENCE inside model narrative. A superset, and stricter
#: where it can afford to be: an execution price and the wider framework-sizing
#: form are worth removing from a paragraph but are not worth withholding an
#: answer over.
SANITIZER_RULES: Final[tuple[tuple[str, re.Pattern[str]], ...]] = (
    ("execution_claim", _EXECUTION_CLAIM),
    ("order_instruction", _ORDER_LIFECYCLE),
    ("leverage_instruction", _LEVERAGE),
    ("framework_sizing", _FRAMEWORK_SIZING),
    ("personal_allocation", _PERSONAL_SIZING),
    ("entry_exit_price", _ENTRY_EXIT_PRICE),
)

#: Text that describes the prohibition itself, or reports somebody else's
#: execution, is not execution. Deliberately narrow and checked per sentence.
_EXECUTION_EXEMPT = re.compile(
    r"\b(?:cannot|can't|can\s+not|(?:do|does|did|is|are|was|were|has|have|had|"
    r"would|could|should)\s+not|don't|doesn't|didn't|isn't|aren't|wasn't|"
    r"weren't|hasn't|haven't|hadn't|wouldn't|couldn't|shouldn't|won't|"
    r"will\s+not|never|no\s+longer|unable\s+to|no\s+ability\s+to|"
    r"not\s+authori[sz]ed|has\s+no|have\s+no|without)\b[^.!?\n]{0,60}?"
    r"(?:order|trade|execut|place|submit|sign|broker|wallet|leverage|"
    r"allocat|invest|expos|weight|position|buy|sell|short|add)"
    r"|\b(?:research\s+only|not\s+investment\s+advice)\b"
    r"|(?:无法|不能|不会|没有|不提供|不支持|未授权)[^。！？\n]{0,20}?"
    r"(?:下单|委托|交易|执行|杠杆|仓位)"
    # A bilingual row reporting that a sizing field is UNAVAILABLE. The English
    # negation patterns look only at English text, so "target allocation 未提供"
    # read as a live sizing instruction. Deliberately a closed list of
    # "not available" phrases — a bare 不/未 would exempt "buy 不要犹豫".
    r"|(?:allocation|exposure|weight(?:ing)?s?|leverage|position\s+size|"
    r"仓位|敞口|配置|持仓|杠杆)\s*[:：|]?\s*"
    r"(?:未提供|不提供|未披露|不适用|不可用|无数据|没有数据|暂无|暂未提供|"
    r"未启用|不存在|未知|N/?A)"
    # Somebody else's book. Reporting that a fund bought 500 BTC is research;
    # the verb list is wider than the placement verbs because the quantified
    # sizing rule above matches ordinary market-flow reporting too.
    r"|\b(?:institutions?|funds?|etfs?|market\s+makers?|whales?|desks?|dealers?|"
    r"the\s+street|traders?|investors?|the\s+(?:system|model|framework|engine)|"
    r"pantheon)\b(?:['’]s)?[^.!?\n]{0,60}?"
    r"(?:placed|submitted|routed|filled|bought|sold|buy|sell|added|accumulated)"
    # Reporting somebody ELSE'S size or leverage is research: "the ETF's target
    # allocation is 60/40", "the fund used 3x leverage in 2024".
    #
    # Pantheon, the system, the model and the framework are deliberately ABSENT
    # from this second subject list. "Pantheon's target allocation is 40% BTC" is
    # Pantheon issuing the sizing itself, which is precisely what the canonical
    # layer refuses to publish, so it must stay fail-closed. A bare "portfolio"
    # is absent for the same reason: it matched "Target portfolio weighting".
    r"|\b(?:institutions?|funds?|etfs?|market\s+makers?|whales?|desks?|"
    r"dealers?|the\s+street|traders?|investors?)\b(?:['’]s)?[^.!?\n]{0,60}?"
    r"(?:allocation|exposure|weight(?:ing)?s?|leverage|position\s+siz)"
    r"|(?:机构|主力|大户|鲸鱼|散户|资金|基金)[^。！？\n]{0,30}?"
    r"(?:买入|卖出|增持|减持|加仓|减仓)",
    re.I,
)

#: Rules no exemption may release. An order-lifecycle command, a leverage
#: instruction, a concrete execution price or framework sizing is never research
#: language whoever the grammatical subject is — "the system says place a limit
#: order at 58,200" is still an executable instruction printed to a subscriber.
UNCONDITIONAL_RULES: Final[frozenset[str]] = frozenset(
    {
        "order_instruction",
        "leverage_instruction",
        "entry_exit_price",
        "framework_sizing",
    }
)


_SENTENCE_END = re.compile(r"(?:[.!?;](?=\s|$)|[。！？；])\s*")


def split_sentences(text: str) -> list[str]:
    """Sentence split, CJK-aware. Shared so the gate and the sanitizer agree."""
    out: list[str] = []
    last = 0
    for match in _SENTENCE_END.finditer(text):
        out.append(text[last : match.end()])
        last = match.end()
    if last < len(text):
        out.append(text[last:])
    return out or [text]


def find_execution_directive(text: str) -> Optional[tuple[str, re.Match[str]]]:
    """Return ``(rule_name, match)`` for the first execution directive, else None.

    Advice is never reported here. Every rule is scoped to one sentence so a
    disclaimer elsewhere in the reply cannot launder an instruction, and so an
    instruction elsewhere cannot condemn a disclaimer.
    """
    if not text:
        return None
    offset = 0
    for sentence in split_sentences(text):
        if not _EXECUTION_EXEMPT.search(sentence):
            for name, pattern in OUTBOUND_RULES:
                match = pattern.search(sentence)
                if match is not None:
                    # Re-anchor into the full text so callers can excerpt it.
                    absolute = pattern.search(text, offset + match.start())
                    return name, (absolute or match)
        offset += len(sentence)
    return None


def is_execution_sentence(sentence: str) -> Optional[tuple[str, str]]:
    """``(rule_name, excerpt)`` when ONE sentence is an execution directive.

    Stricter than :func:`find_execution_directive`, and deliberately so. The
    rules in :data:`UNCONDITIONAL_RULES` are applied here even when the sentence
    carries an exemption, because dropping one sentence out of a paragraph is
    cheap, while withholding the whole reply is not — so the outbound tier keeps
    the exemption and this tier does not.
    """
    if not sentence:
        return None
    exempt = bool(_EXECUTION_EXEMPT.search(sentence))
    for name, pattern in SANITIZER_RULES:
        if exempt and name not in UNCONDITIONAL_RULES:
            continue
        match = pattern.search(sentence)
        if match is not None:
            return name, match.group(0)[:80]
    return None


__all__ = [
    "ALLOWED_ADVICE_TERMS",
    "OUTBOUND_RULES",
    "SANITIZER_RULES",
    "UNCONDITIONAL_RULES",
    "find_execution_directive",
    "is_execution_sentence",
    "split_sentences",
]
