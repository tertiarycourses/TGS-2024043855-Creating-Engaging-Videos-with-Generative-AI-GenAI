import os, subprocess
from PIL import Image, ImageDraw, ImageFont
import tempfile
S=tempfile.mkdtemp()   # intermediate frames and segments
V=os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)),"..","..","..","..","courseware","assets","videos"))
SRC=os.path.join(V,"marketing-sola-15s.mp4")
W,H=1280,720
AR="/System/Library/Fonts/Supplemental/Arial.ttf"; ARB="/System/Library/Fonts/Supplemental/Arial Bold.ttf"
def run(a): subprocess.run(["ffmpeg","-v","error","-y"]+a,check=True)
def font(p,s): return ImageFont.truetype(p,s)
def ctext(d,y,t,f,fill,stroke=0,sf=None):
    w=d.textlength(t,font=f); d.text(((W-w)/2,y),t,font=f,fill=fill,stroke_width=stroke,stroke_fill=sf)
# ---------- BORING (20 s): logo card, static stills, feature lines, no sound
def card(path,lines):
    im=Image.new("RGB",(W,H),"white"); d=ImageDraw.Draw(im)
    y=H/2-len(lines)*30
    for t,s in lines: ctext(d,y,t,font(AR,s),(90,90,90)); y+=s+24
    im.save(path)
def still(path,t,caption):
    tmp=path+".src.png"; run(["-ss",str(t),"-i",SRC,"-frames:v","1","-vf",f"scale={W}:{H}",tmp])
    im=Image.open(tmp).convert("RGB"); d=ImageDraw.Draw(im)
    d.rectangle([0,H-110,W,H],fill="white"); ctext(d,H-80,caption,font(AR,34),(40,40,40)); im.save(path); os.remove(tmp)
parts=[]
card(f"{S}/b0.png",[("Introduction to the SOLA Water Bottle",40),("Product Video",28)]); parts.append(("b0.png",4))
still(f"{S}/b1.png",13.0,"SOLA is a water bottle."); parts.append(("b1.png",4))
still(f"{S}/b2.png",11.5,"It can be used for exercise and other activities."); parts.append(("b2.png",4))
still(f"{S}/b3.png",0.5,"It is available in black."); parts.append(("b3.png",4))
card(f"{S}/b4.png",[("Thank you for watching.",36)]); parts.append(("b4.png",4))
segs=[]
for i,(f,dur) in enumerate(parts):
    o=f"{S}/bseg{i}.mp4"
    run(["-loop","1","-t",str(dur),"-i",f"{S}/{f}","-f","lavfi","-t",str(dur),"-i","anullsrc=r=48000:cl=stereo",
         "-c:v","libx264","-pix_fmt","yuv420p","-r","30","-c:a","aac","-shortest",o]); segs.append(o)
open(f"{S}/blist.txt","w").write("".join(f"file '{p}'\n" for p in segs))
run(["-f","concat","-safe","0","-i",f"{S}/blist.txt","-c","copy","-movflags","+faststart",f"{V}/t1-boring-20s.mp4"])
run(["-ss","5","-i",f"{V}/t1-boring-20s.mp4","-frames:v","1",f"{V}/t1-boring-poster.jpg"])
# ---------- ENGAGING (18 s): question hook in 0-3 s, a character, problem -> payoff, CTA end card
def overlay(path,big,small=None,pos="low"):
    im=Image.new("RGBA",(W,H),(0,0,0,0)); d=ImageDraw.Draw(im)
    y=H-200 if pos=="low" else 90
    d.rectangle([0,y-30,W,y+(150 if small else 100)],fill=(0,0,0,110))
    ctext(d,y,big,font(ARB,60),(255,255,255),3,(0,0,0))
    if small: ctext(d,y+80,small,font(AR,32),(255,214,170),2,(0,0,0))
    im.save(path)
caps=[("e0.png","Warm water by your first kilometre?",None,"top",0.0,3.0),
      ("e1.png","Not this one.",None,"low",3.0,6.0),
      ("e2.png","Still ice-cold after the run.",None,"low",6.0,9.5),
      ("e3.png","Made for 6 AM. Made for 32°C.",None,"low",9.5,12.5),
      ("e4.png","SOLA. Stay cold.","Keep running.","low",12.5,15.0)]
for f,b,s,p,_,_ in caps: overlay(f"{S}/{f}",b,s,p)
inputs=["-i",SRC]; fc=f"[0:v]scale={W}:{H},fps=30[v0];"; last="v0"
for i,(f,_,_,_,a,b) in enumerate(caps,1):
    inputs+=["-i",f"{S}/{f}"]; fc+=f"[{last}][{i}:v]overlay=0:0:enable='between(t,{a},{b})'[v{i}];"; last=f"v{i}"
fc=fc.rstrip(";")
run(inputs+["-filter_complex",fc,"-map",f"[{last}]","-map","0:a","-t","15","-c:v","libx264","-pix_fmt","yuv420p","-r","30","-c:a","aac","-ar","48000","-ac","2",f"{S}/emain.mp4"])
im=Image.new("RGB",(W,H),(24,22,20)); d=ImageDraw.Draw(im)
ctext(d,200,"SOLA",font(ARB,120),(255,255,255)); ctext(d,350,"Stay cold. Keep running.",font(AR,44),(230,230,230))
bw,bh=420,84; x0=(W-bw)/2; d.rounded_rectangle([x0,470,x0+bw,470+bh],22,fill=(217,119,87)); ctext(d,490,"Pre-order today",font(ARB,40),(255,255,255))
im.save(f"{S}/eend.png")
run(["-loop","1","-t","3","-i",f"{S}/eend.png","-f","lavfi","-t","3","-i","anullsrc=r=48000:cl=stereo",
     "-c:v","libx264","-pix_fmt","yuv420p","-r","30","-c:a","aac","-shortest",f"{S}/eend.mp4"])
open(f"{S}/elist.txt","w").write(f"file '{S}/emain.mp4'\nfile '{S}/eend.mp4'\n")
run(["-f","concat","-safe","0","-i",f"{S}/elist.txt","-c","copy","-movflags","+faststart",f"{V}/t1-engaging-18s.mp4"])
run(["-ss","1","-i",f"{V}/t1-engaging-18s.mp4","-frames:v","1",f"{V}/t1-engaging-poster.jpg"])
print("done")
