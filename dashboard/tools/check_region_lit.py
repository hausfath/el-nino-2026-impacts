"""Check data/region_lit.json (the literature text shown in the dashboard El Niño tab): every URL must appear verbatim in the
blog draft or the research dossiers, prose must carry no hardcoded hit/model counts, and every region needs an entry.
usage: python3 tools/check_region_lit.py"""
import json, re, os, sys
HERE_DATA = os.path.relpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data"),
                            os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))   # video/data or dashboard/data
os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
ALL_SRC = ["cb_el_nino_impacts_draft.md"] + ["research/"+f for f in [
 "impacts-literature.md","lit_africa_iod.md","lit_canada_nw.md","lit_chile_altiplano.md","lit_europe.md",
 "lit_missing_americas.md","lit_missing_asiapacific.md","impacts-verification-americas.md",
 "impacts-verification-asia-foundational.md","FACTCHECK.md"]]
# The public repo leaves out the blog draft and two files tied to a separate piece; links and source lines that only
# point there are reported as "not checkable here" instead of failures.
SRC = [f for f in ALL_SRC if os.path.exists(f)]
ABSENT = [f for f in ALL_SRC if f not in SRC]
if ABSENT: print("source files not in this checkout:", ", ".join(ABSENT))
text = {f: open(f, encoding="utf-8").read() for f in SRC}
lines = {f: t.split("\n") for f, t in text.items()}
d = json.load(open(os.path.join(HERE_DATA, "region_lit.json"), encoding="utf-8"))
reg = json.load(open(os.path.join(HERE_DATA, "regions.json")))
unchk = 0
PROSE = ["headline","why","past","caveat"]
fails = 0

# structure
need = set(reg["regions"]) | set(reg["extras"]) | {"_global","_tour"}
miss = need - set(d); extra = set(d) - need
print("keys: %d present; missing=%s extra=%s" % (len(d), sorted(miss), sorted(extra))); fails += bool(miss or extra)
tour = d["_tour"]
print("tour stops:", len(tour)); fails += not (4 <= len(tour) <= 6)
for s in tour:
    bad = [k for k in s["regions"] if k not in d or k.startswith("_")]
    if bad: print("  TOUR BAD KEY", s["id"], bad); fails += 1

entries = {k: v for k, v in d.items() if k != "_tour"}
# (a) URLs verbatim
urls = [(k, l["url"]) for k, v in entries.items() for l in v["links"]]
print("\n(a) URL check: %d links, %d unique" % (len(urls), len(set(u for _, u in urls))))
for k, u in urls:
    hit = [f for f in SRC if u in text[f]]
    if not hit and ABSENT: unchk += 1
    elif not hit: print("  FAIL", k, u); fails += 1
# prose must not contain http; labels in prose
allprose = []
for k, v in entries.items():
    p = " ".join(v[f] for f in PROSE)
    allprose.append((k, p))
    if "http" in p: print("  HTTP IN PROSE", k); fails += 1
    for l in v["links"]:
        if l["label"] not in p: print("  LABEL NOT IN PROSE", k, l["label"]); fails += 1
    if len(v["headline"]) > 70: print("  HEADLINE TOO LONG", k, len(v["headline"])); fails += 1
    for s in v["sources"]:
        f, n = s.rsplit(":", 1)
        if f in ABSENT:
            continue
        if f not in lines or not (1 <= int(n) <= len(lines[f])) or not lines[f][int(n)-1].strip():
            print("  BAD SOURCE REF", k, s); fails += 1
for s in tour: allprose.append(("_tour:"+s["id"], s["title"]+" "+s["text"]))

# (b) count patterns
pats = [r"\bof (8|13|12)\b", r"/(8|13|12)\b", r"\bof (6|7|9|10|11)\b", r"/1[0-3]\b",
        r"\b(all|every) (eight|six|five|seven|thirteen|13)\b", r"\bmedian\b", r"% of normal", r"\bof normal\b",
        r"La Niña (years|winters)", r"\b\d+ (out )?of \d+\b", r"\d\s?C\b",
        r"not [^.]{1,40}, (it'?s|but) ", r"\bnotably\b", r"\bcrucially\b", r"load-bearing", r"tapestry", r"\bnot (a|an) [^.]{1,40}, (a|an) "]
print("\n(b) count/pattern hits (eyeball):")
for k, p in allprose:
    for pat in pats:
        for m in re.finditer(pat, p):
            s = max(0, m.start()-50); print("  [%s] %-28s ...%s..." % (k, pat, p[s:m.end()+40].replace("\n"," ")))
em = sum(p.count("—") for _, p in allprose)
print("\nem-dash count:", em); fails += em > 2
if unchk: print(f"{unchk} links appear only in files not in this checkout (not checkable here)")
print("\nFAILURES:", fails)
