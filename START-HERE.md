# ابدأ من هنا

## ١. التثبيت (مرة وحدة)
1. ثبّت **Node.js** (نسخة LTS) من nodejs.org. يحتاجه Higgsfield CLI.
2. ثبّت **Claude Code**: افتح PowerShell والصق:
   ```
   irm https://claude.ai/install.ps1 | iex
   ```
   أو استخدم تبويب **Code** في تطبيق Claude على الكمبيوتر.
3. اختياري ومفيد: **Git for Windows** من git-scm.com.
4. **الاشتراكات**:
   - Claude Pro أو Max، لأن الخطة المجانية ما تشمل Claude Code.
   - Higgsfield مدفوع عشان الموديلات الأقوى.

## ٢. تجهيز المشروع
1. نزّل المشروع في `Documents\haybah-nd96`:
   ```
   git clone https://github.com/waveSDN/haiba "$HOME\Documents\haybah-nd96"
   ```
2. انسخ مقطعيك للمجلد `footage` بهالأسماء:
   - «مقطع اليوم الوطني.MOV» ← `footage\gmc.mov`
   - «مقطع.MOV» ← `footage\box.mov`
3. حط لقطات Higgsfield المعتمدة في `shots`: `s02.mp4` و`s06.mp4`

## ٣. التشغيل
في PowerShell:
```
cd "$HOME\Documents\haybah-nd96"
claude
```
أول مرة يفتح لك المتصفح عشان تسجّل دخولك.

## ٤. أول رسالة لـ Claude Code (انسخها كما هي)
```
اقرأ CLAUDE.md. تأكد إن ffmpeg وPython موجودين وثبّتهم لو ناقصين، وشغّل pip install -r requirements.txt. ثبّت Higgsfield: npm i -g @higgsfield/cli ثم higgsfield auth login ثم npx skills add higgsfield-ai/skills. بعدها شغّل python scripts/assemble.py --preview وورني النسخة الأولية. لو احتجنا نعيد توليد s02 أو s06، اعرض علي التكلفة قبل ما تصرف أي كريدت.
```

## ٥. بعدها
- التعليق الصوتي: سجّله وحطه في `audio\vo.wav`
- الموسيقى: `audio\music.mp3`
- أي تعديل: قل لـ Claude Code وش تبي بالعربي، مثل «طوّل لقطة الجمس في المشهد ٣» أو «جرّب برومبت ثاني للمشهد ٢».
