#!/usr/bin/env python3
"""
Script 1: Re-embed milestones using richer text
------------------------------------------------
Current embeddings use only the 'event' field.
This re-embeds using: event + significance + strategic_signal
giving the vector full analytical context.

Run:  python3 scripts/01_enrich_embeddings.py
Cost: ~$0.02-0.05 for ~400 milestones at text-embedding-3-small pricing
"""

import json, time, urllib.request, urllib.parse, sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from _config import SB_URL, SB_KEY, get_openai_key
OAI_KEY = get_openai_key()

SB_HDR  = {"apikey": SB_KEY, "Authorization": f"Bearer {SB_KEY}",
           "Content-Type": "application/json"}
OAI_HDR = {"Authorization": f"Bearer {OAI_KEY}",
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

def embed_batch(texts):
    """Embed a batch of texts, return list of vectors."""
    payload = json.dumps({"model": "text-embedding-3-small", "input": texts}).encode()
    req = urllib.request.Request(
        "https://api.openai.com/v1/embeddings",
        data=payload, headers=OAI_HDR
    )
    with urllib.request.urlopen(req) as r:
        data = json.loads(r.read())
    return [d["embedding"] for d in sorted(data["data"], key=lambda x: x["index"])]

# ── Fetch all milestones ──────────────────────────────────────────────────────
print("Fetching milestones...")
rows, offset, page = [], 0, 500
while True:
    batch = sb_get("milestones",
        f"select=id,event,significance,strategic_signal"
        f"&order=id&limit={page}&offset={offset}")
    rows.extend(batch)
    if len(batch) < page:
        break
    offset += page
print(f"  {len(rows)} milestones loaded")

# ── Build enriched text per milestone ────────────────────────────────────────
def make_text(m):
    parts = [m.get("event") or ""]
    if m.get("significance"):
        parts.append(m["significance"])
    if m.get("strategic_signal"):
        parts.append(m["strategic_signal"])
    return " | ".join(p.strip() for p in parts if p.strip())

texts = [make_text(m) for m in rows]

# ── Embed in batches of 100 ───────────────────────────────────────────────────
print("Embedding in batches of 100...")
BATCH = 100
all_vectors = []
for i in range(0, len(texts), BATCH):
    batch_texts = texts[i:i+BATCH]
    vecs = embed_batch(batch_texts)
    all_vectors.extend(vecs)
    print(f"  Embedded {min(i+BATCH, len(texts))}/{len(texts)}")
    time.sleep(0.3)

# ── Write back to Supabase ────────────────────────────────────────────────────
print("Writing vectors back to Supabase...")
updated, skipped = 0, 0
for m, vec in zip(rows, all_vectors):
    try:
        sb_patch("milestones", f"id=eq.{m['id']}", {"embedding": vec})
        updated += 1
    except Exception as e:
        print(f"  SKIP {m['id']}: {e}")
        skipped += 1
    if updated % 50 == 0 and updated:
        print(f"  {updated} updated...")

print(f"\n✓ Done: {updated} updated, {skipped} skipped")
print("Milestones now embedded with event + significance + strategic_signal context.")
