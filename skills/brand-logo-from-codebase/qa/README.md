# QA notes — brand-logo-from-codebase

## Verdict

**Tested end-to-end once, on one real codebase (2026-11-26).** GENERATE mode, `lint`, `colorways`, the Next.js wiring path and 16/32/64px rendering were executed against `hafizu-portfolio` at commit `9e035cd` (Next.js 16.1.6, React 19.2.4, Tailwind 3.4, `--radius: 0px`). The run was done in a throwaway copy of the repo; the source repo was left clean (`git status` empty, file hashes unchanged).

PROMPT-mode output quality is still unverified: the image-generation call failed because the provider API key had expired, which is an environment failure, not a skill failure.

Environment: macOS 15.8.3, Node 24.22.2, Python 3.15.2, Chromium 158 (Playwright), `rsvg-convert`/`cairosvg` absent — raster checks used Chromium screenshots.

## Test matrix

| Area | Method | Result | Verified? |
|---|---|---|---|
| Discovery | Read `PRODUCT.md`, `.impeccable.md`, `app/globals.css`, `tailwind.config.ts`, `public/brand/`, `app/icon.svg` | name, purpose, palette (`#2F1664` ink, `#EACB49` accent, `#F9F4F2` paper, `#D7CDEA` hairline), radius `0`, fonts all extracted correctly | **Verified** |
| GENERATE mode | Built a new HF ligature mark on a 24-unit grid from the discovered tokens | produced a text-free, flat, palette-only SVG | **Verified** |
| `lint` — pass case | `logo_tools.py lint` with the repo palette | `PASS`, exit 0 | **Verified** |
| `lint` — fail cases | Fixture with `<text>`, `<image>`, gradient, `rx`, round caps, off-palette stroke, blurred style | caught all 7 problems, exit 1 | **Verified** |
| `lint --allow-radius` | Same rounded-rect fixture | rounded-corner error suppressed, other errors kept | **Verified** |
| `colorways` | Four outputs with explicit `--src` / `--to` | 4 files written; background rect inserted in the three paper/brand variants and absent from `flat` | **Verified** |
| `colorways` — `currentColor` source | Mark using `stroke="currentColor"` | correctly swapped only when `--src fg=currentColor` is passed | **Verified with caveat** |
| 16 / 32 / 64 px | Chromium screenshots at true pixel sizes, nearest-neighbour inspection | clean at 32 and 64; at 16 the 2-unit corner ticks disappear and the mark softens but stays recognisable | **Verified** |
| Next.js wiring offer | Wrote `public/logo.svg`, `app/icon.svg`, and a `Logo` component in the copy | `tsc --noEmit` passes | **Verified** |
| PROMPT mode — structure | Filled the template against the real brief | every required field present | **Verified by inspection** |
| PROMPT mode — image output | `generate_image` | blocked: expired API key | **Not verified** |
| Other stacks / design judgment | not run | — | **Not verified** |

## Findings

1. **`flat` colorway leaves a hole where the accent was.** Accent and hairline are recoloured to the background colour rather than removed, so on the transparent `flat` output the accent segment becomes a transparent gap. In the test mark that is a 4-unit notch in the mid-arm. This matches the documented "accent removed" intent, but the gap is visible if the mark is placed on a coloured surface.
2. **`ink == brand` produces duplicates.** For single-colour brands (as here, ink is the brand violet) `ink-on-paper.svg` and `brand-on-paper.svg` are byte-identical. Harmless, but callers should not expect four distinct files.
3. **Default `--src` does not understand `currentColor`.** A mark that uses `stroke="currentColor"` is emitted unchanged in all four colorways unless `--src fg=currentColor` is passed explicitly. `lint` accepts `currentColor`, so this is easy to miss. The SKILL snippet does pass `--src`, but the default is a trap.
4. **At 16px the hairline detail is not usable.** The 2-unit corner ticks blur into faint lavender smudges and the whole mark softens; it still reads as HF, but the SKILL's "must work at 16–32px" is only true at the upper end — treat 32px as the real floor for hairline frames.
5. **Design quality is subjective and was not reviewed.** This run proves the pipeline, not that the generated concept is good.

## Note on the bundled palette

`assets/reference-field-instrument.svg`, the defaults inside `scripts/logo_tools.py`, and `references/react-framer.md` in `logo-splash-animation` still carry the example palette (`#2E4FC4`, `#FBF9EF`, `#F5C842`, `#D3D8E8`). This QA run passed `--palette`, `--src` and `--to` explicitly, so no example colour reached the test output. If this repo is meant to carry no brand-specific colours, these bundled defaults are where they live.
