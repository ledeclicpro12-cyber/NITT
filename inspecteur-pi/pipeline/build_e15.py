from PIL import Image
import wave, subprocess, numpy as np, os, json
import render_e15 as R
G='ep15/voix/'
SP=1.10; SR=24000; FPS=24
def load(name, lead):
    out='tmp_e15_'+name+'.wav'
    subprocess.run(['ffmpeg','-y','-loglevel','error','-i',G+name+'.wav','-af',f'atempo={SP}','-ar',str(SR),out],check=True)
    w=wave.open(out); x=np.frombuffer(w.readframes(w.getnframes()),dtype=np.int16).astype(np.float32)/32768
    a=int(max(lead-0.03,0)/SP*SR); s=x[a:].copy(); f=int(.01*SR); s[:f]*=np.linspace(0,1,f); f=int(.04*SR); s[-f:]*=np.linspace(1,0,f); return s
def sil(d): return np.zeros(int(d*SR),np.float32)
def ticks5():
    out=np.zeros(5*SR,np.float32)
    for k in range(5):
        f0=1320 if k==4 else 1000
        L=int(.07*SR); t=np.arange(L)/SR; out[k*SR:k*SR+L]+=0.16*np.sin(2*np.pi*f0*t)*np.exp(-t*45)
    return out
T={}; pos=0.0; parts=[]
def add(arr,gap):
    global pos; st=pos; parts.append(arr); pos+=len(arr)/SR; parts.append(sil(gap)); pos+=gap; return st
def at(st,t,lead): return st+(t-lead)/SP
L=0.0; a=add(load('01_histoire',L),0.35); T['cover']=0
for k,t in [('s1', 0.38), ('s2', 1.2), ('s3', 2.66), ('s4', 4.5), ('s5', 6.2), ('s6', 7.1), ('s7', 8.48), ('s8', 10.58), ('s9', 12.54), ('s10', 14.66), ('s11', 15.98), ('s12', 16.71), ('s13', 17.56), ('s14', 18.62), ('s15', 20.72), ('q', 22.7)]: T[k]=at(a,t,L)
b_=add(load('02_defi',0.0),0.10); T['dec']=b_
tc=pos; parts.append(ticks5()); pos+=5.0; parts.append(sil(0.3)); pos+=0.3
L=0.2; c_=add(load('03_reponse',L),0.5)
for k,t in [('r0', 0.3), ('r1', 2.68), ('r2', 3.83), ('r3', 5.5), ('r4', 9.08), ('r5', 11.68), ('r6', 13.16), ('r7', 16.05), ('r8', 17.27), ('r9', 18.5), ('r10', 20.48), ('r11', 21.7), ('r12', 22.73), ('r13', 25.18), ('r14', 27.45)]: T[k]=at(c_,t,L)
L=0.0; e=add(load('04_fin',L),0.9)
for k,t in [('e0', 0.0), ('e1', 2.62), ('e2', 5.36), ('e3', 6.5)]: T[k]=at(e,t,L)
y=np.concatenate(parts); TOTAL=len(y)/SR
def click(st,f0=1800,vol=0.5):
    a=int(st*SR); L=int(.05*SR); t=np.arange(L)/SR
    y[a:a+L]+=vol*(np.random.RandomState(1).randn(L)*np.exp(-t*140)*0.6+np.sin(2*np.pi*f0*t)*np.exp(-t*90)*0.5)
def thump(st,vol=0.7):
    a=int(st*SR); L=int(.30*SR); t=np.arange(L)/SR
    y[a:a+L]+=vol*np.sin(2*np.pi*(90-60*t)*t)*np.exp(-t*12)
def chime(st,vol=0.25):
    for i,m in enumerate((72,76,79,84)):
        a=int((st+i*0.09)*SR); L=int(.45*SR); t=np.arange(L)/SR; y[a:a+L]+=vol*np.sin(2*np.pi*440*2**((m-69)/12)*t)*np.exp(-t*7)*np.minimum(1,t*300)
def whoosh(st,vol=0.12):
    a=int(st*SR); L=int(.16*SR); t=np.arange(L)/SR; n=np.random.RandomState(2).randn(L); env=np.sin(np.pi*t/0.16)
    y[a:a+L]+=vol*n*env*0.5
V=1/SP
for k in ['s2', 's3', 's4', 's5', 's6', 's7', 's8', 's9', 's10', 's11', 's12', 's13', 's14', 's15', 'q', 'r1', 'r2', 'r3', 'r4', 'r5', 'r6', 'r7', 'r8', 'r9', 'r10', 'r11', 'r12', 'r13', 'r14']: whoosh(T[k]-0.03)
chime(T['r0']); chime(T['r13'])

y=np.clip(y,-1,1)
w=wave.open('voice_e15.wav','wb'); w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((np.clip(y,-1,1)*32767).astype(np.int16).tobytes()); w.close()
json.dump({'tc':tc,'total':TOTAL},open('e15_meta.json','w'))
T['cd']=tc
order=['cover', 's1', 's2', 's3', 's4', 's5', 's6', 's7', 's8', 's9', 's10', 's11', 's12', 's13', 's14', 's15', 'q', 'dec', 'cd', 'r0', 'r1', 'r2', 'r3', 'r4', 'r5', 'r6', 'r7', 'r8', 'r9', 'r10', 'r11', 'r12', 'r13', 'r14', 'e0', 'e1', 'e2', 'e3']
TL=[(T[k],k) for k in order]
for i in range(1,len(TL)): assert TL[i][0]>TL[i-1][0],(TL[i-1],TL[i])
print('total',round(TOTAL,2),'tc',round(tc,2),{k:round(v,1) for k,v in T.items()})
def frame(t):
    i=max(j for j,(t0,k) in enumerate(TL) if t0<=t); t0,k=TL[i]
    if i>0 and t-t0<0.14 and TL[i-1][1] not in ('cd','dec','cover') and k not in ('cd','dec') and not k.startswith('e'):
        a=frame_raw(t0-0.01); b=frame_raw(t); return Image.blend(a.convert('RGB'),b.convert('RGB'),(t-t0)/0.14)
    return frame_raw(t)
def frame_raw(t):
    i=max(j for j,(t0,k) in enumerate(TL) if t0<=t); t0,k=TL[i]; t1=TL[i+1][0] if i+1<len(TL) else TOTAL
    if k=='cover': return R.cover(t)
    if k in R.STORY: return R.story(k,t,(t0,t1),T)
    if k[0]=='r': return R.answer(k,t,(t0,t1),T)
    if k=='dec': return R.decide(5,t)
    if k=='cd':
        n=max(1,5-int(t-tc)); return R.decide(n,t,ft=(t-tc)%1.0)
    return R.end(int(k[1]),t)
if __name__=='__main__':
    n=int(TOTAL*FPS)
    pr=subprocess.Popen(['ffmpeg','-y','-loglevel','error','-f','rawvideo','-pix_fmt','rgb24','-s','1080x1920','-r',str(FPS),'-i','-','-c:v','libx264','-preset','veryfast','-crf','20','-pix_fmt','yuv420p','video_e15.mp4'],stdin=subprocess.PIPE)
    for f in range(n): pr.stdin.write(frame(f/FPS).convert('RGB').tobytes())
    pr.stdin.close(); pr.wait(); print('frames',n)
