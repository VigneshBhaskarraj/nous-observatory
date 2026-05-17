-- Nous Observatory — Google I/O 2025 Seed
-- Paste into Supabase SQL Editor → Run.
-- Idempotent: skips milestones already present by (date, event[:60]).

DO $SEED$
DECLARE
  eid uuid;
  n int := 0;
BEGIN
  SELECT id INTO eid FROM public.entities WHERE name = 'Google DeepMind';
  IF eid IS NULL THEN
    RAISE EXCEPTION 'Entity Google DeepMind not found — check entities table.';
  END IF;
  RAISE NOTICE 'Google DeepMind entity_id: %', eid;

  -- 1. Gemini 2.5 Flash and Gemini 2.5 Pro launch with 'thinking summaries' for
  IF NOT EXISTS (SELECT 1 FROM public.milestones
                WHERE entity_id = eid
                  AND date = '2025-05-20'
                  AND LEFT(event, 60) = 'Gemini 2.5 Flash and Gemini 2.5 Pro launch with ''thinking su') THEN
    INSERT INTO public.milestones (
      entity_id, date, event, significance, strategic_signal,
      ripple_effects, sentiment_at_time, forward_implication_score,
      stack_layer, tags, claim_type, source_event, displacement_entities
    ) VALUES (
      eid,
      '2025-05-20',
      'Gemini 2.5 Flash and Gemini 2.5 Pro launch with ''thinking summaries'' for explainability',
      'Gemini 2.5 family integrated natively into Vertex AI. ''Thinking summaries'' expose the intermediate logical steps the model takes before outputting a final response — a critical feature for enterprise adoption and regulatory compliance where opaque deep-learning outputs are increasingly insufficient.',
      'Thinking summaries are Google''s explainability play, pre-positioning Gemini for regulated industries (financial services, insurance) ahead of the EU AI Act''s August 2026 enforcement of transparency mandates. This makes Gemini the only frontier model with native audit-grade reasoning trails.',
      'Forces Anthropic and OpenAI to surface comparable reasoning-trace features. Establishes ''explainability as a feature'' as a competitive axis distinct from raw capability. Vertex AI integration tightens enterprise lock-in.',
      'positive',
      4,
      'Model',
      ARRAY['gemini', 'frontier-model', 'reasoning', 'thinking', 'vertex-ai', 'explainability'],
      'announced',
      'Google I/O 2025',
      NULL
    );
    n := n + 1;
  END IF;

  -- 2. Live API with Gemini 2.5 Flash Native Audio — proactive video/audio sens
  IF NOT EXISTS (SELECT 1 FROM public.milestones
                WHERE entity_id = eid
                  AND date = '2025-05-20'
                  AND LEFT(event, 60) = 'Live API with Gemini 2.5 Flash Native Audio — proactive vide') THEN
    INSERT INTO public.milestones (
      entity_id, date, event, significance, strategic_signal,
      ripple_effects, sentiment_at_time, forward_implication_score,
      stack_layer, tags, claim_type, source_event, displacement_entities
    ) VALUES (
      eid,
      '2025-05-20',
      'Live API with Gemini 2.5 Flash Native Audio — proactive video/audio sensing in 24 languages',
      'Native multimodal speech generation bypasses the traditional speech-to-text-to-LLM latency pipeline. Supports 24 languages, granular voice style/pace/accent/tone control, and proactive monitoring of live video and audio streams — the model can continuously observe, identify key events, and filter background noise without an explicit prompt.',
      'Shifts the AI interaction paradigm from ''manually summoned via text'' to ''ambient contextual observer''. This is the substrate for always-on agents in Android 17 (announced as ''Gemini Intelligence'' direction). GPT-4o Realtime is the direct competitor — Google is matching, not leading, but with deeper OS hooks.',
      'Accelerates voice-first UX as the default for productivity apps. Pressures OpenAI Realtime API on pricing and language coverage. Sets up Project Rambler (Gboard voice dictation) as the consumer-facing demo of this capability.',
      'positive',
      5,
      'Model',
      ARRAY['gemini', 'multimodal', 'live-api', 'native-audio', 'voice', 'video', 'ambient'],
      'announced',
      'Google I/O 2025',
      NULL
    );
    n := n + 1;
  END IF;

  -- 3. Model Context Protocol (MCP) support added to Gemini API and SDK
  IF NOT EXISTS (SELECT 1 FROM public.milestones
                WHERE entity_id = eid
                  AND date = '2025-05-21'
                  AND LEFT(event, 60) = 'Model Context Protocol (MCP) support added to Gemini API and') THEN
    INSERT INTO public.milestones (
      entity_id, date, event, significance, strategic_signal,
      ripple_effects, sentiment_at_time, forward_implication_score,
      stack_layer, tags, claim_type, source_event, displacement_entities
    ) VALUES (
      eid,
      '2025-05-21',
      'Model Context Protocol (MCP) support added to Gemini API and SDK',
      'Google adopts the MCP standard (originally proposed by Anthropic) for tool integration. Provides a standardized framework for the Gemini API to interface with open-source tools — the ''operational hands'' of the model.',
      'By adopting Anthropic''s MCP rather than fragmenting with a Google-proprietary tool protocol, Google signals it views the inter-tool protocol layer as a commodity and the inter-agent protocol (A2A) as the strategic battleground. This is the same pattern Microsoft used with USB — embrace, extend, control distribution.',
      'Cements MCP as the de facto tool-integration standard across all major AI providers. Lowers integration cost for tool builders. Sets up the A2A vs MCP narrative that played out at Cloud Next 2026.',
      'very positive',
      5,
      'Infrastructure',
      ARRAY['mcp', 'protocol', 'standards', 'interoperability', 'tools', 'gemini', 'sdk'],
      'announced',
      'Google I/O 2025',
      NULL
    );
    n := n + 1;
  END IF;

  -- 4. Computer Use API released to Trusted Testers — agents that browse the we
  IF NOT EXISTS (SELECT 1 FROM public.milestones
                WHERE entity_id = eid
                  AND date = '2025-05-21'
                  AND LEFT(event, 60) = 'Computer Use API released to Trusted Testers — agents that b') THEN
    INSERT INTO public.milestones (
      entity_id, date, event, significance, strategic_signal,
      ripple_effects, sentiment_at_time, forward_implication_score,
      stack_layer, tags, claim_type, source_event, displacement_entities
    ) VALUES (
      eid,
      '2025-05-21',
      'Computer Use API released to Trusted Testers — agents that browse the web and manipulate GUIs',
      'Allows applications to autonomously browse the web and manipulate graphical user interfaces under high-level direction. Released initially to Trusted Testers. Foundational for autonomous agent workflows.',
      'Direct response to Anthropic''s Computer Use (Oct 2024) and OpenAI''s Operator. Google''s trusted-tester rollout is more conservative than Anthropic''s public preview but tighter than OpenAI''s paywalled access — positioned for enterprise pilots.',
      'Three-way agent arms race intensifies. Forces SaaS vendors to either build agent-friendly APIs or risk being scraped via GUI automation. Pressures Anthropic on enterprise distribution where Google has incumbent advantage.',
      'positive',
      5,
      'Model',
      ARRAY['agent', 'computer-use', 'agentic', 'gemini', 'browser', 'automation'],
      'announced',
      'Google I/O 2025',
      ARRAY['Anthropic', 'OpenAI']
    );
    n := n + 1;
  END IF;

  -- 5. URL Context tool — extract and reason over full webpage content from a l
  IF NOT EXISTS (SELECT 1 FROM public.milestones
                WHERE entity_id = eid
                  AND date = '2025-05-21'
                  AND LEFT(event, 60) = 'URL Context tool — extract and reason over full webpage cont') THEN
    INSERT INTO public.milestones (
      entity_id, date, event, significance, strategic_signal,
      ripple_effects, sentiment_at_time, forward_implication_score,
      stack_layer, tags, claim_type, source_event, displacement_entities
    ) VALUES (
      eid,
      '2025-05-21',
      'URL Context tool — extract and reason over full webpage content from a link',
      'Experimental tool letting models extract and reason over full web page context using nothing but a URL. Eliminates manual scraping/parsing for grounded answers.',
      'Reduces friction for grounded RAG-style applications by an order of magnitude. Combined with the Live API, creates the substrate for the ''auto-browse'' Chrome feature predicted for I/O 2026.',
      'Pressures dedicated web-scraping vendors (Browserless, Apify) at the margin. Bing/Brave Search API value proposition shifts toward differentiated content rather than raw extraction.',
      'positive',
      3,
      'Developer Tools',
      ARRAY['url-context', 'web', 'tools', 'gemini', 'developer', 'experimental'],
      'announced',
      'Google I/O 2025',
      NULL
    );
    n := n + 1;
  END IF;

  -- 6. Asynchronous Function Calling — long-running tools execute without block
  IF NOT EXISTS (SELECT 1 FROM public.milestones
                WHERE entity_id = eid
                  AND date = '2025-05-21'
                  AND LEFT(event, 60) = 'Asynchronous Function Calling — long-running tools execute w') THEN
    INSERT INTO public.milestones (
      entity_id, date, event, significance, strategic_signal,
      ripple_effects, sentiment_at_time, forward_implication_score,
      stack_layer, tags, claim_type, source_event, displacement_entities
    ) VALUES (
      eid,
      '2025-05-21',
      'Asynchronous Function Calling — long-running tools execute without blocking conversational flow',
      'Async function calling allows agent tools to run in the background while the model continues conversation, enabling multi-step parallel workflows previously requiring complex orchestration.',
      'Unlocks practical ''agent swarm'' patterns where dozens of tool calls run concurrently. Combined with TPU 8i inference economics (announced at Cloud Next 2026), makes always-on background agents economically viable.',
      'Forces every agent framework (LangChain, CrewAI, AutoGen) to support async natively. Raises the bar for what counts as a production-grade agent runtime.',
      'positive',
      3,
      'Developer Tools',
      ARRAY['async', 'function-calling', 'agent', 'tools', 'developer', 'gemini'],
      'announced',
      'Google I/O 2025',
      NULL
    );
    n := n + 1;
  END IF;

  -- 7. Gemma 3n preview — efficient open multimodal model for audio/text/image/
  IF NOT EXISTS (SELECT 1 FROM public.milestones
                WHERE entity_id = eid
                  AND date = '2025-05-20'
                  AND LEFT(event, 60) = 'Gemma 3n preview — efficient open multimodal model for audio') THEN
    INSERT INTO public.milestones (
      entity_id, date, event, significance, strategic_signal,
      ripple_effects, sentiment_at_time, forward_implication_score,
      stack_layer, tags, claim_type, source_event, displacement_entities
    ) VALUES (
      eid,
      '2025-05-20',
      'Gemma 3n preview — efficient open multimodal model for audio/text/image/video',
      'Open-weights multimodal model preview, optimized for fast on-device inference. Handles audio, text, image, and video natively.',
      'Reaffirms Google''s open-weights play against Meta Llama. Sized for the on-device niche where Llama is heavier; multimodal-native where Llama is text-first. Lays groundwork for Gemini Nano successor on Android.',
      'Pressures Meta to ship a multimodal Llama variant. Gives Android OEMs (Samsung, Pixel, Xiaomi) a Google-blessed open multimodal option for proprietary integrations.',
      'positive',
      3,
      'Model',
      ARRAY['gemma', 'open-weights', 'multimodal', 'on-device', 'preview'],
      'announced',
      'Google I/O 2025',
      ARRAY['Meta']
    );
    n := n + 1;
  END IF;

  -- 8. Lyria RealTime — experimental interactive audio model in AI Studio
  IF NOT EXISTS (SELECT 1 FROM public.milestones
                WHERE entity_id = eid
                  AND date = '2025-05-20'
                  AND LEFT(event, 60) = 'Lyria RealTime — experimental interactive audio model in AI ') THEN
    INSERT INTO public.milestones (
      entity_id, date, event, significance, strategic_signal,
      ripple_effects, sentiment_at_time, forward_implication_score,
      stack_layer, tags, claim_type, source_event, displacement_entities
    ) VALUES (
      eid,
      '2025-05-20',
      'Lyria RealTime — experimental interactive audio model in AI Studio',
      'Real-time generative audio model for interactive applications. Made available for experimentation directly in Google AI Studio.',
      'Music/audio generation is the next front after image (Imagen) and video (Veo). Lyria positions Google ahead of Suno/Udio on the enterprise-developer axis (not consumer virality, which Suno owns).',
      'Pressures Suno and Udio to release developer APIs. Sets up Lyria 3 (predicted for I/O 2026) as the high-fidelity production model.',
      'positive',
      3,
      'Model',
      ARRAY['lyria', 'audio', 'music', 'generative-media', 'real-time', 'ai-studio'],
      'announced',
      'Google I/O 2025',
      ARRAY['Suno', 'Udio']
    );
    n := n + 1;
  END IF;

  -- 9. Firebase Studio transforms into 'prompt to publish' full-stack AI worksp
  IF NOT EXISTS (SELECT 1 FROM public.milestones
                WHERE entity_id = eid
                  AND date = '2025-05-20'
                  AND LEFT(event, 60) = 'Firebase Studio transforms into ''prompt to publish'' full-sta') THEN
    INSERT INTO public.milestones (
      entity_id, date, event, significance, strategic_signal,
      ripple_effects, sentiment_at_time, forward_implication_score,
      stack_layer, tags, claim_type, source_event, displacement_entities
    ) VALUES (
      eid,
      '2025-05-20',
      'Firebase Studio transforms into ''prompt to publish'' full-stack AI workspace',
      'Firebase Studio evolved from a dev tool into a comprehensive cloud-based AI workspace driving full-stack app creation from a prompt. Integrates with Figma via Builder.io plugin: Gemini 2.5 stitches together user flows, swaps placeholders for high-fidelity visuals via Unsplash, and adds functional logic without manual coding.',
      'Direct competitive shot at Vercel v0, Bolt, and Replit Agent. Google is using its incumbent Firebase position (~3M+ developers) to leapfrog standalone agent-coding tools by bundling backend provisioning. The ''prompt to publish'' framing is borrowed from Vercel — Google making the same pitch with backend, auth, and DB included.',
      'Squeezes Bolt/v0 on the BaaS-included axis. Lovable and Replit Agent respond with their own backend stories. Pressure on Vercel to ship deeper Supabase/Neon partnerships.',
      'positive',
      4,
      'Developer Tools',
      ARRAY['firebase', 'firebase-studio', 'developer', 'no-code', 'full-stack', 'gemini', 'figma'],
      'announced',
      'Google I/O 2025',
      ARRAY['Vercel', 'Replit', 'Bolt']
    );
    n := n + 1;
  END IF;

  -- 10. Firebase App Prototyping agent auto-provisions Auth, Firestore, and Host
  IF NOT EXISTS (SELECT 1 FROM public.milestones
                WHERE entity_id = eid
                  AND date = '2025-05-20'
                  AND LEFT(event, 60) = 'Firebase App Prototyping agent auto-provisions Auth, Firesto') THEN
    INSERT INTO public.milestones (
      entity_id, date, event, significance, strategic_signal,
      ripple_effects, sentiment_at_time, forward_implication_score,
      stack_layer, tags, claim_type, source_event, displacement_entities
    ) VALUES (
      eid,
      '2025-05-20',
      'Firebase App Prototyping agent auto-provisions Auth, Firestore, and Hosting from a prompt',
      'The App Prototyping agent dynamically detects structural app requirements from the user''s prompt. If user management is needed, it provisions Firebase Authentication. If data storage is needed, it provisions Cloud Firestore. Architecture is bundled into an ''App Blueprint'' and deployed to Firebase App Hosting on approval.',
      'Backend-as-a-service was always Firebase''s moat. By making provisioning a one-shot agent decision, Google removes the last manual step in indie-app development. This is the BaaS equivalent of v0 for the UI layer — and it ships with Google''s auth, DB, hosting, all monetized.',
      'Lowers the bar for indie SaaS launch from days to minutes. Pressures Supabase to ship an equivalent agentic provisioning flow. Long-term, threatens the value prop of standalone BaaS vendors.',
      'positive',
      4,
      'Developer Tools',
      ARRAY['firebase', 'agent', 'backend', 'auth', 'firestore', 'no-code', 'provisioning'],
      'announced',
      'Google I/O 2025',
      ARRAY['Supabase']
    );
    n := n + 1;
  END IF;

  -- 11. Firebase AI Logic — hybrid on-device + cloud inference SDK with automati
  IF NOT EXISTS (SELECT 1 FROM public.milestones
                WHERE entity_id = eid
                  AND date = '2025-05-20'
                  AND LEFT(event, 60) = 'Firebase AI Logic — hybrid on-device + cloud inference SDK w') THEN
    INSERT INTO public.milestones (
      entity_id, date, event, significance, strategic_signal,
      ripple_effects, sentiment_at_time, forward_implication_score,
      stack_layer, tags, claim_type, source_event, displacement_entities
    ) VALUES (
      eid,
      '2025-05-20',
      'Firebase AI Logic — hybrid on-device + cloud inference SDK with automatic fallback',
      'Successor to Vertex AI in Firebase. Provides robust client-side integrations for the Gemini Developer API. The SDK interrogates local hardware: if capable, runs inference locally via Gemini Nano. If not, automatically falls back to cloud-hosted Vertex AI. Integrates with Firebase App Check to secure API calls.',
      'Architectural commitment to decentralized inference. Reduces cloud compute costs, minimizes latency, and resolves data privacy issues by keeping sensitive data on-device. The auto-fallback removes the last reason developers default to cloud-only — making on-device AI the new normal for mobile apps.',
      'Resets cost expectations for mobile AI features. Pressures Apple to ship a comparable cross-platform on-device SDK (Apple Intelligence is iOS-only). MLC/ONNX runtimes lose ground on the developer-experience axis.',
      'very positive',
      5,
      'Developer Tools',
      ARRAY['firebase', 'on-device', 'gemini-nano', 'hybrid-inference', 'sdk', 'privacy', 'edge'],
      'announced',
      'Google I/O 2025',
      ARRAY['MLC', 'ONNX Runtime']
    );
    n := n + 1;
  END IF;

  -- 12. Genkit adds Go (beta) and Python (alpha); dynamic model lookup for Node.
  IF NOT EXISTS (SELECT 1 FROM public.milestones
                WHERE entity_id = eid
                  AND date = '2025-05-21'
                  AND LEFT(event, 60) = 'Genkit adds Go (beta) and Python (alpha); dynamic model look') THEN
    INSERT INTO public.milestones (
      entity_id, date, event, significance, strategic_signal,
      ripple_effects, sentiment_at_time, forward_implication_score,
      stack_layer, tags, claim_type, source_event, displacement_entities
    ) VALUES (
      eid,
      '2025-05-21',
      'Genkit adds Go (beta) and Python (alpha); dynamic model lookup for Node.js',
      'Server-side Gemini framework Genkit expands language support beyond Node.js. Dynamic model lookup means backend agents can access the latest Gemini iteration without package updates — eliminating refactor cycles.',
      'Go support targets Kubernetes-native backend teams; Python alpha targets the ML-engineer crowd that defaults to LangChain. Dynamic lookup is the kind of low-glamour DX feature that compounds — fewer reasons to leave Genkit means more stickiness.',
      'Eats into LangChain Python''s share on the Gemini-first cohort. Pressures LangChain to ship dynamic model routing as a first-class feature.',
      'positive',
      3,
      'Developer Tools',
      ARRAY['genkit', 'developer', 'go', 'python', 'node', 'gemini', 'backend'],
      'announced',
      'Google I/O 2025',
      ARRAY['LangChain']
    );
    n := n + 1;
  END IF;

  -- 13. Gemini Nano on Android via ML Kit GenAI APIs with prefix caching
  IF NOT EXISTS (SELECT 1 FROM public.milestones
                WHERE entity_id = eid
                  AND date = '2025-05-20'
                  AND LEFT(event, 60) = 'Gemini Nano on Android via ML Kit GenAI APIs with prefix cac') THEN
    INSERT INTO public.milestones (
      entity_id, date, event, significance, strategic_signal,
      ripple_effects, sentiment_at_time, forward_implication_score,
      stack_layer, tags, claim_type, source_event, displacement_entities
    ) VALUES (
      eid,
      '2025-05-20',
      'Gemini Nano on Android via ML Kit GenAI APIs with prefix caching',
      'Democratizes on-device AI for mobile devs via ML Kit GenAI APIs — no ML expertise required. Includes Prompt API, Speech Recognition API, and local agent intelligence via Gemma open models. Prefix caching drastically reduces mobile inference latency, enabling real-time processing.',
      'On-device AI as a platform feature, not a per-app responsibility. Sets Android up as the substrate for the Gemini Intelligence vision: ambient, proactive, cross-app automation that needs zero-latency local inference.',
      'Forces Apple to expose comparable system-level APIs to third-party iOS devs (Apple Intelligence is largely first-party only). Pressures Samsung''s Galaxy AI to either deepen Gemini integration or differentiate hard.',
      'very positive',
      5,
      'Application',
      ARRAY['gemini-nano', 'android', 'on-device', 'ml-kit', 'mobile', 'prefix-caching'],
      'announced',
      'Google I/O 2025',
      ARRAY['Apple Intelligence']
    );
    n := n + 1;
  END IF;

  -- 14. Chrome built-in AI APIs reach Stable in Chrome 138 (Summarizer, Translat
  IF NOT EXISTS (SELECT 1 FROM public.milestones
                WHERE entity_id = eid
                  AND date = '2025-05-20'
                  AND LEFT(event, 60) = 'Chrome built-in AI APIs reach Stable in Chrome 138 (Summariz') THEN
    INSERT INTO public.milestones (
      entity_id, date, event, significance, strategic_signal,
      ripple_effects, sentiment_at_time, forward_implication_score,
      stack_layer, tags, claim_type, source_event, displacement_entities
    ) VALUES (
      eid,
      '2025-05-20',
      'Chrome built-in AI APIs reach Stable in Chrome 138 (Summarizer, Translator, Prompt, Language Detector)',
      'Summarizer, Language Detector, Translator, and Prompt APIs went stable in Chrome 138. Writer, Rewriter, and Proofreader available via Origin Trials. Transforms the browser from a passive document viewer into a localized AI runtime environment. Enables offline functionality and end-to-end encrypted AI features. Early Preview Program for WebMCP initiated.',
      'Locks AI capabilities into the browser itself, bypassing both server APIs and per-site implementations. Combined with WebMCP standardization, this is Google''s bid to make Chrome the agentic runtime for the web — the same play they made with Chrome Apps a decade ago, but with real demand this time.',
      'Sets up a standards fight at W3C over AI primitives. Mozilla and Apple forced to respond — likely with on-device variants leveraging their own model strategies. Pressures every JS library doing client-side ML (transformers.js, Web LLM) on relevance.',
      'positive',
      4,
      'Application',
      ARRAY['chrome', 'web', 'browser', 'on-device', 'summarizer', 'translator', 'prompt-api', 'webmcp', 'standards'],
      'announced',
      'Google I/O 2025',
      NULL
    );
    n := n + 1;
  END IF;

  -- 15. Firebase AI Logic SDK for Unity (preview) — generative AI in games and A
  IF NOT EXISTS (SELECT 1 FROM public.milestones
                WHERE entity_id = eid
                  AND date = '2025-05-21'
                  AND LEFT(event, 60) = 'Firebase AI Logic SDK for Unity (preview) — generative AI in') THEN
    INSERT INTO public.milestones (
      entity_id, date, event, significance, strategic_signal,
      ripple_effects, sentiment_at_time, forward_implication_score,
      stack_layer, tags, claim_type, source_event, displacement_entities
    ) VALUES (
      eid,
      '2025-05-21',
      'Firebase AI Logic SDK for Unity (preview) — generative AI in games and Android XR',
      'Preview SDK enables Unity game developers to integrate generative text, image generation, and the bidirectional streaming Gemini Live API into games and Android XR experiences.',
      'Targets the Unity gamedev ecosystem ahead of Android XR''s consumer launch (anticipated I/O 2026). Game-engine integration is the unglamorous prerequisite for the XR app ecosystem Google needs to compete with Apple Vision Pro and Meta Quest.',
      'Pressures Unreal to ship a comparable Gemini/OpenAI SDK. Sets up the XR-content pipeline Google needs before the glasses ship.',
      'positive',
      3,
      'Developer Tools',
      ARRAY['unity', 'xr', 'android-xr', 'games', 'firebase', 'gemini', 'preview'],
      'announced',
      'Google I/O 2025',
      NULL
    );
    n := n + 1;
  END IF;

  RAISE NOTICE 'Done. Inserted: % of 15 milestones.', n;
END;
$SEED$;
