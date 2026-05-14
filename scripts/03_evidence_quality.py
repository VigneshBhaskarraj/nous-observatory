#!/usr/bin/env python3
"""
Script 3: Backfill evidence_quality on all milestones
------------------------------------------------------
evidence_quality (1–3):
  3 = Confirmed    — demonstrated in production / published paper
  2 = Reported     — announced but unverified (default)
  1 = Speculative  — inferred from signals or analyst estimate

Backfill logic:
  claim_type=demonstrated  → 3
  claim_type=announced     → 2
  claim_type=inferred      → 1  (also any is_contested milestone drops 1 point, floor 1)

Prerequisite: run 00_migrations.sql in Supabase SQL editor first.
Run:  python3 scripts/03_evidence_quality.py
"""

import json, urllib.request, urllib.error, sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from _config import SB_URL, SB_KEY

SB_HDR  = {"apikey": SB_KEY, "Authorization": f"Bearer {SB_KEY}",
           "Content-Type": "application/json"}
SB_WRIT = {**SB_HDR, "Prefer": "return=minimal"}

def sb_get(path, qs=""):
    url = f"{SB_URL}/rest/v1/{path}?{qs}"
    req = urllib.request.Request(url, headers=SB_HDR)
    with urllib.request.urlopen(req) as r:
        return json.loads(r.read())

def sb_patch_bulk(ids, quality):
    """Patch a batch of milestone IDs to the given evidence_quality."""
    if not ids:
        return 0
    id_csv = ",".join(str(i) for i in ids)
    url    = f"{SB_URL}/rest/v1/milestones?id=in.({id_csv})"
    data   = json.dumps({"evidence_quality": quality}).encode()
    req    = urllib.request.Request(url, data=data, headers=SB_WRIT, method="PATCH")
    try:
        with urllib.request.urlopen(req) as r:
            return len(ids)
    except urllib.error.HTTPError as e:
        msg = e.read().decode()
        if "does not exist" in msg:
            print("\n✗  Column 'evidence_quality' missing.")
            print("   Run 00_migrations.sql in Supabase SQL editor first:")
            print("   https://supabase.com/dashboard → SQL editor → paste scripts/00_migrations.sql\n")
            sys.exit(1)
        # Batch may be too large for URL — fall back to individual updates
        print(f"  Batch of {len(ids)} too large, updating individually...")
        ok = 0
        for mid in ids:
            try:
                url2  = f"{SB_URL}/rest/v1/milestones?id=eq.{mid}"
                data2 = json.dumps({"evidence_quality": quality}).encode()
                req2  = urllib.request.Request(url2, data=data2, headers=SB_WRIT, method="PATCH")
                with urllib.request.urlopen(req2):
                    ok += 1
            except:
                pass
        return ok

# ── Fetch milestones ──────────────────────────────────────────────────────────
print("Fetching milestones...")
rows, offset = [], 0
while True:
    batch = sb_get("milestones",
        f"select=id,claim_type,is_contested&order=id&limit=500&offset={offset}")
    rows.extend(batch)
    if len(batch) < 500:
        break
    offset += 500
print(f"  {len(rows)} milestones loaded\n")

# ── Score every milestone ─────────────────────────────────────────────────────
def score(m):
    ct = (m.get("claim_type") or "").lower()
    s  = {"demonstrated": 3, "announced": 2, "inferred": 1}.get(ct, 2)
    if m.get("is_contested"):
        s = max(1, s - 1)
    return s

by_score = {1: [], 2: [], 3: []}
for m in rows:
    by_score[score(m)].append(m["id"])

labels = {3: "Confirmed   ", 2: "Reported    ", 1: "Speculative "}
total  = 0

# ── Apply in bulk (one PATCH per quality level) ───────────────────────────────
print("Applying evidence_quality scores (3 bulk updates)...")

# Split into chunks of 200 IDs to stay within URL length limits
def chunks(lst, n=200):
    for i in range(0, len(lst), n):
        yield lst[i:i+n]

for q in [3, 2, 1]:
    ids = by_score[q]
    if not ids:
        print(f"  quality={q} ({labels[q]}): 0 milestones — skipped")
        continue
    updated = 0
    for chunk in chunks(ids):
        updated += sb_patch_bulk(chunk, q)
    total += updated
    print(f"  quality={q} ({labels[q]}): {updated:>4} milestones ✓")

print(f"\n✓ Done: {total}/{len(rows)} milestones updated with evidence_quality")
