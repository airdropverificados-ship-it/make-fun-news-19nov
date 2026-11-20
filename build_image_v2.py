#!/usr/bin/env python3
"""Rebuild the dense v2 front page for the make.fun news bounty
"Sum up 19 November's world news in one image".

Output: entry.png — a 1024x1024 newspaper-style infographic with 35
verified stories from Thursday 19 November 2026: one lead story plus a
34-item grid in two columns. Pure Pillow, fully deterministic, so every
run writes identical bytes.

How the density stays readable:
- The grid carries headlines only (no summaries); each headline holds the
  key fact, so nothing is lost at small size.
- Bold 15px headlines on an 18px line height, at most two lines per item;
  the build reports any headline that would need a third line.
- A colour-coded category tag opens every item, so the eye can scan by
  topic, and alternating rows are shaded to keep them apart.
- Dark ink on warm paper, a wide gutter between columns, no text over
  pictures.
"""
from PIL import Image, ImageDraw, ImageFont

PAGE = (1024, 1024)
EDGE = 24                      # outer margin
GUTTER = 20                    # space between the two grid columns
COLUMN = (PAGE[0] - 2 * EDGE - GUTTER) // 2   # 478
GRID_TOP = 298
ROW = 41                       # grid row height
LINE = 18                      # headline line height
ROWS_PER_COLUMN = 17

PAPER = (246, 241, 231)
BAND = (240, 234, 220)         # zebra shading for alternate rows
INK = (20, 20, 20)
MUTED = (90, 86, 78)
CRIMSON = (185, 28, 28)
DEEP_BLUE = (30, 58, 95)
SUMMARY_INK = (50, 50, 50)
RULE_FAINT = (200, 192, 176)

FONT_DIR = "/usr/share/fonts/truetype/dejavu/"


def load_typefaces():
    """Return the named fonts used across the page."""
    return {
        "masthead": ImageFont.truetype(FONT_DIR + "DejaVuSerif-Bold.ttf", 46),
        "dateline": ImageFont.truetype(FONT_DIR + "DejaVuSans-Bold.ttf", 19),
        "kicker": ImageFont.truetype(FONT_DIR + "DejaVuSans-Bold.ttf", 16),
        "lead_head": ImageFont.truetype(FONT_DIR + "DejaVuSans-Bold.ttf", 30),
        "lead_body": ImageFont.truetype(FONT_DIR + "DejaVuSans.ttf", 16),
        "section": ImageFont.truetype(FONT_DIR + "DejaVuSans-Bold.ttf", 15),
        "tag": ImageFont.truetype(FONT_DIR + "DejaVuSans-Bold.ttf", 13),
        "headline": ImageFont.truetype(FONT_DIR + "DejaVuSans-Bold.ttf", 15),
        "footer": ImageFont.truetype(FONT_DIR + "DejaVuSans.ttf", 13),
    }


# Category tag -> colour.
TAG_COLOURS = {
    "JUSTICE": (109, 40, 217), "CONFLICT": (194, 65, 12),
    "WAR": (153, 27, 27), "TECH": (29, 78, 216),
    "CULTURE": (21, 128, 61), "WEATHER": (15, 118, 110),
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

# The 34 grid stories (the lead story is drawn separately). Order: the
# six v1 cards, the five v1 ticker items, then the 23 new stories.
GRID_STORIES = [
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
    ("UKRAINE", "UK and Norway fund £100m+ for two Ukrainian naval craft"),
    ("DEFENCE", "Denmark's parliament approves Greenland defence deal, 109-0"),
    ("APEC", "APEC adopts Shenzhen Outlook on trade, data and AI risks"),
    ("GAZA", "Aid groups rate Gaza peace-plan implementation 4 out of 26"),
    ("GAZA", "IDF ends Nuseirat camp invasion after one day; 4 killed in Gaza"),
    ("PAKISTAN", "Pakistan military kills 22 militants in Khyber Pakhtunkhwa raids"),
    ("MONGOLIA", "Mongolia's parliament accepts president's resignation over graft claims"),
    ("ASIA", "India lets Japanese forces fire missiles on its ranges"),
    ("CLIMATE", "COP31 draft drops all fossil-fuel language; outcry in Antalya"),
    ("CHILDREN", "Record 589m children now live in conflict zones — Save the Children"),
    ("DIPLOMACY", "Fifteen nations back UK-Australia sanctions on Israeli settlements"),
    ("US POLITICS", "Democrats secure historic 56-seat Senate majority in midterms"),
    ("SCIENCE", "Physicists send a message through a brick wall using gravity"),
    ("CRICKET", "England beat Australia by 97 runs to win ODI series 2-1"),
    ("FOOTBALL", "Chelsea beat PSG 1-0 in Women's Champions League"),
    ("BASKETBALL", "NC State beats Murray State 93-83; McNeil's record 33 points"),
]

LEAD_KICKER = "TOP STORY  |  SHENZHEN SUMMIT"
LEAD_HEADLINE = "Trump, Xi and Putin sign joint peace declaration at Shenzhen summit"
LEAD_BODY = ("First-ever meeting of the leaders of the three largest nuclear powers, on the "
             "APEC sidelines. The four-point declaration backs peace — but says nothing "
             "about Ukraine or Iran.")

DESTINATION = "/home/hatch/workspace/make-fun-bounties/news-19nov-v2/entry.png"


def split_lines(canvas, text, font, opening_width, following_width):
    """Greedy word wrap; the first line may use opening_width, the rest
    following_width."""
    pieces = text.split(" ")
    wrapped, current = [], ""
    limit = opening_width
    for piece in pieces:
        candidate = (current + " " + piece).strip()
        if canvas.textlength(candidate, font=font) <= limit:
            current = candidate
        else:
            if current:
                wrapped.append(current)
            current, limit = piece, following_width
    if current:
        wrapped.append(current)
    return wrapped


def centred(canvas, text, font, y, colour):
    width = canvas.textlength(text, font=font)
    canvas.text(((PAGE[0] - width) / 2, y), text, font=font, fill=colour)


def draw_header(canvas, fonts):
    centred(canvas, "THE WORLD IN ONE DAY", fonts["masthead"], 16, INK)
    centred(canvas, "THURSDAY, 19 NOVEMBER 2026  ·  35 STORIES FROM AROUND THE GLOBE",
            fonts["dateline"], 72, CRIMSON)
    canvas.rectangle([EDGE, 102, PAGE[0] - EDGE, 106], fill=CRIMSON)
    canvas.rectangle([EDGE, 110, PAGE[0] - EDGE, 111], fill=INK)


def draw_lead(canvas, fonts):
    canvas.text((EDGE, 122), LEAD_KICKER, font=fonts["kicker"], fill=CRIMSON)
    pen_y = 144
    for row in split_lines(canvas, LEAD_HEADLINE, fonts["lead_head"],
                           PAGE[0] - 2 * EDGE, PAGE[0] - 2 * EDGE):
        canvas.text((EDGE, pen_y), row, font=fonts["lead_head"], fill=INK)
        pen_y += 36
    pen_y += 2
    for row in split_lines(canvas, LEAD_BODY, fonts["lead_body"],
                           PAGE[0] - 2 * EDGE, PAGE[0] - 2 * EDGE):
        canvas.text((EDGE, pen_y), row, font=fonts["lead_body"], fill=SUMMARY_INK)
        pen_y += 21
    canvas.rectangle([EDGE, 258, PAGE[0] - EDGE, 259], fill=INK)


def draw_section_heading(canvas, fonts):
    canvas.text((EDGE, 268), "THE DAY IN FULL — 34 MORE STORIES",
                font=fonts["section"], fill=DEEP_BLUE)
    canvas.rectangle([EDGE, 290, PAGE[0] - EDGE, 291], fill=RULE_FAINT)


def draw_grid(canvas, fonts):
    """Draw the 34-item grid and return (bottom edge, overflow notes)."""
    notes = []
    for column in range(2):
        origin_x = EDGE + column * (COLUMN + GUTTER)
        for row in range(ROWS_PER_COLUMN):
            position = column * ROWS_PER_COLUMN + row
            label, headline = GRID_STORIES[position]
            top = GRID_TOP + row * ROW
            if row % 2 == 0:
                canvas.rectangle([origin_x - 4, top - 2,
                                  origin_x + COLUMN + 4, top + ROW - 4],
                                 fill=BAND)
            hue = TAG_COLOURS[label]
            label_width = canvas.textlength(label, font=fonts["tag"])
            canvas.text((origin_x + 4, top + 4), label,
                        font=fonts["tag"], fill=hue)
            opening = COLUMN - (label_width + 16)
            rows = split_lines(canvas, headline, fonts["headline"],
                               opening, COLUMN - 8)
            if len(rows) > 2:
                notes.append(f"{label}: {headline!r} wraps to {len(rows)} lines")
                rows = rows[:2]
                while canvas.textlength(rows[1] + "…", font=fonts["headline"]) > COLUMN - 8:
                    rows[1] = rows[1][:-1]
                rows[1] += "…"
            canvas.text((origin_x + 4 + label_width + 8, top + 2), rows[0],
                        font=fonts["headline"], fill=INK)
            if len(rows) > 1:
                canvas.text((origin_x + 4, top + 2 + LINE), rows[1],
                            font=fonts["headline"], fill=INK)
    return GRID_TOP + ROWS_PER_COLUMN * ROW, notes


def draw_footer(canvas, fonts):
    centred(canvas, "Compiled from public news reports  |  The World in One Day  |  19 November 2026",
            fonts["footer"], 1002, MUTED)


def build():
    assert len(GRID_STORIES) == 34, len(GRID_STORIES)
    sheet = Image.new("RGB", PAGE, PAPER)
    canvas = ImageDraw.Draw(sheet)
    fonts = load_typefaces()
    draw_header(canvas, fonts)
    draw_lead(canvas, fonts)
    draw_section_heading(canvas, fonts)
    bottom, notes = draw_grid(canvas, fonts)
    assert bottom <= 1000, f"grid overflows: {bottom}"
    draw_footer(canvas, fonts)
    sheet.save(DESTINATION, "PNG", optimize=True)
    print(f"saved {DESTINATION} {sheet.size}  stories={1 + len(GRID_STORIES)}  grid_bottom={bottom}")
    if notes:
        print("WARNINGS:")
        for note in notes:
            print(" -", note)
    else:
        print("all headlines fit in 2 lines")


if __name__ == "__main__":
    build()
