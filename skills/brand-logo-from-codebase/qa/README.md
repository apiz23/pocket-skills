# QA notes — brand-logo-from-codebase

## Verdict

**Not verified.** No end-to-end QA run has been recorded for this skill in this repository. It was authored and packaged as a `.skill` bundle and copied here byte-for-byte. Everything below is derived from reading the bundled files, not from executing the skill against a real codebase.

## Test matrix

| Area | Method | Result | Verified? |
|---|---|---|---|
| Bundled file integrity | sha256 of each file vs the source `.skill` zip | all match | **Verified** |
| Frontmatter | YAML parse; `name` kebab-case and equal to folder | pass | **Verified** |
| `scripts/logo_tools.py` — imports | source read; stdlib only (`re`, `argparse`, `pathlib`) | no third-party deps | **Verified by inspection** |
| `scripts/logo_tools.py` — network calls | source read | none | **Verified by inspection** |
| GENERATE mode on a real repo | not run | — | **Not verified** |
| `lint` subcommand | not run | — | **Not verified** |
| `colorways` subcommand | not run | — | **Not verified** |
| 16 / 32 / 64px readability | not run (`rsvg-convert` / `cairosvg` not bundled) | reasoned from stroke widths only | **Not verified** |
| PROMPT mode output quality | not run | — | **Not verified** |
| Next.js / Vite wiring offer | not run | — | **Not verified** |

## Verified vs not verified

**Verified**

- Every bundled file is byte-identical to the source `.skill` archive (see hashes in the repository commit).
- Frontmatter is valid YAML; `name: brand-logo-from-codebase` is kebab-case and matches the folder name.
- The bundled Python script is stdlib-only and makes no network calls.

**Not verified**

- Any actual generation of a logo SVG, on any codebase.
- The linter and colorway exporter, including their `--palette` / `--src` / `--to` argument handling.
- Small-size readability, since no rasteriser is bundled.
- PROMPT-mode output against a real image model.

## Note on the bundled palette

`assets/reference-field-instrument.svg`, `scripts/logo_tools.py`, and `references/react-framer.md` in `logo-splash-animation` all reference the same example palette (`#2E4FC4`, `#FBF9EF`, `#F5C842`, `#D3D8E8`). These files were copied **byte-for-byte at the user's instruction**, so the palette was deliberately left untouched. It is reported here as a finding: if this repo is meant to carry no brand-specific colours, these bundled files are where they live. The `SKILL.md` bodies themselves contain no hex values.
