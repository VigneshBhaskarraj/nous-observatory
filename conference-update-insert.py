"""
Nous Observatory — Conference Update Insert Script
Run: python3 conference-update-insert.py
Date generated: 2026-05-17
Sources:
  - Google Cloud Next 2026 (Apr 22-24): cloud.google.com/transform/google-io-2025-the-top-updates-from-google-cloud-ai
  - Anthropic April 2026: anthropic.com/news (Opus 4.7, Project Glasswing/Mythos)
  - OpenAI May 2026: openai.com/index/gpt-5-5-instant, openai.com/index/gpt-5-5-with-trusted-access-for-cyber
  - Anthropic May 2026: claude.com/blog/new-in-claude-managed-agents, anthropic.com/news/claude-for-small-business

This script:
1. Looks up entity_ids for Anthropic, Google DeepMind, and OpenAI
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
    # ── OpenAI May 2026 ────────────────────────────────────────────────────────
    # Source: openai.com/index/gpt-5-5-instant/ · techcrunch.com/2026/05/05/openai-releases-gpt-5-5-instant-a-new-default-model-for-chatgpt/
    {
        "entity_name": "OpenAI",
        "date": "2026-05-05",
        "event": "GPT-5.5 Instant replaces GPT-5.3 as default ChatGPT model with 52.5% fewer hallucinations",
        "significance": "New default model for all ChatGPT users. Internal evals show 52.5% fewer hallucinated claims vs GPT-5.3 on high-stakes prompts (medicine, law, finance). Responses are 30.2% more concise. Real-time self-correction: the model can identify mid-stream logic errors and fix them before output completes. Enhanced personalization draws on past conversations, uploaded files, and connected Gmail.",
        "strategic_signal": "OpenAI's focus on hallucination reduction and conciseness directly addresses the two most-cited enterprise adoption blockers. The rapid cadence (5.1 → 5.3 → 5.5 Instant in months) signals a shift from capability leaps to continuous reliability refinement — a maturation that favors OpenAI's incumbent ChatGPT distribution over challenger models.",
        "ripple_effects": "Raises baseline hallucination-rate expectations across all AI providers. Forces Anthropic and Google to publish comparable accuracy metrics. Gmail integration sets cross-app memory as a consumer battleground. GPT-5.3 Instant retired in 90 days, creating upgrade pressure for API users.",
        "sentiment_at_time": "positive",
        "forward_implication_score": 4,
        "stack_layer": "Model",
        "tags": ["model-release", "frontier-model", "hallucination-reduction", "personalization", "chatgpt"],
        "thinking_frameworks": None,
        "source_event": "OpenAI May 2026",
    },
    # Source: openai.com/index/gpt-5-5-with-trusted-access-for-cyber/ · cnbc.com/2026/05/07/openai-rolls-out-new-gpt-5point5-cyber-to-vetted-cybersecurity-teams.html
    {
        "entity_name": "OpenAI",
        "date": "2026-05-07",
        "event": "GPT-5.5-Cyber launched via Trusted Access for Cyber program for critical infrastructure defenders",
        "significance": "Specialized cybersecurity model released to vetted defenders securing critical infrastructure. Lower classifier refusals for authorized dual-use workflows: vulnerability identification, malware analysis, binary reverse engineering, detection engineering, and patch validation. UK AI Security Institute benchmark places GPT-5.5 at near-parity with Anthropic Mythos on its 95-task cyber evaluation.",
        "strategic_signal": "OpenAI's direct response to Anthropic's Project Glasswing/Mythos (Apr 7). The tiered Trusted Access model — GPT-5.5 Cyber for vetted defenders, GPT-5.5 Instant for consumers — is OpenAI's framework for managing dual-use risk while still capturing the lucrative enterprise security market. UK AISI near-parity benchmark neutralizes Anthropic's first-mover claim in AI-assisted security.",
        "ripple_effects": "Intensifies security-AI arms race: two frontier labs now targeting the same vetted-defender user base. UK AISI benchmark becomes the industry standard both must respond to. Enterprise security vendors (CrowdStrike, Palo Alto, Cisco) must build integrations or risk disintermediation by direct model access.",
        "sentiment_at_time": "mixed",
        "forward_implication_score": 4,
        "stack_layer": "Model",
        "tags": ["cybersecurity", "model-release", "frontier-model", "safety", "dual-use"],
        "thinking_frameworks": None,
        "source_event": "OpenAI May 2026",
    },
    # ── Anthropic May 2026 ────────────────────────────────────────────────────
    # Source: claude.com/blog/new-in-claude-managed-agents · venturebeat.com/technology/anthropic-introduces-dreaming
    {
        "entity_name": "Anthropic",
        "date": "2026-05-06",
        "event": "Claude Managed Agents adds dreaming (self-improving memory), outcomes rubric evaluation, and multiagent orchestration",
        "significance": "Dreaming is a scheduled offline process that reviews past agent sessions, extracts patterns, curates memories so agents self-improve over time — analogous to sleep-stage memory consolidation in neuroscience. Outcomes lets developers write success rubrics; a separate grader evaluates results in its own context. Multiagent orchestration lets a lead agent break large tasks and delegate to parallel specialists with separate models, prompts, and tools on a shared filesystem. Harvey (legal AI) saw task completion climb ~6x in the pilot.",
        "strategic_signal": "Dreaming is architecturally novel: Managed Agents become more capable the longer they run, creating compounding switching costs that make rip-and-replace extremely painful. Combined with multiagent orchestration, Anthropic is positioning its Agents as the enterprise runtime that learns your workflow — a fundamentally different value proposition than stateless API calls.",
        "ripple_effects": "Forces OpenAI Agents SDK and Google ADK to ship persistent learning. Sets Harvey's 6x improvement as the benchmark enterprises will demand. 'Self-improving agent' becomes a distinct product category requiring its own evaluation methodology.",
        "sentiment_at_time": "very positive",
        "forward_implication_score": 5,
        "stack_layer": "Application",
        "tags": ["agent-platform", "enterprise", "memory", "multiagent", "dreaming", "claude"],
        "thinking_frameworks": None,
        "source_event": "Anthropic May 2026 Release",
    },
    # Source: anthropic.com/news/claude-for-small-business
    {
        "entity_name": "Anthropic",
        "date": "2026-05-13",
        "event": "Claude for Small Business launches with toggle-install connectors for QuickBooks, HubSpot, PayPal, Google Workspace, and Microsoft 365",
        "significance": "No-API product that embeds Claude directly into the tools small businesses already use: Intuit QuickBooks, PayPal, HubSpot, Canva, DocuSign, Google Workspace, and Microsoft 365. Single-toggle install. First Anthropic product explicitly targeting non-technical users and the SMB segment, where ChatGPT and Microsoft Copilot currently dominate.",
        "strategic_signal": "After dominating enterprise/developer mindshare, Anthropic opens a second front in SMB via connector-first distribution. This contrasts with OpenAI's ChatGPT-centric strategy and Google's Workspace-first approach — Anthropic meets customers in their existing tools rather than asking them to switch interfaces.",
        "ripple_effects": "Direct competition with Microsoft Copilot and ChatGPT Plus in SMB. Forces Zapier/Make to prioritize Claude connectors. QuickBooks and HubSpot partnerships signal Anthropic is ready to revenue-share for distribution — a business model shift from pure API licensing.",
        "sentiment_at_time": "positive",
        "forward_implication_score": 3,
        "stack_layer": "Application",
        "tags": ["enterprise", "no-code", "connectors", "smb", "claude", "application"],
        "thinking_frameworks": None,
        "source_event": "Anthropic May 2026 Release",
    },
    # Source: anthropic.com/news/pwc-expanded-partnership · anthropic.com/news (Gates Foundation)
    {
        "entity_name": "Anthropic",
        "date": "2026-05-14",
        "event": "PwC deploys Claude Code and Cowork globally; Anthropic announces $200M Gates Foundation AI partnership",
        "significance": "PwC rolling out Claude Code and Cowork across its global workforce, launching a new Office of the CFO business unit built on Anthropic technology. Simultaneously, $200M Gates Foundation partnership targets AI-powered health and education initiatives in low- and middle-income countries — announced in the same week as a coordinated enterprise and social-impact signal.",
        "strategic_signal": "PwC deployment makes Anthropic the first AI company to have a Big Four firm rebuild a core business unit around its technology stack — a reference architecture other consulting firms will follow. The Gates Foundation partnership adds a mission-driven narrative that differentiates Anthropic in enterprise procurement where ESG credentials now influence vendor selection.",
        "ripple_effects": "Forces McKinsey, Deloitte, and KPMG to announce comparable AI deployments. Gates Foundation health-AI track competes with WHO/Google Health AI programs. Strengthens Anthropic's position in government and regulated-industry procurement where dual-use policy credibility matters.",
        "sentiment_at_time": "very positive",
        "forward_implication_score": 4,
        "stack_layer": "Application",
        "tags": ["enterprise", "partnership", "consulting", "health", "education", "claude", "pwc"],
        "thinking_frameworks": None,
        "source_event": "Anthropic May 2026 Release",
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
    print(f"Window: 2026-04-10 to 2026-05-17\n")

    # Resolve entity IDs
    entity_ids = {}
    for name in ["Anthropic", "Google DeepMind", "OpenAI"]:
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
