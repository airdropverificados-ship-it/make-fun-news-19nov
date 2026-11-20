#!/usr/bin/env python3
"""Build the DENSE v2 1024x1024 infographic for the make.fun bounty
'Sum up 19 November's world news in one image'.

35 verified stories from Thursday 19 November 2026: 1 lead story + a
34-item two-column grid. Pure PIL, deterministic — same bytes every run.

Legibility choices for density:
- Headlines are the only text in the grid (no summaries): each headline
  carries the key fact, so nothing is lost at small size.
- 15px bold headlines on a 18px line height, max 2 lines per item; the
  build FAILS loudly (warning + truncation) if any headline needs 3 lines.
- Colour-coded category tag inline at the start of line 1, so the eye can
  scan by topic; zebra striping every other row to keep rows apart.
- High-contrast ink on paper, generous column gutter, no text over images.
"""
from PIL import Image, ImageDraw, ImageFont

OUT = "/home/hatch/workspace/make-fun-bounties/news-19nov-v2/entry.png"

W, H = 1024, 1024
M = 24  # margin
PAPER = (246, 241, 231)
ZEBRA = (240, 234, 220)
INK = (20, 20, 20)
GRAY = (90, 86, 78)
RED = (185, 28, 28)
NAVY = (30, 58, 95)

FD = "/usr/share/fonts/truetype/dejavu/"
f_title = ImageFont.truetype(FD + "DejaVuSerif-Bold.ttf", 46)
f_date = ImageFont.truetype(FD + "DejaVuSans-Bold.ttf", 19)
f_lead_tag = ImageFont.truetype(FD + "DejaVuSans-Bold.ttf", 16)
f_lead_head = ImageFont.truetype(FD + "DejaVuSans-Bold.ttf", 30)
f_lead_sum = ImageFont.truetype(FD + "DejaVuSans.ttf", 16)
f_section = ImageFont.truetype(FD + "DejaVuSans-Bold.ttf", 15)
f_tag = ImageFont.truetype(FD + "DejaVuSans-Bold.ttf", 13)
f_head = ImageFont.truetype(FD + "DejaVuSans-Bold.ttf", 15)
f_foot = ImageFont.truetype(FD + "DejaVuSans.ttf", 13)

# tag -> colour
COLORS = {
    "JUSTICE": (109, 40, 217), "CONFLICT": (194, 65, 12), "WAR": (153, 27, 27),
    "TECH": (29, 78, 216), "CULTURE": (21, 128, 61), "WEATHER": (15, 118, 110),
    "US": (30, 58, 95), "US POLITICS": (30, 58, 95),
    "MIGRATION": (120, 53, 15), "SPORTS": (190, 24, 93),
    "CRICKET": (190, 24, 93), "FOOTBALL": (190, 24, 93),
    "BASKETBALL": (190, 24, 93), "QUAKES": (100, 100, 100),
    "MARKETS": (180, 83, 9), "ECONOMY": (180, 83, 9),
    "ANIMALS": (101, 163, 13), "UKRAINE": (202, 138, 4),
    "DEFENCE": (71, 85, 105), "APEC": (29, 78, 216),
    "GAZA": (153, 27, 27), "PAKISTAN": (107, 33, 168),
    "MONGOLIA": (107, 33, 168), "ASIA": (107, 33, 168),
    "CLIMATE": (21, 128, 61), "CHILDREN": (190, 24, 93),
    "DIPLOMACY": (107, 33, 168), "SCIENCE": (8, 145, 178),
}

# The 34 grid stories (the lead story is drawn separately). Order: v1's
# six cards, v1's five ticker items, then the 23 new stories.
STORIES = [
    ("JUSTICE", "World Court: Myanmar committed genocide against the Rohingya, 9-6"),
    ("CONFLICT", "Tankers ablaze in the Strait of Hormuz; 11 crew hurt, one missing"),
    ("WAR", "Ukraine strikes the Crimea bridge again, halting road traffic"),
    ("TECH", "Anthropic debuts on Nasdaq after record $81.3B IPO; shares +17%"),
    ("CULTURE", "GTA VI launches worldwide after a 13-year wait"),
    ("WEATHER", "Cyclone Akvan: India evacuates 80,000 in Odisha"),
    ("US", "US Senate rejects Iran war-powers resolution, 51-48"),
    ("US", "Hegseth announces US-Venezuela military pact in Caracas"),
    ("MIGRATION", "Migrant boat sinks off Senegal; dozens missing"),
    ("SPORTS", "Texans rout Colts 26-3 on Thursday Night Football"),
    ("QUAKES", "Magnitude 5.7 quake hits Kumamoto, Japan; two hurt"),
    ("MARKETS", "US stocks slide as AI bust continues despite Anthropic IPO"),
    ("ECONOMY", "US jobless claims unexpectedly rise; ongoing claims surge"),
    ("ECONOMY", "Japan's core inflation accelerates, cementing rate-hike bets"),
    ("ECONOMY", "Australia's jobless rate jumps to highest since 2021"),
    ("US", "Trump pardons late baseball legend Pete Rose for tax crimes"),
    ("ANIMALS", "Beloved hippo Fiona dies at Cincinnati Zoo after eating a hat"),
    ("TECH", "FCC votes to ban Chinese telecoms from US phone numbers"),
    ("UKRAINE", "UK and Norway fund \u00a3100m+ for two Ukrainian naval craft"),
    ("DEFENCE", "Denmark's parliament approves Greenland defence deal, 109-0"),
    ("APEC", "APEC adopts Shenzhen Outlook on trade, data and AI risks"),
    ("GAZA", "Aid groups rate Gaza peace-plan implementation 4 out of 26"),
    ("GAZA", "IDF ends Nuseirat camp invasion after one day; 4 killed in Gaza"),
    ("PAKISTAN", "Pakistan military kills 22 militants in Khyber Pakhtunkhwa raids"),
    ("MONGOLIA", "Mongolia's parliament accepts president's resignation over graft claims"),
    ("ASIA", "India lets Japanese forces fire missiles on its ranges"),
    ("CLIMATE", "COP31 draft drops all fossil-fuel language; outcry in Antalya"),
    ("CHILDREN", "Record 589m children now live in conflict zones \u2014 Save the Children"),
    ("DIPLOMACY", "Fifteen nations back UK-Australia sanctions on Israeli settlements"),
    ("US POLITICS", "Democrats secure historic 56-seat Senate majority in midterms"),
    ("SCIENCE", "Physicists send a message through a brick wall using gravity"),
    ("CRICKET", "England beat Australia by 97 runs to win ODI series 2-1"),
    ("FOOTBALL", "Chelsea beat PSG 1-0 in Women's Champions League"),
    ("BASKETBALL", "NC State beats Murray State 93-83; McNeil's record 33 points"),
]

assert len(STORIES) == 34, len(STORIES)

img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)


def wrap(text, font, first_w, rest_w):
    """Wrap text; first line gets first_w, later lines rest_w."""
    words = text.split(" ")
    lines, cur, max_w = [], "", first_w
    for w in words:
        trial = (cur + " " + w).strip()
        if d.textlength(trial, font=font) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur, max_w = w, rest_w
    if cur:
        lines.append(cur)
    return lines


def center(text, font, y, fill):
    w = d.textlength(text, font=font)
    d.text(((W - w) / 2, y), text, font=font, fill=fill)


# ---- Masthead ----
center("THE WORLD IN ONE DAY", f_title, 16, INK)
center("THURSDAY, 19 NOVEMBER 2026  \u00b7  35 STORIES FROM AROUND THE GLOBE",
       f_date, 72, RED)
d.rectangle([M, 102, W - M, 106], fill=RED)
d.rectangle([M, 110, W - M, 111], fill=INK)

# ---- Lead story ----
d.text((M, 122), "TOP STORY  |  SHENZHEN SUMMIT", font=f_lead_tag, fill=RED)
lead_head = "Trump, Xi and Putin sign joint peace declaration at Shenzhen summit"
y = 144
for line in wrap(lead_head, f_lead_head, W - 2 * M, W - 2 * M):
    d.text((M, y), line, font=f_lead_head, fill=INK)
    y += 36
lead_sum = ("First-ever meeting of the leaders of the three largest nuclear powers, on the "
            "APEC sidelines. The four-point declaration backs peace \u2014 but says nothing "
            "about Ukraine or Iran.")
y += 2
for line in wrap(lead_sum, f_lead_sum, W - 2 * M, W - 2 * M):
    d.text((M, y), line, font=f_lead_sum, fill=(50, 50, 50))
    y += 21
d.rectangle([M, 258, W - M, 259], fill=INK)

# ---- Section label ----
d.text((M, 268), "THE DAY IN FULL \u2014 34 MORE STORIES", font=f_section, fill=NAVY)
d.rectangle([M, 290, W - M, 291], fill=(200, 192, 176))

# ---- Dense 2-column grid ----
COL_GAP = 20
COL_W = (W - 2 * M - COL_GAP) // 2  # 478
GRID_TOP = 298
ROW_H = 41
LH = 18  # headline line height
PER_COL = 17
warnings = []

for col in range(2):
    cx = M + col * (COL_W + COL_GAP)
    for row in range(PER_COL):
        idx = col * PER_COL + row
        tag, head = STORIES[idx]
        ry = GRID_TOP + row * ROW_H
        if row % 2 == 0:
            d.rectangle([cx - 4, ry - 2, cx + COL_W + 4, ry + ROW_H - 4], fill=ZEBRA)
        color = COLORS[tag]
        tw = d.textlength(tag, font=f_tag)
        d.text((cx + 4, ry + 4), tag, font=f_tag, fill=color)
        first_w = COL_W - (tw + 16)
        lines = wrap(head, f_head, first_w, COL_W - 8)
        if len(lines) > 2:
            warnings.append(f"{tag}: {head!r} wraps to {len(lines)} lines")
            lines = lines[:2]
            # truncate line 2 with an ellipsis
            while d.textlength(lines[1] + "\u2026", font=f_head) > COL_W - 8:
                lines[1] = lines[1][:-1]
            lines[1] += "\u2026"
        d.text((cx + 4 + tw + 8, ry + 2), lines[0], font=f_head, fill=INK)
        if len(lines) > 1:
            d.text((cx + 4, ry + 2 + LH), lines[1], font=f_head, fill=INK)

grid_bottom = GRID_TOP + PER_COL * ROW_H
assert grid_bottom <= 1000, f"grid overflows: {grid_bottom}"

# ---- Footer ----
center("Compiled from public news reports  |  The World in One Day  |  19 November 2026",
       f_foot, 1002, GRAY)

img.save(OUT, "PNG", optimize=True)
print(f"saved {OUT} {img.size}  stories={1 + len(STORIES)}  grid_bottom={grid_bottom}")
if warnings:
    print("WARNINGS:")
    for w in warnings:
        print(" -", w)
else:
    print("all headlines fit in 2 lines")
