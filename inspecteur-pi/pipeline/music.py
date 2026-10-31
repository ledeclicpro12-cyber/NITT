import numpy as np, wave
SR=24000; DUR=TOTALD; bpm=110; beat=60/bpm; n=int(DUR*SR); y=np.zeros(n,np.float32)
def f(m): return 440*2**((m-69)/12)
def sq(fr,L,duty=.5):
    t=np.arange(L)/SR; return np.where((t*fr)%1<duty,1.,-1.).astype(np.float32)
def note(m,start,dur,vol,duty=.5,decay=6):
    a=int(start*SR); L=int(dur*SR)
    if a>=n: return
    L=min(L,n-a); t=np.arange(L)/SR
    env=np.exp(-t*decay)*np.minimum(1,t*400); y[a:a+L]+=vol*sq(f(m),L,duty)*env
prog=[(57,[57,60,64]),(53,[53,57,60]),(48,[48,52,55]),(55,[55,59,62])]  # Am F C G
bar=4*beat; nb=int(DUR/bar)+1
for b in range(nb):
    root,ch=prog[b%4]; s0=b*bar
    for i in range(8):
        note(root-12,s0+i*beat/2,beat/2*.9,.5,.25,5)
    for i in range(16):
        note(ch[i%3]+12,s0+i*beat/4,beat/4,.35,.5,14)
    note(ch[0]+24,s0,beat,.0,.5)
y/=np.abs(y).max(); y*=0.5
w=wave.open('music.wav','wb'); w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((y*32767).astype(np.int16).tobytes()); w.close()
