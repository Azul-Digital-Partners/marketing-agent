# 07. CCA Florida Review: Root Causes and Fix Plan

Input: outside review of the CCA Florida rerun (Sept 7, 2026), Run ID 190.
Verdict from the review: strong Tier 1 output. Not ready as a Tier 2 report. Score 3 met, 4 partial, 2 missing.
Status: fix plan for CEO approval. Nothing is changed in `i7n-platform` yet.

I checked each risk against the code at commit `d4edb15`. Five of the seven have a specific cause in the code.

## Root causes found in the code

### Risk 1. "98% automated coverage"

- Cause: the Word and PPTX builders hardcode coverage claims and "auto-pass" rules.
  - Example: `tools/build_report_v2.py:1350`: "Auto-pass: No payment/legal forms detected."
  - The crawler doesn't submit forms or enter checkout, so it never sees those forms. The auto-pass then marks 3.3.4 as covered.
- Fix: three-bucket coverage model. Each criterion is tagged in `webapp/criterion_catalog.py` as:
  - Automated: the tool can decide pass or fail
  - Partly automated: the tool flags candidates, the expert confirms
  - Manual: expert only
- Remove every percentage. Remove "auto-pass". A criterion with no detected candidates reads "No issues detected by automated checks. Expert confirmation required."

### Risk 2. Overlay missed

- Cause: the detector exists (`tools/extended_checks.py:93`, `check_overlay_widgets` at `:968`). Its pattern list covers accessiBe, AudioEye, UserWay, EqualWeb, accessiWay, MaxAccess, ADA Site Compliance and Recite Me. It has no pattern for Skynet Technologies "All in One Accessibility".
- Fix:
  1. Add patterns: `aioa_`, `skynettechnologies`, `All in One Accessibility`.
  2. Promote any overlay detection to a page-1 finding, above the severity counts.
  3. Copy: "An accessibility overlay is installed. Overlays do not fix the underlying code. Review the accessibility statement the overlay publishes for your organization."
- This is the highest-value single finding for CCA Florida. Tell Elemental now, before the code fix lands.

### Risk 3. Inflated issue count (1,036 should be about 730)

- Cause 1: `tools/audit_engine.py:676` maps `LINKS_NEW_WINDOW_NO_WARN` to 3.2.2 On Input at moderate severity. 3.2.2 covers form controls that change context. New-window warnings are an advisory technique. That rule produced 225 issues.
- Cause 2: 4.1.1 Parsing is still graded (`audit_engine.py:678` duplicate ID check, `criterion_catalog.py:370`). WCAG 2.2 removed it. That produced 81 issues.
- Fix: move both rules to the Advisory tier. They stay visible to developers and leave the count and the grade.

### Risk 4. Remediation math doesn't reconcile

- Cause: `tools/build_report_excel.py:722-731`.
  - The comparison builds dicts keyed on `(page, criterion, issue_type, description[:120])`. Issues that share a key collapse into one entry.
  - "Previous audit" and "Current audit" count every issue. "Fixed", "New" and "Remaining" count unique keys. The rows measure different things, so they can't add up.
  - The key includes description text. Any wording change in a check makes every old issue "fixed" and every current issue "new". That explains 719 "new" issues on a site under active remediation.
- Fix: one stable fingerprint per finding: rule ID, normalized page path, and a normalized CSS selector. Use it in the merge step (`tools/merge_results.py:84-93` already hashes a similar key) and in the comparison. Count issues, not keys, on every row.
- Then put the before and after on page 1: "1,594 issues on Aug X. 1,036 on Sept 7." Use the corrected numbers after the Risk 3 reclassification.

### Risk 5. Word, deck and workbook contradict each other

- Cause: three builders compute their own numbers. `build_report_word.py` (1,901 lines), `build_report_v2.py` (2,692 lines) and `build_report_excel.py` each read the merged results and apply their own filters and labels.
  - Example: the Word report excludes the focus-outline rule as unmatched, but the deck counts it.
- Fix: one summary file computed once after the merge (counts, top issues, per-criterion results, remediation delta). Every builder reads only that file. Add a test that fails if any two outputs disagree on a headline number.

### Risk 6. Legal context overreaches

- Cause: hardcoded text in `build_report_word.py:1032-1080` and `build_report_v2.py:1206-1208`.
- Fix: cut to two sourced sentences. Proposed:
  > Courts and the U.S. Department of Justice look to WCAG as the benchmark for website accessibility under the ADA. This report measures the site against WCAG 2.2 Level AA. It is not legal advice.
- Remove: Safe Harbor, settlement ranges, lawsuit counts, Section 508 baseline line, HHS 504 deadline, "rejected by courts" overlay line.

### Risk 7. Scope and polish

- Dev site audited, while a demand letter targets the live site.
- Production and third-party URLs leak into findings.
- Tool text leaks into client copy, such as "Safeguard prevents accidental form submission" and page titles "2" and "3".
- 313-slide, 45 MB deck.
- Fixes:
  - Scope block states the environment, in-scope domains, and flows not tested.
  - Filter findings to in-scope domains.
  - Strip internal strings.
  - Executive deck capped at 20 slides. The appendix moves to the workbook.

## Strategy calls from the review (your decisions)

1. Whose name goes on the report?
   - Reports today say "Prepared by Elemental Methods, LLC."
   - Recommend: "Prepared for [client] by Elemental Methods. Assessed by Steven Christopher, i7n." Elemental keeps the relationship. Your name carries the expert value. The case study can name both.
2. The Next Steps section sends the client to someone else.
   - `build_report_v2.py:1272` says "Schedule manual testing with a certified accessibility specialist." The disclaimer at `build_report_word.py:1617` says the same.
   - Replace with the Tier 2 call to action: "Book an i7n expert review." On white-label reports for Elemental: "Ask Elemental about expert review."
3. Credentials.
   - The reports reference a "certified accessibility specialist". If you sign without a certification, that line works against you.
   - Options: pursue IAAP CPACC (foundational) or WAS (technical). Until then the assessor block states experience, not certification. Example: "[N] years in web accessibility. [N] assessments completed."

## Fix sequence

Items 1 to 6 are the Tier 2 minimum, per the review. The estimates are engineering days, my rough read of the code.

| # | Fix | Files | Est. |
|---|---|---|---|
| 1 | Remove 98%, auto-pass and coverage claims. Three-bucket model. | `criterion_catalog.py`, Word and PPTX builders | 2 |
| 2 | Overlay patterns plus page-1 finding | `extended_checks.py`, builders | 0.5 |
| 3 | 3.2.2 new-window and 4.1.1 to Advisory | `audit_engine.py`, `criterion_catalog.py` | 0.5 |
| 4 | Stable fingerprints, correct remediation math, before and after on page 1 | `merge_results.py`, `build_report_excel.py`, Word builder | 2 |
| 5 | Single summary file feeding all outputs, plus consistency test | new summary step, all builders, tests | 3 |
| 6 | Assessor block, expert notes, Disposition column (Confirmed, Adjusted, False positive, with reason) | webapp review screen, builders | 3 |
| 7 | Legal context rewrite | Word and PPTX builders | 0.5 |
| 8 | Scope block and domain filter | crawler config, builders | 1 |
| 9 | Tier 2 call to action replaces the outside referral | builders | 0.5 |
| 10 | Executive deck capped at 20 slides | `build_report_v2.py` | 1 |
| 11 | Next CCA Florida run against production | ops | 0 |

Total: about 14 engineering days for all eleven. Items 1 to 6: about 11.

Fast path for the CCA deliverable: items 2, 3, 7 and 9 are about 2 days and remove the worst lines and the inflated count. Ship CCA on that, then reissue in the full Tier 2 format once items 1, 4, 5 and 6 land.

## What the review says already works

Keep these as they are:

- Findings with criterion, severity, page, selector and fix
- 30/60/90 roadmap
- Advisory section separating unmatched and AAA items
- Template-level dedup with an excluded URL log
- Annotated screenshots
- Rerun with progress tracking. Most competitors don't have it. After fix 4 it becomes the strongest part of the report.
