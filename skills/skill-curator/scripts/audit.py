#!/usr/bin/env python3
"""Mechanical half of a skill-library audit. Findings, never scores.

Everything here is arithmetic a reader does badly across a library: pairwise
description comparison grows as n squared, line counts drift, a reference link
rots silently. Run it first, then spend the reading on scope, staleness and
whether a skill should exist.

    python3 audit.py ~/.claude/skills
    python3 audit.py --demo
"""
import re, sys, pathlib, itertools, tempfile

# Description boilerplate. These words say nothing about a skill's territory, and
# leaving them in makes every pair look related.
STOP = set("""a an the and or of to for in on with when use used using this that it its
is are be as by from at into not do does user users you your what which who whether
also only own right runs run trigger triggers invoked invoke explicitly exact wants want
asks asked ask existing before after new one two more most any all each every some
other others than then there here about across over under between within
skill skills claude agent agents tool tools file files code
need needs needed make makes making get gets got give gives given
work works working task tasks thing things way ways
should would could can may might will just even still
NOT""".split())

def frontmatter(p):
    t = p.read_text(errors="ignore")
    m = re.match(r"\A---\n(.*?)\n---\n", t, re.S)
    fm = {}
    if m:
        lines, i = m.group(1).split("\n"), 0
        while i < len(lines):
            k = re.match(r"^([a-zA-Z-]+):\s*(.*)$", lines[i])
            if not k:
                i += 1; continue
            key, val = k.group(1), k.group(2).strip()
            # block scalars: "description: >" or "|" with the text indented beneath
            if val in {">", "|", ">-", "|-", ">+"}:
                body, i = [], i + 1
                while i < len(lines) and (not lines[i].strip() or lines[i].startswith((" ", "\t"))):
                    body.append(lines[i].strip()); i += 1
                fm[key] = " ".join(x for x in body if x)
                continue
            fm[key] = val.strip('"\'')
            i += 1
    return fm, t

def load(root):
    out = []
    for skill in sorted(p for p in root.iterdir() if p.is_dir()):
        main = skill / "SKILL.md"
        if not main.exists(): continue
        fm, text = frontmatter(main)
        refs = sorted((skill / "references").glob("*.md")) if (skill / "references").is_dir() else []
        out.append({"name": skill.name, "path": skill, "fm": fm, "text": text,
                    "lines": text.count("\n") + 1,
                    "desc": fm.get("description", ""), "refs": refs,
                    "scripts": sorted((skill / "scripts").glob("*")) if (skill / "scripts").is_dir() else []})
    return out

def keywords(d):
    return {w for w in re.findall(r"[a-z]{3,}", d.lower()) if w not in STOP}

def audit(root):
    skills = load(root)
    findings = []
    if not skills:
        return [("EMPTY", f"no skills with a SKILL.md under {root}")], skills

    # Description collisions. Proportion is the wrong measure: a long description
    # dilutes any ratio, so two skills in the same domain can share every trigger word
    # and still score low. What matters is whether they share DISTINCTIVE terms and
    # neither description names the other as the place to go instead.
    kw = {s["name"]: keywords(s["desc"]) for s in skills}
    freq = {}
    for ks in kw.values():
        for w in ks: freq[w] = freq.get(w, 0) + 1
    # Rank pairs by how much territory they share, and report rather than assert.
    # Which overlaps actually compete is a judgement; the arithmetic just says where
    # to look. A pair whose descriptions name each other is already disambiguated.
    pairs = []
    for a, b in itertools.combinations(skills, 2):
        shared = kw[a["name"]] & kw[b["name"]]
        if len(shared) < 2: continue
        names = lambda x, y: re.search(re.escape(y["name"]), x["desc"], re.I)
        if names(a, b) or names(b, a): continue
        # weight a term by how rare it is across the library: a word in two
        # descriptions discriminates, a word in eight is the house vocabulary
        score = sum(1 / freq[w] for w in shared)
        pairs.append((score, a["name"], b["name"], sorted(shared, key=lambda w: freq[w])))
    for score, an, bn, shared in sorted(pairs, reverse=True)[:5]:
        findings.append(("NEAR-PAIR",
            f"{an} vs {bn}: share {', '.join(shared[:6])}, and neither names the other. "
            "Check whether one prompt could match both; if so, add the NOT-for clause."))

    for s in skills:
        if not s["desc"]:
            findings.append(("NO-DESC", f"{s['name']}: no description in frontmatter, so it "
                                        "cannot be routed to automatically"))
        elif len(s["desc"]) > 1024:
            findings.append(("DESC-LONG", f"{s['name']}: description is {len(s['desc'])} chars "
                                          "and loads every session, for every skill"))
        boundary = re.search(r"\bNOT for\b|\bnot for\b|\binstead\b|\brather than\b|"
                             r"\buse [\w-]+ (?:for|instead|when)\b", s["desc"], re.I)
        if not boundary and len(skills) > 1:
            findings.append(("NO-BOUNDARY", f"{s['name']}: description names no neighbouring "
                                            "territory, which is the clause that fixes collisions"))
        if s["lines"] > 400:
            findings.append(("BLOAT", f"{s['name']}: SKILL.md is {s['lines']} lines and loads "
                                      f"whole on every trigger; push detail into references/"))
        # rotted internal links
        for link in re.findall(r"\]\((?!https?:)([^)#]+)", s["text"]):
            target = (s["path"] / link).resolve()
            if not target.exists():
                findings.append(("DEAD-LINK", f"{s['name']}: SKILL.md links {link}, which is missing"))
        # a script it names but does not ship
        for m in re.findall(r"`?(?:scripts/)([\w-]+\.(?:py|js|sh))`?", s["text"]):
            if not any(x.name == m for x in s["scripts"]):
                findings.append(("MISSING-SCRIPT", f"{s['name']}: names scripts/{m} but does not ship it"))
        # Provenance means a RECORD, not a file with the right name. A harvest log is
        # a table with sources and dates in it; a format reference that happens to be
        # called harvest-log.md is documentation, and passing it here is how the skill
        # that audits provenance ended up with none of its own.
        def is_record(p):
            t = p.read_text(errors="ignore")
            return bool(re.search(r"\b20\d\d-\d\d-\d\d\b", t)) and bool(re.search(r"https?://", t))
        prov_files = [x for x in s["refs"] if x.name in {"harvest-log.md", "maintenance.md"}]
        prov_files += [p for p in [s["path"] / "ATTRIBUTION.md"] if p.exists()]
        if not any(is_record(p) for p in prov_files):
            findings.append(("NO-PROVENANCE", f"{s['name']}: no file records where it came from "
                                              "(a source URL and a date), so an update starts from zero"))
    if len(skills) > 10:
        findings.append(("COUNT", f"{len(skills)} skills in one scope. Past roughly ten, the "
                                  "discovery budget means some stop being surfaced at all."))
    return findings, skills

def report(root):
    findings, skills = audit(root)
    print(f"\n=== {root} ===")
    for s in skills:
        print(f"  {s['name']:<24}{s['lines']:>5} lines  {len(s['refs'])} refs  "
              f"{len(s['scripts'])} scripts  desc {len(s['desc'])} chars")
    print()
    for kind, msg in sorted(findings):
        print(f"  [{kind}] {msg}")
    if not findings:
        print("  clean on the mechanical passes")
    print("\n  Counts, not verdicts. Scope, staleness and whether a skill should exist "
          "are in SKILL.md.")
    return findings

DEMO_A = """---
name: alpha
description: Remove AI writing patterns from prose and make text sound human.
---
# Alpha
See [refs](references/gone.md) and run `scripts/nope.py`.
"""
DEMO_B = """---
name: beta
description: Remove AI patterns from prose so text sounds human when writing.
---
# Beta
"""

if __name__ == "__main__":
    if "--demo" in sys.argv:
        d = pathlib.Path(tempfile.mkdtemp())
        for n, body in (("alpha", DEMO_A), ("beta", DEMO_B)):
            (d / n).mkdir(); (d / n / "SKILL.md").write_text(body)
        got = {k for k, _ in report(d)}
        want = {"NEAR-PAIR", "DEAD-LINK", "MISSING-SCRIPT", "NO-PROVENANCE", "NO-BOUNDARY"}
        missing = want - got
        print(f"\n  self-check: {'PASS' if not missing else 'FAIL, missed ' + ', '.join(sorted(missing))}")
        sys.exit(1 if missing else 0)
    report(pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else
                        pathlib.Path.home() / ".claude/skills").expanduser())
