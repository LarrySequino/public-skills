#!/usr/bin/env python3
"""Find verbatim phrasing shared between a skill and its sources.

8-word runs. Short enough to catch a lifted sentence, long enough that a hit
is copying rather than two people describing the same thing.
"""
import re, sys, pathlib

N = 8
WORD = re.compile(r"[a-z0-9']+")

def words(t):
    t = re.sub(r"```.*?```", " ", t, flags=re.S)      # code fences
    t = re.sub(r"\[\[|\]\]|\{\{|\}\}|<[^>]+>", " ", t)  # wiki/html markup
    return WORD.findall(t.lower())

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

skill_root = pathlib.Path(sys.argv[1])
targets = text_files(skill_root)
src_root = pathlib.Path(sys.argv[2])

for src in sorted(src_root.iterdir()):
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
    if not total_hits:
        print("  no shared 8-word runs")
        continue
    runs.sort(key=lambda r: r[2] - r[1], reverse=True)
    print(f"  {total_hits} matching shingles in {len(runs)} runs")
    for t, a, b in runs[:6]:
        ws = words(t.read_text(errors="ignore"))
        print(f"  [{b - a + N} words] {t.name}: \"{' '.join(ws[a:b+N])[:170]}\"")
