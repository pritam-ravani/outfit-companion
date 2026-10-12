# Moodboards

A moodboard is a single, self-contained HTML file that captures a style visually. Build
it from the user's profile and description — never make the user assemble it themselves.

## Required sections (in this order)

1. **Title & theme** — e.g. "Everyday", "Formal", "Streetwear", plus a one-line vibe summary.
2. **Color palette** — 5–8 swatches from their color season (or the colors they named),
   each shown as a labeled color block with its hex value.
3. **Style keywords** — 4–8 words set as typography (minimalist, tailored, oversized…).
4. **Silhouettes & shapes** — the cuts that flatter their body shape, in words or simple
   shapes (e.g. "high-waisted wide-leg", "structured blazer", "A-line").
5. **Fabrics & textures** — key materials and feel (cotton, linen, denim, silk, knit).
6. **Reference images** — any images from `data/inspiration/` that match, as thumbnails,
   referenced with relative `../inspiration/...` paths so they load from disk.
7. **Avoid** — a short strip of what to steer clear of (their no-go list).

## Rules

- **Self-contained:** all CSS inline in the `<head>`, no external CDN or network needed,
  so the file opens offline and stays private.
- **Works at phone width:** single column that stacks, palette swatches wrap, no
  horizontal scrolling.
- **Palette swatches** should be large, clearly labeled, and legible in both light and
  dark mode (define colors as `:root` tokens and add a dark-mode block).
- **Keep it graspable:** roughly one screen's worth per theme. If it needs scrolling to
  *understand*, it's too long — split into another theme file instead.

## Maintenance

- One file per theme (`everyday.html`, `formal.html`, `streetwear.html`).
- When the user's taste evolves, **update** the existing file rather than replacing it —
  merge new signals so the moodboard and `data/profile.md` stay in sync.
- When image generation is added later, insert generated sample images into the
  "Reference images" section.
