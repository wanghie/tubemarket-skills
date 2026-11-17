#!/usr/bin/env python3
"""auto-reframe - 16:9 -> 9:16 with the speaker's face kept in frame.

Strategy is hard-cut pans, not continuous tracking: the crop window holds
still and only jumps when the subject has genuinely moved and stayed moved.
A crop that drifts every frame reads as a shaky camera; a crop that cuts
reads as an edit.

Usage:
  python3 reframe.py INPUT.mp4 [-o out.mp4] [--aspect 9:16]
          [--mode face|center|top] [--sample 0.4] [--smooth 5] [--dry-run]
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "lib"))
import sfcore as sf  # noqa: E402
import face  # noqa: E402


def sample_face_centers(src: str, step: float, crop_w: int, width: int):
    """Return [(t, cx_pixels)] sampled every `step` seconds. cx is None where
    no face was found - callers hold the last known position. Detection and
    false-hit rejection live in lib/face.py (YuNet first, Haar as the floor)."""
    samples = face.sample_faces(src, step)
    if samples is None:
        sf.info("no face backend - falling back to centre crop")
        return None
    if not any(c for _, c in samples):
        sf.info("no face anywhere - using centre crop")
        return None
    return [(t, c[0] if c else None) for t, c in samples]


def to_shots(samples, width: int, crop_w: int, smooth: int,
             jump_px: float, min_hold: float, duration: float):
    """Fill gaps, moving-average, then quantise into hold-and-jump shots."""
    if not samples:
        return [(0.0, duration, (width - crop_w) / 2)]

    xs, last = [], width / 2
    for t, c in samples:
        if c is None:
            c = last
        last = c
        xs.append((t, c))

    k = max(smooth, 1)
    sm = []
    for i, (t, _) in enumerate(xs):
        lo, hi = max(0, i - k // 2), min(len(xs), i - k // 2 + k)
        sm.append((t, sum(v for _, v in xs[lo:hi]) / (hi - lo)))

    def clamp(cx):
        return max(0.0, min(width - crop_w, cx - crop_w / 2))

    shots = [[sm[0][0], clamp(sm[0][1])]]
    pending = None
    for t, cx in sm[1:]:
        x = clamp(cx)
        if abs(x - shots[-1][1]) < jump_px:
            pending = None
            continue
        if pending is None:
            pending = (t, x)
        elif t - pending[0] >= min_hold:
            # only commit a jump the subject actually sustained
            shots.append([pending[0], x])
            pending = None
    out = []
    for i, (t, x) in enumerate(shots):
        end = shots[i + 1][0] if i + 1 < len(shots) else duration
        if end - t > 0.25:
            out.append((t, end, x))
        elif out:
            out[-1] = (out[-1][0], end, out[-1][2])
    return out or [(0.0, duration, (width - crop_w) / 2)]


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("input")
    ap.add_argument("-o", "--output", default=None)
    ap.add_argument("--aspect", default="9:16")
    ap.add_argument("--mode", default="face", choices=["face", "center", "top"])
    ap.add_argument("--sample", type=float, default=0.4, help="seconds between samples")
    ap.add_argument("--smooth", type=int, default=5)
    ap.add_argument("--jump", type=float, default=0.06,
                    help="min move as fraction of width before a re-cut")
    ap.add_argument("--min-hold", type=float, default=1.2)
    ap.add_argument("--out-height", type=int, default=1920)
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    sf.require("ffmpeg", "ffprobe")
    src = Path(args.input)
    meta = sf.probe(str(src))
    W, H, dur = meta["width"], meta["height"], meta["duration"]

    aw, ah = (int(v) for v in args.aspect.split(":"))
    crop_w = min(W, int(round(H * aw / ah)))
    crop_h = min(H, int(round(crop_w * ah / aw)))
    crop_w -= crop_w % 2
    crop_h -= crop_h % 2

    if crop_w >= W:
        sf.info("source is already at or narrower than target aspect - "
                "cropping height instead")

    if args.mode == "face":
        samples = sample_face_centers(str(src), args.sample, crop_w, W)
    else:
        samples = None
    shots = to_shots(samples or [], W, crop_w, args.smooth,
                     args.jump * W, args.min_hold, dur)
    y = 0 if args.mode == "top" else max(0, (H - crop_h) // 2)

    out = Path(args.output or src.with_name(src.stem + ".vertical.mp4"))
    plan = {"source": str(src.resolve()), "aspect": args.aspect,
            "crop": [crop_w, crop_h], "shots": [
                {"start": round(s, 3), "end": round(e, 3), "x": int(x)}
                for s, e, x in shots]}
    sf.save_json(plan, str(out.with_suffix(".reframe.json")))
    sf.info(f"{W}x{H} -> {crop_w}x{crop_h}, {len(shots)} shot(s)")
    if args.dry_run:
        print(out.with_suffix(".reframe.json"))
        return

    work = out.parent / f".sf-{src.stem}"
    work.mkdir(parents=True, exist_ok=True)
    out_h = args.out_height
    out_w = int(round(out_h * aw / ah))
    out_w -= out_w % 2

    parts = []
    for i, (s, e, x) in enumerate(shots):
        p = work / f"rf{i:04d}.mp4"
        vf = (f"crop={crop_w}:{crop_h}:{int(x)}:{y},"
              f"scale={out_w}:{out_h}:flags=lanczos")
        sf.run(["ffmpeg", "-y", "-v", "error", "-ss", f"{s:.3f}", "-i", str(src),
                "-t", f"{e - s:.3f}", "-vf", vf] + sf.encode_args() +
               ["-r", str(meta["fps"]), str(p)])
        parts.append(p)
    sf.concat(parts, str(out), work)
    for p in parts:
        p.unlink(missing_ok=True)
    print(out)


if __name__ == "__main__":
    main()
