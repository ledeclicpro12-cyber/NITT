from render_c import *
B.NUM='#013'
LIGHT=rgb('#E8D9B5'); DARKC=rgb('#5A3E8C'); HOLE=rgb('#10142A')
CORN=((0,0),(7,7))
def cellcol(r,c): return DARKC if (r+c)%2==0 else LIGHT
def board(dd,x0,y0,cs,removed=(),hl=None,doms=(),holes=(),rows=8,t=0,xmark=()):
    hl=hl or {}
    box(dd,x0-4,y0-4,8*cs+8,8*cs+8,fill=rgb('#6A7096'))
    for r in range(8):
        for c in range(8):
            if r>=rows: continue
            x=x0+c*cs; y=y0+r*cs
            if (r,c) in removed: box(dd,x,y,cs,cs,fill=HOLE)
            else: box(dd,x,y,cs,cs,fill=cellcol(r,c))
    for (a,b) in doms: domino(dd,x0,y0,cs,a,b)
    for cell,col in hl.items():
        r,c=cell; dd.rectangle([(x0+c*cs+1)*S,(y0+r*cs+1)*S,(x0+(c+1)*cs-1)*S,(y0+(r+1)*cs-1)*S],outline=col,width=max(2,int(cs/8))*S)
    if holes and int(t*3)%2==0:
        for (r,c) in holes: dd.rectangle([(x0+c*cs+1)*S,(y0+r*cs+1)*S,(x0+(c+1)*cs-1)*S,(y0+(r+1)*cs-1)*S],outline=RED,width=max(3,int(cs/6))*S)
    for (r,c) in xmark:
        x=x0+c*cs; y=y0+r*cs; m=cs*0.15
        dd.line([((x+m)*S,(y+m)*S),((x+cs-m)*S,(y+cs-m)*S)],fill=RED,width=max(3,int(cs/6))*S); dd.line([((x+cs-m)*S,(y+m)*S),((x+m)*S,(y+cs-m)*S)],fill=RED,width=max(3,int(cs/6))*S)
def domino(dd,x0,y0,cs,a,b,col=None):
    r1,c1=a; r2,c2=b
    ins=3 if cs>=20 else 1
    x=x0+min(c1,c2)*cs+ins; y=y0+min(r1,r2)*cs+ins
    w=(abs(c1-c2)+1)*cs-2*ins; h=(abs(r1-r2)+1)*cs-2*ins
    box(dd,x,y,w,h,fill=(col or CORAL),border=DARK,bw=(2 if cs>=20 else 1))
    if cs<12: return
    if w>h:
        box(dd,x+w/2-1,y+3,2,h-6,fill=DARK)
        for cx in (x+w/4,x+3*w/4): box(dd,cx-cs/10,y+h/2-cs/10,cs/5,cs/5,fill=CREAM)
    else:
        box(dd,x+3,y+h/2-1,w-6,2,fill=DARK)
        for cy in (y+h/4,y+3*h/4): box(dd,x+w/2-cs/10,cy-cs/10,cs/5,cs/5,fill=CREAM)
DOMS=[((0,1),(0,2)),((0,3),(0,4)),((0,5),(0,6))]
for r in range(1,7): DOMS+=[((r,0),(r,1)),((r,2),(r,3)),((r,4),(r,5)),((r,6),(r,7))]
DOMS+=[((7,0),(7,1)),((7,2),(7,3)),((7,4),(7,5))]
HOLES=[(0,7),(7,6)]
cov=set()
for a,b in DOMS: cov|={a,b}
assert len(DOMS)==30 and set((r,c) for r in range(8) for c in range(8))-cov-set(CORN)==set(HOLES)
assert all(cellcol(*a)!=cellcol(*b) for a,b in DOMS)
BX,BY,CS=36,96,30
def moon(dd,cx,cy,r=22):
    dd.ellipse([(cx-r)*S,(cy-r)*S,(cx+r)*S,(cy+r)*S],fill=rgb('#F3E6CF')); dd.ellipse([(cx-r+10)*S,(cy-r-4)*S,(cx+r+10)*S,(cy+r-4)*S],fill=rgb('#10142A'))
def swatch(dd,x,y,w,h,col,label,num,show=True):
    if not show: return
    box(dd,x,y,w,h,fill=CARD,border=EDGE,bw=3,shadow=(3,3,BLACK))
    box(dd,x+10,y+10,22,22,fill=col,border=CREAM,bw=2)
    T(dd,label,x+40,y+16,12,'silk7',9,CREAM,sp=1)
    T(dd,str(num),x+w/2,y+38,56,'press',44,GOLD,align='c',shadow=(3,3,BLACK))
HEADS={'s1':[('Un ',CREAM),('défi',CORAL),(' du ',CREAM),('braqueur',GOLD)],
 's2':[('Une ',CREAM),('nuit',CYAN),(' entière sans réussir',CREAM)],
 's3':[('Un damier de ',CREAM),('64 cases',GOLD)],
 's4':[('Deux coins ',CREAM),('opposés',CORAL),(' retirés',CREAM)],
 's5':[('Il reste ',CREAM),('62 cases',GOLD)],
 's6':[('31 dominos',GOLD),(' sur la table',CREAM)],
 's7':[('1 domino = ',CREAM),('2 cases voisines',CORAL)],
 's8':[('Tout ',CREAM),('recouvrir',GOLD),(' avec les dominos',CREAM)],
 's9':[('Sans aucun ',CREAM),('trou',RED)],
 's10':[('Sans ',CREAM),('chevauchement',RED)],
 's11':[('Oui',CYAN),(' ou ',CREAM),('non',RED),(' ?',CREAM)],
 'q':[('Comment le ',CREAM),('prouver',GOLD),(' ?',CREAM)],
 'r0':[('Réponse : ',CREAM),('impossible',RED)],
 'r1':[('Voici la ',CREAM),('preuve',GOLD)],
 'r2':[('Regarde les ',CREAM),('couleurs',CORAL)],
 'r3':[('Domino : ',CREAM),('claire',GOLD),(' + ',CREAM),('foncée',CORAL)],
 'r4':[('Les 2 coins ',CREAM),('opposés',CORAL),(' : même couleur',CREAM)],
 'r5':[('Retirés : ',CREAM),('2 foncées',CORAL)],
 'r6':[('32 claires',GOLD),(' et ',CREAM),('30 foncées',CORAL)],
 'r7':[('31 dominos : ',CREAM),('31 + 31',GOLD)],
 'r8':[('Donc : ',CREAM),('impossible',RED)],
 'r9':[('Aucun ',CREAM),('essai',GOLD),(' nécessaire',CREAM)]}
STORY=('s1','s2','s3','s4','s5','s6','s7','s8','s9','s10','s11','q')
def scene_fn(key,t,lt,dur):
    def fn(lay,dd):
        if key=='s1':
            braq(dd,84,GY,t,k=8.0); insp(dd,236,GY,t,k=4.4)
            T(dd,'?',SW/2,120,60,'press',48,GOLD,align='c',shadow=(3,3,BLACK)); tagc(dd,SW/2,364,'LE DÉFI DU BRAQUEUR',CORAL,w=230)
        elif key=='s2':
            r=random.Random(4)
            for k_ in range(26):
                sx=r.randint(14,SW-14); sy=r.randint(100,230); on=math.sin(t*3+k_)>0.1; box(dd,sx,sy,3 if on else 2,3 if on else 2,fill=rgb('#C9CFE4') if on else rgb('#5A6BA8'))
            moon(dd,240,130)
            for i,(x,y) in enumerate(((30,GY-14),(62,GY-8),(120,GY-12))): domino(dd,0,0,1,(0,0),(0,0)) if False else box(dd,x,y,26,12,fill=CORAL,border=DARK,bw=2)
            insp(dd,176,GY,t,k=5.4); tagc(dd,SW/2,364,'TOUTE UNE NUIT',CYAN)
        elif key=='s3':
            board(dd,BX,BY,CS,rows=int(ease(lt/0.9)*8+0.999)); tagc(dd,SW/2,364,'64 CASES',GOLD)
        elif key=='s4':
            hl={c:RED for c in CORN} if 0.7<lt<1.4 and int(t*6)%2==0 else {}
            board(dd,BX,BY,CS,removed=(CORN if lt>=1.4 else ()),hl=hl); tagc(dd,SW/2,364,'DEUX COINS OPPOSÉS',CORAL)
        elif key=='s5':
            board(dd,BX,BY,CS,removed=CORN); tagc(dd,SW/2,364,'62 CASES',GOLD)
        elif key=='s6':
            T(dd,'31',SW/2,98,80,'press',64,GOLD,align='c',shadow=(4,4,BLACK))
            n=int(ease(lt/1.3)*31)+1
            for i in range(31):
                row,col=divmod(i,7); x=18+col*40+(row%2)*8; y=200+row*28
                if i<n: box(dd,x,y,36,22,fill=CORAL,border=DARK,bw=2); box(dd,x+17,y+3,2,16,fill=DARK); box(dd,x+8,y+9,4,4,fill=CREAM); box(dd,x+24,y+9,4,4,fill=CREAM)
            tagc(dd,SW/2,364,'31 DOMINOS',CORAL)
        elif key=='s7':
            doms=[((3,3),(3,4))] if lt<1.5 else [((3,3),(3,4)),((4,5),(5,5))]
            hl={}
            for a,b in doms: hl[a]=GOLD; hl[b]=GOLD
            board(dd,BX,BY,CS,removed=CORN,doms=doms)
            tagc(dd,SW/2,364,'1 DOMINO = 2 CASES VOISINES',CORAL,w=290)
        elif key=='s8':
            n=min(30,int(ease(lt/max(dur*0.9,0.1))*31))
            board(dd,BX,BY,CS,removed=CORN,doms=DOMS[:n]); tagc(dd,SW/2,364,'TOUT RECOUVRIR',GOLD)
        elif key=='s9':
            board(dd,BX,BY,CS,removed=CORN,doms=DOMS,holes=HOLES,t=t); tagc(dd,SW/2,364,'AUCUN TROU AUTORISÉ',RED,w=240)
        elif key=='s10':
            board(dd,BX,BY,CS,removed=CORN,doms=[((3,2),(3,3)),((3,3),(3,4))],xmark=[(3,3)]); tagc(dd,SW/2,364,'PAS DE CHEVAUCHEMENT',RED,w=250)
        elif key=='s11':
            board(dd,BX,BY,CS,removed=CORN,doms=[]); T(dd,'?',SW/2,150,100,'press',84,GOLD,align='c',shadow=(5,5,BLACK))
            tagc(dd,86,364,'OUI ?',CYAN,w=110); tagc(dd,226,364,'NON ?',RED,w=110)
        elif key=='q':
            board(dd,84,98,18,removed=CORN); insp(dd,84,GY,t,k=4.4); T(dd,'?',SW-84,226,100,'press',84,GOLD,align='c',shadow=(5,5,BLACK))
            tagc(dd,SW/2,364,'COMMENT LE PROUVER ?',GOLD,w=250)
        # ---- réponse ----
        elif key=='r0':
            board(dd,BX,BY,CS,removed=CORN)
            if lt>0.95:
                dd.line([((BX)*S,BY*S),((BX+8*CS)*S,(BY+8*CS)*S)],fill=RED,width=10*S); dd.line([((BX+8*CS)*S,BY*S),(BX*S,(BY+8*CS)*S)],fill=RED,width=10*S)
            tagc(dd,SW/2,364,'IMPOSSIBLE',RED)
        elif key=='r1':
            insp(dd,100,GY,t,k=5.4); board(dd,176,200,14,removed=())
            tagc(dd,SW/2,364,'LA PREUVE',GOLD)
        elif key=='r2':
            ph=int(t*1.6)%2; hl={(r,c):GOLD for r in range(8) for c in range(8) if (r+c)%2==ph}
            board(dd,BX,BY,CS,hl=hl); tagc(dd,SW/2,364,'CLAIRES ET FONCÉES',CORAL,w=240)
        elif key=='r3':
            seq=[((2,2),(2,3)),((4,5),(5,5)),((6,0),(6,1))][min(2,int(lt/1.1))]
            board(dd,BX,BY,CS,doms=[seq],hl={seq[0]:GOLD,seq[1]:GOLD})
            tagc(dd,SW/2,364,'1 CLAIRE + 1 FONCÉE',GOLD,w=240)
        elif key=='r4':
            hl={c:GOLD for c in CORN}
            board(dd,BX,BY,CS,hl=(hl if int(t*3)%2==0 or lt>1.5 else {}));
            tagc(dd,SW/2,364,'COINS OPPOSÉS : MÊME COULEUR',GOLD,w=300)
        elif key=='r5':
            board(dd,BX,BY,CS,removed=(CORN if lt>0.8 else ()),xmark=(CORN if lt<=0.8 else ())); tagc(dd,SW/2,364,'DEUX FONCÉES RETIRÉES',CORAL,w=250)
        elif key=='r6':
            board(dd,84,92,18,removed=CORN)
            swatch(dd,14,262,136,88,LIGHT,'CLAIRES',32,lt>0.65); swatch(dd,162,262,136,88,DARKC,'FONCÉES',30,lt>2.1)
        elif key=='r7':
            box(dd,SW/2-52,96,104,56,fill=CORAL,border=DARK,bw=3); box(dd,SW/2-2,100,4,48,fill=DARK)
            box(dd,SW/2-48,100,44,48,fill=LIGHT); box(dd,SW/2+4,100,44,48,fill=DARKC); box(dd,SW/2-52,96,104,56,border=DARK,bw=3) if False else None
            T(dd,'x 31',SW/2,168,30,'press',22,GOLD,align='c',shadow=(2,2,BLACK))
            swatch(dd,14,220,136,88,LIGHT,'CLAIRES',31,lt>1.4); swatch(dd,162,220,136,88,DARKC,'FONCÉES',31,lt>1.4)
            tagc(dd,SW/2,364,'IL EN FAUT 31 DE CHAQUE',GOLD,w=260)
        elif key=='r8':
            board(dd,BX,BY,CS,removed=CORN,doms=DOMS,holes=HOLES,t=t)
            if lt>0.3:
                box(dd,26,176,260,52,fill=CARD,border=RED,bw=4,shadow=(4,4,BLACK)); T(dd,'IMPOSSIBLE',SW/2,192,24,'press',19,RED,align='c')
            tagc(dd,SW/2,364,'DEUX CASES CLAIRES RESTENT',RED,w=280)
        elif key=='r9':
            for i in range(6):
                row,col=divmod(i,3); board(dd,28+col*92,100+row*92,8,removed=CORN,doms=DOMS[:12+i*3])
            dd.line([(20*S,96*S),((SW-20)*S,290*S)],fill=RED,width=9*S); dd.line([((SW-20)*S,96*S),(20*S,290*S)],fill=RED,width=9*S)
            insp(dd,SW/2,GY,t,k=2.8); B.confetti(dd,t,t-lt); tagc(dd,SW/2,364,"PAS BESOIN D'ESSAYER",GOLD,w=250)
    return fn
import random
story=frame_fn(__import__('sys').modules[__name__],STORY,HEADS)
answer=story
def cover(t):
    def fn(lay,dd):
        board(dd,BX+6,114,28,removed=CORN,doms=DOMS[:22])
        T(dd,'LE DAMIER',SW/2,18,40,'anton',34,CREAM,sp=1,align='c',shadow=(3,3,BLACK)); T(dd,'IMPOSSIBLE ?',SW/2,58,40,'anton',32,GOLD,sp=1,align='c',shadow=(3,3,BLACK))
        B.band(lay,SH-44,40); d2=ImageDraw.Draw(lay); txt="62 CASES, 31 DOMINOS"; f=F('silk4',11); T(d2,txt,SW/2-tw(txt,f,1)/2,SH-30,14,'silk4',11,CREAM,sp=1)
    return B.frame_with(B.make_scene(fn,t),'ÉNIGME DU JOUR')
decide=make_decide()
end=make_end('#014')
