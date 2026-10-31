#!/usr/bin/env python3
"""FD Pop-Art-Porträts (Finance-Disruptors-Comicstil).

Macht aus 1–3 Porträtfotos mit möglichst einfarbigem Hintergrund
(z. B. Team-Seiten, Pressefotos) Pop-Art-Freisteller im FD-Stil:
Posterize (Ink/Hautton dunkel/Hautton hell/Weiß), Halbton-Raster,
Ink-Konturen, Lime-Versatzschatten.

Aufruf:
  python3 fd_popart.py out_prefix bild1.png [bild2.png bild3.png]

Ausgaben:
  <prefix>_cut_1.png …      Freisteller je Person (transparent, für Stories/Videos)
  <prefix>_band.png          1080x720, alle Personen nebeneinander auf FD-Blau mit Punktraster
                             -> passt in das Feld „Bild“ (Typ punkte-foto / foto)
Danach ins Repo fd-gr-media/assets unter img/JJJJ-MM/ legen und die raw-URL nutzen.

Voraussetzung für gute Ergebnisse: Hintergrund des Fotos einfarbig und
hebt sich von der Person ab (Freistellung per Flood-Fill vom Bildrand aus).
Optionen: --tol 40 (Toleranz Hintergrund), --dark 68 --mid 112 --light 175 (Schwellen)
"""
import sys, argparse
import numpy as np
from PIL import Image, ImageFilter, ImageOps, ImageDraw
from scipy import ndimage

INK=(0x0F,0x11,0x15); BLUE=(0x23,0x46,0xF5); BLUE2=(0x3A,0x5C,0xFF); LIME=(0xC6,0xF4,0x32); WHITE=(255,255,255)
SK1=(0xB8,0x74,0x58); SK2=(0xF0,0xC2,0x9E)

def bg_mask(a, tol):
    border=np.concatenate([a[0],a[-1],a[:,0],a[:,-1]])
    ref=np.median(border,axis=0)
    d=np.sqrt(((a-ref)**2).sum(-1)); lab,_=ndimage.label(d<tol)
    b=set(np.unique(np.concatenate([lab[0],lab[-1],lab[:,0],lab[:,-1]])))-{0}
    return ~np.isin(lab,list(b))   # True = Person

def person(path, H, o):
    src=Image.open(path).convert('RGB'); s=H/src.height
    src=src.resize((max(1,int(src.width*s)),H),Image.BICUBIC)
    a=np.asarray(src).astype(float); m=bg_mask(a,o.tol)
    m=np.asarray(Image.fromarray((m*255).astype('uint8')).filter(ImageFilter.MedianFilter(7)))>127
    g=np.asarray(ImageOps.autocontrast(src.convert('L').filter(ImageFilter.GaussianBlur(1.4)),cutoff=1)).astype(float)
    h,w=g.shape; out=np.zeros((h,w,3),'uint8')
    lv=np.digitize(g,[o.dark,o.mid,o.light])
    for i,c in enumerate([INK,SK1,SK2,WHITE]): out[lv==i]=c
    yy,xx=np.mgrid[0:h,0:w]; st=8; cx=(xx%st)-st/2; cy=(yy%st)-st/2; rr=cx**2+cy**2
    out[(lv==1)&(rr<(np.clip((o.mid-g)/58,0,1)*st*0.5)**2)]=INK
    out[(lv==2)&(rr<(np.clip((o.light-g)/70,0,1)*st*0.45)**2)]=SK1
    out[(lv==3)&(rr<(np.clip((215-g)/45,0,1)*st*0.4)**2)]=SK2
    L=src.convert('L'); g1=np.asarray(L.filter(ImageFilter.GaussianBlur(1.0))).astype(float); g2=np.asarray(L.filter(ImageFilter.GaussianBlur(3.0))).astype(float)
    out[((g2-g1)>9)&m]=INK
    out[m ^ ndimage.binary_erosion(m,iterations=6)]=INK
    alpha=Image.fromarray((m*255).astype('uint8'))
    im=Image.fromarray(np.dstack([out,np.asarray(alpha)]),'RGBA')
    sh=Image.new('RGBA',im.size,LIME+(255,)); sh.putalpha(alpha)
    c=Image.new('RGBA',(im.width+20,im.height+12),(0,0,0,0)); c.paste(sh,(18,10),sh); c.alpha_composite(im,(0,0))
    return c

def dotted(W,H):
    im=Image.new('RGBA',(W,H),BLUE+(255,)); d=ImageDraw.Draw(im)
    for y in range(0,H,22):
        for x in range((y//22)%2*11,W,22): d.ellipse((x-3,y-3,x+3,y+3),fill=BLUE2)
    return im

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('prefix'); ap.add_argument('images',nargs='+')
    ap.add_argument('--tol',type=float,default=40); ap.add_argument('--dark',type=float,default=68)
    ap.add_argument('--mid',type=float,default=112); ap.add_argument('--light',type=float,default=175)
    o=ap.parse_args(); n=len(o.images[:3])
    W,H=1080,720; band=dotted(W,H); slot=W//n
    for i,p in enumerate(o.images[:3]):
        c=person(p,int(H*0.86),o); c.save(f'{o.prefix}_cut_{i+1}.png')
        if c.width>slot+120: c=c.crop(((c.width-slot-120)//2,0,(c.width+slot+120)//2,c.height))
        band.alpha_composite(c,(max(0,min(W-c.width,i*slot+slot//2-c.width//2)),H-c.height))
    band.convert('RGB').save(f'{o.prefix}_band.png'); print('ok',o.prefix)

if __name__=='__main__': main()
