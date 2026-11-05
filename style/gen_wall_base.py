import numpy as np, sys
from PIL import Image, ImageFilter, ImageDraw, ImageFont, ImageChops
W,H=1080,1350
FB='/usr/share/fonts/opentype/inter/InterDisplay-Bold.otf'
FX='/usr/share/fonts/opentype/inter/Inter-ExtraBold.otf'
def rng_(s): return np.random.default_rng(s)
def bn(r,scale,sig,h=H,w=W):
    a=r.random((h//scale+2,w//scale+2)).astype(np.float32)
    im=Image.fromarray((a*255).astype(np.uint8)).resize((w,h),Image.BICUBIC)
    if sig: im=im.filter(ImageFilter.GaussianBlur(sig))
    x=np.asarray(im,np.float32)/255; return (x-x.mean())/(x.std()+1e-6)
def concrete(r,base=34,amp=10):
    n=0.6*bn(r,180,35)+0.5*bn(r,40,8)+0.35*bn(r,8,1.5)+0.45*bn(r,1,0)
    L=base+amp*n+amp*0.7*np.clip(bn(r,300,60),-1.3,2)
    # grime streaks from top
    s=bn(r,1,0,1,W); s=np.asarray(Image.fromarray(((s-s.min())/(np.ptp(s))*255).astype(np.uint8)).resize((W,1)).filter(ImageFilter.GaussianBlur(2)),np.float32)/255
    s=np.clip(s-0.5,0,1)*2
    fall=(np.linspace(1,0,H)**1.5)[:,None]
    L-=amp*2.0*s*fall*(0.6+0.4*bn(r,60,10).clip(-1,1))
    # cracks
    img=Image.fromarray(np.zeros((H,W),np.uint8));d=ImageDraw.Draw(img)
    for _ in range(5):
        x,y=r.integers(0,W),r.integers(0,H);ang=r.random()*6.28
        pts=[(x,y)]
        for k in range(60):
            ang+=r.normal(0,.35);x+=np.cos(ang)*8;y+=np.sin(ang)*8;pts.append((x,y))
        d.line(pts,fill=255,width=2)
    cr=np.asarray(img.filter(ImageFilter.GaussianBlur(.7)),np.float32)/255
    L-=amp*2.5*cr
    # pores
    pm=(r.random((H,W))>0.9975).astype(np.float32)
    pm=np.asarray(Image.fromarray((pm*255).astype(np.uint8)).filter(ImageFilter.MaxFilter(3)).filter(ImageFilter.GaussianBlur(.8)),np.float32)/255
    L-=amp*2*pm
    return np.stack([L*.97,L*.99,L*1.04],-1)
def torn_mask(r,box,torn_sides,holes=2):
    x0,y0,x1,y1=box; w,h=x1-x0,y1-y0
    def edge(n,amp): 
        e=np.cumsum(r.normal(0,amp,n)); e-=np.linspace(e[0],e[-1],n); return e+r.normal(0,amp*.6,n)
    pts=[]
    N=60
    # top
    for i in range(N+1):
        t=i/N; x=x0+t*w; y=y0+(edge(1,0)[0] if False else 0)
        pts.append([x,y])
    pts=[]
    tops=edge(N+1,4) if 't' in torn_sides else np.zeros(N+1)
    bots=edge(N+1,4) if 'b' in torn_sides else np.zeros(N+1)
    lefs=edge(N+1,4) if 'l' in torn_sides else np.zeros(N+1)
    rigs=edge(N+1,4) if 'r' in torn_sides else np.zeros(N+1)
    big=lambda s: (bn(r,30,6,1,N+1)[0]*28 if s else np.zeros(N+1))
    tops+=big('t' in torn_sides);bots+=big('b' in torn_sides);lefs+=big('l' in torn_sides);rigs+=big('r' in torn_sides)
    for i in range(N+1): pts.append((x0+i/N*w, y0+tops[i]))
    for i in range(N+1): pts.append((x1+rigs[i], y0+i/N*h))
    for i in range(N,-1,-1): pts.append((x0+i/N*w, y1+bots[i]))
    for i in range(N,-1,-1): pts.append((x0+lefs[i], y0+i/N*h))
    m=Image.new('L',(W,H),0);d=ImageDraw.Draw(m);d.polygon(pts,fill=255)
    for _ in range(holes):
        cx,cy=r.integers(x0,x1),r.integers(y0,y1);rad=r.integers(30,110)
        hp=[(cx+np.cos(a)*rad*(0.6+0.5*r.random()),cy+np.sin(a)*rad*(0.6+0.5*r.random())) for a in np.linspace(0,6.28,24)]
        d.polygon(hp,fill=0)
    return m
def poster(r,canvas,box,color,content,torn='tblr',holes=2,alpha=1.0):
    m=torn_mask(r,box,torn,holes)
    core=m.filter(ImageFilter.MaxFilter(5))   # white paper fiber rim
    # paper layer
    paper=Image.new('RGB',(W,H),color)
    pn=bn(r,2,0.6)*3.5+bn(r,70,14)*6
    pa=np.asarray(paper,np.float32)+pn[...,None]
    paper=Image.fromarray(np.clip(pa,0,255).astype(np.uint8))
    content(paper,box)
    # shadow
    shf=Image.new('L',(W,H),0);shf.paste(core,(5,7))
    sh=np.asarray(shf.filter(ImageFilter.GaussianBlur(5)),np.float32)/255*(1-np.asarray(core,np.float32)/255)
    cv=np.asarray(canvas,np.float32)
    cv*= (1-0.5*sh[...,None])
    # creases
    cd=Image.new('L',(W,H),0);dc=ImageDraw.Draw(cd)
    x0,y0,x1,y1=box
    for _ in range(3):
        if r.random()<.5: yy=r.integers(y0,y1);dc.line([(x0,yy),(x1,yy+r.integers(-30,30))],fill=255,width=2)
        else: xx=r.integers(x0,x1);dc.line([(xx,y0),(xx+r.integers(-30,30),y1)],fill=255,width=2)
    crease=np.asarray(cd.filter(ImageFilter.GaussianBlur(1.2)),np.float32)/255
    rim=np.asarray(core,np.float32)/255
    cv=cv*(1-rim[...,None]*alpha)+np.array([200,196,186])*rim[...,None]*alpha
    mm=np.asarray(m,np.float32)[...,None]/255*alpha
    pp=np.asarray(paper,np.float32)*(1-0.18*crease[...,None])
    cv=cv*(1-mm)+pp*mm
    return Image.fromarray(np.clip(cv,0,255).astype(np.uint8))
def txt(s,size,fill,rot=0,font=FX):
    def f(img,box):
        d=ImageDraw.Draw(img);F=ImageFont.truetype(font,size)
        x0,y0,x1,y1=box
        layer=Image.new('RGBA',(W,H),(0,0,0,0));dl=ImageDraw.Draw(layer)
        dl.text((x0+10,y0-size*0.15),s,font=F,fill=fill)
        if rot: layer=layer.rotate(rot,center=(x0,y0))
        img.paste(layer,(0,0),layer)
    return f
def halftone(color,step=14,mode='chart',seed=1):
    def f(img,box):
        r=rng_(seed);d=ImageDraw.Draw(img);x0,y0,x1,y1=box
        # chart line values
        xs=np.arange(x0,x1,step); vals=np.cumsum(r.normal(0,1,len(xs))); vals=(vals-vals.min())/(np.ptp(vals)+1e-6)
        for i,x in enumerate(xs):
            top=y1-(y1-y0)*(0.15+0.7*vals[i])
            for y in range(int(top),y1,step):
                k=(y-top)/(y1-top+1); rad=step*0.45*(1-0.8*k)
                d.ellipse([x-rad,y-rad,x+rad,y+rad],fill=color)
    return f
def multi(*fs):
    def f(img,box):
        for g in fs: g(img,box)
    return f
def ticker(color,seed=2):
    def f(img,box):
        r=rng_(seed);d=ImageDraw.Draw(img);x0,y0,x1,y1=box;F=ImageFont.truetype(FB,30)
        names=['ΤΡΑΠ','ΕΝΕΡ','FX','BTC','EUR','ΓΔ','OPAP','DEI','10Y','ATHEX']
        y=y0+10
        while y<y1:
            x=x0+10
            while x<x1:
                s=f"{r.choice(names)} {r.normal(0,2):+.2f}%"
                d.text((x,y),s,font=F,fill=color);x+=260
            y+=44
    return f
def age(img,r,dark,desat):
    a=np.asarray(img,np.float32)
    g=a.mean(-1,keepdims=True); a=a*(1-desat)+g*desat
    grime=np.clip(0.88+0.12*bn(r,120,25)+0.06*bn(r,6,1),0.5,1.1)
    a*=grime[...,None]
    return a*dark
def finish(a,vig=.35,name='x.png'):
    yy,xx=np.mgrid[:H,:W]
    v=((xx-W/2)/(W/2))**2+((yy-H/2)/(H/2))**2
    a=a*(1-vig*np.clip(v,0,1.6)/1.6)[...,None]
    Image.fromarray(np.clip(a,0,255).astype(np.uint8)).save(name)
    print(name,round(float(a.mean()),1))
def greek(color,seed=2,lh=22):
    def f(img,box):
        r=rng_(seed);d=ImageDraw.Draw(img);x0,y0,x1,y1=box
        cols=max(1,(x1-x0)//230)
        for c in range(cols):
            cx=x0+15+c*230
            y=y0+12
            while y<y1:
                if r.random()<0.12: y+=lh;continue
                w=int(200*(0.5+0.5*r.random()))
                d.rectangle([cx,y,cx+w,y+lh*0.42],fill=color);y+=lh
    return f
