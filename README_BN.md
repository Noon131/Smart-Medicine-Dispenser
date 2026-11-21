# Smart Medicine Dispenser — V75 UI + Raspberry Pi 4 backend

এই ZIP-এ V59 interface-কে আগের working Flask/GPIO backend-এর সঙ্গে যুক্ত করা হয়েছে। Raspberry Pi 4 Model B এবং 7-inch HDMI touchscreen-এর জন্য responsive layout রাখা হয়েছে।

## ভয়েস
সব box voice তোমার দেওয়া MP3 ফাইল (`static/audio/`) থেকে বাজে; আলাদা করে ভয়েস তৈরি বা ইন্টারনেট লাগে না।

## V74 পরিবর্তন
- **শিডিউল সেট:** কোনো বক্সের ওষুধের স্টক ০ হলে ওই বক্সের শিডিউল বদলানো যায় না; চেষ্টা করলে "Please refill the stock" পপআপ আসে। Refill করার পর শিডিউল সেট করা যায়।

- **ইউজার পরিবর্তন:** Others-এর যেকোনো স্ক্রিনে (Medicine Entry, Schedule, Refill, History, User Registration) থাকা অবস্থায় ইউজার বদলালে ওই স্ক্রিন সঙ্গে সঙ্গে নতুন ইউজারের ডেটা দিয়ে নতুন করে আঁকা হয়।
- **"ওষুধ বাকি" অ্যালার্ট সাউন্ড:** অন্য ইউজারের ওষুধ বাকি থাকলে যে আইকন দেখা যায়, আইকন আসার সময় (বা নতুন ইউজারের ওষুধ বাকি হলে) ৩-নোটের চাইম বাজে ও ইউজারের নাম টোস্টে দেখায়। আইকন চাপ না দেওয়া পর্যন্ত প্রতি ৩০ সেকেন্ডে আবার বাজে। ভলিউম সেটিং মানে; ৭-ইঞ্চি স্ক্রিনের আইকন আগের রেসপন্সিভ সাইজেই আছে।
- **Refill:** রিফিলের সংখ্যা সরাসরি স্টকে যোগ হয়। (০ বা ফাঁকা দিলে আর ১০ ধরা হয় না — সংখ্যা চাইবে।) আগে কোনো বক্সের প্রথম স্লট ফাঁকা থাকলে ভুল স্লটে রিফিল হতো, সেটিও ঠিক করা হয়েছে।
- **Medicine Entry:** স্টক ঘরটি এখন শুধু দেখার জন্য (এডিট করা যায় না)। স্টক কেবল Refill থেকে বাড়ে। "প্রতি ডোজে ট্যাবলেট" ঘরে শুধু সংখ্যা/দশমিক (০.৫, ১, ১.৫ ...) নেওয়া হয়; অক্ষর বা ভুল মান দিলে আগের মান থেকে যায়।
- **স্বয়ংক্রিয় বাংলা নাম:** ইংরেজিতে ওষুধের নাম লিখলে সিস্টেম নিজেই বাংলা নাম বসিয়ে দেয় (`Napa` → `Napa (নাপা)`), এবং বাংলা ভাষা নির্বাচন করলে বাংলা নামই দেখায়। প্রচলিত ~৭০টি নাম ডিকশনারিতে আছে, বাকিগুলো ধ্বনিভিত্তিক নিয়মে তৈরি হয়। উচ্চারণ ঠিক না হলে ঘরে `Name (বাংলা নাম)` লিখে নিজে ঠিক করা যায়।

## V71 পরিবর্তন
- বিল্ট-ইন অন-স্ক্রিন কিবোর্ড: ইনসুলিন ডোজ, মেডিসিন এন্ট্রি, শিডিউল, রিফিল ও ইউজার রেজিস্ট্রেশনের যেকোনো ঘরে ট্যাপ করলে নিচে কিবোর্ড আসে।
  - সংখ্যার ঘর: এক সারির নম্বর বার (০-৯ . ⌫ ✓), বাংলা UI তে বাংলা অঙ্ক।
  - লেখার ঘর (নাম, ওষুধের নাম): English / বাংলা কিবোর্ড (EN/বাং বাটনে বদলানো যায়)।
  - ঘরটি সবসময় কিবোর্ডের ওপরে দেখা যায়; ✓ চাপলে মান সেভ হয়ে কিবোর্ড বন্ধ হয়।
- OS কিবোর্ড আসে না (inputmode=none); USB কিবোর্ড আগের মতোই কাজ করে।

## V70 পরিবর্তন
- ওষুধের পপআপে প্রতিটি ওষুধের নিচে আলাদা Yes / No। "No" দিলে ১ মিনিট পরে (১০ সেকেন্ডে নয়) বাকি ওষুধের জন্য আবার রিমাইন্ডার আসে।
- "No" বাটন এখন ঠিকমতো কাজ করে (আগে সঙ্গে সঙ্গে পপআপ ফিরে আসত)।
- Basal Dose Adjustment থেকে সবুজ "Save as clinician-approved dose" বাটন সরানো হয়েছে।
- ইমোজি আইকন (💊 🩺 ←) সরিয়ে SVG আইকন — Raspberry Pi তে ফন্ট ছাড়াই দেখাবে।
- মেনুর "ওষুধ বাকি" আইকন/লেবেল ৭ ইঞ্চি স্ক্রিনের জন্য বড় ও রেসপন্সিভ।

## V69 পরিবর্তন
- ইউজার পরিবর্তনের ৩ ডট এখন উপরের নামের ডান পাশে; নামের বাম পাশে "ওষুধ বাকি" আইকন — অন্য কোনো ইউজারের ওষুধ ওই সময়ের মধ্যে বাকি থাকলে দেখায় (মেনুতে ওই ইউজারের পাশেও চিহ্ন)।
- Basal Dose Adjustment বক্সে ডোজের নিচে সব সময় লাল সতর্কতা: ডোজ ডাক্তারের কাছ থেকে নিশ্চিত করতে হবে। ডোজ সমন্বয়ের সময়ের আলাদা টিক-বক্স সতর্কতা সরানো হয়েছে।
- ডাক্তারের ডোজ বাংলায় লিখলে আর বক্সের বাইরে যায় না।

## কী যুক্ত আছে
- Flask backend থেকে `Smart_medicine_dispenser_V75.html` serve হয় (`http://127.0.0.1:5000`)।
- Browser প্রতি 250 ms-এ backend event queue দেখে; GPIO থেকে Box OPEN/CLOSED event এলে V59-এর compartment handler-এ পাঠায়।
- Active profile-এর ৬টি compartment schedule প্রতি 1.8 সেকেন্ডে `/api/schedule`-এ sync হয়; profile/schedule পরিবর্তন হলে নতুন সময় backend-এ যায়।
- ভুল বক্স খুললে বাংলা ও ইংরেজি voice clip ধারাবাহিকভাবে বাজে; reminder বন্ধ থাকে যতক্ষণ বক্স খোলা। বক্স বন্ধ হলে dose এখনও due/pending থাকলে reminder আবার শুরু হয়।
- সঠিক বক্স খুললে বাংলা ও ইংরেজি confirmation voice বাজে এবং ওই নির্দিষ্ট বক্সের নাম/সময়সহ Yes/No confirmation দেখায়। ভুল বক্স খোলা নিজে থেকে medicine taken করে না।
- Medicine History ও Insulin History UI-তে আলাদা থাকে; V59-এর insulin dose history শেষ ১৫ দিনের জন্য, medicine history আলাদা থাকে।
- `static/audio/`-এ box voice MP3 ফাইল আছে: `wrong_*`, `correct_*`, `no_schedule_*`, `closed_*` (`_bn`/`_en`)। Flask-এর static route দিয়ে পরিবেশন হয়। Box বন্ধ হলে English মোডে `closed_en.mp3`, বাংলা মোডে `closed_bn.mp3` বাজে। ফাইল বদলালে HTML-এর `BOX_VOICE_VER` বাড়াও (browser cache এড়াতে)।

## ফাইল
- `Smart_medicine_dispenser_V75.html` — V59 UI + Raspberry Pi API client
- `app.py` — Flask API + Hall sensor GPIO polling
- `config.json` — GPIO mapping, sensor polarity, debounce ও default schedule
- `static/audio/*.mp3` — box voice clips (wrong / correct / no_schedule / closed, বাংলা ও English)
- `requirements.txt`, `run.sh` — install/run helper

## Raspberry Pi-তে চালানো
1. ZIP extract করো এবং project directory-তে ঢুকো:
   ```bash
   unzip Smart_Medicine_Dispenser_V59_RPi_Connected.zip
   cd smart_medicine_pi
   ```
2. `config.json`-এ GPIO pin mapping এবং `closed_level` তোমার বাস্তব sensor wiring অনুযায়ী যাচাই করো।
3. চালাও:
   ```bash
   chmod +x run.sh
   ./run.sh
   ```
4. Raspberry Pi browser-এ `http://127.0.0.1:5000` খোলো। অন্য device থেকে `http://<PI-IP>:5000`।
5. প্রথমে screen-এ একবার touch/click করো, যাতে Chromium audio playback অনুমোদন পায়। এরপর sensor test করো।

## Default BCM wiring
| Box | BCM GPIO | Physical pin |
|---|---:|---:|
| 1 | 17 | 11 |
| 2 | 18 | 12 |
| 3 | 27 | 13 |
| 4 | 22 | 15 |
| 5 | 23 | 16 |
| 6 | 24 | 18 |

**Electrical safety:** Raspberry Pi GPIO-তে 5V signal দিও না। Sensor OUT অবশ্যই 3.3V-safe হতে হবে। `closed_level: 1` initial assumption; Hall module-এর output polarity আলাদা হলে magnet দিয়ে পরীক্ষা করে প্রয়োজনমতো পরিবর্তন করো। Pin mapping বাস্তব wiring-এর সঙ্গে মিলিয়ে নাও।

## API ও mock testing
- `GET /api/health` — backend status
- `GET /api/status` — GPIO state ও expected box
- `GET /api/events` — sensor event queue
- `POST /api/schedule` — active profile-এর schedule sync
- `POST /api/warning/clear` — warning dismiss
- `POST /api/mock/event` — `mock_mode: true` থাকলেই bench testing

Laptop-এ sensor ছাড়াই test করতে `config.json`-এ অস্থায়ীভাবে `"mock_mode": true` করে server চালাও, তারপর:
```bash
curl -X POST http://127.0.0.1:5000/api/mock/event \
  -H 'Content-Type: application/json' \
  -d '{"box_id":"2","action":"BOX_OPENED"}'
```
Hardware-এ ব্যবহারের আগে `mock_mode` আবার `false` করে দেবে।

## 7-inch display
- Display 800×480 landscape হলে সে resolution ব্যবহার করো; panel-এর native resolution ভিন্ন হলে সেটিই ব্যবহার করবে। Browser kiosk/full-screen mode-এ চালালে বেশি জায়গা পাওয়া যায়।
- UI touch-first responsive layout এবং insulin screen auto-fit behavior রাখে।
- Speaker output Raspberry Pi OS Sound settings-এ ঠিক করে volume পরীক্ষা করো। প্রথম touch/click-এর পর voice clips চালু হবে।

## সীমাবদ্ধতা ও যাচাই
- Sensor শুধু compartment খোলা/বন্ধ শনাক্ত করে; ওষুধ সত্যিই খাওয়া হয়েছে কি না নিশ্চিত করে না। User-এর Yes confirmation প্রয়োজন।
- Backend event queue এবং schedule runtime memory-তে থাকে; Flask restart হলে backend event history reset হবে। UI-র medicine/insulin history browser local storage-এ থাকে।
- Pi-তে output device, browser autoplay policy, sensor polarity ও GPIO wiring বাস্তবে পরীক্ষা করতে হবে। এই build environment থেকে Raspberry Pi hardware end-to-end test করা সম্ভব নয়।

## অ্যাপ হিসেবে অটো-স্টার্ট (cmd ছাড়া)
Pi-তে ফোল্ডারটি `/home/pi/smart_medicine_pi` (বা নিজের হোম) এ রেখে একবার:
```bash
cd ~/smart_medicine_pi
./deploy/install.sh
sudo reboot
```
- Pi চালু হলে backend (systemd `smart-medicine`) নিজে চালু হয় এবং Chromium full-screen kiosk-এ UI খোলে (autoplay চালু, তাই voice প্রথম touch ছাড়াই বাজে)।
- Desktop-এ **Smart Medicine** আইকন থাকে; kiosk বন্ধ করলে (Alt+F4) আইকনে ডাবল-ট্যাপ করে আবার খোলা যায়।
- Chromium-এর নির্দিষ্ট profile (`~/.config/smart-medicine-chromium`) ব্যবহার হয়, তাই ইউজার/স্টক/শিডিউল রিস্টার্টের পরও থাকে।
- Status: `systemctl status smart-medicine`, log: `journalctl -u smart-medicine -f`। বন্ধ করতে: `./deploy/uninstall.sh`।

## Touch screen থেকে ডেস্কটপে ফেরা (keyboard ছাড়া)
Home screen-এর উপরের "Smart Medicine Dispenser Box" লেখাটি **৪ সেকেন্ড চেপে ধরে রাখো** → "অ্যাপ বন্ধ করে ডেস্কটপে যাবেন?" confirm আসবে → OK দিলে full-screen app বন্ধ হয়ে ডেস্কটপ দেখাবে (backend চলতে থাকে)। আবার চালাতে Desktop-এর **Smart Medicine** আইকন।

## V76 — 7" Raspberry Pi display-এর জন্য বড় লেখা (বয়স্কদের পড়ার সুবিধা)
- উপরের বারে বার + তারিখ (দুই লাইনে) ও সময় বড়।
- Insulin Dose-এর সব লেখা/ঘর/বাটন বড়; দরকারে স্ক্রল হয়।
- Others মেনুর টাইল (আইকনসহ, ইউজার রেজিস্ট্রেশনের আইকন বড়), Medicine Entry, Schedule ও History-র লেখা, ঘর ও বাটন বড়; প্রতিটি বক্স এক সারিতে।

## V78 — Low stock, ওষুধ মোছা, রিফিল সংশোধন
- **Low stock:** স্টক ৫ বা তার কম হলে প্রতিবার ডোজ নেওয়ার পর beep + ভয়েস রিমাইন্ডার আসে; ডোজ কার্ডে ও "নেওয়া হয়েছে" পপআপেও লাল সতর্কতা দেখায়।
- **Medicine Entry:** প্রতিটি ওষুধের পাশে লাল ডাস্টবিন বাটন — চাপলে নিশ্চিত করতে বলে, তারপর ওষুধটি মুছে যায়।
- **Refill:** প্রতিটি কার্ডে "শেষ রিফিল: +১০ · সময়" ও **সংশোধন** বাটন; সংখ্যা বদলে আপডেট দিলে স্টক পার্থক্য অনুযায়ী ঠিক হয় (০ দিলে ওই রিফিল বাতিল)।

## V79 — ওষুধ ছাড়া সময়সূচি সেট করা যাবে না
- কোনো বক্সে ওষুধ এন্ট্রি না থাকলে সেই বক্সের সময়সূচি (Start/End) বদলানো যায় না; "আগে ওষুধ এন্ট্রি করুন" পপআপ আসে এবং সময় আগের মতোই থাকে।
- ওষুধ এন্ট্রি করার পর স্বাভাবিকভাবে সময়সূচি সেট করা যাবে। বাকি সিস্টেম অপরিবর্তিত।
