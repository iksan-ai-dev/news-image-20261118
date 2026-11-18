#!/usr/bin/env python3
"""Assemble the front page for news-image-20261118.

Reads the five editorial panels in panels/ and renders every word with PIL
so the text is crisp. Output: entry.png, 1024x1024, at most 1 MiB.
"""
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
PANELS = os.path.join(HERE, "panels")

W, H = 1024, 1024
PAPER = (248, 244, 233)
INK = (25, 25, 25)
RED = (168, 35, 26)
NAVY = (30, 58, 92)
GREY = (110, 105, 95)
CARD = (255, 255, 255)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def crop_fill(im, tw, th):
    """Centre-crop an image to the target aspect, then resize."""
    iw, ih = im.size
    scale = max(tw / iw, th / ih)
    im = im.resize((round(iw * scale), round(ih * scale)), Image.LANCZOS)
    x = (im.width - tw) // 2
    y = (im.height - th) // 2
    return im.crop((x, y, x + tw, y + th))


def wrap(draw, text, fnt, max_w):
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_lines(draw, lines, x, y, fnt, fill, leading):
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def story_card(draw, page, x, y, w, h, panel_file, kicker, headline, body):
    draw.rectangle([x, y, x + w, y + h], fill=CARD, outline=(200, 192, 175))
    img_h = 118
    panel = Image.open(os.path.join(PANELS, panel_file)).convert("RGB")
    page.paste(crop_fill(panel, w, img_h), (x, y))
    tx = x + 14
    ty = y + img_h + 8
    draw.text((tx, ty), kicker, font=font(SANS_B, 14), fill=RED)
    ty += 21
    hl = wrap(draw, headline, font(SANS_B, 21), w - 28)
    ty = draw_lines(draw, hl[:2], tx, ty, font(SANS_B, 21), INK, 25)
    ty += 4
    bl = wrap(draw, body, font(SANS, 16), w - 28)
    # Only draw body lines that fit inside the card.
    room = y + h - 8 - ty
    max_lines = max(0, room // 20)
    draw_lines(draw, bl[:max_lines], tx, ty, font(SANS, 16), (60, 58, 52), 20)


def main():
    page = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(page)

    # ---- Masthead ----
    title = "THE WORLD IN ONE DAY"
    tf = font(SERIF_B, 54)
    tw = draw.textlength(title, font=tf)
    draw.text(((W - tw) / 2, 12), title, font=tf, fill=INK)
    date = "WEDNESDAY  18  NOVEMBER  2026"
    df = font(SANS_B, 26)
    dw = draw.textlength(date, font=df)
    draw.text(((W - dw) / 2, 76), date, font=df, fill=RED)
    draw.line([(12, 108), (1012, 108)], fill=INK, width=3)
    draw.line([(12, 113), (1012, 113)], fill=INK, width=1)

    # ---- Lead story: APEC ----
    lead = Image.open(os.path.join(PANELS, "media-generation-panel-apec-0-ec37ef77-d447-4ff5-bf76-346d89ca4afd.webp")).convert("RGB")
    page.paste(crop_fill(lead, 1000, 178), (12, 122))
    draw.text((12, 306), "APEC OPENS IN SHENZHEN", font=font(SANS_B, 34), fill=INK)
    lead_body = ("Xi Jinping gives the keynote as leaders of 21 economies gather. "
                 "Trump arrives in Shenzhen — and a first-ever Xi\u2013Trump\u2013Putin "
                 "meeting is set for Thursday.")
    bl = wrap(draw, lead_body, font(SANS, 20), 1000)
    draw_lines(draw, bl[:2], 12, 348, font(SANS, 20), (60, 58, 52), 25)
    draw.line([(12, 386), (1012, 386)], fill=(200, 192, 175), width=1)

    # ---- Four story cards, 2 x 2 ----
    story_card(draw, page, 12, 398, 494, 252,
               "media-generation-panel-gulf-0-22dd6d64-d405-4bc5-8801-17cfd550bb5a.webp",
               "THE GULF \u2014 OVERNIGHT",
               "US jets hit missile site after drones target Bahrain radar",
               "Iran claims a fourth tanker hit a mine near Hormuz \u2014 "
               "unverified. Bahrain says the drones were intercepted.")
    story_card(draw, page, 518, 398, 494, 252,
               "media-generation-panel-cyclone-0-85a547a7-23e7-485c-9694-659efb7360d6.webp",
               "WEATHER \u2014 INDIA",
               "Cyclone Akvan strengthens as heavy rain reaches the coast",
               "Now a severe cyclonic storm off India\u2019s east coast. "
               "Landfall expected Friday, winds gusting to 145 km/h.")
    story_card(draw, page, 12, 662, 494, 252,
               "media-generation-panel-ukraine-0-4d55615b-c99a-4f01-b5a9-425f96b9538f.webp",
               "UKRAINE \u2014 THE TOLL",
               "UN: 372 civilians killed in Ukraine in October alone",
               "Deaths in the first ten months of 2026 already exceed all "
               "of 2025. Nearly 18,000 killed since 2022.")
    story_card(draw, page, 518, 662, 494, 252,
               "media-generation-panel-court-0-a6d53f70-71d8-43c7-b89b-85decaf4d82a.webp",
               "NEW YORK \u2014 JUSTICE",
               "27\u00bd years for plot to kill Trump",
               "Asif Merchant jailed over an Iran-linked murder-for-hire "
               "plan targeting Trump, Biden and Haley.")

    # ---- Sport strip ----
    draw.rectangle([12, 926, 1012, 1012], fill=NAVY)
    draw.text((28, 938), "SPORT", font=font(SANS_B, 20), fill=(255, 205, 90))
    sport = ("Northern Ireland reach the Nations League top tier \u2014 "
             "1\u20131 in Hungary; Devenny\u2019s strike seals promotion.")
    sl = wrap(draw, sport, font(SANS_B, 20), 1000 - 140)
    draw_lines(draw, sl[:2], 28, 964, font(SANS_B, 20), (255, 255, 255), 24)

    out = os.path.join(HERE, "entry.png")
    page.save(out, "PNG")
    size = os.path.getsize(out)
    if size > 1048576:
        page.save(out, "JPEG", quality=88, optimize=True)
        size = os.path.getsize(out)
    print("entry.png:", page.size, size, "bytes")


if __name__ == "__main__":
    main()
