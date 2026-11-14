#!/usr/bin/env python3
"""Contact sheet: satu frame di akhir setiap segment narasi (untuk review visual cepat).

    python scripts/contact_sheet.py --quality preview [--scenes S10Compute ...] --out build/preview/contact
"""
import argparse
import json
import subprocess
import sys
import tempfile
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "manim"))
import narration  # noqa: E402


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--quality", default="preview")
    ap.add_argument("--scenes", nargs="*")
    ap.add_argument("--out", default=None)
    ap.add_argument("--width", type=int, default=640)
    a = ap.parse_args()
    out = Path(a.out or ROOT / "build" / a.quality / "contact")
    out.mkdir(parents=True, exist_ok=True)
    scenes = a.scenes or [s["scene"] for s in narration.SCENES]
    for sc in scenes:
        tim = json.loads((ROOT / "build" / a.quality / "timings" / f"{sc}.json").read_text())
        video = ROOT / "build" / a.quality / "scenes" / f"{sc}.mp4"
        starts = [s["start"] for s in tim["segments"]] + [tim["duration"]]
        times = [max(0.0, t - 0.7) for t in starts[1:]]
        ims = []
        with tempfile.TemporaryDirectory() as td:
            for k, t in enumerate(times):
                p = Path(td) / f"{k}.png"
                subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{t:.2f}", "-i", str(video), "-frames:v", "1",
                                "-vf", f"scale={a.width}:-1", str(p)], check=True)
                ims.append(Image.open(p).copy())
        cols = 2
        rows = (len(ims) + 1) // 2
        w, h = ims[0].size
        sheet = Image.new("RGB", (w * cols, h * rows), "white")
        for k, im in enumerate(ims):
            sheet.paste(im, ((k % cols) * w, (k // cols) * h))
        sheet.save(out / f"{sc}.png")
        print(out / f"{sc}.png")


if __name__ == "__main__":
    main()
