"""
SINGLE SOURCE OF TRUTH — course metadata for
WSQ Creating Engaging Videos with Generative AI (GenAI), TGS-2024043855.

Every artifact (PPT, LP, LG, LG.md, labs) is generated from this file plus
data_domain1..3.py, so they stay 100% aligned with the assessment:
WA (SAQ) 5 questions cover K1–K5; PP 3 tasks cover A1–A7.
"""

# ------------------------------------------------------------------ metadata
TITLE        = "Creating Engaging Videos with Generative AI (GenAI)"
SHORT_TITLE  = "Creating Engaging Videos with Generative AI (GenAI)"
COURSE_CODE  = "TGS-2024043855"
VERSION      = "v7"
VERSION_DATE = "18 August 2026"
ORG          = "Tertiary Infotech Academy Pte Ltd"
UEN          = "UEN: 201200696W"
TRAINER      = "Dr Alfred Ang"
DAYS         = 2

# ------------------------------------------------------------------ skills framework
TSC_TITLE = "Video Editing"
TSC_CODE  = "MED-MPN-4005-1.1"
TSC_KNOWLEDGE = [
    "K1: Types of quality issues in video content",
    "K2: Types of solutions to rectify quality issues",
    "K3: Parameters to assess video quality",
    "K4: Industry quality standards",
    "K5: Technologies that improve efficiency and quality of video edits",
]
TSC_ABILITIES = [
    "A1: Review scripts to conceptualize the types of edits required to achieve creative vision of production",
    "A2: Develop editing standards and guidelines in accordance to legal requirements and broadcasting standards",
    "A3: Develop work plans to outline the processes and timelines needed for the post production processes",
    "A4: Review edited footage to determine areas of improvement to enhance storytelling",
    "A5: Assess edited footage to ensure alignment with technical and legal requirements",
    "A6: Develop remedial actions for edited footage that does not meet requirements",
    "A7: Evaluate new technologies to improve efficiency and quality of video editing processes",
]

# ------------------------------------------------------------------ outcomes
LEARNING_OUTCOMES = [
    "LO1: Develop video editing strategies and work plans to achieve creative video.",
    "LO2: Assess edited video footage to enhance storytelling and ensure technical compliance.",
    "LO3: Develop remedial actions to ensure industry compliance and facilitate the adoption of new technologies in video editing.",
]

# ------------------------------------------------------------------ topics
TOPICS = [
    dict(num=1, code="01",
         title="Create and Edit Video Script Using Generative AI (GenAI)",
         subtitle="AI script generation · prompt engineering · text-to-video · standards, guidelines & work plans",
         weighting="K1 · A1 · A2 · A3",
         concepts=[
            ("Script writing with GenAI", "Generate ideas, storylines, dialogue and complete video scripts from a prompt."),
            ("The RICCE prompt framework", "Role, Instructions, Context, Constraints, Example — engineer prompts that produce broadcast-ready scripts."),
            ("Story structure", "Hero, desire, obstacle, action, outcome — the elements every engaging video script needs."),
            ("AI text-to-video", "Turn a script into a complete video with VEED's AI Video Maker — scenes, voiceover, captions and music in one pass."),
            ("Standards & guidelines", "Editing standards aligned to legal requirements (copyright, PDPA) and platform/broadcast specs."),
            ("Work plans & timelines", "Plan the production and post-production pipeline with GenAI-drafted work plans."),
         ]),
    dict(num=2, code="02",
         title="Improve Video Footage on GenAI-Powered Video Platforms",
         subtitle="VEED editing essentials · subtitles & captions · audio enhancement · quality assessment",
         weighting="K2 · K3 · A4 · A5",
         concepts=[
            ("Video editing basics", "Trim, split, crop, resize, merge and loop footage on the VEED timeline — no installs, all in the browser."),
            ("Transcripts & captions", "Auto-transcribe speech, generate styled subtitles and closed captions, translate to 100+ languages."),
            ("Audio enhancement", "AI voiceover (text-to-speech), clean audio, background-noise removal and music balancing."),
            ("Fixing quality issues", "Remove cluttered backgrounds, fix framing with smart crop, correct resolution and aspect ratio per platform."),
            ("Assessing footage", "Judge resolution, frame rate, audio levels, visual consistency and pacing against the brief."),
            ("Technical compliance", "Verify the edit meets platform specs and the client's legal and brand requirements before export."),
         ]),
    dict(num=3, code="03",
         title="Apply New AI Technologies to Improve Video Production",
         subtitle="AI avatars & visuals · AI music · voice cloning & dubbing · agentic AI publishing",
         weighting="K4 · K5 · A6 · A7",
         concepts=[
            ("AI avatars", "Photorealistic talking presenters from text — no camera, studio or actor needed."),
            ("AI image & VFX", "Generate images, remove objects and backgrounds, and enhance shots with AI eye contact."),
            ("AI music generation", "Compose custom, royalty-free soundtracks with Suno and Udio from a text prompt."),
            ("Voice cloning & dubbing", "Clone a voice for narration and dub videos into other languages with lip sync."),
            ("Agentic AI publishing", "Let an AI agent draft titles, descriptions and hashtags, then push the video to YouTube and TikTok."),
            ("Evaluating new tech", "Compare AI tools on quality, cost, speed and rights to decide what enters your pipeline."),
         ]),
]

# ------------------------------------------------------------------ the GenAI video pipeline (visual process flow map)
PIPELINE = [
    ("AI-Generated Script", "ChatGPT · Gemini · Claude"),
    ("AI-Generated Video", "VEED · Sora · Kling · Veo"),
    ("AI Voiceover & Music", "TTS · clone · Suno · Udio"),
    ("AI Video Editing", "captions · cleanup · resize"),
    ("Agentic AI Publishing", "YouTube · TikTok"),
]

# ------------------------------------------------------------------ day themes
DAY_THEMES = {
    1: "AI Scripts, Text-to-Video & Editing Essentials",
    2: "Audio, Avatars, Music, Publishing & Assessment",
}

# ------------------------------------------------------------------ assessment
ASSESSMENT = dict(
    written="Written Assessment (WA) — Short-Answer Questions (SAQ), 1 hour, open book.",
    practical="Practical Performance (PP) — hands-on video-production tasks, 1 hour, open book.",
    note="A minimum of 75% attendance is required to be eligible for assessment and funding.",
)
