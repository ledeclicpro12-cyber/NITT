from render14 import *
import render14 as R14
B.NUM='#010'
SAND=rgb('#FFD23F'); WOOD=rgb('#8A5A34'); GLASS=rgb('#5A6BA8')
def lin(a,b,p): return a+(b-a)*max(0,min(1,p))
def chamber(dd,y0,y1,hw0,hw1,cx,f,col):
    if f<=0.005: return
    ys=y1-f*(y1-y0)
    def hw(y): return hw0+(hw1-hw0)*((y-y0)/(y1-y0))
    pts=[(cx-hw(ys),ys),(cx+hw(ys),ys),(cx+hw(y1),y1),(cx-hw(y1),y1)]
    dd.polygon([(px*S,py*S) for px,py in pts],fill=col)
def hourglass(dd,cx,top,w,h,ftop,fbot,hl=False,flow=False,label=None,t=0):
    cap=8; ch=(h-2*cap)/2; hw=w/2; nk=3
    ym=top+cap+ch
    # glass body
    for (a,b,h0,h1) in ((top+cap,ym,hw,nk),(ym,top+h-cap,nk,hw)):
        pts=[(cx-h0,a),(cx+h0,a),(cx+h1,b),(cx-h1,b)]
        dd.polygon([(px*S,py*S) for px,py in pts],fill=rgb('#1A2040'),outline=(GOLD if hl else GLASS),width=2*S)
    chamber(dd,top+cap,ym,hw-2,nk,cx,ftop,SAND)
    chamber(dd,ym,top+h-cap,nk,hw-2,cx,fbot,SAND)
    if flow and ftop>0.01:
        yb=ym+(top+h-cap-ym)*(1-fbot)
        box(dd,cx-1,ym-2,2,yb-ym+2,fill=SAND)
    box(dd,cx-hw-5,top,w+10,cap,fill=WOOD,border=DARK,bw=2); box(dd,cx-hw-5,top+h-cap,w+10,cap,fill=WOOD,border=DARK,bw=2)
    if hl: dd.rectangle([(cx-hw-12)*S,(top-6)*S,(cx+hw+12)*S,(top+h+6)*S],outline=GOLD,width=3*S)
    if label: T(dd,label,cx,top+h+10,12,'silk7',10,(GOLD if hl else CREAM),align='c',sp=1)
def bomb(dd,cx,cy,k=1.0,t=0,boom=False):
    if boom:
        r=random.Random(int(t*12)); pts=[]
        for i in range(16):
            a=i*math.pi/8; rr=(64 if i%2 else 36)*k+r.randint(0,8)
            pts.append((cx+math.cos(a)*rr,cy+math.sin(a)*rr))
        dd.polygon([(x*S,y*S) for x,y in pts],fill=(RED if int(t*8)%2 else GOLD))
        dd.polygon([((cx+(x-cx)*0.55)*S,(cy+(y-cy)*0.55)*S) for x,y in pts],fill=rgb('#FFF3B0'))
        return
    disc(dd,cx,cy,30*k,rgb('#1B1F3A'),rgb('#5A6BA8'),3); box(dd,cx-22*k,cy-22*k,10*k,10*k,fill=rgb('#4A5486'))
    box(dd,cx-6*k,cy-42*k,12*k,12*k,fill=rgb('#6A7096'))
    dd.line([(cx*S,(cy-42*k)*S),((cx+16*k)*S,(cy-58*k)*S)],fill=rgb('#C9A24A'),width=3*S)
    if int(t*8)%2==0: disc(dd,cx+18*k,cy-60*k,5*k,GOLD); disc(dd,cx+18*k,cy-60*k,2.5*k,RED)
HEADS={'s1':[('Une ',CREAM),('bombe,',RED),(' un seul geste',CREAM)],'s2':[('Exactement ',CREAM),('9 minutes',GOLD)],
 's3':[("L'inspecteur doit ",CREAM),('désamorcer',CORAL)],'s4':[('Trop tôt ?',CREAM),(' Trop tard ?',CREAM),(' Boum',RED)],
 's5':[('Ni ',CREAM),('montre,',CORAL),(' ni ',CREAM),('téléphone',CORAL)],'s6':[('Juste ',CREAM),('2 sabliers',GOLD)],
 's7':[('Un sablier de ',CREAM),('4 minutes',CYAN)],'s8':[('Un sablier de ',CREAM),('7 minutes',GOLD)],
 's9':[('On peut les ',CREAM),('retourner',CORAL),(' à tout moment',CREAM)],'q':[('Comment mesurer ',CREAM),('9 minutes',GOLD),(' ?',CREAM)],
 'r0':[('La ',CREAM),('solution',GOLD)],'r1':[('On lance les ',CREAM),('2 sabliers',GOLD)],'r2':[('À 4 min : ',CREAM),('on retourne le petit',CYAN)],
 'r3':[('À 7 min : ',CREAM),('le grand finit',GOLD)],'r4':[('On retourne ',CREAM),('le grand',GOLD)],'r5':[('À 8 min : ',CREAM),('le petit finit',CYAN)],
 'r6':[('On retourne ',CREAM),('le grand',GOLD)],'r7':[('1 minute plus tard : ',CREAM),('9 min',GOLD)],'r8':[('Bombe ',CREAM),('désamorcée',CYAN)]}
STORY=('s1','s2','s3','s4','s5','s6','s7','s8','s9','q')
SM,BG_=(70,120,118),(208,192,190)   # cx, top, h for small / big : (cx,top,h)
def two(dd,t,s,b,hls=(0,0),flow=(0,0),clock=None):
    if clock is not None:
        box(dd,SW/2-70,94,140,34,fill=CARD,border=CORAL,bw=3,shadow=(3,3,BLACK))
        T(dd,'MINUTE '+str(clock),SW/2,102,20,'press',16,CREAM,align='c')
    hourglass(dd,82,212,66,118,s[0],s[1],hl=hls[0],flow=flow[0],label='4 MIN',t=t)
    hourglass(dd,226,140,84,190,b[0],b[1],hl=hls[1],flow=flow[1],label='7 MIN',t=t)
def scene_fn(key,t,lt,dur):
    p=lt/max(dur,0.1)
    def fn(lay,dd):
        if key=='s1':
            bomb(dd,SW/2,238,2.0,t); tagc(dd,SW/2,364,'1 BOMBE',RED)
        elif key=='s2':
            T(dd,'9',SW/2,120,120,'press',100,GOLD,align='c',shadow=(5,5,BLACK)); T(dd,'MINUTES',SW/2,262,24,'press',20,CREAM,align='c')
            tagc(dd,SW/2,364,'NI PLUS, NI MOINS',CORAL)
        elif key=='s3':
            insp(dd,90,GY,t,k=4.6); bomb(dd,232,GY-34,1.5,t); tagc(dd,SW/2,364,'À LA 9e MINUTE',GOLD)
        elif key=='s4':
            if lt<1.0:
                T(dd,'TROP TÔT',SW/2,116,40,'press',30,CREAM,align='c',shadow=(3,3,BLACK)); bomb(dd,SW/2,276,1.2,t,boom=lt>0.5)
            else:
                T(dd,'TROP TARD',SW/2,116,40,'press',30,CREAM,align='c',shadow=(3,3,BLACK)); bomb(dd,SW/2,276,1.2,t,boom=True)
            tagc(dd,SW/2,364,'BOUM !',RED)
        elif key=='s5':
            disc(dd,86,200,44,rgb('#1B1F3A'),rgb('#C9A24A'),4); dd.line([(86*S,200*S),(86*S,172*S)],fill=CREAM,width=3*S); dd.line([(86*S,200*S),(104*S,208*S)],fill=CREAM,width=3*S)
            box(dd,184,150,86,150,fill=rgb('#1B1F3A'),border=STEEL,bw=3); box(dd,198,164,58,96,fill=rgb('#0C0F20'))
            if lt>0.5:
                for (a,b_,c,d_) in ((40,156,134,244),(40,244,134,156),(176,142,278,308),(176,308,278,142)):
                    dd.line([(a*S,b_*S),(c*S,d_*S)],fill=RED,width=6*S)
            tagc(dd,SW/2,364,'NI MONTRE, NI TÉLÉPHONE',RED)
        elif key=='s6':
            two(dd,t,(1,0),(1,0)); tagc(dd,SW/2,364,'DEUX SABLIERS',GOLD)
        elif key=='s7':
            two(dd,t,(1,0),(1,0),hls=(1,0)); tagc(dd,SW/2,364,'4 MINUTES',CYAN)
        elif key=='s8':
            two(dd,t,(1,0),(1,0),hls=(0,1)); tagc(dd,SW/2,364,'7 MINUTES',GOLD)
        elif key=='s9':
            fl=0.5+0.5*math.sin(t*5)
            two(dd,t,(fl,1-fl),(1-fl,fl)); tagc(dd,SW/2,364,'ON PEUT LES RETOURNER',CORAL)
        elif key=='q':
            bomb(dd,SW/2,170,1.3,t); T(dd,'?',SW/2,236,100,'press',84,GOLD,align='c',shadow=(4,4,BLACK)); tagc(dd,SW/2,364,'9 MINUTES PILE',GOLD)
        # ---- réponse ----
        elif key=='r0':
            bomb(dd,86,230,1.6,t); T(dd,'9',236,140,100,'press',80,GOLD,align='c',shadow=(4,4,BLACK)); T(dd,'MIN',236,230,20,'press',16,CREAM,align='c')
        elif key=='r1':
            m=int(p*1.0); two(dd,t,(1-0.12*p,0.12*p),(1-0.08*p,0.08*p),flow=(1,1),clock=0); tagc(dd,SW/2,364,'ON LANCE LES DEUX',GOLD)
        elif key=='r2':
            m=4*p; flip=p>0.82
            sf=(1,0) if flip else (0,1)
            if not flip: sf=(1-p/0.82,p/0.82)
            two(dd,t,sf,(1-m/7,m/7),hls=(flip,0),flow=(not flip,1),clock=min(4,int(m+0.01)))
            if flip: tagc(dd,SW/2,364,'ON RETOURNE LE PETIT',CYAN)
            else: tagc(dd,SW/2,364,'4 MIN : LE PETIT FINIT',CYAN)
        elif key=='r3':
            m=4+3*p; sr=max(0,1-(m-4)/4); two(dd,t,(sr,1-sr),(max(0,1-m/7),min(1,m/7)),flow=(1,m<7),clock=int(m+0.01)); tagc(dd,SW/2,364,'7 MIN : LE GRAND FINIT',GOLD)
        elif key=='r4':
            flip=p>0.35
            two(dd,t,(0.25,0.75),((1,0) if flip else (0,1)),hls=(0,flip),clock=7); tagc(dd,SW/2,364,'ON RETOURNE LE GRAND' if flip else 'LE GRAND EST FINI',GOLD)
        elif key=='r5':
            m=7+p; sr=max(0,0.25-0.25*p); br=1-(m-7)/7
            two(dd,t,(sr,1-sr),(br,1-br),flow=(sr>0,1),clock=int(m+0.01)); tagc(dd,SW/2,364,'8 MIN : LE PETIT FINIT',CYAN)
            if p>0.7: T(dd,'1 MIN DE SABLE\nTOMBÉE'.split('\n')[0],226,342-4,12,'silk7',9,GOLD,align='c') if False else None
        elif key=='r6':
            flip=p>0.4
            two(dd,t,(0,1),((1/7,6/7) if flip else (6/7,1/7)),hls=(0,flip),clock=8); tagc(dd,SW/2,364,'IL NE RESTE QUE 1 MIN' if flip else 'ON LE RETOURNE',GOLD)
        elif key=='r7':
            two(dd,t,(0,1),((1-p)/7,1-(1-p)/7),flow=(0,p<0.98),clock=(9 if p>0.9 else 8)); tagc(dd,SW/2,364,'9 MINUTES PILE !',GOLD)
        elif key=='r8':
            insp(dd,86,GY,t,k=4.6); bomb(dd,232,GY-34,1.5,t)
            box(dd,196,150,72,26,fill=CYAN); T(dd,'STOP',232,155,16,'silk7',12,DARK,align='c',sp=1)
            B.confetti(dd,t,t-lt); tagc(dd,SW/2,364,'DÉSAMORCÉE',CYAN)
    return fn
def story(key,t,tl,T_=None):
    lt=t-tl[0]; dur=max(0.5,tl[1]-tl[0])
    return B.frame_with(B.make_scene(scene_fn(key,t,lt,dur),t,head=HEADS[key]),'LE DÉFI' if key in STORY else 'LA RÉPONSE')
answer=story
def cover(t):
    def fn(lay,dd):
        bomb(dd,SW/2,250,2.1,t); insp(dd,52,334,t,k=3.2)
        if int(t*3)%2==0: dd.rectangle([6*S,6*S,(SW-6)*S,(SH-6)*S],outline=RED,width=4*S)
        T(dd,'9 MINUTES PILE,',SW/2,18,40,'anton',32,CREAM,sp=1,align='c',shadow=(3,3,BLACK)); T(dd,'2 SABLIERS',SW/2,58,40,'anton',32,GOLD,sp=1,align='c',shadow=(3,3,BLACK))
        B.band(lay,SH-44,40); d2=ImageDraw.Draw(lay); txt="DÉSAMORCE LA BOMBE"; f=F('silk4',11); T(d2,txt,SW/2-tw(txt,f,1)/2,SH-30,14,'silk4',11,CREAM,sp=1)
    return B.frame_with(B.make_scene(fn,t),'ÉNIGME DU JOUR')
import inspect
_ns=dict(vars(R14)); exec(inspect.getsource(R14.decide).replace('COMMENTE TON PLAN','COMMENTE TA RÉPONSE').replace("[('Écris ton idée en ',CREAM),('commentaire',CORAL),(' !',CREAM)]","[('Écris ton ',CREAM),('idée !',CORAL)]").replace('def decide','def decide_'),_ns)
def decide(n,t,ft=None): return _ns['decide_'](n,t,ft)
_ne=dict(vars(R14)); exec(inspect.getsource(R14.end).replace("'#010 >>'","'#011 >>'").replace('def end','def end_'),_ne)
def end(level,t): return _ne['end_'](level,t)
