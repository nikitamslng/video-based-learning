#!/usr/bin/env python3
"""Render scene Manim (paralel) untuk quality 'preview' atau 'final'.

    python scripts/render_scenes.py --quality preview                 # semua scene, 480p15
    python scripts/render_scenes.py --quality final                   # semua scene, 1920x1080 @ 30fps
    python scripts/render_scenes.py --quality final --scenes S10Compute S11Construct
    python scripts/render_scenes.py --quality preview --jobs 2

Hasil: build/<quality>/scenes/<Scene>.mp4  (+ build/<quality>/timings/<Scene>.json)
Setiap scene memakai media_dir sendiri agar render paralel tidak bentrok di cache teks Manim.
"""
import argparse
import os
import shutil
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "manim"))

QUALITY = {
    # flag manim, resolusi, fps
    "preview": ["-ql"],                                   # 854x480 @ 15 fps
    "final": ["-qh", "--resolution", "1920,1080", "--frame_rate", "30"],
}


def scene_order():
    import narration
    return [s["scene"] for s in narration.SCENES]


def scene_file(scene):
    for f in sorted((ROOT / "manim" / "scenes").glob("s*.py")):
        if f"class {scene}(" in f.read_text():
            return f
    sys.exit(f"[render] scene {scene} tidak ditemukan di manim/scenes/")


def manim_bin():
    venv = ROOT / ".venv" / "bin" / "manim"
    return str(venv) if venv.exists() else (shutil.which("manim") or "manim")


def render(scene, quality, extra):
    media = ROOT / "build" / quality / "media" / scene
    log = ROOT / "build" / quality / "logs" / f"{scene}.log"
    log.parent.mkdir(parents=True, exist_ok=True)
    cmd = [manim_bin(), "render", *QUALITY[quality], *extra, "--media_dir", str(media),
           "--disable_caching", str(scene_file(scene)), scene]
    env = dict(os.environ, LECTURE_QUALITY=quality)
    t0 = time.time()
    with open(log, "w") as fh:
        rc = subprocess.run(cmd, cwd=ROOT, stdout=fh, stderr=subprocess.STDOUT, env=env).returncode
    if rc != 0:
        return scene, False, time.time() - t0, log
    vids = sorted((media / "videos").rglob(f"{scene}.mp4"), key=lambda p: p.stat().st_mtime)
    vids = [v for v in vids if "partial_movie_files" not in v.parts]
    if not vids:
        return scene, False, time.time() - t0, log
    out = ROOT / "build" / quality / "scenes" / f"{scene}.mp4"
    out.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(vids[-1], out)
    return scene, True, time.time() - t0, log


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--quality", choices=QUALITY, default="preview")
    ap.add_argument("--scenes", nargs="*", help="nama class scene (default: semua, sesuai SCENE_ORDER)")
    ap.add_argument("--jobs", type=int, default=max(1, min(4, os.cpu_count() or 1)))
    ap.add_argument("--extra", nargs=argparse.REMAINDER, default=[], help="argumen tambahan untuk manim")
    a = ap.parse_args()
    scenes = a.scenes or scene_order()
    print(f"[render] quality={a.quality} jobs={a.jobs} scenes={len(scenes)}")
    failed = []
    with ThreadPoolExecutor(a.jobs) as ex:
        futs = [ex.submit(render, s, a.quality, a.extra) for s in scenes]
        for f in as_completed(futs):
            scene, ok, dt, log = f.result()
            print(f"[render] {'OK ' if ok else 'ERR'} {scene:22s} {dt:6.1f}s" + ("" if ok else f"  -> lihat {log}"))
            if not ok:
                failed.append(scene)
    if failed:
        sys.exit(f"[render] gagal: {', '.join(failed)}")


if __name__ == "__main__":
    main()
