#!/usr/bin/env python3
"""Mechanical passes over prose. Counts, never verdicts.

Every check here is one a model does badly and a computer does exactly: counting
dashes across 2,000 words, seeing a zero-width space, working out whether a word
list crosses a density threshold. Run this first so judgment is spent on the
things that need judgment.

It reports findings and never a score. Scoring authorship is a claim this skill
refuses to make; counting characters is not.

    python3 prose-scan.py draft.md
    python3 prose-scan.py --compare original.md rewrite.md   # specifics the rewrite added
    python3 prose-scan.py --demo        # self-check on known input
"""
import re, sys, unicodedata, statistics as st

# --- Vocabulary tiers -----------------------------------------------------------
# The catalogue lives in references/vocabulary.md. This script READS it rather
# than carrying a copy, because a copy drifted within a day of being written:
# 'robust' was Tier 1 in the catalogue and Tier 2 here. The lists below are a
# fallback for running the script outside the skill, and the report says which
# source was used so a drifted fallback cannot pass as the catalogue.
_FALLBACK_TIER1 = {
    "delve": None, "tapestry": "figurative", "testament to": None, "underscore": "verb",
    "leverage": "verb", "seamless": None, "multifaceted": None, "realm": None,
    "interplay": None, "pivotal": None, "landscape": "metaphor", "harness": "metaphor",
    "it's worth noting": None, "it is worth noting": None, "in today's": None,
}
_FALLBACK_TIER2 = ["crucial", "foster", "enhance", "showcase", "notably",
                   "moreover", "furthermore", "garner", "bolster", "supercharge"]
_FALLBACK_TIER3 = ["key", "important", "significant", "various", "effective",
                   "valuable", "powerful", "essential", "comprehensive"]

def load_vocabulary():
    """Parse references/vocabulary.md into (tier1 dict, tier2 list, tier3 list, source)."""
    import os
    here = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(here, "..", "references", "vocabulary.md")
    if not os.path.exists(path):
        return _FALLBACK_TIER1, _FALLBACK_TIER2, _FALLBACK_TIER3, "built-in fallback (vocabulary.md not found)"
    t1, t2, t3, tier = {}, [], [], None
    for line in open(path, encoding="utf-8"):
        h = re.match(r"^##+\s*Tier\s*(\d)", line)
        if h:
            tier = int(h.group(1)); continue
        m = re.match(r"^\|\s*([^|]+?)\s*\|", line)
        if not m or tier is None: continue
        term = m.group(1).strip().strip("`*")
        if not term or term.lower() in {"word", "phrase", "term", "pattern"} or set(term) <= set("-: "):
            continue
        sense = None
        s = re.match(r"^(.*?)\s*\((?:as )?(\w[\w ]*)\)\s*$", term)
        if s:
            term, sense = s.group(1).strip(), s.group(2).strip()
        term = term.lower()
        if tier == 1: t1[term] = sense
        elif tier == 2: t2.append(term)
        elif tier == 3: t3.append(term)
    if not t1:
        return _FALLBACK_TIER1, _FALLBACK_TIER2, _FALLBACK_TIER3, "built-in fallback (vocabulary.md parsed empty)"
    # A term the catalogue lists in more than one tier belongs to the strictest one.
    # Keeping it in both double-counts it everywhere downstream.
    t2 = [w for w in dict.fromkeys(t2) if w not in t1]
    t3 = [w for w in dict.fromkeys(t3) if w not in t1 and w not in t2]
    return t1, t2, t3, f"references/vocabulary.md ({len(t1)}/{len(t2)}/{len(t3)} terms)"

TIER1, TIER2, TIER3, VOCAB_SOURCE = load_vocabulary()

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

    # An artifact quoted as an example is not an artifact. Skip hits that sit
    # inside quotation marks, in a table row, or in a blockquote, and say how many.
    def quoted(i):
        ls = prose.rfind("\n", 0, i) + 1; le = prose.find("\n", i)
        line = prose[ls:le if le != -1 else None]
        if line.lstrip().startswith(("|", ">", '- "', '* "', '1. "')): return True
        before = line[:i - ls]
        return (before.count('"') + before.count("\u201c") + before.count("\u201d")) % 2 == 1
    art_skipped = 0
    for pat, label in ARTIFACTS:
        for m in re.finditer(pat, prose, re.I):
            if quoted(m.start()):
                art_skipped += 1; continue
            out.append(("ARTIFACT", f'{label}: "{m.group()[:48]}"'))
    if art_skipped:
        out.append(("SKIPPED", f"{art_skipped} artifact hits ignored because they sit inside quotes, "
                               "a table row, or a blockquote, which reads as an example"))

    low = prose.lower()
    # A line listing four or more flagged words is a catalogue of them, not prose
    # written with them. Text about AI writing quotes its own examples constantly,
    # and the skill exempts quoted examples, so the scan must too.
    _ALL = list(dict.fromkeys(list(TIER1) + TIER2 + TIER3))
    def is_catalogue(line):
        n = sum(1 for w in _ALL if re.search(rf"\b{re.escape(w)}", line, re.I))
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

NUM   = re.compile(r"(?<![\w.])\d[\d,]*(?:\.\d+)?\s?(?:%|percent|ms|s|x|k|m|bn|million|billion)?(?![\w])", re.I)
YEAR  = re.compile(r"\b(1[89]\d\d|20\d\d)\b")
CITE  = re.compile(r"\(([A-Z][\w&.\- ]+?),?\s+(?:19|20)\d\d[a-z]?\)")
PROPER = re.compile(r"\b(?:[A-Z][a-z]+(?:[-'][A-Z]?[a-z]+)?)(?:\s+(?:[A-Z][a-z]+|&|and|of|de|van|von)){0,3}\b")
_COMMON_CAPS = set("The A An In On At For To Of And But Or If When While Before After "
                   "This That These Those It Its We You They He She I My Our Your Their "
                   "Example Fix Note Step Tier".split())

def facts(text):
    """Specifics a rewrite is not allowed to introduce: numbers, years, citations,
    and capitalised names that are not sentence-initial function words."""
    t = strip_code(text)
    nums  = {n.strip().rstrip(".") for n in NUM.findall(t)}
    years = set(YEAR.findall(t))
    cites = {c.strip() for c in CITE.findall(t)}
    names = set()
    for m in PROPER.finditer(t):
        s = m.group().strip()
        first = s.split()[0]
        if first in _COMMON_CAPS and len(s.split()) == 1: continue
        i = m.start(); prev = t[max(0, i - 2):i]
        if len(s.split()) == 1 and (i == 0 or prev.strip().endswith((".", "!", "?", ":")) or not prev.strip()):
            continue
        names.add(s)
    return {"numbers": nums, "years": years, "citations": cites, "names": names}

def compare(src_path, new_path):
    """Report every specific in the rewrite that the source does not contain.
    Zero is the target. This is the no-fabrication rule as a check instead of
    a promise: a model can say it invented nothing; this shows whether it did."""
    src_text = open(src_path, encoding="utf-8").read()
    a, b = facts(src_text), facts(open(new_path, encoding="utf-8").read())
    src_tokens = set(re.findall(r"[a-z]+", src_text.lower()))
    print(f"\n=== compare: {new_path} against {src_path} ===")
    total = 0
    for k, label in (("numbers", "NEW-NUMBER"), ("years", "NEW-YEAR"), ("citations", "NEW-CITATION"), ("names", "NEW-NAME")):
        new = sorted(b[k] - a[k])
        if k == "names":
            new = [n for n in new if not all(w.lower() in src_tokens for w in n.split())]
        total += len(new)
        if new:
            print(f"  [{label}] {len(new)}: " + ", ".join(new[:12]) + (" ..." if len(new) > 12 else ""))
    if not total:
        print("  no specifics in the rewrite that were absent from the source")
    print("\n  The rewrite may still be wrong in ways this cannot see; it can only see what was added.")
    return total

def report(name, text):
    out, wc = find(text)
    print(f"\n=== {name} ({wc} words) ===")
    print(f"  vocabulary: {VOCAB_SOURCE}")
    if not out:
        print("  clean on the mechanical passes")
    for kind, msg in out:
        print(f"  [{kind}] {msg}")
    print("\n  These are counts, not a verdict. Judgment checks are in references/preflight.md.")
    return out

def _demo_text():
    """Built from the LOADED tiers, so this self-check tracks the catalogue instead of
    a copy of it. Two Tier 2 words in one paragraph; a Tier 3 word repeated past 3%."""
    t2 = [w for w in TIER2 if " " not in w][:2] or ["crucial", "foster"]
    t3 = next((w for w in TIER3 if " " not in w), "key")
    return f"""# The Evolving Landscape Of Modern Systems

We delve into a rich tapestry of ideas here \u2014 and it is worth noting that the
approach is seamless. Great question!

A {t2[0]} finding. The team built a {t2[1]} pipeline over the quarter and shipped
it without incident, which mattered.

The {t3} point is the {t3} point and the {t3} point, a {t3} one, and {t3} again.

- **First:** first
- **Second:** second
- **Third:** third

Here is a \u201cquoted\u201d phrase with a zero\u200bwidth space. See https://x.com/?utm_source=chatgpt.com
"""
DEMO = None

if __name__ == "__main__":
    if "--demo" in sys.argv:
        got = {k for k, _ in report("demo", _demo_text())}
        want = {"DASH", "TIER1", "TIER2", "TIER3", "ARTIFACT", "FORMAT", "QUOTES", "INVISIBLE"}
        missing = want - got
        print(f"\n  self-check: {'PASS' if not missing else 'FAIL, missed ' + ', '.join(sorted(missing))}")
        sys.exit(1 if missing else 0)
    if "--compare" in sys.argv:
        i = sys.argv.index("--compare")
        try:
            src, new = sys.argv[i + 1], sys.argv[i + 2]
        except IndexError:
            print("usage: prose-scan.py --compare SOURCE REWRITE"); sys.exit(2)
        sys.exit(1 if compare(src, new) else 0)
    if len(sys.argv) < 2:
        print(__doc__); sys.exit(2)
    for path in sys.argv[1:]:
        report(path, open(path, encoding="utf-8").read())
