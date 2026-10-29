---
name: market-research-swarm
description: Deep-research a market with several agents running in parallel and produce a verified report where every claim carries a confidence label, numbers are computed rather than quoted, and TAM SAM SOM is mandatory. Runs inside Claude Code (parallel sub-agents) or ChatGPT (sequential), no API key. Use before building, to learn who is in a market, what they charge and where the gap is. Triggers on "research this market", "market research", "do research on", "compare the market".
---

# market-research-swarm

From one question to a report you can trust. Agents do the heavy lifting; you keep the
two jobs that cannot be delegated: setting the goal, and filtering the result.

## When to use

Before building anything you plan to sell, and before tearing down a specific
competitor. Building for yourself does not need deep research.

## Step 0 — Write the goal in one sentence

A report answers a decision, not "everything about X". Write first:

```
I need to know <what> about the <X> market to decide <build or not / what price / which way in>.
```

Without this sentence the agent returns a generic summary that is useful for nothing.

## Step 1 — Launch 2 to 3 research agents in parallel

Split the work:
1. Competitors + pricing — read from their own pricing pages
2. What users praise and hate — from reviews and communities
3. Market size + where the money is flowing

Tip for agent (2): go to product review sites and **filter for 1- and 2-star reviews**.
Customers who already paid and still complain means the need is real and the
incumbents are doing it badly — that may be exactly the way in.

In ChatGPT (no sub-agents) run the three briefs one after another in the same chat.

Paste this contract verbatim into EACH agent's prompt:

> Label every fact: **[CONFIRMED — with URL]** if you opened the original page
> (the vendor's pricing page, docs, announcement), or **[UNVERIFIED — reason]**.
> Prefer primary sources over aggregators. Note the "last updated" date if the page has one.
> If a number is quoted everywhere but cannot be traced to its origin, say so plainly:
> an untraceable number is a FINDING, not a citation.
> Every conversion must state its assumptions. Return raw markdown, keep full
> detail, do not summarise. Do NOT build pages, do NOT publish anything —
> the main session will synthesise.

GitHub facts (stars, license, last push) come from `gh api` or the repo page itself, not from blog posts.

## Step 2 — Synthesise; this is what makes the report trustworthy

- **Three labels on every number:** `confirmed` / `secondary` / `vendor-claimed`.
  A vendor talking about itself is vendor-claimed, however good it sounds.
- **TAM SAM SOM is mandatory**, computed as a chain of multiplications with assumptions printed:
  ```
  TAM = <people with the need> × <annual price>
  SAM = TAM × <% in the right segment, channel, language>
  SOM = SAM × <realistic % with your resources in 12 months>
  ```
  Analyst numbers size the market; this chain sizes YOUR slice. Readers may argue
  with the assumptions, not with the arithmetic.
- **Compute numbers, do not re-quote.** Costs and unit prices are converted to one unit
  (e.g. $ per 1,000 uses), with the conversion assumptions.
- **"Numbers we refused to print" section:** list circulating numbers that cannot be
  traced to a source, and why. This section builds more trust than any citation.
- Market figures state which segment definition they use; never mix them.

## Step 3 — Fill the template and self-check

Before handing in:

- [ ] Every number has a label and a source with the date read
- [ ] TAM SAM SOM with printed assumptions
- [ ] A price column for each competitor
- [ ] A refused-numbers section (no refused numbers is also an answer)
- [ ] You read it all and fixed at least one thing an agent got wrong. If you found
      nothing wrong you almost certainly did not read carefully

## Validate before building — the three cheapest ways

The report says there is a gap. Before writing a line of code, validate with at
least one of these, cheapest first:

1. **Landing page + waitlist.** Build nothing. Describe the product on one page with
   a name and email form; measure who actually signs up.
2. **Talk to 5 real customers** in the exact ICP: what they use today, what they pay,
   whether the pain is what you guessed.
3. **Pre-sell** to people who already know you or already buy from you. Someone paying
   before the product exists is the strongest signal there is.

## Step 4 — Want to show it off? Make it a page

The one-pager is the deliverable. For a nicer web page, give the report to the agent,
ask for one self-contained HTML file, then **open it and look before sending it to
anyone**: do tables overflow, do numbers match the report. Agents build pages fast and
get numbers wrong silently.

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
  below, in this very file, then say `Logged in market-research-swarm LESSONS LOG: WRONG … → RIGHT …`.
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
