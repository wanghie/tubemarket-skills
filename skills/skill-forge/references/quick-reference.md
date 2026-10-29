# skill-forge — quick reference

Reference material split out of `SKILL.md` so the main file keeps room for its LESSONS
LOG to reach the 10-row cap. Open this at Step 9 and before delivering a skill.

## Checklist before delivering a skill

- [ ] `name` is kebab-case and identical to the folder name
- [ ] `description` has all three clauses and at least 3 phrases users really type
- [ ] A thesis line under the title, and a "When to use" section including when NOT to
- [ ] A blocking step 0 (set the goal, or "is it worth doing")
- [ ] Every step has an imperative verb and a visible done condition
- [ ] At least one copy-pasteable block
- [ ] At least one named hard rule with a WRONG/RIGHT pair
- [ ] A self-check list including one line that forces a human to read
- [ ] The 5-point footer `## This skill must improve itself`
- [ ] `## LESSONS LOG` copied verbatim from `references/lessons-log-block.md`,
      4-column table `Date | Source | WRONG | RIGHT`, empty unless there was real feedback
- [ ] `python3 tools/check_lessons_log.py` clean in the repo holding the skill
- [ ] Ran the 3-prompt test from Step 9 in a new agent session
- [ ] Printed "Assumptions I filled in" if anything was assumed

## WRONG/RIGHT pairs

Description:

```
WRONG   A skill that helps with market research professionally.
RIGHT   Deep-research a market with several agents in parallel, TAM SAM SOM
        mandatory. Use when you need to know who is in a market, what they
        charge, where the gap is. Triggers on "research this market",
        "market research", "do research on".
```

The WRONG one fails because it contains no phrase a user would type, and does not say
what the skill enforces.

Step title:

```
WRONG   ## Step 2 — Analyse the data
RIGHT   ## Step 2 — Convert every unit price to one unit, then print the conversion assumptions
```

## Trigger test — what to do on a miss

| Test prompt | Expected | On a miss |
|---|---|---|
| Exact trigger phrase from the description | Must trigger | Check `name` equals the folder name and the symlink is alive (`readlink`) |
| The job in other words, no trigger phrase | Should trigger | Add the user's real phrasing to the description, leave the body alone |
| The closest sibling skill's job | Must **not** trigger | Add a distinguishing clause ("DIFFERENT from <other skill> in that…") to the description |

## Quick reference

| Situation | Do |
|---|---|
| User describes a long process | Check the 6 pieces from Step 0, ask for the missing ones in one go |
| User says "just do it" | Write it, print the assumptions section at the end |
| User says "that's wrong", "next time don't…" | Fix the output; log it if RULE-WORTHY; say you logged it |
| Unsure whether feedback is one-off or a rule | Ask one question: every time from now on, or just this once |
| A skill was just corrected and has no log | Paste the empty block from `lessons-log-block.md` into its SKILL.md in the repo, then write the first row |
| Log already has 10 rows | Merge same-topic rows, or promote the most repeated row to a hard rule and remove it |
| Pasted the log, unsure it is right | `python3 tools/check_lessons_log.py` |
| SKILL.md over 300 lines after pasting the log | Tell the user, move reference material to `references/`, **never cut the log** |
| Skill does not trigger | Fix the description with real phrases, leave the body alone |
| Skill triggers on the wrong job | Add a distinguishing clause to the description |
| A rule sounds good but has no real incident | Ask "how did this go wrong last time?" |
| Editing an existing skill | Keep `name`, only patch what failed the checklist |
