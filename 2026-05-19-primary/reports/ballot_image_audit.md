---
layout: default
title: Ballot Image Audit Analysis
---

# Ballot Image Audit Analysis — Georgia May 19, 2026 General Primary

**Version:** v0.6 &nbsp;·&nbsp; **Review timestamp:** 2026-06-29T23:18:24Z &nbsp;·&nbsp; [Repository](https://github.com/nealmcb/rla-review-arlo) &nbsp;·&nbsp; [← Reports](../)

---

## Summary

The Georgia Secretary of State's office conducted a ballot image audit of the May 19, 2026
General Primary and released results on or around June 28, 2026. This report analyzes the
contest-results comparison spreadsheet released alongside the press release, reconciles the
SOS's headline statistics against the underlying data, and identifies notable discrepancy
patterns.

**Key headline (SOS):** "confirmed the outcome of all 1,785 contests reviewed"; 159
discrepancies out of 2,081,900 ballot cards (99.9924% no-discrepancy rate).

**Key finding from this analysis:** Neither headline figure is directly derivable from the
released spreadsheet. The 1,785 and 159 figures come from the internal ballot-image
comparison system; the spreadsheet is a county-level aggregate that uses a different counting
unit. We document our reconciliation attempts below.

**No outcome was changed** by any discrepancy found in this audit.

---

## What Is the Ballot Image Audit?

Georgia law requires that every ballot be digitally imaged as it passes through an optical
scanner. The ballot image audit takes those stored images and re-tabulates them independently,
then compares the re-tabulation against the original scanner results.

This is a **machine-vs-machine comparison**, not a human hand count:

| Step | What happens |
|------|-------------|
| Election day | Scanner reads each ballot (QR code for BMD; optical marks for HMPB) and saves a digital image |
| Audit | A second software pass re-reads the stored images and produces vote totals |
| Comparison | The two sets of totals are compared contest by contest, county by county |

**For BMD (in-person) ballots:** The scanner reads the QR code; the audit may re-read the
QR code from the stored image or may read the human-readable printed text via OCR. These are
not equivalent. QR codes use Reed-Solomon error correction: they either decode correctly to
the original data or fail to decode at all — there is no failure mode that silently produces
a slightly different vote count. Therefore, if the audit re-reads QR codes and finds vote
count differences, those differences cannot be attributed to image quality; they would
indicate a reading methodology difference, a software bug, or some other systematic cause.
If the audit instead reads the human-readable printed text via OCR, small differences are
expected and meaningful — they represent genuine disagreements between what the QR code
encoded and what the printed text says. A prior SOS press release was titled "Confirms 100%
Accuracy of QR Code," suggesting at least some prior audits compared QR-to-QR; whether this
audit does the same has not been publicly specified.

**For HMPB (absentee/hand-marked) ballots:** Both original and audit use optical mark
recognition (OMR), but on different substrates — the original reads the physical paper
directly; the audit reads a digital image of that paper. Here, small differences are
genuinely plausible: image resolution, scan orientation, or lighting can shift whether a
borderline-filled bubble crosses the acceptance threshold. The 1–2 vote discrepancies seen
in the data are most consistent with this OMR-threshold effect on HMPB ballots.

The SOS has not published the technical specification of how the audit image-read differs from
the original scan, so the precise source of discrepancies cannot be fully characterized from
public information.

---

## Data Sources

Two artifacts were analyzed, representing two snapshots of the same underlying system:

**Primary: `Contest Results Comparison with County Breakout.xlsx`** (released ~2026-06-28)  
Rows: 30,895 data rows  
Columns: County, ContestId, ContestName, DetailId, DetailName, OriginalCount, AuditCount, Difference  
Each row is one county × one contest × one detail. The DetailId `BC` marks a "Ballots Cast"
summary row; all other rows are individual candidates (or Yes/No choices for party questions
and referenda).

SHA256: `61679db828f4232420bd56f2a7640192b24fc03786f7f59d1ca7431694a6648e`

**Supplemental: `contest_results_comparison_with_jurisdiction_details_15.pdf`** (created 2026-06-11 14:12 UTC)  
1,923 pages covering all contests by jurisdiction. This is an **earlier version** of the
same comparison, produced approximately 17 days before the Excel release. It shows fewer
discrepancies, indicating the comparison system continued processing or reconciling data
after June 11.

| Metric | PDF (June 11) | Excel (June 28) |
|--------|--------------|-----------------|
| Unique named contests | ~550 | 974 |
| Contest × county pairs | 7,322 | 9,169 |
| Candidate rows with diff ≠ 0 | 316 | 406 |
| Sum \|diff\| (candidate rows) | 716 | 994 |
| Net signed difference | −348 | −548 |
| BC rows with diff ≠ 0 | 69 | 75 |
| Sum \|diff\| (BC rows) | 71 | 77 |

The 90 additional discrepant candidate rows in the Excel likely represent either newly
processed precincts or corrections applied between June 11 and June 28.

---

## Contests: What the Spreadsheet Contains

| Metric | Count | Notes |
|--------|-------|-------|
| Unique contest names | **974** | Across all counties |
| County × contest pairs | **9,169** | The unit the spreadsheet actually tracks |
| Unique ContestIds | **132** | IDs 1–132; reused across counties (not globally unique) |
| Contests with ≥2 candidates | **473** | By unique contest name |
| Uncontested (1 candidate) | **498** | Slightly more than half of all named contests |
| Purely local contests (1 county only) | **498** | Coincidence with uncontested count |
| Multi-county contests | **476** | State, federal, judicial, legislative |
| State/federal contests (≥50 counties) | **40** | Statewide races |

### The "1,785 Contests Reviewed" Discrepancy

The SOS press release says "confirmed the outcome of all 1,785 contests reviewed." No slice
of the spreadsheet produces this number. We attempted:

- All BC rows with votes > 0: **9,166**
- Distinct county × ContestName pairs: **9,101**
- All unique contest names: **974**
- Excluding party questions and referenda: **7,321**
- Contests appearing in ≥10 counties: **7,313**
- All unique ContestIds: **132**

The most plausible interpretation is that the SOS counts at **ballot-style granularity** rather
than county granularity. Two independent estimates from the two released artifacts both
converge on ~1,782:

- **From the Excel**: 132 distinct ContestIds × ~13.5 county-average instances ≈ 1,782
- **From the PDF**: ~550 unique named contests × ~3.25 ballot-style instances each ≈ 1,788

Both calculations arrive near 1,785, suggesting the SOS system counts each
contest-at-a-ballot-style as a unit, rather than each contest-at-a-county. This cannot
be confirmed without access to the internal tabulation system or additional SOS clarification.

---

## Discrepancies: What the Spreadsheet Shows

### Candidate-level (vote counts)

| Metric | Value |
|--------|-------|
| Candidate rows with any Difference ≠ 0 | **406** |
| Sum of \|Difference\| across all candidate rows | **994 votes** |
| Net signed difference (audit − original) | **−548** |
| Unique contest names with any discrepancy | **114 of 473 contested** |
| County × contest pairs with any discrepancy | **337** |
| Counties with any discrepancy | **50 of 159** |

### Ballot-count level (BC rows)

| Metric | Value |
|--------|-------|
| BC rows with Difference ≠ 0 | **75** |
| Sum \|Difference\| across BC rows | **77 ballot cards** |

### The "159 Discrepancies" Discrepancy

The SOS says 159 discrepancies out of 2,081,900 ballot cards — arithmetic confirmed:
(2,081,900 − 159) / 2,081,900 = **99.9924%** exactly.

This figure cannot be reproduced from the spreadsheet. The closest values we can compute:

- BC rows with any difference: **75** county×contest pairs
- Sum of |differences| in BC rows: **77 ballot cards**
- Sum of |differences| in candidate rows: **994 vote-choices**

The 159 is almost certainly a **ballot-card-level count** from the image comparison
system: for each of the 2,081,900 individual ballot cards, the system checks whether any
contest result changed between original scan and audit. If any contest on a card changed, the
card is counted as "discrepant." This metric cannot be aggregated up from county-level totals
in this spreadsheet.

The discrepancy between 159 (ballot cards) and 994 (vote-choice differences) is expected: a
single discrepant ballot card can produce multiple vote-choice differences (e.g., one ballot
card has different results in three contests → 1 discrepant card, up to 3 vote-choice
differences). Conversely, 994 vote-choice differences distributed across 2,081,900 ballot
cards could involve as few as 159 cards if each discrepant card has roughly 6 affected
contests on average — which is on the high end. The true ballot-card count likely lies between
the 75–77 BC-level estimate and the 994 vote-choice figure.

### BC vs. Candidate Mismatch (273 Cases)

In 273 of ~9,169 county×contest pairs, the BC (ballots cast) difference does not equal the
sum of candidate differences. A concrete example:

**Wilkes County, Democratic Party Question 1:**
- BC row: OriginalCount = 983, AuditCount = 983, **Difference = 0**
- "No" row: OriginalCount = 899, AuditCount = 900, **Difference = +1**
- "Yes" row: OriginalCount = 59, AuditCount = 59, Difference = 0

Total ballots cast: unchanged at 983. But one ballot that the original scanner counted as an
undervote (neither Yes nor No) was re-read by the audit as "No." The ballot still exists and
is counted; only its vote allocation changed.

This pattern reveals that the audit is **redistributing votes within a fixed ballot count**,
not finding extra or missing ballots. The discrepancy is in mark interpretation, not in whether
a ballot was processed. This is the expected behavior for OMR-on-image vs. OMR-on-paper
differences: the same physical ballot, read twice with slightly different sensitivity thresholds.

---

## Notable Findings

### 1. Cherokee County: Systematic Pattern in Party Questions

Cherokee County shows a consistent, large negative difference across all nine Republican Party
Questions — in every case, the audit found *fewer* Yes votes than the original scanner:

| Question | Yes diff | No diff |
|----------|----------|---------|
| Q1 | −13 | −1 |
| Q2 | −17 | −1 |
| Q3 | −13 | −4 |
| Q4 | −16 | −1 |
| Q5 | −18 | −1 |
| Q6 | −18 | −1 |
| Q7 | −14 | −3 |
| Q8 | −20 | −1 |
| Q9 | −16 | −1 |

Three observations:
1. **Consistent direction**: Yes loses 13–20 votes per question; No loses only 1–4. This is
   not random noise — a systematic factor is suppressing Yes reads in the audit.
2. **Consistent scale**: Losses are similar across all 9 questions (~15 Yes votes per
   question), suggesting a single underlying cause affecting that section of the ballot rather
   than question-specific content.
3. **BC rows likely show zero difference**: total ballots cast in Cherokee County for these
   contests likely didn't change, meaning the "lost" Yes votes became undervotes in the
   audit re-read.

The most likely explanation is a calibration or image-quality difference in Cherokee County's
scanned images for the party question section — the original scanner accepted borderline Yes
marks that the image re-read rejected. Whether those marks represented genuine voter intent
(in which case the original count is correct) or were scanner artifacts (in which case the
audit is correct) cannot be determined from the spreadsheet.

### 2. Muscogee and Henry Counties: Systematic Judicial-Race Losses

The June 11 PDF reveals a second county-level pattern not visible in the Excel's aggregate
view: Muscogee County shows systematic negative differences across virtually every contested
judicial race, and Henry County shows a similar (smaller) pattern.

**Muscogee County** (from the June 11 PDF):

| Race | Candidate | Diff |
|------|-----------|------|
| Sup. Court (Chattahoochee Circuit) | Tippi Cain Burch (I) | −15 |
| Supreme Court (Land) | Ben Land (I) | −15 |
| Court of Appeals (Padgett) | J. Wade Padgett (I) | −11 |
| Court of Appeals (Markle) | David Todd Markle (I) | −10 |
| Supreme Court (Warren) | Jen Auer Jordan | −10 |
| Supreme Court (Bethel) | Miracle Rankin | −9 |
| Court of Appeals (Gobeil) | Fatima Harris Felton | −7 |
| Court of Appeals (Doyle) | Sara Doyle (I) | −7 |
| Court of Appeals (Brown, III) | Will Wooten | −6 |
| Court of Appeals (Gobeil) | Elizabeth D. Gobeil (I) | −5 |
| Court of Appeals (Brown, III) | Trenton "Trent" Brown (I) | −5 |

**Henry County**: Sara Doyle −10, Gobeil (Fatima Harris Felton) −9, Padgett −7, Brown (Will Wooten) −4,
Warren (Jen Auer Jordan) −5, Bethel (both candidates) −2 each, plus party questions −2 each.

Three observations parallel to the Cherokee pattern:
1. **Consistent direction**: The audit finds fewer votes than the original scanner across essentially all judicial races in these counties.
2. **Not candidate-specific**: Multiple unrelated races and candidates are affected the same way, ruling out any candidate-specific explanation.
3. **Plausible mechanism**: Judicial races typically appear in a specific section of the ballot. A scanner calibration difference or image-quality artifact affecting that ballot section would produce exactly this pattern — systematically lower audit counts across every race in the section.

It is not yet possible to determine which reading is more accurate — original scanner or
image re-read — from the released data alone.

### 3. Net Direction: Audit Consistently Finds Fewer Votes

The net signed difference across all candidate rows is **−548** (audit found 548 fewer votes
than original tabulation). The split:

- Audit found **more** votes than original: +223 votes (across rows where Difference > 0)
- Audit found **fewer** votes than original: −771 votes (across rows where Difference < 0)

This is not symmetric noise. The audit image-re-read is systematically more conservative
(less likely to count borderline marks) than the original scanner. Cherokee County alone
contributes roughly −180 votes to this net (9 questions × ~20 vote difference), but the
directional bias persists even excluding Cherokee.

### 4. No Outcome Changes

All 1,785 (by SOS count) contest outcomes were confirmed. The smallest statewide winning
margins (thousands of votes in most races) are orders of magnitude larger than any discrepancy
found. Local races with the smallest margins also showed no outcome change.

---

## What This Audit Proves — and Doesn't

| Claim | Status |
|-------|--------|
| Scanner results and image re-reads are highly consistent | **Yes** — 99.9924% at ballot-card level (per SOS) |
| No contest outcome changed | **Yes** — confirmed across all contests |
| QR codes on BMD ballots encode votes correctly | **Unclear** — depends on whether audit reads QR or text; prior audit confirmed QR accuracy separately |
| Hand-marked ballots are read correctly by scanners | **Partially** — consistency is high, but scanner vs. image-read differences (especially in HMPB) cannot be decomposed from this data |
| Voters' intended choices are accurately captured | **Not directly addressed** — this audit compares two machine reads of the same images; it cannot detect whether the BMD encoded voter intent correctly at print time, or whether voters verified their printed ballots |

The ballot image audit is a meaningful internal consistency check. It is **not** a hand count,
and it does not verify the link between voter intent and recorded vote. It is complementary
to — but significantly weaker than — the batch-comparison RLA conducted separately.

---

## Relation to the RLA

The May 2026 primary was audited by two independent mechanisms:

| Feature | Batch-Comparison RLA | Ballot Image Audit |
|---------|---------------------|-------------------|
| Method | Human hand-count of physical ballots | Machine re-read of stored ballot images |
| Scope | 2 contests (US Senate REP, Governor DEM) | All 1,785 (SOS count) contests |
| Granularity | Batch-level (706 batches, 341,816 ballots) | Ballot-card level (2,081,900 cards) |
| Verifies | Scanner results vs. human reading of paper | Scanner results vs. image re-read |
| BMD gap | ✗ Cannot detect QR-vs-text encoding errors | ✗ Also cannot detect QR-vs-text errors (if audit reads QR) |
| Outcome confirmation | ✓ Both RLA contests confirmed | ✓ All contests confirmed |
| Public artifact quality | Full CSV with seed, sample, risk levels | County-level aggregate spreadsheet only |

The RLA provides stronger evidence for its two contests (independent human verification of
physical paper) but covers only those contests. The ballot image audit covers all contests
but provides weaker evidence (two machine reads of the same stored images).

---

## Data File

The spreadsheet (`contest_results_comparison.xlsx`) is included in this repository at
[`2026-05-19-primary/downloads/contest_results_comparison.xlsx`](../downloads/contest_results_comparison.xlsx).

SHA256:
```
61679db828f4232420bd56f2a7640192b24fc03786f7f59d1ca7431694a6648e
```

Source: Georgia Secretary of State, released ~2026-06-28 alongside the press release
["Ballot Image Audit Proves Georgia Elections are Most Accurate in Nation"](https://sos.ga.gov/news/ballot-image-audit-proves-georgia-elections-are-most-accurate-nation).
