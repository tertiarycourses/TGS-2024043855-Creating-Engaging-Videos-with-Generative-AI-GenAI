# Creating Engaging Videos with Generative AI (GenAI) — Learner Guide

**WSQ Course Code:** TGS-2024043855  |  **Conducted by:** Tertiary Infotech Academy Pte Ltd (UEN 201200696W)  |  **Version v7 · 18 August 2026**

## Contents

- [Introduction](#introduction)
- [Course Learning Outcomes](#course-learning-outcomes)
- [The GenAI Video Creation Pipeline](#the-genai-video-creation-pipeline)
- [Before You Start — Environment Setup](#before-you-start--environment-setup)
- [Topic 01 — Create and Edit Video Script Using Generative AI (GenAI)](#topic-01--create-and-edit-video-script-using-generative-ai-genai)
  - [Lab 1 — Generate a Video Script with the RICCE Framework](#lab-1--generate-a-video-script-with-the-ricce-framework)
  - [Lab 2 — Build Story-Driven Scripts with Prompt Templates & Custom GPTs](#lab-2--build-story-driven-scripts-with-prompt-templates--custom-gpts)
  - [Lab 3 — AI Text-to-Video with VEED](#lab-3--ai-text-to-video-with-veed)
  - [Lab 4 — Develop Video Standards, Guidelines & a Production Work Plan](#lab-4--develop-video-standards-guidelines--a-production-work-plan)
- [Topic 02 — Improve Video Footage on GenAI-Powered Video Platforms](#topic-02--improve-video-footage-on-genai-powered-video-platforms)
  - [Lab 5 — VEED Video Editing Essentials](#lab-5--veed-video-editing-essentials)
  - [Lab 6 — Auto Subtitles, Captions, Transcripts & Translation](#lab-6--auto-subtitles-captions-transcripts--translation)
  - [Lab 7 — AI Voiceover, Clean Audio & Background Removal](#lab-7--ai-voiceover-clean-audio--background-removal)
  - [Lab 8 — Mini Project — Assess and Fix Video Quality](#lab-8--mini-project--assess-and-fix-video-quality)
- [Topic 03 — Apply New AI Technologies to Improve Video Production](#topic-03--apply-new-ai-technologies-to-improve-video-production)
  - [Lab 9 — AI Avatars, AI Images & Eye Contact](#lab-9--ai-avatars-ai-images--eye-contact)
  - [Lab 10 — AI Music Generation with Suno & Udio](#lab-10--ai-music-generation-with-suno--udio)
  - [Lab 11 — Voice Cloning, AI Dubbing & Lip Sync](#lab-11--voice-cloning-ai-dubbing--lip-sync)
  - [Lab 12 — Agentic AI Publishing to YouTube & TikTok](#lab-12--agentic-ai-publishing-to-youtube--tiktok)
- [Assessment Preparation](#assessment-preparation)
- [Glossary](#glossary)


## Introduction

This Learner Guide accompanies the WSQ course Creating Engaging Videos with Generative AI (GenAI) (TGS-2024043855), conducted by Tertiary Infotech Academy Pte Ltd. It provides detailed step-by-step instructions and copy-and-adapt GenAI prompts for all 12 hands-on labs, organised by the three course topics. The slides give you the concepts and each lab's overview; THIS guide is where the full procedure lives.

The course is built around the five-stage GenAI video creation pipeline: (1) AI-generated script → (2) AI-generated video → (3) AI voiceover & music → (4) AI video editing → (5) agentic AI publishing to YouTube/TikTok. Every lab maps to a stage of this pipeline, and the final assessment (WA SAQ + Practical Performance) assesses exactly what the labs practise.


## Course Learning Outcomes

- LO1: Develop video editing strategies and work plans to achieve creative video.
- LO2: Assess edited video footage to enhance storytelling and ensure technical compliance.
- LO3: Develop remedial actions to ensure industry compliance and facilitate the adoption of new technologies in video editing.

**Skills Framework alignment**

TSC: Video Editing (MED-MPN-4005-1.1).

- K1: Types of quality issues in video content
- K2: Types of solutions to rectify quality issues
- K3: Parameters to assess video quality
- K4: Industry quality standards
- K5: Technologies that improve efficiency and quality of video edits
- A1: Review scripts to conceptualize the types of edits required to achieve creative vision of production
- A2: Develop editing standards and guidelines in accordance to legal requirements and broadcasting standards
- A3: Develop work plans to outline the processes and timelines needed for the post production processes
- A4: Review edited footage to determine areas of improvement to enhance storytelling
- A5: Assess edited footage to ensure alignment with technical and legal requirements
- A6: Develop remedial actions for edited footage that does not meet requirements
- A7: Evaluate new technologies to improve efficiency and quality of video editing processes


## The GenAI Video Creation Pipeline

Keep this process flow in mind through every lab — it is the map of the whole course:

1. AI-Generated Script — ChatGPT · Gemini · Claude
2. AI-Generated Video — VEED · Sora · Kling · Veo
3. AI Voiceover & Music — TTS · clone · Suno · Udio
4. AI Video Editing — captions · cleanup · resize
5. Agentic AI Publishing — YouTube · TikTok

Labs 1–2 cover stage 1 (AI-generated script). Lab 3 covers stage 2 (AI-generated video). Labs 7, 10 and 11 cover stage 3 (AI voiceover & music). Labs 5–8 cover stage 4 (AI video editing). Lab 12 covers stage 5 (agentic AI publishing). Labs 4 and 9 support the pipeline with standards, work plans and AI visuals.


## Before You Start — Environment Setup

**What you need**

- A laptop (Windows or Mac) with the Chrome browser and a working internet connection.
- A free VEED account — sign up at veed.io with your email or Google account.
- A free ChatGPT account (chatgpt.com) — Gemini, Claude or Copilot also work for every script lab.
- A free Suno (suno.ai) and/or Udio (udio.com) account for the AI music lab.
- Optional: an ElevenLabs free account for voice cloning; a Google/YouTube and TikTok account for the publishing lab.
- A headset or earphones for reviewing audio in class.

**Conventions used in every lab**

- PROMPT blocks are copy-and-adapt — replace the bracketed parts with your own topic before submitting.
- Free-tier limits (watermarks, generation credits) may apply; the labs are designed to work within them.
- Save every artifact (scripts, videos, checklists) — several labs build on the previous lab's output, and they are your evidence for the Practical Performance assessment.
- Only clone YOUR OWN voice, and only use footage, music and faces you have the rights and consent to use.


## Topic 01 — Create and Edit Video Script Using Generative AI (GenAI)

AI script generation · prompt engineering · text-to-video · standards, guidelines & work plans  (Covers K1 · A1 · A2 · A3.)

**Key concepts**

- Script writing with GenAI — Generate ideas, storylines, dialogue and complete video scripts from a prompt.
- The RICCE prompt framework — Role, Instructions, Context, Constraints, Example — engineer prompts that produce broadcast-ready scripts.
- Story structure — Hero, desire, obstacle, action, outcome — the elements every engaging video script needs.
- AI text-to-video — Turn a script into a complete video with VEED's AI Video Maker — scenes, voiceover, captions and music in one pass.
- Standards & guidelines — Editing standards aligned to legal requirements (copyright, PDPA) and platform/broadcast specs.
- Work plans & timelines — Plan the production and post-production pipeline with GenAI-drafted work plans.


### Lab 1 — Generate a Video Script with the RICCE Framework

Maps to: A1 — review scripts and conceptualise the edits needed to achieve the creative vision.

Goal: Use the RICCE prompt framework (Role, Instructions, Context, Constraints, Example) with a text GenAI tool — ChatGPT, Gemini, Claude or Copilot — to generate a complete, engaging video script, then review and refine it for the target platform.

**What you'll build**

A polished 60–90 second video script with scene directions, dialogue and a hook, ready for production.   (Tools: ChatGPT, Gemini, Claude, Copilot.)

**Prompts for this lab**

> **Prompt — RICCE — full script prompt:**
>
> ```
> ROLE: You are an award-winning video scriptwriter for social media marketing.
> INSTRUCTIONS: Write a 60-second promotional video script for an online learning platform.
> CONTEXT: The audience is working adults in Singapore aged 25–45 considering upskilling; the video runs on YouTube and Instagram.
> CONSTRAINTS: Max 150 words of voiceover. Hook in the first 3 seconds. Conversational tone. End with the call-to-action 'Start learning today'.
> EXAMPLE: Format as a table with columns SCENE, VISUAL, VOICEOVER, ON-SCREEN TEXT.
> ```

> **Prompt — Refine the hook:**
>
> ```
> Rewrite the first scene so the opening 3 seconds create curiosity — start with a surprising question or statistic about career growth.
> ```

> **Prompt — Platform re-cut:**
>
> ```
> Adapt this script into a 30-second vertical TikTok version: faster pacing, punchier lines, captions-first, keep the same call-to-action.
> ```

**Step-by-step**

1. Open a text GenAI tool — chatgpt.com, gemini.google.com, claude.ai or copilot.microsoft.com — and sign in.
2. Draft your RICCE prompt: define the Role (expert scriptwriter), Instructions (write a 60-second promo script), Context (product, audience, platform), Constraints (length, tone, format) and an Example of the output structure.
3. Submit the prompt and review the generated script against the story elements: identifiable hero, clear desire, obstacle, action, outcome.
4. Iterate: ask the AI to strengthen the hook in the first 3 seconds, tighten the dialogue, and add a clear call-to-action.
5. Ask the AI to reformat the script as a two-column table — VISUAL (what we see) and AUDIO (voiceover/dialogue) — the standard video script format.
6. Tailor the same script for a second platform (e.g. a 30-second vertical TikTok cut) and compare how pacing and style change.
7. Save the final script to a document — you will use it in Lab 3 to generate the video.

**Check your work**

The script has a hook in the first 3 seconds, a clear hero/desire/obstacle/resolution arc, fits the 60–90 s duration, and is formatted in the two-column VISUAL/AUDIO layout.

> **Note:** This lab has its own folder: labs/lab-01-generate-a-video-script-with-the-ricce-framework/ — open its README.md for the same steps plus tips and troubleshooting.

---


### Lab 2 — Build Story-Driven Scripts with Prompt Templates & Custom GPTs

Maps to: A1 — conceptualise script edits; K1 — recognise script-level quality issues.

Goal: Use the six-step story prompt template (genre → protagonist → antagonist → conflict → setting → plot beats) to co-write a story-driven script step by step, then compare the result with a purpose-built custom GPT script writer.

**What you'll build**

A story-driven video script built beat-by-beat, plus a second version from a custom GPT for comparison.   (Tools: ChatGPT (custom GPTs), Gemini, Claude.)

**Prompts for this lab**

> **Prompt — Six-step template (steps 1–5 combined):**
>
> ```
> We are co-writing a video story script.
> GENRE: heartwarming brand story.
> PROTAGONIST: Sarah, 32, a nurse who dreams of switching into tech but has no time to study.
> OBSTACLE: 12-hour shifts and self-doubt.
> CONFLICT: every course she tries demands rigid schedules she cannot keep.
> SETTING: present-day Singapore, hopeful and warm tone.
> ```

> **Prompt — Plot beats:**
>
> ```
> Generate five plot points that escalate Sarah's conflict to a climax and resolve it when she discovers a flexible online academy. Then expand the five beats into a 90-second script in VISUAL/AUDIO table format.
> ```

> **Prompt — Critique prompt:**
>
> ```
> Act as a script editor. Critique this script for: weak hook, unclear protagonist desire, missing obstacle, flat resolution. List each issue and rewrite the weakest scene.
> ```

**Step-by-step**

1. Start a new chat and set the genre: tell the AI what kind of story you are writing (sci-fi, comedy, thriller, brand story).
2. Define the protagonist — name, age, occupation, personality and goal — in one prompt.
3. Define the antagonist (or the obstacle) — who or what stands in the way, and their motivation.
4. Define the conflict — how the protagonist and the obstacle collide.
5. Define the setting — time, location and tone of the story.
6. Ask the AI to generate five plot points that escalate the conflict to a climax, then expand them into a full script.
7. Open a custom GPT script writer (e.g. 'Video Script Writer' in the GPT Store) and give it the same brief; compare structure, pacing and dialogue between the two versions.
8. Pick the stronger version, note the script-level quality issues you fixed (weak hook, vague hero, no resolution), and save it.

**Check your work**

You can show both script versions, name at least three script-level quality issues you identified, and explain which version you chose for production and why.

> **Note:** This lab has its own folder: labs/lab-02-build-story-driven-scripts-with-prompt-templates/ — open its README.md for the same steps plus tips and troubleshooting.

---


### Lab 3 — AI Text-to-Video with VEED

Maps to: A1, A7 — turn a script into a video with an AI video generator.

Goal: Turn your Lab 1 script into a complete video with VEED's AI Video Maker: describe the video, let AI generate the scenes, voiceover, captions and music, then customise it in the editor. VEED's generator taps models such as Veo, Sora, Kling and Hailuo for the visuals.

**What you'll build**

A complete AI-generated 30–60 s video with scenes, AI voiceover, captions and background music.   (Tools: VEED AI Video Maker (veed.io/tools/ai-video), ChatGPT.)

**Prompts for this lab**

> **Prompt — Text-to-video description:**
>
> ```
> Create a 45-second upbeat promotional video for an online learning platform. Modern, bright visuals of working adults learning on laptops and phones; energetic female voiceover; bold captions; end on the text 'Start learning today'.
> ```

> **Prompt — Scene swap:**
>
> ```
> Generate a 5-second b-roll clip: close-up of hands typing on a laptop in a cosy café, warm morning light, shallow depth of field.
> ```

**Step-by-step**

1. Sign in at veed.io and open Tools → AI Video → AI Video Maker.
2. DESCRIBE: choose the video type (promo/explainer/social clip), paste your Lab 1 script or a one-line description of the topic, and let AI draft the storyboard.
3. CUSTOMIZE: set the aspect ratio (16:9 for YouTube, 9:16 for TikTok/Shorts), pick an AI voice for the narration, and toggle subtitles on.
4. Generate the video and watch the AI assemble scenes, voiceover, captions and music.
5. Open the result in the VEED editor: swap any scene you dislike with stock footage or an AI-generated clip, and adjust the music volume under the voiceover.
6. Export the video in 1080p and share the link with the class on Google Classroom.
7. Optional: repeat the generation on CapCut Web and compare output quality, control and speed with VEED.

**Check your work**

The exported video plays end-to-end with synchronised voiceover, captions and music, in the correct aspect ratio for the chosen platform.

> **Note:** This lab has its own folder: labs/lab-03-ai-text-to-video-with-veed/ — open its README.md for the same steps plus tips and troubleshooting.

---


### Lab 4 — Develop Video Standards, Guidelines & a Production Work Plan

Maps to: A2, A3 — develop editing standards/guidelines and post-production work plans.

Goal: Use GenAI to draft the two documents every production needs: (1) an editing standards & guidelines sheet aligned to legal requirements (copyright, PDPA, platform rules) and broadcast standards, and (2) a work plan with timelines for the post-production process.

**What you'll build**

A one-page editing standards & guidelines document and a phased post-production work plan with timelines.   (Tools: ChatGPT, Gemini, Claude.)

**Prompts for this lab**

> **Prompt — Editing standards:**
>
> ```
> Draft a one-page video editing standards & guidelines sheet for a Singapore digital media agency producing social videos. Cover: technical specs (resolution, frame rate, aspect ratio per platform), caption and subtitle style, audio loudness targets, brand usage, and legal compliance (music/footage licensing, PDPA consent, platform rules). Format as a table.
> ```

> **Prompt — Work plan:**
>
> ```
> Create a post-production work plan for a 60-second promo video due in 5 working days. Phases: script lock, AI asset generation, editing, internal review, client review, final export, publishing. For each phase give owner, duration, dependencies and deliverable. Format as a timeline table.
> ```

**Step-by-step**

1. Prompt the AI to draft video editing standards covering: resolution & frame rate, aspect ratios per platform, caption style, audio loudness, branding, and music licensing.
2. Extend the standards with legal compliance: copyright and licensing of footage/music, PDPA/consent for people appearing on camera, platform community guidelines, and IMDA advertising codes.
3. Review the AI draft critically — remove anything irrelevant to your production and add your organisation's brand rules.
4. Prompt the AI to build a post-production work plan: phases (script lock → asset generation → edit → review → export → publish), owner, duration and dependencies for each.
5. Ask the AI to convert the work plan into a timeline table for a 5-day turnaround, with buffer for client review.
6. Save both documents — they are your quality benchmark when you assess footage in Topic 2.

**Check your work**

The standards sheet names concrete technical specs and at least three legal/compliance rules; the work plan covers every phase to publishing with durations that sum to the 5-day deadline.

> **Note:** This lab has its own folder: labs/lab-04-develop-video-standards-guidelines-a-production/ — open its README.md for the same steps plus tips and troubleshooting.

---


## Topic 02 — Improve Video Footage on GenAI-Powered Video Platforms

VEED editing essentials · subtitles & captions · audio enhancement · quality assessment  (Covers K2 · K3 · A4 · A5.)

**Key concepts**

- Video editing basics — Trim, split, crop, resize, merge and loop footage on the VEED timeline — no installs, all in the browser.
- Transcripts & captions — Auto-transcribe speech, generate styled subtitles and closed captions, translate to 100+ languages.
- Audio enhancement — AI voiceover (text-to-speech), clean audio, background-noise removal and music balancing.
- Fixing quality issues — Remove cluttered backgrounds, fix framing with smart crop, correct resolution and aspect ratio per platform.
- Assessing footage — Judge resolution, frame rate, audio levels, visual consistency and pacing against the brief.
- Technical compliance — Verify the edit meets platform specs and the client's legal and brand requirements before export.


### Lab 5 — VEED Video Editing Essentials

Maps to: K2 — solutions that rectify quality issues; A4 — review footage for improvement.

Goal: Master the VEED browser editor: upload or record footage, then trim, split, crop, resize, merge and loop clips on the timeline, add photos, text overlays and music, and start from professional templates.

**What you'll build**

An edited multi-clip video with text overlays, images and background music, assembled on the VEED timeline.   (Tools: VEED Video Editor (veed.io/create/video-maker).)

**Prompts for this lab**

> **Prompt — Ask AI for an edit plan:**
>
> ```
> Here is my raw footage list: [describe your clips]. Propose an edit sequence for a 45-second video: which clip opens, where to cut, what text overlays to add, and where the music should swell.
> ```

**Step-by-step**

1. Open veed.io → Create → Video Maker and start a new project (or pick a template from veed.io/templates).
2. Upload two or three short clips (or record with the built-in webcam/screen recorder).
3. Trim each clip on the timeline: drag the clip edges to remove dead air at the start and end.
4. Split a clip: place the playhead mid-clip and hit Split; delete the section you don't need, then reorder clips by dragging.
5. Crop and resize: use Smart Crop to reframe the subject, and set the project size (16:9, 9:16, 1:1) from the canvas settings.
6. Add media: drop in a photo/logo, add a text overlay title with an animation, and add background music from the stock library.
7. Loop or merge: loop a short b-roll clip to cover the voiceover, and confirm the merged sequence flows without jump cuts.
8. Preview the full timeline, then export at 1080p.

**Check your work**

The exported video contains at least three clips trimmed and ordered cleanly, a text overlay, an image, and music — with no black gaps or jump cuts on the timeline.

> **Note:** This lab has its own folder: labs/lab-05-veed-video-editing-essentials/ — open its README.md for the same steps plus tips and troubleshooting.

---


### Lab 6 — Auto Subtitles, Captions, Transcripts & Translation

Maps to: K2, A4 — fix accessibility/quality gaps with AI captioning.

Goal: Make any video accessible and social-ready: auto-generate subtitles with AI speech recognition, style them as animated captions, download the transcript, and translate subtitles into other languages.

**What you'll build**

A captioned video with styled, animated subtitles, a downloadable transcript, and a translated subtitle track.   (Tools: VEED Subtitles & Translation.)

**Prompts for this lab**

> **Prompt — Polish the transcript:**
>
> ```
> Clean up this auto-generated transcript: fix punctuation and casing, correct obvious mis-transcriptions, and split it into subtitle lines of max 42 characters without breaking phrases.
> ```

**Step-by-step**

1. Open your Lab 5 project (or upload any talking video) in VEED.
2. Go to Subtitles → Auto Subtitles, pick the spoken language, and let the AI transcribe the audio.
3. Proof-read the generated subtitles in the side panel and fix any misheard words — names and jargon are the usual suspects.
4. Style the captions: choose a caption preset (word-by-word highlight for social), set font, size, colour and position safe for 9:16.
5. Download the transcript (TXT/SRT/VTT) from the subtitles panel.
6. Translate: duplicate the subtitle track and auto-translate it (e.g. to Chinese or Malay); review the translation quality.
7. Export the captioned video and compare engagement value against the uncaptioned original.

**Check your work**

Captions are accurate and synchronised, styled legibly for mobile, the transcript downloads cleanly, and a second-language subtitle track exists.

> **Note:** This lab has its own folder: labs/lab-06-auto-subtitles-captions-transcripts-translation/ — open its README.md for the same steps plus tips and troubleshooting.

---


### Lab 7 — AI Voiceover, Clean Audio & Background Removal

Maps to: K2 — audio/visual fixes; A4, A5 — review and assess footage.

Goal: Fix the two problems that sink most videos — bad audio and cluttered visuals. Generate an AI text-to-speech voiceover, clean background noise from recorded audio, and remove or replace a distracting video background without a green screen.

**What you'll build**

A video with a professional AI voiceover, denoised audio and a clean replaced background.   (Tools: VEED Text-to-Speech, Clean Audio, Background Remover.)

**Prompts for this lab**

> **Prompt — Voiceover script tone:**
>
> ```
> Rewrite this script for text-to-speech narration: short sentences, natural spoken rhythm, no brackets or symbols the TTS would read aloud, warm confident tone.
> ```

> **Prompt — Background scene:**
>
> ```
> Generate an image: modern minimalist studio backdrop in soft teal gradient, subtle depth, no text, suitable as a video call background.
> ```

**Step-by-step**

1. In your VEED project, open Audio → Text to Speech; paste your script, choose a voice (accent, gender, tone) and generate the voiceover track.
2. Align the voiceover on the timeline and duck the music: lower music volume to ~20% under speech.
3. Record (or upload) a webcam clip with room noise, then enable Clean Audio to strip background noise and compare before/after.
4. Select the webcam clip and toggle Remove Background — the AI mattes you out without a green screen.
5. Replace the background: drop in a brand-coloured background, an office image, or an AI-generated scene behind the cut-out.
6. Check lighting/edge artefacts on the matte; if edges shimmer, try a simpler background or better-lit source clip.
7. Export and note the quality issues you fixed (noise, clutter) and the solutions applied — this is exactly what the WA asks you to explain.

**Check your work**

The voiceover is clear and correctly timed, background noise is audibly reduced, and the replaced background has clean edges around the presenter.

> **Note:** This lab has its own folder: labs/lab-07-ai-voiceover-clean-audio-background-removal/ — open its README.md for the same steps plus tips and troubleshooting.

---


### Lab 8 — Mini Project — Assess and Fix Video Quality

Maps to: K1, K3, A4, A5, A6 — assess footage against parameters and remediate.

Goal: Bring it together: assess a flawed video against objective quality parameters (resolution, frame rate, audio levels, consistency, pacing, captions), diagnose its issues, plan remedial actions, and fix it on VEED to meet the standards sheet you wrote in Lab 4.

**What you'll build**

A quality-assessment checklist with findings, plus the remediated video that passes your own standards.   (Tools: VEED, ChatGPT (assessment checklist).)

**Prompts for this lab**

> **Prompt — Generate the checklist:**
>
> ```
> Create a video quality-assessment checklist with pass/fail criteria for: resolution, aspect ratio, frame rate, audio loudness and noise, visual consistency, pacing, caption accuracy, branding, and legal compliance. Format as a table I can score a video against.
> ```

> **Prompt — Diagnose from description:**
>
> ```
> My video has: muffled voice under loud music, captions that lag the speech, and a washed-out opening shot. For each issue, state the likely cause and the fastest fix in an online editor.
> ```

**Step-by-step**

1. Take a deliberately rough cut (your Lab 5 export, or the trainer's sample) and screen it end-to-end once without touching anything.
2. Score it against the assessment parameters: resolution & sharpness, aspect ratio, frame-rate smoothness, audio levels & noise, colour/visual consistency, pacing, caption accuracy, brand & legal compliance.
3. List every failed parameter as a quality issue, and match each issue to a remedial action (K1 → K2 mapping) — e.g. cluttered background → background removal; low voice → duck music + boost voice.
4. Apply the fixes on VEED: re-crop, clean audio, restyle captions, replace the weak opening shot, tighten pacing by cutting dead sections.
5. Re-screen the fixed video against the same checklist and against your Lab 4 standards sheet until every parameter passes.
6. Export the final video and keep the before/after checklist — it is your evidence of A5/A6 competence.

**Check your work**

You can present the scored checklist (before and after), name each issue and its remedial action, and the fixed video passes every parameter including your Lab 4 standards.

> **Note:** This lab has its own folder: labs/lab-08-mini-project-assess-and-fix-video-quality/ — open its README.md for the same steps plus tips and troubleshooting.

---


## Topic 03 — Apply New AI Technologies to Improve Video Production

AI avatars & visuals · AI music · voice cloning & dubbing · agentic AI publishing  (Covers K4 · K5 · A6 · A7.)

**Key concepts**

- AI avatars — Photorealistic talking presenters from text — no camera, studio or actor needed.
- AI image & VFX — Generate images, remove objects and backgrounds, and enhance shots with AI eye contact.
- AI music generation — Compose custom, royalty-free soundtracks with Suno and Udio from a text prompt.
- Voice cloning & dubbing — Clone a voice for narration and dub videos into other languages with lip sync.
- Agentic AI publishing — Let an AI agent draft titles, descriptions and hashtags, then push the video to YouTube and TikTok.
- Evaluating new tech — Compare AI tools on quality, cost, speed and rights to decide what enters your pipeline.


### Lab 9 — AI Avatars, AI Images & Eye Contact

Maps to: K5, A7 — apply and evaluate new AI production technologies.

Goal: Produce presenter-led video without a camera: generate a talking AI avatar from your script, create supporting visuals with the AI image generator, and fix off-camera gaze on recorded clips with AI eye contact correction.

**What you'll build**

An avatar-presented video with AI-generated imagery, plus an eye-contact-corrected webcam clip.   (Tools: VEED AI Avatars, AI Image Generator, AI Eye Contact.)

**Prompts for this lab**

> **Prompt — Avatar script:**
>
> ```
> Condense this script to a 30-second avatar narration: first person, friendly-expert tone, short sentences with natural pauses, no stage directions.
> ```

> **Prompt — B-roll images:**
>
> ```
> Generate an image: isometric illustration of a video production pipeline — script, camera, waveform, play button — clean flat style, teal and blue palette, no text.
> ```

**Step-by-step**

1. In VEED, open AI Avatars and browse the avatar library (or create a personal avatar from a short webcam recording).
2. Paste a 30-second section of your script, choose the avatar's voice and language, and generate the talking-head clip.
3. Use the AI Image Generator to create two supporting visuals for your topic, and cut them in as b-roll over the avatar's narration.
4. Record a 15-second webcam clip while reading from notes (eyes off-camera), then apply AI Eye Contact and compare the corrected gaze.
5. Assemble avatar + b-roll + captions into one sequence and export.
6. Evaluate (A7): note where an avatar beats filming a human (speed, cost, consistency, translation) and where it falls short (authenticity, emotion).

**Check your work**

The avatar's lip sync matches the narration, the AI images support the message, and the eye-contact clip looks naturally at camera.

> **Note:** This lab has its own folder: labs/lab-09-ai-avatars-ai-images-eye-contact/ — open its README.md for the same steps plus tips and troubleshooting.

---


### Lab 10 — AI Music Generation with Suno & Udio

Maps to: K5, A7 — generate custom soundtracks and evaluate the tools.

Goal: Compose custom, royalty-free music for your videos: write a music prompt (genre, mood, tempo, instrumentation), generate tracks on Suno and Udio, and pick and place the best track under your video with correct levels.

**What you'll build**

Two AI-composed soundtrack candidates (Suno + Udio) and your video re-scored with the winner.   (Tools: Suno (suno.ai), Udio (udio.com), VEED.)

**Prompts for this lab**

> **Prompt — Music prompt:**
>
> ```
> Uplifting corporate pop instrumental, 100 BPM, warm piano and soft synths building to a bright chorus, optimistic and modern, no vocals, 60 seconds, clean ending.
> ```

> **Prompt — Mood variation:**
>
> ```
> Same track but calmer: acoustic guitar led, gentle percussion, morning-light feel, suitable under a spoken voiceover.
> ```

**Step-by-step**

1. Sign in at suno.ai, describe the track you need (genre, mood, tempo, instruments, no vocals) and generate two candidates.
2. Repeat the same prompt on udio.com and generate two more candidates.
3. Audition all four against your video's pacing: does the energy match the cut points and the call-to-action?
4. Download the winner, import it into your VEED project, and place it under the voiceover at ~20% volume with a fade-out at the end.
5. Check rights: confirm the plan you used grants commercial use of the generated track.
6. Compare Suno vs Udio (A7): quality, control, speed, licensing — record which you would adopt and why.

**Check your work**

The chosen track matches the video's mood and pacing, sits under the voiceover without masking speech, and you can state its usage rights.

> **Note:** This lab has its own folder: labs/lab-10-ai-music-generation-with-suno-udio/ — open its README.md for the same steps plus tips and troubleshooting.

---


### Lab 11 — Voice Cloning, AI Dubbing & Lip Sync

Maps to: K5, A7 — clone voices, dub languages and evaluate ethics/quality.

Goal: Give your videos a consistent voice at scale: clone your own voice from a short sample, narrate a script with the clone, then auto-dub a video into another language with translated audio and lip-synced delivery.

**What you'll build**

A voiceover in your own cloned voice, and a dubbed version of your video in a second language.   (Tools: VEED Voice Clone & Dubbing, ElevenLabs, Sync Labs / D-ID (explore).)

**Prompts for this lab**

> **Prompt — Dub-ready rewrite:**
>
> ```
> Rewrite this narration for dubbing into Mandarin: avoid idioms and wordplay, keep sentences short, keep brand names in English, target the same 45-second duration.
> ```

**Step-by-step**

1. Record a clean 30–60 s voice sample (quiet room, natural pace) — consent and disclosure rules apply to any voice you clone; clone ONLY your own voice in class.
2. Create the clone (VEED voice cloning or elevenlabs.io) and generate your Lab 1 script in your cloned voice.
3. Compare the cloned narration with the stock TTS voice from Lab 7 — naturalness, pacing, pronunciation of local terms.
4. Auto-dub: take your finished video and use VEED's dubbing to translate the audio into Mandarin/Malay/Spanish, keeping your voice character.
5. Check the lip sync on the dubbed clip; explore D-ID or Sync Labs to lip-sync a still portrait to your cloned audio.
6. Evaluate (A7): where do cloning/dubbing add value (multilingual reach, consistency), and what are the ethical red lines (consent, deepfake misuse, disclosure)?

**Check your work**

The cloned voice is recognisably yours and pronounces the script cleanly; the dubbed video plays in the second language with acceptable lip sync; you can state the consent rule for cloning.

> **Note:** This lab has its own folder: labs/lab-11-voice-cloning-ai-dubbing-lip-sync/ — open its README.md for the same steps plus tips and troubleshooting.

---


### Lab 12 — Agentic AI Publishing to YouTube & TikTok

Maps to: A7 — adopt agentic AI to close the pipeline from edit to publish.

Goal: Close the GenAI video pipeline with an agentic step: export platform-ready cuts, then let an AI agent draft the title, description, hashtags and thumbnail concept, and push the video to YouTube and TikTok — scheduling included — while you stay in review control.

**What you'll build**

Your video live (unlisted) on YouTube and/or TikTok, published via an agent-assisted workflow with AI-drafted metadata.   (Tools: VEED export, ChatGPT/Claude (agent), YouTube Studio, TikTok, n8n/Zapier (optional).)

**Prompts for this lab**

> **Prompt — Publishing kit:**
>
> ```
> You are my publishing agent. For this 45-second video promoting an online learning platform, produce: 3 SEO YouTube title options under 60 characters, a 2-paragraph description with a call-to-action and link placeholder, 10 YouTube tags, a TikTok caption under 150 characters with 5 hashtags, a thumbnail concept (composition, text overlay, colours), and the best posting time for the Singapore audience. Present it as a checklist I can approve item by item.
> ```

> **Prompt — Agentic automation spec:**
>
> ```
> Design an n8n workflow that: watches a Google Drive folder for a new MP4, drafts YouTube metadata with an LLM node, waits for my approval via email, then uploads to YouTube with the approved metadata and posts the link to Slack. List the nodes and the data passed between them.
> ```

**Step-by-step**

1. Export two cuts from VEED: 16:9 1080p for YouTube and 9:16 for TikTok/Shorts, captions burned in for the vertical cut.
2. Ask an AI agent to draft the publishing kit: SEO title options, description with timestamps and links, 10 hashtags per platform, and a thumbnail concept.
3. Generate the thumbnail with the AI image generator from the agent's concept, and review the full kit — you approve every word before it ships.
4. Publish to YouTube: upload the 16:9 cut in YouTube Studio (set to Unlisted for class), paste the agent's title/description/tags, upload the thumbnail, and schedule the release time the agent recommends.
5. Publish to TikTok: upload the 9:16 cut, apply the agent's caption and hashtags, and schedule at the recommended engagement window.
6. Optional — automate: wire an n8n/Zapier flow (or a computer-use agent) that watches a Drive folder and performs the upload + metadata steps automatically, keeping a human-approval gate before anything goes live.
7. Verify both posts, then reflect: which pipeline stages (script → video → audio → edit → publish) are now AI-assisted, and where must a human stay in the loop?

**Check your work**

The video is live (unlisted) on at least one platform with agent-drafted, human-approved metadata, and you can describe where the approval gate sits in the agentic flow.

> **Note:** This lab has its own folder: labs/lab-12-agentic-ai-publishing-to-youtube-tiktok/ — open its README.md for the same steps plus tips and troubleshooting.

---


## Assessment Preparation

- Written Assessment (SAQ), 1 hour, open book — 5 questions covering K1–K5: quality issues, AI solutions, assessment parameters, industry standards and new editing technologies.
- Practical Performance, 1 hour, open book — 3 tasks covering A1–A7: script + video creation, VEED editing with text/music/transitions, and text-to-video with quality remediation.
- Revisit Lab 8's checklist — the WA questions on quality issues and fixes mirror it directly.
- Keep your lab outputs open during the PP — the tasks repeat what Labs 1, 3, 5, 7 and 8 practised.
- Sharpen your GenAI fundamentals with the free practice exams at https://exams.tertiaryinfotech.com (e.g. the Claude Certified Associate — Foundations exam).


## Glossary

- **Generative AI (GenAI)** — AI models that create new content — text, images, audio, video — from a prompt.
- **Prompt engineering** — Structuring the instruction you give an AI (e.g. with RICCE) to control output quality.
- **RICCE** — Role, Instructions, Context, Constraints, Example — a prompt framework for production-ready output.
- **Text-to-video** — Generating complete video footage from a written description (Sora, Veo, Kling, VEED).
- **AI avatar** — A synthetic on-screen presenter that speaks your script with lip-synced delivery.
- **Text-to-speech (TTS)** — Converting written text into natural spoken audio with an AI voice.
- **Voice cloning** — Recreating a specific person's voice from a sample — requires that person's consent.
- **AI dubbing** — Translating a video's speech into another language, re-voiced and lip-synced.
- **Auto subtitles** — AI speech recognition that transcribes audio into synchronised captions.
- **Background removal** — AI matting that separates the subject from the backdrop without a green screen.
- **Aspect ratio** — Frame proportions — 16:9 (YouTube), 9:16 (TikTok/Shorts/Reels), 1:1 (feed).
- **Agentic AI** — AI that plans and executes multi-step tasks (drafting metadata, uploading, scheduling) with human approval gates.
- **SRT/VTT** — Subtitle file formats carrying timed caption text.
- **Royalty-free** — Licensed for use without per-use payments — always verify commercial-use rights on AI output.
