import os
#!/usr/bin/env python3
"""
Nous Observatory — Conference Update Insert Script
Generated: 2026-05-18

Conferences covered (April 18 – May 18, 2026):
  - Google Cloud Next '26    (April 22–24, 2026, Las Vegas)
  - LlamaCon                 (April 29, 2026, Meta's inaugural developer conference)
  - Standalone launches:     OpenAI GPT-5.5, Anthropic partnerships & products

Run with:
    python3 conference-update-insert.py
"""

import json
import urllib.request
import urllib.parse
import urllib.error
import sys

# ── Supabase connection ────────────────────────────────────────────────────────
SUPABASE_URL = "https://yjupiuxuoxmycehkbmwl.supabase.co"
_svc_key = os.environ.get("SUPABASE_SECRET_KEY")
if not _svc_key:
    raise RuntimeError("SUPABASE_SECRET_KEY not set — aborting")
ANON_KEY = _svc_key

HEADERS = {
    "apikey": ANON_KEY,
    "Authorization": f"Bearer {ANON_KEY}",
    "Content-Type": "application/json",
    "Prefer": "return=representation",
}

# ── Milestone data ─────────────────────────────────────────────────────────────
# All events confirmed within the April 18 – May 18, 2026 window.
# entity_name is used for lookup only and is NOT inserted.
MILESTONES = [

    # ── Google DeepMind — Google Cloud Next '26 (April 22–24) ─────────────────

    {
        "entity_name": "Google DeepMind",
        "date": "2026-04-22",
        "event": "Gemini Enterprise Agent Platform launched at Google Cloud Next '26 — unified build/scale/govern/optimize layer for agents",
        "significance": "Google consolidated all Vertex AI services under a single agentic platform, signalling that enterprise AI is now agent-first rather than model-first.",
        "strategic_signal": "Every future Google Cloud AI product ships through this platform; competitors must now match Google's integrated agent lifecycle management or cede enterprise share.",
        "ripple_effects": "Forces Microsoft Azure AI Foundry and AWS Bedrock to accelerate similar unified-agent control planes; pushes ISVs to certify on the platform.",
        "sentiment_at_time": "Strongly positive — analysts called it Google's most coherent enterprise AI story to date.",
        "forward_implication_score": 5,
        "stack_layer": "Infrastructure",
        "tags": ["gemini", "agents", "enterprise", "google-cloud-next", "vertex-ai"],
        "thinking_frameworks": None,
        "source_event": "Google Cloud Next '26",
    },
    {
        "entity_name": "Google DeepMind",
        "date": "2026-04-22",
        "event": "8th-generation TPUs unveiled: TPU 8t (3x faster training, 9600-chip superpod) and TPU 8i (80% better inference cost-performance)",
        "significance": "Splitting the TPU line into dedicated training vs. inference chips reflects the shift to inference-era AI workloads; Google now has purpose-built silicon for each workload phase.",
        "strategic_signal": "Google can price inference workloads more aggressively than NVIDIA-dependent rivals; vertically integrated silicon-to-platform stack becomes a durable moat.",
        "ripple_effects": "Pressures hyperscaler peers (AWS Trainium, Azure Maia) to accelerate inference-optimised silicon; reduces Google Cloud's dependence on NVIDIA GPU supply.",
        "sentiment_at_time": "Very positive — benchmark numbers validated a genuine step change over the prior Ironwood generation.",
        "forward_implication_score": 4,
        "stack_layer": "Infrastructure",
        "tags": ["tpu", "hardware", "inference", "training", "silicon", "google-cloud-next"],
        "thinking_frameworks": None,
        "source_event": "Google Cloud Next '26",
    },
    {
        "entity_name": "Google DeepMind",
        "date": "2026-04-22",
        "event": "Gemma 4 open-model family released with native multimodal, MCP support, audio-visual processing, and 140+ language coverage",
        "significance": "Gemma 4 extends Google's open-weight presence into agentic and multilingual territory, positioning it as the enterprise-safe alternative to Meta Llama 4 for regulated industries.",
        "strategic_signal": "MCP native support on day-one means Gemma 4 plugs directly into the emerging agentic tool ecosystem — an advantage over models requiring wrapper layers.",
        "ripple_effects": "Raises the floor for open-weight multimodal models; smaller AI firms may shift from Llama to Gemma for compliance-sensitive deployments.",
        "sentiment_at_time": "Positive — developer community praised the breadth of modalities and native MCP integration.",
        "forward_implication_score": 4,
        "stack_layer": "Research",
        "tags": ["gemma", "open-weights", "multimodal", "mcp", "multilingual", "google-cloud-next"],
        "thinking_frameworks": None,
        "source_event": "Google Cloud Next '26",
    },

    # ── Meta AI — LlamaCon (April 29) ─────────────────────────────────────────

    {
        "entity_name": "Meta AI",
        "date": "2026-04-29",
        "event": "Llama API launched in limited preview — Meta's first hosted model API combining open-source flexibility with managed cloud convenience",
        "significance": "Meta crossed from pure open-source contributor to model API provider, directly competing with OpenAI and Anthropic APIs while keeping downloadable weights available.",
        "strategic_signal": "Meta can now capture API revenue from developers who prefer Llama but want a managed endpoint; a monetisation path beyond advertising is finally operational.",
        "ripple_effects": "Existing Llama inference providers (Groq, Together AI, Fireworks) face direct competition from the model creator; may trigger price pressure on Llama-based API calls.",
        "sentiment_at_time": "Very positive among developers — seen as a long-overdue move that reduces friction for production adoption.",
        "forward_implication_score": 4,
        "stack_layer": "Developer Tools",
        "tags": ["llama", "api", "meta", "llamacon", "open-source", "developer-tools"],
        "thinking_frameworks": None,
        "source_event": "LlamaCon 2026",
    },
    {
        "entity_name": "Meta AI",
        "date": "2026-04-29",
        "event": "LlamaFirewall, Llama Guard 4, and Llama Prompt Guard 2 released as open-source enterprise safety stack at LlamaCon",
        "significance": "Meta shipped a full enterprise safety suite alongside the Llama API, addressing the primary blocker for regulated industries adopting open-weight models.",
        "strategic_signal": "Safety tooling as open-source infrastructure commoditises safety layers for the industry while positioning Meta as a responsible open-source steward ahead of AI regulation.",
        "ripple_effects": "Raises enterprise buyer expectations for bundled safety tooling from all model providers; smaller safety-tooling startups face pressure from free alternatives.",
        "sentiment_at_time": "Positive — enterprise architects appreciated production-ready safety primitives shipping alongside the model API.",
        "forward_implication_score": 3,
        "stack_layer": "Infrastructure",
        "tags": ["llama", "safety", "llamafirewall", "enterprise", "llamacon", "open-source"],
        "thinking_frameworks": None,
        "source_event": "LlamaCon 2026",
    },

    # ── OpenAI — GPT-5.5 (April 23) + GPT-5.5 Instant (May 5) ───────────────

    {
        "entity_name": "OpenAI",
        "date": "2026-04-23",
        "event": "GPT-5.5 released with 82.7% Terminal-Bench 2.0 and 58.6% SWE-Bench Pro scores — new state-of-the-art in agentic coding",
        "significance": "GPT-5.5 set new benchmarks for autonomous coding and multi-tool agentic workflows, widening OpenAI's lead in the developer segment and approaching human-expert-level software engineering.",
        "strategic_signal": "At 82.7% Terminal-Bench 2.0, GPT-5.5 approaches the threshold where autonomous software engineering becomes reliable enough for unsupervised production use.",
        "ripple_effects": "Forces Anthropic and Google to accelerate agentic coding benchmarks; boosts OpenAI Codex adoption; raises valuations of AI-native software engineering startups.",
        "sentiment_at_time": "Strongly positive — benchmark numbers independently verified; developer enthusiasm exceptionally high.",
        "forward_implication_score": 5,
        "stack_layer": "Application",
        "tags": ["gpt-5.5", "agentic-coding", "openai", "frontier-model", "swe-bench", "computer-use"],
        "thinking_frameworks": None,
        "source_event": "OpenAI product launch April 2026",
    },
    {
        "entity_name": "OpenAI",
        "date": "2026-05-05",
        "event": "GPT-5.5 Instant deployed as default ChatGPT model with cross-conversation memory, Gmail and file context integration",
        "significance": "Rolling the frontier model to all ChatGPT users as the default is the fastest frontier-capability mass distribution in AI history, reaching hundreds of millions of users immediately.",
        "strategic_signal": "Memory + Gmail integration turns ChatGPT from a session tool into a persistent personal AI — raising switching costs and deepening the moat against Google Gemini and Microsoft Copilot.",
        "ripple_effects": "Google and Microsoft must accelerate personal context features; EU privacy regulators may scrutinise Gmail data integration; raises ChatGPT retention metrics.",
        "sentiment_at_time": "Mixed — developers and power users excited; privacy advocates raised Gmail access concerns.",
        "forward_implication_score": 3,
        "stack_layer": "Application",
        "tags": ["gpt-5.5", "chatgpt", "memory", "personalization", "openai", "default-model"],
        "thinking_frameworks": None,
        "source_event": "OpenAI product launch May 2026",
    },
    {
        "entity_name": "OpenAI",
        "date": "2026-05-07",
        "event": "Advanced voice AI models added to OpenAI API with real-time reasoning, multilingual translation, and transcription capabilities",
        "significance": "Moving voice from a consumer feature to a developer API primitive unlocks a new layer of voice-native application development on top of OpenAI infrastructure.",
        "strategic_signal": "OpenAI is completing a full multimodal API surface (text, image, code, voice); voice is the last major modality to go API-first, giving OpenAI a head start in voice-native app infrastructure.",
        "ripple_effects": "Puts pressure on ElevenLabs, Deepgram, and Whisper-wrapper startups; enables a new wave of voice-AI apps; could reshape call-centre and accessibility software markets.",
        "sentiment_at_time": "Positive — developers had been requesting voice API parity for over a year.",
        "forward_implication_score": 3,
        "stack_layer": "Developer Tools",
        "tags": ["voice", "api", "multimodal", "openai", "speech", "realtime"],
        "thinking_frameworks": None,
        "source_event": "OpenAI product launch May 2026",
    },

    # ── Anthropic — May 2026 launches ─────────────────────────────────────────

    {
        "entity_name": "Anthropic",
        "date": "2026-05-13",
        "event": "Claude for Small Business launched with pre-built connectors for QuickBooks, PayPal, HubSpot, Canva, DocuSign, Google Workspace, Microsoft 365",
        "significance": "Anthropic moved down-market with a bundled SMB offering targeting the vast small-business segment that lacks IT resources to deploy AI, diversifying beyond enterprise and developer focus.",
        "strategic_signal": "Anthropic is broadening from safety-research and enterprise-premium positioning into mainstream SMB, directly competing with Microsoft Copilot for Business and Google Workspace AI.",
        "ripple_effects": "SMB software vendors (QuickBooks, HubSpot) gain AI credibility through association; Microsoft and Google must accelerate pre-built connector depth to protect SMB relationships.",
        "sentiment_at_time": "Positive — market saw it as strategic maturation beyond the dev/enterprise niche.",
        "forward_implication_score": 3,
        "stack_layer": "Application",
        "tags": ["anthropic", "smb", "connectors", "claude", "small-business", "product"],
        "thinking_frameworks": None,
        "source_event": "Anthropic product launch May 2026",
    },
    {
        "entity_name": "Anthropic",
        "date": "2026-05-13",
        "event": "Anthropic and Gates Foundation announce $200M AI partnership for global health and education impact",
        "significance": "Largest philanthropic-AI partnership to date; signals Anthropic's commitment to safety-conscious deployment in high-stakes humanitarian domains.",
        "strategic_signal": "Positions Anthropic as the preferred AI partner for mission-driven institutions; builds reputational capital ahead of regulatory scrutiny that will favour safety-forward labs.",
        "ripple_effects": "Creates pressure on OpenAI and Google to announce comparable philanthropic commitments; opens doors for Anthropic in government and NGO sectors globally.",
        "sentiment_at_time": "Strongly positive — praised by policy community and global health sector.",
        "forward_implication_score": 4,
        "stack_layer": "Application",
        "tags": ["anthropic", "gates-foundation", "partnership", "global-health", "education", "impact"],
        "thinking_frameworks": None,
        "source_event": "Anthropic partnership announcement May 2026",
    },
    {
        "entity_name": "Anthropic",
        "date": "2026-05-14",
        "event": "PwC deploying Claude enterprise-wide to build technology, execute deals, and reinvent enterprise functions for global clients",
        "significance": "A Big Four firm deploying Claude at scale (300K+ employees) is one of the largest Claude enterprise rollouts and validates Anthropic's enterprise reliability narrative.",
        "strategic_signal": "Professional services firms are the adoption multipliers for enterprise AI — PwC's public commitment accelerates Claude adoption across PwC's entire client base worldwide.",
        "ripple_effects": "Other Big Four firms (Deloitte, EY, KPMG) face client pressure to announce comparable AI partnerships; accelerates AI adoption in traditional consulting engagements.",
        "sentiment_at_time": "Positive — market viewed it as a significant enterprise trust and scale signal.",
        "forward_implication_score": 3,
        "stack_layer": "Application",
        "tags": ["anthropic", "pwc", "enterprise", "professional-services", "deployment", "claude"],
        "thinking_frameworks": None,
        "source_event": "Anthropic enterprise partnership May 2026",
    },
]


# ── Supabase helpers ───────────────────────────────────────────────────────────

def supabase_get(path: str, params: dict = None) -> list:
    url = f"{SUPABASE_URL}/rest/v1/{path}"
    if params:
        url = f"{url}?{urllib.parse.urlencode(params)}"
    req = urllib.request.Request(url, headers=HEADERS, method="GET")
    try:
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        body = e.read().decode()
        print(f"  [ERROR] GET {path} -> HTTP {e.code}: {body}", file=sys.stderr)
        raise


def supabase_post(path: str, payload: list) -> list:
    url = f"{SUPABASE_URL}/rest/v1/{path}"
    data = json.dumps(payload).encode()
    req = urllib.request.Request(url, data=data, headers=HEADERS, method="POST")
    try:
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        body = e.read().decode()
        print(f"  [ERROR] POST {path} -> HTTP {e.code}: {body}", file=sys.stderr)
        raise


# ── Entity ID cache ────────────────────────────────────────────────────────────

_entity_cache = {}


def get_entity_id(name: str):
    if name in _entity_cache:
        return _entity_cache[name]
    rows = supabase_get("entities", {"name": f"eq.{name}", "select": "id"})
    if not rows:
        print(f"  [WARN] Entity not found in DB: '{name}'")
        return None
    entity_id = rows[0]["id"]
    _entity_cache[name] = entity_id
    return entity_id


# ── Duplicate check ────────────────────────────────────────────────────────────

def fetch_existing_events(entity_id: str) -> list:
    rows = supabase_get(
        "milestones",
        {"entity_id": f"eq.{entity_id}", "select": "event"},
    )
    return [r["event"].lower() for r in rows]


def is_duplicate(new_event: str, existing_events: list) -> bool:
    needle = new_event.lower()
    return any(needle in existing or existing in needle for existing in existing_events)


# ── Main ───────────────────────────────────────────────────────────────────────

def main():
    print("=" * 65)
    print("Nous Observatory - Conference Update Insert")
    print("Window : April 18 - May 18, 2026")
    print("Sources: Google Cloud Next '26 | LlamaCon 2026")
    print("         + OpenAI / Anthropic standalone launches")
    print("=" * 65)

    # Group milestones by entity
    by_entity = {}
    for m in MILESTONES:
        by_entity.setdefault(m["entity_name"], []).append(m)

    total_inserted = 0
    total_skipped = 0

    for entity_name, records in by_entity.items():
        print(f"\n>> {entity_name} ({len(records)} milestone(s) to check)")

        entity_id = get_entity_id(entity_name)
        if entity_id is None:
            print(f"   Skipping - entity not found in database.")
            total_skipped += len(records)
            continue

        existing = fetch_existing_events(entity_id)
        print(f"   Found {len(existing)} existing milestone(s) in DB.")

        to_insert = []
        for m in records:
            if is_duplicate(m["event"], existing):
                print(f"   [SKIP duplicate] {m['event'][:75]}...")
                total_skipped += 1
            else:
                row = {k: v for k, v in m.items() if k != "entity_name"}
                row["entity_id"] = entity_id
                to_insert.append(row)

        if not to_insert:
            print("   Nothing new to insert for this entity.")
            continue

        print(f"   Inserting {len(to_insert)} new milestone(s)...")
        inserted = supabase_post("milestones", to_insert)
        total_inserted += len(inserted)
        for row in inserted:
            print(f"   [OK] {str(row.get('event', ''))[:75]}")

    print("\n" + "=" * 65)
    print(f"  Inserted : {total_inserted}")
    print(f"  Skipped  : {total_skipped} (duplicates or missing entity)")
    print("=" * 65)


if __name__ == "__main__":
    main()
