#!/usr/bin/env python3
"""Ambil beberapa frame dari video dan susun jadi satu grid PNG (untuk pengecekan visual cepat).

    python scripts/snapshot.py VIDEO OUT.png t1 t2 t3 ...      (t dalam detik)
"""
import subprocess
import sys
import tempfile
from pathlib import Path

from PIL import Image


def main():
    video, out, *times = sys.argv[1:]
    times = [float(t) for t in times]
    with tempfile.TemporaryDirectory() as td:
        ims = []
        for k, t in enumerate(times):
            p = Path(td) / f"{k}.png"
            subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", str(t), "-i", video, "-frames:v", "1", str(p)],
                           check=True)
            ims.append(Image.open(p).copy())
    cols = 2 if len(ims) > 1 else 1
    rows = (len(ims) + cols - 1) // cols
    w, h = ims[0].size
    grid = Image.new("RGB", (w * cols, h * rows), "white")
    for k, im in enumerate(ims):
        grid.paste(im, ((k % cols) * w, (k // cols) * h))
    grid.save(out)
    print(out)


if __name__ == "__main__":
    main()
