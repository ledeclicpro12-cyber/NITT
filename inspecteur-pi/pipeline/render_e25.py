from render_e2x import *
B.NUM='#025'
SKIN=rgb('#F1C39B'); HAIRC=rgb('#6B4A2E'); WOODC=rgb('#8A5A3A'); WOODL=rgb('#B58A4A')
HEADS={'s1':[('Deux ',CREAM),('Parisiens,',GOLD),(' même nombre de ',CREAM),('cheveux',CORAL)],
 's2':[('Prouver ',CREAM),('sans compter',GOLD)],
 's3':[('Plus de ',CREAM),('2 millions',GOLD),(' d’habitants',CREAM)],
 's4':[('Environ ',CREAM),('100 000',GOLD),(' cheveux par tête',CREAM)],
 's5':[('Jamais plus de ',CREAM),('200 000',CORAL)],
 's6':[('Impossible',CORAL),(' de les ',CREAM),('compter',GOLD)],
 'q':[('Comment être ',CREAM),('sûr',GOLD),(' ?',CREAM)],
 'r0':[('Le principe des ',CREAM),('tiroirs',GOLD)],
 'r1':[('200 001',GOLD),(' tiroirs',CREAM)],
 'r2':[('De ',CREAM),('0',GOLD),(' à ',CREAM),('200 000',GOLD)],
 'r3':[('Le numéro : ',CREAM),('nombre de cheveux',CYAN)],
 'r4':[('Chacun va dans ',CREAM),('son tiroir',GOLD)],
 'r5':[('Plus de ',CREAM),('2 millions',GOLD),(' de Parisiens',CREAM)],
 'r6':[('Seulement ',CREAM),('200 001',CORAL),(' tiroirs',CREAM)],
 'r7':[('Forcément ',CREAM),('2 Parisiens',GOLD),(' dans un tiroir',CREAM)],
 'r8':[('Au moins ',GOLD),('10',GOLD),(' Parisiens',CREAM)],
 'r9':[('Sans en ',CREAM),('compter',GOLD),(' un seul',CREAM)]}
STORY=('s1','s2','s3','s4','s5','s6','q')

def person(dd,x,y,col=CORAL,k=1.0):
    """petit personnage : x,y = haut de la tête"""
    box(dd,x,y,6*k,5*k,fill=SKIN); box(dd,x,y-1.5*k,6*k,2.5*k,fill=HAIRC); box(dd,x-1*k,y+5*k,8*k,7*k,fill=col)
def hairhead(dd,cx,cy,r=22,t=0.0,n=26,col=HAIRC):
    """grosse tête vue de face avec des cheveux en bataille"""
    rnd=random.Random(5)
    for i in range(n):
        a=math.pi*(1.05+0.9*i/(n-1)); L=r*(0.45+0.25*rnd.random())
        x0=cx+r*0.92*math.cos(a); y0=cy+r*0.92*math.sin(a)
        dd.line([(x0*S,y0*S),((cx+(r*0.92+L)*math.cos(a))*S,(cy+(r*0.92+L)*math.sin(a))*S)],fill=col,width=2*S)
    disc(dd,cx,cy,r+2,DARK); disc(dd,cx,cy,r,SKIN)
    box(dd,cx-r*0.42,cy-r*0.15,r*0.18,r*0.2,fill=DARK); box(dd,cx+r*0.24,cy-r*0.15,r*0.18,r*0.2,fill=DARK)
    box(dd,cx-r*0.25,cy+r*0.4,r*0.5,r*0.1,fill=rgb('#B04A3A'))
def drawer(dd,x,y,w,h,label=None,col=GOLD,hl=False,open_=False):
    box(dd,x,y,w,h,fill=WOODC,border=(GOLD if hl else DARK),bw=(3 if hl else 2))
    box(dd,x+3,y+3,w-6,h-6,fill=WOODL)
    box(dd,x+w/2-6,y+h*0.62,12,3,fill=DARK)
    if label is not None:
        T(dd,label,x+w/2,y+h*0.22,12,'press',8 if len(label)>4 else 9,DARK,align='c')
def chest(dd,x,y,cols,rows,w=44,h=28,gap=4,hl=(),labels=None):
    box(dd,x-6,y-6,cols*(w+gap)-gap+12,rows*(h+gap)-gap+12,fill=rgb('#4A3220'),border=DARK,bw=2)
    for r_ in range(rows):
        for c_ in range(cols):
            i=r_*cols+c_
            drawer(dd,x+c_*(w+gap),y+r_*(h+gap),w,h,(labels[i] if labels else None),hl=(i in hl))
def skyline(dd,base=GY):
    for bx,bw,bh,c in ((6,36,70,'#2C3766'),(46,30,50,'#36427A'),(236,34,64,'#2C3766'),(272,34,84,'#36427A')):
        box(dd,bx,base-bh,bw,bh,fill=rgb(c),border=DARK,bw=2)
        for yy in range(base-bh+8,base-8,16):
            for xx in range(bx+6,bx+bw-8,12): box(dd,xx,yy,5,7,fill=rgb('#4A5486'))
def eiffel(dd,cx,base,h=170):
    w0=h*0.52
    dd.polygon([((cx-w0/2)*S,base*S),((cx+w0/2)*S,base*S),((cx+3)*S,(base-h)*S),((cx-3)*S,(base-h)*S)],fill=rgb('#3A4270'),outline=DARK)
    dd.polygon([((cx-w0*0.28)*S,base*S),((cx+w0*0.28)*S,base*S),((cx+w0*0.2)*S,(base-h*0.3)*S),((cx-w0*0.2)*S,(base-h*0.3)*S)],fill=rgb('#10142A'))
    for f_ in (0.38,0.62):
        ww=w0*(1-f_)*0.95; box(dd,cx-ww/2,base-h*f_,ww,4,fill=rgb('#5A6BA8'))
    box(dd,cx-1,base-h-14,2,14,fill=rgb('#5A6BA8'))
def crowd(dd,x0,y0,cols,rows,gx=17,gy=22,t=0.0,k=1.0):
    cs=[CORAL,CYAN,GOLD,rgb('#B05CFF'),GRN]
    for r_ in range(rows):
        for c_ in range(cols): person(dd,x0+c_*gx,y0+r_*gy,cs[(r_*3+c_)%5],k)
def bignum(dd,cx,y,txt,col=GOLD,w=120,h=64,size=32):
    box(dd,cx-w/2,y,w,h,fill=CARD,border=col,bw=4,shadow=(4,4,BLACK)); T(dd,txt,cx,y+(h-size-4)/2+2,size+4,'press',size,col,align='c')

def scene_fn(key,t,lt,dur):
    def fn(lay,dd):
        if key=='s1':
            eiffel(dd,156,GY,150); skyline(dd)
            hairhead(dd,82,150,28,t); hairhead(dd,230,150,28,t)
            T(dd,'=',156,134,40,'press',34,GOLD,align='c',shadow=(3,3,BLACK))
            tagc(dd,SW/2,364,'À PARIS',GOLD)
        elif key=='s2':
            hairhead(dd,SW/2,200,50,t)
            T(dd,'1 2 3 ...',SW/2,290,26,'press',18,CREAM,align='c')
            if lt>0.6: cross(dd,SW/2,298,128,8,RED) if False else None
            if lt>0.6: box(dd,SW/2-72,296,144,6,fill=RED)
            tagc(dd,SW/2,364,'SANS COMPTER',CORAL)
        elif key=='s3':
            crowd(dd,28,100,15,9,gx=19,gy=22,t=t)
            if lt>0.4: bignum(dd,SW/2,196,'2 000 000+',GOLD,w=250,h=56,size=22)
            tagc(dd,SW/2,364,'HABITANTS DE PARIS',GOLD)
        elif key=='s4':
            hairhead(dd,SW/2,205,64,t,n=44)
            if lt>0.5: bignum(dd,SW/2,300,'100 000',GOLD,w=180,h=40,size=18)
            tagc(dd,SW/2,364,'CHEVEUX PAR TÊTE',CORAL)
        elif key=='s5':
            box(dd,24,200,264,28,fill=CARD,border=EDGE,bw=2)
            box(dd,26,202,132,24,fill=CYAN)
            box(dd,26+260*0.99,190,6,48,fill=RED)
            lbl(dd,92,244,'MOYENNE',CYAN,10) if False else None
            T(dd,'0',30,246,14,'press',10,CREAM)
            T(dd,'200 000',286,246,14,'press',10,RED,align='r')
            lbl(dd,92,160,'100 000',CYAN,11); lbl(dd,250,160,'MAX',RED,11)
            tagc(dd,SW/2,364,'LIMITE : 200 000',RED)
        elif key=='s6':
            clock(dd,226,170,34,10,int(t*8)%60)
            insp(dd,86,GY,t,k=4.2)
            T(dd,'1 2 3 ...',226,236,24,'press',14,CREAM,align='c')
            T(dd,'?',160,150,40,'press',34,CORAL,align='c')
            tagc(dd,SW/2,364,'BEAUCOUP TROP LONG',CORAL)
        elif key=='q':
            eiffel(dd,156,GY,110); skyline(dd)
            hairhead(dd,82,170,28,t); hairhead(dd,230,170,28,t)
            T(dd,'=',156,150,40,'press',34,GOLD,align='c',shadow=(3,3,BLACK))
            T(dd,'?',156,222,44,'press',36,CORAL,align='c',shadow=(3,3,BLACK))
            tagc(dd,SW/2,364,'COMMENT LE PROUVER ?',CORAL)
        # ---- réponse ----
        elif key=='r0':
            insp(dd,64,GY,t,k=3.6)
            if lt>1.0: chest(dd,150,150,2,5,w=60,h=34,gap=5)
            else: T(dd,'?',220,200,60,'press',50,GOLD,align='c',shadow=(4,4,BLACK))
            tagc(dd,SW/2,364,'LES TIROIRS',GOLD)
        elif key=='r1':
            chest(dd,46,120,4,5,w=52,h=32,gap=4)
            bignum(dd,SW/2,300,'200 001',GOLD,w=170,h=36,size=16)
            tagc(dd,SW/2,364,'200 001 TIROIRS',GOLD)
        elif key=='r2':
            for i,lb in enumerate(['0','1','2']):
                drawer(dd,36+i*84,150,72,60,lb,hl=(i==0 and lt>0.2))
            T(dd,'...',SW/2,230,30,'press',22,CORAL,align='c')
            drawer(dd,100,262,112,60,'200 000',hl=(lt>1.5))
            tagc(dd,SW/2,364,'DE 0 À 200 000',GOLD)
        elif key=='r3':
            hairhead(dd,70,190,32,t)
            lbl(dd,70,245,'N CHEVEUX',CYAN,10)
            dotline(dd,(114,196),(176,196),GOLD,t,n=8)
            drawer(dd,178,160,100,70,'N',hl=True)
            lbl(dd,228,240,'TIROIR N',GOLD,10)
            tagc(dd,SW/2,364,'NUMÉRO = NOMBRE DE CHEVEUX',CYAN)
        elif key=='r4':
            for i,(num,y) in enumerate((('98 412',130),('100 007',204),('99 999',278))):
                person(dd,32,y,[CORAL,CYAN,GOLD][i],2.4); lbl(dd,62,y+34,num,CREAM,8) if False else None
                T(dd,num,30,y+34,10,'press',8,CREAM)
                if lt>0.3+i*0.5: dotline(dd,(110,y+14),(170,y+14),GOLD,t,n=8); drawer(dd,176,y-4,104,44,num,hl=True)
            tagc(dd,SW/2,364,'CHACUN SON TIROIR',GOLD)
        elif key=='r5':
            crowd(dd,28,100,15,9,gx=19,gy=22,t=t)
            bignum(dd,SW/2,196,'2 000 000+',GOLD,w=250,h=56,size=22)
            lbl(dd,SW/2,300,'PARISIENS',CREAM,12)
            tagc(dd,SW/2,364,'BEAUCOUP DE PARISIENS',GOLD)
        elif key=='r6':
            crowd(dd,18,120,6,9,gx=18,gy=22,t=t)
            T(dd,'>',134,200,40,'press',30,GOLD,align='c',shadow=(3,3,BLACK))
            chest(dd,176,170,2,3,w=56,h=34,gap=4)
            lbl(dd,60,322,'2 000 000',GOLD,10); lbl(dd,232,290,'200 001',CORAL,10)
            tagc(dd,SW/2,364,'PEU DE TIROIRS',CORAL)
        elif key=='r7':
            chest(dd,28,120,4,2,w=60,h=36,gap=4,hl=(5,) if lt>0.8 else ())
            if lt>0.8:
                drawer(dd,84,236,144,44,None,hl=True)
                person(dd,124,226,CORAL,2.4); person(dd,160,226,CYAN,2.4)
                lbl(dd,SW/2,290,'MÊME TIROIR',GOLD,11)
            tagc(dd,SW/2,364,'FORCÉMENT 2 DANS UN TIROIR',GOLD)
        elif key=='r8':
            box(dd,36,170,240,120,fill=WOODC,border=GOLD,bw=3,shadow=(4,4,BLACK)); box(dd,42,176,228,108,fill=rgb('#2A1F18'))
            n=int(min(10,1+lt*5))
            for i in range(n):
                person(dd,52+(i%5)*42,190+(i//5)*46,[CORAL,CYAN,GOLD,rgb('#B05CFF'),GRN][i%5],2.6)
            if lt>1.4: bignum(dd,SW/2,108,'10 +',GOLD,w=140,h=48,size=24)
            tagc(dd,SW/2,364,'AU MOINS 10 PARISIENS',GOLD)
        elif key=='r9':
            insp(dd,64,GY,t,k=4.2)
            hairhead(dd,214,190,40,t,n=36)
            T(dd,'=',214,240,34,'press',28,GOLD,align='c') if False else None
            ok_stamp(dd,214,270,'PROUVÉ',GRN)
            star(dd,262,236,t,5); star(dd,160,120,t,4)
            tagc(dd,SW/2,364,'PAS UN SEUL CHEVEU COMPTÉ',CORAL)
    return fn
story=frame_fn(__import__('sys').modules[__name__],STORY,HEADS)
answer=story
def cover(t):
    B.NUM='#025'
    def fn(lay,dd):
        eiffel(dd,156,GY,150); skyline(dd)
        hairhead(dd,70,170,30,t); hairhead(dd,242,170,30,t)
        T(dd,'=',156,150,40,'press',34,GOLD,align='c',shadow=(3,3,BLACK))
        T(dd,'DEUX PARISIENS',SW/2,10,36,'anton',28,CREAM,sp=1,align='c',shadow=(3,3,BLACK)); T(dd,'MÊMES CHEVEUX ?',SW/2,44,36,'anton',28,GOLD,sp=1,align='c',shadow=(3,3,BLACK))
        B.band(lay,SH-44,40); d2=ImageDraw.Draw(lay); txt="L'ÉNIGME DES CHEVEUX"; f=F('silk4',11); T(d2,txt,SW/2-tw(txt,f,1)/2,SH-30,14,'silk4',11,CREAM,sp=1)
    return B.frame_with(B.make_scene(fn,t),'ÉNIGME DU JOUR')
decide=make_decide()
end=make_end('#026')
