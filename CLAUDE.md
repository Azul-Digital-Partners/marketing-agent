# Marketing Workspace

## First-Run Check

On every session start, check whether this workspace has been configured:

```
Read context/brand-voice.md — look for the string "<!-- TEMPLATE:"
```

If found: this workspace has not been set up yet. Before doing anything else, tell the user:

> **Welcome.** This marketing workspace isn't configured yet.
> Run `/setup` to get started — it's a 10–15 minute interview that configures your brand voice, content pillars, and LinkedIn calendar. No file editing required.
>
> Or if you just want to explore, try `/write [any topic]` — it will work with generic defaults until you run setup.

If NOT found: workspace is configured. Proceed normally.

---

## Layout

- `context/` — brand voice, style guide, SEO guidelines, internal links map, competitor analysis
- `config/` — LinkedIn voice profile (`li_voice_profile.md`) and other workflow configs
- `topics/` → `research/` → `drafts/` → `published/` — content pipeline
- `rewrites/`, `output/` — side flows
- `examples/castos/` — reference example (do not delete)
- `tools/` — Python research and SEO analysis scripts (run from this dir)
- `data_sources/` — GA4, GSC, DataForSEO, WordPress integrations + `requirements.txt`
- `wordpress/` — MU-plugin for Yoast REST exposure
- `tests/` — test fixtures
- `.claude/commands/` — slash commands (auto-loaded when working in this dir)

## Commands

| Command | What it does |
|---------|-------------|
| `/setup` | First-time interview setup — configures all context files |
| `/research [topic]` | Keyword + competitor research |
| `/write [topic]` | Full SEO article in your brand voice |
| `/rewrite [topic]` | Update existing content |
| `/optimize [file]` | Final SEO polish pass |
| `/cluster [topic]` | Pillar + supporting article map |
| `/repurpose [file]` | Adapt for LinkedIn, Reddit, etc. |
| `/linkedin-calendar` | LinkedIn content calendar + post drafts |
| `/publish-draft [file]` | Publish to WordPress |
| `/performance-review` | Analytics-driven content priorities |
| `/priorities` | Content prioritization matrix |

Full command list: `.claude/commands/`

## Python Setup (optional — enables data integrations)

```bash
pip install -r data_sources/requirements.txt
```

API credentials in `data_sources/config/.env` (copy `.env.example` and fill in). See `data-sources-setup.md` for step-by-step credential setup.

## Conventions

- Drafts and outputs are local files. Final content goes to WordPress (via `/publish-draft`) or gets copy-pasted manually.
- `.tmp/` is disposable.
- Never commit `.env` or files in `credentials/`.
