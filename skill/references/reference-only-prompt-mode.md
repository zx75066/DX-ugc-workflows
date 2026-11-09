# Reference-only prompt mode

Use this zero-credit adaptation only after selecting one creator-based product workflow. It accepts
two existing local images and converts the paid board/video stages into text deliverables.

## Hard call boundary

Make no Higgsfield or other remote generation calls in this mode. Do not call generation, media
upload/import, cost, status, model discovery, assembly, transcription, caption, or publishing tools.
Do not use a free allowance: zero-credit means zero generation and zero remote media operations.

The only media inputs are:

- `character_local_path`: one existing local creator identity image.
- `product_source_path`: one existing local product appearance image.

Validate both paths locally before planning:

1. Resolve each to an absolute path inside an authorized workspace root.
2. Confirm it is a regular, non-empty file with a valid PNG, JPEG, or WebP signature.
3. Inspect both images locally. Freeze the creator's visible identity/wardrobe/environment and the
   product's visible design, angle, scale, mechanism, label state, and honest imperfections.
4. Never replace, edit, copy, upload, or regenerate either image. The original local files are the
   final references.

Run the deterministic start gate before inspecting the images:

```bash
python3 .agents/skills/higgsfield-ugc-workflows/scripts/validate_reference_images.py \
  --workspace-root '<authorized-workspace-root>' \
  --creator '<character_local_path>' \
  --product '<product_source_path>'
```

Continue only when it returns `"valid": true`.

If either image is missing, unreadable, invalid, or not actually the named subject, stop and ask for
that image. Never fall back to `soul-only-prompt` or `full-render` without explicit user permission.

## Product gate

Run the selected child workflow's product intake locally. Freeze `product_description`, `tier`,
`category`, mechanics, visible angle, scale, label state, approved claims, `content_color`, and
`content_color_evidence` once.

For paste, gel, cream, serum, oil, lotion, liquid, mist, foam, or similar visible contents, the real
dispensed color and opacity must be visible in `product_source_path`, visible in user-supplied local
supporting evidence, or explicitly confirmed by the user. Packaging color and product/ingredient
names are never evidence. Missing or conflicting evidence is a hard stop before writing any board
or clip that shows the contents.

Supporting evidence may establish facts but never becomes a video reference unless the user
explicitly changes the two-image contract.

## Adapt the selected child workflow

1. Parse the brief and freeze one child `workflow_id`.
2. Validate and inspect the two local images; do not run the child workflow's creator-generation or
   remote product-import steps.
3. Write the monologue or voice plan at the child workflow's original duration density.
4. Replace each rendered board with a structured text board containing the original slot count,
   arc role, exact time span, POV, distance, location, subject action, product state, both-hand
   allocation, audio mode, spoken words, and continuity constraints.
5. Apply every child-specific rule: Hook slots for talking-head, one-way wardrobe and macros for
   try-on, global real steps for tutorial, or sealed-box/reveal state for unboxing.
6. Write one final clip prompt per text board. Translate every slot into motion and exact hard-cut
   timing. Preserve the script verbatim and repeat creator/product anchors because no rendered board
   supplies them.
7. Deliver the two reference paths, upload order, generator assumptions, and post-generation QA.
8. Stop. Do not claim that a board image, edited image, video, subtitle, or hosted URL exists.

Use the selected child's own references only. Never load a sibling workflow's board or clip rules.

## Reference order

Keep the prompt declarations and actual attachment order identical. Preserve an explicit order from
the user. When no order is specified, default to:

```text
@Image1 = creator identity reference
@Image2 = product appearance reference
```

The final reference section must contain both absolute local paths in attachment order. If the user
explicitly requests product first, use this order everywhere instead:

```text
@Image1 = product appearance reference: <absolute product_source_path>
@Image2 = creator identity reference: <absolute character_local_path>
```

For unboxing, use a generic sealed brown delivery box when no real package reference exists. Do not
add a third reference under the two-image contract.

Eight segments have seven between-shot `Hard cut to.` boundaries; four segments have three. Label
every shot and never append a transition after the last shot.

## Required deliverables

- selected `workflow_id` and execution mode `reference-only-prompt`
- explicit statement that remote/MCP call count and credit use are both zero
- validated creator and product absolute local paths
- frozen creator continuity description
- frozen product analysis and canonical product description, including `content_color` and evidence
- full spoken script or voice plan
- structured text boards with exact time spans
- final video-generation prompt for every clip
- two-image attachment order and generator assumptions
- post-generation QA checklist and multi-clip hard-cut order when applicable
- explicit list of skipped generation and publishing stages

## Unsupported cases

- Reject `ugc-product-flow`: it has no identity-locked creator, so forcing a creator image violates
  its product-only subject model. Use that workflow's own prompt-only adaptation with product input
  if one is added separately.
- Reject `ugc-saas-flow`: real page capture, compositing, and mandatory captions are defining output
  stages and cannot be represented by only creator and product images.
