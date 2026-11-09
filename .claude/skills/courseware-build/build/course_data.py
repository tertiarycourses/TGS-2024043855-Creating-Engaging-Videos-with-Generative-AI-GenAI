"""
SINGLE SOURCE OF TRUTH — course metadata for
WSQ Creating Engaging Videos with Generative AI (GenAI), TGS-2024043855.

v8 (9 Nov 2026): the whole GenAI video pipeline runs inside Higgsfield —
Supercomputer (the agent) and Cinema Studio — replacing the v7 multi-tool
stack (ChatGPT, VEED, Suno, ElevenLabs).

Every artifact (PPT, LP, LG, LG.md, labs) is generated from this file plus
data_domain1..3.py, so they stay aligned with the assessment:
WA (SAQ) 5 questions cover K1–K5; PP 3 tasks cover A1–A7.
Course Proposal (TPG-2024060315) governs LU titles, K/A, durations:
LU1 2 h, LU2 2.5 h, LU3 2.5 h classroom + 7 h practical; WA 1 h + PP 1 h.
"""

# ------------------------------------------------------------------ metadata
TITLE        = "Creating Engaging Videos with Generative AI (GenAI)"
SHORT_TITLE  = "Creating Engaging Videos with Generative AI (GenAI)"
COURSE_CODE  = "TGS-2024043855"
VERSION      = "v11"
VERSION_DATE = "9 November 2026"
ORG          = "Tertiary Infotech Academy Pte Ltd"
UEN          = "UEN: 201200696W"
DAYS         = 2

# ------------------------------------------------------------------ trainer
# Source: linkedin.com/in/hoowee (profile name "Hoo Wee Tay"), read 9 Nov 2026.
TRAINER          = "Mr Tay Hoo Wee"
TRAINER_INITIALS = "TH"
TRAINER_ROLE     = "Producer, Asia Media Alliance\nDirector, Asia Media Academy"
TRAINER_ROWS = [
    ("Current roles", "Producer at Asia Media Alliance (2024–present); Director at Asia Media Academy (2020–present)."),
    ("Film & TV track record", "Team Lead, Camokakis Content (Digital) and Senior Commissioning Editor at So Drama! Entertainment; Executive Producer at Stardust Pictures; VP Physical Productions at Infinite Frameworks Studios."),
    ("Qualifications", "BA (Hons) Digital Film Making, Middlesex University; Diploma in Digital Film Production, SAE Institute Singapore."),
    ("Contact", "linkedin.com/in/hoowee"),
]

# ------------------------------------------------------------------ Higgsfield (the one platform)
HF_SIGNUP   = "https://higgsfield.ai?fpr=alfred-d0d32b"   # trainer's Higgsfield affiliate link
HF_SIGNUP_SHORT = "higgsfield.ai?fpr=alfred-d0d32b"
HF_DISCLOSURE = ("Trainer's affiliate link: the trainer may earn a commission; you pay the normal price.")
HF_PLAN_NOTE = ("Labs run on higgsfield.ai (Supercomputer + Cinema Studio), which needs a paid plan. "
                "On 8 Nov 2026 Plus was US$49/month (US$39 billed yearly) for 1,000 credits. "
                "The free 3-day trial needs a card, renews to Plus unless cancelled within 3 days, "
                "and its credits worked only through the Higgsfield MCP, not on the website.")
HF_TUTORIAL = dict(id="Mt91SiQotOU", title="Higgsfield AI Tutorial for Beginners (2026) | Step-by-Step", author="Metics Media")
HF_DOCS = "https://docs.higgsfield.ai/docs"   # Higgsfield API docs (auth, requests, polling, webhooks, model endpoints)
# Credit facts read from Higgsfield (MCP get_cost / UI) on 8–9 Nov 2026.
CREDITS = dict(draft15=45, hd15=240, sd720_15=105, cs4_5s=80)

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
    "A4: Review edited footage to propose changes that will enhance the story and emotions in each scene",
    "A5: Assess edited footage against technical parameters to ensure alignment to requirements",
    "A6: Develop remedial actions to resolve issues that do not comply with industry standards",
    "A7: Facilitate the adoption of new technologies to improve the efficiency and quality of visual outputs",
]

# ------------------------------------------------------------------ outcomes
LEARNING_OUTCOMES = [
    "LO1: Create video scripts using Generative AI (GAI) and work plans for video production.",
    "LO2: Edit video footage to improve video quality and ensure technical compliance.",
    "LO3: Apply new AI technologies to improve efficiency and quality in accordance to industry standards.",
]

# ------------------------------------------------------------------ topics (CP learning units)
TOPICS = [
    dict(num=1, code="01",
         title="Create and Edit Video Script Using Generative AI (GAI)",
         subtitle="The impact of AI on video · use cases · Supercomputer scripts · AI Director shot lists · standards & work plans",
         weighting="K1 · A1 · A2 · A3",
         concepts=[
            ("AI's impact & use cases", "A US$2,000 TV ad, a 14-day feature: AI movies, micro dramas, influencers, singers and marketing videos already earn audiences."),
            ("The lazy prompt", "Format + vibe gets you a clip in one line, but the model then decides your character, world and camera."),
            ("Scripts with Supercomputer", "Who / where / what happens, then a script and a numbered shot list, drafted and refined in one chat."),
            ("AI Director", "Inside a project, AI Director writes the script and a shot-by-shot storyboard from your brief (Lab 2 asks for six shots)."),
            ("Standards & guidelines", "A one-page sheet: platform specs, consent, licensing, AI disclosure and a Draft-first credit rule."),
            ("Work plans & credit budgets", "Phases, owners, timelines and a credit budget: 45 credits for a 15 s Draft, 240 for the 1080p final."),
         ]),
    dict(num=2, code="02",
         title="Improve Video Footage on GAI Powered Video Platforms",
         subtitle="Elements: characters, locations, props · references · Cinema Studio shots & takes · Draft mode · assess the cut",
         weighting="K2 · K3 · A4 · A5",
         concepts=[
            ("Elements", "Save a character, location or prop once with an @handle and reuse it in every shot: the fix for drifting faces and sets."),
            ("References", "Up to 50 per generation (30 images, 10 videos, 10 audio), each given a role: character, location, camera move or voice."),
            ("Shots & takes", "One continuous shot or multishot with cuts; each run is a take you keep, compare or replace."),
            ("Cinematic controls", "Camera body, lens, aperture, movement, lighting, colour palette, genre, era and tempo."),
            ("Draft mode", "Seedance 2.5 Draft renders 480p for 45 credits; finalise only the take that works at 1080p."),
            ("Assessing footage", "Resolution, continuity, motion, audio, pacing and compliance, judged take by take."),
         ]),
    dict(num=3, code="03",
         title="Apply new AI technologies to Improve Video Production",
         subtitle="Remove & replace objects · cinematic effects · upscale · voice & music · models compared · publish",
         weighting="K4 · K5 · A6 · A7",
         concepts=[
            ("Remove & replace", "Genjutsu Replace Object swaps a product, prop or garment in finished footage, keeping the motion."),
            ("Cinematic effects", "Lighting presets, colour grades and viral effect presets add VFX without a compositor."),
            ("Enhance shots", "Upscale to 1080p or 4K, reframe 16:9 to 9:16, regenerate only the broken shot."),
            ("Voice & music", "Native Seedance audio, a cloned voice for narration and a generated soundtrack."),
            ("Models compared", "Seedance 2.5, Kling 4.0, Cinema Studio 4.0 and Genjutsu: pick per shot on quality, cost and control."),
            ("Publish responsibly", "Export per platform, label synthetic media, clear consent, then share to TikTok or YouTube."),
         ]),
]

# ------------------------------------------------------------------ the pipeline (visual process flow map)
PIPELINE = [
    ("Script & Shot List", "Supercomputer · AI Director"),
    ("Elements", "characters · locations · props"),
    ("Shots & Takes", "Cinema Studio · Seedance 2.5"),
    ("Fix & Finish", "replace · upscale · voice · music"),
    ("Publish", "9:16 + 16:9 · TikTok · YouTube"),
]

# ------------------------------------------------------------------ day themes
DAY_THEMES = {
    1: "Script, Plan, Build Elements, Direct the First Takes",
    2: "Cut, Fix, Finish, Publish & Assessment",
}

# ------------------------------------------------------------------ demo videos (made in Higgsfield for this deck)
DEMO_VIDEOS = [
    dict(key="marketing", title="SOLA: a 15-second product ad",
         file="marketing-sola-15s-h264.mp4", poster="marketing-poster.jpg",
         model="Seedance 2.5 · 1080p · 16:9 · 15 s · native audio · 240 credits",
         shots=["0–3 s  extreme close-up, sun slides across the bottle",
                "3–6 s  runner grabs it mid-stride (tracking)",
                "6–9 s  drink, ice clinks (slow motion)",
                "9–12 s  wide rooftop run, drone pulls back",
                "12–15 s  hero packshot with space for the logo"]),
    dict(key="scifi", title="Ringfall: a 15-second epic sci-fi scene",
         file="scifi-ring-15s-h264.mp4", poster="scifi-poster.jpg",
         model="Seedance 2.5 · 1080p · 16:9 · 15 s · native audio · 240 credits",
         shots=["0–4 s  wide: smoking starship wreck, twin suns",
                "4–8 s  pilot steps out, handheld follow",
                "8–11 s  close-up: awe, ground trembles",
                "11–15 s  extreme wide: the ring rises, crane up"]),
]

LAZY_TEST = dict(key="lazy", title="We ran the lazy prompt: the model chose everything",
    file="lab1-lazy-draft-480p.mp4", poster="lab1-lazy-poster.jpg",
    model="Seedance 2.5 Draft · 480p · 16:9 · 15 s · 45 credits · run 9 Nov 2026",
    shots=["Prompt  'Create a 15-second video of an epic sci-fi scene.'",
           "Character  none: the model left people out",
           "World  abstract space and crystal shards",
           "Camera  a warp-speed fly-through, no story beats",
           "Lesson  brief who / where / what happens (Lab 2)"])

# ------------------------------------------------------------------ core ethical issues (end of Topic 3; owner-supplied list, 9 Nov 2026)
ETHICS = [
    ("Consent and likeness", "Putting real people's faces, voices or movements into training data or digital replicas without permission violates their autonomy and privacy.",
     "Only your own face/voice or people who signed consent; no look-alikes of real people."),
    ("Intellectual property and creator rights", "Models trained on copyrighted film, art and styles without permission or payment face lawsuits from studios and independent creators.",
     "No real brands, songs or characters without a licence; credit owners; check your plan's commercial rights."),
    ("Deepfakes and misinformation", "Hyper-realistic synthetic video enables political manipulation, fake news and non-consensual media, eroding trust in visual evidence.",
     "Never depict real people saying or doing things they did not; never make 'news' footage."),
    ("Economic displacement", "Automation in video production, storyboarding and VFX threatens jobs across the creative industries.",
     "Use AI to extend a crew, not to pass off AI work as a person's; credit the humans who direct and edit."),
    ("Algorithmic bias and representation", "Training data encodes historical, racial and gender stereotypes that generators can reproduce.",
     "Review every cast for stereotypes; specify diverse, respectful characters in the prompt."),
    ("Environmental impact", "Training and running large video models consumes large amounts of electricity and water in data centres.",
     "Draft at 480p first; finalise only the take you will use; delete failed batches, not just hide them."),
    ("Transparency and authenticity", "Presenting synthetic video as genuine, or not labelling it, deceives viewers and blurs reality.",
     "Turn on the platform's AI-generated label; say 'made with AI' in captions or credits."),
]

# Real cases for each issue — verified 9 Nov 2026 (source in the last field).
ETHICS_CASES = [
    ("Consent and likeness", "Scarlett Johansson v. OpenAI 'Sky' (May 2024)",
     "She declined to voice ChatGPT; OpenAI shipped a voice that sounded like her, then paused it after her lawyers wrote.", "CNBC, Variety, 20 May 2024"),
    ("Consent and likeness", "Bryan Cranston, SAG-AFTRA and Sora 2 (Oct 2025)",
     "Unauthorised clips of his voice and likeness appeared after Sora 2 launched; OpenAI agreed opt-in protections with the union.", "CNBC, 20 Oct 2025"),
    ("Intellectual property", "Disney and Universal v. Midjourney (June 2025)",
     "Hollywood's first AI copyright suit: the studios call the image generator 'a bottomless pit of plagiarism' for copying Darth Vader, Elsa and the Minions.", "CNBC, Reuters, 11 Jun 2025"),
    ("Deepfakes and fraud", "Arup deepfake video call, Hong Kong (Jan 2024)",
     "A finance worker joined a video call with a deepfaked CFO and colleagues and paid out HK$200 million (about US$25.6 million) in 15 transfers.", "CNN, 17 May 2024"),
    ("Deepfakes and elections", "Singapore bans election deepfakes (Oct 2024)",
     "The Elections (Integrity of Online Advertising) (Amendment) Act bans realistic fakes of candidates during elections; first applied at GE2025.", "CNA, 15 Oct 2024"),
    ("Economic displacement", "SAG-AFTRA strike (2023, 118 days)",
     "Actors struck partly over AI; the deal requires consent and pay for digital replicas. A video-game strike over AI followed in July 2024.", "Authors Guild; LA Times"),
    ("Bias and representation", "Google pauses Gemini images of people (Feb 2024)",
     "Gemini produced historically inaccurate depictions of people; Google paused people images and apologised.", "TechCrunch; Google blog, 22–23 Feb 2024"),
    ("Environmental impact", "Google 2024 Environmental Report (Jul 2024)",
     "Emissions 48% higher in 2023 than 2019, driven by data-centre energy for AI.", "BBC, Bloomberg, 2 Jul 2024"),
    ("Transparency", "TikTok auto-labels AI content (May 2024)",
     "First video platform to read C2PA Content Credentials and label AI-made videos, including those made elsewhere.", "CNBC, NBC News, 9 May 2024"),
]

# ------------------------------------------------------------------ assessment
ASSESSMENT = dict(
    written="Written Assessment (WA) — Short-Answer Questions (SAQ), 1 hour, open book.",
    practical="Practical Performance (PP) — three Higgsfield production tasks, 1 hour, open book; paste screenshots under each task and upload your final video to the TMS.",
    note="A minimum of 75% attendance is required to be eligible for assessment and funding.",
)
