# Composite — screenshot insets over the live creator (ffmpeg only, no generation)

The sandbox is ephemeral (SKILL.md): run steps A–D as ONE self-contained `sandbox_exec` call
(`background: true`, poll ≤60s) — download the clips and card stills from their hosted URLs at the
top of the command, and upload `output/final.mp4` to a pre-created `media_upload` slot at the end
(or chain the subtitles pipeline in the same command and upload `final_captioned.mp4` instead).

Target 1080×1920 (9:16), clip fps (ffprobe), yuv420p, **audio copied, video encoded exactly
once** (this overlay pass). Geometry is in FRACTIONS of the frame — recompute px for other sizes.
Inputs: `output/clip_<K>.mp4`, `output/section_<label>.png`, the ordered `{section_label, words}`
plan + hook/closer word counts.

## A — base spine

```bash
: > output/clips.txt; for K in $(seq 1 N); do echo "file 'clip_${K}.mp4'" >> output/clips.txt; done
ffmpeg -f concat -safe 0 -i output/clips.txt -c copy output/creator_full.mp4
T=$(ffprobe -v error -show_entries format=duration -of default=nw=1:nk=1 output/creator_full.mp4)
FPS=$(ffprobe -v error -select_streams v:0 -show_entries stream=r_frame_rate -of default=nw=1:nk=1 output/clip_1.mp4)
```

N never matters downstream — all window math runs over the absolute timeline `T`.

## B — card images (no pad, no backing — they float over the live creator)

Every card must carry a **site marker** (logo/navbar/price+CTA/reviews UI); if a crop loses it,
widen the band. Bands differ per site — measure per run: slice `site_full.png` into ~5–12
horizontal strips, VIEW them (upload via `media_upload` → `curl PUT` → `media_confirm` for a URL
you can open), record each element's height fractions.

- **Hero card** (first card, must read as the site): stitch the meaningful top bands
  (logo+navbar, product, name+price), DROPPING empty gaps:
  ```bash
  ffmpeg -i output/site_full.png -vf "crop=iw:ih*(Y1-Y0):0:ih*Y0" band_X.png   # per band
  ffmpeg -i band_logo.png -i band_product.png -i band_price.png \
    -filter_complex "[0][1][2]vstack=inputs=3" output/card_hero.png
  ```
  If the stitch gets so tall the box-fit makes text unreadable, drop one low-value band.
- **Other cards**: use each section still directly.
- **User-provided screenshots** (fallback): use as-is, no stitch, no crop — the Step-D contain-fit
  handles a wide desktop frame (it just lands shorter).

## C — timeline (variant B anchor, no ASR)

`t(cum) = T × cum_words / total_words` over the continuous voice.

- Hook → NO inset; `t_hook = min(2.0, t(hook_words))`.
- Body → every still is its own inset, anchored at its beat: `s_k = t(cum words before beat)`,
  `e_k = s_k + 1.4` (~1.2–1.5s), clamp `s_k ≥ t_hook`, keep a ~0.3–0.5s clean-face gap (push later
  anchors back if they'd collide). First inset is ALWAYS the hero, at the site-naming beat.
- Closer → NO inset; `t_closer = t(total − closer_words)`; drop windows that spill past it.
- If drift is visibly off (Seedance pacing), optionally transcribe `creator_full.mp4` with
  `scripts/transcribe_words.py` and recompute `s_k` from real word times.

## D — overlay (one encode)

```bash
WBOX=$((1080*78/100)); HBOX=$((1920*60/100)); UP=$((1920*4/100))
ffmpeg -i output/creator_full.mp4 -i output/card_hero.png -i output/card_reviews.png … \
  -filter_complex "\
    [1:v]scale=${WBOX}:${HBOX}:force_original_aspect_ratio=decrease[c1]; …\
    [0:v][c1]overlay=(W-w)/2:(H-h)/2-${UP}:enable='between(t,S1,E1)'[v1]; …" \
  -map "[vN]" -map 0:a -c:v libx264 -pix_fmt yuv420p -profile:v high -r "$FPS" -c:a copy output/final.mp4
```

One scaled input + one time-gated `overlay` per card with the real `[s_k, e_k]`. The contain-fit
box (`0.78W × ≤0.60H`) enforces the height ceiling and normalises card sizes; centred + shifted up
`0.04H`, the inset bottom lands ≈0.80H — clear of the bottom ~15% caption band (raise/shrink if a
card ever reaches it). No blur, no backing — the creator stays visible around the edges.
`output/final.mp4` is this step's deliverable.
