"""Topic 2 — Improve Video Footage on GAI Powered Video Platforms.  Activity 2.

v12 (23 Nov 2026): generate the storyboard from Activity 1 in Higgsfield, using cinematic technique
(shot size, camera angle, movement, light, lens, colour). Characters first, as Elements; then one
prompt line per storyboard panel; Draft takes before 1080p finals; review and assess the footage.
"""

DOMAIN2 = [
    dict(
        num=2, topic=2,
        title="Shoot It in Higgsfield: Characters, Cinematic Shots and Takes",
        objective="K2 · K3 · A4 · A5 — fix defects, assess quality, improve story and emotion, check the spec",
        desc="Turn your storyboard into footage. Build your character (and location) as Elements so the face never drifts, "
             "translate every storyboard panel into a prompt line with size, angle, movement and light, shoot cheap 480p "
             "Draft takes, review them against the storyboard, and finalise only the takes that tell the story.",
        build="Your storyboard shot in Higgsfield: one character Element, one location, Draft takes for every panel and 1080p finals of the keepers, reviewed and scored.",
        services="Higgsfield: Supercomputer (character-sheet skill), Image (Soul 2.0 / Nano Banana Pro), Elements, Cinema Studio, Seedance 2.5 Draft",
        flow=["Cast the character", "Save Elements", "Panel → prompt line", "Draft takes", "Review, score, finalise"],
        steps=[
            ("Open higgsfield.ai, sign in and open your project. Keep your Activity 1 storyboard sheet beside you. "
             "No paid Higgsfield plan? Use vidogrid.ai, free to start: generate the character and location on its Image page, attach them "
             "as reference images, and make 480p test takes with the same storyboard prompt (check the cost on the Generate button).", ""),
            ("Cast your character: paste the character prompt into Supercomputer. It offers casting options; pick the one that "
             "matches your storyboard and ask for a reference sheet (full body front, full body back, face portrait).", ""),
            ("Open the sheet and click Save as element: Category Character, Element ID char_<name>. Generate your location with the "
             "location prompt and save it as loc_<place>. Check both appear in My elements.", ""),
            ("Open Cinema Studio (Video). Attach @char_<name> with the Character role and @loc_<place> with the Location role.", ""),
            ("Translate the storyboard: for each panel write one prompt line in the order time, shot size, camera angle, camera "
             "movement, action, light. Add one Sound line for the whole clip. Use the storyboard-to-prompt prompt if you want "
             "Supercomputer to draft the lines from your sheet.", ""),
            ("Set the look once: camera body and lens, aperture (f/1.4 for shallow focus), lighting preset, colour palette. "
             "Choose Seedance 2.5 Draft, 9:16 (or 16:9), 15 s, sound on.", ""),
            ("Generate two or three Draft takes (never more than three per shot; about 45 credits each for 15 s). Watch each with sound.", ""),
            ("Review against your storyboard (A4): does the hook land in 3 s, does the character's emotion read in the close-up, "
             "does the payoff feel like a payoff? Write two changes that would strengthen the story or emotion and apply ONE per new take.", ""),
            ("Assess the takes with assets/footage-scorecard.pdf (A5): resolution, face and prop continuity, motion and physics, audio, "
             "ratio and safe area, length. Mark PASS or FAIL and the fix (K2).", ""),
            ("Finalise only the best take at 1080p (about 240 credits for 15 s) and download the MP4s you will edit in Activity 3.", ""),
            ("Take ONE screenshot of your Higgsfield project or Cinema Studio showing your prompt and your generated takes. "
             "It is the screenshot PP Task 2 asks for.", ""),
        ],
        prompts=[
            ("Cast the character (Supercomputer)",
             "Main character for a 15-second ad: <age>, <job>, <look and clothing>, <mood>.\n"
             "Use the character-sheet skill. Show me casting options first; after I pick one, build a 16:9\n"
             "reference sheet: full body front, full body back, face portrait, plain white background.\n"
             "Same outfit in every view."),
            ("Build the location (Image)",
             "Wide <location>, <time of day>, cinematic still, 16:9. Clear spatial anchors: <three things a shot can point at>,\n"
             "e.g. seats along both sides, silver handrails, a window with city lights passing. No people, no text, no logos."),
            ("Storyboard to prompt (Cinema Studio)",
             "Scene: @char_<name> in @loc_<place>, <one-line story>.\n"
             "Shots (cut between each):\n"
             "1. 0-3s: extreme close-up, low angle, slow push-in: <hook action>, golden-hour backlight.\n"
             "2. 3-6s: medium shot, eye level, handheld: <problem>.\n"
             "3. 6-10s: close-up, eye level, static: <turn - the emotion on her face>.\n"
             "4. 10-13s: wide shot, high angle, drone pull-back: <payoff>.\n"
             "5. 13-15s: medium shot, eye level, locked off: <product hero frame, space for the logo>.\n"
             "Sound: <ambience>, <one key sound effect on the payoff>, no dialogue."),
            ("Review the take (Supercomputer)",
             "Here is my storyboard and my Draft take. As a director, list where the take loses the story or the emotion\n"
             "(hook timing, character expression, payoff, pacing) and as an editor, score resolution, continuity,\n"
             "motion, audio and ratio PASS/FAIL. For each FAIL give the cheapest fix and its credit cost.\n"
             "Tie every story change to a numbered shot, e.g. 'Shot 3: hold the smile one more second'."),
        ],
        assets=["shot-angle-move-cards.pdf — shot sizes, camera angles and movements with what each makes the viewer feel",
                "storyboard-to-prompt.csv — one row per panel: time, size, angle, move, action, light, sound",
                "footage-scorecard.pdf — the quality parameters, PASS/FAIL, fix and credits",
                "sample-character-frame.jpg — a frame from the SOLA film: what a locked character looks like"],
        evidence=["ONE screenshot: your Higgsfield project or Cinema Studio showing your prompt and your generated takes"],
        test="Your character is a saved Element used in every take; every storyboard panel has a prompt line with size, angle and "
             "movement; you shot up to three Draft takes per shot before one 1080p final; you wrote two story/emotion changes and scored the takes "
             "PASS/FAIL on the quality parameters.",
    ),
]
