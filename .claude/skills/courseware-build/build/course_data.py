"""
v12 (23 Nov 2026): restructured to story -> shoot -> edit. Topic 1 story, hooks and storyboard
(Activity 1); Topic 2 cinematic technique in Higgsfield (Activity 2); Topic 3 post-production
in CapCut and ethics (Activity 3). PP = one screenshot per activity.

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
VERSION      = "v12"
VERSION_DATE = "23 November 2026"
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

# Free-to-start alternative (owner request, 23 Nov 2026; observation from the reference deck courseware/reference/Roger.pptx).
VIDOGRID_URL = "https://vidogrid.ai"
VIDOGRID_NOTE = ("vidogrid.ai is free to start: make 480p test takes with the same storyboard prompt. "
                 "Check the cost on the Generate button (observed 23 Nov 2026).")

# SkillsFuture free AI subscription (owner request, 23 Nov 2026). Source: MySkillsFuture 'Redeem AI Subscription',
# last updated 21 Oct 2026. Eligibility depends on the course carrying the 'Free AI sub' label: confirm before claiming it.
FREE_AI_SUB = [
    ("Google AI Pro (Gemini Pro)", "Gemini, Nano Banana Pro images and Omni for video and creative assets; 4x higher limits than free."),
    ("Singtel AI Pass", "Hailuo AI and AKOOL for video, MiniMax Audio for voice and music, Canva, Otter.ai, Manus: all for 3 months, then one tool for 3 more."),
    ("Also on the list", "ChatGPT Plus, Manus AI (8,000 credits a month) and Microsoft 365 Personal with Copilot."),
    ("Who qualifies", "Singapore Citizens aged 18+, after an eligible course labelled 'Free AI sub' on MySkillsFuture (ending 16 Sep 2026 or later). One per person; redeem within 60 days of the email."),
]
FREE_AI_SUB_URL = "myskillsfuture.gov.sg → Redeem AI Subscription"

# ------------------------------------------------------------------ CapCut (post-production, Topic 3)
CAPCUT_URL = "https://www.capcut.com"
CAPCUT_NOTE = ("CapCut desktop (free download from capcut.com; read on CapCut 9.7.1 for Mac, 23 Nov 2026). "
               "The editor's tabs: Media, Audio, Text, Stickers, Effects, Transitions, Captions, Filters, Adjustment; "
               "some tools and effects are marked Pro (paid).")

# ------------------------------------------------------------------ topics (CP learning units)
TOPICS = [
    dict(num=1, code="01",
         title="Create and Edit Video Script Using Generative AI (GAI)",
         subtitle="What makes a video engaging · hooks · one message · characters · storytelling · script and storyboard with GenAI",
         weighting="K1 · A1 · A2 · A3",
         concepts=[
            ("The hook", "Up to 47% of a video ad's value lands in the first 3 seconds (Meta with Nielsen, 2016). Earn the next second."),
            ("One message", "One sentence the viewer must remember: who it is for, what changes, why now."),
            ("A character", "A face with a want and a problem. Viewers follow people, not product features."),
            ("A 15-second story", "Hook, problem, turn, payoff, call to action: five beats, three seconds each."),
            ("Show, don't say", "Shot size, sound, on-screen text and pace carry the message without a voice-over."),
            ("The storyboard", "Panel by panel: time, shot, angle, action, sound, on-screen text. Plan it before you spend a credit."),
         ]),
    dict(num=2, code="02",
         title="Improve Video Footage on GAI Powered Video Platforms",
         subtitle="Shot sizes · camera angles · camera movement · light, colour and lens · cinematic effects · Higgsfield characters and storyboard prompts",
         weighting="K2 · K3 · A4 · A5",
         concepts=[
            ("Shot sizes", "Extreme wide to extreme close-up: each size tells the viewer what to read."),
            ("Camera angles", "Low makes a hero, high makes a victim, Dutch makes trouble, POV puts us inside."),
            ("Camera movement", "Push-in for emotion, tracking for energy, crane for scale, handheld for urgency."),
            ("Light, colour, lens", "Golden hour, silhouette, shallow focus and a colour grade set the mood in one line of prompt."),
            ("Characters as Elements", "Build the cast once in Higgsfield, save it with an @handle, reuse it in every shot."),
            ("Prompt the storyboard", "One storyboard panel becomes one prompt line: time, size, angle, move, action, sound."),
         ]),
    dict(num=3, code="03",
         title="Apply new AI technologies to Improve Video Production",
         subtitle="Post-production in CapCut · what to cut when it runs long · captions, music, colour · quality checks · export · ethics",
         weighting="K4 · K5 · A6 · A7",
         concepts=[
            ("The edit", "Generated clips are raw footage. The story is written a second time on the CapCut timeline."),
            ("Too long? Cut it", "Cut logo intros, warm-ups, repeats and dead air first; keep hook, message, payoff and CTA."),
            ("Polish", "Auto captions, a hook line in 0–3 s, music under the action, one colour look, few transitions."),
            ("Fix and finish with AI", "Remove objects, add VFX, clone a voice with consent, generate music and voice-over, enhance audio; regenerate one shot when CapCut cannot fix it."),
            ("Export to standard", "1080p, 30 fps, MP4; 9:16 for TikTok, Reels and Shorts; 16:9 for YouTube; AI label on."),
            ("Ethics", "Copyright and IP, consent, bias, deepfakes, transparency: the last check before you publish."),
         ]),
]

# LMS subtopics (lms_push.py --units-from reads TOPICS[i]["items"]): the key-concept headings.
for _t in TOPICS:
    _t["items"] = [c[0] for c in _t["concepts"]]

# ------------------------------------------------------------------ the pipeline (visual process flow map)
PIPELINE = [
    ("Story & Storyboard", "hook · message · character"),
    ("Characters", "Higgsfield Elements"),
    ("Shots & Takes", "Cinema Studio · angles · light"),
    ("Edit in CapCut", "cut · captions · music · colour"),
    ("Export & Publish", "1080p · 9:16 / 16:9 · AI label"),
]

# ------------------------------------------------------------------ day themes
DAY_THEMES = {
    1: "Story and Storyboard, then Shoot It in Higgsfield",
    2: "Finish the Shoot, Edit in CapCut, Ethics & Assessment",
}

# ------------------------------------------------------------------ Topic 1 opener: the same footage cut two ways (built with ffmpeg, 23 Nov 2026)
OPENER_VIDEOS = [
    dict(key="boring", title="Video A: 20 seconds, nothing to hold on to",
         file="t1-boring-20s.mp4", poster="t1-boring-poster.jpg",
         model="20 s · 16:9 · stills from the SOLA footage, no sound",
         shots=["0–4 s  logo card: 'Introduction to the SOLA Water Bottle'",
                "4–8 s  still packshot: 'SOLA is a water bottle.'",
                "8–12 s  still wide: 'It can be used for exercise…'",
                "12–16 s  still close-up: 'It is available in black.'",
                "16–20 s  'Thank you for watching.'"]),
    dict(key="engaging", title="Video B: 18 seconds you watch to the end",
         file="t1-engaging-18s.mp4", poster="t1-engaging-poster.jpg",
         model="18 s · 16:9 · the same SOLA footage, cut with a hook and a story",
         shots=["0–3 s  hook: 'Warm water by your first kilometre?'",
                "3–6 s  a runner grabs it: 'Not this one.'",
                "6–9 s  she drinks, ice clinks: 'Still ice-cold after the run.'",
                "9–15 s  sunrise run, packshot: 'SOLA. Stay cold.'",
                "15–18 s  call to action: 'Pre-order today'"]),
]

# ------------------------------------------------------------------ demo videos (made in Higgsfield for this deck)
DEMO_VIDEOS = [
    dict(key="marketing", title="SOLA: the storyboard on film",
         file="marketing-sola-15s-h264.mp4", poster="marketing-poster.jpg",
         model="Seedance 2.5 · 1080p · 16:9 · 15 s · native audio · 240 credits",
         shots=["0–3 s  extreme close-up, sun slides across the bottle",
                "3–6 s  runner grabs it mid-stride (tracking)",
                "6–9 s  drink, ice clinks (slow motion)",
                "9–12 s  wide rooftop run, drone pulls back",
                "12–15 s  hero packshot with space for the logo"]),
    dict(key="scifi", title="Ringfall: the storyboard on film",
         file="scifi-ring-15s-h264.mp4", poster="scifi-poster.jpg",
         model="Seedance 2.5 · 1080p · 16:9 · 15 s · native audio · 240 credits",
         shots=["0–4 s  wide: smoking starship wreck, twin suns",
                "4–8 s  pilot steps out, handheld follow",
                "8–11 s  close-up: awe, ground trembles",
                "11–15 s  extreme wide: the ring rises, crane up"]),
]

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
    practical="Practical Performance (PP) — three tasks, one per activity (storyboard, Higgsfield footage, CapCut final cut), 1 hour, open book; paste ONE screenshot per task and upload your final video to the TMS.",
    note="A minimum of 75% attendance is required to be eligible for assessment and funding.",
)
