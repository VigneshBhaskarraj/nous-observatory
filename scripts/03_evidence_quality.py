#!/usr/bin/env python3
"""
Script 3: Add evidence_quality field and backfill
---------------------------------------------------
evidence_quality (1–3) captures HOW certain we are of a milestone:
  3 = Confirmed    — published paper, shipped product, public announcement with details
  2 = Reported     — announced but unverified; press release without demo
  1 = Speculative  — inferred from signals, rumour, or analyst estimate

Backfill logic:
  demonstrated  → 3
  announced     → 2
  inferred      → 1
  null          → 2 (default)

Run:  python3 scripts/03_evidence_quality.py

After running, the dashboard search will show quality badges automatically.
"""

import json, urllib.request

SB_URL = "https://yjupiuxuoxmycehkbmwl.supabase.co"
SB_KEY = "sb_publishable_RUyNAQRYQq37O0IvOJ9kbQ_Cj8V0Yrr"
SB_HDR = {"apikey": SB_KEY, "Authorization": f"Bearer {SB_KEY}",
          "Content-Type": "application/json", "Prefer": "return=minimal"}

def sb_get(path, qs=""):
    url = f"{SB_URL}/rest/v1/{path}?{qs}"
    req = urllib.request.Request(url, headers={k:v for k,v in SB_HDR.items() if k!="Prefer"})
    with urllib.request.urlopen(req) as r:
        return json.loads(r.read())

def sb_patch(match_qs, body):
    url  = f"{SB_URL}/rest/v1/milestones?{match_qs}"
    data = json.dumps(body).encode()
    req  = urllib.request.Request(url, data=data, headers=SB_HDR, method="PATCH")
    with urllib.request.urlopen(req) as r:
        return r.status

print("Step 1: Add evidence_quality column (run this SQL in Supabase SQL editor if not done):")
print("""
  ALTER TABLE milestones
    ADD COLUMN IF NOT EXISTS evidence_quality INTEGER DEFAULT 2
    CHECK (evidence_quality BETWEEN 1 AND 3);
  COMMENT ON COLUMN milestones.evidence_quality IS
    '3=Confirmed, 2=Reported/Announced, 1=Speculative/Inferred';
""")
input("Press Enter once column exists (or if it already does)...")

# ── Fetch all milestones ──────────────────────────────────────────────────────
print("\nFetching milestones...")
rows, offset = [], 0
while True:
    batch = sb_get("milestones",
        f"select=id,claim_type,is_contested&order=id&limit=500&offset={offset}")
    rows.extend(batch)
    if len(batch) < 500:
        break
    offset += 500
print(f"  {len(rows)} milestones loaded")

# ── Backfill mapping ──────────────────────────────────────────────────────────
def score(m):
    ct = (m.get("claim_type") or "").lower()
    s  = {"demonstrated": 3, "announced": 2, "inferred": 1}.get(ct, 2)
    # Contested claims lose one quality point (floor 1)
    if m.get("is_contested"):
        s = max(1, s - 1)
    return s

# Group by score to batch updates (3 API calls instead of N)
by_score = {1:[], 2:[], 3:[]}
for m in rows:
    by_score[score(m)].append(m["id"])

# ── Apply updates ─────────────────────────────────────────────────────────────
print("\nApplying evidence_quality scores...")
for q, ids in sorted(by_score.items()):
    if not ids:
        continue
    label = {3:"Confirmed", 2:"Reported", 1:"Speculative"}[q]
    # Supabase in() filter
    id_list = ",".join(str(i) for i in ids)
    try:
        sb_patch(f"id=in.({id_list})", {"evidence_quality": q})
        print(f"  ✓ quality={q} ({label:<12}): {len(ids):>4} milestones updated")
    except Exception as e:
        # Fallback: update one by one if batch too large
        print(f"  Batch failed for q={q}, updating individually...")
        ok = 0
        for mid in ids:
            try:
                sb_patch(f"id=eq.{mid}", {"evidence_quality": q})
                ok += 1
            except:
                pass
        print(f"  ✓ quality={q} ({label:<12}): {ok}/{len(ids)} updated individually")

print(f"\n✓ Done: {len(rows)} milestones now have evidence_quality scores")
print("\nQuality distribution:")
for q, ids in sorted(by_score.items()):
    print(f"  {q} — {len(ids):>4} milestones")
