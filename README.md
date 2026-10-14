# pocketskills

A small collection of portable agent skills — drop-in `SKILL.md` folders you can install into Claude Code, claude.ai, or any agent that reads YAML frontmatter.

Each skill is self-contained: its own folder, its own frontmatter, its own README. They are designed to inspect the project in front of them and derive their output from it, rather than hardcoding values from the skill itself.

## Skills

| Skill | Description | Status |
|---|---|---|
| [social-preview-cards](skills/social-preview-cards/) | Builds on-brand social share preview images for a web project — a 1200x630 OpenGraph link-preview card and a 1080x1920 story card — by inspecting the codebase for its framework, palette, fonts, logo and avatar, then wiring up the metadata. | tested on Next.js 16.4.0 (partially tested elsewhere — see the skill README) |
| [brand-logo-from-codebase](skills/brand-logo-from-codebase/) | Designs a logo mark, app icon, favicon or brand symbol for a project by reading its codebase for the name, purpose, palette, radius and tone, then either generating the SVG and its colorways or writing a ready-to-paste design prompt. | partially tested |
| [logo-splash-animation](skills/logo-splash-animation/) | Builds an animated splash screen or loading intro for a project's logo — stroke draw-on, hard snaps, optional scanline — as standalone HTML or a React / Next.js component with Framer Motion. | partially tested |

## Install

### Claude Code

Copy the skill folder (use the folder name):

```bash
mkdir -p ~/.claude/skills
cp -R skills/social-preview-cards ~/.claude/skills/
cp -R skills/brand-logo-from-codebase ~/.claude/skills/
cp -R skills/logo-splash-animation ~/.claude/skills/
```

Then start (or restart) Claude Code and ask for the task in plain language — the `name` and `description` fields in the frontmatter drive discovery.

### claude.ai

Zip the skill folder so the archive is named `<name>.skill`, then upload it:

```bash
cd skills
zip -r social-preview-cards.skill social-preview-cards
zip -r brand-logo-from-codebase.skill brand-logo-from-codebase
zip -r logo-splash-animation.skill logo-splash-animation
```

Upload each `<name>.skill` in claude.ai under Settings → Capabilities → Skills. The zips must keep the bundle contents (`SKILL.md`, `scripts/`, `assets/`, `references/`) at the archive root, as above.

### Other agents

Any agent that loads `SKILL.md` files with YAML frontmatter works. Copy the skill folder into that agent's skills directory — for example, Hermes Agent uses `~/.hermes/skills/`.

## Skill documentation

Each skill folder has its own documentation:

- [social-preview-cards README](skills/social-preview-cards/README.md) · [QA notes](skills/social-preview-cards/qa/README.md)
- [brand-logo-from-codebase SKILL.md](skills/brand-logo-from-codebase/SKILL.md)
- [logo-splash-animation SKILL.md](skills/logo-splash-animation/SKILL.md)

## License

MIT — see [LICENSE](LICENSE).
