exec(open('gen2.py').read())
from PIL import ImageOps
W,H=1080,630
LIME=np.array([198,244,50],np.float32)
def photo_hp(fn,sig=25):
    im=ImageOps.fit(Image.open(fn).convert('L'),(W,H),Image.LANCZOS)
    a=np.asarray(im,np.float32); lo=np.asarray(im.filter(ImageFilter.GaussianBlur(sig)),np.float32)
    hp=a-lo; return hp/(hp.std()+1e-6), (lo-lo.mean())/(lo.std()+1e-6)
def stencil_mask(x,y,size):
    F=ImageFont.truetype('/usr/share/fonts/opentype/inter/InterDisplay-Bold.otf',size)
    full=Image.new('L',(W,H),0);ImageDraw.Draw(full).text((x,y),'FD',font=F,fill=255)
    bb=full.getbbox(); mid=(bb[1]+bb[3])//2; off=int(size*0.09)
    top=Image.new('L',(W,H),0);top.paste(full.crop((0,0,W,mid)),(off,0))
    bot=Image.new('L',(W,H),0);bot.paste(full.crop((0,mid,W,H)),(0,mid))
    letters=ImageChops.lighter(top,bot)
    th=max(6,int(size*0.04));pad=int(size*0.08)
    bar=Image.new('L',(W,H),0);ImageDraw.Draw(bar).rectangle([bb[0]-pad,mid-th//2,bb[2]+off+pad,mid+th//2],fill=255)
    letters=ImageChops.subtract(letters,bar.filter(ImageFilter.MaxFilter(5)))
    return letters,bar
def soft(mask,r,blur=8):
    ms=np.asarray(mask,np.float32)/255
    over=np.asarray(mask.filter(ImageFilter.GaussianBlur(blur)),np.float32)/255
    g=0.8+0.2*np.clip(bn(r,3,0.8,H,W),-1,1)
    return np.clip(ms*0.95+over*0.15,0,1)*g
def L1():  # lime paint on rough wall, chipped
    r=rng_(61); hp,lo=photo_hp('pexels-5622897.jpg')
    a=LIME[None,None,:]*(1+0.045*np.clip(hp,-3,3)[...,None]+0.03*np.clip(lo,-2,2)[...,None])
    # grime toward bottom & edges
    yy,xx=np.mgrid[:H,:W]
    dirt=np.clip(0.06*bn(r,80,18,H,W)+0.08*(yy/H)**2,0,0.2)
    a*=(1-dirt[...,None])
    # chipped paint spots revealing dark wall
    chips=np.zeros((H,W),np.float32);m=Image.new('L',(W,H),0);d=ImageDraw.Draw(m)
    for _ in range(9):
        side=r.integers(0,3); cx=[r.integers(0,40),r.integers(1040,W),r.integers(0,W)][side]; cy=[r.integers(0,H),r.integers(0,H),r.integers(0,18)][side]; rad=r.integers(6,22)
        pts=[(cx+np.cos(t)*rad*(0.5+0.7*r.random()),cy+np.sin(t)*rad*(0.5+0.7*r.random())) for t in np.linspace(0,6.28,14)]
        d.polygon(pts,fill=255)
    ch=np.asarray(m.filter(ImageFilter.GaussianBlur(0.8)),np.float32)/255
    dark=np.array([38,40,44],np.float32)
    a=a*(1-ch[...,None])+dark*ch[...,None]
    letters,bar=stencil_mask(700,330,210)
    sl=soft(letters,r);sb=soft(bar,r)
    a=a*(1-sl[...,None]*0.07)+np.array([15,17,21])*sl[...,None]*0.07
    a=a*(1-sb[...,None]*0.10)+np.array([35,70,245])*sb[...,None]*0.10
    Image.fromarray(np.clip(a,0,255).astype(np.uint8)).save('lime_l1.png')
def L2():  # lime wheatpaste poster with creases, glue, torn corners
    r=rng_(62); hp,lo=photo_hp('pexels-5622897.jpg',10)
    paper=LIME[None,None,:]*(1+0.02*np.clip(bn(r,2,0.6,H,W),-3,3)[...,None]+0.035*np.clip(bn(r,90,20,H,W),-2,2)[...,None])
    # wall texture showing through (wheatpaste)
    paper*= (1+0.025*np.clip(hp,-3,3))[...,None]
    # creases
    cd=Image.new('L',(W,H),0);dc=ImageDraw.Draw(cd)
    for _ in range(4):
        if r.random()<.5: y=r.integers(40,H-40);dc.line([(0,y),(W,y+r.integers(-40,40))],fill=255,width=3)
        else: x=r.integers(60,W-60);dc.line([(x,0),(x+r.integers(-40,40),H)],fill=255,width=3)
    cr=np.asarray(cd.filter(ImageFilter.GaussianBlur(2)),np.float32)/255
    crl=np.asarray(cd.transform((W,H),Image.AFFINE,(1,0,-3,0,1,-3)).filter(ImageFilter.GaussianBlur(2)),np.float32)/255
    paper*=(1-0.07*cr[...,None]+0.05*crl[...,None])
    # glue bubbles
    for _ in range(6):
        cx,cy=r.integers(0,W),r.integers(0,H);rx,ry=r.integers(30,90),r.integers(15,40)
        yy,xx=np.ogrid[:H,:W];dd=((xx-cx)/rx)**2+((yy-cy)/ry)**2
        paper*=(1+0.04*np.clip(1-dd,0,1)*(np.sign(yy-cy)*-1))[...,None]
    # torn corner bottom-right & small tear top-left showing dark wall
    wall=np.array([30,32,36],np.float32)
    m=Image.new('L',(W,H),255);d=ImageDraw.Draw(m)
    pts=[(W,0),(W-150,0)]+[(W-150+int(t*150)+int(r.normal(0,4)),int(t*95)+int(r.normal(0,4))) for t in np.linspace(0,1,24)]
    pass
    pts2=[(0,0),(120,0)]+[(120-int(t*120)+int(r.normal(0,4)),int(t*70)+int(r.normal(0,4))) for t in np.linspace(0,1,24)]
    pass
    mk=np.asarray(m,np.float32)/255
    rim=np.asarray(m.filter(ImageFilter.MinFilter(5)),np.float32)/255
    rimz=mk-rim
    a=wall*(1-mk[...,None])+paper*mk[...,None]
    a=a*(1-rimz[...,None])+np.array([235,235,225])*rimz[...,None]*0.85+a*rimz[...,None]*0.15
    letters,bar=stencil_mask(640,300,210)
    sl=soft(letters,r);sb=soft(bar,r)
    a=a*(1-sl[...,None]*0.06)+np.array([15,17,21])*sl[...,None]*0.06
    a=a*(1-sb[...,None]*0.10)+np.array([35,70,245])*sb[...,None]*0.10
    Image.fromarray(np.clip(a,0,255).astype(np.uint8)).save('lime_l2.png')
L1();L2()
