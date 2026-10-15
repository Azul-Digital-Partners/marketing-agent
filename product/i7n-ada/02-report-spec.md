# 02. Expert-Reviewed ADA Report: Draft Spec

Status: draft for CEO approval. Hold all changes until the outside defensibility review is done (Section 10).

Design rules:

- One document. PDF. Signed.
- Every claim in it must be true and checkable.
- Plain language first, technical detail in tables and appendices.
- The reader is a non-technical owner first and their attorney second.

Fields marked AUTO are filled by the system. EXPERT means you fill or confirm them in the review screen.

---

## Section 1. Cover page

- Title: "ADA Accessibility Assessment Report"
- Subtitle: "Measured against WCAG 2.2 Level AA"
- Organization name and website (AUTO, from intake)
- Assessment date and report issue date (AUTO)
- Report ID and version, e.g. `I7N-2026-0142 v1.1` (AUTO). The version increments when the remediation record updates.
- Assessor name (AUTO, from assessor profile)

## Section 2. Summary (one page)

- Overall result, chosen from three fixed phrases (EXPERT):
  - "Substantially conforms, with the exceptions listed"
  - "Partially conforms. Remediation in progress"
  - "Does not conform. Remediation plan provided"
- Counts: criteria evaluated, supported, partially supported, not supported, not applicable (AUTO)
- Issue counts by severity (AUTO)
- Top three priorities in plain language (EXPERT, prefilled from the highest-severity findings)
- Remediation status: open, fixed, verified (AUTO)

No grades or letter scores. A "C+" invites argument. A criterion count doesn't.

## Section 3. Standard

Fixed text:

> This assessment measures the website against the Web Content Accessibility Guidelines (WCAG) version 2.2, Level AA, published by the World Wide Web Consortium (W3C). WCAG is the technical standard courts, the U.S. Department of Justice, and federal agencies reference when evaluating website accessibility under the Americans with Disabilities Act (ADA).

Optional line, pending your decision on Section 10:

> WCAG 2.2 Level AA includes all WCAG 2.1 Level AA success criteria except 4.1.1 Parsing, which W3C removed as obsolete. A site that conforms to WCAG 2.2 AA also meets the WCAG 2.1 AA criteria.

Recommendation: include it. It costs one paragraph and answers the 2.1 question before anyone asks.

## Section 4. Scope

Table with one row per item (AUTO from intake, EXPERT confirms):

| Type | Item | Notes |
|---|---|---|
| Page | `https://example.org/` | Home |
| Page | `https://example.org/donate` | Template representative of 14 campaign pages |
| Flow | Make a donation | Start: home. End: confirmation page |
| Flow | Submit contact form | |

Plus:

- How pages were selected: full crawl, or representative sample by template (EXPERT picks one)
- Browser and assistive technology used in expert review (EXPERT)
- Out of scope, stated explicitly: third-party embeds, PDFs, mobile apps, pages behind login (EXPERT edits)

Scope is the section that protects the customer and you. A report without stated limits gets read as covering everything.

## Section 5. Methodology

Fixed plain-language text. Only describe steps that actually happen.

> 1. Automated scan. Software tested each page in scope against WCAG 2.2 AA rules using a real browser.
> 2. Expert review. The assessor reviewed every automated finding, removed false positives, and adjusted severity where needed.
> 3. Manual testing. The assessor tested the user flows listed in Scope using keyboard only and [screen reader name]. The assessor evaluated criteria that software cannot reliably test, such as meaningful alt text, logical reading order, and clear error messages.
> 4. Result. Each WCAG 2.2 AA success criterion received one of four results: Supports, Partially supports, Does not support, Not applicable.

Step 3's wording depends on what you actually do per report. Confirm the exact manual steps and tools. The system should only print the tools you tick in the review screen.

## Section 6. Results by success criterion

All 55 WCAG 2.2 AA criteria, one row each (AUTO prefill, EXPERT confirms):

| Criterion | Name | Level | Result | Findings | Notes |
|---|---|---|---|---|---|
| 1.1.1 | Non-text Content | A | Partially supports | 12 | Decorative images OK. Product images missing alt. |

This uses the same result terms as a VPAT. It reads as a standard, not a sales document.

## Section 7. Findings

Grouped by severity, then by criterion. Each finding:

- ID, criterion, severity
- Page URL and element location
- What's wrong, in one sentence a site owner understands
- Who it affects, e.g. "screen reader users cannot tell what this button does"
- How to fix it, in one or two sentences
- Source: automated, expert, or both

Severity scale (keep the current four levels, rewrite the definitions):

- Critical: blocks a user from completing a task in scope
- Serious: makes a task very hard for some users
- Moderate: causes friction or confusion
- Minor: a small barrier with an easy workaround

## Section 8. Expert review notes

Free text, 150 to 400 words (EXPERT). Suggested prompts in the review screen:

- What patterns did you see across the site?
- What does the automated scan miss on this site?
- What should they fix first, and why?

This section is what makes the report yours. It is the part an AI scan can't produce.

## Section 9. Remediation record

Table that grows with each version of the report:

| Finding ID | Status | Fixed on | Verified on | Verified by |
|---|---|---|---|---|
| F-014 | Verified | 2026-11-02 | 2026-11-05 | S. Christopher |

Statuses: Open, Fixed (customer reported), Verified (assessor confirmed), Accepted risk (with reason).

This is the section that answers a demand letter: here is what we found, here is what we fixed, here is when.

## Section 10. Assessor

- Name, title, organization
- Credentials (pending your exact wording, Section 10 open question)
- Years in accessibility and number of assessments, if you want them shown
- Signature image and signature date

## Section 11. Statement of good-faith conformance

Draft for attorney review:

> [Organization] engaged i7n to assess [website] against WCAG 2.2 Level AA. This report records the scope, method, and results of that assessment as of [assessment date], and the remediation completed through [last verified date].
>
> This report is evidence of [Organization]'s good-faith effort to make its website accessible to people with disabilities. It reflects the pages and flows listed in Scope at the time of assessment. Websites change. Content added or changed after the assessment date was not evaluated.
>
> This report is not legal advice. It does not certify ADA compliance and does not guarantee against legal claims. [Organization] should consult its own legal counsel about its obligations under the ADA and other laws.

## Section 12. Appendices

- A. Full findings list (also delivered as Excel for developers)
- B. Pages crawled
- C. Glossary: WCAG, success criterion, Level A and AA, assistive technology

## Remove from the current report

- Lawsuit statistics and settlement figures
- "Safe Harbor" heading
- "Attorney-Client Use" line
- "100% coverage" claims
- Grade badges and letter grades
- VPAT recommendation text
- DOJ Title II effective dates. These shift with rulemaking. If kept, the system needs a dated source.

## Build requirements implied by this spec

1. Intake form: pages, flows, contact, deadline, "received a demand letter?" yes/no
2. Assessor profile: name, credentials, signature, stored once
3. Review screen:
   - Per-criterion result with prefill
   - Bulk disposition
   - Notes field
   - Remediation status per finding
   - Tick list of manual tools used
   - "Sign and publish" button
4. One PDF template. Reissuing a new version is one click after remediation updates.
5. Corrected 55-criterion WCAG 2.2 AA catalog

Target: you spend your time on judgment (Sections 2, 4, 6, 8, 11). The system fills everything else.
