---
name: data-first-voice
description: House voice for short technical write-ups that lead with a measured finding. Use when drafting or reviewing a post in this repo.
---

# Voice: data first, claim narrow, limits stated

Patterns taken from public technical-marketing writing that works for engineer readers: lead with a measurement, say exactly how it was measured, and say what it does not show. This file is the spec; `critic.py` checks a draft against it.

## Shape
1. Title states the finding or the question, not a slogan.
2. One-sentence claim in a quote block, directly under the title.
3. **TL;DR**: 3 to 5 bullets, each with a number or a decision.
4. Numbered sections; a table where a comparison is the point.
5. **What it means**: one concrete action per finding.
6. **Method and limits**: how the data was pulled, what was checked by hand and what agreed, what the data cannot show, a link to the code and data.
7. Closing line states who drafted it and how it was checked.

## Sentences
- First person, plain words, short sentences (average 24 words or fewer; none over 45).
- A number never appears without what it counts and the date range.
- A strong claim is followed by a caveat in the next sentence or two.
- Admit what you did not do ("I did not count distinct reporters").

## Do not
- Hype words: revolutionary, game-changing, seamless, unlock, supercharge, cutting-edge, best-in-class, leverage, delve.
- Claims about people or companies from public profiles. Aggregate counts only.
- Verdicts on a project's quality. Report what the data shows and stop.

## Pipeline (same order every time)
voice (this file) -> outline -> draft -> `python3 critic.py post.md` -> revise -> publish.
