# Product intake — the one place the product gets normalized

Both input forms (a photo the user attached, or a product URL) must end in the SAME structured
result, so nothing downstream behaves differently per path:

- `product_media_id` — the reference image, ready for `medias[].value`
- `product_description` — the canonical staging text, reused VERBATIM everywhere after this
- `tier` — `luxury` | `premium` | `drugstore`, read off packaging cues and brand identity (never
  look up a price)
- `category` — skincare / cosmetics / fragrance / food / fitness / tech / cars / ...
- `content_color` — the locked visible color / opacity of any paste, gel, cream, serum, oil,
  lotion, liquid, mist, foam, or other dispensed contents; `not_applicable` for products with no
  such contents
- `content_color_evidence` — `attached-photo-visible` | `product-page-text` |
  `product-page-media` | `user-confirmed` | `not_applicable`

Decide `tier` and `category` HERE, once. No re-detection downstream.

## Path A — the user attached a product photo (preferred)

You can see the attachment, so read it directly and identify:

1. **Product category** — what it exactly is (perfume, face cream, lip balm, shampoo, body lotion,
   foundation, mascara, sunscreen, serum, hair oil, supplement capsules, protein powder, ...).
2. **Usage mechanic** — how it is physically used:
   - Perfume / spray bottle → **spray** (press nozzle, mist comes out)
   - Tube (cream, gel, toothpaste) → **squeeze + apply** with fingers
   - Pump bottle (serum, lotion, soap) → **press pump** → dispense onto fingers → apply
   - Lipstick / lip gloss → **swipe** directly on lips
   - Mascara → **brush** applied to lashes
   - Powder / compact → **brush or sponge** pressed on skin
   - Dropper / pipette serum → **drop** onto fingertips → press into skin
   - Jar (cream, mask) → **scoop** with fingers → apply
   - Capsule / pill / gummy → **swallow** or **chew**
   - Powder sachet / scoop → **mix** into liquid
3. **Opening mechanic** — uncap / unscrew / pull tab / flip top / press pump. It must be shown
   BEFORE any contents exit the container.
4. **Key visual details** — color, shape, material, label, distinctive features to preserve.
5. **Dispensed-content color gate** — if the product contains or dispenses a paste, gel, cream,
   serum, oil, lotion, liquid, mist, foam, or similar visible substance, inspect its actual color
   and opacity separately from the container. Record one exact, compact phrase such as `opaque
   white cream`, `colorless transparent gel`, `translucent pale amber serum`, or `pale pink
   lotion`, plus the evidence source. Container color, label color, flavor / ingredient names,
   product name, and brand palette are NOT evidence of content color.

Never default to "applies cream". Describe the exact mechanic the photo shows.

Then bring the file into Higgsfield: `media_upload_widget` for a local file (Apps-UI clients), or
`media_upload` → `curl PUT` → `media_confirm` when you hold the bytes. Keep the returned
`media_id` as `product_media_id`.

## Path B — only a URL

There is no page-extraction tool here; the sandbox does it. One `sandbox_exec` call fetches the
page and prints the fields you need:

```bash
curl -sL -A 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125 Safari/537.36' \
  '<PRODUCT_URL>' -o page.html
python3 - <<'PY'
import json, re, html
raw = open("page.html", encoding="utf-8", errors="ignore").read()
def metas(prop):
    pat = rf'<meta[^>]+(?:property|name)=["\']{prop}["\'][^>]+content=["\']([^"\']+)'
    return [html.unescape(m) for m in re.findall(pat, raw, re.I)]
blocks = []
for m in re.findall(r'<script[^>]+application/ld\+json[^>]*>(.*?)</script>', raw, re.S | re.I):
    try: blocks.append(json.loads(m))
    except Exception: pass
def walk(node):
    if isinstance(node, dict):
        if node.get("@type") in ("Product", ["Product"]): yield node
        for v in node.values(): yield from walk(v)
    elif isinstance(node, list):
        for v in node: yield from walk(v)
prod = next(walk(blocks), {})
title = (prod.get("name") or (metas("og:title") or [""])[0] or "").strip()
desc  = (prod.get("description") or (metas("og:description") or [""])[0] or "").strip()
brand = prod.get("brand", {});  brand = brand.get("name") if isinstance(brand, dict) else brand
imgs, seen = [], set()
for cand in ([prod.get("image")] if isinstance(prod.get("image"), str) else prod.get("image") or []) + metas("og:image"):
    if isinstance(cand, str) and cand.startswith("http") and cand not in seen:
        seen.add(cand); imgs.append(cand)
print(json.dumps({"title": title, "brand": brand, "description": desc[:1200],
                  "images": imgs[:6]}, ensure_ascii=False, indent=2))
PY
```

Then:

- Import the first usable image with `media_import_url` → `product_media_id`. Keep at most 4 more
  imports, and only when they are clearly the same SKU from another angle.
- You cannot visually rank the page's images (no vision tool reaches a remote URL here), so
  prefer the JSON-LD / `og:image` hero, and never pull an image from anywhere but the product page.
- The page text is thin, blocked, or image-free → ask the user ONCE for a photo of the product
  ("send a photo" / "try another link"). Never retry scraping on your own, never substitute a
  stock or generated product image.

## Dispensed-content color gate (mandatory)

Run this gate for every product that contains or dispenses a visible paste, gel, cream, serum, oil,
lotion, liquid, mist, foam, or similar substance, regardless of whether the planned shot is a
review, product-only demo, try-on accessory beat, tutorial, or unboxing follow-up.

Acceptable evidence, strongest first:

1. The attached product photo visibly shows the real dispensed contents.
2. The product page explicitly states the content color or shows the real contents outside the
   container in a clear, SKU-matched product image.
3. The user explicitly confirms the color and opacity.

Never infer content color from the container, packaging artwork, product / ingredient / flavor
name, scent, brand palette, or generic category defaults. `Orange`, `rose`, `milk`, `charcoal`, and
similar words do not prove orange, pink, white, black, or any other content color. Never silently
default gel or serum to `clear`, `colorless`, or `translucent`, and never default cream or lotion to
`white`.

If the product qualifies for this gate and no acceptable evidence exists, product intake is NOT
complete: ask once for a clear photo of the dispensed contents or an exact user confirmation of
both color and opacity, then stop before creator generation, boards, scripts that describe the
contents, or video generation. If sources conflict, present the conflict and stop for user
resolution; never pick one silently.

Once confirmed, freeze `content_color` and `content_color_evidence`. Copy the exact
`content_color` phrase verbatim into `product_description` and every downstream board, text board,
clip, video, image, edit, and QA instruction wherever the contents, smear, drop, stream, mist,
foam, residue, or applied product are visible. Add an explicit negative lock: no hue, opacity, or
color change across shots. Do not paraphrase, embellish, or re-detect it downstream.

## The staging contract (both paths)

Write ONE canonical `product_description` and reuse it verbatim in every downstream prompt:
shape, material, color, hand-relative size ("palm-sized, fits entirely in one hand, ~15 cm tall" —
never object comparisons, they drift), mechanism anatomy (which part is where, what moves, where
the output exits), the locked `content_color` phrase when the product passes the dispensed-content
color gate, absent features stated visually ("cordless, smooth body, no buttons"), the label
(below), plus one honest imperfection.

Label handling: with a real product PHOTO the label keeps its real text — the reference image plus
the Product Angle Lock carry it, so never write that it is illegible. Description-only mode (no
photo at all): describe it as "small label, turned slightly away, too small to read". In BOTH
modes, never stage other props carrying legible text or numbers. If the photo shows a big readable
logo, warn the user once (wordmarks render as gibberish or as a real competitor brand) and keep it
angled away only if they agree.

Claims: keep the description visual and mechanical. When the user supplies an explicit list of
approved product claims, use only those, each as its exact verbatim string — never paraphrase,
strengthen, combine, or derive a new one. With no such list, no numeric or comparative product
claim goes into speech, captions, or on-screen text.
