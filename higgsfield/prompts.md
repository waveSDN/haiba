# «الإرث» | برومبتات Higgsfield (مسودة، ما انولّد شي)

**لا تولّد أي شي قبل ما تعرض التكلفة وتاخذ موافقة صريحة.** كل توليد يتسجّل في `renders.json`.

## الإعدادات المعتمدة
- فيديو: `cinematic_studio_video_v2`، **Pro**، **16:9**، بدون صوت (الصوت والموسيقى نركّبها احنا).
- العمودي ينقص من الأفقي، فخل الموضوع المهم في **نص الكادر** (`vertical-safe`).
- الشخصيات تتثبّت بصور مرجعية (الخطوة ١) تنرفع مع كل لقطة.
- المنتج: `brand/box-studio.jpg` (البوكس مسكّر)، `brand/refs/box-open.jpg` (البوكس مفتوح: بطاقة، قلم، مسبحة)، `brand/refs/misbaha-palm.jpg` و`misbaha-leather.jpg` (المسبحة).

## الأسعار (سبتمبر ٢٠٢٦)
| الشي | التكلفة |
|---|---|
| لقطة Pro 5ث (9:16) | 7.5 |
| لقطة std 4ث / 5ث | 4 / 5 |
| صورة مرجعية seedream_5_0_flash 1k | 0.5 |
| التعليق الصوتي seed_audio (النص كامل) | 1.2 |
| reframe لفيديو 50ث | 459 (لا) |

## الستايل
**الماضي:**
`Cinematic historical epic set in Najd, Arabian Peninsula, early 1900s. Desaturated earthy palette of sand, ochre and faded brown, warm dust haze in the air, soft backlight, anamorphic 16:9 framing, 35mm film grain, shallow depth of field, prestige historical drama look. Main subject centered in frame (vertical-safe).`

**اليوم:**
`Cinematic, warm modern Najdi majlis at golden hour: beige walls with subtle traditional triangular niches, low floor seating with red-and-black Sadu cushions, brass dallah and small finjan cups, warm practical lamp light, rich browns and gold, gentle 35mm film grain, shallow depth of field. Main subject centered in frame (vertical-safe).`

## الخطوة ١: الشخصيات (صور مرجعية)
| الملف | الوصف |
|---|---|
| char-boy.png | Saudi boy about 9 years old, early 1900s Najd, thin face, deep brown determined eyes, sun-darkened skin, simple off-white thobe, plain white ghutra loosely wrapped, dusty. Front-facing portrait, neutral background. |
| char-grandfather.png | The same person 80 years later: dignified Saudi man about 88, deep wrinkles, white trimmed beard, same deep brown eyes, white thobe, dark brown bisht with gold trim, red shemagh and black agal. Front-facing portrait, neutral background. (مرجع: char-boy) |
| char-grandson.png | Saudi young man about 22, short neat beard, warm eyes resembling his grandfather, white thobe, white ghutra and black agal. Front-facing portrait, neutral background. (مرجع: char-grandfather) |
| char-father.png | Saudi man about 40, early 1900s Najd, face wrapped in a red-and-white shemagh (lithaam) showing only intense eyes, brown bisht over off-white thobe, cartridge belt. |
| char-leader.png | Tall commanding Saudi leader of the founding era, full black beard, white ghutra, black agal, dark bisht, stern calm gaze, on a dark Arabian horse. (زي المرجع، حسب اختيارك) |

## الخطوة ٢: اللقطات
| # | مدة | المراجع | البرومبت (بعد بلوك الستايل) |
|---|---|---|---|
| 01 | 4 | char-father | Dawn. A long line of horsemen on a dune crest, silhouetted against the rising sun, green banners fluttering, dust drifting. Slow push-in. |
| 02 | 4 | char-father, char-boy, misbaha-palm | Extreme close-up: a weathered man's hand places a black prayer-bead misbaha with a round silver filigree tassel into a small boy's open palm. Dust particles in the backlight. |
| 03 | 3 | char-boy | Close-up of the boy's face, determined eyes, wind moving his ghutra, dust in the air. Very slow push-in. |
| 04 | 4 | char-leader | The leader on a dark horse in front of a massive mud-brick fort with round towers, raising his hand; horsemen behind him begin to move. Low angle. |
| 05 | 4 | char-father | Sunset. A lone horseman on a dune crest raises his sword to the sky, cloak blowing, dust glowing orange. Epic wide shot. |
| 06 | 3 | char-boy, misbaha-palm | Close-up: the boy's small hand slowly closes into a fist around the black misbaha, silver tassel hanging out. Warm dust light. |
| 07 | 4 | char-grandfather, misbaha-palm | (اليوم) Extreme close-up: an old wrinkled hand slowly opens to reveal the same black misbaha; camera slowly pulls back to reveal the grandfather seated in his majlis. |
| 08 | 4 | char-grandfather, char-grandson | The grandson enters the majlis and bends to kiss his seated grandfather's forehead; the grandfather smiles and holds his hand. |
| 09 | 4 | char-grandfather, char-grandson, box-studio | The grandfather hands his grandson a flat gift box with a painted desert artwork lid and a burgundy base. Keep the box artwork unchanged. |
| 10 | 4 | char-grandson, box-open | Close-up: the grandson lifts the lid; inside, a burgundy tray holds a card, an ornate silver-and-black pen and a black misbaha. Keep product details unchanged. |
| 11 | 4 | char-grandfather | The grandfather lights oud in a brass mabkhara; the rising smoke swirls and briefly forms the silhouettes of galloping horsemen before dissolving. |
| 12 | 3 | char-grandfather, char-grandson, misbaha-palm | Close-up: the grandfather places his old black misbaha into the grandson's open palm; the grandson slowly closes his hand around it (mirrors shot 02). |
| 13 | 5 | – | الختام: `brand/endcard-{16x9,9x16}.png` (مو مولّد) |

## الخطوة ٣: الصوت
`seed_audio`، صوت شايب عربي فخم وهادي (نختاره من `list_voices`)، النص كامل من `storyboard/script.txt`.
