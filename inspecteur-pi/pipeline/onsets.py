import sys,wave,numpy as np
def onsets(f,thr=0.02,gap=0.07):
    w=wave.open(f); x=np.frombuffer(w.readframes(w.getnframes()),dtype=np.int16).astype(np.float32)/32768
    h=120; r=np.array([np.sqrt(np.mean(x[i:i+h]**2)) for i in range(0,len(x)-h,h//2)])  # 2.5ms hop? hop=60 samples=2.5ms
    hop=60/24000; sp=r>thr; out=[]; i=0; n=len(sp)
    while i<n:
        if sp[i]:
            # start of speech after >=gap of silence
            j=i-1; k=0
            while j>=0 and not sp[j]: j-=1
            if (i-j)*hop>=gap or j<0: out.append(round(i*hop,2))
            # skip to end of this speech run (allowing short gaps)
            e=i
            while e<n and (sp[e] or (e+int(gap/hop)<n and sp[e:e+int(gap/hop)].any())): e+=1
            i=e
        else: i+=1
    return out
if __name__=="__main__":
    for f in sys.argv[1:]: print(f,onsets(f))
