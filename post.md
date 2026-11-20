# Are AI gateway sites readable by AI agents? A look at 20 sites

> None of the 18 AI gateway sites with a readable robots.txt blocks an AI crawler by name, and 15 of the 20 publish an llms.txt, so access is no longer the question; what agents are pointed to is.

When a developer asks an assistant which AI gateway to use, the assistant reads the web before it answers. I wanted to see how open the vendors in this category are to that reading. So on 2026-11-20 I checked four public files on 20 sites, and sent each home page one request asking for Markdown. Method and limits are at the end.

**TL;DR**
- I scanned 20 sites for 16 vendors in the AI gateway category on 2026-11-20. 19 of 20 answered; 18 of the 20 had a readable robots.txt.
- 0 of 18 block any of 10 named AI crawlers, training or search. An October 2026 study of the top 10,000 sites found that 22.2% of sites with a robots.txt block at least one ([source](https://kuldeep.cc/writing/who-blocks-ai-crawlers-robots-txt-study)).
- 15 of 20 publish an llms.txt and 7 of 20 publish an llms-full.txt. The same study found 9.8% of top sites with an llms.txt.
- 9 of 20 answer a request for Markdown with Markdown. 8 of those also publish an llms.txt.
- The five sites without an llms.txt are three large cloud and enterprise sites and two docs sites.

## 1. What I checked

For each site I fetched `/robots.txt`, `/llms.txt`, `/llms-full.txt` and `/sitemap.xml`. I also sent the home page one request with the header `Accept: text/markdown`. I read robots.txt rules per RFC 9309 (simplified), and counted a crawler as blocked when its group, or the `*` group, disallows `/` with no allow for the root. The 10 crawlers are GPTBot, ClaudeBot, Google-Extended, CCBot, Applebot-Extended, Bytespider and meta-externalagent (training), plus OAI-SearchBot, Claude-SearchBot and PerplexityBot (search and answers).

| Site | robots.txt readable | Blocks an AI crawler | llms.txt | llms-full.txt | sitemap | Markdown on request |
|---|---|---|---|---|---|---|
| getmaxim.ai | yes | no | yes | yes | yes | yes |
| docs.getbifrost.ai | yes | no | yes | yes | yes | yes |
| litellm.ai | yes | no | yes | no | yes | no |
| docs.litellm.ai | yes | no | yes | yes | yes | no |
| portkey.ai | yes | no | yes | no | yes | yes |
| docs.portkey.ai | no | no | no | no | no | yes |
| openrouter.ai | yes | no | yes | yes | yes | yes |
| www.helicone.ai | yes | no | yes | no | yes | no |
| docs.helicone.ai | no | no | no | no | no | no |
| truefoundry.com | yes | no | yes | no | yes | no |
| konghq.com | yes | no | yes | no | yes | no |
| developers.cloudflare.com | yes | no | yes | yes | yes | yes |
| vercel.com | yes | no | yes | no | yes | yes |
| traefik.io | yes | no | yes | no | yes | no |
| tyk.io | yes | no | yes | no | yes | yes |
| aigateway.envoyproxy.io | yes | no | yes | yes | yes | no |
| docs.docker.com | yes | no | yes | yes | yes | yes |
| learn.microsoft.com | yes | no | no | no | no | no |
| www.f5.com | yes | no | no | no | yes | no |
| cloud.google.com | yes | no | no | no | yes | no |

## 2. Nobody blocks, and most publish a guide

Zero of 18 blocks any of the 10 crawlers. That differs from the wider web, where the October study found publishers block training crawlers at about twice the rate of answer crawlers. Vendors who sell to developers appear to want to be read.

The llms.txt file is a plain-text guide to a site for language models. 15 of 20 publish one, against 9.8% of top sites in the October study. 17 of 20 publish a sitemap. I did not check what the llms.txt files point to.

## 3. Markdown on request is the split

9 of 20 sites return Markdown when asked, and 11 do not. All three large cloud and enterprise sites (Microsoft Learn, F5 and Google Cloud) lack both an llms.txt and Markdown on request. Eight sites do both: the two Bifrost sites, Portkey, OpenRouter, Cloudflare, Vercel, Tyk and Docker.

## 4. What it means

- **Being readable is table stakes in this category.** Access does not separate vendors now.
- **What separates them is what the file points to.** An llms.txt that lists the quickstart, the comparison pages and current pricing gives an assistant better material than one that lists everything.
- **If you run a gateway site:** check that the files exist, that they are current, and that the pages they link to carry dated, sourced numbers.
- **If you are choosing a gateway:** ask an assistant, then open the pages it cites and check the numbers yourself.

## Method and limits

- **Data:** four public files per site and one home-page request, fetched once on 2026-11-20 from one location, one request per file with a one-second pause. Code: [`scan.py`](scan.py). Data: [`data/scan.csv`](data/scan.csv). I chose the sites from the vendors that appear in public "best AI gateway" lists, so the sample is not random.
- **Check:** I read five robots.txt files by hand (Microsoft Learn, F5, Google Cloud, Vercel and Kong). Each had only a `*` group and no AI crawler rules, which matched the scanner. I also confirmed Markdown on request for three sites and the llms.txt result for two. A first run missed one site because of a redirect, and I fixed that and re-ran.
- **What this does not show:** whether any assistant reads llms.txt or uses Markdown, how often crawlers visit, or how a site ranks in answers. A site can block crawlers at the network edge without saying so in robots.txt. I tested the home page only for Markdown, and one docs site did not answer at all, so it counts as no data.
- **Window:** one day, so a later run may differ.

Drafted with an AI assistant and checked by hand against the data and the critic script. Corrections welcome.
