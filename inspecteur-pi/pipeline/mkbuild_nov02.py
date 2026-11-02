import re
src=open('build_e15.py').read()
def mk(n,story,ans,fin,chimes,nxt=None):
    s=src.replace('render_e15','render_e%s'%n).replace('ep15/voix/','ep%s/voix/'%n).replace('tmp_e15_','tmp_e%s_'%n).replace('voice_e15','voice_e%s'%n).replace('e15_meta','e%s_meta'%n).replace('video_e15','video_e%s'%n)
    s=re.sub(r"for k,t in \[\('s1'.*?\]: T\[k\]=at\(a,t,L\)",lambda m:"for k,t in %r: T[k]=at(a,t,L)"%story,s,flags=re.S)
    s=re.sub(r"for k,t in \[\('r0'.*?\]: T\[k\]=at\(c_,t,L\)",lambda m:"for k,t in %r: T[k]=at(c_,t,L)"%ans,s,flags=re.S)
    s=re.sub(r"for k,t in \[\('e0'.*?\]: T\[k\]=at\(e,t,L\)",lambda m:"for k,t in %r: T[k]=at(e,t,L)"%fin,s,flags=re.S)
    order=['cover']+[k for k,_ in story]+['dec','cd']+[k for k,_ in ans]+['e0','e1','e2','e3']
    s=re.sub(r"order=\[.*?\]\n",lambda m:"order=%r\n"%order,s,count=1,flags=re.S)
    wh=[k for k,_ in story[1:]]+[k for k,_ in ans[1:]]
    s=re.sub(r"for k in \['s2'.*?\]: whoosh",lambda m:"for k in %r: whoosh"%wh,s,flags=re.S)
    s=re.sub(r"chime\(T\['r0'\]\); chime\(T\['r13'\]\)",";".join("chime(T[%r])"%c for c in chimes),s)
    open('build_e%s.py'%n,'w').write(s)
    return order
if __name__=='__main__':
    st=[('s1', 0.30), ('s2', 1.44), ('s3', 2.86), ('s4', 4.14), ('s5', 5.30), ('s6', 6.24), ('s7', 7.98), ('s8', 9.42), ('s9', 10.92), ('s10', 12.04), ('s11', 13.44), ('s12', 14.94), ('s13', 15.96), ('s14', 17.62), ('s15', 19.44), ('q', 21.56)]
    an=[('r0', 0.00), ('r1', 0.90), ('r2', 2.90), ('r3', 4.48), ('r4', 5.98), ('r5', 7.18), ('r6', 8.38), ('r7', 9.68), ('r8', 10.80), ('r9', 12.24), ('r10', 13.30), ('r11', 14.42), ('r12', 15.94), ('r13', 16.74), ('r14', 17.42), ('r15', 19.38), ('r16', 21.86), ('r17', 23.74), ('r18', 24.58), ('r19', 26.18), ('r20', 27.42)]
    fin=[('e0', 0.0), ('e1', 2.62), ('e2', 5.36), ('e3', 6.5)]
    mk('16',st,an,fin,['r1','r19'])
