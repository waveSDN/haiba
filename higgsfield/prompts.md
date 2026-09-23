# برومبتات Higgsfield

كل المخرجات مسجّلة في `renders.json` وتنزل بـ `python scripts/fetch_renders.py` إلى `higgsfield/renders/`.
**اعرض التكلفة قبل أي توليد** (`get_cost: true`).

المراجع المرفوعة:
- `brand/box-studio.jpg` مرجع الستايل (رسمة البوكس)
- فريم الجمس من الخلف من `footage/gmc.mov` @15.6 مرجع الجمس
- `brand/s06-still.jpg` أول فريم للقطة s06

## الأسعار (خطة مجانية، سبتمبر ٢٠٢٦)
| الموديل | الإعداد | التكلفة |
|---|---|---|
| cinematic_studio_video_v2 | 4ث، std، بدون صوت | 4 |
| cinematic_studio_video_v2 | 5ث، pro | 7.5 |
| kling3_0 | 5ث، std، بدون صوت | 7.5 |
| seedream_5_0_flash | صورة 1k | 0.5 |
| gpt_image_2_5 | يحتاج خطة Basic | - |

الخطة المجانية تشغّل مهمة وحدة بس في نفس الوقت، فالتوليدات لازم تنرسل ورا بعض.

## لقطات الفيديو

### s06-cinema.mp4: البوكس على مرتبة الجمس (Cinema Studio، 4ث، genre=intimate، speedramp=linear)
```
Slow, smooth cinematic dolly push-in toward the illustrated gift box resting on the red ribbed bench seat
of a vintage GMC truck cabin. Warm golden-hour light slowly sweeps across the seat through the window,
tiny dust particles float and glow in the light beam, the gold rope handles of the gift bags sway very
slightly. Rich, moody, premium commercial look. The box and bag artwork, the round logo and all printed
Arabic text stay perfectly sharp and unchanged. No people, no new text, no warping.
```

### s02: البوكس مكان الجريدة (ما انولّدت هنا، المعتمدة عندك في shots/s02.mp4)
أول فريم: `footage/gmc.mov` @0.3 (الرجل يقرأ الجريدة)، وآخر فريم: `brand/s02-still.jpg`.
```
Vertical 9:16 cinematic shot. A Saudi man in a white thobe and red-and-white shemagh stands on a shaded
palm-lined street in front of a vintage red GMC pickup. He slowly lowers the newspaper he was reading and,
in one smooth motion, raises a flat illustrated gift box in its place, covering his face. Dappled afternoon
sunlight, gentle handheld camera, no text changes on the box.
```

## الرسومات (Seedream 5.0 Flash، 9:16، مرجع الستايل box-studio)
كل البرومبتات تبدأ بـ:
`Vertical illustration in the exact art style of the reference gift box artwork: flat vintage travel-poster painting, bold warm golden and burnt-orange desert dunes, deep red-brown rock shadows, teal-blue sky with big painterly white clouds.`
وتنتهي بـ: `No text, no letters, no logos.`

| الملف | المشهد |
|---|---|
| art-village.png | ancient Najdi mud-brick village with tall towers on a hill above golden dunes at dawn, winding sand road, a tiny rider on horseback |
| art-gmc-road.png | (+ مرجع الجمس) the red 1980s GMC pickup seen from behind driving a winding sand road toward a distant mud-brick village, soft dust trail |
| art-rider-flag.png | lone rider on an Arabian horse silhouetted on a dune crest at sunset, holding a plain green flag, sky orange to deep teal, first stars |
| art-poster.png | (+ مرجع الجمس) the red GMC parked by a mud-brick wall with date palms, tailgate down with gift bags on it, top third empty sky for a headline |

## أفكار للجولة الجاية (لو انشحن الرصيد)
- s02 كامل بـ Kling 3.0 بفريم أول وآخر (7.5).
- تحريك art-village وart-gmc-road بـ Cinema Studio 4ث (4 لكل وحدة) بدل الزوم.
- رسمة قلعة طين بأعلام خضراء، ومجلس نجدي فيه دلة ومسبحة وقلم (0.5 لكل وحدة).
