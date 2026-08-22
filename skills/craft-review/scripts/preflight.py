#!/usr/bin/env python3
"""
preflight.py — showstopper gate for HTML artifacts. Deterministic only.

Runs in well under a second on a multi-megabyte page. Every check here is one a
script can DECIDE. Nothing in this file has an opinion, which is the whole point:
it is a gate, not a review. Anything needing judgment belongs in the full pass.

Checks:
  theme-only-color   a color declared ONLY inside a media/[data-theme] block, so it
                     never applies in the un-stamped default state. The classic
                     unreadable-artifact bug.
  no-body-bg         body sets no background, so it borrows the host's ground and
                     renders one theme's text on the other theme's surface.
  contrast           rules that set both a foreground and a background, resolved per
                     theme through var() tokens, checked against WCAG 2.2 AA.
  off-scale          padding/margin/gap values off the 4/8px scale.
  interactivity      script and handler counts, compared against a baseline file.
                     Catches a rewrite silently dropping behavior.

Usage:
    python3 preflight.py page.html
    python3 preflight.py page.html --baseline previous.html
    python3 preflight.py page.html --json

Exit code 1 if any BLOCK finding, else 0. Pure stdlib.
"""
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from contrast import get_ratio, parse_color  # noqa: E402

SCALE = {0, 1, 2, 4, 8, 12, 16, 20, 24, 28, 32, 36, 40, 44, 48, 56, 64, 72, 80, 96, 128}
COLORISH = re.compile(r"(#[0-9a-fA-F]{3,8}|rgba?\([^)]*\)|hsla?\([^)]*\))")
VAR = re.compile(r"var\(\s*(--[\w-]+)\s*(?:,[^)]*)?\)")


def strip_noise(css):
    return re.sub(r"/\*.*?\*/", "", css, flags=re.S)


def blocks(html):
    """Every <style> body, with base64 payloads removed first."""
    html = re.sub(r'src="data:[^"]+"', 'src=""', html)
    return [strip_noise(m) for m in re.findall(r"<style[^>]*>(.*?)</style>", html, flags=re.S)]


def rules(css):
    """(selector, declarations, enclosing_at_rule_or_None), brace-matched so nested
    at-rules are actually seen. A regex cannot do this; the earlier one silently
    dropped every @media block, which is the one place theme bugs hide."""
    out, i = [], 0
    while True:
        j = css.find("{", i)
        if j < 0:
            return out
        head = css[i:j].strip()
        depth, k = 1, j + 1
        while k < len(css) and depth:
            if css[k] == "{":
                depth += 1
            elif css[k] == "}":
                depth -= 1
            k += 1
        body = css[j + 1 : k - 1]
        if head.startswith("@"):
            for sel, b, inner in rules(body):
                out.append((sel, b, inner or head))
        else:
            out.append((head, body, None))
        i = k


def decls(body):
    d = {}
    for part in body.split(";"):
        if ":" in part:
            k, _, v = part.partition(":")
            d[k.strip().lower()] = v.strip()
    return d


def theme_of(sel, at):
    """Which theme state does this rule apply in?"""
    if at and "prefers-color-scheme: dark" in at.replace(" ", " "):
        return "dark-media"
    if '[data-theme="dark"]' in sel:
        return "dark-attr"
    if '[data-theme="light"]' in sel:
        return "light-attr"
    return "base"


def collect(html):
    tokens = {"base": {}, "dark-media": {}, "dark-attr": {}, "light-attr": {}}
    uses = {}          # token name -> themes whose rules read it
    pairs, spacing, findings = [], [], []
    for css in blocks(html):
        for sel, body, at in rules(css):
            t = theme_of(sel, at)
            d = decls(body)
            for v in d.values():
                for name in VAR.findall(v):
                    uses.setdefault(name, set()).add(t)
            for k, v in d.items():
                if k.startswith("--") and COLORISH.search(v):
                    tokens[t][k] = v.strip()
                if k in ("padding", "margin", "gap", "row-gap", "column-gap") or k.startswith(
                    ("padding-", "margin-")
                ):
                    for num in re.findall(r"(-?\d+(?:\.\d+)?)px", v):
                        spacing.append((sel, k, float(num)))
            fg = d.get("color")
            bg = d.get("background-color") or d.get("background")
            if fg and bg and COLORISH.search(bg + fg + "x") or (fg and bg and VAR.search(fg + bg)):
                pairs.append((sel, t, fg, bg))
    return tokens, pairs, spacing, findings, uses


def resolve(val, tokens, theme):
    """Resolve var() chains against a theme, falling back to base."""
    for _ in range(6):
        m = VAR.search(val)
        if not m:
            break
        name = m.group(1)
        repl = tokens[theme].get(name) or tokens["base"].get(name)
        if repl is None:
            return None
        val = val[: m.start()] + repl + val[m.end() :]
    m = COLORISH.search(val)
    return m.group(1) if m else None


def check(html, baseline=None):
    tokens, pairs, spacing, out, uses = collect(html)

    # 1. colors that exist only in a themed block AND are read from outside it.
    # A token defined and consumed entirely inside dark mode is correct; blocking
    # it made a false positive the top finding, since a BLOCK now ranks first.
    base_names = set(tokens["base"])
    # dark-media and dark-attr are the same theme reached two ways. Treating them
    # as separate scopes reported a legitimate dark-only token twice, each block
    # citing the other dark scope as "outside".
    SAME = {"dark-media": {"dark-media", "dark-attr"}, "dark-attr": {"dark-media", "dark-attr"},
            "light-attr": {"light-attr", "base"}}
    reported = set()
    for theme in ("dark-media", "dark-attr", "light-attr"):
        for name in tokens[theme]:
            if name in base_names or name in reported:
                continue
            # defined in the sibling scope too? then it resolves wherever it is read
            if any(name in tokens[t] for t in SAME[theme] - {theme}):
                sibling_covered = True
            else:
                sibling_covered = False
            outside = sorted(uses.get(name, set()) - SAME[theme])
            if sibling_covered and not outside:
                continue
            if not outside:
                continue
            reported.add(name)
            out.append(
                dict(
                    level="BLOCK",
                    check="theme-only-color",
                    detail=f"{name} is read by {', '.join(outside)} rules but defined only in "
                    f"{theme}, so it never resolves in the un-stamped default state",
                )
            )

    # 2. body must paint its own ground
    body_bg = any(
        re.search(r"(^|,)\s*body\b", sel)
        and ("background" in decls(b) or "background-color" in decls(b))
        for css in blocks(html)
        for sel, b, _ in rules(css)
    )
    if not body_bg:
        out.append(
            dict(
                level="BLOCK",
                check="no-body-bg",
                detail="body sets no background; the page borrows the host's ground",
            )
        )

    # 3. contrast on rules that set both fg and bg, per theme
    seen = set()
    for sel, t, fg_raw, bg_raw in pairs:
        # a rule authored in the base block still applies while a dark/light token set
        # is active, with different values. Checking only "base" misses exactly half
        # the failures, which is how the dark-theme miss below went unreported.
        # With no custom properties anywhere, every tokens[k] is empty and this used
        # to produce an empty scope list, so a plain-CSS page got no contrast pass
        # at all. Base is always a scope.
        scopes = ([k for k in tokens if tokens[k]] or ["base"]) if t == "base" else [t]
        for theme in scopes:
            fg, bg = resolve(fg_raw, tokens, theme), resolve(bg_raw, tokens, theme)
            if not fg or not bg:
                continue
            try:
                r = get_ratio(parse_color(fg), parse_color(bg))
            except Exception as e:
                # Swallowing this silently turned an uncheckable pair into a pass,
                # which is the one thing a gate must never do.
                out.append(dict(level="WARN", check="uncheckable-color",
                                detail=f"{sel}: could not compute {fg_raw} on {bg_raw} ({e}); "
                                       "check this pair by hand"))
                continue
            key = (round(r, 2), fg, bg)
            if key in seen:
                continue
            seen.add(key)
            if r < 4.5:
                out.append(
                    dict(
                        level="BLOCK" if r < 3.0 else "WARN",
                        check="contrast",
                        detail=f"{sel.strip()[:44]} [{theme}] {fg} on {bg} = {r:.2f}:1 "
                        f"(AA body needs 4.5, large/UI 3.0)",
                    )
                )

    # 4. spacing off the 4/8 scale
    bad = sorted({v for _, _, v in spacing if v == int(v) and abs(v) not in SCALE and abs(v) < 200})
    if bad:
        out.append(
            dict(
                level="WARN",
                check="off-scale",
                detail=f"{len(bad)} spacing values off the 4/8 scale: "
                + ", ".join(f"{int(v)}px" for v in bad[:10]),
            )
        )

    # 5. interactivity regression against a baseline
    if baseline is not None:
        def sig(doc):
            # a saved/rendered page carries the host's injected runtime before <title>;
            # counting it would report a phantom regression against an authored file
            if "frame-runtime" in doc[:4000] and "<title>" in doc:
                doc = doc[doc.index("<title>"):]
            doc = re.sub(r'src="data:[^"]+"', "", doc)
            return (
                len(re.findall(r"<script", doc)),
                len(re.findall(r"addEventListener", doc)),
                len(re.findall(r"<figure", doc)),
            )
        was, now = sig(baseline), sig(html)
        for i, name in enumerate(("script tags", "event listeners", "figures")):
            if now[i] < was[i]:
                out.append(
                    dict(
                        level="BLOCK",
                        check="interactivity",
                        detail=f"{name}: {was[i]} in baseline, {now[i]} now. A rewrite dropped "
                        f"behavior the old page had",
                    )
                )
    return out


def main(argv):
    args = [a for a in argv if not a.startswith("--")]
    if not args:
        print(__doc__)
        return 0
    html = Path(args[0]).read_text(errors="ignore")
    base = None
    if "--baseline" in argv:
        base = Path(argv[argv.index("--baseline") + 1]).read_text(errors="ignore")
    found = check(html, base)
    if "--json" in argv:
        print(json.dumps(found, indent=1))
    else:
        blocking = [f for f in found if f["level"] == "BLOCK"]
        for f in found:
            mark = "BLOCK" if f["level"] == "BLOCK" else " warn"
            print(f"  [{mark}] {f['check']}: {f['detail']}")
        if not found:
            print("  clean: no showstoppers")
        print(f"\n{len(blocking)} blocking, {len(found) - len(blocking)} warnings.")
    return 1 if any(f["level"] == "BLOCK" for f in found) else 0


def demo():
    bad = """<style>
    :root { --ink: #111; }
    @media (prefers-color-scheme: dark) { :root { --ghost: #222; } }
    .x { color: var(--ink); background: #1a1a1a; border-color: var(--ghost); }
    .y { padding: 13px; margin: 7px; }
    </style><body><script>x.addEventListener('click',f)</script></body>"""
    f = check(bad)
    kinds = {x["check"] for x in f}
    assert "theme-only-color" in kinds, kinds     # --ghost only in dark
    assert "no-body-bg" in kinds, kinds           # body never painted
    assert "contrast" in kinds, kinds             # #111 on #1a1a1a is unreadable
    assert "off-scale" in kinds, kinds            # 13px / 7px
    drop = check(bad, baseline=bad + "<script>a.addEventListener('x',f)</script>")
    assert any(x["check"] == "interactivity" for x in drop), "baseline drop not detected"
    print("demo: all 5 checks fire on a deliberately broken page")


if __name__ == "__main__":
    if "--demo" in sys.argv:
        demo()
    else:
        sys.exit(main(sys.argv[1:]))
