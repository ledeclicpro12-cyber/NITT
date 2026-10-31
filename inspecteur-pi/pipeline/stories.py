from render14 import *
B.NUM='MINI-ÉNIGME'
PINK=dict(PRI); PINK.update({'T':'#FF7AB6','P':'#D9548F'})
def runs_txt(lay,dd,runs,y=112,size=22):
    pass
def mk(fn,head,label,out,foot=None,t=0.0):
    def f(lay,dd):
        fn(lay,dd)
        if foot:
            B.band(lay,SH-44,40); d2=ImageDraw.Draw(lay); f_=F('silk4',11); T(d2,foot,SW/2-tw(foot,f_,1)/2,SH-30,14,'silk4',11,CREAM,sp=1)
    lay=B.make_scene(f,t,head=head)
    B.frame_with(lay,label).save(out)
def kids(lay,dd):
    for i in range(4): pri(dd,50+i*52,GY,0.3,k=4.2,ph=i,still=True)
    pri(dd,50+4*52+6,GY,0.3,k=4.2,pal=PINK,still=True)
    T(dd,'?',SW/2,150,60,'press',52,GOLD,align='c',shadow=(4,4,BLACK))
def kids_a(lay,dd):
    for i in range(4): pri(dd,50+i*52,GY,0.3,k=4.2,ph=i,still=True)
    pri(dd,50+4*52+6,GY,0.3,k=4.2,pal=PINK,still=True)
    T(dd,'5',SW/2,120,100,'press',92,GOLD,align='c',shadow=(5,5,BLACK))
def steps(lay,dd,ans):
    for i in range(6):
        x=24+i*40; y=GY-16-(i%2)*22
        box(dd,x,y,22,12,fill=STEEL); box(dd,x+6,y-9,10,8,fill=STEEL)
    insp(dd,SW-52,GY,0.3,k=3.8)
    if ans: T(dd,'LES PAS',SW/2,130,70,'press',34,GOLD,align='c',shadow=(4,4,BLACK))
    else: T(dd,'?',SW/2,130,70,'press',60,GOLD,align='c',shadow=(4,4,BLACK))
D='../stories/'
mk(kids,[('Un père a ',CREAM),('4 fils. ',CYAN),('Chaque fils a ',CREAM),('une sœur. ',CORAL),('Combien d’enfants ?',CREAM)],'LE DÉFI',D+'q1.png',foot='RÉPONSE CE SOIR À 21H')
mk(kids_a,[('Réponse : ',CREAM),('5 enfants !',GOLD)],'LA RÉPONSE',D+'a1.png',foot='LA MÊME SŒUR POUR TOUS')
mk(lambda l,d:steps(l,d,False),[('Plus j’en prends, ',CREAM),('plus j’en laisse',GOLD),(' derrière moi. ',CREAM),('Que suis-je ?',CORAL)],'LE DÉFI',D+'q2.png',foot='RÉPONSE CE SOIR À 21H')
mk(lambda l,d:steps(l,d,True),[('Réponse : ',CREAM),('les pas !',GOLD)],'LA RÉPONSE',D+'a2.png',foot='TU EN LAISSES À CHAQUE PAS')
