---
name: punch-zoom
description: Add pace to talking-head video with punch zooms on emphasised words and slow Ken Burns pushes on long passages, picking emphasis points from the transcript with separate keyword sets for English and Vietnamese. Runs locally with ffmpeg, no API key. Use when the user says "the video looks static", "add zooms", "punch zoom", "make it less boring", "add rhythm". Needs a transcript from local-whisper-transcriber.
---

# punch-zoom

A static single-camera talking head is the number one reason viewers scroll past. This skill adds two kinds of motion, both tied to the speech rather than sprinkled at random.

- **punch** — an instant hard zoom on the emphasised word, held to the end of the clause
- **push** — a slow Ken Burns push under long passages so the frame never sits still too long

## Run

```bash
python3 skills/punch-zoom/scripts/zoom.py INPUT.mp4 \
  -t work/INPUT.transcript.json \
  --density 0.12 \
  -o work/INPUT.zoom.mp4
```

`--density` = zooms per second. `0.12` ≈ one every 8 seconds (default, fits 30-60s shorts). For a 15s video raise it to `0.2`.
`--dry-run` prints the zoom points and the chosen words without rendering — always run this first.
`--map file.json` uses a hand-written plan instead of the automatic one.

## How words are scored

Each word scores on 4 signals:

| Signal | Points | Why |
|---|---|---|
| In the preset keyword list | +3 | "never", "secret" / "bí quyết", "sự thật", "đừng" |
| Contains a number or % | +2 | Numbers are always emphasis |
| Pause right before it | +2 to +3 | A speaker who pauses before a word is marking it |
| Unusually long vs the median | +1.5 | A stretched sound = vocal stress |

Then a minimum gap of 2.2s between zooms is enforced. Without it the video jitters non-stop.

## VI / EN differences

- Zoom amount: VI `x1.18`, EN `x1.22`. English shorts favour harder zooms; Vietnamese audiences respond better to a moderate amount.
- The keyword sets are completely different, see `presets/audience.*.json` → `zoom.emphasis_keywords`. Add keywords for your own niche — this is where the style becomes yours.

## Technical detail

The punch crop sits high (40% instead of 50% of the height) so the face is not pushed out of frame. For video already reframed to 9:16, run this skill AFTER auto-reframe.

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
  below, in this very file, then say `Logged in punch-zoom LESSONS LOG: WRONG … → RIGHT …`.
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

Kiem ship 15/11: ban cap nhat A (duyet).

Kiem ship 15/11: ban cap nhat B (tu choi).
