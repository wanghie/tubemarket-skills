---
name: appstore-screenshot-builder
description: Build an iOS App Store screenshot set that meets Apple's pixel spec and passes review — competitor research, a 6-frame storyboard, captions, pixel-exact PNG render with local Playwright, review-rule QC. Runs in Claude Code or ChatGPT plus free local tools, no API key. Use for a new store listing or when Apple rejected the old screenshots. Triggers on "make App Store screenshots", "app store screenshots", "store images", "screenshots got rejected".
---

# appstore-screenshot-builder — App Store screenshots that pass review, look good, and sell

Goal: a set of 5–7 iOS App Store screenshots that are **pixel-exact to Apple's requirement**, **break no review rule**, and **convert well** (the first 2 images decide most installs).

Default build: **HTML + Playwright → PNG**, all local and free. Switch to Figma only when the user wants to hand-edit (see Appendix C).

---

## 5 unbreakable rules

Breaking 1 of the 5 = screenshots rejected or the app rejected. Check before anything else.

1. **Only REAL app screens.** No imagined UI, no features that do not exist yet. No real screenshots → stop and ask for them, never invent. (Guidelines 2.3.1, 2.3.3)
2. **No splash screen, login screen or logo art as the first image.** Images must show the app in use. (2.3.3)
3. **No prices, promotions, "Free", "50% off", "Download now" in the images.** (2.3.7)
4. **No Android device names/icons/frames, Google Play, or other platforms.** (2.3.10)
5. **No placeholder content, "Lorem ipsum", "Beta", or real personal data.** Data in images must be a fictional account that looks real. (2.1, 2.2)

---

## Step 0 — Gather inputs (ask briefly, at most one round)

All 5 are needed; ask for what is missing:

| Input | Notes |
|---|---|
| App name + one sentence on what it does for whom | Used for captions |
| 6–10 REAL screenshots | PNG from the Simulator or a device, at native resolution |
| Brand colour + font | If missing, take them from the app icon |
| 3 competitors in the same niche | App name or App Store link |
| Screenshot language | e.g. English / Vietnamese / both |

Clean screenshots from the Simulator (pixel-exact, tidy status bar):

```bash
xcrun simctl io booted screenshot ./shot-01.png
# Make the status bar clean and consistent:
xcrun simctl status_bar booted override --time "9:41" --batteryState charged --batteryLevel 100 --cellularBars 4 --wifiBars 3
```

---

## Step 1 — Competitor research (required, never skip)

Open the App Store pages of 3 competitors and extract exactly 4 things per app:

1. Does their image 1 state an **outcome**, or just show off a **feature**?
2. How many words is the caption, above or below the device?
3. Device frame or not? Solid background, gradient, or photo?
4. Which images repeat the same idea — that is where you win.

Put it in a 3-column table, then **choose a different direction**, do not copy. If all 3 use dark purple gradients → go light or solid colour.

---

## Step 2 — Lock a 6-frame storyboard

One idea per frame, no cramming. Frames 1–2 get the most care because the App Store page only shows the first 2–3 images before a swipe.

| # | Role | Content |
|---|---|---|
| 1 | **Outcome** | What the user GETS from the app. Not "the app has feature X" |
| 2 | **How it works** | The core screen explaining how the app works |
| 3 | **Strongest feature** | What competitors lack |
| 4 | **Depth** | Shows the app is not shallow (data, history, customisation) |
| 5 | **Proof** | Real numbers, real sourced reviews, or before/after. NEVER invent ratings |
| 6 | **Extended** | Widgets, Apple Watch, sync, offline — depends on the app |

5 solid images beat 10 repetitive ones. Apple allows 1–10 images per device size.

---

## Step 3 — Write captions

Rules:

- **At most 6 words** in the headline; 2 lines is the ceiling.
- State a **concrete outcome**; ban vague words: "all-in-one", "optimised experience", "complete solution", "next level".
- Lead with a verb when possible: "Track spending in 5 seconds" > "Spending tracking feature".
- No full stop at the end of the headline.
- No ALL CAPS unless the brand requires it.
- Optional subline: at most 10 words, 45–50% of the headline size.

Quick test: shrink the image to 140px wide (App Store thumbnail size). If the caption is unreadable → text too small or too much text.

---

## Step 4 — Build the HTML

Default canvas **1320 × 2868** (iPhone 6.9", the only size Apple requires). Render one HTML file holding every frame, each a `<section class="shot">`.

Safe grid for the 1320×2868 canvas:

| Area | Value |
|---|---|
| Left/right margin | 96px |
| Caption block | y = 150 → 640px |
| Headline size | 96–120px, weight 700–800, line-height 1.08 |
| Subline size | 48–56px, weight 400–500, opacity .75 |
| Device image | starts at y ≈ 720px, 1060px wide, 88px radius |
| Bottom clearance | ≥ 80px (avoid cropping) |

Base template:

```html
<!doctype html>
<meta charset="utf-8">
<style>
  :root{
    --bg:#0B0B0F; --ink:#FFFFFF; --accent:#7C5CFF; --sub:rgba(255,255,255,.72);
    --W:1320px; --H:2868px;
  }
  *{margin:0;padding:0;box-sizing:border-box}
  body{background:#333}
  .shot{
    width:var(--W); height:var(--H); position:relative; overflow:hidden;
    background:var(--bg);
    font-family:"SF Pro Display",-apple-system,"Inter","Helvetica Neue",sans-serif;
    color:var(--ink); display:flex; flex-direction:column; align-items:center;
  }
  .glow{position:absolute;width:1400px;height:1400px;border-radius:50%;
        background:radial-gradient(circle,var(--accent) 0%,transparent 62%);
        opacity:.32;top:-420px;left:-260px;filter:blur(40px)}
  .cap{position:relative;z-index:2;padding:150px 96px 0;text-align:center;width:100%}
  .cap h1{font-size:108px;font-weight:800;line-height:1.08;letter-spacing:-.02em}
  .cap p{margin-top:28px;font-size:52px;font-weight:450;color:var(--sub);line-height:1.3}
  .device{position:relative;z-index:2;margin-top:auto;width:1060px;
          border-radius:88px;overflow:hidden;
          box-shadow:0 60px 140px rgba(0,0,0,.55);
          border:10px solid rgba(255,255,255,.10);
          transform:translateY(120px)}
  .device img{display:block;width:100%}
</style>

<section class="shot">
  <div class="glow"></div>
  <div class="cap">
    <h1>Turn discipline<br>into XP</h1>
    <p>Every habit you finish is a level up</p>
  </div>
  <div class="device"><img src="shots/shot-01.png"></div>
</section>
<!-- repeat a section per frame -->
```

Aesthetic rules:

- **One colour system across the whole set.** Changing accent between frames looks disjointed.
- Background: solid colour or a 2-stop gradient. Avoid stock photos as backgrounds.
- Device image: bleed off the bottom (`translateY`) for depth, or fully rounded when the UI is the focus.
- A device frame is **optional**. Use it when hardware context helps; drop it when the UI tells the story.
- No 3D-tilted device in frame 1. Straight, clear, readable.

---

## Step 5 — Render pixel-exact PNGs

```bash
npm i -D playwright
npx playwright install chromium   # free; skip if you point CHROME_PATH at an installed Chrome/Chromium
```

```js
// render.mjs
import { chromium } from 'playwright';
const W = 1320, H = 2868;
const b = await chromium.launch({ executablePath: process.env.CHROME_PATH || undefined });
const p = await b.newPage({ viewport:{width:W,height:H}, deviceScaleFactor:1 });
await p.goto('file://' + process.cwd() + '/shots.html');
const n = await p.locator('.shot').count();
for (let i = 0; i < n; i++) {
  await p.locator('.shot').nth(i).screenshot({
    path: `out/appstore-${String(i+1).padStart(2,'0')}.png`,
    scale: 'css'
  });
}
await b.close();
```

**Flattening alpha is mandatory** — Apple rejects PNGs with an alpha channel:

```bash
python3 -c "from PIL import Image;import glob;[Image.open(f).convert('RGB').save(f) for f in glob.glob('out/*.png')]"
```

Verify:

```bash
python3 -c "from PIL import Image;import glob;[print(f, Image.open(f).size, Image.open(f).mode) for f in sorted(glob.glob('out/*.png'))]"
# Must print: (1320, 2868) RGB — off by 1 pixel and App Store Connect blocks the upload
```

---

## Step 6 — QC checklist (run before delivering)

**Technical**

- [ ] Exactly 1320×2868 (or another 6.9" size: 1290×2796, 1260×2736) — all images the same size
- [ ] Mode `RGB`, no alpha, no odd ICC profile
- [ ] .png or .jpg, 1–10 images
- [ ] If the app runs on iPad: a 13" set too (2064×2752)

**Content**

- [ ] Every UI in the images is a real app screen
- [ ] Image 1 is not splash/login
- [ ] No prices, "Free", "Sale", "Download"
- [ ] No Android / Google Play / other platforms
- [ ] No real personal data, no placeholders
- [ ] Ratings/reviews (if any) are real and sourced
- [ ] Consistent status bar (9:41, full battery) in every image

**Conversion**

- [ ] Captions of frames 1 and 2 still readable at 140px
- [ ] One idea per frame, no repeats
- [ ] Captions state outcomes, not bare features
- [ ] The set looks like one system, not loose pieces

---

## Step 7 — Handoff

Deliver exactly 3 things:

1. The `out/` folder with PNGs named in upload order
2. A caption table (so the user can edit text without rebuilding)
3. One note: which size is required, which sizes Apple scales automatically

A/B tip: the App Store has **Product Page Optimization**, up to 3 variants for 90 days. Test a clear hypothesis (image 1 states an outcome vs a feature), not at random.

---

## Appendix A — Apple size spec (short version)

**iPhone — 6.9" required**, Apple scales other sizes:

| Size | Portrait | Landscape |
|---|---|---|
| 6.9" | 1320×2868 · 1290×2796 · 1260×2736 | swapped |
| 6.5" | 1284×2778 · 1242×2688 | swapped |
| 6.3" | 1206×2622 · 1179×2556 | swapped |

**iPad — 13" required** if the app runs on iPad:

| Size | Portrait | Landscape |
|---|---|---|
| 13" | 2064×2752 · 2048×2732 | swapped |
| 11" | 1488×2266 · 1668×2388 | swapped |

General: 1–10 images, .png/.jpg/.jpeg, **no alpha, no transparency**. Mac 16:10 (1280×800…2880×1800); Apple Watch must use the same size for every language.

---

## Appendix B — Rules people hit most

| Guideline | Content |
|---|---|
| 2.3.1 | Misleading marketing — showing features the app does not have |
| 2.3.3 | Images that do not show the app in use (splash, login, title art) |
| 2.3.7 | Prices, terms, descriptions that do not belong in that metadata |
| 2.3.10 | Mentioning other platforms (Android, Google Play) |
| 2.1 | Placeholder content, empty web views |
| 2.2 | Beta/demo/trial builds |

Screenshots rejected → **no new build needed** — fix the images and resubmit the metadata.

---

## Appendix C — Figma branch (when the user wants to hand-edit)

Only on request. Process:

1. Do Steps 1–3 as usual (research, storyboard, captions).
2. With a Figma MCP or by hand, create a file with one 1320×2868 frame per image, named `01 — Outcome`, `02 — How it works`…
3. Make components for the caption block and device mask so one edit updates the whole set.
4. Place the real screenshots into the frames.
5. Export PNG at 1x, then still run the alpha flattening from Step 5 before uploading.

---

## Related

- `app-landing-page` — a landing page for the app, shares the competitor research and copy
- `app-ui-designer` — builds app screens (use BEFORE this skill if the app has no screens yet)

## LESSONS LOG

Read this whole section BEFORE writing the first word of output. Each row is a mistake
someone already pointed out; repeating it is worse than making it the first time.
An empty table means this skill has never been corrected.
**An empty table is honest — never invent sample rows.**

- **Spot feedback:** "that's wrong", "not like that", "don't…", "drop…", "next time…",
  "from now on…", "I already told you", "still…", "how many times", or the user
  hand-edits the output you just gave and sends it back.
- **What to log:** fix the output and sweep every place with the same problem — ALWAYS.
  Logging is CONDITIONAL: only when the mistake is RULE-WORTHY, i.e. it would come back
  with a different input. A ONE-OFF (wrong name, wrong number, wrong link, changed
  preference) gets fixed, not logged. When logging, add EXACTLY ONE row to the table
  below, in this very file, then say `Logged in appstore-screenshot-builder LESSONS LOG: WRONG … → RIGHT …`.
  The **Source** column is required and takes one of three values: `user` (the user
  actually said it) · `review` (a review pass caught it) · `measured` (a tool run showed
  it). Never present the agent's own conclusion as if the user said it — a made-up
  source is worse than no row. The WRONG column describes observable behaviour.
- **Cap: 10 rows** — not an arbitrary number. The parent rule is `SKILL.md < 300 lines`;
  this block takes 28 frame lines, plus one blank separator and 10 rows makes 39, so
  the skill body must stop under 261 lines. Log full and a new row arrives → promote the
  most repeated row to a named hard rule in the skill body and delete it from the log;
  never delete a row just because it is old. If the two rules clash, `< 300 lines` WINS.
  Check with `wc -l SKILL.md` (< 300) and `grep -c '^| 20' SKILL.md` (<= 10).

| Date | Source | WRONG | RIGHT |
|---|---|---|---|
