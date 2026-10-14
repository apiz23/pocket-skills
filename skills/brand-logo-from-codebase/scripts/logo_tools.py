#!/usr/bin/env python3
"""logo_tools.py - lint a logo SVG against brand rules, or emit colorway files.

  python logo_tools.py lint logo.svg [--palette "#2E4FC4,#FBF9EF,#D3D8E8,#F5C842,#1B1E28"] [--allow-radius]
  python logo_tools.py colorways logo.svg outdir \
      [--src "fg=#2E4FC4,bg=#FBF9EF,hl=#D3D8E8,acc=#F5C842"] \
      [--to  "fg=#2E4FC4,bg=#FBF9EF,hl=#D3D8E8,acc=#F5C842,ink=#1B1E28"]

--src = the colors used inside the SVG now. --to = the brand palette to emit.
Produces: ink-on-paper, brand-on-paper, reversed-on-brand, flat (single color, transparent).
"""
import re, sys, argparse, pathlib
import xml.etree.ElementTree as ET

def tag(e): return e.tag.split("}")[-1]
def kv(s): return dict(p.split("=") for p in s.split(",") if p)

def lint(path, palette, allow_radius):
    root = ET.parse(path).getroot()
    problems = []
    allowed = {c.lower() for c in palette} | {"none", "currentcolor", "transparent"}
    for e in root.iter():
        t = tag(e)
        if t in ("filter", "feGaussianBlur", "feDropShadow", "linearGradient", "radialGradient", "mask"):
            problems.append(f"<{t}> not allowed (flat vector only)")
        if t == "text":
            problems.append("<text> found - logo mark must be text-free (outline it or remove)")
        if t == "image":
            problems.append("<image> found - raster content not allowed")
        if t == "rect" and not allow_radius:
            for a in ("rx", "ry"):
                if e.get(a) not in (None, "0"):
                    problems.append(f"rect with {a}={e.get(a)} (rounded corner)")
        for a in ("stroke-linecap", "stroke-linejoin"):
            if e.get(a) == "round":
                problems.append(f"{a}=round on <{t}> (rounded ends)")
        st = e.get("style", "")
        if "shadow" in st or "blur" in st or "filter" in st:
            problems.append(f"style on <{t}> contains shadow/blur/filter")
        for a in ("fill", "stroke"):
            v = e.get(a)
            if v and v.lower() not in allowed and not v.startswith("url("):
                problems.append(f"{a}={v} not in palette")
    if not root.get("viewBox"):
        problems.append("missing viewBox")
    print("PASS" if not problems else "FAIL")
    for p in sorted(set(problems)):
        print(" -", p)
    return 0 if not problems else 1

def add_bg(svg, color):
    m = re.search(r'viewBox="([\d.\-]+) ([\d.\-]+) ([\d.\-]+) ([\d.\-]+)"', svg)
    x, y, w, h = m.groups()
    rect = f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{color}"/>'
    return re.sub(r"(<svg[^>]*>)", lambda mo: mo.group(1) + rect, svg, count=1)

def colorways(path, outdir, src, to):
    text = pathlib.Path(path).read_text()
    s = {"fg": "#2E4FC4", "bg": "#FBF9EF", "hl": "#D3D8E8", "acc": "#F5C842"} | kv(src)
    t = {"ink": "#1B1E28", **s} | kv(to)
    out = pathlib.Path(outdir); out.mkdir(parents=True, exist_ok=True)
    def emit(name, fg, bg, hl, acc, bgrect):
        svg = text
        for old, tok in ((s["fg"], "@FG@"), (s["bg"], "@BG@"), (s["hl"], "@HL@"), (s["acc"], "@AC@")):
            svg = re.sub(re.escape(old), tok, svg, flags=re.I)
        svg = svg.replace("@FG@", fg).replace("@BG@", bg).replace("@HL@", hl).replace("@AC@", acc)
        if bgrect: svg = add_bg(svg, bgrect)
        (out / f"{name}.svg").write_text(svg); print("wrote", out / f"{name}.svg")
    emit("ink-on-paper", t["ink"], t["bg"], t["hl"], t["acc"], t["bg"])
    emit("brand-on-paper", t["fg"], t["bg"], t["hl"], t["acc"], t["bg"])
    emit("reversed-on-brand", t["bg"], t["fg"], t["fg"], t["acc"], t["fg"])
    emit("flat", t["ink"], t["bg"], t["bg"], t["bg"], None)

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    l = sub.add_parser("lint"); l.add_argument("svg"); l.add_argument("--palette", default="#2E4FC4,#FBF9EF,#D3D8E8,#F5C842,#1B1E28"); l.add_argument("--allow-radius", action="store_true")
    c = sub.add_parser("colorways"); c.add_argument("svg"); c.add_argument("outdir"); c.add_argument("--src", default=""); c.add_argument("--to", default="")
    a = ap.parse_args()
    if a.cmd == "lint": sys.exit(lint(a.svg, a.palette.split(","), a.allow_radius))
    else: colorways(a.svg, a.outdir, a.src, a.to)
