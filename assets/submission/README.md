# Submission Assets

Judge-facing product screenshots for this submission.

**Status:** the image files are **not yet committed to this repository.** They
are currently published in the
[Devpost gallery](https://devpost.com/software/pantheon-research-qzn50k), which
is the authoritative source for the submission screenshots today.

This file fixes the naming contract and ordering so the PNGs can be dropped in
without renaming anything or updating links elsewhere.

---

## Naming contract

| # | Filename | Shows |
|---|---|---|
| 01 | `01_Pantheon_Agent_Workflow.png` | Agent workflow and capability surface |
| 02 | `02_AI_Analyst_Consensus_Dashboard.png` | Five-model consensus dashboard |
| 03 | `03_Gemini_Multi_Model_Analysis.png` | Gemini overlay within multi-model comparison |
| 04 | `04_LLM_Research_Summary.png` | LLM research summary (GOOGL) |
| 05 | `05_Equity_Ticker_Profile_GOOGL.png` | Equity Ticker Profile (GOOGL) |
| 06 | `06_Price_Target_and_Fair_Value.png` | Price target and fair value |
| 07 | `07_Technical_Signal_Timeline.png` | Technical signal timeline |
| 08 | `08_Guru_Council_Consensus.png` | Guru Council consensus |
| 09 | `09_Bitcoin_Cycle_Framework.png` | Bitcoin cycle framework |
| 10 | `10_Global_Macro_Framework.png` | Global macro framework and backtest |
| 11 | `11_Automated_Research_Report_Email.png` | Automated research report email |
| 12 | `12_Profit_and_Loss_Statement.png` | Hackathon-period P&L statement |

---

## Usage rules

- **At most 4–6 inline in the README.** The rest are linked through
  [`docs/PRODUCT_EVIDENCE_INDEX.md`](../../docs/PRODUCT_EVIDENCE_INDEX.md). Do
  not inline all twelve — it buries the narrative.
- **Screenshots are from the live product** at
  [pantheon-research.com](https://pantheon-research.com), which covers GOOGL and
  a broad universe. The local judge demo ships evidence packs for **MA and NVDA
  only**. Do not present a screenshot in a way that implies the local demo
  serves GOOGL.
- **No secrets on screen.** Before committing any screenshot, confirm it shows
  no API key, token, admin surface, internal URL, private endpoint, customer
  data, or account identifier.
- **`12_Profit_and_Loss_Statement.png` must match**
  [`docs/business_model_and_pnl.md`](../../docs/business_model_and_pnl.md) §1:
  revenue $0.00, total expenses $926.12, net loss −$926.12.

---

## Adding the images

Drop the twelve PNGs into this directory using exactly the filenames above.
No other file needs to change — the evidence index already points here.
