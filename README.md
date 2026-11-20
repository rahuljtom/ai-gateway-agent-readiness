# ai-gateway-agent-readiness

A small, reproducible check: how readable are AI gateway sites to AI agents? For 20 sites across 16 vendors it records what `robots.txt`, `llms.txt`, `llms-full.txt` and `sitemap.xml` say, and whether the home page answers in Markdown when asked.

**Read the write-up:** [`post.md`](post.md)

| File | What it is |
|---|---|
| `post.md` | The write-up (TL;DR, findings, what it means, method and limits) |
| `scan.py` | Fetches the public files and parses robots.txt rules |
| `data/hosts.csv` | The 20 sites checked, with vendor and kind (marketing or docs) |
| `data/scan.csv` | The result for each site, from the run on 2026-11-20 |
| `voice/SKILL.md` | The writing spec the post follows (data first, claim narrow, limits stated) |
| `critic.py` | Checks a draft against the voice spec and recomputes the key numbers from the CSV |
| `tests/` | Unit tests for the robots.txt parser |

## Reproduce
```bash
python3 scan.py                       # about three minutes; one request per file, one-second pause
python3 critic.py post.md             # checks the post against the voice spec and the data
python3 -I tests/test_robots.py
```
No dependencies beyond Python 3. Re-running later may give different results, so the numbers can differ from the post.

## Limits
One run, one location, 20 sites chosen from public vendor lists (not random). robots.txt rules are read in a simplified way. Zero blocks in robots.txt does not mean no policy, since sites can block at the network edge. Whether assistants use llms.txt or Markdown is not tested. See "Method and limits" in the post.

## How it was made
Drafted with an AI assistant, then checked by hand against the data. The pipeline is: voice spec, outline, draft, critic, revise, publish.

## License
MIT for the code; the data is public file metadata.
