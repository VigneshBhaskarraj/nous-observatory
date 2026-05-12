-- ============================================================
-- Nous Observatory — Phase 2 Schema Migration
-- Run this in: https://supabase.com/dashboard/project/yjupiuxuoxmycehkbmwl/sql/54e86d7d-8126-46b2-96cd-3b0067b3d142
-- ============================================================

-- 1. claim_type: how the claim was established
--    demonstrated = shipped product, legal filing, reproducible benchmark
--    announced    = company/official source stated it directly
--    inferred     = derived from signals; analyst estimate, third-party calc
ALTER TABLE milestones
  ADD COLUMN IF NOT EXISTS claim_type TEXT
  CHECK (claim_type IN ('demonstrated', 'announced', 'inferred'));

-- 2. is_contested: independently disputed by credible source
--    orthogonal to claim_type — a 'demonstrated' fact can still be contested
--    defaults false; existing rows untouched
ALTER TABLE milestones
  ADD COLUMN IF NOT EXISTS is_contested BOOLEAN DEFAULT false;

-- 3. displacement_entities: Sunset Map
--    entities or categories this milestone puts in the danger zone
--    optional, text array, queryable via GIN index
ALTER TABLE milestones
  ADD COLUMN IF NOT EXISTS displacement_entities TEXT[];

-- 4. GIN index for fast array queries
--    e.g. "show all milestones that flagged Perplexity as a displacement risk"
CREATE INDEX IF NOT EXISTS milestones_displacement_gin
  ON milestones USING gin(displacement_entities);

-- ============================================================
-- Verify: run this after the migration to confirm all columns exist
-- ============================================================
SELECT
  column_name,
  data_type,
  column_default,
  is_nullable
FROM information_schema.columns
WHERE table_name = 'milestones'
  AND column_name IN ('claim_type', 'is_contested', 'displacement_entities')
ORDER BY column_name;
