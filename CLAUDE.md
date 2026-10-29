# Rules for agents working on this repo

- New skill: `skills/<kebab-case-name>/SKILL.md`; folder name must equal `name:` in the frontmatter.
- `description` must contain the trigger phrases in quotes.
- After editing run `python3 tools/build_index.py` and `python3 tools/check_lessons_log.py`.
- No skill may require a pay-per-call API. Only Claude/ChatGPT subscriptions + free local tools.
- Never commit API keys, tokens, passwords, personal machine paths, customer data, or anyone's personal voice/stories.
- Never commit media (`.mp4`, `.mov`, `.wav`).
