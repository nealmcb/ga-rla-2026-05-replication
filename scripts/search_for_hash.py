#!/usr/bin/env python3
"""
Search all downloaded and extracted files for the known hash prefix from the
@GASecofState social media commitment.

Known prefix: 7d00771bf178007f4c6f43bf45b6
"""
import hashlib, os, zipfile, sys

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
KNOWN_PREFIX = "7d00771bf178007f4c6f43bf45b6"

def sha256_of(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()

def check(label, path):
    h = sha256_of(path)
    match = h.startswith(KNOWN_PREFIX)
    mark = "✓ MATCH" if match else "  no match"
    print(f"{mark}: {label}")
    print(f"        {h}")
    return match

print(f"Searching for SHA256 prefix: {KNOWN_PREFIX}")
print(f"(This is the claimed @GASecofState tweet hash from 05/28/2026 11:52 AM)")
print()

found = False

# Check main downloads
for fname in sorted(os.listdir(os.path.join(BASE, "downloads"))):
    fpath = os.path.join(BASE, "downloads", fname)
    if os.path.isfile(fpath):
        if check(f"downloads/{fname}", fpath):
            found = True

print()

# Check extracted files
for root, dirs, files in os.walk(os.path.join(BASE, "extracted")):
    for fname in sorted(files):
        fpath = os.path.join(root, fname)
        rel = os.path.relpath(fpath, BASE)
        if check(rel, fpath):
            found = True

print()
if found:
    print("✓ Hash commitment VERIFIED: found a file matching the known prefix.")
else:
    print("✗ Hash commitment NOT VERIFIED from currently available public files.")
    print()
    print("Possible explanations:")
    print("  1. The candidate_totals.zip was recompressed/regenerated after May 28,")
    print("     changing its hash (ZIP timestamps, compression level, metadata).")
    print("  2. The tweeted hash was for a URL that has since changed or been replaced.")
    print("  3. The hash was for a file available directly from Arlo (not MailChimp).")
    print("  4. The MailChimp CDN normalizes ZIP metadata (all timestamps become")
    print("     1980-01-01), changing the hash from the original upload.")
    print("  5. A different combined or normalized file was hashed.")
