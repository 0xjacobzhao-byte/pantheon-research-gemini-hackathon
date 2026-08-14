# Assets

Visual and captured-artifact assets for the README and judging docs.

## Captured (committed)

No captured artifacts are currently committed in this directory. Submission
screenshots live under [`assets/submission/`](../../assets/submission/) at the
repo root — see that directory's `README.md` for the naming contract.

## Screenshots (TODO — capture from the live/local demo)

Screenshots were not auto-captured in the build environment (headless browser
unavailable). To add them, run the demo locally (`docker compose up --build`)
or open the live product, capture the frames below, and drop the PNGs here —
the README will reference them once present.

| File | What to capture | Source |
|------|----------------|--------|
| `demo_overlay_comparison.png` | OverlayComparisonPanel on NVDA: Qwen vs DeepSeek cards, agreement score, divergences, human-review gate | `http://localhost:5173` → select NVDA → Run Comparison, or `https://pantheon-research.com` Ticker Profile → Qwen vs DeepSeek |
| `module_snapshot_grid.png` | ModuleSnapshotGrid (System Scope): Macro / TA / FICC / Equity / Qwen-vs-DeepSeek / Data Quality cards with per-module `data_state` | `/api/modules` rendered at the top of the demo cockpit |
| `data_quality_panel.png` | DataQualityPanel (Research-Ops): provider config, coverage, per-ticker data_state table | Data Quality tab in frontend |
| `judge_quickstart.png` | Terminal running `./scripts/judge_smoke.sh` all green | Local terminal after `docker compose up --build` |

**Image rules:**
- PNG or JPG, ideally < 500 KB each
- No secrets, admin tokens, DB URLs, API keys, or browser auth headers
- Crop to product UI / proof JSON only
