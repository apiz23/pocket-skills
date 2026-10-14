# React / Next.js splash with Framer Motion

Use when the repo has React and the user wants a component. Copy the logo SVG elements into JSX in construction order, converting attributes to camelCase (`stroke-width` -> `strokeWidth`). Keep every `d`, `x`, `y` value from the SVG unchanged.

```tsx
"use client";
import { motion, useReducedMotion } from "framer-motion";

const EASE = [0.65, 0, 0.35, 1] as const;

// stroke draw-on: works on path, rect, circle, line
const draw = (t: number, d = 0.6, reduced = false) => ({
  initial: { pathLength: reduced ? 1 : 0 },
  animate: { pathLength: 1 },
  transition: { delay: reduced ? 0 : t, duration: reduced ? 0 : d, ease: EASE },
});

// hard snap for fills and status marks
const pop = (t: number, reduced = false) => ({
  initial: { opacity: reduced ? 1 : 0 },
  animate: { opacity: 1 },
  transition: { delay: reduced ? 0 : t, duration: 0 },
});

export default function LogoSplash({ onDone }: { onDone?: () => void }) {
  const reduced = !!useReducedMotion();
  return (
    <div className="grid min-h-dvh place-items-center bg-[#FBF9EF]">
      <svg
        viewBox="88 88 504 504"
        role="img"
        aria-label="Brand name"
        className="w-[min(72vmin,420px)]"
      >
        {/* 1. structure */}
        <motion.rect x="100" y="100" width="480" height="480" fill="none" stroke="#2E4FC4" strokeWidth="4" {...draw(0.2, 0.9, reduced)} />
        {/* 2. measurement: repeat with .map(), stagger delay = base + i * 0.02 */}
        {/* 3. signal */}
        <motion.path d="M340 190A150 150 0 0 1 490 340" fill="none" stroke="#2E4FC4" strokeWidth="14" {...draw(2.1, 0.6, reduced)} />
        {/* 4. accent lands last; fire onDone from the final element */}
        <motion.rect
          x="478" y="328" width="24" height="24" fill="#F5C842" stroke="#2E4FC4" strokeWidth="3"
          {...pop(2.7, reduced)}
          onAnimationComplete={onDone}
        />
      </svg>
    </div>
  );
}
```

Notes:
- Circles start drawing at 3 o'clock; add `transform="rotate(-90 cx cy)"` to start at 12.
- A shape with both fill and stroke should be split into two elements: a `pop` fill-only copy and a `draw` stroke-only copy.
- Stagger repeated elements by generating them in a loop with `delay: base + i * 0.02`.
- With Tailwind, set only layout/size/background classes on the wrapper; keep animation in motion props, not utility classes.
- Show once per session: wrap in `useEffect` + `sessionStorage` and unmount on `onDone`.
