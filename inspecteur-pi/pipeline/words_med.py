import sys,json,wave,numpy as np
from faster_whisper import WhisperModel
def ld(f):
    w=wave.open(f); x=np.frombuffer(w.readframes(w.getnframes()),dtype=np.int16).astype(np.float32)/32768
    return np.interp(np.arange(0,len(x),1.5),np.arange(len(x)),x).astype(np.float32)
m=WhisperModel('medium',device='cpu',compute_type='int8')
out={}
for n in sys.argv[1:]:
    for k in ['01_histoire','03_reponse']:
        segs,_=m.transcribe(ld(f'ep{n}/voix/{k}.wav'),language='fr',word_timestamps=True,beam_size=5,condition_on_previous_text=False)
        ws=[(w.word.strip(),round(w.start,2)) for s in segs for w in s.words]
        out[f'{n}/{k}']=ws; print(n,k,' '.join(f'{w}@{a}' for w,a in ws)); print()
json.dump(out,open('words_medium.json','w'),ensure_ascii=False)
