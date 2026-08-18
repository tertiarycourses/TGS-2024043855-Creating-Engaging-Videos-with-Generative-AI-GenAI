#!/usr/bin/env python3
"""Generate the labs/ tree — ONE FOLDER PER LAB (labs/lab-NN-slug/README.md),
plus a labs/README.md index, all from the same single source as the deck/LP/LG."""
import os, sys, shutil
HERE=os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0,HERE)
import course_data as C
from data_domain1 import DOMAIN1; from data_domain2 import DOMAIN2
from data_domain3 import DOMAIN3
ACT=DOMAIN1+DOMAIN2+DOMAIN3

def _find_repo(start):
    env=os.environ.get("COURSE_REPO")
    if env and os.path.isdir(env): return env
    d=start
    for _ in range(8):
        d=os.path.dirname(d)
        if os.path.isdir(os.path.join(d,"courseware")) and os.path.isdir(os.path.join(d,"labs")): return d
    return os.path.dirname(os.path.dirname(HERE))
REPO=_find_repo(HERE)
LABS=os.path.join(REPO,"labs")

def _slug(t):
    import re as _re
    s="".join(ch.lower() if ch.isalnum() else "-" for ch in t)
    return _re.sub(r"-+","-",s).strip("-")[:48].rstrip("-")

TOPICS={t["num"]:t for t in C.TOPICS}

# wipe stale lab folders/files (regenerated fully from source)
for entry in os.listdir(LABS):
    path=os.path.join(LABS,entry)
    if entry.startswith("lab-") and os.path.isdir(path): shutil.rmtree(path)
    elif entry in ("README.md",) or (entry.startswith("lab-") and entry.endswith(".md")):
        os.remove(path)

index=[f"# {C.TITLE} — Hands-On Labs","",
       f"**WSQ Course Code:** {C.COURSE_CODE} · **Version {C.VERSION} · {C.VERSION_DATE}**","",
       "Each lab lives in its own folder with a README carrying the full procedure, "
       "the GenAI prompts, and the success check. Detailed narrative instructions are in the "
       "Learner Guide; the slides carry only each lab's overview.","",
       "## The GenAI video pipeline",""]
for i,(lbl,det) in enumerate(C.PIPELINE,1):
    index.append(f"{i}. **{lbl}** — {det}")
index+=["","## Labs",""]

for t in C.TOPICS:
    index.append(f"### Topic {t['code']} — {t['title']}")
    index.append("")
    for a in [x for x in ACT if x["topic"]==t["num"]]:
        folder=f"lab-{a['num']:02d}-{_slug(a['title'])}"
        index.append(f"- [Lab {a['num']} — {a['title']}]({folder}/README.md)")
        os.makedirs(os.path.join(LABS,folder),exist_ok=True)
        md=[f"# Lab {a['num']} — {a['title']}","",
            f"**Topic {t['code']}:** {t['title']}  ",
            f"**Maps to:** {a['objective']}  ",
            f"**Tools:** {a['services']}","",
            "## Goal","",a["desc"],"",
            "## What you'll build","",a["build"],""]
        if a.get("prompts"):
            md+=["## Prompts",""]
            for lbl,ptext in a["prompts"]:
                md+=[f"**{lbl}**","","```prompt",ptext,"```",""]
        md+=["## Step-by-step",""]
        for i,(instr,cmd) in enumerate(a["steps"],1):
            md.append(f"{i}. {instr}")
            if cmd: md+=["","   ```","   "+cmd,"   ```",""]
        md+=["","## Check your work","",a["test"],"",
             "---",
             f"*{C.ORG} · {C.COURSE_CODE} · {C.VERSION}*",""]
        with open(os.path.join(LABS,folder,"README.md"),"w") as f:
            f.write("\n".join(md))
    index.append("")

with open(os.path.join(LABS,"README.md"),"w") as f:
    f.write("\n".join(index))
print(f"Wrote {len(ACT)} lab folders + index under {LABS}")
