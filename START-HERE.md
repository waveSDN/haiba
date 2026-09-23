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
2. حط لقطات Higgsfield المعتمدة في `shots` بأسماء `01.mp4` … `12.mp4` (بعد ما نولّدها).

## ٣. التشغيل
في PowerShell:
```
cd "$HOME\Documents\haybah-nd96"
claude
```
أول مرة يفتح لك المتصفح عشان تسجّل دخولك.

## ٤. أول رسالة لـ Claude Code (انسخها كما هي)
```
اقرأ CLAUDE.md. تأكد إن ffmpeg وPython موجودين وثبّتهم لو ناقصين، وشغّل pip install -r requirements.txt. بعدها شغّل python scripts/assemble.py --preview وورني النسخة الأولية. لا تولّد أي شي في Higgsfield قبل ما تعرض علي التكلفة وتسألني.
```

## ٥. بعدها
- التعليق الصوتي (صوت الجد): يتولّد بـ Higgsfield ويروح `audio\vo.wav`
- الموسيقى: `audio\music.mp3`
- أي تعديل: قل لـ Claude Code وش تبي بالعربي، مثل «طوّل لقطة الخيّالة» أو «جرّب برومبت ثاني للمشهد ٩».
