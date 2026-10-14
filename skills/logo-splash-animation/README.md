# logo-splash-animation

An agent skill that animates a project's **existing** logo into a splash screen or loading intro. It animates the logo only — the rest of the app is left untouched and wired by you.

## What it generates

- A **standalone HTML file** (default for prototypes and non-React projects), via `scripts/annotate_svg.py`.
- Or a **React / Next.js component** written with Framer Motion, using `references/react-framer.md`.

The choreography follows how the mark is built — structure → measurement → signal → accent last. Strokes draw on, fills snap on, and an optional single scanline sweep can close it for instrument-style brands.

## Example prompt

> Animate the logo in this project as a splash screen. Find the SVG in public/, build a 3.2s intro where the frame draws on first, the ticks follow, and the accent lands last, on the brand paper colour. Expose a done hook and respect prefers-reduced-motion.

Shorter forms also trigger it: "make a loading screen", "animate my logo", "logo intro for the app", "add a splash screen". Triggers even if you only say "make the logo move".

## Tested versions

**Partially tested.** This skill was authored and packaged as a `.skill` bundle but has not had a recorded end-to-end QA run in this repo. Treat the output as a strong first draft to review, not a verified result.

- Bundled tooling: `scripts/annotate_svg.py` (pure-Python; stdlib only — `argparse`, `copy`, `pathlib`, `re`, `xml.etree.ElementTree`). No network calls; the only `http` string is the SVG XML namespace.
- Framework-specific guidance for React / Next.js and Framer Motion lives in `references/react-framer.md` and was not executed against a live app.

## Known limits

- **Raster logos cannot be animated this way.** If the logo is a PNG/JPG, the skill says so and offers to build a vector mark first (see `brand-logo-from-codebase`) rather than faking it.
- **A single outlined blob will just fade.** If the SVG has no separable strokes, the draw-on effect has nothing to work with; the skill tells you and suggests a stroke-based mark.
- **Element order in the SVG *is* the choreography.** If the sequence is wrong, you reorder the SVG, not the script.
- **Framer Motion is not bundled**, and the skill only adds it if you ask for a component.
- **Next.js App Router components must be `"use client"`** — the skill notes this but the integration is yours to place.
- **Reduced-motion and done-hook behaviour are specified, not verified here** — confirm them in your own browser before shipping.

## Requirements

- Python 3 for `scripts/annotate_svg.py`.
- An **SVG** logo in the project (`public/`, `src/assets/`, `assets/`), or the willingness to generate one first.
- For the component path: React / Next.js, plus `framer-motion` (added only on request).

## License

MIT — see the [repository LICENSE](../../LICENSE).
