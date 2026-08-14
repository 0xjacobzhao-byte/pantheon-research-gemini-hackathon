# Documentation Assets

Canonical presentation assets for the Gemini hackathon submission.

Every diagram here is authored as an **editable SVG** and rendered to PNG. The
SVG is the source of truth; regenerate the PNG rather than editing it.

---

## Canonical assets

| Asset | Used where | Size |
|---|---|---|
| [`pantheon_research_gemini_high_level_architecture.svg`](pantheon_research_gemini_high_level_architecture.svg) `.png` | **README § Architecture** — embedded full-width, immediately after "What Pantheon Research Is" | 1280 × 1010 (PNG @2× = 2560 × 2020) |
| [`pantheon_gemini_deployment_architecture.svg`](pantheon_gemini_deployment_architecture.svg) `.png` | **README § Deployment Architecture** — embedded full-width | 1180 × 830 (PNG @2× = 2360 × 1660) |
| [`pantheon_research_gemini_social_preview.svg`](pantheon_research_gemini_social_preview.svg) `.png` | **GitHub → Settings → Social preview.** Not embedded in the README. | **1280 × 640** (GitHub's required size) |

One further diagram lives outside this directory:

| Asset | Used where |
|---|---|
| [`../../assets/architecture_diagram.svg`](../../assets/architecture_diagram.svg) | [`architecture_diagram.md`](../architecture_diagram.md) — the public **demo** request flow (Gemini primary, Qwen/DeepSeek comparison lanes) |

Product screenshots are governed separately in
[`../../assets/submission/README.md`](../../assets/submission/README.md).

---

## Regenerating a PNG

Diagrams are rendered with headless Chrome so the output matches how a browser
lays out the SVG:

```bash
CHROME="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

# high-level architecture (2x for retina)
"$CHROME" --headless --disable-gpu --hide-scrollbars \
  --force-device-scale-factor=2 --window-size=1280,1010 \
  --screenshot=docs/assets/pantheon_research_gemini_high_level_architecture.png \
  "file://$PWD/docs/assets/pantheon_research_gemini_high_level_architecture.svg"

# deployment architecture (2x)
"$CHROME" --headless --disable-gpu --hide-scrollbars \
  --force-device-scale-factor=2 --window-size=1180,830 \
  --screenshot=docs/assets/pantheon_gemini_deployment_architecture.png \
  "file://$PWD/docs/assets/pantheon_gemini_deployment_architecture.svg"

# social preview — must be exactly 1280x640, so render at 1x
"$CHROME" --headless --disable-gpu --hide-scrollbars \
  --force-device-scale-factor=1 --window-size=1280,640 \
  --screenshot=docs/assets/pantheon_research_gemini_social_preview.png \
  "file://$PWD/docs/assets/pantheon_research_gemini_social_preview.svg"
```

`--window-size` must match the SVG's `viewBox` dimensions, or the render will be
cropped or letterboxed.

---

## Design rules

These keep the diagrams legible and honest:

1. **Explicit white card background.** GitHub renders READMEs in both light and
   dark themes; a transparent background makes dark text vanish in dark mode.
   Every diagram draws its own `#ffffff` card.
2. **Gemini is the visual hero**, marked with `★` and Google blue (`#4285f4`) —
   but the other four providers stay visible. The diagram must never imply that
   Claude, ChatGPT, DeepSeek and Qwen do not exist.
3. **No arrow from a model to an order.** The safety path
   (`AI Research → Human Review → Human Decision`) is drawn explicitly; any
   execution box is dashed, greyed, and labelled as staged.
4. **Non-claims are drawn, not just written.** Red-bordered blocks carry the
   explicit non-claims so a reader scanning only the image still sees them.
5. **Body text ≥ 10.5px at native size.** Anything smaller is unreadable once
   GitHub scales the image down.
6. **No secrets, no host IPs, no internal topology.** No token, database URL,
   admin credential, or deployment IP appears in any diagram.
7. **No obsolete cloud branding.** Alibaba Cloud deployment topology was
   deliberately removed from this repository; only "Qwen (Alibaba DashScope)"
   model-provider attribution is permitted.

---

## Screenshots (optional, not currently committed)

If product screenshots are added to *this* directory rather than
`assets/submission/`, they must follow the same rules: PNG or JPG, ideally
< 500 KB, cropped to product UI only, and showing **no** API key, admin token,
database URL, internal URL, customer data, or account identifier.
