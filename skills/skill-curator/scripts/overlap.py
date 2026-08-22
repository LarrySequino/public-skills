#!/usr/bin/env python3
"""Find verbatim phrasing shared between a skill and its sources.

8-word runs: short enough to catch a lifted sentence, long enough to skip most
coincidence. A hit is a lead, not a verdict. Two people writing generic prose can
share nine words by accident ("helps users review pull requests safely and
consistently every"), so weigh run length, distinctiveness and genre before
concluding anything. A run of dozens of words is not a coincidence; a single
boilerplate sentence can be.
"""
import re, sys, pathlib

N = 8
WORD = re.compile(r"[a-z0-9']+")

def words(t):
    t = re.sub(r"```.*?```", " ", t, flags=re.S)      # code fences
    t = re.sub(r"\[\[|\]\]|\{\{|\}\}|<[^>]+>", " ", t)  # wiki/html markup
    return WORD.findall(t.lower())

CODE_N = 12   # longer than prose: shared idiom is common, shared blocks are not

def code_tokens(t):
    """Tokens inside fenced blocks only. Prose shingling drops code, which left the
    highest-risk material (a lifted script, with its license) invisible to the scan."""
    out = []
    for block in re.findall(r"```[^\n]*\n(.*?)```", t, flags=re.S):
        block = re.sub(r"#.*|//.*", " ", block)          # comments drift; code does not
        out.extend(re.findall(r"[A-Za-z_][A-Za-z0-9_]*|[(){}\[\].,:=+\-*/%<>!]+", block))
    return out

def shingles(ws):
    return {" ".join(ws[i:i+N]): i for i in range(len(ws) - N + 1)}

def load(paths, cap=2_000_000):
    out = []
    for p in paths:
        try:
            if p.stat().st_size > cap: continue
            out.extend(words(p.read_text(errors="ignore")))
            out.append("\x00")          # barrier: no runs across file joins
        except Exception: pass
    return out

def text_files(root):
    if root.is_file(): return [root]
    return [p for p in root.rglob("*")
            if p.is_file() and p.suffix.lower() in {".md", ".txt", ".mdx", ".rst"}
            and ".git" not in p.parts and "node_modules" not in p.parts]

skill_root = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else None
if "--demo" in sys.argv or skill_root is None:
    # Self-check: a known-copied passage must be found, unrelated prose must not.
    import tempfile
    shared = ("the quick brown fox jumps over the lazy dog and then keeps running "
              "down the hill toward the river bank")
    with tempfile.TemporaryDirectory() as d:
        d = pathlib.Path(d)
        (d / "skill").mkdir(); (d / "src" / "a").mkdir(parents=True); (d / "src" / "b").mkdir()
        (d / "skill" / "SKILL.md").write_text("intro line\n" + shared + "\nclosing line")
        (d / "src" / "a" / "doc.md").write_text("preamble\n" + shared + "\nepilogue")
        (d / "src" / "b" / "doc.md").write_text("wholly unrelated sentences about tide tables and "
                                                "harbor schedules with nothing in common at all")
        code = "```python\ndef parse(text):\n    rows = []\n    for line in text.splitlines():\n        rows.append(line.strip())\n    return rows\n```"
        (d / "skill" / "SKILL.md").write_text((d / "skill" / "SKILL.md").read_text() + "\n" + code)
        (d / "src" / "a" / "doc.md").write_text((d / "src" / "a" / "doc.md").read_text() + "\n" + code)
        tgt = text_files(d / "skill")
        hit = len(set(shingles(load(text_files(d / "src" / "a")))) & set(shingles(load(tgt))))
        miss = len(set(shingles(load(text_files(d / "src" / "b")))) & set(shingles(load(tgt))))
        ct = code_tokens((d / "skill" / "SKILL.md").read_text())
        cs = code_tokens((d / "src" / "a" / "doc.md").read_text())
        cb = code_tokens((d / "src" / "b" / "doc.md").read_text())
        sh = lambda ws: {" ".join(ws[i:i+CODE_N]) for i in range(len(ws) - CODE_N + 1)}
        code_hit = len(sh(cs) & sh(ct)); code_miss = len(sh(cb) & sh(ct))
    ok = hit > 0 and miss == 0 and code_hit > 0 and code_miss == 0
    print(f"  copied passage: {hit} shared runs (want >0); unrelated: {miss} (want 0)")
    print(f"  copied code: {code_hit} shared runs (want >0); unrelated code: {code_miss} (want 0)")
    print(f"  self-check: {'PASS' if ok else 'FAIL'}")
    sys.exit(0 if ok else 1)

targets = text_files(skill_root)
src_root = pathlib.Path(sys.argv[2])
# A file argument is one source, not a directory to walk. Passing a file used to
# raise NotADirectoryError from iterdir().
sources = [src_root] if src_root.is_file() else sorted(src_root.iterdir())

for src in sources:
    src_ws = load(text_files(src))
    if not src_ws: continue
    src_sh = set(shingles(src_ws))
    print(f"\n=== {src.name}  ({len(src_sh):,} shingles) ===")
    total_hits, runs = 0, []
    for t in targets:
        tw = words(t.read_text(errors="ignore"))
        hits = sorted(i for s, i in shingles(tw).items() if s in src_sh)
        total_hits += len(hits)
        # merge overlapping hit positions into contiguous runs
        for i in hits:
            if runs and runs[-1][0] == t and i <= runs[-1][2] + 1:
                runs[-1][2] = i
            else:
                runs.append([t, i, i])
    src_code = []
    for f in text_files(src):
        try: src_code.extend(code_tokens(f.read_text(errors="ignore")))
        except OSError: pass
    tgt_code = []
    for t in targets:
        tgt_code.extend(code_tokens(t.read_text(errors="ignore")))
    code_shared = 0
    if len(src_code) >= CODE_N and len(tgt_code) >= CODE_N:
        cs = {" ".join(src_code[i:i+CODE_N]) for i in range(len(src_code) - CODE_N + 1)}
        ct = {" ".join(tgt_code[i:i+CODE_N]) for i in range(len(tgt_code) - CODE_N + 1)}
        code_shared = len(cs & ct)
        if code_shared:
            print(f"  [CODE] {code_shared} shared {CODE_N}-token runs inside fenced blocks. "
                  "Copied code carries its own license; name the source in ATTRIBUTION.md.")
    if not total_hits:
        print("  no shared 8-word runs in prose" + ("" if code_shared else ""))
        continue
    runs.sort(key=lambda r: r[2] - r[1], reverse=True)
    print(f"  {total_hits} matching shingles in {len(runs)} runs")
    for t, a, b in runs[:6]:
        ws = words(t.read_text(errors="ignore"))
        print(f"  [{b - a + N} words] {t.name}: \"{' '.join(ws[a:b+N])[:170]}\"")
