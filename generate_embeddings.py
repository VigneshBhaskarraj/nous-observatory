#!/usr/bin/env python3
"""
generate_embeddings.py — Nous Observatory
Populates the embedding vector(1536) column on all milestones using
OpenAI text-embedding-3-small. Re-runnable: only processes NULL rows.

Usage:
    pip install openai requests --break-system-packages
    python3 generate_embeddings.py

Requirements:
    - OPENAI_API_KEY environment variable  OR  edit the OPENAI_KEY constant below
    - Run from any machine that has internet access to Supabase and OpenAI

Cost estimate: ~$0.02 per 256 milestones (text-embedding-3-small at $0.02/1M tokens)
"""

import os
import time
import json
import requests

# ── Config ────────────────────────────────────────────────────────────────────
SB_URL   = "https://yjupiuxuoxmycehkbmwl.supabase.co"
SB_KEY   = "sb_publishable_RUyNAQRYQq37O0IvOJ9kbQ_Cj8V0Yrr"
OPENAI_KEY = os.environ.get("OPENAI_API_KEY", "")   # set env var or paste key here
EMBED_MODEL = "text-embedding-3-small"
BATCH_SIZE  = 100   # OpenAI allows up to 2048 inputs per request; 100 is safe
# ─────────────────────────────────────────────────────────────────────────────

SB_HEADERS = {
    "apikey": SB_KEY,
    "Authorization": f"Bearer {SB_KEY}",
    "Content-Type": "application/json",
}

def fetch_null_milestones():
    """Fetch all milestones where embedding IS NULL."""
    url = f"{SB_URL}/rest/v1/milestones"
    params = {
        "select": "id,event,significance,strategic_signal",
        "embedding": "is.null",
        "order": "date.asc",
    }
    r = requests.get(url, headers=SB_HEADERS, params=params)
    r.raise_for_status()
    return r.json()

def build_text(m):
    """Combine milestone fields into a single string for embedding."""
    parts = [m.get("event") or ""]
    if m.get("significance"):
        parts.append(m["significance"])
    if m.get("strategic_signal"):
        parts.append(m["strategic_signal"])
    return " | ".join(p.strip() for p in parts if p.strip())

def get_embeddings(texts):
    """Call OpenAI embeddings API; returns list of 1536-dim vectors."""
    url = "https://api.openai.com/v1/embeddings"
    headers = {
        "Authorization": f"Bearer {OPENAI_KEY}",
        "Content-Type": "application/json",
    }
    payload = {"model": EMBED_MODEL, "input": texts}
    r = requests.post(url, headers=headers, json=payload)
    r.raise_for_status()
    data = r.json()
    # Return embeddings in original order
    ordered = sorted(data["data"], key=lambda x: x["index"])
    return [item["embedding"] for item in ordered]

def update_embedding(milestone_id, vector):
    """PATCH a single milestone row with its embedding vector."""
    url = f"{SB_URL}/rest/v1/milestones"
    params = {"id": f"eq.{milestone_id}"}
    payload = {"embedding": vector}
    r = requests.patch(url, headers=SB_HEADERS, params=params, json=payload)
    r.raise_for_status()

def main():
    if not OPENAI_KEY:
        print("ERROR: Set OPENAI_API_KEY environment variable before running.")
        print("  export OPENAI_API_KEY='sk-proj-...'")
        return

    print(f"Fetching milestones with NULL embeddings from Supabase...")
    milestones = fetch_null_milestones()
    total = len(milestones)

    if total == 0:
        print("All milestones already have embeddings. Nothing to do.")
        return

    print(f"Found {total} milestones to embed using {EMBED_MODEL}.")
    print(f"Processing in batches of {BATCH_SIZE}...\n")

    success = 0
    errors  = 0

    for batch_start in range(0, total, BATCH_SIZE):
        batch = milestones[batch_start : batch_start + BATCH_SIZE]
        texts = [build_text(m) for m in batch]

        batch_end = min(batch_start + BATCH_SIZE, total)
        print(f"  Embedding rows {batch_start+1}–{batch_end} of {total}...", end=" ", flush=True)

        try:
            vectors = get_embeddings(texts)
        except requests.HTTPError as e:
            print(f"FAILED (OpenAI error: {e})")
            errors += len(batch)
            time.sleep(2)
            continue

        # Write each embedding back to Supabase individually
        for milestone, vector in zip(batch, vectors):
            try:
                update_embedding(milestone["id"], vector)
                success += 1
            except requests.HTTPError as e:
                print(f"\n    ERROR updating {milestone['id']}: {e}")
                errors += 1

        print(f"done ({len(vectors)} vectors written)")
        # Polite rate-limit pause between batches
        if batch_end < total:
            time.sleep(0.5)

    print(f"\n✅ Complete: {success} embeddings written, {errors} errors.")
    print(f"   Total milestones in DB with embeddings: {success} / {total}")

if __name__ == "__main__":
    main()
