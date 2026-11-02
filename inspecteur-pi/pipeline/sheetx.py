import sys, importlib
from PIL import Image, ImageDraw
n=sys.argv[1]; b=importlib.import_module('build_e'+n)
order=[k for _,k in b.TL]
names=sys.argv[2].split(',') if len(sys.argv)>2 and sys.argv[2]!='all' else order
out=sys.argv[3] if len(sys.argv)>3 else 'sheet.png'
cols=int(sys.argv[4]) if len(sys.argv)>4 else 6
fr=float(sys.argv[5]) if len(sys.argv)>5 else 0.7
ims=[]
for k in names:
    i=order.index(k); t0=b.TL[i][0]; t1=b.TL[i+1][0] if i+1<len(b.TL) else b.TOTAL
    t=t0+(t1-t0)*fr if fr<=1 else t0+fr; t=min(t,t1-0.02)
    ims.append((k,b.frame(t).convert('RGB').resize((360,640))))
rows=(len(ims)+cols-1)//cols
sh=Image.new('RGB',(cols*360,rows*640))
for i,(k,im) in enumerate(ims):
    sh.paste(im,((i%cols)*360,(i//cols)*640)); ImageDraw.Draw(sh).text(((i%cols)*360+4,(i//cols)*640+4),k,fill=(255,255,0))
sh.save(out); print(sh.size)
