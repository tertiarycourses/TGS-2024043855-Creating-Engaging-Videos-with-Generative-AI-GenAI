#!/usr/bin/env python3
"""Generate the Learner Guide for WSQ Creating Engaging Videos with Generative AI
(GenAI) as BOTH a Markdown mirror (LG-*.md at repo root) and a DOCX
(courseware/LG-*.docx) from one source, so they never diverge.

House format: cover page, Document Version Control Record, auto TOC, Arial 11pt
body, one section per lab (Objective · Goal · What you'll build · Prompts ·
Step-by-step · Check your work), plus setup, the GenAI pipeline, assessment
prep and glossary. Detailed step-by-step lives HERE (and in labs/), not on the
slides.
"""
import os, sys
from docx import Document
from docx.shared import Pt, RGBColor
HERE=os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0,HERE)
import course_data as C
from data_domain1 import DOMAIN1; from data_domain2 import DOMAIN2
from data_domain3 import DOMAIN3
ACT=DOMAIN1+DOMAIN2+DOMAIN3
import prodoc
def _find_repo(start):
    env=os.environ.get("COURSE_REPO")
    if env and os.path.isdir(env): return env
    d=start
    for _ in range(8):
        d=os.path.dirname(d)
        if os.path.isdir(os.path.join(d,"courseware")) and os.path.isdir(os.path.join(d,"labs")): return d
    return os.path.dirname(os.path.dirname(HERE))
REPO=_find_repo(HERE); ASSETS=os.path.join(os.path.dirname(HERE),"assets")

def _slug(t):
    import re as _re
    s="".join(ch.lower() if ch.isalnum() else "-" for ch in t)
    return _re.sub(r"-+","-",s).strip("-")[:48].rstrip("-")

# ---------------- block DSL (single content stream → MD + DOCX) ----------------
B=[]
def h1(t): B.append(("h1",t))
def h2(t): B.append(("h2",t))
def h3(t): B.append(("h3",t))
def p(t):  B.append(("p",t))
def bullets(xs): B.append(("bullets",xs))
def steps(xs): B.append(("steps",xs))
def prompt(label,text): B.append(("prompt",(label,text)))
def note(t): B.append(("note",t))
def rule(): B.append(("rule",))

# ---------------- content ----------------
h1("Introduction")
p(f"This Learner Guide accompanies the WSQ course {C.TITLE} ({C.COURSE_CODE}), conducted by {C.ORG}. "
  "It provides detailed step-by-step instructions and copy-and-adapt GenAI prompts for all 12 hands-on "
  "labs, organised by the three course topics. The slides give you the concepts and each lab's overview; "
  "THIS guide is where the full procedure lives.")
p("The course is built around the five-stage GenAI video creation pipeline: "
  "(1) AI-generated script → (2) AI-generated video → (3) AI voiceover & music → (4) AI video editing → "
  "(5) agentic AI publishing to YouTube/TikTok. Every lab maps to a stage of this pipeline, and the "
  "final assessment (WA SAQ + Practical Performance) assesses exactly what the labs practise.")

h1("Course Learning Outcomes")
bullets(C.LEARNING_OUTCOMES)
h3("Skills Framework alignment")
p(f"TSC: {C.TSC_TITLE} ({C.TSC_CODE}).")
bullets(C.TSC_KNOWLEDGE + C.TSC_ABILITIES)

h1("The GenAI Video Creation Pipeline")
p("Keep this process flow in mind through every lab — it is the map of the whole course:")
steps([(f"{lbl} — {det}", "") for lbl,det in C.PIPELINE])
p("Labs 1–2 cover stage 1 (AI-generated script). Lab 3 covers stage 2 (AI-generated video). "
  "Labs 7, 10 and 11 cover stage 3 (AI voiceover & music). Labs 5–8 cover stage 4 (AI video editing). "
  "Lab 12 covers stage 5 (agentic AI publishing). Labs 4 and 9 support the pipeline with standards, "
  "work plans and AI visuals.")

h1("Before You Start — Environment Setup")
h3("What you need")
bullets([
 "A laptop (Windows or Mac) with the Chrome browser and a working internet connection.",
 "A free VEED account — sign up at veed.io with your email or Google account.",
 "A free ChatGPT account (chatgpt.com) — Gemini, Claude or Copilot also work for every script lab.",
 "A free Suno (suno.ai) and/or Udio (udio.com) account for the AI music lab.",
 "Optional: an ElevenLabs free account for voice cloning; a Google/YouTube and TikTok account for the publishing lab.",
 "A headset or earphones for reviewing audio in class.",
])
h3("Conventions used in every lab")
bullets([
 "PROMPT blocks are copy-and-adapt — replace the bracketed parts with your own topic before submitting.",
 "Free-tier limits (watermarks, generation credits) may apply; the labs are designed to work within them.",
 "Save every artifact (scripts, videos, checklists) — several labs build on the previous lab's output, and they are your evidence for the Practical Performance assessment.",
 "Only clone YOUR OWN voice, and only use footage, music and faces you have the rights and consent to use.",
])

# ---------------- per-topic, per-lab ----------------
for t in C.TOPICS:
    h1(f"Topic {t['code']} — {t['title']}")
    p(t["subtitle"]+f"  (Covers {t['weighting']}.)")
    h3("Key concepts")
    bullets([f"{k} — {v}" for k,v in t["concepts"]])
    for a in [x for x in ACT if x["topic"]==t["num"]]:
        h2(f"Lab {a['num']} — {a['title']}")
        p(f"Maps to: {a['objective']}.")
        p(f"Goal: {a['desc']}")
        h3("What you'll build")
        p(a["build"]+f"   (Tools: {a['services']}.)")
        if a.get("prompts"):
            h3("Prompts for this lab")
            for lbl,txt_ in a["prompts"]:
                prompt(lbl,txt_)
        h3("Step-by-step")
        steps([(instr,cmd) for instr,cmd in a["steps"]])
        h3("Check your work")
        p(a["test"])
        note(f"This lab has its own folder: labs/lab-{a['num']:02d}-{_slug(a['title'])}/ — "
             "open its README.md for the same steps plus tips and troubleshooting.")
        rule()

h1("Assessment Preparation")
bullets([
 "Written Assessment (SAQ), 1 hour, open book — 5 questions covering K1–K5: quality issues, AI solutions, assessment parameters, industry standards and new editing technologies.",
 "Practical Performance, 1 hour, open book — 3 tasks covering A1–A7: script + video creation, VEED editing with text/music/transitions, and text-to-video with quality remediation.",
 "Revisit Lab 8's checklist — the WA questions on quality issues and fixes mirror it directly.",
 "Keep your lab outputs open during the PP — the tasks repeat what Labs 1, 3, 5, 7 and 8 practised.",
 "Sharpen your GenAI fundamentals with the free practice exams at https://exams.tertiaryinfotech.com (e.g. the Claude Certified Associate — Foundations exam).",
])

h1("Glossary")
gl=[
 ("Generative AI (GenAI)","AI models that create new content — text, images, audio, video — from a prompt."),
 ("Prompt engineering","Structuring the instruction you give an AI (e.g. with RICCE) to control output quality."),
 ("RICCE","Role, Instructions, Context, Constraints, Example — a prompt framework for production-ready output."),
 ("Text-to-video","Generating complete video footage from a written description (Sora, Veo, Kling, VEED)."),
 ("AI avatar","A synthetic on-screen presenter that speaks your script with lip-synced delivery."),
 ("Text-to-speech (TTS)","Converting written text into natural spoken audio with an AI voice."),
 ("Voice cloning","Recreating a specific person's voice from a sample — requires that person's consent."),
 ("AI dubbing","Translating a video's speech into another language, re-voiced and lip-synced."),
 ("Auto subtitles","AI speech recognition that transcribes audio into synchronised captions."),
 ("Background removal","AI matting that separates the subject from the backdrop without a green screen."),
 ("Aspect ratio","Frame proportions — 16:9 (YouTube), 9:16 (TikTok/Shorts/Reels), 1:1 (feed)."),
 ("Agentic AI","AI that plans and executes multi-step tasks (drafting metadata, uploading, scheduling) with human approval gates."),
 ("SRT/VTT","Subtitle file formats carrying timed caption text."),
 ("Royalty-free","Licensed for use without per-use payments — always verify commercial-use rights on AI output."),
]
B.append(("dl",gl))

# ---------------- render Markdown ----------------
def _anchor(txt):
    return "".join(ch.lower() if ch.isalnum() else ("-" if ch in " -" else "") for ch in txt)

def render_md():
    out=[f"# {C.TITLE} — Learner Guide",""]
    out.append(f"**WSQ Course Code:** {C.COURSE_CODE}  |  **Conducted by:** {C.ORG} ({C.UEN.replace('UEN: ','UEN ')})  |  **Version {C.VERSION} · {C.VERSION_DATE}**")
    out.append("")
    out.append("## Contents"); out.append("")
    for kind,*rest in B:
        if kind=="h1": out.append(f"- [{rest[0]}](#{_anchor(rest[0])})")
        elif kind=="h2": out.append(f"  - [{rest[0]}](#{_anchor(rest[0])})")
    out.append("")
    for kind,*rest in B:
        if kind=="h1": out+=["",f"## {rest[0]}",""]
        elif kind=="h2": out+=["",f"### {rest[0]}",""]
        elif kind=="h3": out+=[f"**{rest[0]}**",""]
        elif kind=="p": out+=[rest[0],""]
        elif kind=="bullets": out+=[f"- {x}" for x in rest[0]]+[""]
        elif kind=="steps":
            for i,(instr,cmd) in enumerate(rest[0],1):
                out.append(f"{i}. {instr}")
                if cmd: out+=["","   ```","   "+cmd,"   ```",""]
            out.append("")
        elif kind=="prompt":
            lbl,ptext=rest[0]
            out+=[f"> **Prompt — {lbl}:**",">","> ```"]+["> "+ln for ln in ptext.split("\n")]+["> ```",""]
        elif kind=="note": out+=[f"> **Note:** {rest[0]}",""]
        elif kind=="rule": out+=["---",""]
        elif kind=="dl":
            for term,defn in rest[0]: out.append(f"- **{term}** — {defn}")
            out.append("")
    return "\n".join(out)

MD_OUT=os.path.join(REPO,f"LG-{C.SHORT_TITLE}.md")
with open(MD_OUT,"w") as f: f.write(render_md())
print("Saved",MD_OUT)

# ---------------- render DOCX ----------------
BRAND=RGBColor(0x1F,0x6F,0xEB); INKCODE=RGBColor(0x0B,0x30,0x60)
VIOLET=RGBColor(0x7C,0x3A,0xED)
doc=Document()
normal=doc.styles["Normal"]; normal.font.name="Arial"; normal.font.size=Pt(11)
prodoc.style_headings(doc)
prodoc.add_cover_page(doc,"LEARNER GUIDE",C.TITLE,C.VERSION.lstrip("v"),
                      org_logo=os.path.join(ASSETS,"tertiary-infotech-logo.png"),
                      course_logo=None, course_code=C.COURSE_CODE)
prodoc.add_version_control(doc,[
 ("6.0","1 June 2025","Prior release — Creating Engaging Videos with GenAI Learner Guide.",C.TRAINER),
 (C.VERSION.lstrip("v"),C.VERSION_DATE,
  "Major revamp: 12 hands-on labs with detailed step-by-step instructions and copy-and-adapt GenAI prompts; "
  "restructured around the 5-stage GenAI video pipeline; updated to the 2026 VEED AI toolset; "
  "new Lab 12 — agentic AI publishing to YouTube/TikTok.",C.TRAINER),
])
prodoc.add_toc(doc)

def code_para(text,mono=True):
    for line in text.split("\n"):
        para=doc.add_paragraph()
        r=para.add_run(line); r.font.name="Consolas" if mono else "Arial"
        r.font.size=Pt(9.5); r.font.color.rgb=INKCODE

for kind,*rest in B:
    if kind=="h1": doc.add_heading(rest[0],level=1)
    elif kind=="h2": doc.add_heading(rest[0],level=2)
    elif kind=="h3":
        para=doc.add_paragraph(); r=para.add_run(rest[0]); r.bold=True; r.font.size=Pt(11); r.font.color.rgb=BRAND
    elif kind=="p": doc.add_paragraph(rest[0])
    elif kind=="bullets":
        for x in rest[0]: doc.add_paragraph(x,style="List Bullet")
    elif kind=="steps":
        # manual numbering so every lab's steps restart at 1 (Word's List Number
        # style numbers continuously across the whole document)
        from docx.shared import Inches as _In
        for i,(instr,cmd) in enumerate(rest[0],1):
            para=doc.add_paragraph()
            para.paragraph_format.left_indent=_In(0.3)
            para.paragraph_format.first_line_indent=_In(-0.3)
            r=para.add_run(f"{i}."); r.bold=True
            para.add_run("\t"+instr)
            if cmd: code_para(cmd)
    elif kind=="prompt":
        lbl,ptext=rest[0]
        para=doc.add_paragraph(); r=para.add_run("PROMPT — "+lbl); r.bold=True
        r.font.size=Pt(10); r.font.color.rgb=VIOLET
        code_para(ptext)
    elif kind=="note":
        para=doc.add_paragraph(); r=para.add_run("Note: "); r.bold=True; r.font.color.rgb=BRAND
        para.add_run(rest[0]).font.size=Pt(10)
    elif kind=="rule": doc.add_paragraph("")
    elif kind=="dl":
        for term,defn in rest[0]:
            para=doc.add_paragraph(style="List Bullet")
            r=para.add_run(term+" — "); r.bold=True; para.add_run(defn)

prodoc.add_page_numbers(doc)
prodoc.enable_update_fields(doc)
DOCX_OUT=os.path.join(REPO,"courseware",f"LG-{C.SHORT_TITLE}.docx")
doc.save(DOCX_OUT)
print("Saved",DOCX_OUT)
