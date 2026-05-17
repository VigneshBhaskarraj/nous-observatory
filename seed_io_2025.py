"""
Nous Observatory — Google I/O 2025 Retrospective Seed
Run: python3 seed_io_2025.py

Seeds verified I/O 2025 announcements as milestones (entity = Google DeepMind,
source_event = 'Google I/O 2025'). Uses the same dedup-by-(date, event-prefix)
pattern as conference-update-insert.py — re-running is safe.

Why I/O 2025: the Live Updates and Brief tabs need a real corpus to validate
the synthesis pipeline against before I/O 2026 (May 19–20, 2026). This is that
ground-truth dataset.

Cross-check before pushing into prod:
  - Each milestone's `significance` is sourced from the I/O 2025 keynote /
    developer keynote recap on developers.googleblog.com.
  - `strategic_signal` and `ripple_effects` are analyst-style framing — review
    before insert if you want them stricter.
  - All claim_type = 'announced' (these are keynote claims, not yet benchmark-
    demonstrated at the time of announcement).
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


# Google I/O 2025 ran May 20–21, 2025.
# Anchor everything to 2025-05-20 (Day 1 keynote) unless a feature was
# explicitly Day 2 / developer keynote.
IO_2025_DAY1 = "2025-05-20"
IO_2025_DAY2 = "2025-05-21"

MILESTONES = [
    {
        "date": IO_2025_DAY1,
        "event": "Gemini 2.5 Flash and Gemini 2.5 Pro launch with 'thinking summaries' for explainability",
        "significance": "Gemini 2.5 family integrated natively into Vertex AI. 'Thinking summaries' expose the intermediate logical steps the model takes before outputting a final response — a critical feature for enterprise adoption and regulatory compliance where opaque deep-learning outputs are increasingly insufficient.",
        "strategic_signal": "Thinking summaries are Google's explainability play, pre-positioning Gemini for regulated industries (financial services, insurance) ahead of the EU AI Act's August 2026 enforcement of transparency mandates. This makes Gemini the only frontier model with native audit-grade reasoning trails.",
        "ripple_effects": "Forces Anthropic and OpenAI to surface comparable reasoning-trace features. Establishes 'explainability as a feature' as a competitive axis distinct from raw capability. Vertex AI integration tightens enterprise lock-in.",
        "sentiment_at_time": "positive",
        "forward_implication_score": 4,
        "stack_layer": "Model",
        "tags": ["gemini", "frontier-model", "reasoning", "thinking", "vertex-ai", "explainability"],
        "claim_type": "announced",
    },
    {
        "date": IO_2025_DAY1,
        "event": "Live API with Gemini 2.5 Flash Native Audio — proactive video/audio sensing in 24 languages",
        "significance": "Native multimodal speech generation bypasses the traditional speech-to-text-to-LLM latency pipeline. Supports 24 languages, granular voice style/pace/accent/tone control, and proactive monitoring of live video and audio streams — the model can continuously observe, identify key events, and filter background noise without an explicit prompt.",
        "strategic_signal": "Shifts the AI interaction paradigm from 'manually summoned via text' to 'ambient contextual observer'. This is the substrate for always-on agents in Android 17 (announced as 'Gemini Intelligence' direction). GPT-4o Realtime is the direct competitor — Google is matching, not leading, but with deeper OS hooks.",
        "ripple_effects": "Accelerates voice-first UX as the default for productivity apps. Pressures OpenAI Realtime API on pricing and language coverage. Sets up Project Rambler (Gboard voice dictation) as the consumer-facing demo of this capability.",
        "sentiment_at_time": "positive",
        "forward_implication_score": 5,
        "stack_layer": "Model",
        "tags": ["gemini", "multimodal", "live-api", "native-audio", "voice", "video", "ambient"],
        "claim_type": "announced",
    },
    {
        "date": IO_2025_DAY2,
        "event": "Model Context Protocol (MCP) support added to Gemini API and SDK",
        "significance": "Google adopts the MCP standard (originally proposed by Anthropic) for tool integration. Provides a standardized framework for the Gemini API to interface with open-source tools — the 'operational hands' of the model.",
        "strategic_signal": "By adopting Anthropic's MCP rather than fragmenting with a Google-proprietary tool protocol, Google signals it views the inter-tool protocol layer as a commodity and the inter-agent protocol (A2A) as the strategic battleground. This is the same pattern Microsoft used with USB — embrace, extend, control distribution.",
        "ripple_effects": "Cements MCP as the de facto tool-integration standard across all major AI providers. Lowers integration cost for tool builders. Sets up the A2A vs MCP narrative that played out at Cloud Next 2026.",
        "sentiment_at_time": "very positive",
        "forward_implication_score": 5,
        "stack_layer": "Infrastructure",
        "tags": ["mcp", "protocol", "standards", "interoperability", "tools", "gemini", "sdk"],
        "claim_type": "announced",
        "displacement_entities": ["Proprietary tool-integration frameworks"],
    },
    {
        "date": IO_2025_DAY2,
        "event": "Computer Use API released to Trusted Testers — agents that browse the web and manipulate GUIs",
        "significance": "Allows applications to autonomously browse the web and manipulate graphical user interfaces under high-level direction. Released initially to Trusted Testers. Foundational for autonomous agent workflows.",
        "strategic_signal": "Direct response to Anthropic's Computer Use (Oct 2024) and OpenAI's Operator. Google's trusted-tester rollout is more conservative than Anthropic's public preview but tighter than OpenAI's paywalled access — positioned for enterprise pilots.",
        "ripple_effects": "Three-way agent arms race intensifies. Forces SaaS vendors to either build agent-friendly APIs or risk being scraped via GUI automation. Pressures Anthropic on enterprise distribution where Google has incumbent advantage.",
        "sentiment_at_time": "positive",
        "forward_implication_score": 5,
        "stack_layer": "Model",
        "tags": ["agent", "computer-use", "agentic", "gemini", "browser", "automation"],
        "claim_type": "announced",
        "displacement_entities": ["Anthropic", "OpenAI"],
    },
    {
        "date": IO_2025_DAY2,
        "event": "URL Context tool — extract and reason over full webpage content from a link",
        "significance": "Experimental tool letting models extract and reason over full web page context using nothing but a URL. Eliminates manual scraping/parsing for grounded answers.",
        "strategic_signal": "Reduces friction for grounded RAG-style applications by an order of magnitude. Combined with the Live API, creates the substrate for the 'auto-browse' Chrome feature predicted for I/O 2026.",
        "ripple_effects": "Pressures dedicated web-scraping vendors (Browserless, Apify) at the margin. Bing/Brave Search API value proposition shifts toward differentiated content rather than raw extraction.",
        "sentiment_at_time": "positive",
        "forward_implication_score": 3,
        "stack_layer": "Developer Tools",
        "tags": ["url-context", "web", "tools", "gemini", "developer", "experimental"],
        "claim_type": "announced",
    },
    {
        "date": IO_2025_DAY2,
        "event": "Asynchronous Function Calling — long-running tools execute without blocking conversational flow",
        "significance": "Async function calling allows agent tools to run in the background while the model continues conversation, enabling multi-step parallel workflows previously requiring complex orchestration.",
        "strategic_signal": "Unlocks practical 'agent swarm' patterns where dozens of tool calls run concurrently. Combined with TPU 8i inference economics (announced at Cloud Next 2026), makes always-on background agents economically viable.",
        "ripple_effects": "Forces every agent framework (LangChain, CrewAI, AutoGen) to support async natively. Raises the bar for what counts as a production-grade agent runtime.",
        "sentiment_at_time": "positive",
        "forward_implication_score": 3,
        "stack_layer": "Developer Tools",
        "tags": ["async", "function-calling", "agent", "tools", "developer", "gemini"],
        "claim_type": "announced",
    },
    {
        "date": IO_2025_DAY1,
        "event": "Gemma 3n preview — efficient open multimodal model for audio/text/image/video",
        "significance": "Open-weights multimodal model preview, optimized for fast on-device inference. Handles audio, text, image, and video natively.",
        "strategic_signal": "Reaffirms Google's open-weights play against Meta Llama. Sized for the on-device niche where Llama is heavier; multimodal-native where Llama is text-first. Lays groundwork for Gemini Nano successor on Android.",
        "ripple_effects": "Pressures Meta to ship a multimodal Llama variant. Gives Android OEMs (Samsung, Pixel, Xiaomi) a Google-blessed open multimodal option for proprietary integrations.",
        "sentiment_at_time": "positive",
        "forward_implication_score": 3,
        "stack_layer": "Model",
        "tags": ["gemma", "open-weights", "multimodal", "on-device", "preview"],
        "claim_type": "announced",
        "displacement_entities": ["Meta"],
    },
    {
        "date": IO_2025_DAY1,
        "event": "Lyria RealTime — experimental interactive audio model in AI Studio",
        "significance": "Real-time generative audio model for interactive applications. Made available for experimentation directly in Google AI Studio.",
        "strategic_signal": "Music/audio generation is the next front after image (Imagen) and video (Veo). Lyria positions Google ahead of Suno/Udio on the enterprise-developer axis (not consumer virality, which Suno owns).",
        "ripple_effects": "Pressures Suno and Udio to release developer APIs. Sets up Lyria 3 (predicted for I/O 2026) as the high-fidelity production model.",
        "sentiment_at_time": "positive",
        "forward_implication_score": 3,
        "stack_layer": "Model",
        "tags": ["lyria", "audio", "music", "generative-media", "real-time", "ai-studio"],
        "claim_type": "announced",
        "displacement_entities": ["Suno", "Udio"],
    },
    {
        "date": IO_2025_DAY1,
        "event": "Firebase Studio transforms into 'prompt to publish' full-stack AI workspace",
        "significance": "Firebase Studio evolved from a dev tool into a comprehensive cloud-based AI workspace driving full-stack app creation from a prompt. Integrates with Figma via Builder.io plugin: Gemini 2.5 stitches together user flows, swaps placeholders for high-fidelity visuals via Unsplash, and adds functional logic without manual coding.",
        "strategic_signal": "Direct competitive shot at Vercel v0, Bolt, and Replit Agent. Google is using its incumbent Firebase position (~3M+ developers) to leapfrog standalone agent-coding tools by bundling backend provisioning. The 'prompt to publish' framing is borrowed from Vercel — Google making the same pitch with backend, auth, and DB included.",
        "ripple_effects": "Squeezes Bolt/v0 on the BaaS-included axis. Lovable and Replit Agent respond with their own backend stories. Pressure on Vercel to ship deeper Supabase/Neon partnerships.",
        "sentiment_at_time": "positive",
        "forward_implication_score": 4,
        "stack_layer": "Developer Tools",
        "tags": ["firebase", "firebase-studio", "developer", "no-code", "full-stack", "gemini", "figma"],
        "claim_type": "announced",
        "displacement_entities": ["Vercel", "Replit", "Bolt"],
    },
    {
        "date": IO_2025_DAY1,
        "event": "Firebase App Prototyping agent auto-provisions Auth, Firestore, and Hosting from a prompt",
        "significance": "The App Prototyping agent dynamically detects structural app requirements from the user's prompt. If user management is needed, it provisions Firebase Authentication. If data storage is needed, it provisions Cloud Firestore. Architecture is bundled into an 'App Blueprint' and deployed to Firebase App Hosting on approval.",
        "strategic_signal": "Backend-as-a-service was always Firebase's moat. By making provisioning a one-shot agent decision, Google removes the last manual step in indie-app development. This is the BaaS equivalent of v0 for the UI layer — and it ships with Google's auth, DB, hosting, all monetized.",
        "ripple_effects": "Lowers the bar for indie SaaS launch from days to minutes. Pressures Supabase to ship an equivalent agentic provisioning flow. Long-term, threatens the value prop of standalone BaaS vendors.",
        "sentiment_at_time": "positive",
        "forward_implication_score": 4,
        "stack_layer": "Developer Tools",
        "tags": ["firebase", "agent", "backend", "auth", "firestore", "no-code", "provisioning"],
        "claim_type": "announced",
        "displacement_entities": ["Supabase"],
    },
    {
        "date": IO_2025_DAY1,
        "event": "Firebase AI Logic — hybrid on-device + cloud inference SDK with automatic fallback",
        "significance": "Successor to Vertex AI in Firebase. Provides robust client-side integrations for the Gemini Developer API. The SDK interrogates local hardware: if capable, runs inference locally via Gemini Nano. If not, automatically falls back to cloud-hosted Vertex AI. Integrates with Firebase App Check to secure API calls.",
        "strategic_signal": "Architectural commitment to decentralized inference. Reduces cloud compute costs, minimizes latency, and resolves data privacy issues by keeping sensitive data on-device. The auto-fallback removes the last reason developers default to cloud-only — making on-device AI the new normal for mobile apps.",
        "ripple_effects": "Resets cost expectations for mobile AI features. Pressures Apple to ship a comparable cross-platform on-device SDK (Apple Intelligence is iOS-only). MLC/ONNX runtimes lose ground on the developer-experience axis.",
        "sentiment_at_time": "very positive",
        "forward_implication_score": 5,
        "stack_layer": "Developer Tools",
        "tags": ["firebase", "on-device", "gemini-nano", "hybrid-inference", "sdk", "privacy", "edge"],
        "claim_type": "announced",
        "displacement_entities": ["MLC", "ONNX Runtime"],
    },
    {
        "date": IO_2025_DAY2,
        "event": "Genkit adds Go (beta) and Python (alpha); dynamic model lookup for Node.js",
        "significance": "Server-side Gemini framework Genkit expands language support beyond Node.js. Dynamic model lookup means backend agents can access the latest Gemini iteration without package updates — eliminating refactor cycles.",
        "strategic_signal": "Go support targets Kubernetes-native backend teams; Python alpha targets the ML-engineer crowd that defaults to LangChain. Dynamic lookup is the kind of low-glamour DX feature that compounds — fewer reasons to leave Genkit means more stickiness.",
        "ripple_effects": "Eats into LangChain Python's share on the Gemini-first cohort. Pressures LangChain to ship dynamic model routing as a first-class feature.",
        "sentiment_at_time": "positive",
        "forward_implication_score": 3,
        "stack_layer": "Developer Tools",
        "tags": ["genkit", "developer", "go", "python", "node", "gemini", "backend"],
        "claim_type": "announced",
        "displacement_entities": ["LangChain"],
    },
    {
        "date": IO_2025_DAY1,
        "event": "Gemini Nano on Android via ML Kit GenAI APIs with prefix caching",
        "significance": "Democratizes on-device AI for mobile devs via ML Kit GenAI APIs — no ML expertise required. Includes Prompt API, Speech Recognition API, and local agent intelligence via Gemma open models. Prefix caching drastically reduces mobile inference latency, enabling real-time processing.",
        "strategic_signal": "On-device AI as a platform feature, not a per-app responsibility. Sets Android up as the substrate for the Gemini Intelligence vision: ambient, proactive, cross-app automation that needs zero-latency local inference.",
        "ripple_effects": "Forces Apple to expose comparable system-level APIs to third-party iOS devs (Apple Intelligence is largely first-party only). Pressures Samsung's Galaxy AI to either deepen Gemini integration or differentiate hard.",
        "sentiment_at_time": "very positive",
        "forward_implication_score": 5,
        "stack_layer": "Application",
        "tags": ["gemini-nano", "android", "on-device", "ml-kit", "mobile", "prefix-caching"],
        "claim_type": "announced",
        "displacement_entities": ["Apple Intelligence"],
    },
    {
        "date": IO_2025_DAY1,
        "event": "Chrome built-in AI APIs reach Stable in Chrome 138 (Summarizer, Translator, Prompt, Language Detector)",
        "significance": "Summarizer, Language Detector, Translator, and Prompt APIs went stable in Chrome 138. Writer, Rewriter, and Proofreader available via Origin Trials. Transforms the browser from a passive document viewer into a localized AI runtime environment. Enables offline functionality and end-to-end encrypted AI features. Early Preview Program for WebMCP initiated.",
        "strategic_signal": "Locks AI capabilities into the browser itself, bypassing both server APIs and per-site implementations. Combined with WebMCP standardization, this is Google's bid to make Chrome the agentic runtime for the web — the same play they made with Chrome Apps a decade ago, but with real demand this time.",
        "ripple_effects": "Sets up a standards fight at W3C over AI primitives. Mozilla and Apple forced to respond — likely with on-device variants leveraging their own model strategies. Pressures every JS library doing client-side ML (transformers.js, Web LLM) on relevance.",
        "sentiment_at_time": "positive",
        "forward_implication_score": 4,
        "stack_layer": "Application",
        "tags": ["chrome", "web", "browser", "on-device", "summarizer", "translator", "prompt-api", "webmcp", "standards"],
        "claim_type": "announced",
    },
    {
        "date": IO_2025_DAY2,
        "event": "Firebase AI Logic SDK for Unity (preview) — generative AI in games and Android XR",
        "significance": "Preview SDK enables Unity game developers to integrate generative text, image generation, and the bidirectional streaming Gemini Live API into games and Android XR experiences.",
        "strategic_signal": "Targets the Unity gamedev ecosystem ahead of Android XR's consumer launch (anticipated I/O 2026). Game-engine integration is the unglamorous prerequisite for the XR app ecosystem Google needs to compete with Apple Vision Pro and Meta Quest.",
        "ripple_effects": "Pressures Unreal to ship a comparable Gemini/OpenAI SDK. Sets up the XR-content pipeline Google needs before the glasses ship.",
        "sentiment_at_time": "positive",
        "forward_implication_score": 3,
        "stack_layer": "Developer Tools",
        "tags": ["unity", "xr", "android-xr", "games", "firebase", "gemini", "preview"],
        "claim_type": "announced",
    },
    # ── High-impact milestones missing from original seed — added 2026-05-17 ──
    # Sources: blog.google/technology/ai/google-io-2025-all-our-announcements/
    #          blog.google/innovation-and-ai/infrastructure-and-cloud/google-cloud/ironwood-tpu-age-of-inference/
    #          blog.google/innovation-and-ai/models-and-research/google-labs/jules/
    {
        "date": IO_2025_DAY1,
        "event": "Ironwood TPU (7th-gen) unveiled — 42.5 exaflops per pod, first inference-first AI chip from Google",
        "significance": "Google's 7th-generation TPU is the first designed specifically for AI inference at scale. Delivers 10x peak performance over TPU v5p, 4x better perf/chip vs TPU v6e for both training and inference. 42.5 exaflops per pod. Purpose-built for thinking/inferential workloads — not a general-purpose accelerator.",
        "strategic_signal": "By dedicating a full TPU generation to inference, Google signals the compute bottleneck is shifting from training runs to serving costs. Combined with the training-optimized TPU 8t at Cloud Next 2026, Google has bifurcated its silicon roadmap ahead of any competitor. Inference-optimized silicon enables aggressive Gemini API pricing that NVIDIA GPU-backed competitors cannot match.",
        "ripple_effects": "Accelerates competitive pressure on NVIDIA H100/H200 for inference workloads. Forces Amazon Trainium/Inferentia and Microsoft Azure Maia to reposition. Enables Google to price Gemini API inference well below market rate long-term.",
        "sentiment_at_time": "very positive",
        "forward_implication_score": 5,
        "stack_layer": "Infrastructure",
        "tags": ["tpu", "hardware", "inference", "custom-silicon", "silicon", "training"],
        "claim_type": "announced",
        "displacement_entities": ["Nvidia"],
    },
    {
        "date": IO_2025_DAY1,
        "event": "Veo 3 launched — state-of-the-art video generation with native synchronized audio",
        "significance": "Veo 3 is the most advanced text-to-video model yet, generating ultra-realistic videos with native synchronized audio from text prompts. Audio is generated natively in-model — not post-processed. Paired with Flow, a professional AI filmmaking tool for scene and character asset creation.",
        "strategic_signal": "Native audio in video generation is the key moat: Sora, Kling, and Runway lack it. Combined with Lyria (music) and Live API native audio, Google has assembled a vertically integrated generative media stack. Flow bundles this into a professional filmmaker product targeting the $50B+ video production market.",
        "ripple_effects": "Forces OpenAI Sora, Runway, and Kling to ship synchronized audio as table stakes. Resets the video-generation benchmark. Adobe Premiere and After Effects face competition from AI-native filmmaking tools via Flow.",
        "sentiment_at_time": "very positive",
        "forward_implication_score": 5,
        "stack_layer": "Model",
        "tags": ["veo", "video", "audio", "generative-media", "multimodal", "flow"],
        "claim_type": "announced",
        "displacement_entities": ["OpenAI", "Adobe"],
    },
    {
        "date": IO_2025_DAY1,
        "event": "AI Mode in Google Search rolls out to all US users powered by Gemini 2.5",
        "significance": "AI Mode — the conversational AI-generated search experience — begins rolling out to all US users. Gemini 2.5 powers both AI Mode and AI Overviews. AI Overviews already serving 1.5B+ users per month. Affects billions of daily searches.",
        "strategic_signal": "The full transition of Google's core product from link-based to AI-generated answers is now underway. Revenue implications are unresolved — AI answers reduce click-throughs to advertiser sites, creating structural tension with Google's $175B/year ad business. Google is betting engagement gains outweigh CTR losses.",
        "ripple_effects": "SEO industry faces existential disruption. Publishers see organic traffic decline. OpenAI SearchGPT and Perplexity gain credibility as alternatives for content creators. Advertisers must redesign for AI Mode ad placement.",
        "sentiment_at_time": "mixed",
        "forward_implication_score": 4,
        "stack_layer": "Application",
        "tags": ["search", "gemini", "ai-overviews", "consumer", "web"],
        "claim_type": "announced",
        "displacement_entities": ["Perplexity", "OpenAI"],
    },
    {
        "date": IO_2025_DAY2,
        "event": "Jules autonomous coding agent launched in public beta — async GitHub task delegation",
        "significance": "Jules is an async coding agent integrating directly with GitHub. Handles multiple backlog items simultaneously, writes tests, fixes bugs, and generates audio overviews of codebase changes. Operates fully asynchronously — developers delegate and check back. Now open to all developers in public beta with free and paid plans.",
        "strategic_signal": "Jules is Google's entry into agentic coding against GitHub Copilot Workspace and Devin. GitHub-native integration (not IDE-based) and audio codebase summaries are differentiated UX bets. Async multi-task delegation addresses the 'developer still in the loop' bottleneck limiting Copilot.",
        "ripple_effects": "Pressures GitHub Copilot Workspace to ship full async delegation. Forces Cognition/Devin to accelerate GitHub integration. Resets expectations from inline suggestion to autonomous PR resolution.",
        "sentiment_at_time": "positive",
        "forward_implication_score": 4,
        "stack_layer": "Developer Tools",
        "tags": ["developer", "agent", "coding", "github", "adk", "async", "agentic"],
        "claim_type": "announced",
        "displacement_entities": ["Microsoft AI", "OpenAI"],
    },
    {
        "date": IO_2025_DAY1,
        "event": "Gemini 2.5 Deep Think mode announced — leads math, code, and multimodal reasoning benchmarks",
        "significance": "Enhanced reasoning mode for Gemini 2.5 that leads across math, code, and multimodality benchmarks. Applies extended compute to problem decomposition before answering. Toggled as a reasoning mode parameter on top of Gemini 2.5 Pro.",
        "strategic_signal": "Deep Think positions Gemini directly against Claude Extended Thinking and OpenAI o-series. Combined with Ironwood's inference economics, Google can offer reasoning-on-demand at lower cost than NVIDIA GPU-backed competitors. By tying Deep Think to Gemini 2.5 (top-ranked on LMArena), Google claims both best conversation AND best reasoning.",
        "ripple_effects": "Three-way reasoning competition: Claude Extended Thinking, OpenAI o-series, Gemini Deep Think. Forces benchmark race toward real-world task completion. Sets reasoning mode as a toggleable parameter as the new UX standard.",
        "sentiment_at_time": "positive",
        "forward_implication_score": 4,
        "stack_layer": "Model",
        "tags": ["gemini", "frontier-model", "reasoning", "thinking", "deep-think"],
        "claim_type": "announced",
        "displacement_entities": ["Anthropic", "OpenAI"],
    },
    {
        "date": IO_2025_DAY1,
        "event": "Google Beam unveiled — AI-first 3D video communication platform evolved from Project Starline",
        "significance": "Commercial AI-first video communications platform using a state-of-the-art model to transform 2D video streams into realistic 3D experience in real time. Evolved from Project Starline research prototype. HP announced as hardware partner for enterprise rollout.",
        "strategic_signal": "Google is targeting enterprise video conferencing ($6B+ annual revenue) currently owned by Zoom Rooms, Teams Rooms, and Cisco Webex. The 3D presence differentiator requires Google's array camera hardware and AI model stack — difficult to replicate in software alone. HP partnership gives Google Fortune 500 IT distribution without a direct sales force.",
        "ripple_effects": "Direct competitive pressure on Zoom Rooms and Microsoft Teams Rooms hardware. Forces Poly, Crestron, and Cisco Webex to respond. Positions Google in physical enterprise spaces — a new channel beyond software and cloud.",
        "sentiment_at_time": "positive",
        "forward_implication_score": 3,
        "stack_layer": "Application",
        "tags": ["beam", "device", "hardware", "spatial", "video", "enterprise"],
        "claim_type": "announced",
        "displacement_entities": ["Microsoft AI"],
    },
    {
        "date": IO_2025_DAY1,
        "event": "Imagen 4 and Lyria 2 launched on Vertex AI — most capable image and music generation models",
        "significance": "Imagen 4 is Google's most capable image generation model to date. Lyria 2 is the full-quality music generation model (Lyria RealTime announced separately for interactive use). Both on Vertex AI. Alongside Veo 3, these form a complete generative media stack (image + video + audio/music) on a single enterprise platform.",
        "strategic_signal": "Having leading models across all three generative media modalities on one Vertex AI platform is a critical enterprise pitch vs. cobbling together DALL-E + Suno + Sora from different vendors. Google positions Vertex AI as the one-stop generative media platform for enterprise content pipelines.",
        "ripple_effects": "Pressure on Midjourney and Adobe Firefly in enterprise image generation. Suno and Udio face a well-funded competitor with enterprise distribution. Firefly faces particular risk given its Creative Cloud dependency vs. Vertex AI pipeline integration.",
        "sentiment_at_time": "positive",
        "forward_implication_score": 3,
        "stack_layer": "Model",
        "tags": ["imagen", "lyria", "generative-media", "vision", "audio", "music", "model-release"],
        "claim_type": "announced",
        "displacement_entities": ["Adobe", "OpenAI"],
    },
    {
        "date": IO_2025_DAY1,
        "event": "Stitch launches — generate UI designs and frontend code from text prompts with Figma export",
        "significance": "New AI tool that generates user interface designs and corresponding frontend code from a text or image prompt. Iterates conversationally. Exports to CSS/HTML or Figma. Integrates with Firebase Studio's prompt-to-publish pipeline, compressing design-to-deploy into a single workflow.",
        "strategic_signal": "Stitch enters the UI-gen market (v0, Bolt, Lovable) with Google's Gemini model advantage and Figma export — the critical handoff to professional designers. Bundled into Firebase Studio, it creates a design → code → deploy pipeline standalone tools cannot match.",
        "ripple_effects": "Direct competition with Vercel v0 and Bolt for frontend code generation. Adds Google to the Figma ecosystem as a major AI partner. Sets design-to-deploy pipeline as the developer tools battlefield.",
        "sentiment_at_time": "positive",
        "forward_implication_score": 3,
        "stack_layer": "Developer Tools",
        "tags": ["developer", "no-code", "ui", "figma", "frontend", "firebase", "stitch"],
        "claim_type": "announced",
        "displacement_entities": ["Vercel", "Bolt"],
    },
    {
        "date": IO_2025_DAY1,
        "event": "Google AI Ultra subscription launched at $249.99/month — maximum early access to frontier AI features",
        "significance": "New premium Google One AI tier at $249.99/month gives early and maximum access to bleeding-edge features across Gemini models, NotebookLM, and Google's full product suite. Positioned above Google AI Pro. Targets the professional 'power user' segment willing to pay for state-of-the-art access.",
        "strategic_signal": "At $249.99/month (above ChatGPT Pro at $200), Google signals it believes its multi-product bundle justifies a premium. This tier also serves as a testing sandbox — collecting behavioral data from highest-value users to inform model and product decisions.",
        "ripple_effects": "Forces OpenAI and Anthropic to differentiate premium tiers or match pricing. Creates a 'frontier consumer AI' tier category. Signals that super-users will pay for exclusive early access — a model the industry will broadly adopt.",
        "sentiment_at_time": "positive",
        "forward_implication_score": 3,
        "stack_layer": "Application",
        "tags": ["gemini", "consumer", "subscription", "pro", "enterprise"],
        "claim_type": "announced",
        "displacement_entities": ["OpenAI", "Anthropic"],
    },
]


SOURCE_EVENT_LABEL = "Google I/O 2025"


def get_entity_id(name):
    status, data = _request(
        "GET",
        f"{SUPABASE_URL}/rest/v1/entities",
        params={"name": f"eq.{name}", "select": "id,name"},
    )
    if not data:
        print(f"  ⚠ Entity not found: {name}")
        return None
    return data[0]["id"]


def get_existing(entity_id):
    status, data = _request(
        "GET",
        f"{SUPABASE_URL}/rest/v1/milestones",
        params={"entity_id": f"eq.{entity_id}", "select": "date,event"},
    )
    return {(m["date"], m["event"][:60]) for m in (data or [])}


def insert_batch(rows):
    status, _ = _request(
        "POST",
        f"{SUPABASE_URL}/rest/v1/milestones",
        body=rows,
        extra_headers={"Prefer": "return=minimal"},
    )
    return status


def main():
    print("=== Nous Observatory — Google I/O 2025 Retrospective Seed ===\n")

    eid = get_entity_id("Google DeepMind")
    if not eid:
        print("Cannot proceed without Google DeepMind entity.")
        sys.exit(1)
    print(f"  ✓ Google DeepMind: {eid}\n")

    existing = get_existing(eid)
    print(f"  Existing milestones for this entity: {len(existing)}\n")

    to_insert, skipped = [], 0
    for m in MILESTONES:
        key = (m["date"], m["event"][:60])
        if key in existing:
            print(f"  SKIP (duplicate): {m['date']} — {m['event'][:60]}")
            skipped += 1
            continue
        record = {
            "entity_id": eid,
            "date": m["date"],
            "event": m["event"],
            "significance": m["significance"],
            "strategic_signal": m["strategic_signal"],
            "ripple_effects": m["ripple_effects"],
            "sentiment_at_time": m["sentiment_at_time"],
            "forward_implication_score": m["forward_implication_score"],
            "stack_layer": m["stack_layer"],
            "tags": m["tags"],
            "claim_type": m["claim_type"],
            "source_event": SOURCE_EVENT_LABEL,
            "displacement_entities": m.get("displacement_entities"),
        }
        to_insert.append(record)
        print(f"  QUEUE: {m['date']} — {m['event'][:60]}")

    inserted = 0
    for record in to_insert:
        try:
            status = insert_batch([record])
            print(f"  ✓ INSERT ({status}): {record['date']} — {record['event'][:60]}")
            inserted += 1
        except RuntimeError as e:
            print(f"  ✗ FAILED: {record['date']} — {record['event'][:60]}\n    {e}")

    print(f"\n=== Summary ===")
    print(f"  Inserted: {inserted}")
    print(f"  Skipped (duplicates): {skipped}")
    print(f"  Source event: {SOURCE_EVENT_LABEL}")
    print("Done.")


if __name__ == "__main__":
    main()
