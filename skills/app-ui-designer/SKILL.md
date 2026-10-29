---
name: app-ui-designer
description: Use when the user gives ONE APP IDEA and wants good-looking, clickable, editable UI screens — the skill researches competitors, locks an aesthetic direction, then builds the screens. Runs inside Claude or ChatGPT, no API key. Triggers on "design an app", "make the UI for", "build the screens", "app mockup", "redesign this app".
---

# App UI Designer

Turn a one-line idea into a set of good-looking app screens you can click and edit.
The user brings the idea — the skill handles research, aesthetics and the build.

## Rule 1: THESE ARE APP SCREENS, NOT SLIDES

The most common failure: building a text-heavy deck and calling it design.

- Each artboard = ONE PHONE SCREEN 390×844 (or 1440×900 for web).
- The only text on a screen is REAL in-app text: button labels, section names, numbers. No analysis, no explanations, no bullets.
- All design notes and rationale go into **sticky notes** (`annotations` in canvas.json, or a notes panel beside the artboards), NEVER inside the artboard.
- An artboard with more than ~40 words is almost certainly wrong.

## 5-step process

### 1. Lock the brief with exactly 3 questions
No rambling. Only the 3 things that decide everything else:
- **Who uses it and for what** (one sentence)
- **Platform**: phone app / web / both
- **Feel**: pick 1 — dark & game-like (Solo Leveling, neon) · light & clean (Apple, Notion) · warm & friendly (Finch, Duolingo) · serious & data-heavy (Linear, Bloomberg)

If the user is not around to answer: decide, write the assumption in one line at the end, keep going — do not stop and wait.

### 2. Research before drawing (REQUIRED, never skip)
- Web-search 3-5 apps in the same niche. For each, capture: main tabs, core screen, retention mechanic, the most common complaint in real reviews.
- Preferred sources: App Store / Google Play / official docs / help center. Mark **sourced fact** vs **guess** clearly.
- If the sandbox cannot reach the stores, use a browser tool if one is available, or ask the user for screenshots.
- Close with one short paragraph: what to TAKE, what to DROP, which gap nobody fills yet. This is the foundation of the design, not decoration.

### 3. Lock the aesthetic direction before hi-fi
Build 2-3 low-fi artboards of the SAME screen, each a genuinely different direction (not 3 shades of one). Give each direction a short memorable name. Let the user pick.
Build the full set only after the pick — and keep that direction name from then on.

### 4. Build the screens
If a `design` skill is available (canvas `.dc.html` + `canvas.json`), call it and follow its format; otherwise build one self-contained static HTML file with one artboard per screen. Also:
- **Count**: 5-8 screens for the main flow. Do not build 24 artboards with empty insides.
- **Order**: follow the user's real path (onboarding → main screen → action → reward → settings).
- **Pages**: 1 page for the main flow, 1 page for variations/components. No random page splits.
- Mark artboards with working buttons as interactive (`"is_interactive": true` in canvas mode).

### 5. Short handoff
One or two sentences: what was built, what was assumed, what the user should review. No tutorial on editing — the canvas speaks for itself.

## Aesthetic rules (what makes it "good-looking")

**Type**
- Max 2 fonts. Avoid Inter/Roboto/Arial — overused. Prefer a font with character for headings (e.g. Space Grotesk, Sora, Bricolage Grotesque, Instrument Serif) + one clean body font.
- The font must render the app's language correctly — for Vietnamese check that "ữ ằ ộ" do not break. If marks are missing, change font.
- A clear size scale: 28-32 screen title / 17-20 section title / 15-16 body / 12-13 secondary. Not 7 nearly identical sizes.

**Colour**
- 1 dominant background + 1 accent + at most 1 secondary accent. Define them in oklch with the same chroma/lightness, changing only hue.
- White and black must be tinted (warm or cool), never pure #fff / #000.
- Check text contrast is readable in sunlight.

**Layout**
- Always flex/grid + `gap`. No one-off margins per element — they break when the user drags things around.
- Tap targets no smaller than 44px.
- Do NOT draw a fake iOS status bar (9:41, battery, wifi) and do NOT draw a fake keyboard. Leave the space empty.
- Icons: stroke SVG on a 20/24px grid with one stroke weight. NEVER use emoji as icons.

**Avoid (AI slop)**
- Pointless purple-blue gradients, rounded cards with a coloured left border, emoji everywhere, fake numbers to fill space.
- Never invent real data (prices, dates, names). Where data is missing use `[PRICE]`, `[DATE]` for the user to fill. For clickable prototypes use sample numbers and say they are samples.

## Copyright
When referencing competitor apps: describe STRUCTURE and MECHANICS; never redraw their logo, characters, wordmark or illustrations. Studying competitors is fine; copying their branded interface is not.

## Language
All in-app text and notes are written in the user's language as a native speaker would say it. No machine translation. Proper names and technical terms stay as they are.

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
  below, in this very file, then say `Logged in app-ui-designer LESSONS LOG: WRONG … → RIGHT …`.
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
