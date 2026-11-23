#!/usr/bin/env python3
"""Generate the WSQ 'Creating Engaging Videos with Generative AI (GenAI)' slide deck
(all-white Tertiary house style, v2 visual engine).

Highly visual by design: process maps with real connectors, tile grids, compare
tables, prompt cards and profile cards — NO step-by-step slides (detailed steps
live in the Learner Guide and labs/ only) and no bullet walls. Content is driven
entirely by course_data.py + data_domain1..3.py so the deck stays 100% aligned
with the LP, LG, labs and assessment.
"""
import os, sys, math, re
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE, MSO_CONNECTOR
from pptx.oxml.ns import qn
from lxml import etree

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import course_data as C
from data_domain1 import DOMAIN1
from data_domain2 import DOMAIN2
from data_domain3 import DOMAIN3
ACTIVITIES = DOMAIN1 + DOMAIN2 + DOMAIN3

def _find_repo(start):
    env = os.environ.get("COURSE_REPO")
    if env and os.path.isdir(env):
        return env
    d = start
    for _ in range(8):
        d = os.path.dirname(d)
        if os.path.isdir(os.path.join(d, "courseware")) and os.path.isdir(os.path.join(d, "labs")):
            return d
    return os.path.dirname(os.path.dirname(HERE))
REPO = _find_repo(HERE)
ASSETS = os.path.join(os.path.dirname(HERE), "assets")

# ---------------- palette ----------------
# Design system copied from "Agentic AI Applications with Claude Code" v26 (TGS-2025052468):
# terracotta accent, charcoal dark slides, warm greys, cream cards, Cambria headings + Calibri body.
CORAL=RGBColor(0xD9,0x77,0x57); RUST=RGBColor(0xC2,0x60,0x3F); TEAL=RGBColor(0x3A,0x7D,0x7B)
OCHRE=RGBColor(0xB8,0x8A,0x3E); BLUE=CORAL; VIOLET=RUST; AMBER=OCHRE
INK=RGBColor(0x21,0x20,0x1C); INK2=RGBColor(0x2E,0x2C,0x26); GREY=RGBColor(0x6B,0x68,0x62)
MUTE=RGBColor(0x8A,0x86,0x7D); PALE=RGBColor(0xB9,0xB4,0xA9); LIGHT=RGBColor(0xFA,0xF9,0xF5)
WHITE=RGBColor(0xFF,0xFF,0xFF); LINE=RGBColor(0xE8,0xE5,0xDE); BROWN=RGBColor(0x4A,0x36,0x2C)
DARKBG=RGBColor(0x21,0x20,0x1C); CODEBLUE=RGBColor(0xF2,0xD4,0xC4)
SERIF="Cambria"; SANS="Calibri"

prs=Presentation(); prs.slide_width=Inches(13.333); prs.slide_height=Inches(7.5)
SW,SH=prs.slide_width,prs.slide_height
BLANK=prs.slide_layouts[6]

def slide(): return prs.slides.add_slide(BLANK)
def rect(s,x,y,w,h,color,line=None):
    sp=s.shapes.add_shape(1,x,y,w,h); sp.fill.solid(); sp.fill.fore_color.rgb=color
    if line is None and color==LIGHT: line=LINE
    if line is None: sp.line.fill.background()
    else: sp.line.color.rgb=line; sp.line.width=Pt(0.75)
    sp.shadow.inherit=False; return sp
def oval(s,x,y,w,h,color):
    sp=s.shapes.add_shape(9,x,y,w,h); sp.fill.solid(); sp.fill.fore_color.rgb=color
    sp.line.fill.background(); sp.shadow.inherit=False; return sp
def txt(s,x,y,w,h,runs,align=PP_ALIGN.LEFT,anchor=MSO_ANCHOR.TOP,space=4):
    tb=s.shapes.add_textbox(x,y,w,h); tf=tb.text_frame; tf.word_wrap=True; tf.vertical_anchor=anchor
    for i,line in enumerate(runs):
        p=tf.paragraphs[0] if i==0 else tf.add_paragraph()
        p.alignment=align; p.space_after=Pt(space)
        for t,sz,col,bold in line:
            r=p.add_run(); r.text=t; r.font.size=Pt(sz); r.font.bold=bold
            r.font.color.rgb=col
            kick=bool(bold) and sz<=14 and t.upper()==t and any(c.isalpha() for c in t)
            r.font.name=SERIF if (bold and sz>=12.5 and not kick) else SANS
            if kick: r._r.get_or_add_rPr().set("spc","150")
    return tb
def bullets(s,x,y,w,h,items,size=18,color=INK,gap=10,mcolor=BLUE):
    tb=s.shapes.add_textbox(x,y,w,h); tf=tb.text_frame; tf.word_wrap=True
    for i,it in enumerate(items):
        p=tf.paragraphs[0] if i==0 else tf.add_paragraph(); p.space_after=Pt(gap)
        lvl=it[1] if isinstance(it,tuple) else 0
        text=it[0] if isinstance(it,tuple) else it
        r=p.add_run(); r.text=("•  " if lvl==0 else "–  ")+text
        r.font.size=Pt(size if lvl==0 else size-2); r.font.color.rgb=color if lvl==0 else GREY
        r.font.name=SANS; r.font.bold=(lvl==0 and isinstance(it,tuple) and len(it)>2 and it[2])
    return tb

# ---------------- v2 helpers: transitions, connectors, shapes ----------------
def _transition(s, kind="fade", speed="med"):
    sld=s._element
    for old in sld.findall(qn("p:transition")): sld.remove(old)
    tr=etree.Element(qn("p:transition")); tr.set("spd",speed); tr.set("advClick","1")
    if kind=="fade": etree.SubElement(tr,qn("p:fade"))
    elif kind=="push":
        el=etree.SubElement(tr,qn("p:push")); el.set("dir","l")
    # Schema order is cSld, clrMapOvr, transition, timing, extLst. A transition written AFTER
    # p:timing makes PowerPoint drop the timing, so embedded videos show only their poster.
    anchor=sld.find(qn("p:timing"))
    if anchor is None: anchor=sld.find(qn("p:extLst"))
    if anchor is not None: anchor.addprevious(tr)
    else: sld.append(tr)
    return tr

_TIMING = """<p:timing xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main"
 xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main">
<p:tnLst><p:par><p:cTn id="1" dur="indefinite" restart="never" nodeType="tmRoot">
<p:childTnLst><p:seq concurrent="1" nextAc="seek"><p:cTn id="2" dur="indefinite" nodeType="mainSeq">
<p:childTnLst>{pars}</p:childTnLst></p:cTn>
<p:prevCondLst><p:cond evt="onPrev" delay="0"><p:tgtEl><p:sldTgt/></p:tgtEl></p:cond></p:prevCondLst>
<p:nextCondLst><p:cond evt="onNext" delay="0"><p:tgtEl><p:sldTgt/></p:tgtEl></p:cond></p:nextCondLst>
</p:seq></p:childTnLst></p:cTn></p:par></p:tnLst></p:timing>"""
_PAR = """<p:par><p:cTn id="{i0}" fill="hold"><p:stCondLst><p:cond delay="indefinite"/></p:stCondLst>
<p:childTnLst><p:par><p:cTn id="{i1}" fill="hold"><p:stCondLst><p:cond delay="0"/></p:stCondLst>
<p:childTnLst><p:par><p:cTn id="{i2}" presetID="1" presetClass="entr" presetSubtype="0" fill="hold" nodeType="{nt}">
<p:stCondLst><p:cond delay="0"/></p:stCondLst><p:childTnLst>
<p:set><p:cBhvr><p:cTn id="{i3}" dur="1" fill="hold"><p:stCondLst><p:cond delay="0"/></p:stCondLst></p:cTn>
<p:tgtEl><p:spTgt spid="{spid}"/></p:tgtEl><p:attrNameLst><p:attrName>style.visibility</p:attrName></p:attrNameLst>
</p:cBhvr><p:to><p:strVal val="visible"/></p:to></p:set>
<p:animEffect transition="in" filter="fade"><p:cBhvr><p:cTn id="{i4}" dur="400"/>
<p:tgtEl><p:spTgt spid="{spid}"/></p:tgtEl></p:cBhvr></p:animEffect>
</p:childTnLst></p:cTn></p:par></p:childTnLst></p:cTn></p:par></p:childTnLst></p:cTn></p:par>"""
def _build_on_click(s,spids):
    if not spids: return
    pars,nid=[],10
    for k,spid in enumerate(spids):
        pars.append(_PAR.format(i0=nid,i1=nid+1,i2=nid+2,i3=nid+3,i4=nid+4,
                                spid=spid,nt="clickEffect" if k==0 else "afterEffect"))
        nid+=10
    sld=s._element
    for old in sld.findall(qn("p:timing")): sld.remove(old)
    sld.append(etree.fromstring(_TIMING.format(pars="".join(pars))))

def connector(s,x1,y1,x2,y2,color,width=Pt(2.0),arrow=True):
    cn=s.shapes.add_connector(MSO_CONNECTOR.STRAIGHT,x1,y1,x2,y2)
    cn.line.color.rgb=color; cn.line.width=width
    ln=cn.line._get_or_add_ln()
    if arrow:
        tail=etree.SubElement(ln,qn("a:tailEnd"))
        tail.set("type","triangle"); tail.set("w","med"); tail.set("len","med")
    return cn
def roundrect(s,x,y,w,h,color,line=None,adj=0.10):
    sp=s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE,x,y,w,h)
    sp.fill.solid(); sp.fill.fore_color.rgb=color
    if line is None: sp.line.fill.background()
    else: sp.line.color.rgb=line; sp.line.width=Pt(1.25)
    sp.shadow.inherit=False
    try: sp.adjustments[0]=adj
    except Exception: pass
    return sp
def chevron(s,x,y,w,h,color):
    sp=s.shapes.add_shape(MSO_SHAPE.CHEVRON,x,y,w,h)
    sp.fill.solid(); sp.fill.fore_color.rgb=color
    sp.line.fill.background(); sp.shadow.inherit=False; return sp
def label_in(sp,text,size,color,bold=True):
    tf=sp.text_frame; tf.word_wrap=True; tf.vertical_anchor=MSO_ANCHOR.MIDDLE
    p=tf.paragraphs[0]; p.alignment=PP_ALIGN.CENTER
    r=p.add_run(); r.text=text; r.font.size=Pt(size); r.font.bold=bold
    r.font.color.rgb=color; r.font.name=SERIF if bold else SANS
    return sp

def _ellipsis(text,limit):
    t=" ".join(str(text).split())
    if len(t)<=limit: return t
    cut=t[:limit]; sp=cut.rfind(" ")
    if sp>limit*0.55: cut=cut[:sp]
    return cut.rstrip(" ,.;:-—(")+"…"
def _fit_title(title,size=29):
    n=len(title)
    if n<=52: return size
    if n<=66: return 25
    if n<=82: return 22
    return 20

PAGE={"n":1}   # cover is slide 1, unnumbered
def footer(s,dark=False):
    PAGE["n"]+=1
    col=MUTE if dark else GREY
    txt(s,Inches(0.6),Inches(7.06),Inches(5),Inches(0.3),[[("© Tertiary Infotech Academy Pte Ltd",8,col,False)]])
    txt(s,Inches(6.5),Inches(7.06),Inches(5.6),Inches(0.3),[[(f"{C.SHORT_TITLE}  ·  {C.COURSE_CODE}",8,col,False)]],align=PP_ALIGN.RIGHT)
    txt(s,Inches(12.2),Inches(7.06),Inches(0.6),Inches(0.3),[[(str(PAGE["n"]),8,col,False)]],align=PP_ALIGN.RIGHT)
def head(s,title,kicker=None,kcolor=BLUE):
    rect(s,0,0,SW,SH,WHITE)
    if kicker: txt(s,Inches(0.6),Inches(0.38),Inches(11.6),Inches(0.32),[[(kicker.upper(),12,CORAL,True)]])
    txt(s,Inches(0.6),Inches(0.7),Inches(12.1),Inches(0.85),
        [[(title,_fit_title(title,30),INK,True)]],anchor=MSO_ANCHOR.MIDDLE)
    return s
def dark_bg(s):
    rect(s,0,0,SW,SH,DARKBG)
    for (x,y,d,c) in [(10.2,-1.6,4.4,BROWN),(11.3,5.2,3.2,INK2),(-1.2,5.9,2.6,INK2)]:
        oval(s,Inches(x),Inches(y),Inches(d),Inches(d),c)
def _logo(name):
    p=os.path.join(ASSETS,name)
    return p if os.path.exists(p) else None

# ---------------- slide templates ----------------
def cover():
    s=slide(); dark_bg(s)
    txt(s,Inches(0.6),Inches(0.55),Inches(8),Inches(0.35),[[(f"WSQ COURSE CODE: {C.COURSE_CODE}",12,CORAL,True)]])
    txt(s,Inches(8.2),Inches(0.55),Inches(4.6),Inches(0.35),[[(f"Version {C.VERSION}  ·  {C.VERSION_DATE}",11,PALE,False)]],align=PP_ALIGN.RIGHT)
    txt(s,Inches(0.6),Inches(1.75),Inches(9.6),Inches(2.3),[[(C.TITLE,40,WHITE,True)]],anchor=MSO_ANCHOR.BOTTOM)
    rect(s,Inches(0.62),Inches(4.2),Inches(1.6),Inches(0.05),CORAL)
    txt(s,Inches(0.6),Inches(4.4),Inches(9.4),Inches(0.8),
        [[("Story first, shot in Higgsfield, finished in CapCut: hooks · storyboards · cinematic shots · the edit",15,PALE,False)]])
    txt(s,Inches(0.6),Inches(5.45),Inches(7),Inches(0.8),
        [[("Tertiary Infotech Academy Pte Ltd",13,WHITE,True)],[("UEN 201200696W",10,PALE,False)]],space=2)
    txt(s,Inches(0.6),Inches(6.75),Inches(10),Inches(0.3),
        [[("© 2026 Tertiary Infotech Academy Pte Ltd. All rights reserved.   |   www.tertiarycourses.com.sg   |   enquiry@tertiaryinfotech.com   |   +65 6100 0613",9,MUTE,False)]])
    rect(s,Inches(9.45),Inches(5.25),Inches(3.3),Inches(1.25),WHITE)
    org=_logo("tertiary-infotech-logo.png"); wsq=_logo("wsq-logo.png")
    if org: s.shapes.add_picture(org,Inches(9.65),Inches(5.42),height=Inches(0.9))
    if wsq: s.shapes.add_picture(wsq,Inches(10.75),Inches(5.47),height=Inches(0.8))

def section(kicker,title,n,sub="",items=None):
    s=slide(); dark_bg(s)
    txt(s,Inches(0.9),Inches(2.55),Inches(7.5),Inches(0.35),[[(kicker.upper(),12,CORAL,True)]])
    txt(s,Inches(0.9),Inches(2.95),Inches(7.4),Inches(1.8),[[(title,_fit_title(title,34),WHITE,True)]])
    if sub: txt(s,Inches(0.92),Inches(4.75),Inches(7.2),Inches(0.9),[[(sub,14,PALE,False)]])
    if items:
        y=Inches(3.15)
        for i,it in enumerate(items[:5],1):
            txt(s,Inches(8.75),y,Inches(0.4),Inches(0.4),[[(str(i),14,CORAL,True)]])
            txt(s,Inches(9.2),y,Inches(3.6),Inches(0.5),[[(it,11.5,PALE,False)]])
            y=int(y+Inches(0.55))
    footer(s,dark=True); return s
def content(title,items,kicker=None,size=20):
    s=head(slide(),title,kicker); bullets(s,Inches(0.85),Inches(1.95),Inches(11.6),Inches(4.9),items,size=size); footer(s); return s
def two_col(title,left,right,kicker=None,lhead="",rhead="",size=16):
    s=head(slide(),title,kicker)
    rect(s,Inches(0.85),Inches(1.95),Inches(5.7),Inches(4.7),LIGHT); rect(s,Inches(6.95),Inches(1.95),Inches(5.55),Inches(4.7),LIGHT)
    if lhead: txt(s,Inches(1.1),Inches(2.15),Inches(5.2),Inches(0.4),[[(lhead,16,BLUE,True)]])
    if rhead: txt(s,Inches(7.2),Inches(2.15),Inches(5.0),Inches(0.4),[[(rhead,16,TEAL,True)]])
    bullets(s,Inches(1.1),Inches(2.7),Inches(5.2),Inches(3.8),left,size=size)
    bullets(s,Inches(7.2),Inches(2.7),Inches(5.05),Inches(3.8),right,size=size,mcolor=TEAL); footer(s); return s
def cards3(title,cards,kicker):
    s=head(slide(),title,kicker); xs=[Inches(0.85),Inches(5.0),Inches(9.15)]
    for i,c in enumerate(cards[:3]):
        x=xs[i]; col=c[0]
        rect(s,x,Inches(1.95),Inches(3.65),Inches(4.7),LIGHT); rect(s,x,Inches(1.95),Inches(3.65),Inches(0.12),col)
        txt(s,x+Inches(0.25),Inches(2.2),Inches(3.2),Inches(0.6),[[(c[1],19,col,True)]])
        bullets(s,x+Inches(0.25),Inches(2.95),Inches(3.2),Inches(3.4),c[2],size=14,mcolor=col,gap=9)
    footer(s); return s
GEN=os.path.join(ASSETS,"gen")
def big_statement(line1,line2,kicker,color=BLUE,img=None,note=None):
    """Dark statement slide; with img (assets/gen/<name>.jpg) the text takes the left half and the image the right."""
    s=slide(); dark_bg(s)
    tw=5.9 if img else 9.6
    txt(s,Inches(0.9),Inches(2.1),Inches(tw),Inches(0.4),[[(kicker.upper(),12,CORAL,True)]])
    txt(s,Inches(0.9),Inches(2.6),Inches(tw),Inches(2.3),[[(line1,34 if img else 38,WHITE,True)]])
    rect(s,Inches(0.92),Inches(4.95),Inches(1.6),Inches(0.05),CORAL)
    if line2: txt(s,Inches(0.9),Inches(5.15),Inches(tw),Inches(1.6),[[(line2,14 if img else 16,PALE,False)]])
    if img:
        p=os.path.join(GEN,img)
        if os.path.exists(p): fit_pic(s,p,Inches(7.15),Inches(1.35),Inches(5.7),Inches(4.9),frame=False)
    if note: s.notes_slide.notes_text_frame.text=note
    footer(s,dark=True); return s

PALETTE=[BLUE,TEAL,VIOLET,AMBER]
# Punch lines (owner request, 23 Nov 2026): a one-line pitch under the title of tile, table and process slides.
PUNCH={
 "AI tools that fix and finish the footage":"Reshoots used to cost a day. Now they cost a sentence.",
 "Free AI subscriptions for video creation":"Six months of premium AI, free: pick the one that makes videos.",
 "Four ingredients of an engaging video":"Same footage, same product. The difference was decided before anyone pressed Generate.",
 "Video A vs Video B, second by second":"Video B cost nothing extra. It just had a story.",
 "Six hooks that stop the scroll":"You have three seconds. Spend them on curiosity, not a logo.",
 "One video, one message":"If you say three things, they remember none.",
 "Characters people follow":"Nobody watches a bottle for 20 seconds. Everybody watches a person with a problem.",
 "A 15-second story in five beats":"Hook, problem, turn, payoff, call to action. Three seconds each. Done.",
 "Show it, don't say it: six ways video carries a message":"The ice on the bottle says 'cold' before any caption can.",
 "A storyboard is your video before it costs a credit":"Fixing a panel costs a pencil. Fixing a take costs 240 credits.",
 "Edit the script before you shoot it (A1)":"The AI writes the first draft. The edits you make are the evidence.",
 "Six defects to plan out at the storyboard stage (K1)":"Every defect you plan out now is a reshoot you never pay for.",
 "House rules: one platform, one spec":"Decide the rules before the shoot, not in the panic before posting.",
 "Shot sizes: decide what the viewer must read":"Wide says where. Close says how it feels.",
 "Camera angles change how we feel about the character":"Move the camera ten degrees and the hero becomes the victim.",
 "Camera movement: motion with a meaning":"If the camera moves, it should mean something.",
 "Cinematic effects that lift AI footage":"Effects are seasoning. One or two per film, never the meal.",
 "Storyboard panel → prompt line":"Your storyboard is already your prompt: one row, one shot line.",
 "Review the take for story and emotion (A4)":"'Make it better' is not a note. 'Shot 3: hold the smile' is.",
 "Quality issues → the Higgsfield fix":"Know the defect, know the fix: that is half the Written Assessment.",
 "Parameters to assess the footage (K3, A5)":"Score it before you edit it. Bad footage stays bad on a nice timeline.",
 "Post-production in CapCut: five passes":"Structure first, polish last. Never caption a shot you might cut.",
 "The cutting order when a video runs long":"Kill the logo intro first. Nobody has ever missed it.",
 "Editing rules that keep viewers watching":"Good cuts are invisible. Bad cuts are all anyone remembers.",
 "Polish in CapCut: what each tab is for":"Most viewers start muted: your captions are your soundtrack.",
 "What captions, music and voice add to the cut":"Music under the ice clink, never over it.",
 "Remedial actions: fix it in CapCut, or reshoot one shot":"A trim is free. A reshoot is 240 credits. Try the trim first.",
 "Export to the industry standard (K4)":"A great video in the wrong ratio is a cropped video.",
 "Industry standards and responsible AI (K4)":"Compliance is not paperwork. It is how your video stays online.",
 "Evaluate a new AI technology (A7, K5)":"A new tool earns its place by saving time or raising quality. Ideally both.",
 "Copyright and IP: four questions before you publish":"You can generate anything. You can't publish everything.",
 "Core ethical issues in GenAI video":"Every one of these has already cost someone a lawsuit, a job or their trust.",
 "Seven issues, seven rules for your own videos":"Seven rules. Check them before you press Post.",
 "What You Achieved":"Two days ago you had an idea. Now you have a published-ready video.",
 "The Pipeline You Now Own":"Story first, shoot second, edit last. That order works on any tool.",
}
def tile_grid(title,items,kicker=None,cols=2,size=15,icons=None,accent=BLUE,note=None):
    pl=PUNCH.get(title)
    s=head_sub(slide(),title,kicker,pl,accent) if pl else head(slide(),title,kicker,kcolor=accent)
    n=len(items); rows=math.ceil(n/cols)
    X0=Inches(0.85); Y0=Inches(2.35 if pl else 1.95); TOTW=Inches(11.63); AREAH=Inches(4.38 if pl else 4.78)
    gx=Inches(0.3); gy=Inches(0.26)
    cw=int((TOTW-gx*(cols-1))/cols); ch=int((AREAH-gy*(rows-1))/rows)
    bd=Inches(0.6)
    for i,it in enumerate(items):
        r=i//cols; c=i%cols
        x=int(X0+(cw+gx)*c); y=int(Y0+(ch+gy)*r); col=PALETTE[i%len(PALETTE)]
        rect(s,x,y,cw,ch,LIGHT); rect(s,x,y,Inches(0.1),ch,col)
        oval(s,x+Inches(0.28),int(y+ch/2-bd/2),bd,bd,col)
        ic=icons[i] if icons else str(i+1)
        txt(s,x+Inches(0.28),int(y+ch/2-bd/2),bd,bd,[[(ic,19,WHITE,True)]],align=PP_ALIGN.CENTER,anchor=MSO_ANCHOR.MIDDLE)
        tx=x+Inches(1.08); tw=cw-Inches(1.32)
        if isinstance(it,tuple):
            txt(s,tx,int(y+Inches(0.14)),tw,int(ch-Inches(0.2)),
                [[(it[0],size+2,INK,True)],[(it[1],size-2,GREY,False)]],anchor=MSO_ANCHOR.MIDDLE,space=3)
        else:
            txt(s,tx,int(y+Inches(0.1)),tw,int(ch-Inches(0.16)),[[(it,size,INK,False)]],anchor=MSO_ANCHOR.MIDDLE)
    if note: s.notes_slide.notes_text_frame.text=note
    footer(s); return s

def flow_h(title,steps,kicker=None,color=BLUE):
    s=head(slide(),title,kicker,kcolor=color)
    n=len(steps); X0=Inches(0.85); TOTW=Inches(11.63); gap=Inches(0.34)
    cw=int((TOTW-gap*(n-1))/n); y=Inches(2.55); ch=Inches(3.15); bd=Inches(0.82)
    for i,st in enumerate(steps):
        x=int(X0+(cw+gap)*i)
        rect(s,x,y,cw,ch,LIGHT); rect(s,x,y,cw,Inches(0.1),color)
        oval(s,int(x+cw/2-bd/2),int(y+Inches(0.42)),bd,bd,color)
        txt(s,int(x+cw/2-bd/2),int(y+Inches(0.42)),bd,bd,[[(str(i+1),30,WHITE,True)]],align=PP_ALIGN.CENTER,anchor=MSO_ANCHOR.MIDDLE)
        txt(s,x+Inches(0.16),int(y+Inches(1.55)),cw-Inches(0.32),int(ch-Inches(1.7)),[[(st,14,INK,False)]],align=PP_ALIGN.CENTER)
        if i<n-1:
            cy=int(y+Inches(1.6))
            connector(s,int(x+cw+Inches(0.03)),cy,int(x+cw+gap-Inches(0.03)),cy,color)
    footer(s); return s

def process_map(title,stages,kicker=None,color=BLUE,synthesis=None,animate=True):
    """Real rounded-rect stages joined by real connectors with arrowheads."""
    pl=PUNCH.get(title)
    s=head_sub(slide(),title,kicker,pl,color) if pl else head(slide(),title,kicker,kcolor=color)
    n=len(stages); X0=Inches(0.85); TOTW=Inches(11.63)
    gap=Inches(0.42); cw=int((TOTW-gap*(n-1))/n)
    y=Inches(2.35); ch=Inches(2.35) if synthesis else Inches(3.0)
    spids=[]
    for i,st in enumerate(stages):
        lbl,detail=(st if isinstance(st,tuple) else (st,""))
        x=int(X0+(cw+gap)*i)
        box=roundrect(s,x,y,cw,ch,LIGHT,line=LINE)
        rect(s,x,y,cw,Inches(0.11),color)
        bd=Inches(0.62)
        oval(s,int(x+cw/2-bd/2),int(y+Inches(0.34)),bd,bd,color)
        txt(s,int(x+cw/2-bd/2),int(y+Inches(0.34)),bd,bd,[[(str(i+1),24,WHITE,True)]],
            align=PP_ALIGN.CENTER,anchor=MSO_ANCHOR.MIDDLE)
        lbl=_ellipsis(lbl,44)
        lsz=13 if len(lbl)<=28 else (12 if len(lbl)<=38 else 11)
        txt(s,x+Inches(0.14),int(y+Inches(1.06)),cw-Inches(0.28),Inches(0.94),
            [[(lbl,lsz,INK,True)]],align=PP_ALIGN.CENTER,anchor=MSO_ANCHOR.MIDDLE,space=0)
        if detail:
            det=_ellipsis(detail,34)
            txt(s,x+Inches(0.1),int(y+ch-Inches(0.52)),cw-Inches(0.2),Inches(0.38),
                [[(det,9,GREY,False)]],align=PP_ALIGN.CENTER,anchor=MSO_ANCHOR.MIDDLE,space=0)
        spids.append(box.shape_id)
        if i<n-1:
            cy=int(y+ch/2)
            cn=connector(s,int(x+cw+Inches(0.06)),cy,int(x+cw+gap-Inches(0.06)),cy,color)
            spids.append(cn.shape_id)
    if synthesis:
        by=int(y+ch+Inches(0.34))
        rect(s,Inches(0.85),by,Inches(11.63),Inches(1.15),LIGHT)
        rect(s,Inches(0.85),by,Inches(0.11),Inches(1.15),color)
        txt(s,Inches(1.15),int(by+Inches(0.12)),Inches(11.1),Inches(0.32),
            [[(synthesis[0].upper(),11,color,True)]])
        txt(s,Inches(1.15),int(by+Inches(0.46)),Inches(11.1),Inches(0.62),
            [[(synthesis[1],13,INK,False)]])
    if animate: _build_on_click(s,spids)
    footer(s); return s

def compare_table(title,headers,rows,kicker=None,accent=BLUE,note=None):
    pl=PUNCH.get(title)
    s=head_sub(slide(),title,kicker,pl,accent) if pl else head(slide(),title,kicker,kcolor=accent)
    X0=Inches(0.85); TOTW=Inches(11.63); ncol=len(headers)
    first=int(TOTW*0.26); rest=int((TOTW-first)/(ncol-1))
    widths=[first]+[rest]*(ncol-1)
    y=Inches(2.3 if pl else 1.95); hh=Inches(0.52)
    x=X0
    for i,h in enumerate(headers):
        rect(s,x,y,widths[i],hh,INK)
        txt(s,x+Inches(0.14),y,widths[i]-Inches(0.28),hh,[[(h,13,WHITE,True)]],anchor=MSO_ANCHOR.MIDDLE)
        x+=widths[i]
    ry=int(y+hh)
    BOTTOM=Inches(6.88)-(Inches(1.24) if note else Emu(0))
    avail=BOTTOM-ry
    rh=int(min(Inches(0.78),avail/max(len(rows),1)))
    for r,row in enumerate(rows):
        x=X0
        for i,cell in enumerate(row):
            fill=LIGHT if r%2==0 else WHITE
            rect(s,x,ry,widths[i],rh,fill,line=LINE)
            bold=(i==0)
            txt(s,x+Inches(0.14),ry,widths[i]-Inches(0.28),rh,
                [[(cell,11.5,INK if bold else GREY,bold)]],anchor=MSO_ANCHOR.MIDDLE)
            x+=widths[i]
        ry+=rh
    if note:
        rect(s,X0,int(ry+Inches(0.22)),TOTW,Inches(0.92),LIGHT)
        rect(s,X0,int(ry+Inches(0.22)),Inches(0.11),Inches(0.92),accent)
        txt(s,X0+Inches(0.3),int(ry+Inches(0.34)),TOTW-Inches(0.6),Inches(0.66),
            [[("TIP:  ",11,CORAL,True),(note,12,INK,False)]])
    footer(s); return s

def trainer_slide(kicker,name,role,rows,initials,accent=BLUE):
    s=head(slide(),"About the Trainer",kicker,kcolor=accent)
    lx=Inches(0.85); lw=Inches(3.65)
    rect(s,lx,Inches(1.95),lw,Inches(4.7),LIGHT); rect(s,lx,Inches(1.95),lw,Inches(0.12),accent)
    bd=Inches(1.7); ax=int(lx+(lw-bd)/2)
    oval(s,ax,Inches(2.5),bd,bd,accent)
    txt(s,ax,Inches(2.5),bd,bd,[[(initials,44,WHITE,True)]],align=PP_ALIGN.CENTER,anchor=MSO_ANCHOR.MIDDLE)
    txt(s,lx+Inches(0.15),Inches(4.55),lw-Inches(0.3),Inches(0.6),[[(name,21,INK,True)]],align=PP_ALIGN.CENTER)
    txt(s,lx+Inches(0.15),Inches(5.2),lw-Inches(0.3),Inches(1.2),[[(role,13,GREY,False)]],align=PP_ALIGN.CENTER)
    rx=Inches(4.9); rw=Inches(7.6); ry=Inches(1.95); rh=Inches(4.7)
    n=len(rows); gy=Inches(0.2); th=int((rh-gy*(n-1))/n)
    for i,(label,val) in enumerate(rows):
        y=int(ry+(th+gy)*i); col=PALETTE[i%len(PALETTE)]
        rect(s,rx,y,rw,th,LIGHT); rect(s,rx,y,Inches(0.1),th,col)
        vruns=[(val,14,INK,False)] if val else [("____________________________________________",13,LINE,False)]
        txt(s,rx+Inches(0.32),y,rw-Inches(0.6),th,
            [[(label.upper(),11,col,True)],vruns],anchor=MSO_ANCHOR.MIDDLE,space=3)
    footer(s); return s

def activity_overview(tag,title,desc,build,services,kicker,objective=None):
    s=head(slide(),title,kicker,kcolor=TEAL)
    rect(s,Inches(0.85),Inches(1.85),Inches(1.7),Inches(0.5),TEAL)
    txt(s,Inches(0.85),Inches(1.9),Inches(1.7),Inches(0.4),[[(tag,16,WHITE,True)]],align=PP_ALIGN.CENTER)
    if objective:
        txt(s,Inches(2.75),Inches(1.9),Inches(9.7),Inches(0.42),[[("MAPS TO  ",11,GREY,True),(objective,12,GREY,False)]])
    txt(s,Inches(0.85),Inches(2.55),Inches(11.7),Inches(1.6),[[(desc,19,INK,False)]])
    rect(s,Inches(0.85),Inches(4.35),Inches(11.7),Inches(2.0),LIGHT)
    txt(s,Inches(1.1),Inches(4.55),Inches(11),Inches(0.4),[[("You'll build",14,BLUE,True)]])
    txt(s,Inches(1.1),Inches(4.95),Inches(11),Inches(0.9),[[(build,17,INK,True)]])
    txt(s,Inches(1.1),Inches(5.85),Inches(11.2),Inches(0.45),[[("Tools:  ",13,GREY,True),(services,13,GREY,False)]]); footer(s); return s

def prompt_slide(act_title,items,kicker,part=None):
    """Prompt cards: the example GenAI prompts for a lab, each as a labelled dark
    panel the learner can copy. items: list of (label, prompt_text)."""
    s=head(slide(),act_title+(f" — Prompts {part}" if part else " — Prompts"),kicker,kcolor=VIOLET)
    y=Inches(1.92); X0=Inches(0.85); TOTW=Inches(11.63)
    AVAIL=4.92; gap=0.22
    def need(text,fs):   # panel height (in) for text at font size fs, wrapping estimated
        cpl=max(20,int(11.0*72/(fs*0.53)))
        n=sum(max(1,math.ceil(len(ln)/cpl)) for ln in text.split("\n"))
        return 0.4+0.32+n*fs*1.32/72
    FS=9
    for f in (15,14,13,12,11,10,9):
        if sum(need(t,f) for _,t in items)+gap*(len(items)-1)<=AVAIL: FS=f; break
    for i,(label,text) in enumerate(items):
        ph=Inches(min(AVAIL,need(text,FS)+0.1))
        rect(s,X0,int(y),TOTW,Inches(0.4),LIGHT)
        rect(s,X0,int(y),Inches(0.1),Inches(0.4),VIOLET)
        txt(s,X0+Inches(0.28),int(y+Inches(0.03)),TOTW-Inches(0.5),Inches(0.34),
            [[("PROMPT — "+label.upper(),11.5,VIOLET,True)]])
        bh=ph-Inches(0.4)
        rect(s,X0,int(y+Inches(0.4)),TOTW,int(bh),DARKBG)
        lines=text.split("\n")
        runs=[[(ln,FS,CODEBLUE,False)] for ln in lines]
        txt(s,X0+Inches(0.28),int(y+Inches(0.48)),TOTW-Inches(0.56),int(bh-Inches(0.16)),
            runs,space=2,anchor=MSO_ANCHOR.MIDDLE)
        y=int(y+ph+Inches(gap))
    footer(s); return s

def test_slide(act_title,text,kicker):
    s=head(slide(),act_title,kicker,TEAL)
    rect(s,Inches(0.85),Inches(2.3),Inches(11.7),Inches(2.6),LIGHT); rect(s,Inches(0.85),Inches(2.3),Inches(0.1),Inches(2.6),TEAL)
    txt(s,Inches(1.2),Inches(2.6),Inches(11),Inches(0.5),[[("✓  Check your work",20,TEAL,True)]])
    txt(s,Inches(1.2),Inches(3.3),Inches(11),Inches(1.4),[[(text,17,INK,False)]])
    txt(s,Inches(0.85),Inches(5.2),Inches(11.7),Inches(0.6),
        [[("Detailed step-by-step instructions: Learner Guide + the lab folder in labs/.",13,GREY,False)]])
    footer(s); return s

def screenshot_slide(title,img,steps,kicker,url):
    """Visual how-to: real screenshot left, numbered chips right."""
    s=head(slide(),title,kicker,kcolor=BLUE)
    if img and os.path.exists(img):
        pic=s.shapes.add_picture(img,Inches(0.85),Inches(2.1),width=Inches(6.7))
        if pic.height>Inches(4.5):
            pic.height=Inches(4.5); pic.width=int(4.5/ (pic.image.size[1]/pic.image.size[0]) *914400)
        rect(s,Inches(0.85),Inches(2.1),pic.width,Emu(int(Pt(2))),BLUE)
    txt(s,Inches(0.85),Inches(6.62),Inches(6.7),Inches(0.35),[[(url,12,BLUE,True)]])
    rx=Inches(8.0); rw=Inches(4.5); ry=Inches(2.1); n=len(steps); gy=Inches(0.18)
    th=int((Inches(4.5)-gy*(n-1))/n)
    for i,st in enumerate(steps):
        y=int(ry+(th+gy)*i); col=PALETTE[i%len(PALETTE)]
        rect(s,rx,y,rw,th,LIGHT); rect(s,rx,y,Inches(0.09),th,col)
        bd=Inches(0.42)
        oval(s,rx+Inches(0.2),int(y+th/2-bd/2),bd,bd,col)
        txt(s,rx+Inches(0.2),int(y+th/2-bd/2),bd,bd,[[(str(i+1),14,WHITE,True)]],align=PP_ALIGN.CENTER,anchor=MSO_ANCHOR.MIDDLE)
        txt(s,rx+Inches(0.78),y,rw-Inches(0.95),th,[[(st,12.5,INK,False)]],anchor=MSO_ANCHOR.MIDDLE)
    footer(s); return s

# ================= v8 visual layouts: screenshots, video, YouTube, big numbers =================
from pptx_online_video import add_online_video, set_video_timing
from PIL import Image as _PIL
HF=os.path.join(ASSETS,"hf"); YT=os.path.join(ASSETS,"yt")
VID=os.path.join(REPO,"courseware","assets","videos")
def hf(n): return os.path.join(HF,f"hf_{n}.jpg")

ENABLE_NOTE=("To play: in PowerPoint click Enable Content on the yellow security bar first (online video is blocked until you do), "
             "be online, then in Slide Show click the video. If it still will not play, use the Open in YouTube link.")

_ENABLED_ONCE=[False]
def _enable_once(note):
    """Enable Content reminder in the trainer notes of the FIRST YouTube slide only (owner: not on every slide)."""
    if _ENABLED_ONCE[0]: return note
    _ENABLED_ONCE[0]=True
    return ENABLE_NOTE+(" "+note if note else "")

def notes(s,text):
    if text: s.notes_slide.notes_text_frame.text=text

def head_sub(s,title,kicker,sub,kcolor=BLUE):
    """Header with a one-line pitch under the title (y≈1.8in). Content starts at 2.35in."""
    head(s,title,kicker,kcolor)
    if sub: txt(s,Inches(0.6),Inches(1.62),Inches(12.0),Inches(0.5),[[(sub,15,GREY,False)]])
    return s

def fit_pic(s,img,x,y,w,h,frame=True,align="center"):
    """Place img inside the box (x,y,w,h EMU) keeping aspect; returns (px,py,pw,ph)."""
    iw,ih=_PIL.open(img).size
    sc=min(w/iw,h/ih); pw,ph=int(iw*sc),int(ih*sc)
    px=int(x+(w-pw)/2) if align=="center" else int(x); py=int(y+(h-ph)/2)
    if frame:
        pad=Inches(0.06)
        bg=rect(s,px-pad,py-pad,pw+2*pad,ph+2*pad,WHITE,line=LINE)
    s.shapes.add_picture(img,px,py,pw,ph)
    return px,py,pw,ph

def mark(s,px,py,pw,ph,fx,fy,n,col):
    """Numbered marker on a screenshot at fractional position (fx,fy)."""
    d=Inches(0.42); x=int(px+pw*fx-d/2); y=int(py+ph*fy-d/2)
    o=oval(s,x,y,d,d,col); o.line.color.rgb=WHITE; o.line.width=Pt(2)
    txt(s,x,y,d,d,[[(str(n),13,WHITE,True)]],align=PP_ALIGN.CENTER,anchor=MSO_ANCHOR.MIDDLE)

def shot_steps(title,img,steps,kicker,sub=None,marks=None,url=None,note=None,accent=BLUE,img_w=7.35):
    """Screenshot left (with optional numbered markers), numbered explanation chips right.
    steps: list of (label, text) or text."""
    s=head_sub(slide(),title,kicker,sub,accent)
    iw,ih=_PIL.open(img).size
    if iw/ih>1.9 and not url:
        # wide screenshot: full width on top, numbered chips in a row underneath
        px,py,pw,ph=fit_pic(s,img,Inches(0.85),Inches(2.35),Inches(11.63),Inches(3.05))
        n=len(steps); gx=Inches(0.18); cw=int((Inches(11.63)-gx*(n-1))/n)
        y=Inches(5.62); h=Inches(1.23)
        for i,st in enumerate(steps):
            x=int(Inches(0.85)+(cw+gx)*i); col=PALETTE[i%len(PALETTE)]
            rect(s,x,y,cw,h,LIGHT); rect(s,x,y,cw,Inches(0.07),col)
            d=Inches(0.36); oval(s,x+Inches(0.12),y+Inches(0.18),d,d,col)
            txt(s,x+Inches(0.12),y+Inches(0.18),d,d,[[(str(i+1),12,WHITE,True)]],align=PP_ALIGN.CENTER,anchor=MSO_ANCHOR.MIDDLE)
            lab,t=(st if isinstance(st,tuple) else (st,""))
            txt(s,x+Inches(0.56),y+Inches(0.12),cw-Inches(0.66),Inches(0.5),[[(lab,12.5,INK,True)]],anchor=MSO_ANCHOR.MIDDLE)
            if t: txt(s,x+Inches(0.14),y+Inches(0.6),cw-Inches(0.26),h-Inches(0.64),[[(t,10.5,GREY,False)]])
            if marks and i<len(marks) and marks[i]: mark(s,px,py,pw,ph,marks[i][0],marks[i][1],i+1,col)
        notes(s,note); footer(s); return s
    bx,by,bw,bh=Inches(0.85),Inches(2.35),Inches(img_w),Inches(4.45 if not url else 4.1)
    px,py,pw,ph=fit_pic(s,img,bx,by,bw,bh)
    rx=int(bx+bw+Inches(0.3)); rw=int(Inches(12.48)-rx); n=len(steps); gy=Inches(0.14)
    th=int((Inches(4.45)-gy*(n-1))/n)
    for i,st in enumerate(steps):
        y=int(by+(th+gy)*i); col=PALETTE[i%len(PALETTE)]
        rect(s,rx,y,rw,th,LIGHT); rect(s,rx,y,Inches(0.08),th,col)
        d=Inches(0.4); oval(s,rx+Inches(0.18),int(y+th/2-d/2),d,d,col)
        txt(s,rx+Inches(0.18),int(y+th/2-d/2),d,d,[[(str(i+1),13,WHITE,True)]],align=PP_ALIGN.CENTER,anchor=MSO_ANCHOR.MIDDLE)
        if isinstance(st,tuple):
            runs=[[(st[0],13,INK,True)],[(st[1],11.5,GREY,False)]]
        else:
            runs=[[(st,12,INK,False)]]
        txt(s,rx+Inches(0.7),y,rw-Inches(0.82),th,runs,anchor=MSO_ANCHOR.MIDDLE,space=2)
        if marks and i<len(marks) and marks[i]: mark(s,px,py,pw,ph,marks[i][0],marks[i][1],i+1,col)
    if url: txt(s,bx,Inches(6.55),bw,Inches(0.3),[[(url,12,accent,True)]])
    notes(s,note); footer(s); return s

def shot_hero(title,img,cols,kicker,sub=None,note=None,accent=BLUE,img_h=3.2):
    """Wide screenshot on top, an explanation band of 2–3 labelled columns underneath."""
    s=head_sub(slide(),title,kicker,sub,accent)
    fit_pic(s,img,Inches(0.85),Inches(2.35),Inches(11.63),Inches(img_h))
    y=Inches(2.35+img_h+0.22); h=Inches(6.85)-y; n=len(cols); gx=Inches(0.25)
    cw=int((Inches(11.63)-gx*(n-1))/n)
    for i,(lab,t) in enumerate(cols):
        x=int(Inches(0.85)+(cw+gx)*i); col=PALETTE[i%len(PALETTE)]
        rect(s,x,y,cw,h,LIGHT); rect(s,x,y,cw,Inches(0.07),col)
        txt(s,x+Inches(0.2),y+Inches(0.12),cw-Inches(0.4),h-Inches(0.16),
            [[(lab,13.5,col,True)],[(t,12,INK,False)]],anchor=MSO_ANCHOR.MIDDLE,space=3)
    notes(s,note); footer(s); return s

def shot_pair(title,left,right,kicker,sub=None,note=None,accent=BLUE,img_h=3.25):
    """Two screenshots side by side; left/right = (img, label, text)."""
    s=head_sub(slide(),title,kicker,sub,accent)
    cw=Inches(5.66)
    for i,(img,lab,t) in enumerate((left,right)):
        x=int(Inches(0.85)+(cw+Inches(0.31))*i); col=[BLUE,TEAL][i]
        fit_pic(s,img,x,Inches(2.35),cw,Inches(img_h))
        y=Inches(2.35+img_h+0.2); h=Inches(6.85)-y
        rect(s,x,y,cw,h,LIGHT); rect(s,x,y,Inches(0.08),h,col)
        txt(s,x+Inches(0.25),y,cw-Inches(0.4),h,[[(lab,14,col,True)],[(t,12,INK,False)]],anchor=MSO_ANCHOR.MIDDLE,space=3)
    notes(s,note); footer(s); return s

def shot_gallery(title,items,kicker,sub=None,band=None,note=None,accent=BLUE,img_h=3.3):
    """3–4 screenshots in a row with a label under each, optional one-line band."""
    s=head_sub(slide(),title,kicker,sub,accent)
    n=len(items); gx=Inches(0.25); cw=int((Inches(11.63)-gx*(n-1))/n)
    for i,(img,lab) in enumerate(items):
        x=int(Inches(0.85)+(cw+gx)*i); col=PALETTE[i%len(PALETTE)]
        fit_pic(s,img,x,Inches(2.35),cw,Inches(img_h))
        txt(s,x,Inches(2.35+img_h+0.12),cw,Inches(0.75),[[(lab,12.5,col,True)]],align=PP_ALIGN.CENTER)
    if band:
        y=Inches(6.05); rect(s,Inches(0.85),y,Inches(11.63),Inches(0.78),LIGHT); rect(s,Inches(0.85),y,Inches(0.1),Inches(0.78),accent)
        txt(s,Inches(1.15),y,Inches(11.2),Inches(0.78),[[(band,13,INK,False)]],anchor=MSO_ANCHOR.MIDDLE)
    notes(s,note); footer(s); return s

def big_numbers(title,nums,kicker,sub=None,band=None,note=None,accent=BLUE):
    """2–4 huge figures with a label each; nums = [(figure, label, detail)]."""
    s=head_sub(slide(),title,kicker,sub,accent)
    n=len(nums); gx=Inches(0.3); cw=int((Inches(11.63)-gx*(n-1))/n)
    for i,(fig,lab,det) in enumerate(nums):
        x=int(Inches(0.85)+(cw+gx)*i); col=PALETTE[i%len(PALETTE)]
        rect(s,x,Inches(2.45),cw,Inches(3.3),LIGHT); rect(s,x,Inches(2.45),cw,Inches(0.1),col)
        txt(s,x,Inches(2.7),cw,Inches(1.4),[[(fig,60,col,True)]],align=PP_ALIGN.CENTER,anchor=MSO_ANCHOR.MIDDLE)
        txt(s,x+Inches(0.2),Inches(4.15),cw-Inches(0.4),Inches(1.5),[[(lab,16,INK,True)],[(det,12,GREY,False)]],align=PP_ALIGN.CENTER,space=4)
    if band:
        y=Inches(5.98); rect(s,Inches(0.85),y,Inches(11.63),Inches(0.85),LIGHT); rect(s,Inches(0.85),y,Inches(0.1),Inches(0.85),accent)
        txt(s,Inches(1.15),y,Inches(11.2),Inches(0.85),[[(band,13,INK,False)]],anchor=MSO_ANCHOR.MIDDLE)
    notes(s,note); footer(s); return s

def video_slide(v,kicker,sub,note=None,prompt_hint=None):
    """Embedded MP4 (plays in PowerPoint) left, the shot list it was prompted with right."""
    s=head_sub(slide(),v["title"],kicker,sub,TEAL)
    mp4=os.path.join(VID,v["file"]); poster=os.path.join(VID,v["poster"])
    x,y,w=Inches(0.85),Inches(2.35),Inches(7.6); h=int(w*9/16)
    rect(s,x-Inches(0.06),y-Inches(0.06),w+Inches(0.12),h+Inches(0.12),INK)
    if os.path.exists(mp4):
        s.shapes.add_movie(mp4,x,y,w,h,poster_frame_image=poster,mime_type="video/mp4")
        set_video_timing(s)   # click plays / pauses, as PowerPoint writes for Insert > Video
    txt(s,x,int(y+h+Inches(0.12)),w,Inches(0.35),[[("▶ Click to play  ·  ",11,TEAL,True),(v["model"],11,GREY,False)]])
    rx=Inches(8.75); rw=Inches(3.73); n=len(v["shots"]); gy=Inches(0.12)
    txt(s,rx,y,rw,Inches(0.35),[[("THE SHOTS WE PROMPTED",11,TEAL,True)]])
    th=int((Inches(4.0)-gy*(n-1))/n); y0=int(y+Inches(0.42))
    for i,sh in enumerate(v["shots"]):
        yy=int(y0+(th+gy)*i); col=PALETTE[i%len(PALETTE)]
        rect(s,rx,yy,rw,th,LIGHT); rect(s,rx,yy,Inches(0.07),th,col)
        tm,_,act=sh.partition("  ")
        txt(s,rx+Inches(0.2),yy,rw-Inches(0.3),th,[[(tm,11.5,col,True)],[(act,11,INK,False)]],anchor=MSO_ANCHOR.MIDDLE,space=1)
    notes(s,note); footer(s); return s

def yt_pair(title,items,kicker,sub=None,note=None,accent=VIOLET):
    """Two click-to-play YouTube examples; items = [(video_id, label, fact)]."""
    note=_enable_once(note)
    s=head_sub(slide(),title,kicker,sub,accent)
    cw=5.66; h=cw*9/16
    for i,(vid,lab,fact) in enumerate(items):
        x=0.85+(cw+0.31)*i
        th=os.path.join(YT,f"{vid}.jpg")
        add_online_video(s,f"https://www.youtube.com/watch?v={vid}",x,2.35,cw,h,
                         poster=th if os.path.exists(th) else None,name=lab)
        y=2.35+h+0.42
        rect(s,Inches(x),Inches(y),Inches(cw),Inches(6.85-y),LIGHT)
        rect(s,Inches(x),Inches(y),Inches(0.08),Inches(6.85-y),PALETTE[i])
        txt(s,Inches(x+0.25),Inches(y),Inches(cw-0.4),Inches(6.85-y),[[(lab,13.5,PALETTE[i],True)],[(fact,11.5,INK,False)]],anchor=MSO_ANCHOR.MIDDLE,space=3)
    notes(s,note); footer(s); return s

def link_slide(title,url,short,lines,kicker,sub=None,note=None):
    """A sign-up link with a QR code, the disclosure and the plan terms."""
    import qrcode, io as _io
    s=head_sub(slide(),title,kicker,sub,TEAL)
    q=qrcode.make(url); buf=_io.BytesIO(); q.save(buf,format="PNG"); buf.seek(0)
    rect(s,Inches(0.85),Inches(2.35),Inches(3.6),Inches(4.45),LIGHT)
    s.shapes.add_picture(buf,Inches(1.15),Inches(2.55),Inches(3.0),Inches(3.0))
    txt(s,Inches(0.85),Inches(5.7),Inches(3.6),Inches(0.9),[[("Scan to sign up",13,TEAL,True)],[(short,11,INK,False)]],align=PP_ALIGN.CENTER,space=2)
    rx=Inches(4.75); rw=Inches(7.73); n=len(lines); gy=Inches(0.16); th=int((Inches(4.45)-gy*(n-1))/n)
    for i,(lab,t) in enumerate(lines):
        y=int(Inches(2.35)+(th+gy)*i); col=PALETTE[i%len(PALETTE)]
        rect(s,rx,y,rw,th,LIGHT); rect(s,rx,y,Inches(0.08),th,col)
        txt(s,rx+Inches(0.3),y,rw-Inches(0.5),th,[[(lab.upper(),11,col,True)],[(t,13,INK,False)]],anchor=MSO_ANCHOR.MIDDLE,space=3)
    notes(s,note); footer(s); return s

def resource_slide(title,vid,vlabel,vfact,cards,kicker,sub=None,note=None):
    """One landscape YouTube walkthrough + reference cards (docs, links)."""
    s=head_sub(slide(),title,kicker,sub,TEAL)
    w=6.2; h=w*9/16
    th=os.path.join(YT,f"{vid}.jpg")
    add_online_video(s,f"https://www.youtube.com/watch?v={vid}",0.85,2.35,w,h,poster=th if os.path.exists(th) else None,name=vlabel)
    y=2.35+h+0.42
    rect(s,Inches(0.85),Inches(y),Inches(w),Inches(6.85-y),LIGHT)
    txt(s,Inches(1.05),Inches(y),Inches(w-0.3),Inches(6.85-y),[[("WATCH BEFORE LAB 1  ·  "+vfact,9.5,TEAL,True)],[(vlabel,12,INK,True)]],anchor=MSO_ANCHOR.MIDDLE,space=1)
    cx=0.85+w+0.3; cw=12.48-cx; n=len(cards); gy=0.18; ch=(4.5-gy*(n-1))/n
    for i,(lab,t,url) in enumerate(cards):
        yy=2.35+(ch+gy)*i; col=PALETTE[i%len(PALETTE)]
        rect(s,Inches(cx),Inches(yy),Inches(cw),Inches(ch),LIGHT); rect(s,Inches(cx),Inches(yy),Inches(0.08),Inches(ch),col)
        tb=txt(s,Inches(cx+0.25),Inches(yy),Inches(cw-0.4),Inches(ch),[[(lab,13,INK,True)],[(t,11,GREY,False)],[(url,10.5,col,True)]],anchor=MSO_ANCHOR.MIDDLE,space=2)
        tb.text_frame.paragraphs[-1].runs[0].hyperlink.address=url if url.startswith("http") else "https://"+url
    notes(s,note); footer(s); return s



def _dark_head(s,kicker,title):
    txt(s,Inches(0.6),Inches(0.62),Inches(11),Inches(0.32),[[(kicker.upper(),12,CORAL,True)]])
    txt(s,Inches(0.6),Inches(0.95),Inches(12),Inches(0.85),[[(title,30,WHITE,True)]],anchor=MSO_ANCHOR.MIDDLE)

def lms_login_slide():
    """Same as the Claude Code deck: dark slide, large TMS login screenshot, one-line caption."""
    s=slide(); rect(s,0,0,SW,SH,DARKBG)
    _dark_head(s,"COURSE PORTAL","Login to LMS and Download Course Material")
    img=_logo("lms-tms-login-2026.png")
    if img: fit_pic(s,img,Inches(2.23),Inches(2.08),Inches(8.87),Inches(4.42),frame=False)
    txt(s,Inches(0.67),Inches(6.58),Inches(12),Inches(0.45),
        [[("Log in at lms-tms.tertiaryinfotech.com with your registered email and the OTP sent to your inbox, then open this course to download the slides and Learner Guide.",12,PALE,False)]],align=PP_ALIGN.CENTER)
    footer(s,dark=True); return s

def lms_courseware_slide():
    """Same as the Claude Code deck: three icon rows, a thumbnail of the TMS, and the LMS link band."""
    s=slide(); rect(s,0,0,SW,SH,DARKBG)
    oval(s,Inches(10.6),Inches(-1.4),Inches(4.6),Inches(4.6),BROWN)
    _dark_head(s,"LEARNING MANAGEMENT SYSTEM","Courseware & Assessment on the LMS")
    rows=[("icon-download.png","Download the courseware","Get the slides and Learner Guide from the LMS for the open-book assessment."),
          ("icon-assessment.png","Take the assessment","Complete the Written Assessment and Practical Performance on the LMS; upload your PP screenshots and videos there."),
          ("icon-login.png","Log in","Use your enrolled account to access the course materials and assessment.")]
    for i,(ic,h,t) in enumerate(rows):
        y=2.25+1.15*i
        oval(s,Inches(0.7),Inches(y+0.05),Inches(0.6),Inches(0.6),CORAL)
        p=_logo(ic)
        if p: s.shapes.add_picture(p,Inches(0.85),Inches(y+0.2),Inches(0.3),Inches(0.3))
        txt(s,Inches(1.5),Inches(y),Inches(6.8),Inches(0.42),[[(h,16,WHITE,True)]])
        txt(s,Inches(1.5),Inches(y+0.45),Inches(6.8),Inches(0.5),[[(t,12,PALE,False)]])
    img=_logo("lms-tms-login-2026.png")
    if img: fit_pic(s,img,Inches(8.9),Inches(2.7),Inches(3.4),Inches(1.7),frame=False)
    rect(s,Inches(0.7),Inches(5.95),Inches(11.9),Inches(0.7),INK2)
    tb=txt(s,Inches(1.0),Inches(5.95),Inches(11.3),Inches(0.7),[[("LMS:  ",14,CORAL,True),("https://lms-tms.tertiaryinfotech.com/",14,WHITE,False)]],anchor=MSO_ANCHOR.MIDDLE)

    footer(s,dark=True); return s

# ============================================================ BUILD
cover()

# ---------------- ADMIN ----------------
section("COURSE ADMINISTRATION","Welcome & Housekeeping","")
tile_grid("Digital Attendance (Mandatory)",[
 "It is mandatory to take the AM, PM and Assessment digital attendance for WSQ-funded courses.",
 "The trainer/administrator displays the digital attendance QR code from the SSG portal.",
 "Scan the QR code with your mobile phone camera and submit your attendance.",
 "A minimum of 75% attendance is required to be eligible for assessment and funding."],kicker="TRAQOM · SSG DIGITAL ATTENDANCE")
trainer_slide("YOUR TRAINER · GENERAL","Your Trainer","General Trainer template —\nto be completed by the trainer",
 [("Name",""),("Title / Designation",""),("Qualifications",""),
  ("Areas of expertise",""),("Training & industry experience",""),("Contact","")],
 initials="?",accent=GREY)
trainer_slide("YOUR TRAINER",C.TRAINER,C.TRAINER_ROLE,C.TRAINER_ROWS,
 initials=C.TRAINER_INITIALS,accent=BLUE)
tile_grid("Let's Know Each Other",[
 "Your name and organisation / role.",
 "Your experience with video creation or editing (if any).",
 "What videos do you want to create after this course — marketing, training, social media?"],kicker="ICE-BREAKER")
tile_grid("Ground Rules",[
 "Set your mobile phone to silent mode.","Participate actively — no question is too small.",
 "Respect each other's views.","One conversation at a time.",
 "Exit quietly for calls or breaks.","Be punctual; 75% attendance is required."],
 kicker="HOUSEKEEPING",cols=2,size=15)
lms_login_slide()
lms_courseware_slide()
tile_grid("Lesson Plan — 2 Days, 8 hours/day",[
 ("Day 1 · 9:30–14:30 · LU1 (4 h)","Welcome and attendance; what makes a video engaging (two videos); hooks, message, characters, storytelling; script and storyboard with GenAI; Activity 1. Lunch 13:00–14:00."),
 ("Day 1 · 14:30–18:30 · LU2","Shot sizes, camera angles and movement, light, lens and cinematic effects; the Higgsfield UI; character and storyboard prompts; Activity 2 begins. Recap 18:15."),
 ("Day 2 · 9:30–10:30 · LU2 (5 h in total)","Attendance; finish Activity 2: review, score and finalise the takes."),
 ("Day 2 · 10:30–16:15 · LU3 (5 h)","Post-production in CapCut: cut to time, captions, music, colour, quality checks, remedial actions, export; Activity 3; ethics (IP, copyright, bias, consent)."),
 ("Day 2 · 16:15–16:30 · close of LU3","Revision, TRAQOM survey, Briefing for Assessment and assessment attendance."),
 ("Day 2 · 16:30–18:30 · Assessment","Written Assessment (SAQ), 1 h, then Practical Performance (PP), 1 h: one screenshot per activity.")],
 kicker="SCHEDULE · LU1 4 H · LU2 5 H · LU3 5 H",cols=2,size=12)
two_col("Skills Framework",[
 (f"TSC: {C.TSC_TITLE}  ·  {C.TSC_CODE}",0)]+[(k,1) for k in C.TSC_KNOWLEDGE],
 [(a,1) for a in C.TSC_ABILITIES],
 kicker="WSQ · SKILLS FRAMEWORK",lhead="Knowledge (assessed in the WA)",rhead="Abilities (assessed in the PP)",size=13)
tile_grid("Learning Outcomes",[
 ("LO1 — Script & plan","Create video scripts using Generative AI (GAI) and work plans for video production."),
 ("LO2 — Edit & assess","Edit video footage to improve video quality and ensure technical compliance."),
 ("LO3 — Apply new AI","Apply new AI technologies to improve efficiency and quality in accordance to industry standards.")],
 kicker="WHAT YOU'LL ACHIEVE",cols=1,size=16)
tile_grid("Course Outline",[
 (f"Topic 1 — {C.TOPICS[0]['title']}","Story before software: what makes a video engaging, hooks, one message, characters, a five-beat story, a GenAI script and a storyboard.  (Activity 1: your storyboard)"),
 (f"Topic 2 — {C.TOPICS[1]['title']}","Shoot it like a director: shot sizes, camera angles and movement, light, lens and cinematic effects; characters and storyboard prompts in Higgsfield.  (Activity 2: your footage)"),
 (f"Topic 3 — {C.TOPICS[2]['title']}","Finish it in CapCut: cut to time, captions, music, colour, quality checks and fixes, export to platform spec; ethics before you publish.  (Activity 3: your final video)")],
 kicker="THREE TOPICS · THREE ACTIVITIES · ONE VIDEO FROM IDEA TO EXPORT",cols=1,size=15)
tile_grid("Briefing for Assessment",[
 "Place phones and other materials under the table or on the floor.",
 "No photos or recording of assessment scripts.",
 "No discussion during the assessment.",
 "Use a black/blue pen for hard-copy assessments.",
 "No liquid paper / correction tape.",
 "Scripts are collected when time is up."],
 kicker="ASSESSMENT RULES",cols=2,size=13)
tile_grid("Assessment",[
 C.ASSESSMENT["written"], C.ASSESSMENT["practical"],
 "Format: Open Book — slides, Learner Guide and approved materials only.",
 C.ASSESSMENT["note"],"An appeal process is available if required."],kicker="FINAL ASSESSMENT")
flow_h("Assessment Flow",[
 "TRAQOM survey — scan the QR code on the LMS",
 "Assessment digital attendance — scan the SSG QR",
 "Sit WA (SAQ) then PP — open book",
 "Submit your answers on the LMS",
 "Sign the Assessment Summary Record"],kicker="ON ASSESSMENT DAY")
tile_grid("Criteria for Funding",[
 ("75% attendance","Minimum attendance rate of 75% based on the SSG Digital Attendance record."),
 ("Assessed Competent","Complete the assessment and be assessed as 'Competent'.")],
 kicker="WSQ FUNDING",cols=1,size=15)

# ================= v12 (23 Nov 2026): story -> shoot in Higgsfield -> edit in CapCut =================
from pptx.enum.dml import MSO_LINE
CC=os.path.join(ASSETS,"capcut"); SB=os.path.join(ASSETS,"sb")
def cc(n): return os.path.join(CC,f"capcut_{n}.jpg")
def sb(n): return os.path.join(SB,f"{n}.jpg")

def placeholder_slide(title,kicker,sub,what,shows,note=None,accent=TEAL):
    """A clearly marked VIDEO TO ADD frame (owner rule, 23 Nov 2026: no video yet -> a visual the trainer replaces)."""
    s=head_sub(slide(),title,kicker,sub,accent)
    x,y,w=0.85,2.35,7.2; h=w*9/16
    box=rect(s,Inches(x),Inches(y),Inches(w),Inches(h),LIGHT,line=GREY)
    box.line.dash_style=MSO_LINE.DASH; box.line.width=Pt(2)
    d=1.1; oval(s,Inches(x+w/2-d/2),Inches(y+h/2-d/2-0.45),Inches(d),Inches(d),accent)
    txt(s,Inches(x+w/2-d/2),Inches(y+h/2-d/2-0.45),Inches(d),Inches(d),[[("▶",30,WHITE,True)]],align=PP_ALIGN.CENTER,anchor=MSO_ANCHOR.MIDDLE)
    txt(s,Inches(x+0.3),Inches(y+h/2+0.3),Inches(w-0.6),Inches(1.0),
        [[("VIDEO TO ADD · TRAINER",13,accent,True)],[(what,12,GREY,False)]],align=PP_ALIGN.CENTER,space=3)
    rx=x+w+0.3; rw=12.48-rx; n=len(shows); gy=0.14; th=(h-gy*(n-1))/n
    for i,(lab,t) in enumerate(shows):
        yy=y+(th+gy)*i; col=PALETTE[i%len(PALETTE)]
        rect(s,Inches(rx),Inches(yy),Inches(rw),Inches(th),LIGHT); rect(s,Inches(rx),Inches(yy),Inches(0.08),Inches(th),col)
        txt(s,Inches(rx+0.25),Inches(yy),Inches(rw-0.4),Inches(th),[[(lab,13,col,True)],[(t,11.5,INK,False)]],anchor=MSO_ANCHOR.MIDDLE,space=2)
    notes(s,(note or "")+" Placeholder: record a short screen capture (30–90 s) and insert it over the dashed frame (Insert > Video > This Device), then delete the frame.")
    footer(s); return s

def picture_slide(title,img,kicker,sub=None,note=None,accent=BLUE):
    """One full-width visual (storyboard sheet, timeline diagram) with a one-line pitch."""
    s=head_sub(slide(),title,kicker,sub,accent)
    fit_pic(s,img,Inches(0.85),Inches(2.3),Inches(11.63),Inches(4.6))
    notes(s,note); footer(s); return s

# ---------------- TOPIC 1: story, hooks, storyboard ----------------
def topic1_concepts():
    big_statement("Same bottle. Same footage. Only one makes you care.",
     "Watch two short videos made from the same Higgsfield clips. Then tell us: what makes a video engaging?",
     "TOPIC 1 · WHAT MAKES A VIDEO ENGAGING?",color=BLUE,img="creator-desk.jpg",
     note="Image: generated with Higgsfield GPT Image 2.6. Set up the experiment: no explanation yet, just 'watch these two'.")
    video_slide(C.OPENER_VIDEOS[0],"VIDEO A · 20 SECONDS",
     "Watch it to the end. Notice the moment you stopped paying attention.",
     note="Play with sound (there is none, deliberately). Ask: at which second did you lose interest? Most rooms say 'at the logo card'. Built for the course from stills of the SOLA footage, 23 Nov 2026.")
    video_slide(C.OPENER_VIDEOS[1],"VIDEO B · 18 SECONDS",
     "Same product, same footage. A hook, a person and a payoff.",
     note="Play with sound. Then ask the room the question on the next slide before you reveal the answer. Built for the course from the Higgsfield SOLA ad, 23 Nov 2026.")
    big_statement("Your turn: what makes a video engaging?",
     "Two minutes with your neighbour. Name three things Video B did that Video A did not. Write them down before the next slide.",
     "DISCUSSION · 5 MINUTES",color=TEAL,
     note="Collect answers on the whiteboard. Group them into the four ingredients on the next slide: hooks, message, characters, storytelling.")
    tile_grid("Four ingredients of an engaging video",[
     ("Hooks","Earn the next second in the first three. Video B opens on a question; Video A opens on a logo."),
     ("Message","One sentence the viewer keeps: 'stays cold after the run'. Video A lists three features."),
     ("Characters","A person with a problem. We watch the runner; nobody watches a packshot for 20 s."),
     ("Storytelling","Hook, problem, turn, payoff, call to action. Video A has no turn and no payoff.")],
     kicker="TOPIC 1 · THE ANSWER",cols=2,size=15,icons=["H","M","C","S"])
    compare_table("Video A vs Video B, second by second",
     ["","Video A","Video B"],
     [["0–3 s","Logo card, small grey text","Question hook over a sweating bottle"],
      ["Message","Three features, no point","One promise: still cold after the run"],
      ["Character","None","A runner at sunrise"],
      ["Story","None: still, still, still","Problem → grab → drink → payoff"],
      ["Sound","Silence","Ice clink, breath, city"],
      ["Ending","'Thank you for watching'","Call to action: 'Pre-order today'"]],
     kicker="DECONSTRUCT THE TWO CUTS",accent=VIOLET,
     note="Point out that Video B is not more expensive: it uses the same footage. The difference is decided before the camera rolls, in the story and the storyboard.")
    big_numbers("The first three seconds decide the rest",[
     ("47%","of the value","of a video campaign was delivered in the first 3 seconds"),
     ("74%","of the value","was delivered within the first 10 seconds"),
     ("3 s","your hook window","in every video you make in this course")],
     kicker="HOOKS · WHY THE OPENING MATTERS",sub="Meta (then Facebook) with Nielsen, February 2016: 'up to' these shares of campaign value",
     band="Start on the action, the question or the surprise. Never on a logo, a greeting or a title card.",
     note="Source: Facebook for Business, 'Updated features for video ads', Feb 2016, citing Nielsen analysis ('up to 47%… in the first three seconds', 'up to 74%… in the first ten'). Quote it as 'up to'.")
    tile_grid("Six hooks that stop the scroll",[
     ("Ask a question","'Warm water by your first kilometre?'"),
     ("Drop a number","'3 hours a day on your phone. Try 15 minutes on you.'"),
     ("Break the pattern","An unexpected image: the bottle sweating in a freezer of ice."),
     ("Start mid-action","Open on the runner already sprinting; explain nothing yet."),
     ("Show before / after","Tired face, cut, the same face smiling: the story in two frames."),
     ("Open a loop","'Watch what happens at the top of the stairs.' Pay it off at the end.")],
     kicker="HOOKS · PICK ONE FOR ACTIVITY 1",cols=2,size=13,accent=VIOLET,
     note="hook-cards.pdf in the Activity 1 folder has these six with blank lines. Learners write three hook options and circle one.")
    tile_grid("One video, one message",[
     ("The one-sentence test","[Audience] should [feel or do] because [reason]. 'Weekend runners should pick SOLA because it stays cold after the run.'"),
     ("Two 'and's = two videos","'Cold and stylish and eco-friendly' is three messages. Pick one; save the rest for episode 2."),
     ("Say it with pictures","If the message needs a voice-over to make sense, the shots are wrong. The drink, the ice, the smile carry it."),
     ("End on the action","The call to action is the message turned into a verb: pre-order, book, try, share.")],
     kicker="MESSAGE · THE ONE THING THEY REMEMBER",cols=2,size=13)
    tile_grid("Characters people follow",[
     ("A face in 3 seconds","People watch people. Get a face on screen early, even in a product ad."),
     ("A want","She wants to finish the run. The viewer leans in because she wants something."),
     ("A problem","Heat, tiredness, a deadline: no obstacle, no story."),
     ("A consistent look","Same face, hair and clothes in every shot. In Topic 2 you lock it as a Higgsfield Element."),
     ("A change","The last shot shows her different: refreshed, proud, relieved. That change is your payoff.")],
     kicker="CHARACTERS · THE ONE THE CAMERA FOLLOWS",cols=1,size=13,accent=TEAL)
    process_map("A 15-second story in five beats",[
     ("Hook","0–3 s · stop the scroll"),
     ("Problem","3–6 s · what is in the way"),
     ("Turn","6–10 s · the product or idea acts"),
     ("Payoff","10–13 s · the world changes"),
     ("Call to action","13–15 s+ · what to do now")],
     kicker="STORYTELLING · THE STRUCTURE YOU WILL STORYBOARD",color=VIOLET,
     synthesis=("Five beats, three seconds each","Video B follows it exactly. Pixar's story spine says the same thing in long form: once upon a time… every day… one day… because of that… until finally."))
    tile_grid("Show it, don't say it: six ways video carries a message",[
     ("The picture","Ice on the bottle says 'cold' faster than any caption."),
     ("Shot size","A close-up says 'feel this'; a wide says 'look where we are'."),
     ("Sound","An ice clink, a breath, a music hit on the payoff."),
     ("On-screen text","Six words or fewer: most social video starts muted."),
     ("Pace","Fast cuts for energy; hold a shot for emotion."),
     ("Colour and light","Golden hour feels warm and hopeful; blue night feels lonely.")],
     kicker="HOW VIDEO CONVEYS THE MESSAGE",cols=2,size=13,accent=AMBER)
    compare_table("A storyboard is your video before it costs a credit",
     ["Panel field","What you write","Example (SOLA, panel 1)"],
     [["Time","Where the panel sits in the 15 s","0–3 s"],
      ["Size · angle · move","Shot size, camera angle, camera movement","Extreme close-up · low · slow push-in"],
      ["Action","What we see happen","Sun slides across the sweating bottle"],
      ["Sound","Ambience, effect, music, voice","Wind, distant city"],
      ["On-screen text","Hook, caption or call to action","'Warm water by your first kilometre?'"],
      ["Frame","A sketch or a generated still","Stick figure or a 2-credit Higgsfield image"]],
     kicker="STORYBOARD · THE SIX FIELDS",accent=TEAL,
     note="storyboard-sheet.pdf in the Activity 1 folder has these fields for six panels, plus boxes for the house rules and the work plan.")
    picture_slide("Example 1: the SOLA storyboard",sb("storyboard-sola"),"STORYBOARD · EXAMPLE",
     "Five panels, each with size, angle, movement, action and sound. Next: the film it became.",
     note="Ask: which panel is the hook, which is the payoff? (Panel 1 and panel 5.)")
    video_slide(C.DEMO_VIDEOS[0],"STORYBOARD → FILM · MADE IN HIGGSFIELD",
     "The same five panels, generated in one Seedance 2.5 prompt",
     note="Play with sound. Point out each panel as it arrives. The bottle stays identical because every shot names it; the music hit lands on the packshot because the Sound line asked for it.")
    picture_slide("Example 2: the Ringfall storyboard",sb("storyboard-ringfall"),"STORYBOARD · EXAMPLE",
     "Four panels for a sci-fi scene: establish, follow, react, reveal.",
     note="Ask: why does the close-up of her face (panel 3) come before the reveal (panel 4)? We see her awe before we see what she sees.")
    video_slide(C.DEMO_VIDEOS[1],"STORYBOARD → FILM · MADE IN HIGGSFIELD",
     "Establish, follow, react, reveal: the storyboard on screen",
     note="The extreme wide at 11–15 s sells the scale. Ask which shot learners would cut if it had to be 10 s.")
    shot_hero("Let GenAI draft the script: brief it like a director",hf("015"),[
     ("WHO","Your character: 'a runner, 30, at sunrise'."),
     ("WHERE","One location you could photograph: 'a city rooftop'."),
     ("WHAT HAPPENS","One visible action with an ending: 'drinks, smiles, runs on'.")],
     kicker="SCRIPT · HIGGSFIELD SUPERCOMPUTER",sub="Three lines remove the three guesses a lazy prompt leaves to the model",img_h=2.4)
    shot_steps("AI Director turns a brief into a script and storyboard",hf("040"),[
     ("Project brief","Where the locked script and storyboard live."),
     ("Elements","The characters and locations this project can call."),
     ("AI Director","Opens the director chat inside the project."),
     ("Suggested starts","'Write a script', 'Generate an 8-shot storyboard'.")],
     kicker="SCRIPT · AI DIRECTOR",sub="Your writers' room sits inside the project, next to the footage",
     marks=[(0.07,0.14),(0.05,0.25),(0.06,0.47),(0.87,0.52)])
    tile_grid("Edit the script before you shoot it (A1)",[
     ("Hook in 3 s?","If the first panel is a logo or a greeting, rewrite it."),
     ("One message?","Strike every line that serves a second message."),
     ("A character who wants something?","Give them a problem in panel 2."),
     ("A visual payoff?","The last panel must look different from the first."),
     ("Shootable in time?","Three actions in a 3-second panel will not render."),
     ("Write the edits down","Each edit you make is A1 evidence for PP Task 1.")],
     kicker="A1 · REVIEW THE SCRIPT LIKE AN EDITOR",cols=2,size=13,
     note="AI drafts; you decide. The PP asks for the edits you made, not the AI's first version.")
    tile_grid("Six defects to plan out at the storyboard stage (K1)",[
     ("Identity drift","The hero's face or clothes change between shots."),
     ("Prop teleport","The bottle swaps hands or vanishes mid-scene."),
     ("Broken physics","Hands merge, liquids melt, people walk through tables."),
     ("Audio mismatch","Footsteps without feet, music over dialogue."),
     ("Garbled text","Signs and labels turn into nonsense letters: add text in the edit instead."),
     ("Wrong spec","Wrong ratio, 480p left in the final, a cut mid-movement.")],
     kicker="K1 · TYPES OF QUALITY ISSUES",cols=2,size=13,accent=AMBER)
    compare_table("House rules: one platform, one spec",
     ["","YouTube","TikTok / Shorts","Instagram Reels"],
     [["Ratio","16:9 landscape","9:16 vertical","9:16 vertical"],
      ["Your length","15–60 s","15–20 s","15–20 s"],
      ["Pacing","Build with structure","Hook in 1–3 s, fast cuts","Aesthetic-first, fast"],
      ["Captions","Recommended","Essential (muted viewing)","Essential"],
      ["AI label","Disclose realistic AI content","AI-generated label","Label AI content"]],
     kicker="A2 · STANDARDS AND GUIDELINES",accent=VIOLET,
     note="The house rules box on the storyboard sheet: platform spec, captions, music rights, PDPA consent, AI label, IMDA/ASAS codes.")
    big_numbers("Plan the budget before the shoot",[
     ("45","credits","a 15 s Seedance 2.5 Draft at 480p"),
     ("240","credits","the same 15 s at 1080p, about 5× the price"),
     ("3","Drafts max","per shot before you finalise one")],
     kicker="A3 · WORK PLAN AND CREDIT BUDGET",sub="Read on Higgsfield, 9 Nov 2026: put these numbers in the work-plan box",
     band="Work plan: storyboard lock → Elements → Draft takes → 1080p finals → CapCut edit → review → export → publish.")

# ---------------- TOPIC 2: cinematic technique in Higgsfield ----------------
def topic2_concepts():
    tile_grid("Shot sizes: decide what the viewer must read",[
     ("Extreme wide (EWS)","Where are we? Scale, world, the city at sunrise."),
     ("Wide (WS)","The whole body and the place around it."),
     ("Medium (MS)","Waist up: action and gesture."),
     ("Medium close-up (MCU)","Chest up: the face starts to talk."),
     ("Close-up (CU)","The face, the emotion, the reaction."),
     ("Extreme close-up (ECU)","A detail: the ice, the label, an eye.")],
     kicker="TOPIC 2 · SHOTS",cols=2,size=13)
    shot_hero("Every numbered shot in your prompt starts with a size",hf("058"),[
     ("Wide","Character and surroundings: where are we?"),
     ("Medium close-up","Expression and upper-body action: what are they doing?"),
     ("Close-up","A face, a reaction or an important detail: what do they feel?")],
     kicker="SHOTS · SIZE IN HIGGSFIELD",sub="Three words at the start of each shot line change the whole film",img_h=3.1)
    tile_grid("Camera angles change how we feel about the character",[
     ("Eye level","Neutral, honest: we meet them as equals."),
     ("Low angle","Looking up: power, confidence, a hero."),
     ("High angle","Looking down: small, tired, vulnerable."),
     ("Bird's-eye / top shot","A map of the action; patterns, scale."),
     ("Dutch tilt","A tilted horizon: unease, something is wrong."),
     ("Over-the-shoulder / POV","Put the viewer inside the scene, in their shoes.")],
     kicker="CAMERA ANGLES",cols=2,size=13,accent=TEAL)
    tile_grid("Camera movement: motion with a meaning",[
     ("Push-in (dolly in)","Move closer as the emotion rises."),
     ("Pull-out / drone pull-back","Reveal the world: the payoff in scale."),
     ("Pan / tilt","Follow a look, reveal the next thing in the room."),
     ("Tracking","Move with the runner: energy and momentum."),
     ("Crane / orbit","A hero moment; circle the product."),
     ("Handheld / locked off","Handheld for urgency; locked off for calm and packshots.")],
     kicker="CAMERA MOVEMENT",cols=2,size=13,accent=VIOLET)
    shot_pair("Compose the frame, then write what we hear",
     (hf("060"),"Rule of thirds","Eyes on the upper third, the subject off-centre, space in the direction she looks."),
     (hf("061"),"Sound is part of the prompt","Ambience, footsteps, clothing movement, dialogue. Seedance renders it with the picture."),
     kicker="COMPOSITION AND SOUND",sub="Two lines in the prompt that separate a clip from a scene")
    shot_pair("Light and lens: the look in two settings",
     (hf("005"),"Camera, lens, aperture","DV Camcorder to Modern; Halation Vintage to Clean Sharp; f/1.4 for shallow focus, f/11 for deep focus."),
     (hf("003"),"Lighting presets","Silhouette, Practicals, Window, Overhead fall, or place your own lights. Golden hour reads warm and hopeful."),
     kicker="CINEMATIC TECHNIQUE · LIGHT + LENS",sub="Cinema Studio puts a camera crew's choices in two menus")
    shot_pair("Grade the colour, set the genre",
     (hf("004"),"Colour palette","Film colors, Nostalgic blue, Black gloss, Soft palette, or build your own grade."),
     (hf("006"),"Genre, era, tempo","The conventions, the period and the cutting pace the model should follow."),
     kicker="CINEMATIC TECHNIQUE · COLOUR + GENRE",sub="A grade and a genre tell the model the mood in two clicks")
    tile_grid("Cinematic effects that lift AI footage",[
     ("Slow motion","Stretch the payoff: the drink, the ice, the splash."),
     ("Speed ramp","Fast into the action, slow on the moment, fast out."),
     ("Shallow depth of field","Blur the background so the eye goes where you want."),
     ("Silhouette and backlight","Shape and mood without showing every detail."),
     ("Lens flare and halation","Warm, filmic highlights at golden hour."),
     ("Colour grade","One look across every shot, so Draft and final takes match.")],
     kicker="CINEMATIC EFFECTS",cols=2,size=13,accent=AMBER)
    shot_steps("Higgsfield: every tool on one home page",hf("002"),[
     ("Supercomputer","The agent: brief it in plain English; it asks before it spends."),
     ("Seedance 2.5","The video model: 4–30 s, up to 1080p, native sound."),
     ("Cinema Studio 4.0","The director's chair: camera, lens, light, colour, genre."),
     ("Genjutsu","Swap objects or copy motion in existing footage."),
     ("Higgsfield in Claude & ChatGPT","The same studio through an MCP connector.")],
     kicker="HIGGSFIELD UI · THE HOME PAGE",sub="Learn five tiles and you can find everything else",
     marks=[(0.80,0.735),(0.59,0.735),(0.40,0.93),(0.43,0.735),(0.59,0.93)])
    link_slide("Sign up with the course link",C.HF_SIGNUP,C.HF_SIGNUP_SHORT,[
     ("Sign up",f"Open {C.HF_SIGNUP_SHORT} and create your account with Google or email."),
     ("Disclosure",C.HF_DISCLOSURE),
     ("Plan for Activity 2","The website needs a paid plan. Plus: US$49/month or US$39 billed yearly for 1,000 credits (8 Nov 2026)."),
     ("Free trial terms","3 days, needs a card, renews to Plus unless cancelled; trial credits worked only via the Higgsfield MCP (8 Nov 2026)."),
     ("No paid plan? Try VidoGrid free",C.VIDOGRID_NOTE)],
     kicker="HIGGSFIELD · SIGN-UP",sub="One account: your characters, takes and finals all live in it",
     note="Check every learner can see a credit balance before Activity 2. If the class uses trainer-provided accounts, hand them out here.")
    tile_grid("Free AI subscriptions for video creation",[(h,d) for h,d in C.FREE_AI_SUB]+
     [("Free to start, today","VidoGrid (vidogrid.ai): 480p test takes with your storyboard prompt; check the cost on the Generate button.")],
     kicker="SKILLSFUTURE · FREE 6-MONTH AI SUBSCRIPTION",cols=1,size=12,accent=TEAL,icons=["G","S","+","✓","V"],
     note="Source: MySkillsFuture, 'Redeem AI Subscription to Further Your AI Learning' (last updated 21 Oct 2026). Only courses carrying the 'Free AI sub' label qualify: check this course's MySkillsFuture listing before telling learners they are eligible.")
    shot_steps("Cinema Studio: the panel where the storyboard becomes footage",hf("036"),[
     ("References 0/50","Attach your character and location Elements."),
     ("Film setup · Camera","Camera body, lens and aperture."),
     ("Colour palette · Lighting","The grade and the light scheme."),
     ("Describe your scene","Type @ to drop in a saved character or location."),
     ("Model and settings","Model, resolution, ratio, length, sound, takes, credits.")],
     kicker="HIGGSFIELD UI · CINEMA STUDIO",sub="Set the look once, then every take inherits it",
     marks=[(0.38,0.50),(0.54,0.50),(0.76,0.50),(0.49,0.58),(0.47,0.66)])
    shot_pair("Prompt your character before you shoot a frame",
     (hf("038"),"Ask Supercomputer to cast","'Main character for a 15-second ad: 30, runner, grey sportswear.' It loads the character-sheet skill."),
     (hf("039"),"Choose from the options","Photoreal candidates. You pick one; only then does it build the reference sheet."),
     kicker="CHARACTER ASSETS · CASTING PROMPT",sub="A cast you chose on purpose beats a face the model invents every take",img_h=3.4)
    shot_hero("One sheet, three views: the reference every shot obeys",hf("041"),[
     ("Full body, front","Clothes, shoes, proportions. 'Same outfit in every view.'"),
     ("Full body, back","What the camera sees when she runs away from it."),
     ("Face portrait","The one face every shot copies: Higgsfield covers the full-body face on purpose.")],
     kicker="CHARACTER ASSETS · REFERENCE SHEET",sub="Plain background, consistent light: the model copies exactly what it sees",img_h=3.0,
     note="The covered full-body face is Higgsfield's identity trick, not a defect: one sharp face for the model to copy.")
    shot_pair("Save once as an Element, call it by name",
     (hf("048"),"@char_runner in every prompt","One saved Element, attached automatically, prompt after prompt: the fix for drifting faces (K2)."),
     (hf("049"),"The Element form","Category (Character, Location, Prop), Name, Element ID such as char_runner, a one-line description."),
     kicker="CHARACTER ASSETS · ELEMENTS",sub="Naming rule: char_, loc_, prop_ + a short slug")
    shot_hero("Locations need anchors a shot can point at",hf("046"),[
     ("Spatial anchors","The counter, the stools, the window: things a shot line can name."),
     ("No people","Your saved character will be placed into it."),
     ("Save it","loc_rooftop becomes @loc_rooftop in every prompt.")],
     kicker="CHARACTER ASSETS · LOCATIONS",sub="'She sits on the third stool' only works if the stool exists in the reference",img_h=3.0)
    compare_table("Storyboard panel → prompt line",
     ["Panel","Time","Size · angle · move","Action · light"],
     [["1 Hook","0–3 s","ECU · low · slow push-in","Sun slides across the sweating bottle · golden backlight"],
      ["2 Problem","3–6 s","MS · eye level · handheld","@char_runner stops, breathless, wipes her brow"],
      ["3 Turn","6–10 s","CU · eye level · static","She drinks; ice clinks; eyes close"],
      ["4 Payoff","10–13 s","EWS · high · drone pull-back","She runs on across @loc_rooftop at sunrise"],
      ["5 CTA","13–15 s","MS · eye level · locked off","Hero packshot, space for the logo"]],
     kicker="PROMPTS THAT FOLLOW THE STORYBOARD",accent=VIOLET,
     note="One storyboard row = one numbered shot line. Add ONE Sound line for the whole clip. storyboard-to-prompt.csv in the Activity 2 folder has this layout.")
    shot_pair("Write the scene, attach the references, number the shots",
     (hf("056"),"Context, references, shots","01 scene context in 1–2 sentences; 02 references and their roles; 03 the numbered, timed shots."),
     (hf("057"),"A real prompt with @handles","Each Element '100% as shown', with who holds what and where they stand."),
     kicker="PROMPTS THAT FOLLOW THE STORYBOARD",sub="The format the Activity 2 prompt gives you to adapt")
    shot_steps("Draft mode: three test takes cost less than one final",hf("062"),[
     ("References attached","Character and location Elements."),
     ("Your storyboard prompt","Scene, references, numbered shots, Sound line."),
     ("Seedance 2.5 Draft","480p, your ratio, 15 s, sound on."),
     ("Generate Draft","About 45 credits a 15 s take; review before you spend more.")],
     kicker="TAKES · DRAFT MODE",sub="Explore at 480p, commit at 1080p",
     marks=[(0.35,0.445),(0.80,0.60),(0.30,0.965),(0.925,0.81)])
    shot_pair("Up to three Drafts per shot, then finalise one",
     (hf("063"),"Draft takes at 480p","Same prompt, several takes (four shown here). Compare the face, the bottle and the light."),
     (hf("064"),"Generate the keeper in 1080p","The selected Draft re-rendered at full resolution: same take, full quality."),
     kicker="TAKES · DRAFT → FINAL",sub="Drafts can be finalised within seven days")
    tile_grid("Review the take for story and emotion (A4)",[
     ("Look for","A weak opening image, a payoff with no sound, a reaction cut too early."),
     ("Tie it to a shot","'Shot 3: hold the smile one more second.' A change without a shot number is vague."),
     ("Name two","A4 needs at least two story or emotion improvements, each tied to a numbered shot."),
     ("Change one thing per take","Then you know which change fixed it.")],
     kicker="A4 · REVIEW FOOTAGE FOR STORY AND EMOTION",cols=2,size=13,accent=TEAL)
    compare_table("Quality issues → the Higgsfield fix",
     ["Issue (K1)","Typical cause","Fix (K2)"],
     [["Face changes between shots","No character reference","Character Element + sheet"],
      ["Set changes between shots","No location reference","Location Element with anchors"],
      ["Prop swaps hands or vanishes","Holder not stated","'@prop… in @char…'s right hand'"],
      ["Wrong object in the shot","Model guessed","Genjutsu Replace Object, or regenerate"],
      ["Soft, low-res footage","480p Draft exported","Finalise at 1080p or Upscale"],
      ["Garbled on-screen text","Model drew the letters","Remove it; add text in CapCut"]],
     kicker="K1 → K2 · THE WA ASKS EXACTLY THIS",accent=TEAL)
    tile_grid("Parameters to assess the footage (K3, A5)",[
     ("Resolution & sharpness","1080p for the final; no 480p Draft left in."),
     ("Motion & physics","No melting hands, sliding feet or stutter."),
     ("Continuity","Face, clothes, props and set match shot to shot."),
     ("Audio","Effects match the action; nothing clipped."),
     ("Pacing & length","Each panel lands in its time; total 15–20 s."),
     ("Compliance","Ratio, safe area, rights, consent, AI label planned.")],
     kicker="K3 · SCORE EVERY TAKE BEFORE YOU EDIT",cols=2,size=13)

# ---------------- TOPIC 3: post-production in CapCut ----------------
def topic3_concepts():
    big_statement("The edit is where the story is written a second time.",
     "Higgsfield gives you raw takes. CapCut is where you cut them to time, add the words and the music, and make it publishable.",
     "TOPIC 3 · POST-PRODUCTION",color=BLUE,img="directors-chair.jpg")
    process_map("Post-production in CapCut: five passes",[
     ("Import + ratio","clips in, 9:16 or 16:9"),
     ("Assemble","storyboard order"),
     ("Cut to time","15–20 s, hook first"),
     ("Polish","captions · text · music · colour"),
     ("Check + export","house rules · 1080p · MP4")],
     kicker="THE EDITING WORKFLOW",color=TEAL,
     synthesis=("One pass at a time","Structure before polish: never caption a clip you may still cut."))
    shot_steps("CapCut home: start a project, or let AI start it",cc("home"),[
     ("Create project","Opens an empty editor: you will use this in Activity 3."),
     ("EditPilot","Describe an idea or task; CapCut's AI drafts and edits in one flow."),
     ("AI video","Turn an idea or image into a clip."),
     ("Extend video","Extend a clip that ends too soon."),
     ("AI edit","Edit clips by describing the change."),
     ("Video Studio","Generate 30-second videos with Seedance 2.5, the model you used in Higgsfield.")],
     kicker="CAPCUT UI · HOME (DESKTOP 9.7.1)",sub="Read on CapCut for Mac, 23 Nov 2026; the account panel is blurred",
     marks=[(0.455,0.143),(0.19,0.235),(0.56,0.26),(0.775,0.26),(0.885,0.26),(0.075,0.39)],
     note="Labels read from CapCut desktop 9.7.1 on 23 Nov 2026. Some tools are marked Pro (paid). The free editor covers everything Activity 3 needs.")
    shot_steps("The CapCut editor: five areas you will use",cc("editor"),[
     ("Import","Bring in your Higgsfield MP4s."),
     ("Tool tabs","Media, Audio, Text, Effects, Transitions, Captions, Filters, Adjustment."),
     ("Player + Ratio","Preview; set 9:16 or 16:9 with Ratio."),
     ("Timeline","Clips, text, captions and audio as stacked tracks."),
     ("Export","Resolution, frame rate, format.")],
     kicker="CAPCUT UI · THE EDITOR",sub="Left: what you add. Centre: what you see. Bottom: when it happens.",
     marks=[(0.215,0.32),(0.20,0.065),(0.64,0.696),(0.30,0.876),(0.964,0.02)],
     note="Project name and local path are blurred. Split at the playhead: Cmd+B (Mac) or Ctrl+B (Windows).")
    placeholder_slide("Watch the edit: from takes to a timeline","CAPCUT · DEMO",
     "A one-minute walkthrough of Activity 3, recorded by the trainer",
     "Screen recording of CapCut: import three Higgsfield takes, set 9:16, split and delete, add auto captions and music, export.",
     [("0:00 Import + Ratio","Three MP4s in; Ratio → 9:16."),
      ("0:15 Split and delete","Cmd/Ctrl+B at the playhead; delete the warm-up."),
      ("0:30 Text + captions","Hook line in 0–3 s; auto captions, fix one word."),
      ("0:45 Music + export","Track under the ice clink; 1080p, 30 fps, MP4.")],
     note="Owner rule (23 Nov 2026): where we have no video yet, show a visual and the trainer adds the recording.")
    picture_slide("Too long? Here is what to cut first",sb("cut-timeline"),"CUT TO TIME",
     "A 32-second raw assembly becomes a 16-second ad: same footage, half the length, twice the punch",
     note="Walk the grey blocks: logo intro, warm-up, repeated drink, second wide, thank-you card. None of them serves the one message.")
    tile_grid("The cutting order when a video runs long",[
     ("1 · Intros and outros","Logo cards, greetings, 'thank you for watching'. Put the logo on the last shot instead."),
     ("2 · Warm-ups","Cut to the action: start each shot the moment something happens."),
     ("3 · Repeats","Two drinks, two wides: keep the better take, delete the other."),
     ("4 · Dead air","Pauses, slow starts, the second after the payoff."),
     ("5 · Second messages","Anything that serves a message you are not telling."),
     ("Never cut","The hook, every beat of the one message, the payoff, the call to action.")],
     kicker="TOO LONG? WHAT TO CUT",cols=2,size=13,accent=AMBER)
    tile_grid("Editing rules that keep viewers watching",[
     ("Cut on action","Cut while something moves: the hand reaching, the head turning. The cut disappears."),
     ("Change the size at every cut","Wide to close-up, not wide to wide: a jump cut feels like a mistake."),
     ("Hold the emotion","Give the close-up one more beat than feels necessary."),
     ("J-cut and L-cut","Let the sound of the next shot start early, or the last shot's sound run on."),
     ("1–3 s per shot","Social pacing; slow down only for the payoff."),
     ("End on the payoff","Cut out the moment after the story has landed.")],
     kicker="PACING AND RHYTHM",cols=2,size=13,accent=VIOLET)
    tile_grid("Polish in CapCut: what each tab is for",[
     ("Text","Hook line in 0–3 s; call-to-action card at the end; inside the safe area."),
     ("Captions","Auto captions, then read and fix every word. Muted viewers rely on them."),
     ("Audio","Music cleared for commercial use, lowered under the key sound, faded out."),
     ("Filters · Adjustment","One colour look across every clip so Draft and final shots match."),
     ("Transitions","One or two, or none: a hard cut is the default."),
     ("Ratio","9:16 for TikTok, Reels and Shorts; 16:9 for YouTube; reframe the subject into the safe area.")],
     kicker="POLISH · CAPTIONS, TEXT, MUSIC, COLOUR",cols=2,size=13)
    tile_grid("AI tools that fix and finish the footage",[
     ("Remove or replace objects","Higgsfield Genjutsu Replace Object swaps a wrong prop in finished footage and keeps the motion."),
     ("Add VFX","Higgsfield effect presets on a shot, or CapCut's Effects tab on the timeline: one or two, never the meal."),
     ("Clone a voice","Higgsfield Create Voice from a clean sample of YOUR voice, or a voice whose owner gave written consent."),
     ("Generative AI music","Higgsfield Audio composes a track from genre, tempo and mood: cleared, original, cut to your length."),
     ("AI voice-over","Type the narration, generate the voice, drop it on the CapCut audio track under the picture."),
     ("Enhance audio","CapCut's audio settings: volume, fades, keyframes, and noise reduction or voice enhancement where your version offers them.")],
     kicker="K5 · NEW AI TECHNOLOGIES FOR THE FINISH",cols=2,size=12,accent=VIOLET,
     note="Covers the CP's LU3 techniques: remove objects, add VFX, clone voice, generative AI music, generative AI voice-over, enhance audio. Consent rule: only clone a voice whose owner agreed in writing.")
    shot_steps("Remove an object without re-shooting",hf("019"),[
     ("Attach the shot","Drop the image or clip into Supercomputer."),
     ("Say what changes","'Remove the table and put the glasses on a plinth.'"),
     ("Keep everything else","Light, angle and the object itself stay as they were.")],
     kicker="REMOVE OBJECTS · HIGGSFIELD",sub="For video, Genjutsu Replace Object does the same while keeping the motion",img_w=7.6)
    compare_table("What captions, music and voice add to the cut",
     ["Feature","Parameter it supports","How"],
     [["Captions","Clarity and accessibility","Viewers on mute still follow the story; keep them in the safe area"],
      ["Music","Pacing and engagement","A track matched to the cut, under the key sounds, landing on the payoff"],
      ["Voice","Clarity and consistency","One recognisable voice: a stock voice, or your own with consent"]],
     kicker="K3 · CAPTIONS, MUSIC AND VOICE",accent=TEAL,
     note="Rights check: generated or licensed music only. Voice cloning only with the owner's written consent.")
    compare_table("Remedial actions: fix it in CapCut, or reshoot one shot",
     ["Fails the check","Remedial action (A6)","Where"],
     [["Runs 32 s, platform wants 15–20 s","Cut in the order above","CapCut: split + delete"],
      ["Captions wrong or off-screen","Correct words, move into safe area","CapCut: Captions"],
      ["Music drowns the key sound","Lower music, fade, keyframe volume","CapCut: Audio"],
      ["Shots don't match in colour","One filter / adjustment on all clips","CapCut: Filters, Adjustment"],
      ["Face drifts in one shot","Regenerate that shot with the Element","Higgsfield, then re-import"],
      ["Soft 480p footage","Finalise the Draft at 1080p","Higgsfield, then re-import"]],
     kicker="A6 · REMEDIAL ACTIONS",accent=AMBER,
     note="Cheapest fix first: a CapCut trim costs nothing; a 1080p regeneration costs about 240 credits.")
    compare_table("Export to the industry standard (K4)",
     ["Platform","Ratio · size","Frame rate · format","Before you post"],
     [["TikTok","9:16 · 1080×1920","30 fps · MP4 (H.264)","AI-generated label on"],
      ["Instagram Reels","9:16 · 1080×1920","30 fps · MP4","Label AI content"],
      ["YouTube Shorts","9:16 · 1080×1920","30 fps · MP4","Altered or synthetic content setting"],
      ["YouTube","16:9 · 1920×1080","30 fps · MP4","Altered or synthetic content setting"]],
     kicker="K4 · EXPORT SETTINGS",accent=VIOLET,
     note="CapCut's export dialog sets resolution, frame rate, bitrate, codec and format. Watch the exported file once on a phone before posting.")
    tile_grid("Industry standards and responsible AI (K4)",[
     ("Platform specs","Ratio, resolution, duration and loudness per platform."),
     ("Commercial rights","Your Higgsfield plan and your CapCut music must cover client work."),
     ("Consent & PDPA","Written permission for any real face or voice."),
     ("AI disclosure","TikTok's AI-generated label; YouTube's altered or synthetic content setting."),
     ("Advertising codes","IMDA and ASAS rules apply to AI ads too."),
     ("Accuracy","No claims you cannot prove: 'stays cold' needs a test, or a softer line.")],
     kicker="COMPLY BEFORE YOU PUBLISH",cols=2,size=13,accent=AMBER)
    compare_table("Evaluate a new AI technology (A7, K5)",
     ["Criterion","Ask","Example"],
     [["Efficiency","Minutes or credits saved per finished video?","CapCut auto captions: minutes, not an hour of typing"],
      ["Quality","Does the output meet your house rules?","Higgsfield Elements: the same face in every shot"],
      ["Control","Can you direct and correct it?","Draft mode: up to three takes to compare before you commit"],
      ["Rights","Commercial use allowed on your plan?","Check the music licence and the plan terms"],
      ["Fit","Does it slot into Higgsfield → CapCut?","Seedance 2.5 is also inside CapCut Video Studio"]],
     kicker="A REPEATABLE EVALUATION RUBRIC",accent=VIOLET,
     note="The AI drafts the evaluation; the learner decides the rating. PP Task 3 asks for two technologies, each with an efficiency and a quality gain.")

def ethics_slides():
    big_statement("Just because you can generate it doesn't mean you should publish it.",
        "Copyright and IP, consent, bias, deepfakes, disclosure: the last check before your video goes live.",
        "TOPIC 3 · ETHICS",img="ethics-face.jpg",
        note="Image: generated with Higgsfield GPT Image 2.6. Fictional face, not a real person.")
    tile_grid("Copyright and IP: four questions before you publish",[
     ("Who owns the output?","Read your Higgsfield plan: commercial use is a plan feature, not a given."),
     ("Is the music licensed?","Use generated music or a track cleared for commercial use; a trending song is not."),
     ("Did you copy a brand, a character or a style on purpose?","Disney and Universal sued Midjourney in June 2025 over Darth Vader, Elsa and the Minions."),
     ("What does your editor's licence say?","In June 2025 creators protested CapCut's updated terms over the licence they grant to uploaded content. Read before you upload client work.")],
     kicker="ETHICS · INTELLECTUAL PROPERTY AND COPYRIGHT",cols=1,size=13,accent=RUST,
     note="Sources: CNBC and Reuters, 11 Jun 2025 (Disney and Universal v. Midjourney); creator discussion of CapCut's June 2025 terms update (r/CapCut, June 2025): describe it as complaints, not a ruling.")
    tile_grid("Core ethical issues in GenAI video",[(h,d) for h,d,_ in C.ETHICS],
        kicker="TOPIC 3 · ETHICS BEFORE YOU PUBLISH",cols=2,size=12,accent=RUST,
        note="Ask each table to pick the issue most relevant to the video they made in Activity 3.")
    for part,rows in (("1/2",C.ETHICS_CASES[:5]),("2/2",C.ETHICS_CASES[5:])):
        compare_table(f"When it went wrong: real cases ({part})",
            ["Issue","Case","What happened"],
            [[i,c,w] for i,c,w,_ in rows],kicker="TOPIC 3 · LAWSUITS, DISPUTES AND RULINGS",accent=RUST,
            note="Sources (verified 9 Nov 2026): "+"; ".join(f"{c} — {src}" for _,c,_,src in rows))
    compare_table("Seven issues, seven rules for your own videos",
        ["Issue","Your rule in every project"],
        [[h,r] for h,_,r in C.ETHICS],kicker="TOPIC 3 · FROM ETHICS TO PRACTICE",accent=RUST)

TOPIC_CONCEPTS={1:topic1_concepts,2:topic2_concepts,3:topic3_concepts}

# ---------------- TOPICS + ACTIVITIES ----------------
TOPIC_ACTS={t["num"]:[a for a in ACTIVITIES if a["topic"]==t["num"]] for t in C.TOPICS}

def act_flow(a):
    process_map(f"How Activity {a['num']} Runs",[(t,"") for t in a["flow"]],
        kicker=f"ACTIVITY {a['num']} · HOW IT RUNS — FULL STEPS IN THE LEARNER GUIDE",color=TEAL,animate=False)

def evidence_slide(a):
    s=head_sub(slide(),f"Activity {a['num']} evidence: one screenshot",f"ACTIVITY {a['num']} · YOUR PP SCREENSHOT",
               "The Practical Performance asks for exactly this screenshot, plus a few typed lines",TEAL)
    rect(s,Inches(0.85),Inches(2.35),Inches(11.63),Inches(1.5),LIGHT); rect(s,Inches(0.85),Inches(2.35),Inches(0.1),Inches(1.5),TEAL)
    txt(s,Inches(1.2),Inches(2.35),Inches(11.1),Inches(1.5),[[("📸  "+a["evidence"][0],17,INK,True)]],anchor=MSO_ANCHOR.MIDDLE)
    rect(s,Inches(0.85),Inches(4.1),Inches(11.63),Inches(2.6),LIGHT); rect(s,Inches(0.85),Inches(4.1),Inches(0.1),Inches(2.6),BLUE)
    txt(s,Inches(1.2),Inches(4.2),Inches(11.1),Inches(2.4),[[("✓  Check your work",16,BLUE,True)],[(a["test"],14,INK,False)]],anchor=MSO_ANCHOR.MIDDLE,space=6)
    footer(s); return s

for t in C.TOPICS:
    acts=TOPIC_ACTS[t["num"]]
    section(f"TOPIC {int(t['code'])}",t["title"],t["code"],t["subtitle"],
            items=[f"Activity {a['num']} — {a['title']}" for a in acts])
    tile_grid(f"Key Concepts — Topic {int(t['code'])}",t["concepts"],
              kicker=f"COVERS {t['weighting']}",cols=2,size=13)
    a0=acts[0]
    tile_grid(f"Hands-On Activity — Topic {int(t['code'])}",
        [(f"Activity {a0['num']} — {a0['title']}",a0["build"]),
         ("Your PP evidence",a0["evidence"][0]),
         ("It builds on",{1:"Nothing yet: this is where your video starts. Activity 2 shoots this storyboard.",
                          2:"Your Activity 1 storyboard. Activity 3 edits the takes you make here.",
                          3:"Your Activity 2 takes. The export is the final video you upload to the TMS."}[t["num"]])],
        kicker="WHAT YOU'LL DO",cols=1,size=14,icons=[str(a0["num"]),"📸","↻"])
    TOPIC_CONCEPTS[t["num"]]()
    for a in acts:
        activity_overview(f"ACTIVITY {a['num']}",a["title"],a["desc"],a["build"],a["services"],
                          kicker=f"ACTIVITY {a['num']} · TOPIC {t['code']} · HANDS-ON",objective=a["objective"])
        act_flow(a)
        pgs=[]; cur=[]; cur_len=0
        for pr in a.get("prompts",[]):
            if cur and (len(cur)==2 or cur_len+len(pr[1])>900):
                pgs.append(cur); cur=[]; cur_len=0
            cur.append(pr); cur_len+=len(pr[1])
        if cur: pgs.append(cur)
        for pi,pg in enumerate(pgs,1):
            prompt_slide(f"Activity {a['num']}",pg,kicker=f"ACTIVITY {a['num']} · COPY-AND-ADAPT PROMPTS",
                         part=f"({pi}/{len(pgs)})" if len(pgs)>1 else None)
        evidence_slide(a)
    if t["num"]==3:
        ethics_slides()
    tile_grid(f"Recap — Topic {int(t['code'])}",
            [(f"Activity {a['num']} — {a['title']}", "You built: "+a["build"]) for a in acts]+
            [(k,v) for k,v in t["concepts"][:3]],
            kicker="TOPIC RECAP · WHAT YOU CAN NOW DO",cols=1,size=12,icons=[str(a["num"]) for a in acts]+["✓","✓","✓"])

# ---------------- CLOSE ----------------
section("WRAP-UP","Course Summary & Next Steps","")
process_map("The Pipeline You Now Own",C.PIPELINE,
 kicker="FROM IDEA TO PUBLISHED — RECAP",
 synthesis=("Three activities, one video",
  "Story and storyboard (Activity 1) → characters, cinematic shots and takes in Higgsfield (Activity 2) → cut, polish and export in CapCut (Activity 3)."),
 animate=False)
tile_grid("What You Achieved",[
 ("Hooks & message","A hook for the first 3 seconds and one message in one sentence."),
 ("Story & storyboard","Five beats on a six-panel storyboard, with house rules and a credit-priced work plan."),
 ("Characters","A face that never drifts: a Higgsfield Element used in every shot."),
 ("Cinematic shots","Size, angle, movement, light and lens written into every prompt line."),
 ("The edit","Cut to time, captions, music and colour in CapCut; fixed what failed."),
 ("Publish responsibly","1080p to platform spec, AI label on, rights and consent checked.")],
 kicker="LEARNING OUTCOMES DELIVERED",cols=2,size=13)
tile_grid("Recommended Next Courses",[
 "WSQ - Mastering Prompt Engineering for Generative AI Content Creation",
 "WSQ - Practical Image Generation Using GAN, VAE, and Diffusion Models",
 "WSQ - Digital Transformation and Business Innovation with Generative AI (GenAI)",
 "WSQ - Develop Generative AI Solutions with Azure OpenAI Service",
 "WSQ - Build LLM Applications Using Langchain and Flowise"],kicker="KEEP LEARNING")
tile_grid("Support",[
 "If you have any enquiries during and after the class, contact us:",
 "Email: enquiry@tertiaryinfotech.com",
 "Tel: +65 6100 0613",
 "Web: www.tertiarycourses.com.sg"],kicker="WE'RE HERE TO HELP")
lms_courseware_slide()
tile_grid("Cert & TRAQOM Survey (Mandatory)",[
 "Complete the TRAQOM course feedback survey on the LMS — it is mandatory for WSQ funding.",
 "Your digital certificate is issued on the LMS after you are assessed Competent.",
 "Portal: https://lms-tms.tertiaryinfotech.com"],kicker="BEFORE YOU LEAVE")
tile_grid("Briefing for Assessment",[
 "Place phones and other materials under the table or on the floor.",
 "No photos or recording of assessment scripts.",
 "No discussion during the assessment.",
 "PP: paste ONE screenshot per task, type the short answers, upload your final MP4 to the TMS.",
 "No liquid paper / correction tape.",
 "Scripts are collected when time is up."],
 kicker="ASSESSMENT RULES",cols=2,size=13)
tile_grid("Assessment",[
 C.ASSESSMENT["written"], C.ASSESSMENT["practical"],
 "Open book: slides, Learner Guide and approved materials only.",
 "Remember to take the Assessment digital attendance.",
 "Submit your completed answers and your MP4 on the LMS."],kicker="FINAL ASSESSMENT")
flow_h("Assessment Flow",[
 "TRAQOM survey — scan the QR code on the LMS",
 "Assessment digital attendance — scan the SSG QR",
 "Sit WA (SAQ) then PP — open book",
 "Submit your answers on the LMS",
 "Sign the Assessment Summary Record"],kicker="ON ASSESSMENT DAY")
tile_grid("Digital Attendance (Mandatory)",[
 "It is mandatory to take the AM, PM and Assessment digital attendance for WSQ-funded courses.",
 "The trainer/administrator displays the digital attendance QR code from the SSG portal.",
 "Scan the QR code with your mobile phone camera and submit your attendance.",
 "A minimum of 75% attendance is required to be eligible for assessment and funding."],kicker="TRAQOM · SSG DIGITAL ATTENDANCE")
big_statement("Thank You!","You can now take an idea from a hook to a published video: story first, shot in Higgsfield, finished in CapCut.","HAPPY CREATING",color=TEAL,img="directors-chair.jpg",
 note="Image: generated with Higgsfield GPT Image 2.6 (medium, 1K).")


# ---------------- transitions (one pass) ----------------
for i,s in enumerate(prs.slides):
    is_section=False
    # heuristic: section slides have the big pale number textbox at top-right
    _transition(s,"fade","fast")

OUT=os.path.join(REPO,"courseware",f"{C.SHORT_TITLE}-{C.VERSION}.pptx")
prs.save(OUT)
n=len(prs.slides._sldIdLst)
print(f"Saved {OUT}  ({n} slides)")
# Gates (user rule, 9 Nov 2026): every slide has a transition before p:timing; every video plays on click.
import subprocess
_here=os.path.dirname(os.path.abspath(__file__))
subprocess.run([sys.executable,os.path.join(_here,"ensure_transitions.py"),OUT],check=True)
subprocess.run([sys.executable,os.path.join(_here,"ensure_transitions.py"),OUT,"--check"],check=True)
subprocess.run([sys.executable,os.path.join(_here,"pptx_online_video.py"),"check",OUT],check=True)
