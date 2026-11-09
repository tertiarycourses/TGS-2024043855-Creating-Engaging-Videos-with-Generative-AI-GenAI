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
  "It gives the full step-by-step instructions and copy-and-adapt prompts for all 10 hands-on labs (Lab 10 is a mini capstone), organised "
  "by the three course topics. The slides give you the concepts and each lab's overview; this guide is where "
  "the full procedure lives.")
p("Every lab runs in one studio: Higgsfield (higgsfield.ai). You brief Supercomputer, Higgsfield's agent, in plain "
  "English, or you direct each shot yourself in Cinema Studio. Two 15-second films made this way for the course "
  "(a SOLA product ad and the Ringfall sci-fi scene) are embedded in the slides, so you can see the finish line before you start.")

h1("Course Learning Outcomes")
bullets(C.LEARNING_OUTCOMES)
h3("Skills Framework alignment")
p(f"TSC: {C.TSC_TITLE} ({C.TSC_CODE}).")
bullets(C.TSC_KNOWLEDGE + C.TSC_ABILITIES)

h1("The Higgsfield Video Pipeline")
p("Keep this process in mind through every lab; it is the map of the whole course:")
steps([(f"{lbl} — {det}", "") for lbl,det in C.PIPELINE])
p("Labs 1–3 cover stage 1 (script, shot list, standards and budget). Lab 4 covers stage 2 (Elements). "
  "Labs 5–6 cover stage 3 (shots, takes and assessing the cut). Labs 7–8 cover stage 4 (fix and finish). "
  "Lab 9 runs the whole pipeline on a real use case and covers stage 5 (publish).")

h1("Before You Start — Environment Setup")
h3("What you need")
bullets([
 "A laptop (Windows or Mac) with Chrome and a working internet connection; a headset for reviewing audio.",
 f"A Higgsfield account. Sign up at {C.HF_SIGNUP} ({C.HF_DISCLOSURE})",
 C.HF_PLAN_NOTE,
 "Budget guide: a 15-second Seedance 2.5 Draft (480p) costs about 45 credits; the 1080p final of the same 15 s about 240 (read on Higgsfield, 9 Nov 2026). Labs 1–9 are designed around Draft takes, with one or two 1080p finals.",
 "Optional for Lab 9: a TikTok account to connect in Higgsfield (post as private or only-me in class).",
 f"Reference: Higgsfield API docs — {C.HF_DOCS} (authentication, requests, polling, webhooks, model endpoints); Supercomputer and Skills — https://higgsfield.ai/supercomputer-intro",
])
h3("Conventions used in every lab")
bullets([
 "PROMPT blocks are copy-and-adapt: replace the bracketed parts with your own idea before submitting.",
 "Draft first: test every idea on Seedance 2.5 Draft (480p) and finalise only the take you would show a client.",
 "Approve every spend yourself in Supercomputer; leave 'Always allow' off in class.",
 "Save every artefact (prompts, takes, checklists, exports): later labs build on them, and they are your Practical Performance evidence.",
 "Only clone YOUR OWN voice, and only use faces, products, music and footage you have the rights and consent to use.",
 "Each lab folder holds README.pdf (these steps), prompts.pdf, prompts.html (one-click copy) and assets/ with the mock files.",
 "All prompts in one place: open labs/prompts.html — every lab's prompts with a search box and a Copy button on each.",
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
        if a.get("assets"):
            h3("Mock assets in the lab folder")
            bullets(a["assets"])
        if a.get("evidence"):
            h3("Evidence to keep (screenshots for the PP)")
            bullets(a["evidence"])
        note(f"This lab has its own folder: labs/lab-{a['num']:02d}-{_slug(a['title'])}/ — "
             "README.pdf holds these steps; prompts.html copies each prompt in one click.")
        rule()

h2("Core Ethical Issues in GenAI Video")
p("Topic 3 ends with the ethical issues every AI video raises. Each comes with the rule you apply in your own Higgsfield projects.")
for h_,d_,r_ in C.ETHICS:
    h3(h_); p(d_); p("Your rule: "+r_)
h3("Real cases: lawsuits, disputes and rulings")
bullets([f"{c} — {w} ({src})" for _,c,w,src in C.ETHICS_CASES])
rule()

h1("Assessment Preparation")
bullets([
 "Written Assessment (SAQ), 1 hour, open book: 5 questions covering K1–K5: quality issues in AI video, solutions in Higgsfield, quality parameters, industry standards and new technologies.",
 "Practical Performance (PP), 1 hour, open book: 3 Higgsfield tasks covering A1–A7 that mirror Labs 1–3, 4–6 and 7–9. Paste screenshots of your work into the box under each task and upload your final video (MP4) to the TMS.",
 "Revisit the slide 'Quality issues → the Higgsfield fix' and your Lab 6 checklist: the WA questions on issues and fixes mirror them.",
 "Keep your Lab Studio project open during the PP; your saved Elements and prompts save you time.",
])

h1("Glossary")
gl=[
 ("Higgsfield","An AI video studio (higgsfield.ai) holding many image and video models, an agent and cinematic controls in one place."),
 ("Supercomputer","Higgsfield's agent: you brief it in plain English, it writes prompts, calls tools and asks you to approve each spend."),
 ("Cinema Studio","Higgsfield's director panel: references, camera body, lens, aperture, lighting, colour palette, genre, model and settings."),
 ("AI Director","The director chat inside a Higgsfield project that writes scripts and storyboards."),
 ("Seedance 2.5","ByteDance's video model in Higgsfield: 4–30 s, up to 1080p, native audio, up to 50 references."),
 ("Draft mode","Seedance 2.5 Draft renders a cheap 480p take that can be finalised at 1080p within seven days."),
 ("Element","A saved character, location or prop with an @handle (e.g. @char_biker) reused as a reference in any prompt."),
 ("Reference","An image, video or audio file attached to a generation with a role: character, location, camera move or voice."),
 ("Shot / take","A shot is one camera set-up in the script; a take is one generated attempt at it."),
 ("Multishot","One generation containing several shots with cuts between them."),
 ("Genjutsu","Higgsfield's tool for replacing objects or copying motion in existing footage."),
 ("Aspect ratio","Frame proportions: 16:9 (YouTube), 9:16 (TikTok, Shorts, Reels), 21:9 (cinema)."),
 ("AI disclosure label","The platform setting that marks realistic AI-generated content (TikTok's AI-generated label, YouTube's altered or synthetic content setting)."),
 ("Credits","Higgsfield's usage currency; every generation shows its credit cost before you approve it."),
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
 ("6.0","1 June 2025","Prior release — Creating Engaging Videos with GenAI Learner Guide.","Tertiary Infotech Academy"),
 ("7","18 August 2026","12 hands-on labs on VEED and companion AI tools, restructured around a 5-stage GenAI video pipeline.","Tertiary Infotech Academy"),
 ("8","9 November 2026",
  "Whole pipeline moved into Higgsfield: 9 labs on Supercomputer, AI Director, Elements, references, Cinema Studio, "
  "Seedance 2.5 Draft mode, remedial fixes, voice, music, effects and a published use-case ad; mock assets and one-click "
  "prompt pages per lab; Higgsfield sign-up and plan terms; PP evidence by pasted screenshots and a TMS video upload.","Tertiary Infotech Academy"),
 (C.VERSION.lstrip("v"),C.VERSION_DATE,"deck aligned to the Claude Code house design throughout — LMS login and LMS courseware slides redesigned, Big Picture folded into Topic 1, Practice Exam slide removed (not a certification-exam course), YouTube and MP4 videos click-to-play in Slide Show, Shorts-only rule applied to examples, admin and recap slides as cards, a one-page all-prompts copy page for learners, and a new Lab 10 mini capstone in which each learner directs their own 15-second video (LU3 re-timed, still 5 h); Topic 3 now ends with the core ethical issues of GenAI video; LP, LG, FG and AP realigned to the v9 slide numbers.","Tertiary Infotech Academy"),
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
