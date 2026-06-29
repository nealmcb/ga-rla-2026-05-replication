#!/usr/bin/env python3
"""
Attempt to reproduce the Georgia May 19, 2026 RLA sample selection.

STATUS: PARTIALLY REPRODUCIBLE.
  - Ticket numbers for individual batches CAN be reproduced from the
    public seed and public batch keys using consistent_sampler.first_fraction().
  - Two ticket numbers verified against the final audit report.
  - Full PPEB/MACRO sample draw uses numpy weighted random.choice() with
    weights derived from batch-level candidate totals (public) and
    ballot counts from the manifests (public). The exact numpy version
    matters for reproducibility.
  - Missing: exact Arlo version, numpy version used at audit time.

Requirements:
    pip install consistent_sampler numpy
"""
import sys, os, csv, collections
from io import StringIO

try:
    import consistent_sampler as cs
    from numpy.random import default_rng
    import numpy as np
except ImportError as e:
    print(f"Missing dependency: {e}")
    print("Run: pip install consistent_sampler numpy")
    sys.exit(1)

BASE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "2026-05-19-primary")

# ── Key audit parameters (from final_audit_report.csv) ───────────────────────
SEED = "06712221796172622814"
RISK_LIMIT = 0.05
REP_SAMPLE_SIZE = 138  # from audit report Round 1
DEM_SAMPLE_SIZE = 18   # from audit report Round 1

# ── Load manifests ────────────────────────────────────────────────────────────
def load_manifests():
    manifest_dir = os.path.join(BASE, "extracted", "manifests")
    manifests = {}  # (county, batch_name) -> ballot_count
    for county in sorted(os.listdir(manifest_dir)):
        for fname in os.listdir(os.path.join(manifest_dir, county)):
            fpath = os.path.join(manifest_dir, county, fname)
            with open(fpath, encoding="utf-8-sig") as f:
                for row in csv.DictReader(StringIO(f.read())):
                    bname = row.get("Batch Name", "")
                    if bname:
                        for k, v in row.items():
                            if "Ballot" in k or "ballot" in k:
                                try:
                                    manifests[(county, bname)] = int(v)
                                except ValueError:
                                    pass
                                break
    return manifests

# ── Load candidate totals ────────────────────────────────────────────────────
def load_batch_results():
    ct_dir = os.path.join(BASE, "extracted", "candidate_totals")
    rep_pfx = "US Senate - Rep - "
    dem_pfx = "Governor - Dem - "
    batch_results = {}
    for county in sorted(os.listdir(ct_dir)):
        for fname in os.listdir(os.path.join(ct_dir, county)):
            fpath = os.path.join(ct_dir, county, fname)
            with open(fpath, encoding="utf-8-sig") as f:
                for row in csv.DictReader(StringIO(f.read())):
                    bname = row.get("Batch Name", "")
                    if not bname:
                        continue
                    key = (county, bname)
                    rep_v, dem_v = {}, {}
                    for k, v in row.items():
                        if k.startswith(rep_pfx):
                            try: rep_v[k[len(rep_pfx):]] = int(v)
                            except ValueError: pass
                        elif k.startswith(dem_pfx):
                            try: dem_v[k[len(dem_pfx):]] = int(v)
                            except ValueError: pass
                    if rep_v or dem_v:
                        batch_results[key] = {}
                        if rep_v: batch_results[key]["US Senate - Rep"] = rep_v
                        if dem_v: batch_results[key]["Governor - Dem"] = dem_v
    return batch_results

# ── Verify ticket numbers against audit report ───────────────────────────────
def verify_tickets():
    print("=== TICKET NUMBER VERIFICATION ===")
    print("Verifying that batch ticket numbers are reproducible from public seed.")
    print(f"Seed: {SEED}")
    print()

    # Known ticket numbers from final_audit_report.csv
    known = [
        (("BALDWIN", "ED-North Baldwin ICP 1 - 0"), "0.427297706310130710"),
        (("BARROW", "ICC-Absentee by Mail - 2"),   "0.9088955580466120027"),
        (("BARTOW", "ED-Cartersville West ICP 1 - 0"), "0.468722862632969295"),
        (("WARE", "AV-Administrative Building ICP 1 - 0"), "0.239288422106382693"),
    ]

    all_match = True
    for batch_key, expected in known:
        ticket = cs.first_fraction(batch_key, SEED)
        trimmed = cs.trim(ticket, 18)
        match = trimmed == expected
        status = "✓ MATCH" if match else "✗ MISMATCH"
        print(f"{status}: {batch_key[0]}/{batch_key[1]}")
        print(f"         computed:  {trimmed}")
        print(f"         expected:  {expected}")
        if not match:
            all_match = False
    print()
    if all_match:
        print("All ticket numbers reproduced correctly.")
    else:
        print("WARNING: Some tickets did not match.")
    return all_match

# ── Main ──────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("Georgia May 19, 2026 RLA — Sample Reproduction Attempt")
    print("=" * 60)

    verified = verify_tickets()

    print()
    print("=== WHAT IS REPRODUCIBLE ===")
    print("  ✓ Ticket number for any (county, batch_name) pair, given the seed")
    print("    Formula: consistent_sampler.first_fraction((county, batch_name), seed)")
    print("    Trimmed to 18 digits: consistent_sampler.trim(ticket, 18)")
    print()
    print("=== WHAT IS NOT INDEPENDENTLY REPRODUCIBLE ===")
    print("  ✗ Full PPEB/MACRO sample draw uses numpy.random.default_rng with")
    print("    weighted random.choice() based on per-batch max-error bounds.")
    print("    Requires: exact numpy version, Arlo MACRO math code, and batch")
    print("    ballot counts from manifests.")
    print()
    print("=== REQUIRED INPUTS FOR FULL REPRODUCTION ===")
    print("  ✓ Random seed (found in final_audit_report.csv): 06712221796172622814")
    print("  ✓ Ballot manifests (public, downloaded)")
    print("  ✓ Candidate totals per batch (public, downloaded)")
    print("  ✓ consistent_sampler library (public, pip-installable)")
    print("  ? Exact numpy version used by Georgia's Arlo instance")
    print("  ? Arlo version / git commit used for the audit")
    print("  ? Contest parameters (total ballots, winners, risk limit)")
    print("    — these CAN be inferred from the audit report and contest totals")
    print()
    print("See reports/sample_reproducibility.md for full analysis.")
