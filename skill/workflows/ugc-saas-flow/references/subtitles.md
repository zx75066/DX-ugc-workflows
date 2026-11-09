# Subtitles — hook plate (top) + word-by-word bottom captions (always on)

Two layers, handed off at a **word boundary**: the hook line as a top plate (Metropolis-ExtraBold)
for exactly the hook segment, then 1-2-word bottom captions (Montserrat-ExtraBold) that blank out
in pauses. CAPS, white/black outline, no animation, nothing duplicated. Deliverable:
`output/final_captioned.mp4`.

Uses three bundle scripts (`transcribe_words.py`, `group_captions.py`, `make_captions.py`).
The sandbox is ephemeral (SKILL.md), so run the WHOLE block below as ONE `sandbox_exec` call
(`background: true`, poll ≤60s) with `load_workflow_files: { workflow: "ugc-saas-flow" }` —
prefixed by `curl -sL -o output/final.mp4 <hosted url>` if the composite ran in an earlier call,
and suffixed by the upload of `final_captioned.mp4` to a pre-created `media_upload` slot.
Caption TEXT comes from the authored `script.txt` (whisper is only the clock), so brand names are
always spelled as authored; the `[QA]` line flags any word not in the script — resolve before
burning. The plate's end = the start of the first whole body word (never a pause guess, never a
fixed 2s); caption groups falling under the plate are dropped.

## Pipeline (after `output/final.mp4` exists; script.txt + hook.txt saved in step 4)

```bash
# 1. word-level timings — from the FINISHED video (word_timestamps are mandatory; phrase-level drifts)
python3 scripts/transcribe_words.py output/final.mp4 -o output/words.json

# 2. split at the hook/body word boundary → hook plate segment + body words
python3 - <<'PY'
import json, re, difflib
norm = lambda t: re.sub(r"[^a-z0-9]", "", t.lower())
words = json.load(open("output/words.json"))                 # [[start,end,word],...]
hook  = open("output/hook.txt", encoding="utf-8").read().split()
a, b = [norm(w[2]) for w in words], [norm(t) for t in hook]
i_end = 0
for tag, i1, i2, j1, j2 in difflib.SequenceMatcher(a=a, b=b, autojunk=False).get_opcodes():
    if tag in ("equal", "replace"):
        i_end = max(i_end, i2)
first_body = i_end if 0 < i_end < len(words) else min(len(hook), len(words) - 1)
plate_end  = round(words[first_body][0], 2)                  # start of the first WHOLE body word
hook_start = round(words[0][0], 2)
json.dump({"video": "output/final.mp4",
           "segments": [{"start": hook_start, "end": plate_end,
                         "text": open("output/hook.txt").read().strip()}]},
          open("output/hook_seg.json", "w"))
json.dump([w for w in words if w[0] >= plate_end - 1e-6], open("output/body_words.json", "w"))
print(f"plate {hook_start}-{plate_end}s; body starts at {plate_end}s")
PY

# 3a. hook plate — Metropolis default, no --anim; re-anchor to TOP (~0.10·H)
python3 scripts/make_captions.py output/hook_seg.json -o output/hook.ass
python3 - <<'PY'
H = 1920; TOP = round(0.10 * H)
p = "output/hook.ass"; out = []
for ln in open(p):
    ln = ln.rstrip("\n")
    if ln.startswith("Style: Cap,"):
        parts = ln.split(","); parts[-5] = "8"; parts[-2] = str(TOP); ln = ",".join(parts)  # top-center
    out.append(ln)
open(p, "w").write("\n".join(out) + "\n")
PY

# 3b. bottom captions — script-aligned grouping, Montserrat 52; re-anchor to BOTTOM (~0.15·H)
python3 scripts/group_captions.py output/body_words.json -o output/segments.json \
  --video output/final.mp4 --script output/script.txt      # [QA] line → resolve before burn
python3 scripts/make_captions.py output/segments.json -o output/captions.ass --font "Montserrat" --size 52
python3 - <<'PY'
H = 1920; MARGIN_V = round(0.15 * H)
p = "output/captions.ass"; out = []
for ln in open(p):
    ln = ln.rstrip("\n")
    if ln.startswith("Style: Cap,"):
        parts = ln.split(","); parts[-5] = "2"; parts[-2] = str(MARGIN_V); ln = ",".join(parts)  # bottom
    out.append(ln)
open(p, "w").write("\n".join(out) + "\n")
PY

# 4. burn both layers — fonts are preinstalled system-wide (fontconfig), no fontsdir needed
ffmpeg -y -i output/final.mp4 -vf "ass=output/hook.ass,ass=output/captions.ass" \
  -c:a copy output/final_captioned.mp4
```

Grouping defaults live in `group_captions.py` (pair ≤11 chars, join gap <0.35s, 0.15s tail = the
pause-blanking, 0.20s min hold, de-overlap trim). The bottom ~15% band is the caption safe-zone —
the composite's inset never enters it.
