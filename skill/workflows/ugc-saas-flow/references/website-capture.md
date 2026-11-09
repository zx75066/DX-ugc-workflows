# Website capture — real mobile stills from the URL (sandbox headless Chromium)

Produce `output/site_full.png` (one mobile full-page capture → the section map) plus dedicated
stills of the USEFUL sections (product, reviews, specs, pricing) that become the overlay cards.
Real pixels only — never generated, never upscaled/restyled; don't size or crop here (geometry is
Step D of `screen-broll-and-composite.md`). One product = one site.

The sandbox is ephemeral (SKILL.md): pre-create `media_upload` slots for `site_full.png` and the
expected section stills first, then capture AND upload in ONE `sandbox_exec` call with
`load_workflow_files: { workflow: "ugc-saas-flow" }`:

```bash
node scripts/capture_site.mjs <url> --out output/site_full.png     # mobile full-page (overlays auto-dismissed)
node scripts/capture_site.mjs <url> --sections "Reviews,Pricing,Specifications,Dashboard,Product gallery" --outdir output
for f in output/*.png; do curl -X PUT --upload-file "$f" "<upload_url for $f>"; done
```

(`media_confirm` after the call; slots for sections that weren't found just go unused.)

The sections run clicks matching tabs/headings, centres each in the viewport (site chrome stays in
frame), and saves `output/section_<label>.png` — one JSON line per capture; unfound sections print
an error line and are skipped (crop that card from a `site_full.png` band instead, or drop it).
**Capture generously (~6-10 stills)** — card count = number of distinct useful stills; break broad
sections into individual feature screens, a couple of review shots, pricing + a plan, product
views. Skip filler (nav, footer, logo strips).

**Verify FIRST:** VIEW `output/site_full.png` (upload via `media_upload` → `curl PUT` →
`media_confirm` for an openable URL). A bot wall (CAPTCHA / "verify you are human" / Cloudflare /
access denied / blank) is NOT the site — build no cards from it.

**Section map:** from the full capture (optionally `curl` the HTML for heading order), record
sections top→bottom with height fractions and key/filler flags, e.g.
`{label:"hero", y:0.00-0.18, key:true} … {label:"footer", y:0.94-1.00, key:false}`. The map drives
monologue order and card order; filler never becomes a card.

## Failure = ask for screenshots (hard gate, first try)

Any first-try failure — error / bot wall / login / unreachable / **<3 usable cards** — ask the
user immediately, ONE question ("Couldn't capture the site"): **"I'll send screenshots"** (paste
the key screens: product, reviews, price, specs) / **"Try to get through"** (warn only that it
takes longer). No self-started retries, no web-searching for images, never proceed with <3 cards,
never fabricate UI. User screenshots replace the capture: upload them
(`media_upload_and_confirm` / widget) and use as the section stills as-is — desktop frames are
fine (contain-fit handles them; never cover-crop, no band-stitch).
