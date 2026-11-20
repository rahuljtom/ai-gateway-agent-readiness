#!/usr/bin/env python3
"""Check a draft against voice/SKILL.md and against the data. Exit code 1 if any check fails.
Usage: python3 critic.py post.md [--csv data/scan.csv]"""
import argparse, csv, re, sys
from collections import Counter

HYPE = ["revolutionary", "game-changing", "game changing", "seamless", "unlock", "supercharge", "cutting-edge",
        "best-in-class", "leverage", "delve", "world-class", "blazing"]
LIMIT_PHRASES = ["i did not", "i didn't", "can't tell", "cannot tell", "does not show", "doesn't show", "not a ", "no way to"]

def sentences(text):
    text = re.sub(r"```.*?```", " ", text, flags=re.S)
    text = re.sub(r"\|.*\|", " ", text)           # table rows
    text = re.sub(r"[#>*`\[\]()-]", " ", text)
    return [s.split() for s in re.split(r"(?<=[.!?])\s+", text) if len(s.split()) > 2]

def facts(csv_path):
    rows = list(csv.DictReader(open(csv_path)))
    yes = lambda k: sum(r[k] == "True" for r in rows)
    return {"hosts scanned": f"{len(rows)} sites", "reachable": f"{sum(r['home_status'] == '200' for r in rows)} of {len(rows)}",
            "valid robots.txt": f"{yes('robots_valid')} of", "block any AI crawler": f"{yes('blocks_any_ai')} of",
            "llms.txt": f"{yes('llms_txt')} of", "llms-full.txt": f"{yes('llms_full_txt')} of",
            "sitemap": f"{yes('sitemap')} of", "markdown on request": f"{yes('markdown_on_request')} of"}

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("post"); ap.add_argument("--csv", default="data/scan.csv")
    a = ap.parse_args()
    t = open(a.post).read(); low = t.lower(); results = []
    def check(name, ok, detail=""): results.append((name, ok, detail))
    check("has TL;DR", "tl;dr" in low)
    tl = re.search(r"tl;dr\*{0,2}\s*\n((?:\s*[-*] .*\n?)+)", t, re.I)
    nb = len(re.findall(r"^\s*[-*] ", tl.group(1), re.M)) if tl else 0
    check("TL;DR has 3 to 5 bullets", 3 <= nb <= 5, f"{nb} bullets")
    check("has Method and limits section", re.search(r"^#+ .*method and limits", t, re.I | re.M) is not None)
    check("states at least 2 limitations", sum(p in low for p in LIMIT_PHRASES) >= 2)
    check("no hype words", not [w for w in HYPE if w in low], ", ".join(w for w in HYPE if w in low))
    s = sentences(t); lens = [len(x) for x in s]
    avg = sum(lens) / max(1, len(lens))
    check("average sentence <= 24 words", avg <= 24, f"{avg:.1f}")
    check("no sentence over 45 words", max(lens) <= 45, f"longest {max(lens)}")
    check("first person", re.search(r"\bI\b", t) is not None)
    check("links to code and data", "scan.py" in t and "scan.csv" in t)
    check("states who drafted it", "drafted with an ai" in low)
    for name, val in facts(a.csv).items():
        check(f"data fact present: {name} = {val}", val in t)
    width = max(len(n) for n, _, _ in results)
    for n, ok, d in results:
        print(f"{'PASS' if ok else 'FAIL'}  {n:<{width}}  {d}")
    failed = [n for n, ok, _ in results if not ok]
    print(f"\n{len(results)-len(failed)}/{len(results)} checks passed")
    sys.exit(1 if failed else 0)

if __name__ == "__main__":
    main()
