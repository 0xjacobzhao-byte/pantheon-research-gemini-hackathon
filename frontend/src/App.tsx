import { useState, useEffect, useCallback } from "react";
import {
  fetchProject,
  fetchDemoFlow,
  fetchComparison,
  fetchAlibabaProof,
  fetchDataQuality,
  fetchModules,
  fetchTickerProfile,
  fetchProviderHealth,
  fetchValidationTimeline,
  fetchMacroMini,
  fetchMarketPulseMini,
  fetchFiccMini,
  fetchGeminiOverlay,
  fetchGeminiProof,
  type ProjectInfo,
  type DemoFlow,
  type ComparisonResult,
  type AlibabaCloudProof,
  type DataQualityReport,
  type ModuleSnapshotGridData,
  type TickerProfile,
  type ProviderHealthData,
  type ValidationTimelineData,
  type MacroMiniPanelData,
  type MarketPulseMiniPanelData,
  type FiccMiniPanelData,
  type QualitativeOverlay,
  type GeminiProof,
} from "./api";
import OverlayComparisonPanel from "./components/equity/OverlayComparisonPanel";
import DataQualityPanel from "./components/DataQualityPanel";
import ModuleSnapshotGrid from "./components/ModuleSnapshotGrid";
import TickerProfilePanel from "./components/TickerProfilePanel";
import ProviderHealthPanel from "./components/ProviderHealthPanel";
import ValidationTimeline from "./components/ValidationTimeline";
import MacroMiniPanel from "./components/MacroMiniPanel";
import MarketPulseMiniPanel from "./components/MarketPulseMiniPanel";
import FiccMiniPanel from "./components/FiccMiniPanel";
import GeminiOverlayPanel from "./components/GeminiOverlayPanel";

const TICKERS = ["MA", "NVDA"];

function App() {
  const [project, setProject] = useState<ProjectInfo | null>(null);
  const [demoFlow, setDemoFlow] = useState<DemoFlow | null>(null);
  const [proof, setProof] = useState<AlibabaCloudProof | null>(null);
  const [dataQuality, setDataQuality] = useState<DataQualityReport | null>(null);
  const [modules, setModules] = useState<ModuleSnapshotGridData | null>(null);
  const [providerHealth, setProviderHealth] = useState<ProviderHealthData | null>(null);
  const [timeline, setTimeline] = useState<ValidationTimelineData | null>(null);
  const [macro, setMacro] = useState<MacroMiniPanelData | null>(null);
  const [marketPulse, setMarketPulse] = useState<MarketPulseMiniPanelData | null>(null);
  const [ficc, setFicc] = useState<FiccMiniPanelData | null>(null);
  const [geminiProof, setGeminiProof] = useState<GeminiProof | null>(null);
  const [geminiOverlay, setGeminiOverlay] = useState<QualitativeOverlay | null>(null);
  const [selected, setSelected] = useState<string>("");
  const [comparison, setComparison] = useState<ComparisonResult | null>(null);
  const [tickerProfile, setTickerProfile] = useState<TickerProfile | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetchProject().then(setProject).catch(() => {});
    fetchDemoFlow().then(setDemoFlow).catch(() => {});
    fetchAlibabaProof().then(setProof).catch(() => {});
    fetchDataQuality().then(setDataQuality).catch(() => {});
    fetchModules().then(setModules).catch(() => {});
    fetchProviderHealth().then(setProviderHealth).catch(() => {});
    fetchValidationTimeline().then(setTimeline).catch(() => {});
    fetchMacroMini().then(setMacro).catch(() => {});
    fetchMarketPulseMini().then(setMarketPulse).catch(() => {});
    fetchFiccMini().then(setFicc).catch(() => {});
    fetchGeminiProof().then(setGeminiProof).catch(() => {});
  }, []);

  const handleCompare = useCallback(async () => {
    if (!selected) return;
    setLoading(true);
    setError(null);
    setTickerProfile(null);
    setGeminiOverlay(null);
    try {
      const [comp, profile, gemini] = await Promise.all([
        fetchComparison(selected),
        fetchTickerProfile(selected).catch(() => null),
        fetchGeminiOverlay(selected).catch(() => null),
      ]);
      setComparison(comp);
      setTickerProfile(profile);
      setGeminiOverlay(gemini);
    } catch (e) {
      setError(e instanceof Error ? e.message : "Unknown error");
    } finally {
      setLoading(false);
    }
  }, [selected]);

  const ev = comparison?.evidence;

  return (
    <div className="app">
      <header className="hero">
        <h1>Pantheon Research — Gemini Hackathon</h1>
        <p className="subtitle">
          Gemini-powered investment research overlay for human-in-the-loop
          financial decision intelligence. Qwen and DeepSeek serve as secondary
          comparison models.
        </p>
        {project && (
          <p className="demo-mode">
            Mode: {project.demo_mode} · v{project.version}
          </p>
        )}
      </header>

      {/* Gemini proof banner */}
      {geminiProof && (
        <section className="card" style={{ borderTop: "3px solid #4285f4" }}>
          <h2>Gemini Integration</h2>
          <p className="section-lead">
            The Gemini Analyst layer is the hackathon-specific AI research feature.
            Gemini converts structured evidence packs into explainable financial
            research overlays. Gemini does not execute trades — humans remain
            final decision-makers.
          </p>
          <div className="alibaba-grid">
            <div className="alibaba-item">
              <span className="label">Provider</span>
              <span className="value">{geminiProof.provider}</span>
            </div>
            <div className="alibaba-item">
              <span className="label">Model</span>
              <span className="value">{geminiProof.model}</span>
            </div>
            <div className="alibaba-item">
              <span className="label">Demo Mode</span>
              <span className="value">{geminiProof.demo_mode}</span>
            </div>
            <div className="alibaba-item">
              <span className="label">Credential</span>
              <span className="value">
                {geminiProof.credential_configured
                  ? "configured"
                  : "not set (offline samples)"}
              </span>
            </div>
            <div className="alibaba-item">
              <span className="label">Prompt</span>
              <span className="value">{geminiProof.prompt_version}</span>
            </div>
            <div className="alibaba-item">
              <span className="label">External Calls</span>
              <span className="value">
                {geminiProof.proof_endpoint_external_calls ? "yes" : "none (secret-free)"}
              </span>
            </div>
          </div>
          <details className="proof-claims" style={{ marginTop: "1rem" }}>
            <summary>Safe claims &amp; non-claims</summary>
            <div className="claims-grid">
              <div>
                <h4>Safe claims</h4>
                <ul>
                  {geminiProof.safe_claims.map((c, i) => (
                    <li key={i}>{c}</li>
                  ))}
                </ul>
              </div>
              <div>
                <h4>Non-claims</h4>
                <ul>
                  {geminiProof.non_claims.map((c, i) => (
                    <li key={i}>{c}</li>
                  ))}
                </ul>
              </div>
            </div>
          </details>
        </section>
      )}

      {/* Four-layer architecture */}
      <section className="card">
        <h2>Four-Layer Architecture</h2>
        <div className="arch-layers">
          {(project?.architecture_layers ||
            demoFlow?.architecture_layers || [
              "Strategy",
              "Information",
              "Signal",
              "Trading",
            ]).map((layer, i, arr) => (
            <div key={layer} className="arch-layer">
              <span className="layer-num">{i + 1}</span>
              <span className="layer-name">{layer}</span>
              {i < arr.length - 1 && <span className="arch-arrow">→</span>}
            </div>
          ))}
        </div>
        <p className="arch-desc">
          Strategy → Information (evidence pack) → Signal (Gemini + dual-LLM overlay) →
          Trading — every signal gated by human review.
        </p>
      </section>

      {/* System scope — module snapshot grid */}
      {modules && (
        <section className="card">
          <h2>System Scope — Module Snapshots</h2>
          <p className="section-lead">
            Pantheon Research is a multi-asset research operating system. This grid
            maps its full scope (Macro · TA · FICC · Equity · Research-Ops) with
            each module&apos;s honest governance state.
          </p>
          <ModuleSnapshotGrid grid={modules} />
        </section>
      )}

      {/* Multi-asset context mini panels */}
      {(macro || marketPulse || ficc) && (
        <section className="card">
          <h2>Multi-Asset Context (Context-Only)</h2>
          <p className="section-lead">
            Illustrative panels showing the shape of Pantheon Research&apos;s Macro, TA, and FICC modules.
            Not investment advice. Values are bundled samples, not live feeds.
          </p>
          <div className="mini-panels-grid">
            {macro && <MacroMiniPanel data={macro} />}
            {marketPulse && <MarketPulseMiniPanel data={marketPulse} />}
            {ficc && <FiccMiniPanel data={ficc} />}
          </div>
        </section>
      )}

      {/* Provider Health */}
      {providerHealth && (
        <section className="card">
          <ProviderHealthPanel data={providerHealth} />
        </section>
      )}

      {/* Ticker panel */}
      <section className="card">
        <h2>Run an Analysis</h2>
        <p className="section-lead">
          Select a ticker to load the Gemini Analyst overlay alongside the
          Qwen vs DeepSeek comparison.
        </p>
        <div className="ticker-panel">
          {TICKERS.map((t) => (
            <button
              key={t}
              className={`ticker-btn ${selected === t ? "selected" : ""}`}
              onClick={() => setSelected(t)}
            >
              {t}
            </button>
          ))}
          <button
            className="run-btn"
            onClick={handleCompare}
            disabled={!selected || loading}
          >
            {loading ? "Analyzing…" : "Run Analysis"}
          </button>
        </div>
        {error && <div className="error-box">{error}</div>}
      </section>

      {/* Ticker Profile (production-feel) */}
      {tickerProfile && (
        <section className="card">
          <h2>Ticker Profile</h2>
          <TickerProfilePanel profile={tickerProfile} />
        </section>
      )}

      {/* Evidence pack */}
      {ev && (
        <section className="card">
          <h2>
            Evidence Pack — {ev.company_name} ({ev.ticker})
          </h2>
          <p className="meta">
            {ev.exchange} · {ev.sector} · {ev.industry}
            {comparison?.evidence_hash && (
              <>
                {" "}
                · <code className="oc-hash">{comparison.evidence_hash.slice(0, 22)}…</code>
              </>
            )}
          </p>
          <p>{ev.summary}</p>
          <div className="metrics-grid">
            {ev.pe_ratio != null && <span>P/E: {ev.pe_ratio}</span>}
            {ev.pb_ratio != null && <span>P/B: {ev.pb_ratio}</span>}
            {ev.roic_pct != null && <span>ROIC: {ev.roic_pct}%</span>}
            {ev.fcf_ttm_usd != null && (
              <span>FCF: ${ev.fcf_ttm_usd.toLocaleString()}</span>
            )}
            {ev.revenue_growth_yoy_pct != null && (
              <span>Rev Growth: {ev.revenue_growth_yoy_pct}%</span>
            )}
            {ev.gross_margin_pct != null && (
              <span>Gross Margin: {ev.gross_margin_pct}%</span>
            )}
            {ev.net_margin_pct != null && (
              <span>Net Margin: {ev.net_margin_pct}%</span>
            )}
            {ev.debt_to_equity != null && <span>D/E: {ev.debt_to_equity}</span>}
          </div>
        </section>
      )}

      {/* Gemini Analyst Overlay — PRIMARY */}
      {geminiOverlay && (
        <section className="card" style={{ borderTop: "3px solid #4285f4" }}>
          <h2>Gemini Analyst Overlay</h2>
          <p className="section-lead">
            Gemini-powered qualitative research overlay — this is the
            hackathon-specific AI analyst layer. Gemini does not execute trades.
            All outputs are research overlays reviewed by humans.
          </p>
          <GeminiOverlayPanel overlay={geminiOverlay} />
          <p className="safety-text" style={{ marginTop: "1rem", fontStyle: "italic" }}>
            Human-in-the-loop: Gemini outputs are research overlays, not trade signals.
            A human portfolio manager always makes the final decision.
          </p>
        </section>
      )}

      {/* Qwen vs DeepSeek comparison — SECONDARY */}
      {comparison && (
        <section className="card">
          <h2>Qwen vs DeepSeek — Secondary Comparison</h2>
          <p className="section-lead">
            For additional context, Qwen and DeepSeek provide independent overlays.
            The Gemini Analyst overlay above is the primary hackathon submission feature.
          </p>
          <OverlayComparisonPanel comparison={comparison} />
        </section>
      )}

      {/* Alibaba Cloud proof (secondary context) */}
      {proof && (
        <section className="card">
          <details>
            <summary style={{ cursor: "pointer", fontWeight: 600 }}>
              Platform Deployment Proof (Alibaba Cloud — secondary context)
            </summary>
            <p className="proof-schema" style={{ marginTop: "0.5rem" }}>
              schema <code>{proof.schema_version}</code> · git{" "}
              <code>{proof.git_sha}</code> · {proof.demo_mode} mode
            </p>
            <div className="alibaba-grid">
              <div className="alibaba-item">
                <span className="label">Compute Host</span>
                <span className="value">{proof.host_runtime}</span>
              </div>
              <div className="alibaba-item">
                <span className="label">Backend</span>
                <span className="value">{proof.backend_runtime}</span>
              </div>
              <div className="alibaba-item">
                <span className="label">Database</span>
                <span className="value">{proof.database.provider}</span>
              </div>
            </div>
          </details>
        </section>
      )}

      {/* Research-Ops mini: data quality */}
      {dataQuality && (
        <section className="card">
          <h2>Research-Ops · Data Quality</h2>
          <DataQualityPanel report={dataQuality} />
        </section>
      )}

      {/* Validation Timeline */}
      {timeline && (
        <section className="card">
          <ValidationTimeline data={timeline} />
        </section>
      )}

      {/* Safety statement */}
      <section className="card safety-card">
        <h2>Safety &amp; Human-in-the-Loop Statement</h2>
        <p className="safety-text">
          LLMs do not execute trades; a human remains the portfolio manager.
        </p>
        <p className="safety-text">
          Pantheon Research is not an autonomous trading bot. It is a
          framework-first, data-governed, human-in-the-loop AI research
          operating system. The Gemini Analyst layer produces explainable
          research overlays — not trade signals, not alpha, not investment advice.
        </p>
        <p className="safety-text">
          This public repository is a sanitized vertical slice; the production
          system stays private.
        </p>
      </section>

      <footer>
        <p>
          Apache-2.0 · Built for the Gemini Hackathon ·{" "}
          <a
            href="https://github.com/0xjacobzhao-byte/pantheon-research-gemini-hackathon"
            target="_blank"
            rel="noopener noreferrer"
          >
            GitHub
          </a>
        </p>
      </footer>
    </div>
  );
}

export default App;
