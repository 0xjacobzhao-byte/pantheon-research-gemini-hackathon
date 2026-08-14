/**
 * Sanitized production reference.
 * Source: private Pantheon Research production repository.
 * Snapshot date: 2026-08-14.
 * Secrets, provider-specific configuration, operational details, and proprietary
 * strategy logic removed where applicable.
 *
 * Removed for publication: deployment-target references, and two internal
 * imports (`apiUrl`, `LlmQualitativeOverlay`) replaced with local declarations
 * so this file reads standalone. The comparison contract itself — provider set,
 * agreement scoring, divergence, evidence discipline, and the two analysis
 * lanes — is published unchanged.
 *
 * ---
 *
 * API client for the multi-provider equity overlay-comparison endpoint.
 *
 * This is the contract that makes Pantheon's model comparison auditable rather
 * than decorative. Note what it carries and what it deliberately does not:
 *
 *   - Every provider reports its own `ProviderOverlayState` — a provider that
 *     failed, was skipped, or produced nothing stays visible as that state. It
 *     is never dropped from the response, because a silently absent provider
 *     reads as agreement.
 *   - `MajorDivergence` is a first-class field. Disagreement between models is
 *     surfaced to the reader, not averaged into a consensus number.
 *   - `AnalysisLane` splits `evidence_backed` from `model_inferred`. An AI prior
 *     can never present itself as source-backed.
 *   - `MultiComparisonStatus` can be `NOT_COMPARABLE`. When the providers
 *     answered different questions, the correct output is a refusal to compare,
 *     not a fabricated agreement score.
 */

// Local stand-ins for two internal imports, so this reference file is readable
// standalone. In production these come from the shared API-URL helper and the
// equity overlay schema module respectively.
declare function apiUrl(path: string): string;

/** Opaque in this reference: the validated per-provider qualitative overlay. */
type LlmQualitativeOverlay = Record<string, unknown>;

// ── Data State Constants (mirror backend OverlayDataState) ──────────────────
export type OverlayComparisonDataState =
  | "HEALTHY_REAL_DATA"
  | "PARTIAL_QWEN_AVAILABLE"
  | "QWEN_NOT_GENERATED"
  | "QWEN_BLOCKED_BY_MISSING_CREDENTIAL"
  | "QWEN_GENERATION_FAILED"
  | "DEEPSEEK_NOT_AVAILABLE"
  | "ERROR";

// ── Factor Comparison ───────────────────────────────────────────────────────
export interface FactorComparisonSide {
  verdict: string | null;
  evidence_count: number;
  has_summary: boolean;
}

export interface FactorComparison {
  factor: string;
  label: string;
  deepseek: FactorComparisonSide | null;
  qwen: FactorComparisonSide | null;
  agreement: boolean | null;
}

// ── Agreement Summary ───────────────────────────────────────────────────────
export interface AgreementSummary {
  total_factors: number;
  comparable_factors: number;
  agreeing_factors: number;
  disagreeing_factors: number;
  agreement_rate: number | null;
  factors_with_agreement: string[];
  factors_with_disagreement: string[];
}

// ── Evidence Discipline ─────────────────────────────────────────────────────
export interface EvidenceDisciplineSide {
  evidence_tier: string | null;
  evidence_tier_label: string | null;
  source_pack_coverage_score: number | null;
  source_pack_evidence_ready: boolean | null;
  can_render_qualitative_brief: boolean | null;
}

export interface EvidenceDiscipline {
  deepseek: EvidenceDisciplineSide;
  qwen: EvidenceDisciplineSide;
}

// ── Risk Coverage ───────────────────────────────────────────────────────────
export interface RiskCoverage {
  deepseek_risk_count: number;
  qwen_risk_count: number;
  overlapping_risk_topics: string[];
  deepseek_only_risks: number;
  qwen_only_risks: number;
}

// ── Model Info ──────────────────────────────────────────────────────────────
export interface ModelInfo {
  provider: string | null;
  model: string | null;
  as_of: string | null;
}

// ── Multi-provider (V1.9) ───────────────────────────────────────────────────
// Mirrors `build_multi_provider_comparison` in
// backend_gateway/services/equity_overlay_comparison.py.

/** The five overlay providers, in contractual display order. */
export type OverlayProvider =
  | "deepseek"
  | "qwen"
  | "claude"
  | "chatgpt"
  | "gemini";

export const OVERLAY_PROVIDER_ORDER: readonly OverlayProvider[] = [
  "deepseek",
  "qwen",
  "claude",
  "chatgpt",
  "gemini",
] as const;

export const OVERLAY_PROVIDER_LABELS: Record<OverlayProvider, string> = {
  deepseek: "DeepSeek Analysis",
  qwen: "Qwen Analysis",
  claude: "Claude Analysis",
  chatgpt: "ChatGPT Analysis",
  gemini: "Gemini Analysis",
};

/**
 * Order the model views are presented in. Distinct from OVERLAY_PROVIDER_ORDER,
 * which mirrors the backend's contractual order and is what `providers_available`
 * / `provider_order` are counted against. Display order is a product decision and
 * must stay stable even when a provider has no cached overlay.
 */
export const OVERLAY_PROVIDER_DISPLAY_ORDER: readonly OverlayProvider[] = [
  "claude",
  "chatgpt",
  "deepseek",
  "qwen",
  "gemini",
] as const;

/** Provider names as a reader should see them. Never the raw payload key. */
export const OVERLAY_PROVIDER_DISPLAY_NAMES: Record<OverlayProvider, string> = {
  claude: "Claude",
  chatgpt: "ChatGPT",
  deepseek: "DeepSeek",
  qwen: "Qwen",
  gemini: "Gemini",
};

/**
 * Honest per-provider states. There is deliberately no state meaning "assume
 * success" — a provider is SUCCESS only when a usable cached overlay exists.
 */
export type ProviderOverlayState =
  | "SUCCESS"
  | "NOT_GENERATED"
  | "BLOCKED_BY_MISSING_CREDENTIAL"
  | "API_ERROR"
  | "PARSE_ERROR"
  | "STALE"
  | "INSUFFICIENT_EVIDENCE"
  // A usable overlay exists, but only under a smoke/probe model (e.g.
  // gemini-2.5-flash) rather than the family's formal analyst model. Shown for
  // audit; never counted as that family's analysis.
  | "FALLBACK_MODEL_ONLY";

export type MultiComparisonStatus = "COMPARABLE" | "NOT_COMPARABLE";

export interface MultiProviderModelInfo {
  provider: string | null;
  model: string | null;
  as_of: string | null;
  state: ProviderOverlayState;
  cached_status: string | null;
  display_name: string;
}

export interface MultiFactorComparison {
  factor: string;
  label: string;
  verdicts: Partial<Record<OverlayProvider, string>>;
  comparable: boolean;
  agreement: boolean | null;
}

export interface MajorDivergence {
  field: string;
  label: string;
  verdicts: Partial<Record<OverlayProvider, string>>;
  distinct_verdicts: string[];
}

export interface ProviderEvidence {
  evidence_tier: string | null;
  evidence_tier_label: string | null;
  mean_confidence: number | null;
}

// ── Dual-lane (model-inferred AI prior) block ───────────────────────────────
// Mirrors backend_gateway/services/equity_llm_qualitative/model_inferred.py.
// A model-inferred overlay is an AI prior: NOT source-backed, never affects
// the canonical rating, and must always render with a clear "AI prior" badge.

export type AnalysisLane = "evidence_backed" | "model_inferred";

export type ProviderLaneState =
  | "SUCCESS_EVIDENCE_BACKED"
  | "SUCCESS_MODEL_INFERRED"
  | "MISSING"
  | "ERROR"
  | "STALE";

export interface ModelInferredFactor {
  factor_name: string;
  prior_verdict: "positive" | "neutral" | "negative" | "uncertain";
  confidence: "high" | "medium" | "low";
  reasoning: string;
  basis_type: string;
  source_backed: false;
  needs_verification: boolean;
  verification_question: string | null;
}

export interface ModelInferredOverlay {
  market: string;
  ticker: string;
  canonical_symbol: string;
  company_name: string;
  provider: string;
  model: string;
  as_of: string;
  expires_at: string;
  analysis_lane: "model_inferred";
  status: "ok";
  evidence_tier: "MODEL_INFERRED";
  source_policy: "not_source_backed";
  canonical_signal: null;
  does_not_affect_rating: true;
  overall_prior: "constructive" | "balanced" | "cautious" | "uncertain";
  confidence: "high" | "medium" | "low";
  factors: ModelInferredFactor[];
  evidence_gaps: string[];
  research_questions: string[];
  verification_tasks: string[];
  limitations: string[];
  is_fresh?: boolean;
  snapshot_created_at?: string | null;
}

export interface MultiProviderComparison {
  provider_order: OverlayProvider[];
  provider_states: Record<OverlayProvider, ProviderOverlayState>;
  providers_available: OverlayProvider[];
  providers_missing: OverlayProvider[];
  providers_degraded: Partial<Record<OverlayProvider, ProviderOverlayState>>;
  models: Record<OverlayProvider, MultiProviderModelInfo>;
  disclaimer: string;
  overlays?: Partial<Record<OverlayProvider, LlmQualitativeOverlay | null>>;

  status: MultiComparisonStatus;
  not_comparable_reason: string | null;
  /** `null` when no factor had two or more comparable verdicts — never faked to 0 or 1. */
  agreement_score: number | null;
  /** `null` when fewer than two providers declared a confidence. Never coerced to 0. */
  confidence_dispersion: number | null;
  consensus_summary: string | null;
  factor_comparisons: MultiFactorComparison[];
  major_divergences: MajorDivergence[];
  risk_disagreement: boolean | null;
  evidence: Partial<Record<OverlayProvider, ProviderEvidence>>;
  weak_evidence_providers?: OverlayProvider[];
  human_review_required: boolean;
  human_review_reasons: string[];

  /** Dual-lane additive block — optional so a stale backend cannot break the page. */
  provider_lanes?: Partial<Record<OverlayProvider, AnalysisLane | null>>;
  lane_states?: Partial<Record<OverlayProvider, ProviderLaneState>>;
  model_inferred_overlays?: Partial<
    Record<OverlayProvider, ModelInferredOverlay | null>
  >;
  model_inferred_disclaimer?: string;
}

// ── Model Comparison Summary (LLM Research cockpit) ─────────────────────────
// Mirrors the backend `model_comparison_summary` block. This is the reader-facing
// synthesis that leads the panel: a human takeaway, a confidence read, a
// bull/base/bear frame, consensus + divergence, and next verification tasks.
// It NEVER presents an AI-prior conclusion as source-backed — every claim carries
// an explicit support level / lane so the reader can tell evidence from prior.

export type SummaryDirection = "positive" | "neutral" | "cautious";
export type SummarySupportLevel = "evidence_backed" | "mixed" | "ai_prior_only";
export type SummaryLane = "evidence_backed" | "ai_prior";
export type SummaryPriority = "P0" | "P1" | "P2";
export type SummaryConfidenceLabel = "low" | "medium" | "high" | "unknown";

export interface SummaryConsensusItem {
  factor: string;
  label: string;
  direction: SummaryDirection;
  summary: string;
  support_level: SummarySupportLevel;
  supporting_providers: string[];
  confidence: number;
  why_it_matters: string;
}

export interface SummaryDivergenceItem {
  factor: string;
  label: string;
  providers_positive: string[];
  providers_negative: string[];
  providers_neutral: string[];
  likely_reason:
    | "source_difference"
    | "stale_evidence"
    | "model_style"
    | "missing_evidence";
  severity: "high" | "moderate";
  summary: string;
  research_implication: string;
}

export interface SummaryEvidenceConclusion {
  factor: string;
  label: string;
  providers: string[];
  verdicts: Record<string, string>;
}

export interface SummaryEvidenceHierarchy {
  evidence_backed_conclusions: SummaryEvidenceConclusion[];
  ai_prior_conclusions: SummaryEvidenceConclusion[];
  missing_evidence: Array<{ factor: string; label: string }>;
  stale_or_blocked_sources: Array<{ provider: string; state: string }>;
}

export interface SummaryConfidence {
  provider_agreement_score: number | null;
  evidence_support_score: number | null;
  identity_confidence_score: number | null;
  freshness_score: number | null;
  overall_llm_confidence: number | null;
  overall_label: SummaryConfidenceLabel;
  basis: string;
}

export interface SummaryScenario {
  case: string;
  support_level: string;
  needed_evidence: string[];
}

export interface SummaryBullBaseBear {
  bull: SummaryScenario;
  base: SummaryScenario;
  bear: SummaryScenario;
}

export interface SummaryRisk {
  risk: string;
  lane: SummaryLane;
  providers: string[];
}

export interface SummaryVerificationTask {
  market: string;
  ticker: string;
  company_name: string;
  factor: string | null;
  question: string;
  needed_evidence: string;
  reason: string;
  priority: SummaryPriority;
  source_provider: string | null;
  source_lane: string;
  suggested_owner: string;
  status: string;
}

export interface SummaryProviderQuality {
  display_name: string;
  evidence_state: string | null;
  lane_state: string | null;
  best_lane: string | null;
  evidence_tier: string | null;
  evidence_tier_label: string | null;
  has_evidence_body: boolean;
  has_model_inferred_prior: boolean;
  model_inferred_fresh: boolean | null;
}

export interface SummarySourceLimitation {
  limitation: string;
  lane: SummaryLane;
  providers: string[];
}

export interface ModelComparisonSummary {
  market: string;
  ticker: string;
  company_name: string | null;
  human_takeaway: string;
  consensus: SummaryConsensusItem[];
  divergence: SummaryDivergenceItem[];
  evidence_hierarchy: SummaryEvidenceHierarchy;
  confidence: SummaryConfidence;
  bull_base_bear: SummaryBullBaseBear;
  top_risks: SummaryRisk[];
  next_verification_tasks: SummaryVerificationTask[];
  provider_quality: Record<string, SummaryProviderQuality>;
  source_limitations: SummarySourceLimitation[];
  model_inferred_disclaimer: string;
  disclaimer: string;
}

// ── Comparison Response ─────────────────────────────────────────────────────
export interface OverlayComparisonResponse {
  ticker: string;
  market: string;
  data_state: OverlayComparisonDataState;
  generated_at: string;
  overlays: {
    deepseek: LlmQualitativeOverlay | null;
    qwen: LlmQualitativeOverlay | null;
    claude?: LlmQualitativeOverlay | null;
    chatgpt?: LlmQualitativeOverlay | null;
    gemini?: LlmQualitativeOverlay | null;
  };
  comparison: {
    factor_comparisons: FactorComparison[];
    agreement_summary: AgreementSummary;
    evidence_discipline: EvidenceDiscipline;
    risk_coverage: RiskCoverage;
  } | null;
  differences: {
    aggregate_overlay: {
      deepseek: string | null;
      qwen: string | null;
      match: boolean;
    };
    evidence_tier: {
      deepseek: string | null;
      qwen: string | null;
    };
  } | null;
  limitations: {
    deepseek: string[];
    qwen: string[];
  };
  models: {
    deepseek: ModelInfo;
    qwen: ModelInfo;
  };
  /** V1.9 additive block. Optional so a stale backend cannot break the page. */
  multi_provider?: MultiProviderComparison;
  /**
   * Reader-facing synthesis that leads the panel. Optional so a stale backend
   * cannot break the page; when present it renders as the cockpit card above the
   * consensus header.
   */
  model_comparison_summary?: ModelComparisonSummary | null;
  _disclaimer?: string;
}

// ── Fetch Function ──────────────────────────────────────────────────────────
async function _getJson<T>(path: string): Promise<T> {
  const res = await fetch(apiUrl(path), {
    headers: { Accept: "application/json" },
  });
  if (!res.ok) {
    throw new Error(
      `overlay comparison fetch failed: ${res.status} ${res.statusText}`,
    );
  }
  return (await res.json()) as T;
}

export function fetchOverlayComparison(
  market: string,
  ticker: string,
): Promise<OverlayComparisonResponse> {
  const m = encodeURIComponent(market.trim().toUpperCase());
  const t = encodeURIComponent(ticker.trim().toUpperCase());
  return _getJson<OverlayComparisonResponse>(
    `/api/equity/overlay-comparison/${m}/${t}`,
  );
}
