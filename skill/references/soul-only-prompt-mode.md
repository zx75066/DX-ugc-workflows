# Soul-only prompt mode

Use this adaptation only after selecting one creator-based product workflow. It preserves the child
workflow's planning rules while replacing paid board and video generation with text deliverables.

Enter this mode only when no usable local creator image exists and the user explicitly permits one
Soul generation. If a usable creator image and product image already exist, select
`reference-only-prompt` instead. Never spend a Soul call merely to replace an available identity
reference.

## Call boundary

The selected local child `SKILL.md` remains the orchestrator. Do not call remote workflow discovery.
Higgsfield calls are allowed only inside the creator stage:

1. Optionally preflight the one Soul image cost.
2. Submit `generate_image` with `model: soul_2`, `aspect_ratio: 3:4`, and `quality: 2k`.
3. Use the exposed job-display/status operation only as required to obtain that image.
4. Immediately archive the completed image locally with:

   ```bash
   python3 .agents/skills/higgsfield-ugc-workflows/scripts/save_creator_image.py \
     --url '<character_url>' \
     --job-id '<character_job_id>'
   ```

   The script saves into `higgs -ugc/模特图/`, validates the image signature, writes atomically,
   and prints the absolute path. Freeze that path as `character_local_path`. A hosted URL alone is
   not a completed creator stage. If the download or validation fails, retry the same URL once;
   if it still fails, stop and report the archival failure instead of continuing to text boards.

Do not pass the product image as Soul media. Analyze it locally and use its category/tier context to
write a product-free creator prompt. Do not call any other image, video, audio, assembly, caption,
or publishing operation.

When supported by the live generation schema, perform the preflight through
`generate_image(..., get_cost: true)`; it does not submit a job. Missing creator gender is a real
input gap: bundle it into the single intake question and never default it from examples or product
stereotypes.

## Adapt the pipeline

1. Parse the request exactly as the selected child workflow requires.
2. Inspect and normalize the product locally. Freeze the continuity contract. For every paste,
   gel, cream, serum, oil, lotion, liquid, mist, foam, or similar visible content, complete the
   selected workflow's mandatory dispensed-content color gate before creator generation. Missing
   or conflicting evidence stops this mode; never invent a color in a text board or clip prompt.
3. Write and submit the product-free creator prompt once. Freeze the visual traits, returned creator
   image, hosted `character_url`, and verified local `character_local_path`.
4. Write the child workflow's monologue or voice plan at its original duration density.
5. Replace each rendered board with a structured text board containing the exact original slot
   count, arc role, time span, POV, distance, location, subject action, product state, both-hand
   allocation, audio mode, spoken words, and continuity constraints.
6. Apply every child-specific law to the text board: Hook slots for talking-head, one-way wardrobe
   and macros for try-on, global real steps for tutorial, or sealed-box/reveal state for unboxing.
7. Write one final clip prompt per text board. Translate each slot into motion and exact hard-cut
   timing. Preserve the monologue verbatim and repeat identity/product anchors where the missing
   rendered board would otherwise have supplied them.
8. Stop and deliver the prompt package. Do not pretend a board image, video, QA result, subtitle, or
   hosted URL exists.

## Reference order

The original full workflows send `[board, character, product]` to video generation. With the board
omitted, preserve any explicit reference order from the user. When no order is specified, declare
and deliver the remaining references as:

```text
@Image1 = creator identity reference
@Image2 = product appearance reference
```

The attachment order must match those declarations. For unboxing, add an optional package image
only when the final target generator accepts a third independent reference and name it explicitly.

If the user explicitly requests product first, use this order consistently in both the prompt and
the final paths:

```text
@Image1 = product appearance reference
@Image2 = creator identity reference
```

Treat the child files' `eight-cut` and `four-cut` wording as segment counts: eight shots have seven
between-shot `Hard cut to.` boundaries, and four shots have three. Label every shot, but do not add
an extra transition after the final shot.

## Required deliverables

- selected `workflow_id` and execution mode `soul-only-prompt`
- explicit statement that exactly one generation stage was used, including its preflight/credit
  result, and that every later generation/publishing stage was skipped
- frozen product analysis and canonical product description, including locked `content_color` and
  `content_color_evidence` (or `not_applicable`)
- Soul creator prompt, generated creator image, hosted URL, and verified local absolute path
- frozen creator continuity description
- full spoken script
- structured text boards with exact time spans
- final video-generation prompt for each clip
- reference-image order and generator assumptions
- post-generation QA checklist and multi-clip hard-cut order when applicable
- explicit list of skipped generation stages

The final reference section must label both local files explicitly, in the resolved attachment
order. The default is:

```text
@Image1 = creator identity reference: <absolute character_local_path>
@Image2 = product appearance reference: <absolute product source path>
```

Never finish with only the hosted creator URL when a local product path is shown.

## Unsupported cases

- Reject `ugc-product-flow`: it has no creator identity stage, so one Soul image is wasteful and
  violates its subject model.
- Reject `ugc-saas-flow`: real screenshot capture, timed compositing, and mandatory captions are the
  core output rather than optional render stages.
