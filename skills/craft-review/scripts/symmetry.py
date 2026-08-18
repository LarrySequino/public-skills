#!/usr/bin/env python3
"""
symmetry.py — measure paired-component consistency, grid adherence, and (opt-in) centering
from Figma geometry. Deterministic checks so the review computes instead of eyeballing.

Feed it a JSON of frames and their children (absolute x/y/w/h bounds, exactly what
`get_metadata` / `get_design_context` return). It computes each frame's inner padding from the
bounding box of its children and flags, without false positives:

  1. PAIRED-COMPONENT MISMATCH (strongest): frames listed in "pairs" whose content insets differ
     — the classic "two cards with unequal padding" finding. Compares left & top insets.
  2. GRID ADHERENCE: left inset, top inset, width, and height that aren't on the grid
     (multiple of grid_base; 4pt allowed as a "fine" polish note).
  3. CENTERING (opt-in): a frame with "expect": "center" | "center-h" | "center-v" whose content
     isn't actually centered in its box. Only checked when you assert the intent, so left-aligned
     text is never wrongly flagged.

Right/bottom "leftover" space is measured and shown but NOT auto-flagged (it's usually intentional
whitespace for top-left-anchored content), except under an explicit "expect".

Usage:
    python3 symmetry.py page.html                  # HTML mock, real layout via headless Chromium
    python3 symmetry.py page.html --viewport 390,844   # same mock at a phone width
    python3 symmetry.py geometry.json              # Figma geometry (get_metadata output)
    python3 symmetry.py --demo

Both sources land in the same schema, so the analysis is identical. HTML mocks
declare derived_sizes, so they are checked on insets only: the engine computes
width and height from the container, and grid-checking those reports the
viewport rather than a decision.

JSON schema:
{
  "grid_base": 8,                # optional, default 8
  "tolerance": 1,                # optional px slack, default 1
  "frames": [
    { "name": "GO card",
      "bounds": {"x": 40, "y": 900, "w": 300, "h": 120},
      "expect": "center-h",      # optional: center | center-h | center-v
      "children": [ {"name": "GO", "bounds": {"x": 52, "y": 924, "w": 60, "h": 24}} ] }
  ],
  "pairs": [ ["GO card", "Loud Ring card"] ]     # optional
}
"""
import sys
import json
import re
from pathlib import Path



def _chromium():
    """Any cached headless Chromium. Nothing is installed for this; it reuses what
    playwright or a Chrome install already put on disk."""
    import glob
    pats = [
        str(Path.home()) + "/Library/Caches/ms-playwright/chromium_headless_shell-*/*/chrome-headless-shell",
        str(Path.home()) + "/Library/Caches/ms-playwright/chromium-*/*/Chromium.app/Contents/MacOS/Chromium",
        "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
        "/Applications/Chromium.app/Contents/MacOS/Chromium",
        "/usr/bin/chromium", "/usr/bin/chromium-browser", "/usr/bin/google-chrome",
    ]
    for pat in pats:
        hits = sorted(glob.glob(pat))
        if hits:
            return hits[-1]
    return None


def geometry_from_html(src, viewport="1440,900"):
    """Render the page and collect boxes. CSS has no geometry until a layout engine
    runs, so this is the only honest way to measure an HTML mock."""
    import subprocess
    import tempfile
    import html as _html

    chrome = _chromium()
    if not chrome:
        sys.exit("no headless Chromium found. Install one, e.g. `npx playwright install chromium`.")
    collector = Path(__file__).resolve().parent / "collect-boxes.js"
    if not collector.exists():
        sys.exit(f"missing {collector}")

    is_url = src.startswith(("http://", "https://"))
    page = Path(src).resolve() if not is_url else None
    if not is_url and not page.exists():
        sys.exit(f"no such file: {src}")
    doc = "" if is_url else page.read_text(errors="ignore")

    inject = ("<pre id=\"__boxes\"></pre><script>" + collector.read_text() +
              "\nwindow.addEventListener('load',function(){"
              "document.getElementById('__boxes').textContent=JSON.stringify(collectBoxes());});</script>")

    # write the instrumented copy beside the original so relative assets still resolve
    tmpdir = None
    if is_url:
        sys.exit("URL input needs the page saved locally first; pass the .html file.")
    target = page.with_name("._symmetry_" + page.name)
    target.write_text(doc.replace("</body>", inject + "</body>") if "</body>" in doc else doc + inject)
    try:
        out = subprocess.run(
            [chrome, "--headless", "--disable-gpu", f"--window-size={viewport}",
             "--virtual-time-budget=5000", "--dump-dom", target.as_uri()],
            capture_output=True, text=True, timeout=90).stdout
    finally:
        target.unlink(missing_ok=True)
        if tmpdir:
            tmpdir.cleanup()

    m = re.search(r'<pre id="__boxes">(.*?)</pre>', out, re.S)
    if not m or not m.group(1).strip():
        sys.exit("collector produced nothing. Is the page valid HTML with a <body>?")
    return json.loads(_html.unescape(m.group(1)))


def _b(o):
    b = o["bounds"]
    return b["x"], b["y"], b["w"], b["h"]


def padding(frame):
    fx, fy, fw, fh = _b(frame)
    kids = frame.get("children") or []
    if not kids:
        return None
    xs0 = [_b(k)[0] for k in kids]
    ys0 = [_b(k)[1] for k in kids]
    xs1 = [_b(k)[0] + _b(k)[2] for k in kids]
    ys1 = [_b(k)[1] + _b(k)[3] for k in kids]
    return {
        "left": round(min(xs0) - fx, 1),
        "right": round((fx + fw) - max(xs1), 1),
        "top": round(min(ys0) - fy, 1),
        "bottom": round((fy + fh) - max(ys1), 1),
    }


def off_grid(value, base, fine=4):
    v = abs(round(value))
    if v == 0 or v % base == 0:
        return False
    return "fine" if v % fine == 0 else True


SEV_ICON = {"CRITICAL": "🔴", "MAJOR": "🟠", "MINOR": "🟡", "POLISH": "🔵"}


def analyze(data):
    base = data.get("grid_base", 8)
    tol = data.get("tolerance", 1)
    frames = {f["name"]: f for f in data.get("frames", [])}
    findings = []
    pads = {}

    for name, f in frames.items():
        p = padding(f)
        pads[name] = p
        if not p:
            continue

        # (2) grid adherence — only meaningful values: left/top insets, width, height.
        # A source with derived_sizes (HTML, where the engine computes width and height
        # from the container and the content) gets insets only: a derived size reports
        # the viewport, not a decision, and grid-checking it is pure noise.
        _, _, fw, fh = _b(f)
        checks = {"left inset": p["left"], "top inset": p["top"]}
        if not data.get("derived_sizes"):
            checks.update({"width": fw, "height": fh})
        for label, val in checks.items():
            og = off_grid(val, base)
            if og is True:
                findings.append(("MINOR", "Grid", name,
                    f"{label} {val}px is off the {base}pt grid (and off 4pt)"))
            elif og == "fine":
                findings.append(("POLISH", "Grid", name,
                    f"{label} {val}px is on 4pt but not the {base}pt grid"))

        # (3) centering — opt-in only
        exp = f.get("expect")
        if exp in ("center", "center-h") and abs(p["left"] - p["right"]) > tol:
            findings.append(("MINOR", "Symmetry", name,
                f"expected horizontally centered but left {p['left']}px != right {p['right']}px "
                f"(delta {round(abs(p['left']-p['right']),1)}px)"))
        if exp in ("center", "center-v") and abs(p["top"] - p["bottom"]) > tol:
            findings.append(("MINOR", "Symmetry", name,
                f"expected vertically centered but top {p['top']}px != bottom {p['bottom']}px "
                f"(delta {round(abs(p['top']-p['bottom']),1)}px)"))

    # (1) paired-component consistency — compare left & top insets
    for pair in data.get("pairs", []):
        a, b = pair
        pa, pb = pads.get(a), pads.get(b)
        if not pa or not pb:
            continue
        diffs = [k for k in ("left", "top") if abs(pa[k] - pb[k]) > tol]
        if diffs:
            detail = "; ".join(f"{k} inset {pa[k]}px vs {pb[k]}px" for k in diffs)
            findings.append(("MAJOR", "Symmetry(pair)", f"{a} ~ {b}",
                f"paired components have different padding — {detail}. "
                f"Unify to one value and make them a shared component instance."))

    return findings, pads


def report(findings, pads):
    print("Padding measured per frame (left/right/top/bottom):")
    for name, p in pads.items():
        print(f"  {name}: {p}")
    print()
    if not findings:
        print("No paired-mismatch, grid, or centering issues found. ✅")
        return
    order = {"CRITICAL": 1, "MAJOR": 2, "MINOR": 3, "POLISH": 4}
    findings.sort(key=lambda f: order.get(f[0], 9))
    print(f"{len(findings)} finding(s):")
    for sev, cat, where, msg in findings:
        print(f"  {SEV_ICON.get(sev,'')} {sev:8} {cat:16} [{where}] {msg}")


DEMO = {
    "grid_base": 8, "tolerance": 1,
    "frames": [
        {"name": "GO card", "bounds": {"x": 40, "y": 900, "w": 300, "h": 120},
         "children": [{"name": "GO", "bounds": {"x": 52, "y": 924, "w": 60, "h": 24}},
                      {"name": "Sleep Aid", "bounds": {"x": 52, "y": 956, "w": 120, "h": 18}}]},
        {"name": "Loud Ring card", "bounds": {"x": 356, "y": 900, "w": 300, "h": 120},
         "children": [{"name": "Loud Ring", "bounds": {"x": 376, "y": 916, "w": 120, "h": 24}},
                      {"name": "Alarm Settings", "bounds": {"x": 376, "y": 948, "w": 150, "h": 18}}]},
        {"name": "AM/PM pill (in track)", "bounds": {"x": 40, "y": 700, "w": 280, "h": 56},
         "expect": "center-h",
         "children": [{"name": "pill", "bounds": {"x": 44, "y": 704, "w": 130, "h": 48}}]},
    ],
    "pairs": [["GO card", "Loud Ring card"]],
}


def main(argv):
    viewport = "1440,900"
    if "--viewport" in argv:
        viewport = argv[argv.index("--viewport") + 1]
    args = [a for a in argv if not a.startswith("--")]
    # skip a value that belongs to a flag
    if "--viewport" in argv and viewport in args:
        args.remove(viewport)

    if "--demo" in argv:
        data = DEMO
    elif args:
        src = args[0]
        if src.lower().endswith((".html", ".htm")):
            data = geometry_from_html(src, viewport)
            print(f"# {src} rendered at {viewport}; {len(data['frames'])} frames, "
                  f"{len(data['pairs'])} auto-detected pairs\n")
        else:
            with open(src) as fh:
                data = json.load(fh)
    else:
        print(__doc__)
        return
    findings, pads = analyze(data)
    report(findings, pads)


if __name__ == "__main__":
    main(sys.argv[1:])
