# i7n ADA Product: First Tasks from the Oct 15, 2026 Handoff

Responses to Section 9 of the CEO handoff. Everything here is a proposal. Nothing is built, priced, or published.

| # | Task | File |
|---|---|---|
| 1 | Gap list: current report vs Step 1 | [01-report-gap-list.md](01-report-gap-list.md) |
| 2 | Report spec, section by section | [02-report-spec.md](02-report-spec.md) |
| 3 | Scan results page to Tier 2 upsell | [03-scan-to-tier2-upsell.md](03-scan-to-tier2-upsell.md) |
| 4 | Tier 1 and Tier 2 pricing options | [04-pricing-options.md](04-pricing-options.md) |
| 5 | Elemental and CCA case study plan | [05-elemental-cca-case-study-plan.md](05-elemental-cca-case-study-plan.md) |
| 6 | Defensibility review instructions | [06-defensibility-review-prompt.md](06-defensibility-review-prompt.md) |

Evidence comes from `Azul-Digital-Partners/i7n-platform` at commit `d4edb15`.

## Most important finding

Today's reports contain statements that would hurt the customer in front of an attorney:

- The PDF claims manual screen reader testing (NVDA, VoiceOver) that the pipeline never performs.
- Reports say they are "intended for use in legal and compliance proceedings" under an "Attorney-Client Use" label.
- A "Safe Harbor" section and settlement figures read as legal advice.
- "100% coverage" claims contradict the app's own "30-40%" disclaimer.

Removing these is a one-day copy fix. Do it before the CCA reports ship.

## Other facts that change the plan

- Stripe isn't started. No code exists. Step 3 is a build, not a finish.
- No named expert appears anywhere in the funnel or the report.
- The WCAG catalog is built on 2.1 (50 criteria). 2.2 AA has 55. 2.4.13 is wrongly graded as AA, and 4.1.1 is still graded.
- The only reviewer input in the app is "false positive / not applicable". No notes, no sign-off, no "fixed" state.

## Decisions needed from you

1. Approve the fix-now copy edits (gap list, top section). Recommend: yes, now.
2. Pricing: Option A, B, or C (recommend B).
3. Your real review hours per report, or approval to measure them on CCA first.
4. Credentials wording for the assessor block.
5. Include the WCAG 2.1 equivalence paragraph (recommend: yes).
6. Elemental's CCA timeline, and permission to request case study rights now.
7. Public site copy fixes listed in file 03.
