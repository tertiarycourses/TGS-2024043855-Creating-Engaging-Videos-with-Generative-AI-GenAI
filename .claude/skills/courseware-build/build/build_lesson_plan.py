#!/usr/bin/env python3
"""Generate the Lesson Plan (LP) DOCX for WSQ Creating Engaging Videos with
Generative AI (GenAI) — Tertiary house format.

Cover page + Document Version Control Record + auto TOC + Arial 11pt body +
colour-coded 2-day schedule tables (9:30am–6:30pm, 8 training hours/day, 1h
lunch, tea within, final assessment Day 2 4:30pm). Content comes from
course_data + the domain data files so the LP stays aligned with the deck,
guide and labs.
"""
import os, sys
from docx import Document
from docx.shared import Pt, RGBColor, Inches
from docx.enum.table import WD_TABLE_ALIGNMENT

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

BRAND=RGBColor(0x1F,0x6F,0xEB); GREY=RGBColor(0x55,0x5B,0x66)
HEADER_FILL="1F6FEB"; TOPIC_FILL="E8F0FE"; BREAK_FILL="FFF4E5"; LUNCH_FILL="FDE9D9"; ASSESS_FILL="E8F7EE"

# ------------------------------------------------ slide references (read from the built deck)
def _slide_ranges():
    """Map each lab to its (first, last) slide number in the current deck, and each
    topic to its section slide. Slide numbers match the printed footer (cover = 1)."""
    from pptx import Presentation
    path=os.path.join(REPO,"courseware",f"{C.SHORT_TITLE}-{C.VERSION}.pptx")
    labs,topics={},{}
    if not os.path.exists(path):
        return labs,topics
    prs=Presentation(path)
    for i,s in enumerate(prs.slides,1):
        texts=[sh.text_frame.text for sh in s.shapes if sh.has_text_frame]
        joined="\n".join(texts)
        for a in ACT:
            n=a["num"]
            if f"LAB {n} · " in joined or f"LAB {n}\n" in joined or any(t.strip()==f"LAB {n}" for t in texts):
                lo,hi=labs.get(n,(i,i)); labs[n]=(min(lo,i),max(hi,i))
        for tp in C.TOPICS:
            if any(t.strip()==f"TOPIC {tp['code']}" for t in texts) and tp["num"] not in topics:
                topics[tp["num"]]=i
    return labs,topics
LAB_SLIDES,TOPIC_SLIDES=_slide_ranges()

def _ref(nums):
    rng=[LAB_SLIDES[n] for n in nums if n in LAB_SLIDES]
    if not rng: return ""
    lo=min(r[0] for r in rng); hi=max(r[1] for r in rng)
    return f" (Slides {lo}–{hi})"

def lab_titles(nums):
    return "; ".join(f"Lab {a['num']}: {a['title']}" for a in ACT if a['num'] in nums)+_ref(nums)

def topic_ref(tnum):
    return f" (from Slide {TOPIC_SLIDES[tnum]})" if tnum in TOPIC_SLIDES else ""

# ------------------------------------------------ schedule (single source of truth for timing)
SCHEDULE = {   # each LU block sums to the CP hours: LU1 4 h (9:30-14:30), LU2 5 h (14:30-18:30 + Day 2 9:30-10:30), LU3 5 h (10:30-16:30)
 1: (C.DAY_THEMES[1], [
    ("9:30","10:00",30,"admin","LU1 · Welcome, digital attendance (AM), introductions, ground rules, outline, learning outcomes and Higgsfield sign-up with the course link"),
    ("10:00","10:40",40,"topic","LU1 · Concepts for Lab 1: the impact of AI on video creation, five use cases (AI movie, micro drama, influencer, singer, marketing), Cinema Studio, the lazy prompt, Supercomputer approvals, K1 quality issues"+topic_ref(1)),
    ("10:40","11:15",35,"lab","LU1 · Hands-on: "+lab_titles([1])),
    ("11:15","11:30",15,"break","LU1 · Tea break"),
    ("11:30","12:00",30,"topic","LU1 · Concepts for Lab 2: who/where/what happens, the Supercomputer loop, AI Director, story elements, the three-part prompt, presets and Skills"),
    ("12:00","12:40",40,"lab","LU1 · Hands-on: "+lab_titles([2])),
    ("12:40","13:00",20,"topic","LU1 · Concepts for Lab 3: platform specs, credit budgets, turning standards into a skill"),
    ("13:00","14:00",60,"lunch","Lunch break"),
    ("14:00","14:30",30,"lab","LU1 · Digital attendance (PM). Hands-on: "+lab_titles([3])),
    ("14:30","15:15",45,"topic","LU2 · Concepts for Lab 4: Elements — casting, character sheets, locations, props, saving Elements, image models"+topic_ref(2)),
    ("15:15","16:15",60,"lab","LU2 · Hands-on: "+lab_titles([4])),
    ("16:15","16:30",15,"break","LU2 · Tea break"),
    ("16:30","17:00",30,"topic","LU2 · Concepts for Lab 5: references and roles, Cinema Studio controls, shot structure and sizes, sound, Draft mode and takes"),
    ("17:00","18:15",75,"lab","LU2 · Hands-on: "+lab_titles([5])),
    ("18:15","18:30",15,"recap","LU2 · Day 1 recap, Q&A"),
 ]),
 2: (C.DAY_THEMES[2], [
    ("9:30","9:45",15,"recap","LU2 · Day 1 recap and digital attendance (AM)"),
    ("9:45","10:00",15,"topic","LU2 · Concepts for Lab 6: the director's loop, continuity, issues → fixes, quality parameters"),
    ("10:00","10:30",30,"lab","LU2 · Hands-on: "+lab_titles([6])),
    ("10:30","10:45",15,"break","LU3 · Tea break"),
    ("10:45","11:15",30,"topic","LU3 · Concepts for Lab 7: remedial actions, removing and replacing objects, industry standards (K4)"+topic_ref(3)),
    ("11:15","12:00",45,"lab","LU3 · Hands-on: "+lab_titles([7])),
    ("12:00","12:20",20,"topic","LU3 · Concepts for Lab 8: voice, music and cinematic effects (K5); evaluating new technologies (A7)"),
    ("12:20","13:00",40,"lab","LU3 · Hands-on: "+lab_titles([8])),
    ("13:00","14:00",60,"lunch","Lunch break"),
    ("14:00","14:20",20,"topic","LU3 · Digital attendance (PM). Concepts for Lab 9: product references, campaign stills, from stills to video"),
    ("14:20","15:00",40,"lab","LU3 · Hands-on: "+lab_titles([9])),
    ("15:00","15:15",15,"break","LU3 · Tea break"),
    ("15:15","16:00",45,"lab","LU3 · Mini capstone (concepts + hands-on): "+lab_titles([10])),
    ("16:00","16:15",15,"topic","LU3 · Core ethical issues in GenAI video (consent, IP, deepfakes, jobs, bias, environment, transparency) and course summary"),
    ("16:15","16:30",15,"recap","LU3 · Revision, TRAQOM survey, Briefing for Assessment, Assessment digital attendance"),
    ("16:30","17:30",60,"assess","Written Assessment (WA) — Short-Answer Questions (SAQ), 1 hour, open book"),
    ("17:30","18:30",60,"assess","Practical Performance (PP) — three Higgsfield tasks, 1 hour, open book; Task 3 is the learner's own 15-second mini-project video; screenshots pasted under each task and videos uploaded to the TMS"),
 ]),
}

# ------------------------------------------------ build document
doc=Document()
normal=doc.styles["Normal"]; normal.font.name="Arial"; normal.font.size=Pt(11)
prodoc.style_headings(doc)

prodoc.add_cover_page(doc,"LESSON PLAN",C.TITLE,C.VERSION.lstrip("v"),
                      org_logo=os.path.join(ASSETS,"tertiary-infotech-logo.png"),
                      course_logo=None, course_code=C.COURSE_CODE)
prodoc.add_version_control(doc,[
 ("6","1 June 2025","Prior release — Creating Engaging Videos with GenAI 2-day lesson plan.","Tertiary Infotech Academy"),
 ("7","18 August 2026","Restructured around a 5-stage GenAI video pipeline with 12 labs on VEED and companion AI tools.","Tertiary Infotech Academy"),
 ("8","9 November 2026",
  "Whole pipeline moved into Higgsfield (Supercomputer, AI Director, Elements, Cinema Studio, Seedance 2.5 and Draft mode), replacing the multi-tool v7 stack; 9 labs in 3 topics re-timed to the CP learning units; Higgsfield sign-up with the trainer's affiliate link; two demo films and 10 real-world use-case videos embedded; trainer changed to Mr Tay Hoo Wee; PP evidence by pasted screenshots plus a TMS video upload.","Tertiary Infotech Academy"),
 ("9","9 November 2026","deck aligned to the Claude Code house design throughout — LMS login and LMS courseware slides redesigned, Big Picture folded into Topic 1, Practice Exam slide removed (not a certification-exam course), YouTube and MP4 videos click-to-play in Slide Show, Shorts-only rule applied to examples, admin and recap slides as cards, a one-page all-prompts copy page for learners, and a new Lab 10 mini capstone in which each learner directs their own 15-second video (LU3 re-timed, still 5 h); Topic 3 now ends with the core ethical issues of GenAI video; LP, LG, FG and AP realigned to the v9 slide numbers.","Tertiary Infotech Academy"),
 ("10","9 November 2026","Embedded videos fixed: each slide's transition now precedes its click-to-play timing (PowerPoint dropped the timing when the order was reversed), so all YouTube Shorts and MP4 demo films play in Slide Show; three GPT Image 2.6 images added (Topic 1 opener, ethics opener, Thank You); LP, LG, FG and AP realigned to the v10 slide numbers.","Tertiary Infotech Academy"),
 (C.VERSION.lstrip("v"),C.VERSION_DATE,"Character-sheet slides and Lab 4 now explain the covered full-body face as Higgsfield's identity trick (one clear face for the model to copy), not a defect; the first YouTube slide's trainer notes (slide 28) and the Facilitator Guide's trainer preparation say to click Enable Content first; LU and topic titles aligned to the Course Proposal wording; schedule slide redrawn as timed tiles; one Higgsfield workflow screenshot per lab added to the Learner Guide; FG, AP and answer-key formatting tidied (code lines, rubric rows, record order).","Tertiary Infotech Academy"),
])
prodoc.add_toc(doc)

def H(text,level=1):
    return doc.add_heading(text,level=level)

H("Course Information",1)
info=[("Course Title",C.TITLE),("WSQ Course Reference",C.COURSE_CODE),
      ("Training Provider",C.ORG+"  ("+C.UEN.replace('UEN: ','UEN ')+")"),
      ("TSC",f"{C.TSC_TITLE} ({C.TSC_CODE})"),
      ("Duration","2 days · 8 hours per day (16 hours, including the 2-hour final assessment)"),
      ("Daily Timing","9:30 am – 6:30 pm (1-hour lunch; tea breaks within training time)"),
      ("Mode","Classroom, instructor-led; hands-on GenAI video production labs, all in Higgsfield (higgsfield.ai, paid plan)"),
      ("Trainer",C.TRAINER)]
t=doc.add_table(rows=0,cols=2); t.style="Table Grid"
for k,v in info:
    c=t.add_row().cells; c[0].text=""; r=c[0].paragraphs[0].add_run(k); r.bold=True; r.font.size=Pt(10)
    prodoc._shade_cell(c[0],TOPIC_FILL)
    c[1].text=""; c[1].paragraphs[0].add_run(v).font.size=Pt(10)

H("Learning Outcomes",1)
doc.add_paragraph("On completion of this course, learners will be able to:")
for lo in C.LEARNING_OUTCOMES:
    p=doc.add_paragraph(style="List Bullet"); p.add_run(lo).font.size=Pt(10.5)

H("Assessment",1)
for a in [C.ASSESSMENT["written"],C.ASSESSMENT["practical"],
          "Format: Open Book — course slides, Learner Guide and approved materials only.",
          "Final assessment is conducted on Day 2 from 4:30 pm.",C.ASSESSMENT["note"]]:
    p=doc.add_paragraph(style="List Bullet"); p.add_run(a).font.size=Pt(10.5)

def set_cell(cell,text,bold=False,size=9.5,color=None,fill=None):
    cell.text=""; p=cell.paragraphs[0]
    r=p.add_run(text); r.bold=bold; r.font.size=Pt(size); r.font.name="Arial"
    if color: r.font.color.rgb=color
    if fill: prodoc._shade_cell(cell,fill)

KIND_FILL={"topic":TOPIC_FILL,"break":BREAK_FILL,"lunch":LUNCH_FILL,"assess":ASSESS_FILL,
           "admin":"F3F5F8","recap":"F3F5F8","lab":None}

H("Course Schedule",1)
for day,(theme,rows) in SCHEDULE.items():
    H(f"Day {day} — {theme}",2)
    tbl=doc.add_table(rows=0,cols=3); tbl.style="Table Grid"; tbl.alignment=WD_TABLE_ALIGNMENT.CENTER
    hdr=tbl.add_row().cells
    for i,htext in enumerate(["Time","Duration","Topic / Activity"]):
        set_cell(hdr[i],htext,bold=True,size=10,color=RGBColor(0xFF,0xFF,0xFF),fill=HEADER_FILL)
    training=0
    for start,end,mins,kind,text in rows:
        cells=tbl.add_row().cells; fill=KIND_FILL.get(kind)
        set_cell(cells[0],f"{start}–{end}",bold=(kind in ("topic","assess")),size=9.5,fill=fill)
        set_cell(cells[1],f"{mins} min",size=9.5,fill=fill)
        set_cell(cells[2],text,bold=(kind in ("topic","assess")),size=9.5,fill=fill)
        if kind!="lunch": training+=mins
    for row in tbl.rows:
        row.cells[0].width=Inches(1.15); row.cells[1].width=Inches(0.9); row.cells[2].width=Inches(4.75)
    p=doc.add_paragraph(); r=p.add_run(f"Total time: {training} minutes ({training//60} hours), excluding lunch."); r.italic=True; r.font.size=Pt(9.5); r.font.color.rgb=GREY
    assert training==480, f"Day {day} training minutes = {training}, expected 480"

H("Lab Reference (aligned to the TSC)",1)
tt=doc.add_table(rows=0,cols=3); tt.style="Table Grid"
hdr=tt.add_row().cells
for i,htext in enumerate(["Topic","K/A coverage","Labs"]):
    set_cell(hdr[i],htext,bold=True,size=10,color=RGBColor(0xFF,0xFF,0xFF),fill=HEADER_FILL)
for tp in C.TOPICS:
    acts=[a for a in ACT if a["topic"]==tp["num"]]
    cells=tt.add_row().cells
    set_cell(cells[0],f"Topic {tp['code']}: {tp['title']}",bold=True,size=9.5,fill=TOPIC_FILL)
    set_cell(cells[1],tp["weighting"],size=9.5,fill=TOPIC_FILL)
    set_cell(cells[2],", ".join(f"Lab {a['num']}" for a in acts),size=9.5)

prodoc.add_page_numbers(doc)
prodoc.enable_update_fields(doc)
OUT=os.path.join(REPO,"courseware",f"LP-{C.SHORT_TITLE}.docx")
doc.save(OUT)
print("Saved",OUT)
