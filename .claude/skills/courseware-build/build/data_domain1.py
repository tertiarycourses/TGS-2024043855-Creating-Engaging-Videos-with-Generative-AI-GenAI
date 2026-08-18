"""Topic 1 — Create and Edit Video Script Using Generative AI (GenAI).
Labs 1–4. Each activity carries `steps` (rendered in the Learner Guide and the
lab folder ONLY — never as step-by-step slides) and `prompts` (example GenAI
prompts, rendered on the PPT prompt slide AND in the Learner Guide)."""

DOMAIN1 = [
    dict(
        num=1, topic=1,
        title="Generate a Video Script with the RICCE Framework",
        objective="A1 — review scripts and conceptualise the edits needed to achieve the creative vision",
        desc="Use the RICCE prompt framework (Role, Instructions, Context, Constraints, Example) "
             "with a text GenAI tool — ChatGPT, Gemini, Claude or Copilot — to generate a complete, "
             "engaging video script, then review and refine it for the target platform.",
        build="A polished 60–90 second video script with scene directions, dialogue and a hook, ready for production.",
        services="ChatGPT, Gemini, Claude, Copilot",
        flow=['Open a text GenAI tool', 'Draft the RICCE prompt', 'Review against story elements', 'Iterate hook, dialogue, CTA', 'Format as VISUAL / AUDIO table'],
        steps=[
            ("Open a text GenAI tool — chatgpt.com, gemini.google.com, claude.ai or copilot.microsoft.com — and sign in.", ""),
            ("Draft your RICCE prompt: define the Role (expert scriptwriter), Instructions (write a 60-second promo script), Context (product, audience, platform), Constraints (length, tone, format) and an Example of the output structure.", ""),
            ("Submit the prompt and review the generated script against the story elements: identifiable hero, clear desire, obstacle, action, outcome.", ""),
            ("Iterate: ask the AI to strengthen the hook in the first 3 seconds, tighten the dialogue, and add a clear call-to-action.", ""),
            ("Ask the AI to reformat the script as a two-column table — VISUAL (what we see) and AUDIO (voiceover/dialogue) — the standard video script format.", ""),
            ("Tailor the same script for a second platform (e.g. a 30-second vertical TikTok cut) and compare how pacing and style change.", ""),
            ("Save the final script to a document — you will use it in Lab 3 to generate the video.", ""),
        ],
        prompts=[
            ("RICCE — full script prompt",
             "ROLE: You are an award-winning video scriptwriter for social media marketing.\n"
             "INSTRUCTIONS: Write a 60-second promotional video script for an online learning platform.\n"
             "CONTEXT: The audience is working adults in Singapore aged 25–45 considering upskilling; the video runs on YouTube and Instagram.\n"
             "CONSTRAINTS: Max 150 words of voiceover. Hook in the first 3 seconds. Conversational tone. End with the call-to-action 'Start learning today'.\n"
             "EXAMPLE: Format as a table with columns SCENE, VISUAL, VOICEOVER, ON-SCREEN TEXT."),
            ("Refine the hook",
             "Rewrite the first scene so the opening 3 seconds create curiosity — start with a surprising question or statistic about career growth."),
            ("Platform re-cut",
             "Adapt this script into a 30-second vertical TikTok version: faster pacing, punchier lines, captions-first, keep the same call-to-action."),
        ],
        test="The script has a hook in the first 3 seconds, a clear hero/desire/obstacle/resolution arc, "
             "fits the 60–90 s duration, and is formatted in the two-column VISUAL/AUDIO layout.",
    ),
    dict(
        num=2, topic=1,
        title="Build Story-Driven Scripts with Prompt Templates & Custom GPTs",
        objective="A1 — conceptualise script edits; K1 — recognise script-level quality issues",
        desc="Use the six-step story prompt template (genre → protagonist → antagonist → conflict → "
             "setting → plot beats) to co-write a story-driven script step by step, then compare the "
             "result with a purpose-built custom GPT script writer.",
        build="A story-driven video script built beat-by-beat, plus a second version from a custom GPT for comparison.",
        services="ChatGPT (custom GPTs), Gemini, Claude",
        flow=['Set the genre', 'Define hero, obstacle, conflict', 'Set the setting and tone', 'Generate 5 beats, then script', 'Compare with a custom GPT'],
        steps=[
            ("Start a new chat and set the genre: tell the AI what kind of story you are writing (sci-fi, comedy, thriller, brand story).", ""),
            ("Define the protagonist — name, age, occupation, personality and goal — in one prompt.", ""),
            ("Define the antagonist (or the obstacle) — who or what stands in the way, and their motivation.", ""),
            ("Define the conflict — how the protagonist and the obstacle collide.", ""),
            ("Define the setting — time, location and tone of the story.", ""),
            ("Ask the AI to generate five plot points that escalate the conflict to a climax, then expand them into a full script.", ""),
            ("Open a custom GPT script writer (e.g. 'Video Script Writer' in the GPT Store) and give it the same brief; compare structure, pacing and dialogue between the two versions.", ""),
            ("Pick the stronger version, note the script-level quality issues you fixed (weak hook, vague hero, no resolution), and save it.", ""),
        ],
        prompts=[
            ("Six-step template (steps 1–5 combined)",
             "We are co-writing a video story script.\n"
             "GENRE: heartwarming brand story.\n"
             "PROTAGONIST: Sarah, 32, a nurse who dreams of switching into tech but has no time to study.\n"
             "OBSTACLE: 12-hour shifts and self-doubt.\n"
             "CONFLICT: every course she tries demands rigid schedules she cannot keep.\n"
             "SETTING: present-day Singapore, hopeful and warm tone."),
            ("Plot beats",
             "Generate five plot points that escalate Sarah's conflict to a climax and resolve it when she discovers a flexible online academy. Then expand the five beats into a 90-second script in VISUAL/AUDIO table format."),
            ("Critique prompt",
             "Act as a script editor. Critique this script for: weak hook, unclear protagonist desire, missing obstacle, flat resolution. List each issue and rewrite the weakest scene."),
        ],
        test="You can show both script versions, name at least three script-level quality issues you identified, "
             "and explain which version you chose for production and why.",
    ),
    dict(
        num=3, topic=1,
        title="AI Text-to-Video with VEED",
        objective="A1, A7 — turn a script into a video with an AI video generator",
        desc="Turn your Lab 1 script into a complete video with VEED's AI Video Maker: describe the video, "
             "let AI generate the scenes, voiceover, captions and music, then customise it in the editor. "
             "VEED's generator taps models such as Veo, Sora, Kling and Hailuo for the visuals.",
        build="A complete AI-generated 30–60 s video with scenes, AI voiceover, captions and background music.",
        services="VEED AI Video Maker (veed.io/tools/ai-video), ChatGPT",
        flow=['Open VEED AI Video Maker', 'Describe: paste your script', 'Customize ratio, voice, captions', 'Generate, then refine scenes', 'Export 1080p and share'],
        steps=[
            ("Sign in at veed.io and open Tools → AI Video → AI Video Maker.", ""),
            ("DESCRIBE: choose the video type (promo/explainer/social clip), paste your Lab 1 script or a one-line description of the topic, and let AI draft the storyboard.", ""),
            ("CUSTOMIZE: set the aspect ratio (16:9 for YouTube, 9:16 for TikTok/Shorts), pick an AI voice for the narration, and toggle subtitles on.", ""),
            ("Generate the video and watch the AI assemble scenes, voiceover, captions and music.", ""),
            ("Open the result in the VEED editor: swap any scene you dislike with stock footage or an AI-generated clip, and adjust the music volume under the voiceover.", ""),
            ("Export the video in 1080p and share the link with the class on Google Classroom.", ""),
            ("Optional: repeat the generation on CapCut Web and compare output quality, control and speed with VEED.", ""),
        ],
        prompts=[
            ("Text-to-video description",
             "Create a 45-second upbeat promotional video for an online learning platform. Modern, bright visuals of working adults learning on laptops and phones; energetic female voiceover; bold captions; end on the text 'Start learning today'."),
            ("Scene swap",
             "Generate a 5-second b-roll clip: close-up of hands typing on a laptop in a cosy café, warm morning light, shallow depth of field."),
        ],
        test="The exported video plays end-to-end with synchronised voiceover, captions and music, in the "
             "correct aspect ratio for the chosen platform.",
    ),
    dict(
        num=4, topic=1,
        title="Develop Video Standards, Guidelines & a Production Work Plan",
        objective="A2, A3 — develop editing standards/guidelines and post-production work plans",
        desc="Use GenAI to draft the two documents every production needs: (1) an editing standards & "
             "guidelines sheet aligned to legal requirements (copyright, PDPA, platform rules) and "
             "broadcast standards, and (2) a work plan with timelines for the post-production process.",
        build="A one-page editing standards & guidelines document and a phased post-production work plan with timelines.",
        services="ChatGPT, Gemini, Claude",
        flow=['Draft editing standards with AI', 'Add legal compliance rules', 'Review and brand the draft', 'Build the phased work plan', 'Convert to a 5-day timeline'],
        steps=[
            ("Prompt the AI to draft video editing standards covering: resolution & frame rate, aspect ratios per platform, caption style, audio loudness, branding, and music licensing.", ""),
            ("Extend the standards with legal compliance: copyright and licensing of footage/music, PDPA/consent for people appearing on camera, platform community guidelines, and IMDA advertising codes.", ""),
            ("Review the AI draft critically — remove anything irrelevant to your production and add your organisation's brand rules.", ""),
            ("Prompt the AI to build a post-production work plan: phases (script lock → asset generation → edit → review → export → publish), owner, duration and dependencies for each.", ""),
            ("Ask the AI to convert the work plan into a timeline table for a 5-day turnaround, with buffer for client review.", ""),
            ("Save both documents — they are your quality benchmark when you assess footage in Topic 2.", ""),
        ],
        prompts=[
            ("Editing standards",
             "Draft a one-page video editing standards & guidelines sheet for a Singapore digital media agency producing social videos. Cover: technical specs (resolution, frame rate, aspect ratio per platform), caption and subtitle style, audio loudness targets, brand usage, and legal compliance (music/footage licensing, PDPA consent, platform rules). Format as a table."),
            ("Work plan",
             "Create a post-production work plan for a 60-second promo video due in 5 working days. Phases: script lock, AI asset generation, editing, internal review, client review, final export, publishing. For each phase give owner, duration, dependencies and deliverable. Format as a timeline table."),
        ],
        test="The standards sheet names concrete technical specs and at least three legal/compliance rules; "
             "the work plan covers every phase to publishing with durations that sum to the 5-day deadline.",
    ),
]
