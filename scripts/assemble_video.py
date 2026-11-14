#!/usr/bin/env python3
"""Gabungkan semua scene (video + audio narasi), lalu burn subtitle -> video final.

    python scripts/assemble_video.py --quality final     # -> final_video.mp4 (1920x1080, 30 fps)
    python scripts/assemble_video.py --quality preview   # -> build/preview/preview_video.mp4

Langkah:
  1. concat build/<q>/scenes/*.mp4 sesuai urutan narration.SCENES (stream copy, tanpa re-encode)
  2. burn caption (build/<q>/captions.ass) + normalisasi loudness audio (EBU R128, -16 LUFS)
  3. encode H.264 (yuv420p, faststart) + AAC 48 kHz
"""
import argparse
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "manim"))
import narration  # noqa: E402

PRESET = {
    "final": dict(out=ROOT / "final_video.mp4", crf="20", preset="medium", fps="30", scale="1920:1080"),
    "preview": dict(out=ROOT / "build" / "preview" / "preview_video.mp4", crf="28", preset="veryfast", fps="15",
                    scale="854:480"),
}


def run(cmd):
    print("[assemble] " + " ".join(str(c) for c in cmd[:6]) + " ...")
    subprocess.run(cmd, check=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--quality", choices=PRESET, default="final")
    a = ap.parse_args()
    p = PRESET[a.quality]
    bdir = ROOT / "build" / a.quality
    scenes = [bdir / "scenes" / f"{s['scene']}.mp4" for s in narration.SCENES]
    missing = [s for s in scenes if not s.exists()]
    if missing:
        sys.exit(f"[assemble] scene belum dirender: {[m.name for m in missing]}")
    ass = bdir / "captions.ass"
    if not ass.exists():
        sys.exit("[assemble] captions.ass belum ada -> jalankan scripts/build_captions.py dulu")

    lst = bdir / "concat.txt"
    lst.write_text("".join(f"file '{s}'\n" for s in scenes))
    joined = bdir / "joined.mp4"
    run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", str(lst), "-c", "copy", str(joined)])

    # path filter ffmpeg: escape ':' dan '\'
    ass_f = str(ass).replace("\\", "\\\\").replace(":", "\\:")
    fonts = "/usr/share/fonts"
    vf = f"scale={p['scale']}:flags=lanczos,ass='{ass_f}':fontsdir={fonts},fps={p['fps']},format=yuv420p"
    p["out"].parent.mkdir(parents=True, exist_ok=True)
    run(["ffmpeg", "-v", "error", "-y", "-i", str(joined), "-vf", vf,
         "-c:v", "libx264", "-preset", p["preset"], "-crf", p["crf"], "-profile:v", "high", "-tune", "animation",
         "-af", "loudnorm=I=-16:TP=-1.5:LRA=11", "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-ac", "2",
         "-movflags", "+faststart", str(p["out"])])
    print(f"[assemble] selesai -> {p['out']}")


if __name__ == "__main__":
    main()
