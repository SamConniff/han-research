# 21 Geezers to Go: how the video was built (24 Nov 2026)

Recount before build: `dash.v_rct_progress` = 44 nails + 22 surveys + 13 waiting = 79, so 21 places.

- **Audio:** Sunday's track, Higgsfield job f05dcd9a (vocal checked by transcription, kept as is).
- **Stills:** Nano Banana, from the `Sam-Conniff` element. B&W with the nails as the only colour.
- **Motion:** Kling 3.0 image-to-video. Hook lines lip-synced with Sync Lipsync 3 against the isolated vocal.
- **`treat.py`** B&W man, rhodamine halftone ground, nails keep their own pixels.
- **`pretreat.py`** runs the treatment over a clip.
- **`compose.py`** the edit: clone crew, captions, end card. `PLACES` and `NUM_WORD` at the top change every "21".

Rendered MP4s go in `../out/` (gitignored).
