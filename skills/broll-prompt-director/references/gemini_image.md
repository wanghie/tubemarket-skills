# Gemini Image — first-frame prompt (Nano Banana)

The first frame is where the image-to-video clip starts. It locks the whole look. Nail this frame and half the clip is won.
The structure below works for other image models too (ChatGPT image generation, etc.).

## Pick the model

- **Nano Banana Pro (Gemini 3 Pro Image):** default for cinematic B-roll — strong composition reasoning, high detail/lighting, accepts up to ~14 reference images, renders text correctly (useful when text is in frame). Turn on "Thinking" for complex shots.
- **Nano Banana (Gemini 2.5 Flash Image):** fast; good when you only need a *light edit* of an image that is nearly right, or a quick style transfer.
- Edit first: if the image is 80% right, **do not regenerate from scratch** — tell it "keep the composition, change only the lighting to golden hour".

## Prompt frame (this order reads clearest)

```
[Subject — specific] , [Composition/framing] , [Setting/environment] ,
[Lighting] , [STYLE DNA block] , [Lens & camera] , [Aspect ratio]
```

Write in **English**, natural descriptive sentences (Gemini reads prose well; no Midjourney-style tag stuffing). 40-120 words is usually enough.

### Components

1. **Subject** — who/what, specific. *"a steaming cup of black coffee beside an open laptop"* beats *"coffee"*. For faceless B-roll: hands + objects + environment.
2. **Composition** — `extreme close-up / medium shot / wide establishing / low angle / top-down / over-the-shoulder`, plus subject placement (`off-center, rule of thirds`).
3. **Setting** — space + time. *"a quiet café at late evening, rain on the window"*.
4. **Lighting** — taken straight from Style DNA axis 2.
5. **STYLE DNA** — paste grade + texture + mood from the card. **This is what keeps the set consistent** — never drop it.
6. **Lens & camera** — `shot on 35mm lens, f/2, shallow depth of field, cinematic`. You can add a body: `shot on Arri Alexa` to push the film look.
7. **Aspect ratio** — state `16:9` (or `9:16`). Wrong ratio = redo, burning credits.

## RULES SPECIFIC TO THE FIRST FRAME (because it goes into video)

This is make-or-break — the frame must **have room to move**:

- **Leave negative space** in the direction the camera/subject will move. A packed frame = a frozen clip.
- **Have foreground/background layers** for parallax on a push-in (e.g. a blurred object in front, bokeh lights behind).
- **Compose the "just before" state.** If the clip is "pouring coffee", the first frame is *the pot tilting, about to pour*, not pouring. Give the motion room to play.
- **Clean, well-lit frame with one clear subject.** Higgsfield/Kling warp most on dirty, cluttered or very dark images. Garbage in = garbage out.
- **Avoid close-up faces and many-fingered hands** unless needed — the zone AI breaks most when animating.

## Using reference images (keep a character/product/style)

Nano Banana Pro accepts several images. Assign each a role:
```
Use Image 1 as the character reference — maintain this exact person, face and outfit.
Use Image 2 as the style reference — match its color grade and lighting.
Place the subject in: [new setting]. Cinematic, shot at 35mm, 16:9.
```
Useful when the user wants themselves or their product to appear consistently across shots.

## Complete example

**Idea:** "working late alone" (faceless, default cinematic DNA)
```
An extreme close-up of hands typing on a laptop keyboard in a dim home office at
midnight, the screen's glow lighting the fingers from the front, a half-empty cup of
coffee softly out of focus in the foreground. Warm amber shadows, low saturation,
slight crushed blacks, fine 35mm film grain, gentle halation on the screen highlights.
Contemplative late-night mood, generous negative space on the right of the frame.
Shot on 35mm lens, f/2, shallow depth of field, cinematic. 16:9.
```
Why it works as a first frame: the hands do not need to move much, there is a foreground (blurred cup) for parallax, and negative space on the right for the camera to drift into.
