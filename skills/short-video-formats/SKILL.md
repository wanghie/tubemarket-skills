---
name: short-video-formats
description: Write and edit short-form videos in 10 proven formats for knowledge and education channels - Straight Talk, Hands-On Explainer, Backdrop Commentary, Second Screen, Whiteboard Breakdown, Side-by-Side, Do / Don't List, Myth vs Fact, Tier Ranking, Field Test. From a topic it writes the script, shot list, on-screen text and edit notes in the format's exact structure; from a talking-head clip it renders a finished 9:16 MP4 with the format's graphics, silence cuts, punch zooms and word captions. Runs locally with ffmpeg, no API key. Use when the user says "which format should I use", "make this a myth vs fact video", "turn my clip into a short", "do/don't video", "tier list video", "whiteboard video", "10 formats", "short video format", "faceless education short".
---

# short-video-formats

Most education shorts fail because they have no shape: one person talking with nothing that tells the viewer where the video is going. Each of these 10 formats is a shape. The spoken part is cut by the existing skills; what makes a format a format is the **graphic layer** (a do/don't table, a tier board, a MYTH/FACT stamp, a building diagram, a field counter) and the **beat structure** of the script.

All 10 share one skeleton: pinned headline with a promise in the first 3 seconds -> body in labelled blocks -> one-line close + a comment/save CTA.

## The 10 formats

Full spec (beats, length, cut pace, on-screen text, b-roll) is in `formats.json`. `python3 skills/short-video-formats/scripts/render.py list` prints it.

| # | Format | What it is | Clip only? |
|---|---|---|---|
| 1 | Straight Talk | one person, one idea, to camera | yes |
| 2 | Hands-On Explainer | explain while doing the task with your hands | needs hands footage |
| 3 | Backdrop Commentary | comment in front of a headline/chart/screenshot | needs backdrop images |
| 4 | Second Screen | a phone/laptop/clip shown beside the speaker | needs screen recording |
| 5 | Whiteboard Breakdown | a diagram or timeline that builds as you talk | yes (graphic board) |
| 6 | Side-by-Side | compare A vs B, mark the winner | yes |
| 7 | Do / Don't List | wrong (red) / right (accent) pairs pop in | yes |
| 8 | Myth vs Fact | break one common wrong belief | yes |
| 9 | Tier Ranking | place items into S/A/B/C/D tiers | yes |
| 10 | Field Test | try it for real, report the result | needs activity footage |

"Needs footage" formats still render from one clip: the skill adds a graphic stand-in (`inset` image/clip, `tag` counter) and the shot list tells the user what to film to upgrade it.

## Picking a format ("auto")

When the user says "auto" or doesn't choose, pick by the content of the idea or transcript:

- a belief that is wrong -> 8 · two options -> 6 · mistakes and fixes -> 7
- several items to judge -> 9 · a process, timeline or system -> 5
- "I tried / we went / I tested" -> 10 · a news item, stat or post -> 3 or 4
- a skill done with the hands -> 2 · one strong opinion -> 1

Say which format you picked and why in one line, then proceed.

## Mode A - topic only (no footage)

Deliver, in this order:
1. **Format + why** (one line).
2. **Script** in the format's beats from `formats.json`, timed (`0-3s hook`, ...). Target the format's length range. Spoken lines short enough to say in one breath.
3. **On-screen text**: the pinned 2-line headline (max ~24 characters per line) and every row/stamp/tag with the line it appears on.
4. **Shot list**: numbered shots, framing, what to film for the "needs footage" formats.
5. **Edit notes**: cut pace, where the punch zooms land, CTA.
6. A **plan.json** ready for Mode B (see below), with `at` set to phrases from the script.

## Mode B - from a talking-head clip

```bash
# 1. transcript (once)
python3 skills/local-whisper-transcriber/scripts/transcribe.py CLIP.mp4 --audience en -o work/CLIP.transcript.json
# 2. a skeleton plan for the chosen format, with the transcript lines listed inside
python3 skills/short-video-formats/scripts/render.py template --format 8 -t work/CLIP.transcript.json > work/plan.json
# 3. fill the plan (you, the agent), then render
python3 skills/short-video-formats/scripts/render.py render CLIP.mp4 -t work/CLIP.transcript.json \
  --plan work/plan.json --outdir work/out --audience en
```

The render chain reuses the other skills, it does not reimplement them:
`trim` -> **video-shorts-pipeline** (= **silence-cutter** -> **auto-reframe** -> **punch-zoom**) -> stacked layout (graphics panel on top 40%, speaker below) -> format graphics -> **word-captions**.
Need AI b-roll for the `inset` slots? Run **broll-prompt-director** on the transcript and drop the generated clips into `inset` elements.

### plan.json

```json
{
  "format": 8, "name": "myth-vs-fact",
  "title": ["Can the body survive", "a year in space?"],
  "trim": [0, 28.7],
  "focus_x": 0.48, "scale": 1.15,
  "elements": [
    {"type": "row", "style": "bad", "text": "MYTH: a year up there breaks you", "at": "one of the people"},
    {"type": "stamp", "style": "bad", "text": "Myth", "at": "one of the people", "until": "the human body can endure"},
    {"type": "row", "style": "good", "text": "FACT: the body endures and adapts", "at": "the human body can endure"},
    {"type": "cta", "text": "Follow for more", "at": "learn just how"}
  ]
}
```

| Element | Used by | Notes |
|---|---|---|
| `row` style `bad` / `good` / `neutral` | 1, 6, 7, 8, 10 | stacks under the headline; `mark` sets the prefix for neutral; `side: left/right` for format 6 |
| `row` style `board` | 5 | dark text on a white board that appears with the first board row |
| `row` style `tier:S` ... `tier:D` | 9 | coloured tier letter + item |
| `stamp` style `bad` / `good` | 8, 10 | rotated word top-right (MYTH, FACT, UNUSUAL) |
| `tag` | 2, 10 | accent pill on the speaker area (Day 1, Step 2, 160 m) |
| `inset` + `file` | 3, 4 | image or clip over the speaker area, `width` 0.42 default |
| `cta` | all | white pill at the bottom for the last ~3s |

- `at` / `until` = **a phrase the speaker says** (preferred - survives silence cutting) or seconds on the final timeline. A phrase that is not in the transcript stops the render with an error, so copy words from the transcript.
- The panel holds 4 rows at default `--panel 0.40`. More rows -> raise `--panel` or merge rows.
- `focus_x` (0-1) = horizontal centre of the speaker in the 16:9 source. Extract one frame and look at it before setting it. Without it the clip goes through auto-reframe face mode.
- `trim` cuts the source first; the transcript is shifted for you, whisper runs once.

## Hard rules

- Never name or label a format after a creator. Formats are named by function.
- Headline: max 2 lines, max ~24 characters each, contains the promise or the question.
- Do not put rows over the speaker's face: graphics live in the top panel, only `tag`, `inset`, captions and `cta` sit on the speaker area.
- Facts in rows must come from what the speaker says or a source the user gave. If the speaker states a plan or a date that may be outdated, label it ("as announced in 2019").
- Always extract frames from the result (`ffmpeg -i out.mp4 -vf "fps=1/3,scale=300:-1,tile=5x2" -frames:v 1 sheet.jpg`) and look at them before handing over.
- Footage you do not own: only public domain or CC BY, and credit the source.

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
  below, in this very file, then say `Logged in short-video-formats LESSONS LOG: WRONG … → RIGHT …`.
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
| 2026-11-17 | measured | Rendered a wide shot through auto-reframe face mode; the 9:16 crop locked onto background equipment and the speaker was out of frame | Look at one source frame and set `focus_x` in the plan for wide or busy shots |
