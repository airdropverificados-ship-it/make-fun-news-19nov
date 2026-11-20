# The World in One Day — 19 November 2026 (v2, dense edition)

Entry for the make.fun bounty **"Sum up 19 November's world news in one image"**
(`make.fun/bounty/news-image-20261119`, $250, ends Fri 20 Nov 2026 19:00 CDT).

## What it is

A dense newspaper-front-page infographic (1024x1024 PNG, ~185 KB) summing up
Thursday 19 November 2026: masthead with the date, one lead story, and a
two-column grid of 34 more stories — **35 stories in total**, up from 12 in v1.

## How density stays legible

- Headlines are the only text in the grid (no summaries): each headline
  carries the key fact, so nothing is lost at small size.
- 15px bold headlines, max 2 lines per item; the build script warns if any
  headline would need a third line (none does).
- Colour-coded category tag inline at the start of each item, so the eye can
  scan by topic; zebra striping every other row keeps rows apart.
- High-contrast ink on paper, wide column gutter, no text over images.

## Stories covered (35)

**Lead — Shenzhen summit:** Trump, Xi and Putin sign a joint peace declaration
(first-ever meeting of the three leaders; no deal on Ukraine or Iran).

**Grid, left column:** ICJ rules Myanmar committed genocide against the
Rohingya, 9-6 · Tankers ablaze in the Strait of Hormuz, 11 crew hurt, one
missing · Ukraine strikes the Crimea bridge again, halting road traffic ·
Anthropic debuts on Nasdaq after a record $81.3B IPO; shares +17% · GTA VI
launches worldwide after a 13-year wait · Cyclone Akvan: India evacuates
80,000 in Odisha · US Senate rejects Iran war-powers resolution 51-48 ·
Hegseth announces US-Venezuela military pact · Migrant boat sinks off Senegal;
dozens missing · Texans rout Colts 26-3 (Thursday Night Football) · Magnitude
5.7 quake in Kumamoto, Japan · US stocks slide as AI bust continues despite
Anthropic IPO · US jobless claims unexpectedly rise · Japan's core inflation
accelerates, cementing rate-hike bets · Australia's jobless rate jumps to
highest since 2021 · Trump pardons late baseball legend Pete Rose for tax
crimes · Beloved hippo Fiona dies at Cincinnati Zoo after eating a hat.

**Grid, right column:** FCC votes to ban Chinese telecoms from US phone numbers
· UK and Norway fund £100m+ for two Ukrainian naval craft · Denmark's
parliament approves Greenland defence deal, 109-0 · APEC adopts Shenzhen
Outlook on trade, data and AI risks · Aid groups rate Gaza peace-plan
implementation 4 out of 26 · IDF ends Nuseirat camp invasion after one day;
4 killed in Gaza · Pakistan military kills 22 militants in Khyber Pakhtunkhwa
raids · Mongolia's parliament accepts president's resignation over graft claims
· India lets Japanese forces fire missiles on its ranges · COP31 draft drops
all fossil-fuel language; outcry in Antalya · Record 589m children now live in
conflict zones (Save the Children) · Fifteen nations back UK-Australia
sanctions on Israeli settlements · Democrats secure historic 56-seat Senate
majority in midterms · Physicists send a message through a brick wall using
gravity · England beat Australia by 97 runs to win ODI series 2-1 · Chelsea
beat PSG 1-0 in Women's Champions League · NC State beats Murray State 93-83;
McNeil's record 33 points.

## Sources and caveats

Facts were checked against public news reports on 20 Nov 2026: Reuters, CNN,
AP (via KXL/NBC), Dow Jones/Morningstar, The Times, Le Monde, Foreign
Exchanges, Standard Topic, University of Queensland, Gizmodo, Smithsonian,
USA Today, WSJ, and the Fayetteville Observer, plus aggregators (AppiSToS,
News Media House, LA Post) for items also carried there. No story was invented.

Caveats:
- The 56-seat Senate majority was confirmed when the final Alaska count was
  called on 17–18 Nov; the "historic 56-seat majority" story itself was
  published on 19 Nov.
- The gravity-message paper appeared in *Science Advances* on 18 Nov; the
  University of Queensland announcement and press coverage ran on 19 Nov.
- The 589m-children figure is Save the Children's record count as reported on
  19 Nov; Le Monde's same-day wording is "nearly a quarter of the world's
  children".
- The fifteen-nations sanctions story and the UK–Norway naval-craft programme
  rest on single-outlet reports (News Media House / AppiSToS) dated 19 Nov.

## How the program works

`main.py` (Python 3.13, standard library only) copies the pre-built image
`entry.png` to `/output/entry.png`. No network, no randomness: both runs write
identical bytes (verified by sha256). `build_image_v2.py` is the script that
generated `entry.png` with PIL (kept for transparency; it is not needed at
run time).

## License

MIT — see `LICENSE`.
