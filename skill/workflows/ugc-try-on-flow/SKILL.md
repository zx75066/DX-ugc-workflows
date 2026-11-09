---
name: ugc-try-on-flow
version: 1.0
description: |
  A UGC-style try-on video — a creator wears and poses with a specific wearable product, showing the
  fit and the texture detail.
  Triggers only with ALL of: (a) try-on / wearing / OOTD / fit-check intent, (b) UGC framing (UGC /
  creator / tiktok / "video of me trying on"), (c) a specific wearable product (photo, URL, or
  "this/our/my X").
  A product URL is fine here as the SOURCE of the product (the page itself is never shown on
  screen); a brief about showing the site / app / page itself goes to ugc-saas-flow.
  NOT for: a talking-head review with no try-on (ugc-flow), unboxing a delivery box
  (ugc-unboxing-flow), step-by-step how-to (ugc-tutorial-flow), product-only with no creator
  (ugc-product-flow), a site or app URL (ugc-saas-flow).
---

# ugc-try-on-flow

The try-on pipeline: a creator receives a kraft shopping bag, wears a specific garment, shows the
texture detail, and lands in a styled pose. Each **board** is a 16:9 sheet of 8 vertical 9:16 slots —
eight beats inside ONE Seedance clip, rendered as 8 internal hard cuts. Deliverable: a hosted 9:16
MP4 (`output/final.mp4`, or `output/final_captioned.mp4` when the user opts into on-video text).

**Hard rules (apply everywhere):**
- Outfit continuity is one-way: board 1 slot 1 is the pre-wear base outfit with the kraft bag; from
  slot 2 onward, for every board, the product IS the outfit and the bag is gone forever. Never
  return to the pre-wear look, never show a costume change on camera — the hard cut carries it.
- Kraft bag rule: ONE plain brown kraft shopping bag, no logo, handles optionally tinted to the
  product color, in board 1 slot 1 ONLY. The creator does not open it, does not lift the product out
  of it on camera, does not peek inside, does not vlog it — it is a contextual prop, held by one
  handle or set upright on a premium surface.
- Hand-free macros: slots 4 and 6 read texture through framing, drape, and light only. NO hand
  contact with the fabric, no operator hand in frame, and slot 6 lands on a DIFFERENT detail than
  slot 4.
- No mirrors and no reflections, ever — no mirror selfies, shop windows, phone screens, or any
  reflective surface showing the creator.
- Garment consistency lock: silhouette, color, print, and recognizable design details are identical
  in every cut where the product is worn; the garment rotates naturally with the body.
- Hairstyle and creator identity stay locked across every board and slot.
- No CTA tail. The video ends naturally on the final cut — no "link in bio", no "subscribe".
- Never bake text into a generation. On-video text is a post-render burn the user asked for.

## Media plumbing

- Generated outputs chain forward by their `job_id` into the next call's `medias[].value`
  (`role: "image"`). No download, no re-upload.
- ONE exception: Seedream i2i (`role: "image_references"`) rejects a `job_id`. Import the board's
  hosted URL with `media_import_url` first and use the returned `media_id`.
- User files come in via `media_upload_widget` (Apps-UI clients) or `media_upload` → `curl PUT` →
  `media_confirm`; a product page image via `media_import_url`.
- Shell work (ffmpeg, python) runs in the E2B sandbox via `sandbox_exec`, never locally. The sandbox
  is EPHEMERAL — every call curls its inputs in and PUTs its outputs out inside the same command,
  with `load_workflow_files: { workflow: "ugc-try-on-flow" }` when it runs a bundle script.
- You cannot re-inspect a generated image later; the text you wrote about the creator, the garment,
  and the location IS the continuity contract.

## Duration to boards

| Total D | N | Clip durations |
|---|---|---|
| 4-15 | 1 | D |
| 16-19 | 2 | balance to >=4s each (18 -> 14+4) |
| 20-30 | 2 | 15, D-15 |
| 31-45 | 3 | 15, 15, D-30 |
| 46-60 | 4 | 15, 15, 15, D-45 |
| >60 | ceil(D/15) | 15 each, last >=4s |

## The canonical 8-slot arc (board 1)

| Slot | Role | Frame |
|---|---|---|
| 1 | PRE_WEAR | Creator in a muted home-base outfit (basic tee + lounge pants, oversized hoodie + cotton shorts, plain knit + sweatpants, simple robe), one kraft bag held by a handle or set upright beside them. Product NOT visible. |
| 2 | WEARING | Now wearing the product, full-body or three-quarter, locked-off static camera. Pre-wear outfit gone, bag gone. Genuine peak reaction on the new look. ONE brief natural twirl revealing the back, then settles front-facing — board 1 only, one spin, never continuous. |
| 3 | FRONT_POSE | Front-facing at a DIFFERENT distance / POV from slot 2, reading the whole fit head to toe in an alive stance. Lip-sync slot. |
| 4 | TEXTURE_CLOSEUP | Tight hand-free macro on fabric / cut / texture. Voiceover, silent on camera. |
| 5 | TURN | Mid-turn showing the side or back, over-the-shoulder glance to the lens. Lip-sync slot. |
| 6 | DETAIL | Second hand-free macro on a different detail (hem, sleeve, collar, hardware, print, seam). Voiceover, silent on camera. |
| 7 | STYLE_POSE | A DIFFERENT room of the same home, styled pose (accent armchair, window seat, doorframe, mid-step, kitchen island, stairs, balcony). Outfit-complete, up to one paired accessory. Confident victory. |
| 8 | FINAL_LOOK | Settled alive wrap in that room, a last confident look to the lens, loop-ready mid-motion. Lip-sync slot. |

Audio model: slots 1, 2, 3, 5, 7, 8 are ON-CAMERA dialogue (the creator lip-syncs, in SELFIE and in
STATIC POV alike); slots 4 and 6 are VOICEOVER with the mouth not forming words, because those are
hand-free macros. In board 1 the slot-2 lip-sync pauses during the twirl (back to camera) and
resumes the moment they settle front-facing.

Per-board progression:

| K | Arc role | Vibe |
|---|---|---|
| 1 | `BOARD_1_TRY_ON_CANONICAL` | The arc above; slots 7-8 in a different room of the same home |
| 2 | `BOARD_2_TRY_ON_HOME_TOUR` | Slot 1 continues board 1's slot 7-8 location; slots 2-8 across other rooms |
| 3 | `BOARD_3_TRY_ON_OUTDOOR` | All 8 slots outdoor, tier-matched; light rain from slot 2 on, hair stays dry, wet-droplet macros in 4 and 6; no puddle or wet-glass reflections of the creator |
| 4 | `BOARD_4_TRY_ON_HOME_REFLECT` | Back inside, all 8 slots settled seated / lounging, narration-heavy in a settled-glow register; slot 1 may be a selfie talking head |
| >=5 | `BOARD_K_TRY_ON_LOOP` | Alternate shown / new rooms or outdoor spots, pose variations |

Rain in K=3 is an explicit exception to the consistency lock: droplets, surface sheen, and minor
temporary darkening are fine; silhouette, color, and print stay identical, and never soak through.

## Pipeline

**1. Parse.** Product (photo or URL), duration, creator gender, and any explicit overrides
(location, hair, ethnicity, outfit register, mood, props). Compute N and the per-clip durations.
Classify the brief's specificity for the board and clip prompts: `auto` (1-5 words, no scenario) =
full autopilot; `guided` (1-3 sentences of idea, tone, rough flow) = preserve the user's tone;
`director` (4+ sentences with scenario, shot list, or location sequence) = map their beats 1:1.

**2. Product intake** — `references/product-intake.md`. Ends in `product_media_id`, the canonical
`product_description` (garment mechanics, material, drape), `tier`, `category`, `content_color`,
and `content_color_evidence`, decided once. The last two fields normally resolve to
`not_applicable` for garments; any included visible paste / liquid product must pass the color gate
or the run stops.

**3. Creator.** A person photo attached by the user IS the creator: bring it in, keep
`(character_media_id, character_url)`, skip the generation. Hard gate — do not ask to confirm.

Otherwise generate per `references/ugc-character.md` (beauty floor, variety roll, wardrobe matrix,
modesty, safety): `generate_image`, model `soul_2`, `aspect_ratio: "3:4"`, `quality: "2k"`; poll `job_status`; `(character_media_id, character_url)` =
`(job_id, result.url)`. MANDATORY when no photo was attached — boards need a real identity image to
lock against.

Accent and quirk are OPT-IN: offer them inside the single intake question when the brief names an
origin or asks for "weird" / "viral" energy. Default is neutral English, no quirk. If opted in,
write the persona sentence ONCE and restate it VERBATIM in the character prompt, every board prompt,
and every clip prompt. If the user can drop a 5-10s voice sample, attach it to the clip generation as
an audio reference ("accent and vocal delivery reference only — do not copy words, only the accent,
melody, and timbre"). Offer once, never block.

**4. Write the monologue.** Density: <=10s ~ 12-20 words, 11-12s ~ 20-28, 13-15s ~ 28-35. Split into
N board segments; the per-cut distribution is the clip prompt's job. Greetings and product
introduction only in board 1.

Default frame is a PERSONAL-WANT MINI-STORY, not generic praise — the product is the premise, so
there is no product delay to engineer: real stakes in the wanting, ONE "but then" beat (the fit
moment), the CTA-free landing inside the resolution.
- Board 1 opener (inside cut 1) plants the wanting / waiting / finally-here frame ("I have been
  eyeing this for actual months and the package finally landed", "the second I saw this drop I knew
  it was mine"). Pick a variant that matches the creator reference's apparent gender.
- Board 1 middle (cuts 2-3) is the first fit / fabric / drape observation in creator language.
- Board 1 close (cuts 7-8) is the location vibe and the keep-it verdict.
- K>1 continues mid-thought with fit, fabric, location, outdoor, or settled-reflection observations;
  K=4 shifts into a "now that I have actually lived in this for a few hours" register with longer,
  calmer lines.

Optional board-1 opener flavors that still fit a PRE_WEAR first cut: a mid-sentence confession opened
on word four, a hostile open aimed at the viewer, a result-first line referring backwards to what
made them order it, or one short performed hold (<=0.7s) over the bag before the line.

Anti-slop on every line: never open with `Okay wait / Okay so / OMG / Hey guys / So basically / Stop
scrolling / You NEED this / Story time`; never use "literally", "obsessed", "game-changer", "holy
grail", "changed my life", "hits different", or corporate words (elevate / seamless / effortless).
Avoid abstract praise entirely — specific sensations replace it. Every claim carries one concrete,
unless the user supplied an approved-claims list, in which case only those exact strings are allowed.
At most ONE peak reaction per clip in the monologue. Cut echoes and repeats first.

**First-word constraint (every board segment):** the literal first word must be hook content — never
`OK / Okay / Okay so / Alright / Alright so / So / Yeah so / Right so / Um / Well / Like / Wait /
Wait what / Hold on`.

Save the full monologue verbatim to `output/script.txt`, and the hook headline to `output/hook.txt`
if a plate might be burned later.

**5. Generate boards sequentially** — `references/ugc-try-board.md`. `generate_image`, model
`gpt_image_2`, `aspect_ratio: "16:9"`, `resolution: "2k"`, `quality: "high"`. Medias in this order,
matching the `@ImageN` declarations the prompt opens with: `[product, character]`, plus
`previous_board_job_id` when K > 1. Pass K, N, the arc role from the progression table, the clip
duration, `tier`, the specificity tier, and the product description. Poll `job_status`; keep
`(board_K_media_id, board_K_url)` = `(job_id, result.url)`.

**6. De-slop every board (MANDATORY)** — two calls, in this order:

1. `media_import_url` on `board_K_url` -> `board_K_input_id`.
2. `generate_image` with model `seedream_v5_pro`, `aspect_ratio: "16:9"`, `resolution: "2k"`,
   `medias: [{ value: board_K_input_id, role: "image_references" }]`, and this exact prompt:

> KEEP EXACTLY the framing, composition, slot layout, camera distances, poses, subjects and product of this horizontal storyboard sheet and every one of its side-by-side vertical slots — no reframe, no zoom, no crop, no re-layout, no change to the scene, to any person's face / hair / body, or to the product design. CHANGE ONLY micro-realism, applied identically in every slot: true-to-life pore-level skin with natural texture and fine vellus hair, real material detail, even natural daytime light with gentle highlight roll-off and faint true sensor noise, a flat authentic iPhone photo, deep focus. PRESERVE each face's exact shape / width / proportions 1:1 — do NOT squeeze / narrow / slim / stretch any face. AVOID AI-slop: waxy plastic skin, airbrushed poreless skin, beauty-filter smoothing, over-saturation, HDR glow / bloom / halos, oversharpening, teal-orange grade, shallow depth of field, bokeh, cinematic / DSLR look. Keep the product blank / unbranded, no added text, no watermark, no baked slot labels.

The de-slopped output OVERWRITES `(board_K_media_id, board_K_url)`; for K>1 the `previous_board` fed
into step 5 is the cleaned board K-1. Moderation block → retry once on `seedream_v5_lite`; still
failing → continue with the raw board rather than stalling.

**7. Write the clip prompts** — `references/ugc-try-clip.md`, one per board, all written before any
submission. Give it K, N, the clip duration, the arc role, this board's monologue segment verbatim,
the specificity tier, and the board / character / product references. That file carries the per-cut
audio model, the phrase bank, and the banned AI-tell phrases.

**8. Submit the clips.** `generate_video`, model `seedance_2_0`, `aspect_ratio: "9:16"`,
`resolution: "1080p"`, the per-clip `duration`, `medias: [board_K, character, product]`. One call
per board, all in ONE parallel batch. Seedance renders the speech natively — no `generate_audio`.

**Frozen-frame QA on every clip, before stitching or showing anything.** Evenly spaced stills, every
garment close-up, plus 2-3 mid-word frames: the garment matches the reference in silhouette, color,
and print; no hand touches the fabric in the macro cuts; no mirror or reflection anywhere; the kraft
bag appears only in board 1 slot 1; hands <=2 per person (edges included); hairstyle unchanged; lips
free of doubled edges or smears on mid-word frames, and closed in the voiceover cuts; the face
matches the character reference; no baked text. Staging failure → fix the prompt and re-roll THAT
clip; lip slop → cut spoken words first.

**9. Stitch and deliver.**
- N == 1: the clip is the deliverable — show its hosted URL, no sandbox needed.
- N >= 2: pre-create a `media_upload` slot, then ONE `sandbox_exec` call that curls the N clips in
  board order, concatenates with stream copy (`ffmpeg -f concat -safe 0 -i clips.txt -c copy
  output/final.mp4`, hard cuts only, no transitions), and PUTs the result to the slot; then
  `media_confirm`. Use `background: true` and poll at least every 60s.

Report the hosted URL and the total duration. Hide job ids and intermediate steps.

**10. On-video text (opt-in, at the end).** Ask ONE bundled question unless the brief answered it:
on-video text (`Subtitles` / `Hook` / `Both` / `No text`, default No text) and whether they want a
post package. Text runs through `references/subtitles.md` — timing from a word-level transcript of
the FINAL audio, never planned beats. Deliverable becomes `output/final_captioned.mp4`, with
`output/final.mp4` kept alongside.

**Post package (only if asked):** chat text, never burned — one comment-bait caption line, 3-5
hashtags (2 niche + 1-2 broad), a pinned first comment, and a one-line loop note.

## Asking the user

Everything technical is pinned — models per step, 9:16 output, 16:9 boards, 1080p, audio on, `medias`
shape, N from duration, hard cuts, the canonical 8-slot arc, no identity training. NEVER ask about
those and never offer an "alternative arc" fork. Bundle the real gaps into ONE question: duration
(offer 10s / 15s / 30s / 45s), the product (URL or a photo of the item being tried on), and the
optional accent/quirk offer. The step-10 delivery question is the one sanctioned extra ask.

## Failure handling — character re-roll

If board generation or clip submission fails twice in a row on the same call, assume the Soul
character render was rejected. Re-submit the SAME character prompt from step 3 (new seed, same
described person), capture fresh `(character_media_id, character_url)`, discard every
`board_K_media_id`, and re-run from step 5. Cap at 2 re-rolls per session, then stop and report —
never fall through to `generate_video` with an empty `medias` array, which silently becomes
text-to-video of the wrong thing.

## Critical rules

- Product analysis happens ONCE; `tier`, `category`, product description, `content_color`, and
  `content_color_evidence` are reused verbatim. Visible contents never change hue or opacity.
- The `@ImageN` declarations that open a board prompt must match the `medias` order exactly.
- `Hard cut to.` markers belong only in clip prompts, never in board prompts.
- Never write a `@voice` or audio-reference note into a prompt string — audio references are attached
  to the generation, not described in the prompt.
- Realistic fit: the product drapes naturally with real-world proportions, never exaggerated.
- Two-handed actions force a static camera; a selfie POV leaves only one hand free.

## References

Load with `get_workflow_bundle_file({ workflow: "ugc-try-on-flow", path })`:
- `references/product-intake.md` — product normalization, both input paths, staging contract
- `references/ugc-character.md` — creator prompt rules (`soul_2`)
- `references/ugc-try-board.md` — the 8-slot board prompt rules (`gpt_image_2`), kraft bag and
  per-K location progression
- `references/ugc-try-clip.md` — the Seedance clip prompt rules (8 internal hard cuts, audio model)
- `references/subtitles.md` — the opt-in caption burn (uses `scripts/`)

Do NOT reach for a sibling flow's references — the rules here are self-contained and the sibling
files (talking-head, product-only, tutorial, unboxing) contradict them.
