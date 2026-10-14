# social-preview-cards

An agent skill that adds on-brand social share preview images to an existing web project — by inspecting the repo, learning its identity, generating the images, and wiring up the metadata.

## What it generates

Two images, both at exact pixel sizes:

- **1200x630 link-preview card** — the landscape image that LinkedIn, X, Facebook, WhatsApp and Slack render when the URL is pasted. This is the one that matters most.
- **1080x1920 story card** — a 9:16 portrait for Instagram/Facebook Stories, Reels and TikTok, plus a small preview page so you can open and save both.

Note the tradeoff: social platforms crop link previews to landscape, so the portrait image is **not** used as the link preview.

The skill derives the palette, fonts, logo and avatar from your repo — it never hardcodes values from the skill itself. It supports Next.js (App Router, Pages Router, static export, monorepos) via `next/og`'s `ImageResponse`, and uses a `satori` + `sharp` build script for Vite, Astro, React Router 7 and plain static sites.

## Example prompt

Paste this into your agent, with the project as the working directory:

> Add a social link preview card to this project. Inspect the codebase for the framework, palette, fonts and logo, generate a 1200x630 OpenGraph card and a 1080x1920 story card that match the brand, and wire up the `og:image` and `twitter:card` metadata. Then verify the build passes and both images come out at the exact sizes.

Shorter forms also trigger it: "Add an OG image to this project", "Generate a social link preview card", "Make a share card for this site", "I need a story image for Instagram". The skill triggers even if you don't say "OpenGraph".

## Tested versions

| Framework | App Router | Pages Router | Static | Monorepo | Result |
|---|---|---|---|---|---|
| Next.js 16.4.0 | yes | yes | yes (export) | yes (pnpm) | both images at exact sizes |
| Vite + React | — | — | yes | — | both images at exact sizes |
| Astro | — | — | yes | — | both images at exact sizes |
| React Router 7 | — | — | yes | — | both images at exact sizes |
| Plain static | — | — | yes | — | drop-in PNGs |

Full detail, including what was and wasn't verified, is in [qa/README.md](qa/README.md).

## Known limits

- **Edge runtime is not supported.** Image routes must use the Node.js runtime — `readFileSync` and every local-image example need it. `export const runtime = "edge"` fails the build. If the project forces Edge, fetch the image over HTTP or inline it as a literal string instead of reading from disk.
- **Non-Latin text needs an explicit font.** The `next/og` default font and standalone `satori` cover Latin only. Arabic and other complex scripts can fail the build, and Korean and parts of CJK render as missing glyphs. Pass a font file that covers the script via the `fonts` option.
- **Windows, Linux-shell and Docker paths are not tested.** Only macOS was exercised in the QA run; Windows guidance in the skill is provided but was never executed.
- **Only Next.js 16 was tested.** Older versions may differ in the `cacheComponents` / `dynamic` interaction.

## Requirements

- **Next.js path:** Next.js with `next/og`.
- **Build-script path:** `satori` + `sharp` (or `@vercel/og` / `resvg`), plus `react`, and — for JSX-authored scripts — a runner such as `tsx`.

## License

MIT — see the [repository LICENSE](../../LICENSE).
