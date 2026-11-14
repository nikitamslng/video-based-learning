#!/usr/bin/env python3
"""Generate narration audio (Indonesian TTS, Microsoft Edge Neural — gratis) from manim/narration.py.

Setiap segment di-TTS SEKALIGUS sebagai satu paragraf, sehingga intonasi, tempo, dan jeda antar
kalimat terdengar natural (tidak "disambung-sambung"). Waktu mulai/akhir tiap kalimat diambil dari
event WordBoundary Edge TTS, lalu dipakai untuk sinkronisasi animasi (seg.wait_sentence) dan caption.

Output:
    audio/cache/<hash>.mp3 + <hash>.json   hasil TTS mentah per segment + timing kata (cache, aman dihapus)
    audio/segments/<segment>.wav           audio per segment (dipakai Manim lewat add_sound)
    audio/manifest.json                    durasi segment + timing tiap kalimat

Usage:
    python scripts/generate_audio.py            # hanya generate segment yang belum ada / teksnya berubah
    python scripts/generate_audio.py --force    # paksa generate ulang semuanya
"""
import argparse
import asyncio
import hashlib
import json
import os
import re
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
TAIL = 0.15  # detik hening yang disisakan setelah kata terakhir


def sh(cmd):
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)


def duration(path: Path) -> float:
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(path)],
        check=True, capture_output=True, text=True).stdout.strip()
    return float(out)


def key_for(speech: str) -> str:
    return hashlib.sha1(f"seg|{N.VOICE}|{N.RATE}|{N.PITCH}|{speech}".encode()).hexdigest()[:16]


async def tts_segment(speech: str, mp3: Path, words_json: Path, sem: asyncio.Semaphore, proxy):
    import edge_tts
    async with sem:
        for attempt in range(5):
            try:
                com = edge_tts.Communicate(speech, N.VOICE, rate=N.RATE, pitch=N.PITCH,
                                           boundary="WordBoundary", proxy=proxy)
                audio, words = bytearray(), []
                async for ch in com.stream():
                    if ch["type"] == "audio":
                        audio += ch["data"]
                    elif ch["type"] == "WordBoundary":
                        words.append({"t": ch["offset"] / 1e7, "d": ch["duration"] / 1e7, "w": ch["text"]})
                if len(audio) < 2000 or not words:
                    raise RuntimeError("TTS menghasilkan audio kosong")
                mp3.write_bytes(bytes(audio))
                words_json.write_text(json.dumps(words, ensure_ascii=False))
                return
            except Exception as e:  # noqa: BLE001
                wait = 2 * (attempt + 1)
                print(f"  ! TTS gagal ({e}); retry dalam {wait}s", file=sys.stderr)
                await asyncio.sleep(wait)
        raise SystemExit(f"TTS gagal permanen untuk: {speech[:60]}...")


def n_words(speech: str) -> int:
    return len([w for w in speech.split() if re.search(r"\w", w)])


def sentence_times(speeches, words, total):
    """Petakan kalimat -> (start, end) memakai urutan WordBoundary."""
    counts = [n_words(s) for s in speeches]
    if sum(counts) != len(words):  # fallback: skala proporsional jika tokenisasi berbeda
        scale = len(words) / max(1, sum(counts))
        acc, idx = 0.0, []
        for c_ in counts:
            idx.append(min(len(words) - 1, int(round(acc))))
            acc += c_ * scale
    else:
        idx, acc = [], 0
        for c_ in counts:
            idx.append(acc)
            acc += c_
    out = []
    for k, i0 in enumerate(idx):
        i1 = (idx[k + 1] - 1) if k + 1 < len(idx) else len(words) - 1
        i1 = max(i0, i1)
        start = words[i0]["t"]
        end = min(total, words[i1]["t"] + words[i1]["d"])
        out.append((start, end))
    return out


async def main_async(force: bool):
    CACHE.mkdir(parents=True, exist_ok=True)
    SEGS.mkdir(parents=True, exist_ok=True)
    proxy = os.environ.get("TTS_PROXY") or os.environ.get("HTTPS_PROXY") or os.environ.get("https_proxy")

    plan, jobs = [], []
    sem = asyncio.Semaphore(4)
    for scene, seg_id, text in N.all_segments():
        caps = N.split_sentences(text)
        speeches = [N.to_speech(s) for s in caps]
        speech = " ".join(speeches)
        key = key_for(speech)
        mp3, wj = CACHE / f"{key}.mp3", CACHE / f"{key}.json"
        if force:
            for f in (mp3, wj):
                f.unlink(missing_ok=True)
        if not (mp3.exists() and wj.exists()):
            jobs.append(tts_segment(speech, mp3, wj, sem, proxy))
        plan.append((scene, seg_id, caps, speeches, key))
    if jobs:
        print(f"[audio] TTS {len(jobs)} segment dengan voice {N.VOICE} (rate {N.RATE}) ...")
        await asyncio.gather(*jobs)
    else:
        print("[audio] semua segment sudah ada di cache")

    manifest = {"voice": N.VOICE, "rate": N.RATE, "mode": "segment", "segments": {}}
    old = json.loads(MANIFEST.read_text()) if MANIFEST.exists() else {"segments": {}}
    for scene, seg_id, caps, speeches, key in plan:
        wav = SEGS / f"{seg_id}.wav"
        prev = old["segments"].get(seg_id)
        if prev and prev.get("sig") == key and wav.exists() and not force:
            manifest["segments"][seg_id] = prev
            continue
        words = json.loads((CACHE / f"{key}.json").read_text())
        end = words[-1]["t"] + words[-1]["d"] + TAIL
        # potong ekor hening; awal tidak dipotong agar offset WordBoundary tetap tepat
        sh(["ffmpeg", "-y", "-i", str(CACHE / f"{key}.mp3"), "-t", f"{end:.3f}",
            "-ar", str(SR), "-ac", "1", "-c:a", "pcm_s16le", str(wav)])
        total = duration(wav)
        times = sentence_times(speeches, words, total)
        sentences = [{"text": c_, "speech": s, "start": round(a, 3), "end": round(b, 3)}
                     for c_, s, (a, b) in zip(caps, speeches, times)]
        manifest["segments"][seg_id] = {"scene": scene, "file": f"audio/segments/{seg_id}.wav",
                                        "duration": round(total, 3), "sentences": sentences, "sig": key}
        print(f"[audio] {seg_id:18s} {total:6.2f}s  ({len(sentences)} kalimat)")

    MANIFEST.write_text(json.dumps(manifest, indent=1, ensure_ascii=False))
    total = sum(s["duration"] for s in manifest["segments"].values())
    print(f"[audio] manifest: {len(manifest['segments'])} segment, total narasi {total/60:.1f} menit")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--force", action="store_true")
    asyncio.run(main_async(ap.parse_args().force))
