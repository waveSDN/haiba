#!/usr/bin/env python3
"""بوستر اليوم الوطني ٩٦ (1080x1920) من رسمة Higgsfield + شعار هيبة + النص بخط عام الحرف اليدوية.

    python scripts/poster.py                          # higgsfield/renders/art-poster.png -> out/poster.png
    python scripts/poster.py --art brand/s06-still.jpg --out out/poster-test.png
"""
import argparse
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter

from assemble import BG_DARK, CREAM, FONT_AR, FONT_AR_REG, GOLD, ROOT, cover, draw_ar, font

W, H = 1080, 1920


def logo_disc(size):
    """نقص دائرة الشعار من brand/logo-card.png."""
    card = Image.open(ROOT / "brand" / "logo-card.png").convert("RGBA")
    cx, cy, r = 540, 698, 232
    disc = card.crop((cx - r, cy - r, cx + r, cy + r)).resize((size, size), Image.LANCZOS)
    mask = Image.new("L", (size * 4, size * 4), 0)
    ImageDraw.Draw(mask).ellipse([0, 0, size * 4 - 1, size * 4 - 1], fill=255)
    disc.putalpha(mask.resize((size, size), Image.LANCZOS))
    return disc


def sadu_band(draw, y, color, step=46):
    """شريط السدو (معينات) مثل حافة البوكس."""
    draw.line([(0, y - 30), (W, y - 30)], fill=color, width=3)
    draw.line([(0, y + 30), (W, y + 30)], fill=color, width=3)
    for x in range(step // 2, W, step):
        s = 14
        draw.polygon([(x, y - s), (x + s, y), (x, y + s), (x - s, y)], outline=color, width=3)
        draw.rectangle([x - 3, y - 3, x + 3, y + 3], fill=color)


def shadowed_text(img, xy, text, fnt, fill, blur=10):
    shadow = Image.new("RGBA", img.size, (0, 0, 0, 0))
    draw_ar(ImageDraw.Draw(shadow), (xy[0], xy[1] + 4), text, fnt, (20, 8, 6, 200))
    img.alpha_composite(shadow.filter(ImageFilter.GaussianBlur(blur)))
    draw_ar(ImageDraw.Draw(img), xy, text, fnt, fill)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--art", default="higgsfield/renders/art-poster.png")
    ap.add_argument("--out", default="out/poster.png")
    args = ap.parse_args()

    tmp = ROOT / "out" / "_poster-art.png"
    tmp.parent.mkdir(exist_ok=True)
    cover(ROOT / args.art, W, H, tmp)
    img = Image.open(tmp).convert("RGBA")

    # تدرّج بني من تحت عشان النص يبان
    fade = Image.new("L", (1, H))
    for y in range(H):
        fade.putpixel((0, y), int(255 * max(0.0, (y - H * 0.45) / (H * 0.33))) if y < H * 0.78 else 255)
    band = Image.new("RGBA", (W, H), BG_DARK + (255,))
    band.putalpha(fade.resize((W, H)))
    img.alpha_composite(band)

    disc = logo_disc(230)
    img.alpha_composite(disc, ((W - 230) // 2, 150))

    shadowed_text(img, (W / 2, 1300), "هيبة مو بس براند..", font(FONT_AR, 104), CREAM)
    shadowed_text(img, (W / 2, 1440), "هيبة تاريخ!", font(FONT_AR, 132), GOLD)
    d = ImageDraw.Draw(img)
    draw_ar(d, (W / 2, 1600), "كل عام والوطن بهيبته", font(FONT_AR_REG, 58), CREAM)
    draw_ar(d, (W / 2, 1680), "اليوم الوطني ٩٦ | ٢٣ سبتمبر", font(FONT_AR_REG, 46), (200, 180, 160))
    sadu_band(d, 1810, GOLD)

    out = ROOT / args.out
    out.parent.mkdir(parents=True, exist_ok=True)
    img.convert("RGB").save(out, quality=95)
    tmp.unlink()
    print(f"-> {out}")


if __name__ == "__main__":
    main()
