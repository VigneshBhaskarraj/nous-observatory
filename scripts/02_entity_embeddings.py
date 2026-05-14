#!/usr/bin/env python3
"""
Script 2: Entity aggregate embeddings + cosine similarity
----------------------------------------------------------
1. Averages all milestone embeddings per entity → entity "strategic DNA" vector
2. Stores in entities.aggregate_embedding (adds column if missing)
3. Computes pairwise cosine similarity matrix
4. Stores top-3 most similar entities per entity in entities.similar_entities (JSON array)

This powers the "Strategically similar to X, Y" feature on entity cards.

Run AFTER 01_enrich_embeddings.py for best results.
Run:  python3 scripts/02_entity_embeddings.py
"""

import json, math, urllib.request

SB_URL = "https://yjupiuxuoxmycehkbmwl.supabase.co"
SB_KEY = "sb_publishable_RUyNAQRYQq37O0IvOJ9kbQ_Cj8V0Yrr"
SB_HDR = {"apikey": SB_KEY, "Authorization": f"Bearer {SB_KEY}",
          "Content-Type": "application/json"}

def sb_get(path, qs=""):
    url = f"{SB_URL}/rest/v1/{path}?{qs}"
    req = urllib.request.Request(url, headers=SB_HDR)
    with urllib.request.urlopen(req) as r:
        return json.loads(r.read())

def sb_patch(path, match_qs, body):
    url = f"{SB_URL}/rest/v1/{path}?{match_qs}"
    data = json.dumps(body).encode()
    hdrs = {**SB_HDR, "Prefer": "return=minimal"}
    req  = urllib.request.Request(url, data=data, headers=hdrs, method="PATCH")
    with urllib.request.urlopen(req) as r:
        return r.status

def cosine(a, b):
    dot  = sum(x*y for x,y in zip(a,b))
    magA = math.sqrt(sum(x*x for x in a))
    magB = math.sqrt(sum(x*x for x in b))
    return dot / (magA * magB) if magA and magB else 0.0

def avg_vec(vecs):
    if not vecs:
        return None
    n = len(vecs[0])
    avg = [sum(v[i] for v in vecs) / len(vecs) for i in range(n)]
    # L2-normalise
    mag = math.sqrt(sum(x*x for x in avg))
    return [x/mag for x in avg] if mag else avg

# ── Fetch milestones WITH embeddings ─────────────────────────────────────────
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

# ── Fetch entities ────────────────────────────────────────────────────────────
entities = sb_get("entities", "select=id,name&order=name&limit=100")
eid_to_name = {e["id"]: e["name"] for e in entities}
print(f"  {len(entities)} entities")

# ── Compute per-entity average embedding ─────────────────────────────────────
entity_vecs = {}   # entity_id → avg embedding
by_entity   = {}
for m in rows:
    eid = m["entity_id"]
    emb = m.get("embedding")
    if not emb:
        continue
    # embedding may be stored as string in some Supabase setups
    if isinstance(emb, str):
        emb = json.loads(emb)
    by_entity.setdefault(eid, []).append(emb)

for eid, vecs in by_entity.items():
    entity_vecs[eid] = avg_vec(vecs)
    print(f"  {eid_to_name.get(eid,'?')} — {len(vecs)} milestone vectors averaged")

# ── Pairwise cosine similarity ────────────────────────────────────────────────
print("\nComputing pairwise similarity...")
eids  = list(entity_vecs.keys())
sims  = {}   # eid → list of (other_name, score) sorted desc
for i, a in enumerate(eids):
    scores = []
    for b in eids:
        if a == b:
            continue
        s = cosine(entity_vecs[a], entity_vecs[b])
        scores.append((eid_to_name.get(b, b), round(s, 4)))
    scores.sort(key=lambda x: -x[1])
    sims[a] = scores[:5]   # top 5 similar entities

# ── Write aggregate embedding + similar_entities back to Supabase ─────────────
print("\nWriting to Supabase entities table...")
updated = 0
for eid, vec in entity_vecs.items():
    payload = {
        "aggregate_embedding": vec,
        "similar_entities": json.dumps([
            {"name": n, "similarity": s} for n, s in sims.get(eid, [])
        ])
    }
    try:
        sb_patch("entities", f"id=eq.{eid}", payload)
        updated += 1
        top = sims.get(eid, [])[:3]
        top_str = ", ".join(f"{n} ({s:.3f})" for n,s in top)
        print(f"  ✓ {eid_to_name.get(eid,'?'):<30} similar: {top_str}")
    except Exception as ex:
        print(f"  ✗ {eid_to_name.get(eid,'?')}: {ex}")

print(f"\n✓ Done: {updated}/{len(entity_vecs)} entity vectors written")
print("\nNote: requires aggregate_embedding (vector) and similar_entities (jsonb)")
print("columns on entities table. Run migration SQL below if they don't exist:")
print("""
  ALTER TABLE entities
    ADD COLUMN IF NOT EXISTS aggregate_embedding vector(1536),
    ADD COLUMN IF NOT EXISTS similar_entities    jsonb;
""")
