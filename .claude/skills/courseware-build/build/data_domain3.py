"""Topic 3 — Apply new AI technologies to Improve Video Production.  Activity 3.

v12 (23 Nov 2026): post-production in CapCut. The Higgsfield takes from Activity 2 are raw footage:
cut them to time, polish (captions, text, music, colour), check against the standards, fix what fails
(in CapCut or by regenerating one shot in Higgsfield), export to platform spec, evaluate the tools.
"""

DOMAIN3 = [
    dict(
        num=3, topic=3,
        title="Finish It in CapCut: Cut, Polish and Export the Final Video",
        objective="K4 · K5 · A6 · A7 — industry standards, new AI tools, remedial actions, evaluate the tools",
        desc="Bring your Higgsfield takes into CapCut and write the story a second time on the timeline. Cut it to 15–20 "
             "seconds, put the hook line in the first 3 seconds, add captions, music and a call to action, match the colour, "
             "check it against your house rules, fix what fails, and export a 1080p video ready to publish with an AI label.",
        build="Your final 15–20 second video, exported from CapCut at 1080p for your platform, with a quality check, two fixes and a short tool evaluation.",
        services="CapCut desktop: Media, Text, Captions (auto captions), Audio, Filters, Adjustment, Transitions, Ratio, Export · Higgsfield to regenerate one shot if needed",
        flow=["Import + ratio", "Assemble to storyboard", "Cut to 15–20 s", "Captions, text, music, colour", "Check, fix, export"],
        steps=[
            ("Open CapCut desktop (free at capcut.com) and click Create project. Click Import and add your Higgsfield MP4s "
             "from Activity 2.", ""),
            ("Set the canvas ratio in the player (Ratio → 9:16 for TikTok, Reels and Shorts, or 16:9 for YouTube). "
             "Drag the clips onto the timeline in storyboard order.", ""),
            ("Cut to time. Move the playhead and split with Cmd+B (Mac) or Ctrl+B (Windows). Delete in this order until the "
             "video is 15–20 s: logo intros and warm-ups, dead air, repeated beats, anything that does not serve the one message. "
             "Keep the hook, the payoff and the call to action. Use assets/cut-list.pdf to log each cut.", ""),
            ("Tighten the rhythm: start each shot on the action, cut on movement, hold the emotional close-up a beat longer, "
             "and end on the payoff, not after it.", ""),
            ("Text tab: put your hook line on screen in the first 3 seconds and a call-to-action card at the end. "
             "Keep text inside the safe area (away from the bottom fifth and the right edge on 9:16).", ""),
            ("Captions tab: generate auto captions, then read every line and fix wrong words, names and timing. "
             "Most viewers on social start muted.", ""),
            ("Audio tab: add music that is cleared for commercial use, lower it under the key sound (ice clink, footsteps) and fade it out at the end.", ""),
            ("Filters or Adjustment: give every clip the same colour look so Draft and final shots match. Use at most one or two transitions.", ""),
            ("Check the cut with assets/final-check.pdf against your Activity 1 house rules (K4): length, ratio, 1080p, captions correct, "
             "audio level, character continuity, rights, AI label planned. For each FAIL apply a remedial action (A6): fix it in CapCut, "
             "or regenerate just that shot in Higgsfield, then re-check.", ""),
            ("Export: 1080p, 30 fps, MP4. Watch the exported file once on your phone.", ""),
            ("Evaluate two technologies you used (A7), e.g. Higgsfield Draft mode or Elements, CapCut auto captions or AI tools: "
             "what each saved (time, credits) and what it improved (quality, consistency), and one limit.", ""),
            ("Take ONE screenshot of your finished CapCut timeline (video, text, caption and audio tracks visible). It is the screenshot "
             "PP Task 3 asks for. Upload the exported MP4 to the TMS.", ""),
        ],
        prompts=[
            ("Plan the cut (Supercomputer or any chat assistant)",
             "My raw footage runs <xx> seconds. Here is my storyboard and the list of clips with their lengths: <list>.\n"
             "I need a 15-20 second cut for <platform> with the hook in the first 3 seconds and one message: <message>.\n"
             "Tell me which clips or seconds to cut, which to keep, the order, and where the hook text,\n"
             "captions and call to action go. Give me a cut list as a table: clip, in, out, keep/cut, reason."),
            ("Caption and CTA copy",
             "Write the on-screen text for my 15-second video: a hook line of at most 6 words for 0-3 s,\n"
             "two short captions for the middle beats, and a call to action of at most 4 words.\n"
             "One message: <message>. Tone: <tone>. No claims we cannot prove."),
            ("Score the cut before export",
             "Score my cut against my house rules: 15-20 s; 9:16 at 1080p, 30 fps; hook in 0-3 s; captions accurate and\n"
             "inside the safe area; music under the key sounds, no clipping; same face in every shot; music cleared for\n"
             "commercial use; AI-generated label planned. PASS or FAIL with one reason each. For each FAIL give the cheapest\n"
             "fix: in CapCut (trim, re-caption, re-level, re-colour, reframe) or regenerate one shot in Higgsfield. Plain list."),
            ("Evaluate two technologies",
             "I used these two technologies: <first, e.g. CapCut auto captions> and <second, e.g. Higgsfield Draft mode>.\n"
             "For each, give one efficiency gain and one quality gain, one limit, then rate it on quality, speed and cost,\n"
             "control, rights and fit."),
        ],
        assets=["cut-list.pdf — clip, in, out, keep/cut, reason (the 'too long' log)",
                "final-check.pdf — the pre-export check: length, ratio, resolution, captions, audio, continuity, rights, AI label",
                "export-settings.pdf — 1080p / 30 fps / MP4 and the ratio per platform",
                "sample-cut-timeline.jpg — a 32 s raw assembly cut down to 16 s, and why each piece went"],
        evidence=["ONE screenshot: your finished CapCut timeline with video, text, caption and audio tracks visible (plus the MP4 uploaded to the TMS)"],
        test="The export runs 15–20 s at 1080p in the right ratio; the hook text lands in 0–3 s; captions are corrected; music sits "
             "under the key sounds; your check names at least two FAILs and the remedial action for each; you evaluated two "
             "technologies on what they saved and improved.",
    ),
]
