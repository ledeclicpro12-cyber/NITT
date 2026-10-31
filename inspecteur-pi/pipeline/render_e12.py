from render_c import *
B.NUM='#012'
SIDE=54
def facec(code): return {'R':RED_,'B':BLU_}.get(code)
def face(dd,x,y,code,s=SIDE,hl=False,dim=False,badge=None,lab=None):
    c=facec(code)
    if c is None:
        box(dd,x,y,s,s,fill=rgb('#1A2347'),border=(GOLD if hl else EDGE),bw=3)
        T(dd,'?',x+s/2,y+s*0.18,s*0.7,'press',int(s*0.55),GOLD,align='c')
    else:
        if dim: c=lerpc(c,rgb('#10142A'),0.6)
        box(dd,x,y,s,s,fill=c,border=(GOLD if hl else DARK),bw=(4 if hl else 2))
        T(dd,code,x+s/2,y+s*0.22,s*0.6,'press',int(s*0.42),(DARK if not dim else rgb('#3A4270')),align='c')
    if badge: 
        box(dd,x+s-18,y-9,22,22,fill=GOLD,border=DARK,bw=2); T(dd,str(badge),x+s-7,y-4,14,'press',11,DARK,align='c')
    if lab: T(dd,lab,x+s/2,y-14,12,'silk7',9,GOLD if hl else GREY,align='c',sp=1)
def card2(dd,x,y,a,b,s=SIDE,hl=(False,False),dim=False,badges=(None,None),labs=(None,None)):
    box(dd,x-5,y-5,2*s+6+10,s+10,fill=(rgb('#3A4270') if dim else CREAM))
    face(dd,x,y,a,s,hl[0],dim,badges[0],labs[0]); face(dd,x+s+6,y,b,s,hl[1],dim,badges[1],labs[1])
CX=100; CY=[98,168,238]
def cards_col(dd,show=3,dim=(0,0,0),hl=None,badges=None,t=0):
    spec=[('R','R'),('B','B'),('R','B')]
    for i in range(show):
        T(dd,'CARTE %d'%(i+1),CX-14,CY[i]+SIDE/2-6,12,'silk7',9,CREAM,align='r',sp=1)
        h=hl[i] if hl else (False,False)
        bd=badges[i] if badges else (None,None)
        card2(dd,CX,CY[i],spec[i][0],spec[i][1],hl=h,dim=bool(dim[i]),badges=bd)
def back(dd,x,y,w=66,h=96,hl=False):
    box(dd,x,y,w,h,fill=rgb('#2A3A7A'),border=(GOLD if hl else CREAM),bw=3)
    box(dd,x+8,y+8,w-16,h-16,fill=rgb('#1A2347'))
    T(dd,'?',x+w/2,y+h*0.26,h*0.5,'press',int(h*0.36),GOLD,align='c')
def hat(dd,cx,top,cards=True,t=0,k=1.0):
    if cards:
        for i,dx in enumerate((-22,0,22)):
            r=-6+int(math.sin(t*3+i)*3)
            box(dd,cx+dx*k-14*k,top-34*k+r,28*k,44*k,fill=rgb('#2A3A7A'),border=CREAM,bw=2)
            T(dd,'?',cx+dx*k,top-26*k+r,14*k,'press',int(12*k),GOLD,align='c')
    box(dd,cx-34*k,top,68*k,54*k,fill=rgb('#0B0D14'),border=rgb('#3A4270'),bw=2)
    box(dd,cx-34*k,top+34*k,68*k,10*k,fill=CORAL)
    box(dd,cx-52*k,top+52*k,104*k,10*k,fill=rgb('#0B0D14'),border=rgb('#3A4270'),bw=2)
def table(dd,y=300):
    box(dd,10,y,SW-20,10,fill=rgb('#8A5A3A')); box(dd,10,y+10,SW-20,4,fill=rgb('#5A3A22'))
    box(dd,28,y+14,10,60,fill=rgb('#5A3A22')); box(dd,SW-38,y+14,10,60,fill=rgb('#5A3A22'))
def coins(dd,cx,cy,n=3):
    for i in range(n):
        box(dd,cx-14,cy-i*7,28,8,fill=GOLD,border=rgb('#C9A24A'),bw=2)
def frac(dd,cx,top,n,d,size=40,col=GOLD,sh=(3,3,BLACK)):
    lh=size+6; w=max(tw(str(n),F('press',size),0),tw(str(d),F('press',size),0))+16
    T(dd,str(n),cx,top,lh,'press',size,col,align='c',shadow=sh)
    box(dd,cx-w/2,top+size+6,w,max(4,size//8),fill=col)
    T(dd,str(d),cx,top+size+6+max(4,size//8)+6,lh,'press',size,col,align='c',shadow=sh)
    return top+2*size+22
HEADS={'s1':[('Trois ',CREAM),('cartes,',CORAL),(' un seul ',CREAM),('pari',GOLD)],
 's2':[('Le ',CREAM),('braqueur',CORAL),(' et son ',CREAM),('chapeau',GOLD)],
 's3':[('Carte 1 : ',CREAM),('rouge',RED),(' des deux côtés',CREAM)],
 's4':[('Carte 2 : ',CREAM),('bleue',CYAN),(' des deux côtés',CREAM)],
 's5':[('Carte 3 : ',CREAM),('rouge',RED),(' et ',CREAM),('bleue',CYAN)],
 's6':[('Il ',CREAM),('mélange',CORAL),(' et ',CREAM),('pioche',GOLD)],
 's8':[('Une carte ',CREAM),('au hasard',GOLD),(' sur la table',CREAM)],
 's9':[('Tu vois une ',CREAM),('face rouge',RED)],
 's10':[('Le braqueur ',CREAM),('sourit',CORAL)],
 's11':[("L'autre face : ",CREAM),('rouge',RED),(' ?',CREAM)],
 's12':[('Une chance sur ',CREAM),('deux',GOLD),(' ?',CREAM)],
 'q':[('Quelle ',CREAM),('probabilité',GOLD),(' ?',CREAM)],
 'r0':[('Réponse : ',CREAM),('2 sur 3',GOLD)],
 'r1':[('Voici ',CREAM),('pourquoi',CORAL)],
 'r2':[('Compte les ',CREAM),('faces rouges',RED)],
 'r3':[('La carte 1 en a ',CREAM),('deux',GOLD)],
 'r4':[('La carte 3 en a ',CREAM),('une',GOLD)],
 'r5':[('Au total : ',CREAM),('3 faces rouges',RED)],
 'r6':[('Même chance de ',CREAM),('la voir',GOLD)],
 'r7':[('2 cas sur 3 : ',CREAM),('carte 1',GOLD)],
 'r8':[("L'autre face est ",CREAM),('rouge',RED)],
 'r9':[('1 cas sur 3 : ',CREAM),('carte mixte',GOLD)],
 'r10':[('Le braqueur gagne ',CREAM),('2 fois sur 3',GOLD)]}
STORY=('s1','s2','s3','s4','s5','s6','s8','s9','s10','s11','s12','q')
def scene_fn(key,t,lt,dur):
    def fn(lay,dd):
        if key=='s1':
            for i,x in enumerate((34,123,212)): back(dd,x,120+int(math.sin(t*3+i*1.3)*4))
            tagc(dd,SW/2,364,'TROIS CARTES · UN PARI',GOLD)
        elif key=='s2':
            braq(dd,70,GY,t,k=8.0); hat(dd,226,236,True,t,k=1.35); tagc(dd,SW/2,364,'LE BRAQUEUR',CORAL)
        elif key=='s3':
            cards_col(dd,1); tagc(dd,SW/2,364,'ROUGE / ROUGE',RED)
        elif key=='s4':
            cards_col(dd,2); tagc(dd,SW/2,364,'BLEUE / BLEUE',CYAN)
        elif key=='s5':
            cards_col(dd,3); tagc(dd,SW/2,364,'ROUGE / BLEUE',CREAM)
        elif key=='s6':
            hat(dd,SW/2,250,False,t)
            slots=[48,123,198]
            if lt<0.8:
                ph=int(lt/0.3)%3; p=ease((lt%0.3)/0.3)
                perm=[[0,1,2],[1,0,2],[1,2,0]]; a=perm[ph]; b=perm[(ph+1)%3] if ph<2 else [0,2,1]
                for i in range(3):
                    xa=slots[a.index(i)]; xb=slots[b.index(i)]
                    back(dd,lerp(xa,xb,p),112,w=64,h=92)
                tagc(dd,SW/2,364,'ON MÉLANGE',CORAL)
            else:
                for i,x in enumerate(slots):
                    up=(i==1); back(dd,x,112-(34*ease((lt-0.8)/0.35) if up else 0),w=64,h=92,hl=up)
                tagc(dd,SW/2,364,'UNE CARTE AU HASARD',GOLD)
        elif key=='s8':
            table(dd,300); y=lerp(130,196,ease(lt/0.8)); back(dd,SW/2-33,y,w=66,h=96,hl=True)
            if lt>0.8: box(dd,SW/2-40,296,80,4,fill=BLACK)
            tagc(dd,SW/2,364,'SUR LA TABLE',CREAM)
        elif key=='s9':
            table(dd,300); card2(dd,CX,210,'R','?',hl=(True,False),labs=('VISIBLE','CACHÉE'))
            tagc(dd,SW/2,364,'FACE VISIBLE : ROUGE',RED)
        elif key=='s10':
            braq(dd,80,GY,t,k=8.0)
            if lt>1.3: bubble(dd,128,118,176,66,['JE PARIE','UN MILLION !'],GOLD,12)
            coins(dd,236,GY-6,4); coins(dd,266,GY-6,3)
            tagc(dd,SW/2,364,'IL PARIE',GOLD)
        elif key=='s11':
            table(dd,300); card2(dd,CX,210,'R','?',hl=(True,True),labs=('VISIBLE','CACHÉE'))
            T(dd,'ROUGE AUSSI ?',SW/2,132,22,'press',15,GOLD,align='c',shadow=(2,2,BLACK))
            tagc(dd,SW/2,364,"PARI : L'AUTRE FACE EST ROUGE",RED,w=290)
        elif key=='s12':
            frac(dd,SW/2,98,1,2,56)
            if lt>0.9: tagc(dd,SW/2,250,'PLUS ?',CORAL)
            if lt>1.4: tagc(dd,SW/2,276,'MOINS ?',CYAN)
        elif key=='q':
            table(dd,300); card2(dd,CX,222,'R','?',hl=(True,False),labs=('VISIBLE','CACHÉE'))
            T(dd,'?',SW/2,98,100,'press',84,GOLD,align='c',shadow=(4,4,BLACK))
            tagc(dd,SW/2,364,'FACE CACHÉE = ROUGE ?',RED)
        # ---- réponse ----
        elif key=='r0':
            insp(dd,SW/2,GY,t,k=4.0)
            if lt<1.0: T(dd,'?',SW/2,120,100,'press',84,GOLD,align='c',shadow=(4,4,BLACK))
            else:
                frac(dd,SW/2,100,2,3,60); B.confetti(dd,t,t-lt)
                tagc(dd,SW/2,364,'DEUX CHANCES SUR TROIS',GOLD)
        elif key=='r1':
            insp(dd,SW/2,GY,t,k=5.4); T(dd,'?',SW/2+80,120+int(math.sin(t*4)*4),60,'press',48,CYAN,align='c')
            tagc(dd,SW/2,364,'VOICI POURQUOI',CORAL)
        elif key=='r2':
            on=int(t*3)%2==0
            cards_col(dd,3,hl=[(on,on),(False,False),(on,False)]); tagc(dd,SW/2,364,'COMPTE LES FACES ROUGES',RED,w=250)
        elif key=='r3':
            cards_col(dd,3,dim=(0,1,1),hl=[(True,True),(False,False),(False,False)],badges=[(1 if lt>0.95 else None,2 if lt>1.05 else None),(None,None),(None,None)])
            tagc(dd,SW/2,364,'CARTE 1 : 2 FACES ROUGES',RED,w=270)
        elif key=='r4':
            cards_col(dd,3,dim=(1,1,0),hl=[(False,False),(False,False),(True,False)],badges=[(1,2),(None,None),(3 if lt>0.85 else None,None)])
            tagc(dd,SW/2,364,'CARTE 3 : 1 FACE ROUGE',RED,w=260)
        elif key=='r5':
            cards_col(dd,3,dim=(0,1,0),hl=[(True,True),(False,False),(True,False)],badges=[(1,2),(None,None),(3,None)])
            T(dd,'3',274,150,70,'press',60,GOLD,align='c',shadow=(3,3,BLACK))
            tagc(dd,SW/2,364,'3 FACES ROUGES POSSIBLES',RED,w=290)
        elif key=='r6':
            i=int(t*2.5)%3
            for k,x in enumerate((46,126,206)):
                face(dd,x,170,'R',s=60,hl=(k==i),badge=k+1)
                if k==i: T(dd,'TU VOIS',x+30,140,12,'silk7',9,GOLD,align='c',sp=1)
            T(dd,'MÊME CHANCE',SW/2,262,22,'press',14,CREAM,align='c')
            tagc(dd,SW/2,364,'CHACUNE : 1 CHANCE SUR 3',GOLD,w=270)
        elif key=='r7':
            for k,x in enumerate((46,126,206)):
                face(dd,x,196,'R',s=60,hl=(k<2),dim=(k==2),badge=k+1)
            dd.line([(46*S,276*S),(186*S,276*S)],fill=GOLD,width=4*S)
            T(dd,'CARTE ROUGE / ROUGE',116,288,14,'silk7',9,GOLD,align='c',sp=1)
            frac(dd,SW/2,92,2,3,22)
            tagc(dd,SW/2,364,'2 CAS SUR 3',GOLD)
        elif key=='r8':
            table(dd,300); card2(dd,CX,210,'R','R',hl=(True,False),labs=('VISIBLE','CACHÉE'))
            T(dd,'ROUGE !',SW/2,140,40,'press',28,RED,align='c',shadow=(3,3,BLACK))
            tagc(dd,SW/2,364,"L'AUTRE FACE EST ROUGE",RED,w=270)
        elif key=='r9':
            rev=lt>2.8
            table(dd,300); card2(dd,CX,210,'R','B' if rev else '?',hl=(True,rev),labs=('VISIBLE','CACHÉE'))
            frac(dd,SW/2,96,1,3,26)
            tagc(dd,SW/2,364,"L'AUTRE FACE EST BLEUE" if rev else '1 CAS SUR 3',CYAN if rev else GOLD,w=(270 if rev else None))
        elif key=='r10':
            braq(dd,66,GY,t,k=7.0); coins(dd,262,GY-6,5)
            if lt>1.0: frac(dd,SW/2+50,98,2,3,40)
            if lt>2.0:
                frac(dd,SW/2+50,210,1,2,22,GREY,None)
                dd.line([((SW/2+10)*S,262*S),((SW/2+90)*S,222*S)],fill=RED,width=5*S)
            tagc(dd,SW/2,364,'PAS UNE CHANCE SUR DEUX' if lt>2.0 else 'IL GAGNE !',RED if lt>2.0 else GOLD,w=(280 if lt>2.0 else None))
    return fn
story=frame_fn(__import__('sys').modules[__name__],STORY,HEADS)
answer=story
def cover(t):
    def fn(lay,dd):
        for i,(a,b) in enumerate((('R','R'),('B','B'),('R','B'))):
            pass
        card2(dd,CX-4,112+int(math.sin(t*3)*3),'R','R',s=60); card2(dd,CX-4,196,'B','B',s=60); card2(dd,CX-4,280,'R','B',s=60)
        T(dd,'LA CARTE CACHÉE',SW/2,18,40,'anton',32,CREAM,sp=1,align='c',shadow=(3,3,BLACK)); T(dd,'TU PARIES ?',SW/2,58,40,'anton',32,GOLD,sp=1,align='c',shadow=(3,3,BLACK))
        B.band(lay,SH-44,40); d2=ImageDraw.Draw(lay); txt="TROIS CARTES, UN PARI"; f=F('silk4',11); T(d2,txt,SW/2-tw(txt,f,1)/2,SH-30,14,'silk4',11,CREAM,sp=1)
    return B.frame_with(B.make_scene(fn,t),'ÉNIGME DU JOUR')
decide=make_decide()
end=make_end('#013')
