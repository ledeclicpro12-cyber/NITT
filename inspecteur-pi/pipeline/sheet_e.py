import sys,importlib
n=sys.argv[1]; b=importlib.import_module('build_e'+n)
from PIL import Image, ImageDraw
order=[k for _,k in b.TL]
names=sys.argv[2].split(',') if sys.argv[2]!='all' else order
fr=[float(x) for x in sys.argv[4].split(',')] if len(sys.argv)>4 else [0.7]
ims=[]
for k in names:
    i=order.index(k); t0=b.TL[i][0]; t1=b.TL[i+1][0] if i+1<len(b.TL) else b.TOTAL
    for f in fr:
        t=t0+(t1-t0)*f if f<=1 else t0+f
        ims.append((k,b.frame(min(t,t1-0.02)).convert('RGB').resize((270,480))))
cols=6; rows=(len(ims)+cols-1)//cols
sh=Image.new('RGB',(cols*270,rows*480))
for n_,(k,im) in enumerate(ims):
    sh.paste(im,((n_%cols)*270,(n_//cols)*480)); ImageDraw.Draw(sh).text(((n_%cols)*270+4,(n_//cols)*480+4),k,fill=(255,255,0))
sh.save(sys.argv[3]); print(sh.size)
