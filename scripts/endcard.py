#!/usr/bin/env python3
"""كرت الختام (المشهد ١٣) بالمقاسين: brand/endcard-16x9.png و brand/endcard-9x16.png.

    python scripts/endcard.py
"""
from PIL import Image, ImageDraw

from assemble import BG_DARK, CREAM, FONT_AR, FONT_AR_REG, GOLD, ROOT, draw_ar, font, glow_background
from poster import logo_disc, sadu_band, shadowed_text

LINES = {
    "brand": "هيبة مو بس براند..",
    "history": "هيبة تاريخ!",
    "wish": "كل عام والوطن بهيبته",
    "day": "اليوم الوطني ٩٦ | ٢٣ سبتمبر",
}


def render(w, h, dest):
    s = min(w, h) / 1080
    img = glow_background(w // 4, h // 4).resize((w, h), Image.BICUBIC).convert("RGBA")
    vertical = h > w
    disc = int(300 * s)
    top = h * (0.26 if vertical else 0.1)
    img.alpha_composite(logo_disc(disc), ((w - disc) // 2, int(top)))
    y = top + disc + 150 * s
    shadowed_text(img, (w / 2, y), LINES["brand"], font(FONT_AR, int(96 * s)), CREAM)
    shadowed_text(img, (w / 2, y + 130 * s), LINES["history"], font(FONT_AR, int(124 * s)), GOLD)
    d = ImageDraw.Draw(img)
    draw_ar(d, (w / 2, y + 280 * s), LINES["wish"], font(FONT_AR_REG, int(56 * s)), CREAM)
    draw_ar(d, (w / 2, y + 360 * s), LINES["day"], font(FONT_AR_REG, int(44 * s)), (200, 180, 160))
    sadu_band(d, h - 90 * s, GOLD, width=w)
    img.convert("RGB").save(dest)
    print(f"-> {dest.relative_to(ROOT)}")


if __name__ == "__main__":
    render(1920, 1080, ROOT / "brand" / "endcard-16x9.png")
    render(1080, 1920, ROOT / "brand" / "endcard-9x16.png")
