#!/usr/bin/env python3
"""short-video-formats - turn one talking-head clip into a finished vertical
short in one of 10 knowledge-video formats.

Chain: [trim] -> video-shorts-pipeline (cut silence, reframe 9:16, punch zoom)
       -> stacked layout (graphics panel on top, speaker below)
       -> format graphics (ASS) -> word-captions.

Subcommands:
  render.py list
  render.py template --format 8 -t clip.transcript.json > plan.json
  render.py render CLIP.mp4 --plan plan.json [--outdir DIR] [--audience en]
                   [--panel 0.36] [--crop-top 0.08] [--density 0.15] [--keep]

Plan timing: every "at"/"until" is either seconds on the FINAL (post-cut)
timeline, or a phrase the speaker says ("at": "human body"). Phrases survive
silence cutting; seconds do not, so prefer phrases.
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SKILL = HERE.parent
ROOT = SKILL.parents[1]
sys.path.insert(0, str(ROOT / "lib"))
import sfcore as sf  # noqa: E402

FORMATS = json.loads((SKILL / "formats.json").read_text(encoding="utf-8"))["formats"]

# colours as ASS &HBBGGRR
WHITE, INK = "&HFFFFFF&", "&H140F0B&"
ACCENT, ACCENT_SOFT = "&HF65C8B&", "&HFA8BA7&"      # #8B5CF6 / #A78BFA
BAD = "&H4444EF&"                                  # #EF4444
PANEL = "&H100B0B&"                                # #0B0B10
TIERS = {"S": "&H7F7FFF&", "A": "&H7FBFFF&", "B": "&H7FDFFF&",
         "C": "&HFFBF7F&", "D": "&HF6A0C4&"}
FONT = "Avenir Next"


def ts(t: float) -> str:
    t = max(t, 0)
    h, rem = divmod(t, 3600)
    m, s = divmod(rem, 60)
    return f"{int(h)}:{int(m):02d}:{s:05.2f}"


def esc(text: str) -> str:
    return str(text).replace("{", "(").replace("}", ")").replace("\n", "\\N")


# ---------------------------------------------------------------- timing
class Clock:
    def __init__(self, words: list, duration: float):
        self.words = [(sf.norm_word(w["word"]), w["start"], w["end"]) for w in words]
        self.words = [w for w in self.words if w[0]]
        self.duration = duration
        self.cursor = 0

    def at(self, ref, default=None, ordered=True) -> float:
        if ref is None:
            return default
        if ref == "end":
            return self.duration
        if isinstance(ref, (int, float)):
            return float(ref)
        toks = [sf.norm_word(x) for x in str(ref).split()]
        toks = [x for x in toks if x]
        starts = list(range(self.cursor if ordered else 0, len(self.words))) + \
            (list(range(0, self.cursor)) if ordered else [])
        for i in starts:
            if [w[0] for w in self.words[i:i + len(toks)]] == toks:
                if ordered:
                    self.cursor = i
                return self.words[i][1]
        sf.die(f"Phrase not found in transcript: '{ref}'. Use words the speaker actually says.")


# ---------------------------------------------------------------- ASS
def rect(x1, y1, x2, y2, colour, t0, t1, alpha="00", fade=(120, 0), layer=1, blur=0):
    shape = f"m {x1:.0f} {y1:.0f} l {x2:.0f} {y1:.0f} l {x2:.0f} {y2:.0f} l {x1:.0f} {y2:.0f}"
    return (f"Dialogue: {layer},{ts(t0)},{ts(t1)},Box,,0,0,0,,"
            f"{{\\an7\\pos(0,0)\\bord0\\shad0\\blur{blur}\\1c{colour}\\1a&H{alpha}&\\fad({fade[0]},{fade[1]})\\p1}}{shape}")


def text(x, y, s, t0, t1, size, colour=WHITE, an=5, bold=1, layer=3, extra=""):
    return (f"Dialogue: {layer},{ts(t0)},{ts(t1)},Txt,,0,0,0,,"
            f"{{\\an{an}\\pos({x:.0f},{y:.0f})\\fs{size:.0f}\\b{bold}\\1c{colour}\\fad(120,0){extra}}}{esc(s)}")


def build_overlay(plan: dict, clock: Clock, W: int, H: int, panel_h: int) -> str:
    end = clock.duration
    ev = []
    # panel background + soft accent glow (no hard edge)
    ev.append(rect(0, 0, W, panel_h, PANEL, 0, end, fade=(0, 0), layer=0))
    ev.append(rect(W * 0.15, panel_h * 0.05, W * 0.85, panel_h * 0.55, ACCENT, 0, end,
                   alpha="C8", fade=(0, 0), layer=0, blur=90))
    pad = W * 0.06
    # format badge
    fmt = next((f for f in FORMATS if f["id"] == plan.get("format")), None)
    if fmt and plan.get("badge", True):
        ev.append(text(pad, panel_h * 0.07, fmt["name"].upper(), 0, end, H * 0.016,
                       ACCENT_SOFT, an=4, extra="\\fsp4"))
    # pinned title (2 lines: white + accent)
    title = plan.get("title", [])
    if isinstance(title, str):
        title = [title]
    ty = panel_h * 0.17
    for i, line in enumerate(title[:2]):
        ev.append(text(W / 2, ty + i * H * 0.042, line.upper(), 0, end, H * 0.040,
                       WHITE if i == 0 else ACCENT_SOFT, an=5,
                       extra="\\bord0\\shad0"))
    list_top = ty + max(len(title[:2]), 1) * H * 0.042 + H * 0.010
    row_h, gap = H * 0.050, H * 0.008
    n_rows = {"left": 0, "right": 0, "full": 0}
    board_drawn = False
    clock.cursor = 0
    for el in plan.get("elements", []):
        kind = el.get("type")
        t0 = clock.at(el.get("at"), 0.0)
        t1 = clock.at(el.get("until"), end, ordered=False) if el.get("until") else end
        if kind == "row":
            style = el.get("style", "neutral")
            side = el.get("side", "full")
            x1, x2 = (pad, W - pad) if side == "full" else \
                ((pad, W / 2 - pad / 4) if side == "left" else (W / 2 + pad / 4, W - pad))
            k = n_rows[side]
            n_rows[side] += 1
            y1 = list_top + k * (row_h + gap)
            y2 = y1 + row_h
            if y2 > panel_h - H * 0.01:
                sf.die("Too many rows for the panel. Raise --panel or split into fewer rows.")
            size = H * 0.029
            if style == "board":
                if not board_drawn:
                    ev.append(rect(pad - 10, list_top - 12, W - pad + 10,
                                   panel_h - H * 0.012, WHITE, t0, end, layer=1))
                    board_drawn = True
                ev.append(text(x1 + 18, (y1 + y2) / 2, el["text"], t0, t1, size * 1.08,
                               INK, an=4, layer=3))
                continue
            if style.startswith("tier"):
                tier = style.split(":")[1] if ":" in style else "A"
                ev.append(rect(x1, y1, x2, y2, "&H241C1C&", t0, t1))
                ev.append(rect(x1, y1, x1 + row_h * 1.25, y2, TIERS.get(tier, ACCENT), t0, t1, layer=2))
                ev.append(text(x1 + row_h * 0.62, (y1 + y2) / 2, tier, t0, t1, size * 1.3, INK))
                ev.append(text(x1 + row_h * 1.25 + 18, (y1 + y2) / 2, el["text"], t0, t1, size, an=4))
                continue
            colour = {"bad": BAD, "good": ACCENT}.get(style, "&H2A2222&")
            mark = {"bad": "✕ ", "good": "✓ "}.get(style, el.get("mark", ""))
            ev.append(rect(x1, y1, x2, y2, colour, t0, t1))
            ev.append(text(x1 + 18, (y1 + y2) / 2, mark + el["text"], t0, t1, size, an=4,
                           extra="\\t(0,140,\\fscx104\\fscy104)\\t(140,260,\\fscx100\\fscy100)"))
        elif kind == "stamp":
            colour = BAD if el.get("style") == "bad" else ACCENT
            ev.append(text(W - pad - 10, panel_h * 0.07, el["text"].upper(), t0, t1, H * 0.034,
                           colour, an=6, layer=4,
                           extra=f"\\bord5\\3c{WHITE}\\frz6\\t(0,160,\\fscx118\\fscy118)\\t(160,300,\\fscx100\\fscy100)"))
        elif kind == "tag":
            ev.append(rect(W - pad - W * 0.30, panel_h + H * 0.02, W - pad, panel_h + H * 0.065,
                           ACCENT, t0, t1, layer=1))
            ev.append(text(W - pad - W * 0.15, panel_h + H * 0.0425, el["text"].upper(), t0, t1,
                           H * 0.021, WHITE, layer=3))
        elif kind == "cta":
            t0 = clock.at(el.get("at"), max(end - 3.0, 0))
            ev.append(rect(W * 0.2, H * 0.935, W * 0.8, H * 0.975, WHITE, t0, end, layer=5))
            ev.append(text(W / 2, H * 0.955, el.get("text", "Save this for later"), t0, end,
                           H * 0.022, INK, layer=6))
        elif kind == "inset":
            continue  # handled in ffmpeg overlay
        else:
            sf.die(f"Unknown element type: {kind}")
    head = f"""[Script Info]
ScriptType: v4.00+
PlayResX: {W}
PlayResY: {H}
WrapStyle: 2
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Box,{FONT},20,&H00FFFFFF,&H00FFFFFF,&H00000000,&H00000000,0,0,0,0,100,100,0,0,1,0,0,7,0,0,0,1
Style: Txt,{FONT},40,&H00FFFFFF,&H00FFFFFF,&H00000000,&H00000000,-1,0,0,0,100,100,0,0,1,0,0,5,0,0,0,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    return head + "\n".join(ev) + "\n"


# ---------------------------------------------------------------- commands
def cmd_list(_):
    for f in FORMATS:
        tag = "clip-only" if f["clip_only"] else "needs extra footage"
        print(f"{f['id']:>2}. {f['name']:<22} {f['length_s'][0]}-{f['length_s'][1]}s  [{tag}]  {f['function']}")


def cmd_template(a):
    fmt = next(f for f in FORMATS if f["id"] == a.format)
    tr = json.loads(Path(a.transcript).read_text(encoding="utf-8")) if a.transcript else {"segments": []}
    plan = {
        "format": fmt["id"],
        "title": ["<HOOK LINE 1>", "<HOOK LINE 2>"],
        "trim": [0, round(tr.get("duration", 0), 2)],
        "beats": fmt["beats"],
        "transcript": [f"{s['start']:.1f}s {s['text'].strip()}" for s in tr.get("segments", [])],
        "elements": [{"type": e.split(":")[0], "style": e.split(":")[1].split()[0] if ":" in e else None,
                      "text": "<TEXT>", "at": "<PHRASE THE SPEAKER SAYS>"} for e in fmt["elements"]],
    }
    print(json.dumps(plan, indent=2, ensure_ascii=False))


def cmd_render(a):
    sf.require("ffmpeg", "ffprobe")
    plan = json.loads(Path(a.plan).read_text(encoding="utf-8"))
    clip = Path(a.clip).resolve()
    out = Path(a.outdir or clip.parent / "svf-out").resolve()
    out.mkdir(parents=True, exist_ok=True)
    base = clip.stem
    src = clip
    if plan.get("trim"):
        s, e = plan["trim"]
        src = out / f"{base}.trim.mp4"
        sf.run(["ffmpeg", "-y", "-v", "error", "-ss", str(s), "-to", str(e), "-i", str(clip),
                *sf.encode_args(crf=16, preset="fast"), str(src)])
    # reuse an existing transcript (shifted to the trim) so whisper runs once
    if a.transcript:
        tr0 = json.loads(Path(a.transcript).read_text(encoding="utf-8"))
        s0, e0 = (plan.get("trim") or [0, 1e9])
        shift = lambda xs: [dict(x, start=round(x["start"] - s0, 3), end=round(x["end"] - s0, 3))
                            for x in xs if x["start"] >= s0 and x["end"] <= e0 + 0.05]
        tr0 = dict(tr0, words=shift(tr0["words"]), segments=shift(tr0.get("segments", [])),
                   duration=sf.probe(str(src))["duration"])
        (out / "pipe").mkdir(exist_ok=True)
        (out / "pipe" / f"{src.stem}.transcript.json").write_text(json.dumps(tr0, ensure_ascii=False), encoding="utf-8")
    # 1) cut + reframe + zoom via the existing pipeline (captions burned later)
    skip = "captions" + ("" if plan.get("cut", True) else ",cut")
    focus = plan.get("focus_x")  # 0..1 speaker centre in the 16:9 source; set it after looking at a frame
    if focus is not None or sf.probe(str(src))["width"] < sf.probe(str(src))["height"]:
        skip += ",reframe"
    pipe = ROOT / "skills/video-shorts-pipeline/scripts/pipeline.sh"
    r = subprocess.run(["bash", str(pipe), str(src), "--audience", a.audience, "--outdir", str(out / "pipe"),
                        "--skip", skip, "--density", str(a.density)], text=True,
                       stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if r.returncode != 0:
        sys.stderr.write(r.stderr[-2000:])
        sf.die("video-shorts-pipeline failed")
    cur = r.stdout.strip().splitlines()[-1].split("->")[-1].strip()
    sb = src.stem
    trp = out / "pipe" / f"{sb}.cut.transcript.json"
    if not trp.exists():
        trp = out / "pipe" / f"{sb}.transcript.json"
    tr = json.loads(trp.read_text(encoding="utf-8"))
    info = sf.probe(cur)
    W, H = 1080, 1920
    panel_h = int(H * a.panel) // 2 * 2
    vid_h = H - panel_h
    clock = Clock(tr["words"], info["duration"])
    ass = out / f"{base}.format.ass"
    ass.write_text(build_overlay(plan, clock, W, H, panel_h), encoding="utf-8")
    # 2) stacked layout: speaker scaled to full width, cropped to fit under the panel
    if focus is not None and info["width"] > info["height"]:
        sh = int(vid_h * float(plan.get("scale", 1.0))) // 2 * 2
        sw = int(info["width"] * sh / info["height"]) // 2 * 2
        cx = int(min(max(float(focus) * sw - W / 2, 0), sw - W))
        cy = int(min(max((sh - vid_h) * a.crop_top / 0.5, 0), sh - vid_h))
        vf = (f"[0:v]scale={sw}:{sh},crop={W}:{vid_h}:{cx}:{cy},pad={W}:{H}:0:{panel_h}:color=0x0B0B10,setsar=1[v0]")
    else:
        crop_y = f"min(ih-{vid_h},ih*{a.crop_top})"
        vf = (f"[0:v]scale={W}:-2,crop={W}:{vid_h}:0:'{crop_y}',pad={W}:{H}:0:{panel_h}:color=0x0B0B10,setsar=1[v0]")
    inputs = ["-i", cur]
    last = "v0"
    for i, el in enumerate([e for e in plan.get("elements", []) if e.get("type") == "inset"], start=1):
        t0 = clock.at(el.get("at"), 0.0, ordered=False)
        t1 = clock.at(el.get("until"), info["duration"], ordered=False) if el.get("until") else info["duration"]
        inputs += (["-loop", "1"] if Path(el["file"]).suffix.lower() in (".png", ".jpg", ".jpeg", ".webp") else []) + ["-i", el["file"]]
        iw = int(W * el.get("width", 0.42)) // 2 * 2
        vf += f";[{i}:v]scale={iw}:-2,setsar=1[i{i}];[{last}][i{i}]overlay=x=W-w-{int(W*0.06)}:y={panel_h}+{int(H*0.08)}:enable='between(t,{t0:.2f},{t1:.2f})':shortest=0[o{i}]"
        last = f"o{i}"
    assp = str(ass).replace("\\", "/").replace(":", "\\:").replace("'", "\\'")
    vf += f";[{last}]ass='{assp}'[vout]"
    stacked = out / f"{base}.stacked.mp4"
    sf.run(["ffmpeg", "-y", "-v", "error", *inputs, "-filter_complex", vf, "-map", "[vout]", "-map", "0:a?",
            "-t", f"{info['duration']:.3f}", *sf.encode_args(crf=17, preset="fast"), str(stacked)])
    # 3) word captions on the speaker area
    final = out / f"{base}.{plan.get('name', 'format' + str(plan.get('format', '')))}.mp4"
    sf.run([sys.executable, str(ROOT / "skills/word-captions/scripts/captions.py"), str(stacked), "-t", str(trp),
            "--audience", tr.get("audience", a.audience), "--style", "bold", "--position", str(a.caption_pos),
            "-o", str(final)])
    (out / f"{base}.final.transcript.json").write_text(json.dumps(tr, ensure_ascii=False), encoding="utf-8")
    if not a.keep:
        stacked.unlink(missing_ok=True)
    print(final)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("list")
    t = sub.add_parser("template")
    t.add_argument("--format", type=int, required=True, choices=range(1, 11))
    t.add_argument("-t", "--transcript")
    r = sub.add_parser("render")
    r.add_argument("clip")
    r.add_argument("--plan", required=True)
    r.add_argument("--outdir")
    r.add_argument("-t", "--transcript", help="existing transcript of CLIP (skips a second whisper run)")
    r.add_argument("--audience", default="auto")
    r.add_argument("--panel", type=float, default=0.40, help="graphics panel height as fraction of 1920")
    r.add_argument("--crop-top", type=float, default=0.06, help="where to start the speaker crop (fraction of height)")
    r.add_argument("--density", type=float, default=0.15, help="punch zooms per second")
    r.add_argument("--caption-pos", type=float, default=0.10)
    r.add_argument("--keep", action="store_true")
    a = ap.parse_args()
    {"list": cmd_list, "template": cmd_template, "render": cmd_render}[a.cmd](a)


if __name__ == "__main__":
    main()
