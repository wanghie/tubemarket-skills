---
name: local-whisper-transcriber
description: Create a word-level transcript (JSON) for any video or audio file with Whisper running locally (faster-whisper, no API key), and auto-detect a Vietnamese or English audience. Use when the user wants the spoken words, per-word timestamps, or before running any other video skill here (silence-cutter, word-captions and punch-zoom all read this file). Triggers on "transcribe this video", "get the transcript", "word timestamps", "prep this for a short".
---

# local-whisper-transcriber

Step 0 of every pipeline in this repo. The other skills never read pixels — they read this JSON.
Runs fully offline after the model downloads once; no API key, no per-call cost.

## Run

```bash
python3 skills/local-whisper-transcriber/scripts/transcribe.py INPUT.mp4 \
  --audience auto \
  -o work/INPUT.transcript.json
```

`--audience`:
- `vi` — force Vietnamese and load the Vietnamese initial prompt (fewer errors on names and terms)
- `en` — force English
- `auto` (default) — let Whisper detect, then re-classify by tone-mark density in the result

`--model base|small|medium|large-v3` overrides the preset model (smaller = faster, less accurate).

## Output

```json
{
  "audience": "vi",
  "duration": 61.4,
  "fps": 30.0, "width": 1920, "height": 1080,
  "words": [{"start": 0.12, "end": 0.41, "word": "chào", "prob": 0.98}],
  "segments": [{"start": 0.1, "end": 4.2, "text": "..."}]
}
```

## Field notes

- Vietnamese: use `large-v3`. Smaller models (`base`, `small`) get word timestamps noticeably wrong on Vietnamese because syllables are short — captions drift visibly. Do NOT save here.
- Apple Silicon: CPU with `compute_type=int8` is fast enough (~1/3 real time with large-v3). No CUDA needed.
- Loud background music: separating vocals first improves accuracy a lot.

## Requirements

`ffmpeg`, `ffprobe`, `pip install faster-whisper "av<16"` (PyAV 16+ breaks faster-whisper 1.2's audio decoder).

## When the ASR gives no per-word timestamps

Some ASR paths return TEXT only: sherpa-onnx Whisper (ONNX), most cheap cloud tiers, and any hand-typed transcript.

Use `lib/align.py` to rebuild timestamps from the audio itself:

```bash
ffmpeg -y -i INPUT.mp4 -vn -ac 1 -ar 16000 -c:a pcm_s16le audio.wav
python3 lib/align.py audio.wav \
  --text "Google just released 15 AI tools" \
  --audience vi --source INPUT.mp4 -o transcript.json
```

How it works: find energy peaks in the audio envelope — each peak is a syllable nucleus — then assign syllables to words in order.

**This works far better for Vietnamese than English.** Vietnamese is monosyllabic and syllable-timed: one word is one syllable, each syllable has a clear energy peak, and syllables are about equally long, so peak ↔ syllable ↔ word is nearly one-to-one. English is stress-timed with uneven syllables — there it is only a fallback.

Three details make it work on real files:

- **Two separate thresholds.** A loose peak threshold (max−22dB) so quiet syllables still count; a stricter speech-region threshold (max−18dB) because room tone and breaths sit just under the loose one.
- **Only accept speech regions ≥60ms.** A single frame over threshold is a codec click at the start/end — taking it as a boundary stretches the first and last words over the whole clip.
- **Linear rescale onto the speech region.** Peak picking often misses the tail of the last syllable, so the last caption ends early and the cut eats into the word. One rescale fixes both ends.

Accuracy: good enough for captions and punch zoom. NOT good enough for `aggressive` cutting — use `--mode gentle` when the transcript came from this path. Prefer real Whisper word-level output whenever you have it.

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
  below, in this very file, then say `Logged in local-whisper-transcriber LESSONS LOG: WRONG … → RIGHT …`.
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
