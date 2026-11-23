"""Topic 1 — Create and Edit Video Script Using Generative AI (GAI).  Activity 1.

v12 (23 Nov 2026): one activity per topic. Activity 1 plans the video the learner will shoot in
Activity 2 (Higgsfield) and edit in Activity 3 (CapCut): hook, one message, character, a five-beat
story, a GenAI script and a storyboard sheet that also carries the house standards and the work plan.
`steps` render in the Learner Guide and the lab folder ONLY (never as slides); `prompts` render on the
PPT prompt slide, in the LG and in the lab prompts page; `assets` ship in the lab folder; `evidence`
is the ONE screenshot PP Task 1 asks for.
"""

DOMAIN1 = [
    dict(
        num=1, topic=1,
        title="Hook, Story and Storyboard: Plan Your 15-Second Video",
        objective="K1 · A1 · A2 · A3 — plan out defects, edit the script, house rules, work plan",
        desc="Pick a product or cause, write the one message, choose a hook and a character, then let Higgsfield "
             "Supercomputer draft the script and a six-panel storyboard. You review it as an editor, fix what is weak, "
             "and finish one storyboard sheet that also carries your house rules and a work plan with a credit budget.",
        build="One storyboard sheet: brief, one message, hook, character, six timed panels (size, angle, move, action, sound, on-screen text), house rules and a work plan with a credit budget.",
        services="Higgsfield: Supercomputer (Ask mode), AI Director, image models for storyboard frames · storyboard-sheet template",
        flow=["Brief + one message", "Hook + character", "Five-beat story", "GenAI script + storyboard", "Review, rules, work plan"],
        steps=[
            ("Choose what you will advertise: your own product, service or cause, or the default brief in assets/brief-kopi-kaki.pdf "
             "(a fictional neighbourhood coffee bar launching an iced kopi). You will shoot it in Activity 2 and edit it in Activity 3.", ""),
            ("Write the one message in one sentence on the storyboard sheet: '[Audience] should [feel or do] because [reason].' "
             "If you need 'and' twice, you have two messages: cut one.", ""),
            ("Pick your hook from assets/hook-cards.pdf (question, bold number, pattern interrupt, start mid-action, before/after, "
             "curiosity gap). Write three hook lines for the first 3 seconds and circle the strongest.", ""),
            ("Define your character in three lines: who they are (age, job, look), what they want, and what is in the way. "
             "This is the face the viewer follows; you will build it as an Element in Activity 2.", ""),
            ("Lay out the five beats for 15–20 seconds: HOOK (0–3 s), PROBLEM (3–6 s), TURN (6–10 s), PAYOFF (10–13 s), "
             "CALL TO ACTION (13–15 s+).", ""),
            ("Open Higgsfield Supercomputer and paste the script-and-storyboard prompt with your brief, message, hook and character. "
             "It returns a timed script and a six-panel storyboard table. (Or open your project and ask AI Director.)", ""),
            ("Review the script as an editor (A1) with the critique prompt and assets/story-review-checklist.pdf: does the hook land "
             "in 3 s, is there one message, does the character want something, is there a payoff, can each panel be shot in its time? "
             "Write down every edit you decide.", ""),
            ("Make the storyboard visual: for each panel either sketch a stick-figure frame on assets/storyboard-sheet.pdf or generate a "
             "frame in Higgsfield Image (about 2 credits each) with the frame prompt, then place it on the sheet.", ""),
            ("In Supercomputer Ask mode run the house-rules prompt and copy the five rules that apply onto the sheet (A2): "
             "platform spec, captions, music rights, consent, AI-disclosure label.", ""),
            ("Run the work-plan prompt and copy the phases onto the sheet (A3): storyboard lock, Elements, Draft takes, 1080p finals, "
             "CapCut edit, review, export, publish, each with a time and its credits (45 per 15 s Draft, 240 per 15 s 1080p final).", ""),
            ("Take ONE screenshot of the completed storyboard sheet. It is your Activity 1 evidence and the screenshot PP Task 1 asks for.", ""),
        ],
        prompts=[
            ("Script and storyboard (Supercomputer)",
             "I am making a 15-20 second vertical (9:16) video for <platform>.\n"
             "Product: <product or cause>. Audience: <who>.\n"
             "One message: <audience> should <feel/do> because <reason>.\n"
             "Hook (0-3 s): <your hook line>. Character: <who, what they want, what is in the way>.\n"
             "Write a timed script in five beats: hook, problem, turn, payoff, call to action.\n"
             "Then give me a 6-panel storyboard table with: time, shot size, camera angle, camera movement,\n"
             "action, sound, on-screen text. Do not generate any video yet."),
            ("Edit the script like an editor",
             "Act as a commercial film editor. Review this script and storyboard for: a hook that lands in 3 seconds,\n"
             "ONE clear message, a character with a want and a problem, a visual payoff, a call to action, and\n"
             "panels that cannot be shot in their time slot. List each problem and the edit you recommend,\n"
             "then rewrite only the weakest two panels."),
            ("A storyboard frame (Higgsfield Image)",
             "Storyboard frame, 9:16, simple cinematic still: <shot size> <camera angle> of <character> <action>\n"
             "in <location>, <lighting>. Plain composition, no text, no logos."),
            ("House rules: standards and guidelines (Supercomputer, Ask mode)",
             "Draft a one-page video standards and guidelines checklist for a Singapore agency making 15-30 second\n"
             "AI videos in Higgsfield and CapCut. Cover: resolution and frame rate; aspect ratio per platform (YouTube 16:9,\n"
             "TikTok and Reels 9:16); captions and audio level; saved character and location Elements only; commercial-use\n"
             "rights for footage and music; PDPA consent for real faces and voices; AI-content labels on TikTok and YouTube;\n"
             "IMDA and ASAS advertising codes. Plain checklist, five to eight lines."),
            ("Work plan with timelines and credits (Supercomputer, Ask mode)",
             "Create a post-production work plan for my 15-20 second video, due in 3 working days. Phases: storyboard lock,\n"
             "Elements, 480p Draft takes, 1080p finals, CapCut edit (cut, captions, music, colour), fixes, client review,\n"
             "export 9:16 and 16:9, publish. For each phase give owner, duration, dependency and credits (45 per 15 s Draft,\n"
             "240 per 15 s 1080p final, max three Drafts per shot). End with the credit total. Plain list."),
        ],
        assets=["brief-kopi-kaki.pdf — the default client brief (fictional coffee bar, iced kopi launch)",
                "hook-cards.pdf — six hook types with an example line for each",
                "story-review-checklist.pdf — hook, one message, character, payoff, CTA, shootable panels",
                "storyboard-sheet.pdf — the one-page sheet: brief, six panels, house rules, work plan",
                "storyboard-example-sola.jpg — a finished storyboard and the film it became (SOLA)"],
        evidence=["ONE screenshot: your completed storyboard sheet (brief, message, hook, six panels, house rules, work plan)"],
        test="The sheet states one message in one sentence and a hook for 0–3 s; it has six timed panels with size, angle, "
             "movement, action, sound and on-screen text; you listed at least two script edits; the house rules cover spec, captions, "
             "rights, consent and AI label; the work plan has phases, times and a credit total.",
    ),
]
