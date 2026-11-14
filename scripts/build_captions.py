#!/usr/bin/env python3
"""Bangun caption (SRT, VTT, ASS) yang tersinkron dengan narasi.

Timing dihitung dari:
  * durasi tiap video scene  (build/<q>/scenes/<Scene>.mp4)
  * waktu mulai tiap segment di dalam scene (build/<q>/timings/<Scene>.json, ditulis oleh LectureScene)
  * waktu mulai/akhir tiap kalimat di dalam segment (audio/manifest.json)

    python scripts/build_captions.py --quality final      # -> captions.srt, captions.vtt (root) + build/final/captions.ass
    python scripts/build_captions.py --quality preview    # -> build/preview/captions.{srt,vtt,ass}
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

MAX_CUE = 88      # karakter maksimum per cue (2 baris)
MAX_LINE = 46     # karakter maksimum per baris


def probe_duration(p: Path) -> float:
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(p)],
                         check=True, capture_output=True, text=True).stdout
    return float(out.strip())


def display(text: str) -> str:
    t = text.replace("O(2^n)", "O(2ⁿ)").replace("...", "…")
    return t


def split_chunks(text: str, limit=MAX_CUE):
    """Pecah kalimat panjang di tanda baca, lalu di spasi, agar tiap cue <= limit karakter."""
    if len(text) <= limit:
        return [text]
    parts = re.split(r"(?<=[,;:])\s+", text)
    chunks, cur = [], ""
    for p in parts:
        cand = (cur + " " + p).strip()
        if len(cand) <= limit:
            cur = cand
        else:
            if cur:
                chunks.append(cur)
            cur = p
    if cur:
        chunks.append(cur)
    out = []
    for ch in chunks:  # potong lagi per kata kalau masih kepanjangan
        while len(ch) > limit:
            cut = ch.rfind(" ", 0, limit)
            cut = cut if cut > limit * 0.5 else limit
            out.append(ch[:cut].strip())
            ch = ch[cut:].strip()
        out.append(ch)
    # gabungkan potongan yang terlalu pendek dengan tetangganya
    merged = []
    for ch in out:
        if merged and len(ch) < 18 and len(merged[-1]) + len(ch) + 1 <= limit + 12:
            merged[-1] = merged[-1] + " " + ch
        else:
            merged.append(ch)
    return merged


def wrap2(text: str, width=MAX_LINE):
    """Bungkus menjadi maksimal 2 baris yang seimbang."""
    if len(text) <= width:
        return [text]
    words = text.split()
    best, best_score = [text], 1e9
    for k in range(1, len(words)):
        a, b = " ".join(words[:k]), " ".join(words[k:])
        score = max(len(a), len(b)) + (0 if len(a) >= len(b) * 0.6 else 5)
        if score < best_score:
            best, best_score = [a, b], score
    return best


def fmt_ts(t, sep=","):
    t = max(0.0, t)
    h = int(t // 3600)
    m = int(t % 3600 // 60)
    s = int(t % 60)
    ms = int(round((t - int(t)) * 1000))
    if ms == 1000:
        s, ms = s + 1, 0
    return f"{h:02d}:{m:02d}:{s:02d}{sep}{ms:03d}"


def fmt_ass(t):
    t = max(0.0, t)
    h = int(t // 3600)
    m = int(t % 3600 // 60)
    s = t % 60
    return f"{h:d}:{m:02d}:{s:05.2f}"


def build_cues(quality):
    manifest = json.loads((ROOT / "audio" / "manifest.json").read_text())["segments"]
    cues, offset = [], 0.0
    for sc in narration.SCENES:
        name = sc["scene"]
        tim = json.loads((ROOT / "build" / quality / "timings" / f"{name}.json").read_text())
        video = ROOT / "build" / quality / "scenes" / f"{name}.mp4"
        dur = probe_duration(video)
        for seg in tim["segments"]:
            data = manifest[seg["id"]]
            base = offset + seg["start"]
            for s in data["sentences"]:
                text = display(s["text"])
                t0, t1 = base + s["start"], base + s["end"]
                chunks = split_chunks(text)
                total = sum(len(c) for c in chunks)
                t = t0
                for ch in chunks:
                    d = (t1 - t0) * len(ch) / total
                    cues.append([t, t + d, ch])
                    t += d
        offset += dur
    # rapikan: tanpa overlap, durasi minimum, sedikit "hold" setelah kalimat selesai
    for k, cue in enumerate(cues):
        nxt = cues[k + 1][0] if k + 1 < len(cues) else cue[1] + 1.0
        cue[1] = min(max(cue[1] + 0.25, cue[0] + 0.9), nxt - 0.04)
    return cues, offset


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--quality", default="final")
    a = ap.parse_args()
    cues, total = build_cues(a.quality)
    out_dir = ROOT if a.quality == "final" else ROOT / "build" / a.quality
    out_dir.mkdir(parents=True, exist_ok=True)

    srt = []
    vtt = ["WEBVTT", "Kind: captions", "Language: id", ""]
    for k, (t0, t1, text) in enumerate(cues, 1):
        lines = wrap2(text)
        srt += [str(k), f"{fmt_ts(t0)} --> {fmt_ts(t1)}", *lines, ""]
        vtt += [str(k), f"{fmt_ts(t0, '.')} --> {fmt_ts(t1, '.')} line:88% align:center", *lines, ""]
    (out_dir / "captions.srt").write_text("\n".join(srt), encoding="utf-8")
    (out_dir / "captions.vtt").write_text("\n".join(vtt), encoding="utf-8")

    ass = [
        "[Script Info]", "ScriptType: v4.00+", "PlayResX: 1920", "PlayResY: 1080", "WrapStyle: 2",
        "ScaledBorderAndShadow: yes", "",
        "[V4+ Styles]",
        "Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, "
        "Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, "
        "MarginR, MarginV, Encoding",
        "Style: Default,Inter,44,&H00FFFFFF,&H00FFFFFF,&H64000000,&H64000000,0,0,0,0,100,100,0,0,3,10,0,2,80,80,34,1",
        "", "[Events]", "Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text",
    ]
    for t0, t1, text in cues:
        body = r"\N".join(wrap2(text)).replace("{", "(").replace("}", ")")
        ass.append(f"Dialogue: 0,{fmt_ass(t0)},{fmt_ass(t1)},Default,,0,0,0,,{body}")
    ass_path = ROOT / "build" / a.quality / "captions.ass"
    ass_path.parent.mkdir(parents=True, exist_ok=True)
    ass_path.write_text("\n".join(ass) + "\n", encoding="utf-8")
    print(f"[captions] {len(cues)} cue, durasi video {total/60:.2f} menit -> {out_dir/'captions.srt'}, "
          f"{out_dir/'captions.vtt'}, {ass_path}")


if __name__ == "__main__":
    main()
