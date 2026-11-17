"""Face detection + a smoothed face track, shared by auto-reframe and punch-zoom.

Backends, tried in order:
  1. OpenCV YuNet (cv2.FaceDetectorYN) - ships inside opencv-python >= 4.5.4.
     The 230 KB model (MIT licence, opencv_zoo) is read from SF_YUNET_MODEL,
     else ~/.cache/tubemarket/face_detection_yunet_2023mar.onnx, and is
     downloaded there once if missing. Accurate, and it does not mistake
     props (a capsule model, a lamp, a poster) for a face.
  2. OpenCV Haar cascade - always available, but it fires on face-like props.
     Its hits are only kept when they agree with the rest of the track
     (see track_faces: outlier rejection).

Every function returns positions in SOURCE pixels. A sample with no face is
None; callers decide what "no face" means (reframe: hold last crop; zoom: no
zoom at all - a zoom with nothing to aim at is not a zoom worth making).
"""
from __future__ import annotations

import os
import urllib.request
from pathlib import Path

YUNET_URL = ("https://github.com/opencv/opencv_zoo/raw/main/models/"
             "face_detection_yunet/face_detection_yunet_2023mar.onnx")


def _info(msg: str) -> None:
    import sys
    print(f"  {msg}", file=sys.stderr)


def _yunet_model() -> str | None:
    env = os.environ.get("SF_YUNET_MODEL")
    if env and Path(env).exists():
        return env
    p = Path.home() / ".cache" / "tubemarket" / "face_detection_yunet_2023mar.onnx"
    if p.exists() and p.stat().st_size > 100_000:
        return str(p)
    try:
        p.parent.mkdir(parents=True, exist_ok=True)
        tmp = p.with_suffix(".part")
        urllib.request.urlretrieve(YUNET_URL, tmp)
        if tmp.stat().st_size > 100_000:
            tmp.rename(p)
            return str(p)
    except Exception as e:  # offline: fall through to haar
        _info(f"could not fetch YuNet model ({e.__class__.__name__}) - using haar")
    return None


def make_detector():
    """Return (detect(frame) -> (cx, cy, w, h) | None, backend_name) or (None, reason)."""
    try:
        import cv2
    except ImportError:
        return None, "opencv not installed"

    if hasattr(cv2, "FaceDetectorYN"):
        model = _yunet_model()
        if model:
            try:
                det = cv2.FaceDetectorYN.create(model, "", (320, 320), 0.8, 0.3, 50)
                state = {"size": None}

                def f(frame):
                    h, w = frame.shape[:2]
                    # detect on a <=640px copy: faster, and YuNet is trained at that scale
                    k = min(1.0, 640.0 / max(w, h))
                    small = cv2.resize(frame, (int(w * k), int(h * k))) if k < 1 else frame
                    sh, sw = small.shape[:2]
                    if state["size"] != (sw, sh):
                        det.setInputSize((sw, sh))
                        state["size"] = (sw, sh)
                    _, faces = det.detect(small)
                    if faces is None or len(faces) == 0:
                        return None
                    x, y, fw, fh = max(faces, key=lambda r: r[2] * r[3])[:4]
                    return ((x + fw / 2) / k, (y + fh / 2) / k, fw / k, fh / k)

                return f, "opencv.yunet"
            except Exception as e:
                _info(f"YuNet failed to load ({e}) - using haar")

    try:
        cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
        if cascade.empty():
            raise RuntimeError("cascade did not load")

        def f(frame):
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = cascade.detectMultiScale(gray, 1.15, 6, minSize=(60, 60))
            if len(faces) == 0:
                return None
            x, y, w, h = max(faces, key=lambda r: r[2])
            return (x + w / 2, y + h / 2, w, h)

        return f, "opencv.haar"
    except Exception as e:
        return None, f"no face backend ({e})"


def sample_faces(src: str, step: float = 0.2, start: float = 0.0, end: float | None = None):
    """[(t, (cx, cy, w, h) | None)] every `step` seconds, or None if no backend."""
    try:
        import cv2
    except ImportError:
        _info("opencv not installed - no face tracking")
        return None
    detect, name = make_detector()
    if detect is None:
        _info(f"{name} - no face tracking")
        return None
    _info(f"face backend: {name}")
    cap = cv2.VideoCapture(src)
    if not cap.isOpened():
        return None
    fps = cap.get(cv2.CAP_PROP_FPS) or 30.0
    stride = max(int(round(fps * step)), 1)
    first = int(start * fps)
    if first:
        cap.set(cv2.CAP_PROP_POS_FRAMES, first)
    out, idx = [], first
    while True:
        if end is not None and idx / fps > end:
            break
        if not cap.grab():
            break
        if (idx - first) % stride == 0:
            ok, frame = cap.retrieve()
            if ok:
                try:
                    out.append((idx / fps, detect(frame)))
                except Exception:
                    out.append((idx / fps, None))
        idx += 1
    cap.release()
    found = sum(1 for _, c in out if c is not None)
    _info(f"sampled {len(out)} frames, face found in {found}")
    return clean_track(out)


def clean_track(samples):
    """Drop detections that disagree with the track: a box far smaller/larger
    than the median face, or one that sits far from both neighbours while
    they agree with each other (a one-off false hit on a prop)."""
    hits = [c for _, c in samples if c]
    if len(hits) < 3:
        return samples
    hs = sorted(c[3] for c in hits)
    med_h = hs[len(hs) // 2]
    out = []
    for t, c in samples:
        if c and not (0.55 * med_h <= c[3] <= 1.8 * med_h):
            c = None
        out.append((t, c))
    for i in range(1, len(out) - 1):
        a, b, n = out[i - 1][1], out[i][1], out[i + 1][1]
        if a and b and n:
            near = abs(a[0] - n[0]) < med_h * 0.6
            far = abs(b[0] - (a[0] + n[0]) / 2) > med_h * 1.5
            if near and far:
                out[i] = (out[i][0], None)
    return out


def smooth_track(samples, window: int = 5):
    """Fill gaps by holding the nearest found face, then moving-average x/y.
    Returns [(t, cx, cy, h)] or [] if no face anywhere."""
    if not samples or not any(c for _, c in samples):
        return []
    filled, last = [], next(c for _, c in samples if c)
    for t, c in samples:
        if c:
            last = c
        filled.append((t, last))
    k = max(window, 1)
    res = []
    for i, (t, _) in enumerate(filled):
        lo, hi = max(0, i - k // 2), min(len(filled), i - k // 2 + k)
        seg = [c for _, c in filled[lo:hi]]
        res.append((t, sum(c[0] for c in seg) / len(seg), sum(c[1] for c in seg) / len(seg),
                    sum(c[3] for c in seg) / len(seg)))
    return res
