---
name: logo-splash-animation
description: Build an animated splash screen / loading intro for a project's logo by finding the logo SVG in the codebase and animating it (stroke draw-on, hard snaps, optional scanline) as standalone HTML or as a React / Next.js component with Framer Motion. Use this whenever the user asks for a splash screen, logo animation, logo intro, loading screen, app launch animation or "animate my logo", even if they only say "make the logo move". Logo-only focus; the rest of the app is wired by the user.
---

# Logo splash animation

Animate the logo only. Output is either a drop-in HTML file or a component. The rest of the app stays untouched.

## 1. Find the logo and the stack

```bash
ls public/ src/assets/ assets/ app/ 2>/dev/null | grep -Ei "logo|icon|mark|brand"
grep -E '"(next|react|vite|framer-motion|motion|tailwindcss)"' package.json
ls pnpm-lock.yaml yarn.lock package-lock.json 2>/dev/null
```

- No logo SVG exists? Use the `brand-logo-from-codebase` skill first, or ask the user for the file.
- Logo is raster (png/jpg)? Do not animate it as a splash. Say so and offer to build a vector mark first.
- Use the package manager the repo already uses (pnpm if `pnpm-lock.yaml`). Only add `framer-motion` if the user asked for a component and it is missing.

## 2. Choose the output

| Situation | Output |
|---|---|
| User wants a file / prototype / non-React project | Standalone HTML via `scripts/annotate_svg.py` |
| Next.js / React project | Component, see `references/react-framer.md` |
| Unsure | HTML first, then offer the component |

Standalone HTML:

```bash
python scripts/annotate_svg.py path/to/logo.svg splash.html --total 3.2 --bg "<paper hex>" --title "<Name>" --scan
```

The script gives every shape a delay in document order: strokes draw on (`pathLength=1`), fills snap on, shapes with both are split. **Order of elements in the SVG is the choreography**, so reorder the SVG if the sequence is wrong. If the SVG is a single outlined blob, it will just fade; say that and suggest a stroke-based mark.

## 3. Motion rules

1. Sequence follows how the mark is built: structure/frame -> measurement/ticks -> signal -> accent last. The accent lands last and alone.
2. Total 2.5-4s, played once. Click or a `replay()` hook replays it. Never loop a splash.
3. Match the brand's motion language to its tokens: sharp/technical brands use linear or `cubic-bezier(.65,0,.35,1)` draws and `steps(1)` snaps; soft brands use ease-out and gentle springs. No bounces on a clinical brand.
4. Optional single scanline sweep at the end for instrument-style brands. One effect per splash, not several.
5. No glow, blur, drop shadows, gradients, particles, or color changes beyond the logo's own palette.
6. Respect `prefers-reduced-motion`: render the finished logo immediately.
7. Expose completion: dispatch `splash:done` (HTML) or call `onDone` (component). Never navigate for the user unless asked.
8. Logo must be keyboard/screen-reader safe: `role="img"` and an `aria-label` with the brand name.

## 4. Verify

- Open or reason through the timeline: first element < 0.3s, last element lands by the `--total` target, nothing animates after `splash:done`.
- Confirm no element stays invisible at the end (all `pop` and `draw` end states are visible) and the final frame equals the static logo.
- Check reduced motion CSS is present.

## 5. Integration notes (only if asked)

- Show once per session: `sessionStorage.getItem("splash") ` check in a client component.
- Do not delay first contentful paint behind it; mount the splash as an overlay above the page and unmount on `onDone`.
- Next.js app router: component must be `"use client"`.

Deliver: the file or component, the done-hook location, and one line on timing. No long explanation.
