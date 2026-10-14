# pocketskills

A small collection of portable agent skills — drop-in `SKILL.md` folders you can install into Claude Code, claude.ai, or any agent that reads YAML frontmatter.

Each skill is self-contained: its own folder, its own frontmatter, its own README. They are designed to inspect the project in front of them and derive their output from it, rather than hardcoding values from the skill itself.

## Skills

| Skill | Description | Status |
|---|---|---|
| [social-preview-cards](skills/social-preview-cards/) | Builds on-brand social share preview images for a web project — a 1200x630 OpenGraph link-preview card and a 1080x1920 story card — by inspecting the codebase for its framework, palette, fonts, logo and avatar, then wiring up the metadata. | tested on Next.js 16.4.0 (partially tested elsewhere — see the skill README) |

## Install

### Claude Code

Copy the skill folder into your Claude Code skills directory:

```bash
mkdir -p ~/.claude/skills
cp -R skills/social-preview-cards ~/.claude/skills/
```

Then start (or restart) Claude Code and ask for the task in plain language — the `name` and `description` fields in the frontmatter drive discovery.

### claude.ai

Zip the skill folder so the archive is named `<name>.skill`, then upload it:

```bash
cd skills
zip -r social-preview-cards.skill social-preview-cards
```

Upload `social-preview-cards.skill` in claude.ai under Settings → Capabilities → Skills.

### Other agents

Any agent that loads `SKILL.md` files with YAML frontmatter works. Copy the skill folder into that agent's skills directory — for example, Hermes Agent uses `~/.hermes/skills/`.

## Skill documentation

Each skill folder has its own README with usage, an example prompt, tested versions and known limits:

- [social-preview-cards/skills README](skills/social-preview-cards/README.md)
- [social-preview-cards QA notes](skills/social-preview-cards/qa/README.md)

## License

MIT — see [LICENSE](LICENSE).
