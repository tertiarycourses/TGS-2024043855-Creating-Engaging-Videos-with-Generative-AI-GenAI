#!/usr/bin/env python3
"""Generate the labs/ tree from the single source — ONE FOLDER PER LAB, no Markdown:

  labs/index.html                     lab home page (sign-up link + every lab)
  labs/lab-NN-slug/README.pdf         overview, steps, assets, evidence, check
  labs/lab-NN-slug/prompts.html       prompt link page: one-click Copy per prompt
  labs/lab-NN-slug/prompts.pdf        the same prompts, printable
  labs/lab-NN-slug/assets/            mock files (PDF / CSV / JPG frames)

PDFs are printed from HTML with headless Chrome.
"""
import os, sys, re, csv, html, shutil, subprocess, tempfile
HERE=os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0,HERE)
import course_data as C
from data_domain1 import DOMAIN1; from data_domain2 import DOMAIN2; from data_domain3 import DOMAIN3
from lab_assets import ASSETS
ACT=DOMAIN1+DOMAIN2+DOMAIN3
CHROME="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

def _find_repo(start):
    env=os.environ.get("COURSE_REPO")
    if env and os.path.isdir(env): return env
    d=start
    for _ in range(8):
        d=os.path.dirname(d)
        if os.path.isdir(os.path.join(d,"courseware")) and os.path.isdir(os.path.join(d,"labs")): return d
    return os.path.dirname(os.path.dirname(HERE))
REPO=_find_repo(HERE); LABS=os.path.join(REPO,"labs"); VID=os.path.join(REPO,"courseware","assets","videos")
LOGO=os.path.join(os.path.dirname(HERE),"assets","tertiary-infotech-logo.png")

def _slug(t):
    s="".join(ch.lower() if ch.isalnum() else "-" for ch in t)
    return re.sub(r"-+","-",s).strip("-")[:48].rstrip("-")
def folder(a): return f"lab-{a['num']:02d}-{_slug(a['title'])}"
E=html.escape

CSS="""
*{box-sizing:border-box} body{font-family:Arial,Helvetica,sans-serif;color:#161B26;margin:0;background:#fff;font-size:11pt;line-height:1.45}
.wrap{max-width:900px;margin:0 auto;padding:28px 34px}
.top{display:flex;align-items:center;gap:14px;border-bottom:3px solid #1F6FEB;padding-bottom:10px;margin-bottom:16px}
.top img{height:44px} .kick{color:#1F6FEB;font-weight:700;font-size:9.5pt;letter-spacing:.5px;text-transform:uppercase}
h1{font-size:20pt;margin:2px 0 4px} h2{font-size:13.5pt;color:#1F6FEB;margin:20px 0 6px} h3{font-size:11.5pt;margin:14px 0 4px}
.meta{color:#5B6372;font-size:9.5pt} .box{background:#F5F8FC;border-left:5px solid #10B981;padding:10px 14px;margin:10px 0}
.warn{background:#FFF7E6;border-left:5px solid #F59E0B;padding:10px 14px;margin:10px 0;font-size:10pt}
ol.steps li{margin:0 0 7px} table{border-collapse:collapse;width:100%;margin:8px 0;font-size:9.5pt}
th{background:#1F6FEB;color:#fff;text-align:left;padding:6px} td{border:1px solid #E2E8F0;padding:6px;vertical-align:top;height:22px}
.prompt{border:1px solid #E2E8F0;border-radius:8px;margin:12px 0;overflow:hidden;page-break-inside:avoid}
.prompt .ph{background:#F5F8FC;display:flex;justify-content:space-between;align-items:center;padding:7px 12px;border-left:5px solid #7C3AED}
.prompt .ph b{color:#7C3AED;font-size:9.5pt;text-transform:uppercase}
.prompt pre{margin:0;background:#0B1220;color:#9CDCFE;padding:12px 14px;white-space:pre-wrap;font-family:Menlo,Consolas,monospace;font-size:9.5pt}
button.copy{background:#7C3AED;color:#fff;border:0;border-radius:6px;padding:5px 12px;font-weight:700;cursor:pointer}
button.copy.done{background:#10B981} .blank{color:#5B6372;margin:6px 0}
.card{border:1px solid #E2E8F0;border-left:5px solid #1F6FEB;border-radius:6px;padding:10px 14px;margin:10px 0}
.card a{color:#1F6FEB;font-weight:700;text-decoration:none} .foot{color:#5B6372;font-size:8.5pt;margin-top:24px;border-top:1px solid #E2E8F0;padding-top:8px}
@media print{button.copy{display:none} .wrap{padding:10px 18px}}
"""
COPYJS="""<script>
document.querySelectorAll('button.copy').forEach(b=>b.addEventListener('click',()=>{
 const t=document.getElementById(b.dataset.t).innerText;
 navigator.clipboard.writeText(t).then(()=>{b.textContent='Copied ✓';b.classList.add('done');
 setTimeout(()=>{b.textContent='Copy';b.classList.remove('done')},1800)});}));
</script>"""

def page(title,kicker,body,logo_rel,js=False):
    return (f"<!DOCTYPE html><html lang='en'><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'>"
            f"<title>{E(title)}</title><style>{CSS}</style></head><body><div class='wrap'>"
            f"<div class='top'><img src='{logo_rel}' alt='Tertiary Infotech'><div><div class='kick'>{E(kicker)}</div>"
            f"<div class='meta'>{E(C.TITLE)} · {C.COURSE_CODE} · {C.VERSION} · {C.VERSION_DATE}</div></div></div>"
            f"{body}<div class='foot'>© 2026 {E(C.ORG)}. Labs run in Higgsfield (higgsfield.ai). "
            f"Sign up: <a href='{C.HF_SIGNUP}'>{E(C.HF_SIGNUP_SHORT)}</a> — {E(C.HF_DISCLOSURE)}</div></div>"
            f"{COPYJS if js else ''}</body></html>")

def to_pdf(html_path,pdf_path):
    subprocess.run([CHROME,"--headless=new","--disable-gpu","--no-pdf-header-footer",
                    f"--print-to-pdf={pdf_path}","file://"+html_path],check=True,
                   stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)

def prompts_body(a):
    out=[f"<h1>Lab {a['num']} — {E(a['title'])}</h1><p class='meta'>Copy-and-adapt prompts. Click <b>Copy</b>, paste into Higgsfield, replace anything in &lt;angle brackets&gt;.</p>"]
    for i,(lab,t) in enumerate(a.get("prompts",[])):
        out.append(f"<div class='prompt'><div class='ph'><b>Prompt {i+1} — {E(lab)}</b>"
                   f"<button class='copy' data-t='p{i}'>Copy</button></div><pre id='p{i}'>{E(t)}</pre></div>")
    out.append("<div class='warn'>Draft first: generate on Seedance 2.5 Draft (480p, about "
               f"{C.CREDITS['draft15']} credits for 15 s) and finalise only the take you keep (about {C.CREDITS['hd15']} credits at 1080p).</div>")
    return "".join(out)

def readme_body(a):
    t=next(x for x in C.TOPICS if x["num"]==a["topic"])
    b=[f"<h1>Lab {a['num']} — {E(a['title'])}</h1>",
       f"<p class='meta'>Topic {t['code']} · {E(t['title'])} · Maps to: {E(a['objective'])}</p>",
       f"<p>{E(a['desc'])}</p>",
       f"<div class='box'><b>You'll build:</b> {E(a['build'])}<br><b>Tools:</b> {E(a['services'])}</div>"]
    if a["num"]==1:
        b.append(f"<div class='warn'><b>Sign up:</b> {E(C.HF_SIGNUP)} — {E(C.HF_DISCLOSURE)}<br>{E(C.HF_PLAN_NOTE)}</div>")
    b.append("<h2>Steps</h2><ol class='steps'>"+"".join(f"<li>{E(s)}</li>" for s,_ in a["steps"])+"</ol>")
    b.append("<h2>Prompts</h2><p>Open <b>prompts.html</b> in this folder for one-click copy (or prompts.pdf to print).</p>")
    for lab,tx in a.get("prompts",[]):
        b.append(f"<div class='prompt'><div class='ph'><b>{E(lab)}</b></div><pre>{E(tx)}</pre></div>")
    if a.get("assets"):
        b.append("<h2>Mock assets (assets/)</h2><ul>"+"".join(f"<li>{E(x)}</li>" for x in a["assets"])+"</ul>")
    if a.get("evidence"):
        b.append("<h2>Evidence to keep</h2><p>Screenshot these. The Practical Performance asks you to paste screenshots like them under each task.</p><ul>"+
                 "".join(f"<li>{E(x)}</li>" for x in a["evidence"])+"</ul>")
    b.append(f"<h2>Check your work</h2><div class='box'>{E(a['test'])}</div>")
    return "".join(b)

def make_asset(path,spec,tmp):
    kind=spec[0]
    if kind=="csv":
        with open(path,"w",newline="") as f: csv.writer(f).writerows(spec[1])
    elif kind=="frame":
        vid,sec=spec[1]
        subprocess.run(["ffmpeg","-v","error","-y","-ss",str(sec),"-i",os.path.join(VID,vid),"-frames:v","1",
                        "-vf","scale=1280:-2","-q:v","2",path],check=True)
    elif kind=="copy":
        shutil.copy(os.path.join(VID,spec[1]),path)
    elif kind=="pdf":
        _,title,blocks=spec
        h=os.path.join(tmp,os.path.basename(path)+".html")
        open(h,"w").write(page(title,"LAB ASSET",f"<h1>{E(title)}</h1>"+"".join(blocks),"file://"+LOGO))
        to_pdf(h,path)

def main():
    os.makedirs(LABS,exist_ok=True)
    for e in os.listdir(LABS):           # regenerate fully from source
        p=os.path.join(LABS,e)
        if e.startswith("lab-") and os.path.isdir(p): shutil.rmtree(p)
        elif e.endswith((".md",".html",".pdf")): os.remove(p)
    shutil.copy(LOGO,os.path.join(LABS,"logo.png"))
    tmp=tempfile.mkdtemp()
    for a in ACT:
        d=os.path.join(LABS,folder(a)); os.makedirs(os.path.join(d,"assets"),exist_ok=True)
        ph=os.path.join(d,"prompts.html")
        open(ph,"w").write(page(f"Lab {a['num']} prompts",f"LAB {a['num']} · PROMPT PAGE",prompts_body(a),"../logo.png",js=True))
        to_pdf(ph,os.path.join(d,"prompts.pdf"))
        rh=os.path.join(tmp,f"readme{a['num']}.html")
        open(rh,"w").write(page(f"Lab {a['num']}",f"LAB {a['num']} · INSTRUCTIONS",readme_body(a),"file://"+LOGO))
        to_pdf(rh,os.path.join(d,"README.pdf"))
        for fn,spec in ASSETS.get(a["num"],{}).items():
            make_asset(os.path.join(d,"assets",fn),spec,tmp)
        print("built",folder(a),sorted(os.listdir(os.path.join(d,"assets"))))
    # home page
    cards=[]
    for t in C.TOPICS:
        cards.append(f"<h2>Topic {t['code']} — {E(t['title'])}</h2>")
        for a in [x for x in ACT if x["topic"]==t["num"]]:
            f=folder(a)
            cards.append(f"<div class='card'><b>Lab {a['num']} — {E(a['title'])}</b><br><span class='meta'>{E(a['build'])}</span><br>"
                         f"<a href='{f}/prompts.html'>Prompts (one-click copy)</a> · <a href='{f}/README.pdf'>Instructions PDF</a> · "
                         f"<a href='{f}/prompts.pdf'>Prompts PDF</a> · <a href='{f}/assets/'>Mock assets</a></div>")
    body=(f"<h1>Labs — {E(C.TITLE)}</h1><p>Ten hands-on labs, all inside Higgsfield — Lab 10 is your mini capstone. Every prompt is also on <a href='prompts.html'>one copy page</a>.</p>"
          f"<div class='warn'><b>Step 0 — sign up:</b> <a href='{C.HF_SIGNUP}'>{E(C.HF_SIGNUP_SHORT)}</a>. {E(C.HF_DISCLOSURE)}<br>{E(C.HF_PLAN_NOTE)}</div>"
          +"".join(cards)
          +f"<h2>References</h2><div class='card'>"
           f"<a href='{C.HF_DOCS}'>Higgsfield API docs</a> · <a href='https://higgsfield.ai/supercomputer-intro'>Supercomputer and Skills</a></div>")
    open(os.path.join(LABS,"index.html"),"w").write(page("Labs","LAB HOME",body,"logo.png"))
    # one page with every prompt: search + one-click copy
    parts=["<h1>All prompts — copy and paste into Higgsfield</h1>",
           "<p class='meta'>Type in the box to filter. Click <b>Copy</b>, paste into Higgsfield (Supercomputer or Cinema Studio), "
           "replace anything in &lt;angle brackets&gt;. Test on Seedance 2.5 Draft first.</p>",
           "<input id='q' placeholder='Search prompts, e.g. Elements, bar scene, soundtrack' "
           "style='width:100%;padding:10px 12px;font-size:12pt;border:1px solid #E8E5DE;border-radius:8px;margin:6px 0 10px'>"]
    k=0
    for t in C.TOPICS:
        parts.append(f"<h2>Topic {t['code']} — {E(t['title'])}</h2>")
        for a in [x for x in ACT if x["topic"]==t["num"]]:
            parts.append(f"<h3 class='labh'>Lab {a['num']} — {E(a['title'])} · <a href='{folder(a)}/README.pdf'>instructions</a></h3>")
            for lab,tx in a.get("prompts",[]):
                parts.append(f"<div class='prompt' data-s='{E((a['title']+' '+lab+' '+tx).lower())}'><div class='ph'><b>Lab {a['num']} · {E(lab)}</b>"
                             f"<button class='copy' data-t='a{k}'>Copy</button></div><pre id='a{k}'>{E(tx)}</pre></div>"); k+=1
    filt="""<script>document.getElementById('q').addEventListener('input',e=>{const v=e.target.value.toLowerCase();
document.querySelectorAll('.prompt').forEach(p=>{p.style.display=p.dataset.s.includes(v)?'':'none'});});</script>"""
    open(os.path.join(LABS,"prompts.html"),"w").write(page("All prompts","ALL PROMPTS · ONE-CLICK COPY","".join(parts),"logo.png",js=True).replace("</body>",filt+"</body>"))
    print(f"labs/prompts.html written ({k} prompts)")
    shutil.rmtree(tmp)
    print("labs/index.html written")

if __name__=="__main__":
    main()
