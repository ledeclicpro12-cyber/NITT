set -e
N=$1
TOT=$(python3 -c "import json;print(json.load(open('e${N}_meta.json'))['total'])")
D=$(python3 -c "print(round($TOT+1,2))")
sed "s/TOTALD/$D/;s/music.wav/music_e${N}.wav/" music.py > music_e${N}.py
python3 music_e${N}.py
sed "s/e15/e${N}/g" mux_e15.sh > mux_e${N}.sh
bash mux_e${N}.sh
