/**
 * GeminiOverlayPanel — displays the Gemini-powered qualitative overlay
 * for a given ticker. Shows model, status, takeaway, risk summary,
 * missing evidence, confidence, and human review notes.
 */

import type { QualitativeOverlay } from "../api";

const STATUS_COLORS: Record<string, string> = {
  SUCCESS: "#16a34a",
  OFFLINE_SAMPLE: "#2563eb",
  BLOCKED_BY_MISSING_CREDENTIAL: "#dc2626",
  API_ERROR: "#dc2626",
  PARSE_ERROR: "#dc2626",
};

function Badge({ text, color }: { text: string; color: string }) {
  return (
    <span className="badge" style={{ backgroundColor: color }}>
      {text}
    </span>
  );
}

export default function GeminiOverlayPanel({
  overlay,
}: {
  overlay: QualitativeOverlay;
}) {
  const statusColor = STATUS_COLORS[overlay.status] ?? "#6b7280";
  const a = overlay.assessment;

  return (
    <div className="gemini-overlay-panel" data-testid="gemini-overlay-panel">
      <div className="provider-card" style={{ borderTop: "3px solid #4285f4" }}>
        <div className="provider-card-header">
          <div className="provider-title-row">
            <h3>Google Gemini</h3>
            <Badge text={overlay.status} color={statusColor} />
          </div>
          <div className="provider-meta">
            <span className="model-name">{overlay.model}</span>
            {overlay.latency_ms != null && (
              <span className="latency">{overlay.latency_ms} ms</span>
            )}
          </div>
          {overlay.prompt_version && (
            <div className="provider-versions">
              prompt {overlay.prompt_version} · schema {overlay.output_schema_version}
            </div>
          )}
        </div>

        {!a && overlay.error_message && (
          <div className="error-box fail-closed" role="alert">
            <strong>Fail-closed:</strong> {overlay.error_message}
          </div>
        )}

        {overlay.takeaway && (
          <div className="gemini-section">
            <h4>Takeaway</h4>
            <p>{overlay.takeaway}</p>
          </div>
        )}

        {a && (
          <>
            <div className="assessment-grid">
              <div className="assessment-field">
                <h4>Business Quality</h4>
                <p>{a.business_quality || "—"}</p>
              </div>
              <div className="assessment-field">
                <h4>Moat</h4>
                <p>{a.moat || "—"}</p>
              </div>
              <div className="assessment-field">
                <h4>Pricing Power</h4>
                <p>{a.pricing_power || "—"}</p>
              </div>
              <div className="assessment-field">
                <h4>Capital Allocation</h4>
                <p>{a.capital_allocation || "—"}</p>
              </div>
              <div className="assessment-field">
                <h4>Red Flags & Risks</h4>
                <p>{a.red_flags || "—"}</p>
              </div>
              <div className="assessment-field confidence-field">
                <h4>Confidence</h4>
                <div className="confidence-bar">
                  <div
                    className="confidence-fill"
                    style={{
                      width: `${a.confidence * 100}%`,
                      backgroundColor: "#4285f4",
                    }}
                  />
                  <span>{Math.round(a.confidence * 100)}%</span>
                </div>
              </div>
            </div>

            {a.missing_evidence.length > 0 && (
              <div className="gemini-section">
                <h4>Missing Evidence</h4>
                <ul className="gap-list">
                  {a.missing_evidence.map((g, i) => (
                    <li key={i}>{g}</li>
                  ))}
                </ul>
              </div>
            )}
          </>
        )}
      </div>
    </div>
  );
}
