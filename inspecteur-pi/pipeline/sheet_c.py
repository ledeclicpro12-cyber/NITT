import sys, importlib
from PIL import Image, ImageDraw
mod=sys.argv[1]; b=importlib.import_module(mod)
order=[k for _,k in b.TL]
names=sys.argv[2].split(',') if sys.argv[2]!='all' else order
fr=[float(x) for x in (sys.argv[4].split(',') if len(sys.argv)>4 else ['0.7'])]
ims=[]
for k in names:
    i=order.index(k); t0=b.TL[i][0]; t1=b.TL[i+1][0] if i+1<len(b.TL) else b.TOTAL
    for f in fr:
        t=t0+(t1-t0)*f; ims.append((k+('@%.1f'%f if len(fr)>1 else ''),b.frame_raw(t).convert('RGB').resize((270,480))))
cols=6; rows=(len(ims)+cols-1)//cols
sh=Image.new('RGB',(cols*270,rows*480),(0,0,0))
for n,(k,im) in enumerate(ims):
    sh.paste(im,((n%cols)*270,(n//cols)*480)); ImageDraw.Draw(sh).text(((n%cols)*270+4,(n//cols)*480+4),k,fill=(255,255,0))
sh.save(sys.argv[3]); print(sh.size)
