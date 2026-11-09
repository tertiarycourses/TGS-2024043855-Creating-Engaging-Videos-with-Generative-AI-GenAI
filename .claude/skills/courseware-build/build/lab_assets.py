"""Mock assets shipped in each lab folder (labs/lab-NN-*/assets/).

Each entry: filename -> ("pdf", title, [html blocks]) | ("csv", [rows]) | ("frame", (video, second)).
PDFs are rendered from HTML by build_labs.py; frames are grabbed from the demo films.
"""
import course_data as C

def table(head, rows):
    h = "".join(f"<th>{x}</th>" for x in head)
    b = "".join("<tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>" for r in rows)
    return f"<table><thead><tr>{h}</tr></thead><tbody>{b}</tbody></table>"

def blanks(n, label=""):
    return "".join(f"<p class='blank'>{label}{i+1}. ________________________________________________</p>" for i in range(n))

ASSETS = {
 1: {
  "first-video-log.pdf": ("pdf", "Lab 1 — First video log", [
     "<p>Fill this in after each take. It is your evidence that you can spot quality issues (K1).</p>",
     table(["", "Take A — lazy prompt", "Take B — interviewed by Supercomputer"],
           [["Character the model chose", "", ""], ["World / location", "", ""], ["Camera (size, movement)", "", ""],
            ["Sound", "", ""], ["Credits spent", "", ""]]),
     "<h3>Three quality issues I spotted</h3>", blanks(3),
     "<h3>Which issues did the interviewed take fix, and why?</h3>", blanks(2)]),
  "sample-scifi-take.jpg": ("frame", ("scifi-ring-15s.mp4", 13.8)),
  "sample-lazy-prompt-draft.mp4": ("copy", "lab1-lazy-draft-480p.mp4"),
 },
 2: {
  "story-elements-checklist.pdf": ("pdf", "Lab 2 — Story elements checklist", [
     table(["Element", "Question to ask", "Present? (Y/N)", "Edit I will make"],
           [["Identifiable hero", "Do we know who she is in the first shot?", "", ""],
            ["Clear desire", "What does she want, in one sentence?", "", ""],
            ["Obstacle", "What stands in her way?", "", ""],
            ["Action", "What visible thing does she do about it?", "", ""],
            ["Outcome", "How is her world different in the last shot?", "", ""],
            ["Filmable in 15 s", "Can every shot be seen and heard in its time slot?", "", ""]])]),
  "shot-list-template.csv": ("csv", [["shot", "time", "size (wide / MCU / CU)", "camera (static / push-in / tracking / handheld)", "action", "sound / dialogue"],
                                     ["1", "0-3s", "", "", "", ""], ["2", "3-6s", "", "", "", ""], ["3", "6-9s", "", "", "", ""],
                                     ["4", "9-12s", "", "", "", ""], ["5", "12-15s", "", "", "", ""], ["6", "", "", "", "", ""]]),
  "client-brief-online-learning.pdf": ("pdf", "Client brief — SkillUp Academy promo", [
     "<p><b>Client:</b> SkillUp Academy, a (fictional) Singapore online learning platform for working adults.</p>",
     "<p><b>Ask:</b> a 15-second promo for YouTube (16:9) and TikTok (9:16) that makes a tired working adult believe they can upskill in 15 minutes a day.</p>",
     "<p><b>Audience:</b> 25–45, full-time workers, watch on the commute with sound off.</p>",
     "<p><b>Must have:</b> one recurring character, a phone or laptop in shot, the line 'Start learning today' at the end, burned captions, an AI-generated label on publish.</p>",
     "<p><b>Must not:</b> real people's faces, competitor logos, unlicensed music, claims about salary increases.</p>",
     "<p><b>Budget:</b> 600 Higgsfield credits including all Drafts.</p>"]),
 },
 3: {
  "credit-plan-template.csv": ("csv", [["item", "shots", "drafts per shot", "credits per draft (15 s)", "finals", "credits per final (15 s)", "subtotal"],
                                       ["Scene A", "1", "3", str(C.CREDITS['draft15']), "1", str(C.CREDITS['hd15']), "=B2*C2*D2+E2*F2"],
                                       ["Scene B", "1", "3", str(C.CREDITS['draft15']), "1", str(C.CREDITS['hd15']), "=B3*C3*D3+E3*F3"],
                                       ["Elements (images)", "", "", "", "", "", "20"],
                                       ["TOTAL", "", "", "", "", "", "=SUM(G2:G4)"]]),
  "work-plan-template.csv": ("csv", [["phase", "owner", "start", "end", "dependency", "deliverable", "credits"],
                                     ["Script lock", "", "Day 1 AM", "", "brief approved", "script + shot list", "0"],
                                     ["Elements", "", "", "", "script lock", "@char / @loc / @prop", ""],
                                     ["480p Draft takes", "", "", "", "Elements", "4 takes per scene", ""],
                                     ["1080p finals", "", "", "", "take approved", "final clips", ""],
                                     ["Fix & finish", "", "", "", "finals", "captions, music, fixes", ""],
                                     ["Client review", "", "", "", "fix & finish", "approval email", "0"],
                                     ["Export 16:9 + 9:16", "", "", "", "approval", "two MP4s", "0"],
                                     ["Publish", "", "Day 3 PM", "", "export", "live post with AI label", "0"]]),
  "standards-checklist.pdf": ("pdf", "Lab 3 — Minimum items for your standards sheet", [
     table(["Area", "Your sheet must state"],
           [["Resolution & frame rate", "1080p minimum for finals; no 480p Draft in any export"],
            ["Aspect ratio", "16:9 YouTube; 9:16 TikTok / Reels / Shorts; safe area for captions"],
            ["Audio", "Dialogue clearly above music; no clipping"],
            ["Captions", "Burned in for social; max two lines; accurate and in sync"],
            ["Consistency", "Characters, locations and props only from saved Elements"],
            ["Rights", "Commercial use covered by the Higgsfield plan; music cleared"],
            ["Consent & PDPA", "No real person's face or voice without written consent"],
            ["AI disclosure", "TikTok AI-generated label on; YouTube altered/synthetic setting on"],
            ["Advertising codes", "IMDA / ASAS: no misleading claims"],
            ["Quality gate", "Draft approved before any 1080p final; checklist before export"]])]),
  "skill-template.pdf": ("pdf", "Lab 3 — Supercomputer skill template", [
     "<p>A skill is rules and guidelines for one job. Higgsfield calls Skills installable workflows: install them from the "
     "Marketplace, import them from Claude, Claude Code, Codex or ChatGPT, or write your own. Run one by typing / in Supercomputer.</p>",
     table(["Part", "What to write", "Example: /house-standards"],
           [["Name", "short, lower-case, hyphenated", "house-standards"],
            ["When to use", "the job it does and when", "Every video we make for clients"],
            ["Rules", "the non-negotiables", "Saved Elements only; Draft before 1080p; AI label on; written consent for real faces/voices; cleared music"],
            ["Steps", "the order of work", "Brief → three-part prompt → Draft → review → finalise → checklist → export 16:9 + 9:16"],
            ["Output format", "what it must hand back", "Three-part prompt + credit estimate + pass/fail checklist"]]),
     "<h3>Your skill</h3>", blanks(5)]),
 },
 4: {
  "character-brief.pdf": ("pdf", "Lab 4 — Character brief: biker road movie", [
     "<p><b>Lead:</b> a 25-year-old biker, modern style clothing, quiet and confident.</p>",
     "<p><b>Second character:</b> his friend, early 30s, curly hair and moustache, waits at the bar.</p>",
     "<h3>Casting checklist</h3>",
     table(["Check", "Option 1", "Option 2", "Option 3", "Option 4", "Option 5"],
           [["Fits the brief", "", "", "", "", ""], ["Readable face at close-up", "", "", "", "", ""],
            ["Outfit works in a dark bar", "", "", "", "", ""], ["Not a real person's likeness", "", "", "", "", ""]]),
     "<p>Sheet layout: full body front · full body back · face portrait, plain white background, 16:9.</p>"]),
  "element-naming-sheet.csv": ("csv", [["category", "name", "element id (@handle)", "reference image", "quality issue it prevents"],
                                       ["Character", "Biker", "char_biker", "", "identity drift"],
                                       ["Character", "Friend", "char_friend", "", ""],
                                       ["Location", "Bar interior", "loc_bar-interior", "", ""],
                                       ["Location", "Bar entrance", "loc_bar-entrance", "", ""],
                                       ["Prop", "Suitcase", "prop_suitcase", "", ""]]),
  "sample-product-sola.jpg": ("frame", ("marketing-sola-15s.mp4", 13.5)),
  "sample-location-bar.jpg": ("copy", "lab4-test-bar.jpg"),
  "sample-prop-suitcase.jpg": ("copy", "lab4-test-case.jpg"),
 },
 5: {
  "cinema-studio-cheatsheet.pdf": ("pdf", "Lab 5 — Cinema Studio cheat sheet", [
     table(["Control", "Options you will see", "Use it for"],
           [["References", "up to 50: 30 images, 10 videos, 10 audio", "characters, locations, camera moves, voices"],
            ["Film setup · Camera", "DV Camcorder, Modern …", "the texture of the image"],
            ["Lens", "Halation Vintage, Clean Sharp …", "glow and sharpness"],
            ["Aperture", "f/11 Deep Focus … f/1.4 Wide Open", "how much is in focus"],
            ["Movement", "static, push-in, tracking, crane …", "how the camera travels"],
            ["Lighting", "Auto, Silhouette, Practicals, Window, Overhead fall", "mood and time of day"],
            ["Colour palette", "Lime Jam, Black gloss, Film colors, Nostalgic blue, Candy pink, Soft palette, Static Noon", "the grade"],
            ["Genre · Era · Tempo", "General, Drama, Sci-fi … / period / pace", "story conventions"],
            ["Model", "Cinema Studio 4.0, Seedance 2.5, Seedance 2.5 Draft", "quality vs cost"],
            ["Settings", "480p / 720p / 1080p · 16:9 / 21:9 / 9:16 · 4–30 s · sound · 1–4 takes", "what you pay for"]])]),
  "shot-size-guide.pdf": ("pdf", "Lab 5 — Shot sizes", [
     table(["Size", "Shows", "Use it when the audience must read"],
           [["Wide", "character and surroundings", "where we are; who is in the room"],
            ["Medium close-up", "expression and upper-body action", "what they are doing"],
            ["Close-up", "a face, a reaction or an important detail", "what they feel; the prop that matters"]]),
     "<p>Write every shot as: <b>SHOT n · time · size · camera · action · sound</b>.</p>"]),
  "take-log.csv": ("csv", [["take", "character match (1-5)", "prop correct (Y/N)", "camera as asked (Y/N)", "audio (1-5)", "notes", "keep?"],
                           ["1", "", "", "", "", "", ""], ["2", "", "", "", "", "", ""], ["3", "", "", "", "", "", ""], ["4", "", "", "", "", "", ""]]),
 },
 6: {
  "quality-checklist.pdf": ("pdf", "Lab 6 — Quality checklist (K3)", [
     table(["Parameter", "PASS when", "PASS / FAIL", "Evidence / note"],
           [["Resolution & sharpness", "1080p, no soft 480p shots in the cut", "", ""],
            ["Motion & physics", "no melting hands, sliding feet or stutter at cuts", "", ""],
            ["Continuity", "faces, clothes, props and sets match shot to shot", "", ""],
            ["Audio", "dialogue clear above music, foley matches action, no clipping", "", ""],
            ["Captions", "accurate, in sync, readable, inside the safe area", "", ""],
            ["Pacing", "cuts land on action or reaction; no dead frames", "", ""],
            ["Compliance", "ratio per platform, AI label planned, consent and rights recorded", "", ""]]),
     "<h3>Three storytelling improvements (A4)</h3>", blanks(3)]),
  "continuity-log.csv": ("csv", [["shot", "prop position", "who holds it", "which hand", "same as previous shot? (Y/N)", "fix needed"],
                                 ["1", "", "", "", "-", ""], ["2", "", "", "", "", ""], ["3", "", "", "", "", ""], ["4", "", "", "", "", ""], ["5", "", "", "", "", ""]]),
  "client-standards-example.pdf": ("pdf", "Example — a filled standards sheet", [
     table(["Area", "Standard"],
           [["Finals", "1080p, 24 fps, H.264 MP4"], ["Ratios", "16:9 master; 9:16 reframe with captions inside the centre 80%"],
            ["Audio", "dialogue peaks above music by about 6 dB; no clipping"], ["Captions", "white, bottom third, two lines max"],
            ["Elements", "only @char_biker, @char_friend, @loc_bar-interior, @loc_bar-entrance, @prop_suitcase"],
            ["Disclosure", "TikTok AI-generated label on; YouTube altered/synthetic content = Yes"],
            ["Rights", "Higgsfield Plus plan, commercial use; soundtrack generated in Higgsfield"]])]),
 },
 7: {
  "remedy-map.pdf": ("pdf", "Lab 7 — Remedy map: issue → Higgsfield fix", [
     table(["Fails the check", "Likely cause", "Remedial action (A6)", "Higgsfield tool", "Typical cost"],
           [["Wrong or drifting object", "model guessed the prop", "swap the object, keep the motion", "Genjutsu Replace Object", "one generation"],
            ["Face changes in one shot", "no character reference", "regenerate that shot with @char", "Cinema Studio", f"{C.CREDITS['draft15']} credits as Draft"],
            ["Soft / 480p footage", "Draft exported", "finalise the Draft or upscale", "Seedance 2.5 · Upscale", f"{C.CREDITS['hd15']} credits per 15 s"],
            ["16:9 only", "no vertical version", "reframe to 9:16 with a safe area", "Reframe", "one job"],
            ["Muddy / wrong sound", "no Sound line", "rewrite the Sound line, regenerate", "Seedance native audio", f"{C.CREDITS['draft15']} credits as Draft"],
            ["No AI label / consent", "process gap", "turn the label on, record consent", "publish settings", "0"]])]),
  "remedy-table.csv": ("csv", [["issue (from Lab 6)", "cause", "Higgsfield fix", "credits", "before (PASS/FAIL)", "after (PASS/FAIL)"],
                               ["", "", "", "", "FAIL", ""], ["", "", "", "", "FAIL", ""], ["", "", "", "", "FAIL", ""]]),
  "flawed-cut-notes.pdf": ("pdf", "Worked example — a failing cut and its fixes", [
     "<p>A learner's 20-second bar scene scored FAIL on three parameters:</p>",
     table(["Issue", "Cause", "Fix applied", "Result"],
           [["The orange case turns black in shot 4", "prop not referenced in shot 4", "Genjutsu Replace Object with @prop_suitcase image", "PASS"],
            ["Exported at 480p", "Draft sent to export", "finalised the Draft at 1080p", "PASS"],
            ["Only 16:9", "no vertical plan", "Reframe to 9:16, captions moved up", "PASS"]]),
     "<p>Order of work: cheapest fixes first, then re-score with the same checklist.</p>"]),
 },
 8: {
  "music-prompt-cards.pdf": ("pdf", "Lab 8 — Music prompt cards", [
     table(["Card", "Genre", "Tempo", "Instruments", "Mood"],
           [["Late-night bar", "jazz-hop", "80 BPM", "Rhodes, brushed drums, upright bass", "moody, warm"],
            ["Rooftop sunrise", "electronic", "118 BPM", "plucks, sub bass, claps", "uplifting"],
            ["Sci-fi reveal", "orchestral hybrid", "70 BPM", "low strings, synth drones, taiko", "epic, awe"],
            ["Micro-drama twist", "trailer", "90 BPM", "piano hits, risers, silence", "tense"]]),
     "<p>Prompt pattern: <b>genre, length, tempo, instruments, build, vocals or instrumental</b>.</p>"]),
  "voice-consent-form.pdf": ("pdf", "Voice consent form", [
     "<p>I, ______________________, consent to my voice being recorded and used to create an AI voice in Higgsfield for "
     "the purpose of this course's lab exercises only. I understand I may delete the voice at any time.</p>",
     "<p>Signature: ____________________ &nbsp;&nbsp; Date: ____________</p>",
     "<p>Only clone your own voice, or a voice whose owner has signed this form.</p>"]),
  "tech-evaluation.csv": ("csv", [["technology", "minutes", "credits", "quality (1-5)", "speed (1-5)", "cost (1-5)", "control (1-5)", "rights (1-5)", "keep or drop"],
                                  ["Generated soundtrack", "", "", "", "", "", "", "", ""],
                                  ["Voiceover (stock or cloned)", "", "", "", "", "", "", "", ""],
                                  ["Cinematic effect / preset", "", "", "", "", "", "", "", ""]]),
 },
 9: {
  "sample-product-sola.jpg": ("frame", ("marketing-sola-15s.mp4", 13.5)),
  "campaign-brief.pdf": ("pdf", "Campaign brief — SOLA bottle", [
     "<p><b>Product:</b> SOLA, a (fictional) matte-black insulated steel water bottle.</p>",
     "<p><b>Deliverable:</b> one 15-second ad in 16:9 (YouTube) and 9:16 (TikTok), plus six campaign stills.</p>",
     "<p><b>Audience:</b> Singapore runners and gym-goers, 20–35.</p>",
     "<p><b>Mandatory:</b> the bottle accurate in every shot; space for the logo in the last 3 seconds; AI-generated label on publish.</p>",
     "<p><b>Budget:</b> 500 credits; Drafts first.</p>"]),
  "model-comparison.csv": ("csv", [["model", "product accuracy (1-5)", "motion (1-5)", "audio (1-5)", "credits", "render time", "verdict"],
                                   ["Seedance 2.5 (Draft then 1080p)", "", "", "", "", "", ""],
                                   ["Kling 4.0 / Cinema Studio 4.0", "", "", "", "", "", ""]]),
  "publish-checklist.pdf": ("pdf", "Lab 9 — Publish checklist", [
     table(["Check", "Done"],
           [["16:9 and 9:16 exports at 1080p", ""], ["Product accurate in every shot", ""], ["AI-generated label on (TikTok) / altered or synthetic = Yes (YouTube)", ""],
            ["No unlicensed logos or music", ""], ["Consent recorded for any real face or voice", ""], ["Caption written, 3–5 hashtags", ""],
            ["Posted as private / only-me in class, or MP4 uploaded to the TMS", ""]])]),
 },
 10: {
  "capstone-brief.pdf": ("pdf", "Lab 10 — Mini capstone brief", [
     "<p>Pick ONE use case, then fill in the brief. Keep it to what 15 seconds can show.</p>",
     table(["Use case", "Idea starter"],
           [["AI marketing ad", "One product, one person, one hero packshot"],
            ["AI micro drama", "Two characters, one twist in the last 3 seconds, 9:16"],
            ["AI influencer post", "One consistent creator, one product or tip, talking to camera"],
            ["Sci-fi / cinematic moment", "One world, one reveal, an establishing shot and a payoff"]]),
     table(["Brief", "Your answer"],
           [["WHO", ""], ["WHERE", ""], ["WHAT HAPPENS", ""], ["Platform and ratio", ""], ["Credit budget", "500 credits"]])]),
  "capstone-scorecard.pdf": ("pdf", "Lab 10 — Capstone scorecard", [
     table(["Parameter", "Before (PASS/FAIL)", "Fix applied", "After (PASS/FAIL)"],
           [["Resolution & sharpness", "", "", ""], ["Motion & physics", "", "", ""], ["Continuity (face / prop / set)", "", "", ""],
            ["Audio", "", "", ""], ["Captions", "", "", ""], ["Pacing", "", "", ""], ["Compliance (ratio, AI label, consent, rights)", "", "", ""]]),
     "<h3>Credit log</h3>", table(["Step", "Model / setting", "Credits"], [["", "", ""], ["", "", ""], ["", "", ""], ["", "", ""], ["Total", "", ""]]),
     "<h3>Two technologies evaluated (quality · cost · control)</h3>", blanks(2)]),
  "capstone-checklist.csv": ("csv", [["PP Task 3 evidence item", "done (Y/N)"],
                                     ["Screenshot: your planning prompt", ""], ["Screenshot: at least two Draft takes", ""],
                                     ["Screenshot: the 1080p final", ""], ["Screenshot: fix 1 before/after", ""], ["Screenshot: fix 2 before/after", ""],
                                     ["Scored scorecard", ""], ["Evaluation of two technologies", ""], ["Final MP4 downloaded for the TMS upload", ""]]),
 },
}
