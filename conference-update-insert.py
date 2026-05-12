"""
Nous Observatory — Conference Update Insert Script
Run: python3 conference-update-insert.py
Date generated: 2026-05-10
Source: Google Cloud Next 2026 (Apr 22-24) + Anthropic April 2026 releases

This script:
1. Looks up entity_ids for Anthropic and Google DeepMind
2. Checks existing milestones to skip duplicates
3. Inserts new milestones
"""

import json
import sys
import urllib.request
import urllib.parse
import urllib.error

SUPABASE_URL = "https://yjupiuxuoxmycehkbmwl.supabase.co"
API_KEY = "sb_publishable_RUyNAQRYQq37O0IvOJ9kbQ_Cj8V0Yrr"

BASE_HEADERS = {
    "apikey": API_KEY,
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json",
}


def _request(method, url, params=None, body=None, extra_headers=None):
    """Minimal HTTP helper using stdlib urllib."""
    if params:
        url = url + "?" + urllib.parse.urlencode(params)
    data = json.dumps(body).encode() if body is not None else None
    headers = {**BASE_HEADERS, **(extra_headers or {})}
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            raw = resp.read()
            return resp.status, json.loads(raw) if raw else None
    except urllib.error.HTTPError as e:
        body_text = e.read().decode()
        raise RuntimeError(f"HTTP {e.code} from {url}: {body_text}") from e

# ─────────────────────────────────────────────
# Milestone data (entity_id filled in at runtime)
# ─────────────────────────────────────────────

MILESTONES_TEMPLATE = [
    {
        "entity_name": "Anthropic",
        "date": "2026-04-16",
        "event": "Claude Opus 4.7 released with benchmark-leading coding and 3x vision capacity",
        "significance": "Major capability upgrade over Opus 4.6 with notable gains in advanced software engineering. Image resolution tripled to 3.75 megapixels. Available simultaneously on Anthropic API, Amazon Bedrock, Google Cloud Vertex AI, and Microsoft Foundry.",
        "strategic_signal": "Steady, incremental model iteration cadence at unchanged pricing ($5/$25/MTok) signals Anthropic's confidence in its enterprise positioning. Multi-cloud simultaneous availability cements Anthropic as a platform-agnostic provider rather than a single-cloud play—increasing stickiness across all major hyperscaler ecosystems.",
        "ripple_effects": "Intensifies competition with Gemini 3.1 Pro (released same week) in enterprise coding market. Multi-cloud availability reduces vendor lock-in risk for enterprise customers and expands TAM. OpenAI forced to respond with coding-focused model updates.",
        "sentiment_at_time": "positive",
        "forward_implication_score": 4,
        "stack_layer": "Model",
        "tags": ["model-release", "coding", "vision", "claude", "enterprise", "multi-cloud"],
        "thinking_frameworks": None,
        "source_event": "Anthropic April 2026 Release",
    },
    {
        "entity_name": "Anthropic",
        "date": "2026-04-07",
        "event": "Anthropic unveils Mythos model with step-change cybersecurity capability via Project Glasswing",
        "significance": "Mythos discovered 271 zero-day vulnerabilities in Firefox and developed working exploits for 181. Described by Anthropic as 'the most capable model we've built.' Released only to vetted defenders (Amazon, Apple, Cisco, CrowdStrike, Microsoft, Palo Alto) under Project Glasswing.",
        "strategic_signal": "Mythos demonstrates that AI has crossed into genuinely new territory for offensive and defensive security. Anthropic's controlled-release strategy represents Responsible Scaling Policy in action at the frontier. This is a major moment for AI safety credibility but also signals the industry is entering an era where AI capabilities pose systemic risk.",
        "ripple_effects": "Triggered OpenAI to release GPT-5.5 Cyber (May 7) for vetted security teams. Sparked regulatory scrutiny and cybersecurity 'hysteria' in banking sector. CEO warned of 'moment of danger' May 5. Unauthorized access incident April 21 raised supply-chain security concerns.",
        "sentiment_at_time": "mixed",
        "forward_implication_score": 5,
        "stack_layer": "Model",
        "tags": ["safety", "cybersecurity", "frontier-model", "responsible-scaling", "mythos", "zero-day", "project-glasswing"],
        "thinking_frameworks": None,
        "source_event": "Anthropic Mythos Preview April 2026",
    },
    {
        "entity_name": "Google DeepMind",
        "date": "2026-04-22",
        "event": "Google rebrands Vertex AI as Gemini Enterprise Agent Platform; absorbs Agentspace into unified product",
        "significance": "Full vertical integration play from custom silicon to end-user inbox. Vertex AI rebranded as Gemini Enterprise Agent Platform with no-code Workspace Studio, 200+ model garden (including Anthropic Claude), persistent memory agents, ADK v1.0, and partner agents from Salesforce, Workday, Box, ServiceNow.",
        "strategic_signal": "Google is making an explicit bet that vertical integration wins the enterprise agentic era. By owning silicon (TPUs), frontier model (Gemini), cloud platform, and distribution (3B+ Workspace users), Google can offer price/performance and seamless integration that assembled-stack competitors cannot match.",
        "ripple_effects": "Forces Microsoft to respond with tighter Copilot/Azure integration. Accelerates enterprise agentic adoption at Google Workspace's 3B+ user base. 200+ model garden creates a multi-model marketplace normalizing Claude and Llama as cloud-native choices.",
        "sentiment_at_time": "bullish",
        "forward_implication_score": 5,
        "stack_layer": "Application",
        "tags": ["agent-platform", "enterprise", "vertex-ai", "gemini", "no-code", "workspace", "vertical-integration", "cloud-next"],
        "thinking_frameworks": None,
        "source_event": "Google Cloud Next 2026",
    },
    {
        "entity_name": "Google DeepMind",
        "date": "2026-04-22",
        "event": "A2A Protocol v1.2 reaches 150 organizations in production under Linux Foundation governance",
        "significance": "Agent-to-Agent protocol routing real tasks in production at Microsoft, AWS, Salesforce, SAP, ServiceNow. Under Linux Foundation Agentic AI Foundation governance. Cryptographically signed agent cards. Native support in LangGraph, CrewAI, LlamaIndex, Semantic Kernel, AutoGen, and Google ADK.",
        "strategic_signal": "Google is establishing the inter-agent communication standard layer—complementary to Anthropic's MCP (agent-to-tool). The combination creates a de facto two-protocol stack for the agentic internet. Whoever defines the protocol layer controls the network effects in multi-agent orchestration.",
        "ripple_effects": "Creates protocol duopoly with Anthropic's MCP. Dramatically lowers multi-vendor agent integration complexity for enterprises. Establishes Linux Foundation as governance home for agentic AI standards.",
        "sentiment_at_time": "very positive",
        "forward_implication_score": 5,
        "stack_layer": "Infrastructure",
        "tags": ["a2a", "protocol", "interoperability", "multi-agent", "linux-foundation", "standards", "mcp"],
        "thinking_frameworks": None,
        "source_event": "Google Cloud Next 2026",
    },
    {
        "entity_name": "Google DeepMind",
        "date": "2026-04-22",
        "event": "8th-gen TPUs announced: TPU 8t (3x training, 121 exaFLOPS) and TPU 8i (80% better inference $/perf)",
        "significance": "Google bifurcated AI silicon into two specialized chips: TPU 8t for training (9,600-chip superpod at 121 exaFLOPS, 2.8x price/perf vs prior gen) and TPU 8i for inference (1,152-chip pod, 3x on-chip SRAM, 288GB HBM, 80% better inference cost).",
        "strategic_signal": "Specialization of silicon for training vs. inference signals maturation of AI infrastructure from general-purpose to workload-optimized. Google's vertical silicon ownership enables aggressive inference pricing that cloud providers buying NVIDIA GPUs at retail cannot match.",
        "ripple_effects": "Accelerates competitive pressure on NVIDIA; signals end of general-purpose GPU dominance for AI inference. Google can pass infrastructure cost savings to enterprise customers as inference pricing drops.",
        "sentiment_at_time": "positive",
        "forward_implication_score": 4,
        "stack_layer": "Infrastructure",
        "tags": ["tpu", "hardware", "inference", "training", "custom-silicon", "ai-infrastructure", "nvidia-competition"],
        "thinking_frameworks": None,
        "source_event": "Google Cloud Next 2026",
    },
    {
        "entity_name": "Google DeepMind",
        "date": "2026-04-22",
        "event": "Gemini 3.1 Pro launches in preview: 1M token context, MEDIUM thinking mode, agentic reasoning gains",
        "significance": "Most advanced Gemini reasoning model in preview on Vertex AI. New MEDIUM thinking_level parameter enables cost-performance tradeoffs. Improved software engineering and finance domain performance. Alongside Gemini 3.1 Flash Image and Lyria 3 for audio in unified model family.",
        "strategic_signal": "Gemini 3.1 Pro directly competes with Claude Opus 4.7 (released April 16) in enterprise reasoning. Simultaneous release with Enterprise Agent Platform creates a vertically locked story: model + platform + compute all from Google.",
        "ripple_effects": "Creates price competition with Claude Opus 4.7. MEDIUM thinking_level parameter signals cost-optimized reasoning as a differentiator. Gemini 3.2 signals aggressive 2026 release cadence to maintain parity at the frontier.",
        "sentiment_at_time": "positive",
        "forward_implication_score": 4,
        "stack_layer": "Model",
        "tags": ["gemini", "frontier-model", "reasoning", "agentic", "long-context", "thinking"],
        "thinking_frameworks": None,
        "source_event": "Google Cloud Next 2026",
    },
]


def get_entity_id(entity_name):
    """Look up entity_id by name."""
    status, data = _request(
        "GET",
        f"{SUPABASE_URL}/rest/v1/entities",
        params={"name": f"eq.{entity_name}", "select": "id,name"},
    )
    if not data:
        print(f"  ⚠ Entity not found: {entity_name}")
        return None
    return data[0]["id"]


def get_existing_milestones(entity_id):
    """Return set of (date, first 60 chars of event) for dedup check."""
    status, data = _request(
        "GET",
        f"{SUPABASE_URL}/rest/v1/milestones",
        params={"entity_id": f"eq.{entity_id}", "select": "date,event"},
    )
    return {(m["date"], m["event"][:60]) for m in (data or [])}


def insert_milestones(milestones):
    """Batch insert milestones (normalized keys)."""
    status, _ = _request(
        "POST",
        f"{SUPABASE_URL}/rest/v1/milestones",
        body=milestones,
        extra_headers={"Prefer": "return=minimal"},
    )
    return status


def main():
    print("=== Nous Observatory — Conference Update Insert ===")
    print(f"Window: 2026-04-10 to 2026-05-10\n")

    # Resolve entity IDs
    entity_ids = {}
    for name in ["Anthropic", "Google DeepMind"]:
        print(f"Looking up entity: {name}")
        eid = get_entity_id(name)
        if eid:
            entity_ids[name] = eid
            print(f"  ✓ Found: {eid}")
        else:
            print(f"  ✗ Not found — skipping milestones for {name}")

    inserted = 0
    skipped = 0

    for entity_name, entity_id in entity_ids.items():
        print(f"\nProcessing milestones for {entity_name} ({entity_id})")
        existing = get_existing_milestones(entity_id)
        print(f"  Existing milestone count: {len(existing)}")

        to_insert = []
        for m in MILESTONES_TEMPLATE:
            if m["entity_name"] != entity_name:
                continue
            key = (m["date"], m["event"][:60])
            if key in existing:
                print(f"  SKIP (duplicate): {m['date']} — {m['event'][:60]}")
                skipped += 1
            else:
                # Build normalized insert record
                record = {
                    "entity_id": entity_id,
                    "date": m["date"],
                    "event": m["event"],
                    "significance": m["significance"],
                    "strategic_signal": m["strategic_signal"],
                    "ripple_effects": m["ripple_effects"],
                    "sentiment_at_time": m["sentiment_at_time"],
                    "forward_implication_score": m["forward_implication_score"],
                    "stack_layer": m["stack_layer"],
                    "tags": m["tags"],
                    "thinking_frameworks": m["thinking_frameworks"],
                    "source_event": m["source_event"],
                }
                to_insert.append(record)
                print(f"  QUEUE: {m['date']} — {m['event'][:60]}")

        if to_insert:
            status = insert_milestones(to_insert)
            print(f"  ✓ Inserted {len(to_insert)} milestones (HTTP {status})")
            inserted += len(to_insert)

    print(f"\n=== Summary ===")
    print(f"  Inserted: {inserted}")
    print(f"  Skipped (duplicates): {skipped}")
    print("Done.")


if __name__ == "__main__":
    main()
