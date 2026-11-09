---
name: ugc-flow
version: 1.0
description: |
  A UGC-style talking-head review video — a real creator is on camera and speaks while reviewing or
  showcasing a specific product. THE default for a UGC video brief ("make me a UGC video", "creator
  ad", "tiktok-style review").
  Triggers with BOTH: (a) review / talking-head / creator-ad intent, (b) UGC framing (UGC / creator /
  tiktok / "video of me"). A specific product confirms the match but is not required — the intake
  asks for it.
  A product URL is fine here as the SOURCE of the product (the page itself is never shown on
  screen); a brief about showing the site / app / page itself goes to ugc-saas-flow.
  NOT for: product-only with no creator (ugc-product-flow), unboxing as the climax
  (ugc-unboxing-flow), step-by-step how-to (ugc-tutorial-flow), wearing / fitting
  (ugc-try-on-flow), a site or app URL (ugc-saas-flow).
---

# ugc-flow

The talking-head UGC pipeline, every duration. Each **board** is a 16:9 sheet of 8 vertical 9:16
slots — eight beats inside ONE Seedance clip, rendered as 8 internal hard cuts. Adjacent slots
always differ in POV + distance + action, which is what makes the boundaries snap as cuts instead of
morphing. Deliverable: a hosted 9:16 MP4 (`output/final.mp4`, or `output/final_captioned.mp4` when
the user opts into on-video text).

**Hard rules (apply everywhere):**
- One creator identity: the same `character_media_id` seeds every board and clip; never regenerate it
  mid-run, never describe the creator inline as a substitute for generating them.
- Boards are generated SEQUENTIALLY (each conditioned on the previous); clips are submitted in ONE
  parallel batch.
- Never bake text into a generation. On-video text is a post-render burn the user asked for.
- The de-slop pass (step 6) runs for EVERY board. Never feed a raw `gpt_image_2` board to Seedance.
- English speech, American accent, unless the user explicitly asks otherwise.
- No greetings or re-introductions after board 1 — the monologue continues mid-thought.
- A selected Marketing Studio Hook is resolved once into `hook_contract` and changes only Board 1 /
  Clip 1. Carry the same contract through script, board, and clip prompts; never append it as loose
  text at the end.

## Media plumbing

- Generated outputs chain forward by their `job_id` into the next call's `medias[].value`
  (`role: "image"`). No download, no re-upload.
- ONE exception: Seedream i2i (`role: "image_references"`) rejects a `job_id`. Import the board's
  hosted URL with `media_import_url` first and use the returned `media_id`.
- User files come in via `media_upload_widget` (Apps-UI clients) or `media_upload` → `curl PUT` →
  `media_confirm`; a product page image via `media_import_url`.
- Shell work (ffmpeg, python) runs in the E2B sandbox via `sandbox_exec`, never locally. The sandbox
  is EPHEMERAL — every call curls its inputs in and PUTs its outputs out inside the same command,
  with `load_workflow_files: { workflow: "ugc-flow" }` when it runs a bundle script.
- You cannot re-inspect a generated image later. Whatever you wrote about the creator, the product,
  and the location IS the continuity contract — carry that text forward verbatim.

## Duration to boards

| Total D | N | Clip durations |
|---|---|---|
| 4-15 | 1 | D |
| 16-19 | 2 | balance to >=4s each (18 -> 14+4) |
| 20-30 | 2 | 15, D-15 |
| 31-45 | 3 | 15, 15, D-30 |
| 46-60 | 4 | 15, 15, 15, D-45 |
| >60 | ceil(D/15) | 15 each, last >=4s |

## Story arc by N

| N | Per-board roles |
|---|---|
| 1 | one arc HOOK → MAIN → CLOSER across the 8 slots (`FULL_ARC`) |
| 2 | `HOOK+SETUP`, then `APPLY+CLOSER` |
| 3 | `HOOK`, `MAIN`, `CLOSER` |
| 4 | `HOOK`, `REVEAL`, `APPLY`, `CLOSER` |
| >4 | `HOOK` first, `CLOSER` last, middles are `REVEAL` / `APPLY` |

Inside a board the 8 slots carry their own mini-arc (introduce → develop → land) — that is the board
prompt's job, not yours.

## Pipeline

**1. Parse.** Product (photo or URL), duration, creator gender, optional Hook selection, and any
explicit overrides (location, hair, ethnicity, outfit register, mood, props). Compute N,
per-clip durations, and the
arc role per board. Classify the brief's specificity, because the board and clip prompts need it:
`auto` (1-5 words, no scenario) = full autopilot; `guided` (1-3 sentences of idea, tone, or rough
flow) = preserve the user's tone, structure inside the board; `director` (4+ sentences with a
scenario, shot list, or location sequence) = map the user's beats 1:1 onto slots.

Resolve `Hook: Auto | None | <preset name> | Custom — <description>` through
`references/marketing-studio-hooks.md` into one `hook_contract`. Omitted means `Auto`; do not
ask a separate question merely to choose a Hook.

**2. Product intake** — `references/product-intake.md`. Ends in `product_media_id`, the canonical
`product_description`, `tier`, `category`, `content_color`, and `content_color_evidence`, decided
once and reused verbatim downstream. The last two fields are `not_applicable` only when the product
has no visible paste / liquid contents; missing or conflicting required evidence is a hard stop.

**3. Creator.** A person photo attached by the user IS the creator: bring it in
(`media_upload_widget` or `media_upload` → `media_confirm`), keep
`(character_media_id, character_url)`, and skip the generation. Hard gate — do not ask to confirm,
and the photo's framing quality is the user's own call.

Otherwise generate the creator per `references/ugc-character.md` (that file carries the beauty floor,
the variety roll, the wardrobe matrix, modesty, and the safety rules): `generate_image`, model
`soul_2`, `aspect_ratio: "3:4"`, `quality: "2k"`; poll `job_status`;
`(character_media_id, character_url)` = `(job_id, result.url)`. This step is MANDATORY when no photo
was attached — boards need a real identity image to lock against, so without it you are not ready
for step 5. Wardrobe stays fixed across boards unless the story explicitly changes context.

**4. Write the monologue** — `references/monologue-craft.md` (density, voice archetype, story-shape
menu, hook patterns, anti-slop, performed dialogue, the opt-in quiet and silent registers, series
mode). When `hook_contract.name` is neither `Auto` nor `None`, its `spoken_bridge` controls
the first line and its `internal_pattern` replaces writer's choice for the opener. Split the
result into N board segments. Save the full monologue verbatim to
`output/script.txt` and, if a hook plate might be burned later, the chosen headline to
`output/hook.txt`.

**5. Generate boards sequentially** — `references/ugc-board.md`. `generate_image`, model
`gpt_image_2`, `aspect_ratio: "16:9"`, `resolution: "2k"`, `quality: "high"`. Medias in this order,
matching the `@ImageN` declarations the prompt must open with: `[product, character]` for board 1,
`[product, character, previous_board_job_id]` for K>1 (drop the product entry when there is no
product and shift the numbering). Pass K, N, the arc role, the clip duration, `tier`, the brief's
specificity tier, the product description, and `hook_contract` for K=1 only. Board 1 must spend
exactly `hook_contract.slot_budget` opening slots on the contracted event and recovery. Poll `job_status`; keep
`(board_K_media_id, board_K_url)` = `(job_id, result.url)`.

**6. De-slop every board (MANDATORY)** — two calls, in this order:

1. `media_import_url` on `board_K_url` -> `board_K_input_id`.
2. `generate_image` with model `seedream_v5_pro`, `aspect_ratio: "16:9"`, `resolution: "2k"`,
   `medias: [{ value: board_K_input_id, role: "image_references" }]`, and this exact prompt:

> KEEP EXACTLY the framing, composition, slot layout, camera distances, poses, subjects and product of this horizontal storyboard sheet and every one of its side-by-side vertical slots — no reframe, no zoom, no crop, no re-layout, no change to the scene, to any person's face / hair / body, or to the product design. CHANGE ONLY micro-realism, applied identically in every slot: true-to-life pore-level skin with natural texture and fine vellus hair, real material detail, even natural daytime light with gentle highlight roll-off and faint true sensor noise, a flat authentic iPhone photo, deep focus. PRESERVE each face's exact shape / width / proportions 1:1 — do NOT squeeze / narrow / slim / stretch any face. AVOID AI-slop: waxy plastic skin, airbrushed poreless skin, beauty-filter smoothing, over-saturation, HDR glow / bloom / halos, oversharpening, teal-orange grade, shallow depth of field, bokeh, cinematic / DSLR look. Keep the product blank / unbranded, no added text, no watermark, no baked slot labels.

The de-slopped output OVERWRITES `(board_K_media_id, board_K_url)`; for K>1 the `previous_board` fed
into step 5 is the cleaned board K-1, so the cleaned look carries across boards. Moderation block →
retry once on `seedream_v5_lite`; still failing → continue with the raw board rather than stalling.

**7. Write the clip prompts** — `references/ugc-clip.md`, one per board, all written before any
submission. Give it K, N, the clip duration, the arc role, this board's monologue segment verbatim,
the brief's specificity tier, the board / character / product references, and `hook_contract` for
K=1 only. Clip 1 cuts 1..`slot_budget` must execute the same event; later clips receive no Hook.

**8. Submit the clips.** `generate_video`, model `seedance_2_0`, `aspect_ratio: "9:16"`,
`resolution: "1080p"`, the per-clip `duration`, `medias: [board_K, character, product]`. One call
per board, all in ONE parallel batch. Seedance renders the speech natively — no `generate_audio`.

**Frozen-frame QA on every clip, before stitching or showing anything.** Evenly spaced stills, every
product close-up, plus 2-3 mid-word frames: exactly ONE hero product (no clones); hands <=2 per
person (mirrors and frame edges included); absent features stayed absent (no cord or button on a
product sold on not having one); prop states consistent (a cap is ON or OFF, never both); the label
is not gibberish, mirrored, or another real brand; product scale matches the holding hand; lips free
of doubled edges or smears on mid-word frames; the face matches the character reference; no baked
text or subtitles. Staging failure → fix the prompt and re-roll THAT clip; lip slop → cut spoken
words first; baked text → one re-roll, then remove in post. This is a human-eye check; a motion pass
misses frozen-frame defects.

**9. Stitch and deliver.**
- N == 1: the clip is the deliverable — show its hosted URL, no sandbox needed.
- N >= 2: pre-create a `media_upload` slot, then ONE `sandbox_exec` call that curls the N clips in
  board order, concatenates with stream copy (`ffmpeg -f concat -safe 0 -i clips.txt -c copy
  output/final.mp4`, hard cuts only, no transitions), and PUTs the result to the slot; then
  `media_confirm`. Use `background: true` and poll at least every 60s.

Report the hosted URL and the total duration. Hide job ids and intermediate steps.

**10. On-video text (opt-in, at the end).** Ask ONE bundled question unless the brief already
answered it: on-video text (`Subtitles` / `Hook` / `Both` / `No text`, default No text) and whether
they want a post package. Text runs through `references/subtitles.md`, whose timing comes from a
word-level transcript of the FINAL audio — never planned beats, and no captions over silence.
Deliverable becomes `output/final_captioned.mp4`, with `output/final.mp4` kept alongside.

**Post package (only if asked):** chat text, never burned — one comment-bait caption line (open loop
the video does not answer), 3-5 hashtags (2 niche + 1-2 broad + a brand tag if any), a pinned first
comment that answers the loop or adds proof, and a one-line loop note so nobody "fixes" the loop by
adding an outro.

## Asking the user

Everything technical is pinned — models per step, 9:16 output, 16:9 boards, 1080p, audio on,
`medias` shape, N from duration, hard cuts, no identity training. NEVER ask about those and never
offer a fork. Bundle the real gaps into ONE question: duration (offer 10s / 15s / 30s / 45s), product
(URL or photo), and the optional accent/quirk offer. If the user wants creative control, include
`Hook: Auto / None / preset name / Custom` in that same question; never add a second Hook-only
question. The step-10 delivery question is the one
sanctioned extra ask.

## Critical rules

- Product analysis happens ONCE; `tier`, `category`, product description, `content_color`, and
  `content_color_evidence` are decided there and reused verbatim. Visible contents never change hue
  or opacity downstream.
- Hook resolution happens ONCE. Copy the selected contract verbatim into the first monologue,
  Board 1, and Clip 1; never change the product or repeat the Hook later.
- The `@ImageN` declarations that open a board prompt must match the `medias` order exactly.
- `Hard cut to.` markers belong only in clip prompts, never in board prompts.
- Never write a `@voice` or audio-reference note into a prompt string — audio references are attached
  to the generation, not described in the prompt.
- Two-handed actions force a static camera; a selfie POV leaves only one hand free.

## References

Load with `get_workflow_bundle_file({ workflow: "ugc-flow", path })`:
- `references/product-intake.md` — product normalization, both input paths, staging contract
- `references/ugc-character.md` — creator prompt rules (`soul_2`)
- `references/monologue-craft.md` — density, archetype, story shapes, hook patterns, anti-slop
- `references/marketing-studio-hooks.md` — selectable Marketing Studio Hook contracts and safety
  adaptations; load when a Hook is selected or offered
- `references/ugc-board.md` — the 8-slot board prompt rules (`gpt_image_2`)
- `references/ugc-clip.md` — the Seedance clip prompt rules (8 internal hard cuts)
- `references/subtitles.md` — the opt-in caption burn (uses `scripts/`)

Do NOT reach for a sibling flow's references — the rules here are self-contained and the sibling
files (product-only, unboxing, tutorial, try-on) contradict them.
