from render_x import *
B.NUM='#018'
import random as _rnd
HEADS={'s1':[('1 seul ',GOLD),('étourdi',CORAL)],
 's2':[('Le dernier ',CREAM),('risque',RED),(' sa place',CREAM)],
 's3':[('100 ',GOLD),('passagers',CREAM),(' attendent',CREAM)],
 's4':[('Un avion de ',CREAM),('100 places',CYAN)],
 's5':[('Un billet : ',CREAM),('un siège',GOLD)],
 's6':[('Le 1er a perdu ',CREAM),('son billet',RED)],
 's7':[('Il s’assoit ',CREAM),('au hasard',CORAL)],
 's8':[('Chacun à ',CREAM),('sa place',GOLD),(' si libre',CREAM)],
 's9':[('Place prise : ',CREAM),('au hasard',CORAL)],
 's10':[('Il monte ',CREAM),('en dernier',GOLD)],
 'q':[('Sa propre ',CREAM),('place',GOLD),(' ?',CREAM)],
 'r0':[('Une chance ',CREAM),('sur deux',GOLD)],
 'r1':[('Voici ',CREAM),('pourquoi',CYAN)],
 'r2':[('Deux places ',CREAM),('à retenir',GOLD)],
 'r3':[('La ',CREAM),('place 1',GOLD),(' et la ',CREAM),('place 100',CORAL)],
 'r4':[('Aucune ',CREAM),('n’est prise',CYAN)],
 'r5':[('Même ',CREAM),('chance',GOLD)],
 'r6':[('Le 1er choix ',CREAM),('décide',CORAL)],
 'r7':[('Si c’est la ',CREAM),('place 1',GOLD)],
 'r8':[('Tous ',CREAM),('à leur place',CYAN)],
 'r9':[('Si c’est la ',CREAM),('place 100',CORAL)],
 'r10':[('Le dernier ',CREAM),('perd sa place',RED)],
 'r11':[('Autant de ',CREAM),('chances',GOLD)],
 'r12':[('Donc : ',CREAM),('1 chance sur 2',GOLD)],
 'r13':[('Quel que soit le ',CREAM),('nombre',CYAN)],
 'r14':[('Cinquante ',CREAM),('pour cent',GOLD)]}
STORY=('s1','s2','s3','s4','s5','s6','s7','s8','s9','s10','q')
SX0=33; SY0=100; PXS=24; SZ=20
SEATC={'e':(rgb('#1A2244'),EDGE),'p':(CREAM,DARK),'g':(GOLD,DARK),'c':(CORAL,DARK),'x':(RED,DARK),'y':(CYAN,DARK),'o':(ORG,DARK),'d':(DIM,DIM),'w':(GRN,DARK),'f':(rgb('#1A2244'),CORAL),'h':(rgb('#1A2244'),GOLD)}
def seat_xy(k):
    r,c=divmod(k-1,10); return SX0+c*PXS, SY0+r*PXS
def seat(dd,k,s):
    x,y=seat_xy(k); fill,bd=SEATC[s]
    box(dd,x,y,SZ,SZ,fill=fill,border=bd,bw=2)
    if s in 'pgcxyow': box(dd,x+2,y+2,SZ-4,5,fill=lerpc(fill,(0,0,0),0.28))
def seats(dd,st,n=100):
    for k in range(1,n+1):
        s=st(k)
        if s: seat(dd,k,s)
def snum(dd,k,txt,col=DARK):
    x,y=seat_xy(k)
    if len(txt)>=3: lbl(dd,x+SZ/2-6,339,txt,CORAL)
    else: T(dd,txt,x+SZ/2,y+8,8,'press',7,col,align='c')
def bigseat(dd,cx,cy,s,k=1.0,label=None,lcol=CREAM,pas=False,t=0.0):
    fill,bd=SEATC[s]; w=70*k; h=70*k
    box(dd,cx-w/2,cy-h/2,w,h,fill=fill,border=bd,bw=4)
    box(dd,cx-w/2+6,cy-h/2+6,w-12,16*k,fill=lerpc(fill,(0,0,0),0.28))
    if pas: pri(dd,cx,cy+h/2-8,t,k=3.2)
    if label: T(dd,label,cx,cy-h/2-22,16,'press',12,lcol,align='c',shadow=(2,2,BLACK))
def ticket(dd,x,y,w,txt,sub,col=GOLD,t=None):
    box(dd,x,y,w,56,fill=CARD,border=col,bw=3,shadow=(3,3,BLACK))
    box(dd,x+w-52,y+3,3,50,fill=EDGE)
    icon(dd,x+14,y+20,ORG)
    T(dd,sub,x+40,y+10,12,'silk7',9,GREY,sp=1)
    T(dd,txt,x+40,y+28,18,'press',14,col)
    T(dd,'✈'.replace('✈','>>'),x+w-26,y+22,14,'press',10,col,align='c')
def pie(dd,cx,cy,r,a0,a1,fill):
    dd.pieslice([(cx-r)*S,(cy-r)*S,(cx+r)*S,(cy+r)*S],a0,a1,fill=fill)
FREE_AFTER=[1]+list(range(43,101))

def scene_fn(key,t,lt,dur):
    def fn(lay,dd):
        if key=='s1':
            pri(dd,SW/2,300,t,k=7.0)
            for i in range(3):
                a=t*2.2+i*2.09; x=SW/2+math.cos(a)*70; y=170+math.sin(a)*14
                T(dd,'?',x,y,26,'press',22,[GOLD,CYAN,CORAL][i],align='c',shadow=(2,2,BLACK))
            tagc(dd,SW/2,364,'UN SEUL ÉTOURDI',GOLD)
        elif key=='s2':
            seats(dd,lambda k:'c' if k==100 else 'e')
            if int(t*3)%2==0: x,y=seat_xy(100); dd.rectangle([(x-5)*S,(y-5)*S,(x+SZ+5)*S,(y+SZ+5)*S],outline=RED,width=3*S)
            snum(dd,100,'100')
            tagc(dd,SW/2,364,'LE DERNIER RISQUE SA PLACE',RED)
        elif key=='s3':
            headgrid(dd,int(ease(lt/0.9)*100))
            tagc(dd,SW/2,364,'CENT PASSAGERS',GOLD)
        elif key=='s4':
            n=int(ease(lt/0.9)*100)
            seats(dd,lambda k:'e' if k<=n else None)
            tagc(dd,SW/2,364,'CENT PLACES',CYAN)
        elif key=='s5':
            for i,(num,y) in enumerate(((17,102),(58,166),(91,230))):
                if lt>i*0.5: ticket(dd,32,y,248,'SIÈGE N°%d'%num,'BILLET',GOLD if i==0 else CREAM)
            tagc(dd,SW/2,364,'UN NUMÉRO DE SIÈGE',GOLD)
        elif key=='s6':
            ticket(dd,32,130,248,'SIÈGE N°??','PASSAGER N°1',CORAL)
            if lt>0.7:
                stamp(dd,SW/2,240,'BILLET PERDU',RED,18)
            pri(dd,SW/2,336,t,k=3.6)
            tagc(dd,SW/2,364,'LE 1ER A PERDU SON BILLET',RED)
        elif key=='s7':
            land=lt>1.05
            f=(int(t*16)*37+11)%100+1
            seats(dd,lambda k:('y' if k==42 else 'e') if land else ('o' if k==f else 'e'))
            if land: snum(dd,42,'42')
            tagc(dd,SW/2,364,'IL S’ASSOIT AU HASARD',CORAL)
        elif key=='s8':
            n=2+int(lt*14)
            seats(dd,lambda k:'y' if k==42 else ('p' if k<=n and k>1 else 'e'))
            snum(dd,42,'42')
            tagc(dd,SW/2,364,'SA PLACE EST LIBRE',GOLD)
        elif key=='s9':
            f=FREE_AFTER[(int(t*16)*7)%len(FREE_AFTER)]; land=lt>1.1
            fin=77
            def st(k):
                if 2<=k<=41: return 'p'
                if k==42: return 'y'
                if land and k==fin: return 'o'
                if (not land) and k==f: return 'o'
                return 'e'
            seats(dd,st)
            snum(dd,42,'42')
            if lt<1.1:
                T(dd,'N°42 : PLACE PRISE !',SW/2,340,14,'silk7',10,RED,align='c',sp=1)
            tagc(dd,SW/2,364,'PLACE PRISE : AU HASARD',CORAL)
        elif key=='s10':
            seats(dd,lambda k:'f' if k==100 and int(t*3)%2==0 else ('e' if k==100 else 'p'))
            snum(dd,100,'100',CORAL)
            tagc(dd,SW/2,364,'LE DERNIER MONTE EN DERNIER',GOLD)
        elif key=='q':
            ticket(dd,32,102,248,'SIÈGE N°100','DERNIER PASSAGER',CORAL)
            T(dd,'?',SW/2,196,100,'press',84,GOLD,align='c',shadow=(4,4,BLACK))
            pri(dd,SW/2,336,t,k=3.6)
            tagc(dd,SW/2,364,'SA PROPRE PLACE ?',CORAL)
        # ---- réponse ----
        elif key=='r0':
            box(dd,SW/2-100,112,200,110,fill=CARD,border=GOLD,bw=4,shadow=(4,4,BLACK))
            T(dd,'1/2',SW/2,142,60,'press',48,GOLD,align='c',shadow=(4,4,BLACK))
            insp(dd,SW/2,GY,t,k=3.6)
            tagc(dd,SW/2,364,'UNE CHANCE SUR DEUX',GOLD)
        elif key=='r1':
            insp(dd,90,GY,t,k=5.0); bubble(dd,150,120,150,70,['POURQUOI','?'],CYAN,14)
            tagc(dd,SW/2,364,'VOICI POURQUOI',CYAN)
        elif key=='r2':
            seats(dd,lambda k:'g' if k==1 else ('c' if k==100 else 'e'))
            snum(dd,1,'1'); snum(dd,100,'100')
            tagc(dd,SW/2,364,'DEUX PLACES À RETENIR',GOLD)
        elif key=='r3':
            bigseat(dd,86,206,'g',label='PLACE 1',lcol=GOLD); bigseat(dd,226,206,'c',label='PLACE 100',lcol=CORAL)
            tagc(dd,SW/2,364,'PLACE 1 ET PLACE 100',GOLD)
        elif key=='r4':
            bigseat(dd,86,206,'h',label='PLACE 1',lcol=GOLD); bigseat(dd,226,206,'f',label='PLACE 100',lcol=CORAL)
            T(dd,'LIBRE',86,252,12,'silk7',10,GREY,align='c',sp=2); T(dd,'LIBRE',226,252,12,'silk7',10,GREY,align='c',sp=2)
            tagc(dd,SW/2,364,'AUCUNE N’EST PRISE',CYAN)
        elif key=='r5':
            bigseat(dd,76,206,'h',label='PLACE 1',lcol=GOLD); bigseat(dd,236,206,'f',label='PLACE 100',lcol=CORAL)
            T(dd,'=',156,190,40,'press',34,CREAM,align='c',shadow=(3,3,BLACK))
            T(dd,'1/100',76,252,14,'press',11,GOLD,align='c'); T(dd,'1/100',236,252,14,'press',11,CORAL,align='c')
            tagc(dd,SW/2,364,'MÊME CHANCE CHACUNE',GOLD)
        elif key=='r6':
            A=int(t*10)%2==0
            land=lt>1.5
            on1=(not land and A) or (land and True)
            bigseat(dd,86,206,'g' if on1 else 'h',label='PLACE 1',lcol=GOLD); bigseat(dd,226,206,'f' if on1 else 'c',label='PLACE 100',lcol=CORAL)
            T(dd,'?' if not land else '!',156,190,40,'press',34,GOLD,align='c',shadow=(3,3,BLACK))
            tagc(dd,SW/2,364,'LE PREMIER CHOIX DÉCIDE',CORAL)
        elif key=='r7':
            bigseat(dd,86,206,'g',label='PLACE 1',lcol=GOLD,pas=True,t=t); bigseat(dd,226,206,'f',label='PLACE 100',lcol=CORAL)
            T(dd,'CHOISIE',86,252,12,'silk7',10,GOLD,align='c',sp=1); T(dd,'LIBRE',226,252,12,'silk7',10,GREY,align='c',sp=2)
            tagc(dd,SW/2,364,'SI C’EST LA PLACE 1',GOLD)
        elif key=='r8':
            n=int(ease(lt/1.2)*99)+1
            seats(dd,lambda k:'p' if (k<=n and k!=100) else ('c' if (k==100 and lt>1.3) else ('e' if k==100 else 'e')))
            if lt>1.3: stamp(dd,SW/2,214,'SA PLACE !',GRN,18)
            tagc(dd,SW/2,364,'LE DERNIER A SA PLACE',CYAN)
        elif key=='r9':
            bigseat(dd,86,206,'h',label='PLACE 1',lcol=GOLD); bigseat(dd,226,206,'c',label='PLACE 100',lcol=CORAL,pas=True,t=t)
            T(dd,'LIBRE',86,252,12,'silk7',10,GREY,align='c',sp=2); T(dd,'CHOISIE',226,252,12,'silk7',10,CORAL,align='c',sp=1)
            tagc(dd,SW/2,364,'SI C’EST LA PLACE 100',CORAL)
        elif key=='r10':
            bigseat(dd,226,176,'c',label='PLACE 100',lcol=CORAL,pas=True,t=t)
            pri(dd,70,GY-30,t,k=4.4); T(dd,'?',70,150,40,'press',34,GOLD,align='c',shadow=(3,3,BLACK))
            if lt>0.5: stamp(dd,SW/2,262,'PLACE PRISE',RED,16)
            tagc(dd,SW/2,364,'LE DERNIER PERD SA PLACE',RED)
        elif key=='r11':
            barrow(dd,0,'PLACE 1 CHOISIE EN 1ER','1/2',ease(lt/0.6)*0.5,GOLD,hl=True)
            barrow(dd,1,'PLACE 100 CHOISIE EN 1ER','1/2',ease(lt/0.6)*0.5,CORAL)
            T(dd,'ET LE DERNIER ?',SW/2,236,14,'silk7',10,GREY,align='c',sp=1) if False else None
            if lt>0.9:
                box(dd,24,222,264,40,fill=CARD,border=EDGE,bw=2)
                T(dd,'1 : TOUT LE MONDE A SA PLACE',32,228,12,'silk7',9,GOLD,sp=1)
                T(dd,'100 : LE DERNIER PERD SA PLACE',32,246,12,'silk7',9,CORAL,sp=1)
            tagc(dd,SW/2,364,'AUTANT DE CHANCES',GOLD)
        elif key=='r12':
            pie(dd,SW/2,206,84,-90,90,GOLD); pie(dd,SW/2,206,84,90,270,CORAL)
            dd.ellipse([(SW/2-84)*S,(206-84)*S,(SW/2+84)*S,(206+84)*S],outline=DARK,width=4*S)
            box(dd,SW/2-64,178,128,56,fill=CARD,border=CREAM,bw=3,shadow=(3,3,BLACK))
            T(dd,'1/2',SW/2,190,36,'press',28,CREAM,align='c')
            tagc(dd,SW/2,364,'UNE CHANCE SUR DEUX',GOLD)
        elif key=='r13':
            for i,(n,c) in enumerate(((10,CYAN),(100,GOLD),(1000,CORAL))):
                y=104+i*76
                if lt>i*0.3:
                    box(dd,24,y,264,64,fill=CARD,border=c,bw=3)
                    T(dd,'%d PASSAGERS'%n,38,y+24,14,'press',9,CREAM)
                    T(dd,'1/2',274,y+16,32,'press',26,c,align='r')
            tagc(dd,SW/2,364,'TOUJOURS 1 CHANCE SUR 2',GOLD)
        elif key=='r14':
            box(dd,SW/2-120,120,240,110,fill=CARD,border=GOLD,bw=4,shadow=(4,4,BLACK))
            T(dd,'50 %',SW/2,152,56,'press',44,GOLD,align='c',shadow=(4,4,BLACK))
            star(dd,SW/2,290,t,8); B.confetti(dd,t,t-lt)
            tagc(dd,SW/2,364,'CINQUANTE POUR CENT',GOLD)
    return fn
story=frame_fn(__import__('sys').modules[__name__],STORY,HEADS)
answer=story
def cover(t):
    def fn(lay,dd):
        seats(dd,lambda k:'c' if k==100 else 'p')
        T(dd,'?',SW/2,176,100,'press',84,GOLD,align='c',shadow=(5,5,BLACK))
        T(dd,'CENT PASSAGERS,',SW/2,18,40,'anton',32,CREAM,sp=1,align='c',shadow=(3,3,BLACK)); T(dd,'UNE SEULE PLACE',SW/2,58,40,'anton',32,GOLD,sp=1,align='c',shadow=(3,3,BLACK))
        B.band(lay,SH-44,40); d2=ImageDraw.Draw(lay); txt="LE PASSAGER ÉTOURDI"; f=F('silk4',11); T(d2,txt,SW/2-tw(txt,f,1)/2,SH-30,14,'silk4',11,CREAM,sp=1)
    return B.frame_with(B.make_scene(fn,t),'ÉNIGME DU JOUR')
decide=make_decide()
end=make_end('#019')
