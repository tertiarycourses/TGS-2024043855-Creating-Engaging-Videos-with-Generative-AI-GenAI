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
BLUE=RGBColor(0x1F,0x6F,0xEB); TEAL=RGBColor(0x10,0xB9,0x81); AMBER=RGBColor(0xF5,0x9E,0x0B)
INK=RGBColor(0x16,0x1B,0x26); GREY=RGBColor(0x5B,0x63,0x72); LIGHT=RGBColor(0xF5,0xF8,0xFC)
WHITE=RGBColor(0xFF,0xFF,0xFF); LINE=RGBColor(0xE2,0xE8,0xF0); VIOLET=RGBColor(0x7C,0x3A,0xED)
DARKBG=RGBColor(0x0B,0x12,0x20); CODEBLUE=RGBColor(0x9C,0xDC,0xFE)

prs=Presentation(); prs.slide_width=Inches(13.333); prs.slide_height=Inches(7.5)
SW,SH=prs.slide_width,prs.slide_height
BLANK=prs.slide_layouts[6]

def slide(): return prs.slides.add_slide(BLANK)
def rect(s,x,y,w,h,color,line=None):
    sp=s.shapes.add_shape(1,x,y,w,h); sp.fill.solid(); sp.fill.fore_color.rgb=color
    if line is None: sp.line.fill.background()
    else: sp.line.color.rgb=line; sp.line.width=Pt(1)
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
            r.font.color.rgb=col; r.font.name="Arial"
    return tb
def bullets(s,x,y,w,h,items,size=18,color=INK,gap=10,mcolor=BLUE):
    tb=s.shapes.add_textbox(x,y,w,h); tf=tb.text_frame; tf.word_wrap=True
    for i,it in enumerate(items):
        p=tf.paragraphs[0] if i==0 else tf.add_paragraph(); p.space_after=Pt(gap)
        lvl=it[1] if isinstance(it,tuple) else 0
        text=it[0] if isinstance(it,tuple) else it
        r=p.add_run(); r.text=("•  " if lvl==0 else "–  ")+text
        r.font.size=Pt(size if lvl==0 else size-2); r.font.color.rgb=color if lvl==0 else GREY
        r.font.name="Arial"; r.font.bold=(lvl==0 and isinstance(it,tuple) and len(it)>2 and it[2])
    return tb

# ---------------- v2 helpers: transitions, connectors, shapes ----------------
def _transition(s, kind="fade", speed="med"):
    sld=s._element
    for old in sld.findall(qn("p:transition")): sld.remove(old)
    tr=etree.SubElement(sld,qn("p:transition")); tr.set("spd",speed); tr.set("advClick","1")
    if kind=="fade": etree.SubElement(tr,qn("p:fade"))
    elif kind=="push":
        el=etree.SubElement(tr,qn("p:push")); el.set("dir","l")
    sld.append(tr); return tr

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
    r.font.color.rgb=color; r.font.name="Arial"
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
def footer(s):
    PAGE["n"]+=1
    txt(s,Inches(0.4),Inches(7.05),Inches(7.5),Inches(0.35),
        [[(f"{C.SHORT_TITLE}  ·  {C.COURSE_CODE}",9,GREY,False)]])
    txt(s,Inches(5.0),Inches(7.05),Inches(3.3),Inches(0.35),
        [[("© 2026 Tertiary Infotech Academy Pte Ltd",9,GREY,False)]],align=PP_ALIGN.CENTER)
    txt(s,Inches(12.4),Inches(7.05),Inches(0.6),Inches(0.35),
        [[(str(PAGE["n"]),9,GREY,False)]],align=PP_ALIGN.RIGHT)
def head(s,title,kicker=None,kcolor=BLUE):
    rect(s,0,0,SW,SH,WHITE); rect(s,0,0,Inches(0.28),Inches(1.55),kcolor)
    if kicker: txt(s,Inches(0.85),Inches(0.5),Inches(11.6),Inches(0.4),[[(kicker,14,kcolor,True)]])
    txt(s,Inches(0.85),Inches(0.88),Inches(11.9),Inches(0.78),
        [[(title,_fit_title(title),INK,True)]],anchor=MSO_ANCHOR.MIDDLE)
    rect(s,Inches(0.85),Inches(1.7),Inches(11.63),Inches(0.02),LINE)
    return s
def _logo(name):
    p=os.path.join(ASSETS,name)
    return p if os.path.exists(p) else None

# ---------------- slide templates ----------------
def cover():
    s=slide(); rect(s,0,0,SW,SH,WHITE)
    rect(s,0,0,SW,Inches(0.22),BLUE); rect(s,0,Inches(7.28),SW,Inches(0.22),TEAL)
    org=_logo("tertiary-infotech-logo.png")
    if org: s.shapes.add_picture(org,Inches(0.85),Inches(0.7),height=Inches(1.05))
    # course motif (top-right): AI x video badge
    bx,by=Inches(10.6),Inches(0.62)
    roundrect(s,bx,by,Inches(1.95),Inches(1.2),BLUE)
    tri=s.shapes.add_shape(MSO_SHAPE.ISOSCELES_TRIANGLE,int(bx+Inches(0.28)),int(by+Inches(0.3)),Inches(0.6),Inches(0.6))
    tri.rotation=90; tri.fill.solid(); tri.fill.fore_color.rgb=WHITE; tri.line.fill.background(); tri.shadow.inherit=False
    txt(s,int(bx+Inches(0.92)),int(by+Inches(0.18)),Inches(1.0),Inches(0.9),
        [[("GEN",16,WHITE,True)],[("AI",16,WHITE,True)]],space=0)
    txt(s,Inches(0.9),Inches(2.3),Inches(12),Inches(0.6),[[("COURSE SLIDES  ·  WSQ",16,BLUE,True)]])
    txt(s,Inches(0.9),Inches(2.85),Inches(12.0),Inches(1.9),[[(C.TITLE,40,INK,True)]])
    rect(s,Inches(0.92),Inches(4.35),Inches(2.4),Inches(0.06),TEAL)
    txt(s,Inches(0.9),Inches(4.65),Inches(12),Inches(1.6),
        [[("AI-generated scripts · text-to-video · AI voice & music · AI editing · agentic publishing",15,GREY,False)],
         [(f"WSQ Course Code: {C.COURSE_CODE}",16,GREY,False)],
         [("Conducted by Tertiary Infotech Academy Pte Ltd  ·  UEN 201200696W",14,GREY,False)]],space=8)
    txt(s,Inches(0.9),Inches(6.5),Inches(12),Inches(0.4),[[(f"Version {C.VERSION}  ·  {C.VERSION_DATE}",12,GREY,False)]])
    txt(s,Inches(0.9),Inches(6.85),Inches(12),Inches(0.34),[[("© 2026 Tertiary Infotech Academy Pte Ltd. All rights reserved.  ·  www.tertiarycourses.com.sg",10,GREY,False)]])

def section(kicker,title,n,sub=""):
    s=slide(); rect(s,0,0,SW,SH,WHITE); rect(s,0,0,Inches(0.28),SH,BLUE)
    rect(s,Inches(0.85),Inches(2.5),Inches(0.14),Inches(2.0),TEAL)
    txt(s,Inches(1.25),Inches(2.55),Inches(11),Inches(0.6),[[(kicker,18,BLUE,True)]])
    txt(s,Inches(1.25),Inches(3.0),Inches(11.4),Inches(1.6),[[(title,_fit_title(title,40),INK,True)]])
    if sub: txt(s,Inches(1.27),Inches(4.55),Inches(11),Inches(0.8),[[(sub,16,GREY,False)]])
    txt(s,Inches(10.0),Inches(0.7),Inches(2.8),Inches(1.6),[[(n,72,LINE,True)]],align=PP_ALIGN.RIGHT)
    footer(s); return s
def content(title,items,kicker=None,size=20):
    s=head(slide(),title,kicker); bullets(s,Inches(0.85),Inches(1.95),Inches(11.6),Inches(4.9),items,size=size); footer(s); return s
def two_col(title,left,right,kicker=None,lhead="",rhead=""):
    s=head(slide(),title,kicker)
    rect(s,Inches(0.85),Inches(1.95),Inches(5.7),Inches(4.7),LIGHT); rect(s,Inches(6.95),Inches(1.95),Inches(5.55),Inches(4.7),LIGHT)
    if lhead: txt(s,Inches(1.1),Inches(2.15),Inches(5.2),Inches(0.4),[[(lhead,16,BLUE,True)]])
    if rhead: txt(s,Inches(7.2),Inches(2.15),Inches(5.0),Inches(0.4),[[(rhead,16,TEAL,True)]])
    bullets(s,Inches(1.1),Inches(2.7),Inches(5.2),Inches(3.8),left,size=16)
    bullets(s,Inches(7.2),Inches(2.7),Inches(5.05),Inches(3.8),right,size=16,mcolor=TEAL); footer(s); return s
def cards3(title,cards,kicker):
    s=head(slide(),title,kicker); xs=[Inches(0.85),Inches(5.0),Inches(9.15)]
    for i,c in enumerate(cards[:3]):
        x=xs[i]; col=c[0]
        rect(s,x,Inches(1.95),Inches(3.65),Inches(4.7),LIGHT); rect(s,x,Inches(1.95),Inches(3.65),Inches(0.12),col)
        txt(s,x+Inches(0.25),Inches(2.2),Inches(3.2),Inches(0.6),[[(c[1],19,col,True)]])
        bullets(s,x+Inches(0.25),Inches(2.95),Inches(3.2),Inches(3.4),c[2],size=14,mcolor=col,gap=9)
    footer(s); return s
def big_statement(line1,line2,kicker,color=BLUE):
    s=slide(); rect(s,0,0,SW,SH,WHITE); rect(s,0,0,Inches(0.28),SH,color)
    txt(s,Inches(1.1),Inches(2.2),Inches(11),Inches(0.5),[[(kicker,16,color,True)]])
    txt(s,Inches(1.1),Inches(2.8),Inches(11.3),Inches(2.4),[[(line1,38,INK,True)]])
    if line2: txt(s,Inches(1.12),Inches(4.9),Inches(11),Inches(1.2),[[(line2,20,GREY,False)]])
    footer(s); return s

PALETTE=[BLUE,TEAL,VIOLET,AMBER]
def tile_grid(title,items,kicker=None,cols=2,size=15,icons=None,accent=BLUE):
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
        col=accent if i==0 else PALETTE[(i-1)%len(PALETTE)]
        rect(s,x,y,widths[i],hh,col)
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
            [[("WHY IT MATTERS  ",11,accent,True),(note,12,INK,False)]])
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
    AVAIL=Inches(4.92); gap=Inches(0.22)
    total=sum(len(t) for _,t in items)
    for i,(label,text) in enumerate(items):
        share=max(0.22,len(text)/max(total,1)) if len(items)>1 else 1.0
        ph=int((AVAIL-gap*(len(items)-1))*share) if len(items)>1 else int(AVAIL)
        rect(s,X0,int(y),TOTW,Inches(0.4),LIGHT)
        rect(s,X0,int(y),Inches(0.1),Inches(0.4),VIOLET)
        txt(s,X0+Inches(0.28),int(y+Inches(0.03)),TOTW-Inches(0.5),Inches(0.34),
            [[("PROMPT — "+label.upper(),11.5,VIOLET,True)]])
        bh=ph-Inches(0.4)
        rect(s,X0,int(y+Inches(0.4)),TOTW,int(bh),DARKBG)
        lines=text.split("\n")
        fs=11 if len(text)<420 else (10 if len(text)<640 else 9)
        runs=[[(ln,fs,CODEBLUE,False)] for ln in lines]
        txt(s,X0+Inches(0.28),int(y+Inches(0.48)),TOTW-Inches(0.56),int(bh-Inches(0.16)),
            runs,space=2,anchor=MSO_ANCHOR.MIDDLE)
        y=int(y+ph+gap)
    footer(s); return s

def test_slide(act_title,text,kicker):
    s=head(slide(),act_title,kicker,TEAL)
    rect(s,Inches(0.85),Inches(2.3),Inches(11.7),Inches(2.6),RGBColor(0xE8,0xF7,0xEE))
    txt(s,Inches(1.2),Inches(2.6),Inches(11),Inches(0.5),[[("✅  Check your work",20,RGBColor(0x12,0x7A,0x3E),True)]])
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

# ============================================================ BUILD
cover()

# ---------------- ADMIN ----------------
section("COURSE ADMINISTRATION","Welcome & Housekeeping","")
content("Digital Attendance (Mandatory)",[
 "It is mandatory to take the AM, PM and Assessment digital attendance for WSQ-funded courses.",
 "The trainer/administrator displays the digital attendance QR code from the SSG portal.",
 "Scan the QR code with your mobile phone camera and submit your attendance.",
 "A minimum of 75% attendance is required to be eligible for assessment and funding."],kicker="TRAQOM · SSG DIGITAL ATTENDANCE")
trainer_slide("YOUR TRAINER · GENERAL","Your Trainer","General Trainer template —\nto be completed by the trainer",
 [("Name",""),("Title / Designation",""),("Qualifications",""),
  ("Areas of expertise",""),("Training & industry experience",""),("Contact","")],
 initials="?",accent=GREY)
trainer_slide("YOUR TRAINER",C.TRAINER,"Principal Trainer\nTertiary Infotech Academy Pte Ltd",
 [("Role","Principal Trainer and Founder, Tertiary Infotech Academy Pte Ltd"),
  ("Expertise","Generative AI, AI video production, data science and machine learning."),
  ("Delivers","WSQ courses on GenAI content creation, AI video, prompt engineering and analytics."),
  ("Background","PhD; 15+ years training professionals across AI, engineering and digital media.")],
 initials="AA",accent=BLUE)
content("Let's Know Each Other",[
 "Your name and organisation / role.",
 "Your experience with video creation or editing (if any).",
 "What videos do you want to create after this course — marketing, training, social media?"],kicker="ICE-BREAKER")
tile_grid("Ground Rules",[
 "Set your mobile phone to silent mode.","Participate actively — no question is too small.",
 "Respect each other's views.","One conversation at a time.",
 "Exit quietly for calls or breaks.","Be punctual; 75% attendance is required."],
 kicker="HOUSEKEEPING",cols=2,size=15)
screenshot_slide("Download Course Material",
 _logo("lms-tms-screenshot.png"),
 ["Go to lms-tms.tertiaryinfotech.com and sign in with your registered email.",
  "Open My Courses and select this course.",
  "Download the Trainer Slides, Learner Guide and Lesson Plan PDFs.",
  "Keep them handy — the final assessment is open book."],
 kicker="LMS / TMS COURSE PORTAL", url="https://lms-tms.tertiaryinfotech.com")
two_col("Lesson Plan — 2 Days, 8 hours/day",[
 (f"Day 1 — {C.DAY_THEMES[1]}",0),
 ("Digital attendance (AM) · introductions",1),
 ("Topic 1: Create & Edit Video Script Using GenAI (Labs 1–4)",1),
 ("Topic 2 begins: Improve Video Footage on VEED (Labs 5–6)",1),
 ("Digital attendance (PM) · Day 1 recap",1)],
 [(f"Day 2 — {C.DAY_THEMES[2]}",0),
 ("Digital attendance (AM) · recap",1),
 ("Topic 2: Audio & quality mini project (Labs 7–8)",1),
 ("Topic 3: Avatars, music, cloning, agentic publishing (Labs 9–12)",1),
 ("Revision · TRAQOM survey · Assessment attendance",1),
 ("Final Assessment: WA (1 h) + PP (1 h)",1)],
 kicker="SCHEDULE",lhead="Day 1",rhead="Day 2")
two_col("Skills Framework",[
 (f"TSC: {C.TSC_TITLE}  ·  {C.TSC_CODE}",0)]+[(k,1) for k in C.TSC_KNOWLEDGE],
 [("Abilities",0)]+[(a,1) for a in C.TSC_ABILITIES[:4]]+[("Plus A5–A7 (assessed in the PP)",1)],
 kicker="WSQ · SKILLS FRAMEWORK",lhead="Knowledge (assessed in the WA)",rhead="Abilities (assessed in the PP)")
tile_grid("Learning Outcomes",[
 ("LO1 — Plan","Develop video editing strategies and work plans to achieve creative video."),
 ("LO2 — Assess","Assess edited video footage to enhance storytelling and ensure technical compliance."),
 ("LO3 — Improve","Develop remedial actions for compliance and adopt new technologies in video editing.")],
 kicker="WHAT YOU'LL ACHIEVE",cols=1,size=16)
tile_grid("Course Outline",[
 ("Topic 1 — AI Scripts & Text-to-Video","RICCE prompts, story structure, script templates, VEED AI Video Maker, standards & work plans.  (Labs 1–4)"),
 ("Topic 2 — Improve Footage on VEED","Editing essentials, subtitles & captions, AI voiceover & clean audio, quality assessment.  (Labs 5–8)"),
 ("Topic 3 — New AI Technologies","AI avatars & images, AI music, voice cloning & dubbing, agentic publishing to YouTube/TikTok.  (Labs 9–12)")],
 kicker="THREE TOPICS · TWELVE HANDS-ON LABS",cols=1,size=15)
tile_grid("Briefing for Assessment",[
 "Place phones and other materials under the table or on the floor.",
 "No photos or recording of assessment scripts.",
 "No discussion during the assessment.",
 "Use a black/blue pen for hard-copy assessments.",
 "No liquid paper / correction tape.",
 "Scripts are collected when time is up."],
 kicker="ASSESSMENT RULES",cols=2,size=13)
content("Assessment",[
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

# ---------------- THE BIG PICTURE ----------------
section("THE BIG PICTURE","How Generative AI Creates Video","")
big_statement("An entire video production studio, in your browser.",
 "Script, footage, voice, music, editing and publishing — every stage of video production now has a GenAI tool. McKinsey estimates generative AI adds trillions in economic value; content creation is one of its biggest use cases.",
 "WHY THIS COURSE",color=BLUE)
process_map("The GenAI Video Creation Pipeline",C.PIPELINE,
 kicker="THE PROCESS FLOW YOU'LL MASTER — EVERY LAB MAPS TO A STAGE",
 synthesis=("One pipeline, five AI stages",
  "You'll write scripts with GenAI (Topic 1), generate and edit the video with AI tools (Topics 1–2), add AI voice and music (Topics 2–3), and let an agentic AI push the finished video to YouTube and TikTok (Topic 3)."))
tile_grid("The GenAI Toolbox by Pipeline Stage",[
 ("1 · Script","ChatGPT, Gemini, Claude, Copilot, custom GPTs — ideas, storylines, dialogue, formats."),
 ("2 · Video","VEED AI Video Maker, Sora, Veo, Kling, Hailuo, Pika, Runway, CapCut — text/image to video."),
 ("3 · Voice & music","VEED TTS, ElevenLabs, Play.ht (voice) · Suno, Udio, AIVA (music)."),
 ("4 · Editing","VEED editor — subtitles, clean audio, background removal, resize, translate, eye contact."),
 ("5 · Publishing","Agentic AI + YouTube Studio, TikTok — metadata, thumbnails, scheduling, automation."),
 ("Cross-stage","Prompt engineering (RICCE) drives quality at every stage of the pipeline.")],
 kicker="TOOL LANDSCAPE 2026",cols=2,size=13)
compare_table("AI Video Generation Models",
 ["Model","Made by","Strength","Access"],
 [["Sora 2","OpenAI","Cinematic realism, physics, long shots","ChatGPT / VEED"],
  ["Veo 3.1","Google","Native audio + dialogue in generation","Gemini / VEED"],
  ["Kling","Kuaishou","Motion quality, character consistency","Kling / VEED"],
  ["Hailuo","MiniMax","Fast, expressive short clips","Hailuo / VEED"],
  ["Fabric 1.0","HeyGen","Talking avatars from one photo","HeyGen / VEED"]],
 kicker="STATE OF THE ART · 2026",accent=BLUE,
 note="VEED aggregates multiple models behind one editor — you pick per shot, so one platform covers the whole pipeline.")
process_map("How VEED Builds a Video from Text",[
 ("Describe","type your idea or script"),
 ("AI drafts scenes","storyboard + footage"),
 ("Customize","avatar, voice, captions"),
 ("Refine in editor","swap scenes, fix audio"),
 ("Export & share","1080p, any ratio")],
 kicker="VEED.IO · AI VIDEO MAKER WORKFLOW",color=TEAL,
 synthesis=("No filming, no studio","From a text prompt to a finished, voiced, captioned video in minutes — you stay in control at every stage."))

# ---------------- TOPICS + ACTIVITIES ----------------
TOPIC_ACTS={t["num"]:[a for a in ACTIVITIES if a["topic"]==t["num"]] for t in C.TOPICS}
CARD_COLORS=[BLUE,TEAL,VIOLET]

def topic_extra_slides(tnum):
    """Substantive teaching slides per topic (beyond the key-concepts grid)."""
    if tnum==1:
        tile_grid("What Makes a Script Work",[
         ("Understand the brief","Decode the client's goal, audience and message before writing a word."),
         ("Research the topic","Primary and secondary sources, expert interviews, competitor videos."),
         ("Develop the narrative","A storyline that carries the message — not a list of features."),
         ("Platform fit","A TV ad, a YouTube explainer and a TikTok hook are different scripts.")],
         kicker="SCRIPT DEVELOPMENT",cols=2,size=14)
        tile_grid("Good Story Elements",[
         ("Identifiable hero","A protagonist the audience recognises themselves in."),
         ("A clear desire","What does the hero want? Ambiguity kills engagement."),
         ("A real obstacle","No obstacle, no story — conflict is the heart of drama."),
         ("Action & outcome","The hero acts; the world changes. Show the transformation."),
         ("Resolution","End the story world in a new, better state — with your CTA."),
         ("The story spine","Once upon a time… then one day… but… so… until finally…")],
         kicker="STORYTELLING",cols=2,size=13)
        compare_table("Tailoring Scripts to the Platform",
         ["","YouTube","TikTok / Shorts","Instagram Reels"],
         [["Length","60 s – 10 min","15 – 60 s","15 – 90 s"],
          ["Ratio","16:9 landscape","9:16 vertical","9:16 vertical"],
          ["Pacing","Build with structure","Hook in 1–3 s, fast cuts","Aesthetic-first, fast"],
          ["Captions","Recommended","Essential (muted viewing)","Essential"],
          ["Style","Explainer / narrative","Trend-led, punchy","Polished, visual"]],
         kicker="ONE SCRIPT ≠ EVERY PLATFORM",accent=VIOLET,
         note="Ask the AI to re-cut the same story per platform — Lab 1 does exactly this.")
        process_map("The RICCE Prompt Framework",[
         ("Role","who the AI should be"),
         ("Instructions","the task, with a verb"),
         ("Context","background & audience"),
         ("Constraints","length, tone, limits"),
         ("Example","show the output format")],
         kicker="PROMPT ENGINEERING FOR SCRIPTS",color=VIOLET,
         synthesis=("Quality in, quality out","The RICCE structure turns a vague ask into a production-ready script brief — it is the single biggest lever on GenAI output quality."))
        tile_grid("Common Script Pitfalls (and the AI fix)",[
         ("Vague hero","Ask the AI to give the protagonist a name, job and one burning goal."),
         ("No clear desire","Prompt: 'State what the hero wants in one sentence — rewrite the opening around it.'"),
         ("No obstacle = boring","Prompt the AI to inject a concrete obstacle and raise the stakes."),
         ("No resolution = puzzling","Ask for an ending that resolves the conflict and lands the CTA.")],
         kicker="K1 · SCRIPT-LEVEL QUALITY ISSUES",cols=2,size=13)
    if tnum==2:
        tile_grid("The VEED Editor at a Glance",[
         ("Timeline","Layer clips, audio, text and images; drag to reorder, snap to cut points."),
         ("Trim · split · merge","Cut dead air, split takes, merge clips into one sequence."),
         ("Crop · resize · loop","Smart-crop the subject; one-click resize to 16:9, 9:16, 1:1; loop b-roll."),
         ("Text & templates","Animated titles, lower thirds, brand kits and thousands of templates."),
         ("Record","Webcam, screen or both — record straight into the project."),
         ("Stock library","Royalty-free video, images and music inside the editor.")],
         kicker="VIDEO EDITING BASICS",cols=2,size=13)
        tile_grid("Subtitles, Captions & Translation",[
         ("Auto subtitles","AI speech-to-text transcribes your audio in seconds — ~95% accuracy on clean audio."),
         ("Styled captions","Word-by-word animated captions tuned for muted social feeds."),
         ("Transcripts","Download TXT/SRT/VTT for accessibility, SEO and repurposing."),
         ("Auto translate","Subtitles in 100+ languages — one video, global reach.")],
         kicker="ACCESSIBILITY = ENGAGEMENT",cols=2,size=14)
        tile_grid("The AI Audio Toolbox",[
         ("Text-to-speech","Type a script, pick from 100+ voices and languages, get narration instantly."),
         ("Clean audio","One click strips background noise, hum and echo from recordings."),
         ("Music ducking","Keep music ~20% under speech so the voice always wins."),
         ("Voice consistency","Same AI voice across every video = recognisable brand sound.")],
         kicker="AUDIO ENHANCEMENT",cols=2,size=14)
        compare_table("Quality Issues → AI Solutions",
         ["Issue (K1)","Typical cause","AI solution (K2)"],
         [["Cluttered background","Filmed at desk / home","Remove background + replace scene"],
          ["Noisy / muffled audio","Room echo, aircon, traffic","Clean Audio noise removal"],
          ["Off-frame subject","Static camera, bad framing","Smart crop / reframe"],
          ["Wrong aspect ratio","One master file for all platforms","One-click resize per platform"],
          ["Missing captions","No time to transcribe","Auto subtitles + styled captions"],
          ["Flat delivery","Reading from notes off-camera","AI eye contact correction"]],
         kicker="K1 → K2 · THE WA ASKS EXACTLY THIS",accent=TEAL,
         note="Every issue on the left appears in the Written Assessment — know the matching fix.")
        tile_grid("Parameters to Assess Video Quality",[
         ("Resolution & sharpness","1080p minimum for social; no upscaled blur."),
         ("Frame rate","Smooth, consistent motion — no stutter at cuts."),
         ("Audio levels","Voice clear above music; no clipping or noise floor."),
         ("Visual consistency","Colour, lighting and style hold across every clip."),
         ("Pacing","Cuts match the message rhythm; no dead sections."),
         ("Compliance","Platform specs, brand rules, licensing, consent.")],
         kicker="K3 · ASSESSMENT PARAMETERS",cols=2,size=13)
        content("Working Across Multiple AI Tools",[
         "Feature compatibility: tools export different resolutions and frame rates — mismatches show at the joins.",
         "Visual consistency: each tool grades colour and styles transitions differently — the look drifts.",
         "Audio quality: different loudness handling produces jarring level jumps between segments.",
         "The fix: finish everything on ONE editing platform (VEED) and export once, per platform."],
         kicker="WHY A SINGLE FINISHING PLATFORM",size=17)
    if tnum==3:
        tile_grid("The AI Features in VEED",[
         ("AI avatars","Photorealistic presenters speak your script — 50+ stock or clone yourself."),
         ("AI image generator","On-brand stills and backgrounds from a text prompt."),
         ("AI text-to-video","Whole videos from a description (Lab 3)."),
         ("Eye contact","Fixes off-camera gaze so you look at the lens."),
         ("Voice clone & dub","Your voice, any language, lip-synced."),
         ("Auto clips","Repurpose one long video into many short ones.")],
         kicker="K5 · NEW EDITING TECHNOLOGIES",cols=2,size=13)
        tile_grid("TTS & Voice Cloning — Use Cases",[
         ("Dubbing & voice-overs","Narrate without a studio; dub into any market language."),
         ("Brand personification","One consistent voice across every touchpoint."),
         ("E-learning & audiobooks","Turn documents into narrated content at scale."),
         ("Accessibility","Reading assistance and speech-impairment aid."),
         ("Digital avatars","Give a face and voice to virtual presenters and agents."),
         ("Call centres & IVR","Natural prompts without re-recording sessions.")],
         kicker="WHERE AI SPEECH CREATES VALUE",cols=2,size=13)
        compare_table("GenAI Music & Speech Tools",
         ["Tool","Type","Best for","Cost"],
         [["Suno","Music + vocals","Full songs from a text prompt","Free tier"],
          ["Udio","Music + vocals","High-fidelity tracks, fine control","Free tier"],
          ["AIVA / Soundraw","Instrumental","Soundtrack beds by mood/genre","Free credits"],
          ["ElevenLabs","Speech","Ultra-natural TTS + voice cloning","Free tier"],
          ["Play.ht / Resemble","Speech","Cloning + API integration","Free trial"]],
         kicker="PICK YOUR AUDIO STACK",accent=AMBER,
         note="Always check the plan's commercial-use rights before a client project — free tiers often exclude them.")
        tile_grid("Lip Sync & Talking Heads",[
         ("VEED dubbing","Translated audio re-synced to the speaker's lips."),
         ("D-ID","Animate a still portrait into a conversational agent."),
         ("Sync Labs","Lip-sync any audio onto any face in video."),
         ("HeyGen / EMO","Audio-driven avatar video from a single photo.")],
         kicker="AUDIO-DRIVEN VIDEO",cols=2,size=14)
        process_map("Agentic AI Publishing Workflow",[
         ("Export cuts","16:9 + 9:16 from VEED"),
         ("Agent drafts kit","title · desc · hashtags"),
         ("Human approves","you review every word"),
         ("Agent publishes","YouTube · TikTok upload"),
         ("Track & iterate","analytics feed next video")],
         kicker="THE LAST MILE — AGENTIC AI",color=VIOLET,
         synthesis=("Automation with a human gate",
          "The agent does the busywork — metadata, thumbnails, scheduling, uploads — but a human approves before anything goes live. That's the professional agentic pattern."))
        tile_grid("Industry Standards & Responsible AI (K4)",[
         ("Platform specs","Resolution, ratio, duration and loudness rules per platform."),
         ("Copyright & licensing","Only rights-cleared footage, music and fonts — AI output included."),
         ("Consent & PDPA","Permission for faces and voices; clone only with consent."),
         ("AI disclosure","Label synthetic media where platforms and law require it."),
         ("Brand & broadcast codes","House style plus IMDA/ASAS advertising standards."),
         ("Accuracy","AI hallucinates — fact-check every claim before publishing.")],
         kicker="COMPLY BEFORE YOU PUBLISH",cols=2,size=13)
        compare_table("Evaluating a New AI Tool (A7)",
         ["Criterion","Ask","Red flag"],
         [["Quality","Does output meet your standards sheet?","Artefacts, drift, robotic voice"],
          ["Speed & cost","Time and $ per finished minute?","Credits burn faster than value"],
          ["Control","Can you edit/iterate the result?","Black-box, no editing"],
          ["Rights","Commercial use on your plan?","Licence excludes client work"],
          ["Integration","Fits your existing pipeline?","New silo, manual re-export"]],
         kicker="A REPEATABLE EVALUATION RUBRIC",accent=VIOLET,
         note="Use this rubric in Labs 10–12 when you compare Suno vs Udio, clones vs stock TTS, and manual vs agentic publishing.")

def lab_flow(a):
    """The lab's 5-stage process map from its explicit `flow` labels (no step-by-step)."""
    stages=[(t,"") for t in a["flow"]]
    process_map(f"How Lab {a['num']} Runs",stages,
        kicker=f"LAB {a['num']} · HOW IT RUNS — FULL STEPS IN THE LEARNER GUIDE",
        color=TEAL,animate=False)

for t in C.TOPICS:
    section(f"TOPIC {t['code']}",t["title"],t["code"],t["subtitle"])
    tile_grid(f"Key Concepts — Topic {int(t['code'])}",t["concepts"],
              kicker=f"COVERS {t['weighting']}",cols=2,size=13)
    topic_extra_slides(t["num"])
    acts=TOPIC_ACTS[t["num"]]
    cards=[]
    for gi,a in enumerate(acts):
        cards.append((CARD_COLORS[gi%3],f"Lab {a['num']}",[a["title"],a["build"]]))
    # 4 labs → tile grid instead of cards3
    tile_grid(f"Hands-On Labs — Topic {int(t['code'])}",
        [(f"Lab {a['num']} — {a['title']}",a["build"]) for a in acts],
        kicker="WHAT YOU'LL DO",cols=1,size=13,icons=[str(a["num"]) for a in acts])
    for a in acts:
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
    content(f"Recap — {t['title']}",
            ["You can now: "+a["objective"] for a in {x["objective"]:x for x in acts}.values()][:6],
            kicker="TOPIC RECAP",size=17)

# ---------------- CLOSE ----------------
section("WRAP-UP","Course Summary & Next Steps","")
process_map("The Pipeline You Now Own",C.PIPELINE,
 kicker="FROM PROMPT TO PUBLISHED — RECAP",
 synthesis=("Twelve labs, one pipeline",
  "Scripts (Labs 1–2) → video generation (Lab 3) → standards & plans (Lab 4) → editing & quality (Labs 5–8) → avatars, music, voice (Labs 9–11) → agentic publishing (Lab 12)."),
 animate=False)
tile_grid("What You Achieved",[
 ("AI scripts","RICCE prompts, story templates and custom GPTs produce platform-ready scripts."),
 ("AI video","Text-to-video with VEED and today's frontier models — plus full editor control."),
 ("AI audio","Voiceovers, cleaned audio, cloned voices, dubbed languages and generated music."),
 ("Quality & compliance","Assessed footage against real parameters, fixed issues, met standards."),
 ("Agentic publishing","An AI agent drafts, you approve, it ships to YouTube and TikTok."),
 ("Evaluation skill","A rubric to judge every new AI tool that arrives after this course.")],
 kicker="LEARNING OUTCOMES DELIVERED",cols=2,size=13)
screenshot_slide("Practice Exam — Test Yourself",
 _logo("exams-screenshot.png"),
 ["Go to exams.tertiaryinfotech.com.",
  "Free practice exams sharpen your GenAI knowledge — try the Claude Certified Associate (Foundations) exam for GenAI fundamentals.",
  "Attempt questions under timed conditions and review every explanation.",
  "Revisit any lab whose topic you miss."],
 kicker="EXAMS.TERTIARYINFOTECH.COM",url="https://exams.tertiaryinfotech.com")
content("Recommended Next Courses",[
 "WSQ - Mastering Prompt Engineering for Generative AI Content Creation",
 "WSQ - Practical Image Generation Using GAN, VAE, and Diffusion Models",
 "WSQ - Digital Transformation and Business Innovation with Generative AI (GenAI)",
 "WSQ - Develop Generative AI Solutions with Azure OpenAI Service",
 "WSQ - Build LLM Applications Using Langchain and Flowise"],kicker="KEEP LEARNING")
content("Support",[
 "If you have any enquiries during and after the class, contact us:",
 "Email: enquiry@tertiaryinfotech.com",
 "Tel: +65 6100 0613",
 "Web: www.tertiarycourses.com.sg"],kicker="WE'RE HERE TO HELP")
content("Cert & TRAQOM Survey (Mandatory)",[
 "Complete the TRAQOM course feedback survey on the LMS — it is mandatory for WSQ funding.",
 "Your digital certificate is issued on the LMS after you are assessed Competent.",
 "Portal: https://lms-tms.tertiaryinfotech.com"],kicker="BEFORE YOU LEAVE")
content("Assessment",[
 C.ASSESSMENT["written"], C.ASSESSMENT["practical"],
 "Open book: slides, Learner Guide and approved materials only.",
 "Remember to take the Assessment digital attendance.",
 "Submit your completed answers to the assessor."],kicker="FINAL ASSESSMENT")
flow_h("Assessment Flow",[
 "TRAQOM survey — scan the QR code on the LMS",
 "Assessment digital attendance — scan the SSG QR",
 "Sit WA (SAQ) then PP — open book",
 "Submit your answers on the LMS",
 "Sign the Assessment Summary Record"],kicker="ON ASSESSMENT DAY")
content("Digital Attendance (Mandatory)",[
 "It is mandatory to take the AM, PM and Assessment digital attendance for WSQ-funded courses.",
 "The trainer/administrator displays the digital attendance QR code from the SSG portal.",
 "Scan the QR code with your mobile phone camera and submit your attendance.",
 "A minimum of 75% attendance is required to be eligible for assessment and funding."],kicker="TRAQOM · SSG DIGITAL ATTENDANCE")
big_statement("Thank You!","You can now take a video from a text prompt to a published post — with AI at every stage and you in control.","HAPPY CREATING",color=TEAL)

# ---------------- transitions (one pass) ----------------
for i,s in enumerate(prs.slides):
    is_section=False
    # heuristic: section slides have the big pale number textbox at top-right
    _transition(s,"fade","fast")

OUT=os.path.join(REPO,"courseware",f"{C.SHORT_TITLE}-{C.VERSION}.pptx")
prs.save(OUT)
n=len(prs.slides._sldIdLst)
print(f"Saved {OUT}  ({n} slides)")
