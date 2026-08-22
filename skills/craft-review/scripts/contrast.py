#!/usr/bin/env python3
"""
contrast.py — WCAG 2.x contrast ratio for two colors.

Deterministic math so the review never guesses a ratio. Pure stdlib.

Usage:
    python3 contrast.py "#F2F3F5" "#191B1F"
    python3 contrast.py "76,141,255" "#101114"        # rgb or hex, either order
    python3 contrast.py --json "#A8ADB7" "#101114"    # machine-readable output

Exit code 0 on a computed ratio, 2 on unusable input; read the PASS/FAIL fields for the verdict. Import get_ratio()/verdicts() to use in code.
"""
import re
import sys
import json


RGBA = re.compile(r"rgba?\(\s*([\d.]+)[\s,]+([\d.]+)[\s,]+([\d.]+)(?:\s*[,/]\s*([\d.]+%?))?\s*\)", re.I)


def parse_color(s):
    """Accept '#RGB', '#RRGGBB', 'RRGGBB', 'r,g,b', or rgb()/rgba(). Return
    (r, g, b, a) with a in 0-1. Alpha used to be dropped on the floor, and a
    translucent foreground then passed the gate without a ratio being computed."""
    s = s.strip()
    m = RGBA.fullmatch(s)
    if m:
        rgb = tuple(max(0.0, min(255.0, float(m.group(i)))) for i in (1, 2, 3))
        a = m.group(4)
        alpha = float(a[:-1]) / 100 if a and a.endswith("%") else (float(a) if a else 1.0)
        return (*rgb, max(0.0, min(1.0, alpha)))
    if "," in s:
        parts = [float(p) for p in s.split(",")]
        if len(parts) not in (3, 4):
            raise ValueError(f"bad rgb: {s!r}")
        rgb = tuple(max(0.0, min(255.0, p)) for p in parts[:3])
        return (*rgb, parts[3] if len(parts) == 4 else 1.0)
    s = s.lstrip("#")
    if len(s) == 3:
        s = "".join(c * 2 for c in s)
    if len(s) == 8:                      # #RRGGBBAA
        return tuple(int(s[i:i + 2], 16) for i in (0, 2, 4)) + (int(s[6:8], 16) / 255,)
    if len(s) != 6 or not re.fullmatch(r"[0-9a-fA-F]{6}", s):
        raise ValueError(f"bad hex: {s!r}")
    return tuple(int(s[i:i + 2], 16) for i in (0, 2, 4)) + (1.0,)


def composite(fg, bg):
    """Flatten a translucent foreground onto its background. WCAG ratios are
    defined for what the eye sees, which is the composited color."""
    a = fg[3] if len(fg) > 3 else 1.0
    if a >= 1.0:
        return tuple(fg[:3])
    return tuple(f * a + b * (1 - a) for f, b in zip(fg[:3], bg[:3]))


def _lin(c):
    c = c / 255.0
    return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4


def relative_luminance(rgb):
    r, g, b = (_lin(v) for v in rgb[:3])
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def get_ratio(c1, c2):
    """Contrast ratio between two colors (hex/rgb strings or (r,g,b) tuples)."""
    if isinstance(c1, str):
        c1 = parse_color(c1)
    if isinstance(c2, str):
        c2 = parse_color(c2)
    # The second color is the ground: flatten a translucent first color onto it.
    c1 = composite(c1, c2)
    c2 = tuple(c2[:3])
    l1, l2 = relative_luminance(c1), relative_luminance(c2)
    hi, lo = max(l1, l2), min(l1, l2)
    return (hi + 0.05) / (lo + 0.05)


def verdicts(ratio):
    """Pass/fail per WCAG 2.2 use case."""
    return {
        "ratio": round(ratio, 2),
        "body_text_AA": ratio >= 4.5,      # < 24px (or < 18.66px bold)
        "body_text_AAA": ratio >= 7.0,
        "large_text_AA": ratio >= 3.0,     # >= 24px (or >= 18.66px bold)
        "large_text_AAA": ratio >= 4.5,
        "ui_component_AA": ratio >= 3.0,   # icons, borders, graphical objects
    }


def _fmt(v):
    return "PASS" if v else "FAIL"


def main(argv):
    as_json = False
    args = []
    for a in argv:
        if a in ("--json", "-j"):
            as_json = True
        else:
            args.append(a)
    if len(args) != 2:
        print(__doc__)
        return 2
    try:
        c1, c2 = parse_color(args[0]), parse_color(args[1])
    except ValueError as e:
        print(f"error: {e}", file=sys.stderr)
        return 2
    r = get_ratio(c1, c2)
    v = verdicts(r)
    if as_json:
        print(json.dumps({"fg": args[0], "bg": args[1], **v}, indent=2))
        return
    print(f"{args[0]}  on  {args[1]}")
    print(f"  contrast ratio: {v['ratio']}:1")
    print(f"  body text   (< 24px)   AA {_fmt(v['body_text_AA'])}   AAA {_fmt(v['body_text_AAA'])}")
    print(f"  large text  (>= 24px)  AA {_fmt(v['large_text_AA'])}   AAA {_fmt(v['large_text_AAA'])}")
    print(f"  UI / icons / borders   AA {_fmt(v['ui_component_AA'])}")
    if not v["body_text_AA"]:
        print("  ! fails AA for body text — enlarge, embolden, or increase contrast.")


def _demo():
    """Self-check on values with known answers. Exits 1 on any miss."""
    cases = [
        ("#000000", "#FFFFFF", 21.0),       # the WCAG maximum, by definition
        ("#FFFFFF", "#FFFFFF", 1.0),        # identical colors, the minimum
        ("#767676", "#FFFFFF", 4.54),       # the canonical just-passes-AA gray
        ("255,255,255", "#000", 21.0),      # rgb and short-hex parse to the same thing
    ]
    bad = []
    for a, b, want in cases:
        got = get_ratio(parse_color(a), parse_color(b))
        ok = abs(got - want) < 0.01
        print(f"  {a:>12} on {b:<8} {got:6.2f}:1  want {want:5.2f}  {'ok' if ok else 'MISS'}")
        if not ok:
            bad.append((a, b, got, want))
        verdicts(got)                       # must not raise on any ratio
    print(f"\n  self-check: {'PASS' if not bad else 'FAIL'}")
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    if "--demo" in sys.argv:
        _demo()
    # A bad color used to print an error and exit 0, so a CI wrapper read it as a pass.
    sys.exit(main(sys.argv[1:]) or 0)
