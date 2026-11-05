import sys,json,wave,numpy as np,importlib
from faster_whisper import WhisperModel
n=sys.argv[1]; b=importlib.import_module('build_e'+n)
w=wave.open(f'voice_e{n}.wav'); x=np.frombuffer(w.readframes(w.getnframes()),dtype=np.int16).astype(np.float32)/32768
x=np.interp(np.arange(0,len(x),1.5),np.arange(len(x)),x).astype(np.float32)
m=WhisperModel('small',device='cpu',compute_type='int8')
segs,_=m.transcribe(x,language='fr',word_timestamps=True,beam_size=5)
ws=[(wd.word.strip(),round(wd.start,2)) for s in segs for wd in s.words]
for t,k in b.TL:
    if k in('cover','cd','dec'): continue
    c=[(a,s) for a,s in ws if s>=t-0.5][:3]
    print(f'{k:4s} {t:6.2f} ->',' | '.join(f'{a}@{s-t:+.2f}' for a,s in c))
