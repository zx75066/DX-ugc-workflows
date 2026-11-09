---
name: ugc-saas-flow
description: |
  UGC-style video for any website / web app / store / product page at a URL: a talking-head creator on camera the whole time while REAL captured screenshots of the site pop in as overlay cards (never a screen recording, never AI-generated UI). Works for a physical product too when it has a store/product URL — shown via its PAGE, in hand only in the closer.
  Triggers: "SaaS UGC" / "UGC SaaS", "UGC ad from this link/URL", "video about my site / app / store / product page", "site tour". A URL whose PAGE should appear on screen routes here; when the URL is only where the product lives and the page is never shown, use the product-side flows (ugc-flow / ugc-product-flow / ugc-unboxing-flow / ugc-try-on-flow / ugc-tutorial-flow). Naming this flow always selects it.
  NOT for: a product with NO URL shown only in-hand; building/editing a website; AI-generating a UI.
---

# ugc-saas-flow

One continuous **talking-head creator** (9:16, US accent, high-energy UGC pace) narrates
hook → the site solves it → result. The site appears ONLY as **real captured screenshots**
overlaid as large insets over the face (~1.2–1.5s each); the creator's voice runs under everything.
Deliverable: `output/final_captioned.mp4`, uploaded and delivered as a hosted URL.

**Hard rules (apply everywhere):**
- The screen is ALWAYS real captured pixels. Never AI-generate UI, never animate a screenshot,
  never ask the user to record their screen.
- Product appears ONLY in the closer (in hand if physical, acting on a blank/turned-away phone if
  SaaS); the body is product-free.
- English speech, American accent (never British), unless the user explicitly asks otherwise.
- Subtitles always on: hook plate (top, Metropolis) + word-by-word bottom captions (Montserrat).
- One creator identity: the same `character_media_id` seeds every clip; never regenerate mid-run.
- Capture fails on the FIRST try (error / bot wall / login / <3 usable cards) → ask the user for
  screenshots immediately (one question; options "I'll send screenshots" / "Try to get through").
  Never retry on your own, never pull images from anywhere but the page.

## Sandbox script execution

All shell/media work (capture, ffmpeg, python) runs in the E2B sandbox via `sandbox_exec` — never
locally. The template preinstalls ffmpeg, Playwright+Chromium, faster-whisper (model pre-baked),
Pillow, and the caption fonts.

**The sandbox is EPHEMERAL** — discarded seconds after each call returns; files do NOT survive
between calls. Every `sandbox_exec` call must therefore be self-contained:
- Pass `load_workflow_files: { workflow: "ugc-saas-flow" }` on every call that runs a bundle
  script — it writes `scripts/*` into the sandbox server-side before the command (never read
  script contents with `get_workflow_bundle_file`, never paste them into commands).
- Bring inputs in and send outputs out INSIDE the same command: pre-create slots with
  `media_upload` BEFORE the call, then in the command `curl -sL -o` the inputs, do the work, and
  `curl -X PUT --upload-file <file> <upload_url>` the outputs; `media_confirm` after.
- Long renders (composite, transcription): `background: true`, poll the log at least every 60s —
  each poll keeps the sandbox alive; the command itself must end by uploading its outputs.

## Pipeline

**1. Parse.** Extract the site URL (required), duration, creator gender/overrides. Classify the
site (`type`: saas/ecommerce/…, `audience`, `surface`) — steers look and tone only. No URL and a
pure product-in-hand ask → out of scope; say so and stop. Duration → N clips:

| Total D | N | Clip durations |
|---|---|---|
| 4-15 | 1 | D |
| 16-19 | 2 | balance to ≥4s each |
| 20-30 | 2 | 15, D-15 |
| 31-45 | 3 | 15, 15, D-30 |
| 46-60 | 4 | 15, 15, 15, D-45 |
| >60 | ceil(D/15) | 15 each, last ≥4s |

**1.1 Persona source.** User attached a person photo → that IS the creator: upload it
(`media_upload_and_confirm` / widget), capture `(character_media_id, character_url)`, skip step 3.

**2. Capture the site** — `references/website-capture.md`. Full-page mobile capture via
`scripts/capture_site.mjs`, then section stills (`--sections`) of the USEFUL parts (product,
reviews, specs, pricing) — target ~6-10 stills; each becomes one overlay card. Build a section map
(top→bottom bands). Minimum 3 usable cards or fall back to asking.

**3. Generate the creator** (skip if provided) — `references/saas-ugc-character.md` layered over
`references/soul-v2-ugc-character.md`. `generate_image` model `soul_2`, `3:4`, `2k`,
`enhance_prompt: false`; poll with `job_status`; `(character_media_id, character_url)` =
`(job_id, result.url)`.

**4. Write the monologue** — `references/saas-monologue.md`. Hook (≤8 words, hook token) → body
naming the sections in card order (first body beat names the site → hero card) → closer with the
product action. ~2.7–3.0 words/sec, varied rhythm. Save verbatim to `output/script.txt`, hook to
`output/hook.txt`, plus ordered `{section_label, words}` beats.

**5. Generate the talking-head clips** — `references/saas-clip-prompt.md`. ONE continuous shot per
clip, no boards/cuts. `generate_video` model `seedance_2_0`, `9:16`, `1080p`,
`medias=[character_media_id]` for every clip; the physical-product closer adds the product image
(from the product page only — `media_import_url` → second `medias[].value`). Submit all N in one
parallel batch. Closer returns `nsfw` → retry the closer only, without product media, neutral
gesture, same character. Run the pre-submit checklist in the reference. Frozen-frame QA each clip
(one creator, ≤2 hands, face matches, no baked text).

**6. Composite** — `references/screen-broll-and-composite.md`. Concat clips (stream-copy) →
`output/creator_full.mp4`; build card images; anchor each card at its narrated word-time
(`t = T × cum_words/total_words`), ~1.2–1.5s each with ~0.3–0.5s gaps, none during hook/closer;
overlay contain-fit into `0.78W × ≤0.60H`, centred slightly up; audio copied →
`output/final.mp4`.

**7. Subtitles** — `references/subtitles.md` (always on). Whisper word timestamps → hook plate +
script-aligned bottom captions → ffmpeg burn → `output/final_captioned.mp4`.

**8. Deliver.** Upload from the sandbox: `media_upload` → returned `curl PUT` → `media_confirm`;
show the hosted URL + duration; hide job ids. Then ask once: "Publish to TikTok?" (Yes / No). On
yes: `tiktok_accounts` → (`tiktok_connect` if needed, link, wait for OAuth) → `tiktok_publish_form`
→ after explicit form submit only, `publish_tiktok` with the form's args → `tiktok_publish_status`.

## Asking the user

Everything technical is pinned (models, 9:16 1080p, audio on, captions on, composite style, N from
duration) — NEVER ask about those. Ask (one bundled question) only for: missing URL; missing
duration (offer 10/15/30/45s); capture failure (see hard rules); the TikTok publish question.

## References

Load via `get_workflow_bundle_file({ workflow: "ugc-saas-flow", path })`:
- `references/website-capture.md` — capture commands + fallback gate
- `references/saas-monologue.md` — script arc, hook rules, density
- `references/saas-ugc-character.md` — framing / setting / voice overrides
- `references/soul-v2-ugc-character.md` — creator base prompt (identity, anti-slop, safety)
- `references/saas-clip-prompt.md` — Seedance clip prompt + hard bans
- `references/screen-broll-and-composite.md` — card build + overlay recipe
- `references/subtitles.md` — caption pipeline (uses `scripts/`)
