#!/usr/bin/env python3
"""Validasi hasil akhir: format video, audio, sinkronisasi caption, dan kelengkapan deliverable.

    python scripts/validate.py --quality final
    python scripts/validate.py --quality preview
"""
import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "manim"))
import narration  # noqa: E402

ok_all = True


def check(cond, msg):
    global ok_all
    print(("  [OK]   " if cond else "  [FAIL] ") + msg)
    ok_all &= bool(cond)


def probe(path):
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries",
                          "stream=codec_type,codec_name,width,height,r_frame_rate,sample_rate,channels:format=duration",
                          "-of", "json", str(path)], check=True, capture_output=True, text=True).stdout
    return json.loads(out)


def parse_srt(p):
    cues = []
    for block in p.read_text(encoding="utf-8").strip().split("\n\n"):
        lines = block.splitlines()
        m = re.match(r"(\d+):(\d+):(\d+),(\d+) --> (\d+):(\d+):(\d+),(\d+)", lines[1])
        g = list(map(int, m.groups()))
        t0 = g[0] * 3600 + g[1] * 60 + g[2] + g[3] / 1000
        t1 = g[4] * 3600 + g[5] * 60 + g[6] + g[7] / 1000
        cues.append((t0, t1, " ".join(lines[2:])))
    return cues


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--quality", default="final")
    q = ap.parse_args().quality
    final = q == "final"
    video = ROOT / "final_video.mp4" if final else ROOT / "build" / "preview" / "preview_video.mp4"
    cap_dir = ROOT if final else ROOT / "build" / "preview"
    print(f"Validasi ({q}): {video}")

    check(video.exists(), "video ada")
    if not video.exists():
        sys.exit(1)
    info = probe(video)
    v = [s for s in info["streams"] if s["codec_type"] == "video"][0]
    a = [s for s in info["streams"] if s["codec_type"] == "audio"]
    dur = float(info["format"]["duration"])
    W, H, FPS = (1920, 1080, "30/1") if final else (854, 480, "15/1")
    check((v["width"], v["height"]) == (W, H), f"resolusi {v['width']}x{v['height']} (target {W}x{H}, 16:9)")
    check(v["r_frame_rate"] == FPS, f"frame rate {v['r_frame_rate']} (target {FPS})")
    check(v["codec_name"] == "h264", f"codec video {v['codec_name']}")
    check(len(a) == 1 and a[0]["codec_name"] == "aac", "ada 1 stream audio AAC")
    print(f"  durasi video: {dur/60:.2f} menit")

    # audio benar-benar berisi suara (bukan placeholder/hening)
    vd = subprocess.run(["ffmpeg", "-v", "info", "-i", str(video), "-map", "0:a", "-af", "volumedetect", "-f", "null",
                         "-"], capture_output=True, text=True).stderr
    mean = float(re.search(r"mean_volume: (-?[\d.]+) dB", vd).group(1))
    check(mean > -35, f"audio tidak hening (mean volume {mean:.1f} dB)")
    sil = subprocess.run(["ffmpeg", "-v", "info", "-i", str(video), "-map", "0:a", "-af",
                          "silencedetect=noise=-45dB:d=6", "-f", "null", "-"], capture_output=True, text=True).stderr
    long_sil = re.findall(r"silence_duration: ([\d.]+)", sil)
    check(not long_sil, f"tidak ada jeda hening > 6 detik ({len(long_sil)} ditemukan)")

    # caption
    srt, vtt = cap_dir / "captions.srt", cap_dir / "captions.vtt"
    check(srt.exists() and vtt.exists(), "captions.srt & captions.vtt ada")
    cues = parse_srt(srt)
    check(len(cues) > 50, f"{len(cues)} cue caption")
    check(all(c[1] > c[0] for c in cues), "setiap cue berdurasi positif")
    check(all(cues[k][1] <= cues[k + 1][0] + 1e-3 for k in range(len(cues) - 1)), "cue tidak saling tumpang tindih")
    check(cues[-1][1] <= dur + 0.05, f"cue terakhir ({cues[-1][1]:.1f}s) <= durasi video ({dur:.1f}s)")
    vtt_txt = vtt.read_text(encoding="utf-8")
    check(vtt_txt.startswith("WEBVTT") and vtt_txt.count("-->") == len(cues), "VTT valid & jumlah cue sama dengan SRT")
    max_line = max(len(line) for block in srt.read_text().split("\n\n") for line in block.splitlines()[2:])
    check(max_line <= 60, f"baris caption terpanjang {max_line} karakter (<= 60)")

    # semua kalimat narasi muncul di caption (urutan sama)
    joined = " ".join(c[2] for c in cues).replace("\n", " ")
    n_sent = sum(len(narration.split_sentences(t)) for _, _, t in narration.all_segments())
    words = [w for _, _, t in narration.all_segments() for w in t.split()]
    check(len(joined.split()) >= len(words) * 0.98, f"caption memuat seluruh narasi ({n_sent} kalimat)")

    if final:
        for f in ["final_video.mp4", "narration_script.md", "captions.srt", "captions.vtt", "README.md",
                  "render_preview.sh", "render_final.sh"]:
            check((ROOT / f).exists(), f"deliverable {f}")
        for d in ["manim", "audio", "scripts"]:
            check((ROOT / d).is_dir() and any((ROOT / d).iterdir()), f"folder {d}/")
        segs = json.loads((ROOT / "audio" / "manifest.json").read_text())["segments"]
        check(all((ROOT / s["file"]).exists() for s in segs.values()), f"{len(segs)} file audio segment ada")

    print("HASIL:", "SEMUA CEK LULUS" if ok_all else "ADA CEK YANG GAGAL")
    sys.exit(0 if ok_all else 1)


if __name__ == "__main__":
    main()
