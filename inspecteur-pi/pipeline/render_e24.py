from render_e2x import *
B.NUM='#024'
PAPER=rgb('#F3E6CF'); PAPERD=rgb('#B9A98C'); EARTHB=rgb('#2E6FC0'); EARTHG=rgb('#4CC36B'); MOONC=rgb('#E8E4D0'); MOOND=rgb('#B9B4A0')
HEADS={'s1':[('Une ',CREAM),('feuille',GOLD),(' vers la ',CREAM),('Lune',CYAN),(' !',CREAM)],
 's2':[('Fine comme un ',CREAM),('cheveu',GOLD)],
 's3':[('Un ',CREAM),('dixième',GOLD),(' de millimètre',CREAM)],
 's4':[('Un pli : l’épaisseur ',CREAM),('double',GOLD)],
 's5':[('Encore un pli : ',CREAM),('ça double',CORAL)],
 's6':[('Il plie ',CREAM),('encore',GOLD),(' et ',CREAM),('encore',CORAL)],
 's7':[('La Lune : ',CREAM),('384 000 km',CYAN)],
 'q':[('Combien de ',CREAM),('plis',GOLD),(' pour toucher la Lune ?',CREAM)],
 'r0':[('Réponse : ',CREAM),('42 fois',GOLD),(' !',CREAM)],
 'r1':[('Chaque pli : ',CREAM),('épaisseur ×2',GOLD)],
 'r2':[('10 plis',GOLD),(' = ',CREAM),('10 cm',CYAN)],
 'r3':[('20 plis',GOLD),(' = ',CREAM),('100 m',CYAN)],
 'r4':[('30 plis',GOLD),(' = ',CREAM),('107 km',CYAN)],
 'r5':[('40 plis',GOLD),(' = ',CREAM),('110 000 km',CYAN)],
 'r6':[('41 plis',GOLD),(' : ',CREAM),('pas assez',CORAL)],
 'r7':[('42 plis',GOLD),(' = ',CREAM),('440 000 km',CYAN)],
 'r8':[('Tu ',CREAM),('dépasses',GOLD),(' la Lune !',CREAM)],
 'r9':[('En vrai : ',CREAM),('12 plis',CORAL),(' maximum',CREAM)],
 'r10':[('En ',CREAM),('maths,',GOLD),(' 42 suffisent',CREAM)]}
STORY=('s1','s2','s3','s4','s5','s6','s7','q')

def earth(dd,cx,cy,r=26):
    disc(dd,cx,cy,r+3,DARK); disc(dd,cx,cy,r,EARTHB)
    disc(dd,cx-r*0.35,cy-r*0.2,r*0.38,EARTHG); disc(dd,cx+r*0.3,cy+r*0.35,r*0.3,EARTHG); disc(dd,cx+r*0.35,cy-r*0.45,r*0.2,EARTHG)
def moonbig(dd,cx,cy,r=30):
    disc(dd,cx,cy,r+3,DARK); disc(dd,cx,cy,r,MOONC)
    disc(dd,cx-r*0.35,cy-r*0.25,r*0.2,MOOND); disc(dd,cx+r*0.3,cy+r*0.2,r*0.26,MOOND); disc(dd,cx-r*0.1,cy+r*0.5,r*0.14,MOOND)
def sheet(dd,x,y,w,h,fold=False):
    box(dd,x,y,w,h,fill=PAPER,border=DARK,bw=2,shadow=(3,3,BLACK))
    for i in range(1,5): box(dd,x+6,y+h*i/6-1,w-12,2,fill=PAPERD)
    if fold: box(dd,x+w/2-1,y,2,h,fill=CORAL)
def layers(dd,x,base,w,n,col=PAPER,h1=5):
    """pile de n couches vue de côté, posée sur y=base"""
    for i in range(n):
        box(dd,x,base-(i+1)*h1,w,h1-1,fill=col if i%2==0 else PAPERD)
    box(dd,x,base-n*h1-1,w,1,fill=DARK)
def bignum(dd,cx,y,txt,col=GOLD,w=120,h=64,size=32):
    box(dd,cx-w/2,y,w,h,fill=CARD,border=col,bw=4,shadow=(4,4,BLACK)); T(dd,txt,cx,y+(h-size-4)/2+2,size+4,'press',size,col,align='c')
def stars_bg(dd,seed=3):
    r=random.Random(seed)
    for _ in range(22): box(dd,r.randint(10,300),r.randint(100,330),2,2,fill=rgb('#8A93C0'))
# barre Terre -> Lune : échelle 0.39 px / millier de km
EX=40; MX=216; X0=EX+28
def distbar(dd,kkm,t,col=CYAN,y=250,over=False):
    earth(dd,EX,y,22); moonbig(dd,MX,y,14)
    box(dd,X0,y-4,MX-14-X0-2,8,fill=CARD,border=EDGE,bw=2)
    w=kkm*0.39
    x1=X0+w
    box(dd,X0,y-3,max(2,min(x1,MX+22)-X0),6,fill=col)
    return x1

def scene_fn(key,t,lt,dur):
    def fn(lay,dd):
        if key=='s1':
            moonbig(dd,238,150,36)
            insp(dd,64,GY,t,k=4.0)
            sheet(dd,104,236,52,66)
            dotline(dd,(164,230),(206,170),GOLD,t,n=10)
            tagc(dd,SW/2,364,'UNE FEUILLE DE PAPIER',GOLD)
        elif key=='s2':
            sheet(dd,60,150,70,92)
            # cheveu : fine ligne ondulée
            for i in range(60):
                x=170+i*1.6; y=196+math.sin(i*0.35)*10
                box(dd,x,y,2,2,fill=rgb('#6B4A2E'))
            lbl(dd,95,256,'FEUILLE',CREAM); lbl(dd,218,226,'CHEVEU',CORAL)
            if lt>1.0:
                T(dd,'=',156,176,30,'press',26,GOLD,align='c',shadow=(3,3,BLACK)) if False else None
                lbl(dd,156,290,'AUSSI FINE',GOLD)
            tagc(dd,SW/2,364,'FINE COMME UN CHEVEU',GOLD)
        elif key=='s3':
            bignum(dd,SW/2,128,'0,1 MM',GOLD,w=210,h=60,size=26)
            # règle
            box(dd,26,236,260,34,fill=rgb('#E8C98A'),border=DARK,bw=2)
            for i in range(0,27): box(dd,26+i*10+4,236,2,(14 if i%5==0 else 8),fill=DARK)
            tagc(dd,SW/2,364,'UN DIXIÈME DE MILLIMÈTRE',GOLD)
        elif key=='s4':
            insp(dd,64,GY,t,k=3.6)
            sheet(dd,128,150,64,80,fold=(lt<1.0)) if lt<1.0 else None
            if lt>=1.0:
                layers(dd,128,230,64,2,h1=14)
            if lt>1.2:
                T(dd,'×2',250,170,40,'press',32,GOLD,align='c',shadow=(4,4,BLACK))
            lbl(dd,160,244,'1 PLI',CORAL) if lt>=1.0 else None
            tagc(dd,SW/2,364,'1 PLI, ÉPAISSEUR DOUBLE',GOLD)
        elif key=='s5':
            base=300
            layers(dd,24,base,50,1,h1=14); lbl(dd,49,base+8,'1',CREAM)
            if lt>0.2: layers(dd,104,base,50,2,h1=14); lbl(dd,129,base+8,'2',CREAM)
            if lt>0.6: layers(dd,184,base,50,4,h1=14); lbl(dd,209,base+8,'4',GOLD)
            if lt>0.9: T(dd,'×2',92,160,26,'press',20,CORAL,align='c'); T(dd,'×2',172,160,26,'press',20,CORAL,align='c')
            tagc(dd,SW/2,364,'ENCORE UN PLI : ×2',CORAL)
        elif key=='s6':
            base=320; n=int(min(8,1+lt*3.2))
            for i in range(n):
                h=min(200,6*(2**i)); x=22+i*35
                box(dd,x,base-h,28,h,fill=PAPER if i%2==0 else PAPERD,border=DARK,bw=2)
            T(dd,'...',270,110,26,'press',20,CORAL,align='c')
            tagc(dd,SW/2,364,'ÇA DOUBLE, ENCORE ET ENCORE',CORAL)
        elif key=='s7':
            earth(dd,70,300,38); moonbig(dd,238,140,30)
            dotline(dd,(104,270),(214,170),CYAN,t,n=14)
            if lt>0.6: bignum(dd,168,206,'384 000 KM',CYAN,w=170,h=40,size=16)
            tagc(dd,SW/2,364,'DISTANCE TERRE - LUNE',CYAN)
        elif key=='q':
            earth(dd,60,310,30); moonbig(dd,244,130,28)
            layers(dd,98,320,44,6,h1=8)
            dotline(dd,(124,260),(214,160),GOLD,t,n=10)
            T(dd,'?',160,210,60,'press',50,GOLD,align='c',shadow=(4,4,BLACK))
            tagc(dd,SW/2,364,'COMBIEN DE PLIS ?',CORAL)
        # ---- réponse ----
        elif key=='r0':
            insp(dd,SW/2,GY,t,k=4.2)
            if lt>1.0:
                bignum(dd,SW/2,120,'42',GOLD,w=170,h=96,size=64)
                lbl(dd,SW/2,228,'FOIS !',CORAL,14)
            else:
                T(dd,'?',SW/2,140,60,'press',50,GOLD,align='c',shadow=(4,4,BLACK))
            tagc(dd,SW/2,364,'LA RÉPONSE',GOLD)
        elif key=='r1':
            labs=['1','2','4','8']
            for i,s in enumerate(labs):
                if lt>i*0.35 or i==0:
                    x=40+i*72; bignum(dd,x+14,170,s,GOLD if i==3 else CREAM,w=50,h=50,size=22)
                    if i<3 and lt>i*0.35+0.3: T(dd,'×2',x+50,120,22,'press',14,CORAL,align='c')
            insp(dd,SW/2,GY,t,k=3.2)
            tagc(dd,SW/2,364,'À CHAQUE PLI : DOUBLE',CORAL)
        elif key=='r2':
            layers(dd,60,300,70,10,h1=7)
            box(dd,170,300-71,10,71,fill=rgb('#E8C98A'),border=DARK,bw=1)
            for i in range(11): box(dd,180,300-i*7-1,6 if i%5 else 10,2,fill=DARK)
            bignum(dd,236,160,'10 CM',CYAN,w=110,h=44,size=16)
            insp(dd,252,GY,t,k=2.6) if False else None
            tagc(dd,SW/2,364,'UNE PILE DE 10 CM',CYAN)
        elif key=='r3':
            # gratte-ciel de 100 m
            bx=190; box(dd,bx,150,70,GY-150,fill=rgb('#2C3766'),border=DARK,bw=2)
            for r_ in range(10):
                for c_ in range(4):
                    box(dd,bx+8+c_*15,160+r_*18,8,10,fill=GOLD if (r_+c_)%3 else rgb('#4A5486'))
            box(dd,bx+30,126,10,24,fill=STEEL)
            insp(dd,96,GY,t,k=2.0)
            bignum(dd,96,150,'100 M',CYAN,w=120,h=44,size=16)
            tagc(dd,SW/2,364,'COMME UN GRATTE-CIEL',CYAN)
        elif key=='r4':
            stars_bg(dd)
            disc(dd,156,520,200,EARTHB); disc(dd,156,520,196,None,rgb('#8FE3FF'),3)
            box(dd,0,196,SW,2,fill=CORAL)
            T(dd,'ESPACE',60,176,16,'silk7',11,CORAL) if False else None
            lbl(dd,70,170,'ESPACE',CORAL)
            lbl(dd,70,204,'100 KM',CORAL,9)
            box(dd,150,150,6,GY-150-60,fill=PAPER) if False else None
            layers(dd,206,328,26,1,h1=2)
            box(dd,216,160,6,170,fill=PAPER,border=DARK,bw=1)
            bignum(dd,150,250,'107 KM',CYAN,w=130,h=44,size=16)
            tagc(dd,SW/2,364,'30 PLIS : DANS L’ESPACE',CYAN)
        elif key=='r5':
            x1=distbar(dd,110,t,CYAN)
            bignum(dd,150,140,'110 000 KM',CYAN,w=200,h=44,size=14); lbl(dd,150,112,'PRESQUE',CORAL,10)
            bignum(dd,150,300,'40 PLIS',GOLD,w=130,h=40,size=16)
            lbl(dd,MX,272,'LUNE',CREAM)
            tagc(dd,SW/2,364,'ENCORE LOIN DE LA LUNE',CYAN)
        elif key=='r6':
            x1=distbar(dd,220,t,CORAL)
            bignum(dd,150,140,'220 000 KM',CORAL,w=200,h=44,size=14)
            bignum(dd,150,300,'41 PLIS',GOLD,w=130,h=40,size=16)
            lbl(dd,MX,272,'LUNE',CREAM)
            if lt>0.6: cross(dd,SW/2,200,20,7,RED) if False else None
            if lt>0.6: stamp(dd,150,205,'PAS ASSEZ',RED,12)
            tagc(dd,SW/2,364,'IL MANQUE ENCORE',CORAL)
        elif key=='r7':
            p=ease(lt/max(0.5,dur*0.7)); x1=distbar(dd,440*p,t,GOLD)
            bignum(dd,150,140,'440 000 KM',GOLD,w=200,h=44,size=14)
            bignum(dd,150,300,'42 PLIS',GOLD,w=130,h=40,size=16)
            lbl(dd,MX,272,'LUNE',CREAM)
            tagc(dd,SW/2,364,'42 PLIS, C’EST BON',GOLD)
        elif key=='r8':
            moonbig(dd,SW/2+20,200,56)
            box(dd,30,196,230,8,fill=GOLD); tri_down(dd,262,200,GOLD,0) if False else None
            dd.polygon([(256*S,188*S),(286*S,200*S),(256*S,212*S)],fill=GOLD)
            star(dd,60,140,t,5)
            lbl(dd,SW/2,300,'LUNE DÉPASSÉE',GOLD,11)
            tagc(dd,SW/2,364,'TU DÉPASSES LA LUNE',GOLD)
        elif key=='r9':
            layers(dd,92,300,128,3,h1=26)
            box(dd,92,200,128,4,fill=CORAL)
            T(dd,'12',SW/2,150,44,'press',36,CORAL,align='c',shadow=(4,4,BLACK))
            lbl(dd,SW/2,310,'LA FEUILLE RÉSISTE',CORAL,11)
            tagc(dd,SW/2,364,'IMPOSSIBLE EN VRAI',CORAL)
        elif key=='r10':
            insp(dd,64,GY,t,k=4.2)
            bignum(dd,214,150,'42',GOLD,w=130,h=100,size=60)
            lbl(dd,214,260,'EN MATHS',CYAN,12)
            star(dd,130,300,t,4) if lt>0.5 else None
            tagc(dd,SW/2,364,'42 PLIS SUFFISENT',GOLD)
    return fn
story=frame_fn(__import__('sys').modules[__name__],STORY,HEADS)
answer=story
def cover(t):
    B.NUM='#024'
    def fn(lay,dd):
        moonbig(dd,236,190,48); insp(dd,70,GY,t,k=4.2); sheet(dd,112,250,52,66)
        dotline(dd,(168,244),(196,214),GOLD,t,n=8)
        T(dd,'UNE FEUILLE',SW/2,10,36,'anton',28,CREAM,sp=1,align='c',shadow=(3,3,BLACK)); T(dd,'JUSQU’À LA LUNE ?',SW/2,44,36,'anton',28,GOLD,sp=1,align='c',shadow=(3,3,BLACK))
        B.band(lay,SH-44,40); d2=ImageDraw.Draw(lay); txt="L'ÉNIGME DU PAPIER"; f=F('silk4',11); T(d2,txt,SW/2-tw(txt,f,1)/2,SH-30,14,'silk4',11,CREAM,sp=1)
    return B.frame_with(B.make_scene(fn,t),'ÉNIGME DU JOUR')
decide=make_decide()
end=make_end('#025')
