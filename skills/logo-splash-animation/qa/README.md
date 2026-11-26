# QA notes — logo-splash-animation

## Verdict

**Tested end-to-end once, on one real codebase (2026-11-26), then re-tested after fixes.** Both output paths were executed against `hafizu-portfolio` at commit `9e035cd` (Next.js 16.1.6, React 19.2.4, framer-motion 12.42.2, pnpm): the standalone HTML from `scripts/annotate_svg.py` and a Framer Motion component built from `references/react-framer.md`. The run was done in a throwaway copy of the repo; the source repo was left clean (`git status` empty, file hashes unchanged).

The first pass found four defects: `--total` was ignored for small logos, `replay()` was documented but missing, replay was pointer-only, and an SVG without `viewBox` crashed the script. All four are fixed and re-verified below. The raster-logo refusal path remains an instruction, not code, so it was not executable here.

Environment: macOS 15.8.3, Node 24.22.2, Python 3.15.2, Chromium 158 (Playwright).

## Test matrix

| Area | Method | Result | Verified? |
|---|---|---|---|
| Find logo + stack | `public/brand/hf-mark.svg`, `pnpm-lock.yaml`, Next/React/framer-motion in `package.json` | correct logo and stack identified | **Verified** |
| `annotate_svg.py` — stroke-only logo | 9-shape test mark, `--total 3.2 --scan` | 9 `draw` shapes, 0 `pop`, valid HTML | **Verified** |
| `annotate_svg.py` — real logo | `public/brand/hf-mark.svg` | 11 shapes annotated, `~4.3s` with scan | **Verified** |
| Fill/stroke split | Fixture with `<rect>` and `<circle>` carrying both | each split into fill `pop` + stroke `draw`; circle got `rotate(-90 cx cy)` | **Verified** |
| `--total` contract | `--total 3.2` on a 9-shape mark | delays `0 … 1.92 s`, duration `1.28 s`, last lands at `3.2 s`; `DONE_MS = 3400` without scan, `4500` with scan | **Fixed + verified** |
| HTML render | Chromium, screenshots through the timeline | draws in document order, no console or page errors | **Verified** |
| `splash:done` | Listener injected before load | fired at 3434 ms (no scan, target 3400) | **Verified** |
| `replay()` hook | `typeof window.replay`, then call it | `function`; restarts the draw and reschedules `splash:done` | **Fixed + verified** |
| Click replay | Click `#splash` after completion | restarts from blank frame; second done ~3.4 s later | **Verified** |
| Keyboard replay | Focus the control, press Enter and Space | both activate replay; focus-visible outline present | **Fixed + verified** |
| Final frame == static logo | Pixel diff against the static SVG at the same 368.64 px box | 11 of 262,144 px differ (0.004%) | **Verified** |
| `prefers-reduced-motion` | Browser context `reducedMotion: "reduce"` | full logo at 80 ms; computed `animation-delay: 0s`, `duration: 0.001s` | **Verified** |
| Accessibility | DOM + Chromium accessibility snapshot | control is a native `<button>` labelled `Replay <name> animation`; status message and title present | **Fixed + verified** |
| React / Framer component | Adapted reference into a real component + route, `tsc --noEmit`, Next dev render | typechecks, runs, `onDone` fires, reduced-motion renders finished logo | **Verified** |
| SVG without `viewBox` | fixture | clear `SystemExit` message; numeric `width`/`height` fallback synthesises a viewBox | **Fixed + verified** |
| Raster-logo refusal | instruction only (no code path) | SKILL says refuse; not executable | **Not run** |
| Other browsers | not run | — | **Not verified** |

## Findings

1. **`--scan` makes the splash longer than `--total`.** The timeline now honours `--total`, then the scanline starts at `total + 0.1` and runs for 1 s, so `splash:done` lands about 1.3 s after the last shape (3.2 s total → 4.5 s done). That exceeds the SKILL's "Total 2.5–4s" rule if the bound is meant to cover the whole splash rather than the mark. Either overlap the scan or document the extra time.
2. **Single-shape logos inherit the whole duration.** With one shape, `--total 3.2` produces a 3.2 s draw. Honest to the contract, but slow for a simple blob; cap or document for the fill-only case.
3. **Fill-only logos still just fade.** The split logic marks them `pop`, as documented; no true draw-on is possible without strokes.
4. **Keyboard replay is now native.** The clickable area is a `<button>`, so Enter and Space work without custom key handling; the wrapper no longer carries `role="img"`, removing the nested-image problem.
5. **Component start is app-level.** In dev, `onDone` arrived at ~2.1 s wall time including ~0.8 s of hydration, while reduced-motion completed at ~0.9 s. The component timeline itself is correct.

## Related

The reference palette used in `references/react-framer.md` is documented as a finding in the [brand-logo-from-codebase QA notes](../brand-logo-from-codebase/qa/README.md). It was left untouched to preserve byte-for-byte fidelity.
