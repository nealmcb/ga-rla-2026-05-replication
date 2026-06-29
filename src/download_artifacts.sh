#!/usr/bin/env bash
# Download Georgia May 19, 2026 RLA artifacts with HTTP headers saved separately.
set -euo pipefail
BASE="$(cd "$(dirname "$0")/.." && pwd)/2026-05-19-primary"
mkdir -p "$BASE/downloads" "$BASE/headers"

echo "Downloading final audit report..."
curl -L -D "$BASE/headers/final_report.headers.txt" \
     -o "$BASE/downloads/final_audit_report.csv" \
     'https://mcusercontent.com/bb95d9c7cf4b94c9f44421f7c/files/3bfd233a-ba7a-b94e-5f0c-a43dacbf5aae/final_audit_report_May_19_2026_General_Primary_Election_2026_06_02T2128Z.csv'

echo "Downloading ballot manifests..."
curl -L -D "$BASE/headers/manifests.headers.txt" \
     -o "$BASE/downloads/manifests.zip" \
     'https://mcusercontent.com/bb95d9c7cf4b94c9f44421f7c/files/161e79a4-c41b-a0b3-f066-21b3f3ceb961/May_19_2026_General_Primary_Election_2026_06_02T2146Z_manifests.zip'

echo "Downloading candidate totals (machine batch tallies)..."
curl -L -D "$BASE/headers/candidate_totals.headers.txt" \
     -o "$BASE/downloads/candidate_totals.zip" \
     'https://mcusercontent.com/bb95d9c7cf4b94c9f44421f7c/files/212e9ebf-d71c-817d-0a44-051c9e192b2a/May_19_2026_General_Primary_Election_2026_06_02T2148Z_candidate_totals.zip'

echo "Done. Files in $BASE/downloads/"
ls -lh "$BASE/downloads/"
