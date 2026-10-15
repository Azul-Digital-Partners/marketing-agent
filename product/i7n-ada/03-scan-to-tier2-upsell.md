# 03. Scan Results Page to Tier 2 Upsell

Status: proposal for CEO approval. Copy is draft.

## Current flow

1. Landing page: "Run my free audit" form. Email and URL, both required.
2. Scan runs on up to 5 pages, about 5 minutes.
3. Email: "Your i7n sample audit is ready".
4. Results page (`webapp/templates/free_sample_results.html`):
   - "X of 50 WCAG 2.1 Level AA criteria passing" with a grade
   - Download buttons
   - All findings, ungated
   - "Want more?" with three CTAs: See pricing, Talk to our team, Sign in with Google
5. Every paid path goes to a contact form, then "We'll get back to you within 24 hours."

## What's wrong with it

- The page never says "ADA". The customer's word is missing from the one page where they feel the problem.
- It says WCAG 2.1 and "of 50". Section 3 positioning says 2.2.
- Tier 2 doesn't exist on the page. No expert, no name, no sample report.
- Three CTAs compete. "Sign in with Google" isn't a buying step.
- "See pricing" sends people to the automated per-audit table, not the expert report.
- It never explains what the scan can't see. That gap is the reason to buy Tier 2.
- Broken pieces:
  - The expired-sample page links to `/free?url=`, which doesn't exist (`webapp/free_sample.py:177`).
  - `POST /lead` is built but nothing calls it (`webapp/lead_capture.py:45`).

## Proposed page order

Keep findings ungated. Showing the full list builds trust, and the email is already captured.

### Block 1. The problem (top of page)

> Your website has [N] ADA accessibility issues
>
> We scanned [5] pages of [site] against WCAG 2.2 Level AA, the technical standard used in ADA website claims. [N_critical] of these issues block people with disabilities from using your site.

Severity counts below, as today. Remove the letter grade.

### Block 2. Top 5 issues, in plain language

One line each: what's broken, who it affects, which page.

> Donate button has no label. Screen reader users can't tell what it does. Page: /donate

Link: "See all [N] findings" (jumps to the full list lower on the page).

### Block 3. What this scan can't see

> Automated scans catch some accessibility problems. They can't judge whether alt text makes sense, whether a form's error messages are clear, or whether someone using only a keyboard can finish a donation. Those need a person.
>
> This scan checked [5] pages. Your site has about [crawl estimate] pages.

Use a real crawl estimate if the scan can cheaply count sitemap URLs. If not, drop the second line.

### Block 4. The offer (Tier 2)

> Get an expert-reviewed ADA report
>
> [Name], [credential], reviews your site personally. You get a signed report that shows:
> - The standard you're measured against: WCAG 2.2 Level AA
> - Exactly which pages and user flows were tested
> - Every issue, mapped to the WCAG criterion it fails
> - A record of what you fixed and when
>
> If you receive an ADA demand letter, this is the document you send back: here's our standard, here's what we assessed, here's what we fixed.
>
> From $[price]. Delivered in [N] business days.
>
> [Button] Get my expert ADA report
> [Link] See a sample report

Small print under the offer:

> This report documents your good-faith accessibility work. It isn't legal advice and doesn't guarantee against claims.

### Block 5. Secondary option (Tier 1)

> Just want the full automated scan? Scan every page for $[Tier 1 price]. [Link]

### Block 6. Full findings list

The current list, unchanged.

Remove: "Sign in with Google" as a CTA. Move it to a small "Save this report" link in the footer.

## Checkout flow

Before Stripe:

1. "Get my expert ADA report" opens a short intake form:
   - Name, organization, email (prefilled)
   - Site URL (prefilled)
   - Approximate page count
   - Key user flows (checkboxes: donate, contact, buy, register, apply, other)
   - "Have you received an ADA demand letter or legal notice?" Yes / No
   - Deadline, optional
2. The form posts to the existing `/lead` endpoint (HubSpot, Slack, email already wired).
3. Demand-letter "yes" leads get flagged in Slack for same-day reply.
4. You send a quote and an invoice.

After Stripe:

1. Same intake form.
2. A page count tier sets the price. Stripe Checkout charges the card.
3. Above the top tier, or with a demand letter: route to a call instead of checkout.

The intake form is the same in both cases. Build it once, now.

## Email follow-up (scan ran, no purchase)

The results page expires in 7 days. Use that clock.

| Day | Subject | Content |
|---|---|---|
| 0 | Your ADA scan found [N] issues | Current "ready" email. Add one line about the expert report. |
| 2 | The [N_critical] issues that block visitors on [site] | Top 3 issues in plain language. CTA: expert report. |
| 4 | What an automated scan misses | Block 3 content, plus the sample report link. |
| 6 | Your scan results expire tomorrow | Reminder plus both offers. |

## Copy rules for every customer-facing surface

- Say "ADA". Name "WCAG 2.2 Level AA" as the standard.
- Say "conformance" or "accessibility", not "compliant".
- Never: "guarantee", "lawsuit-proof", "certified compliant", "protects you from lawsuits".
- Allowed: "demand letter", "ADA claims", "evidence of good-faith effort".
- Usability can appear once, as a secondary benefit. Don't pitch it.

## Site fixes found during review

These conflict with the positioning. They need your approval because they change public copy.

- Hero badge "ADA & WCAG 2.1 / 2.2 audits" and "WCAG 2.2 criteria covered: 78" vs. pricing "all 50 WCAG 2.1" (`site/index.html:1152`, `1325`, `1507`). Pick 2.2 AA everywhere.
- "ADA: Title II & III compliance" stat (`:1328`). Reword to avoid "compliance" as an outcome.
- Meta description says "in under 60 seconds". The form says "about 5 minutes". (`:10`)
- Old app landing page still shows Pro $299 and Agency $499 (`webapp/templates/landing.html:1151`, `1170`). Remove it or redirect it to the main site.

## Measure

- Scan to intake form submit, target 5%. No baseline exists yet, so the first month sets one.
- Intake to paid Tier 2
- Demand-letter "yes" rate. This tells you which hook is working.
