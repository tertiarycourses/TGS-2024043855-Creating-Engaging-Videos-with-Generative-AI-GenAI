# Creating Engaging Videos with Generative AI (GenAI) — Learner Guide

**WSQ Course Code:** TGS-2024043855  |  **Conducted by:** Tertiary Infotech Academy Pte Ltd (UEN 201200696W)  |  **Version v8 · 9 November 2026**

## Contents

- [Introduction](#introduction)
- [Course Learning Outcomes](#course-learning-outcomes)
- [The Higgsfield Video Pipeline](#the-higgsfield-video-pipeline)
- [Before You Start — Environment Setup](#before-you-start--environment-setup)
- [Topic 01 — Create and Edit Video Script Using Generative AI (GenAI)](#topic-01--create-and-edit-video-script-using-generative-ai-genai)
  - [Lab 1 — Sign Up and Make Your First 15-Second Video](#lab-1--sign-up-and-make-your-first-15-second-video)
  - [Lab 2 — Write the Script and Shot List with Supercomputer and AI Director](#lab-2--write-the-script-and-shot-list-with-supercomputer-and-ai-director)
  - [Lab 3 — Set the House Rules: Standards, Work Plan and Credit Budget](#lab-3--set-the-house-rules-standards-work-plan-and-credit-budget)
- [Topic 02 — Improve Video Footage on GenAI-Powered Video Platforms](#topic-02--improve-video-footage-on-genai-powered-video-platforms)
  - [Lab 4 — Build Your Elements: Characters, Locations and Props](#lab-4--build-your-elements-characters-locations-and-props)
  - [Lab 5 — Direct Shots and Takes in Cinema Studio](#lab-5--direct-shots-and-takes-in-cinema-studio)
  - [Lab 6 — Cut, Caption and Assess the Scene](#lab-6--cut-caption-and-assess-the-scene)
- [Topic 03 — Apply New AI Technologies to Improve Video Production](#topic-03--apply-new-ai-technologies-to-improve-video-production)
  - [Lab 7 — Fix What Fails: Remedial Actions in Higgsfield](#lab-7--fix-what-fails-remedial-actions-in-higgsfield)
  - [Lab 8 — Add Voice, Music and Cinematic Effects](#lab-8--add-voice-music-and-cinematic-effects)
  - [Lab 9 — Use-Case Sprint: One Product Photo to a Published 15-Second Ad](#lab-9--use-case-sprint-one-product-photo-to-a-published-15-second-ad)
- [Assessment Preparation](#assessment-preparation)
- [Glossary](#glossary)


## Introduction

This Learner Guide accompanies the WSQ course Creating Engaging Videos with Generative AI (GenAI) (TGS-2024043855), conducted by Tertiary Infotech Academy Pte Ltd. It gives the full step-by-step instructions and copy-and-adapt prompts for all 9 hands-on labs, organised by the three course topics. The slides give you the concepts and each lab's overview; this guide is where the full procedure lives.

Every lab runs in one studio: Higgsfield (higgsfield.ai). You brief Supercomputer, Higgsfield's agent, in plain English, or you direct each shot yourself in Cinema Studio. Two 15-second films made this way for the course (a SOLA product ad and the Ringfall sci-fi scene) are embedded in the slides, so you can see the finish line before you start.


## Course Learning Outcomes

- LO1: Create video scripts using Generative AI (GAI) and work plans for video production.
- LO2: Edit video footage to improve video quality and ensure technical compliance.
- LO3: Apply new AI technologies to improve efficiency and quality in accordance to industry standards.

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
- A4: Review edited footage to propose changes that will enhance the story and emotions in each scene
- A5: Assess edited footage against technical parameters to ensure alignment to requirements
- A6: Develop remedial actions to resolve issues that do not comply with industry standards
- A7: Facilitate the adoption of new technologies to improve the efficiency and quality of visual outputs


## The Higgsfield Video Pipeline

Keep this process in mind through every lab; it is the map of the whole course:

1. Script & Shot List — Supercomputer · AI Director
2. Elements — characters · locations · props
3. Shots & Takes — Cinema Studio · Seedance 2.5
4. Fix & Finish — replace · upscale · voice · music
5. Publish — 9:16 + 16:9 · TikTok · YouTube

Labs 1–3 cover stage 1 (script, shot list, standards and budget). Lab 4 covers stage 2 (Elements). Labs 5–6 cover stage 3 (shots, takes and assessing the cut). Labs 7–8 cover stage 4 (fix and finish). Lab 9 runs the whole pipeline on a real use case and covers stage 5 (publish).


## Before You Start — Environment Setup

**What you need**

- A laptop (Windows or Mac) with Chrome and a working internet connection; a headset for reviewing audio.
- A Higgsfield account. Sign up at https://higgsfield.ai?fpr=alfred-d0d32b (Trainer's affiliate link: the trainer may earn a commission; you pay the normal price.)
- Labs run on higgsfield.ai (Supercomputer + Cinema Studio), which needs a paid plan. On 8 Nov 2026 Plus was US$49/month (US$39 billed yearly) for 1,000 credits. The free 3-day trial needs a card, renews to Plus unless cancelled within 3 days, and its credits worked only through the Higgsfield MCP, not on the website.
- Budget guide: a 15-second Seedance 2.5 Draft (480p) costs about 45 credits; the 1080p final of the same 15 s about 240 (read on Higgsfield, 9 Nov 2026). Labs 1–9 are designed around Draft takes, with one or two 1080p finals.
- Optional for Lab 9: a TikTok account to connect in Higgsfield (post as private or only-me in class).
- Watch before Lab 1: 'Higgsfield AI Tutorial for Beginners (2026) | Step-by-Step' by Metics Media — https://www.youtube.com/watch?v=Mt91SiQotOU
- Reference: Higgsfield API docs — https://docs.higgsfield.ai/docs (authentication, requests, polling, webhooks, model endpoints); Supercomputer and Skills — https://higgsfield.ai/supercomputer-intro

**Conventions used in every lab**

- PROMPT blocks are copy-and-adapt: replace the bracketed parts with your own idea before submitting.
- Draft first: test every idea on Seedance 2.5 Draft (480p) and finalise only the take you would show a client.
- Approve every spend yourself in Supercomputer; leave 'Always allow' off in class.
- Save every artefact (prompts, takes, checklists, exports): later labs build on them, and they are your Practical Performance evidence.
- Only clone YOUR OWN voice, and only use faces, products, music and footage you have the rights and consent to use.
- Each lab folder holds README.pdf (these steps), prompts.pdf, prompts.html (one-click copy) and assets/ with the mock files.


## Topic 01 — Create and Edit Video Script Using Generative AI (GenAI)

The impact of AI on video · use cases · Supercomputer scripts · AI Director shot lists · standards & work plans  (Covers K1 · A1 · A2 · A3.)

**Key concepts**

- AI's impact & use cases — A US$2,000 TV ad, a 14-day feature: AI movies, micro dramas, influencers, singers and marketing videos already earn audiences.
- The lazy prompt — Format + vibe gets you a clip in one line, but the model then decides your character, world and camera.
- Scripts with Supercomputer — Who / where / what happens, then a script and a numbered shot list, drafted and refined in one chat.
- AI Director — Inside a project, AI Director writes the script and an 8-shot storyboard from your brief.
- Standards & guidelines — A one-page sheet: platform specs, consent, licensing, AI disclosure and a Draft-first credit rule.
- Work plans & credit budgets — Phases, owners, timelines and a credit budget: 45 credits for a 15 s Draft, 240 for the 1080p final.


### Lab 1 — Sign Up and Make Your First 15-Second Video

Maps to: K1 — spot quality issues; A2 — generate a new video from scratch on a GenAI video platform.

Goal: Sign up to Higgsfield through the course link, tour the two doors (Supercomputer and Cinema Studio), then make the same 15-second sci-fi clip twice: once from a one-line lazy prompt, once after Supercomputer interviews you. Compare what the model decided for you.

**What you'll build**

Two 15-second Draft clips of the same idea, plus a log of what the model decided and three quality issues you spotted.   (Tools: Higgsfield: Cinema Studio (Video), Supercomputer, Seedance 2.5 Draft.)

**Prompts for this lab**

> **Prompt — The lazy prompt (format + vibe):**
>
> ```
> Create a 15-second video of an epic sci-fi scene.
> ```

> **Prompt — Make Supercomputer interview you first:**
>
> ```
> I want a 15-second epic sci-fi scene for a cinema-style trailer moment.
> Before you write or generate anything, ask me up to five short questions about:
> the main character, the world/location, what happens, the camera, and the sound.
> Then write the full prompt with timed shots and wait for my approval.
> Use Seedance 2.5 Draft, 16:9, 15 seconds, sound on.
> ```

**Step-by-step**

1. Open the course sign-up link higgsfield.ai?fpr=alfred-d0d32b and create your account with Google or email. It is the trainer's affiliate link: the trainer may earn a commission and you pay the normal price. Use the plan your trainer gives you; the website labs need a paid plan (Plus).
2. On the home page find the tiles you will use all course: Supercomputer (the agent), Cinema Studio 4.0, Seedance 2.5, Higgsfield Genjutsu and AI Influencer. Click your avatar to see your credit balance.
3. Open Video. In the bottom bar pick the model Seedance 2.5 Draft (480p, 4–30 s). Set 16:9, 15 s, sound On and 1 video.
4. Type the lazy prompt exactly as given in the prompts page and press Generate. A 15-second Draft costs about 45 credits (a 1080p final of the same clip is about 240).
5. Watch the clip twice with sound. In the log (assets/first-video-log.pdf) write what the model decided for you: the character, the world or location, and the camera.
6. Write three quality issues you can see or hear (K1): for example a face that changes, objects that melt, audio that does not match the action, unreadable text, or a shot that ends mid-movement.
7. Open Supercomputer from the home page. Paste the interview prompt so it asks you questions before it generates. Answer each question in one line.
8. Read the full prompt Supercomputer writes (scene, shots, camera, sound). Check the approval card shows Seedance 2.5 Draft, 16:9, 15 s, then press Approve. Never tick Always allow in class.
9. Compare the two takes side by side. Note which decisions you now control and which issues disappeared.
10. Create a project named 'Lab Studio – <your name>' and move both clips into it. Screenshot the project page with both takes visible for your evidence.

**Check your work**

Both clips are 15 s Drafts in one project; your log names the character, world and camera the model chose and three concrete quality issues, and says which ones the interviewed take fixed.

**Mock assets in the lab folder**

- first-video-log.pdf — what the model decided + three quality issues
- sample-scifi-take.jpg — a frame from the trainer's finished 15 s sci-fi clip
- sample-lazy-prompt-draft.mp4 — the lazy prompt, run as a 480p Draft for this course (compare with yours)

**Evidence to keep (screenshots for the PP)**

- Higgsfield project page showing both Draft takes
- Your completed first-video log (what the model decided, three quality issues)

> **Note:** This lab has its own folder: labs/lab-01-sign-up-and-make-your-first-15-second-video/ — README.pdf holds these steps; prompts.html copies each prompt in one click.

---


### Lab 2 — Write the Script and Shot List with Supercomputer and AI Director

Maps to: A1 — review scripts to conceptualise the edits needed; A2 — edit video scripts with GenAI.

Goal: Turn a three-line idea (who, where, what happens) into a 15-second script and a timed shot list. AI Director drafts it inside your project; you review it against the story elements and decide the edits: shot sizes, cuts, camera and sound. Then you refine it one change at a time.

**What you'll build**

A reviewed 15-second script and a 6-shot shot list in the three-part prompt format, saved in your project brief.   (Tools: Higgsfield: Projects, AI Director, Supercomputer (/youtube-script skill).)

**Prompts for this lab**

> **Prompt — Brief AI Director — who / where / what happens:**
>
> ```
> WHO: a bartender in her thirties, tired but proud of her bar.
> WHERE: her empty neighbourhood bar after closing time.
> WHAT HAPPENS: she switches the lights off one by one and walks to the window as the city lights come on.
> Write a 15-second cinematic script, then a 6-shot storyboard with shot sizes and timings.
> ```

> **Prompt — Three-part prompt skeleton:**
>
> ```
> Scene context: <the visible action in one or two sentences>.
> References: <@element — role, 100% as shown in the reference image>.
> Shots (cut between each):
> 1. 0–3s: <shot size>, <action>, <camera>.
> 2. 3–6s: ...
> Sound: <ambience>, <footsteps/clothing>, <dialogue or none>.
> ```

> **Prompt — Script critique:**
>
> ```
> Act as a film editor. Check this script for: weak opening shot, unclear hero, no obstacle, no visual payoff, and shots that cannot be filmed in 15 seconds. List each issue, then rewrite only the weakest shot.
> ```

**Step-by-step**

1. Open your Lab Studio project and click AI Director in the left panel (Tools → AI Director).
2. Give the three-line brief from the prompts page: WHO (a bartender), WHERE (an empty bar), WHAT HAPPENS (lights off, she walks to the window). Ask AI Director to write a 15-second script.
3. Ask for a 6-shot storyboard of the same script with shot sizes and timings.
4. Review the script with assets/story-elements-checklist.pdf: is there an identifiable hero, a clear desire, an obstacle, an action and an outcome? Mark what is missing.
5. Conceptualise the edits (A1): for every shot decide the size (wide, medium close-up, close-up), whether the camera moves, where the cut lands and what we hear. Write them into assets/shot-list-template.csv.
6. Rewrite the result as a three-part prompt: SCENE CONTEXT (visible action in 1–2 sentences), REFERENCES (leave empty for now), SHOTS (numbered, timed, one camera instruction each), then a SOUND line.
7. Refine and save: describe ONE change to AI Director, read the updated prompt, keep the version that works. Repeat twice.
8. In Supercomputer open Skills in the left sidebar and browse the Marketplace. Install one script or storyboard skill that fits your brief (official skills such as Cinematic Director are listed with the community ones).
9. Type / in the Supercomputer prompt, pick /youtube-script (or the skill you installed) and ask for a 30-second vertical re-cut of the same story. Compare pacing and hook with your 15-second version.
10. Paste the final script and shot list into Project brief. Screenshot the brief for your evidence.

**Check your work**

The script fits 15 s, every shot has a size, a camera instruction and a time, the story-elements review names at least two edits you made, and the prompt is in the three-part format.

**Mock assets in the lab folder**

- story-elements-checklist.pdf — hero, desire, obstacle, action, outcome
- shot-list-template.csv — shot, time, size, camera, action, sound
- client-brief-online-learning.pdf — the PP scenario brief to practise on

**Evidence to keep (screenshots for the PP)**

- Project brief showing your final script and 6-shot list
- Your story-elements review with the edits you decided

> **Note:** This lab has its own folder: labs/lab-02-write-the-script-and-shot-list-with-supercompute/ — README.pdf holds these steps; prompts.html copies each prompt in one click.

---


### Lab 3 — Set the House Rules: Standards, Work Plan and Credit Budget

Maps to: K1 — quality issues to prevent; A2 — develop editing standards and guidelines; A3 — develop work plans and timelines.

Goal: Have Supercomputer draft the two documents every Higgsfield production needs: a one-page standards and guidelines sheet (platform specs, legal and AI-disclosure rules, quality gates) and a post-production work plan with timelines and a credit budget built on real Draft and 1080p costs.

**What you'll build**

A one-page standards & guidelines sheet, a phased work plan with timelines and a credit budget, and your own /house-standards skill.   (Tools: Higgsfield: Supercomputer (Ask mode, Skills).)

**Prompts for this lab**

> **Prompt — Standards & guidelines sheet:**
>
> ```
> Draft a one-page video standards & guidelines sheet for a Singapore agency making 15–30 second AI videos in Higgsfield.
> Cover: resolution and frame rate; aspect ratio per platform (YouTube 16:9, TikTok/Reels/Shorts 9:16); audio level and captions;
> branding; character and location consistency (saved Elements only); commercial-use rights on our plan;
> PDPA consent for real faces and voices; AI-content disclosure labels on TikTok and YouTube; IMDA/ASAS advertising codes.
> Format as a table.
> ```

> **Prompt — Work plan with timelines and credits:**
>
> ```
> Create a post-production work plan for a 15-second promo due in 3 working days, made entirely in Higgsfield.
> Phases: script lock, Elements (characters, locations, props), 480p Draft takes, 1080p finals, fix & finish
> (replace, upscale, captions, music), client review, export 16:9 + 9:16, publish.
> For each phase give owner, duration, dependency, deliverable and credits (45 per 15 s Draft, 240 per 15 s 1080p final,
> max three Drafts per shot). Format as a timeline table with a credit total.
> ```

> **Prompt — Save the rules as a skill:**
>
> ```
> Save these standards as a reusable skill named house-standards.
> When to use: every video we make for clients.
> Rules: saved Elements only; Draft at 480p before any 1080p final; 1080p finals; 16:9 and 9:16 exports;
> AI-generated label on; no real person's face or voice without written consent; music cleared for commercial use.
> Steps: brief -> three-part prompt -> Draft -> review -> finalise -> quality checklist -> export.
> Output: the three-part prompt, a credit estimate and a pass/fail checklist.
> ```

**Step-by-step**

1. Open Supercomputer and switch to Ask mode so it answers without generating media (no credits spent on video).
2. Paste the standards prompt. Check the draft covers resolution, frame rate, aspect ratio per platform, audio level, captions and branding.
3. Add the legal layer: commercial-use rights on your Higgsfield plan, consent for any real face or voice (PDPA), music rights, platform AI-content labels on TikTok and YouTube, and IMDA/ASAS advertising codes.
4. Add two quality gates: every shot is approved as a 480p Draft before a 1080p final, and every final is checked against the quality checklist before export.
5. Paste the work-plan prompt. Each phase needs an owner, a duration, a dependency and a deliverable.
6. Ask Supercomputer to add a credit column using 45 credits per 15 s Draft and 240 per 15 s 1080p final, with three Drafts allowed per shot. Compare the total with assets/credit-plan-template.csv.
7. Review the drafts critically: delete anything that does not apply to your video and add your own brand rule.
8. Save both documents in Project brief and download them. Screenshot both for your evidence.
9. Turn the standards into your own skill: open Skills in the left sidebar and create a new skill named house-standards, using assets/skill-template.pdf (name, when to use, rules, steps, output format). Paste your rules into it. If your account offers no create button, give Supercomputer the 'save as a skill' prompt instead.
10. Test it: type /house-standards with a one-line video idea and check the reply follows your rules (Elements only, Draft first, AI label, three-part prompt, credit estimate). Screenshot the skill and the test reply.

**Check your work**

The sheet names concrete specs per platform and at least three legal or disclosure rules; the plan covers every phase to publishing within 3 days and its credit total matches 45/240 rates; /house-standards answers a test idea with your rules applied.

**Mock assets in the lab folder**

- credit-plan-template.csv — shots × Drafts × finals with the 45 / 240 credit rates
- work-plan-template.csv — phase, owner, start, end, dependency, deliverable, credits
- standards-checklist.pdf — the minimum items your sheet must cover
- skill-template.pdf — the five parts of a Supercomputer skill, with a filled /house-standards example

**Evidence to keep (screenshots for the PP)**

- Your standards & guidelines sheet (with legal and AI-disclosure rules)
- Your work plan with timelines and the credit total
- Your /house-standards skill and its test reply

> **Note:** This lab has its own folder: labs/lab-03-set-the-house-rules-standards-work-plan-and-cred/ — README.pdf holds these steps; prompts.html copies each prompt in one click.

---


## Topic 02 — Improve Video Footage on GenAI-Powered Video Platforms

Elements: characters, locations, props · references · Cinema Studio shots & takes · Draft mode · assess the cut  (Covers K2 · K3 · A4 · A5.)

**Key concepts**

- Elements — Save a character, location or prop once with an @handle and reuse it in every shot: the fix for drifting faces and sets.
- References — Up to 50 per generation (30 images, 10 videos, 10 audio), each given a role: character, location, camera move or voice.
- Shots & takes — One continuous shot or multishot with cuts; each run is a take you keep, compare or replace.
- Cinematic controls — Camera body, lens, aperture, movement, lighting, colour palette, genre, era and tempo.
- Draft mode — Seedance 2.5 Draft renders 480p for 45 credits; finalise only the take that works at 1080p.
- Assessing footage — Resolution, continuity, motion, audio, pacing and compliance, judged take by take.


### Lab 4 — Build Your Elements: Characters, Locations and Props

Maps to: K2 — solutions that rectify quality issues (consistency); A4 — review footage for improvement.

Goal: Faces that change between shots are the commonest AI video defect. Fix it before you shoot: cast a character with Supercomputer, turn the pick into a reference sheet, build a location and a prop, and save each one as an Element with an @handle you can call in any prompt.

**What you'll build**

Five saved Elements, two characters, two locations and one prop, each with a reference image and an @handle.   (Tools: Higgsfield: Supercomputer (character-sheet skill), Soul 2.0, Seedream 5.0 Pro, Nano Banana Pro, Elements.)

**Prompts for this lab**

> **Prompt — Cast a character (Supercomputer):**
>
> ```
> Main character in a biker road movie, 25 years old, modern style clothing.
> Use the character-sheet skill. Show me five photoreal casting options first; I will pick one before you build the reference sheet.
> ```

> **Prompt — Edit one detail, keep it consistent:**
>
> ```
> Give him a silver wallet chain hanging off his jeans pocket. Replace the black t-shirt with a plain white ribbed cotton tank top, same tank top in all views.
> ```

> **Prompt — Location with spatial anchors:**
>
> ```
> Wide interior of a dim neighbourhood bar at night: long wooden counter on the right with eight black stools, beer taps and backlit bottles, a pool table at the back, warm practical lamps, one large window on the left wall. Photoreal, 16:9, no people.
> ```

> **Prompt — Prop (run on two models):**
>
> ```
> A slim orange hard-shell briefcase with a ribbed moulded lid, rounded corners, a black top handle and two metal latches, white background, soft studio light, no logos or text.
> ```

**Step-by-step**

1. In Supercomputer paste the casting prompt. It loads the character-sheet skill and offers five photoreal casting options (Soul 2.0). Pick the one that fits your brief.
2. Ask for a 16:9 reference sheet of your pick: full body front, full body back, and a face portrait, plain white background.
3. Make one targeted edit with the edit prompt (Image → Seedream 5.0 Pro, about 3 credits): change one garment and keep it the same in all views.
4. Open the sheet, click Save as element. Set Category = Character, Name = Biker, Element ID = char_biker. Add a one-line description. Repeat for a second character (char_friend).
5. Generate the bar interior with the location prompt (Nano Banana Pro, about 2 credits). Check the space has clear spatial anchors (the counter, the stools, the window) you can name in a shot. Save as loc_bar-interior; repeat for loc_bar-entrance.
6. Generate the prop on two image models with the same prompt and compare shape, colour and credit cost. Save the better one as prop_suitcase.
7. Open My elements and check all five Elements are listed with their @handles. Screenshot the list for your evidence.
8. Review: which quality issue does each Element prevent (K2)? Write one line per Element in the naming sheet.

**Check your work**

Five Elements are saved with char_/loc_/prop_ handles; the character sheet shows the same face and outfit in all three views; each Element has a line saying which quality issue it prevents.

**Mock assets in the lab folder**

- character-brief.pdf — the biker road-movie brief and casting checklist
- element-naming-sheet.csv — category, name, @handle, what it prevents
- sample-product-sola.jpg — a product reference for Labs 8–9
- sample-location-bar.jpg and sample-prop-suitcase.jpg — the Lab 4 prompts run for this course

**Evidence to keep (screenshots for the PP)**

- My elements page showing your saved characters, locations and prop with @handles
- Your character reference sheet (front, back, face)

> **Note:** This lab has its own folder: labs/lab-04-build-your-elements-characters-locations-and-pro/ — README.pdf holds these steps; prompts.html copies each prompt in one click.

---


### Lab 5 — Direct Shots and Takes in Cinema Studio

Maps to: A4 — review footage to improve storytelling; K2 — solutions to rectify quality issues.

Goal: Direct a 15-second bar scene the way a film crew would: attach your Elements as references with roles, set camera, lens, lighting and colour, write the shots and the sound, then render four 480p Draft takes. Finalise only the best take in 1080p.

**What you'll build**

Four Draft takes of one scene and one 1080p final of the best take, made from your Elements.   (Tools: Higgsfield: Cinema Studio, Seedance 2.5 / Seedance 2.5 Draft, References, Elements.)

**Prompts for this lab**

> **Prompt — Bar scene — three-part prompt (Seedance 2.5):**
>
> ```
> Scene context: Biker enters a bar with a suitcase, looking for his friend. They notice each other, and the biker walks over and sits next to him as he lays his case flat on the counter.
> References:
> @char_biker — biker, 100% as shown in the reference image.
> @char_friend — friend, 100% as shown in the reference image. He is seated on a stool on the side of the bar counter.
> @prop_suitcase — suitcase, 100% as shown in the reference image. It belongs to @char_biker. He carries it in his left hand.
> @loc_bar-interior — the bar, 100% as shown in the location reference.
> Shots (cut between each):
> 1. 0–3s: wide, the biker pushes through the door, suitcase in his left hand.
> 2. 3–6s: medium shot, the friend looks up from his beer. Static camera.
> 3. 6–9s: close-up, the biker recognises him.
> 4. 9–12s: medium close-up, the biker sits; dialogue: "Told you I'd make it."
> 5. 12–15s: close-up, he lays the case flat on the counter.
> Sound: bar ambience, footsteps, leather jacket movement, the line of dialogue.
> ```

> **Prompt — One continuous shot (compare):**
>
> ```
> One continuous 15-second take. Follow a man along a busy New York sidewalk. Move from behind him to a frontal view as he reaches the corner. Keep the action uninterrupted, with no cuts.
> ```

**Step-by-step**

1. Open Video → Cinema Studio. Click References and attach @char_biker, @char_friend, @prop_suitcase and @loc_bar-interior. One generation accepts up to 50 references: 30 images, 10 videos, 10 audio.
2. Give each reference a role: Character for the people, Location for the bar. Type @ in the prompt to insert a handle.
3. Open Film setup: choose a camera body, a lens and an aperture (f/1.4 wide open for shallow focus). Open Lighting: pick Practicals. Open Colour palette: pick Film colors. Set Genre to Drama.
4. Write the prompt in three parts (prompts page): scene context, references with '100% as shown in the reference image', then numbered shots with sizes and camera.
5. Choose the shot structure: one continuous 15-second shot, or multishot with a cut between each. Use the multishot version for this lab.
6. Add the Sound line: bar ambience, footsteps, clothing movement and the one line of dialogue.
7. Select Seedance 2.5 Draft, 480p, 21:9 or 16:9, 15 s, sound On, 4 videos. Press Generate Draft (about 45 credits per take).
8. Watch all four takes with sound. Note for each: character match, prop position, camera, audio. Pick one.
9. Open the chosen Draft and finalise it in 1080p (Seedance 2.5 renders the same take at full resolution, about 240 credits for 15 s; drafts can be finalised within 7 days).
10. Screenshot the Cinema Studio prompt panel with the references attached and the four-take grid for your evidence.

**Check your work**

All four Drafts use your Elements; your take log scores each take; the 1080p final is the take you scored best and keeps the same faces, prop and bar.

**Mock assets in the lab folder**

- cinema-studio-cheatsheet.pdf — camera, lens, aperture, lighting, colour, genre, era, tempo
- shot-size-guide.pdf — wide, medium close-up, close-up and what each one is for
- take-log.csv — take, character match, prop, camera, audio, keep?

**Evidence to keep (screenshots for the PP)**

- Cinema Studio prompt panel with your references attached
- The four Draft takes and your 1080p final

> **Note:** This lab has its own folder: labs/lab-05-direct-shots-and-takes-in-cinema-studio/ — README.pdf holds these steps; prompts.html copies each prompt in one click.

---


### Lab 6 — Cut, Caption and Assess the Scene

Maps to: A4 — review edited footage to improve storytelling; A5 — assess footage against technical and legal requirements; K3 — quality parameters.

Goal: Keep the useful first take, direct one more, then have Supercomputer assemble the takes into a captioned cut with a soundtrack. Score the cut against the quality parameters and your Lab 3 standards before anything is exported.

**What you'll build**

A captioned 15–30 s cut in 16:9 and 9:16 with a scored quality checklist and a list of storytelling improvements.   (Tools: Higgsfield: Cinema Studio, Supercomputer (video montage: trims, soundtrack, burned captions).)

**Prompts for this lab**

> **Prompt — Direct one change:**
>
> ```
> Keep everything in this take the same. Change one thing only: in shot 3 make the camera push in slowly on the biker's face as he recognises his friend, and add a beat of silence before the dialogue.
> ```

> **Prompt — Assemble, caption and score (Supercomputer):**
>
> ```
> Assemble these two clips into one 20-second cut: take 2 first, then shots 4–5 of take 1. Trim dead frames at each cut.
> Add a moody low-tempo soundtrack under the bar ambience, keep the dialogue clearly above the music.
> Burn captions for the dialogue: white, bottom third, two lines max. Export 16:9 and 9:16.
> Then score the cut against: resolution, motion, face/prop continuity, audio, captions, pacing, platform compliance. Table, pass/fail.
> ```

**Step-by-step**

1. Watch your Lab 5 final with sound. Choose ONE change (or one variation) and write it as a single instruction.
2. Generate one new Draft take with that change. Keep both prompts and both clips: the comparison is your evidence.
3. Run the continuity check on the prop: where is it, who holds it, does it stay the same from shot to shot? Log it in assets/continuity-log.csv.
4. Open Supercomputer and paste the assembly prompt with your two best clips. It trims, orders, adds a soundtrack and burns captions, then exports 16:9 and 9:16.
5. Score the cut with assets/quality-checklist.pdf: resolution and sharpness, frame rate and motion, continuity of faces and props, audio (dialogue above music, no clipping), captions (accurate, in sync, readable), pacing, compliance.
6. Assess compliance against your Lab 3 sheet: correct ratio per platform, AI-content label planned, no real person's likeness without consent, music cleared for commercial use.
7. List three areas of improvement that would make the story land better (A4), for example a stronger opening image, a cut that lands on the reaction, or a sound cue on the payoff.
8. Screenshot the scored checklist and both exports for your evidence.

**Check your work**

The checklist scores every parameter with a reason, the cut exports in both ratios with readable captions, and you name three storytelling improvements tied to specific shots.

**Mock assets in the lab folder**

- quality-checklist.pdf — the seven quality parameters with pass/fail criteria
- continuity-log.csv — shot, prop position, who holds it, same as previous?
- client-standards-example.pdf — a filled standards sheet to assess against

**Evidence to keep (screenshots for the PP)**

- Your scored quality checklist (before export)
- Your 16:9 and 9:16 exports with captions

> **Note:** This lab has its own folder: labs/lab-06-cut-caption-and-assess-the-scene/ — README.pdf holds these steps; prompts.html copies each prompt in one click.

---


## Topic 03 — Apply New AI Technologies to Improve Video Production

Remove & replace objects · cinematic effects · upscale · voice & music · models compared · publish  (Covers K4 · K5 · A6 · A7.)

**Key concepts**

- Remove & replace — Genjutsu Replace Object swaps a product, prop or garment in finished footage, keeping the motion.
- Cinematic effects — Lighting presets, colour grades and viral effect presets add VFX without a compositor.
- Enhance shots — Upscale to 1080p or 4K, reframe 16:9 to 9:16, regenerate only the broken shot.
- Voice & music — Native Seedance audio, a cloned voice for narration and a generated soundtrack.
- Models compared — Seedance 2.5, Kling 4.0, Cinema Studio 4.0 and Genjutsu: pick per shot on quality, cost and control.
- Publish responsibly — Export per platform, label synthetic media, clear consent, then share to TikTok or YouTube.


### Lab 7 — Fix What Fails: Remedial Actions in Higgsfield

Maps to: A6 — develop remedial actions for footage that does not meet requirements; K4 — industry quality standards.

Goal: Take every FAIL from your Lab 6 checklist and match it to a Higgsfield fix: replace the wrong object, upscale soft footage, reframe for vertical, or regenerate only the broken shot with the same Elements. Apply at least two fixes and re-score.

**What you'll build**

A remediated cut with a before/after checklist and a remedy table (issue, cause, Higgsfield fix, result).   (Tools: Higgsfield: Genjutsu Replace Object, Upscale, Reframe, Cinema Studio (regenerate a shot).)

**Prompts for this lab**

> **Prompt — Diagnose the cut (Supercomputer):**
>
> ```
> Here is my cut and my quality checklist. For every FAIL, give: the issue, the likely cause, the Higgsfield fix
> (Replace Object, Upscale, Reframe, regenerate one shot with the same Elements, or a new Sound line) and the credit cost.
> Order the fixes cheapest first. Table.
> ```

> **Prompt — Replace an object (Genjutsu):**
>
> ```
> Replace the orange briefcase in this clip with the black hard-shell case in the reference image. Keep the hand position, motion, lighting and timing exactly the same.
> ```

> **Prompt — Regenerate one shot only:**
>
> ```
> Regenerate shot 3 only. Same Elements (@char_biker, @loc_bar-interior), same framing and timing. Fix: his face must match the reference sheet and the case stays in his left hand.
> ```

**Step-by-step**

1. Copy every FAIL from your Lab 6 checklist into assets/remedy-table.csv with its likely cause.
2. Match each issue to a fix using assets/remedy-map.pdf: wrong or drifting object → Genjutsu Replace Object; soft or 480p footage → Upscale; wrong ratio → Reframe 16:9 to 9:16; broken shot → regenerate that shot only with the same Elements; muddy audio → regenerate with a clearer Sound line.
3. Replace an object: open Genjutsu, choose Replace Object, upload the clip and the new prop image, describe the swap. The motion, framing and timing stay; only the object changes.
4. Apply at least one more fix from the map. Test it on a Draft before spending on a final.
5. Re-score the cut with the same checklist and record before/after in the remedy table.
6. Compliance pass (K4): platform specs met, AI-content label ready, consent and rights recorded.
7. Screenshot the before/after frames and the completed remedy table for your evidence.

**Check your work**

At least two FAILs are fixed with named Higgsfield tools, the re-score shows them as PASS, and the remedy table states the cause and credit cost of each fix.

**Mock assets in the lab folder**

- remedy-map.pdf — issue → Higgsfield fix → typical credit cost
- remedy-table.csv — issue, cause, fix, before, after
- flawed-cut-notes.pdf — a worked example of a failing cut and its fixes

**Evidence to keep (screenshots for the PP)**

- Before/after frames of each fix
- Your completed remedy table with the re-scored checklist

> **Note:** This lab has its own folder: labs/lab-07-fix-what-fails-remedial-actions-in-higgsfield/ — README.pdf holds these steps; prompts.html copies each prompt in one click.

---


### Lab 8 — Add Voice, Music and Cinematic Effects

Maps to: K5 — technologies that improve efficiency and quality; A7 — evaluate new technologies.

Goal: Finish the scene with the three upgrades that used to need three vendors: a generated soundtrack, a voiceover in a cloned or stock voice, and a cinematic effect. Time each one and rate it on quality, cost and control.

**What you'll build**

Your scene with a generated soundtrack, a voiceover line and one cinematic effect, plus a rated technology evaluation.   (Tools: Higgsfield: Audio (music + voice), Create Voice, lighting and colour presets, effect presets.)

**Prompts for this lab**

> **Prompt — Soundtrack:**
>
> ```
> Moody late-night bar soundtrack, 20 seconds, slow 80 BPM, warm Rhodes piano, soft brushed drums, upright bass, building slightly on the last 5 seconds. Instrumental, no vocals.
> ```

> **Prompt — Voiceover line:**
>
> ```
> Calm, low male voice, unhurried, Singapore English: "Some nights you don't need a plan. You just need to show up."
> ```

> **Prompt — Cinematic effect re-run:**
>
> ```
> Same shot, same Elements. Lighting: silhouette against the window, city lights behind. Colour: Black gloss. Slow push-in. Keep timing and action identical.
> ```

**Step-by-step**

1. Open Audio and generate a 20-second soundtrack from the music prompt. Generate two variations and keep the one that fits the cut's pace.
2. Voice: either pick a stock voice, or create your own voice from a clean 30-second recording of YOUR voice. Clone only a voice you have consent to use; sign assets/voice-consent-form.pdf for your own.
3. Generate the voiceover line and place it over the opening shot.
4. Apply one cinematic effect: re-run a shot with a different Lighting preset (Silhouette or Window) and Colour palette, or apply an effect preset from the effects gallery to one shot.
5. Record minutes and credits for each step in assets/tech-evaluation.csv and estimate what the same job takes with a studio, a composer and a voice artist.
6. Rate each technology 1–5 on quality, speed, cost, control and rights (A7), and decide whether it joins your pipeline.
7. Screenshot the Audio page, the effect before/after and your rated evaluation for your evidence.

**Check your work**

The scene carries a generated soundtrack and a consented voiceover, one shot shows a clear cinematic effect, and every technology has a 1–5 rating with a keep/drop verdict.

**Mock assets in the lab folder**

- music-prompt-cards.pdf — genre, tempo, instrument and mood cards
- voice-consent-form.pdf — consent to clone and use your own voice
- tech-evaluation.csv — technology, minutes, credits, quality, speed, cost, control, rights, verdict

**Evidence to keep (screenshots for the PP)**

- Your generated soundtrack and voiceover in Higgsfield
- Effect before/after and your rated technology evaluation

> **Note:** This lab has its own folder: labs/lab-08-add-voice-music-and-cinematic-effects/ — README.pdf holds these steps; prompts.html copies each prompt in one click.

---


### Lab 9 — Use-Case Sprint: One Product Photo to a Published 15-Second Ad

Maps to: A7 — evaluate new technologies; K4 — industry standards before publishing.

Goal: Run the whole pipeline on a real use case. Start from one product photo, shoot a campaign with the product-photoshoot skill, make a 15-second ad in Cinema Studio, compare two video models on the same prompt, then export, label and publish.

**What you'll build**

A 15-second ad (16:9 and 9:16) made from one product photo, a two-model comparison, and a publish-ready post.   (Tools: Higgsfield: Supercomputer (/product-photoshoot), Cinema Studio, Seedance 2.5, Kling 4.0, TikTok publishing.)

**Prompts for this lab**

> **Prompt — Campaign stills (/product-photoshoot):**
>
> ```
> /product-photoshoot Make a cool photoshoot for this bottle with our runner in the three Singapore locations we picked. Six photos: three with her and three of just the bottle. Make them vertical, 9:16.
> ```

> **Prompt — 15-second ad — five shots (Cinema Studio):**
>
> ```
> Scene context: A 15-second premium commercial for SOLA, a matte-black insulated steel bottle, at sunrise on a Singapore rooftop running track.
> References: @prop_sola — the bottle, 100% as shown. @char_runner — runner, 100% as shown.
> Shots (hard cut between each):
> 1. 0–3s: extreme close-up, first sun ray slides across the bottle. Slow push-in.
> 2. 3–6s: medium, the runner grabs it mid-stride. Tracking.
> 3. 6–9s: close-up, she drinks; ice clinks. Slow motion.
> 4. 9–12s: wide, she runs along the rooftop edge, skyline glowing. Drone pulls back.
> 5. 12–15s: hero packshot, clean space at top for the logo.
> Sound: upbeat electronic beat building to a hit on the packshot, footsteps, ice, whoosh on each cut. No on-screen text.
> ```

> **Prompt — Pick a use case (variation):**
>
> ```
> Rewrite this ad brief as a 15-second AI micro-drama cliffhanger: same product, two characters, one twist in the last 3 seconds, vertical 9:16, dialogue in one line.
> ```

**Step-by-step**

1. Upload the product photo from assets/ (or your own product) to Supercomputer with a character sheet and a street location.
2. Type /product-photoshoot and ask for six vertical 9:16 photos: three with your character, three of the product alone.
3. Open Cinema Studio, attach the product, the character and the location as references, and write the 15-second ad with the five-shot structure on the prompts page. Generate a Draft first.
4. Run the same prompt on a second model (Kling 4.0 or Cinema Studio 4.0) and compare with assets/model-comparison.csv: product accuracy, motion, audio, credits, render time.
5. Finalise the winner in 1080p and reframe a 9:16 version.
6. Pre-publish check: AI-generated label on, no unlicensed logos or music, consent recorded, caption and hashtags ready.
7. Publish to TikTok from Higgsfield (connect your account, post as private or only-me in class), or download the MP4 for the TMS upload. Screenshot the comparison table and the post settings for your evidence.

**Check your work**

The ad runs 15 s in both ratios, keeps the product accurate in every shot, the comparison table justifies the chosen model on at least three criteria, and the post carries an AI-generated label.

**Mock assets in the lab folder**

- sample-product-sola.jpg — the product photo to start from
- campaign-brief.pdf — SOLA brief, audience, platforms, mandatory label
- model-comparison.csv — model, product accuracy, motion, audio, credits, time, verdict
- publish-checklist.pdf — AI label, rights, consent, caption, hashtags

**Evidence to keep (screenshots for the PP)**

- Your two-model comparison table
- The final 15 s ad (upload the MP4 to the TMS) and the publish settings

> **Note:** This lab has its own folder: labs/lab-09-use-case-sprint-one-product-photo-to-a-published/ — README.pdf holds these steps; prompts.html copies each prompt in one click.

---


## Assessment Preparation

- Written Assessment (SAQ), 1 hour, open book: 5 questions covering K1–K5: quality issues in AI video, solutions in Higgsfield, quality parameters, industry standards and new technologies.
- Practical Performance (PP), 1 hour, open book: 3 Higgsfield tasks covering A1–A7 that mirror Labs 1–3, 4–6 and 7–9. Paste screenshots of your work into the box under each task and upload your final video (MP4) to the TMS.
- Revisit the slide 'Quality issues → the Higgsfield fix' and your Lab 6 checklist: the WA questions on issues and fixes mirror them.
- Keep your Lab Studio project open during the PP; your saved Elements and prompts save you time.
- Practise with the free exams at https://exams.tertiaryinfotech.com.


## Glossary

- **Higgsfield** — An AI video studio (higgsfield.ai) holding many image and video models, an agent and cinematic controls in one place.
- **Supercomputer** — Higgsfield's agent: you brief it in plain English, it writes prompts, calls tools and asks you to approve each spend.
- **Cinema Studio** — Higgsfield's director panel: references, camera body, lens, aperture, lighting, colour palette, genre, model and settings.
- **AI Director** — The director chat inside a Higgsfield project that writes scripts and storyboards.
- **Seedance 2.5** — ByteDance's video model in Higgsfield: 4–30 s, up to 1080p, native audio, up to 50 references.
- **Draft mode** — Seedance 2.5 Draft renders a cheap 480p take that can be finalised at 1080p within seven days.
- **Element** — A saved character, location or prop with an @handle (e.g. @char_biker) reused as a reference in any prompt.
- **Reference** — An image, video or audio file attached to a generation with a role: character, location, camera move or voice.
- **Shot / take** — A shot is one camera set-up in the script; a take is one generated attempt at it.
- **Multishot** — One generation containing several shots with cuts between them.
- **Genjutsu** — Higgsfield's tool for replacing objects or copying motion in existing footage.
- **Aspect ratio** — Frame proportions: 16:9 (YouTube), 9:16 (TikTok, Shorts, Reels), 21:9 (cinema).
- **AI disclosure label** — The platform setting that marks realistic AI-generated content (TikTok's AI-generated label, YouTube's altered or synthetic content setting).
- **Credits** — Higgsfield's usage currency; every generation shows its credit cost before you approve it.
