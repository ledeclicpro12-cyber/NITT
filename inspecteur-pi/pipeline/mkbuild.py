import re,sys
src=open('build_e11.py').read()
def mk(n,story,ans,fin,order,whoosh):
    s=src.replace('render_e11','render_e%s'%n).replace("ep11b/voix/","ep%s/voix/"%n).replace('tmp_e11_','tmp_e%s_'%n).replace('voice_e11','voice_e%s'%n).replace('e11_meta','e%s_meta'%n).replace('video_e11','video_e%s'%n)
    s=re.sub(r"for k,t in \[\('s1'.*?\]: T\[k\]=at\(a,t,L\)",lambda m:"for k,t in %r: T[k]=at(a,t,L)"%story,s,flags=re.S)
    s=re.sub(r"for k,t in \[\('r0'.*?\]: T\[k\]=at\(c_,t,L\)",lambda m:"for k,t in %r: T[k]=at(c_,t,L)"%ans,s,flags=re.S)
    s=re.sub(r"for k,t in \[\('e0'.*?\]: T\[k\]=at\(e,t,L\)",lambda m:"for k,t in %r: T[k]=at(e,t,L)"%fin,s,flags=re.S)
    s=re.sub(r"order=\[.*?\]\n",lambda m:"order=%r\n"%order,s,count=1,flags=re.S)
    s=re.sub(r"for k in \['s2'.*?\]: whoosh",lambda m:"for k in %r: whoosh"%whoosh,s,flags=re.S)
    s=re.sub(r"click\(T\['s5'\].*?\n","",s)
    return s
fin=[('e0',0.0),('e1',2.80),('e2',5.36),('e3',6.41)]
def gen(n,st,an):
    order=['cover']+[k for k,_ in st]+['dec','cd']+[k for k,_ in an]+['e0','e1','e2','e3']
    wh=[k for k,_ in st[1:]]+[k for k,_ in an[1:]]
    open('build_e%s.py'%n,'w').write(mk(n,st,an,fin,order,wh))
