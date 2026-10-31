set -e
TC=$(python3 -c "import json;print(json.load(open('e11_meta.json'))['tc'])")
A=$(python3 -c "print($TC-0.2)"); B=$(python3 -c "print($TC+5.2)")
TOT=$(python3 -c "import json;print(json.load(open('e11_meta.json'))['total'])")
FO=$(python3 -c "print($TOT-2)")
ffmpeg -y -loglevel error -i voice_e11.wav -i music_e11.wav -filter_complex "[1:a]volume='if(between(t,$A,$B),0.03,0.10)':eval=frame,afade=t=in:d=1,afade=t=out:st=$FO:d=2[m];[0:a][m]amix=inputs=2:duration=first:normalize=0,loudnorm=I=-16:TP=-1.5:LRA=11,aresample=44100[a]" -map "[a]" -c:a aac -b:a 192k mix_e11.m4a
ffmpeg -y -loglevel error -i video_e11.mp4 -i mix_e11.m4a -c:v copy -c:a copy -shortest Enigme_e11.mp4
ffprobe -v error -show_entries format=duration -of csv=p=0 Enigme_e11.mp4
