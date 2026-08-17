#!/usr/bin/env python3
"""
slop-scan.py — deterministic detector for the mechanically-checkable AI design tells.

Companion to the `design-review` skill's Group E (distinctiveness / anti-slop). It does NOT judge
taste — it flags the reflex patterns from `design-tropes.md` that can be found statically in
HTML/CSS source, so a human (or the review pass) can decide whether each is earned or slop.

Usage:
    python3 slop-scan.py file1.html [file2.css ...]
    python3 slop-scan.py --demo          # run against a tiny built-in sample
    python3 slop-scan.py --json file.html

Checks (each maps to an entry in design-tropes.md):
  - pure-black-white     #000 / #fff (and rgb/rgba equivalents) used as color
  - gradient-text        gradient + background-clip:text (gradient text as decoration)
  - layout-animation     transition/animation on layout props (width/height/top/left/margin/...)
  - uniform-shadow       the same box-shadow value repeated across many elements
  - purple-blue-gradient the canonical purple->blue SaaS gradient
  - glass-default        many backdrop-filter:blur surfaces (glassmorphism-by-default)
  - side-stripe-border   decorative border-left/right accent stripes
  - one-duration-motion  a single transition duration used everywhere

Exit code: 0 if no findings, 1 if any findings (so it can gate CI). --json prints machine output.

Pure stdlib. No installs. Heuristic by design: report, don't fail the build on its own.
"""
import sys, re, json, colorsys

# ---------- helpers ----------

def _strip_comments(css):
    return re.sub(r'/\*.*?\*/', ' ', css, flags=re.S)

HEX = re.compile(r'#([0-9a-fA-F]{3}|[0-9a-fA-F]{6})\b')

def _hex_to_rgb(h):
    if len(h) == 3:
        h = ''.join(c * 2 for c in h)
    return tuple(int(h[i:i + 2], 16) for i in range(0, 6, 2))

def _is_pure_bw(h):
    rgb = _hex_to_rgb(h)
    return rgb in ((0, 0, 0), (255, 255, 255))

def _hue_of(h):
    r, g, b = (c / 255 for c in _hex_to_rgb(h))
    hh, _, s = colorsys.rgb_to_hls(r, g, b)[0], 0, colorsys.rgb_to_hls(r, g, b)[2]
    return hh * 360, s

def _line_of(text, idx):
    return text.count('\n', 0, idx) + 1

# ---------- checks ----------

LAYOUT_PROPS = ('width', 'height', 'top', 'left', 'right', 'bottom',
                'margin', 'padding', 'inset', 'flex-basis')

def scan_text(name, text):
    findings = []
    css = _strip_comments(text)

    # 1. pure black / white as color (ignore #000 inside device-frame bezels is impossible to know;
    #    flag but note context in design-tropes). Also catch rgb(0,0,0)/rgb(255,255,255).
    pure = []
    for m in HEX.finditer(css):
        if _is_pure_bw(m.group(1)):
            pure.append((_line_of(text, m.start()), m.group(0)))
    for m in re.finditer(r'rgba?\(\s*0\s*,\s*0\s*,\s*0\s*(?:,\s*1(?:\.0)?\s*)?\)', css):
        pure.append((_line_of(text, m.start()), 'rgb(0,0,0)'))
    for m in re.finditer(r'rgba?\(\s*255\s*,\s*255\s*,\s*255\s*(?:,\s*1(?:\.0)?\s*)?\)', css):
        pure.append((_line_of(text, m.start()), 'rgb(255,255,255)'))
    if pure:
        findings.append(('pure-black-white', 'low',
                         f'{len(pure)} pure #000/#fff color use(s) — real materials are never pure; '
                         f'use near-black / off-white',
                         pure[:8]))

    # 2. gradient text as decoration
    gt = []
    for m in re.finditer(r'background-clip\s*:\s*text|-webkit-background-clip\s*:\s*text', css):
        # only a tell if a gradient is nearby in the same rule block
        window = css[max(0, m.start() - 400):m.start() + 100]
        if 'gradient' in window:
            gt.append((_line_of(text, m.start()), 'background-clip:text + gradient'))
    if gt:
        findings.append(('gradient-text', 'med',
                         f'{len(gt)} gradient-text instance(s) — reserve gradient text for a '
                         f'deliberate brand mark, not decoration', gt[:8]))

    # 3. transition/animation on layout properties
    la = []
    for m in re.finditer(r'transition\s*:\s*([^;{}]+)', css):
        val = m.group(1)
        for prop in LAYOUT_PROPS:
            if re.search(r'(^|[\s,])' + prop + r'([\s,]|$)', val):
                la.append((_line_of(text, m.start()), f'transition: …{prop}…'))
                break
    if la:
        findings.append(('layout-animation', 'med',
                         f'{len(la)} transition(s) on layout properties — animate transform/opacity, '
                         f'not width/height/top/left (jank + reflow)', la[:8]))

    # 4. uniform shadow: same box-shadow value repeated a lot
    shadows = {}
    for m in re.finditer(r'box-shadow\s*:\s*([^;{}]+)', css):
        val = re.sub(r'\s+', ' ', m.group(1).strip().lower())
        if val in ('none', 'inherit'):
            continue
        shadows.setdefault(val, []).append(_line_of(text, m.start()))
    for val, lines in shadows.items():
        if len(lines) >= 5:
            findings.append(('uniform-shadow', 'low',
                             f'same box-shadow repeated {len(lines)}× — map shadows to a real '
                             f'elevation scale; most elements sit flat',
                             [(l, val[:48]) for l in lines[:6]]))

    # 5. purple->blue SaaS gradient: a linear-gradient whose stops span purple(~270) and blue(~215)
    for m in re.finditer(r'linear-gradient\(([^()]*(?:\([^()]*\)[^()]*)*)\)', css):
        hexes = HEX.findall(m.group(1))
        hues = []
        for h in hexes:
            deg, sat = _hue_of(h)
            if sat > 0.25:
                hues.append(deg)
        has_purple = any(255 <= d <= 290 for d in hues)
        has_blue = any(200 <= d <= 250 for d in hues)
        if has_purple and has_blue:
            findings.append(('purple-blue-gradient', 'med',
                             'the canonical purple→blue SaaS gradient — the most-generated gradient '
                             'on earth; tie gradients to the brand and use with intent',
                             [(_line_of(text, m.start()), 'linear-gradient(purple→blue)')]))

    # 6. glassmorphism by default: many backdrop-filter blur surfaces
    glass = [(_line_of(text, m.start()), 'backdrop-filter:blur')
             for m in re.finditer(r'backdrop-filter\s*:\s*[^;{}]*blur', css)]
    if len(glass) >= 4:
        findings.append(('glass-default', 'low',
                         f'{len(glass)} backdrop-blur surfaces — use translucency only where a real '
                         f'layer floats over scrolling content, not as default decoration', glass[:8]))

    # 7. decorative side-stripe borders
    stripes = []
    for m in re.finditer(r'border-(left|right)\s*:\s*([^;{}]+)', css):
        w = re.search(r'(\d+(?:\.\d+)?)px', m.group(2))
        if w and 1 <= float(w.group(1)) <= 6 and ('var(' in m.group(2) or HEX.search(m.group(2))
                                                   or 'rgb' in m.group(2)):
            stripes.append((_line_of(text, m.start()), m.group(0)[:48]))
    if len(stripes) >= 2:
        findings.append(('side-stripe-border', 'low',
                         f'{len(stripes)} colored side-stripe border(s) — a recognizable reflex; '
                         f'reserve for a genuine quote/citation semantic', stripes[:8]))

    # 8. one-duration motion: a single transition duration dominates
    durs = {}
    for m in re.finditer(r'transition(?:-duration)?\s*:\s*[^;{}]*?(\d+(?:\.\d+)?)(m?s)', css):
        v = float(m.group(1)) * (1000 if m.group(2) == 's' else 1)
        durs[v] = durs.get(v, 0) + 1
    total = sum(durs.values())
    if total >= 8 and durs:
        top_dur, top_n = max(durs.items(), key=lambda kv: kv[1])
        if top_n / total >= 0.8:
            findings.append(('one-duration-motion', 'low',
                             f'{top_n}/{total} transitions use {top_dur:g}ms — duration should track '
                             f'distance & importance, not one value for everything',
                             [(0, f'{top_dur:g}ms ×{top_n}')]))

    return findings


def main(argv):
    as_json = '--json' in argv
    argv = [a for a in argv if a != '--json']

    if '--demo' in argv:
        files = [('demo.html', DEMO)]
    else:
        paths = [a for a in argv if not a.startswith('--')]
        if not paths:
            print(__doc__)
            return 0
        files = []
        for p in paths:
            try:
                files.append((p, open(p, encoding='utf-8', errors='replace').read()))
            except OSError as e:
                print(f'skip {p}: {e}', file=sys.stderr)

    results = {}
    total = 0
    for name, text in files:
        f = scan_text(name, text)
        results[name] = f
        total += len(f)

    if as_json:
        print(json.dumps({n: [{'check': c, 'severity': s, 'message': msg,
                                'hits': [{'line': ln, 'snippet': sn} for ln, sn in ex]}
                               for c, s, msg, ex in fs]
                          for n, fs in results.items()}, indent=2))
        return 1 if total else 0

    SEV = {'high': '🔴', 'med': '🟠', 'low': '🔵'}
    for name, fs in results.items():
        print(f'\n=== {name} ===')
        if not fs:
            print('  clean — no mechanical design tells found')
            continue
        for check, sev, msg, ex in fs:
            print(f'  {SEV.get(sev, "•")} [{check}] {msg}')
            for ln, sn in ex:
                loc = f'L{ln}' if ln else '—'
                print(f'        {loc}: {sn}')
    print(f'\n{total} finding(s) across {len(files)} file(s). '
          f'Heuristic — each is a prompt to check intent, not an automatic failure.')
    return 1 if total else 0


DEMO = """<style>
  :root{ --accent:#7c3aed; }
  body{ background:#fff; color:#000; }
  .card{ box-shadow:0 4px 12px rgba(0,0,0,.1); }
  .card2{ box-shadow:0 4px 12px rgba(0,0,0,.1); }
  .card3{ box-shadow:0 4px 12px rgba(0,0,0,.1); }
  .card4{ box-shadow:0 4px 12px rgba(0,0,0,.1); }
  .card5{ box-shadow:0 4px 12px rgba(0,0,0,.1); }
  h1{ background:linear-gradient(90deg,#7c3aed,#3b82f6); -webkit-background-clip:text; }
  .panel{ transition:width .2s, opacity .2s; }
  .nav{ backdrop-filter:blur(10px); }
  .callout{ border-left:3px solid var(--accent); }
</style>"""

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
