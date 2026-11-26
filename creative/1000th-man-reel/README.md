# 1000th man reel (draft)

1080x1920, 54s, silent, with the text on screen (music added in-app). The story runs 1 man, then 2 (Daniele), 20, 100, the science, a ticker that freezes on 999, and an empty slot asking "Is that you?".

- `reel.html` is the whole animation. `render(t)` draws frame t.
- Link the portraits in first, then render:

      ln -s ../../../hard-as-nails-site/assets/100men img/100men
      node render.js            # full video -> out.mp4
      node render.js 2 10 46    # stills at those seconds

- **Photo slots to fill.** Drop the file in and render again:
  - `img/sam-first.jpg`: Sam's first nails, on his own (early Instagram). Until it arrives, a marked placeholder shows.
  - `img/daniele-selfie.jpg`: Daniele's selfie from the Leaders in Sport and Salesforce decks. Falls back to `img/daniele-0.jpg`.
- Opening: `img/sam-harry.jpg` (Love On Tour, 2023; daughter's face pixelated for social) then `sam-ig-1/2/3.jpg`, cropped from Sam's Instagram posts as used on slide 11 of the Salesforce launch talk deck (4 Nov 2026, v3). Then `img/daniele-0.jpg` (WhatsApp, Nov 2024), `img/first-20.jpg` (to come; falls back to the site's `group-20.jpg`), the 100 Men wall, then `g3-salon.jpg` and `g5-stage.jpg` for "Then hundreds".
- The scale scene draws 8,500 squares, one per 1,000 men: the first is the 1,000th man, 500 pink are the target, the rest are the UK's 8.5 million midlife men (ONS mid-2024, from the stats card). The 3.5% to 10% range and "about 6%" are also from the card.
