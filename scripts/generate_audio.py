#!/usr/bin/env python3
"""Generate narration audio (Indonesian TTS) from manim/narration.py.

Output:
    audio/cache/<hash>.mp3          raw TTS per kalimat (cache, aman dihapus)
    audio/segments/<segment>.wav    audio per segment (dipakai Manim lewat add_sound)
    audio/manifest.json             durasi segment + timing tiap kalimat (dipakai Manim & caption)

Usage:
    python scripts/generate_audio.py            # hanya generate yang belum ada / berubah
    python scripts/generate_audio.py --force    # paksa generate ulang semuanya
"""
import argparse
import asyncio
import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "manim"))
import narration as N  # noqa: E402

AUDIO = ROOT / "audio"
CACHE = AUDIO / "cache"
SEGS = AUDIO / "segments"
MANIFEST = AUDIO / "manifest.json"
SR = 48000


def sh(cmd):
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)


def duration(path: Path) -> float:
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(path)],
        check=True, capture_output=True, text=True).stdout.strip()
    return float(out)


def key_for(speech: str) -> str:
    return hashlib.sha1(f"{N.VOICE}|{N.RATE}|{N.PITCH}|{speech}".encode()).hexdigest()[:16]


async def tts_one(speech: str, out: Path, sem: asyncio.Semaphore, proxy):
    import edge_tts
    async with sem:
        for attempt in range(5):
            try:
                tmp = out.with_suffix(".part")
                com = edge_tts.Communicate(speech, N.VOICE, rate=N.RATE, pitch=N.PITCH, proxy=proxy)
                await com.save(str(tmp))
                if tmp.stat().st_size < 1000:
                    raise RuntimeError("TTS menghasilkan file kosong")
                tmp.rename(out)
                return
            except Exception as e:  # noqa: BLE001
                wait = 2 * (attempt + 1)
                print(f"  ! TTS gagal ({e}); retry dalam {wait}s", file=sys.stderr)
                await asyncio.sleep(wait)
        raise SystemExit(f"TTS gagal permanen untuk: {speech[:60]}...")


async def main_async(force: bool):
    CACHE.mkdir(parents=True, exist_ok=True)
    SEGS.mkdir(parents=True, exist_ok=True)
    proxy = os.environ.get("TTS_PROXY") or os.environ.get("HTTPS_PROXY") or os.environ.get("https_proxy")

    # 1) TTS per kalimat (paralel, dengan cache)
    jobs, plan = [], []
    sem = asyncio.Semaphore(4)
    for scene, seg_id, text in N.all_segments():
        sentences = N.split_sentences(text)
        items = []
        for s in sentences:
            speech = N.to_speech(s)
            mp3 = CACHE / f"{key_for(speech)}.mp3"
            if force and mp3.exists():
                mp3.unlink()
            if not mp3.exists():
                jobs.append(tts_one(speech, mp3, sem, proxy))
            items.append((s, speech, mp3))
        plan.append((scene, seg_id, items))
    if jobs:
        print(f"[audio] TTS {len(jobs)} kalimat dengan voice {N.VOICE} ...")
        await asyncio.gather(*jobs)
    else:
        print("[audio] semua kalimat sudah ada di cache")

    # 2) Rakit WAV per segment + manifest
    manifest = {"voice": N.VOICE, "rate": N.RATE, "sentence_gap": N.SENTENCE_GAP, "segments": {}}
    old = json.loads(MANIFEST.read_text()) if MANIFEST.exists() else {"segments": {}}
    for scene, seg_id, items in plan:
        sig = hashlib.sha1("|".join(str(m.name) for _, _, m in items).encode() + str(N.SENTENCE_GAP).encode()).hexdigest()
        wav = SEGS / f"{seg_id}.wav"
        prev = old["segments"].get(seg_id)
        if prev and prev.get("sig") == sig and wav.exists() and not force:
            manifest["segments"][seg_id] = prev
            continue
        sentences, t = [], 0.0
        concat_list = SEGS / f"{seg_id}.txt"
        gap = SEGS / "_gap.wav"
        if not gap.exists() or force:
            sh(["ffmpeg", "-y", "-f", "lavfi", "-i", f"anullsrc=r={SR}:cl=mono", "-t", str(N.SENTENCE_GAP), str(gap)])
        parts = []
        for k, (cap, speech, mp3) in enumerate(items):
            w = CACHE / f"{mp3.stem}.wav"
            if not w.exists():
                # trim leading/trailing silence agar jeda konsisten
                sh(["ffmpeg", "-y", "-i", str(mp3), "-af",
                    "silenceremove=start_periods=1:start_threshold=-50dB,areverse,"
                    "silenceremove=start_periods=1:start_threshold=-50dB,areverse",
                    "-ar", str(SR), "-ac", "1", str(w)])
            d = duration(w)
            sentences.append({"text": cap, "speech": speech, "start": round(t, 3), "end": round(t + d, 3)})
            parts.append(w)
            t += d
            if k < len(items) - 1:
                parts.append(gap)
                t += N.SENTENCE_GAP
        concat_list.write_text("".join(f"file '{p.resolve()}'\n" for p in parts))
        sh(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(concat_list),
            "-ar", str(SR), "-ac", "1", "-c:a", "pcm_s16le", str(wav)])
        concat_list.unlink()
        manifest["segments"][seg_id] = {
            "scene": scene, "file": f"audio/segments/{seg_id}.wav",
            "duration": round(duration(wav), 3), "sentences": sentences, "sig": sig,
        }
        print(f"[audio] {seg_id:18s} {manifest['segments'][seg_id]['duration']:6.2f}s")

    MANIFEST.write_text(json.dumps(manifest, indent=1, ensure_ascii=False))
    total = sum(s["duration"] for s in manifest["segments"].values())
    print(f"[audio] manifest: {len(manifest['segments'])} segment, total narasi {total/60:.1f} menit")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--force", action="store_true")
    asyncio.run(main_async(ap.parse_args().force))
