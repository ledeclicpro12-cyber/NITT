from render_e2x import *
B.NUM='#022'
HEADS={'s1':[('Le braqueur t’a ',CREAM),('enfermé',CORAL)],
 's2':[('Un ',CREAM),('jeu',GOLD),(' pour ta ',CREAM),('liberté',CYAN)],
 's3':[('21 ',GOLD),('allumettes',CREAM),(' sur la table',CREAM)],
 's4':[('Chacun ',CREAM),('son tour',GOLD)],
 's5':[('On en prend ',CREAM),('1, 2',GOLD),(' ou ',CREAM),('3',CORAL)],
 's6':[('La ',CREAM),('dernière',GOLD),(' gagne',CREAM)],
 's7':[('L’autre reste ',CREAM),('enfermé',CORAL)],
 's8':[('Le braqueur te laisse ',CREAM),('commencer',GOLD)],
 'q':[('Combien en prendre ',CREAM),('au 1er tour',GOLD),(' ?',CREAM)],
 'r0':[('Prends-en ',CREAM),('une seule',GOLD)],
 'r1':[('20',GOLD),(' = multiple de ',CREAM),('4',CYAN)],
 'r2':[('Toi : ',CREAM),('4 moins',GOLD),(' son nombre',CREAM)],
 'r3':[('Il en prend ',CREAM),('1,',CORAL),(' tu en prends ',CREAM),('3',CYAN)],
 'r4':[('Il en prend ',CREAM),('2,',CORAL),(' tu en prends ',CREAM),('2',CYAN)],
 'r5':[('Il en prend ',CREAM),('3,',CORAL),(' tu en prends ',CREAM),('1',CYAN)],
 'r6':[('Toujours ',CREAM),('4 de moins',GOLD)],
 'r7':[('16, 12, 8, 4, ',CREAM),('0',GOLD)],
 'r8':[('La dernière ',CREAM),('est pour toi',GOLD)],
 'r9':[('Le secret : ',CREAM),('multiple de 4',GOLD)]}
STORY=('s1','s2','s3','s4','s5','s6','s7','s8','q')
def tbl_small(dd,y):
    box(dd,92,y,128,12,fill=TABLEC,border=TABLED,bw=2); box(dd,100,y+12,10,GY-y-12,fill=TABLED); box(dd,202,y+12,10,GY-y-12,fill=TABLED)
def numbox(dd,cx,y,txt,col=GOLD,w=44,h=44,size=28):
    box(dd,cx-w/2,y,w,h,fill=CARD,border=col,bw=3,shadow=(3,3,BLACK)); T(dd,txt,cx,y+(h-size-4)/2+2,size+4,'press',size,col,align='c')
def bracket(dd,x0,x1,y,col):
    box(dd,x0,y,2,8,fill=col); box(dd,x1-2,y,2,8,fill=col); box(dd,x0,y+6,x1-x0,2,fill=col)
def turn_row(dd,lt,n_him,n_you):
    group(dd,84,128,n_him,gap=20,head=CORAL,h=62); lbl(dd,84,206,'LUI',CORAL)
    if lt>0.9: group(dd,224,128,n_you,gap=20,head=CYAN,h=62); lbl(dd,224,206,'TOI',CYAN)
    if lt>0.2: T(dd,'+',154,140,34,'press',28,CREAM,align='c')
def scene_fn(key,t,lt,dur):
    def fn(lay,dd):
        if key=='s1':
            bars(dd,14,106,170,GY-106,gap=14)
            insp(dd,98,GY,t,k=4.2)
            braq(dd,248,GY,t,k=4.4)
            tagc(dd,SW/2,364,'ENFERMÉ DANS LA CAVE',CORAL)
        elif key=='s2':
            braq(dd,70,GY,t,k=4.4)
            bubble(dd,22,104,150,52,['UN JEU','POUR TOI'],GOLD,13)
            padlock(dd,238,236,1.2)
            if lt>0.5: lbl(dd,238,262,'LIBERTÉ',CYAN)
            tagc(dd,SW/2,364,'UN JEU POUR SORTIR',GOLD)
        elif key=='s3':
            table(dd,246)
            n=21 if lt>1.9 else int(max(0,(lt-0.9)/1.0*21))
            grid21(dd,y0=100,gap=38,rowh=52,show=min(21,max(0,n)),h=38)
            tagc(dd,SW/2,364,'21 ALLUMETTES',GOLD)
        elif key=='s4':
            braq(dd,44,GY,t,k=3.8); insp(dd,SW-44,GY,t,k=3.8)
            tbl_small(dd,276);
            group(dd,SW/2,222,3,gap=18,h=46)
            who=int(t*2)%2
            tri_down(dd,44 if who==0 else SW-44,150,CORAL if who==0 else CYAN,12)
            lbl(dd,44,166,'LUI',CORAL); lbl(dd,SW-44,166,'TOI',CYAN)
            tagc(dd,SW/2,364,'À TOUR DE RÔLE',CORAL)
        elif key=='s5':
            if lt>0.25: group(dd,52,120,1,h=70)
            if lt>0.85: group(dd,SW/2,120,2,gap=24,h=70)
            if lt>1.2: group(dd,SW-62,120,3,gap=24,h=70)
            for cx,txt,th in ((52,'1',0.25),(SW/2,'2',0.85),(SW-62,'3',1.2)):
                if lt>th: numbox(dd,cx,214,txt,GOLD,w=48,h=48)
            tagc(dd,SW/2,364,'1, 2 OU 3 ALLUMETTES',GOLD)
        elif key=='s6':
            for dx in range(-3,4):
                if dx: stick(dd,SW/2+dx*34,150,52,CORAL,dim=True)
            stick(dd,SW/2,150,52,GOLD,hl=True)
            if lt>0.4: lbl(dd,SW/2,222,'LA DERNIÈRE',GOLD)
            if lt>1.5:
                trophy(dd,SW/2,254,1.2); stamp(dd,SW/2,326,'GAGNÉ',GRN,14)
            tagc(dd,SW/2,364,'LA DERNIÈRE GAGNE',GOLD)
        elif key=='s7':
            bars(dd,60,106,192,GY-106,gap=14)
            insp(dd,SW/2,GY,t,k=4.2)
            if lt>0.5: stamp(dd,SW/2,150,'ENFERMÉ',RED,14)
            tagc(dd,SW/2,364,'LE PERDANT RESTE LÀ',CORAL)
        elif key=='s8':
            insp(dd,70,GY,t,k=4.4); braq(dd,SW-62,GY,t,k=4.4)
            bubble(dd,28,108,100,48,['TOI','D’ABORD'],CYAN,13)
            if lt>0.6: bubble(dd,176,108,106,48,['À TOI','DE JOUER'],CORAL,13)
            tagc(dd,SW/2,364,'TOI EN PREMIER',CYAN)
        elif key=='q':
            T(dd,'?',SW/2,98,60,'press',50,GOLD,align='c',shadow=(4,4,BLACK))
            grid21(dd,y0=164,gap=38,rowh=52,h=38)
            tagc(dd,SW/2,364,'COMBIEN AU 1ER TOUR ?',CORAL)
        # ---- réponse ----
        elif key=='r0':
            grid21(dd,y0=164,gap=38,rowh=52,h=38,hl=((0,) if lt>0.5 else ()),lift=((0,) if lt>0.5 else ()))
            if lt>0.4: numbox(dd,SW/2,98,'1',GOLD,w=56,h=48,size=34)
            tagc(dd,SW/2,364,'UNE SEULE ALLUMETTE',GOLD)
        elif key=='r1':
            cols=[GOLD,CYAN,CORAL,GRN,VIO]
            cx0=SW/2-2*58
            for g in range(5):
                group(dd,cx0+g*58,130,4,gap=12,head=cols[g],h=46)
                if lt>0.8: bracket(dd,cx0+g*58-26,cx0+g*58+26,190,cols[g])
            if lt>1.5:
                box(dd,SW/2-120,226,240,50,fill=CARD,border=GOLD,bw=3,shadow=(3,3,BLACK))
                T(dd,'20 = 5 × 4',SW/2,240,24,'press',20,GOLD,align='c')
            tagc(dd,SW/2,364,'20 = MULTIPLE DE QUATRE',CYAN)
        elif key=='r2':
            braq(dd,50,GY,t,k=3.8); insp(dd,SW-50,GY,t,k=3.8)
            T(dd,'?',50,110,40,'press',34,CORAL,align='c')
            if lt>1.4:
                box(dd,SW/2-108,170,216,56,fill=CARD,border=GOLD,bw=3,shadow=(3,3,BLACK))
                T(dd,'4 - LUI = TOI',SW/2,190,20,'press',14,GOLD,align='c')
            tagc(dd,SW/2,364,'QUATRE MOINS SON NOMBRE',GOLD)
        elif key in ('r3','r4','r5'):
            a={'r3':1,'r4':2,'r5':3}[key]; b=4-a
            turn_row(dd,lt,a,b)
            if lt>1.3:
                box(dd,SW/2-95,252,190,48,fill=CARD,border=GOLD,bw=3,shadow=(3,3,BLACK))
                T(dd,f'{a} + {b} = 4',SW/2,266,24,'press',20,GOLD,align='c')
            tagc(dd,SW/2,364,'TOUJOURS QUATRE AU TOTAL',CORAL)
        elif key=='r6':
            cx0=SW/2-2*58
            for g in range(5):
                group(dd,cx0+g*58,130,4,gap=12,head=CORAL,h=46,dim=(g==4 and lt>1.2))
            if lt>1.2:
                T(dd,'- 4',SW/2,214,40,'press',34,CORAL,align='c',shadow=(4,4,BLACK))
            tagc(dd,SW/2,364,'QUATRE DE MOINS PAR TOUR',CORAL)
        elif key=='r7':
            vals=['16','12','8','4','0']; th=[0.0,0.35,0.75,1.15,1.5]
            for i,(v,tt) in enumerate(zip(vals,th)):
                cx=SW/2+(i-2)*58
                if lt>tt:
                    numbox(dd,cx,150,v,GOLD if i==4 else CREAM,w=54,h=60,size=22)
            tagc(dd,SW/2,364,'IL RESTE DE MOINS EN MOINS',GOLD)
        elif key=='r8':
            insp(dd,64,GY,t,k=4.2)
            stick(dd,SW/2+10,130,56,GOLD,hl=True)
            trophy(dd,SW-60,160,1.3)
            if lt>0.3: stamp(dd,196,300,'POUR TOI',GRN,14)
            if lt>1.0: B.confetti(dd,t,t-lt)
            tagc(dd,SW/2,364,'LA DERNIÈRE EST À TOI',GOLD)
        elif key=='r9':
            insp(dd,60,GY,t,k=4.0)
            box(dd,120,108,172,200,fill=CARD,border=GOLD,bw=4,shadow=(4,4,BLACK))
            T(dd,'× 4',206,120,34,'press',26,CORAL,align='c')
            for i,v in enumerate(['4','8','12','16','20']):
                T(dd,v,206,164+i*28,24,'press',18,GOLD if i==4 else CREAM,align='c')
            B.confetti(dd,t,t-lt)
            tagc(dd,SW/2,364,'LAISSE UN MULTIPLE DE QUATRE',GOLD)
    return fn
story=frame_fn(__import__('sys').modules[__name__],STORY,HEADS)
answer=story
def cover(t):
    B.NUM='#022'
    def fn(lay,dd):
        grid21(dd,y0=118,gap=32,rowh=46,h=32)
        braq(dd,262,340,t,k=3.0,still=True); insp(dd,50,340,t,k=3.0)
        T(dd,'21 ALLUMETTES',SW/2,18,40,'anton',32,CREAM,sp=1,align='c',shadow=(3,3,BLACK)); T(dd,'TU JOUES EN 1ER',SW/2,58,40,'anton',32,GOLD,sp=1,align='c',shadow=(3,3,BLACK))
        B.band(lay,SH-44,40); d2=ImageDraw.Draw(lay); txt="LE JEU DE LA DERNIÈRE ALLUMETTE"; f=F('silk4',11); T(d2,txt,SW/2-tw(txt,f,1)/2,SH-30,14,'silk4',11,CREAM,sp=1)
    return B.frame_with(B.make_scene(fn,t),'ÉNIGME DU JOUR')
decide=make_decide()
end=make_end('#023')
