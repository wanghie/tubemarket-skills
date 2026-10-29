---
name: silence-cutter
description: Cut silences, dead air and filler words (um, uh, you know / ừ, à, kiểu như) out of talking-head video, with separate filler sets for English and Vietnamese audiences. Runs locally with ffmpeg, no API key. Use when the user says "cut the silences", "remove the ums", "tighten this video", "cut dead air", "this video drags", or as step 2 of video-shorts-pipeline. Needs a transcript from local-whisper-transcriber first.
---

# silence-cutter

Cuts from the transcript, not just from loudness. Measuring volume only finds where *nobody speaks*; the transcript also finds where *someone speaks but says nothing*. Both get cut.

## Run

```bash
python3 skills/silence-cutter/scripts/cut.py INPUT.mp4 \
  -t work/INPUT.transcript.json \
  --mode balanced \
  -o work/INPUT.cut.mp4
```

`--mode`:
| mode | pause threshold | use for |
|---|---|---|
| `aggressive` | x0.7 | shorts/reels that need a tight pace |
| `balanced` | x1.0 | default |
| `gentle` | x1.5 | podcasts, videos that need natural breathing room |

`--keep-fillers` keeps filler words and only cuts silence.
`--dry-run` only writes the `.edl.json` keep-list so you can preview it, no render.

## VI / EN differences

This is where most foreign skills get Vietnamese wrong:

- **Silence threshold**: the VI preset uses `-34dB / 380ms`, EN uses `-30dB / 300ms`. Vietnamese speakers talk more continuously; the EN threshold cuts mid-sentence.
- **Fillers**: VI has `kiểu như là, thì là, nói chung là, tức là, đại loại`. These are 2-3 word phrases and must match as phrases — cutting the single word "là" breaks the sentence.
- **Keep sentence openers**: "So," or "Thì" at the start of a sentence is delivery, not junk. The script keeps it when a pause > 450ms precedes it.

## Output

- `INPUT.cut.mp4` — the cut video
- `INPUT.cut.edl.json` — keep-list, so later skills (word-captions, punch-zoom) can remap timestamps

## Note

After cutting, the original transcript timestamps are WRONG. Re-run `local-whisper-transcriber` on the cut file before captioning, or let `video-shorts-pipeline` handle it (it remaps without re-transcribing).

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
  below, in this very file, then say `Logged in silence-cutter LESSONS LOG: WRONG … → RIGHT …`.
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
