#!/usr/bin/env python3
"""Are AI gateway sites readable by AI agents?

For each host in data/hosts.csv, fetch four public files and record what they say:
  /robots.txt  -> which AI crawlers are blocked (parsed per RFC 9309, simplified)
  /llms.txt and /llms-full.txt -> present or not
  /sitemap.xml -> present or not
and send one request with `Accept: text/markdown` to the home page to see whether it answers in Markdown.
Public files only, one request each, a one-second pause between requests, an honest User-Agent.
Usage: python3 scan.py [--hosts data/hosts.csv] [--out data/scan.csv]
"""
import argparse, csv, re, time, urllib.request, urllib.error

UA = "ai-gateway-agent-readiness-study (public files only; one request per file)"
TRAINING = ["GPTBot", "ClaudeBot", "Google-Extended", "CCBot", "Applebot-Extended", "Bytespider", "meta-externalagent"]
SEARCH = ["OAI-SearchBot", "Claude-SearchBot", "PerplexityBot"]

class _Redirect(urllib.request.HTTPRedirectHandler):
    """Follow 308 as well (older Python versions don't)."""
    def http_error_308(self, req, fp, code, msg, headers):
        return self.http_error_302(req, fp, 301, msg, headers)

_OPENER = urllib.request.build_opener(_Redirect)

def get(url, accept=None):
    h = {"User-Agent": UA}
    if accept: h["Accept"] = accept
    try:
        with _OPENER.open(urllib.request.Request(url, headers=h), timeout=20) as r:
            return r.status, r.headers.get("content-type", ""), r.read(400000).decode("utf-8", "ignore")
    except urllib.error.HTTPError as e:
        return e.code, "", ""
    except Exception:
        return 0, "", ""

def parse_robots(text):
    """Return {lowercase user-agent: [(directive, path), ...]}."""
    groups, cur, last_was_ua = {}, [], False
    for raw in text.splitlines():
        line = raw.split("#", 1)[0].strip()
        if ":" not in line: continue
        k, v = [x.strip() for x in line.split(":", 1)]
        k = k.lower()
        if k == "user-agent":
            if not last_was_ua: cur = []
            cur.append(v.lower()); groups.setdefault(v.lower(), []); last_was_ua = True
        elif k in ("allow", "disallow"):
            for ua in cur: groups[ua].append((k, v))
            last_was_ua = False
        else:
            last_was_ua = False
    return groups

def blocked(groups, bot):
    rules = groups.get(bot.lower()) if bot.lower() in groups else groups.get("*", [])
    has_block = any(d == "disallow" and p == "/" for d, p in rules)
    has_allow_root = any(d == "allow" and p == "/" for d, p in rules)
    return has_block and not has_allow_root

def valid_text_file(status, ctype, body):
    return status == 200 and "html" not in ctype.lower() and not body.lstrip().lower().startswith("<!doctype") and bool(body.strip())

def scan(host):
    base = "https://" + host
    row = {"host": host}
    s, c, b = get(base + "/robots.txt"); time.sleep(1)
    row["robots_valid"] = valid_text_file(s, c, b) and "user-agent" in b.lower()
    g = parse_robots(b) if row["robots_valid"] else {}
    row["blocked_training"] = [t for t in TRAINING if row["robots_valid"] and blocked(g, t)]
    row["blocked_search"] = [t for t in SEARCH if row["robots_valid"] and blocked(g, t)]
    row["blocks_any_ai"] = bool(row["blocked_training"] or row["blocked_search"])
    s, c, b = get(base + "/llms.txt"); time.sleep(1)
    row["llms_txt"] = valid_text_file(s, c, b) and ("](" in b or b.lstrip().startswith("#"))
    s, c, b = get(base + "/llms-full.txt"); time.sleep(1)
    row["llms_full_txt"] = valid_text_file(s, c, b) and len(b) > 200
    s, c, b = get(base + "/sitemap.xml"); time.sleep(1)
    row["sitemap"] = s == 200 and ("<urlset" in b or "<sitemapindex" in b)
    s, c, b = get(base + "/", accept="text/markdown"); time.sleep(1)
    row["markdown_on_request"] = s == 200 and "markdown" in c.lower()
    row["home_status"] = s
    return row

if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("--hosts", default="data/hosts.csv"); ap.add_argument("--out", default="data/scan.csv")
    a = ap.parse_args()
    meta = list(csv.DictReader(open(a.hosts)))
    out = []
    for m in meta:
        r = scan(m["host"]); r.update(vendor=m["vendor"], kind=m["kind"])
        r["blocked_training"] = " ".join(r["blocked_training"]); r["blocked_search"] = " ".join(r["blocked_search"])
        out.append(r)
        print(f"{r['host']:<28} robots={'Y' if r['robots_valid'] else 'n'} blocks_ai={'Y' if r['blocks_any_ai'] else 'n'} llms={'Y' if r['llms_txt'] else 'n'} full={'Y' if r['llms_full_txt'] else 'n'} sitemap={'Y' if r['sitemap'] else 'n'} md={'Y' if r['markdown_on_request'] else 'n'} home={r['home_status']}")
    cols = ["host", "vendor", "kind", "home_status", "robots_valid", "blocks_any_ai", "blocked_training", "blocked_search", "llms_txt", "llms_full_txt", "sitemap", "markdown_on_request"]
    with open(a.out, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols); w.writeheader(); w.writerows([{k: r[k] for k in cols} for r in out])
