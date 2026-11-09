# Monologue craft — what the creator actually says

Load this at the monologue step, before splitting text into board segments. Word density first:
<=10s ~ 12-20 words, 11-12s ~ 20-28, 13-15s ~ 28-35. Sum across clips for the total, then split
into N board segments (the 8 slot-level beats inside a board are the board/clip prompt's job, not
yours). Greetings and product introduction are allowed ONLY in board 1; later boards continue
mid-thought.

## Voice archetype (a default, not a question — state it for veto)

Every video gets ONE performance persona that colours HOW the creator talks. It is picked from the
tier of the already-resolved register and NEVER changes that register. Resolve the register FIRST
(NATURAL by default; HYPED or CALM only on an explicit signal), THEN pick a persona from its tier:

- **NATURAL tier (the default — use unless a signal says otherwise):** a warm, genuine, engaged
  creator — girl-next-door / easy-going relatable / dry-witty. Lively and real, ONE honest
  human-scale peak (a real grin, a delighted "oh"), NEVER squealing or screaming. Beauty, fashion,
  and most briefs get THIS by default — not It-Girl.
- **HYPED tier (only on a hyped signal):** 2000s It-Girl (stretched vowels, squeals on the reveal),
  Hype Beast (explosive bursts), Drama Queen.
- **CALM tier (only on a calm signal):** Deadpan Contrast (flat, one micro-crack at the peak), quiet
  Gossip Whisperer, Southern Sweetheart (soft warm).

HARD RULE: under the NATURAL default the persona sentence carries NO energy words — never `squeal`,
`scream`, `stretched vowels`, `explosive`, `screaming`. Energy comes from the REGISTER; the persona
adds only attitude, melody, and cadence, never volume. Write the chosen persona as ONE sentence and
carry it verbatim into the character prompt, every board prompt, and every clip prompt — restated
each time, or it drifts. Archetype and accent stack independently.

## Accent and quirk (opt-in)

If the brief names an identifiable origin for the creator, or asks for "weird" / "viral" character
energy, offer it inside the single intake question (accent consent + one quirk). Never add an accent
the user did not approve; the default is neutral English with no quirk. If opted in, write the
persona/quirk sentence once (identity + attitude, e.g. "a young Korean it-girl — English is her
second language and you hear it in every sentence") and restate it verbatim everywhere downstream.
Text-only accent enforcement lands roughly one render in three: if the user can drop a 5-10s voice
sample, attach it to the clip generation as an audio reference ("accent and vocal delivery reference
only — do not copy words, only the accent, melody, and timbre"). Offer that once; never block on it.

## Story mode is the default

ONE story spans the whole video: human stakes first (pain, embarrassment, money, a ruined plan), and
the product enters as a SUPPORTING ACTOR at 40-60% of total runtime, mapped onto the arc roles —
stakes live in the HOOK board, the single "but then" twist opens the mid arc, and the CTA rides
INSIDE the closer's resolution, never as an outro beat. The story must survive with the product
deleted. Plain review structure only on explicit request.

**Story-shape menu — pick ONE spine (it decides WHAT happens; the hook pattern decides how it
OPENS). Brainstorm at least 3 candidates, then choose; combine two only if it deepens the gap
without clutter:**

- S1 Accidental Find (mishap → forced pause → discovery)
- S2 After-First Loop (open on the result, then rewind)
- S3 Wrong Turn (bought for X, used for Y)
- S4 Witness (the creator was the skeptic, converts on camera — highest trust)
- S5 Confession (a secret surrendered)
- S6 Interrupted Storytime (a story about something else; the product interrupts, the story never
  quite finishes)
- S7 GRWM With Stakes (getting ready FOR a charged thing; the stakes carry it)
- S8 New-Place Mini-Vlog
- S9 Day-in-the-Life With a Twist
- S10 Caved-In Unboxing ("I caved", filmed first real reaction)
- S11 POV Frame (talks TO the viewer as a character)
- S12 Process Win (real work, one small win — native for B2B and small business)
- S13 Reply-to-Comment (answer an accusation, show the receipt)
- S14 Green-Screen Commentary (talk over on-screen evidence)
- S15 Rating Ritual (rate a set until the product lands last)
- S16 Street Ask (one stranger, one question)
- S17 Fail-First (try WITHOUT it, fail honestly, then with)
- S18 Silent Flex
- S19 ASMR (see the silent/ASMR mode below)

Every shape carries exactly ONE "but then" twist (the mid-arc peak) — no twist is a flat anecdote,
two will not fit in 15s. Realize the shape through the arc-role boards, never as a new field.

**Review / demo mode** (only on an explicit "just review it / plain demo" ask): give the body ONE
compact skeleton — PAS (Problem → Agitate → Solve), BAB (Before → After → Bridge),
Hook-Story-Offer, Us-vs-Them (against a lazy pricey default), or Demonstration ("watch this" — the
product does something visible in ~5s). Two or three spoken lines; even here the FIRST line carries
one human concrete.

## Hook-pattern menu — the HOOK board's opener

If the brief selects a Marketing Studio Hook, first load `marketing-studio-hooks.md` and use its
`hook_contract.internal_pattern`; its `spoken_bridge` controls the first line. This explicit
contract outranks writer's choice below. `Hook: None` uses a direct natural review opener.
`Hook: Auto` or an omitted Hook uses this native menu.

Pick ONE pattern per video, never blend. The pattern decides what KIND of moment the opener is; the
first-word constraint below still governs its words. H2/H5/H7 are text-led — the opener LINE
embodies them. H1/H3/H4 are visual-led — the line lands mid-event and the staging carries it.

- **H1 Impact Action** — frame one is something physical mid-peak (box mid-rip, product mid-catch,
  mid-stumble); the first word lands DURING the action.
- **H2 Mid-Sentence Confession** — opens on word four of a sentence, as if the viewer walked in on
  it; confessional volume.
- **H3 Pattern Interrupt** — a normal setting with one thing deeply wrong, delivered with total
  normalcy; the wrongness is visual, the voice ignores it.
- **H4 Freeze-Reaction** — frame one: the face already in full reaction, locked on something; a
  performed hold (<=0.7s), THEN the first line.
- **H5 Hostile Open** — the first line is a challenge or accusation aimed at the viewer; slight
  lean-in, finger already pointing.
- **H6 Quirk-First** — the quirk IS the literal first event, before any context. Only when a quirk
  was opted into.
- **H7 Result-First** — the outcome visibly on screen, unexplained; the first line refers backwards
  ("Gone in six days. Let me explain."). For multi-board videos the HOOK outcome is the HUMAN result
  (the after-face, the ruined plan resolved), never the product.
- **H8 Fake Stitch** (advanced, story mode only, needs a product image) — board 1 slot 1 is staged
  as repost-texture product-only footage (rougher light, slight compression, no face); ONE hard cut
  into slot 2 where the creator is mid-reaction with the product already in hand and the first line
  lands on the cut. The character enters one slot later than usual. Closer device: absurd family
  proof ("my mom bought FIVE. Five."). The slot-1 footage reads as a found repost clip, not the
  product's story entrance, so the 40-60% product entry still stands.

Write the chosen pattern into the HOOK board's prompt as ONE plain visual staging sentence — same
mechanism as the persona sentence, on board 1 only, never a pattern code.

For a selected Marketing Studio Hook, write the first line so it lands during or immediately after
the contracted event and performs the `spoken_bridge`. Do not narrate the event literally. The
opening event belongs in the board and clip prompts; the voice supplies the product pivot.

## Anti-slop pass on every line

- The first words are never `Okay wait / Okay so / OMG / Hey guys / So basically / Stop scrolling /
  You NEED this / Story time`.
- Banned anywhere: "literally", "obsessed", "game-changer", "holy grail", "changed my life", "hits
  different", and corporate words (elevate / seamless / effortless).
- Friction openers beat enthusiasm ("I almost returned this.").
- Every claim carries one concrete — a number, a time, a named comparison; praise without a concrete
  gets cut. When the user supplied an approved-claims list, use only those exact strings and never
  invent a concrete to satisfy this rule.
- At most ONE peak reaction per clip in the monologue (the clip prompt may stage up to two — the arc
  peak plus an optional product-motivated closer beat).
- Echoes and repeats count toward the word budget but carry no information — cut them first.

**First-word constraint (positional, every board's segment):** the literal FIRST WORD must be hook
content — never `OK / Okay / Okay so / Alright / Alright so / So / Yeah so / Right so / Um / Well /
Like / Wait / Wait what / Hold on`. Those read as recording warmup. They are fine mid-sentence
later; the constraint is the first word only.

**Performed dialogue** (emotion lives IN the words — the video model under-renders flat prose):
vowel-stretch on the peak word ("it's SO good"), 1-2 CAPS volume spikes per line max, one broken
sentence at the peak ("it's— okay wait. LOOK."), a whisper-to-spike swing, and a flat → spike →
settle arc across the clip. Under the NATURAL default the peak stays human-scale (a real gasp, a
breaking grin), never staged screaming. NEVER write engineered or dramatic pauses — they bloat the
line and break the render.

## Optional registers

- **Quiet process-led** (only on an explicit "quiet routine" / "aesthetic process video" ask): the
  monologue drops to soft half-thoughts, <=20 words per 15s clip — the density floor is waived,
  ceilings still bind. Sound carries the clip. The product enters as one honest routine step.
  Skincare and beauty routines start bare-faced. Tell the boards and clips the register is quiet
  process-led with ONE plain staging sentence.
- **Silent / ASMR** (shapes S18 / S19; best for products with satisfying physical feedback): spoken
  budget drops to ZERO (S18) or <=15 whispered words (S19). The SFX line becomes the script — each
  trigger named and timed; micro-movement density doubles; framing goes macro-close for S19. The
  absence of a synthetic voice is itself the anti-slop move. The CTA lives only in the post package.
  For S19 restate "no on-screen words of any kind" — the model loves to bake karaoke subtitles into
  ASMR.
- **Music is opt-in.** When the user asks for music, pass the request into the clip prompts; they
  carry the music line. Never invent music uninvited.

## Series mode (opt-in — a content calendar, not one long video)

Triggers only on an explicit ask for a SERIES / "a week of content" / "N posts from one creator".
Different from a >15s multi-board video (that is ONE stitched video): a series is N SEPARATE posts,
each its own full run, sharing one creator and a week arc. It costs N times the renders — always
output the arc TABLE first, get a nod, then generate post by post.

- Carry forward VERBATIM across all posts: the persona sentence, voice archetype, accent delivery,
  quirk, and wardrobe anchors. Reuse the SAME `character_media_id` — no regeneration.
- 7-post skeleton (adapt the count): 1 = S10 Caved-In Unboxing · 2 = S1/S8 (creator earns attention,
  product barely mentioned) · 3 = S7 GRWM With Stakes (first soft sell) · 4 = S4 Witness (the
  conversion post) · 5 = S3 Wrong Turn (rewatch fuel) · 6 = S2 After-First Loop (proof, hardest CTA)
  · 7 = S5 Confession / quirk payoff (community post).
- Product-pressure curve: light (1-2) → selling (3-6) → community (7). A series that sells in every
  post burns the account.
- Quirk escalation: identical in posts 1-4, NOTICED by the creator in post 5, paid off or subverted
  in post 7 — that anticipation is the follow mechanic.
