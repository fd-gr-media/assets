exec(open('gen2.py').read())
from PIL import ImageOps
W,H=1080,1350
r=rng_(71)
im=ImageOps.fit(Image.open('pexels-5622897.jpg').convert('L'),(W,H),Image.LANCZOS)
a=np.asarray(im,np.float32); lo=np.asarray(im.filter(ImageFilter.GaussianBlur(10)),np.float32)
hp=(a-lo)/((a-lo).std()+1e-6)
g=128+10*np.clip(bn(r,2,0.6),-3,3)*0.6+9*np.clip(hp,-3,3)+10*np.clip(bn(r,120,25),-2,2)
# creases across whole poster
cd=Image.new('L',(W,H),0);dc=ImageDraw.Draw(cd)
lines=[]
for k in range(6):
    if k%2==0: y=r.integers(80,H-80);lines.append(((0,y),(W,y+r.integers(-50,50))))
    else: x=r.integers(80,W-80);lines.append(((x,0),(x+r.integers(-50,50),H)))
for p in lines:
    (x0,y0),(x1,y1)=p; pts=[]
    for t in np.linspace(0,1,40): pts.append((x0+(x1-x0)*t+r.normal(0,1.5),y0+(y1-y0)*t+r.normal(0,1.5)))
    dc.line(pts,fill=255,width=3)
cr=np.asarray(cd.filter(ImageFilter.GaussianBlur(1.6)),np.float32)/255
crl=np.asarray(cd.transform((W,H),Image.AFFINE,(1,0,-3,0,1,-3)).filter(ImageFilter.GaussianBlur(2.5)),np.float32)/255
broad=np.asarray(cd.filter(ImageFilter.GaussianBlur(18)),np.float32)/255
broad2=np.asarray(cd.transform((W,H),Image.AFFINE,(1,0,-14,0,1,-14)).filter(ImageFilter.GaussianBlur(18)),np.float32)/255
g+= -70*cr + 45*crl + 120*(broad2-broad)
# glue bubbles / wrinkles
yy,xx=np.ogrid[:H,:W]
for _ in range(9):
    cx,cy=r.integers(0,W),r.integers(0,H);rx,ry=r.integers(40,120),r.integers(15,45)
    dd=((xx-cx)/rx)**2+((yy-cy)/ry)**2
    bump=np.exp(-dd*1.5)
    dy=np.gradient(bump,axis=0)
    g+= -dy*ry*22
# dirty edges
yy2,xx2=np.mgrid[:H,:W]
edge=np.minimum.reduce([xx2,W-1-xx2,yy2,H-1-yy2]).astype(np.float32)
g-=30*np.exp(-edge/40)*(0.6+0.4*np.clip(bn(r,30,6),-1,1))
Image.fromarray(np.clip(g,0,255).astype(np.uint8)).save('wp_overlay.png')
print(g.mean())
