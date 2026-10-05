from PIL import Image, ImageDraw
from pathlib import Path
import json, math

HERE=Path(__file__).parent
OUT=HERE/'assets'; OUT.mkdir(exist_ok=True)
S=3; N=768
INK='#302b3c'; FUR='#d9ad7f'; LIGHT='#efcc9f'
def new():
    im=Image.new('RGBA',(N*S,N*S)); return im,ImageDraw.Draw(im)
def ellipse(d,box,fill,stroke=INK,w=6): d.ellipse(tuple(int(x*S) for x in box),fill=fill,outline=stroke,width=w*S)
def rect(d,box,fill,rad=30,stroke=INK,w=6): d.rounded_rectangle(tuple(int(x*S) for x in box),rad*S,fill,stroke,w*S)
def line(d,pts,fill=INK,w=6): d.line([(int(x*S),int(y*S)) for x,y in pts],fill,width=w*S,joint='curve')
def arc(d,box,start,end,fill=INK,w=6): d.arc(tuple(int(x*S) for x in box),start,end,fill,width=w*S)
def save(im,name):
    im.resize((N,N),Image.Resampling.LANCZOS).save(OUT/f'{name}.png')

im,d=new()
# Fixed base: warm, bold silhouette with separated paws and muzzle.
ellipse(d,(217,451,551,731),FUR)
ellipse(d,(150,511,292,698),FUR); ellipse(d,(477,511,619,698),FUR)
ellipse(d,(190,129,332,284),FUR); ellipse(d,(436,129,578,284),FUR)
ellipse(d,(221,158,305,242),'#b98666',None,0); ellipse(d,(463,158,547,242),'#b98666',None,0)
ellipse(d,(176,195,592,572),FUR)
ellipse(d,(285,380,484,528),LIGHT,None,0)
ellipse(d,(344,380,424,427),INK,None,0)
line(d,[(384,421),(384,454)],w=5)
arc(d,(339,427,384,472),0,170,w=5);arc(d,(384,427,429,472),10,180,w=5)
ellipse(d,(223,402,274,424),'#d59784',None,0);ellipse(d,(494,402,545,424),'#d59784',None,0)
save(im,'base')

for name,color in [('hoodie-coral','#e58878'),('hoodie-mint','#8cc5b3')]:
    im,d=new(); rect(d,(244,531,524,730),color,45)
    ellipse(d,(286,506,482,588),color);line(d,[(335,555),(335,623)],'#faf0dc',5);line(d,[(433,555),(433,623)],'#faf0dc',5)
    rect(d,(305,652,465,705),color,18,w=4);line(d,[(324,654),(310,679)],w=4);line(d,[(446,654),(460,679)],w=4)
    save(im,name)
im,d=new();ellipse(d,(270,337,294,375),INK,None,0);ellipse(d,(474,337,498,375),INK,None,0)
ellipse(d,(278,344,284,354),'#fff8eb',None,0);ellipse(d,(482,344,488,354),'#fff8eb',None,0);save(im,'eyes-open')
im,d=new();arc(d,(260,333,308,376),190,345,w=8);arc(d,(461,333,509,376),190,345,w=8);save(im,'eyes-happy')
im,d=new();ellipse(d,(252,296,516,391),'#7297bb');rect(d,(274,277,494,346),'#87acce',30);line(d,[(310,302),(310,324)],'#b8d5e7',5);save(im,'hat-blue')
im,d=new();ellipse(d,(239,319,344,411),(0,0,0,0),'#c69b45',9);ellipse(d,(424,319,529,411),(0,0,0,0),'#c69b45',9);arc(d,(338,349,430,394),180,360,'#c69b45',8);line(d,[(211,345),(244,354)],'#c69b45',8);line(d,[(527,354),(558,345)],'#c69b45',8);save(im,'glasses-gold')

files=list(OUT.glob('*.png'))
for f in files:
    a=Image.open(f); assert a.mode=='RGBA' and a.size==(N,N)
    assert all(a.getpixel(p)[3]==0 for p in [(0,0),(N-1,0),(0,N-1),(N-1,N-1)])
variants=[]
for i,(hoodie,eyes,hat,glasses) in enumerate([
 ('hoodie-coral','eyes-open',None,None),('hoodie-mint','eyes-happy','hat-blue',None),
 ('hoodie-coral','eyes-happy',None,'glasses-gold'),('hoodie-mint','eyes-open','hat-blue','glasses-gold')]):
    comp=Image.new('RGBA',(N,N))
    for name in ['base',hoodie,eyes,hat,glasses]:
        if name:comp=Image.alpha_composite(comp,Image.open(OUT/f'{name}.png'))
    comp.save(OUT/f'composition-{i+1}.png');variants.append({'file':f'composition-{i+1}.png','traits':[hoodie,eyes,hat,glasses]})
(HERE/'validation.json').write_text(json.dumps({'canvas':[N,N],'color_mode':'RGBA','layers':len(files),'corner_alpha':0,'variants':variants},indent=2))
print(f'{len(files)} aligned RGBA layers; four compositions; transparent corners verified.')
