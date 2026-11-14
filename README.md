# Dynamic Programming: Maximum Subarray Sum — Video Pembelajaran (Manim)

Video pembelajaran animasi berbahasa Indonesia untuk materi **Session 15 — Dynamic Programming: Maximum Subarray Sum (Kadane's Algorithm)**.
Seluruh visual dibuat dengan **Manim Community Edition**. Narasi memakai **TTS Bahasa Indonesia gratis** (Microsoft Edge Neural, suara `id-ID-ArdiNeural`, tempo −3%, satu paragraf per segment agar intonasi natural). Subtitle di-*burn* ke video dan juga tersedia sebagai `.srt` dan `.vtt`.

| Deliverable | Keterangan |
|---|---|
| `final_video.mp4` | Video final 1920×1080, 30 fps, H.264 + AAC, narasi + subtitle burn-in (±18 menit) |
| `narration_script.md` | Naskah narasi per scene/segment (di-generate dari `manim/narration.py`) |
| `captions.srt`, `captions.vtt` | Subtitle Bahasa Indonesia, tersinkron dengan narasi |
| `manim/` | Seluruh source code Manim (theme, komponen, 14 scene) |
| `audio/` | Audio narasi per segment (`audio/segments/*.wav`) + `audio/manifest.json` (durasi & timing kalimat) |
| `scripts/` | Pipeline: TTS, render scene, caption, penggabungan, validasi |
| `render_preview.sh` / `render_final.sh` | Satu perintah untuk preview / render final |

---

## 1. Alur materi (mengikuti slide)

| # | Scene (`manim/scenes/`) | Isi |
|---|---|---|
| 1 | `S01Intro` | Judul, Learning Outcomes (LO 2, LO 3), Outline |
| 2 | `S02WhyDP` | FIB rekursif, recursion tree `fib(5)`, fib(2) ×3 & fib(3) ×2, O(2ⁿ) |
| 3 | `S03Memoization` | MEMOIZED-FIB, trace pengisian `memo`, memo hit & pruning tree, O(n) |
| 4 | `S04Definition` | Definisi DP, optimal substructure & overlapping subproblems, kontras D&C / Greedy |
| 5 | `S05TopDownBottomUp` | Top-down vs bottom-up, FIB-DP + animasi pengisian tabel, tabel perbandingan |
| 6 | `S06DesignSteps` | 4 langkah desain DP: characterize → define → compute → construct |
| 7 | `S07Problem` | Problem Maximum Subarray Sum, contoh `A[4..7]`, sum = 6 |
| 8 | `S08Naive` | Enumerasi subarray, O(n²)·O(n) = O(n³), BRUTE-FORCE-SUM, overlapping |
| 9 | `S09Characterize` | Step 1 (dp[i], extend vs start, teorema) & Step 2 (recurrence, base case, GlobalMax) |
| 10 | `S10Compute` | Step 3: KADANE-TABLE + trace dp, space-optimized O(1), FIB-SPACE-OPTIMIZED |
| 11 | `S11Construct` | Step 4: expansion & global rule, KADANE-CONSTRUCT, tabel trace `[-2,1,-3,4,-1,2,1]` |
| 12 | `S12WhyNotGreedy` | Kadane memenuhi properti DP, contoh greedy gagal `[-1,3,-1,4]`, tabel DP vs Greedy |
| 13 | `S13Summary` | Ringkasan |
| 14 | `S14Exercise` | Climbing Stairs, Maximum Product Subarray, References, penutup |

**Koreksi kecil terhadap slide** (agar perhitungan akurat):
- KADANE-TABLE baris 2 di slide tertulis `let s[1..n]`; di video ditulis `let dp[1..n]` (array yang memang dipakai).
- Tabel trace slide 26: baris i = 3 tertulis `max(−3, 1 + (−3)) = 1`, yang benar `= −2` (sesuai kolom curr_max); baris i = 7 subarray tertulis `[4, 1, 2, 1]`, yang benar `[4, −1, 2, 1]`. Kolom *Subarray Tracked* di video menampilkan subarray berjalan `A[temp_start..i]`.

## 2. Struktur folder

```
video-based-learning/
├── final_video.mp4            # hasil akhir
├── captions.srt / captions.vtt
├── narration_script.md
├── render_preview.sh          # preview cepat 480p15
├── render_final.sh            # final 1080p30
├── requirements.txt
├── manim/
│   ├── narration.py           # ★ SUMBER KEBENARAN naskah (teks, voice, aturan ucapan TTS)
│   ├── lecture.py             # theme, komponen (CodePanel, ArrayRow, tabel, title bar), LectureScene (sinkron audio)
│   ├── fibtree.py             # komponen recursion tree Fibonacci
│   └── scenes/s01_intro.py … s14_exercise.py   # satu file = satu scene
├── audio/
│   ├── manifest.json          # durasi segment + waktu mulai/akhir tiap kalimat
│   └── segments/*.wav         # audio narasi per segment
├── scripts/
│   ├── generate_audio.py      # TTS per segment/paragraf (cache) + timing kata → wav per segment + manifest
│   ├── render_scenes.py       # render scene Manim paralel (preview / final)
│   ├── build_captions.py      # SRT + VTT + ASS (style burn-in) dari timing nyata
│   ├── assemble_video.py      # concat scene → burn subtitle → loudnorm → MP4
│   ├── validate.py            # cek resolusi, fps, audio, sinkronisasi caption, deliverable
│   ├── export_script_md.py    # narration.py → narration_script.md
│   ├── contact_sheet.py       # 1 frame per segment untuk review visual
│   └── snapshot.py            # ambil frame tertentu dari video
└── build/                     # file sementara (di-ignore git): media Manim, timing, log
```

### Cara sinkronisasi bekerja
1. `generate_audio.py` men-TTS **satu segment sekaligus sebagai satu paragraf** (bukan kalimat per kalimat), sehingga intonasi, tempo, dan jeda antar kalimat terdengar natural seperti dosen membaca penjelasan. Waktu mulai/akhir tiap kalimat diambil dari event *WordBoundary* Edge TTS dan disimpan di `audio/manifest.json`.
2. Di Manim, setiap segment dibungkus `with self.say("segment_id") as seg:`. Audio diputar (`add_sound`) tepat saat blok dimulai, animasi bisa ditunggu-kan ke kalimat tertentu dengan `seg.wait_sentence(k)`, dan di akhir blok scene otomatis menunggu sampai audio selesai. Waktu mulai segment ditulis ke `build/<quality>/timings/<Scene>.json`.
3. `build_captions.py` menghitung waktu caption = offset scene (durasi video nyata) + waktu segment + waktu kalimat, sehingga subtitle selalu pas dengan suara.

---

## 3. Instalasi

Diuji di Linux (Ubuntu/Debian), Python 3.10–3.13, Manim CE 0.22.1. **LaTeX tidak dibutuhkan** (semua rumus dirender dengan font Unicode).

### 3.1 Dependency sistem
```bash
sudo apt-get update
```
```bash
sudo apt-get install -y ffmpeg libcairo2-dev libpango1.0-dev pkg-config python3-venv fonts-inter fonts-dejavu-core
```
- macOS: `brew install ffmpeg cairo pango pkg-config` lalu install font **Inter** (https://rsms.me/inter/).
- Windows: gunakan WSL2 (Ubuntu) dan ikuti langkah Linux.
- `ffmpeg` harus mendukung filter `ass` (libass). Cek: `ffmpeg -filters | grep " ass "`.

### 3.2 Masuk ke folder project & buat virtualenv
```bash
cd video-based-learning
```
```bash
python3 -m venv .venv
```
```bash
source .venv/bin/activate
```
```bash
pip install --upgrade pip setuptools wheel
```
```bash
pip install -r requirements.txt
```

### 3.3 Cek layanan TTS
TTS membutuhkan akses internet ke `speech.platform.bing.com` (HTTPS).
```bash
edge-tts --voice id-ID-ArdiNeural --text "Halo, tes suara." --write-media /tmp/tes.mp3 && ffprobe -v error -show_entries format=duration /tmp/tes.mp3
```
Daftar suara Indonesia: `edge-tts --list-voices | grep id-ID` (ada `id-ID-ArdiNeural` dan `id-ID-GadisNeural`).

---

## 4. Rendering

> Semua perintah dijalankan dari folder project dengan virtualenv aktif (`source .venv/bin/activate`). Script `.sh` sudah mengaktifkan `.venv` otomatis bila ada.

### 4.1 Satu perintah
Preview cepat (854×480, 15 fps, ±2–3 menit di 4 core):
```bash
./render_preview.sh
```
Hasil: `build/preview/preview_video.mp4`.

Final (1920×1080, 30 fps, ±15–25 menit di 4 core):
```bash
./render_final.sh
```
Hasil: `final_video.mp4`, `captions.srt`, `captions.vtt`, `narration_script.md`.

Batasi jumlah proses paralel (jika RAM terbatas):
```bash
JOBS=2 ./render_final.sh
```

### 4.2 Render satu scene tertentu
Preview kualitas rendah langsung dengan Manim (paling cepat untuk iterasi visual):
```bash
manim -ql manim/scenes/s10_compute.py S10Compute
```
Preview lalu otomatis buka hasilnya:
```bash
manim -pql manim/scenes/s10_compute.py S10Compute
```
Satu scene kualitas final 1920×1080 @ 30 fps:
```bash
manim -qh --resolution 1920,1080 --frame_rate 30 manim/scenes/s10_compute.py S10Compute
```
Lewat pipeline (hasil disalin ke `build/<quality>/scenes/` dan siap dirakit):
```bash
python scripts/render_scenes.py --quality preview --scenes S10Compute
```
```bash
python scripts/render_scenes.py --quality final --scenes S10Compute S11Construct
```
Render semua scene saja (tanpa merakit):
```bash
python scripts/render_scenes.py --quality final --jobs 4
```

### 4.3 Render ulang setelah mengubah kode / narasi
- **Mengubah animasi satu scene** → render ulang scene itu lalu rakit ulang (scene lain tidak dirender lagi):
  ```bash
  ./render_final.sh S10Compute
  ```
- **Mengubah teks narasi** di `manim/narration.py` → jalankan seluruh pipeline. Hanya segment yang teksnya berubah yang di-TTS ulang (cache di `audio/cache/`), tetapi scene yang memakai segment itu harus dirender ulang karena durasinya berubah:
  ```bash
  ./render_final.sh S07Problem
  ```
  (ganti `S07Problem` dengan scene yang narasinya diubah; tanpa argumen = semua scene).
- **Paksa generate ulang semua audio** (mis. setelah ganti `VOICE`/`RATE` di `narration.py`):
  ```bash
  python scripts/generate_audio.py --force
  ```
- **Mengubah gaya subtitle saja** (font/ukuran di `scripts/build_captions.py`) → tidak perlu render Manim:
  ```bash
  python scripts/build_captions.py --quality final && python scripts/assemble_video.py --quality final
  ```

### 4.4 Menggabungkan animasi + audio + subtitle secara manual
Setiap video scene dari Manim **sudah berisi audio narasinya** (dimasukkan via `add_sound`). Penggabungan:
```bash
python scripts/build_captions.py --quality final
```
```bash
python scripts/assemble_video.py --quality final
```
Ekuivalen ffmpeg-nya (untuk referensi):
```bash
ffmpeg -f concat -safe 0 -i build/final/concat.txt -c copy build/final/joined.mp4
```
```bash
ffmpeg -i build/final/joined.mp4 -vf "ass=build/final/captions.ass:fontsdir=/usr/share/fonts,fps=30,format=yuv420p" -c:v libx264 -crf 20 -preset medium -tune animation -af loudnorm=I=-16:TP=-1.5:LRA=11 -c:a aac -b:a 192k -ar 48000 -movflags +faststart final_video.mp4
```
Versi tanpa subtitle burn-in (subtitle sebagai track terpisah / soft-sub):
```bash
ffmpeg -i build/final/joined.mp4 -i captions.srt -c:v copy -c:a copy -c:s mov_text -metadata:s:s:0 language=ind video_softsub.mp4
```

### 4.5 Validasi & review visual
```bash
python scripts/validate.py --quality final
```
```bash
python scripts/contact_sheet.py --quality final
```
`contact_sheet.py` membuat `build/final/contact/<Scene>.png` berisi frame di akhir setiap segment narasi — cara cepat mengecek layout tanpa menonton seluruh video.

---

## 5. Mengedit konten

- **Narasi**: edit `manim/narration.py` (`SCENES` → daftar `(segment_id, teks)`). Notasi seperti `dp[i-1]`, `O(n²)`, `-2` boleh ditulis apa adanya; `to_speech()` mengubahnya menjadi ucapan ("d p i minus 1", "big O n kuadrat", "minus 2") hanya untuk TTS, caption tetap memakai notasi.
- **Suara**: ubah `VOICE`, `RATE`, `PITCH` di `manim/narration.py`, lalu `python scripts/generate_audio.py --force`.
- **Tampilan**: warna, font, dan komponen di `manim/lecture.py` (`BG`, `BLUE`, `ORANGE`, `CodePanel`, `ArrayRow`, `grid_table`, `title_bar`).
- **Menambah scene**: buat `manim/scenes/sXX_nama.py` berisi class turunan `LectureScene`, tambahkan entri ke `SCENES` di `narration.py` (urutan di sana = urutan video).
- Area subtitle: konten Manim dijaga di atas y ≈ −2.8 (unit Manim) agar tidak tertutup subtitle.

---

## 6. Troubleshooting

| Gejala | Penyebab & solusi |
|---|---|
| `pip install manim` gagal: `Package 'pangocairo' was not found` | Header Pango belum ada: `sudo apt-get install -y libpango1.0-dev pkg-config`, lalu ulangi pip. |
| `Could not build wheels for srt` | setuptools lama di Python sistem. Gunakan venv dan `pip install --upgrade pip setuptools wheel` sebelum install. |
| `edge_tts ... Cannot connect to host speech.platform.bing.com` / `ClientConnectorDNSError` | Tidak ada akses internet ke host TTS. Pastikan firewall/proxy mengizinkan `speech.platform.bing.com`. Di balik proxy, set `HTTPS_PROXY` (script otomatis meneruskannya ke edge-tts) atau `TTS_PROXY=http://host:port`. |
| `SkewAdjustmentError: No server date in headers` | Request TTS diblokir/diganggu proxy (respons bukan dari server Microsoft). Izinkan host di atas, lalu jalankan ulang `python scripts/generate_audio.py` (otomatis retry 5×). |
| Error SSL saat TTS | Set CA bundle: `export SSL_CERT_FILE=/path/to/ca-bundle.crt`. |
| `[WARN] audio untuk ... belum ada` saat render | `audio/manifest.json` belum ada / segment baru. Jalankan `python scripts/generate_audio.py` dulu. Tanpa audio, scene tetap dirender dengan durasi estimasi (hanya untuk uji visual). |
| `There are no scenes inside that module` | Render file scene-nya langsung (`manim/scenes/sXX_*.py`), bukan modul lain yang meng-import scene. |
| `FileNotFoundError ... media/texts/*.svg` saat render paralel | Beberapa proses Manim berbagi cache teks. Pakai `scripts/render_scenes.py` (tiap scene punya `media_dir` sendiri) atau render serial. |
| Font tampak berbeda / warning `Font Inter not in ...` | Install font Inter & DejaVu (`fonts-inter fonts-dejavu-core`) lalu `fc-cache -f`. Cek: `fc-list | grep -i -E "inter|dejavu sans mono"`. |
| Subtitle tidak muncul di video | ffmpeg tanpa libass. Cek `ffmpeg -filters | grep " ass "`; install ffmpeg dari distro (`apt-get install ffmpeg`). |
| Subtitle tidak sinkron setelah edit | Jalankan ulang `build_captions.py` **setelah** scene yang berubah dirender ulang (timing diambil dari `build/<quality>/timings`). `./render_final.sh` sudah melakukannya berurutan. |
| `concat` gagal / audio hilang di sebagian scene | Semua scene harus dirender dengan quality yang sama. Render ulang: `python scripts/render_scenes.py --quality final`. |
| Render lambat / kehabisan RAM | Kurangi paralel: `JOBS=1 ./render_final.sh`; iterasi pakai `./render_preview.sh`. |
| `No space left on device` | Hapus `build/preview` / `build/final/media` (file sementara, bisa digenerate ulang). |
| `validate.py` FAIL "jeda hening > 6 detik" | Ada animasi yang lebih panjang dari narasinya. Cek scene terkait dan percepat `run_time` animasi. |

---

## 7. Spesifikasi output

- Video: 1920×1080 (16:9), 30 fps, H.264 High (yuv420p, `+faststart`), CRF 20
- Audio: AAC 192 kb/s, 48 kHz stereo, loudness dinormalisasi −16 LUFS
- Subtitle burn-in: Inter 44 px, kotak semi-transparan di tengah bawah; file `.srt` & `.vtt` (UTF-8), maks. 2 baris per cue
- Referensi materi: Cormen et al. (2022) *Introduction to Algorithms* 4th ed., Ch. 14.3; Skiena (2020) *The Algorithm Design Manual* 3rd ed., Ch. 10.1
