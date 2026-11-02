from render_x import *
B.NUM='#017'
HEADS={'s1':[('1 seul sur 100 ',GOLD),('sera libéré',CYAN)],
 's2':[('Un seul sera ',CREAM),('libéré',CYAN)],
 's3':[('Placés ',CREAM),('en cercle',GOLD)],
 's4':[('Numérotés ',CREAM),('de 1 à 100',GOLD)],
 's5':[('Le 1 ',GOLD),('élimine',RED),(' le 2',CREAM)],
 's6':[('Le 3 ',GOLD),('élimine',RED),(' le 4',CREAM)],
 's7':[('Et ainsi ',CREAM),('de suite',CORAL)],
 's8':[('On saute ',CREAM),('les éliminés',RED)],
 's9':[('Exemple : ',CREAM),('5 détenus',GOLD)],
 's10':[('Le 1 ',GOLD),('élimine',RED),(' le 2',CREAM)],
 's11':[('Le 3 ',GOLD),('élimine',RED),(' le 4',CREAM)],
 's12':[('Le 5 ',GOLD),('élimine',RED),(' le 1',CREAM)],
 's13':[('Le 3 ',GOLD),('élimine',RED),(' le 5',CREAM)],
 's14':[('Il ne reste ',CREAM),('que le 3',GOLD)],
 's15':[('Le 3 est ',CREAM),('libéré',CYAN)],
 's16':[('Maintenant',CORAL)],
 's17':[('Avec ',CREAM),('100 détenus',GOLD)],
 'q':[('Quel numéro ',CREAM),('choisir?',CORAL)],
 'r0':[('La ',CREAM),('réponse :',GOLD)],
 'r1':[('Le ',CREAM),('73',GOLD)],
 'r2':[('Voici ',CREAM),('pourquoi',CYAN)],
 'r3':[('Avec ',CREAM),('64 détenus',GOLD)],
 'r4':[('Le 1 ',GOLD),('gagne ',CREAM),('toujours',CYAN)],
 'r5':[('À chaque tour : ',CREAM),('la moitié',RED)],
 'r6':[('Le 1 ',GOLD),('reste',CYAN)],
 'r7':[('Mais ici : ',CREAM),('100',GOLD)],
 'r8':[('36 ',CORAL),('de trop',CREAM)],
 'r9':[('On en élimine ',CREAM),('36',CORAL)],
 'r10':[('Du 2 ',CREAM),('au 72',RED)],
 'r11':[('Il reste ',CREAM),('64',GOLD)],
 'r12':[('Au ',CREAM),('73',GOLD),(' de jouer',CREAM)],
 'r13':[('Le 73 devient ',CREAM),('le 1',GOLD)],
 'r14':[('Il ',CREAM),('gagne',GOLD)],
 'r15':[('Le ',CREAM),('73',GOLD)]}
STORY=('s1','s2','s3','s4','s5','s6','s7','s8','s9','s10','s11','s12','s13','s14','s15','s16','s17','q')

def halo(dd,k,n=100,col=GOLD,r=12):
    x,y=rpos(k,n)
    dd.ellipse([(x-r)*S,(y-r)*S,(x+r)*S,(y+r)*S],outline=col,width=2*S)
def pent_pos(k,R=82,c=(156,222)):
    a=-math.pi/2+(k-1)*2*math.pi/5; return c[0]+R*math.cos(a), c[1]+R*math.sin(a)
def pent(dd,state,t=0.0):
    """state(k)->'a' vivant | 'g' or | 'd' éliminé | 'c' cible"""
    for k in range(1,6):
        a=pent_pos(k); b=pent_pos(k%5+1); dd.line([(a[0]*S,a[1]*S),(b[0]*S,b[1]*S)],fill=EDGE,width=2*S)
    for k in range(1,6):
        x,y=pent_pos(k); s=state(k); r=23
        if s=='d':
            disc(dd,x,y,r,rgb('#10142A'),DIM,3); T(dd,str(k),x,y-9,18,'press',16,DIM,align='c'); xmark_(dd,x,y,r-4,4)
        else:
            col={'a':CREAM,'g':GOLD,'c':CORAL}[s]
            disc(dd,x,y,r,GOLD if s=='g' else CARD,col,3); T(dd,str(k),x,y-9,18,'press',16,DARK if s=='g' else col,align='c')
def kill_state(dead_always,killer,victim,vdead_lt,lt,base_dead=()):
    d=set(dead_always)|set(base_dead)
    def st(k):
        if k in d or (k==victim and lt>vdead_lt): return 'd'
        if k==killer: return 'g'
        if k==victim: return 'c'
        return 'a'
    return st

def scene_fn(key,t,lt,dur):
    def fn(lay,dd):
        if key=='s1':
            headgrid(dd,int(ease(lt/0.5)*100),hl=(36 if lt>0.6 else None),hlcol=GOLD)
            tagc(dd,SW/2,364,'UN SEUL SUR CENT',GOLD)
        elif key=='s2':
            exit_door(dd,176,118,100,GY-118,ease(lt/0.5),t)
            pri(dd,100+min(lt,1.2)*30,GY-abs(math.sin(t*6))*14,t,k=5.0)
            B.confetti(dd,t,t-lt); tagc(dd,SW/2,364,'LIBÉRÉ',CYAN)
        elif key=='s3':
            n=int(ease(lt/0.9)*100)
            ring(dd,lambda k:'a' if k<=n else None)
            tagc(dd,SW/2,364,'EN CERCLE',GOLD)
        elif key=='s4':
            ring(dd,lambda k:'g' if k==1 else 'a')
            for v,at_ in ((1,0.1),(25,0.3),(50,0.5),(75,0.7),(100,0.9)):
                if lt>at_:
                    x,y=rpos(v,100,R=82); f=F('silk7',10); w=tw(str(v),f,1)+14
                    box(dd,x-w/2,y-9,w,18,fill=CARD,border=(GOLD if v==1 else EDGE),bw=2); T(dd,str(v),x-w/2+7,y-5,12,'silk7',10,GOLD if v==1 else CREAM,sp=1)
            tagc(dd,SW/2,364,'NUMÉROTÉS DE 1 À 100',GOLD)
        elif key=='s5':
            def st(k):
                if k==1: return 'g'
                if k==2: return 'x' if lt>0.55 else 'c'
                return 'a'
            ring(dd,st); halo(dd,1); halo(dd,2,col=RED)
            ctext(dd,['1 ÉLIMINE','LE 2'],CREAM,18)
            tagc(dd,SW/2,364,'LE 1 ÉLIMINE LE 2',RED)
        elif key=='s6':
            def st(k):
                if k==2: return 'd'
                if k==3: return 'g'
                if k==4: return 'x' if lt>0.9 else 'c'
                return 'a'
            ring(dd,st); halo(dd,3); halo(dd,4,col=RED)
            ctext(dd,['3 ÉLIMINE','LE 4'],CREAM,18)
            tagc(dd,SW/2,364,'LE 3 ÉLIMINE LE 4',RED)
        elif key=='s7':
            nk=int(ease(lt/1.35)*50)
            def st(k):
                if k%2==0 and k<=2*nk: return 'd'
                if k==2*nk+1 and nk<50: return 'g'
                return 'a'
            ring(dd,st); ctext(dd,['ET AINSI','DE SUITE'],CREAM,18)
            tagc(dd,SW/2,364,'ON TOURNE AUTOUR DU CERCLE',CORAL)
        elif key=='s8':
            def st(k):
                if k%2==0: return 'd'
                if k==1: return 'g'
                if k==3: return 'x' if lt>0.85 else 'c'
                return 'a'
            ring(dd,st); halo(dd,1); halo(dd,3,col=RED)
            ctext(dd,['ON SAUTE','LES ÉLIMINÉS'],CREAM,16)
            tagc(dd,SW/2,364,'1 SAUTE LE 2 ET ÉLIMINE LE 3',RED)
        elif key=='s9':
            n=int(lt/0.22)+1
            pent(dd,lambda k:'a' if k<=n else 'd' if False else 'a') if n>=5 else None
            if n<5:
                for k in range(1,6):
                    if k<=n:
                        x,y=pent_pos(k); disc(dd,x,y,23,CARD,CREAM,3); T(dd,str(k),x,y-9,18,'press',16,CREAM,align='c')
            tagc(dd,SW/2,364,'EXEMPLE : 5 DÉTENUS',GOLD)
        elif key=='s10':
            pent(dd,kill_state((),1,2,0.75,lt));
            if lt<0.75: dotline(dd,pent_pos(1),pent_pos(2),RED,t,3,10)
            tagc(dd,SW/2,364,'LE 1 ÉLIMINE LE 2',RED)
        elif key=='s11':
            pent(dd,kill_state((2,),3,4,0.9,lt))
            if lt<0.9: dotline(dd,pent_pos(3),pent_pos(4),RED,t,3,10)
            tagc(dd,SW/2,364,'LE 3 ÉLIMINE LE 4',RED)
        elif key=='s12':
            pent(dd,kill_state((2,4),5,1,0.85,lt))
            if lt<0.85: dotline(dd,pent_pos(5),pent_pos(1),RED,t,3,10)
            tagc(dd,SW/2,364,'LE 5 ÉLIMINE LE 1',RED)
        elif key=='s13':
            pent(dd,kill_state((1,2,4),3,5,0.75,lt))
            if lt<0.75: dotline(dd,pent_pos(3),pent_pos(5),RED,t,3,10)
            tagc(dd,SW/2,364,'LE 3 ÉLIMINE LE 5',RED)
        elif key=='s14':
            pent(dd,lambda k:'g' if k==3 else 'd'); x,y=pent_pos(3); star(dd,x,y-50,t,6)
            tagc(dd,SW/2,364,'IL NE RESTE QUE LE 3',GOLD)
        elif key=='s15':
            pent(dd,lambda k:'g' if k==3 else 'd'); B.confetti(dd,t,t-lt)
            stamp(dd,SW/2,336,'LIBÉRÉ !',GRN,16)
            tagc(dd,SW/2,364,'LE 3 EST LIBÉRÉ',CYAN)
        elif key=='s16':
            ring(dd,lambda k:'a'); ctext(dd,['MAINTENANT'],CREAM,18)
            tagc(dd,SW/2,364,'MAINTENANT',CORAL)
        elif key=='s17':
            ring(dd,lambda k:'a'); ctext(dd,['100'],GOLD,44,y=RC[1]-38); T(dd,'DÉTENUS',RC[0],RC[1]+14,16,'silk7',11,CREAM,align='c',sp=2)
            tagc(dd,SW/2,364,'AVEC 100 DÉTENUS',GOLD)
        elif key=='q':
            g=int(t*18)%100+1
            ring(dd,lambda k:'g' if k==g else 'a'); ctext(dd,['?'],GOLD,60)
            tagc(dd,SW/2,364,'QUEL NUMÉRO CHOISIR ?',CORAL)
        # ---- réponse ----
        elif key=='r0':
            ring(dd,lambda k:'a'); ctext(dd,['LA','RÉPONSE'],GOLD,20)
            tagc(dd,SW/2,364,'LA RÉPONSE',GOLD)
        elif key=='r1':
            ring(dd,lambda k:'g' if k==73 else 'a'); halo(dd,73,col=GOLD,r=14)
            ctext(dd,['73'],GOLD,56)
            tagc(dd,SW/2,364,'LE 73',GOLD)
        elif key=='r2':
            insp(dd,90,GY,t,k=5.0); bubble(dd,150,120,150,70,['POURQUOI','?'],CYAN,14)
            tagc(dd,SW/2,364,'VOICI POURQUOI',CYAN)
        elif key=='r3':
            ring(dd,lambda k:'a',n=64,sz=6); ctext(dd,['64'],GOLD,46,y=RC[1]-38); T(dd,'DÉTENUS',RC[0],RC[1]+14,16,'silk7',11,CREAM,align='c',sp=2)
            tagc(dd,SW/2,364,'AVEC 64 DÉTENUS',GOLD)
        elif key=='r4':
            ring(dd,lambda k:'g' if k==1 else 'a',n=64,sz=6)
            if lt>0.6: star(dd,SW/2,RC[1]-30,t,7)
            ctext(dd,['LE 1','GAGNE'],CREAM,18,y=RC[1]+4)
            tagc(dd,SW/2,364,'LE 1 GAGNE TOUJOURS',GOLD)
        elif key=='r5':
            nk=int(ease((lt-0.2)/1.3)*32)
            ring(dd,lambda k:('d' if (k%2==0 and k<=2*nk) else ('g' if k==1 else 'a')),n=64,sz=6)
            ctext(dd,['LA MOITIÉ','ÉLIMINÉE'],CREAM,16)
            tagc(dd,SW/2,364,'1 SUR 2 ÉLIMINÉ',RED)
        elif key=='r6':
            ring(dd,lambda k:('d' if k%2==0 else ('g' if k==1 else 'a')),n=64,sz=6); halo(dd,1,64,GOLD,r=13)
            ctext(dd,['LE 1','RESTE'],CREAM,18)
            tagc(dd,SW/2,364,'LE 1 JOUE DE NOUVEAU',GOLD)
        elif key=='r7':
            ring(dd,lambda k:'a'); ctext(dd,['100'],GOLD,44,y=RC[1]-38); T(dd,'DÉTENUS',RC[0],RC[1]+14,16,'silk7',11,CREAM,align='c',sp=2)
            tagc(dd,SW/2,364,'ICI : 100 DÉTENUS',GOLD)
        elif key=='r8':
            nn=int(ease(lt/1.2)*36)
            ring(dd,lambda k:'c' if (k%2==0 and k<=2*nn) else 'a')
            ctext(dd,['36'],CORAL,44,y=RC[1]-38); T(dd,'DE TROP',RC[0],RC[1]+14,16,'silk7',11,CREAM,align='c',sp=2)
            tagc(dd,SW/2,364,'36 DE TROP',CORAL)
        elif key=='r9':
            ring(dd,lambda k:'c' if (k%2==0 and k<=72) else 'a')
            ctext(dd,['ON ÉLIMINE','36'],[CREAM,CORAL],18)
            tagc(dd,SW/2,364,'ON ÉLIMINE 36 DÉTENUS',CORAL)
        elif key=='r10':
            nk=int(ease(lt/1.05)*36)
            def st(k):
                if k%2==0 and k<=72:
                    return 'd' if k<2*nk else ('x' if k==2*nk else 'c')
                return 'a'
            ring(dd,st); ctext(dd,['DU 2','AU 72'],CREAM,20)
            tagc(dd,SW/2,364,'DU 2 JUSQU’AU 72',RED)
        elif key=='r11':
            ring(dd,lambda k:'d' if (k%2==0 and k<=72) else 'a')
            ctext(dd,['64'],GOLD,46,y=RC[1]-38); T(dd,'RESTENT',RC[0],RC[1]+14,16,'silk7',11,CREAM,align='c',sp=2)
            tagc(dd,SW/2,364,'IL RESTE 64 DÉTENUS',GOLD)
        elif key=='r12':
            ring(dd,lambda k:'g' if k==73 else ('d' if (k%2==0 and k<=72) else 'a')); halo(dd,73,col=GOLD,r=14)
            ctext(dd,['AU 73','DE JOUER'],GOLD,18)
            tagc(dd,SW/2,364,'C’EST AU 73 DE JOUER',GOLD)
        elif key=='r13':
            ring(dd,lambda k:'g' if k==73 else ('d' if (k%2==0 and k<=72) else 'a')); halo(dd,73,col=GOLD,r=14)
            lbl(dd,RC[0],RC[1]+34,'NOUVEAU 1',GOLD)
            ctext(dd,['73 = 1'],GOLD,26,y=RC[1]-22)
            tagc(dd,SW/2,364,'LE 73 DEVIENT LE 1',GOLD)
        elif key=='r14':
            ring(dd,lambda k:'g' if k==73 else ('d' if (k%2==0 and k<=72) else 'a')); halo(dd,73,col=GOLD,r=14)
            star(dd,SW/2,RC[1]-34,t,8); ctext(dd,['IL GAGNE'],GOLD,18,y=RC[1]+6)
            tagc(dd,SW/2,364,'IL GAGNE',GOLD)
        elif key=='r15':
            ring(dd,lambda k:'g' if k==73 else ('d' if (k%2==0 and k<=72) else 'a')); halo(dd,73,col=GOLD,r=14)
            ctext(dd,['73'],GOLD,60); B.confetti(dd,t,t-lt)
            tagc(dd,SW/2,364,'LE 73 EST LIBÉRÉ',GOLD)
    return fn
story=frame_fn(__import__('sys').modules[__name__],STORY,HEADS)
answer=story
def cover(t):
    def fn(lay,dd):
        ring(dd,lambda k:'a',sz=5); ring(dd,lambda k:'g' if k==1 else None)
        T(dd,'?',RC[0],RC[1]-36,70,'press',60,GOLD,align='c',shadow=(4,4,BLACK))
        T(dd,'LE DERNIER DEBOUT',SW/2,18,40,'anton',32,CREAM,sp=1,align='c',shadow=(3,3,BLACK)); T(dd,'QUEL NUMÉRO ?',SW/2,58,40,'anton',32,GOLD,sp=1,align='c',shadow=(3,3,BLACK))
        B.band(lay,SH-44,40); d2=ImageDraw.Draw(lay); txt="CERCLE DE 100 DÉTENUS"; f=F('silk4',11); T(d2,txt,SW/2-tw(txt,f,1)/2,SH-30,14,'silk4',11,CREAM,sp=1)
    return B.frame_with(B.make_scene(fn,t),'ÉNIGME DU JOUR')
decide=make_decide()
end=make_end('#018')
