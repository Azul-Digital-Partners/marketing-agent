# /setup — First-Time Setup

Runs a guided interview to configure your marketing workspace. Takes 10–15 minutes. At the end, your context files are written and you can immediately run `/research`, `/write`, and `/linkedin-calendar`.

## Detection

Before anything else, check whether setup has already been run:

```
Read context/brand-voice.md
```

If the file contains `<!-- TEMPLATE:`, setup has not been run. Proceed.

If the file does NOT contain `<!-- TEMPLATE:`, setup was already completed. Tell the user:

> Setup was already completed. Your context files are configured. Run `/research [topic]` to start.
>
> To reconfigure a specific file, you can re-run `/setup` — it will overwrite your existing context files. To update just one file, edit it directly in `context/`.

Then stop.

---

## Interview Phases

Run phases in order. Keep it conversational — one topic at a time, not a form dump. You will write files to disk at the end of each phase, not at the very end.

---

### Phase 1 — Business Foundation

> "Let's start with the basics. I'll ask you a few questions about your business — plain answers are fine, no need to be formal."

Ask these questions, one at a time:

1. **What do you do, and who do you serve?** (A sentence or two — the way you'd explain it to someone at a dinner party.)

2. **What's the main thing you want people to do after reading your content?** (Book a call / sign up for a trial / download something / follow you / something else — pick what's truest.)

3. **Who is the specific person you most want to reach?** Get them to be concrete: job title, company size, situation they're in right now. "Marketing managers" is not specific enough. "Heads of marketing at 50-person B2B SaaS companies who just inherited a content team they didn't hire" is.

4. **Who are 2–3 competitors you watch?** (Just names — you'll ask about positioning next.)

5. **What's the one thing that makes you different from those competitors?** Push past "we're more personalized" or "we care more." Get to something concrete and provable.

**After Phase 1:** Write `context/brand-voice.md` and `context/competitor-analysis.md`. Tell the user you're doing it before you do.

---

### Phase 2 — Voice and Style

> "Now let's figure out how you actually write. This matters more than most people think — the context files are only as good as your voice."

Ask:

1. **Can you paste in something you've written that you're proud of?** A LinkedIn post, an email, a paragraph from a proposal. Anything in your own words. If they can't, ask: "How would you describe your writing style in 3 words?"

2. **When you read content from other people in your space, what makes you cringe?** (This is often as useful as what they like — tells you what to avoid.)

3. **What writing style do you gravitate toward?** Options to offer if they're stuck:
   - Data-first (lead with numbers and proof)
   - Story-first (lead with an anecdote or scenario)
   - Direct takes (short sentences, strong opinions, no hedging)
   - Frameworks and systems (teach a process)
   - Mix of the above

After their answers, write a **3-sentence voice calibration** that captures what you heard, and ask them to confirm or correct it before you write the files.

**After Phase 2 confirmation:** Write `context/style-guide.md` and update `context/brand-voice.md` with their voice section.

---

### Phase 3 — SEO and Keywords (can skim if they're not doing SEO content)

Ask:

1. **What are the 3–5 topics you most want to rank for or be known for?** Don't overthink it — what would your ideal client Google when they have the problem you solve?

2. **Do you have a website? If so, what's the URL?** (Needed for internal links map.)

3. **Are there any topics you'd rather stay out of?** (Competitive keywords where you can't win, topics outside your scope, anything sensitive.)

**After Phase 3:** Write `context/target-keywords.md` and `context/internal-links-map.md` (URL placeholder + structure they can fill in later).

---

### Phase 4 — LinkedIn Strategy (optional)

Ask:

> "One optional module — LinkedIn content. Do you want to set up a LinkedIn content calendar as part of this? I'll run a quick interview and generate your first 4–6 weeks of posts. Takes about 5 minutes."

If **yes**: Run the full `linkedin-intelligence` skill interview (Phases 1–6 from that skill). At the end, save the voice profile to `config/li_voice_profile.md` and the calendar to `output/linkedin-calendar-[date].md`.

If **no**: Skip. They can run `/linkedin-calendar` later when ready.

---

### Phase 5 — Data Integrations (optional, skip if they don't want analytics)

Ask:

> "The last optional piece is data integrations — Google Analytics, Search Console, DataForSEO, and WordPress. These power the `/performance-review`, `/research`, and `/publish-draft` commands with real data. Do you want to set those up now, or skip and come back to them?"

If **yes**: Walk them through each one in turn, pointing to `data-sources-setup.md` for credential steps. Do NOT attempt to write credentials yourself — tell them each step, confirm they've done it, then move to the next.

If **no**: Tell them they can run `data-sources-setup.md` later. The core commands (`/write`, `/optimize`, `/linkedin-calendar`) work without data integrations.

---

## File Writes

After each phase (not all at once at the end), write the relevant context files. Use the Write tool. Confirm each write to the user.

### `context/brand-voice.md` template to fill in:

```markdown
# Brand Voice

## Business
[Filled from Phase 1 Q1]

## Primary CTA
[Filled from Phase 1 Q2]

## Target Audience
[Filled from Phase 1 Q3]

## Differentiation
[Filled from Phase 1 Q5]

## Voice Pillars
[Synthesized from Phase 2]

## Tone
[Filled from Phase 2]

## What We Avoid
[Filled from Phase 2 Q2]
```

### `context/style-guide.md` template:

```markdown
# Style Guide

## Writing Approach
[From Phase 2 Q3 — data-first / story-first / direct / frameworks / mix]

## Voice Calibration
[The 3-sentence calibration confirmed in Phase 2]

## Writing Sample Reference
[If they provided a sample, include first 100 words here as anchor]

## Rules
- [Specific rules derived from their "what makes you cringe" answer]
- No fabricated statistics or made-up anecdotes
- [Any platform-specific rules they mentioned]
```

### `context/target-keywords.md` template:

```markdown
# Target Keywords

## Primary Topics
[From Phase 3 Q1 — 3-5 topics]

## Topics to Avoid
[From Phase 3 Q3]

## Website
[From Phase 3 Q2]

## Keyword Clusters
[Leave as placeholder — populate after running /research]
```

### `context/competitor-analysis.md` template:

```markdown
# Competitor Analysis

## Competitors
[From Phase 1 Q4]

## Our Differentiation
[From Phase 1 Q5]

## Notes
[Populate further after running /research-gaps]
```

---

## Completion

After all files are written, print a summary:

```
Setup complete. Here's what was configured:

  context/brand-voice.md       ✓
  context/style-guide.md       ✓
  context/target-keywords.md   ✓
  context/competitor-analysis.md ✓
  context/internal-links-map.md  ✓ (partial — add your page URLs)
  config/li_voice_profile.md   [✓ or skipped]
  output/linkedin-calendar-[date].md [✓ or skipped]

Ready to use:

  /research [topic]       — keyword + competitor research for any topic
  /write [topic]          — full SEO article in your brand voice
  /optimize [file]        — final SEO polish before publishing
  /linkedin-calendar      — run or refresh your LinkedIn content calendar

Data integrations (GA4, GSC, DataForSEO, WordPress):
  See data-sources-setup.md to connect analytics and enable /performance-review.
```
