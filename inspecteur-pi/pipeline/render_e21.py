from render_x import *
B.NUM='#021'
VIO=rgb('#B05CFF')
HEADS={'s1':[('L’inspecteur ',CREAM),('devine',GOLD),(' ton résultat',CREAM)],
 's2':[('Prends un ',CREAM),('papier',GOLD),(' et un ',CREAM),('crayon',CYAN)],
 's3':[('Étape 1 : ',GOLD),('3 chiffres',CREAM)],
 's4':[('Premier chiffre ',CREAM),('plus grand',CORAL),(' que le dernier',CREAM)],
 's5':[('Étape 2 : ',GOLD),('à l’envers',CYAN)],
 's6':[('Étape 3 : ',GOLD),('soustrais',CORAL)],
 's7':[('Étape 4 : ',GOLD),('à l’envers',CYAN)],
 's8':[('Étape 5 : ',GOLD),('additionne',CORAL)],
 's9':[('L’inspecteur a ',CREAM),('prédit',GOLD),(' ton résultat',CREAM)],
 'q':[('Quel ',CREAM),('nombre',GOLD),(' a-t-il prédit\u00a0?',CREAM)],
 'r0':[('Toujours ',CREAM),('1089',GOLD)],
 'r1':[('Prenons ',CREAM),('832',GOLD)],
 'r2':[('832',GOLD),(' à l’envers : ',CREAM),('238',CYAN)],
 'r3':[('832',GOLD),(' moins ',CREAM),('238',CYAN),(' : ',CREAM),('594',CORAL)],
 'r4':[('594',CORAL),(' à l’envers : ',CREAM),('495',VIO)],
 'r5':[('594',CORAL),(' plus ',CREAM),('495',VIO),(' : ',CREAM),('1089',GOLD)],
 'r6':[('Mais ',CREAM),('pourquoi',CYAN),(' ?',CREAM)],
 'r7':[('Le chiffre du ',CREAM),('milieu',GOLD),(' : toujours 9',CREAM)],
 'r8':[('Les ',CREAM),('2 autres',CORAL),(' font 9 ensemble',CREAM)],
 'r9':[('Résultat : ',CREAM),('1089',GOLD),(' !',CREAM)]}
STORY=('s1','s2','s3','s4','s5','s6','s7','s8','s9','q')
DW,DH=48,60
def dbox(dd,cx,y,ch,col=CREAM,hl=False,w=DW,h=DH,fill=CARD,size=30):
    box(dd,cx-w/2,y,w,h,fill=fill,border=(GOLD if hl else col),bw=3,shadow=(3,3,BLACK))
    if ch: T(dd,ch,cx,y+(h-size-4)/2+2,size+4,'press',size,col,align='c')
def row(dd,cy,y,chs,cols=None,hl=(),w=DW,h=DH,gap=8,size=30,hlcol=None):
    n=len(chs); tot=n*w+(n-1)*gap; x0=cy-tot/2+w/2
    for i,ch in enumerate(chs):
        c=(cols[i] if cols else CREAM)
        dbox(dd,x0+i*(w+gap),y,ch,c,hl=(i in hl),w=w,h=h,size=size)
    return x0,w,gap
ABC=[GOLD,CREAM,CYAN]; DEF=[CORAL,CREAM,VIO]
def tri_down(dd,x,y,col=CYAN,k=7):
    dd.polygon([((x-k)*S,(y-k)*S),((x+k)*S,(y-k)*S),(x*S,(y+k)*S)],fill=col)
def env(dd,cx,cy,t,w=150,h=100,seal=True):
    box(dd,cx-w/2,cy-h/2,w,h,fill=rgb('#E8D9B5'),border=DARK,bw=3,shadow=(4,4,BLACK))
    dd.polygon([((cx-w/2+3)*S,(cy-h/2+3)*S),((cx+w/2-3)*S,(cy-h/2+3)*S),(cx*S,(cy+8)*S)],fill=rgb('#D3C196'),outline=DARK)
    if seal: disc(dd,cx,cy+8,13,RED,DARK,2); T(dd,'!',cx,cy+1,16,'press',13,CREAM,align='c')
def scene_fn(key,t,lt,dur):
    def fn(lay,dd):
        if key=='s1':
            insp(dd,SW/2,336,t,k=5.0)
            bubble(dd,46,106,220,56,['JE DEVINE','TON RÉSULTAT'],GOLD,13)
            tagc(dd,SW/2,364,'AVANT QUE TU CALCULES',CORAL)
        elif key=='s2':
            box(dd,70,110,172,230,fill=rgb('#F3EBDD'),border=DARK,bw=3,shadow=(4,4,BLACK))
            for yy in range(138,330,22): box(dd,82,yy,148,2,fill=rgb('#B8C4DA'))
            box(dd,92,110,2,230,fill=rgb('#E07070'))
            ang=math.sin(t*5)*6
            dd.polygon([((196+ang)*S,196*S),((214+ang)*S,196*S),((240)*S,246*S),((226)*S,252*S)],fill=GOLD,outline=DARK)
            dd.polygon([((226)*S,252*S),((240)*S,246*S),((232)*S,262*S)],fill=rgb('#F1C39B'),outline=DARK)
            tagc(dd,SW/2,364,'PAPIER + CRAYON',GOLD)
        elif key=='s3':
            T(dd,'1',SW/2,100,90,'press',72,GOLD,align='c',shadow=(5,5,BLACK))
            row(dd,SW/2,210,['A','B','C'],ABC)
            if lt>0.3: lbl(dd,SW/2,290,'UN NOMBRE À 3 CHIFFRES',CYAN)
            tagc(dd,SW/2,364,'ÉTAPE 1',GOLD)
        elif key=='s4':
            row(dd,SW/2,170,['A','B','C'],ABC,hl=(0,2))
            if lt>1.0:
                x0=SW/2-56; x1=SW/2+56
                box(dd,x0-1,250,2,14,fill=GOLD); box(dd,x1-1,250,2,14,fill=GOLD); box(dd,x0-1,262,x1-x0+2,2,fill=GOLD)
            if lt>1.6:
                box(dd,SW/2-120,284,240,40,fill=CARD,border=GOLD,bw=3,shadow=(3,3,BLACK))
                T(dd,'A DÉPASSE C DE 2 OU PLUS',SW/2,298,14,'silk7',10,GOLD,align='c',sp=1)
            tagc(dd,SW/2,364,'A PLUS GRAND QUE C',CORAL)
        elif key in ('s5','s7'):
            top=['A','B','C'] if key=='s5' else ['D','E','F']; bot=top[::-1]; cols=ABC if key=='s5' else DEF
            row(dd,SW/2,122,top,cols)
            for dx in (-56,0,56): tri_down(dd,SW/2+dx,202,CYAN,8)
            if lt>0.5: row(dd,SW/2,226,bot,cols[::-1])
            tagc(dd,SW/2,364,'ÉCRIS-LE À L’ENVERS',CYAN)
        elif key=='s6':
            row(dd,SW/2,118,['A','B','C'],ABC,h=54)
            T(dd,'-',46,206,34,'press',30,CORAL,align='c')
            row(dd,SW/2,190,['C','B','A'],ABC[::-1],h=54)
            dd.rectangle([40*S,262*S,(SW-40)*S,266*S],fill=CREAM)
            if lt>0.9: row(dd,SW/2,274,['D','E','F'],DEF,h=54)
            tagc(dd,SW/2,364,'LE GRAND MOINS LE PETIT',CORAL)
        elif key=='s8':
            row(dd,SW/2+10,112,['D','E','F'],DEF,h=52,w=44)
            T(dd,'+',44,170,34,'press',30,CORAL,align='c')
            row(dd,SW/2+10,168,['F','E','D'],DEF[::-1],h=52,w=44)
            dd.rectangle([30*S,238*S,(SW-30)*S,242*S],fill=CREAM)
            if lt>0.8: row(dd,SW/2+10,252,['?','?','?','?'],[GOLD]*4,h=52,w=44,size=26)
            tagc(dd,SW/2,364,'ADDITIONNE LES DEUX',CORAL)
        elif key=='s9':
            env(dd,100,236,t,w=140,h=96)
            insp(dd,244,330,t,k=3.8)
            lbl(dd,100,170,'PRÉDICTION',GOLD)
            tagc(dd,SW/2,364,'SCELLÉE À L’AVANCE',GOLD)
        elif key=='q':
            env(dd,SW/2,236,t,w=170,h=112,seal=False)
            T(dd,'?',SW/2,206,80,'press',64,GOLD,align='c',shadow=(4,4,BLACK))
            tagc(dd,SW/2,364,'QUEL NOMBRE ?',CORAL)
        # ---- réponse ----
        elif key=='r0':
            insp(dd,SW/2,336,t,k=4.0)
            if lt>0.55:
                box(dd,SW/2-120,112,240,100,fill=CARD,border=GOLD,bw=4,shadow=(4,4,BLACK))
                T(dd,'1089',SW/2,140,56,'press',44,GOLD,align='c',shadow=(4,4,BLACK))
            tagc(dd,SW/2,364,'TOUJOURS 1089',GOLD)
        elif key=='r1':
            row(dd,SW/2,170,['8','3','2'],ABC,w=56,h=72,size=36)
            tagc(dd,SW/2,364,'UN NOMBRE AU CHOIX',GOLD)
        elif key=='r2':
            row(dd,SW/2,120,['8','3','2'],ABC)
            for dx in (-56,0,56): tri_down(dd,SW/2+dx,202,CYAN,8)
            if lt>0.9: row(dd,SW/2,226,['2','3','8'],ABC[::-1])
            tagc(dd,SW/2,364,'À L’ENVERS : 238',CYAN)
        elif key=='r3':
            row(dd,SW/2+14,126,['8','3','2'],ABC,h=54)
            if lt>1.0:
                T(dd,'-',40,206,34,'press',30,CORAL,align='c')
                row(dd,SW/2+14,190,['2','3','8'],ABC[::-1],h=54)
            dd.rectangle([30*S,262*S,(SW-30)*S,266*S],fill=CREAM)
            if lt>2.2: row(dd,SW/2+14,274,['5','9','4'],DEF,h=54,hl=(0,1,2))
            tagc(dd,SW/2,364,'832 - 238 = 594',CORAL)
        elif key=='r4':
            row(dd,SW/2,120,['5','9','4'],DEF)
            for dx in (-56,0,56): tri_down(dd,SW/2+dx,202,CYAN,8)
            if lt>0.85: row(dd,SW/2,226,['4','9','5'],DEF[::-1])
            tagc(dd,SW/2,364,'À L’ENVERS : 495',CYAN)
        elif key=='r5':
            row(dd,SW/2+14,126,['5','9','4'],DEF,h=54)
            if lt>0.7:
                T(dd,'+',40,206,34,'press',30,CORAL,align='c')
                row(dd,SW/2+14,190,['4','9','5'],DEF[::-1],h=54)
            dd.rectangle([30*S,262*S,(SW-30)*S,266*S],fill=CREAM)
            if lt>2.85: row(dd,SW/2+14,274,['1','0','8','9'],[GOLD]*4,h=54,w=44,hl=(0,1,2,3))
            tagc(dd,SW/2,364,'594 + 495 = 1089',GOLD)
        elif key=='r6':
            insp(dd,90,336,t,k=5.0); bubble(dd,150,120,150,70,['POURQUOI','?'],CYAN,14)
            tagc(dd,SW/2,364,'MAIS POURQUOI ?',CYAN)
        elif key=='r7':
            row(dd,SW/2,150,['5','9','4'],DEF,hl=((1,) if lt>1.7 else ()),w=56,h=72,size=36)
            if lt>1.7:
                tri_down(dd,SW/2,250,GOLD,9); lbl(dd,SW/2,266,'TOUJOURS 9',GOLD)
            tagc(dd,SW/2,364,'LE CHIFFRE DU MILIEU',GOLD)
        elif key=='r8':
            row(dd,SW/2,150,['5','9','4'],DEF,hl=((0,2) if lt>0.4 else ()),w=56,h=72,size=36)
            if lt>1.4:
                box(dd,SW/2-100,262,200,44,fill=CARD,border=GOLD,bw=3,shadow=(3,3,BLACK))
                T(dd,'5 + 4 = 9',SW/2,274,26,'press',20,GOLD,align='c')
            tagc(dd,SW/2,364,'LES DEUX AUTRES : 9 ENSEMBLE',CORAL)
        elif key=='r9':
            insp(dd,SW/2,336,t,k=4.0)
            box(dd,SW/2-120,112,240,100,fill=CARD,border=GOLD,bw=4,shadow=(4,4,BLACK))
            T(dd,'1089',SW/2,140,56,'press',44,GOLD,align='c',shadow=(4,4,BLACK))
            B.confetti(dd,t,t-lt)
            tagc(dd,SW/2,364,'TOUJOURS 1089',GOLD)
    return fn
story=frame_fn(__import__('sys').modules[__name__],STORY,HEADS)
answer=story
def cover(t):
    def fn(lay,dd):
        env(dd,SW/2,236,t,w=180,h=118)
        T(dd,'?',SW/2,168,60,'press',50,GOLD,align='c',shadow=(4,4,BLACK))
        insp(dd,56,340,t,k=3.4)
        T(dd,'IL DEVINE',SW/2,18,40,'anton',32,CREAM,sp=1,align='c',shadow=(3,3,BLACK)); T(dd,'TON RÉSULTAT',SW/2,58,40,'anton',32,GOLD,sp=1,align='c',shadow=(3,3,BLACK))
        B.band(lay,SH-44,40); d2=ImageDraw.Draw(lay); txt="LE TOUR DE MAGIE DES CHIFFRES"; f=F('silk4',11); T(d2,txt,SW/2-tw(txt,f,1)/2,SH-30,14,'silk4',11,CREAM,sp=1)
    return B.frame_with(B.make_scene(fn,t),'ÉNIGME DU JOUR')
decide=make_decide()
end=make_end('#022')
