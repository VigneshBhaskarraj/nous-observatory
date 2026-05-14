#!/usr/bin/env python3
"""
Script 2: Entity aggregate embeddings + cosine similarity
----------------------------------------------------------
1. Averages all milestone embeddings per entity → "strategic DNA" vector (in memory only)
2. Computes pairwise cosine similarity matrix
3. Writes top-5 most similar entities per entity → entities.similar_entities (jsonb)

Prerequisite: run 00_migrations.sql in Supabase SQL editor first.
Run AFTER 01_enrich_embeddings.py for best quality.

Run:  python3 scripts/02_entity_embeddings.py
"""

import json, math, urllib.request, urllib.error, sys, pathlib
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

def sb_patch(path, match_qs, body):
    url  = f"{SB_URL}/rest/v1/{path}?{match_qs}"
    data = json.dumps(body).encode()
    req  = urllib.request.Request(url, data=data, headers=SB_WRIT, method="PATCH")
    try:
        with urllib.request.urlopen(req) as r:
            return r.status
    except urllib.error.HTTPError as e:
        msg = e.read().decode()
        if "does not exist" in msg:
            print("\n✗  Column missing — run 00_migrations.sql in Supabase SQL editor first:")
            print("   https://supabase.com/dashboard → SQL editor → paste 00_migrations.sql\n")
            sys.exit(1)
        raise

def cosine(a, b):
    dot  = sum(x*y for x,y in zip(a, b))
    magA = math.sqrt(sum(x*x for x in a))
    magB = math.sqrt(sum(x*x for x in b))
    return dot / (magA * magB) if magA and magB else 0.0

def avg_vec(vecs):
    if not vecs:
        return None
    n   = len(vecs[0])
    avg = [sum(v[i] for v in vecs) / len(vecs) for i in range(n)]
    mag = math.sqrt(sum(x*x for x in avg))
    return [x/mag for x in avg] if mag else avg

# ── Fetch milestones with embeddings ─────────────────────────────────────────
print("Fetching milestone embeddings...")
rows, offset, page = [], 0, 500
while True:
    batch = sb_get("milestones",
        f"select=id,entity_id,embedding&embedding=not.is.null"
        f"&order=id&limit={page}&offset={offset}")
    rows.extend(batch)
    if len(batch) < page:
        break
    offset += page
print(f"  {len(rows)} milestones with embeddings")

if not rows:
    print("\n✗  No milestone embeddings found. Run 01_enrich_embeddings.py first.")
    sys.exit(1)

# ── Fetch entities ────────────────────────────────────────────────────────────
entities   = sb_get("entities", "select=id,name&order=name&limit=100")
eid_to_name = {e["id"]: e["name"] for e in entities}
print(f"  {len(entities)} entities\n")

# ── Per-entity average embedding ─────────────────────────────────────────────
by_entity = {}
for m in rows:
    emb = m.get("embedding")
    if not emb:
        continue
    if isinstance(emb, str):
        emb = json.loads(emb)
    by_entity.setdefault(m["entity_id"], []).append(emb)

entity_vecs = {}
for eid, vecs in by_entity.items():
    entity_vecs[eid] = avg_vec(vecs)

print("Entity vectors computed:")
for eid, vecs in by_entity.items():
    print(f"  {eid_to_name.get(eid,'?'):<30} {len(vecs)} milestone vectors")

# ── Pairwise cosine similarity ────────────────────────────────────────────────
print("\nComputing pairwise cosine similarity...")
eids = list(entity_vecs.keys())
sims = {}
for a in eids:
    scores = []
    for b in eids:
        if a == b:
            continue
        s = cosine(entity_vecs[a], entity_vecs[b])
        scores.append({"name": eid_to_name.get(b, b), "similarity": round(s, 4)})
    scores.sort(key=lambda x: -x["similarity"])
    sims[a] = scores[:5]

# ── Write similar_entities to Supabase ───────────────────────────────────────
print("\nWriting similar_entities to Supabase...")
updated, failed = 0, 0
for eid in eids:
    try:
        sb_patch("entities", f"id=eq.{eid}", {"similar_entities": sims.get(eid, [])})
        updated += 1
        top = sims.get(eid, [])[:3]
        top_str = ", ".join(f"{s['name']} ({s['similarity']:.3f})" for s in top)
        print(f"  ✓ {eid_to_name.get(eid,'?'):<28}  →  {top_str}")
    except Exception as ex:
        print(f"  ✗ {eid_to_name.get(eid,'?')}: {ex}")
        failed += 1

print(f"\n{'✓' if not failed else '!'} Done: {updated} updated, {failed} failed")
if failed:
    print("  → Run 00_migrations.sql in Supabase SQL editor, then retry.")
