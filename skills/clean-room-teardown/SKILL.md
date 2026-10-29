---
name: clean-room-teardown
description: Take apart an existing product to understand how it works inside, write a clean specification, then build your own version in a fresh session that reads only the spec — the two-team clean-room method the tech industry uses to learn from competitors without infringing. Runs inside Claude or ChatGPT, no API key. Triggers on "teardown", "take this product apart", "reverse engineer", "build something like X", "how does product X work".
---

# clean-room-teardown

Learn from competitors by taking them apart, not by copying. Two teams, one wall:
team A reads the original product and writes a spec, team B reads only the spec and
builds. Team B has never seen the original, so what it builds is yours.

This clean-room method has real case history in tech: a small company reverse-engineered
the IBM PC BIOS with exactly this two-team model, was challenged, and prevailed because
the build team had never seen the original code.

## When to use

After market research has picked the slice to enter. Market research answers "which
slice"; a teardown answers "how does the original work so I can build mine". In the
wrong order you take apart a product before knowing whether it is worth building.

## Step 0 — Is it worth building? Answer before spending hours

Three questions, written down:

1. Why this product, why now, and who exactly is YOUR user?
2. What is your wedge: copy the core plus improve exactly where?
3. Are you building for yourself, shipping publicly, or beyond? The further you go,
   the more strictly the clean-room rules below must hold from day one.

If the answer is "not worth it yet", stop here. That is a good outcome, not a failure.

## Step 1 — Gather sources, public sources only

Pull everything into an `input/` folder: demo videos, homepage, pricing page, docs,
screenshots, the repo if it is open source. For videos, give the agent the transcript
plus frames captured at timestamps.

**Public material only.** No cracking, no data from behind someone else's login, no
buying accounts to extract code.

## Step 2 — Decompose the core, do not describe the shell

From `input/`, have the agent split it into analysis files:

```
features.md        what the product can do, feature by feature
ui-states.md       screens, states, user flows
api-endpoints.md   which routes the product uses to talk to its server
tech-stack.md      what it runs on, what it builds itself, what it rents
pricing.md         price per plan, what is billed on
```

**Clean-room rule, non-negotiable:** in every analysis file describe in words; do NOT
paste more than 3 lines of code, and never copy any passage longer than one sentence.
Verbatim quotes are only for short factual strings (button labels, error messages).

## Step 3 — Write a clean spec

From the analysis files write `SPEC.md`: for each feature, what the user gets, what
triggers it, inputs and outputs, states, what happens on error, and **what it does NOT do**.

Test: open a NEW agent session, paste the SPEC, ask it to build one feature. If it asks
back about behaviour (rather than only about technical choices), the spec is not done.

## Step 4 — Name it yourself and find the wedge

- **Give your product a name clearly different from the original.** No `X-clone`,
  `X-port`, `my-X`. Folder names live forever in git history; a folder called
  `stripe-clone` is a confession in any future audit.
- **First-principles audit:** ask "if I did not know the original existed, what is the
  minimum spec that solves my user's pain?". Compare with SPEC: what is in SPEC but not
  in the answer, consider dropping; what is in the answer but missing from SPEC is your
  wedge. Without this step you get a 5% better copy, not a 10x different product.

## Step 5 — Build behind the wall

Open a **new folder and a new agent session**. Copy in exactly two files: `SPEC.md` and
the v0.1 task list. The first message of that session:

```
Read only SPEC.md in this folder. Do not read anything outside it.
Do not ask me about behaviour, only about technical choices. Build part 1.
```

From now on, the old session writes no code and the new session never sees the original.
If the spec is missing something, go back to the old session, fix the spec, copy the new
version across.

## Step 6 — Compare

Run the same user flow on the original and on yours and compare by eye: is the behaviour
equivalent, and where it deliberately differs (the wedge), say so. Pass → ship; fail →
back to step 5.

## Remember one line

Tear down to understand why they win, then do it differently in the gap. A conclusion of
"the same but cheaper" means you are not done — go back to the market matrix and find
the slice nobody holds.

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
  below, in this very file, then say `Logged in clean-room-teardown LESSONS LOG: WRONG … → RIGHT …`.
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
