import build14 as b, sys
from PIL import Image
order=[k for _,k in b.TL]
names=sys.argv[1].split(',') if len(sys.argv)>1 else order
ims=[]
for k in names:
    i=order.index(k); t0=b.TL[i][0]; t1=b.TL[i+1][0] if i+1<len(b.TL) else b.TOTAL
    t=t0+min(0.9,(t1-t0)*0.7); im=b.frame(t).convert('RGB').resize((270,480)); ims.append((k,im))
cols=6; rows=(len(ims)+cols-1)//cols
sh=Image.new('RGB',(cols*270,rows*480),(0,0,0))
from PIL import ImageDraw
for n,(k,im) in enumerate(ims):
    sh.paste(im,((n%cols)*270,(n//cols)*480)); ImageDraw.Draw(sh).text(((n%cols)*270+4,(n//cols)*480+4),k,fill=(255,255,0))
sh.save(sys.argv[2] if len(sys.argv)>2 else 'sheet14.png'); print(sh.size)
