#!/usr/bin/env node
// capture_site.mjs — real mobile screenshots of a live site, run inside the E2B sandbox.
// Replaces the hermes `website_screenshot` tool: mobile full-page capture + dedicated
// section stills. Uses the sandbox template's global Playwright + its Chromium.
//
// Usage:
//   node capture_site.mjs <url> --out output/site_full.png                 # full page
//   node capture_site.mjs <url> --sections "Reviews,Pricing" --outdir output  # section stills
//
// Prints one JSON line per capture: {"kind":"full"|"section","label":...,"path":...}
// and exits non-zero if NOTHING could be captured.
import { createRequire } from "node:module";
import { execSync } from "node:child_process";
import { existsSync, mkdirSync } from "node:fs";
import path from "node:path";

// The template installs browsers at /ms-playwright, but its ENV vars don't reach
// sandbox command sessions — point Playwright there explicitly.
if (!process.env.PLAYWRIGHT_BROWSERS_PATH && existsSync("/ms-playwright")) {
  process.env.PLAYWRIGHT_BROWSERS_PATH = "/ms-playwright";
}

function loadPlaywright() {
  const roots = [process.env.NODE_PATH];
  try { roots.push(execSync("npm root -g", { encoding: "utf8" }).trim()); } catch {}
  for (const root of roots) {
    if (!root) continue;
    try { return createRequire(path.join(root, "x.js"))("playwright"); } catch {}
  }
  throw new Error("playwright not found — expected the sandbox template's global install");
}

const args = process.argv.slice(2);
const url = args.find((a) => !a.startsWith("--"));
const flag = (name, dflt) => {
  const i = args.indexOf(`--${name}`);
  return i >= 0 ? args[i + 1] : dflt;
};
if (!url) { console.error("usage: node capture_site.mjs <url> [--out file.png] [--sections 'A,B'] [--outdir dir]"); process.exit(2); }
const out = flag("out", "output/site_full.png");
const outdir = flag("outdir", "output");
const sections = (flag("sections", "") || "").split(",").map((s) => s.trim()).filter(Boolean);
// Keep Unicode letters (labels are often non-Latin); fall back to the index so
// two sections can never collapse into the same filename.
const slug = (s, i) => s.toLowerCase().replace(/[^\p{L}\p{N}]+/gu, "_").replace(/^_+|_+$/g, "") || `s${i + 1}`;

const { chromium, devices } = loadPlaywright();

// Best-effort cookie/consent dismissal — never fails the capture.
async function dismissOverlays(page) {
  const texts = /^(accept( all)?|agree|allow( all)?|got it|ok(ay)?|i (understand|agree|accept)|continue|reject all|no thanks)$/i;
  for (let round = 0; round < 2; round++) {
    for (const el of await page.locator("button, [role=button], a").all()) {
      try {
        const t = ((await el.textContent()) || "").trim();
        if (t.length <= 24 && texts.test(t) && (await el.isVisible())) { await el.click({ timeout: 1000 }); await page.waitForTimeout(400); break; }
      } catch {}
    }
  }
}

// Scroll through the page so lazy-loaded content renders, then return to top.
async function forceLazyLoad(page) {
  await page.evaluate(async () => {
    const step = window.innerHeight;
    for (let y = 0; y < document.body.scrollHeight; y += step) { window.scrollTo(0, y); await new Promise((r) => setTimeout(r, 120)); }
    window.scrollTo(0, 0);
  });
  await page.waitForTimeout(600);
}

const browser = await chromium.launch({ args: ["--no-sandbox", "--disable-dev-shm-usage"] });
try {
  const ctx = await browser.newContext({ ...devices["iPhone 13"] });
  const page = await ctx.newPage();
  await page.goto(url, { waitUntil: "domcontentloaded", timeout: 45_000 });
  await page.waitForLoadState("networkidle", { timeout: 15_000 }).catch(() => {});
  await dismissOverlays(page);
  await forceLazyLoad(page);

  let captured = 0;
  if (sections.length === 0) {
    mkdirSync(path.dirname(out), { recursive: true });
    await page.screenshot({ path: out, fullPage: true });
    console.log(JSON.stringify({ kind: "full", path: out }));
    captured++;
  } else {
    mkdirSync(outdir, { recursive: true });
    // Clickable controls (tabs/accordions) first, then plain headings/text (scroll only — clicking
    // a heading that is a link would navigate away). Skip matches that can't be scrolled to
    // (e.g. links hidden in a collapsed mobile nav) and try the next one.
    const scrollToSection = async (label) => {
      for (const g of [
        { sel: "[role=tab], summary, button, [role=button]", click: true },
        { sel: "h1, h2, h3, h4, strong", click: false },
      ]) {
        const matches = page.locator(g.sel, { hasText: label });
        const n = Math.min(await matches.count(), 5);
        for (let i = 0; i < n; i++) {
          const el = matches.nth(i);
          try {
            await el.scrollIntoViewIfNeeded({ timeout: 2500 });
            if (g.click) { await el.click({ timeout: 1200 }).catch(() => {}); await page.waitForTimeout(700); }
            // Centre the section in the viewport so surrounding site chrome stays in frame.
            await el.evaluate((node) => node.scrollIntoView({ block: "center" })).catch(() => {});
            await page.waitForTimeout(400);
            return true;
          } catch {}
        }
      }
      return false;
    };
    for (const [i, label] of sections.entries()) {
      if (await scrollToSection(label)) {
        const p = path.join(outdir, `section_${slug(label, i)}.png`);
        await page.screenshot({ path: p });                        // viewport shot, not full page
        console.log(JSON.stringify({ kind: "section", label, path: p }));
        captured++;
      } else {
        console.log(JSON.stringify({ kind: "section", label, error: "not reachable" }));
      }
    }
  }
  if (captured === 0) { console.error("no captures succeeded"); process.exit(1); }
} finally {
  await browser.close();
}
