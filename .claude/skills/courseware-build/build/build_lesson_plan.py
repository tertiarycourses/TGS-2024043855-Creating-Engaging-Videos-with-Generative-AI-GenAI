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
SCHEDULE = {
 1: (C.DAY_THEMES[1], [
    ("9:30","10:00",30,"admin","Welcome, digital attendance (AM), trainer and learner introductions, ground rules, course outline and learning outcomes"),
    ("10:00","11:00",60,"topic","Topic 1 — Create and Edit Video Script Using GenAI: the GenAI video pipeline, script writing, story structure, the RICCE prompt framework (concepts + demo)"+topic_ref(1)),
    ("11:00","11:15",15,"break","Tea break"),
    ("11:15","13:00",105,"lab","Hands-on: "+lab_titles([1,2])),
    ("13:00","14:00",60,"lunch","Lunch break"),
    ("14:00","15:30",90,"lab","Digital attendance (PM). Hands-on: "+lab_titles([3,4])),
    ("15:30","15:45",15,"break","Tea break"),
    ("15:45","16:45",60,"topic","Topic 2 — Improve Video Footage on GenAI-Powered Video Platforms: VEED editor toolbox, subtitles and captions, audio enhancement, quality parameters (concepts + demo)"+topic_ref(2)),
    ("16:45","18:15",90,"lab","Hands-on: "+lab_titles([5,6])),
    ("18:15","18:30",15,"recap","Day 1 recap and Q&A"),
 ]),
 2: (C.DAY_THEMES[2], [
    ("9:30","9:45",15,"recap","Day 1 recap and digital attendance (AM)"),
    ("9:45","10:45",60,"lab","Hands-on: "+lab_titles([7])),
    ("10:45","11:00",15,"break","Tea break"),
    ("11:00","12:15",75,"lab","Hands-on: "+lab_titles([8])),
    ("12:15","13:00",45,"topic","Topic 3 — Apply New AI Technologies to Improve Video Production: AI avatars, AI music, voice cloning and dubbing, agentic AI publishing, industry standards (concepts + demo)"+topic_ref(3)),
    ("13:00","14:00",60,"lunch","Lunch break"),
    ("14:00","15:00",60,"lab","Digital attendance (PM). Hands-on: "+lab_titles([9,10])),
    ("15:00","16:00",60,"lab","Hands-on: "+lab_titles([11,12])),
    ("16:00","16:15",15,"break","Tea break"),
    ("16:15","16:30",15,"recap","Revision, course feedback and TRAQOM survey, Briefing for Assessment, Assessment digital attendance"),
    ("16:30","17:30",60,"assess","Written Assessment (WA) — Short-Answer Questions (SAQ), 1 hour, open book"),
    ("17:30","18:30",60,"assess","Practical Performance (PP) — hands-on video-production tasks, 1 hour, open book"),
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
 ("6.0","1 June 2025","Prior release — Creating Engaging Videos with GenAI 2-day lesson plan.",C.TRAINER),
 (C.VERSION.lstrip("v"),C.VERSION_DATE,
  "Major revamp: restructured around the 5-stage GenAI video pipeline (AI script → AI video → AI voice & music → AI editing → agentic publishing); 12 hands-on labs in individual folders; updated to the 2026 VEED AI toolset (AI Video Maker, avatars, voice clone, dubbing); added agentic AI publishing to YouTube/TikTok (Lab 12).",C.TRAINER),
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
      ("Mode","Instructor-led, hands-on GenAI video production labs on VEED and companion AI tools"),
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
