import os, subprocess, sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter
S=sys.argv[1]; A=sys.argv[2]
V=os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)),"..","..","..","..","courseware","assets","videos"))
AR="/System/Library/Fonts/Supplemental/Arial.ttf"; ARB="/System/Library/Fonts/Supplemental/Arial Bold.ttf"
F=lambda p,s: ImageFont.truetype(p,s)
# --- CapCut: blur personal data
def blur(im,box,r=22):
    reg=im.crop(box).filter(ImageFilter.GaussianBlur(r)); im.paste(reg,box)
h=Image.open(f"{S}/capcut_main.png").convert("RGB")   # 2418x1612
k=2418/2000
blur(h,tuple(int(v*k) for v in (40,75,325,140)))
h.save(f"{A}/capcut/capcut_home.jpg",quality=90)
e=Image.open(f"{S}/cc_editor0.png").convert("RGB")    # 3000x1730
k=1.5
blur(e,tuple(int(v*k) for v in (1370,115,1975,210)))      # project name + local path
blur(e,tuple(int(v*k) for v in (900,5,1100,40)))          # window title (project name)
e.save(f"{A}/capcut/capcut_editor.jpg",quality=90)
# --- storyboard sheets from the demo films
def frame(src,t,out):
    subprocess.run(["ffmpeg","-v","error","-y","-ss",str(t),"-i",src,"-frames:v","1","-vf","scale=640:-2",out],check=True)
    return Image.open(out).convert("RGB")
def sheet(name,title,src,panels,out):
    W=2400
    n=len(panels); cols=3 if n>4 else n; rows=(n+cols-1)//cols
    pw=(W-120-(cols-1)*40)//cols; ph=int(pw*9/16); ch=ph+175
    H=170+rows*(ch+30)+20
    im=Image.new("RGB",(W,H),(250,248,244)); d=ImageDraw.Draw(im)
    d.text((60,40),"STORYBOARD",font=F(ARB,30),fill=(217,119,87)); d.text((60,80),title,font=F(ARB,46),fill=(33,32,28))
    for i,(t,shot,size,act,snd,ost) in enumerate(panels):
        r,c=divmod(i,cols); x=60+c*(pw+40); y=170+r*(ch+30)
        fr=frame(src,t,f"{S}/sbf.jpg").resize((pw,ph)); im.paste(fr,(x,y)); d.rectangle([x,y,x+pw,y+ph],outline=(60,60,60),width=3)
        d.rounded_rectangle([x+12,y+12,x+12+190,y+62],10,fill=(217,119,87)); d.text((x+26,y+18),f"{i+1} · {shot}",font=F(ARB,28),fill="white")
        yy=y+ph+14
        for lab,val,col in (("SIZE · ANGLE · MOVE",size,(58,125,123)),("ACTION",act,(33,32,28)),("SOUND",snd,(194,96,63)),("ON SCREEN",ost,(184,138,62))):
            d.text((x,yy),lab,font=F(ARB,20),fill=col); d.text((x+250,yy-2),val,font=F(AR,24),fill=(40,40,40)); yy+=36
    im.save(out,quality=90)
sola=os.path.join(V,"marketing-sola-15s.mp4"); ring=os.path.join(V,"scifi-ring-15s.mp4")
sheet("sola","SOLA · 15-second product ad (16:9)",sola,[
 (1.0,"0–3 s","ECU · low · slow push-in","Sun slides across the bottle","Wind, distant city","—"),
 (4.0,"3–6 s","MS · eye level · tracking","Runner grabs it mid-stride","Footsteps, breath","—"),
 (7.5,"6–9 s","CU · eye level · slow-mo","She drinks; ice clinks","Ice clink, swallow","—"),
 (11.0,"9–12 s","EWS · high · drone pull-back","Rooftop run at sunrise","Music swells","—"),
 (13.5,"12–15 s","MS · eye level · locked off","Hero packshot, logo space","Music hit","SOLA")],f"{A}/sb/storyboard-sola.jpg")
sheet("ring","Ringfall · 15-second sci-fi scene (16:9)",ring,[
 (2.0,"0–4 s","EWS · eye level · slow pan","Smoking wreck, twin suns","Wind, metal creak","—"),
 (6.0,"4–8 s","MS · eye level · handheld","Pilot steps out, follows","Boots on sand","—"),
 (9.5,"8–11 s","CU · low · push-in","Her face: awe; ground shakes","Low rumble","—"),
 (13.5,"11–15 s","EWS · low · crane up","The ring rises over the dunes","Choir swell","RINGFALL")],f"{A}/sb/storyboard-ringfall.jpg")
# --- what to cut: raw 32 s vs final 16 s timeline
W,H=2400,900; im=Image.new("RGB",(W,H),"white"); d=ImageDraw.Draw(im)
def bar(y,label,segs,scale):
    d.text((60,y-60),label,font=F(ARB,38),fill=(33,32,28)); x=60
    for dur,txt_,col,keep in segs:
        w=int(dur*scale); fill=col if keep else (225,222,215)
        d.rectangle([x,y,x+w-6,y+130],fill=fill)
        if not keep:
            for k in range(0,max(0,w-50),24): d.line([x+k,y,x+k+40,y+130],fill=(200,196,188),width=3)
        d.text((x+10,y+14),txt_,font=F(ARB,24),fill=(255,255,255) if keep else (120,116,110))
        d.text((x+10,y+90),f"{dur:g} s",font=F(AR,22),fill=(255,255,255) if keep else (120,116,110)); x+=w
sc=2250/32
raw=[(3,"Logo intro",None,False),(2,"Hook",(217,119,87),True),(4,"Warm-up jog",None,False),(3,"Grab",(58,125,123),True),
     (3,"Drink (slow-mo)",(58,125,123),True),(3,"2nd drink, same",None,False),(4,"Wide run",(184,138,62),True),(4,"Wide, again",None,False),
     (3,"Packshot",(194,96,63),True),(3,"Thank you card",None,False)]
bar(170,"RAW ASSEMBLY · 32 s · everything we generated",raw,sc)
fin=[(2,"Hook",(217,119,87),True),(3,"Grab",(58,125,123),True),(3,"Drink",(58,125,123),True),(3,"Wide run",(184,138,62),True),(2,"Packshot",(194,96,63),True),(3,"CTA card",(33,32,28),True)]
bar(560,"FINAL CUT · 16 s · hook, one message, payoff, call to action",fin,sc)
d.text((60,760),"Cut first: logo intros, warm-ups, repeated beats, dead air, 'thank you' cards. Keep: the hook, every beat of the one message, the payoff, the CTA.",font=F(AR,28),fill=(90,90,90))
im.save(f"{A}/sb/cut-timeline.jpg",quality=90)
print("ok")
