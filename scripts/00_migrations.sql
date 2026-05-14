-- Nous Observatory — one-time schema additions
-- Run this ONCE in your Supabase SQL editor (https://supabase.com/dashboard → SQL editor)
-- Safe to re-run (uses IF NOT EXISTS)

-- 1. Entity similarity (written by 02_entity_embeddings.py)
ALTER TABLE entities
  ADD COLUMN IF NOT EXISTS similar_entities jsonb;

COMMENT ON COLUMN entities.similar_entities IS
  'Top-5 strategically similar entities by milestone embedding cosine similarity. Array of {name, similarity}.';

-- 2. Evidence quality (written by 03_evidence_quality.py)
ALTER TABLE milestones
  ADD COLUMN IF NOT EXISTS evidence_quality INTEGER DEFAULT 2
  CHECK (evidence_quality BETWEEN 1 AND 3);

COMMENT ON COLUMN milestones.evidence_quality IS
  '3=Confirmed (demonstrated), 2=Reported/Announced, 1=Speculative/Inferred';
