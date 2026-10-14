# QA notes — social-preview-cards

This folder records what was actually verified for this skill, and what was not. The matrix below is copied from the skill's own project README; no results have been invented or extrapolated.

## Test matrix

| Framework | App Router | Pages Router | Static | Monorepo | Result | Verified? |
|---|---|---|---|---|---|---|
| Next.js 16.4.0 | yes | yes | yes (export) | yes (pnpm) | both images at exact sizes | **Verified** |
| Vite + React | — | — | yes | — | both images at exact sizes | **Verified** |
| Astro | — | — | yes | — | both images at exact sizes | **Verified** |
| React Router 7 | — | — | yes | — | both images at exact sizes | **Verified** |
| Plain static | — | — | yes | — | drop-in PNGs | **Verified** |

## Verdict

The skill works as specified on the frameworks above, producing both images at their exact pixel sizes. Behaviour was additionally verified for: Edge-runtime failures (build or runtime), static export, pre-existing OpenGraph metadata, custom fonts, missing design docs, dark/light palettes, headline overflow, non-Latin text (Latin, Arabic, CJK), and missing env vars at build time.

## Verified vs not verified

**Verified**

- Next.js 16.4.0 — App Router, Pages Router, static export (`output: "export"`), and pnpm monorepo.
- Vite + React, Astro, React Router 7, and plain static sites (via the build-script path).
- Both images at exact sizes: 1200x630 and 1080x1920.
- Edge-runtime failure modes (build and runtime).
- Static export and the `cacheComponents` / `dynamic` interaction.
- Pre-existing OpenGraph metadata / precedence behaviour.
- Custom fonts, missing design docs, dark and light palettes.
- Headline overflow, and non-Latin text (Latin, Arabic, CJK).
- Missing env vars at build time.

**Not verified**

- **Edge runtime as a supported path** — it is tested only as a documented failure; there is no supported Edge workflow.
- **Windows** — guidance is written but no Windows run was performed. The Windows one-liner in the skill is untested.
- **Linux** — see the note below; treated as partially tested, not fully verified.
- **Docker / CI environments** — no `node_modules` and restricted-filesystem scenarios were not exercised.
- **Next.js versions other than 16** — older versions may differ in the `cacheComponents` / `dynamic` interaction.
- **Frameworks not in the matrix** — Remix (v1/v2) and other setups were not run. Remix v2 is noted as React Router v7 in the skill.

**Note on Linux:** the source README states that macOS **and** Linux-style shell commands were executed. Only macOS is confirmed in the QA run recorded here, so Linux is marked partially tested rather than verified. Verify on your own platform before relying on it.
