#!/usr/bin/env bash
# Render FINAL (1920x1080, 30 fps, H.264 + AAC) lengkap dengan narasi + subtitle burn-in.
# Hasil: final_video.mp4, captions.srt, captions.vtt, narration_script.md
#
#   ./render_final.sh                         # semua scene
#   ./render_final.sh S10Compute              # render ulang scene tertentu saja, lalu rakit ulang
#   JOBS=2 ./render_final.sh                  # batasi jumlah render paralel (hemat RAM/CPU)
set -euo pipefail
cd "$(dirname "$0")"
[ -f .venv/bin/activate ] && source .venv/bin/activate
[ -f /root/.ccr/ca-bundle.crt ] && export SSL_CERT_FILE="${SSL_CERT_FILE:-/root/.ccr/ca-bundle.crt}"
JOBS="${JOBS:-4}"

SCENES=("$@")
echo "== 1/5 Generate audio narasi (TTS, cache) =="
python scripts/generate_audio.py
python scripts/export_script_md.py
echo "== 2/5 Render scene Manim (1920x1080 @ 30fps) =="
if [ ${#SCENES[@]} -gt 0 ]; then
  python scripts/render_scenes.py --quality final --jobs "$JOBS" --scenes "${SCENES[@]}"
else
  python scripts/render_scenes.py --quality final --jobs "$JOBS"
fi
echo "== 3/5 Build caption (captions.srt, captions.vtt) =="
python scripts/build_captions.py --quality final
echo "== 4/5 Gabung video + audio + burn subtitle =="
python scripts/assemble_video.py --quality final
echo "== 5/5 Validasi =="
python scripts/validate.py --quality final
echo "Video final siap: final_video.mp4"
