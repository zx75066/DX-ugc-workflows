# SaaS creator overrides — framing, setting, voice (layer over the Soul base)

Load `references/soul-v2-ugc-character.md` first (identity, anti-slop, safety); apply these
overrides in BOTH the Soul prompt and the Seedance clip prompt so still and video match.

- **Framing (9:16 video; Soul seed is 3:4):** medium shot from mid-torso up, creator ~2/3 of the
  frame, head centred, eyeline into the lens. Clear headroom in the top ~15-20% (breathing room +
  where the screenshot inset's top lands — NOT for subtitles). Face/hands stay out of the bottom
  ~15% caption band.
- **Setting:** authentic self-filmed spot — phone propped up, real lived-in home (couch / bed /
  kitchen counter / desk), natural light, slight handheld imperfection; never a studio backdrop.
  Pick from site `type`/`audience` (b2b founder at a tidy desk vs consumer-app creator on a couch)
  and lock ONE setting for the whole video.
- **Voice:** natural **American accent — never British**; state it in the Seedance prompt ("speaks
  in a natural American accent"). One voice, one identity throughout.
- **Delivery:** "natural, lively spoken delivery with varied rhythm and emphasis — like a real
  creator talking to a friend, NOT a narrator; natural hand gestures"; ~2.7–3.0 words/sec varying
  within the take; 2–3 emphasis/non-verbal beats spread across the clip.
- **Audio texture (in every clip prompt):** recorded on the scene's iPhone front-camera mic —
  natural, slightly compressed, NOT studio-clean, NO music; ambient = the natural sound of what
  the picture shows (same scene → same ambient every clip), kept low under the voice.

Output: `(character_media_id, character_url)` from `generate_image` model `soul_2` (3:4, 2k, poll
to terminal) — chained forward by job-id, no download/re-upload.
