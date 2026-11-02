from render_x import *
B.NUM='#016'
SEQ='PFFPFPPFPFFFPPFFPFPF'
HEADS={'s1':[('Le ',CREAM),('braqueur',CORAL)],
 's2':[('Sortir : ',CREAM),('1 seule chance',GOLD)],
 's3':[('Devine le ',CREAM),('résultat',GOLD)],
 's4':[('Un ',CREAM),('jeu de pièce',CYAN)],
 's5':[('Il lance ',CREAM),('une pièce',GOLD)],
 's6':[('Encore',CORAL),(' et ',CREAM),('encore',CORAL)],
 's7':[('Il note ',CREAM),('chaque résultat',GOLD)],
 's8':[('Première ',CREAM),('série',CYAN)],
 's9':[('Dès qu’il obtient ',CREAM),('Pile',GOLD)],
 's10':[('Pile,',GOLD),(' puis ',CREAM),('Face',CYAN)],
 's11':[('Deuxième ',CREAM),('série',CORAL)],
 's12':[('Dès qu’il obtient ',CREAM),('Pile',GOLD)],
 's13':[('Pile,',GOLD),(' puis ',CREAM),('Pile',GOLD)],
 's14':[('Des milliers ',CREAM),('de fois',CORAL)],
 's15':[('Nombre moyen ',CREAM),('de lancers',GOLD)],
 'q':[('Laquelle finit ',CREAM),('la première?',CORAL)],
 'r0':[('La ',CREAM),('réponse!',GOLD)],
 'r1':[('Pile,',GOLD),(' Face',CYAN)],
 'r2':[('Pile, Face :',CREAM),(' 4 lancers',GOLD)],
 'r3':[('Pile, Pile :',CREAM),(' 6 lancers',CORAL)],
 'r4':[('Voici ',CREAM),('pourquoi',CYAN)],
 'r5':[('Après un ',CREAM),('Pile',GOLD)],
 'r6':[('Deux ',CREAM),('possibilités',CYAN)],
 'r7':[('Objectif : ',CREAM),('Pile, Pile',GOLD)],
 'r8':[('Face',CYAN),(' : raté',RED)],
 'r9':[('Tout repart ',CREAM),('de zéro',RED)],
 'r10':[('Objectif : ',CREAM),('Pile, Face',GOLD)],
 'r11':[('Encore ',CREAM),('Pile',GOLD)],
 'r12':[('On ne perd ',CREAM),('rien',GRN)],
 'r13':[('Prêt à ',CREAM),('gagner',GOLD)],
 'r14':[('Dès le prochain ',CREAM),('Face',CYAN)],
 'r15':[('Jamais de ',CREAM),('retour à zéro',GRN)],
 'r16':[('Pile, Pile : ',CREAM),('il recommence',RED)],
 'r17':[('Le ',CREAM),('résultat',GOLD)],
 'r18':[('Pile, Face :',CREAM),(' 4 lancers',GOLD)],
 'r19':[('Pile, Pile :',CREAM),(' 6 lancers',CORAL)],
 'r20':[('Même ',CREAM),('hasard,',GOLD),(' pas la même ',CREAM),('attente',CYAN)]}
STORY=('s1','s2','s3','s4','s5','s6','s7','s8','s9','s10','s11','s12','s13','s14','s15','q')
X1,X2=96,216  # emplacements des 2 pièces
SY=214

def pair(dd,a,b,lt=None,hl=None,shown=(True,True),r=34):
    slot(dd,X1,SY,r,a if shown[0] else None,hl=hl); slot(dd,X2,SY,r,b if shown[1] else None,hl=hl)
    T(dd,'1',X1,SY+r+12,16,'silk7',10,GREY,align='c'); T(dd,'2',X2,SY+r+12,16,'silk7',10,GREY,align='c')
    dd.line([((X1+r+8)*S,SY*S),((X2-r-8)*S,SY*S)],fill=EDGE,width=3*S)

def seriecard(dd,x,y,w,h,n,a,b,col,hl=False):
    box(dd,x,y,w,h,fill=CARD,border=(col if hl else EDGE),bw=3,shadow=(3,3,BLACK))
    T(dd,'SÉRIE %d'%n,x+w/2,y+10,16,'silk7',11,col,align='c',sp=1)
    slot(dd,x+w*0.28,y+h*0.58,20,a); slot(dd,x+w*0.72,y+h*0.58,20,b)

def scene_fn(key,t,lt,dur):
    def fn(lay,dd):
        if key=='s1':
            braq(dd,92,GY,t,k=9.0)
            coin(dd,222,170+math.sin(t*3)*8,34,'P' if math.cos(t*9)>0 else 'F',squash=math.cos(t*9))
            tagc(dd,SW/2,364,'LE BRAQUEUR',CORAL)
        elif key=='s2':
            exit_door(dd,106,112,100,GY-112,0.0,t)
            if int(t*4)%2==0: box(dd,106,GY-4,100,4,fill=GOLD)
            T(dd,'1',50,150,60,'press',52,GOLD,align='c',shadow=(4,4,BLACK))
            tagc(dd,SW/2,364,'1 SEULE CHANCE',GOLD)
        elif key=='s3':
            sq=math.cos(t*7); coin(dd,SW/2,206,62,'P' if sq>0 else 'F',squash=sq)
            T(dd,'?',SW/2,284,60,'press',48,GOLD,align='c',shadow=(4,4,BLACK))
            tagc(dd,SW/2,364,'DEVINE LE RÉSULTAT',GOLD)
        elif key=='s4':
            coin(dd,92,206,56,'P'); coin(dd,220,206,56,'F')
            T(dd,'PILE',92,276,20,'press',16,GOLD,align='c'); T(dd,'FACE',220,276,20,'press',16,CYAN,align='c')
            tagc(dd,SW/2,364,'UN JEU DE PIÈCE',CYAN)
        elif key=='s5':
            braq(dd,70,GY,t,k=8.0)
            p=(lt*0.9)%1.0; x=150+p*110; y=250-math.sin(p*math.pi)*150
            coin(dd,x,y,24,'P' if int(p*8)%2==0 else 'F',squash=math.cos(p*20))
            tagc(dd,SW/2,364,'IL LANCE LA PIÈCE',GOLD)
        elif key=='s6':
            n=min(len(SEQ),int(lt/0.11)+1)
            for i in range(n):
                r_,c_=divmod(i,5); coin(dd,44+c_*56,130+r_*58,19,SEQ[i])
            tagc(dd,SW/2,364,'ENCORE ET ENCORE',CORAL)
        elif key=='s7':
            box(dd,40,96,232,240,fill=rgb('#F3E6CF'),border=DARK,bw=3,shadow=(4,4,BLACK))
            for k in range(6): box(dd,40+14*k,96,6,12,fill=DARK)
            n=min(7,int(lt/0.12)+1)
            for i in range(n):
                y=118+i*30; ch=SEQ[i]; T(dd,'%d'%(i+1),78,y,20,'press',14,DARK,align='r')
                T(dd,ch,106,y,20,'press',16,rgb('#B8860B') if ch=='P' else rgb('#1F7A99'))
                T(dd,'PILE' if ch=='P' else 'FACE',140,y+2,18,'silk7',11,DARK,sp=1)
            tagc(dd,SW/2,364,'IL NOTE TOUT',GOLD)
        elif key in ('s8','s11'):
            n=1 if key=='s8' else 2; col=CYAN if key=='s8' else CORAL
            T(dd,'SÉRIE',SW/2,112,30,'press',22,CREAM,align='c',shadow=(3,3,BLACK))
            T(dd,str(n),SW/2,150,140,'press',120,col,align='c',shadow=(6,6,BLACK))
            tagc(dd,SW/2,364,'PREMIÈRE SÉRIE' if n==1 else 'DEUXIÈME SÉRIE',col)
        elif key=='s9':
            pair(dd,'P',None,shown=(lt>0.6,False),hl=None)
            T(dd,'SÉRIE 1',SW/2,100,16,'silk7',11,CYAN,align='c',sp=1)
            tagc(dd,SW/2,364,'DÈS QU’IL OBTIENT PILE',GOLD)
        elif key=='s10':
            pair(dd,'P','F',shown=(True,lt>0.40))
            T(dd,'SÉRIE 1',SW/2,100,16,'silk7',11,CYAN,align='c',sp=1)
            if lt>0.85: stamp(dd,SW/2,320,'STOP !',RED,16)
            tagc(dd,SW/2,364,'PILE PUIS FACE',CYAN)
        elif key=='s12':
            pair(dd,'P',None,shown=(lt>0.58,False))
            T(dd,'SÉRIE 2',SW/2,100,16,'silk7',11,CORAL,align='c',sp=1)
            tagc(dd,SW/2,364,'DÈS QU’IL OBTIENT PILE',GOLD)
        elif key=='s13':
            pair(dd,'P','P',shown=(True,lt>0.60))
            T(dd,'SÉRIE 2',SW/2,100,16,'silk7',11,CORAL,align='c',sp=1)
            if lt>1.0: stamp(dd,SW/2,320,'STOP !',RED,16)
            tagc(dd,SW/2,364,'PILE PUIS PILE',GOLD)
        elif key=='s14':
            rs=random.Random(int(t*5))
            for r_ in range(6):
                for c_ in range(8):
                    ch=SEQ[(r_*7+c_*3+int(t*6))%len(SEQ)]
                    coin(dd,34+c_*34,112+r_*34,10,ch)
            box(dd,SW/2-90,300,180,40,fill=CARD,border=GOLD,bw=3,shadow=(3,3,BLACK))
            v=int(ease(lt/1.3)*5000); T(dd,'%d'%v,SW/2,310,24,'press',20,GOLD,align='c')
            tagc(dd,SW/2,364,'DES MILLIERS DE FOIS',CORAL)
        elif key=='s15':
            for i,(n,col) in enumerate(((1,CYAN),(2,CORAL))):
                x=18+i*150; box(dd,x,112,138,150,fill=CARD,border=col,bw=3,shadow=(3,3,BLACK))
                T(dd,'SÉRIE %d'%n,x+69,122,16,'silk7',11,col,align='c',sp=1)
                T(dd,'?',x+69,166,60,'press',50,GOLD,align='c',shadow=(3,3,BLACK))
                T(dd,'LANCERS',x+69,236,14,'silk7',10,CREAM,align='c',sp=1)
            T(dd,'MOYENNE',SW/2,290,18,'silk7',12,GREY,align='c',sp=2)
            tagc(dd,SW/2,364,'NOMBRE MOYEN DE LANCERS',GOLD)
        elif key=='q':
            ph=int(t*2)%2
            seriecard(dd,14,106,138,128,1,'P','F',CYAN,hl=(ph==0)); seriecard(dd,160,106,138,128,2,'P','P',CORAL,hl=(ph==1))
            T(dd,'?',SW/2,252,90,'press',76,GOLD,align='c',shadow=(5,5,BLACK))
            tagc(dd,SW/2,364,'LA PLUS RAPIDE ?',CORAL)
        # ---- réponse ----
        elif key=='r0':
            pair(dd,'P','F',hl=GOLD); star(dd,SW/2,128,t,7)
            tagc(dd,SW/2,364,'LA RÉPONSE',GOLD)
        elif key=='r1':
            pair(dd,'P','F',hl=GOLD); star(dd,SW/2,128,t,7)
            tagc(dd,SW/2,364,'PILE, PUIS FACE',GOLD)
        elif key=='r2':
            barrow(dd,0,'PILE, FACE','4 lancers' if lt>0.4 else '',ease((lt-0.4)/0.7)*4/8,GOLD,hl=True)
            insp(dd,SW/2,GY,t,k=3.6); tagc(dd,SW/2,364,'4 EN MOYENNE',GOLD)
        elif key=='r3':
            barrow(dd,0,'PILE, FACE','4 lancers',4/8,GOLD)
            barrow(dd,1,'PILE, PILE','6 lancers' if lt>0.25 else '',ease((lt-0.25)/0.7)*6/8,CORAL,hl=True)
            insp(dd,SW/2,GY,t,k=3.6); tagc(dd,SW/2,364,'6 EN MOYENNE',CORAL)
        elif key=='r4':
            insp(dd,90,GY,t,k=5.0); bubble(dd,150,120,150,70,['POURQUOI','?'],CYAN,14)
            tagc(dd,SW/2,364,'VOICI POURQUOI',CYAN)
        elif key=='r5':
            coin(dd,SW/2,206,60,'P',ring=GOLD)
            T(dd,'DÉJÀ TIRÉ',SW/2,292,16,'silk7',11,GREY,align='c',sp=1)
            tagc(dd,SW/2,364,'APRÈS UN PILE',GOLD)
        elif key=='r6':
            coin(dd,64,226,30,'P',ring=GOLD)
            for (x,y,ch,col) in ((228,140,'F',CYAN),(228,312,'P',GOLD)):
                dotline(dd,(100,226),(x-42,y),col,t,3,10); coin(dd,x,y,30,ch)
            T(dd,'OU',SW/2+36,226,24,'press',18,CREAM,align='c')
            tagc(dd,SW/2,364,'DEUX POSSIBILITÉS',CYAN)
        elif key=='r7':
            pair(dd,'P','P',hl=GOLD); lbl(dd,SW/2,128,'OBJECTIF',GOLD)
            tagc(dd,SW/2,364,'POUR PILE, PILE',GOLD)
        elif key=='r8':
            pair(dd,'P','F',shown=(True,lt>0.5))
            lbl(dd,SW/2,128,'OBJECTIF : PILE, PILE',GOLD)
            if lt>0.8: xmark_(dd,X2,SY,40,7)
            tagc(dd,SW/2,364,'SI FACE : RATÉ',RED)
        elif key=='r9':
            n=int(lt/0.12)
            slot(dd,X1,SY,34,None); slot(dd,X2,SY,34,None)
            T(dd,'0',SW/2,126,90,'press',76,RED,align='c',shadow=(5,5,BLACK))
            a0=(t*3)%6.28
            dd.arc([(SW/2-50)*S,290*S,(SW/2+50)*S,336*S],30,320,fill=CORAL,width=4*S)
            dd.polygon([((SW/2+48)*S,308*S),((SW/2+34)*S,296*S),((SW/2+36)*S,316*S)],fill=CORAL)
            tagc(dd,SW/2,364,'TOUT REPART DE ZÉRO',RED)
        elif key=='r10':
            pair(dd,'P','F',hl=GOLD); lbl(dd,SW/2,128,'OBJECTIF',GOLD)
            tagc(dd,SW/2,364,'POUR PILE, FACE',GOLD)
        elif key=='r11':
            pair(dd,'P','P',shown=(True,lt>0.75))
            lbl(dd,SW/2,128,'OBJECTIF : PILE, FACE',GOLD)
            tagc(dd,SW/2,364,'SI ENCORE PILE',GOLD)
        elif key=='r12':
            slot(dd,X1,SY,34,'P',hl=GRN); slot(dd,X2,SY,34,None)
            T(dd,'DÉJÀ UN PILE',X1,SY+52,16,'silk7',10,GRN,align='c',sp=1)
            tagc(dd,SW/2,364,'RIEN DE PERDU',GRN)
        elif key=='r13':
            slot(dd,X1,SY,34,'P',hl=GRN); slot(dd,X2,SY,34,None,hl=(GOLD if int(t*3)%2 else None),t=t)
            T(dd,'FACE ?',X2,SY+52,16,'silk7',10,CYAN,align='c',sp=1)
            tagc(dd,SW/2,364,'PRÊT À GAGNER',GOLD)
        elif key=='r14':
            slot(dd,X1,SY,34,'P')
            if lt<0.9:
                sq=math.cos(t*12); coin(dd,X2,SY,34,'P' if sq>0 else 'F',squash=sq)
            else:
                coin(dd,X2,SY,34,'F',ring=GOLD); star(dd,SW/2,128,t,7); B.confetti(dd,t,t-lt)
            tagc(dd,SW/2,364,'DÈS LE PROCHAIN FACE',CYAN)
        elif key=='r15':
            pair(dd,'P','F',hl=GRN)
            cxm=SW/2; dd.arc([(cxm-60)*S,262*S,(cxm+60)*S,312*S],20,340,fill=CORAL,width=4*S)
            dd.polygon([((cxm+58)*S,282*S),((cxm+44)*S,270*S),((cxm+46)*S,292*S)],fill=CORAL)
            xmark_(dd,cxm,288,18,5)
            tagc(dd,SW/2,364,'JAMAIS DE RETOUR À ZÉRO',GRN)
        elif key=='r16':
            pair(dd,'P','P',hl=CORAL)
            cxm=SW/2; dd.arc([(cxm-60)*S,262*S,(cxm+60)*S,312*S],20,340,fill=CORAL,width=4*S)
            dd.polygon([((cxm+58)*S,282*S),((cxm+44)*S,270*S),((cxm+46)*S,292*S)],fill=CORAL)
            T(dd,'0',cxm,276,30,'press',22,RED,align='c')
            tagc(dd,SW/2,364,'PILE, PILE : IL RECOMMENCE',RED)
        elif key=='r17':
            barrow(dd,0,'PILE, FACE','',0,GOLD); barrow(dd,1,'PILE, PILE','',0,CORAL)
            insp(dd,SW/2,GY,t,k=3.6); tagc(dd,SW/2,364,'LE RÉSULTAT',GOLD)
        elif key=='r18':
            barrow(dd,0,'PILE, FACE','4 lancers' if lt>0.3 else '',ease((lt-0.3)/0.6)*4/8,GOLD,hl=True); barrow(dd,1,'PILE, PILE','',0,CORAL)
            insp(dd,SW/2,GY,t,k=3.6); tagc(dd,SW/2,364,'PILE, FACE : 4',GOLD)
        elif key=='r19':
            barrow(dd,0,'PILE, FACE','4 lancers',4/8,GOLD); barrow(dd,1,'PILE, PILE','6 lancers' if lt>0.3 else '',ease((lt-0.3)/0.6)*6/8,CORAL,hl=True)
            insp(dd,SW/2,GY,t,k=3.6); tagc(dd,SW/2,364,'PILE, PILE : 6',CORAL)
        elif key=='r20':
            insp(dd,SW/2,GY,t,k=4.8)
            sq=math.cos(t*5); coin(dd,SW/2,176,40,'P' if sq>0 else 'F',squash=sq)
            tagc(dd,SW/2,364,'MÊME HASARD, AUTRE ATTENTE',CYAN)
    return fn
story=frame_fn(__import__('sys').modules[__name__],STORY,HEADS)
answer=story
def cover(t):
    def fn(lay,dd):
        slot(dd,44,226,21,'P'); slot(dd,98,226,21,'F'); slot(dd,214,226,21,'P'); slot(dd,268,226,21,'P')
        T(dd,'VS',SW/2,214,24,'press',16,CREAM,align='c'); T(dd,'PILE, FACE',71,270,20,'press',11,CYAN,align='c'); T(dd,'PILE, PILE',241,270,20,'press',11,CORAL,align='c')
        T(dd,'PILE, FACE',SW/2,18,40,'anton',34,CREAM,sp=1,align='c',shadow=(3,3,BLACK)); T(dd,'OU PILE, PILE ?',SW/2,58,40,'anton',32,GOLD,sp=1,align='c',shadow=(3,3,BLACK))
        B.band(lay,SH-44,40); d2=ImageDraw.Draw(lay); txt="LA SÉRIE LA PLUS RAPIDE"; f=F('silk4',11); T(d2,txt,SW/2-tw(txt,f,1)/2,SH-30,14,'silk4',11,CREAM,sp=1)
    return B.frame_with(B.make_scene(fn,t),'ÉNIGME DU JOUR')
decide=make_decide()
end=make_end('#017')
