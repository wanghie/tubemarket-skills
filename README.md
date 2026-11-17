# tubemarket-skills

Agent skills for **Claude Code, the Claude app and ChatGPT**: short-form video editing,
market and product research, app design, and API-key hygiene.

**No pay-per-call API key needed.** Everything runs on the Claude or ChatGPT subscription
you already have, plus free local tools — `ffmpeg`, Whisper running on your own machine
(faster-whisper), MediaPipe and Python. No skill in this repo calls a paid API.

---

## Skills

<!-- INDEX:START -->

### Video

| Skill | What it does | Say |
|---|---|---|
| [`auto-reframe`](./skills/auto-reframe) | Turn horizontal 16:9 video into vertical 9:16 (or 4:5, 1:1) that follows the face of the speaker with MediaPipe, using hard cuts instead of floaty pans. Runs locally, no API key | `make it vertical`, `convert to 9:16`, `crop for TikTok/Reels/Shorts`, `horizontal video to short`, `reframe` |
| [`broll-prompt-director`](./skills/broll-prompt-director) | Use when the user wants PROMPTS for B-roll — cutaway shots that illustrate a YouTube or talking-head video. The skill only writes prompts (no API calls); the user pastes them… | `write B-roll prompts`, `prompts for cutaway shots`, `B-roll for this video`, `Kling / Higgsfield prompt`, `Gemini image prompt for video`, `illustrate this line with a shot` |
| [`local-whisper-transcriber`](./skills/local-whisper-transcriber) | Create a word-level transcript (JSON) for any video or audio file with Whisper running locally (faster-whisper, no API key), and auto-detect a Vietnamese or English audience.… | `transcribe this video`, `get the transcript`, `word timestamps`, `prep this for a short` |
| [`punch-zoom`](./skills/punch-zoom) | Add pace to talking-head video with punch zooms on emphasised words and slow Ken Burns pushes on long passages, picking emphasis points from the transcript with separate… | `the video looks static`, `add zooms`, `punch zoom`, `make it less boring`, `add rhythm` |
| [`silence-cutter`](./skills/silence-cutter) | Cut silences, dead air and filler words (um, uh, you know / ừ, à, kiểu như) out of talking-head video, with separate filler sets for English and Vietnamese audiences. Runs… | `cut the silences`, `remove the ums`, `tighten this video`, `cut dead air`, `this video drags` |
| [`video-shorts-pipeline`](./skills/video-shorts-pipeline) | Run the full pipeline that turns one raw talking-head video into a finished 9:16 short — transcribe, cut silences and fillers, face-tracking reframe, punch zoom, burned-in… | `make this a short`, `turn this into reels`, `make a TikTok from this`, `run the full pipeline`, `edit this video for me` |
| [`word-captions`](./skills/word-captions) | Burn word-by-word highlighted captions onto a video, with separate styles for Vietnamese and English audiences — correct Vietnamese diacritics, words per line, Unicode-safe… | `add captions`, `burn subtitles`, `Hormozi-style captions`, `word-by-word subs`, `Vietnamese captions lose their accents` |

### Research

| Skill | What it does | Say |
|---|---|---|
| [`clean-room-teardown`](./skills/clean-room-teardown) | Take apart an existing product to understand how it works inside, write a clean specification, then build your own version in a fresh session that reads only the spec — the… | `teardown`, `take this product apart`, `reverse engineer`, `build something like X`, `how does product X work` |
| [`creator-product-rnd`](./skills/creator-product-rnd) | An R&D process for a new product by a creator/founder who already has an audience, shared across 6 formats (physical/digital/SaaS/service/course/community). Forces the agent to… | `creator product R&D`, `build a new product`, `what product should I sell`, `prototype this idea`, `what should a creator sell` |
| [`creator-product-teardown`](./skills/creator-product-teardown) | Tear down one specific creator product through a type switch (SaaS / Service / Physical / Digital / Community) plus a layer set specific to that type. The service branch… | `research this creator product`, `tear down product X`, `can I clone this product` |
| [`market-research-swarm`](./skills/market-research-swarm) | Deep-research a market with several agents running in parallel and produce a verified report where every claim carries a confidence label, numbers are computed rather than… | `research this market`, `market research`, `do research on`, `compare the market` |

### App / Design

| Skill | What it does | Say |
|---|---|---|
| [`app-landing-page`](./skills/app-landing-page) | Use when the user wants a LANDING PAGE for a mobile app and/or a set of APP STORE screenshots, starting from research on competitors in the same niche and extracting the DNA of… | `landing page for my app`, `app intro page`, `app landing page`, `app store images`, `app store screenshots`, `build a page to sell the app` |
| [`app-ui-designer`](./skills/app-ui-designer) | Use when the user gives ONE APP IDEA and wants good-looking, clickable, editable UI screens — the skill researches competitors, locks an aesthetic direction, then builds the… | `design an app`, `make the UI for`, `build the screens`, `app mockup`, `redesign this app` |
| [`app-ux-teardown`](./skills/app-ux-teardown) | Turn a competitor app's UX into product decisions — tear down 3 apps at once to separate industry convention from individual choice, check transfer conditions before borrowing… | `s UX into product decisions — tear down 3 apps at once to separate industry convention from individual choice, check transfer conditions before borrowing a mechanic, count friction and paywall position, flag TOXIC mechanics, and take motion numbers only from screen recordings measured with ffmpeg. Runs in Claude Code or ChatGPT plus local ffmpeg, no API key. Triggers on`, `,`, `s UX`, `break down the animations of`, `how is this app` |
| [`appstore-screenshot-builder`](./skills/appstore-screenshot-builder) | Build an iOS App Store screenshot set that meets Apple's pixel spec and passes review — competitor research, a 6-frame storyboard, captions, pixel-exact PNG render with local… | `s pixel spec and passes review — competitor research, a 6-frame storyboard, captions, pixel-exact PNG render with local Playwright, review-rule QC. Runs in Claude Code or ChatGPT plus free local tools, no API key. Use for a new store listing or when Apple rejected the old screenshots. Triggers on`, `,` |

### Dev / Agents

| Skill | What it does | Say |
|---|---|---|
| [`agent-secrets-guard`](./skills/agent-secrets-guard) | Keep API keys and passwords safe when handing work to an AI agent, and push code to GitHub without leaking anything. Use when touching an API key, secret, .env, password… | `merged but the site did not change` |
| [`skill-forge`](./skills/skill-forge) | Turn a process or hard-won lesson into a proper SKILL.md — you tell the story, the skill does the rest. Every skill, new or existing, carries a LESSONS LOG inside its own… | `write a skill`, `make a skill for this`, `fix this skill`, `skill does not trigger`, `standardise my skills` |

### Other

| Skill | What it does | Say |
|---|---|---|
| [`short-video-formats`](./skills/short-video-formats) | Write and edit short-form videos in 10 proven formats for knowledge and education channels - Straight Talk, Hands-On Explainer, Backdrop Commentary, Second Screen, Whiteboard… | `t List, Myth vs Fact, Tier Ranking, Field Test. From a topic it writes the script, shot list, on-screen text and edit notes in the format`, `s graphics, silence cuts, punch zooms and word captions. Runs locally with ffmpeg, no API key. Use when the user says`, `,`, `t video`, `tier list video`, `whiteboard video` |

<!-- INDEX:END -->

---

## Install

Requires `git`, `python3` (3.10+) and `ffmpeg`. The video skills also need a few free
Python packages.

```bash
git clone <repo-url> tubemarket-skills
cd tubemarket-skills
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt           # faster-whisper (local), numpy, PyAV pin
pip install mediapipe opencv-python       # optional: face-tracking reframe
```

The first transcription downloads a Whisper model from Hugging Face once (free, no
account). After that it runs offline.

### Claude Code

```bash
./setup            # symlinks every skill into ~/.claude/skills
```

Start a new Claude Code session and ask in plain words — the agent picks the skill from
its description (see the "Say" column). Example: `transcribe ~/Videos/clip.mp4` runs
`local-whisper-transcriber`.

### Claude app (claude.ai / desktop)

Settings → Capabilities → Skills → upload a skill folder as a `.zip`.
Research and design skills run directly in the app. Video skills need the local scripts:
run them through Claude Code, or run the commands from the SKILL.md yourself.

### ChatGPT

ChatGPT does not load skill folders. Create a Project (or a Custom GPT), paste the skill's
`SKILL.md` into the instructions and attach any files from its `references/` folder.
For video skills ChatGPT gives you the commands; the scripts in `skills/*/scripts/` run
fully offline on your machine.

`market-research-swarm` runs best in Claude Code (parallel sub-agents); in ChatGPT it runs
the same method sequentially.

---

## Why no API key

| Job | How it runs |
|---|---|
| Transcription | `faster-whisper` on your CPU/GPU, no service call |
| Cutting, zoom, reframe, captions | `ffmpeg` + Python, local |
| Research, teardown, design | the web search / browsing built into Claude or ChatGPT |
| B-roll | `broll-prompt-director` only **writes prompts**; paste them into the image/video tool you already use |

## Contributing

- One skill = one folder `skills/<kebab-case-name>/SKILL.md`; the folder name must equal
  `name:` in the frontmatter. Names describe the job (`silence-cutter`, `auto-reframe`).
- `description` must contain the trigger phrases in quotes.
- After editing:

```bash
python3 tools/build_index.py          # refresh the table above
python3 tools/check_lessons_log.py    # check every skill's LESSONS LOG block
```

- Never commit API keys, tokens, passwords, personal machine paths, customer data or media
  files (`.gitignore` blocks `.env`, `*.key`, `*.mp4`, `*.mov`, `*.wav`).

---

## Tiếng Việt (tóm tắt)

Bộ skill cho Claude Code / Claude app / ChatGPT: dựng video ngắn, nghiên cứu thị trường,
thiết kế app, giữ an toàn API key. **Không cần API key trả tiền theo lượt** — chạy bằng
gói thuê bao Claude/ChatGPT + công cụ miễn phí trên máy (ffmpeg, Whisper local).

- Claude Code: `./setup` rồi mở phiên mới, nói việc cần làm.
- Claude app: Settings → Capabilities → Skills → upload thư mục skill dạng `.zip`.
- ChatGPT: tạo Project/Custom GPT, dán nội dung `SKILL.md` vào phần Instructions.

Toàn bộ skill viết bằng tiếng Anh; agent vẫn trả lời bằng tiếng Việt nếu bạn hỏi bằng tiếng Việt.

## License

MIT — see [LICENSE](./LICENSE).
