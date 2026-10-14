---
name: brand-logo-from-codebase
description: Design a logo mark, app icon, favicon or brand symbol for a project by reading its codebase (README, package.json, theme tokens, Tailwind config, design docs) and then either generating the SVG or writing a ready-to-paste design prompt. Use this whenever the user asks for a logo, brand mark, icon, wordmark, favicon, app icon, "brand identity", or "design a logo for this repo/app/project", even if they never say "SVG" or "skill". Produces a text-free 1:1 vector mark plus ink, brand, reversed and single-color versions, and checks them with a linter.
---

# Brand logo from codebase

Turn what a project already says about itself (name, purpose, colors, radius, fonts, tone) into a precise, flat vector logo. Two modes:

- **GENERATE** (default): build the SVG and colorways, lint them, show them.
- **PROMPT**: user says "give me a prompt", or an image model / another agent will do the work. Output one self-contained prompt (template at the bottom). Never paste the codebase; paste the distilled brief.

If unsure, GENERATE, then offer the prompt.

## 1. Discover (read, don't guess)

Run only what exists. Prefer 5-8 reads over a full crawl.

```bash
cat README* package.json 2>/dev/null | head -80
ls DESIGN* docs/ design/ .claude/ CLAUDE.md AGENTS.md 2>/dev/null
grep -rEn "primary|accent|--color|radius|font-family|fontFamily" tailwind.config.* app/globals.css src/**/*.css 2>/dev/null | head -40
ls public/ src/assets/ assets/ 2>/dev/null   # existing favicon/logo to respect or replace
```

Extract into this brief (state assumptions in one line if a field is missing; ask at most 2 questions, only if the name or purpose is unknown):

| Field | Source |
|---|---|
| Name (exact casing/punctuation) | package.json, README title |
| What it does, in one sentence + the core user loop | README |
| Voice/tone and what must never be implied | README, design docs, copy |
| Palette (hex) and which color is brand vs semantic | tailwind config, CSS variables |
| Corner radius, border style, shadows | tokens (radius 0 = sharp geometry) |
| Typeface (only matters if a wordmark is requested) | CSS/font imports |
| Constraints given by the user | the request |

Semantic colors (success/warning/danger, risk levels) are **reserved**. Never use them in the mark unless the user says so.

## 2. Pick the concept

1. Choose one metaphor from the product's own world (instrument, seal, map, ledger, key, signal, grid, aperture, stamp). One idea, not three.
2. Let the design tokens decide the geometry: radius 0 -> squares, miters, hairlines; large radius -> circles and soft joins; mono/technical type -> grid and measurement motifs; playful tone -> asymmetry and bold fills.
3. Spend boldness in one place: one memorable element, everything else quiet. One small accent detail in the secondary color, max.
4. Safety framing: depict the *guardian/measurer/community*, never the threat. No mascots, no hazard or alarm symbols, no depictions of whatever the product warns about, no real brands.
5. If the codebase has a "Field Instrument" / scientific-survey style (sharp, hairline, mono, grid), start from `assets/reference-field-instrument.svg` (survey plate + gauge reticle) and adapt the *method*, not the picture: do not ship the reference unchanged for a different product.

## 3. Build the SVG

- Square 1:1 `viewBox` with ~5% padding. No `<text>`, no raster, no gradients, shadows, filters, masks.
- Geometric primitives only (`rect`, `circle`, `path`, `line`). Work on a grid (e.g. 24 units) and place everything on it.
- Stroke weights from a short scale (e.g. 3 / 4 / 5 / 14). Thin lines must survive at 32px: if a detail disappears at 32px, remove it from the icon version rather than thickening the whole mark.
- Sharp products: `stroke-linejoin="miter"`, `stroke-linecap="butt"`, no `rx`.
- Repeats (ticks, grid) via loops or `transform="rotate()"`, written out as plain elements.
- Use real hex values from the codebase palette. Give structure, fill, hairline and accent distinct roles (fg, bg, hl, acc).

## 4. Verify and export

```bash
python scripts/logo_tools.py lint logo.svg --palette "#hex1,#hex2,..."     # add --allow-radius for soft brands
python scripts/logo_tools.py colorways logo.svg out/ \
  --src "fg=#..,bg=#..,hl=#..,acc=#.." --to "fg=#..,bg=#..,hl=#..,acc=#..,ink=#.."
```

Colorways emitted: ink on paper, brand on paper, reversed on brand, single flat color (grid and accent removed). Check readability at 16, 32 and 64 px (`rsvg-convert -w 32` or `cairosvg` if installed; otherwise reason from stroke widths). Fix and re-lint until PASS.

If the codebase uses Next.js/Vite, also offer to wire it up: save `public/logo.svg`, favicon (`app/icon.svg` in the Next.js app router), and a `Logo` component. Do this only if asked.

## 5. Deliver

Short: the mark, the four colorways, one paragraph on the concept, hex roles, and what was assumed from the codebase. No long essays.

## PROMPT mode template

```
Design a logo mark (1:1, no text, flat vector look) for "<NAME>".
Product: <one sentence + core loop>.
Voice: <tone>. Must never imply: <list>. Must not depict: <list>.
Style: <geometry derived from tokens: radius, borders, shadows, type feel>.
Concept: <the single metaphor and its 3 parts>.
Palette (hex only, nothing else): <brand>, <accent for one small detail>, <paper>, <ink>, <hairline>. Reserved, do not use: <semantic colors>.
Must work: ink on paper, brand on paper, reversed on brand, single flat color, and at 16-32px.
Do not: <rounded corners / gradients / shadows / mascots / extra hues>.
Deliver: the mark only, centered with even padding, plain background.
```
