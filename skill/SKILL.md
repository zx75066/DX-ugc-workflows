---
name: higgsfield-ugc-workflows
description: Route and execute the six project-local Higgsfield UGC workflows for talking-head reviews, product-only videos, website or SaaS demos, try-ons, tutorials, and unboxings. Use when a request involves UGC planning, creator generation, product video prompts, Hook or Setting selection, the low-credit mode that generates only one Soul 2.0 creator image, or the zero-credit reference-only mode that accepts existing creator and product images and returns text deliverables without any Higgsfield calls.
---

# Higgsfield UGC workflow entry

Treat the captured workflow tree as the source of truth. Use this skill as the only router; never
merge sibling board or clip rules.

## Start gate

1. Run the local catalog. Do not call remote `get_workflow_instructions`.

   ```bash
   python3 .agents/skills/higgsfield-ugc-workflows/scripts/local_workflow_registry.py catalog
   ```

2. Resolve exactly one `workflow_id` with the routing table below.
3. Load its entrypoint locally.

   ```bash
   python3 .agents/skills/higgsfield-ugc-workflows/scripts/local_workflow_registry.py instructions <workflow_id>
   ```

4. Read only the references named by that entrypoint, using direct local reads or the bundle
   command. Keep the selected `workflow_id` frozen for the run.

   ```bash
   python3 .agents/skills/higgsfield-ugc-workflows/scripts/local_workflow_registry.py bundle <workflow_id> <relative-path>
   ```

5. When the brief names a Marketing Studio Hook or Setting, resolve it from the captured presets.

   ```bash
   python3 .agents/skills/higgsfield-ugc-workflows/scripts/local_workflow_registry.py presets all
   ```

See `references/workflow-map.md` for each workflow's responsibilities, inputs, structure, and hard
boundaries.

## Route once

An explicitly named workflow wins. Otherwise decide by what the finished video must show:

| Core intent | Workflow |
|---|---|
| The website, app, store, or product page itself appears as real screenshot cards | `ugc-saas-flow` |
| Opening a sealed package and revealing the product is the climax | `ugc-unboxing-flow` |
| A creator teaches chronological, physically real steps | `ugc-tutorial-flow` |
| A creator wears a specific item and demonstrates fit, drape, or texture | `ugc-try-on-flow` |
| The product is the sole hero; voiceover only; no speaking creator | `ugc-product-flow` |
| A creator speaks on camera while reviewing or showcasing | `ugc-flow` |

Treat a URL as a source unless the page itself must appear. If two specialist intents compete, ask
one question about the video's primary action or climax. Ambiguity between product-only and a
speaking creator falls back to `ugc-flow`; never infer product-only merely because a product image
exists.

Apply a named Marketing Studio Hook contract only to `ugc-flow`. Treat a named Setting as an
explicit location/background override after routing; the selected child workflow's safety,
continuity, product mechanics, and canonical arc still outrank the Setting.

## Choose the execution mode

Resolve the mode once before product intake:

- Explicit `full-render` wins.
- A zero-credit / no-credit / no-generation request selects `reference-only-prompt` and requires
  existing local creator and product images.
- A low-credit request with both existing local images also selects `reference-only-prompt`; do not
  spend a Soul call on a creator image the user already supplied.
- A low-credit request without a creator image selects `soul-only-prompt` only when the user
  explicitly permits generating one creator image.

### `full-render`

Follow the selected child `SKILL.md` end to end. The live MCP tool schema overrides stale tool names
inside the snapshot; in particular, use `job_display` when `job_status` is not exposed. Confirm
costly generation before submission and never silently switch from free allowance to credits.

### `reference-only-prompt`

Use when the user wants zero credit use and provides one existing local creator image plus one
existing local product image. Read `references/reference-only-prompt-mode.md` completely before
execution.

This mode makes no Higgsfield calls at all: no generation, media upload/import, cost preflight,
status polling, assembly, caption, or publishing operation. Validate both local images, inspect the
product locally, then follow the selected child workflow through script/voice planning, structured
text boards, clip prompts, reference order, and QA. The two images are inputs and final references,
not newly generated outputs.

This mode is valid for `ugc-flow`, `ugc-try-on-flow`, `ugc-tutorial-flow`, and
`ugc-unboxing-flow`. It is invalid for `ugc-product-flow` and `ugc-saas-flow` for the same subject
model and real-page reasons documented by the reference file.

### `soul-only-prompt`

Use only when the user explicitly wants one creator image and text deliverables afterward. Read
`references/soul-only-prompt-mode.md` completely before execution.

This mode is valid for `ugc-flow`, `ugc-try-on-flow`, `ugc-tutorial-flow`, and
`ugc-unboxing-flow`. It is invalid for:

- `ugc-product-flow`, which has no identity-locked creator.
- `ugc-saas-flow`, whose defining output requires real page capture, compositing, and subtitles.

Within this mode, inspect the product locally and follow the selected workflow through product
analysis and creator-prompt writing. Call Higgsfield only inside the creator stage for
`generate_image(model: soul_2)` and the status/cost operations required for that one image. Do not
upload the product image to Soul; the creator image must remain product-free. Then return to local
reasoning, replace rendered boards with structured text boards, write the clip prompts, and stop.
Do not call GPT Image, Seedream, Seedance, stitching, transcription, subtitle, or publishing tools.
Immediately after the Soul job completes, download its hosted image to `higgs -ugc/模特图/` with
`scripts/save_creator_image.py` and keep the absolute result as `character_local_path`. Local
archival is mandatory in this mode and does not replace the hosted job id used for media chaining.

## Shared invariants

- Analyze the product once. Freeze `product_description`, `tier`, `category`, real mechanics,
  visible angle, scale, label state, approved claims, and `content_color` plus
  `content_color_evidence` for any paste / gel / cream / serum / oil / lotion / liquid / mist /
  foam contents. Container color and product / ingredient names are never content-color evidence.
  Missing or conflicting content-color evidence is a hard stop before creator generation, text-board
  writing, or clip-prompt writing; once confirmed, reuse the exact locked phrase and forbid hue /
  opacity changes in every downstream stage.
- Preserve user overrides. Do not replace explicit gender, age, ethnicity, hair, wardrobe,
  location, language, accent, Hook, or Setting choices with defaults.
- For a child workflow that requires creator gender, ask once when it is missing. Never infer a
  woman from examples or infer gender from the product category, audience, or visual stereotypes.
- Keep media order and `@ImageN` declarations identical whenever a prompt names references.
- Keep `Hard cut to.` markers in clip prompts only, never in board prompts.
- Never cross-load a sibling workflow's board or clip reference.
- Never invent product claims, unseen product sides, UI, usage mechanics, or package details.
- Distinguish internal planning from deliverables. Final prompts and scripts contain only content the
  target generator or viewer needs, not production commentary.

## Local registry

`scripts/local_workflow_registry.py` is the programmatic local equivalent of the read-only workflow
catalog and bundle access. It returns JSON, discovers the six child workflows from disk, excludes
hidden files, exposes the captured Hook/Setting presets, and rejects path traversal. It does not
execute a workflow or call Higgsfield.

## Prompt-mode finish gate

Before reporting either prompt mode complete, run:

```bash
python3 .agents/skills/higgsfield-ugc-workflows/scripts/check_mode_contracts.py
```

For `reference-only-prompt`, also require the reference-image start gate to have returned
`"valid": true`. For `soul-only-prompt`, require the Soul job to be complete and the downloaded
`character_local_path` to exist with a valid image signature. In both modes, verify every required
deliverable from the selected mode reference, the child-specific slot count, the exact hard-cut
count, and identical `@ImageN` declaration/attachment order before completion.
