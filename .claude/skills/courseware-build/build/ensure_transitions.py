#!/usr/bin/env python3
"""Every slide in every Tertiary deck gets a slide transition, in the right schema place.

User rule (9 Nov 2026): always add a slide transition effect to ALL slides of every PPT.

    python3 ensure_transitions.py deck.pptx            # fix in place: add missing, reorder misplaced
    python3 ensure_transitions.py deck.pptx --check    # QA gate: exit 1 if any slide fails
    python3 ensure_transitions.py deck.pptx --kind push --speed med   # change the default added

What it enforces on each ppt/slides/slideN.xml:
  1. a transition exists (p:transition, or mc:AlternateContent wrapping one, as PowerPoint writes
     for 2010+ effects); missing -> a `fade` (speed fast, advClick=1) is added;
  2. it sits in schema order  cSld, clrMapOvr, TRANSITION, timing, extLst.  A transition written
     after p:timing makes PowerPoint discard the timing, so click-to-play videos and click builds
     silently stop working (TGS-2024043855 v9: every embedded video showed only its poster);
  3. no auto-advance (advTm) and no transition sound; trainer stays in control.
Existing transitions keep their effect; only their position and the auto-advance/sound are fixed.
"""
import argparse, shutil, sys, tempfile, zipfile, re
from lxml import etree

P = "http://schemas.openxmlformats.org/presentationml/2006/main"
MC = "http://schemas.openxmlformats.org/markup-compatibility/2006"
q = lambda ns, t: "{%s}%s" % (ns, t)
SLIDE = re.compile(r"^ppt/slides/slide\d+\.xml$")


def _is_transition(el):
    if el.tag == q(P, "transition"):
        return True
    if el.tag == q(MC, "AlternateContent"):
        return el.find(".//" + q(P, "transition")) is not None
    return False


def inspect(root):
    """-> (has_transition, in_order, problems list)."""
    kids = list(root)
    trs = [i for i, k in enumerate(kids) if _is_transition(k)]
    tim = [i for i, k in enumerate(kids) if k.tag in (q(P, "timing"), q(P, "extLst"))]
    probs = []
    if not trs:
        probs.append("no transition")
    elif tim and min(trs) > min(tim):
        probs.append("transition after p:timing/extLst (PowerPoint drops the timing)")
    for t in root.iter(q(P, "transition")):
        if t.get("advTm"):
            probs.append("auto-advance advTm=%s" % t.get("advTm"))
        if t.find(q(P, "sndAc")) is not None:
            probs.append("transition sound")
    return probs


def fix(root, kind="fade", speed="fast"):
    trs = [k for k in root if _is_transition(k)]
    if not trs:
        tr = etree.Element(q(P, "transition"))
        tr.set("spd", speed); tr.set("advClick", "1")
        el = etree.SubElement(tr, q(P, kind))
        if kind == "push":
            el.set("dir", "l")
        trs = [tr]
    for t in trs:                      # detach, re-insert before timing/extLst
        if t.getparent() is not None:
            root.remove(t)
    anchor = root.find(q(P, "timing"))
    if anchor is None:
        anchor = root.find(q(P, "extLst"))
    for t in trs:
        if anchor is not None:
            anchor.addprevious(t)
        else:
            root.append(t)
    for t in root.iter(q(P, "transition")):
        t.attrib.pop("advTm", None)
        t.set("advClick", "1")
        for s in t.findall(q(P, "sndAc")):
            t.remove(s)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("pptx")
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--kind", default="fade", choices=["fade", "push"])
    ap.add_argument("--speed", default="fast", choices=["fast", "med", "slow"])
    a = ap.parse_args()

    zin = zipfile.ZipFile(a.pptx)
    names = sorted((n for n in zin.namelist() if SLIDE.match(n)),
                   key=lambda n: int(re.findall(r"\d+", n)[-1]))
    bad = {}
    for n in names:
        p = inspect(etree.fromstring(zin.read(n)))
        if p:
            bad[n] = p
    if a.check:
        for n, p in bad.items():
            print("FAIL %s: %s" % (n.split("/")[-1], "; ".join(p)))
        print("%d/%d slides pass the transition gate" % (len(names) - len(bad), len(names)))
        sys.exit(1 if bad else 0)
    if not bad:
        print("all %d slides already have a correctly placed transition" % len(names)); return
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".pptx").name
    with zipfile.ZipFile(tmp, "w", zipfile.ZIP_DEFLATED) as zout:
        for item in zin.infolist():
            data = zin.read(item.filename)
            if item.filename in bad:
                root = etree.fromstring(data)
                fix(root, a.kind, a.speed)
                data = etree.tostring(root, xml_declaration=True, encoding="UTF-8", standalone=True)
            zout.writestr(item, data)
    zin.close()
    shutil.move(tmp, a.pptx)
    print("fixed %d of %d slides" % (len(bad), len(names)))


if __name__ == "__main__":
    main()
