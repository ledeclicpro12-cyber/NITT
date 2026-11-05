import sys,importlib
from PIL import Image,ImageDraw
n=sys.argv[1]; mode=sys.argv[2] if len(sys.argv)>2 else 'mid'
b=importlib.import_module('build_e'+n)
TL=b.TL; items=[]
for i,(t0,k) in enumerate(TL):
    t1=TL[i+1][0] if i+1<len(TL) else b.TOTAL
    if k=='cover': continue
    ts=[t0+(t1-t0)*0.5] if mode=='mid' else [t0+0.15,t1-0.12]
    for t in ts: items.append((k,t,b.frame(t)))
cols=int(sys.argv[3]) if len(sys.argv)>3 else 6
W,H=300,533
rows=(len(items)+cols-1)//cols
sh=Image.new('RGB',(cols*W,rows*H),(0,0,0))
for j,(k,t,im) in enumerate(items):
    im=im.convert('RGB').resize((W,H)); d=ImageDraw.Draw(im); d.text((6,H-14),f'{k} {t:.1f}s',fill=(255,255,0))
    sh.paste(im,((j%cols)*W,(j//cols)*H))
out=f'/tmp/sheet_{n}_{mode}.png'; sh.save(out); print(out,len(items))
