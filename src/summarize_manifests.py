#!/usr/bin/env python3
"""
Summarize ballot manifests: county counts, batch counts, ballot counts, batch sizes.
"""
import csv, os, statistics, collections
from io import StringIO

BASE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "2026-05-19-primary")
manifest_dir = os.path.join(BASE, "extracted", "manifests")
counties = sorted(os.listdir(manifest_dir))

total_batches = 0
total_ballots = 0
batch_sizes = []
county_batches = {}
county_ballots = {}
voting_modes = collections.Counter()

for county in counties:
    county_path = os.path.join(manifest_dir, county)
    for fname in sorted(os.listdir(county_path)):
        fpath = os.path.join(county_path, fname)
        with open(fpath, encoding="utf-8-sig") as f:
            content = f.read()
        reader = csv.DictReader(StringIO(content))
        rows = list(reader)
        county_batches[county] = len(rows)
        cb = 0
        for row in rows:
            n = 0
            for k, v in row.items():
                if "Ballot" in k or "ballot" in k:
                    try:
                        n = int(v)
                    except ValueError:
                        pass
                    break
            batch_sizes.append(n)
            cb += n
            voting_modes[row.get("Container", "Unknown")] += 1
        county_ballots[county] = cb
        total_batches += len(rows)
        total_ballots += cb

print("=== BALLOT MANIFEST SUMMARY ===")
print(f"Counties: {len(counties)}")
print(f"Total batches: {total_batches}")
print(f"Total ballots in manifests: {total_ballots:,}")
print(f"Batch sizes - min: {min(batch_sizes)}, max: {max(batch_sizes)}, "
      f"median: {statistics.median(batch_sizes):.1f}, mean: {statistics.mean(batch_sizes):.1f}")

print("\nVoting modes (batch counts by container type):")
for mode, count in sorted(voting_modes.items(), key=lambda x: -x[1]):
    print(f"  {mode!r}: {count:,}")

print("\nTop 10 counties by ballot count:")
for c, b in sorted(county_ballots.items(), key=lambda x: -x[1])[:10]:
    print(f"  {c}: {b:,} ballots in {county_batches[c]} batches")

print("\nSmallest 10 counties by ballot count:")
for c, b in sorted(county_ballots.items(), key=lambda x: x[1])[:10]:
    print(f"  {c}: {b:,} ballots in {county_batches[c]} batches")
