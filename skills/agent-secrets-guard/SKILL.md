---
name: agent-secrets-guard
description: Keep API keys and passwords safe when handing work to an AI agent, and push code to GitHub without leaking anything. Use when touching an API key, secret, .env, password manager or environment variable, when connecting a new API or MCP, before a commit or push, when setting up CI, when letting a second person or another agent into the repo, and when "merged but the site did not change".
---

# agent-secrets-guard

Hand work to an agent without handing over the keys, and push code without leaking anything.

---

## When to use

Read this file before doing any of these:

- Touching an API key, secret, `.env`, environment variable
- Connecting a new API or MCP to an agent
- Committing or pushing, especially the first time in a project
- Letting a second person, or another agent, into your repo
- Setting up CI, or deciding which rules need automatic checks
- Hearing "merged but the site did not change"

---

## 1. Two kinds of key, do not mix them up

A **public key** is like a bank account number. Anyone may know it.

A **private key** (secret key) is like your online-banking password. Leaked means lost.

Many services call both an "API key". One-line rule:

> Any key starting with `sk_`, `sb_secret_`, `secret`, `service_role`, or that the
> service calls a **secret**, **never leaves your machine**.

---

## 2. Where to store it, three tiers

| Tier | Tools | Use when |
|---|---|---|
| Password manager | 1Password, Bitwarden, Doppler | Source of truth for the team. The agent must ask permission every time |
| The platform's own secrets | Vercel env, GitHub Actions secrets, Supabase Vault, Cloudflare Workers secrets | A key used by one service only |
| Dedicated secret store | AWS Secrets Manager, Google Secret Manager, HashiCorp Vault | Many environments, need an audit log of who took which key when |

On your machine: macOS Keychain, `.env` in `.gitignore` with no exceptions, and
`.env.example` containing **variable names only, never values**.

### Four places people actually lose keys

```
export API_KEY=...   in .zshrc
messaging the key to yourself on Slack / WhatsApp
keeping it in Notion, Google Keep, Apple Notes
the clipboard — copied, then forgotten
```

### Clear the clipboard after using a key

The clipboard is the one surface the OS does not guard. Any process can read it,
silently, without a trace. Universal Clipboard pushes it over iCloud to your iPhone
and iPad. It stays there until overwritten.

Run right after you are done with the key:

```bash
pbcopy < /dev/null
```

---

## 3. Four rules when handing work to an agent

Copy these four into your project's `AGENTS.md`.

### Rule 1. Give the variable name, not the value

```
WRONG   Call the Linear API for me, the key is lin_api_a1b2c3...
RIGHT   The key is in LINEAR_API_KEY. Read it from process.env, never print it.
```

A key pasted into chat lives forever in the conversation history and third-party
logs. You cannot delete it. A variable name is harmless to anyone.

### Rule 2. Do not let it print the key

```
WRONG   console.log('key:', process.env.API_KEY)
        echo $API_KEY
        curl -v ...                    -v prints the Authorization header too

RIGHT   echo ${API_KEY:0:8}...                     first eight characters only
        [ -n "$API_KEY" ] && echo "key present"    check presence only
        curl -s ... -o /dev/null -w "%{http_code}" status code only
```

The terminal may be screen-shared or recorded. Platform and CI logs keep it too.

### Rule 3. Scan before pushing, even private repos

```bash
# gitleaks: free and open source (brew install gitleaks)
gitleaks git --staged --redact     # scan what is about to be committed
gitleaks git --redact              # scan the whole repo history
```

It recognises OpenAI/Anthropic keys, GitHub tokens, AWS keys, Slack tokens, PEM
private keys… without printing the value (`--redact`).

Any finding means stop. Private today, open-sourced tomorrow, leaked forever.

### Rule 4. Leaked? Rotate the key, do not chase the commit

**Git keeps every blob forever:**

- Deleting the file in a later commit does **not** remove it from history
- Force-pushing after `git filter-repo` does **not** remove it from existing clones
- Making the repo private does **not** remove it, because forks share the object store

The only thing that works: go to the service, revoke the old key, create a new one.

---

## 4. Let the agent use a key without holding it

The model to aim for, instead of `.env`:

```
IN .env                             IN A PASSWORD MANAGER
agent needs a key                   agent needs a key
   ↓                                   ↓
it opens .env itself                it only has the vault reference
   ↓                                   ↓
has the key, calls the API          the manager receives the request
                                       ↓
Nobody is asked.                    YOUR MACHINE ASKS FOR YOUR FINGERPRINT
No step in between.                    ↓
No trace left.                      hands the key to that one command
                                    the value never shows on screen
```

One-time setup (1Password example): `Settings` → `Developer` → enable `Command-Line Interface`.
Then tell the agent:

```
Move every key currently in my .env into 1Password,
organised into one vault per project.
Do not print the value of any key.
```

**Trade-off:** slower, because you touch the fingerprint reader every time the agent
needs a key. A project with no sensitive data is fine with `.env`. Customer data,
money, bank accounts — the inconvenience is worth it.

---

## 5. A key that lives in exactly one place is a risk

> Your most important key must live in **at least two places**, and **one of them must
> ask a human** before handing it out.

Check your project now: how many places does each key live?

---

## 6. Three things you never commit

**Secrets.** No API keys, no tokens, no `.env`.

**Real user lists.** No `.xlsx` or `.csv` with real names and emails.

**Heavy files.** Video, raw images, renders. They go through separate storage, not git.

Before each commit look at `git status` once, and `git add <specific file>` rather
than `git add -A`.

---

## 7. Working with a second person, and with other agents

### Put rules where the agent actually reads them

An agent only auto-loads `AGENTS.md` or `CLAUDE.md` at the **root of the repo it is
standing in**. Great instructions in another repo are never read.

### Write a "stop and ask a human" list

Having technical permission does not mean the agent may decide. For example:

1. Running any command with `--apply`, because that flag writes for real
2. Pushing straight to `main`
3. Touching user identity
4. Deleting or editing data other people submitted
5. Rotating the session signing key, because that logs everyone out

### Make the agent pull the latest before working

```bash
git checkout main && git pull
```

Working on a stale copy means following rules that were already changed, and the
mistake only shows after the push.

---

## 8. Documentation is not a guarantee

Writing rules into `CONTRIBUTING.md` stops nobody. Only CI stops mistakes.

Minimum checks for a small project, on every pull request:

```yaml
- No forbidden files, no key-like strings in the repo
- Existing tests do not break
- Generated files match their source
- Every path to an external file points to something real
```

Every red step must **print what to do**, not just that it failed.

---

## 9. Merged does not mean deployed

Deploy platforms can block by **commit author**. Vercel only builds when the commit
author is on the team. Otherwise the deployment shows `Deployment was blocked`; the
code is correctly on `main`, yet the site does not change.

It blocks `github-actions[bot]` too, i.e. your own automated workflows.

When you hear "merged but the site did not change", **check deploy permissions before
hunting for bugs in the code**.

---

## 10. The rule behind everything: silent failure is the most expensive kind

> Every path needs a place that reports when something that should have happened did not.
> Without it, silence reads as success.

Apply it to everything you build: after writing, read back and compare. After
uploading, measure the size again. After merging, check it actually went live.

---

## Quick reference

| Situation | Do |
|---|---|
| Just copied a key | `pbcopy < /dev/null` when done |
| Agent asks for a key to call an API | Give the variable name, not the value |
| About to push for the first time | Scan per Rule 3, check `.gitignore` has `.env` |
| Pasted a key into chat by mistake | Rotate it now. Do not delete commits, it is useless |
| New person joins the repo | Write `AGENTS.md` at that repo's root |
| Merged but the site did not change | Check deploy permissions first, do not touch code |
| Suspect a file uploaded incomplete | Read back its size in storage, compare with the local copy |

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
  below, in this very file, then say `Logged in agent-secrets-guard LESSONS LOG: WRONG … → RIGHT …`.
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
