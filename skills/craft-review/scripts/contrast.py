#!/usr/bin/env python3
"""
contrast.py — WCAG 2.x contrast ratio for two colors.

Deterministic math so the review never guesses a ratio. Pure stdlib.

Usage:
    python3 contrast.py "#F2F3F5" "#191B1F"
    python3 contrast.py "76,141,255" "#101114"        # rgb or hex, either order
    python3 contrast.py --json "#A8ADB7" "#101114"    # machine-readable output

Exit code is 0 always; read the PASS/FAIL fields. Import get_ratio()/verdicts() to use in code.
"""
import sys
import json


def parse_color(s):
    """Accept '#RGB', '#RRGGBB', 'RRGGBB', or 'r,g,b'. Return (r, g, b) 0-255 ints."""
    s = s.strip()
    if "," in s:
        parts = [int(p) for p in s.split(",")]
        if len(parts) != 3:
            raise ValueError(f"bad rgb: {s!r}")
        return tuple(max(0, min(255, p)) for p in parts)
    s = s.lstrip("#")
    if len(s) == 3:
        s = "".join(c * 2 for c in s)
    if len(s) != 6:
        raise ValueError(f"bad hex: {s!r}")
    return tuple(int(s[i:i + 2], 16) for i in (0, 2, 4))


def _lin(c):
    c = c / 255.0
    return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4


def relative_luminance(rgb):
    r, g, b = (_lin(v) for v in rgb)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def get_ratio(c1, c2):
    """Contrast ratio between two colors (hex/rgb strings or (r,g,b) tuples)."""
    if isinstance(c1, str):
        c1 = parse_color(c1)
    if isinstance(c2, str):
        c2 = parse_color(c2)
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
        return
    try:
        c1, c2 = parse_color(args[0]), parse_color(args[1])
    except ValueError as e:
        print(f"error: {e}")
        return
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


if __name__ == "__main__":
    main(sys.argv[1:])
