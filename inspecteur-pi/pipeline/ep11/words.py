from faster_whisper import WhisperModel
import json,sys,wave,numpy as np
def ld(f):
    w=wave.open(f); x=np.frombuffer(w.readframes(w.getnframes()),dtype=np.int16).astype(np.float32)/32768
    import numpy as np2
    return np.interp(np.arange(0,len(x),1.5),np.arange(len(x)),x).astype(np.float32)
m=WhisperModel('small',device='cpu',compute_type='int8')
out={}
for k in ['01_histoire','03_reponse','02_defi','04_fin']:
    segs,_=m.transcribe(ld(f'voix/{k}.wav'),language='fr',word_timestamps=True,beam_size=5)
    ws=[(w.word.strip(),round(w.start,2),round(w.end,2)) for s in segs for w in s.words]
    out[k]=ws
    print(k,' '.join(f'{w}@{a}' for w,a,b in ws))
json.dump(out,open('words.json','w'),ensure_ascii=False)
