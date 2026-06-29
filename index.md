---
layout: home
title: Georgia May 2026 RLA Transparency Investigation
---

# Georgia May 19, 2026 General Primary — RLA Transparency Investigation

**Investigator:** Neal McBurnett ([nealmcb@gmail.com](mailto:nealmcb@gmail.com))  
**Investigation date:** 2026-06-29  
**Audit conducted by:** Georgia Secretary of State / Arlo (VotingWorks)

---

## What This Repository Contains

Independent verification and transparency analysis of Georgia's statewide
Risk-Limiting Audit of the May 19, 2026 General Primary and Nonpartisan
General Election. The audit used Arlo BATCH_COMPARISON/MACRO math, covered
both the Republican US Senate primary and Democratic Governor's primary,
encompassed all 159 counties with a 5% risk limit, and hand-counted 706 batches.

**Key findings:**
- ✓ Both committed SHA256 hashes verified — files are byte-identical to what was tweeted May 28
- ✓ Four sample ticket numbers independently reproduced from the public seed
- ✓ Discrepancy rates differ by ballot type: BMD batches 14–34% vs. HMPB batches 5–7% (expected)
- ✓ Risk limit met for both contests (p = 4.91% Rep, p = 4.17% Dem)
- ⚠ Hash commitment was post-seed (~3 min after seed entry), not pre-seed
- ⚠ Commitment hosted only on X/Twitter; not archived on sos.ga.gov

---

## Reports

| Report | Description |
|--------|-------------|
| [Executive Summary](reports/README.md) | Timeline, key values, SHA256 hashes, recommendations |
| [Hash Commitment Analysis](reports/hash_commitment.md) | Verification of the @GaSecofState tweet hashes (VERIFIED) |
| [Transparency Gap Analysis](reports/transparency_gap_analysis.md) | PR #2350 comparison table, BMD vs. HMPB discrepancy rates |
| [Sample Reproducibility](reports/sample_reproducibility.md) | PPEB/MACRO algorithm, ticket number verification |
| [Manifest & Tally Analysis](reports/manifest_and_tally_analysis.md) | Schema, county statistics, diluted margins |
| [Artifact Inventory](reports/artifact_inventory.md) | All download URLs, SHA256/SHA512, HTTP headers |

---

## Scripts

| Script | Description |
|--------|-------------|
| [download_artifacts.sh](scripts/download_artifacts.sh) | Reproduce artifact downloads |
| [hash_artifacts.sh](scripts/hash_artifacts.sh) | Compute SHA256/SHA512 of all downloads |
| [reproduce_sample.py](scripts/reproduce_sample.py) | Verify ticket numbers from public seed |
| [inspect_artifacts.py](scripts/inspect_artifacts.py) | Summarize audit report structure |
| [summarize_manifests.py](scripts/summarize_manifests.py) | Summarize ballot manifest data |
| [search_for_hash.py](scripts/search_for_hash.py) | Search files for hash values |

---

## Artifacts (Downloaded)

The original SOS-published artifacts are included verbatim in `downloads/`:

| File | SHA256 | Tweeted? |
|------|--------|----------|
| [final_audit_report.csv](downloads/final_audit_report.csv) | `1efa76b8...042a8` | — |
| [manifests.zip](downloads/manifests.zip) | `c31d1f67...17aaf` | ✓ Tweeted & verified |
| [candidate_totals.zip](downloads/candidate_totals.zip) | `2842be86...10312` | ✓ Tweeted & verified |
| [jasper_rla_results_notice.pdf](downloads/jasper_rla_results_notice.pdf) | — | — |

Extracted per-county CSVs are in [extracted/manifests/](extracted/manifests/) and
[extracted/candidate_totals/](extracted/candidate_totals/).

---

## How to Replicate

```bash
# 1. Clone this repository
git clone https://github.com/nealmcb/ga-rla-2026-05-replication.git
cd ga-rla-2026-05-replication

# 2. Install dependencies
pip install consistent_sampler numpy

# 3. Verify hashes
sha256sum downloads/manifests.zip downloads/candidate_totals.zip
# Expected:
# c31d1f67404634ea04b4c68a5272655c9bd3879fe2233f4878819963cfc17aaf  manifests.zip
# 2842be86bd615160f36f0af8f6d52a2fe1192103163dd51de8d8a1617ca10312  candidate_totals.zip

# 4. Reproduce ticket numbers
python3 scripts/reproduce_sample.py
```

---

## Related

- **Arlo PR #2350**: [docs: Arlo comparison audit transparency report and guide](https://github.com/votingworks/arlo/pull/2350) (nealmcb, June 20, 2026)
- **Arlo Issue #2351**: [Document and support best practices for running robust transparent reproducible audits](https://github.com/votingworks/arlo/issues/2351)
- **Georgia SOS audit page**: [sos.ga.gov/page/elections-audit-information](https://sos.ga.gov/page/elections-audit-information)
