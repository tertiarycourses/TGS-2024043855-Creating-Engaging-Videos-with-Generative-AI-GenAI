"""Topic 2 — Improve Video Footage on GenAI-Powered Video Platforms. Labs 5–8."""

DOMAIN2 = [
    dict(
        num=5, topic=2,
        title="VEED Video Editing Essentials",
        objective="K2 — solutions that rectify quality issues; A4 — review footage for improvement",
        desc="Master the VEED browser editor: upload or record footage, then trim, split, crop, resize, "
             "merge and loop clips on the timeline, add photos, text overlays and music, and start from "
             "professional templates.",
        build="An edited multi-clip video with text overlays, images and background music, assembled on the VEED timeline.",
        services="VEED Video Editor (veed.io/create/video-maker)",
        flow=['Start a VEED project', 'Upload or record clips', 'Trim, split and reorder', 'Crop, resize, add media', 'Preview and export 1080p'],
        steps=[
            ("Open veed.io → Create → Video Maker and start a new project (or pick a template from veed.io/templates).", ""),
            ("Upload two or three short clips (or record with the built-in webcam/screen recorder).", ""),
            ("Trim each clip on the timeline: drag the clip edges to remove dead air at the start and end.", ""),
            ("Split a clip: place the playhead mid-clip and hit Split; delete the section you don't need, then reorder clips by dragging.", ""),
            ("Crop and resize: use Smart Crop to reframe the subject, and set the project size (16:9, 9:16, 1:1) from the canvas settings.", ""),
            ("Add media: drop in a photo/logo, add a text overlay title with an animation, and add background music from the stock library.", ""),
            ("Loop or merge: loop a short b-roll clip to cover the voiceover, and confirm the merged sequence flows without jump cuts.", ""),
            ("Preview the full timeline, then export at 1080p.", ""),
        ],
        prompts=[
            ("Ask AI for an edit plan",
             "Here is my raw footage list: [describe your clips]. Propose an edit sequence for a 45-second video: which clip opens, where to cut, what text overlays to add, and where the music should swell."),
        ],
        test="The exported video contains at least three clips trimmed and ordered cleanly, a text overlay, "
             "an image, and music — with no black gaps or jump cuts on the timeline.",
    ),
    dict(
        num=6, topic=2,
        title="Auto Subtitles, Captions, Transcripts & Translation",
        objective="K2, A4 — fix accessibility/quality gaps with AI captioning",
        desc="Make any video accessible and social-ready: auto-generate subtitles with AI speech "
             "recognition, style them as animated captions, download the transcript, and translate "
             "subtitles into other languages.",
        build="A captioned video with styled, animated subtitles, a downloadable transcript, and a translated subtitle track.",
        services="VEED Subtitles & Translation",
        flow=['Open your project in VEED', 'Auto-generate subtitles', 'Proof-read and fix errors', 'Style captions, get transcript', 'Translate and export'],
        steps=[
            ("Open your Lab 5 project (or upload any talking video) in VEED.", ""),
            ("Go to Subtitles → Auto Subtitles, pick the spoken language, and let the AI transcribe the audio.", ""),
            ("Proof-read the generated subtitles in the side panel and fix any misheard words — names and jargon are the usual suspects.", ""),
            ("Style the captions: choose a caption preset (word-by-word highlight for social), set font, size, colour and position safe for 9:16.", ""),
            ("Download the transcript (TXT/SRT/VTT) from the subtitles panel.", ""),
            ("Translate: duplicate the subtitle track and auto-translate it (e.g. to Chinese or Malay); review the translation quality.", ""),
            ("Export the captioned video and compare engagement value against the uncaptioned original.", ""),
        ],
        prompts=[
            ("Polish the transcript",
             "Clean up this auto-generated transcript: fix punctuation and casing, correct obvious mis-transcriptions, and split it into subtitle lines of max 42 characters without breaking phrases."),
        ],
        test="Captions are accurate and synchronised, styled legibly for mobile, the transcript downloads "
             "cleanly, and a second-language subtitle track exists.",
    ),
    dict(
        num=7, topic=2,
        title="AI Voiceover, Clean Audio & Background Removal",
        objective="K2 — audio/visual fixes; A4, A5 — review and assess footage",
        desc="Fix the two problems that sink most videos — bad audio and cluttered visuals. Generate an AI "
             "text-to-speech voiceover, clean background noise from recorded audio, and remove or replace "
             "a distracting video background without a green screen.",
        build="A video with a professional AI voiceover, denoised audio and a clean replaced background.",
        services="VEED Text-to-Speech, Clean Audio, Background Remover",
        flow=['Generate the TTS voiceover', 'Align and duck the music', 'Clean noisy audio', 'Remove, replace background', 'Export and note fixes'],
        steps=[
            ("In your VEED project, open Audio → Text to Speech; paste your script, choose a voice (accent, gender, tone) and generate the voiceover track.", ""),
            ("Align the voiceover on the timeline and duck the music: lower music volume to ~20% under speech.", ""),
            ("Record (or upload) a webcam clip with room noise, then enable Clean Audio to strip background noise and compare before/after.", ""),
            ("Select the webcam clip and toggle Remove Background — the AI mattes you out without a green screen.", ""),
            ("Replace the background: drop in a brand-coloured background, an office image, or an AI-generated scene behind the cut-out.", ""),
            ("Check lighting/edge artefacts on the matte; if edges shimmer, try a simpler background or better-lit source clip.", ""),
            ("Export and note the quality issues you fixed (noise, clutter) and the solutions applied — this is exactly what the WA asks you to explain.", ""),
        ],
        prompts=[
            ("Voiceover script tone",
             "Rewrite this script for text-to-speech narration: short sentences, natural spoken rhythm, no brackets or symbols the TTS would read aloud, warm confident tone."),
            ("Background scene",
             "Generate an image: modern minimalist studio backdrop in soft teal gradient, subtle depth, no text, suitable as a video call background."),
        ],
        test="The voiceover is clear and correctly timed, background noise is audibly reduced, and the "
             "replaced background has clean edges around the presenter.",
    ),
    dict(
        num=8, topic=2,
        title="Mini Project — Assess and Fix Video Quality",
        objective="K1, K3, A4, A5, A6 — assess footage against parameters and remediate",
        desc="Bring it together: assess a flawed video against objective quality parameters (resolution, "
             "frame rate, audio levels, consistency, pacing, captions), diagnose its issues, plan remedial "
             "actions, and fix it on VEED to meet the standards sheet you wrote in Lab 4.",
        build="A quality-assessment checklist with findings, plus the remediated video that passes your own standards.",
        services="VEED, ChatGPT (assessment checklist)",
        flow=['Screen the rough cut', 'Score the quality checklist', 'Map issues to remedies', 'Apply the fixes on VEED', 'Re-screen until all pass'],
        steps=[
            ("Take a deliberately rough cut (your Lab 5 export, or the trainer's sample) and screen it end-to-end once without touching anything.", ""),
            ("Score it against the assessment parameters: resolution & sharpness, aspect ratio, frame-rate smoothness, audio levels & noise, colour/visual consistency, pacing, caption accuracy, brand & legal compliance.", ""),
            ("List every failed parameter as a quality issue, and match each issue to a remedial action (K1 → K2 mapping) — e.g. cluttered background → background removal; low voice → duck music + boost voice.", ""),
            ("Apply the fixes on VEED: re-crop, clean audio, restyle captions, replace the weak opening shot, tighten pacing by cutting dead sections.", ""),
            ("Re-screen the fixed video against the same checklist and against your Lab 4 standards sheet until every parameter passes.", ""),
            ("Export the final video and keep the before/after checklist — it is your evidence of A5/A6 competence.", ""),
        ],
        prompts=[
            ("Generate the checklist",
             "Create a video quality-assessment checklist with pass/fail criteria for: resolution, aspect ratio, frame rate, audio loudness and noise, visual consistency, pacing, caption accuracy, branding, and legal compliance. Format as a table I can score a video against."),
            ("Diagnose from description",
             "My video has: muffled voice under loud music, captions that lag the speech, and a washed-out opening shot. For each issue, state the likely cause and the fastest fix in an online editor."),
        ],
        test="You can present the scored checklist (before and after), name each issue and its remedial "
             "action, and the fixed video passes every parameter including your Lab 4 standards.",
    ),
]
