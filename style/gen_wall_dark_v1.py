exec(open('make3.py').read().split('def V1():')[0])
FD_FONT='/usr/share/fonts/opentype/inter/InterDisplay-Bold.otf'
def spray(a,r,mask,color,op,drips=10):
    ms=np.asarray(mask,np.float32)/255
    over=np.asarray(mask.filter(ImageFilter.GaussianBlur(10)),np.float32)/255
    speck=(r.random((H,W))<over*0.18).astype(np.float32)
    grain=0.82+0.18*np.clip(bn(r,3,0.8),-1,1)   # fine spray grain, no blotches
    paint=np.clip(ms*0.95+over*0.15+speck*0.4,0,1)*grain
    dd=Image.new('L',(W,H),0);dr=ImageDraw.Draw(dd)
    ys,xs=np.where(ms>0.5)
    for _ in range(drips):
        k=r.integers(0,len(ys));px,py=xs[k],ys[k]
        if ms[min(H-1,py+6),px]<0.5:
            ln=r.integers(30,200);w=int(r.integers(2,5));dr.line([(px,py),(px,py+ln)],fill=220,width=w);dr.ellipse([px-w,py+ln-w,px+w,py+ln+w],fill=220)
    paint=np.maximum(paint,np.asarray(dd,np.float32)/255*0.8)
    return a*(1-paint[...,None]*op)+np.array(color,np.float32)*paint[...,None]*op
def logo_stencil(a,r,x,y,size,op=.2):
    F=ImageFont.truetype(FD_FONT,size)
    full=Image.new('L',(W,H),0);ImageDraw.Draw(full).text((x,y),'FD',font=F,fill=255)
    bb=full.getbbox(); mid=(bb[1]+bb[3])//2
    off=int(size*0.09)
    top=Image.new('L',(W,H),0);top.paste(full.crop((0,0,W,mid)),(off,0))
    bot=Image.new('L',(W,H),0);bot.paste(full.crop((0,mid,W,H)),(0,mid))
    letters=ImageChops.lighter(top,bot)
    th=max(6,int(size*0.04))
    pad=int(size*0.08)
    bar=Image.new('L',(W,H),0);ImageDraw.Draw(bar).rectangle([bb[0]-pad,mid-th//2,bb[2]+off+pad,mid+th//2],fill=255)
    letters=ImageChops.subtract(letters,bar.filter(ImageFilter.MaxFilter(5)))  # small gap like the logo
    a=spray(a,r,letters,(200,204,212),op,10)
    a=spray(a,r,bar,(198,244,50),min(1,op*1.6),4)
    return a
def V3():
    r=rng_(53); a=base_photo('pexels-5622897.jpg',110,contrast=1.2)
    c=Image.fromarray(np.clip(a,0,255).astype(np.uint8))
    c=poster(r,c,(-50,-40,520,380),(35,70,245),multi(halftone((198,244,50),16,seed=4)),torn='rb',holes=2)
    c=poster(r,c,(-60,1150,330,1420),(214,208,194),multi(halftone((30,30,30),14,seed=6),greek((40,40,40),2,24)),torn='tl',holes=2)
    a=age(c,r,0.25,0.35)
    a=logo_stencil(a,r,640,860,270,op=.11)
    finish(a,.3,name='wall_p3.png')
V3()
