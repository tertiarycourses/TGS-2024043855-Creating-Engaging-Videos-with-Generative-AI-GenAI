"""Topic 1 — Create and Edit Video Script Using Generative AI (GenAI).  Labs 1–3.

Every lab runs inside Higgsfield (higgsfield.ai): Supercomputer, the agent you
brief in plain English, and Cinema Studio, where you set every control.
`steps` render in the Learner Guide and the lab folder ONLY (never as slides);
`prompts` render on the PPT prompt slide, in the LG and in the lab prompts page;
`assets` are the mock files shipped in the lab folder; `evidence` lists the
screenshots the PP asks for.
"""

DOMAIN1 = [
    dict(
        num=1, topic=1,
        title="Sign Up and Make Your First 15-Second Video",
        objective="K1 — spot quality issues; A2 — generate a new video from scratch on a GenAI video platform",
        desc="Sign up to Higgsfield through the course link, tour the two doors (Supercomputer and Cinema Studio), "
             "then make the same 15-second sci-fi clip twice: once from a one-line lazy prompt, once after "
             "Supercomputer interviews you. Compare what the model decided for you.",
        build="Two 15-second Draft clips of the same idea, plus a log of what the model decided and three quality issues you spotted.",
        services="Higgsfield: Cinema Studio (Video), Supercomputer, Seedance 2.5 Draft",
        flow=["Sign up via the course link", "Tour Supercomputer + Cinema Studio", "Lazy prompt, Draft take",
              "Supercomputer interviews you", "Compare and log issues"],
        steps=[
            ("Open the course sign-up link higgsfield.ai?fpr=alfred-d0d32b and create your account with Google or email. "
             "It is the trainer's affiliate link: the trainer may earn a commission and you pay the normal price. "
             "Use the plan your trainer gives you; the website labs need a paid plan (Plus).", ""),
            ("On the home page find the tiles you will use all course: Supercomputer (the agent), Cinema Studio 4.0, "
             "Seedance 2.5, Higgsfield Genjutsu and AI Influencer. Click your avatar to see your credit balance.", ""),
            ("Open Video. In the bottom bar pick the model Seedance 2.5 Draft (480p, 4–30 s). Set 16:9, 15 s, sound On and 1 video.", ""),
            ("Type the lazy prompt exactly as given in the prompts page and press Generate. A 15-second Draft costs about 45 credits "
             "(a 1080p final of the same clip is about 240).", ""),
            ("Watch the clip twice with sound. In the log (assets/first-video-log.pdf) write what the model decided for you: "
             "the character, the world or location, and the camera.", ""),
            ("Write three quality issues you can see or hear (K1): for example a face that changes, objects that melt, "
             "audio that does not match the action, unreadable text, or a shot that ends mid-movement.", ""),
            ("Open Supercomputer from the home page. Paste the interview prompt so it asks you questions before it generates. "
             "Answer each question in one line.", ""),
            ("Read the full prompt Supercomputer writes (scene, shots, camera, sound). Check the approval card shows "
             "Seedance 2.5 Draft, 16:9, 15 s, then press Approve. Never tick Always allow in class.", ""),
            ("Compare the two takes side by side. Note which decisions you now control and which issues disappeared.", ""),
            ("Create a project named 'Lab Studio – <your name>' and move both clips into it. Screenshot the project page "
             "with both takes visible for your evidence.", ""),
        ],
        prompts=[
            ("The lazy prompt (format + vibe)",
             "Create a 15-second video of an epic sci-fi scene."),
            ("Make Supercomputer interview you first",
             "I want a 15-second epic sci-fi scene for a cinema-style trailer moment.\n"
             "Before you write or generate anything, ask me up to five short questions about:\n"
             "the main character, the world/location, what happens, the camera, and the sound.\n"
             "Then write the full prompt with timed shots and wait for my approval.\n"
             "Use Seedance 2.5 Draft, 16:9, 15 seconds, sound on."),
        ],
        assets=["first-video-log.pdf — what the model decided + three quality issues",
                "sample-scifi-take.jpg — a frame from the trainer's finished 15 s sci-fi clip",
                "sample-lazy-prompt-draft.mp4 — the lazy prompt, run as a 480p Draft for this course (compare with yours)"],
        evidence=["Higgsfield project page showing both Draft takes",
                  "Your completed first-video log (what the model decided, three quality issues)"],
        test="Both clips are 15 s Drafts in one project; your log names the character, world and camera the model chose "
             "and three concrete quality issues, and says which ones the interviewed take fixed.",
    ),
    dict(
        num=2, topic=1,
        title="Write the Script and Shot List with Supercomputer and AI Director",
        objective="A1 — review scripts to conceptualise the edits needed; A2 — edit video scripts with GenAI",
        desc="Turn a three-line idea (who, where, what happens) into a 15-second script and a timed shot list. "
             "AI Director drafts it inside your project; you review it against the story elements and decide the edits: "
             "shot sizes, cuts, camera and sound. Then you refine it one change at a time.",
        build="A reviewed 15-second script and a 6-shot shot list in the three-part prompt format, saved in your project brief.",
        services="Higgsfield: Projects, AI Director, Supercomputer (/youtube-script skill)",
        flow=["Who / where / what happens", "AI Director drafts script", "Review against story elements",
              "Rewrite as a 3-part prompt", "Refine one change at a time"],
        steps=[
            ("Open your Lab Studio project and click AI Director in the left panel (Tools → AI Director).", ""),
            ("Give the three-line brief from the prompts page: WHO (a bartender), WHERE (an empty bar), WHAT HAPPENS "
             "(lights off, she walks to the window). Ask AI Director to write a 15-second script.", ""),
            ("Ask for a 6-shot storyboard of the same script with shot sizes and timings.", ""),
            ("Review the script with assets/story-elements-checklist.pdf: is there an identifiable hero, a clear desire, "
             "an obstacle, an action and an outcome? Mark what is missing.", ""),
            ("Conceptualise the edits (A1): for every shot decide the size (wide, medium close-up, close-up), whether the "
             "camera moves, where the cut lands and what we hear. Write them into assets/shot-list-template.csv.", ""),
            ("Rewrite the result as a three-part prompt: SCENE CONTEXT (visible action in 1–2 sentences), REFERENCES "
             "(leave empty for now), SHOTS (numbered, timed, one camera instruction each), then a SOUND line.", ""),
            ("Refine and save: describe ONE change to AI Director, read the updated prompt, keep the version that works. "
             "Repeat twice.", ""),
            ("In Supercomputer open Skills in the left sidebar and browse the Marketplace. Install one script or storyboard "
             "skill that fits your brief (official skills such as Cinematic Director are listed with the community ones).", ""),
            ("Type / in the Supercomputer prompt, pick /youtube-script (or the skill you installed) and ask for a 30-second "
             "vertical re-cut of the same story. Compare pacing and hook with your 15-second version.", ""),
            ("Paste the final script and shot list into Project brief. Screenshot the brief for your evidence.", ""),
        ],
        prompts=[
            ("Brief AI Director — who / where / what happens",
             "WHO: a bartender in her thirties, tired but proud of her bar.\n"
             "WHERE: her empty neighbourhood bar after closing time.\n"
             "WHAT HAPPENS: she switches the lights off one by one and walks to the window as the city lights come on.\n"
             "Write a 15-second cinematic script, then a 6-shot storyboard with shot sizes and timings."),
            ("Three-part prompt skeleton",
             "Scene context: <the visible action in one or two sentences>.\n"
             "References: <@element — role, 100% as shown in the reference image>.\n"
             "Shots (cut between each):\n"
             "1. 0–3s: <shot size>, <action>, <camera>.\n"
             "2. 3–6s: ...\n"
             "Sound: <ambience>, <footsteps/clothing>, <dialogue or none>."),
            ("Script critique",
             "Act as a film editor. Check this script for: weak opening shot, unclear hero, no obstacle, no visual "
             "payoff, and shots that cannot be filmed in 15 seconds. List each issue, then rewrite only the weakest shot."),
        ],
        assets=["story-elements-checklist.pdf — hero, desire, obstacle, action, outcome",
                "shot-list-template.csv — shot, time, size, camera, action, sound",
                "client-brief-online-learning.pdf — the PP scenario brief to practise on"],
        evidence=["Project brief showing your final script and 6-shot list",
                  "Your story-elements review with the edits you decided"],
        test="The script fits 15 s, every shot has a size, a camera instruction and a time, the story-elements review "
             "names at least two edits you made, and the prompt is in the three-part format.",
    ),
    dict(
        num=3, topic=1,
        title="Set the House Rules: Standards, Work Plan and Credit Budget",
        objective="K1 — quality issues to prevent; A2 — develop editing standards and guidelines; A3 — develop work plans and timelines",
        desc="Have Supercomputer draft the two documents every Higgsfield production needs: a one-page standards and "
             "guidelines sheet (platform specs, legal and AI-disclosure rules, quality gates) and a post-production work "
             "plan with timelines and a credit budget built on real Draft and 1080p costs.",
        build="A one-page standards & guidelines sheet, a phased work plan with timelines and a credit budget, and your own /house-standards skill.",
        services="Higgsfield: Supercomputer (Ask mode, Skills)",
        flow=["Draft standards with Supercomputer", "Add legal + AI-disclosure rules", "Build the work plan + credits",
              "Save the rules as a skill", "Test /house-standards"],
        steps=[
            ("Open Supercomputer and switch to Ask mode so it answers without generating media (no credits spent on video).", ""),
            ("Paste the standards prompt. Check the draft covers resolution, frame rate, aspect ratio per platform, "
             "audio level, captions and branding.", ""),
            ("Add the legal layer: commercial-use rights on your Higgsfield plan, consent for any real face or voice "
             "(PDPA), music rights, platform AI-content labels on TikTok and YouTube, and IMDA/ASAS advertising codes.", ""),
            ("Add two quality gates: every shot is approved as a 480p Draft before a 1080p final, and every final is "
             "checked against the quality checklist before export.", ""),
            ("Paste the work-plan prompt. Each phase needs an owner, a duration, a dependency and a deliverable.", ""),
            ("Ask Supercomputer to add a credit column using 45 credits per 15 s Draft and 240 per 15 s 1080p final, "
             "with three Drafts allowed per shot. Compare the total with assets/credit-plan-template.csv.", ""),
            ("Review the drafts critically: delete anything that does not apply to your video and add your own brand rule.", ""),
            ("Save both documents in Project brief and download them. Screenshot both for your evidence.", ""),
            ("Turn the standards into your own skill: open Skills in the left sidebar and create a new skill named "
             "house-standards, using assets/skill-template.pdf (name, when to use, rules, steps, output format). Paste your "
             "rules into it. If your account offers no create button, give Supercomputer the 'save as a skill' prompt instead.", ""),
            ("Test it: type /house-standards with a one-line video idea and check the reply follows your rules (Elements only, "
             "Draft first, AI label, three-part prompt, credit estimate). Screenshot the skill and the test reply.", ""),
        ],
        prompts=[
            ("Standards & guidelines sheet",
             "Draft a one-page video standards & guidelines sheet for a Singapore agency making 15–30 second AI videos in Higgsfield.\n"
             "Cover: resolution and frame rate; aspect ratio per platform (YouTube 16:9, TikTok/Reels/Shorts 9:16); audio level and captions;\n"
             "branding; character and location consistency (saved Elements only); commercial-use rights on our plan;\n"
             "PDPA consent for real faces and voices; AI-content disclosure labels on TikTok and YouTube; IMDA/ASAS advertising codes.\n"
             "Format as a table."),
            ("Work plan with timelines and credits",
             "Create a post-production work plan for a 15-second promo due in 3 working days, made entirely in Higgsfield.\n"
             "Phases: script lock, Elements (characters, locations, props), 480p Draft takes, 1080p finals, fix & finish\n"
             "(replace, upscale, captions, music), client review, export 16:9 + 9:16, publish.\n"
             "For each phase give owner, duration, dependency, deliverable and credits (45 per 15 s Draft, 240 per 15 s 1080p final,\n"
             "max three Drafts per shot). Format as a timeline table with a credit total."),
            ("Save the rules as a skill",
             "Save these standards as a reusable skill named house-standards.\n"
             "When to use: every video we make for clients.\n"
             "Rules: saved Elements only; Draft at 480p before any 1080p final; 1080p finals; 16:9 and 9:16 exports;\n"
             "AI-generated label on; no real person's face or voice without written consent; music cleared for commercial use.\n"
             "Steps: brief -> three-part prompt -> Draft -> review -> finalise -> quality checklist -> export.\n"
             "Output: the three-part prompt, a credit estimate and a pass/fail checklist."),
        ],
        assets=["credit-plan-template.csv — shots × Drafts × finals with the 45 / 240 credit rates",
                "work-plan-template.csv — phase, owner, start, end, dependency, deliverable, credits",
                "standards-checklist.pdf — the minimum items your sheet must cover",
                "skill-template.pdf — the five parts of a Supercomputer skill, with a filled /house-standards example"],
        evidence=["Your standards & guidelines sheet (with legal and AI-disclosure rules)",
                  "Your work plan with timelines and the credit total",
                  "Your /house-standards skill and its test reply"],
        test="The sheet names concrete specs per platform and at least three legal or disclosure rules; the plan covers "
             "every phase to publishing within 3 days and its credit total matches 45/240 rates; /house-standards answers a test "
             "idea with your rules applied.",
    ),
]
