#!/usr/bin/env python3
"""يركّب إعلان هيبة (اليوم الوطني ٩٦) من storyboard/timeline.json.

    python scripts/assemble.py --preview              # نسخة أولية سريعة بنص الدقة -> out/preview-16x9.mp4
    python scripts/assemble.py                        # النسخة النهائية الأفقية -> out/haybah-nd96-16x9.mp4
    python scripts/assemble.py --vertical             # النسخة العمودية المقصوصة -> out/haybah-nd96-9x16.mp4
    python scripts/assemble.py --only 3 --vertical    # مشهد واحد بس -> out/scene-3-9x16.mp4

العمودي ينقص من الأفقي: كل لقطة تقدر تحدد وين ينقص بـ vx (٠ يسار، ٠٫٥ نص، ١ يمين).
أي مصدر فيه {orient} يتبدّل بـ 16x9 أو 9x16، مثل brand/endcard-{orient}.png.

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
    s = min(w, h) / 1080
    img = glow_background(w // 4, h // 4).resize((w, h), Image.BICUBIC)
    d = ImageDraw.Draw(img)
    cy = h / 2 - 300 * s
    d.ellipse([w / 2 - 120 * s, cy - 120 * s, w / 2 + 120 * s, cy + 120 * s], outline=GOLD, width=max(2, int(5 * s)))
    number = str(scene["id"]).split(".")[0].translate(AR_DIGITS)
    draw_ar(d, (w / 2, cy), number, font(FONT_AR, int(140 * s)), GOLD)
    draw_ar(d, (w / 2, cy + 200 * s), scene["title"], font(FONT_AR, int(72 * s)), CREAM)
    y = cy + 290 * s
    for line in wrap_ar(scene.get("desc", ""), 26 if h > w else 48)[:3]:
        draw_ar(d, (w / 2, y), line, font(FONT_AR_REG, int(42 * s)), CREAM)
        y += 60 * s
    draw_ar(d, (w / 2, cy + 510 * s), "المقطع الناقص", font(FONT_AR_REG, int(38 * s)), GOLD)
    d.text((w / 2, cy + 565 * s), missing, font=latin_font(int(38 * s)), fill=CREAM, anchor="mm")
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

def cover(src, w, h, dest, vx=0.5):
    img = Image.open(src).convert("RGB")
    k = max(w / img.width, h / img.height)
    img = img.resize((math.ceil(img.width * k), math.ceil(img.height * k)), Image.LANCZOS)
    left, top = round((img.width - w) * vx), (img.height - h) // 2
    img.crop((left, top, left + w, top + h)).save(dest)


def encode_args(cfg):
    return ["-c:v", "libx264", "-preset", cfg["preset"], "-crf", cfg["crf"], "-pix_fmt", "yuv420p",
            "-r", cfg["fps"], "-an"]


def render_still(image, scene, cfg, dest, work, zoom=0.06):
    """صورة ثابتة مع زوم بطيء عشان ما تكون ميتة."""
    w, h, fps = cfg["w"], cfg["h"], cfg["fps"]
    frames = round(scene["dur"] * fps)
    big = work / f"scene-{scene['id']}-still.png"
    cover(image, w * 2, h * 2, big, scene.get("vx", 0.5))
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
    chain += [f"scale={w}:{h}:force_original_aspect_ratio=increase:flags=lanczos", f"crop={w}:{h}:(iw-{w})*{scene.get('vx', 0.5)}:(ih-{h})/2", "setsar=1",
              f"fps={fps}", f"tpad=stop_mode=clone:stop_duration={dur}"]
    run(["-ss", start, "-i", src, "-vf", ",".join(chain), "-t", dur, *encode_args(cfg), dest])


def scene_shots(scene):
    """المشهد إما مصدر واحد (sources) أو عدة لقطات قصيرة (shots). نرجّعها كلها كلقطات."""
    base = {"title": scene["title"], "desc": scene.get("desc", "")}
    if "shots" not in scene:
        return [{**base, "id": str(scene["id"]), "sources": scene["sources"], "in": scene.get("in", 0.0),
                 "dur": scene["dur"], "still": scene.get("still"), "vx": scene.get("vx", 0.5)}]
    shots = []
    for k, shot in enumerate(scene["shots"], 1):
        src = shot["src"]
        shots.append({**base, "id": f"{scene['id']}.{k}", "sources": [src] if isinstance(src, str) else src,
                      "in": shot.get("in", 0.0), "dur": shot["dur"], "still": shot.get("still"),
                      "vx": shot.get("vx", scene.get("vx", 0.5))})
    return shots


def scene_dur(scene):
    return round(sum(s["dur"] for s in scene_shots(scene)), 3)


def render_shot(shot, cfg, work, warnings):
    dest = work / f"shot-{shot['id']}.mp4"
    shot = {**shot, "sources": [s.format(orient=cfg["orient"]) for s in shot["sources"]]}
    src = next((ROOT / s for s in shot["sources"] if (ROOT / s).exists()), None)
    if src and src.suffix.lower() in VIDEO_EXT:
        render_video(src, shot, cfg, dest, warnings)
        used = src.relative_to(ROOT).as_posix() + f" @{shot['in']}"
    elif src:
        render_still(src, shot, cfg, dest, work, zoom=0.05)
        used = src.relative_to(ROOT).as_posix()
    elif shot.get("still") and (ROOT / shot["still"]).exists():
        render_still(ROOT / shot["still"], shot, cfg, dest, work)
        used = f"{shot['still']}  (صورة مؤقتة بدل {shot['sources'][0]})"
    else:
        card = work / f"shot-{shot['id']}-card.png"
        placeholder_card(shot, shot["sources"][0], cfg["w"], cfg["h"], card)
        render_still(card, shot, cfg, dest, work, zoom=0.02)
        used = f"كرت بديل  (ناقص {shot['sources'][0]})"
    return dest, used


def concat(clips, dest, work):
    listing = work / f"{dest.stem}.txt"
    listing.write_text("".join(f"file '{c.as_posix()}'\n" for c in clips), encoding="utf-8")
    run(["-f", "concat", "-safe", 0, "-i", listing, "-c", "copy", dest])


def render_scene(scene, cfg, work, warnings):
    """يرجّع ملف المشهد وقائمة (مدة اللقطة، وش استخدمنا فيها)."""
    rendered = [(render_shot(shot, cfg, work, warnings), shot["dur"]) for shot in scene_shots(scene)]
    dest = work / f"scene-{scene['id']}.mp4"
    concat([clip for (clip, _), _ in rendered], dest, work)
    return dest, [(dur, used) for (_, used), dur in rendered]


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
    tw, th = (270, 480) if cfg["h"] > cfg["w"] else (320, 180)
    thumbs = []
    for clip, scene in clips:
        frame = clip.with_suffix(".jpg")
        run(["-ss", scene_dur(scene) / 2, "-i", clip, "-frames:v", 1, "-q:v", 3, frame])
        thumbs.append(Image.open(frame).resize((tw, th)))
    cols = min(len(thumbs), 7)
    rows = math.ceil(len(thumbs) / cols)
    sheet = Image.new("RGB", (cols * (tw + 10) + 10, rows * (th + 10) + 10), BG_DARK)
    for i, t in enumerate(thumbs):  # من اليمين لليسار
        r, c = divmod(i, cols)
        sheet.paste(t, (10 + (cols - 1 - c) * (tw + 10), 10 + r * (th + 10)))
    sheet.save(dest, quality=88)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--preview", action="store_true", help="نسخة أولية سريعة بنص الدقة")
    ap.add_argument("--only", type=int, help="ركّب مشهد واحد بس")
    ap.add_argument("--vertical", action="store_true", help="النسخة العمودية 9:16 مقصوصة من الأفقي")
    ap.add_argument("--out", help="مسار ملف الإخراج")
    args = ap.parse_args()

    tl = json.loads(TIMELINE.read_text(encoding="utf-8"))
    scale = 0.5 if args.preview else 1.0
    width, height = (tl["height"], tl["width"]) if args.vertical else (tl["width"], tl["height"])
    orient = "9x16" if args.vertical else "16x9"
    cfg = {"w": int(width * scale) // 2 * 2, "h": int(height * scale) // 2 * 2, "fps": tl["fps"], "orient": orient,
           "crf": "28" if args.preview else "18", "preset": "veryfast" if args.preview else "slow"}
    scenes = [s for s in tl["scenes"] if args.only in (None, s["id"])]
    if not scenes:
        sys.exit(f"ما فيه مشهد رقمه {args.only}")

    work = OUT / "_work" / f"{'preview' if args.preview else 'final'}-{orient}"
    shutil.rmtree(work, ignore_errors=True)
    work.mkdir(parents=True)

    warnings, clips, t = [], [], 0.0
    print(f"{cfg['w']}x{cfg['h']} @ {cfg['fps']}fps\n")
    for scene in scenes:
        clip, shots = render_scene(scene, cfg, work, warnings)
        clips.append((clip, scene))
        print(f"  {t:5.2f} - {t + scene_dur(scene):5.2f}  [{scene['id']}] {scene['title']}")
        for dur, used in shots:
            print(f"               {dur:4.2f}ث  {used}")
        t += scene_dur(scene)

    silent = work / "video.mp4"
    concat([c for c, _ in clips], silent, work)

    name = (f"scene-{args.only}" if args.only else "preview" if args.preview else "haybah-nd96") + f"-{orient}.mp4"
    dest = Path(args.out) if args.out else OUT / name
    dest.parent.mkdir(parents=True, exist_ok=True)
    offset = sum(scene_dur(s) for s in tl["scenes"][: tl["scenes"].index(scenes[0])]) if args.only else 0.0
    vo, music = mix_audio(silent, t, dest, offset)
    if not args.only:
        contact_sheet(clips, cfg, OUT / f"contact-sheet-{orient}.jpg")

    print(f"\n  المدة: {t:.1f}ث" + ("" if abs(t - tl["duration"]) < 0.05 or args.only else f"  (تنبيه: المفروض {tl['duration']}ث)"))
    print(f"  التعليق: {vo.name if vo else 'ما فيه (audio/vo.wav)'}   الموسيقى: {music.name if music else 'ما فيه (audio/music.mp3)'}")
    for w in warnings:
        print(f"  ! {w}")
    print(f"\n  -> {dest}")


if __name__ == "__main__":
    main()
