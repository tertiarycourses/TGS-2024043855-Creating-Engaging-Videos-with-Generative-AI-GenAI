"""Templates and samples shipped in each activity folder (labs/lab-0N-*/assets/).

v12 (23 Nov 2026): three activities. Each entry: filename -> ("pdf", title, [html blocks]) | ("csv", [rows])
| ("frame", (video, second)) | ("copy", video file) | ("img", path under the skill's assets/).
"""
import course_data as C

def table(head, rows):
    h = "".join(f"<th>{x}</th>" for x in head)
    b = "".join("<tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>" for r in rows)
    return f"<table><thead><tr>{h}</tr></thead><tbody>{b}</tbody></table>"

def blanks(n, label=""):
    return "".join(f"<p class='blank'>{label}{i+1}. ________________________________________________</p>" for i in range(n))

PANEL_ROWS = [[str(i), "", "", "", "", "", ""] for i in range(1, 7)]

ASSETS = {
 1: {
  "brief-kopi-kaki.pdf": ("pdf", "Client brief — Kopi Kaki iced kopi launch (fictional)", [
     "<p><b>Client:</b> Kopi Kaki, a (fictional) neighbourhood coffee bar in Tiong Bahru launching a bottled iced kopi.</p>",
     "<p><b>Ask:</b> a 15–20 second vertical video (9:16) for TikTok and Instagram Reels.</p>",
     "<p><b>Audience:</b> office workers aged 25–40 who need an afternoon pick-me-up; they watch on their phone with sound off.</p>",
     "<p><b>One message (draft):</b> office workers should grab an iced kopi at 3 pm because it beats the slump in one sip.</p>",
     "<p><b>Must have:</b> a recurring character, the bottle in shot, a hook in the first 3 seconds, burned captions, a call to action, an AI-generated label on publish.</p>",
     "<p><b>Must not:</b> real people's faces, competitor logos, unlicensed music, health claims.</p>",
     "<p><b>Budget:</b> 600 Higgsfield credits including all Drafts.</p>"]),
  "hook-cards.pdf": ("pdf", "Activity 1 — Six hook types", [
     table(["Hook type", "How it works", "Example", "Your hook line"],
           [["Ask a question", "Opens a gap the viewer wants closed", "'Still yawning at 3 pm?'", ""],
            ["Drop a number", "A specific figure feels like news", "'One sip. Zero slump.'", ""],
            ["Break the pattern", "An image the feed does not expect", "A coffee cup in a snow globe", ""],
            ["Start mid-action", "Open on movement; explain later", "Ice cascading into a glass", ""],
            ["Before / after", "Two frames tell the story", "Slumped at the desk → sitting up, grinning", ""],
            ["Open a loop", "Promise a payoff at the end", "'Watch what happens at 3:01 pm.'", ""]]),
     "<h3>My three hook lines (circle the strongest)</h3>", blanks(3)]),
  "story-review-checklist.pdf": ("pdf", "Activity 1 — Story review checklist (A1)", [
     table(["Check", "Question to ask", "Y / N", "Edit I made"],
           [["Hook", "Does something happen in the first 3 seconds?", "", ""],
            ["One message", "Can I say it in one sentence without 'and' twice?", "", ""],
            ["Character", "Do we see a face early? What do they want? What is in the way?", "", ""],
            ["Turn", "What does the product or idea do in panel 3?", "", ""],
            ["Payoff", "Does the last panel look different from the first?", "", ""],
            ["Call to action", "Does the viewer know what to do next?", "", ""],
            ["Shootable", "Can each panel happen in its time slot?", "", ""]])]),
  "storyboard-sheet.pdf": ("pdf", "Activity 1 — Storyboard sheet", [
     table(["Brief", "One message (one sentence)", "Hook (0–3 s)", "Character (who · want · problem)", "Platform · ratio · length"],
           [["", "", "", "", ""]]),
     table(["Panel", "Time", "Frame (sketch or image)", "Size · angle · move", "Action", "Sound", "On-screen text"], PANEL_ROWS),
     "<h3>House rules (A2)</h3>", blanks(5, "Rule "),
     "<h3>Work plan and credit budget (A3)</h3>",
     table(["Phase", "Owner", "When", "Credits"],
           [["Storyboard lock", "", "", "0"], ["Elements", "", "", ""], ["480p Draft takes", "", "", ""], ["1080p finals", "", "", ""],
            ["CapCut edit", "", "", "0"], ["Review", "", "", "0"], ["Export + publish", "", "", "0"], ["TOTAL", "", "", ""]])]),
  "storyboard-example-sola.jpg": ("img", "sb/storyboard-sola.jpg"),
 },
 2: {
  "shot-angle-move-cards.pdf": ("pdf", "Activity 2 — Shot sizes, camera angles, camera movement", [
     table(["Shot size", "Shows", "Use it for"],
           [["Extreme wide (EWS)", "The whole world", "Where are we? Scale."], ["Wide (WS)", "Full body + place", "Context, entrances"],
            ["Medium (MS)", "Waist up", "Action, gesture"], ["Medium close-up (MCU)", "Chest up", "Conversation"],
            ["Close-up (CU)", "The face", "Emotion, reaction"], ["Extreme close-up (ECU)", "A detail", "The product, a hand, an eye"]]),
     table(["Camera angle", "Makes the viewer feel"],
           [["Eye level", "Neutral, honest"], ["Low angle", "Power, confidence"], ["High angle", "Small, tired, vulnerable"],
            ["Bird's-eye", "Pattern, overview"], ["Dutch tilt", "Unease"], ["Over-the-shoulder / POV", "Inside the scene"]]),
     table(["Camera movement", "Meaning"],
           [["Push-in", "Emotion rising"], ["Pull-out / drone pull-back", "Reveal, scale"], ["Pan / tilt", "Follow a look"],
            ["Tracking", "Energy, momentum"], ["Crane / orbit", "Hero moment"], ["Handheld / locked off", "Urgency / calm"]])]),
  "storyboard-to-prompt.csv": ("csv", [["panel", "time", "shot size", "camera angle", "camera movement", "action", "light", "sound"],
                                       ["1 hook", "0-3s", "", "", "", "", "", ""], ["2 problem", "3-6s", "", "", "", "", "", ""],
                                       ["3 turn", "6-10s", "", "", "", "", "", ""], ["4 payoff", "10-13s", "", "", "", "", "", ""],
                                       ["5 call to action", "13-15s", "", "", "", "", "", ""], ["6 (optional)", "", "", "", "", "", "", ""]]),
  "footage-scorecard.pdf": ("pdf", "Activity 2 — Footage scorecard (K3, A5)", [
     table(["Parameter", "What PASS looks like", "Take 1", "Take 2", "Fix (K2)", "Credits"],
           [["Resolution", "1080p for the final; no 480p left", "", "", "", ""],
            ["Continuity", "Same face, clothes, prop, set", "", "", "", ""],
            ["Motion & physics", "No melting hands or sliding feet", "", "", "", ""],
            ["Audio", "Effects match the action", "", "", "", ""],
            ["Ratio & safe area", "9:16 or 16:9 as planned", "", "", "", ""],
            ["Length & pacing", "Each panel lands in its time", "", "", "", ""]]),
     "<h3>Two story or emotion changes, each tied to a shot (A4)</h3>", blanks(2, "Shot ")]),
  "sample-character-frame.jpg": ("frame", ("marketing-sola-15s.mp4", 7.5)),
 },
 3: {
  "cut-list.pdf": ("pdf", "Activity 3 — Cut list (too long? log every cut)", [
     table(["Clip", "In", "Out", "Keep / cut", "Reason"], [[str(i), "", "", "", ""] for i in range(1, 11)]),
     "<p>Cut in this order: intros and outros, warm-ups, repeats, dead air, second messages. Never cut the hook, the one message, the payoff or the call to action.</p>"]),
  "final-check.pdf": ("pdf", "Activity 3 — Final check before export (K4, A6)", [
     table(["Check", "Standard", "PASS / FAIL", "Remedial action (A6)"],
           [["Length", "15–20 s", "", ""], ["Ratio", "9:16 (TikTok, Reels, Shorts) or 16:9 (YouTube)", "", ""],
            ["Resolution", "1080p, 30 fps", "", ""], ["Hook", "On screen in 0–3 s", "", ""],
            ["Captions", "Accurate, in sync, inside the safe area", "", ""], ["Audio", "Music under the key sounds; no clipping", "", ""],
            ["Continuity", "Same face and colour look in every shot", "", ""], ["Rights", "Music and footage cleared for commercial use", "", ""],
            ["Consent", "No real face or voice without written consent", "", ""], ["AI label", "Planned for TikTok / YouTube", "", ""]]),
     "<h3>Two technologies I used and what they did (A7)</h3>", blanks(2)]),
  "export-settings.pdf": ("pdf", "Activity 3 — Export settings per platform", [
     table(["Platform", "Ratio", "Size", "Frame rate", "Format", "Before you post"],
           [["TikTok", "9:16", "1080×1920", "30 fps", "MP4 (H.264)", "AI-generated label on"],
            ["Instagram Reels", "9:16", "1080×1920", "30 fps", "MP4", "Label AI content"],
            ["YouTube Shorts", "9:16", "1080×1920", "30 fps", "MP4", "Altered or synthetic content setting"],
            ["YouTube", "16:9", "1920×1080", "30 fps", "MP4", "Altered or synthetic content setting"]]),
     f"<p>{C.CAPCUT_NOTE}</p>"]),
  "sample-cut-timeline.jpg": ("img", "sb/cut-timeline.jpg"),
 },
}
