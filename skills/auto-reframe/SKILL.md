---
name: auto-reframe
description: Turn horizontal 16:9 video into vertical 9:16 (or 4:5, 1:1) that follows the face of the speaker with MediaPipe, using hard cuts instead of floaty pans. Runs locally, no API key. Use when the user says "make it vertical", "convert to 9:16", "crop for TikTok/Reels/Shorts", "horizontal video to short", "reframe". No transcript needed.
---

# auto-reframe

## Run

```bash
python3 skills/auto-reframe/scripts/reframe.py INPUT.mp4 \
  --aspect 9:16 --mode face \
  -o work/INPUT.vertical.mp4
```

`--mode`:
- `face` (default) — MediaPipe face detection, picks the largest face (the person talking to camera)
- `center` — centre crop, for footage that is already framed
- `top` — horizontal centre crop pinned to the top edge, for screen recordings

`--dry-run` writes `.reframe.json` so you can review the crop plan before rendering.

## Why hard cuts, not smooth pans

A crop that moves every frame with the face looks like a shaky handheld camera. This script keeps the frame still and only jumps to a new position once the speaker has moved **and stayed there** long enough (`--min-hold`, default 1.2s) by a large enough amount (`--jump`, default 6% of width). It looks like someone made a cut, not like the camera got bumped.

These two parameters control the whole feel:
- Seated talking head: raise `--jump 0.10` so the frame almost never jumps
- Speaker walking around, multi-cam: lower `--min-hold 0.6`

## Real limits

- Several people in frame: the script picks the LARGEST face, not the one SPEAKING. Two people side by side in an interview will be tracked wrong. That needs active-speaker detection, which is not in this repo yet.
- Without MediaPipe installed the script falls back to a centre crop and says so clearly instead of failing.

## Requirements

`ffmpeg`, `pip install mediapipe opencv-python` (optional — without them it runs in centre mode)

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
  below, in this very file, then say `Logged in auto-reframe LESSONS LOG: WRONG … → RIGHT …`.
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
