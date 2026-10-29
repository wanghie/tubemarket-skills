# Video Motion — image-to-video prompts (Kling 3.0 / Higgsfield)

You have the first frame. Now only add **motion**. The golden rule of image-to-video: **the image already encodes appearance/light/colour — the video prompt ONLY describes motion.** Re-describing appearance = the model drops the frame and the clip morphs.

## Pick the tool

| Shot type | Use | Why |
|---|---|---|
| A clean preset camera move on a still scene / single subject (dolly, orbit, crane, push-in) | **Higgsfield** | Strongest at a library of cinematic camera presets; "one move per clip" is home turf |
| Subtle subject/environment motion (drifting smoke, moving hair, flickering light, liquid), or several action beats | **Kling 3.0** | Better physics and motion detail, handles multi-beat prompts |
| Not sure | Give the user **both** variants | Each tool reads images differently |

Both handle short, slow 3-5s clips well — exactly what B-roll needs.

---

## KLING 3.0 — image-to-video (motion only)

Structure:
```
[Camera move] . [Timed action beats] . [One short mood phrase] .
Negative: ...
```

Rules:
- **Motion only.** No colour, no lens, no "a man wearing…" (the image has it).
- **Timed beats** for 3-5s clips, usually 2-3: `0-2s: ...` `2-4s: ...` `4-5s: ...`. Kling spends its "motion budget" on the most active beat → put the important beat first.
- **Describe the end state** to avoid stalls: say where the shot ends.
- **Spatial language** ("from left to right", "toward the camera") for stable physics.
- **One camera move.** Never orbit + zoom together.
- Slow: add `slow, steady, smooth, no abrupt motion`.

Kling camera vocabulary: `slow push-in / slow dolly-in / gentle drift left / subtle parallax / rack focus from foreground to subject / slight handheld sway / tilt up`.

Example (frame "hands typing on a laptop at night"):
```
Slow push-in toward the laptop screen. 0-2s: fingers continue typing softly,
the coffee steam drifts upward in the foreground. 2-5s: camera settles, screen glow
pulses gently. Slow, steady, intimate late-night mood.
Negative: warping, morphing, distorted hands, extra fingers, jittery, bending lines, flickering, sudden zoom
```

## HIGGSFIELD — image-to-video (preset-driven)

Higgsfield revolves around **camera presets**. Structure:
```
[Preset/camera move] on [subject in the image] , [direction & speed] , [mood] .
Negative: ...
```

Common presets (pick EXACTLY ONE):
`Dolly In / Dolly Out / Push-in / Orbit (360 or half) / Crane Up / Crane Down / Tracking / Tilt Up / Boom / Rack Focus / Slow Zoom / Parallax`.
(Avoid Whip Pan / Bullet Time / FPV for slow B-roll — those are for action.)

Rules:
- **One preset per clip.** Higgsfield recommends not mixing moves.
- Name the subject briefly as an anchor (e.g. "the laptop and hands") but do NOT re-describe its appearance.
- Add speed: `at a slow, steady creep` / `constant slow radius` (for orbit).
- Pro tip: pair **dolly-in + a still/held-expression subject** → the camera move alone creates the drama.
- 3-5s clips are the sweet spot; longer ones drift.

Example (same frame):
```
Slow dolly-in on the laptop and typing hands, camera glides forward at a steady creep,
coffee steam rising in the foreground, intimate contemplative late-night mood.
Negative: warping, morphing, distorted hands, extra fingers, jittery, flickering, sudden zoom
```

---

## Standard negative prompt (always include)

Base:
```
warping, morphing, distorted face, extra fingers, deformed hands, jittery, bending lines, flickering, sudden zoom, abrupt motion
```
Add per shot:
- Architecture/straight lines: `+ warping structure, bending walls, distorted windows`
- Text in frame: `+ garbled text, changing letters`
- Liquids: `+ floating liquid, unnatural splashes`

## Pacing slow 3-5s clips (guide)

- **3s:** one camera move, one beat (a decisive push-in). Quick cutaways.
- **4s:** one camera move + one light subject motion (steam, hair, light).
- **5s:** one camera move + 2 beats (e.g. push-in, then settle + rack focus). A "breathing" shot — fits when the speaker lands a heavy line and the audience needs a moment.

## Common failures → fixes

- **Clip morphs/deforms** → the video prompt describes appearance. Delete it all, keep only motion.
- **Stalls / does not move** → the first frame is packed with no room to move, or the end state is missing. Fix the frame or add "ends with…".
- **Jerky/fast motion** → add `slow, steady, smooth`; reduce the number of beats.
- **Broken faces/hands** → show less face/hand in the first frame, or strengthen the negative.
- **Several moves tangled** → split into several clips, one move each.
