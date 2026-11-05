exec(open('gen2.py').read())
from PIL import ImageOps
def base_photo(fn,target=105,gamma=1.0,contrast=1.25,flip=False):
    im=Image.open(fn).convert('RGB')
    if flip: im=ImageOps.mirror(im)
    im=ImageOps.fit(im,(W,H),Image.LANCZOS)
    a=np.asarray(im,np.float32)
    g=a.mean(-1)
    g=(g-g.mean())*contrast+target
    g=np.clip(g,0,255)
    return np.stack([g*.97,g*.99,g*1.04],-1)
def stencil(a,r,x,y,size,op=.30):
    F=ImageFont.truetype(FX,size)
    m=Image.new('L',(W,H),0);d=ImageDraw.Draw(m);d.text((x,y),'FD',font=F,fill=255)
    bb=m.getbbox(); d.rectangle([bb[0],int(bb[1]+(bb[3]-bb[1])*0.47),bb[2],int(bb[1]+(bb[3]-bb[1])*0.51)],fill=0)
    ms=np.asarray(m,np.float32)/255
    over=np.asarray(m.filter(ImageFilter.GaussianBlur(12)),np.float32)/255
    speck=(r.random((H,W))<over*0.22).astype(np.float32)
    paint=np.clip(ms*0.95+over*0.2+speck*0.5,0,1)*(0.75+0.25*np.clip(bn(r,20,4),-1,1))
    dd=Image.new('L',(W,H),0);dr=ImageDraw.Draw(dd)
    ys,xs=np.where(ms>0.5)
    for _ in range(16):
        k=r.integers(0,len(ys));px,py=xs[k],ys[k]
        if ms[min(H-1,py+6),px]<0.5:
            ln=r.integers(40,240);w=int(r.integers(3,7));dr.line([(px,py),(px,py+ln)],fill=230,width=w);dr.ellipse([px-w,py+ln-w,px+w,py+ln+w],fill=230)
    paint=np.maximum(paint,np.asarray(dd,np.float32)/255*0.85)
    lime=np.array([198,244,50],np.float32)
    return a*(1-paint[...,None]*op)+lime*paint[...,None]*op
def V1():  # dark cracked concrete + own torn posters
    r=rng_(51); a=base_photo('pexels-3122779.jpg',115,contrast=1.4)
    c=Image.fromarray(np.clip(a,0,255).astype(np.uint8))
    c=poster(r,c,(-40,-40,470,430),(214,208,194),multi(halftone((30,30,30),16,seed=3),greek((40,40,40),8,26)),torn='rb',holes=1)
    c=poster(r,c,(690,-40,1120,470),(35,70,245),txt('→',300,(198,244,50)),torn='lb',holes=1)
    c=poster(r,c,(-60,930,420,1400),(198,244,50),txt('FD',300,(15,17,21)),torn='tr',holes=1)
    c=poster(r,c,(640,960,1130,1400),(214,208,194),greek((40,40,40),5),torn='tl',holes=2)
    a=age(c,r,0.26,0.3); finish(a,.3,name='wall_p1.png')
def V2():  # concrete blocks with drip stains + lime stencil
    r=rng_(52); a=base_photo('pexels-8746913.jpg',120,contrast=1.3)
    a=a*0.24
    a=stencil(a,r,330,720,560,op=.32)
    finish(a,.3,name='wall_p2.png')
def V3():  # rusty grunge wall + posters + small stencil
    r=rng_(53); a=base_photo('pexels-5622897.jpg',110,contrast=1.2)
    c=Image.fromarray(np.clip(a,0,255).astype(np.uint8))
    c=poster(r,c,(-50,-40,520,380),(35,70,245),multi(halftone((198,244,50),16,seed=4)),torn='rb',holes=2)
    c=poster(r,c,(700,980,1130,1400),(214,208,194),multi(halftone((30,30,30),14,seed=6),greek((40,40,40),2,24)),torn='tl',holes=2)
    a=age(c,r,0.25,0.35)
    a=stencil(a,r,640,500,300,op=.26)
    finish(a,.3,name='wall_p3.png')
V1();V2();V3()
