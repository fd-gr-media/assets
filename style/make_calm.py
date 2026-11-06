exec(open('make4.py').read().split('def V3():')[0])
def calm():
    r=rng_(53); a=base_photo('pexels-5622897.jpg',110,contrast=1.2)
    c=Image.fromarray(np.clip(a,0,255).astype(np.uint8))
    a=age(c,r,0.25,0.35)
    a=logo_stencil(a,r,700,1015,200,op=.09)
    finish(a,.3,name='wall_calm.png')
calm()
