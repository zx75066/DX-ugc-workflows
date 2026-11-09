# Workflow responsibility map

## Routing principle

Route by the visual subject and the primary action, not by the mere presence of a product image or
URL. Once selected, use only that workflow's references.

## `ugc-flow`

- Purpose: default talking-head UGC review or creator ad.
- Subject and audio: one identity-locked creator speaks on camera; lip sync matters.
- Product: optional at initial routing; a product URL may be source-only.
- Structure: each board has eight vertical slots and becomes one eight-cut clip. Story roles scale
  from one `FULL_ARC` board to multiple Hook/Main/Apply/Closer boards.
- Unique ownership: creator casting, first-person monologue, native hook patterns, local Marketing
  Studio Hook contracts, eight-slot boards, and eight-cut talking-head prompts.
- Output: 9:16 rendered video in full mode; creator image, monologue, text boards, and video prompts
  in soul-only mode; or existing creator/product references plus the same text deliverables in
  zero-credit reference-only mode.
- Hard boundary: do not use for product-only, page demos, unboxing climax, tutorials, or try-ons.

## `ugc-product-flow`

- Purpose: product-only UGC where the product is the sole hero.
- Subject and audio: voiceover only. People may appear only as hands, POV, or cropped support; no
  identity lock and no on-camera dialogue.
- Product: required. Stop if there is no usable product reference.
- Structure: four slots per board: Product Intro, Demo A, Demo B, Result.
- Unique ownership: product board rules, grip/weight physics, voice gender alignment, and four-cut
  product prompts.
- Output: 9:16 product video, optional post-render text.
- Hard boundary: no creator generation and no soul-only creator mode.

## `ugc-saas-flow`

- Purpose: UGC for a website, web app, store, or product page when the page must appear.
- Subject and audio: one continuous talking-head creator with voice under real screenshot cards.
- Input: site URL is required; capture six to ten useful sections, with at least three usable cards.
- Structure: no storyboard boards and no internal cuts. Generate continuous creator clips, then
  composite static page cards at narrated word times.
- Unique ownership: mobile page capture, capture fallback, screenshot mapping, card compositing,
  mandatory hook plate and word captions, and optional TikTok publication.
- Output: always-captioned hosted video.
- Hard boundary: never AI-generate UI, use screen recording, or select this merely because a product
  URL exists.

## `ugc-try-on-flow`

- Purpose: wearable try-on, OOTD, or fit-check content.
- Subject and audio: one identity-locked creator; dialogue in creator shots and voiceover in fabric
  macros.
- Structure: eight slots. Board 1 moves once from pre-wear plus kraft bag to worn outfit, then front
  pose, two hand-free details, turns, styling, and final look. Later boards progress through home,
  outdoor, and reflective contexts.
- Unique ownership: one-way outfit continuity, one-slot kraft bag, garment identity, drape and fit,
  hand-free macro rules, no reflections, and CTA-free ending.
- Output: 9:16 try-on video, soul-only prompt package, or two-reference zero-credit prompt package.
- Hard boundary: do not show an on-camera costume change or reuse general review/unboxing boards.

## `ugc-tutorial-flow`

- Purpose: chronological how-to content for a real product.
- Subject and audio: one identity-locked creator demonstrates each real step.
- Structure: four global steps per board. Every slot owns one baked `Step N - Heading` caption; the
  final clip alone may add a short CTA tail.
- Unique ownership: mandatory usage analysis, global step numbering, step-caption typography,
  chronological state, and tutorial clip prompts.
- Output: 9:16 tutorial video, soul-only prompt package, or two-reference zero-credit prompt package.
  Extra captions are optional because step labels already exist.
- Hard boundary: never invent steps or let a text-board adaptation pretend captions were rendered.

## `ugc-unboxing-flow`

- Purpose: package opening where the product reveal is the climax.
- Subject and audio: one identity-locked creator speaks through the reveal.
- Inputs: product is required; a real package photo is optional, otherwise use one generic sealed
  brown delivery box.
- Structure: four slots: Packed, Reveal, Product Focus, Satisfaction. Later boards continue after
  reveal.
- Unique ownership: sealed-box start, one-way box disappearance, optional package reference,
  reveal reaction, and post-reveal continuation.
- Output: 9:16 unboxing video, soul-only prompt package, or two-reference zero-credit prompt package.
- Hard boundary: the product is absent in the first slot and the box never returns after reveal.

## Shared support files

Each workflow owns its own `product-intake.md`, `subtitles.md`, and helper scripts even where the
contents look similar. Keep the selected workflow name when loading or executing them because
sandbox loading and downstream assumptions are workflow-specific.
