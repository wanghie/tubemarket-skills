# Style DNA — extracting a style from references

Goal: turn the user's references (images/videos/links/descriptions) into a **Style DNA card** of English phrases usable directly in image prompts. The card is locked once and applied to the whole B-roll set for consistency.

## Ground rules

- **Look first, talk second.** Images: open them. Videos: watch or read frame descriptions. NEVER invent.
- **Extract what repeats, drop what is random.** If all 3 references are dark + yellow lamps + slow camera → that is the DNA. One stray blue reference → ignore it.
- **Use technical keywords**, not vague adjectives. "Beautiful" is useless; "warm-amber grade, crushed blacks, soft window key" is usable.
- When references conflict → ask the user which one wins, or pick the one they said they "like most".

## 9 axes to extract

### 1. Colour / Grade
Dominant tones, saturation, where shadows/highlights are pushed.
Vocabulary: `warm amber / teal-orange / desaturated / muted earth tones / high contrast / crushed blacks / lifted shadows / filmic LUT / monochrome / pastel`.

### 2. Light
Source, direction, softness, contrast ratio.
Vocabulary: `soft single key light / hard directional light / window light / golden hour / blue hour / practical lamps / rim light / low-key / high-key / volumetric god rays / neon glow / candlelit`.

### 3. Lens & depth of field
Perceived focal length and depth.
Vocabulary: `35mm / 50mm / 85mm / wide 24mm / anamorphic / f/1.8 shallow depth of field / deep focus / bokeh / focus breathing / lens flare`.

### 4. Texture / grain / "realness"
Image surface.
Vocabulary: `fine 35mm film grain / clean digital / halation on highlights / soft haze / sharp 4K clarity / vintage VHS texture / matte finish`.

### 5. Camera movement style (read from video references)
How the reference moves — so step 5 picks a matching move.
Vocabulary: `slow push-in / drift / handheld sway / locked-off static / orbit / crane up / whip pan / parallax`. For talking-head B-roll, prefer **slow & deliberate**.

### 6. Atmosphere / mood
The feeling the shot leaves.
Vocabulary: `contemplative / premium / energetic / moody / nostalgic / clinical-minimal / warm intimate / epic`.

### 7. Composition & aspect ratio
Subject placement, negative space, framing.
Vocabulary: `rule of thirds / centered symmetry / negative space / tight close-up / wide establishing / low angle / top-down / over-the-shoulder`.
Ratios: `16:9` (horizontal YouTube, default), `9:16` (Shorts/Reels), `4:5` (feed), `2.39:1` (cinematic anamorphic).

### 8. Subject treatment
People or not? Close or far? Faces shown (faceless channels hide them)? Objects/products/scenery?
E.g. `faceless — hands and objects only / silhouette / back of subject / product hero shot / empty environment`.

### 9. Aesthetic reference
A cultural anchor that helps the model lock on fast.
E.g. `A24 film look / Apple product ad / founder-documentary YouTube style / Kinfolk minimal / cyberpunk`.

## Card template

```
STYLE DNA — [video set name]
- Grade: [axis 1]
- Light: [axis 2]
- Lens: [axis 3]
- Texture: [axis 4]
- Motion: [axis 5 — prefer slow]
- Mood: [axis 6]
- Frame: [axis 7]
- Subject: [axis 8]
- Aesthetic ref: [axis 9]
- Aspect: [16:9 / 9:16 ...]
```

## Default when there are no references (cinematic founder look)

```
STYLE DNA — default cinematic
- Grade: warm amber shadows, low saturation, slight crushed blacks
- Light: soft single key from window-left, deep falloff, practical lamp glow
- Lens: 35mm, f/2, shallow depth of field
- Texture: fine 35mm film grain, gentle halation
- Motion: slow push-in / drift / parallax only
- Mood: contemplative, premium, late-evening calm
- Frame: rule of thirds, generous negative space
- Subject: hands + objects + environment (faceless-friendly)
- Aesthetic ref: founder-documentary / A24
- Aspect: 16:9
```
Tell the user clearly this is the default and references will make it more accurate.
