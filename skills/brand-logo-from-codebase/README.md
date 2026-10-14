# brand-logo-from-codebase

An agent skill that designs a logo mark for a project by reading what the project already says about itself — name, purpose, palette, radius, tone — rather than inventing a brand from nothing.

## What it generates

- A text-free **1:1 vector mark** (SVG), geometric-only, with no gradients, shadows or filters.
- Four colorways: **ink on paper, brand on paper, reversed on brand, and single flat colour**.
- A linter pass (`scripts/logo_tools.py lint`) that checks the mark against your palette and brand rules.
- In **PROMPT mode**, one self-contained design prompt you can paste into an image model or another agent.

Two modes: **GENERATE** (default — builds the SVG) and **PROMPT** (user asks for a prompt, or another model will do the work). If your codebase has a "Field Instrument" / scientific-survey style, the skill ships `assets/reference-field-instrument.svg` as a starting method, not a picture to ship unchanged.

## Example prompt

> Design a logo mark for this project. Read the README, package.json and theme tokens for the name, purpose, palette, radius and tone, then generate a flat 1:1 geometric SVG with no text, plus ink-on-paper, brand-on-paper, reversed and single-colour versions. Lint it against the palette and check it reads at 32px.

Shorter forms also trigger it: "make a favicon for this repo", "we need an app icon", "design a brand mark", "give me a logo prompt". The skill triggers even if you never say "SVG".

## Tested versions

**Partially tested.** This skill was authored and packaged as a `.skill` bundle but has not had a recorded end-to-end QA run in this repo. Treat the output as a strong first draft to review, not a verified result.

- Bundled tooling: `scripts/logo_tools.py` (pure-Python; uses `re`, `argparse`, `pathlib` — no network calls).
- Optional external checks named in the skill: `rsvg-convert` or `cairosvg` for rasterising to 16/32/64px. Neither is bundled; the skill says to reason from stroke widths if they are absent.

## Known limits

- **Non-Latin and wordmark text are out of scope.** The mark is deliberately text-free; a wordmark only matters if you explicitly ask for one, and it inherits the font problems of whatever renders it.
- **Image-model PNGs are not covered.** The skill produces SVG. If you use PROMPT mode with a raster image model, you get a bitmap back, not editable vectors.
- **The linter is a rules check, not a designer.** It catches palette and geometry violations; it cannot tell you the concept is weak.
- **Readability at 32px is reasoned, not measured, when `rsvg-convert`/`cairosvg` are missing** — which is the default in this repo, since neither is bundled.
- **Only the frameworks it inspects are covered.** It reads Tailwind config, CSS variables, `package.json` and design docs; a codebase with none of those needs you to state the palette.

## Requirements

- Python 3 for `scripts/logo_tools.py`.
- A codebase it can read (README, `package.json`, theme tokens, CSS) — or be ready to answer two questions about name and purpose.

## License

MIT — see the [repository LICENSE](../../LICENSE).
