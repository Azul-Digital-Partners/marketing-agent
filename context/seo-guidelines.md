# SEO Guidelines — [Your Company] + [your product]

SEO best practices and requirements for all [Your Company] blog and [your product] content. Reference alongside [target-keywords.md](target-keywords.md) (what to target), [internal-links-map.md](internal-links-map.md) (what to link to), and [style-guide.md](style-guide.md) (writing mechanics).

> Living document. SEO conventions change — review and update twice a year.

## Content Length

### Target word counts

- **Standard blog post**: 1,500–3,000 words (target: 2,000–2,500).
- **Pillar / cluster head page**: 3,000–5,000 words. Comprehensive coverage of a topic cluster.
- **Comparison content** (e.g., "Deque vs [your product]"): 1,800–2,500 words.
- **Landing page**: 600–1,200 words.
- **Short answer / explainer**: 800–1,200 words. Use when the search intent is direct ("what is WCAG").

### Why these lengths

- Sub-1,200 words rarely earns top SERP positions for commercial queries.
- 3,000+ words is justified only when topic depth supports it. Padding to hit a word count is worse than a tighter article.
- Match length to search intent. "What is WCAG 2.1 AA" wants 800 clear words; "complete WCAG audit guide" wants 3,000.

## Keyword Strategy

### Primary keyword (one per page)

- Volume: 100+ monthly searches (validate in DataForSEO before committing).
- Difficulty: medium or lower for new content; higher only when we have a real authority advantage.
- Intent match: pick a keyword whose SERP shape matches what we're going to write (informational vs commercial).

### Secondary keywords (3–5 per page)

- Variations on the primary: "WCAG 2.1 AA audit" → "WCAG audit," "automated WCAG testing," "accessibility audit."
- Question forms: "How does automated WCAG testing work?"
- Long-tail extensions: "WCAG 2.1 AA audit for agencies," "WCAG 2.1 AA audit React app."

### Avoid keyword stuffing

❌ "WCAG audit is important. WCAG audit helps companies. Our WCAG audit platform offers WCAG audit services for WCAG audit needs."

✅ "WCAG audits matter for companies that need procurement-ready accessibility evidence. A real audit reports against the actual code — not a layered overlay — and that distinction is what holds up under legal review."

### Keyword density

- Primary keyword: 0.5%–1.5% density (rough target — modern SEO is semantic, not density-driven).
- Use the primary keyword in: title, first 100 words, at least one H2, meta description, URL.
- Use secondary keywords: 1–3 times each, distributed naturally.

## Title Tags

- **Length**: 50–60 characters (including " | [Your Company]" or " | [your product]" suffix when used).
- **Primary keyword**: in the first 30 characters when possible.
- **Brand suffix**: include " | [Your Company]" or " | [your product]" when space allows. Skip if it pushes over 60 characters.
- **Unique**: every page on the site has a unique title.

### Patterns that work

- `[Primary keyword]: [Specific angle] | [your product]`  — "WCAG 2.1 AA Audit: Full Coverage for Agencies | [your product]"
- `[Number] [Topic] [Outcome] | [Your Company]` — "5 Ways to Ship AI to Production in 90 Days | [Your Company]"
- `[Topic] Guide for [Audience]` — "WCAG Audit Guide for Mid-Market Compliance Teams"

### Examples

- ✅ "ADA Title III Website Compliance: 2026 Checklist | [your product]" (53 chars)
- ✅ "axe DevTools vs [your product]: Which Fits Agency Workflows?" (51 chars)
- ❌ "Accessibility Tips" (too vague, no keyword)
- ❌ "The Ultimate Comprehensive Complete Guide to Everything About WCAG 2.1 AA Compliance for Mid-Market Companies and Their Agencies in 2026" (way too long)

## Meta Descriptions

- **Length**: 150–160 characters.
- **Lead with value proposition**: not "This article covers..."
- **Include primary keyword naturally**: don't force-fit if it reads awkwardly.
- **Include CTA when natural**: "Get the checklist." "See how it works." "Compare side by side."
- **Active voice**: "Audit your sites in minutes" not "Sites can be audited in minutes."

### Examples

- ✅ "Run full WCAG 2.1 AA audits across every site you manage. AI-cleaned findings, authenticated SPA scanning, agency workspaces. See how [your product] fits your workflow." (159 chars)
- ✅ "ADA Title III applies to most public-facing websites. Here's what mid-market compliance teams need to verify before the next demand letter arrives." (155 chars)
- ❌ "This is a blog post about WCAG audits where we discuss many WCAG-related topics." (vague, no value prop, no keyword)

## URL Structure

- **Length**: 3–5 words ideal. 60 characters max.
- **Lowercase only.** Hyphens, not underscores.
- **Match primary keyword**: include without stuffing.
- **Strip stop words**: "and," "or," "the," "a," "in" go away unless removing them changes meaning.
- **Predictable pattern**: `/blog/[slug]` for all blog content.

### Examples

- ✅ `/blog/wcag-audit-guide`
- ✅ `/blog/ada-title-iii-checklist`
- ✅ `/blog/axe-vs-[your product]-comparison`
- ❌ `/blog/the-ultimate-comprehensive-guide-to-wcag-2-1-aa-audits-in-2026` (too long)
- ❌ `/blog/Article_002_FINAL_v3.html` (underscores, capitals, version suffix)

## On-Page SEO

### H1

- Match or closely paraphrase the title tag.
- Include primary keyword.
- One H1 per page.
- Don't repeat verbatim in body content.

### H2 / H3 structure

- H2s break the article into scannable sections.
- Reading only the H2s should give a coherent argument.
- Include primary keyword in 1–2 H2s naturally.
- Use question-form H2s for "people also ask" capture: "How does automated WCAG testing work?" "What does a WCAG 2.1 AA audit actually test?"

### First 100 words

- Include the primary keyword once, naturally.
- State what the reader will learn / get from the article.
- Don't waste them on throat-clearing ("In today's fast-paced digital landscape...").

### Internal linking

- 3–5 internal links per blog post minimum (when blog has 5+ posts).
- Link to: relevant service page, related blog posts, the most relevant case study on /work.
- See [internal-links-map.md](internal-links-map.md) for the full linking strategy.

### Outbound links

- Link to authoritative sources: W3C for WCAG, ADA.gov for legal references, court decisions for lawsuit content.
- 2–4 outbound links per article — enough to demonstrate research, not so many that readers leave.
- Don't link to direct competitors except when the comparison content explicitly requires it.

## E-E-A-T Signals

Content needs to demonstrate Experience, Expertise, Authoritativeness, and Trustworthiness:

- **Experience**: name real engagements (BrandExtract, Elemental Methods), real platforms ([your product] at [your product]app.com), real outcomes.
- **Expertise**: cite relevant credentials (decades on both sides, WCAG 2.1 AA full coverage, $100M+ portfolio programs managed).
- **Authoritativeness**: link to and be linked from credible industry sources. Build agency partnerships.
- **Trustworthiness**: be honest about what we do and don't do. Acknowledge competitor strengths. Don't fabricate stats.

[Your Name]'s first-person LinkedIn voice (see [writing-examples.md](writing-examples.md)) is a major E-E-A-T asset for [Your Company]. Use it.

## Image SEO

### File naming

- Lowercase, hyphenated, descriptive: `[your product]-dashboard-screenshot.png`, `wcag-coverage-comparison.jpg`.
- Include the primary keyword when relevant.
- Avoid generic names: `image1.png`, `chart.jpg`.

### Alt text

- Describe the image accurately.
- Include primary keyword *only when natural*.
- Keep under 125 characters.

### Captions

- Use sparingly. Add only when the image needs context that's not obvious.

### File size and format

- Compress images. Target under 200KB for inline images.
- Use modern formats (WebP) when supported.
- SVG for diagrams, logos, icons.

## Featured Snippets / Answer Boxes

For informational queries, structure content to capture featured snippets:

### Definition snippets

Open the relevant section with: `[Term] is [definition].`

> **What is a WCAG audit?**
> A WCAG audit is an evaluation of a website's accessibility against the Web Content Accessibility Guidelines, typically version 2.1 Level AA. It identifies barriers that prevent users with disabilities from accessing content and provides remediation guidance.

### List snippets

Use ordered or unordered lists with H3-introduced items. Match query patterns ("steps to," "ways to," "best...").

### Table snippets

Use HTML tables (not just bulleted comparisons) when the query implies a comparison or matrix.

## AI Search / GEO Optimization

AI search engines (ChatGPT, Perplexity, Google AI Overviews) cite content that:

- Provides the clearest, earliest answer in the article.
- Uses structured headings and lists that the AI can parse.
- Cites authoritative sources.
- Avoids fluff before the answer.

### Practical implication

The first 200 words of any article should contain the canonical answer to the article's primary question. Save the deeper context for later sections.

> When a user asks ChatGPT "best automated WCAG audit tool" or "how does ADA Title III apply to websites," the AI scans articles and pulls from the earliest clear answer it finds. If we bury the answer at line 1,500, we don't get cited.

See [ai-citation-targets.md](ai-citation-targets.md) for the off-page strategy on AI citations.

## What to NEVER do

- Buy backlinks or use private blog networks (PBNs).
- Auto-generate content without human edit pass.
- Cloak content (different content for bots vs users).
- Stuff keywords beyond natural usage.
- Publish thin content (under 800 words for any topic that warrants depth).
- Duplicate content across pages.
- Plagiarize from competitors.
- Make claims we can't substantiate (e.g., "we've shipped 500 AI products" when the real number is much smaller).

## QA Before Publishing

Run this checklist before any blog post or landing page goes live:

- [ ] Primary keyword in title, H1, first 100 words, meta description, URL
- [ ] Title tag 50–60 characters
- [ ] Meta description 150–160 characters
- [ ] At least one internal link to a service page
- [ ] Closing CTA links to /contact
- [ ] All images have alt text
- [ ] All images compressed (under 200KB each)
- [ ] No banned words (see [style-guide.md](style-guide.md))
- [ ] No AI-template patterns (see brand-voice + writing-examples)
- [ ] Outbound links open in same tab
- [ ] Brand names spelled correctly ([Your Company], [your product], lowercase [your product])
- [ ] No fabricated stats or lived experience in first-person [Your Name] content
- [ ] Featured-snippet-friendly structure if informational intent

## Open items

- [ ] Set up search-console / GA4 tracking for first cohort of blog posts
- [ ] Define schema markup approach (Article, FAQ, HowTo) for blog templates
- [ ] Build canonical URL strategy for syndicated content (LinkedIn republishing, etc.)
