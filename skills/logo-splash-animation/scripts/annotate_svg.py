#!/usr/bin/env python3
"""annotate_svg.py - turn a flat logo SVG into an animated splash HTML page.

  python annotate_svg.py logo.svg splash.html [--total 3.2] [--bg "#FBF9EF"] [--title "Name"] [--scan]

Every shape becomes a stroke "draw-on" (pathLength=1) or a hard "pop" (fills).
Shapes with both fill and stroke are split: fill pops, stroke draws.
Delay order = document order, so write the SVG in construction order
(structure -> measurement -> signal -> accent). Reorder the SVG, not this script.
"""
import argparse, copy, pathlib, re
import xml.etree.ElementTree as ET

NS = "http://www.w3.org/2000/svg"
ET.register_namespace("", NS)
SHAPES = {"path", "rect", "circle", "ellipse", "line", "polyline", "polygon"}
SKIP = {"defs", "clipPath", "mask", "symbol"}
INH = ("fill", "stroke", "stroke-width")

def tag(e): return e.tag.split("}")[-1]

def collect(e, inh, parent, out):
    if tag(e) in SKIP: return
    cur = dict(inh)
    for k in INH:
        if k in e.attrib: cur[k] = e.attrib[k]
    if tag(e) in SHAPES: out.append((e, cur, parent))
    for c in list(e): collect(c, cur, e, out)

def none(v): return v is None or v.lower() in ("none", "transparent")

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("svg"); ap.add_argument("out")
    ap.add_argument("--total", type=float, default=3.2, help="seconds until the last element lands")
    ap.add_argument("--bg", default="#FBF9EF"); ap.add_argument("--title", default="Logo")
    ap.add_argument("--scan", action="store_true", help="add one scanline sweep at the end")
    a = ap.parse_args()

    root = ET.parse(a.svg).getroot()
    shapes = []; collect(root, {}, None, shapes)
    n = len(shapes)
    step = min(0.08, (a.total * 0.7) / max(n, 1))
    dur = max(0.35, a.total * 0.2)
    last = 0.0

    for i, (e, cur, parent) in enumerate(shapes):
        t = round(i * step, 3); last = max(last, t + dur)
        fill = cur.get("fill", "#000"); stroke = cur.get("stroke", "none")
        has_fill, has_stroke = not none(fill), not none(stroke)
        e.set("fill", fill); e.set("stroke", stroke)
        if "stroke-width" in cur: e.set("stroke-width", cur["stroke-width"])
        if has_fill and has_stroke:
            twin = copy.deepcopy(e); twin.set("stroke", "none")
            twin.set("class", "pop"); twin.set("style", f"--t:{t}s")
            parent.insert(list(parent).index(e), twin)
            e.set("fill", "none"); has_fill = False
        if has_stroke:
            e.set("class", "draw"); e.set("pathLength", "1"); e.set("style", f"--t:{t}s;--d:{dur:.2f}s")
            if tag(e) == "circle":
                tr = f'rotate(-90 {e.get("cx","0")} {e.get("cy","0")})'
                e.set("transform", (e.get("transform", "") + " " + tr).strip())
        elif has_fill:
            e.set("class", "pop"); e.set("style", f"--t:{t}s")

    vb = [float(x) for x in root.get("viewBox").split()]
    scan_at = round(last + 0.1, 2)
    if a.scan:
        stroke_color = next((c.get("stroke") for _, c, _ in shapes if not none(c.get("stroke"))), "#000")
        r = ET.SubElement(root, f"{{{NS}}}rect", {"class": "scan", "x": str(vb[0]), "y": str(vb[1] - 1),
            "width": str(vb[2]), "height": "3", "fill": stroke_color, "style": f"--travel:{vb[3]}px"})
        last = scan_at + 1.0
    for k in ("width", "height"): root.attrib.pop(k, None)
    root.set("overflow", "visible")

    svg = ET.tostring(root, encoding="unicode")
    html = pathlib.Path(__file__).resolve().parent.parent.joinpath("assets", "splash-template.html").read_text()
    for k, v in {"{{SVG}}": svg, "{{BG}}": a.bg, "{{TITLE}}": a.title,
                 "{{SCAN_AT}}": str(scan_at), "{{DONE_MS}}": str(int((last + 0.2) * 1000))}.items():
        html = html.replace(k, v)
    pathlib.Path(a.out).write_text(html)
    print(f"{n} shapes, ~{last:.1f}s, wrote {a.out}")

if __name__ == "__main__": main()
