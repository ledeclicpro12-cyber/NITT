from render_x import *
B.NUM='#019'
HEADS={'s1':[('Quatre ',GOLD),('personnes',CREAM)],
 's2':[('Une seule ',CREAM),('lampe',GOLD)],
 's3':[('Le pont va ',CREAM),('s’effondrer',RED)],
 's4':[('Traverser ',CREAM),('de nuit',CYAN)],
 's5':[('Pont étroit : ',CREAM),('2 maximum',GOLD)],
 's6':[('Toujours ',CREAM),('la lampe',GOLD)],
 's7':[('L’inspecteur : ',CREAM),('1 minute',GOLD)],
 's8':[('Les ',CREAM),('3 témoins',CORAL)],
 's9':[('À deux : ',CREAM),('le plus lent',CORAL)],
 'q':[('Temps ',CREAM),('minimum',GOLD),(' ?',CREAM)],
 'r0':[('La réponse : ',CREAM),('17 minutes',GOLD)],
 'r1':[('Et ',CREAM),('pas 19',RED)],
 'r2':[('Voici ',CREAM),('comment',CYAN)],
 'r3':[('Étape 1 : ',CREAM),('2 minutes',CYAN)],
 'r4':[('Étape 2 : ',CREAM),('1 minute',GOLD)],
 'r5':[('Étape 3 : ',CREAM),('10 minutes',CORAL)],
 'r6':[('Étape 4 : ',CREAM),('2 minutes',CYAN)],
 'r7':[('Étape 5 : ',CREAM),('2 minutes',CYAN)],
 'r8':[('Le ',CREAM),('total',GOLD)],
 'r9':[('Total : ',CREAM),('17 minutes',GOLD)],
 'r10':[('L’astuce',GOLD)]}
STORY=('s1','s2','s3','s4','s5','s6','s7','s8','s9','q')
VIO=rgb('#B05CFF'); PNK=rgb('#FF7AB8'); BLU=rgb('#4DA3FF')
PCOL={0:GOLD,1:CYAN,2:VIO,3:PNK}
MIN={0:1,1:2,2:5,3:10}
def wpal(i):
    p=dict(MPAL); p['T']={1:'#4DA3FF',2:'#B05CFF',3:'#FF7AB8'}[i]; return p
WPAL={i:wpal(i) for i in (1,2,3)}
SKY=rgb('#0A0E24'); BANK=rgb('#1A1F3C'); BANKT=rgb('#3A4270'); DECK=272
def stars(dd,t):
    r=_r(7)
    for k in range(46):
        x=r.randint(8,SW-8); y=r.randint(90,230); tw_=(int(t*2+k)%3)
        if tw_==0: box(dd,x,y,2,2,fill=rgb('#6A7096'))
        else: box(dd,x,y,2,2,fill=rgb('#2E3560'))
def _r(s):
    import random; return random.Random(s)
def moon(dd,cx=266,cy=118,r=15):
    disc(dd,cx,cy,r,rgb('#E9E2C8')); disc(dd,cx+6,cy-4,r-2,SKY)
def night(dd,t,planks_fall=None,shake=0.0):
    box(dd,0,0,SW,SH,fill=SKY); stars(dd,t); moon(dd)
    # gouffre
    box(dd,0,DECK-8,SW,SH-DECK+8,fill=rgb('#05060F'))
    for x in range(8,SW,26): box(dd,x,DECK,2,SH-DECK,fill=rgb('#0B0E22'))
    # berges (plateformes en perspective : 2 rangées)
    for x0,x1 in ((0,112),(200,SW)):
        box(dd,x0,DECK-30,x1-x0,SH-DECK+30,fill=BANK); box(dd,x0,DECK-30,x1-x0,30,fill=rgb('#232A52')); box(dd,x0,DECK-30,x1-x0,3,fill=BANKT)
        for yy in range(DECK+14,SH,22): box(dd,x0,yy,x1-x0,2,fill=rgb('#222850'))
    # pont
    for i in range(8):
        x=112+i*11; dy=0
        if planks_fall and i in planks_fall:
            f=planks_fall[i]; dy=max(0,f)*f*110 if f>0 else 0
            if f>0 and dy>130: continue
        box(dd,x,DECK-12+dy+(math.sin(t*30+i)*shake if shake else 0),10,8,fill=rgb('#7A5A3A'),border=rgb('#4A3524'),bw=1)
    # cordes
    box(dd,110,DECK-44,4,34,fill=rgb('#5A4330')); box(dd,198,DECK-44,4,34,fill=rgb('#5A4330'))
    for i in range(0,88,4):
        x=114+i; y=DECK-42+int(math.sin(i/88*math.pi)*5)
        box(dd,x,y,4,2,fill=rgb('#8A6B4A'))
SLOT={'L':{0:(24,DECK),1:(74,DECK),2:(50,DECK-24),3:(98,DECK-24)},'R':{0:(288,DECK),1:(238,DECK),2:(262,DECK-24),3:(214,DECK-24)}}
BF=DECK-6
def person(dd,i,cx,t,k=None,feet=DECK,ph=0.0):
    if i==0: insp(dd,cx,feet,t,k=k or 1.9)
    else: pri(dd,cx,feet,t,k=k or 3.0,pal=WPAL[i],ph=ph+i)
def plabel(dd,i,cx,feet=DECK,hl=False,k=1.0):
    h=46 if i==0 else 42
    txt=str(MIN[i]); f=F('silk7',11); w=tw(txt,f,1)+12
    box(dd,cx-w/2,feet-h-24,w,18,fill=CARD,border=(GOLD if hl else PCOL[i]),bw=2); T(dd,txt,cx-w/2+6,feet-h-20,12,'silk7',11,PCOL[i],sp=1)
def lantern(dd,cx,cy,t,k=1.0,lit=True):
    box(dd,cx-8*k,cy-14*k,16*k,4*k,fill=STEEL); box(dd,cx-8*k,cy+10*k,16*k,4*k,fill=STEEL)
    box(dd,cx-6*k,cy-10*k,12*k,20*k,fill=lerpc(rgb('#2A2A3A'),GOLD,0.55) if lit else rgb('#2A2A3A'),border=DARK,bw=1)
    box(dd,cx-1*k,cy-10*k,2*k,20*k,fill=DARK)
    box(dd,cx-5*k,cy-20*k,10*k,2*k,fill=STEEL); box(dd,cx-5*k,cy-20*k,2*k,8*k,fill=STEEL); box(dd,cx+3*k,cy-20*k,2*k,8*k,fill=STEEL)
    if lit:
        fl=int(t*5)%2
        box(dd,cx-3*k,cy-5*k-fl,6*k,9*k+fl,fill=ORG); box(dd,cx-1.5*k,cy-2*k,3*k,6*k,fill=LGOLD)
def lerp_(a,b,p): return a+(b-a)*p
def mvpos(i,src,dst,pair,p):
    """position x de la personne i qui traverse src->dst avec 'pair' ; p 0..1"""
    (xs,fs)=SLOT[src][i]; (xd,fd)=SLOT[dst][i]
    entry=124 if src=='L' else 188; ex=188 if dst=='R' else 124
    off=0 if len(pair)==1 else (-21 if pair.index(i)==0 else 21)
    if p<0.18: q=ease(p/0.18); return lerp_(xs,entry+off,q),lerp_(fs,BF,q)
    if p<0.82: return lerp_(entry+off,ex+off,(p-0.18)/0.64),BF
    q=ease((p-0.82)/0.18); return lerp_(ex+off,xd,q),lerp_(BF,fd,q)
def timer(dd,val,col=CREAM,y=92):
    box(dd,SW/2-80,y,160,34,fill=CARD,border=EDGE,bw=3)
    T(dd,'TEMPS',SW/2-70,y+12,10,'silk7',8,GREY,sp=1)
    T(dd,'%d MIN'%val,SW/2+72,y+8,18,'press',15,col,align='r')
def bridge(dd,t,L,R,mv=None,holder=0,labels=True,hl=(),timer_val=None,planks=None,shake=0.0,tcol=CREAM,lamp=True):
    night(dd,t,planks,shake)
    pos={}
    for i in L: pos[i]=SLOT['L'][i]
    for i in R: pos[i]=SLOT['R'][i]
    if mv:
        pair,src,dst,p=mv
        for i in pair: pos[i]=mvpos(i,src,dst,pair,p)
    order=sorted(pos,key=lambda i:(pos[i][1],pos[i][0]))
    for i in order: person(dd,i,pos[i][0],t,feet=pos[i][1],ph=i)
    if labels:
        for i in order: plabel(dd,i,pos[i][0],feet=pos[i][1],hl=(i in hl))
    if lamp and holder is not None and holder in pos:
        hx,hf=pos[holder]
        lantern(dd,hx+19,hf-22,t,k=1.15)
    if timer_val is not None: timer(dd,timer_val,tcol)
def big_fig(dd,i,cx,feet,t,k):
    if i==0: insp(dd,cx,feet,t,k=k*0.8)
    else: pri(dd,cx,feet,t,k=k,pal=WPAL[i],ph=i)
def biglab(dd,cx,y,txt,col,w=None):
    f=F('press',12); ww=w or tw(txt,f,0)+22
    box(dd,cx-ww/2,y,ww,30,fill=CARD,border=col,bw=3,shadow=(3,3,BLACK)); T(dd,txt,cx,y+8,16,'press',12,col,align='c')

def scene_fn(key,t,lt,dur):
    def fn(lay,dd):
        if key=='s1':
            night(dd,t); 
            for i,cx in enumerate((50,116,182,248)): big_fig(dd,i,cx,330,t,4.4)
            tagc(dd,SW/2,364,'QUATRE PERSONNES',GOLD)
        elif key=='s2':
            night(dd,t); lantern(dd,SW/2,220,t,k=5.0)
            for i,cx in enumerate((40,86,226,272)): big_fig(dd,[0,1,2,3][i],cx,330,t,3.4)
            tagc(dd,SW/2,364,'UNE SEULE LAMPE',GOLD)
        elif key=='s3':
            fall={}
            if lt>0.8:
                for j,i in enumerate((3,4,2,5,1,6)):
                    f=(lt-0.8-j*0.18)/0.9
                    if f>0: fall[i]=f
            night(dd,t,fall,shake=(1.6 if lt<1.4 else 0))
            if int(t*4)%2==0: T(dd,'!',SW/2,150,60,'press',48,RED,align='c',shadow=(3,3,BLACK))
            tagc(dd,SW/2,364,'LE PONT VA S’EFFONDRER',RED)
        elif key=='s4':
            bridge(dd,t,[0,1,2,3],[],holder=0,labels=False)
            tagc(dd,SW/2,364,'L’INSPECTEUR + 3 TÉMOINS',CYAN)
        elif key=='s5':
            bridge(dd,t,[2,3],[],mv=([0,1],'L','R',0.5),holder=0,labels=False)
            box(dd,SW/2-34,150,68,50,fill=CARD,border=GOLD,bw=3,shadow=(3,3,BLACK))
            T(dd,'MAX',SW/2,158,12,'silk7',10,GREY,align='c',sp=2); T(dd,'2',SW/2,174,22,'press',22,GOLD,align='c')
            tagc(dd,SW/2,364,'DEUX PERSONNES MAXIMUM',GOLD)
        elif key=='s6':
            bridge(dd,t,[0,1,2,3],[],holder=None,labels=False,lamp=False)
            lantern(dd,SW/2,176,t,k=3.2)
            T(dd,'v',SW/2,224,20,'press',16,GOLD,align='c') if False else None
            lbl(dd,SW/2,216,'LA LAMPE',GOLD)
            tagc(dd,SW/2,364,'TOUJOURS LA LAMPE',GOLD)
        elif key=='s7':
            night(dd,t); insp(dd,SW/2,330,t,k=5.4)
            biglab(dd,SW/2,118,'1 MIN',GOLD,w=120)
            tagc(dd,SW/2,364,'L’INSPECTEUR : 1 MINUTE',GOLD)
        elif key=='s8':
            night(dd,t)
            for i,(cx,thr) in enumerate(((60,0.0),(156,0.0),(252,0.0))):
                big_fig(dd,i+1,cx,330,t,4.4)
            for i,(cx,txt,thr) in enumerate(((60,'2 MIN',1.35),(156,'5 MIN',1.85),(252,'10 MIN',2.45))):
                if lt>thr: biglab(dd,cx,166,txt,PCOL[i+1],w=84 if i<2 else 92)
            tagc(dd,SW/2,364,'TROIS TÉMOINS',CYAN)
        elif key=='s9':
            night(dd,t)
            big_fig(dd,1,104,330,t,4.6); big_fig(dd,3,208,330,t,4.6)
            biglab(dd,104,172,'2 MIN',CYAN,w=84); biglab(dd,208,172,'10 MIN',PNK,w=92)
            if lt>1.0:
                box(dd,SW/2-110,104,220,48,fill=CARD,border=GOLD,bw=3,shadow=(3,3,BLACK))
                T(dd,'ENSEMBLE : 10 MIN',SW/2,120,16,'press',12,GOLD,align='c')
            tagc(dd,SW/2,364,'LE PLUS LENT DÉCIDE',CORAL)
        elif key=='q':
            bridge(dd,t,[0,1,2,3],[],holder=0,labels=True)
            T(dd,'?',SW/2,130,100,'press',84,GOLD,align='c',shadow=(4,4,BLACK))
            tagc(dd,SW/2,364,'TEMPS MINIMUM ?',CORAL)
        # ---- réponse ----
        elif key=='r0':
            night(dd,t); box(dd,SW/2-110,112,220,100,fill=CARD,border=GOLD,bw=4,shadow=(4,4,BLACK))
            T(dd,'17 MIN',SW/2,146,56,'press',34,GOLD,align='c',shadow=(4,4,BLACK))
            insp(dd,SW/2,336,t,k=4.0)
            tagc(dd,SW/2,364,'17 MINUTES',GOLD)
        elif key=='r1':
            night(dd,t); box(dd,SW/2-110,112,220,100,fill=CARD,border=RED,bw=4,shadow=(4,4,BLACK))
            T(dd,'19 MIN',SW/2,146,56,'press',34,GREY,align='c')
            dd.line([((SW/2-90)*S,134*S),((SW/2+90)*S,190*S)],fill=RED,width=6*S)
            dd.line([((SW/2-90)*S,190*S),((SW/2+90)*S,134*S)],fill=RED,width=6*S)
            insp(dd,SW/2,336,t,k=4.0); T(dd,'?',SW/2+70,250,40,'press',34,GOLD,align='c',shadow=(3,3,BLACK))
            tagc(dd,SW/2,364,'PAS 19 MINUTES',RED)
        elif key=='r2':
            night(dd,t); insp(dd,90,336,t,k=5.0); bubble(dd,150,120,150,70,['COMMENT','?'],CYAN,14)
            tagc(dd,SW/2,364,'VOICI COMMENT',CYAN)
        elif key in ('r3','r4','r5','r6','r7'):
            pair,src,dst,v0,v1,tg={'r3':([0,1],'L','R',0,2,'ALLER : 2 MIN'),
                  'r4':([0],'R','L',2,3,'RETOUR : 1 MIN'),
                  'r5':([2,3],'L','R',3,13,'ALLER : 10 MIN'),
                  'r6':([1],'R','L',13,15,'RETOUR : 2 MIN'),
                  'r7':([0,1],'L','R',15,17,'ALLER : 2 MIN')}[key]
            Ls={'r3':[2,3],'r4':[2,3],'r5':[0],'r6':[0],'r7':[]}[key]
            Rs={'r3':[],'r4':[1],'r5':[1],'r6':[2,3],'r7':[2,3]}[key]
            p=ease(lt/max(0.5,dur*0.72))
            holder=pair[0]
            tv=int(round(v0+(v1-v0)*p))
            bridge(dd,t,Ls,Rs,mv=(pair,src,dst,p),holder=holder,labels=True,timer_val=tv,hl=pair)
            tagc(dd,SW/2,364,tg,{'r3':CYAN,'r4':GOLD,'r5':CORAL,'r6':CYAN,'r7':CYAN}[key])
        elif key=='r8':
            night(dd,t)
            items=[('2',0.0,CYAN),('+',0.3,CREAM),('1',0.56,GOLD),('+',0.9,CREAM),('10',1.22,CORAL),('+',1.55,CREAM),('2',1.88,CYAN),('+',2.2,CREAM),('2',2.48,CYAN)]
            xs=[]; x=0
            for s,_,_ in items: 
                f=F('press',16); w=tw(s,f,0)+10; xs.append((x,w)); x+=w
            x0=(SW-x)/2
            for (s,thr,c),(xx,w) in zip(items,xs):
                if lt>thr: T(dd,s,x0+xx+w/2,152,24,'press',16,c,align='c',shadow=(3,3,BLACK))
            if lt>2.6: T(dd,'= ?',SW/2,210,40,'press',34,GOLD,align='c',shadow=(3,3,BLACK))
            insp(dd,SW/2,336,t,k=4.0)
            tagc(dd,SW/2,364,'2 + 1 + 10 + 2 + 2',GOLD)
        elif key=='r9':
            night(dd,t); box(dd,SW/2-110,112,220,100,fill=CARD,border=GOLD,bw=4,shadow=(4,4,BLACK))
            T(dd,'17 MIN',SW/2,146,56,'press',34,GOLD,align='c',shadow=(4,4,BLACK))
            insp(dd,SW/2,336,t,k=4.0); B.confetti(dd,t,t-lt)
            tagc(dd,SW/2,364,'17 MINUTES',GOLD)
        elif key=='r10':
            night(dd,t)
            big_fig(dd,2,104,330,t,4.4); big_fig(dd,3,208,330,t,4.4)
            biglab(dd,104,166,'5 MIN',VIO,w=84); biglab(dd,208,166,'10 MIN',PNK,w=92)
            if int(t*3)%2==0: dd.rectangle([52*S,138*S,260*S,340*S],outline=GOLD,width=3*S)
            lbl(dd,SW/2,112,'ENSEMBLE',GOLD)
            tagc(dd,SW/2,364,'LES 2 PLUS LENTS ENSEMBLE',GOLD)
    return fn
story=frame_fn(__import__('sys').modules[__name__],STORY,HEADS)
answer=story
def cover(t):
    def fn(lay,dd):
        bridge(dd,t,[0,1,2,3],[],holder=0,labels=True,lamp=True)
        T(dd,'?',SW/2,150,100,'press',84,GOLD,align='c',shadow=(5,5,BLACK))
        T(dd,'4 PERSONNES,',SW/2,18,40,'anton',32,CREAM,sp=1,align='c',shadow=(3,3,BLACK)); T(dd,'1 SEULE LAMPE',SW/2,58,40,'anton',32,GOLD,sp=1,align='c',shadow=(3,3,BLACK))
        B.band(lay,SH-44,40); d2=ImageDraw.Draw(lay); txt="TRAVERSER LE PONT"; f=F('silk4',11); T(d2,txt,SW/2-tw(txt,f,1)/2,SH-30,14,'silk4',11,CREAM,sp=1)
    return B.frame_with(B.make_scene(fn,t),'ÉNIGME DU JOUR')
decide=make_decide()
end=make_end('#020')
