#!/usr/bin/env python3
"""Ekspor naskah narasi (manim/narration.py) menjadi narration_script.md.

    python scripts/export_script_md.py
Jika audio/manifest.json ada, durasi tiap segment ikut dicantumkan.
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "manim"))
import narration as N  # noqa: E402


def main():
    man = ROOT / "audio" / "manifest.json"
    segs = json.loads(man.read_text())["segments"] if man.exists() else {}
    total = sum(s["duration"] for s in segs.values()) if segs else 0
    out = [
        "# Naskah Narasi — Dynamic Programming: Maximum Subarray Sum (Session 15)",
        "",
        f"- **Bahasa:** Indonesia (istilah teknis CS tetap dalam bahasa Inggris)",
        f"- **Voice TTS:** `{N.VOICE}` (Microsoft Edge Neural TTS), rate `{N.RATE}`",
        f"- **Jumlah scene:** {len(N.SCENES)}  ·  **Jumlah segment:** {sum(len(s['segments']) for s in N.SCENES)}",
    ]
    if total:
        out.append(f"- **Total durasi narasi:** {total/60:.1f} menit")
    out += [
        "",
        "> File ini di-generate otomatis dari `manim/narration.py` (sumber kebenaran). "
        "Untuk mengubah narasi, edit `manim/narration.py`, lalu jalankan ulang `./render_preview.sh` / `./render_final.sh`.",
        "",
    ]
    for k, sc in enumerate(N.SCENES, 1):
        out += [f"## {k}. {sc['title']}", "", f"*Scene Manim:* `{sc['scene']}`", ""]
        for seg_id, text in sc["segments"]:
            d = segs.get(seg_id, {}).get("duration")
            tag = f" · {d:.1f} s" if d else ""
            out += [f"**[{seg_id}{tag}]**", "", text, ""]
    (ROOT / "narration_script.md").write_text("\n".join(out), encoding="utf-8")
    print(f"[script] -> {ROOT / 'narration_script.md'}")


if __name__ == "__main__":
    main()
