# marketing-agent

Interview-driven marketing agent for Claude Code. Self-configures your brand voice, content pillars, and social strategy in 10–15 minutes. Create SEO-optimized blog content, conversion-focused landing pages, and LinkedIn content calendars with full post drafts.

Forked from [TheCraigHewitt/seomachine](https://github.com/TheCraigHewitt/seomachine).

## What You Get

**Quick Setup**
- `/setup` — Interview-driven configuration. No file editing required. Fills all brand context files automatically.

**Content Creation**
- `/write [topic]` — Full SEO article (2000–3000+ words) in your brand voice
- `/research [topic]` — Keyword research, competitor analysis, content gaps
- `/rewrite [topic]` — Update existing content with data-driven improvements
- `/optimize [file]` — Final SEO polish pass before publishing
- `/repurpose [file]` — Adapt content for LinkedIn, Reddit, newsletters
- `/linkedin-calendar` — 4–6 week LinkedIn content calendar with full post drafts (voice profile interview + structured calendar builder)
- `/cluster [topic]` — Pillar + supporting article map
- `/article [topic]` — Simplified workflow for one-shot articles

**Strategy & Analysis**
- `/priorities` — Content prioritization matrix (analytics-driven)
- `/performance-review` — Highest-impact content tasks from real GA4 and GSC data
- `/research-gaps`, `/research-trending`, `/research-performance` — Specialized research flavors
- `/scrub [file]` — Strip AI patterns and template language from drafts

**Landing Pages**
- `/landing-write [topic]` — Conversion-focused landing page
- `/landing-audit [file]` — CRO issues and fix recommendations
- `/landing-research [topic]` — Competitor landing page positioning
- `/landing-competitor [URL]` — Deep competitor analysis
- `/landing-publish [file]` — Publish to WordPress

**Auto-Running Agents**
After `/write`, these agents analyze automatically:
- **Content Analyzer** — Search intent, keyword density, readability, SEO quality score
- **SEO Optimizer** — On-page recommendations
- **Meta Creator** — Multiple meta title/description options
- **Internal Linker** — Specific internal linking suggestions
- **Keyword Mapper** — Keyword placement and density analysis
- **Editor** — Humanity score and robotic pattern detection
- **Headline Generator** — 10+ headline variations
- **CRO Analyst** — Landing page conversion analysis
- **Performance** — Analytics-driven prioritization

**Marketing Skills**
38 slash commands for copywriting, CRO, strategy, email, social, SEO, analytics, pricing, product marketing, and more:
`/copy-editing`, `/page-cro`, `/form-cro`, `/signup-flow-cro`, `/onboarding-cro`, `/popup-cro`, `/paywall-upgrade-cro`, `/content-strategy`, `/email-sequence`, `/social-content`, `/paid-ads`, `/marketing-psychology`, `/ab-test-setup`, `/pricing-strategy`, `/launch-strategy`, `/referral-program`, `/free-tool-strategy`, `/seo-audit`, `/schema-markup`, `/programmatic-seo`, `/competitor-alternatives`, `/analytics-tracking`, and more.

## Quick Start

```bash
git clone https://github.com/Azul-Digital-Partners/marketing-agent.git
cd marketing-agent
./setup.sh
```

Then open in Claude Code:
```bash
claude .
```

Run `/setup` in Claude Code — it's a 5-phase interview (business foundation → voice calibration → SEO strategy → LinkedIn strategy → data integrations). Takes 10–15 minutes. No file editing required.

Once configured, try:
```
/write sustainable product design trends
```

## Prerequisites

- [Claude Code](https://claude.com/claude-code)
- Python 3.8+
- Anthropic API account

## Data Integrations (Optional)

SEO analysis and prioritization require credentials, but the workspace works fine without them. Set up only what you need:

| Integration | Purpose | Setup |
|-------------|---------|-------|
| **Google Analytics 4** | Traffic trends, engagement metrics | Google Cloud Console → service account → `GA4_CREDENTIALS_PATH` |
| **Google Search Console** | Keyword rankings, CTR, impressions | Google Cloud Console → service account → `GSC_CREDENTIALS_PATH` |
| **DataForSEO** | Competitor rankings, SERP features | dataforseo.com → email/password → `DATAFORSEO_LOGIN`, `DATAFORSEO_PASSWORD` |
| **WordPress REST API + Yoast** | Publish directly from drafts | WordPress → enable REST API, Yoast plugin → `WORDPRESS_URL`, `WORDPRESS_USERNAME`, `WORDPRESS_PASSWORD` |
| **LinkedIn OAuth** (for /linkedin-calendar) | Flagged posts tracking | linkedin.com/developers → app credentials → `LINKEDIN_CLIENT_ID`, `LINKEDIN_CLIENT_SECRET` |

Details: See `data-sources-setup.md`.

## Configuration

Run `/setup` first. It writes all context files for you:
- `context/brand-voice.md` — Your voice, messaging, examples
- `context/writing-examples.md` — 3–5 exemplary posts
- `context/features.md` — Product/service benefits
- `context/internal-links-map.md` — Key pages to link to
- `context/style-guide.md` — Tone, formatting preferences
- `context/target-keywords.md` — Topic clusters
- `context/competitor-analysis.md` — Competitor positioning
- `context/seo-guidelines.md` — SEO requirements

If you prefer manual configuration, see `examples/castos/` for a real-world example.

## Directory Structure

```
.claude/
  commands/           # Slash commands (auto-loaded)
  rules/             # Agent behavior rules
  skills/            # Marketing sub-skills
context/             # Brand voice, style, SEO, competitors (templates — run /setup to fill)
config/              # LinkedIn voice profile, workflow configs
data_sources/        # GA4, GSC, DataForSEO, WordPress integration
  config/.env        # API credentials (created by setup.sh)
  requirements.txt   # Python dependencies
tools/               # Python analysis modules (SEO, CRO, analytics)
topics/              # Content ideas and planning
research/            # Research briefs and analysis
drafts/              # Article drafts before publishing
published/           # Published articles (local reference)
rewrites/            # Updated versions of articles
output/              # Generated content and reports
examples/castos/     # Real-world example (Castos podcast hosting)
wordpress/           # WordPress MU-plugin for Yoast REST exposure
.env.example         # Environment template (copy to .env)
```

## Workflows

### Create New Content

1. **Research**
   ```
   /research sustainable product design for SaaS
   ```
   Outputs research brief to `research/`. Includes keywords, competitors, gaps, outline.

2. **Write**
   ```
   /write sustainable product design for SaaS
   ```
   Full article to `drafts/`. Auto-runs Content Analyzer, SEO Optimizer, Meta Creator, Internal Linker, Keyword Mapper.

3. **Optimize**
   ```
   /optimize drafts/sustainable-design-2025-07-17.md
   ```
   Final polish pass. SEO score, priority fixes, meta options, readiness assessment.

4. **Publish**
   ```
   /publish-draft drafts/sustainable-design-2025-07-17.md
   ```
   Send to WordPress with Yoast metadata.

### Update Existing Content

```
/rewrite sustainable design guide
```
Refreshes outdated content, adds new gaps, maintains what works. Saves to `rewrites/`.

### Content Planning

```
/priorities
```
Analytics-driven prioritization matrix. Shows highest-impact tasks from GA4 + GSC.

```
/cluster sustainable product design
```
Pillar + supporting article map for topic clusters.

### LinkedIn Calendar

```
/linkedin-calendar
```
6-phase interview (business, voice, storytelling, tone, posting frequency, pillar topics) → generates 4–6 week calendar with full post drafts for weeks 1–2. Posting is always manual.

## Using with Claude Code

This workspace is optimized for Claude Code. Key files:
- `CLAUDE.md` — First-run detection, command list, architecture
- `.claude/commands/` — Slash commands
- `.claude/skills/` — Marketing sub-skills
- `.claude/rules/` — Agent behavior

When you open in Claude Code:
```bash
claude .
```

Claude reads `CLAUDE.md` automatically. First time? Run `/setup`.

## Python Setup

If you want analytics integrations, install Python dependencies:

```bash
pip install -r data_sources/requirements.txt
```

This installs:
- Google Analytics/Search Console APIs
- DataForSEO client
- NLP (nltk, textstat)
- Machine learning (scikit-learn)
- Web scraping (beautifulsoup4)
- Markdown processing

Then follow `data-sources-setup.md` to connect your GA4, GSC, DataForSEO accounts.

## Contributing

This project welcomes contributions. See [CONTRIBUTING.md](CONTRIBUTING.md) for:
- How to report issues
- How to submit pull requests
- Conventions for new skills and commands

## License

MIT License. See [LICENSE](LICENSE) for details.

## Support

- **First-time help**: Run `/setup` in Claude Code
- **Questions**: Check `CLAUDE.md` for full command reference
- **Issues**: See [CONTRIBUTING.md](CONTRIBUTING.md) to report bugs
- **Examples**: `examples/castos/` has a complete, real-world setup

## Acknowledgments

Built on [seomachine](https://github.com/TheCraigHewitt/seomachine) by Craig Hewitt. Expanded with interview-driven setup, LinkedIn calendars, landing page workflows, and 38 marketing skills.
