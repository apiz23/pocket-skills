# QA notes — logo-splash-animation

## Verdict

**Not verified.** No end-to-end QA run has been recorded for this skill in this repository. It was authored and packaged as a `.skill` bundle and copied here byte-for-byte. Everything below is derived from reading the bundled files, not from executing the skill against a real app or browser.

## Test matrix

| Area | Method | Result | Verified? |
|---|---|---|---|
| Bundled file integrity | sha256 of each file vs the source `.skill` zip | all match | **Verified** |
| Frontmatter | YAML parse; `name` kebab-case and equal to folder | pass | **Verified** |
| `scripts/annotate_svg.py` — imports | source read; stdlib only | no third-party deps | **Verified by inspection** |
| `scripts/annotate_svg.py` — network calls | source read | none (only the SVG XML namespace URI) | **Verified by inspection** |
| Standalone HTML output | not run | — | **Not verified** |
| React / Framer Motion component | not run | — | **Not verified** |
| Timing / choreography (`--total`) | not run | — | **Not verified** |
| `splash:done` event and `replay()` | not run | — | **Not verified** |
| `prefers-reduced-motion` behaviour | not run | — | **Not verified** |
| Keyboard / screen-reader safety (`role`, `aria-label`) | not run | — | **Not verified** |
| Raster-logo refusal path | not run | — | **Not verified** |

## Verified vs not verified

**Verified**

- Every bundled file is byte-identical to the source `.skill` archive (see hashes in the repository commit).
- Frontmatter is valid YAML; `name: logo-splash-animation` is kebab-case and matches the folder name.
- The bundled Python script is stdlib-only and makes no network calls.

**Not verified**

- Any rendered splash screen, in a browser or in a React app.
- The annotate script's handling of real SVGs, including the fill/stroke split and delay ordering.
- The done-hook contract (`splash:done` / `onDone`) and the `sessionStorage` once-per-session pattern.
- Accessibility behaviour, reduced-motion rendering, and the final-frame-equals-static-logo claim.
- Framer Motion integration, since `references/react-framer.md` was never executed.

## Related

The reference palette used in `references/react-framer.md` is documented as a finding in the [brand-logo-from-codebase QA notes](../brand-logo-from-codebase/qa/README.md). It was left untouched to preserve byte-for-byte fidelity.
