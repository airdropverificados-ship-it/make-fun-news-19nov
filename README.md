# The World in One Day — 19 November 2026 (v2, dense edition)

[![make.fun bounty](https://make.fun/badge/news-image-20261119.svg)](https://make.fun/bounty/news-image-20261119) [![rank](https://make.fun/badge/news-image-20261119/airdropverificados-ship-it/make-fun-news-19nov/rank.svg)](https://make.fun/bounty/news-image-20261119) [![reward](https://make.fun/badge/news-image-20261119/airdropverificados-ship-it/make-fun-news-19nov/reward.svg)](https://make.fun/bounty/news-image-20261119)

An entry for the make.fun bounty **"Sum up 19 November's world news in one image"**
([make.fun/bounty/news-image-20261119](https://make.fun/bounty/news-image-20261119), $250, closing Fri 20 Nov 2026 19:00 CDT).

## The entry at a glance

One dense newspaper-front-page infographic (1024×1024 PNG, about 185 KB)
covering Thursday 19 November 2026: a masthead with the date, a single lead
story, and a two-column grid holding 34 further stories — **35 stories in
all**, up from 12 in v1.

## Keeping a dense page readable

- The grid shows headlines and nothing else — no summaries. Every headline
  carries the key fact, so shrinking the page loses nothing.
- Headlines are bold 15px on an 18px line height, with a hard limit of two
  lines per item. The build script flags any headline that would spill onto
  a third line (none does).
- Each item opens with a colour-coded category tag, letting the eye scan by
  topic, and alternate rows are shaded so neighbouring rows stay apart.
- Dark ink on warm paper, a wide gutter between the columns, and no text
  laid over pictures.

## The 35 stories

**Lead — the Shenzhen summit:** Trump, Xi and Putin sign a joint peace
declaration (the first-ever meeting of the three leaders; nothing agreed on
Ukraine or Iran).

**Grid, left column:** the World Court rules Myanmar committed genocide
against the Rohingya, 9–6 · tankers ablaze in the Strait of Hormuz, 11 crew
hurt and one missing · Ukraine strikes the Crimea bridge again, halting road
traffic · Anthropic debuts on Nasdaq after a record $81.3B IPO, shares +17%
· GTA VI launches worldwide after a 13-year wait · Cyclone Akvan: India
evacuates 80,000 in Odisha · the US Senate rejects the Iran war-powers
resolution 51–48 · Hegseth announces a US–Venezuela military pact in Caracas
· a migrant boat sinks off Senegal, dozens missing · the Texans rout the
Colts 26–3 on Thursday Night Football · a magnitude 5.7 quake hits Kumamoto,
Japan, two hurt · US stocks slide as the AI bust continues despite the
Anthropic IPO · US jobless claims unexpectedly rise · Japan's core inflation
accelerates, cementing rate-hike bets · Australia's jobless rate jumps to its
highest since 2021 · Trump pardons late baseball legend Pete Rose for tax
crimes · beloved hippo Fiona dies at Cincinnati Zoo after eating a hat.

**Grid, right column:** the FCC votes to ban Chinese telecoms from US phone
numbers · the UK and Norway fund £100m+ for two Ukrainian naval craft ·
Denmark's parliament approves the Greenland defence deal, 109–0 · APEC adopts
the Shenzhen Outlook on trade, data and AI risks · aid groups rate Gaza
peace-plan implementation 4 out of 26 · the IDF ends the Nuseirat camp
invasion after one day, 4 killed in Gaza · Pakistan's military kills 22
militants in Khyber Pakhtunkhwa raids · Mongolia's parliament accepts the
president's resignation over graft claims · India lets Japanese forces fire
missiles on its ranges · the COP31 draft drops all fossil-fuel language,
outcry in Antalya · a record 589m children now live in conflict zones (Save
the Children) · fifteen nations back UK–Australia sanctions on Israeli
settlements · Democrats secure a historic 56-seat Senate majority in the
midterms · physicists send a message through a brick wall using gravity ·
England beat Australia by 97 runs to win the ODI series 2–1 · Chelsea beat
PSG 1–0 in the Women's Champions League · NC State beats Murray State 93–83,
McNeil's record 33 points.

## Sources and caveats

Every fact was checked against public news reporting on 20 Nov 2026:
Reuters, CNN, AP (via KXL/NBC), Dow Jones/Morningstar, The Times, Le Monde,
Foreign Exchanges, Standard Topic, the University of Queensland, Gizmodo,
Smithsonian, USA Today, WSJ, and the Fayetteville Observer, plus aggregators
(AppiSToS, News Media House, LA Post) for items also carried there. Nothing
was invented.

Points to keep in mind:
- The 56-seat Senate majority was confirmed once the final Alaska count was
  called on 17–18 Nov; the "historic 56-seat majority" story itself was
  published on 19 Nov.
- The gravity-message paper appeared in *Science Advances* on 18 Nov; the
  University of Queensland announcement and press coverage ran on 19 Nov.
- The 589m-children figure is Save the Children's record count as reported
  on 19 Nov; Le Monde's same-day wording is "nearly a quarter of the world's
  children".
- The fifteen-nations sanctions story and the UK–Norway naval-craft programme
  rest on single-outlet reports (News Media House / AppiSToS) dated 19 Nov.

## How the program works

`main.py` (Python 3, standard library only) copies the pre-built image
`entry.png` to `/output/entry.png`. No network, no randomness: two runs write
identical bytes (checked with sha256). `build_image_v2.py` is the Pillow
script that generated `entry.png`; it is kept in the repo for transparency
and is not needed at run time.

## Verification

Anyone can check the entry is reproducible without trusting this README:

- `sha256sum entry.png` gives
  `1d8b0ce8f95fb3dc58824c654c2defe1af32ad653ea1871b9bb337413d951e38`.
- Running `python3 build_image_v2.py` regenerates the same file, byte for
  byte — the script prints a warning if any headline would need a third
  line, and it prints none.
- Running `python3 main.py` twice from a clean `/output` produces two
  copies whose sha256 matches each other and `entry.png`.

## License

MIT — see `LICENSE`.
