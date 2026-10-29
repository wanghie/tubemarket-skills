---
name: skill-forge
description: "Turn a process or hard-won lesson into a proper SKILL.md — you tell the story, the skill does the rest. Every skill, new or existing, carries a LESSONS LOG inside its own SKILL.md so corrected mistakes do not come back. Works in Claude Code, the Claude app and ChatGPT, no API key. Triggers on \"write a skill\", \"make a skill for this\", \"fix this skill\", \"skill does not trigger\", \"standardise my skills\"."
---

# skill-forge

A skill is not a nice article. It is the rule sheet an agent reads IN THE MIDDLE of
work, when it is in a hurry and wants to cut corners. Write for that moment, not for
someone reading at leisure.

Three things decide whether a skill lives or dies: **does the description make the
agent trigger it at the right time**, **can each step be checked**, and **are past
corrections recorded in the file**. Without the third, every session repeats the same
mistake.

## When to use

- A process you repeat by hand, re-pasting the same prompt every time
- A real failure you never want to happen twice
- A skill that exists but does not trigger, triggers at the wrong time, or a whole set to standardise

**Do not use when:** the job happens once, or the rules change every week. A skill is
what settles, not a place to track work in progress.

## Step 0 — Collect all 6 pieces before writing a word

The user only has to tell the story. The agent's job is to **check all 6 pieces** and
ask for whichever is missing.

| # | Piece | Question if missing |
|---|---|---|
| 1 | What the skill does, one sentence | "What job does this skill do for you, in one sentence?" |
| 2 | Trigger phrases | "What will you type when you need it? Give 3-5 REAL sentences" |
| 3 | Process | "Walk me through how you do it by hand, messy is fine" |
| 4 | Hard rules | "What is absolutely forbidden? Has it ever broken because someone skipped it?" |
| 5 | Output | "What comes out at the end: which file, what format, who reads it?" |
| 6 | When not to use | "When should this skill NOT be used?" |

Ask at most **3 questions per turn**, grouped; **never re-ask what the user already
said**. If they say "just do it", fill assumptions yourself, write the skill, and print
an `## Assumptions I filled in` section at the end for them to fix — do not wait.
Piece 4 matters most: rules drawn from real incidents get followed, rules from books get
skipped — if you cannot get one, ask "how did this go wrong last time?".

## Step 1 — Write the frontmatter first, and write it for a MACHINE

This is the only part always in the agent's context. The body is read only AFTER the
skill triggers. A wrong description makes the whole file pointless. Three-clause formula:

> `[What it does, with its distinctive hard constraint]. [Use when <situation>]. [Triggers on "phrase 1", "phrase 2", "phrase 3"].`

- `name`: kebab-case, English, describes the job (e.g. `silence-cutter`), identical to the
  folder name. Third person, describes the skill, never "I"
- Use **the exact phrases users really type**, in every language they use; keep it under
  ~500 characters — stuffing everything in dilutes the signal
- State what makes it DIFFERENT from sibling skills. WRONG/RIGHT samples: [`references/quick-reference.md`](./references/quick-reference.md)

## Step 2 — One thesis line right under the title

`# skill-name`, new line, then 2-3 sentences with the core insight — not a summary, but
**the line that lets the agent grasp the spirit** so it handles cases the file never lists.

## Step 3 — The skill's step 0 is always "set the goal" or "is it worth doing"

Every good skill blocks at the start, before effort is spent. Research or production
skills require a one-sentence goal; build or long-commitment skills require an answer to
"is it worth doing" and allow the conclusion **stop** — stopping is a good outcome, not a failure.

## Step 4 — Split into steps, one checkable action each

- Number them. Titles start with an **imperative verb** and describe the result, not the topic
- Each step has a **done condition** you can see, and a **copy-pasteable block**: a prompt
  for a sub-agent, a bash command, a table, or a formula
- Prompts handed to sub-agents are framed with `>` like a contract, including the return
  format and what it must NOT do on its own
- Independent work → say plainly "launch 2-3 agents in parallel" (or "run them in sequence"
  where sub-agents are unavailable), with a clear split

## Step 5 — Hard rules: name them, pair WRONG/RIGHT, tie them to real incidents

- Name each rule so it can be called back: "Clean-room rule", "Rule 3 — scan before
  push". Named rules get recalled; unnamed rules drift away
- Important rules as a one-line blockquote; prefer a **two-column WRONG/RIGHT pair** over
  a paragraph. Tie each heavy rule to one real failure, one line is enough
- State trade-offs **plainly**: "this is slower because…; small projects do not need it".
  Skills that hide trade-offs get abandoned halfway. Separate **measured risk** from
  **vague threats**

## Step 6 — Self-check list, then one line to remember

A `- [ ]` checklist right before delivering, each line checkable by eye, with at least
one line that **forces a human to read**:

> - [ ] You read it all and fixed at least one thing the agent got wrong. If you found
>   nothing wrong you almost certainly did not read carefully

Skills over ~200 lines get a two-column quick-reference table (situation → do), in a
side file if SKILL.md is full. Close with `## Remember one line` if there is one worth keeping.

## Step 7 — Apply the LESSONS LOG block, to NEW and EXISTING skills

A finished skill ends with two blocks: `## This skill must improve itself` (the 5-point
version), then `## LESSONS LOG`. Block 1 only "suggests updates" — at session end the
feedback is gone; block 2 is WHERE IT IS WRITTEN, and it must live INSIDE SKILL.md
because the agent loads only SKILL.md on trigger. **The mechanism does not spread on
its own**: if nobody applies it, old skills never get a log. 7b says who and when.

### 7a — One master copy, copy it, never retype

The master block is [`references/lessons-log-block.md`](./references/lessons-log-block.md),
28 lines, empty table. Copy it verbatim, replacing only `<skill-name>` with the target skill:

```bash
D=<repo>/skills/auto-reframe                                  # target skill folder
MASTER=<repo>/skills/skill-forge/references/lessons-log-block.md
printf '\n' >> "$D/SKILL.md" && sed "s/<skill-name>/$(basename "$D")/" "$MASTER" >> "$D/SKILL.md"
```

No retyping, no paraphrasing. Inside the block **no reference outside the target file**
("see Step 7", "rules in skill-forge"): child skills have no Step 7, so such a reference
is dead the moment it is pasted — the block must carry its own 3 rules and the cap.

### 7b — Who applies it, when

| Who | When | What |
|---|---|---|
| Agent running this skill | Generating a NEW skill | Paste the empty block + the 5-point footer when writing the file |
| Agent running ANY skill | Just corrected on a skill that has no log | Paste the EMPTY block at the end of that skill's SKILL.md in the repo, then write the first row — in that same session, not later |
| Agent running this skill | Asked to "fix the skill", "standardise the skills" | Sweep the repo, paste the EMPTY block wherever it is missing. **Never** invent rows for a skill that was never corrected |

An EXISTING skill only strictly needs the LESSONS LOG block: its 3 rules let it stand
alone. Add the 5-point footer at the next edit if there is room under 300 lines. After
pasting, run the checker in the repo instead of eyeballing:

```bash
python3 tools/check_lessons_log.py
```

It catches: missing block, a table that is not the 4 columns `Date | Source | WRONG | RIGHT`,
more than 10 rows, sources other than `user · review · measured`, a block that differs from
the master, and files over 300 lines. Over 300 → **tell the user**, never cut existing
content to make room.

### 7c — Which copy to write to: THE FILE IN THE REPO

`~/.claude/skills/<skill-name>` is a **symlink** into the repo — editing the repo file takes
effect immediately, nothing to copy:

```
<repo>/skills/<skill-name>/SKILL.md
```

- **Not everything in `~/.claude/skills` is a symlink.** `readlink` before trusting it;
  a real folder should be moved into the repo and `./setup` re-run, never edited in place
- After writing, `git -C <repo> diff` must show the new row. No diff means nothing was written

### 7d — The logging contract: one copy, it lives here

> **Priority.** This section 7d is the real one. Footer point 2, the quick reference and
> the block pasted into child skills only restate 7d; wherever they differ, **7d WINS**
> and the other place gets fixed, not 7d.

Three actions, done IN THE SESSION where the correction happened:

1. **Fix the output — ALWAYS, unconditionally.** Fix every place of the same kind, not
   just the one pointed at: re-scan the whole piece, the whole file, everything sent this session
2. **Write one row into the log — CONDITIONALLY, only when the mistake is RULE-WORTHY.**
   Write it into the log of the skill that produced the corrected passage, not the skill
   that was called first
3. **Say it**: `Logged in <skill-name> LESSONS LOG: WRONG … → RIGHT …`

A ONE-OFF stops after action 1. Decide with exactly one question, never guess:

> Would this mistake come back with a different input? Yes → log it. No → only fix the output.

| Log it (RULE-WORTHY) | Only fix the output (ONE-OFF) |
|---|---|
| About HOW to work: tone, pronouns, format, order, what to drop | Tied to this run's data: wrong name, number, link |
| Uses future words: "next time", "from now on", "always", "never" | A change of preference, not a fix: "make a shorter version" |
| Corrected for the second time | Picking between two equally good options |

If it fits neither column, ask "every time from now on, or just this once?" — one question
is cheaper than a wrong hard rule in the log.

### 7e — Write one row, and keep the log from bloating

```
| YYYY-MM-DD | user · review · measured | WRONG: the agent's specific behaviour | RIGHT: the replacement behaviour, doable at once |
```

**The SOURCE column is required**, exactly three values: `user` (the user actually said
it) · `review` (a review pass caught it) · `measured` (a tool run showed it). Never present
the agent's own conclusion as if the user said it — a made-up source is worse than no row;
if unsure, use the weaker source. The WRONG column describes **observable behaviour**:
"bland writing" cannot be checked, "opens the short with a rhetorical question" can be
seen in a second.

- Read the log before adding. A near-identical row = corrected **a second time** → do NOT
  add a row; promote it to a named hard rule in the skill body (Step 5) and remove it from the log
- Log full and a new row arrives → merge rows on the same topic, or promote the most
  repeated row to a hard rule. **Never delete a row just because it is old**
- A log row that contradicts a rule in the body → the body is wrong, fix the body
- Nearing 300 lines → move reference material to a side file, **never cut the log**

## Step 8 — Write the file to the right place

The real copy is the one in the repo (Step 7c); `~/.claude/skills/<skill-name>/SKILL.md`
is only a symlink to it, and is where Claude Code loads it from.

- One skill per folder, folder name **identical** to `name` in the frontmatter. Side files
  (templates, examples, scripts) sit next to SKILL.md and are **linked from SKILL.md**
- SKILL.md under 300 lines AND with room for the log to reach its 10-row cap, i.e. the
  body stops under 261 lines. Longer → move reference material to a separate file
- Skills that carry a personal voice or private stories belong in a private repo, never a public one
- Claude.ai / ChatGPT cannot write into the account directly: build the file and hand it
  to the user to upload (Claude: Settings → Capabilities → Skills; ChatGPT: paste into a Project/GPT)

## Step 9 — Test triggering before calling it done

Open a **new agent session** and try three prompts: the exact trigger phrase → must
trigger; the job described in other words → should trigger; a sibling skill's job →
must **not** trigger. What to do on a miss: the "Trigger test" section in
[`references/quick-reference.md`](./references/quick-reference.md).

## Writing rules for every skill produced here

- Short sentences, no emoji, no marketing. No sentence that only links ideas
- Never write "be professional", "be careful" — those are not instructions. Prefer
  tables and command blocks over paragraphs
- Wrap around column 80 for terminal reading
- A skill talks to the agent, not to a reader. Instructions, not a lecture

## Before delivering: run the checklist

The four lines below are the ones where a miss means broken. The full 13-line checklist
and the 12-situation quick reference are in [`references/quick-reference.md`](./references/quick-reference.md) — **open it and run it all**.

- [ ] `## LESSONS LOG` copied from `references/lessons-log-block.md`, 4-column table
      `Date | Source | WRONG | RIGHT`, empty unless there was real feedback
- [ ] `python3 tools/check_lessons_log.py` clean, `wc -l SKILL.md` under 300
- [ ] Ran the 3-prompt test from Step 9 in a new agent session
- [ ] Printed "Assumptions I filled in" if anything was assumed

## Remember one line

A skill makes the agent remember the rules and follow the process. It does not make the
result correct. Three jobs stay human: set the goal before delegating, read the result and
fix what is wrong before trusting it, and approve before anything leaves the machine.

## This skill must improve itself

1. **Read the LESSONS LOG before working.** The log at the end of this file is hard
   rules, not notes. Read all of it before writing the first word.
2. **When corrected, act in that same session**, per the Step 7d contract and without
   paraphrasing it: ALWAYS fix the output, log one row ONLY WHEN the mistake is
   RULE-WORTHY, then say you logged it. Do not leave it for the end of the session, do not
   stop at "suggesting". If two places disagree, Step 7d wins.
3. **Evaluate after each run.** Score briefly against the checklist: which step was
   missed, what the user had to fix by hand. Things worth fixing that were not corrections
   → suggest the user update this SKILL.md directly.
4. **Look things up now and then.** Where skills live, length limits and how agents load
   skills change between tool versions. Details a few months old should be re-checked at the source.
5. **When you do not know, ask a person.** Say plainly what is out of reach and point the
   user to who can help. Real people are a source of help, not only documentation.

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
  below, in this very file, then say `Logged in skill-forge LESSONS LOG: WRONG … → RIGHT …`.
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
| 2026-09-22 | review | Step 7 only required pasting the block into NEW skills; existing skills were never patched so they never got a log | 7b says who patches and when — any agent that was just corrected on a skill without a log pastes the empty block there and logs the first row in the same session |
| 2026-09-22 | review | The block pasted into child skills said "cap 12 rows" and pointed to "rules in Step 7", while child skills have no Step 7 and the real cap is 10 | One master copy `references/lessons-log-block.md`, self-contained with its 3 rules and the cap |
| 2026-09-22 | review | Step 7 said log "only if RULE-WORTHY" while footer item 2 said log unconditionally — two contracts clashing | One contract in 7d with a priority order: ALWAYS fix the output, log ONLY WHEN rule-worthy |
| 2026-09-22 | review | Presented the agent's own conclusion as if the user had said it, though no user message said so | Source column required with exactly `user · review · measured`; never attribute to the user without a message to point at |
| 2026-09-22 | review | Rolled a new mechanism across the whole skill set in one pass before a sample was approved | Change one sample skill first, approve the contract, then copy it to the rest |
