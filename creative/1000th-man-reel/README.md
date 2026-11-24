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
- The "Then twenty" montage: `img/g1-trio.jpg`, `g2-vitacoco.jpg`, `g3-salon.jpg`, `group-20.jpg` (from the site), `g4-pub.jpg`, `g5-stage.jpg`. Sam sent these on 24 Nov 2026. Check consent before posting: some show women nail techs and partner logos.
- The Daniele slot uses `daniele-0.jpg`, the WhatsApp photo from November 2024.
- Stats on screen: "fear of judgement halved" and "willingness to stand up for others doubled", both from the approved stats card. The target is half a million.
