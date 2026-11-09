# Marketing Studio Hook presets

Use this file only for `ugc-flow` talking-head review videos. A selected Hook is an opening
creative contract, not text appended to the end of a prompt. It controls the first spoken line,
Board 1 opening slots, and Clip 1 opening cuts.

## Selection contract

Accept any of these brief fields:

- `Hook: Auto` or omitted: use the native H1-H8 menu in `monologue-craft.md`.
- `Hook: None`: use a direct natural product-review opener without a stunt.
- `Hook: <preset name>`: resolve one exact preset below, case-insensitively.
- `Hook: Custom — <description>`: normalize the description into the same contract.

Resolve the choice once during Parse and carry this object forward verbatim:

```json
{
  "name": "<preset, Custom, Auto, or None>",
  "type": "subtle | stunt | custom | native | none",
  "opening_event": "<one concrete visible event>",
  "spoken_bridge": "<how the first line pivots into the review without narrating the event>",
  "slot_budget": 0,
  "internal_pattern": "H1 | H2 | H3 | H4 | H5 | H7 | native",
  "risk": "low | medium | high"
}
```

`slot_budget` is 0 for None, 1 for a one-beat opener, and 2 for an event plus recovery. Never let
a Hook consume more than Board 1 slots 1-2 / Clip 1 cuts 1-2. By slot/cut 3, return to the selected
UGC story arc.

## Presets

### Product Hit

- Type: stunt
- Internal pattern: H1
- Slot budget: 2
- Risk: medium
- Opening event: A harmless lightweight non-product object flies into frame and lightly bumps the
  creator; the creator catches or brushes it aside, reacts once, then raises the real product.
- Spoken bridge: The first word lands during impact; the line immediately pivots to the product.
- Guardrail: Never throw, strike, drop, duplicate, or deform the hero product.

### Spicy

- Type: subtle
- Internal pattern: H4
- Slot budget: 2
- Risk: low
- Opening event: Start on an extreme beauty-detail close-up, tilt to the finished look, then pull
  back into an intimate selfie frame with one brief silent hold.
- Spoken bridge: The first line lands after the hold and names one concrete product result.
- Guardrail: Use only when the product has a credible beauty, fashion, grooming, or appearance
  result. Otherwise adapt the close-up to the product's real result detail.

### Interview

- Type: subtle
- Internal pattern: H2
- Slot budget: 2
- Risk: high
- Opening event: An off-camera interviewer asks one odd product-relevant question; the creator gives
  a briefly confused look, notices the product, and pivots into the review.
- Spoken bridge: Start mid-answer, not with a greeting or a repeated question.
- Guardrail: Keep the interviewer off camera and silent after cut 1. Do not introduce a second
  visible identity.

### Random Object Mic

- Type: stunt
- Internal pattern: H3
- Slot budget: 2
- Risk: medium
- Opening event: A harmless absurd non-product prop drops gently into the creator's free hand; they
  use it as a mock microphone for one beat, then set it down and show the real product.
- Spoken bridge: Deliver the first product claim into the prop with total seriousness.
- Guardrail: The prop must not resemble, replace, cover, or duplicate the hero product.

### Product Crash

- Type: subtle
- Internal pattern: H3
- Slot budget: 2
- Risk: high
- Opening event: A generic shipping box or unrelated prop falls in the background and makes a mess;
  a hard cut restores the clean scene, where the creator calmly holds the intact hero product.
- Spoken bridge: Ignore the crash verbally and begin with one concrete product claim after the cut.
- Guardrail: Never destroy, drop, clone, transform, or restore the referenced hero product. This
  stability adaptation intentionally replaces the original preset's destroyed-product event.

### Blizzard

- Type: stunt
- Internal pattern: H3
- Slot budget: 2
- Risk: high
- Opening event: A brief impossible gust of snow crosses an otherwise normal room; the creator
  shields their face while the product remains fixed and intact, then the room returns to normal.
- Spoken bridge: The first claim lands as the gust ends; do not explain the weather.
- Guardrail: Preserve face, clothing, room layout, product state, label, and scale across the cut.

### Camera Bump

- Type: subtle
- Internal pattern: H1
- Slot budget: 2
- Risk: low
- Opening event: The handheld camera makes a small accidental bump and quick correction; the creator
  gives one natural reaction, recenters, and reveals the product.
- Spoken bridge: Open mid-recovery with a concrete product observation.
- Guardrail: No injury, fall, collision with the product, or prolonged camera shake.

### Product Dodge

- Type: stunt
- Internal pattern: H1
- Slot budget: 2
- Risk: medium
- Opening event: A harmless generic prop crosses frame; the creator ducks once, rises holding the
  already-present intact product, and begins the review.
- Spoken bridge: The first word lands while rising into frame.
- Guardrail: The flying object is never the hero product. Do not make the product appear from
  nowhere; stage it on the counter or in the creator's free hand before the dodge.

### Epic Fail

- Type: subtle
- Internal pattern: H1
- Slot budget: 2
- Risk: high
- Opening event: The creator attempts a small safe flourish, fumbles the non-product prop, catches
  balance, and immediately presents the intact product with deadpan confidence.
- Spoken bridge: Start mid-recovery and pivot directly to one product concrete.
- Guardrail: No backflip, dangerous fall, impact, injury, product drop, or product damage.

## Integration rules

1. The selected Hook overrides writer's choice inside the native H1-H8 menu, but it never changes
   the workflow route, duration, board count, models, product intake, creator identity, or QA.
2. Write the `spoken_bridge` into the first monologue segment. Do not describe the visual event
   word-for-word; image and video prompts carry the event.
3. Write `opening_event` into Board 1 slots 1..`slot_budget` using the named internal pattern.
4. Repeat the same event and recovery in Clip 1 cuts 1..`slot_budget`, with exact timing and
   `Hard cut to.` boundaries.
5. Never re-run the Hook on later boards, clips, variants, or the closer.
6. User-supplied explicit shot directions win over a preset. Preserve the preset's function and
   adapt its staging to those directions.
7. Product fidelity, exactly-one-hero-product, two-hand limits, identity lock, safety, and the
   route's story arc outrank the Hook. Adapt or reject a conflicting custom Hook.
8. `Hook: None` is different from the optional post-render Hook text plate. The latter is handled
   only by `subtitles.md`.

## Custom Hook normalization

Reduce a custom description to one event, one reaction, one review pivot, and at most two opening
slots. Reject or safely adapt requests that require dangerous stunts, injury, product destruction,
extra limbs, product duplication, a second persistent creator, false claims, or more than two
opening beats. Assign the closest H1-H8 internal pattern and state the adapted contract before
writing downstream prompts.
