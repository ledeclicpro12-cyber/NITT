import re,sys
b=open('build14.py').read()
def mk(ep,dirn,story,ans,endt,sound_lines,V):
    x=b.replace("render14 as R","render_%s as R"%ep).replace("'ep11/voix/'","'%s/voix/'"%dirn).replace("tmp14_","tmp_%s_"%ep).replace("voice_ep14.wav","voice_%s.wav"%ep).replace("ep14_meta.json","%s_meta.json"%ep).replace("video_ep14.mp4","video_%s.mp4"%ep)
    x=re.sub(r"for k,t in \[\('s1'.*?\]: T\[k\]=at\(a,t,L\)",lambda m:"for k,t in %r: T[k]=at(a,t,L)"%story,x,flags=re.S)
    x=re.sub(r"for k,t in \[\('r0'.*?\]: T\[k\]=at\(c_,t,L\)",lambda m:"for k,t in %r: T[k]=at(c_,t,L)"%ans,x,flags=re.S)
    x=re.sub(r"for k,t in \[\('e0'.*?\]: T\[k\]=at\(e,t,L\)",lambda m:"for k,t in %r: T[k]=at(e,t,L)"%endt,x,flags=re.S)
    keys=[k for k,_ in story]+[k for k,_ in ans]
    order=['cover']+[k for k,_ in story]+['dec','cd']+[k for k,_ in ans]+['e0','e1','e2','e3']
    x=re.sub(r"order=\[.*?\]\n",lambda m:"order=%r\n"%order,x,count=1,flags=re.S)
    a=x.index("V=1/SP"); bb=x.index("y=np.clip(y,-1,1)\nw=wave")
    x=x[:a]+"V=1/SP\n"+sound_lines+"\n"+x[bb:]
    return x
END=[('e0',0.0),('e1',2.56),('e2',5.42),('e3',6.47)]
# EP10
st=[('s1',0.46),('s2',2.14),('s3',5.0),('s4',8.08),('s5',11.32),('s6',13.84),('s7',15.0),('s8',16.58),('s9',18.48),('q',21.52)]
an=[('r0',0.0),('r1',1.68),('r2',3.92),('r3',7.78),('r4',10.36),('r5',14.82),('r6',20.02),('r7',23.0),('r8',25.56)]
snd10="""for k in ['s2','s3','s5','s6','s7','s8','s9','q','r1','r2','r3','r4','r5','r6','r7']: whoosh(T[k]-0.03)
thump(T['s4'],0.6); thump(T['s4']+1.0*V,0.6); click(T['s1']+0.3); click(T['r2']+1.9*V); click(T['r4']+0.5*V); click(T['r6']+0.6*V)
chime(T['r8'])
"""
open('build_e10.py','w').write(mk('e10','ep10',st,an,END,snd10,1))
# EP11
st=[('s1',0.5),('s2',4.86),('s3',7.58),('s4',9.3),('s5',11.6),('s6',13.18),('s7',15.48),('s8',17.68),('q',19.38)]
an=[('r0',0.0),('r1',3.08),('r2',4.3),('r3',7.7),('r4',11.86),('r5',16.5),('r6',19.56)]
snd11="""for k in ['s2','s3','s4','s5','s6','s7','s8','q','r1','r2','r3','r4','r5','r6']: whoosh(T[k]-0.03)
click(T['s5']+0.9*V); click(T['s6']+0.6*V); click(T['s7']+0.9*V); click(T['s8']+0.6*V)
chime(T['r0']); chime(T['r5'])
"""
open('build_e11.py','w').write(mk('e11','ep11b',st,an,END,snd11,1))
