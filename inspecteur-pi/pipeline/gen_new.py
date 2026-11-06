import re,sys
src=open('build_e23.py').read()
def gen(n,st,an,wh_extra,chimes):
    s=src.replace('render_e23','render_e%s'%n).replace('ep23/voix/','ep%s/voix/'%n).replace('tmp_e23_','tmp_e%s_'%n).replace('voice_e23','voice_e%s'%n).replace('e23_meta','e%s_meta'%n).replace('video_e23','video_e%s'%n)
    s=re.sub(r"for k,t in \[\('s1'.*?\]: T\[k\]=at\(a,t,L\)",lambda m:"for k,t in %r: T[k]=at(a,t,L)"%st,s,flags=re.S)
    s=re.sub(r"for k,t in \[\('r0'.*?\]: T\[k\]=at\(c_,t,L\)",lambda m:"for k,t in %r: T[k]=at(c_,t,L)"%an,s,flags=re.S)
    order=['cover']+[k for k,_ in st]+['dec','cd']+[k for k,_ in an]+['e0','e1','e2','e3']
    s=re.sub(r"order=\[.*?\]\n",lambda m:"order=%r\n"%order,s,count=1,flags=re.S)
    wh=[k for k,_ in st[1:]]+[k for k,_ in an[1:]]
    s=re.sub(r"for k in \['s2'.*?\]: whoosh",lambda m:"for k in %r: whoosh"%wh,s,flags=re.S)
    s=s.replace("chime(T['r4']);chime(T['r7'])",";".join("chime(T['%s'])"%c for c in chimes))
    assert 'render_e%s'%n in s and "chime(T['%s'])"%chimes[0] in s
    open('build_e%s.py'%n,'w').write(s)
st24=[('s1',0.05),('s2',3.62),('s3',6.52),('s4',8.40),('s5',10.64),('s6',13.12),('s7',15.48),('q',18.66)]
an24=[('r0',0.0),('r1',2.44),('r2',4.56),('r3',7.16),('r4',10.0),('r5',13.66),('r6',16.66),('r7',18.68),('r8',21.58),('r9',22.96),('r10',25.10)]
gen('24',st24,an24,None,['r0','r8'])
st25=[('s1',0.05),('s2',4.34),('s3',7.04),('s4',9.68),('s5',12.26),('s6',15.10),('q',17.90)]
an25=[('r0',0.0),('r1',3.04),('r2',5.30),('r3',7.76),('r4',10.28),('r5',13.54),('r6',15.80),('r7',18.32),('r8',21.34),('r9',24.88)]
gen('25',st25,an25,None,['r0','r8'])
