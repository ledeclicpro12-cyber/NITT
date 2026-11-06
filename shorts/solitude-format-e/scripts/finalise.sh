#!/bin/bash
# Chaîne complète pour le Format E (Solitude) : timeline → musique → mixage → -14 LUFS → rendu → contrôles.
set -e
cd "$(dirname "$0")/.."
FF="npx remotion ffmpeg -hide_banner"
R="--log=error ${REMOTION_FLAGS:-}"
node scripts/timeline.mjs
node scripts/music.mjs
node scripts/mix.mjs
mv public/mix.wav public/mix-brut.wav
lufs() { $FF -i "$1" -af loudnorm=I=-14:TP=-1.5:print_format=json -f null - 2>&1 | grep '"input_i"' | grep -oE '[-0-9.]+'; }
I=$(lufs public/mix-brut.wav)
G=$(node -e "console.log((-14 - $I + 0.25).toFixed(2))")
node scripts/limiter.mjs public/mix-brut.wav public/mix.wav $G -1.6
echo "mix brut $I LUFS, gain $G dB → $(lufs public/mix.wav) LUFS"
npx remotion render Solitude out/declic-solitude.mp4 --audio-bitrate=320k $R
npx remotion still Cover out/cover-solitude.jpg --image-format=jpeg --jpeg-quality=90 $R
$FF -y -loglevel error -i out/declic-solitude.mp4 -vn -c:a pcm_s16le -ar 48000 out/controle.wav
echo "dans le mp4 : $(lufs out/controle.wav) LUFS"
