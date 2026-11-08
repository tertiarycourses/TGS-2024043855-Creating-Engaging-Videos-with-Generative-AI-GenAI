"""Topic 2 — Improve Video Footage on GenAI-Powered Video Platforms.  Labs 4–6.

All in Higgsfield: Elements (characters, locations, props), references,
Cinema Studio shots and takes, Seedance 2.5 Draft, and assessing the cut.
"""

DOMAIN2 = [
    dict(
        num=4, topic=2,
        title="Build Your Elements: Characters, Locations and Props",
        objective="K2 — solutions that rectify quality issues (consistency); A4 — review footage for improvement",
        desc="Faces that change between shots are the commonest AI video defect. Fix it before you shoot: cast a "
             "character with Supercomputer, turn the pick into a reference sheet, build a location and a prop, and "
             "save each one as an Element with an @handle you can call in any prompt.",
        build="Five saved Elements, two characters, two locations and one prop, each with a reference image and an @handle.",
        services="Higgsfield: Supercomputer (character-sheet skill), Soul 2.0, Seedream 5.0 Pro, Nano Banana Pro, Elements",
        flow=["Cast five options", "Pick and build a sheet", "Edit one detail", "Build location + prop", "Save as @Elements"],
        steps=[
            ("In Supercomputer paste the casting prompt. It loads the character-sheet skill and offers five photoreal casting "
             "options (Soul 2.0). Pick the one that fits your brief.", ""),
            ("Ask for a 16:9 reference sheet of your pick: full body front, full body back, and a face portrait, plain white background.", ""),
            ("Make one targeted edit with the edit prompt (Image → Seedream 5.0 Pro, about 3 credits): change one garment and keep "
             "it the same in all views.", ""),
            ("Open the sheet, click Save as element. Set Category = Character, Name = Biker, Element ID = char_biker. "
             "Add a one-line description. Repeat for a second character (char_friend).", ""),
            ("Generate the bar interior with the location prompt (Nano Banana Pro, about 2 credits). Check the space has clear "
             "spatial anchors (the counter, the stools, the window) you can name in a shot. Save as loc_bar-interior; "
             "repeat for loc_bar-entrance.", ""),
            ("Generate the prop on two image models with the same prompt and compare shape, colour and credit cost. "
             "Save the better one as prop_suitcase.", ""),
            ("Open My elements and check all five Elements are listed with their @handles. Screenshot the list for your evidence.", ""),
            ("Review: which quality issue does each Element prevent (K2)? Write one line per Element in the naming sheet.", ""),
        ],
        prompts=[
            ("Cast a character (Supercomputer)",
             "Main character in a biker road movie, 25 years old, modern style clothing.\n"
             "Use the character-sheet skill. Show me five photoreal casting options first; I will pick one before you build the reference sheet."),
            ("Edit one detail, keep it consistent",
             "Give him a silver wallet chain hanging off his jeans pocket. Replace the black t-shirt with a plain white ribbed cotton tank top, "
             "same tank top in all views."),
            ("Location with spatial anchors",
             "Wide interior of a dim neighbourhood bar at night: long wooden counter on the right with eight black stools, beer taps and backlit "
             "bottles, a pool table at the back, warm practical lamps, one large window on the left wall. Photoreal, 16:9, no people."),
            ("Prop (run on two models)",
             "A slim orange hard-shell briefcase with a ribbed moulded lid, rounded corners, a black top handle and two metal latches, "
             "white background, soft studio light, no logos or text."),
        ],
        assets=["character-brief.pdf — the biker road-movie brief and casting checklist",
                "element-naming-sheet.csv — category, name, @handle, what it prevents",
                "sample-product-sola.jpg — a product reference for Labs 8–9",
                "sample-location-bar.jpg and sample-prop-suitcase.jpg — the Lab 4 prompts run for this course"],
        evidence=["My elements page showing your saved characters, locations and prop with @handles",
                  "Your character reference sheet (front, back, face)"],
        test="Five Elements are saved with char_/loc_/prop_ handles; the character sheet shows the same face and outfit "
             "in all three views; each Element has a line saying which quality issue it prevents.",
    ),
    dict(
        num=5, topic=2,
        title="Direct Shots and Takes in Cinema Studio",
        objective="A4 — review footage to improve storytelling; K2 — solutions to rectify quality issues",
        desc="Direct a 15-second bar scene the way a film crew would: attach your Elements as references with roles, "
             "set camera, lens, lighting and colour, write the shots and the sound, then render four 480p Draft takes. "
             "Finalise only the best take in 1080p.",
        build="Four Draft takes of one scene and one 1080p final of the best take, made from your Elements.",
        services="Higgsfield: Cinema Studio, Seedance 2.5 / Seedance 2.5 Draft, References, Elements",
        flow=["Attach references with roles", "Set camera, light, colour", "Write context, shots, sound",
              "Render 4 Draft takes", "Finalise the best in 1080p"],
        steps=[
            ("Open Video → Cinema Studio. Click References and attach @char_biker, @char_friend, @prop_suitcase and "
             "@loc_bar-interior. One generation accepts up to 50 references: 30 images, 10 videos, 10 audio.", ""),
            ("Give each reference a role: Character for the people, Location for the bar. Type @ in the prompt to insert a handle.", ""),
            ("Open Film setup: choose a camera body, a lens and an aperture (f/1.4 wide open for shallow focus). "
             "Open Lighting: pick Practicals. Open Colour palette: pick Film colors. Set Genre to Drama.", ""),
            ("Write the prompt in three parts (prompts page): scene context, references with '100% as shown in the "
             "reference image', then numbered shots with sizes and camera.", ""),
            ("Choose the shot structure: one continuous 15-second shot, or multishot with a cut between each. Use the "
             "multishot version for this lab.", ""),
            ("Add the Sound line: bar ambience, footsteps, clothing movement and the one line of dialogue.", ""),
            ("Select Seedance 2.5 Draft, 480p, 21:9 or 16:9, 15 s, sound On, 4 videos. Press Generate Draft "
             "(about 45 credits per take).", ""),
            ("Watch all four takes with sound. Note for each: character match, prop position, camera, audio. Pick one.", ""),
            ("Open the chosen Draft and finalise it in 1080p (Seedance 2.5 renders the same take at full resolution, "
             "about 240 credits for 15 s; drafts can be finalised within 7 days).", ""),
            ("Screenshot the Cinema Studio prompt panel with the references attached and the four-take grid for your evidence.", ""),
        ],
        prompts=[
            ("Bar scene — three-part prompt (Seedance 2.5)",
             "Scene context: Biker enters a bar with a suitcase, looking for his friend. They notice each other, and the biker walks over and "
             "sits next to him as he lays his case flat on the counter.\n"
             "References:\n"
             "@char_biker — biker, 100% as shown in the reference image.\n"
             "@char_friend — friend, 100% as shown in the reference image. He is seated on a stool on the side of the bar counter.\n"
             "@prop_suitcase — suitcase, 100% as shown in the reference image. It belongs to @char_biker. He carries it in his left hand.\n"
             "@loc_bar-interior — the bar, 100% as shown in the location reference.\n"
             "Shots (cut between each):\n"
             "1. 0–3s: wide, the biker pushes through the door, suitcase in his left hand.\n"
             "2. 3–6s: medium shot, the friend looks up from his beer. Static camera.\n"
             "3. 6–9s: close-up, the biker recognises him.\n"
             "4. 9–12s: medium close-up, the biker sits; dialogue: \"Told you I'd make it.\"\n"
             "5. 12–15s: close-up, he lays the case flat on the counter.\n"
             "Sound: bar ambience, footsteps, leather jacket movement, the line of dialogue."),
            ("One continuous shot (compare)",
             "One continuous 15-second take. Follow a man along a busy New York sidewalk. Move from behind him to a frontal view as he "
             "reaches the corner. Keep the action uninterrupted, with no cuts."),
        ],
        assets=["cinema-studio-cheatsheet.pdf — camera, lens, aperture, lighting, colour, genre, era, tempo",
                "shot-size-guide.pdf — wide, medium close-up, close-up and what each one is for",
                "take-log.csv — take, character match, prop, camera, audio, keep?"],
        evidence=["Cinema Studio prompt panel with your references attached",
                  "The four Draft takes and your 1080p final"],
        test="All four Drafts use your Elements; your take log scores each take; the 1080p final is the take you scored best "
             "and keeps the same faces, prop and bar.",
    ),
    dict(
        num=6, topic=2,
        title="Cut, Caption and Assess the Scene",
        objective="A4 — review edited footage to improve storytelling; A5 — assess footage against technical and legal requirements; K3 — quality parameters",
        desc="Keep the useful first take, direct one more, then have Supercomputer assemble the takes into a captioned "
             "cut with a soundtrack. Score the cut against the quality parameters and your Lab 3 standards before anything is exported.",
        build="A captioned 15–30 s cut in 16:9 and 9:16 with a scored quality checklist and a list of storytelling improvements.",
        services="Higgsfield: Cinema Studio, Supercomputer (video montage: trims, soundtrack, burned captions)",
        flow=["Keep a useful first take", "Direct one change", "Continuity check",
              "Assemble, caption, soundtrack", "Score against the checklist"],
        steps=[
            ("Watch your Lab 5 final with sound. Choose ONE change (or one variation) and write it as a single instruction.", ""),
            ("Generate one new Draft take with that change. Keep both prompts and both clips: the comparison is your evidence.", ""),
            ("Run the continuity check on the prop: where is it, who holds it, does it stay the same from shot to shot? "
             "Log it in assets/continuity-log.csv.", ""),
            ("Open Supercomputer and paste the assembly prompt with your two best clips. It trims, orders, adds a soundtrack "
             "and burns captions, then exports 16:9 and 9:16.", ""),
            ("Score the cut with assets/quality-checklist.pdf: resolution and sharpness, frame rate and motion, continuity of "
             "faces and props, audio (dialogue above music, no clipping), captions (accurate, in sync, readable), pacing, compliance.", ""),
            ("Assess compliance against your Lab 3 sheet: correct ratio per platform, AI-content label planned, no real "
             "person's likeness without consent, music cleared for commercial use.", ""),
            ("List three areas of improvement that would make the story land better (A4), for example a stronger opening "
             "image, a cut that lands on the reaction, or a sound cue on the payoff.", ""),
            ("Screenshot the scored checklist and both exports for your evidence.", ""),
        ],
        prompts=[
            ("Direct one change",
             "Keep everything in this take the same. Change one thing only: in shot 3 make the camera push in slowly on the biker's face "
             "as he recognises his friend, and add a beat of silence before the dialogue."),
            ("Assemble, caption and score (Supercomputer)",
             "Assemble these two clips into one 20-second cut: take 2 first, then shots 4–5 of take 1. Trim dead frames at each cut.\n"
             "Add a moody low-tempo soundtrack under the bar ambience, keep the dialogue clearly above the music.\n"
             "Burn captions for the dialogue: white, bottom third, two lines max. Export 16:9 and 9:16.\n"
             "Then score the cut against: resolution, motion, face/prop continuity, audio, captions, pacing, platform compliance. Table, pass/fail."),
        ],
        assets=["quality-checklist.pdf — the seven quality parameters with pass/fail criteria",
                "continuity-log.csv — shot, prop position, who holds it, same as previous?",
                "client-standards-example.pdf — a filled standards sheet to assess against"],
        evidence=["Your scored quality checklist (before export)",
                  "Your 16:9 and 9:16 exports with captions"],
        test="The checklist scores every parameter with a reason, the cut exports in both ratios with readable captions, "
             "and you name three storytelling improvements tied to specific shots.",
    ),
]
