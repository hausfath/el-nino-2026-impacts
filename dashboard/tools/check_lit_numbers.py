"""Every number in the prose of data/region_lit.json must appear in one of that entry's cited source lines (±4 lines),
and years are skipped. Prints the misses for review.  usage: python3 tools/check_lit_numbers.py"""
import json, re, os
HERE_DATA = os.path.relpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data"),
                            os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))   # video/data or dashboard/data
os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
L = json.load(open(os.path.join(HERE_DATA, "region_lit.json"), encoding="utf-8"))
cache = {}
def lines(f):
    if f not in cache: cache[f] = open(f, encoding="utf-8").read().split("\n")
    return cache[f]
norm = lambda s: s.replace(",", "").replace("−", "-").replace("–", "-").replace("—", "-")
unchk = 0   # numbers in entries that cite files not in this checkout (public repo)
NUM = re.compile(r"\d+(?:[.,]\d+)*")
miss = 0
for k, v in L.items():
    if k == "_tour":
        continue
    win = ""
    for ref in v.get("sources", []):
        f, _, n = ref.rpartition(":")
        try: n = int(n)
        except ValueError: continue
        if not os.path.exists(f): continue
        ls = lines(f); win += "\n".join(ls[max(0, n - 5): n + 4]) + "\n"
    win = norm(win)
    for fld in ("headline", "why", "past", "caveat"):
        for tok in NUM.findall(v.get(fld, "")):
            t = norm(tok)
            if re.fullmatch(r"(19|20)\d\d", t): continue
            if re.search(rf"(?<![\d.]){re.escape(t)}(?![\d])", win):
                continue
            if any(not os.path.exists(r.rpartition(":")[0]) for r in v.get("sources", [])):
                unchk += 1; continue
            miss += 1
            i = v[fld].find(tok); print(f"  [{k}.{fld}] {tok!r}: ...{v[fld][max(0, i - 50): i + 40]}...")
print(f"\n{miss} numbers not found in the cited source lines" + (f"; {unchk} not checkable here (cite files not in this checkout)" if unchk else ""))
