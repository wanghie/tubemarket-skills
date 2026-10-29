---
name: app-landing-page
description: Use when the user wants a LANDING PAGE for a mobile app and/or a set of APP STORE screenshots, starting from research on competitors in the same niche and extracting the DNA of their pages. Runs inside Claude or ChatGPT, no API key. Triggers on "landing page for my app", "app intro page", "app landing page", "app store images", "app store screenshots", "build a page to sell the app".
---

# App Landing Page

One-line app idea → a buildable landing page + an App Store screenshot set that meets Apple's spec.
The foundation of everything is COMPETITOR RESEARCH, not inspiration.

## Rule 1: THE LANDING SELLS AN APP, IT IS NOT A COMPANY PAGE

Common failure: a feature-stuffed B2B SaaS page with a download button bolted on.

- The only conversion = **tapping the download button** (App Store / Google Play badge). Everything else is secondary.
- The hero image must be **the app screen inside a phone frame**, not a stock photo of smiling people.
- The page is read mostly on phones, not desktop. Design at 390px first, expand later.
- If a section does not move people closer to the download button, cut it.

## 6-step process

### Step 0 — Lock the brief with exactly 3 questions

- **What the app does, for whom** (one sentence)
- **What is needed**: landing only / App Store images only / both
- **Feel**: pick 1 — dark & game-like · light & clean (Apple, Linear) · warm & friendly (Finch, Duolingo) · serious & data-heavy

If the user is not around: decide, note the assumption in one line at the end, keep going. Do not stop and wait.

### Step 1 — Competitor research (REQUIRED, never skip)

Optional helper skill: `competitor-alternatives` — **use only its research part, do NOT write an SEO comparison page**.

Find **5-8 apps in the same niche** that have a real landing page. For each, open the page and extract exactly 7 things:

| Extract | Record specifically |
|---|---|
| Hero headline | Copy verbatim, count the words |
| Sub-headline | Which objection it handles |
| Hero image | How many phone frames, angled or straight, any hands |
| Section order | List top to bottom, in order |
| Social proof | Type (downloads / rating / press logos / testimonials) and placement |
| CTA button | Button text, store badges, how many times repeated |
| What they DO NOT have | Sections the whole niche is missing |

Preferred sources: the app's homepage, its App Store / Google Play listing, Product Hunt. Mark **sourced fact** vs **my guess** clearly.
If the sandbox cannot reach the pages, use a browser tool if available, or ask the user for screenshots.

**Step 1 output** — a compact DNA table + 3 lines of conclusions:
- What the whole niche does → we must have it, do not reinvent.
- What only 1-2 apps do and it works → we take it.
- The gap nobody fills → where we differ.

No DNA table, NO step 2.

### Step 2 — Lock the page structure

Optional helper skill: `landing-page`.

Default skeleton for an app landing (adjust to the step 1 DNA):

1. **Hero** — headline + sub + phone frame + 2 store badges
2. **Pain** — 1 sentence the user says in their own head
3. **3 core benefits** — each with 1 real screen, no generic icons
4. **How it works** — 3 steps, no more than 3
5. **Proof** — rating, downloads, real named reviews
6. **FAQ** — 4-6 questions handling exactly the objections found in step 1
7. **Final CTA** — store badges again, nothing else on screen

Drop multi-item navigation. An app landing does not need a 7-tab menu.

### Step 3 — Write copy by formula

Optional helper skill: `landing-page-design`.

- Headline **6-12 words**, states the RESULT, not the feature.
  Wrong: "AI-powered habit tracking app". Right: "Keep your habit past week three".
- Sub-headline handles the biggest objection, never repeats the headline.
- Button text states value: "Download free" > "Download"; "Try 7 days free" > "Start".
- Above the fold at 390px must show: headline + 1 phone frame + 1 store badge. No scrolling.
- Three headline styles, pick 1 and stay consistent: **paint a moment** · **state the result** · **kill a pain**.

`landing-page-design` includes hero-image generation through an external paid image CLI. **Skip that part** — this repo needs no API key; use only the skeleton + copy formula.

### Step 4 — Build the code

Optional helper skill: `frontend-design`.

- Output real, runnable HTML/React, not an image mockup.
- Mobile-first: write 390px first, add breakpoints after.
- Draw the phone frame in CSS or SVG, no heavy mockup images.
- App Store / Google Play badges: use the official Apple/Google assets, never redraw them.

### Step 5 — App Store images

Optional helper skill: `app-store-screenshots`, or this repo's `appstore-screenshot-builder`.

- **Core principle: screenshots are ADS, not documentation.** Each slide sells ONE idea.
- 5-8 slide arc: biggest benefit → differentiator → core features (2-3 slides) → trust proof.
- Short captions, readable at phone thumbnail size.
- Required resolutions: iPhone 1320×2868 and 1125×2436; iPad 2064×2752 and 2048×2732.
- Export with `html-to-image` `toPng()` using the **call-twice trick** (first call loads assets, second gives a clean image).

### Step 6 — Review before handoff

Optional helper skill: `page-cro`.

Required checklist, self-review then report:

- [ ] Does a stranger understand what the app does within 5 seconds?
- [ ] Is a store badge visible at 390px without scrolling?
- [ ] Tap targets ≥ 44px?
- [ ] Headline 6-12 words and states a result?
- [ ] Every number is real or marked `[NUMBER]`?
- [ ] Any section that does not push toward download? Cut?
- [ ] Accented text (e.g. Vietnamese) renders correctly, no broken glyphs?

Report in 3 groups: **Fix now** · **Big fix, prioritise** · **Worth an A/B test**.

## Aesthetic rules

**Type**
- Max 2 fonts. Avoid Inter/Roboto/Arial. Prefer a font with character for headings (Space Grotesk, Sora, Bricolage Grotesque, Instrument Serif) + one clean body font.
- The font must cover the page's language — for Vietnamese check "ữ ằ ộ" do not break. If they do, change font.
- Clear scale: 40-56 hero headline / 28-32 section title / 16-18 body / 13-14 secondary.

**Colour**
- 1 dominant background + 1 accent + at most 1 secondary accent. Define in oklch, same chroma/lightness, only hue changes.
- White and black must be tinted (warm or cool), never pure #fff / #000.

**Layout**
- Flex/grid + `gap`. No one-off margins per element.
- Icons: stroke SVG, 20/24px grid, one stroke weight. NEVER use emoji as icons.

**Avoid (AI slop)**
- Pointless purple-blue gradients, rounded cards with a coloured left border, emoji everywhere, stock photos of smiling people, fake numbers to fill space.
- Never invent real data (downloads, rating, price, reviewer names). Missing → `[DOWNLOADS]`, `[RATING]` for the user to fill.

## Copyright

Studying competitors is fine. Redrawing their logo, wordmark, characters or illustrations is not.
Extract **structure and mechanics**, not **brand assets**.
Never put a competitor's testimonials, ratings or press logos on your page.

## Language

All copy in the target audience's language, written as a native speaker would say it. No machine translation.
Proper names and technical terms stay as they are.

## If the helper skills are not installed

The helper skills above are optional. To install them for Claude Code:

```bash
mkdir -p ~/skills-src && cd ~/skills-src
git clone https://github.com/boraoztunc/skills.git bora-skills
mkdir -p ~/.claude/skills
for s in competitor-alternatives landing-page page-cro app-store-screenshots frontend-design; do
  ln -sfn ~/skills-src/bora-skills/$s ~/.claude/skills/$s
done
npx skills add https://github.com/inference-sh/skills --skill landing-page-design
```

Without them the 6 steps still run from the checklists embedded in this file — you only lose each helper's deeper detail.

## Handoff

One or two sentences: what was built, which competitors it is based on, what was assumed, what the user should review.
Attach the step 1 DNA table so the user can verify it — it is the part most likely to be wrong.

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
  below, in this very file, then say `Logged in app-landing-page LESSONS LOG: WRONG … → RIGHT …`.
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
