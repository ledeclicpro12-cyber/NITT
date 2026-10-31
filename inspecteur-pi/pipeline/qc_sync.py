import sys, json, wave, numpy as np, importlib
from faster_whisper import WhisperModel
n=sys.argv[1]; kw=json.loads(sys.argv[2])
b=importlib.import_module('build_e'+n)
w=wave.open(f'voice_e{n}.wav'); x=np.frombuffer(w.readframes(w.getnframes()),dtype=np.int16).astype(np.float32)/32768
x=np.interp(np.arange(0,len(x),1.5),np.arange(len(x)),x).astype(np.float32)
m=WhisperModel('small',device='cpu',compute_type='int8')
segs,_=m.transcribe(x,language='fr',word_timestamps=True,beam_size=5)
ws=[(wd.word.strip().lower(),wd.start) for s in segs for wd in s.words]
json.dump(ws,open(f'qc_words_{n}.json','w'),ensure_ascii=False)
print(' '.join(f'{a}@{t:.2f}' for a,t in ws)); print()
TL=dict((k,t) for t,k in b.TL)
for k,(word,occ) in kw.items():
    c=[t for a,t in ws if word in a]
    if len(c)<=occ: print(k,'MOT INTROUVABLE',word); continue
    wt=c[occ]; st=TL[k]; print(f'{k:5s} scene {st:6.2f}  mot "{word}" {wt:6.2f}  delta={wt-st:+.2f}')
