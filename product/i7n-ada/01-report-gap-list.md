# 01. Report Gap List: Current Output vs Step 1

Source: `Azul-Digital-Partners/i7n-platform` at commit `d4edb15` (Sept 13, 2026).
Status: for CEO review.

## What ships today

- Full audits produce four files: Word, PowerPoint, Excel, PDF (`webapp/worker.py:567-640`).
- Word is the primary deliverable. The PDF uses a separate template with different wording.
- The pipeline is close to 100% automated. The only human input is marking a finding "false positive" or "not applicable" with a reason of up to 500 characters.

## Fix now: live risks in shipped reports

These are already in reports customers receive. Each one weakens the report in front of an attorney.

1. The PDF claims testing that never happened.
   - `tools/templates/report_pdf.html:699-713` says "Manual keyboard navigation and screen reader verification" and lists "WAVE browser extension" and "NVDA and VoiceOver screen readers".
   - The pipeline runs none of these.
   - Opposing counsel only needs one false methodology claim to discredit the whole document.

2. The "Attorney-Client Use" line.
   - Word, Excel and PPTX say the report "is intended for use in legal and compliance proceedings" (`build_report_word.py:676`).
   - A vendor report cannot claim privilege, and the line implies legal standing it doesn't have.

3. "Safe Harbor" and settlement figures.
   - `build_report_word.py:1044-1050` cites settlement ranges ("$25,000 to $100,000+") and a "Safe Harbor" heading.
   - There is no ADA web safe harbor. The heading reads as legal advice.

4. "100% coverage" claims.
   - Word says "100% WCAG 2.1 Level AA criterion coverage" (`:616`, `:1111`).
   - The webapp's own disclaimer says automated tools find "approximately 30-40%" of issues (`audit_detail.html:618`).
   - The report contradicts the product.

5. "Compliance" language.
   - Examples: "no page achieves WCAG 2.2 AA compliance" (`build_report_v2.py:685`) and "passing 2.2 implies 2.1 compliance" (`build_report_word.py:1327`).
   - Use "conformance" for WCAG. Keep "ADA" for the framing, never "ADA compliant" as a result.

Fix effort: copy edits in three templates. Roughly a day of engineering. Recommend doing this before the next report goes out, including Elemental and CCA.

## Gap list against Step 1

| # | Requirement | Status | Gap |
|---|---|---|---|
| 1 | Standard named: ADA, WCAG 2.2 AA | Partial | The label constant says "WCAG 2.2 AA" (`criterion_catalog.py:388`), but hardcoded "WCAG 2.1" text appears in Word, PDF and PPTX. The catalog is built on "all 50 WCAG 2.1 AA criteria". WCAG 2.2 AA has 55. |
| 1a | 2.2 criteria correct | Partial | 2.4.13 Focus Appearance is graded as AA. It is AAA in 2.2. 4.1.1 Parsing is still graded. It is obsolete in 2.2. |
| 2 | Scope: URLs, pages, user flows | Partial | Lists the site and the crawled pages. No defined sample, no rationale for page selection, no user flows (checkout, donate, contact form, event signup). |
| 3 | Assessment date | Present | Two dates appear (audit date and "generated on"). Pick one assessment date and label the other "report issued". |
| 4 | Methodology in plain language | Wrong | Word describes a "4-layer automated pipeline" in technical terms. PDF describes manual testing that didn't happen. No description of expert review, because none is captured. |
| 5 | Findings mapped to SC with severity | Present | Critical, Serious, Moderate, Minor plus Advisory. Missing: a per-criterion result table (Supports, Partially supports, Does not support, Not applicable). That table is what attorneys and procurement reviewers look for. |
| 6 | Expert review notes | Missing | No section in any builder. No field in the webapp. |
| 7 | Remediation record | Missing | Dispositions allow only "false positive" or "not applicable" (`server.py:1492`). No "fixed" state, fix date, or verification date. Reruns exist but don't produce a record of what was fixed. |
| 8 | Assessor name and credentials | Missing | "Prepared by i7n". No person, credentials, or signature. |
| 9 | Good-faith conformance statement with limits | Missing | Disclaimers exist but are scattered. No single statement. Risky lines listed above sit next to them. |

## Gaps that slow your review time

Report speed caps Tier 2 volume, so these matter as much as the content gaps.

- You can only disposition findings one at a time. No bulk actions.
- Dispositions made after the build don't reach the files. There is no regenerate button (`server.py:831`, `875`).
- You have nowhere to write notes or sign off in the app. Today that means hand-editing Word.
- You have four formats to check for consistency on every audit.

## Recommendation

- One signed deliverable: a PDF generated from one template. Keep Excel as the working findings list for the customer's developers. Drop PPTX from Tier 2.
- Build the reviewer screen before the report template. The template is the easy part. The time savings come from the review screen.
- Order of work:
  1. Fix-now copy edits (1 day)
  2. WCAG 2.2 catalog correction (2.4.13, 4.1.1, 55 criteria)
  3. Reviewer screen: per-criterion verdict, notes, bulk disposition, "fixed" state, sign-off
  4. New report template per the spec in `02-report-spec.md`

Hold: per Section 10, items 2 through 4 wait for the outside defensibility review of your sample reports. Item 1 removes false statements and doesn't need to wait.
