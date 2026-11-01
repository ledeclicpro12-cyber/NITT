import sys, importlib
from PIL import Image, ImageDraw
n=sys.argv[1]; b=importlib.import_module('build_e'+n)
order=[k for _,k in b.TL]
names=sys.argv[2].split(',') if len(sys.argv)>2 and sys.argv[2]!='all' else order
fr=float(sys.argv[4]) if len(sys.argv)>4 else 0.8
ims=[]
for k in names:
    i=order.index(k); t0=b.TL[i][0]; t1=b.TL[i+1][0] if i+1<len(b.TL) else b.TOTAL
    t=t0+min(fr,(t1-t0)*0.9); im=b.frame(t).convert('RGB').resize((270,480)); ims.append((k,im))
cols=6; rows=(len(ims)+cols-1)//cols
sh=Image.new('RGB',(cols*270,rows*480),(0,0,0))
for j,(k,im) in enumerate(ims):
    sh.paste(im,((j%cols)*270,(j//cols)*480)); ImageDraw.Draw(sh).text(((j%cols)*270+4,(j//cols)*480+4),k,fill=(255,255,0))
sh.save(sys.argv[3] if len(sys.argv)>3 else 'sheet.png'); print(sh.size)
