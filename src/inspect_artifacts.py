#!/usr/bin/env python3
"""
Inspect the structure and contents of Georgia May 19, 2026 RLA artifacts.
Prints schema, row counts, contests, and key values from the final audit report.
"""
import csv, sys, os
from io import StringIO

BASE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "2026-05-19-primary")

def inspect_final_report():
    path = os.path.join(BASE, "downloads", "final_audit_report.csv")
    print(f"=== FINAL AUDIT REPORT: {path} ===")
    with open(path) as f:
        lines = f.readlines()
    print(f"Total lines: {len(lines)}")
    print("\nSection headers:")
    for i, line in enumerate(lines):
        if "########" in line:
            print(f"  Line {i+1}: {line.strip()}")

    # ELECTION INFO
    print("\n--- ELECTION INFO ---")
    for line in lines[1:4]:
        print("  " + line.strip())

    # CONTESTS
    print("\n--- CONTESTS ---")
    contest_start = next(i for i,l in enumerate(lines) if "CONTESTS" in l) + 1
    for line in lines[contest_start:contest_start+3]:
        if line.strip():
            print("  " + line.strip()[:120])

    # AUDIT SETTINGS
    print("\n--- AUDIT SETTINGS ---")
    settings_start = next(i for i,l in enumerate(lines) if "AUDIT SETTINGS" in l) + 1
    for line in lines[settings_start:settings_start+3]:
        if line.strip():
            row = list(csv.reader([line]))[0]
            print("  " + str(row))

    # ROUNDS
    print("\n--- ROUNDS ---")
    rounds_start = next(i for i,l in enumerate(lines) if "ROUNDS" in l) + 1
    for line in lines[rounds_start:rounds_start+4]:
        if line.strip():
            row = list(csv.reader([line]))[0]
            if row[0]:
                print("  Round: " + str(row[:10]))

    # SAMPLED BATCHES
    print("\n--- SAMPLED BATCHES ---")
    batch_start = next(i for i,l in enumerate(lines) if "SAMPLED BATCHES" in l) + 1
    header = list(csv.reader([lines[batch_start]]))[0]
    print(f"  Columns ({len(header)}):")
    for j, col in enumerate(header):
        print(f"    [{j}] {col}")

    batch_rows = []
    for line in lines[batch_start+1:]:
        if not line.strip() or "########" in line:
            break
        row = list(csv.reader([line]))[0]
        if len(row) >= 3 and row[0] not in ("", "Totals"):
            batch_rows.append(row)

    print(f"\n  Total batch rows: {len(batch_rows)}")
    disc = [r for r in batch_rows if (len(r)>8 and r[8].strip()) or (len(r)>12 and r[12].strip())]
    print(f"  Rows with discrepancies: {len(disc)}")

    rep_extra = sum(1 for r in batch_rows if len(r)>3 and r[3].strip()=="Round 1: EXTRA")
    rep_num   = sum(1 for r in batch_rows if len(r)>3 and r[3].strip() not in ("", "Round 1: EXTRA"))
    dem_extra = sum(1 for r in batch_rows if len(r)>4 and r[4].strip()=="Round 1: EXTRA")
    dem_num   = sum(1 for r in batch_rows if len(r)>4 and r[4].strip() not in ("", "Round 1: EXTRA"))
    print(f"  Rep Senate primary sample (PPEB-selected): {rep_num}")
    print(f"  Rep Senate EXTRA (combined into other batch): {rep_extra}")
    print(f"  Dem Governor primary sample: {dem_num}")
    print(f"  Dem Governor EXTRA: {dem_extra}")

    totals = [r for r in list(csv.reader(lines[batch_start+1:batch_start+len(batch_rows)+10])) if r and r[0]=="Totals"]
    if totals:
        tr = totals[0]
        print(f"\n  Totals row - Ballots in sample: {tr[2]}")

if __name__ == "__main__":
    inspect_final_report()
