#!/usr/bin/env bash
# Render PREVIEW cepat (854x480, 15 fps) lengkap dengan audio + subtitle.
# Hasil: build/preview/preview_video.mp4 (+ captions.srt/.vtt di build/preview/)
#
#   ./render_preview.sh                         # semua scene
#   ./render_preview.sh S10Compute S11Construct # hanya scene tertentu (scene lain memakai hasil render sebelumnya)
set -euo pipefail
cd "$(dirname "$0")"
[ -f .venv/bin/activate ] && source .venv/bin/activate
[ -f /root/.ccr/ca-bundle.crt ] && export SSL_CERT_FILE="${SSL_CERT_FILE:-/root/.ccr/ca-bundle.crt}"

SCENES=("$@")
echo "== 1/5 Generate audio narasi (TTS, cache) =="
python scripts/generate_audio.py
python scripts/export_script_md.py
echo "== 2/5 Render scene Manim (preview) =="
if [ ${#SCENES[@]} -gt 0 ]; then
  python scripts/render_scenes.py --quality preview --scenes "${SCENES[@]}"
else
  python scripts/render_scenes.py --quality preview
fi
echo "== 3/5 Build caption =="
python scripts/build_captions.py --quality preview
echo "== 4/5 Gabung video + audio + subtitle =="
python scripts/assemble_video.py --quality preview
echo "== 5/5 Validasi =="
python scripts/validate.py --quality preview
echo "Preview siap: build/preview/preview_video.mp4"
