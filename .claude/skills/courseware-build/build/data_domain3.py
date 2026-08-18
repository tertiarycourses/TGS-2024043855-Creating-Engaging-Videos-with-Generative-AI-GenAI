"""Topic 3 — Apply New AI Technologies to Improve Video Production. Labs 9–12."""

DOMAIN3 = [
    dict(
        num=9, topic=3,
        title="AI Avatars, AI Images & Eye Contact",
        objective="K5, A7 — apply and evaluate new AI production technologies",
        desc="Produce presenter-led video without a camera: generate a talking AI avatar from your script, "
             "create supporting visuals with the AI image generator, and fix off-camera gaze on recorded "
             "clips with AI eye contact correction.",
        build="An avatar-presented video with AI-generated imagery, plus an eye-contact-corrected webcam clip.",
        services="VEED AI Avatars, AI Image Generator, AI Eye Contact",
        flow=['Pick or create an avatar', 'Generate the talking clip', 'Create AI b-roll images', 'Fix gaze with AI Eye Contact', 'Assemble, caption, export'],
        steps=[
            ("In VEED, open AI Avatars and browse the avatar library (or create a personal avatar from a short webcam recording).", ""),
            ("Paste a 30-second section of your script, choose the avatar's voice and language, and generate the talking-head clip.", ""),
            ("Use the AI Image Generator to create two supporting visuals for your topic, and cut them in as b-roll over the avatar's narration.", ""),
            ("Record a 15-second webcam clip while reading from notes (eyes off-camera), then apply AI Eye Contact and compare the corrected gaze.", ""),
            ("Assemble avatar + b-roll + captions into one sequence and export.", ""),
            ("Evaluate (A7): note where an avatar beats filming a human (speed, cost, consistency, translation) and where it falls short (authenticity, emotion).", ""),
        ],
        prompts=[
            ("Avatar script",
             "Condense this script to a 30-second avatar narration: first person, friendly-expert tone, short sentences with natural pauses, no stage directions."),
            ("B-roll images",
             "Generate an image: isometric illustration of a video production pipeline — script, camera, waveform, play button — clean flat style, teal and blue palette, no text."),
        ],
        test="The avatar's lip sync matches the narration, the AI images support the message, and the "
             "eye-contact clip looks naturally at camera.",
    ),
    dict(
        num=10, topic=3,
        title="AI Music Generation with Suno & Udio",
        objective="K5, A7 — generate custom soundtracks and evaluate the tools",
        desc="Compose custom, royalty-free music for your videos: write a music prompt (genre, mood, tempo, "
             "instrumentation), generate tracks on Suno and Udio, and pick and place the best track under "
             "your video with correct levels.",
        build="Two AI-composed soundtrack candidates (Suno + Udio) and your video re-scored with the winner.",
        services="Suno (suno.ai), Udio (udio.com), VEED",
        flow=['Write the music prompt', 'Generate on Suno', 'Generate on Udio', 'Audition against the cut', 'Place, mix and check rights'],
        steps=[
            ("Sign in at suno.ai, describe the track you need (genre, mood, tempo, instruments, no vocals) and generate two candidates.", ""),
            ("Repeat the same prompt on udio.com and generate two more candidates.", ""),
            ("Audition all four against your video's pacing: does the energy match the cut points and the call-to-action?", ""),
            ("Download the winner, import it into your VEED project, and place it under the voiceover at ~20% volume with a fade-out at the end.", ""),
            ("Check rights: confirm the plan you used grants commercial use of the generated track.", ""),
            ("Compare Suno vs Udio (A7): quality, control, speed, licensing — record which you would adopt and why.", ""),
        ],
        prompts=[
            ("Music prompt",
             "Uplifting corporate pop instrumental, 100 BPM, warm piano and soft synths building to a bright chorus, optimistic and modern, no vocals, 60 seconds, clean ending."),
            ("Mood variation",
             "Same track but calmer: acoustic guitar led, gentle percussion, morning-light feel, suitable under a spoken voiceover."),
        ],
        test="The chosen track matches the video's mood and pacing, sits under the voiceover without "
             "masking speech, and you can state its usage rights.",
    ),
    dict(
        num=11, topic=3,
        title="Voice Cloning, AI Dubbing & Lip Sync",
        objective="K5, A7 — clone voices, dub languages and evaluate ethics/quality",
        desc="Give your videos a consistent voice at scale: clone your own voice from a short sample, "
             "narrate a script with the clone, then auto-dub a video into another language with translated "
             "audio and lip-synced delivery.",
        build="A voiceover in your own cloned voice, and a dubbed version of your video in a second language.",
        services="VEED Voice Clone & Dubbing, ElevenLabs, Sync Labs / D-ID (explore)",
        flow=['Record a clean voice sample', 'Clone your voice', 'Narrate with the clone', 'Auto-dub a second language', 'Check lip sync and ethics'],
        steps=[
            ("Record a clean 30–60 s voice sample (quiet room, natural pace) — consent and disclosure rules apply to any voice you clone; clone ONLY your own voice in class.", ""),
            ("Create the clone (VEED voice cloning or elevenlabs.io) and generate your Lab 1 script in your cloned voice.", ""),
            ("Compare the cloned narration with the stock TTS voice from Lab 7 — naturalness, pacing, pronunciation of local terms.", ""),
            ("Auto-dub: take your finished video and use VEED's dubbing to translate the audio into Mandarin/Malay/Spanish, keeping your voice character.", ""),
            ("Check the lip sync on the dubbed clip; explore D-ID or Sync Labs to lip-sync a still portrait to your cloned audio.", ""),
            ("Evaluate (A7): where do cloning/dubbing add value (multilingual reach, consistency), and what are the ethical red lines (consent, deepfake misuse, disclosure)?", ""),
        ],
        prompts=[
            ("Dub-ready rewrite",
             "Rewrite this narration for dubbing into Mandarin: avoid idioms and wordplay, keep sentences short, keep brand names in English, target the same 45-second duration."),
        ],
        test="The cloned voice is recognisably yours and pronounces the script cleanly; the dubbed video "
             "plays in the second language with acceptable lip sync; you can state the consent rule for cloning.",
    ),
    dict(
        num=12, topic=3,
        title="Agentic AI Publishing to YouTube & TikTok",
        objective="A7 — adopt agentic AI to close the pipeline from edit to publish",
        desc="Close the GenAI video pipeline with an agentic step: export platform-ready cuts, then let an "
             "AI agent draft the title, description, hashtags and thumbnail concept, and push the video to "
             "YouTube and TikTok — scheduling included — while you stay in review control.",
        build="Your video live (unlisted) on YouTube and/or TikTok, published via an agent-assisted workflow with AI-drafted metadata.",
        services="VEED export, ChatGPT/Claude (agent), YouTube Studio, TikTok, n8n/Zapier (optional)",
        flow=['Export 16:9 and 9:16 cuts', 'Agent drafts the publishing kit', 'You approve every item', 'Upload and schedule posts', 'Verify live and reflect'],
        steps=[
            ("Export two cuts from VEED: 16:9 1080p for YouTube and 9:16 for TikTok/Shorts, captions burned in for the vertical cut.", ""),
            ("Ask an AI agent to draft the publishing kit: SEO title options, description with timestamps and links, 10 hashtags per platform, and a thumbnail concept.", ""),
            ("Generate the thumbnail with the AI image generator from the agent's concept, and review the full kit — you approve every word before it ships.", ""),
            ("Publish to YouTube: upload the 16:9 cut in YouTube Studio (set to Unlisted for class), paste the agent's title/description/tags, upload the thumbnail, and schedule the release time the agent recommends.", ""),
            ("Publish to TikTok: upload the 9:16 cut, apply the agent's caption and hashtags, and schedule at the recommended engagement window.", ""),
            ("Optional — automate: wire an n8n/Zapier flow (or a computer-use agent) that watches a Drive folder and performs the upload + metadata steps automatically, keeping a human-approval gate before anything goes live.", ""),
            ("Verify both posts, then reflect: which pipeline stages (script → video → audio → edit → publish) are now AI-assisted, and where must a human stay in the loop?", ""),
        ],
        prompts=[
            ("Publishing kit",
             "You are my publishing agent. For this 45-second video promoting an online learning platform, produce: 3 SEO YouTube title options under 60 characters, a 2-paragraph description with a call-to-action and link placeholder, 10 YouTube tags, a TikTok caption under 150 characters with 5 hashtags, a thumbnail concept (composition, text overlay, colours), and the best posting time for the Singapore audience. Present it as a checklist I can approve item by item."),
            ("Agentic automation spec",
             "Design an n8n workflow that: watches a Google Drive folder for a new MP4, drafts YouTube metadata with an LLM node, waits for my approval via email, then uploads to YouTube with the approved metadata and posts the link to Slack. List the nodes and the data passed between them."),
        ],
        test="The video is live (unlisted) on at least one platform with agent-drafted, human-approved "
             "metadata, and you can describe where the approval gate sits in the agentic flow.",
    ),
]
