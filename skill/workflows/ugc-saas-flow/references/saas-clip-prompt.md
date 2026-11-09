# Seedance clip prompt — ONE continuous talking-head shot

Each clip is a single continuous shot of the creator speaking one beat to camera — **no
storyboard, no intra-clip cut, no Angle Lock**. The site and product are added later in the
composite; they are never rendered inside a clip.

## Compose each prompt, in order

1. **Subject** — the creator (seeded by the SAME `character_media_id`; never re-describe a person).
2. **Framing** — 9:16, medium shot ~2/3 of frame, head centred, headroom above, eyeline into the
   lens; face/hands out of the bottom ~15%.
3. **Setting** — the locked self-film scene, same every clip.
4. **Delivery** — US accent (never British); ~2.7–3.0 words/sec varying within the take (quicker
   connectives, slower on the number/price/CTA); natural gestures.
5. **Spoken line** — the beat's monologue segment, verbatim, English. Split into short spoken
   phrases (one idea each, payload word at the END of its phrase).
6. **Audio** — iPhone front-camera mic, scene-matched ambient low under the voice, no music.
7. **The ban line** (below) in EVERY clip.

Anti-slop: same banned-word list and one-concrete-per-claim rule as `saas-monologue.md`.

## Two hard bans

- **Bug D — product only in the closer.** A body clip's VISUAL never mentions the product (the
  spoken line may) — with no input image Seedance invents a fake one. The closer names/shows it
  only via the real product image passed as a second `media`.
- **Bug E — never render a site/UI.** Include verbatim in every clip: *"No website, no web
  interface, no app UI, no screen / monitor / browser / rendered content on any phone or device
  screen anywhere in the shot."* SaaS closer: the creator acts on a phone with the screen turned
  away or blank.

## Pre-submit check (grep each prompt; any hit → rewrite)

`Hard cut` / `Cut 1` / `slot` / `board` → multi-shot, rewrite · product name in a body VISUAL →
remove (Bug D) · `website/UI/screen/browser` in any visual → convert to the Bug-E ban · confirm
framing, US accent, varied ~2.7–3.0 wps, phone-mic ambient, no music in every clip.
