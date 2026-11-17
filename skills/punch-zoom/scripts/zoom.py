#!/usr/bin/env python3
"""punch-zoom - add rhythm to a static talking head.

Two moves, both driven by the transcript:
  punch  - instant hard-cut zoom on an emphasised word, held to end of clause
  push   - slow push in toward the speaker under a long statement

Every zoom is AIMED AT THE SPEAKER'S FACE: the face is tracked (lib/face.py),
smoothed, and the zoomed window follows it so the face sits centred with
headroom. A move whose window has no face is dropped (rendered as a hold) -
a zoom into empty background or the middle of the frame has no purpose.
--anchor center restores the old fixed-centre crop for faceless footage.

Auto-detection scores each word on: emphasis keyword, a pause right before it
(a speaker pausing before a word is telling you it matters), unusual word
duration, and numbers. Highest scores win, spaced out so the video does not
pulse like a strobe.

Usage:
  python3 zoom.py INPUT.mp4 -t transcript.json [-o out.mp4]
          [--audience vi|en] [--density 0.12] [--map zoommap.json] [--dry-run]
          [--anchor face|center]
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "lib"))
import sfcore as sf  # noqa: E402
import face  # noqa: E402

NUM = re.compile(r"\d")


def score_words(words: list, keywords: set) -> list:
    if not words:
        return []
    durs = sorted(w["end"] - w["start"] for w in words)
    med = durs[len(durs) // 2] or 0.2
    scored = []
    for i, w in enumerate(words):
        n = sf.norm_word(w["word"])
        if len(n) < 2 and not NUM.search(n):
            continue
        s = 0.0
        if n in keywords:
            s += 3.0
        if NUM.search(n) or "%" in w["word"]:
            s += 2.0
        gap = w["start"] - words[i - 1]["end"] if i else 0.0
        if gap > 0.35:
            s += 2.0 + min(gap, 1.0)
        d = w["end"] - w["start"]
        if d > med * 1.8:
            s += 1.5
        if s > 0:
            scored.append((s, i, w))
    return sorted(scored, key=lambda x: -x[0])


def plan_moves(words, preset, duration, density, min_spacing=2.2):
    z = preset["zoom"]
    keywords = {sf.norm_word(k) for k in z["emphasis_keywords"]}
    budget = max(1, int(duration * density))
    picked, taken = [], []
    for s, i, w in score_words(words, keywords):
        if len(picked) >= budget:
            break
        if any(abs(w["start"] - t) < min_spacing for t in taken):
            continue
        # hold the zoom to the end of the clause, not just the word
        end = w["end"]
        for nxt in words[i + 1:]:
            if nxt["start"] - end > 0.45:
                break
            end = nxt["end"]
            if end - w["start"] > 3.0:
                break
        picked.append({"type": "punch", "start": round(w["start"], 3),
                       "end": round(min(end + 0.15, duration), 3),
                       "scale": z["punch_scale"], "word": w["word"],
                       "score": round(s, 2)})
        taken.append(w["start"])
    picked.sort(key=lambda m: m["start"])

    # merge overlaps, then fill long quiet stretches with a slow push
    merged = []
    for m in picked:
        if merged and m["start"] < merged[-1]["end"] + 0.4:
            continue  # merging would turn two punches into one long static zoom
        merged.append(m)

    out, cursor = [], 0.0
    for m in merged:
        gap = m["start"] - cursor
        if gap >= z["kenburns_min_sec"] * 2:
            out.append({"type": "push", "start": round(cursor, 3),
                        "end": round(m["start"], 3), "scale": z["kenburns_scale"]})
        elif gap > 0:
            out.append({"type": "hold", "start": round(cursor, 3),
                        "end": round(m["start"], 3), "scale": 1.0})
        out.append(m)
        cursor = m["end"]
    if duration - cursor > 0.1:
        kind = "push" if duration - cursor >= z["kenburns_min_sec"] * 2 else "hold"
        out.append({"type": kind, "start": round(cursor, 3),
                    "end": round(duration, 3),
                    "scale": z["kenburns_scale"] if kind == "push" else 1.0})
    return [m for m in out if m["end"] - m["start"] > 0.12]


FACE_Y = 0.42   # face centre sits at 42% of the zoomed frame height (headroom above)


def _interp(track, t):
    """(cx, cy, h) at time t from a smoothed track [(t, cx, cy, h)]."""
    if t <= track[0][0]:
        return track[0][1:]
    for (t0, *a), (t1, *b) in zip(track, track[1:]):
        if t0 <= t <= t1:
            k = (t - t0) / ((t1 - t0) or 1)
            return tuple(x + (y - x) * k for x, y in zip(a, b))
    return track[-1][1:]


def _face_in(raw, s, e):
    """Share of samples in [s, e] where a face was actually detected."""
    xs = [c for t, c in raw if s - 0.05 <= t <= e + 0.05]
    return (sum(1 for c in xs if c) / len(xs)) if xs else 0.0


def _pw(points, var):
    """Piecewise-linear ffmpeg expression of `var` through [(t, v)]."""
    if len(points) == 1:
        return f"{points[0][1]:.2f}"
    expr = f"{points[-1][1]:.2f}"
    for (t0, v0), (t1, v1) in reversed(list(zip(points, points[1:]))):
        sl = (v1 - v0) / ((t1 - t0) or 1)
        expr = f"if(lt({var},{t1:.3f}),{v0:.2f}+({sl:.4f})*({var}-{t0:.3f}),{expr})"
    return expr


def aim(track, m, W, H, scale, step=0.4):
    """Top-left of the zoomed window over the move, as [(t_local, x, y)],
    so the face sits at (50%, FACE_Y) of the window, clamped to the frame."""
    cw, ch = W / scale, H / scale
    dur = m["end"] - m["start"]
    n = max(1, int(dur / step))
    pts = []
    for i in range(n + 1):
        tl = min(dur, i * step)
        cx, cy, _ = _interp(track, m["start"] + tl)
        x = min(max(cx - cw / 2, 0.0), W - cw)
        y = min(max(cy - ch * FACE_Y, 0.0), H - ch)
        pts.append((tl, x, y))
    return pts


def render(src: str, moves: list, out: Path, work: Path, meta: dict,
           anchor: str = "face") -> list:
    W, H, fps = meta["width"], meta["height"], meta["fps"]
    raw, track = None, []
    if anchor == "face" and any(m["scale"] > 1.001 for m in moves):
        raw = face.sample_faces(src, 0.2)
        track = face.smooth_track(raw or [], window=7)
        if not track:
            sf.info("no face found - zooms dropped (use --anchor center for faceless footage)")
    parts, done = [], []
    for i, m in enumerate(moves):
        p = work / f"z{i:04d}.mp4"
        dur = m["end"] - m["start"]
        zoom = m["scale"] > 1.001
        if zoom and anchor == "face" and (not track or _face_in(raw, m["start"], m["end"]) < 0.5):
            sf.info(f"  {m['start']:6.2f}s {m['type']} dropped: no face to aim at")
            m = dict(m, type="hold", scale=1.0, dropped="no face")
            zoom = False
        if zoom and anchor == "face":
            pts = aim(track, m, W, H, m["scale"])
            m = dict(m, aim=[{"t": round(m["start"] + t, 2), "x": int(x), "y": int(y)} for t, x, y in pts])
        if zoom and m["type"] == "push":
            # zoom grows linearly; window aimed at the face (or the centre).
            # 2x upscale first: zoompan positions are whole pixels, this halves the step.
            U = 2
            z = f"(1+({m['scale'] - 1:.4f})*min(on/{max(dur * fps, 1):.1f},1))"
            if anchor == "face":
                # face-centred window of the CURRENT zoom: x = cx - iw/zoom/2 (in upscaled px)
                cxs = [(t, (x + W / m['scale'] / 2) * U) for t, x, _ in pts]
                cys = [(t, (y + H / m['scale'] * FACE_Y) * U) for t, _, y in pts]
                tx = f"on/{fps}"
                xe = f"max(0,min(iw-iw/zoom,({_pw(cxs, tx)})-iw/zoom/2))"
                ye = f"max(0,min(ih-ih/zoom,({_pw(cys, tx)})-ih/zoom*{FACE_Y}))"
            else:
                xe, ye = "iw/2-(iw/zoom/2)", "ih/2-(ih/zoom/2)"
            vf = (f"scale={W * U}:{H * U}:flags=lanczos,"
                  f"zoompan=z='{z}':x='{xe}':y='{ye}':d=1:s={W}x{H}:fps={fps},setsar=1")
        elif zoom:
            cw, ch = int(W / m["scale"]) // 2 * 2, int(H / m["scale"]) // 2 * 2
            if anchor == "face":
                xe = _pw([(t, x) for t, x, _ in pts], "n/" + str(fps))
                ye = _pw([(t, y) for t, _, y in pts], "n/" + str(fps))
                vf = (f"crop={cw}:{ch}:x='{xe}':y='{ye}',"
                      f"scale={W}:{H}:flags=lanczos,setsar=1")
            else:
                vf = (f"crop={cw}:{ch}:{(W - cw) // 2}:{int((H - ch) * 0.40)},"
                      f"scale={W}:{H}:flags=lanczos,setsar=1")
        else:
            vf = "setsar=1"
        sf.run(["ffmpeg", "-y", "-v", "error", "-ss", f"{m['start']:.3f}",
                "-i", src, "-t", f"{dur:.3f}", "-vf", vf] +
               sf.encode_args() + ["-r", str(fps), str(p)])
        parts.append(p)
        done.append(m)
    sf.concat(parts, str(out), work)
    for p in parts:
        p.unlink(missing_ok=True)
    return done


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("input")
    ap.add_argument("-t", "--transcript", default=None)
    ap.add_argument("-o", "--output", default=None)
    ap.add_argument("--audience", default=None)
    ap.add_argument("--density", type=float, default=0.12,
                    help="zoom events per second (0.12 ~ one per 8s)")
    ap.add_argument("--map", default=None, help="hand-written zoom map JSON")
    ap.add_argument("--anchor", default="face", choices=["face", "center"],
                    help="aim zooms at the tracked face (default) or the fixed centre")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    sf.require("ffmpeg", "ffprobe")
    src = Path(args.input)
    meta = sf.probe(str(src))
    out = Path(args.output or src.with_name(src.stem + ".zoom.mp4"))

    if args.map:
        import json
        moves = json.loads(Path(args.map).read_text(encoding="utf-8"))["moves"]
    else:
        if not args.transcript:
            sf.die("Need --transcript for auto mode, or --map for a manual plan.")
        tr = sf.load_transcript(args.transcript)
        audience = args.audience or tr.get("audience", "en")
        preset = sf.load_preset(audience)
        moves = plan_moves(tr["words"], preset, meta["duration"], args.density)
        sf.info(f"audience={audience} "
                f"{sum(1 for m in moves if m['type'] == 'punch')} punch, "
                f"{sum(1 for m in moves if m['type'] == 'push')} push")

    sf.save_json({"source": str(src.resolve()), "moves": moves},
                 str(out.with_suffix(".zoommap.json")))
    if args.dry_run:
        for m in moves:
            if m["type"] == "punch":
                sf.info(f"  {m['start']:6.2f}s punch x{m['scale']}  \"{m.get('word','')}\"")
        print(out.with_suffix(".zoommap.json"))
        return

    work = out.parent / f".sf-{src.stem}"
    work.mkdir(parents=True, exist_ok=True)
    moves = render(str(src), moves, out, work, meta, args.anchor)
    sf.save_json({"source": str(src.resolve()), "anchor": args.anchor, "moves": moves},
                 str(out.with_suffix(".zoommap.json")))
    print(out)


if __name__ == "__main__":
    main()
