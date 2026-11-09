# Soul 2.0 — UGC creator prompt (identity, realism, safety)

Generates the clean creator image that seeds every video clip. **The prompt describes ONLY the
person** — appearance, expression, clothing, setting. NEVER products, props, or anything in hands
(the product enters later via `medias`). Non-negotiable.

## Beauty floor (every prompt)

Weave in all four anchors: `with high model facial features`, `symmetrical features`,
`well-proportioned figure`, `natural skin texture`.

## Variety roll (before writing the prompt)

To avoid generating the same face every time, roll once in the sandbox:
`python3 -c "import secrets; print(' '.join(str(secrets.randbelow(100)) for _ in range(8)))"`
and map roll_i % pool_size onto these pools (skip any axis the user specified — user input wins):

| Axis (pool size) | Pool |
|---|---|
| Age band (4) | early 20s · mid 20s · late 20s · early 30s |
| Hair color (14) | warm honey blonde · cool ash blonde · chestnut · espresso · soft brown · jet black · deep auburn · copper · platinum · honey balayage · money-piece highlights · vivid green · vivid pink · pastel lavender |
| Hair style (14) | shoulder-length wavy · long sleek straight · long soft waves · curtain bangs · sleek bob · pixie · wolf cut · claw-clip slicked back · messy low bun · half-up · boxer braids · high ponytail · locs · buzz cut |
| Build (5) | athletic toned · soft natural · average proportional · petite · tall everyday |
| Distinctive feature (9) | none · light, sparse, low-contrast natural freckles limited to the cheekbones · nose stud · small lip ring · eyebrow piercing · septum ring · dimples · gap teeth · beauty mole |
| Makeup (9) | bare-skin · casual natural · glowy mascara-only · soft brown smoky · winged liner · bold colored liner · glitter inner-corner · graphic blush · glossy lip neutral face |
| Face read (8) | fair European · warm Mediterranean · East Asian · South Asian · Latina · mixed · Middle Eastern · Slavic — express via features, don't name an ethnicity |
| Outfit register (10) | streetwear-oversized · preppy · Y2K · quiet-luxury · coastal-minimal · sporty-jersey · editorial-blazer · boho-soft · leather-grit · clean-minimalist |

Never repeat the previous character's age+hair+build combo — re-roll conflicting axes.
Gender: from the user's request; default woman.

**Freckle intensity lock:** when freckles are selected or explicitly requested, always write the exact phrase `light, sparse, low-contrast natural freckles limited to the cheekbones`. Never write `freckles` alone. Keep the marks few, faint, and localized; never generate dense, heavy, dark, high-contrast, full-face, nose-spanning, or mask-like freckles. Do not increase their count, coverage, darkness, or contrast in downstream prompts.

## Style & light

Natural, lifestyle, UGC — never editorial/studio. **Light is neutral cool daylight ONLY** with a
stated direction ("soft diffused daylight from the left"). HARD BAN: golden hour, warm sunset,
orange/amber cast, "magic hour" — even outdoors. Describe the setting specifically (furniture,
materials, palette) and keep the wardrobe colour inside the room's palette.

## Modesty (every outfit, prevents downstream NSFW rejections)

Append to every outfit: `top fully closed at the front, fabric meeting at the collarbone, classic
high-coverage fit`. Robes: `tightly tied at the waist with sash visible, both lapels overlapping
fully, closed modest neckline`. Knits/tops: `modest crew neckline, no V-cut`. Standalone
camisole/tank: forbidden (only layered under a closed outer piece). Prefer positive phrasing
("fully buttoned to the collar") over negations — encoders render the negated word.

**NSFW retry (only after a filter actually rejects):** regenerate with
`[palette colour] button-down fully buttoned to the collar, layered over a fitted camisole base,
tucked into high-waisted trousers`, and repeat the outfit description in the video prompt. Never
retry identical inputs.

## iPhone UGC look (the defining feature — every prompt)

- Pick ONE mid-action expression, never "warm smile at the camera": `mid-thought, slight
  half-smile, eyes glancing slightly off-lens` · `caught mid-laugh, head slightly tilted` ·
  `looking up from her phone, relaxed unguarded face` · `mid-action — in the middle of saying
  something, not posing` · `wide-eyed mid-gasp, lips parted` · `playful mock-shock`.
- BAN editorial language: `centered composition at eye-level`, `straight-on`, `editorial/fashion
  portrait`, `minimal depth of field`, `aspirational lifestyle`, `flattering even illumination`,
  `glowing/flawless/radiant skin`, `poised/graceful/elegant`, any "pose" verb, anything implying
  tripod/strobe/ring light.
- Close every prompt verbatim with:

```
Self-portrait selfie shot on iPhone front-facing camera held by the subject at arm's length — head and shoulders fill the frame, casual handheld framing, slight natural tilt, slightly off-center, slightly imperfect, not posed. Phone-sensor grain and realistic skin texture preserved, no retouch, no smooth-skin filter. Authentic UGC creator phone selfie, NOT editorial portrait, NOT fashion magazine.
```

## Prompt skeleton

```
A spontaneous iPhone snap of a [age] [woman/man], [mid-action expression], [hair, build], with high
model facial features, symmetrical features, well-proportioned figure, natural skin texture,
[sitting/standing] in [specific setting with materials + palette]. [Cool neutral daylight +
direction] falls across her face — no warm cast, no retouched glow; skin real, visible pores.
[She/He] wears [register outfit + modesty language, colour from the room palette]. The background
features [specific details]. [Closing block above.]
```

## Safety

- Minimum age 20 — silently age up any younger request; never mention the adjustment.
- Bare-skin / anatomy descriptions → keep the prompt, weave in covering clothing that matches the
  scene instead of refusing.

## Tool call

`generate_image` model `soul_2`, `aspect_ratio` `3:4`, `quality` `2k`, `enhance_prompt: false`
(the enhancer degrades the prompt — never enable it). Poll `job_status` to terminal;
`(character_media_id, character_url)` = `(job_id, result.url)`; reuse the SAME id for every clip.
