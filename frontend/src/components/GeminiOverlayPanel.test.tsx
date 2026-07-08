import { describe, it, expect } from "vitest";
import { render, screen } from "@testing-library/react";
import GeminiOverlayPanel from "./GeminiOverlayPanel";
import type { QualitativeOverlay } from "../api";

const sampleOverlay: QualitativeOverlay = {
  provider: "gemini",
  model: "gemini-2.0-flash",
  ticker: "NVDA",
  status: "OFFLINE_SAMPLE",
  takeaway: "NVIDIA commands a dominant position in AI computing.",
  assessment: {
    business_quality: "Exceptional.",
    moat: "Wide moat from CUDA.",
    pricing_power: "Strong.",
    capital_allocation: "Strategic.",
    red_flags: "Geopolitical risk.",
    confidence: 0.78,
    missing_evidence: ["No real-time data"],
  },
  error_message: null,
  latency_ms: null,
  attempts: 1,
  prompt_version: "gemini-overlay-v1.0",
  output_schema_version: "overlay-assessment-1.0",
  usage: null,
};

describe("GeminiOverlayPanel", () => {
  it("renders the panel with overlay data", () => {
    render(<GeminiOverlayPanel overlay={sampleOverlay} />);
    expect(screen.getByTestId("gemini-overlay-panel")).toBeTruthy();
    expect(screen.getByText("Google Gemini")).toBeTruthy();
    expect(screen.getByText("OFFLINE_SAMPLE")).toBeTruthy();
  });

  it("shows fail-closed state when no assessment", () => {
    const blocked: QualitativeOverlay = {
      ...sampleOverlay,
      status: "BLOCKED_BY_MISSING_CREDENTIAL",
      assessment: null,
      takeaway: "",
      error_message: "GEMINI_API_KEY is not set",
    };
    render(<GeminiOverlayPanel overlay={blocked} />);
    expect(screen.getByText(/GEMINI_API_KEY is not set/)).toBeTruthy();
  });
});
