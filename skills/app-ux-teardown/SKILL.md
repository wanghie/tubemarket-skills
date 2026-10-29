---
name: app-ux-teardown
description: Turn a competitor app's UX into product decisions — tear down 3 apps at once to separate industry convention from individual choice, check transfer conditions before borrowing a mechanic, count friction and paywall position, flag TOXIC mechanics, and take motion numbers only from screen recordings measured with ffmpeg. Runs in Claude Code or ChatGPT plus local ffmpeg, no API key. Triggers on "UX teardown", "tear down this app's UX", "break down the animations of", "how is this app's UX", "research competitor apps". DIFFERENT from app-landing-page (builds the page that sells the app) and clean-room-teardown (takes apart the technical internals to rebuild).
---

# app-ux-teardown

Tearing down an app is not retelling which screens it has. This skill turns an app
that won into **decisions for your own app** — and blocks the most expensive trap in
the trade: copying their mechanic wholesale without asking what conditions it lives on.

Three principles govern the whole file:

1. **Tear down three apps, not one.** One app is one data point; it cannot separate
   industry convention from individual choice.
2. **Every mechanic has living conditions.** Not checking them is cargo-culting.
3. **Every number must trace to a source.** Structure from screenshots, motion from
   video, everything else labelled `[GUESS]`.

Method background: Nielsen's 10 heuristics, cognitive walkthrough, Hooked, Fogg B=MAP,
Material/Apple motion numbers, Growth.Design case studies.

## When to use

- About to build an app and want to know what this niche has already solved
- You like how an app feels but cannot name what you like
- You must decide a hard flow: onboarding, permission prompts, paywall placement
- You need a set of motion numbers to hand to a design tool

**Do not use when:** you need who is in the market and what they charge
(`creator-product-teardown`) · you already know what you want and just need screens
(`app-ui-designer`) · you have neither screenshots nor a recording of the app — no
source, no teardown; say so instead of guessing.

---

## Step 0 — Block first: write one sentence "tearing down for what"

> Tear down `<app>` to borrow `<specific mechanic>` for `<which screen of my app>`.

Pass: "Tear down Opal to borrow the gem-as-mirror-of-behaviour mechanic for my app's
Home screen."  Fail: "Tear down Opal to see what's good about it."

No sentence yet → ask exactly one question and continue. User not around → fill it in
yourself and list it in the assumptions section at the end.

---

## Step 1 — Three apps, and count friction straight from screenshots

> **Three-app rule** — Pick the leader, a peer, and one that does it differently.
> Where **all three agree** is industry convention: doing it differently makes users
> relearn, and usually loses. Where **each does its own thing** nobody is right yet —
> your playground. Where **only the winner has it** is the top candidate to borrow.

Sources for screens and flows: a UI library such as Mobbin (via its MCP if you have
one, or its website), App Store screenshots, or screenshots the user takes. Look for
flows first (a flow keeps the ORDER, and order is the UX), with the app name in the
query; if several versions of a flow exist, take them all. **Actually open the images** —
never describe a screen from metadata.

Then fill this table, from screenshots alone, no video needed. These are the cheapest
numbers and say more about product intent than any motion token:

| Metric | App A | App B | App C |
|---|---|---|---|
| Steps to **first value** (the moment the app proves useful) | | | |
| Required fields to fill | | | |
| Skippable screens / total screens | | | |
| **Paywall at step number** — before or after first value | | | |
| Where permissions are asked — is the reason explained first | | | |
| Hard sign-in wall or not | | | |

Paywall timing is the app's biggest economic decision. Do not leave it in a parenthesis.

**Done when:** an ordered flow table per app, plus the three-column friction table.

---

## Step 2 — Read the history, because a winning app is not right about everything

A winning app may live on ASO and PR while the thing you love is just a passenger.
The closest thing to causal evidence is free:

- **App Store → Version History**, the last 3-5 releases
- **1-2 star reviews**, sorted "Most Recent", read 20

Three questions to answer:

| What you see | What it means |
|---|---|
| What they keep fixing across releases | A pain not solved yet |
| What they QUIETLY REMOVED (comparing two flow versions shows it too) | They measured it did not work |
| Where people who hate the app hate it | Your gap |

---

## Step 3 — Extract mechanics, four layers, in this order

### Layer 0 — Transfer conditions (run BEFORE every other layer)

For each mechanic you plan to borrow, fill three boxes:

1. What **state** do that app's users arrive in — guilt, curiosity, urgency, boredom, FOMO?
2. Where does the mechanic feed on that state?
3. Do MY app's users have that state? If not, what must the mechanic change?

> **Transfer-condition rule** — If you cannot answer box 3, the mechanic goes in the
> DROP column, not TAKE. Opal's data shock works because people downloading Opal already
> feel guilty before opening it. Moved into an app with no background guilt, it becomes
> an insult to the user.

### Layer A — Three mechanic questions, per core screen

| Question | Passing example (Opal) |
|---|---|
| What does it do to **emotion**? | Makes you guess your screen time, then connects real Screen Time to hit you with a bigger number — a shock from THEIR OWN data |
| What does it turn **dry data** into? | A gem that looks good/bad depending on behaviour. One look at the gem tells you how today went |
| What creates a **reason to come back tomorrow**? | Daily reset score + streak + comparison with others |

### Layer B — Cognitive walkthrough, per STEP of the flow

Play a first-time user and ask four questions. Record which step fails which question —
each question has a different cure:

| # | Question | Fail = problem with |
|---|---|---|
| 1 | Are they trying to achieve the right outcome? | Goal |
| 2 | Can they SEE that the right action is available? | Visibility |
| 3 | Can they connect that action to the outcome they want? | Wording |
| 4 | After acting, can they see they got closer to the goal? | Feedback — cure with motion, not more text |

### Layer C — The four Hooked beats, for the whole app

**Trigger** (external or internal) → **Action** (the minimum action traded for a reward)
→ **Variable Reward** (is the reward uncertain) → **Investment** (what users put in that
makes leaving hard). A beat you cannot write is a beat the app REALLY LACKS — put it in
the GAP column.

### Layer D — Flag TOXIC

Half of Hooked's techniques are dark patterns when misused. A self-improvement app that
borrows them wrongly becomes an app that punishes its users. Five detection lines:

- Is losing a streak punished harder than keeping it is rewarded?
- Is the decline button written as self-insult ("No, I like wasting my life")?
- Is cancelling harder than subscribing?
- Do notifications create anxiety instead of motivation?
- Do stats compare with others in a belittling way?

A mechanic that trips any line retains users by making them feel bad about themselves.
It goes in the TOXIC column, not TAKE.

> **"Mechanics, not skin" rule** — Describing structure and mechanics is fine. Redrawing
> their logo, wordmark, characters or illustrations is not, even recoloured. The line:
> would an outsider recognise the other app.

---

## Step 4 — Accessibility, five lines, checkable from screenshots

Without this section it is not a UX teardown. Check from screenshots plus a minute on a device:

| Check | Threshold |
|---|---|
| Tap targets | ≥ 44×44pt (Apple HIG) |
| Text contrast | ≥ 4.5:1 (WCAG AA) — measurable from screenshots |
| Dynamic Type | Set the largest text size, does the layout break |
| **Reduce Motion** | Does the app respect it |
| VoiceOver | Do icon-only buttons have labels |

The Reduce Motion line ties directly into motion: borrowing tokens without a fallback
makes your app non-compliant.

---

## Step 5 — Motion: source, measurement, and score by PURPOSE

> **"No video, no numbers" rule** — Screenshots are STILL images. Every duration/easing
> number pulled from a still image is invented, however plausible it sounds.

Only two valid sources: **a real screen recording**, and **first-party documentation**
(Apple HIG, WWDC, that app's engineering blog). Anything else gets `[GUESS]` on the same
line, not in a disclaimer at the end.

**The agent cannot run an iPhone app itself.** Do not promise to look and then quietly invent.

Recording request — send this block to the user verbatim:

> Please record your iPhone screen: Control Center → Record. Three clips: (1) open the
> app to Home and leave it still for 10 seconds; (2) run through the whole `<name>` flow,
> pausing 2 seconds on each screen; (3) tap `<element with the effect>` then exit, twice.
> Please tell me **which iPhone model** you used. Turn on 60fps in Settings → Camera →
> Record Video first. Then AirDrop it to your computer, into one folder.

### Measure

Run it on the machine that has the video (Claude Code's terminal, or run it yourself and
paste the output into ChatGPT); do not upload the video to the cloud. This block has been
run for real, paste it as is:

```bash
V=<video-folder>/recording.mov
ffprobe -v error -select_streams v:0 -show_entries stream=r_frame_rate \
  -show_entries format=duration -of default=nw=1 "$V"

ffmpeg -i "$V" -vf \
  "tblend=all_mode=difference,signalstats,metadata=print:key=lavfi.signalstats.YAVG" \
  -f null - 2>&1 \
| grep -oE "pts_time:[0-9.]+|YAVG=[0-9.]+" | paste - - \
| sed 's/pts_time://; s/YAVG=//' \
| awk '{n=int($2*4); s=""; while(n-->0) s=s"#"; printf "%8.3fs %6.2f %s\n", $1, $2, s}'
```

The series sits at 0, spikes, falls back to 0. `duration = (last non-zero second − first
non-zero second) × 1000`. To measure one element, insert `crop=w:h:x:y,` right before `tblend`.

**Four limits that must be written into the file, never ignored:**

- **YAVG measures how many pixels changed, not position** → it cannot tell a fade from a
  move. To read the easing of a positional move you must crop tightly to the element.
- **ProMotion 120Hz**: iPhone Pro runs UI at 120Hz but screen recordings are 60fps, so
  anything under 16ms is invisible. Record the device model in the file.
- **Dropped frames when the phone is hot**: check real timestamp gaps between frames
  before trusting them, do not assume they are even.
- **30fps recordings**: ±33ms error, put it in `tolerance`.

### Score in two tiers

**Tier 1 — what is this effect for?** This is the conclusion worth handing to the builder:

| Purpose | Keep |
|---|---|
| Hiding network latency | Yes |
| Keeping spatial continuity (the user knows where they came from and went) | Yes |
| Directing the eye to what just changed | Yes |
| Confirming an action | Yes |
| Pure decoration | **Cut** |

**Tier 2 — fast or slow against the standard:**

| Type | Standard | Source |
|---|---|---|
| Tap feedback | ≤100ms feels "instant"; >1s breaks the train of thought | Nielsen |
| Screen transitions | short 50-200 · medium 250-400 · long 450-600ms | Material 3 |
| Spring settles | ~0.5s (`.smooth/.snappy/.bouncy` in SwiftUI) | Apple |
| Following the finger | response ~0.15s (`.interactiveSpring`) | Apple |
| Button / tooltip / dropdown / modal | 100-160 · 125-200 · 150-250 · 200-500ms | Kowalski — **a WEB standard, not iOS native. Say so when quoting** |
| Stagger | ≤20ms (Material 1) · whole sequence ≤500ms | M1 / Carbon |
| Frame rate | ≤16ms/frame for 60fps | Google RAIL |

Apple HIG **publishes no duration numbers** — only qualitative guidance. Do not cite HIG
for a number; cite the SwiftUI API docs.

**Haptics cannot be measured from video.** Write `[NOT MEASURABLE]`.

---

## Step 6 — Output three things, end with experiments

**`<app>-TEARDOWN.md`** — opens with 5 takeaways, one line each. Required at the top:
**app name, version number, teardown date, recording device model.** Without those four,
in three months the file is hearsay.

Sections: three-app flow table · friction table · four mechanic layers · **table of
walkthrough failures, stating which question failed** · accessibility · motion.

The closing table has **five columns**, not three:

| Mechanic | TAKE / DROP / GAP / TOXIC | Build cost (hours) | How to validate |
|---|---|---|---|

End with **three testable hypotheses, ranked by impact over cost** — not twelve equally
nice ideas.

> **"Don't crown a winner" rule** — The goal is not to score the competitor. A report
> that ends "their app is better" is useless. End with the gap you can fill. Tear down the
> design only; do not drift into judging whether the company is good or bad.

**`MOTION-TOKENS.json`** — readable directly by a design tool:

```json
{
  "source": "opal-home.mov", "device": "iPhone 15 Pro", "refreshRate": 120,
  "capturedFps": 60, "tolerance": "±16ms", "measuredOn": "2026-09-06",
  "platform": "ios-native",
  "duration": { "tap": 120, "reveal": 320, "screen": 400 },
  "easing": { "standard": "cubic-bezier(0.2, 0, 0, 1)",
              "hero": "spring(response=0.5, damping=0.825)" },
  "stagger": { "list": 40 },
  "appliesTo": { "reveal": "stat cards on Home", "screen": "tab switch" },
  "reducedMotion": { "reveal": "opacity only, 160ms", "screen": "cross-fade" },
  "measured": ["duration.reveal", "duration.screen"],
  "guessed": ["easing.hero", "stagger.list"]
}
```

`measured` / `guessed` are required. `platform` is required because SwiftUI springs differ
from CSS cubic-bezier, and most design tools take web input. `reducedMotion` is required
because without it borrowed tokens make your app fail accessibility.

**Evidence** — extract 3-5 key frames as PNG and keep them next to the MD file. The
original video will be deleted; the images stay.

---

## Checklist before delivering

- [ ] The "tearing down for what" sentence is at the top
- [ ] **Three apps** torn down, with convention vs playground marked
- [ ] Friction table filled, including paywall position
- [ ] Read the changelog + 20 one-to-two-star reviews
- [ ] **Layer 0 ran before Layer A**; every TAKE mechanic passes box 3
- [ ] The walkthrough-failure table is in the file, stating which question failed
- [ ] The TOXIC column checked against all five dark-pattern lines
- [ ] The five accessibility lines checked
- [ ] Every effect scored by PURPOSE before speed
- [ ] Device model, fps, tolerance, date and app version recorded
- [ ] Unmeasurable lines labelled `[GUESS]` in place
- [ ] No redrawn logo/characters/wordmark from the app torn down
- [ ] Ends with 3 hypotheses with cost and validation method
- [ ] **Marked the 3 least-confident conclusions and what evidence would settle them** —
      so the reader checks the right places

---

## Quick reference

| Situation | Do |
|---|---|
| No screenshots available for the app | Skip the screenshot part, go straight to video. State the missing structure source |
| No video yet | Finish steps 1-4, deliver, leave motion empty. Do not guess to fill it |
| Only 1 app could be torn down | Still do it, but state it: convention cannot be separated from choice |
| The app has a Mac version | It can be driven on macOS, BUT Mac Catalyst motion differs from iOS — Mac measurements are not valid iOS tokens |
| The competitor is made by Apple | Check HIG/WWDC first — system effects have public names and numbers |
| Done and want to build screens | Move to `app-ui-designer`, feed it `MOTION-TOKENS.json` |

## Remember one line

Every mechanic lives on a condition. Copy the mechanic without the condition and you copy a corpse.

## This skill must improve itself

1. **Evaluate after each run.** Score briefly against the checklist: which step was
   missed, what the user had to fix by hand. Worth fixing → suggest updating this SKILL.md directly.
2. **Look things up now and then.** UI libraries reorganise their data, ffmpeg flags
   change between versions, iOS changes its animation system yearly, WCAG gets new
   versions. Any number or tool name a few months old should be re-checked at the source.
3. **When you do not know, ask a person.** Say plainly what is out of reach and point
   the user to who can help. Real people are a source of help, not only documentation.

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
  below, in this very file, then say `Logged in app-ux-teardown LESSONS LOG: WRONG … → RIGHT …`.
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
