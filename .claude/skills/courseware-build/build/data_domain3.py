"""Topic 3 — Apply New AI Technologies to Improve Video Production.  Labs 7–9.

All in Higgsfield: remedial fixes (replace, upscale, reframe, regenerate),
voice, music and cinematic effects, model comparison and the use-case sprint
that ends in a published (or TMS-uploaded) 15-second video.
"""

DOMAIN3 = [
    dict(
        num=7, topic=3,
        title="Fix What Fails: Remedial Actions in Higgsfield",
        objective="A6 — develop remedial actions for footage that does not meet requirements; K4 — industry quality standards",
        desc="Take every FAIL from your Lab 6 checklist and match it to a Higgsfield fix: replace the wrong object, "
             "upscale soft footage, reframe for vertical, or regenerate only the broken shot with the same Elements. "
             "Apply at least two fixes and re-score.",
        build="A remediated cut with a before/after checklist and a remedy table (issue, cause, Higgsfield fix, result).",
        services="Higgsfield: Genjutsu Replace Object, Upscale, Reframe, Cinema Studio (regenerate a shot)",
        flow=["List every FAIL", "Match issue to fix", "Apply two fixes (Draft first)", "Re-score the cut", "Compliance pass"],
        steps=[
            ("Copy every FAIL from your Lab 6 checklist into assets/remedy-table.csv with its likely cause.", ""),
            ("Match each issue to a fix using assets/remedy-map.pdf: wrong or drifting object → Genjutsu Replace Object; "
             "soft or 480p footage → Upscale; wrong ratio → Reframe 16:9 to 9:16; broken shot → regenerate that shot only "
             "with the same Elements; muddy audio → regenerate with a clearer Sound line.", ""),
            ("Replace an object: open Genjutsu, choose Replace Object, upload the clip and the new prop image, describe the swap. "
             "The motion, framing and timing stay; only the object changes.", ""),
            ("Apply at least one more fix from the map. Test it on a Draft before spending on a final.", ""),
            ("Re-score the cut with the same checklist and record before/after in the remedy table.", ""),
            ("Compliance pass (K4): platform specs met, AI-content label ready, consent and rights recorded.", ""),
            ("Screenshot the before/after frames and the completed remedy table for your evidence.", ""),
        ],
        prompts=[
            ("Diagnose the cut (Supercomputer)",
             "Here is my cut and my quality checklist. For every FAIL, give: the issue, the likely cause, the Higgsfield fix\n"
             "(Replace Object, Upscale, Reframe, regenerate one shot with the same Elements, or a new Sound line) and the credit cost.\n"
             "Order the fixes cheapest first. Table."),
            ("Replace an object (Genjutsu)",
             "Replace the orange briefcase in this clip with the black hard-shell case in the reference image. Keep the hand position, "
             "motion, lighting and timing exactly the same."),
            ("Regenerate one shot only",
             "Regenerate shot 3 only. Same Elements (@char_biker, @loc_bar-interior), same framing and timing. Fix: his face must match "
             "the reference sheet and the case stays in his left hand."),
        ],
        assets=["remedy-map.pdf — issue → Higgsfield fix → typical credit cost",
                "remedy-table.csv — issue, cause, fix, before, after",
                "flawed-cut-notes.pdf — a worked example of a failing cut and its fixes"],
        evidence=["Before/after frames of each fix",
                  "Your completed remedy table with the re-scored checklist"],
        test="At least two FAILs are fixed with named Higgsfield tools, the re-score shows them as PASS, and the remedy table "
             "states the cause and credit cost of each fix.",
    ),
    dict(
        num=8, topic=3,
        title="Add Voice, Music and Cinematic Effects",
        objective="K5 — technologies that improve efficiency and quality; A7 — evaluate new technologies",
        desc="Finish the scene with the three upgrades that used to need three vendors: a generated soundtrack, a voiceover "
             "in a cloned or stock voice, and a cinematic effect. Time each one and rate it on quality, cost and control.",
        build="Your scene with a generated soundtrack, a voiceover line and one cinematic effect, plus a rated technology evaluation.",
        services="Higgsfield: Audio (music + voice), Create Voice, lighting and colour presets, effect presets",
        flow=["Generate the soundtrack", "Voiceover: clone or stock", "Apply a cinematic effect",
              "Time and cost each step", "Rate each technology"],
        steps=[
            ("Open Audio and generate a 20-second soundtrack from the music prompt. Generate two variations and keep the one "
             "that fits the cut's pace.", ""),
            ("Voice: either pick a stock voice, or create your own voice from a clean 30-second recording of YOUR voice. "
             "Clone only a voice you have consent to use; sign assets/voice-consent-form.pdf for your own.", ""),
            ("Generate the voiceover line and place it over the opening shot.", ""),
            ("Apply one cinematic effect: re-run a shot with a different Lighting preset (Silhouette or Window) and Colour "
             "palette, or apply an effect preset from the effects gallery to one shot.", ""),
            ("Record minutes and credits for each step in assets/tech-evaluation.csv and estimate what the same job takes "
             "with a studio, a composer and a voice artist.", ""),
            ("Rate each technology 1–5 on quality, speed, cost, control and rights (A7), and decide whether it joins your pipeline.", ""),
            ("Screenshot the Audio page, the effect before/after and your rated evaluation for your evidence.", ""),
        ],
        prompts=[
            ("Soundtrack",
             "Moody late-night bar soundtrack, 20 seconds, slow 80 BPM, warm Rhodes piano, soft brushed drums, upright bass, building "
             "slightly on the last 5 seconds. Instrumental, no vocals."),
            ("Voiceover line",
             "Calm, low male voice, unhurried, Singapore English: \"Some nights you don't need a plan. You just need to show up.\""),
            ("Cinematic effect re-run",
             "Same shot, same Elements. Lighting: silhouette against the window, city lights behind. Colour: Black gloss. "
             "Slow push-in. Keep timing and action identical."),
        ],
        assets=["music-prompt-cards.pdf — genre, tempo, instrument and mood cards",
                "voice-consent-form.pdf — consent to clone and use your own voice",
                "tech-evaluation.csv — technology, minutes, credits, quality, speed, cost, control, rights, verdict"],
        evidence=["Your generated soundtrack and voiceover in Higgsfield",
                  "Effect before/after and your rated technology evaluation"],
        test="The scene carries a generated soundtrack and a consented voiceover, one shot shows a clear cinematic effect, "
             "and every technology has a 1–5 rating with a keep/drop verdict.",
    ),
    dict(
        num=9, topic=3,
        title="Use-Case Sprint: One Product Photo to a Published 15-Second Ad",
        objective="A7 — evaluate new technologies; K4 — industry standards before publishing",
        desc="Run the whole pipeline on a real use case. Start from one product photo, shoot a campaign with the "
             "product-photoshoot skill, make a 15-second ad in Cinema Studio, compare two video models on the same prompt, "
             "then export, label and publish.",
        build="A 15-second ad (16:9 and 9:16) made from one product photo, a two-model comparison, and a publish-ready post.",
        services="Higgsfield: Supercomputer (/product-photoshoot), Cinema Studio, Seedance 2.5, Kling 4.0, TikTok publishing",
        flow=["One product photo in", "Campaign stills", "15 s ad, Draft first", "Compare two models", "Label, export, publish"],
        steps=[
            ("Upload the product photo from assets/ (or your own product) to Supercomputer with a character sheet and a street location.", ""),
            ("Type /product-photoshoot and ask for six vertical 9:16 photos: three with your character, three of the product alone.", ""),
            ("Open Cinema Studio, attach the product, the character and the location as references, and write the 15-second ad "
             "with the five-shot structure on the prompts page. Generate a Draft first.", ""),
            ("Run the same prompt on a second model (Kling 4.0 or Cinema Studio 4.0) and compare with assets/model-comparison.csv: "
             "product accuracy, motion, audio, credits, render time.", ""),
            ("Finalise the winner in 1080p and reframe a 9:16 version.", ""),
            ("Pre-publish check: AI-generated label on, no unlicensed logos or music, consent recorded, caption and hashtags ready.", ""),
            ("Publish to TikTok from Higgsfield (connect your account, post as private or only-me in class), or download the MP4 "
             "for the TMS upload. Screenshot the comparison table and the post settings for your evidence.", ""),
        ],
        prompts=[
            ("Campaign stills (/product-photoshoot)",
             "/product-photoshoot Make a cool photoshoot for this bottle with our runner in the three Singapore locations we picked. "
             "Six photos: three with her and three of just the bottle. Make them vertical, 9:16."),
            ("15-second ad — five shots (Cinema Studio)",
             "Scene context: A 15-second premium commercial for SOLA, a matte-black insulated steel bottle, at sunrise on a Singapore "
             "rooftop running track.\n"
             "References: @prop_sola — the bottle, 100% as shown. @char_runner — runner, 100% as shown.\n"
             "Shots (hard cut between each):\n"
             "1. 0–3s: extreme close-up, first sun ray slides across the bottle. Slow push-in.\n"
             "2. 3–6s: medium, the runner grabs it mid-stride. Tracking.\n"
             "3. 6–9s: close-up, she drinks; ice clinks. Slow motion.\n"
             "4. 9–12s: wide, she runs along the rooftop edge, skyline glowing. Drone pulls back.\n"
             "5. 12–15s: hero packshot, clean space at top for the logo.\n"
             "Sound: upbeat electronic beat building to a hit on the packshot, footsteps, ice, whoosh on each cut. No on-screen text."),
            ("Pick a use case (variation)",
             "Rewrite this ad brief as a 15-second AI micro-drama cliffhanger: same product, two characters, one twist in the last 3 seconds, "
             "vertical 9:16, dialogue in one line."),
        ],
        assets=["sample-product-sola.jpg — the product photo to start from",
                "campaign-brief.pdf — SOLA brief, audience, platforms, mandatory label",
                "model-comparison.csv — model, product accuracy, motion, audio, credits, time, verdict",
                "publish-checklist.pdf — AI label, rights, consent, caption, hashtags"],
        evidence=["Your two-model comparison table",
                  "The final 15 s ad (upload the MP4 to the TMS) and the publish settings"],
        test="The ad runs 15 s in both ratios, keeps the product accurate in every shot, the comparison table justifies the "
             "chosen model on at least three criteria, and the post carries an AI-generated label.",
    ),
]
