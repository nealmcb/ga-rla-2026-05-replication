#!/usr/bin/env bash
# Compute SHA256 hashes for all downloaded and extracted artifacts.
set -euo pipefail
BASE="$(cd "$(dirname "$0")/.." && pwd)/2026-05-19-primary"
mkdir -p "$BASE/hashes"

echo "=== File listing ==="
ls -lh "$BASE/downloads/"

echo ""
echo "=== File types ==="
file "$BASE/downloads/"*

echo ""
echo "=== SHA256 of downloaded files ==="
sha256sum "$BASE/downloads/"* | tee "$BASE/hashes/downloads.sha256.txt"

echo ""
echo "=== Extracting ZIPs (if not already extracted) ==="
mkdir -p "$BASE/extracted/candidate_totals" "$BASE/extracted/manifests"
unzip -q -n "$BASE/downloads/candidate_totals.zip" -d "$BASE/extracted/candidate_totals"
unzip -q -n "$BASE/downloads/manifests.zip"         -d "$BASE/extracted/manifests"

echo ""
echo "=== SHA256 of all extracted files ==="
find "$BASE/extracted" -type f -print0 | sort -z | \
  xargs -0 sha256sum | tee "$BASE/hashes/extracted_files.sha256.txt"
