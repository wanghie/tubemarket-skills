---
name: video-shorts-pipeline
description: Run the full pipeline that turns one raw talking-head video into a finished 9:16 short — transcribe, cut silences and fillers, face-tracking reframe, punch zoom, burned-in captions — tuned for a Vietnamese or English audience. Runs locally (ffmpeg + local Whisper), no API key. Use when the user hands over a video file and says "make this a short", "turn this into reels", "make a TikTok from this", "run the full pipeline", "edit this video for me".
---

# video-shorts-pipeline

Orchestrator. Calls the other five video skills in the right order and carries timestamps between steps.

## Run

```bash
bash skills/video-shorts-pipeline/scripts/pipeline.sh INPUT.mp4 --audience en
```

Options:

| Flag | Default | Notes |
|---|---|---|
| `--audience` | `auto` | `vi`, `en`, or `auto` (detected from the transcript) |
| `--outdir` | `<input folder>/sf-out` | |
| `--mode` | `balanced` | cutting strength: `aggressive` / `balanced` / `gentle` |
| `--aspect` | `9:16` | `4:5` for Facebook/LinkedIn, `1:1` for square feeds |
| `--density` | `0.12` | zooms per second |
| `--skip` | — | e.g. `--skip zoom,reframe` |
| `--dry-run` | — | only write plan files (edl/reframe/zoommap/ass), no render |

## Order and why

```
1  transcribe   → transcript.json (word-level)
2  cut-silence  → cut.mp4 + edl.json
   remap        → cut.transcript.json   (does NOT run Whisper again)
3  reframe      → vertical.mp4          (9:16 following the face)
4  punch-zoom   → zoom.mp4              (after reframe, so zooms happen on the vertical frame)
5  captions     → final.mp4             (last, so text is never cropped away)
```

The `remap` step is the biggest saving: after cutting, every transcript timestamp is wrong. Instead of re-running Whisper large-v3 (minutes), the script shifts the old timestamps onto the new timeline using the EDL, in under a second.

## Recommended workflow

Run `--dry-run` first, look at the 3 plan files, adjust the preset if needed, then render for real:

```bash
bash skills/video-shorts-pipeline/scripts/pipeline.sh raw.mp4 --audience en --dry-run
# review sf-out/raw.cut.edl.json, raw.reframe.json, raw.zoommap.json
bash skills/video-shorts-pipeline/scripts/pipeline.sh raw.mp4 --audience en
```

An existing transcript is reused, not re-transcribed — so the second run is much faster.

## Limits

- One speaker, one camera angle. Two-person interviews need active-speaker detection, not built yet.
- It does not pick the best moment from a long video. It edits the whole video you give it; to cut a highlight from a 30-minute video, rough-cut it first.

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
  below, in this very file, then say `Logged in video-shorts-pipeline LESSONS LOG: WRONG … → RIGHT …`.
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
