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
        [[("Made entirely in Higgsfield: Supercomputer · Cinema Studio · Seedance 2.5 · Elements · Draft mode",15,PALE,False)]])
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
        y=Inches(2.45)
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
def tile_grid(title,items,kicker=None,cols=2,size=15,icons=None,accent=BLUE,note=None):
    s=head(slide(),title,kicker,kcolor=accent)
    n=len(items); rows=math.ceil(n/cols)
    X0=Inches(0.85); Y0=Inches(1.95); TOTW=Inches(11.63); AREAH=Inches(4.78)
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
    s=head(slide(),title,kicker,kcolor=color)
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
    s=head(slide(),title,kicker,kcolor=accent)
    X0=Inches(0.85); TOTW=Inches(11.63); ncol=len(headers)
    first=int(TOTW*0.26); rest=int((TOTW-first)/(ncol-1))
    widths=[first]+[rest]*(ncol-1)
    y=Inches(1.95); hh=Inches(0.52)
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
 ("Day 1 · 9:30–14:30 · LU1 (4 h)","Attendance, introductions, Higgsfield sign-up; the impact of AI on video and its use cases; Labs 1–3. PM attendance at 14:00."),
 ("Day 1 · 14:30–18:30 · LU2","Elements: characters, locations, props (Lab 4); shots and takes in Cinema Studio (Lab 5); Day 1 recap at 18:15."),
 ("Day 2 · 9:30–10:30 · LU2 (5 h in total)","Attendance; cut, caption and assess the scene (Lab 6)."),
 ("Day 2 · 10:30–16:30 · LU3 (5 h)","Tea break 10:30–10:45, then fix, voice, music and effects (Labs 7–8); use-case sprint (Lab 9); mini capstone (Lab 10); ethics of GenAI video and course summary."),
 ("Day 2 · 16:15–16:30 · close of LU3","Revision, TRAQOM survey, Briefing for Assessment and assessment attendance."),
 ("Day 2 · 16:30–18:30 · Assessment","Written Assessment (SAQ), 1 h, then Practical Performance (PP), 1 h.")],
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
 (f"Topic 1 — {C.TOPICS[0]['title']}","Script, plan and make your first video: Higgsfield sign-up, Supercomputer and AI Director scripts and shot lists, standards, work plan and credit budget.  (Labs 1–3)"),
 (f"Topic 2 — {C.TOPICS[1]['title']}","Build, shoot and assess: Elements (characters, locations, props), references, Cinema Studio shots and takes, Draft mode, cut, captions and quality scoring.  (Labs 4–6)"),
 (f"Topic 3 — {C.TOPICS[2]['title']}","Fix, finish and publish: replace objects, upscale, reframe, voice, music, effects, model comparison, a published ad and your own mini capstone video.  (Labs 7–10)")],
 kicker="THREE TOPICS · TEN HANDS-ON LABS · ONE STUDIO: HIGGSFIELD",cols=1,size=15)
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

# ---- use cases (shown in Topic 1)
def yt_short_slide(title,lead,second,kicker,sub=None,band=None,note=None,lead_vertical=True):
    """Embed the owner-named YouTube video (a Short, or one named long film) and show a second, sourced example
    as a fact card with no embed or link (house rule: learners only get Shorts, plus videos the owner names).
    lead = (video_id, label, fact); second = (label, fact)."""
    s=head_sub(slide(),title,kicker,sub,VIOLET)
    lid,llab,lfact=lead; slab,sfact=second
    if lead_vertical:
        lw,lh=2.42,4.3; url=f"https://www.youtube.com/shorts/{lid}"
    else:
        lw,lh=7.0,7.0*9/16; url=f"https://www.youtube.com/watch?v={lid}"
    th=os.path.join(YT,f"{lid}.jpg")
    add_online_video(s,url,0.85,2.35,lw,lh,poster=th if os.path.exists(th) else None,name=llab)
    def card(x,y,w,h,col,tag,lab,fact):
        rect(s,Inches(x),Inches(y),Inches(w),Inches(h),LIGHT); rect(s,Inches(x),Inches(y),Inches(0.08),Inches(h),col)
        txt(s,Inches(x+0.25),Inches(y),Inches(w-0.4),Inches(h),[[(tag,9.5,col,True)],[(lab,13,INK,True)],[(fact,11.5,GREY,False)]],anchor=MSO_ANCHOR.MIDDLE,space=3)
    cx=0.85+lw+0.35; cw=12.48-cx
    tag="◀ CLICK TO PLAY · THE SHORT" if lead_vertical else "◀ CLICK TO PLAY · THE FILM"
    note=_enable_once(note)
    if band:
        card(cx,2.35,cw,1.45,VIOLET,tag,llab,lfact)
        card(cx,3.95,cw,1.45,TEAL,"ALSO IN THE NEWS",slab,sfact)
        y=5.55; rect(s,Inches(cx),Inches(y),Inches(cw),Inches(6.85-y),LIGHT); rect(s,Inches(cx),Inches(y),Inches(cw),Inches(0.07),AMBER)
        txt(s,Inches(cx+0.25),Inches(y+0.08),Inches(cw-0.4),Inches(6.85-y-0.1),[[("WHAT IT MEANS FOR YOU",9.5,AMBER,True)],[(band,12,INK,False)]],anchor=MSO_ANCHOR.MIDDLE,space=3)
    else:
        card(cx,2.35,cw,2.0,VIOLET,tag,llab,lfact)
        card(cx,4.5,cw,2.35,TEAL,"ALSO IN THE NEWS",slab,sfact)
    notes(s,note); footer(s); return s

def use_case_slides():
    big_numbers("AI has changed the economics of video",[
     ("US$2K","a national TV ad","Kalshi's NBA Finals spot: about US$2,000 and 15 clips cut from 300–400 generations (The Keyword)"),
     ("14 days","a 95-minute feature","Hell Grind: 15 people, under US$500K (CineD)"),
     ("45","credits a test take","one 15-second Seedance 2.5 Draft in Higgsfield, before you commit to 1080p")],
     kicker="TOPIC 1 · THE IMPACT OF AI ON VIDEO CREATION",sub="Budgets, crews and timelines that used to decide who could make video no longer do",
     band="The new bottleneck is direction: knowing what to ask for, judging the take, and fixing what fails. That is this course.",
     note="Sources on slide. Kalshi's view counts (30M+/100M) are the creator's own claims, so quote the cost and the airing.")
    compare_table("What AI changes at each stage of production",
     ["Stage","Before AI","With AI (in Higgsfield)"],
     [["Script & storyboard","Writer + storyboard artist, days","Supercomputer / AI Director, minutes; you review and edit"],
      ["Casting & locations","Auditions, permits, travel","Elements: cast, sets and props generated and saved"],
      ["The shoot","Crew, camera, lights, a day per scene","Cinema Studio takes: camera, lens, light set in the prompt"],
      ["Fixes & reshoots","Re-book cast and crew","Replace an object, regenerate one shot, upscale"],
      ["Sound & music","Composer, voice artist, studio","Native audio, generated soundtrack, consented voice"],
      ["New risks","—","Likeness, rights, disclosure, quality drift: K4 rules apply"]],
     kicker="TOPIC 1 · BEFORE AND AFTER",accent=VIOLET,
     note="Ask: which of these jobs disappears, and which becomes more valuable? (Direction, review, compliance.)")
    tile_grid("Five ways AI video already earns audiences",[
     ("AI movie","Hell Grind: a 95-minute Higgsfield feature, 15 people, 14 days (CineD)."),
     ("AI micro drama","Kling's Mountains & Seas premiered on Kuaishou on 13 Jul 2024: 52M+ views (Caixin)."),
     ("AI influencer","Aitana López, an AI model, earns up to €10,000 a month (Euronews)."),
     ("AI singer","Xania Monet: first AI act on a Billboard radio chart, No. 30 Adult R&B Airplay (Nov 2025)."),
     ("AI marketing","Kalshi's NBA Finals ad: about US$2,000, made with Google Veo 3 (The Keyword)."),
     ("Your turn","Lab 9 ends with your own 15-second ad, published or uploaded to the TMS.")],
     kicker="TOPIC 1 · USE CASES",cols=2,size=13,accent=VIOLET)
    yt_short_slide("AI movies: cinema-grade scenes from a prompt",
     ("1yLAbK5F3E8","The Most Insane AI Film You'll See Today (Seedance 2.5)","Video: Theoretically Media. A short film made with Seedance 2.5, the model you will use in Labs 1–9."),
     ("Hell Grind — Higgsfield Originals (2026)","95 minutes, under US$500K, 15 people, 14 days (CineD). Billed by Higgsfield as the first AI feature film."),
     kicker="USE CASE 1 · AI MOVIE",sub="Long-form stories need what Topic 2 teaches: Elements that keep every face and set consistent",
     lead_vertical=False,
     note="Slide Show: click the video to play (internet needed; click Enable Content on the yellow bar first). Hell Grind did not screen in the official Cannes programme; say so if asked.")
    yt_short_slide("AI micro dramas: one-minute episodes, no film set",
     ("opCFOkfX6YE","The Healer's Refusal — an AI-generated Chinese micro drama","A vertical, cliff-hanger episode made entirely with AI: the format built for TikTok and YouTube Shorts."),
     ("Mountains & Seas: Breaking Waves — Kling AI","Kuaishou's AI micro drama premiered 13 Jul 2024 and passed 52M views (Caixin)."),
     kicker="USE CASE 2 · AI MICRO DRAMA",sub="Short, serial, vertical stories: the format Lab 9's variation prompt practises",
     band="Two characters, one twist, 9:16. Save the cast as Elements so episode 2 looks like episode 1.")
    yt_short_slide("AI influencers: one face, posting every day",
     ("jZZJHrrlg04","Creating an AI influencer with Higgsfield AI Influencer Studio","A creator builds a consistent virtual influencer inside Higgsfield (Shafin Tech)."),
     ("Aitana López — BBC World Service report","An AI model earning up to €10,000 a month, about €3,000 on average (Euronews)."),
     kicker="USE CASE 3 · AI INFLUENCER",sub="Higgsfield's AI Influencer tool and a saved @char Element make the same face repeatable",
     band="Consistency is the product: a character sheet plus an @char Element. Disclose that the person is synthetic (K4).",
     note="Link to K4: TikTok and YouTube both ask creators to label realistic AI content.")
    yt_short_slide("AI singers: a voice, a song, a music video",
     ("Y7i1z6UGOnQ","Pretty Little Baby — an AI cover (Ai Music Sunny)","An AI singer covering Connie Francis's song: a fast-growing Shorts genre, and a live rights question."),
     ("Xania Monet — How Was I Supposed to Know?","First AI act on a Billboard radio chart: No. 30 on Adult R&B Airplay (Billboard, Nov 2025). Music made with Suno."),
     kicker="USE CASE 4 · AI SINGER",sub="Music video, voice and soundtrack: Lab 8 gives you all three inside Higgsfield",
     band="Covering someone else's song or voice needs the rights holder's permission. Original music and your own voice are safe ground.",
     note="Discussion (K4): is an AI cover of a real artist's song publishable? Who owns the voice? Tie to the Lab 8 consent form.")
    yt_short_slide("AI marketing: studio-quality ads in minutes",
     ("THplxezacD8","Higgsfield Marketing Studio — UGC ads in seconds","A creator makes UGC-style product ads in Higgsfield's Marketing Studio (AI Tech Pro)."),
     ("Kalshi NBA Finals ad — PJ Ace (2025)","About US$2,000; 300–400 generations cut to 15 clips with Google Veo 3; aired in Game 3 of the NBA Finals (The Keyword)."),
     kicker="USE CASE 5 · AI MARKETING",sub="The use case you will run end to end in Lab 9: one product photo to a published ad",
     band="Start from a clean product photo, keep the product identical in every shot, label the ad as AI-generated.",
     note="The SOLA ad in the Big Picture section was made the same way: one prompt, five shots, 240 credits at 1080p.")

def bp_intro():
    """Topic 1 opener: why AI video, two demo films, the pipeline."""
    big_statement("Two 15-second films. Two prompts. Zero cameras.",
     "Both clips on the next slides were made for this course in Higgsfield with Seedance 2.5, one prompt each, sound included. By the end of Day 2 you will direct your own.",
     "WHY THIS COURSE",color=BLUE,img="creator-desk.jpg",
     note="Image: generated with Higgsfield GPT Image 2.6 (medium, 1K, 0.5 credits). Prompt: modern video creator's desk at night, laptop with an editing timeline, storyboard notebook, terracotta lamp light, no text or logos.")
    video_slide(C.DEMO_VIDEOS[0],"MADE IN HIGGSFIELD · AI MARKETING",
     "A product ad with a hero packshot, written as five timed shots",
     note="Play it with sound. Point out: the bottle stays the same in every shot because the prompt names it in every shot; the beat hits on the packshot because the Sound line asked for it. Cost: 240 credits at 1080p; the same take as a 480p Draft costs 45.")
    video_slide(C.DEMO_VIDEOS[1],"MADE IN HIGGSFIELD · AI SCI-FI",
     "An epic scene with an establishing shot, a reveal and a payoff",
     note="Ask learners which shot sells the scale (the extreme wide at 11–15 s) and why the close-up comes before it (we see her awe before we see what she sees).")
    process_map("The Higgsfield Video Pipeline",C.PIPELINE,
     kicker="THE PROCESS YOU'LL RUN — EVERY LAB MAPS TO A STAGE",
     synthesis=("One platform, five stages",
      "You script and plan in Supercomputer (Topic 1), build Elements and direct takes in Cinema Studio (Topic 2), then fix, finish and publish (Topic 3)."))

def bp_studio():
    """Topic 1: the Higgsfield studio, sign-up, references and models (before Lab 1)."""
    shot_steps("Every tool you need sits on one home page",hf("002"),[
     ("Supercomputer","The agent: brief it in plain English, it plans, prompts and asks before it spends."),
     ("Seedance 2.5","ByteDance's video model: 4–30 s, up to 1080p, native sound, 50 references."),
     ("Cinema Studio 4.0","The director's chair: camera, lens, light, colour, genre."),
     ("Genjutsu","One upload, many versions: swap objects, copy motion."),
     ("Higgsfield in Claude & ChatGPT","The same studio through an MCP connector.")],
     kicker="HIGGSFIELD.AI · THE HOME PAGE",sub="Learn five tiles today and you can find everything else from them",
     marks=[(0.80,0.735),(0.59,0.735),(0.40,0.93),(0.43,0.735),(0.59,0.93)],
     note="Live demo: open higgsfield.ai, hover each tile. The top nav (Image, Video, Audio, Genjutsu, Shorts Studio, AI Influencer) holds the single-purpose tools; Supercomputer can call all of them.")
    link_slide("Sign up with the course link",C.HF_SIGNUP,C.HF_SIGNUP_SHORT,[
     ("Sign up",f"Open {C.HF_SIGNUP_SHORT} and create your account with Google or email."),
     ("Disclosure",C.HF_DISCLOSURE),
     ("Plan for the labs","Labs run on the website, which needs a paid plan. Plus: US$49/month or US$39 billed yearly for 1,000 credits (8 Nov 2026)."),
     ("Free trial terms","3 days, needs a card, renews to Plus unless cancelled within 3 days; trial credits worked only through the Higgsfield MCP, not the website (8 Nov 2026).")],
     kicker="SIGN-UP · BEFORE YOU START",sub="One link, one account: everything in this course happens inside it",
     note="Check every learner can see a credit balance before Lab 1. If the class uses trainer-provided accounts, hand them out here and skip sign-up.")
    tile_grid("Keep these three open beside the labs",[
     ("Higgsfield API docs","For automation: authentication, requests, polling, webhooks and model endpoints — docs.higgsfield.ai/docs"),
     ("Supercomputer and Skills","The agent, its Skills Marketplace and skill import from Claude, Claude Code, Codex and ChatGPT — higgsfield.ai/supercomputer-intro"),
     ("Course labs","Every prompt on one copy page (labs/prompts.html), plus instruction PDFs and mock assets for Labs 1–10 — labs/index.html")],
     kicker="HIGGSFIELD · REFERENCES",cols=1,size=14,
     note="Trainer prep (not for learners, house rule: Shorts only): 'Higgsfield AI Tutorial for Beginners (2026) | Step-by-Step' by Metics Media, youtube.com/watch?v=Mt91SiQotOU — a good walkthrough of the UI to rehearse before class.")
    compare_table("The models inside Higgsfield",
     ["Model","Made by","Best for","Length · quality"],
     [["Seedance 2.5","ByteDance","General video, native sound, 50 references","4–30 s · up to 1080p"],
      ["Seedance 2.5 Draft","ByteDance","Cheap test takes you finalise later","4–30 s · 480p"],
      ["Cinema Studio 4.0","Higgsfield","Camera, lens, light and genre control","next-gen cinematic"],
      ["Kling 4.0 / Flash","Kuaishou","Motion quality, multi-shot","3–30 s · 1080p"],
      ["Higgsfield Genjutsu","Higgsfield","Replace objects, copy motion, many versions","4–30 s · 1080p"]],
     kicker="WHAT THE PICKER SHOWS · NOV 2026",accent=BLUE,
     note="Pick per shot, not per project: Draft to explore, Seedance 2.5 to finish, Genjutsu to fix.")
    shot_pair("Two menus, one decision: which engine shoots this take?",
     (hf("007"),"Cinema Studio versions","4.0 is the next-gen cinematic model; 3.5 added camera selection, style presets and AI Director; 3.0 added speed ramps; 2.5 moves the camera from a start frame."),
     (hf("008"),"The video model list","Seedance 2.5 (TOP) and its 480p Draft, Genjutsu and Genjutsu Lite, Kling 4.0 and the new 4.0 Flash, each with its resolution and 3–30 s range."),
     kicker="MODELS · WHERE TO CHOOSE",sub="You will compare two of these on the same prompt in Lab 9")

# ---------------- TOPICS + ACTIVITIES ----------------
TOPIC_ACTS={t["num"]:[a for a in ACTIVITIES if a["topic"]==t["num"]] for t in C.TOPICS}
CARD_COLORS=[BLUE,TEAL,VIOLET]

def lab_concepts(lab):
    """Knowledge → lab: the concept slides each lab applies, shown directly before that lab."""
    if lab==1:
        bp_intro()
        use_case_slides()
        bp_studio()
        shot_steps("Type one line, get fifteen seconds of film",hf("009c"),[
         ("Describe the scene","Plain English in the prompt box; @ adds a saved character or location."),
         ("Pick the model","Seedance 2.5 here; switch to Draft for cheap tests."),
         ("Set quality and length","720p and 15 s cost 105 credits; 1080p costs 240."),
         ("Generate","Credits are shown on the button before you press it.")],
         kicker="CINEMA STUDIO · VIDEO",sub="The fastest route from idea to clip, and the one Lab 1 starts with",
         marks=[(0.52,0.60),(0.23,0.75),(0.42,0.75),(0.84,0.70)])
        shot_pair("A lazy prompt works, but the model makes your choices",
         (hf("011"),"Format + vibe","'15-second video' + 'epic sci-fi scene' is enough to generate. That is the lazy prompt you type first in Lab 1."),
         (hf("012"),"What you leave out, the model decides","Character, world/location and camera all become the model's guess, so every take tells a different story."),
         kicker="THE LAZY PROMPT",sub="Speed now, inconsistency later: know the trade before you press Generate",
         note="Run the lazy prompt live on Draft (45 credits). Ask the room to name what the model chose for them.")
        video_slide(C.LAZY_TEST,"LAB 1 PREVIEW · TESTED IN HIGGSFIELD",
         "Same prompt you will type in Lab 1. No character, no plot: proof that unbriefed means undirected",
         note="Rendered for this course on 9 Nov 2026 as a Seedance 2.5 Draft (45 credits). Learners' takes will differ: that variation is the point.")
        shot_steps("Supercomputer asks before it spends a credit",hf("014c"),[
         ("The prompt it wrote","Read the scene, shots and grade it built from your chat."),
         ("The settings","Model, ratio, length, resolution and quality, all editable."),
         ("Approve with the price","240 credits for 15 s at 1080p; switch to Draft first."),
         ("Leave 'Always allow' off","Approve each spend by hand in class.")],
         kicker="SUPERCOMPUTER · THE APPROVAL CARD",sub="An agent with a budget gate: you stay the producer",
         marks=[(0.25,0.80),(0.25,0.89),(0.85,0.96),(0.58,0.96)],
         note="Supercomputer is Higgsfield's agent ('powered by Opus 5.5' on the home tile). It can call every Higgsfield tool; the approval card is where a human stays in charge.")
        tile_grid("Six defects every AI video can have (K1)",[
         ("Identity drift","The hero's face, hair or clothes change between shots."),
         ("Prop teleport","The case swaps hands or vanishes mid-scene."),
         ("Broken physics","Hands merge, liquids melt, people walk through tables."),
         ("Audio mismatch","Footsteps without feet, lips out of sync, music over dialogue."),
         ("Garbled text","Signs and labels turn into nonsense letters."),
         ("Wrong spec","Wrong ratio, 480p left in the final, cut mid-movement.")],
         kicker="K1 · TYPES OF QUALITY ISSUES",cols=2,size=13,accent=AMBER)
    if lab==2:
        shot_hero("Brief like a director: who, where, what happens",hf("015"),[
         ("WHO","One character with a job and a look: 'a bartender'."),
         ("WHERE","One location you could photograph: 'an empty bar'."),
         ("WHAT HAPPENS","One visible action with an ending: 'lights off, walk to the window'.")],
         kicker="SCRIPT · THE THREE-LINE BRIEF",sub="Three lines remove the three guesses the lazy prompt left to the model",img_h=2.4)
        shot_pair("Talk the scene through, then refine one change at a time",
         (hf("016"),"Start → talk → draft","New chat, your idea (and a photo if you have one), let it ask questions, answer, read its prompt, generate the draft."),
         (hf("017"),"Refine & save","Describe ONE change, read the updated prompt, keep the take that works. One change per run tells you what fixed it."),
         kicker="SUPERCOMPUTER · THE WORKING LOOP",sub="The loop you will repeat in every lab from here on")
        shot_steps("AI Director turns a brief into a script and storyboard",hf("040"),[
         ("Project brief","Where the locked script and shot list live."),
         ("Elements","The characters, locations and props this project can call."),
         ("AI Director","Opens the director chat inside the project."),
         ("Suggested starts","'Write a script', 'Generate an 8-shot storyboard', '15-second perfume commercial'.")],
         kicker="PROJECTS · AI DIRECTOR",sub="Your writers' room lives inside the project, next to the footage",
         marks=[(0.07,0.14),(0.05,0.25),(0.06,0.47),(0.87,0.52)])
        tile_grid("Good Story Elements",[
         ("Identifiable hero","A protagonist the audience recognises themselves in."),
         ("A clear desire","What does the hero want? Ambiguity kills engagement."),
         ("A real obstacle","No obstacle, no story: conflict is the heart of drama."),
         ("Action & outcome","The hero acts; the world changes. Show the transformation."),
         ("Resolution","End the story world in a new state, with your call to action."),
         ("The story spine","Once upon a time… then one day… but… so… until finally…")],
         kicker="A1 · REVIEW THE SCRIPT BEFORE YOU SHOOT",cols=2,size=13)
        process_map("Build every prompt in three parts",[
         ("Scene context","visible action, 1–2 sentences"),
         ("References","@elements and their roles"),
         ("Shots","numbered, timed, sized"),
         ("Sound","ambience, foley, dialogue"),
         ("Settings","model, ratio, length, Draft")],
         kicker="THE HIGGSFIELD PROMPT FORMAT",color=VIOLET,
         synthesis=("Write it like a call sheet","Every shot names a size, an action and a camera. The model stops guessing and starts following."))
        shot_pair("Ready-made presets and skills do the heavy lifting",
         (hf("013"),"A preset packs scene, camera, light and sound","Pick one and the model receives a full brief. Good for speed; you still check it fits your story."),
         (hf("023"),"Skills: rules for a specific job","Type / in Supercomputer: Katana, Visual Studio, Cinematic Director, Brand Asset Creation, Video Motion Graphics Editor, /youtube-script."),
         kicker="SHORTCUTS · PRESETS AND SKILLS",sub="Lab 2 uses /youtube-script; Lab 9 uses /product-photoshoot")
        tile_grid("Add a skill to Supercomputer: three ways",[
         ("Install from the Marketplace","Skills in the left sidebar → browse official and community skills → Install. Higgsfield calls Skills 'installable workflows'."),
         ("Import what you already have","Bring your skills and memory from Claude, Claude Code, Codex or ChatGPT (the import uses the Higgsfield MCP connection)."),
         ("Create your own","A skill is rules + guidelines for one job: when to use it, the steps, the style rules, the output format."),
         ("Run it with a slash","Type / in the Supercomputer prompt and pick the skill: /youtube-script, /product-photoshoot, /house-standards.")],
         kicker="SUPERCOMPUTER · SKILLS",cols=2,size=13,
         note="Sources: higgsfield.ai/supercomputer-intro (Skills = installable workflows from the Marketplace; import from Claude, Claude Code, Codex, ChatGPT). Confirm the exact Create/Import button labels on your own account before class; the UI changes often.")
    if lab==3:
        compare_table("Tailoring the cut to the platform",
         ["","YouTube","TikTok / Shorts","Instagram Reels"],
         [["Length","60 s – 10 min","15 – 60 s","15 – 90 s"],
          ["Ratio","16:9 landscape","9:16 vertical","9:16 vertical"],
          ["Pacing","Build with structure","Hook in 1–3 s, fast cuts","Aesthetic-first, fast"],
          ["Captions","Recommended","Essential (muted viewing)","Essential"],
          ["AI label","Disclose realistic AI content","AI-generated label","Label AI content"]],
         kicker="ONE SCENE ≠ EVERY PLATFORM",accent=VIOLET,
         note="Higgsfield's Reframe turns a 16:9 take into 9:16; plan the safe area when you write the shots.")
        big_numbers("Draft first: the cheapest quality gate you have",[
         ("45","credits","a 15 s Seedance 2.5 Draft at 480p"),
         ("240","credits","the same 15 s at 1080p, 5× the price"),
         ("7","days","to finalise any Draft you keep at 1080p")],
         kicker="A3 · BUDGET THE WORK PLAN IN CREDITS",sub="Read on Higgsfield, 9 Nov 2026: put these numbers in your Lab 3 work plan",
         band="Rule for every lab: test the idea on Draft, finalise only the take you would show a client.")
        compare_table("Turn your standards sheet into a skill",
         ["Part of the skill","What you write","Example: /house-standards"],
         [["Name","short, lower-case, hyphenated","house-standards"],
          ["When to use","the job it does","Every video for our agency's clients"],
          ["Rules","the non-negotiables","Saved Elements only; 1080p finals; AI label on; no real likeness without consent"],
          ["Steps","the order of work","Draft 480p → review → finalise 1080p → checklist → export 16:9 + 9:16"],
          ["Output format","what it must hand back","Prompt in three parts + a credit estimate + a pass/fail checklist"]],
         kicker="LAB 3 PREVIEW · CREATE YOUR OWN SKILL",accent=TEAL,
         note="A skill turns a one-off standards document into a rule the agent follows on every job: the A2 standards become enforced, not just written.")
    if lab==4:
        shot_pair("Cast your lead before you shoot a frame",
         (hf("038"),"Ask Supercomputer to cast","'Main character in a biker road movie, 25, modern clothing'. It loads the character-sheet skill and writes a casting prompt for Soul 2.0."),
         (hf("039"),"Choose from five options","Five photoreal candidates. You pick one; only then does it build the reference sheet."),
         kicker="ELEMENTS · CHARACTERS",sub="A cast you chose on purpose beats a face the model invents every take",img_h=3.4)
        shot_hero("One sheet, three views: the reference every shot obeys",hf("041"),[
         ("Full body, front","Clothes, shoes, proportions."),
         ("Full body, back","What the camera sees when he walks away."),
         ("Face portrait","The identity every shot copies. Next: make it the only face on the sheet.")],
         kicker="ELEMENTS · CHARACTER SHEET",sub="Plain background, consistent light: the model copies exactly what it sees",img_h=3.0)
        shot_pair("Cover one face, keep one face: the trick that locks identity",
         (hf("042"),"Blank the full-body face","The white oval is deliberate. The small, soft face in the full-body view is hidden, so the model copies the sharp close-up into every shot."),
         (hf("043"),"Same trick for the friend","His full-body face is covered too. Each character has exactly one face to copy, so two people share a shot without swapping faces."),
         kicker="ELEMENTS · CONSISTENCY",sub="Two faces on one sheet means two identities to blend; leave the model only one (K2)",
         note="The covered face is not a defect. Higgsfield's character-sheet skill hides the face on the full-body view so the close-up portrait is the only face reference, which keeps the face identical from shot to shot. Outfit and body still come from the full-body views.")
        shot_pair("Edit one detail and keep it in every view",
         (hf("044"),"A targeted edit","'Give him a silver wallet chain… white ribbed tank top, same in all views.' Seedream 5.0 Pro, 3 credits."),
         (hf("045"),"Different models, different casts","Soul 2.0, Seedream 5.0 Pro and Nano Banana Pro each read the same brief their own way."),
         kicker="ELEMENTS · REFINE THE CHARACTER",sub="Fix wardrobe on the sheet, not shot by shot")
        shot_hero("Build locations with anchors you can name in a shot",hf("046"),[
         ("Spatial anchors","The counter, the stools, the pool table, the window: things a shot can point at."),
         ("People optional","Extras give scale; your saved characters will replace them."),
         ("Save it","loc_bar-interior becomes @loc_bar-interior in every prompt.")],
         kicker="ELEMENTS · LOCATIONS",sub="'He sits on the third stool' only works if the stool exists in the reference",img_h=3.0)
        shot_hero("A prop on four models: compare before you commit",hf("047"),[
         ("Same prompt","A slim orange hard-shell briefcase, white background, no logos."),
         ("Different cost","Nano Banana Pro 2 credits, GPT Image Sunburst 3, Seedream 5.0 Pro 3, Soul Cinema 0.125."),
         ("Pick on fit","Shape, colour and detail that survive a close-up.")],
         kicker="ELEMENTS · PROPS",sub="The cheapest image is not always the cheapest choice: a wrong prop costs a re-shoot",img_h=3.0)
        shot_pair("Save once, reuse by name",
         (hf("048"),"@char_biker in every prompt","One saved Element, one reference attached automatically, prompt after prompt."),
         (hf("049"),"The Element form","Category (Character, Location, Prop), Name, Element ID such as char_biker, description and custom properties."),
         kicker="ELEMENTS · SAVE AS ELEMENT",sub="Naming rule: char_, loc_, prop_ + a short slug, so the whole crew finds it")
        shot_hero("Five saved Elements: your cast, sets and props",hf("050"),[
         ("Characters","@char_biker, @char_friend"),
         ("Locations","@loc_bar-interior, @loc_bar-entrance"),
         ("Prop","@prop_suitcase, ready for every shot")],
         kicker="ELEMENTS · THE FINISH LINE",sub="What your My elements page should show at the end of the Elements lab",img_h=3.0)
        shot_pair("Pick the image model for the job",
         (hf("034"),"Four image models","Soul 2.0 for people, Soul Cinema for film stills, GPT Image Sunburst for scenes, Nano Banana Pro for detailed places."),
         (hf("037"),"Two ways to generate","Text to image from a prompt, or image to image from a single picture to make variations."),
         kicker="IMAGES · MODELS AND MODES",sub="Elements start as images, so the image model decides the look of your film")
        shot_pair("Tested for this course: the Elements prompts work as written",
         (os.path.join(VID,"lab4-test-bar.jpg"),"Location prompt → the bar","Counter on the right, eight stools, pool table at the back, window on the left: every spatial anchor the prompt named. About 2 credits."),
         (os.path.join(VID,"lab4-test-case.jpg"),"Prop prompt → the case","Slim orange ribbed lid, black handle, two metal latches, white background, no logos. About 2 credits."),
         kicker="LAB 4 PREVIEW · TESTED IN HIGGSFIELD",sub="Name what the shot must contain and the image model delivers it",
         note="Generated 9 Nov 2026 with the exact Lab 4 prompts. The same images ship in labs/lab-04…/assets as samples.")
    if lab==5:
        shot_hero("Each reference gets a job: character, location, camera, voice",hf("051"),[
         ("Face / image → Character","Who appears, exactly as shown."),
         ("Place / image → Location · video → Camera move","Where it happens, and how the camera travels."),
         ("Audio → Voice","What the character sounds like.")],
         kicker="REFERENCES · ROLES",sub="A reference without a role is a suggestion; with a role it is an instruction",img_h=3.1)
        big_numbers("Up to fifty references in one generation",[
         ("30","images","faces, outfits, products, places"),
         ("10","videos","camera moves and motion to copy"),
         ("10","audio files","voices, music, sound to match")],
         kicker="REFERENCES · SEEDANCE 2.5 LIMITS",sub="More references, fewer guesses",
         band="What each image carries: a person = face + clothes; a prop = shape + colour + details; a place = space + light + colour.")
        shot_steps("Cinema Studio: every control a film crew has",hf("036"),[
         ("References 0/50","Attach Elements, images, video and audio."),
         ("Film setup · Camera","Camera body, lens and aperture."),
         ("Colour palette · Lighting","The grade and the light scheme."),
         ("Describe your scene","Type @ to drop in a saved character or location."),
         ("Model and settings","Cinema Studio 4.0, 1080p, 16:9, 5 s, sound, 1–4 takes; 80 credits.")],
         kicker="CINEMA STUDIO · THE PANEL",sub="Set the look once, then every take inherits it",
         marks=[(0.38,0.50),(0.54,0.50),(0.76,0.50),(0.49,0.58),(0.47,0.66)])
        shot_pair("Set the camera and the light like a DP",
         (hf("005"),"Camera, lens, aperture, movement","DV Camcorder to Modern; Halation Vintage to Clean Sharp; f/11 deep focus to f/1.4 wide open."),
         (hf("003"),"Lighting presets","Auto, Silhouette, Practicals, Window, Overhead fall, or place your own lights."),
         kicker="CINEMATIC EFFECTS · CAMERA + LIGHT",sub="Shallow focus and practical lamps make the bar feel real at night")
        shot_pair("Grade the colour and set the genre",
         (hf("004"),"Colour palette","Lime Jam, Black gloss, Film colors, Nostalgic blue, Candy pink, Soft palette, Static Noon, or build your own."),
         (hf("006"),"Genre, era, tempo","The story conventions the model should follow, the period, and the cutting pace."),
         kicker="CINEMATIC EFFECTS · COLOUR + GENRE",sub="A grade and a genre tell the model the mood in two clicks")
        shot_hero("One continuous shot or a multishot with cuts",hf("053"),[
         ("One continuous shot","'Follow a man along a busy sidewalk… frontal view at the corner… no cuts.' Good for immersion."),
         ("Multishot · cuts","'15 seconds, six shots, a cut between each': feet, hand, pedestrian pass, profile, kerb, corner."),
         ("Seedance range","4–30 seconds per generation; you choose the structure in the prompt.")],
         kicker="SHOTS · STRUCTURE",sub="Decide the structure before the words: it changes every line you write",img_h=3.0)
        shot_pair("Write the three parts, then attach the references",
         (hf("056"),"Context, references, shots","01 scene context in 1–2 sentences; 02 references and their roles; 03 the shots that describe the action."),
         (hf("057"),"A real prompt with @handles","@char_biker, @char_friend and @prop_suitcase each '100% as shown', with who holds what and where they sit."),
         kicker="SHOTS · THE PROMPT",sub="Lab 5 gives you this exact bar-scene prompt to adapt")
        shot_hero("Choose the shot size for what the audience must read",hf("058"),[
         ("Wide","Character and surroundings: where are we?"),
         ("Medium close-up","Expression and upper-body action: what are they doing?"),
         ("Close-up","A face, a reaction or an important detail: what do they feel?")],
         kicker="SHOTS · SIZE",sub="Every numbered shot in your prompt starts with one of these three words",img_h=3.1)
        shot_gallery("Write each shot as size + purpose + camera",[
         (hf("059_0"),"CLOSE-UP · recognition, exit frame"),
         (hf("059_1"),"CUT TO THE FRIEND · shot 2, 5–8 s, medium, static"),
         (hf("059_2"),"BEHIND THE COUNTER · left hand, dialogue in the action")],
         kicker="SHOTS · ANNOTATED",sub="Three shot cards from the bar scene: copy the pattern into your shot list",
         band="Pattern: SHOT n · time · size · camera · action · the line or sound that lands in it.",img_h=2.95)
        shot_pair("Compose the frame, then write what we hear",
         (hf("060"),"Rule of thirds","Eyes on the upper third, the subject off-centre, space in the direction he looks."),
         (hf("061"),"Sound is part of the prompt","Bar ambience, footsteps, clothing movement, dialogue already written in shot 4. Seedance renders it with the picture."),
         kicker="TAKES · COMPOSITION AND SOUND",sub="Two lines in the prompt that separate a clip from a scene")
        shot_steps("Draft mode: four test takes for the price of one final",hf("062"),[
         ("References attached","Characters, prop and both bar locations."),
         ("Three-part prompt","Scene context, references with roles, shots."),
         ("Seedance 2.5 Draft","480p, 21:9, 16 s, 4 takes, sound on."),
         ("Generate Draft","About 45 credits a take for 15 s; review before you spend more.")],
         kicker="SHOTS & TAKES · DRAFT MODE",sub="Explore at 480p, commit at 1080p",
         marks=[(0.18,0.44),(0.41,0.60),(0.21,0.87),(0.83,0.81)])
        shot_pair("Test four ideas, finalise one",
         (hf("063"),"Four 480p Drafts","Same prompt, four takes. Compare the walk, the case and the light."),
         (hf("064"),"Generate the keeper in 1080p","The selected Draft is re-rendered at full resolution: same take, full quality."),
         kicker="SHOTS & TAKES · DRAFT → FINAL",sub="Drafts can be finalised within seven days")
    if lab==6:
        shot_pair("Keep a useful first take, then direct the next one",
         (hf("066"),"Before you refine","Watch with sound, choose ONE change or a variation, save the prompt and the take so you can compare."),
         (hf("068"),"Direct the next take","Change one instruction, generate one take, compare, choose. Keep both prompts and clips."),
         kicker="TAKES · THE DIRECTOR'S LOOP",sub="A take is a decision you can undo; a deleted take is a lesson lost")
        shot_hero("Continuity: check the prop through the whole scene",hf("067"),[
         ("Where?","Its position in each shot."),
         ("Who holds it?","The right character, the right hand."),
         ("Same?","Colour, shape and size from shot to shot.")],
         kicker="A5 · ASSESS THE FOOTAGE",sub="Prop teleport is the defect viewers spot first",img_h=2.6)
        compare_table("Quality issues → the Higgsfield fix",
         ["Issue (K1)","Typical cause","Fix in Higgsfield (K2)"],
         [["Face changes between shots","No character reference","Character Element + sheet"],
          ["Set changes between shots","No location reference","Location Element with anchors"],
          ["Prop swaps hands or vanishes","Holder not stated","'@prop… belongs to @char…, left hand'"],
          ["Wrong object in the shot","Model guessed","Genjutsu Replace Object"],
          ["Soft, low-res final","480p Draft exported","Finalise at 1080p or Upscale"],
          ["Wrong ratio for TikTok","16:9 master only","Reframe to 9:16"]],
         kicker="K1 → K2 · THE WA ASKS EXACTLY THIS",accent=TEAL,
         note="Every issue on the left appears in the Written Assessment: know the matching fix.")
        tile_grid("Parameters to assess AI video quality (K3)",[
         ("Resolution & sharpness","1080p minimum for social; no 480p Draft in the final."),
         ("Motion & physics","No melting hands, sliding feet or stutter at cuts."),
         ("Continuity","Faces, clothes, props and sets match shot to shot."),
         ("Audio","Dialogue clear above music; foley matches the action."),
         ("Captions & pacing","Accurate, in sync, readable; cuts on the beat."),
         ("Compliance","Platform specs, AI label, consent, rights.")],
         kicker="K3 · SCORE EVERY CUT BEFORE EXPORT",cols=2,size=13)
    if lab==7:
        compare_table("Remedial actions: from FAIL to fixed",
         ["Fails the check","Remedial action (A6)","Higgsfield tool"],
         [["Wrong or drifting object","Swap it, keep the motion","Genjutsu Replace Object"],
          ["One broken shot","Regenerate that shot only, same Elements","Cinema Studio"],
          ["Soft or 480p footage","Upscale or finalise the Draft","Upscale · Seedance 2.5"],
          ["16:9 only, TikTok needs 9:16","Reframe with a safe area","Reframe"],
          ["Muddy or wrong sound","Rewrite the Sound line, regenerate","Seedance native audio"],
          ["No AI label / no consent","Add label, record consent","Publish settings"]],
         kicker="A6 · REMEDIAL ACTIONS",accent=AMBER,
         note="Order fixes cheapest first: a sound-line rewrite on Draft costs 45 credits; a full 1080p re-shoot costs 240.")
        shot_steps("Remove or replace an object without re-shooting",hf("019"),[
         ("Attach the shot","Drop the image or clip into Supercomputer."),
         ("Say what changes","'Remove the table and put the glasses on a plinth.'"),
         ("Keep everything else","Light, angle and the object itself stay as they were.")],
         kicker="REMOVE OBJECTS FROM A SCENE",sub="For video, Genjutsu Replace Object does the same while keeping the motion",img_w=7.6)
        tile_grid("Industry standards & responsible AI (K4)",[
         ("Platform specs","Resolution, ratio, duration and loudness per platform."),
         ("Commercial rights","Check your Higgsfield plan covers client work."),
         ("Consent & PDPA","Permission for real faces and voices; clone only with consent."),
         ("AI disclosure","TikTok's AI-generated label; YouTube's altered or synthetic content setting."),
         ("Advertising codes","IMDA and ASAS rules apply to AI ads too."),
         ("Accuracy","No invented product claims; fact-check every line.")],
         kicker="COMPLY BEFORE YOU PUBLISH",cols=2,size=13,accent=AMBER)
    if lab==8:
        tile_grid("Voice, music and effects: three vendors become three prompts",[
         ("Native sound","Seedance 2.5 renders ambience, foley and dialogue with the picture."),
         ("Soundtrack","Higgsfield Audio composes a track from genre, tempo and mood."),
         ("Your voice","Create Voice from a clean sample: only with consent."),
         ("Cinematic effects","Lighting presets, colour grades and effect presets on any shot."),
         ("Enhance","Upscale to 1080p or 4K; reframe for vertical."),
         ("Publish","Connect TikTok and post from Higgsfield, or export MP4.")],
         kicker="K5 · TECHNOLOGIES THAT SPEED UP THE EDIT",cols=2,size=13)
        compare_table("Evaluating a new AI technology (A7)",
         ["Criterion","Ask","Red flag"],
         [["Quality","Does output meet your standards sheet?","Drift, artefacts, robotic voice"],
          ["Speed & cost","Minutes and credits per finished 15 s?","Credits burn faster than value"],
          ["Control","Can you direct and iterate the result?","Black box, no editing"],
          ["Rights","Commercial use on your plan?","Licence excludes client work"],
          ["Fit","Works inside your Higgsfield pipeline?","New silo, manual re-export"]],
         kicker="A REPEATABLE EVALUATION RUBRIC",accent=VIOLET,
         note="Labs 8 and 9 use this rubric: rate voice, music and effects, then two video models on the same prompt.")
    if lab==9:
        shot_hero("Start every product video from a clean product reference",hf("018"),[
         ("Full object","The whole product in frame, nothing cropped."),
         ("Clear light","Even light, no hard shadows hiding the shape."),
         ("Visible edges","A plain background so the outline is unmistakable.")],
         kicker="AI MARKETING · PRODUCT REFERENCE",sub="The model can only keep what it can see",img_h=3.0)
        shot_pair("Check the product survives generation",
         (hf("020"),"Original vs generated","Compare the outline, the bridge and the frame. If a detail changed in a still, it will change in video."),
         (hf("021"),"One photo becomes a campaign","Photo shoot, creator video and commercial, all from one product photo plus a character and a location."),
         kicker="AI MARKETING · PRODUCT FIDELITY",sub="Approve the product in stills before you spend on video")
        shot_pair("Cast a model and scout three locations",
         (hf("025"),"One person, different views","Full body and face on one 16:9 sheet: the creator for every shot."),
         (hf("028"),"Round 3 of the location scout","Generate, compare, tweak the prompt, run it again until three streets feel right."),
         kicker="AI MARKETING · CAST AND SCOUT",sub="The same Elements workflow as Lab 4, pointed at a product")
        shot_pair("Run the photoshoot skill, get the stills",
         (hf("030"),"/product-photoshoot","'Six photos: three with her and three of just the glasses. Make them vertical, 9:16.'"),
         (hf("031"),"Product close-ups","The product placed in each scouted location, light matched to the scene."),
         kicker="AI MARKETING · CAMPAIGN STILLS",sub="Lab 9 runs this on the SOLA bottle")
        shot_pair("Three references in, a viral reel out",
         (hf("033"),"Character sheet + product photo + street image","The three references every shot of the reel inherits."),
         (hf("035"),"One instruction to Supercomputer","'Generate a video in Cinema Studio using these images. Create a viral cinematic reels sunglasses commercial.'"),
         kicker="AI MARKETING · FROM STILLS TO VIDEO",sub="Supercomputer writes the shots; you approve the spend")
    if lab==10:
        process_map("Mini capstone: your video, start to finish",[
         ("Brief","use case + who/where/what"),
         ("Elements","cast, set, product"),
         ("Draft takes","2+ at 480p"),
         ("Final + score","1080p, 7 parameters"),
         ("Fix + publish","2 fixes, AI label")],
         kicker="LAB 10 · PREVIEW · MINI CAPSTONE",color=TEAL,
         synthesis=("The rehearsal for PP Task 3","Same evidence as the assessment: screenshots of your prompt, takes and fixes, a scorecard, and the MP4 you upload to the TMS. Budget: 500 credits."))
        compare_table("What a strong capstone looks like",
         ["Check","Competent looks like","Watch out for"],
         [["Story","One clear who / where / what happens in 15 s","Three ideas crammed into one clip"],
          ["Consistency","Saved Elements in every shot","Faces or products that change"],
          ["Process","Draft takes before one 1080p final","Spending 240 credits per experiment"],
          ["Quality","Scorecard before and after, two named fixes","'Looks fine' with no evidence"],
          ["Compliance","Ratio per platform, AI label, no real likeness","Unlicensed logos or music"]],
         kicker="LAB 10 · SCORECARD",accent=TEAL,
         note="Walk the room during the capstone: check every learner has two Draft takes before they finalise, and that the checklist matches PP Task 3.")

def lab_flow(a):
    """The lab's 5-stage process map from its explicit `flow` labels (no step-by-step)."""
    stages=[(t,"") for t in a["flow"]]
    process_map(f"How Lab {a['num']} Runs",stages,
        kicker=f"LAB {a['num']} · HOW IT RUNS — FULL STEPS IN THE LEARNER GUIDE",
        color=TEAL,animate=False)

for t in C.TOPICS:
    section(f"TOPIC {int(t['code'])}",t["title"],t["code"],t["subtitle"],
            items=[f"Lab {a['num']} — {a['title']}" for a in TOPIC_ACTS[t["num"]]])
    tile_grid(f"Key Concepts — Topic {int(t['code'])}",t["concepts"],
              kicker=f"COVERS {t['weighting']}",cols=2,size=13)
    acts=TOPIC_ACTS[t["num"]]
    cards=[]
    for gi,a in enumerate(acts):
        cards.append((CARD_COLORS[gi%3],f"Lab {a['num']}",[a["title"],a["build"]]))
    # 4 labs → tile grid instead of cards3
    tile_grid(f"Hands-On Labs — Topic {int(t['code'])}",
        [(f"Lab {a['num']} — {a['title']}",a["build"]) for a in acts],
        kicker="WHAT YOU'LL DO",cols=1,size=13,icons=[str(a["num"]) for a in acts])
    for a in acts:
        lab_concepts(a["num"])
        activity_overview(f"LAB {a['num']}",a["title"],a["desc"],a["build"],a["services"],
                          kicker=f"TOPIC {t['code']} · HANDS-ON",objective=a["objective"])
        lab_flow(a)
        # prompts: paginate so a slide never carries >2 prompts or >900 chars
        pgs=[]; cur=[]; cur_len=0
        for pr in a.get("prompts",[]):
            if cur and (len(cur)==2 or cur_len+len(pr[1])>900):
                pgs.append(cur); cur=[]; cur_len=0
            cur.append(pr); cur_len+=len(pr[1])
        if cur: pgs.append(cur)
        for pi,pg in enumerate(pgs,1):
            prompt_slide(f"Lab {a['num']}",pg,kicker=f"LAB {a['num']} · COPY-AND-ADAPT PROMPTS",
                         part=f"({pi}/{len(pgs)})" if len(pgs)>1 else None)
        test_slide(a["title"],a["test"],kicker=f"LAB {a['num']} · VERIFY")
    if t["num"]==3:
        big_statement("Just because you can generate it doesn't mean you should publish it.",
            "Seven ethical issues, nine real cases and one rule for each: the last stop before anything you make goes live.",
            "TOPIC 3 · ETHICS",img="ethics-face.jpg",
            note="Image: generated with Higgsfield GPT Image 2.6 (medium, 1K). Prompt: fictional face, photographic on one side, dissolving into a digital wireframe on the other, charcoal background, terracotta rim light, no text. Not a real person.")
        tile_grid("Core ethical issues in GenAI video",[(h,d) for h,d,_ in C.ETHICS],
            kicker="TOPIC 3 · ETHICS BEFORE YOU PUBLISH",cols=2,size=12,accent=RUST,
            note="Owner-supplied list (9 Nov 2026). Facilitate: ask each table to pick the issue most relevant to the video they made in Lab 10.")
        for part,rows in (("1/2",C.ETHICS_CASES[:5]),("2/2",C.ETHICS_CASES[5:])):
            compare_table(f"When it went wrong: real cases ({part})",
                ["Issue","Case","What happened"],
                [[i,c,w] for i,c,w,_ in rows],kicker="TOPIC 3 · LAWSUITS, DISPUTES AND RULINGS",accent=RUST,
                note="Sources (verified 9 Nov 2026): "+"; ".join(f"{c} — {src}" for _,c,_,src in rows))
        compare_table("Seven issues, seven rules for your own videos",
            ["Issue","Your rule in every Higgsfield project"],
            [[h,r] for h,_,r in C.ETHICS],kicker="TOPIC 3 · FROM ETHICS TO PRACTICE",accent=RUST,
            note="These rules sit on top of the K4 compliance checks: label AI content, clear consent and rights, follow platform and IMDA/ASAS codes.")
    tile_grid(f"Recap — {t['title']}",
            [(f"Lab {a['num']} — {a['title']}", "You built: "+a["build"]) for a in acts],
            kicker="TOPIC RECAP · WHAT YOU CAN NOW DO",cols=1,size=13,icons=[str(a["num"]) for a in acts])

# ---------------- CLOSE ----------------
section("WRAP-UP","Course Summary & Next Steps","")
process_map("The Pipeline You Now Own",C.PIPELINE,
 kicker="FROM PROMPT TO PUBLISHED — RECAP",
 synthesis=("Ten labs, one studio",
  "Script and plan (Labs 1–3) → Elements (Lab 4) → shots and takes (Lab 5) → cut and assess (Lab 6) → fix (Lab 7) → voice, music, effects (Lab 8) → a published ad (Lab 9) → your own video, start to finish (Lab 10)."),
 animate=False)
tile_grid("What You Achieved",[
 ("Scripts & shot lists","Supercomputer and AI Director turn three lines into a timed, reviewable shot list."),
 ("Standards & budgets","A standards sheet and a work plan priced in real Draft and 1080p credits."),
 ("Elements","Characters, locations and props saved once and reused by @handle."),
 ("Shots & takes","Cinema Studio controls, references with roles, Draft first, 1080p for the keeper."),
 ("Fix & finish","Replace, upscale, reframe, voice, music and cinematic effects."),
 ("Evaluate & publish","A rubric for every new model, and an ad that is labelled and live.")],
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
lms_courseware_slide()   # end-of-deck "Courseware & Assessment on the LMS" (wsq-slides order item 15)
tile_grid("Cert & TRAQOM Survey (Mandatory)",[
 "Complete the TRAQOM course feedback survey on the LMS — it is mandatory for WSQ funding.",
 "Your digital certificate is issued on the LMS after you are assessed Competent.",
 "Portal: https://lms-tms.tertiaryinfotech.com"],kicker="BEFORE YOU LEAVE")
tile_grid("Briefing for Assessment",[
 "Place phones and other materials under the table or on the floor.",
 "No photos or recording of assessment scripts.",
 "No discussion during the assessment.",
 "Paste PP screenshots in the boxes; upload videos to the TMS.",
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
big_statement("Thank You!","You can now take an idea to a published 15-second film in one studio: Higgsfield, with you as the director.","HAPPY CREATING",color=TEAL,img="directors-chair.jpg",
 note="Image: generated with Higgsfield GPT Image 2.6 (medium, 1K). Prompt: empty director's chair on a dark film stage under a warm spotlight, blank clapperboard, charcoal and terracotta, no text.")

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
