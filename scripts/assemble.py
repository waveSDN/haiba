#!/usr/bin/env python3
"""يركّب إعلان هيبة (اليوم الوطني ٩٦) من storyboard/timeline.json.

    python scripts/assemble.py --preview   # نسخة أولية سريعة 540x960 -> out/preview.mp4
    python scripts/assemble.py             # النسخة النهائية 1080x1920 -> out/haybah-nd96.mp4
    python scripts/assemble.py --only 3    # مشهد واحد بس -> out/scene-3.mp4

أي مقطع ناقص يتعوّض بصورة (still) أو بكرت بديل مكتوب عليه اسم الملف الناقص،
عشان تقدر تشوف الإيقاع قبل ما تكتمل المواد. التعليق الصوتي والموسيقى من audio/
يندمجون تلقائي لو موجودين.
"""
import argparse
import json
import math
import re
import shutil
import subprocess
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, features

ROOT = Path(__file__).resolve().parent.parent
TIMELINE = ROOT / "storyboard" / "timeline.json"
OUT = ROOT / "out"
FONT_AR = ROOT / "fonts" / "TheYearofHandicrafts-Bold.otf"
FONT_AR_REG = ROOT / "fonts" / "TheYearofHandicrafts-Regular.otf"
VIDEO_EXT = {".mov", ".mp4", ".m4v", ".mkv", ".webm"}
AR_DIGITS = str.maketrans("0123456789", "٠١٢٣٤٥٦٧٨٩")

# ألوان الهوية: بني غامق وذهبي البرتقالي حق الشعار
BG_DARK = (36, 19, 18)
BG_GLOW = (104, 62, 42)
GOLD = (248, 176, 64)
CREAM = (240, 226, 206)


def find_ffmpeg():
    exe = shutil.which("ffmpeg")
    if exe:
        return exe
    try:
        import imageio_ffmpeg

        return imageio_ffmpeg.get_ffmpeg_exe()
    except ImportError:
        sys.exit("ffmpeg مو موجود. ثبّته (winget install Gyan.FFmpeg) أو: pip install imageio-ffmpeg")


FFMPEG = find_ffmpeg()


def run(args, quiet=True):
    cmd = [FFMPEG, "-hide_banner", "-y", "-loglevel", "error" if quiet else "info", *map(str, args)]
    res = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    if res.returncode != 0:
        sys.exit(f"ffmpeg فشل:\n{' '.join(cmd)}\n{res.stderr[-3000:]}")
    return res


def has_filter(name, _cache={}):
    if not _cache:
        res = subprocess.run([FFMPEG, "-hide_banner", "-filters"], capture_output=True, text=True)
        _cache["list"] = {line.split()[1] for line in res.stdout.splitlines() if len(line.split()) > 2}
    return name in _cache["list"]


def probe(path):
    """مدة المقطع وهل هو HDR، من غير ما نحتاج ffprobe."""
    res = subprocess.run([FFMPEG, "-hide_banner", "-i", str(path)], capture_output=True, text=True,
                         encoding="utf-8", errors="replace")
    m = re.search(r"Duration: (\d+):(\d+):([\d.]+)", res.stderr)
    dur = int(m[1]) * 3600 + int(m[2]) * 60 + float(m[3]) if m else None
    video_line = next((l for l in res.stderr.splitlines() if "Video:" in l), "")
    hdr = any(t in video_line for t in ("arib-std-b67", "smpte2084"))
    return dur, hdr


# ---------- نصوص عربية ----------

def font(path, size):
    try:
        return ImageFont.truetype(str(path), size)
    except OSError:
        return ImageFont.load_default(size)


def latin_font(size):
    for name in ("arial.ttf", "DejaVuSans.ttf", "Helvetica.ttc"):
        try:
            return ImageFont.truetype(name, size)
        except OSError:
            continue
    return ImageFont.load_default(size)


def draw_ar(draw, xy, text, fnt, fill):
    """يكتب نص عربي متوسّط على xy. يستخدم raqm لو متوفر، وإلا arabic_reshaper + bidi."""
    if features.check("raqm"):
        draw.text(xy, text, font=fnt, fill=fill, anchor="mm", direction="rtl")
        return
    try:
        import arabic_reshaper
        from bidi.algorithm import get_display

        text = get_display(arabic_reshaper.reshape(text))
    except ImportError:
        pass
    draw.text(xy, text, font=fnt, fill=fill, anchor="mm", layout_engine=ImageFont.Layout.BASIC)


def glow_background(w, h):
    img = Image.new("RGB", (w, h), BG_DARK)
    px = img.load()
    cx, cy, r = w / 2, h * 0.4, max(w, h) * 0.6
    for y in range(h):
        for x in range(w):
            t = max(0.0, 1 - math.hypot(x - cx, y - cy) / r) ** 1.6
            px[x, y] = tuple(int(BG_DARK[i] + (BG_GLOW[i] - BG_DARK[i]) * t) for i in range(3))
    return img


def placeholder_card(scene, missing, w, h, dest):
    s = w / 1080
    img = glow_background(w // 4, h // 4).resize((w, h), Image.BICUBIC)
    d = ImageDraw.Draw(img)
    d.ellipse([w / 2 - 170 * s, h * 0.3 - 170 * s, w / 2 + 170 * s, h * 0.3 + 170 * s], outline=GOLD, width=max(2, int(6 * s)))
    draw_ar(d, (w / 2, h * 0.3), str(scene["id"]).translate(AR_DIGITS), font(FONT_AR, int(200 * s)), GOLD)
    draw_ar(d, (w / 2, h * 0.47), scene["title"], font(FONT_AR, int(80 * s)), CREAM)
    y = h * 0.55
    for line in wrap_ar(scene.get("desc", ""), 26):
        draw_ar(d, (w / 2, y), line, font(FONT_AR_REG, int(46 * s)), CREAM)
        y += 70 * s
    draw_ar(d, (w / 2, h * 0.78), "المقطع الناقص", font(FONT_AR_REG, int(44 * s)), GOLD)
    d.text((w / 2, h * 0.82), missing, font=latin_font(int(44 * s)), fill=CREAM, anchor="mm")
    img.save(dest)


def wrap_ar(text, width):
    lines, cur = [], ""
    for word in text.split():
        if cur and len(cur) + 1 + len(word) > width:
            lines.append(cur)
            cur = word
        else:
            cur = f"{cur} {word}".strip()
    return lines + [cur] if cur else lines


# ---------- المشاهد ----------

def cover(src, w, h, dest):
    img = Image.open(src).convert("RGB")
    k = max(w / img.width, h / img.height)
    img = img.resize((math.ceil(img.width * k), math.ceil(img.height * k)), Image.LANCZOS)
    left, top = (img.width - w) // 2, (img.height - h) // 2
    img.crop((left, top, left + w, top + h)).save(dest)


def encode_args(cfg):
    return ["-c:v", "libx264", "-preset", cfg["preset"], "-crf", cfg["crf"], "-pix_fmt", "yuv420p",
            "-r", cfg["fps"], "-an"]


def render_still(image, scene, cfg, dest, work, zoom=0.06):
    """صورة ثابتة مع زوم بطيء عشان ما تكون ميتة."""
    w, h, fps = cfg["w"], cfg["h"], cfg["fps"]
    frames = round(scene["dur"] * fps)
    big = work / f"scene-{scene['id']}-still.png"
    cover(image, w * 2, h * 2, big)
    zp = (f"zoompan=z='1+{zoom}*on/{frames}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)'"
          f":d={frames}:s={w}x{h}:fps={fps},setsar=1")
    run(["-i", big, "-vf", zp, "-frames:v", frames, *encode_args(cfg), dest])


def render_video(src, scene, cfg, dest, warnings):
    w, h, fps, dur = cfg["w"], cfg["h"], cfg["fps"], scene["dur"]
    length, hdr = probe(src)
    start = scene.get("in", 0.0)
    if length is not None and start + dur > length + 0.01:
        warnings.append(f"المشهد {scene['id']}: {src.name} طوله {length:.1f}ث بس، وطلبنا {start}+{dur}. آخر فريم بيتثبّت.")
    chain = []
    if hdr:
        if has_filter("zscale"):
            chain.append("zscale=t=linear:npl=100,format=gbrpf32le,zscale=p=bt709,"
                         "tonemap=hable:desat=0,zscale=t=bt709:m=bt709:r=tv,format=yuv420p")
        else:
            warnings.append(f"المشهد {scene['id']}: {src.name} مصوّر HDR والـffmpeg ما فيه zscale، الألوان بتطلع باهتة. "
                            "ثبّت ffmpeg كامل (winget install Gyan.FFmpeg) أو صوّر SDR.")
    chain += [f"scale={w}:{h}:force_original_aspect_ratio=increase:flags=lanczos", f"crop={w}:{h}", "setsar=1",
              f"fps={fps}", f"tpad=stop_mode=clone:stop_duration={dur}"]
    run(["-ss", start, "-i", src, "-vf", ",".join(chain), "-t", dur, *encode_args(cfg), dest])


def render_scene(scene, cfg, work, warnings):
    dest = work / f"scene-{scene['id']}.mp4"
    src = next((ROOT / s for s in scene["sources"] if (ROOT / s).exists()), None)
    if src and src.suffix.lower() in VIDEO_EXT:
        render_video(src, scene, cfg, dest, warnings)
        used = src.relative_to(ROOT).as_posix()
    elif src:
        render_still(src, scene, cfg, dest, work, zoom=0.04)
        used = src.relative_to(ROOT).as_posix()
    elif scene.get("still") and (ROOT / scene["still"]).exists():
        render_still(ROOT / scene["still"], scene, cfg, dest, work)
        used = f"{scene['still']}  (صورة مؤقتة بدل {scene['sources'][0]})"
    else:
        card = work / f"scene-{scene['id']}-card.png"
        placeholder_card(scene, scene["sources"][0], cfg["w"], cfg["h"], card)
        render_still(card, scene, cfg, dest, work, zoom=0.02)
        used = f"كرت بديل  (ناقص {scene['sources'][0]})"
    return dest, used


# ---------- الصوت ----------

def find_audio(stem):
    return next((p for p in sorted((ROOT / "audio").glob(f"{stem}.*")) if p.suffix.lower() != ".txt"), None)


def mix_audio(video, total, dest, offset=0.0):
    vo, music = find_audio("vo"), find_audio("music")
    seek = ["-ss", offset] if offset else []
    fade = max(0.0, total - 1.5)
    inputs, graph = ["-i", video], []
    pad = f"aformat=sample_rates=48000:channel_layouts=stereo,atrim=0:{total},apad=whole_dur={total}"
    if vo and music:
        inputs += [*seek, "-i", vo, *seek, "-i", music]
        graph = [f"[1:a]{pad},asplit=2[vo][key]",
                 f"[2:a]{pad},volume=0.8[m]",
                 "[m][key]sidechaincompress=threshold=0.03:ratio=8:attack=20:release=400[md]",
                 f"[vo][md]amix=inputs=2:duration=first:normalize=0,afade=t=out:st={fade}:d=1.5,"
                 "loudnorm=I=-14:TP=-1.5:LRA=11[a]"]
    elif vo or music:
        inputs += [*seek, "-i", vo or music]
        graph = [f"[1:a]{pad},afade=t=out:st={fade}:d=1.5,loudnorm=I=-14:TP=-1.5:LRA=11[a]"]
    else:
        inputs += ["-f", "lavfi", "-i", "anullsrc=r=48000:cl=stereo"]
        graph = ["[1:a]anull[a]"]
    run([*inputs, "-filter_complex", ";".join(graph), "-map", "0:v", "-map", "[a]", "-c:v", "copy",
         "-c:a", "aac", "-b:a", "192k", "-ar", 48000, "-t", total, "-movflags", "+faststart", dest])
    return vo, music


# ---------- لوحة المشاهد ----------

def contact_sheet(clips, cfg, dest):
    thumbs = []
    for clip, scene in clips:
        frame = clip.with_suffix(".jpg")
        run(["-ss", scene["dur"] / 2, "-i", clip, "-frames:v", 1, "-q:v", 3, frame])
        thumbs.append(Image.open(frame).resize((270, 480)))
    sheet = Image.new("RGB", (len(thumbs) * 280 + 10, 490), BG_DARK)
    for i, t in enumerate(reversed(thumbs)):  # من اليمين لليسار
        sheet.paste(t, (10 + i * 280, 5))
    sheet.save(dest, quality=88)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--preview", action="store_true", help="نسخة أولية سريعة بنص الدقة")
    ap.add_argument("--only", type=int, help="ركّب مشهد واحد بس")
    ap.add_argument("--out", help="مسار ملف الإخراج")
    args = ap.parse_args()

    tl = json.loads(TIMELINE.read_text(encoding="utf-8"))
    scale = 0.5 if args.preview else 1.0
    cfg = {"w": int(tl["width"] * scale) // 2 * 2, "h": int(tl["height"] * scale) // 2 * 2, "fps": tl["fps"],
           "crf": "28" if args.preview else "18", "preset": "veryfast" if args.preview else "slow"}
    scenes = [s for s in tl["scenes"] if args.only in (None, s["id"])]
    if not scenes:
        sys.exit(f"ما فيه مشهد رقمه {args.only}")

    work = OUT / "_work" / ("preview" if args.preview else "final")
    shutil.rmtree(work, ignore_errors=True)
    work.mkdir(parents=True)

    warnings, clips, t = [], [], 0.0
    print(f"{cfg['w']}x{cfg['h']} @ {cfg['fps']}fps\n")
    for scene in scenes:
        clip, used = render_scene(scene, cfg, work, warnings)
        clips.append((clip, scene))
        print(f"  {t:5.1f} - {t + scene['dur']:5.1f}  [{scene['id']}] {scene['title']}: {used}")
        t += scene["dur"]

    listing = work / "concat.txt"
    listing.write_text("".join(f"file '{c.as_posix()}'\n" for c, _ in clips), encoding="utf-8")
    silent = work / "video.mp4"
    run(["-f", "concat", "-safe", 0, "-i", listing, "-c", "copy", silent])

    name = f"scene-{args.only}.mp4" if args.only else ("preview.mp4" if args.preview else "haybah-nd96.mp4")
    dest = Path(args.out) if args.out else OUT / name
    dest.parent.mkdir(parents=True, exist_ok=True)
    offset = sum(s["dur"] for s in tl["scenes"][: tl["scenes"].index(scenes[0])]) if args.only else 0.0
    vo, music = mix_audio(silent, t, dest, offset)
    if not args.only:
        contact_sheet(clips, cfg, OUT / "contact-sheet.jpg")

    print(f"\n  المدة: {t:.1f}ث" + ("" if abs(t - 30) < 0.05 or args.only else "  (تنبيه: مو ٣٠ ثانية)"))
    print(f"  التعليق: {vo.name if vo else 'ما فيه (audio/vo.wav)'}   الموسيقى: {music.name if music else 'ما فيه (audio/music.mp3)'}")
    for w in warnings:
        print(f"  ! {w}")
    print(f"\n  -> {dest}")


if __name__ == "__main__":
    main()
