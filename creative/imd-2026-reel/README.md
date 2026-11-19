# IMD 2026 reel: Daniele and the 100 Men Project

International Men's Day, 19 Nov 2026. 1080x1920, 66.5s, silent (music added in-app).

- `reel.html` is the whole animation; `render(t)` draws frame t. `render.js` screenshots
  every frame headlessly and pipes them to ffmpeg.
- Portraits come from the site repo: link them in first, then render.

      ln -s ../../../hard-as-nails-site/assets/100men img/100men
      node render.js              # full video -> out.mp4 (OUT=name.mp4 to rename)
      node render.js 2.5 31 50    # stills at those seconds

- `men.json` is the 99 men and their three words, parsed from `/100men/` on the site.
  Top five (Open, Empathy, Kind, Vulnerable, Honest) as ranked on that page.
- Daniele photos are crops of his own public Instagram posts (yelli) and a WhatsApp
  photo; `times-full.jpg` is The Times, 17 Nov 2026, times2.
- `lym.html` / `lym.js`: the "Love you mate" images Daniele asked for on WhatsApp.
