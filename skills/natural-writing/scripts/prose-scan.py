#!/usr/bin/env python3
"""Mechanical passes over prose. Counts, never verdicts.

Every check here is one a model does badly and a computer does exactly: counting
dashes across 2,000 words, seeing a zero-width space, working out whether a word
list crosses a density threshold. Run this first so judgment is spent on the
things that need judgment.

It reports findings and never a score. Scoring authorship is a claim this skill
refuses to make; counting characters is not.

    python3 prose-scan.py draft.md
    python3 prose-scan.py --demo        # self-check on known input
"""
import re, sys, unicodedata, statistics as st

# --- Tier 1: replace on sight. Sense-gated entries carry their qualifier. ---
TIER1 = {
    "delve": None, "tapestry": "figurative", "testament to": None, "underscore": "verb",
    "leverage": "verb", "seamless": None, "multifaceted": None, "realm": None,
    "interplay": None, "pivotal": None, "landscape": "metaphor", "harness": "metaphor",
    "it's worth noting": None, "it is worth noting": None, "in today's": None,
}
TIER2 = ["crucial", "vibrant", "robust", "foster", "enhance", "showcase", "notably",
         "moreover", "furthermore", "garner", "bolster", "utilize", "supercharge"]
TIER3 = ["key", "important", "significant", "various", "effective", "valuable",
         "powerful", "essential", "comprehensive"]

ARTIFACTS = [
    (r"\b(great|excellent|good) question\b", "sycophantic opener"),
    (r"\bI hope this helps\b", "chatbot closer"),
    (r"\b(certainly|of course)[!,]", "chatbot affirmation"),
    (r"as an AI\b", "assistant disclaimer"),
    (r"\bmy (knowledge |training )?cut[- ]?off\b", "cutoff disclaimer"),
    (r"as of my last update", "cutoff disclaimer"),
    (r"citeturn\d+\w*", "leaked citation token"),
    (r"utm_source=(chatgpt|claude|perplexity)", "AI-tool URL parameter"),
    (r"\[(TODO|PLACEHOLDER|INSERT[^\]]*)\]", "unfilled placeholder"),
    (r"let me think step by step", "reasoning-chain leak"),
]
INVISIBLE = {"​": "zero-width space", "‌": "zero-width non-joiner",
             "‍": "zero-width joiner", "­": "soft hyphen",
             "﻿": "byte-order mark", "⁠": "word joiner"}
# Cyrillic/Greek letters that render as Latin
HOMOGLYPH = re.compile(r"[Ѐ-ӿͰ-Ͽ]")

WORD = re.compile(r"\b[\w'-]+\b")
def words(t): return WORD.findall(t)
def paras(t): return [p for p in re.split(r"\n\s*\n", t) if p.strip()]

def sentences(t):
    t = re.sub(r"```.*?```", " ", t, flags=re.S)
    t = re.sub(r"^\s*[-*+#>|].*$", " ", t, flags=re.M)      # lists, headings, tables
    return [s for s in re.split(r"(?<=[.!?])\s+", t) if len(words(s)) > 2]

def strip_code(t):
    t = re.sub(r"\A---\n.*?\n---\n", " ", t, flags=re.S)   # YAML frontmatter, whose --- is not a dash
    t = re.sub(r"```.*?```", " ", t, flags=re.S)
    return re.sub(r"`[^`]*`", " ", t)

def find(text):
    out, prose = [], strip_code(text)
    wc = len(words(prose))

    if wc < 40:
        out.append(("FLOOR", f"{wc} words: under the ~40-word floor, report that the sample "
                             "is too short rather than returning a verdict"))
        return out, wc

    # dashes, exempting numeric ranges
    # (?<!-)--(?!-) so a --- rule or a longer run is not counted as two dashes
    dash = [m for m in re.finditer(r"—|(?<!-)--(?!-)|(?<![\d\s])–|–(?!\d)", prose)]
    per1k = 1000 * len(dash) / wc
    if per1k > 1:
        out.append(("DASH", f"{len(dash)} in {wc} words = {per1k:.1f} per 1,000 (cap is 1). "
                            "A voice sample overrides this."))

    # invisible characters and homoglyphs
    for ch, name in INVISIBLE.items():
        n = text.count(ch)
        if n:
            out.append(("INVISIBLE", f"{n}x {name} (U+{ord(ch):04X})"))
    for m in HOMOGLYPH.finditer(text):
        ctx = text[max(0, m.start()-12):m.start()+12].replace("\n", " ")
        if re.search(r"[a-zA-Z]", ctx):     # only flag when embedded in Latin text
            out.append(("HOMOGLYPH", f"{unicodedata.name(m.group(), '?')} in \"{ctx.strip()}\""))
            break

    for pat, label in ARTIFACTS:
        for m in re.finditer(pat, prose, re.I):
            out.append(("ARTIFACT", f'{label}: "{m.group()[:48]}"'))

    low = prose.lower()
    # A line listing four or more flagged words is a catalogue of them, not prose
    # written with them. Text about AI writing quotes its own examples constantly,
    # and the skill exempts quoted examples, so the scan must too.
    def is_catalogue(line):
        n = sum(1 for w in list(TIER1) + TIER2 + TIER3 if re.search(rf"\b{re.escape(w)}", line, re.I))
        return n >= 4
    lines = prose.split("\n")
    starts, off = [], 0
    for ln in lines:
        starts.append((off, off + len(ln), is_catalogue(ln))); off += len(ln) + 1
    def catalogued(i):
        return any(a <= i <= b and c for a, b, c in starts)

    skipped = 0
    for w, sense in TIER1.items():
        for m in re.finditer(rf"\b{re.escape(w)}\w*", low):
            if catalogued(m.start()):
                skipped += 1
                continue
            note = f" — gated to the {sense} sense, check this one" if sense else ""
            out.append(("TIER1", f'"{prose[m.start():m.end()]}"{note}'))
    if skipped:
        out.append(("SKIPPED", f"{skipped} vocabulary hits ignored on lines that list four or "
                               "more flagged words, which reads as a catalogue rather than prose"))

    for p in paras(prose):
        body = "\n".join(l for l in p.split("\n") if not is_catalogue(l))
        hits = [w for w in TIER2 if re.search(rf"\b{w}\w*", body, re.I)]
        if len(hits) >= 2:
            out.append(("TIER2", f"{len(hits)} in one paragraph: {', '.join(hits)}"))

    t3 = [w for w in TIER3 if re.search(rf"\b{w}\b", low)]
    t3n = sum(len(re.findall(rf"\b{w}\b", low)) for w in TIER3)
    if wc and 100 * t3n / wc >= 3:
        out.append(("TIER3", f"{t3n} hits = {100*t3n/wc:.1f}% of text (threshold 3%): {', '.join(t3)}"))
    else:
        for p in paras(prose):
            p = "\n".join(l for l in p.split("\n") if not is_catalogue(l))
            n3 = sum(len(re.findall(rf"\b{w}\b", p, re.I)) for w in TIER3)
            if n3 >= 2 and any(re.search(rf"\b{w}\b", p, re.I) for w in list(TIER1) + TIER2):
                out.append(("TIER3", f"{n3} Tier 3 words in a paragraph that also carries a "
                                     "Tier 1 or 2 hit (co-occurrence gate)"))
                break

    # formatting
    for m in re.finditer(r"^#{1,6}\s+(.*)$", text, re.M):
        h = m.group(1)
        if re.search(r"[\U0001F300-\U0001FAFF←-⇿☀-➿]", h):
            out.append(("FORMAT", f'emoji or arrow in heading: "{h[:44]}"'))
        ws = [x for x in h.split() if x[:1].isalpha()]
        if len(ws) >= 4 and sum(x[:1].isupper() for x in ws) / len(ws) > 0.8:
            out.append(("FORMAT", f'heading looks Title Case: "{h[:44]}"'))
    n_bold = len(re.findall(r"^\s*[-*+]\s+\*\*[^*]+\*\*\s*[:—-]", text, re.M))
    if n_bold >= 3:
        out.append(("FORMAT", f"{n_bold} bullets open with a bold label plus a colon; "
                              "check they are not restating the line"))
    tags = re.findall(r"(?<!\w)#[a-z]\w+", text)
    if len(tags) >= 6:
        out.append(("FORMAT", f"{len(tags)} hashtags"))
    if re.search(r"[‘’“”]", prose):
        out.append(("QUOTES", "curly quotes present; straight quotes read as typed"))

    # rhythm, reported not scored
    sl = [len(words(s)) for s in sentences(prose)]
    if len(sl) >= 6:
        cv = st.pstdev(sl) / st.mean(sl) if st.mean(sl) else 0
        if cv < 0.35:
            out.append(("RHYTHM", f"sentence lengths are uniform (mean {st.mean(sl):.0f} words, "
                                  f"variation {cv:.2f}). Not a defect on its own; look at whether "
                                  "every sentence has the same shape."))
    pl = [len(words(p)) for p in paras(prose)]
    if len(pl) >= 5 and st.pstdev(pl) / max(1, st.mean(pl)) < 0.3:
        out.append(("RHYTHM", f"paragraphs are near-identical in length (mean {st.mean(pl):.0f} words)"))
    return out, wc

def report(name, text):
    out, wc = find(text)
    print(f"\n=== {name} ({wc} words) ===")
    if not out:
        print("  clean on the mechanical passes")
    for kind, msg in out:
        print(f"  [{kind}] {msg}")
    print("\n  These are counts, not a verdict. Judgment checks are in references/preflight.md.")
    return out

DEMO = """# The Evolving Landscape Of Modern Systems

We delve into a rich tapestry of ideas here — and it is worth noting that the
approach is seamless. Great question!

A crucial finding. The team built a robust pipeline over the quarter and shipped
it without incident, which mattered.

The key significant important various effective points are essential and valuable.

- **First:** first
- **Second:** second
- **Third:** third

Here is a “quoted” phrase with a zero​width space. See https://x.com/?utm_source=chatgpt.com
"""

if __name__ == "__main__":
    if "--demo" in sys.argv:
        got = {k for k, _ in report("demo", DEMO)}
        want = {"DASH", "TIER1", "TIER2", "TIER3", "ARTIFACT", "FORMAT", "QUOTES", "INVISIBLE"}
        missing = want - got
        print(f"\n  self-check: {'PASS' if not missing else 'FAIL, missed ' + ', '.join(sorted(missing))}")
        sys.exit(1 if missing else 0)
    if len(sys.argv) < 2:
        print(__doc__); sys.exit(2)
    for path in sys.argv[1:]:
        report(path, open(path, encoding="utf-8").read())
