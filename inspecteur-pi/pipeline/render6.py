from render import *
from render3 import MAN, MPAL, ease, lerp, line
from render5 import txt_lines, PAL, GIRL
import math, random
NUM='#004'
SW,SH=312,396; CXo,CYo=24,112          # scene card position (safe area : y 112 -> 508)
FLOOR=270; DX=[34,126,218]; DW=60; DT=108; DH=150
HOSTPAL=dict(PAL); HOSTPAL.update({'T':'#1B1F3A','K':'#2A1A10'})
def header4(d,label):
    T(d, NUM, 24, 84, 18, 'press', 12, CORAL); T(d, label, 336, 84, 18, 'silk4', 11, GREY, sp=2, align='r')
def car(d,cx,by,k=1.0):
    box(d,cx-22*k,by-14*k,44*k,10*k,fill=CORAL); box(d,cx-12*k,by-24*k,24*k,10*k,fill=rgb('#C9553A'))
    box(d,cx-9*k,by-22*k,8*k,6*k,fill=CYAN); box(d,cx+1*k,by-22*k,8*k,6*k,fill=CYAN)
    box(d,cx-16*k,by-6*k,9*k,8*k,fill=DARK); box(d,cx+7*k,by-6*k,9*k,8*k,fill=DARK); box(d,cx+20*k,by-12*k,3*k,4*k,fill=rgb('#FFD27A'))
def goat(d,cx,by,k=1.0):
    W_=rgb('#F3EBDD'); box(d,cx-14*k,by-18*k,28*k,12*k,fill=W_)
    for dx in (-12,-5,5,10): box(d,cx+dx*k,by-6*k,4*k,6*k,fill=rgb('#B8A98E'))
    box(d,cx+10*k,by-26*k,12*k,12*k,fill=W_); box(d,cx+12*k,by-32*k,3*k,6*k,fill=rgb('#C99A5B')); box(d,cx+18*k,by-32*k,3*k,6*k,fill=rgb('#C99A5B'))
    box(d,cx+17*k,by-22*k,3*k,3*k,fill=DARK); box(d,cx+18*k,by-14*k,3*k,5*k,fill=rgb('#B8A98E'))
def door(d,i,f=0.0,content=None,hl=False,glow=False,t=0.0):
    x=DX[i]; y=DT
    box(d,x-6,y-6,DW+12,DH+6,fill=rgb('#4A2E1C'))
    box(d,x,y,DW,DH,fill=rgb('#0A0A14'))
    if content=='car': car(d,x+DW/2,y+DH-10,1.15)
    elif content=='goat': goat(d,x+DW/2,y+DH-10,1.4)
    w=DW*(1-0.88*f)
    if w>2:
        pts=[(x,y),(x+w,y+f*14),(x+w,y+DH-f*14),(x,y+DH)]
        d.polygon([(px*S,py*S) for px,py in pts],fill=rgb('#C99A5B'))
        if f<0.6:
            box(d,x+6,y+54,w-12,40,fill=None,border=rgb('#9C7340'),bw=2) if False else None
            d.rectangle([(x+7)*S,(y+60)*S,(x+w-7)*S,(y+100)*S],outline=rgb('#9C7340'),width=2*S)
            box(d,x+w-10,y+84,5,5,fill=rgb('#FFD27A'))
            if f<0.2:
                box(d,x+DW/2-13,y+14,26,26,fill=DARK,border=rgb('#FFD27A'),bw=2); T(d,str(i+1),x+DW/2,y+19,18,'press',16,CREAM,align='c')
    if glow and content is None and f<0.2 and int(t*2)%2==0: T(d,'?',x+DW/2,y+110,28,'press',22,CORAL,align='c')
    if hl:
        d.rectangle([(x-8)*S,(y-8)*S,(x+DW+8)*S,(y+DH+2)*S],outline=CORAL,width=3*S)
def stage(dd,lay,t):
    box(dd,0,0,SW,SH,fill=rgb('#14122B'))
    for k in range(0,SW,12):
        pass
    box(dd,3,3,SW-6,16,fill=rgb('#5A1F2E'))
    for sx in (3,SW-22):
        box(dd,sx,3,19,SH-6,fill=rgb('#5A1F2E'))
        for k in range(0,19,6): box(dd,sx+k,19,3,SH-24,fill=rgb('#7A2A3E'))
    box(dd,22,FLOOR,SW-44,SH-FLOOR-3,fill=rgb('#201B3F')); box(dd,22,FLOOR,SW-44,3,fill=rgb('#3F4F86'))
    for k in range(5): box(dd,22+k*58,FLOOR+3,2,SH-FLOOR-6,fill=rgb('#2B2556'))
def spot(lay,t):
    ov=Image.new('RGBA',lay.size,(0,0,0,0)); od=ImageDraw.Draw(ov)
    for k,(cx0,ph) in enumerate([(66,0),(156,2),(246,4)]):
        cx=cx0+math.sin(t*1.3+ph)*14
        od.polygon([((cx-6)*S,20*S),((cx+6)*S,20*S),((cx+44)*S,FLOOR*S),((cx-44)*S,FLOOR*S)],fill=(255,240,200,26))
    lay=Image.alpha_composite(lay.convert('RGBA'),ov).convert('RGB'); return lay
def band(lay,y,h,a=0.78):
    r=lay.crop((3*S,y*S,(SW-3)*S,(y+h)*S)); r=Image.blend(r,Image.new('RGB',r.size,(7,9,15)),a); lay.paste(r,(3*S,y*S))
def det(dd,x,t,cell=3.2,feet=352):
    b=math.sin(t*4)*1.5; sprite(dd,DET,DPAL,x,feet-24*cell+b,cell,20)
def host(dd,x,t,cell=4.2,feet=352,arm=False):
    b=math.sin(t*3.2)*1.2; sprite(dd,MAN,HOSTPAL,x,feet-14*cell+b,cell,10)
    box(dd,x+cell*9.5,feet-14*cell+cell*6+b,3*cell,2*cell,fill=SKIN if False else rgb('#F1C39B'))
    box(dd,x+cell*10.5,feet-14*cell+cell*5+b,2*cell,3*cell,fill=rgb('#CCCCCC'))   # micro
    if arm: box(dd,x-cell*3,feet-14*cell+cell*(3 if int(t*4)%2 else 4)+b,3*cell,2*cell,fill=rgb('#F1C39B'))
def confetti(dd,t,t0):
    r=random.Random(11)
    for k in range(40):
        x0=r.randint(10,SW-10); sp=r.randint(60,140); y=((t-t0)*sp+r.randint(0,200))%(SH+20)-10
        c=[CORAL,CYAN,CREAM,rgb('#FFD27A')][k%4]; box(dd,x0+math.sin(t*3+k)*6,y,5,5,fill=c)
def make_scene(draw_fn,t,head=None):
    lay=Image.new('RGB',(SW*S,SH*S),CARD); dd=ImageDraw.Draw(lay)
    stage(dd,lay,t); lay=spot(lay,t); dd=ImageDraw.Draw(lay)
    draw_fn(lay,dd)
    if head: txt_lines(dd,head,16,26,26,'grot7',22,SW-40)
    dd.rectangle([0,0,SW*S-1,3*S-1],fill=EDGE); dd.rectangle([0,(SH-3)*S,SW*S-1,SH*S-1],fill=EDGE); dd.rectangle([0,0,3*S-1,SH*S-1],fill=EDGE); dd.rectangle([(SW-3)*S,0,SW*S-1,SH*S-1],fill=EDGE)
    return lay
def frame_with(lay,label):
    img=bg(); d=ImageDraw.Draw(img); header4(d,label)
    d.rectangle([(CXo+4)*S,(CYo+4)*S,(CXo+SW+4)*S,(CYo+SH+4)*S],fill=BLACK)
    img.paste(lay,(CXo*S,CYo*S)); return img
def tag(dd,x,y,txt,col=CORAL,w=None):
    f=F('silk7',10); ww=w or tw(txt,f,1)+16; box(dd,x-ww/2,y,ww,18,fill=CARD,border=col,bw=2); T(dd,txt,x-ww/2+8,y+4,12,'silk7',10,col,sp=1)
def pill4(dd,x,y,txt,col=CORAL,fg=DARK,size=11):
    f=F('silk7',size); w=tw(txt,f,1)+22; box(dd,x-w/2,y,w,26,fill=col); T(dd,txt,x-w/2+11,y+7,14,'silk7',size,fg,sp=1)
def cover(t):
    def fn(lay,dd):
        for i in range(3): door(dd,i,glow=True,t=t+i*0.3)
        host(dd,238,t,feet=350,arm=True); det(dd,40,t,feet=352)
        T(dd,'TU CHANGES',SW/2,22,40,'anton',38,CREAM,sp=1,align='c',shadow=(3,3,BLACK)); T(dd,'DE PORTE ?',SW/2,52,40,'anton',38,CORAL,sp=1,align='c',shadow=(3,3,BLACK))
        band(lay,SH-44,40); d2=ImageDraw.Draw(lay); txt='PARADOXE DE MONTY HALL'; f=F('silk4',11); T(d2,txt,SW/2-tw(txt,f,1)/2,SH-30,14,'silk4',11,CREAM,sp=1)
    return frame_with(make_scene(fn,t),'ÉNIGME DU JOUR')
HEAD={'s1':[('Jeu télévisé : ',CREAM),('3 portes',CORAL)],'s2':[('1 voiture',CORAL),(' et ',CREAM),('2 chèvres',CORAL)],'s3':[('Tu choisis la ',CREAM),('porte 1',CORAL)],
 's4':[('Le présentateur ouvre la ',CREAM),('porte 3',CORAL)],'s5':[('Garder',CORAL),(' ou ',CREAM),('changer ?',CORAL)]}
def story(key,t,tl,T_):
    lt=t-tl[0]; dur=max(0.5,tl[1]-tl[0])
    def fn(lay,dd):
        f3=0.0
        if key=='s4': f3=ease((lt-dur*0.45)/1.0)
        if key=='s5': f3=1.0
        door(dd,0,hl=key in ('s3','s4','s5'),glow=True,t=t); door(dd,1,glow=True,t=t+0.4); door(dd,2,f=f3,content='goat' if f3>0 else None,glow=True,t=t+0.8)
        if key in ('s3','s4','s5'): tag(dd,DX[0]+DW/2,84,'TON CHOIX')
        if key=='s4' and f3>0.6 and int(t*3)%2==0: tag(dd,DX[2]+DW/2,84,'BÊÊÊ !',CREAM)
        if key in ('s1','s2','s3','s4'):
            dx=lerp(236,236,0)
            host(dd,238,t,feet=350,arm=(key=='s4' and lt>dur*0.4))
            x=40 if key!='s3' else lerp(150,DX[0]+DW/2-32,ease(lt/(dur*0.8)))
            det(dd,x,t,feet=352)
        if key=='s2':
            band(lay,SH-72,68); d2=ImageDraw.Draw(lay)
            car(d2,56,SH-24,1.25); T(d2,'x1',96,SH-44,20,'press',16,CORAL)
            goat(d2,190,SH-20,1.2); goat(d2,236,SH-20,1.2); T(d2,'x2',262,SH-44,20,'press',16,CORAL)
        if key=='s5':
            band(lay,SH-92,88,0.82); d2=ImageDraw.Draw(lay)
            for i,(l1,l2,col) in enumerate([('GARDER','porte 1',CORAL),('CHANGER','porte 2',CYAN)]):
                x=8+i*152; on=int(t*2)%2==i
                box(d2,x,SH-84,144,76,fill=CARD,border=(col if on else EDGE),bw=3)
                T(d2,l1,x+72,SH-70,24,'press',16,col,align='c'); T(d2,l2,x+72,SH-38,16,'grot7',14,SOFT,align='c')
    return frame_with(make_scene(fn,t,head=HEAD[key]),'LE JEU')
def decide(n,t,ft=None):
    img=bg(); d=ImageDraw.Draw(img); header4(d,'À TOI')
    txt_lines(d,[('Écris ton choix en ',CREAM),('commentaire',CORAL),(' !',CREAM)],24,112,28,'grot7',22,312,shadow=None)
    ph=int(t*2)%2
    for i,(w,s,col) in enumerate([('GARDER','porte 1',CORAL),('CHANGER','porte 2',CYAN)]):
        x=24+i*162; bc=col if ph==i else EDGE
        box(d,x,160,150,176,fill=CARD,border=bc,bw=3,shadow=(4,4,BLACK))
        dx=x+75-DW/2
        box(d,dx-6,176,DW+12,106,fill=rgb('#4A2E1C')); w2=DW; d.polygon([(dx*S,176*S),((dx+w2)*S,176*S),((dx+w2)*S,282*S),(dx*S,282*S)],fill=rgb('#C99A5B'))
        d.rectangle([(dx+7)*S,(176+36)*S,(dx+w2-7)*S,(176+78)*S],outline=rgb('#9C7340'),width=2*S)
        T(d,str(i+1),dx+DW/2,184,18,'press',16,CREAM,align='c',shadow=(2,2,BLACK))
        T(d,w,x+75,296,22,'press',16,col,align='c'); T(d,s,x+75,318,14,'grot7',12,SOFT,align='c')
    cy=352; box(d,92,cy,176,100,fill=CARD,border=EDGE,bw=3,shadow=(4,4,BLACK))
    fr=(t%1.0) if ft is None else ft; size=70+int(14*max(0,1-fr*4))
    T(d,str(n),180,cy+(100-size)/2+2,size,'press',size,CREAM,align='c',shadow=(4,4,BLACK))
    box(d,24,464,312,12,fill=CARD,border=EDGE,bw=2)
    if n/5.0>0.02: box(d,26,466,308*n/5.0,8,fill=CORAL)
    pill4(d,180,480,'COMMENTE : GARDER OU CHANGER',CORAL,DARK,10)
    return img
HEADR={'r0':[('La réponse : ',CREAM),('CHANGER !',CORAL)],'r1':[('Au départ : ',CREAM),('1 chance sur 3',CORAL)],'r2':[('Les 2 autres : ',CREAM),('2 chances sur 3',CYAN)],
       'r3':[('Il ouvre une chèvre : le ',CREAM),('2/3',CYAN),(' passe sur la porte 2',CREAM)],'r4':[('Changer = ',CREAM),('gagner 2 fois sur 3',CORAL)]}
def answer(key,t,tl,T_):
    lt=t-tl[0]
    def fn(lay,dd):
        if key=='r0':
            f2=ease(lt/0.9); f1=ease((lt-1.2)/0.9)
            door(dd,0,f=f1,content='goat' if f1>0 else None); door(dd,1,f=f2,content='car' if f2>0 else None,hl=f2>0.9); door(dd,2,f=1.0,content='goat')
            if f2>0.6: confetti(dd,t,tl[0]+0.5)
            if f2>0.9: tag(dd,DX[1]+DW/2,84,'GAGNÉ !',CYAN)
            det(dd,40,t,feet=352); host(dd,238,t,feet=350,arm=True)
        elif key in ('r1','r2','r3'):
            f3=ease(lt/0.8) if key=='r3' else 0
            door(dd,0,hl=True); door(dd,1); door(dd,2,f=f3,content='goat' if f3>0 else None)
            if key=='r1':
                T(dd,'1/3',DX[0]+DW/2,FLOOR+26,44,'press',32,CORAL,align='c',shadow=(3,3,BLACK)); T(dd,'ta porte',DX[0]+DW/2,FLOOR+78,16,'grot7',13,SOFT,align='c')
            if key=='r2':
                bx0,bx1=DX[1]-6,DX[2]+DW+6; box(dd,bx0,FLOOR+10,bx1-bx0,4,fill=CYAN); box(dd,bx0,FLOOR+4,4,10,fill=CYAN); box(dd,bx1-4,FLOOR+4,4,10,fill=CYAN)
                T(dd,'2/3',(bx0+bx1)/2,FLOOR+26,44,'press',32,CYAN,align='c',shadow=(3,3,BLACK)); T(dd,'les deux autres portes',(bx0+bx1)/2,FLOOR+78,16,'grot7',13,SOFT,align='c')
            if key=='r3':
                p=ease((lt-0.8)/1.2); x=lerp((DX[1]+DX[2]+DW)/2,DX[1]+DW/2,p)
                T(dd,'2/3',x,FLOOR+26,34,'press',24,CYAN,align='c',shadow=(3,3,BLACK)); T(dd,'porte 2',DX[1]+DW/2,FLOOR+78,16,'grot7',13,SOFT,align='c')
                T(dd,'1/3',DX[0]+DW/2,FLOOR+26,34,'press',24,CORAL,align='c',shadow=(3,3,BLACK))
        else:
            cases=[('VOITURE PORTE 1','CHANGER : PERDU',CORAL,0),('VOITURE PORTE 2','CHANGER : GAGNÉ',CYAN,1),('VOITURE PORTE 3','CHANGER : GAGNÉ',CYAN,2)]
            for k,(a,b,col,idx) in enumerate(cases):
                if lt<k*0.5-0.01: continue
                y=88+k*84; box(dd,16,y,SW-32,76,fill=CARD,border=col,bw=3)
                for j in range(3):
                    bxx=30+j*30; box(dd,bxx,y+14,24,40,fill=rgb('#4A2E1C')); box(dd,bxx+2,y+16,20,36,fill=(CORAL if j==idx else rgb('#0A0A14')))
                    T(dd,str(j+1),bxx+12,y+58,12,'press',8,CREAM,align='c')
                T(dd,a,120,y+16,14,'silk4',10,GREY,sp=1); T(dd,b,120,y+40,16,'press',10,col)
            if lt>1.6:
                pill4(dd,SW/2,SH-34,'CHANGER : 2 VICTOIRES SUR 3',CYAN,DARK,11)
    return frame_with(make_scene(fn,t,head=HEADR[key] if key!='r4' else HEADR[key]),'LA RÉPONSE')
def end(level,t):
    img=bg(); d=ImageDraw.Draw(img); header4(d,'ET TOI ?')
    txt_lines(d,[('Tu t\'es trompé ? ',CREAM),('Normal !',CORAL)],24,112,30,'grot7',24,312,shadow=None)
    sprite(d,DET,DPAL,56,170,6.0,20)
    T(d,'π',34,200,18,'press_greek',16,CORAL); T(d,'Σ',36,290,16,'press_greek',14,CYAN); T(d,'?',190,180,20,'press',18,CORAL)
    sprite(d,MAN,HOSTPAL,210,230,5.0,10)
    if level>=1: pill4(d,180,350,'PARTAGE LA VIDÉO À UN AMI',CREAM,DARK,12)
    if level>=2:
        pulse=int(t*3)%2==0; pill4(d,180,392,"ABONNE-TOI POUR LA SUITE",CORAL,DARK,12)
    if level>=3:
        T(d,'DEMAIN',24,470,14,'silk4',12,GREY,sp=1); T(d,'#005 >>',336,470,14,'press',14,CREAM,align='r')
    return img
