---
name: word-captions
description: Burn word-by-word highlighted captions onto a video, with separate styles for Vietnamese and English audiences — correct Vietnamese diacritics, words per line, Unicode-safe fonts. Runs locally with ffmpeg/libass, no API key. Use when the user says "add captions", "burn subtitles", "Hormozi-style captions", "word-by-word subs", "Vietnamese captions lose their accents". Needs a transcript from local-whisper-transcriber.
---

# word-captions

Writes an `.ass` file with one event per word (the line stays put, the spoken word changes colour and scales up 8%), then burns it into the video.

## Run

```bash
python3 skills/word-captions/scripts/captions.py INPUT.mp4 \
  -t work/INPUT.transcript.json \
  --style bold \
  -o work/INPUT.captioned.mp4
```

`--style bold` (thick outline, shadow) or `--style clean` (thin outline, no shadow).
`--position 0.22` moves captions up/down (fraction of frame height).
`--ass-only` writes only the `.ass` file so you can fine-tune it in Premiere/CapCut.

## VI / EN differences — the most important part of this skill

| | Vietnamese audience | English audience |
|---|---|---|
| Upper case | **NO** full caps | YES, ALL CAPS |
| Words / line | 4 | 2 |
| Max characters / line | 22 | 16 |
| Default font | Be Vietnam Pro | Montserrat |

Two reasons:

1. **Upper-case Vietnamese breaks diacritics.** Accented capitals (Ế, Ữ, Ộ) stack marks high; many fonts overlap or clip them at the top edge, and reading slows down visibly. The VI preset capitalises **only the highlighted word**, keeping emphasis without hurting legibility.
2. **Vietnamese words are shorter.** Most are 1-2 syllables. Two words per line like the EN standard looks empty and jumps lines constantly; four words per line gives the same density.

The script picks the first installed font from a priority list; with no Vietnamese font it falls back to a full-Unicode font instead of rendering boxes.

## Line breaks follow speech rhythm

A caption line always breaks at a pause > 0.8s, even before it is full. A caption that spans a silence lies about the rhythm — viewers see words frozen while nobody talks.

## Requirements

`ffmpeg` built with `libass` (the default Homebrew build has it).
Fonts: `brew install --cask font-be-vietnam-pro font-montserrat` (or install them from Google Fonts).

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
  below, in this very file, then say `Logged in word-captions LESSONS LOG: WRONG … → RIGHT …`.
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
