#!/usr/bin/env python3
"""Cross-language consistency audit: docs/paper_en.md  vs  docs/paper_cn.md"""
import re
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT = Path(__file__).resolve().parent.parent
EN = (ROOT / "docs" / "paper_en.md").read_text(encoding="utf-8").splitlines()
CN = (ROOT / "docs" / "paper_cn.md").read_text(encoding="utf-8").splitlines()

print(f"EN={len(EN)} lines   CN={len(CN)} lines")
if len(EN) != len(CN):
    print("!! line counts differ — alignment cannot be assumed")
n = min(len(EN), len(CN))

# ---- 1. structural alignment -------------------------------------------------
print("\n=== 1. structural alignment (heading / table-row positions) ===")
mismatch = []
for i in range(n):
    e, c = EN[i], CN[i]
    e_kind = "H" if re.match(r"^#{1,3} ", e) else ("T" if e.startswith("|") else "P")
    c_kind = "H" if re.match(r"^#{1,3} ", c) else ("T" if c.startswith("|") else "P")
    if e_kind != c_kind:
        mismatch.append((i + 1, e_kind, c_kind, e[:70], c[:70]))
if mismatch:
    for ln, ek, ck, es, cs in mismatch:
        print(f"  MISMATCH L{ln}: EN={ek} CN={ck}\n     EN: {es}\n     CN: {cs}")
else:
    print("  all line kinds aligned (H/T/P) — 0 mismatches")

# ---- 2. token-level counts ---------------------------------------------------
TOKENS = [
    "RPT_1", "RPT_2", "GWT_1", "GWT_2", "GWT_3", "GWT_4",
    "HOT_1", "HOT_2", "HOT_3", "HOT_4", "AST_1", "PP_1", "AE_1", "AE_2",
    "R0-", "R1-", "R2-", "R3-", "R4-", "R5-",
    "✅", "🔶", "❌", "—",
    "Tier-1", "Tier-2",
    "Kammerer", "Schwitzgebel", "Butlin", "Friston", "Seth", "Thompson",
    "Damasio", "Maturana", "Varela", "Godfrey-Smith", "Ginsburg", "Jablonka",
    "Birch", "Velmans", "Atmanspacher", "FlyWire", "Minecraft", "Bénard",
    "RPT", "GWT", "HOT", "AST", "PP", "AE",
]
print("\n=== 2. token counts ===")
bad = 0
for t in TOKENS:
    e = sum(line.count(t) for line in EN)
    c = sum(line.count(t) for line in CN)
    if e != c:
        print(f"  DIFF {t!r}: EN={e} CN={c}")
        bad += 1
print(f"  {len(TOKENS)} tokens checked, {bad} differing")

# ---- 2b. localise the differing tokens --------------------------------------
if bad:
    print("\n=== 2b. where the differing tokens occur ===")
    for t in TOKENS:
        lines = [i + 1 for i in range(n) if EN[i].count(t) != CN[i].count(t)]
        if not lines:
            continue
        print(f"  {t!r} differs on line(s): {lines}")
        for ln in lines[:4]:
            print(f"    L{ln}")
            print(f"      EN: {EN[ln-1][:140]}")
            print(f"      CN: {CN[ln-1][:140]}")

# ---- 3. years ----------------------------------------------------------------
def years(lines):
    d = {}
    for line in lines:
        for y in re.findall(r"(?:19|20)\d{2}", line):
            d[y] = d.get(y, 0) + 1
    return d

ey, cy = years(EN), years(CN)
print("\n=== 3. years ===")
for y in sorted(set(ey) | set(cy)):
    a, b = ey.get(y, 0), cy.get(y, 0)
    print(f"  {y}: EN={a} CN={b}" + ("   <-- DIFF" if a != b else ""))

# ---- 4. per-line numbers -----------------------------------------------------
print("\n=== 4. lines whose numeric content differs ===")
diffs = 0
for i in range(n):
    e = re.findall(r"\d+(?:\.\d+)?", EN[i])
    c = re.findall(r"\d+(?:\.\d+)?", CN[i])
    if e != c:
        diffs += 1
        print(f"  L{i+1}: EN={e}")
        print(f"        CN={c}")
        print(f"     EN: {EN[i][:110]}")
        print(f"     CN: {CN[i][:110]}")
if not diffs:
    print("  none")

# ---- 5. table rows: cell-by-cell symbol comparison ---------------------------
print("\n=== 5. matrix table rows (verdict cells) ===")
for i in range(n):
    if EN[i].startswith("| **") and CN[i].startswith("| **"):
        ec = [x.strip() for x in EN[i].split("|")[1:-1]]
        cc = [x.strip() for x in CN[i].split("|")[1:-1]]
        if len(ec) < 4 or len(cc) < 4:
            continue
        # index 1..3 are Tier-1 / Tier-2 / final verdict
        def sym(x):
            return "".join(ch for ch in x if ch in "✅🔶❌—")
        e3, c3 = [sym(v) for v in ec[1:4]], [sym(v) for v in cc[1:4]]
        flag = "OK " if e3 == c3 else "DIFF"
        print(f"  L{i+1} {flag} EN={e3} CN={c3}  | {ec[0][:38]}")

# ---- 6. references -----------------------------------------------------------
print("\n=== 6. references ===")
def refs(lines):
    out = []
    started = False
    for line in lines:
        if re.match(r"^## (References|参考文献)", line):
            started = True
            continue
        if started and line.startswith("* "):
            m = re.search(r"\*([A-Z][^,*]+),", line)
            y = re.search(r"\((\d{4})\)", line)
            if m:
                out.append((m.group(1).strip(), y.group(1) if y else "?"))
    return out

er, cr = refs(EN), refs(CN)
print(f"  EN: {len(er)} entries   CN: {len(cr)} entries")
if er == cr:
    print("  identical author/year set ✅")
else:
    se, sc = set(er), set(cr)
    print(f"  only-in-EN: {sorted(se - sc)}")
    print(f"  only-in-CN: {sorted(sc - se)}")
    if se == sc:
        print("  (same set, order differs)")
