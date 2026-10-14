---
name: social-preview-cards
description: Build social share preview images for any web project — a 1200x630 OpenGraph link-preview card and a 1080x1920 story card. Inspects the codebase for the framework, palette, fonts, logo and avatar, then generates on-brand images (next/og Satori for Next.js, or a build script otherwise) and wires up the metadata. Use whenever the user asks for an OG image, social/link preview, share card, Twitter card, LinkedIn/WhatsApp/Slack link preview, or story/reel image, even if they don't say "OpenGraph".
---

# Social Preview Metadata Cards

Add social share preview images to an existing web project. Inspect the codebase, learn its identity, generate on-brand preview cards. Do not hardcode anything from this skill. Derive everything from the repo in front of you.

Tested against Next.js 16 (App Router, Pages Router, static export, pnpm monorepo), Vite, Astro and React Router 7. Older Next versions may behave differently; verify with the build.

## Step 1 — Inspect the codebase (do this first, don't guess)

Detect framework and conventions before writing code. Check:

- **Framework:** `package.json`. Next.js, Vite, Astro, React Router/Remix, or pure static? The approach differs (Step 3).
- **Next.js router and config:** App Router (`app/`) or Pages (`pages/`)? Check `next.config.*` for `output: "export"`, `cacheComponents`, and any `runtime = "edge"` in layouts/routes.
- **Brand tokens:** read `tailwind.config.*` if it exists, plus `app/globals.css` or `src/**/*.css`, and any theme/tokens files. Tailwind v4 usually has no config file; the palette lives in an `@theme { ... }` block in the global CSS. Extract the real palette, fonts, border radius, spacing.
- **Existing logo/icons:** look in `public/`, `src/assets/`, `assets/`, `app/icon.*`, `app/favicon.*`. Reuse an existing logo SVG.
- **Profile image:** find a headshot/avatar if one exists (any image under `public/`, `src/assets/`, `assets/`). SVG and raster files both work; inline either as a base64 data URI. If none exists, skip the photo. Do not ask.
- **Design docs:** `README.md`, `PRODUCT.md`, `DESIGN.md`, `CLAUDE.md`, `AGENTS.md`, and any other repo-level design or tone doc. These often state tone, anti-references, and what to never imply. If none exist, proceed from the tokens alone.
- **Existing metadata:** current `openGraph` / `twitter` config in the layout. Note it. Step 6 says how to avoid breaking it.

Only after this, state a one-line brief:

> "This is a `<framework>` project with `<palette: hex>` on `<paper: hex>`, display font `<X>`, radius `<Y>`, tone `<Z>`. I'll build the preview cards to match."

Then proceed.

## Step 2 — Decide the deliverables

Produce **both** images unless the user asks for only one:

1. **Link-preview card** — landscape, default 1200×630. What LinkedIn / X / Facebook / WhatsApp / Slack render when the URL is pasted. The one that matters most.
2. **Portrait story card** — 9:16, default 1080×1920. For Instagram/Facebook Stories, Reels, TikTok. Also add a small preview page so the user can open/save both.

Always tell the user the tradeoff: portrait 1080×1920 is a story format. Social platforms crop link previews to landscape, so the portrait image is **not** used as the link preview. Do not stop to ask which size they want. Build both and explain the difference in the report.

## Step 3 — Choose the generation method (adapt to the framework)

### Next.js App Router (recommended path)

Use `next/og`'s `ImageResponse` (Satori). Create `app/opengraph-image.tsx` and `app/story/opengraph-image.tsx`. Next.js auto-injects the `og:image` tag. Do not hardcode a `.png` path.

**Node runtime only.** `readFileSync` and every local-image example here need the Node.js runtime. Never set `export const runtime = "edge"` on an image route. It fails the build ("not supported in the Edge Runtime", "Failed to collect page data"). If the project forces Edge elsewhere, fetch the image over HTTP or inline it as a literal string instead of reading from disk.

**Static export (`output: "export"`).** Add `export const dynamic = "force-static"` to every `opengraph-image` route. If the build then errors with `Route segment config 'dynamic' is not compatible with nextConfig.cacheComponents`, remove `cacheComponents: true` from `next.config`. Exported PNGs may be served with an empty Content-Type; this is expected.

### Next.js Pages Router

No file convention exists. Create `pages/api/og.tsx`:

- `export const config = { runtime: "nodejs" }`. Edge returns HTTP 500 on `node:fs`.
- Default handler returns `new ImageResponse(<jsx/>, { width: 1200, height: 630 })`. Read it with `Buffer.from(await img.arrayBuffer())` and reply via `res.status(200).send(buf)`.
- Pages Router has no `metadata` export. Add the `og:image` and `twitter:card` tags in `pages/_document.tsx` `<Head>` (or per-page `next/head`), using an absolute URL.

### Vite, Astro, React Router (Remix v2 is now React Router v7), other

Generate PNGs with a build script (`satori` + `sharp`, `@vercel/og`, or `resvg`) and emit them into the public dir. Requirements:

- **JSX:** plain `node script.mjs` cannot parse JSX (`SyntaxError: Unexpected token '<'`). Either author the script with `React.createElement`, or run it through a JSX-capable runner such as `tsx`.
- **Dependencies:** `satori` needs `react` installed (and `react-dom` if a renderer asks for it), plus `sharp` or `resvg` for PNG output.
- **Fonts:** standalone `satori` requires at least one real font buffer (see Step 4).
- **Build order:** the script must run **before** the framework build, or the images are missing from `dist/` / `build/` and 404. Wire it as a `prebuild` npm script.
- Add `og:image` and `twitter:card` tags by hand in the HTML head or layout, with absolute URLs.

### Pure static site, or if unsure

Generate static PNG/SVG files the user can drop in, and hand-write the meta tags.

Whatever the method, images must come out at the exact pixel sizes required.

## Step 4 — If using Satori / next/og, respect its constraints

Non-negotiable. The #1 causes of build failures:

- **Flexbox only.** No CSS grid. No CSS files. Everything inline via `style={{}}`. No Tailwind classes.
- **Any element with more than one child needs `display: "flex"` explicitly.**
- **Local images can't be referenced by path.** `ImageResponse` cannot read `/public`. Read the file and inline it as a base64 data URI (use the matching MIME type, e.g. `image/svg+xml`, `image/png`, `image/jpeg`):

  ```ts
  import { readFileSync } from "node:fs";
  import { join } from "node:path";

  const buf = readFileSync(join(process.cwd(), "public/<your-image-file>"));
  const src = `data:image/jpeg;base64,${buf.toString("base64")}`;
  ```

  Render with a plain `<img>` (not `next/image`), passing `width`/`height` attributes and `style={{ objectFit: "cover", objectPosition: "top" }}`. Add `// eslint-disable-next-line @next/next/no-img-element`. In a monorepo, confirm `process.cwd()` resolves to the app directory.
- **Fonts.**
  - Inside `next/og`, a system stack like `"Georgia, serif"` works because Next ships a default font.
  - Standalone `satori` has no default. It throws `No fonts are loaded` unless you pass at least one real font buffer via `fonts`.
  - The `next/og` default font covers Latin only. Arabic and other complex scripts can fail the build (`lookupType: 5 - substFormat: 3 is not yet supported`). Korean and parts of CJK render as missing glyphs. For any non-Latin text, pass an explicit font file that covers the script via the `fonts` option.
  - Don't assume a webfont is available.
- **Logo as vector:** inline the SVG as a React component with explicit camelCase props (`strokeWidth`, `strokeLinejoin`, `strokeLinecap`). Satori won't fetch an external SVG file. An SVG data URI in `<img>` also works.

## Step 5 — Compose on-brand

Use the real tokens from Step 1.

- **Landscape (1200×630):** two columns. Left = identity (logo/wordmark, big short headline, hairline rule, footer with a skills line and a small status pill). Right = portrait photo in a ringed frame with a tiny caption. Optional faint vertical column rulers as a background layer. No photo available: let the left column span the card.
- **Portrait (1080×1920):** single centered column, `justifyContent: "space-between"`. Top = logo + name. Middle = large portrait + headline (~100px+). Bottom = rule + skills + accent status pill.
- Match the project's shape language: sharp corners → `borderRadius: 0`; soft → round to match. Match its border style (hairline, ring, shadow) and any accent-usage rule stated in its design docs.
- Respect the project's anti-references. No gradients, shadows or glass if the brand is flat and severe.
- **Text overflow.** Satori does not wrap or ellipsize a long unbroken word. It clips at the card edge with no warning. Set `wordBreak: "break-word"` / `overflowWrap: "anywhere"`, cap the headline length, and check the text doesn't reach the right edge.
- **Contrast.** Satori renders unreadable text without warning. Compute contrast between text and background hexes (aim for at least 4.5:1) before rendering. If the brand palette is dark, use light text, and vice versa, even if the site itself pairs them differently.

## Step 6 — Wire up metadata correctly

- Never point `openGraph.images` at a file that doesn't exist. With a dynamic image route, let the framework auto-inject it, or reference the route URL.
- **Precedence.** In Next.js App Router, a file-convention route (`app/opengraph-image.tsx`) silently overrides any `images` already set in `metadata.openGraph`; the existing image stops being emitted. Choose one: keep the project's manual image and point the new card at the route URL explicitly, or remove the manual entry. Tell the user which you did.
- Add a Twitter card: `twitter: { card: "summary_large_image", title, description }`.
- Keep `metadataBase` set (absolute URLs) so crawlers resolve the image.

## Step 7 — Verify (do all of these, report the results)

1. **Build passes.** Run the project's build (`pnpm build` / `npm run build` per the lockfile). Image routes should appear in the output. Image routes are evaluated at build time: if the project reads required env vars at module scope (e.g. a DB client that throws when a key is missing), the build fails. Set the env vars, or mention it in the report.
2. **Both images return the right type and dimensions.** Next.js example:

   ```bash
   curl -s -o /tmp/og.png -w "%{http_code} %{content_type} %{size_download}b\n" http://localhost:3000/opengraph-image
   file /tmp/og.png
   # Any platform, no dependencies (reads the PNG header):
   node -e "const b=require('fs').readFileSync('/tmp/og.png');console.log(b.readUInt32BE(16)+'x'+b.readUInt32BE(20))"
   ```

   Confirm exactly 1200×630 and 1080×1920. On Windows, use the same Node one-liner with a Windows path.
3. **Image isn't blank or failed.** A failed Satori render is usually tiny; a correct one is sizeable. If a photo is included, confirm it rendered. Missing avatar is the most common failure. Causes: `next/image` instead of `<img>`, a path instead of a data URI, or the file read failed.
4. **Meta tags are present in the HTML:**

   ```bash
   curl -s http://localhost:3000/ | grep -oE 'og:image[^>]*>|twitter:card[^>]*>'
   ```

   Expect `og:image` with width 1200 and the twitter card. For static builds, grep the built HTML in `dist/` or `out/`.
5. **Text check.** Confirm the headline doesn't clip and contrast is readable.
6. **Preview page** (if made) loads.

## Step 8 — Report back

Deliver: files created, tokens read from the codebase and used, verification results. Then tell the user:

- Which image is for link previews vs stories.
- LinkedIn caches aggressively. Use its Post Inspector to re-scrape after deploy.
- Env vars needed at build time must also be set in the hosting platform, or the deploy can fail.

Keep the explanation short.
