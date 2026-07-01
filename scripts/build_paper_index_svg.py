# -*- coding: utf-8 -*-
import json, re, html
specs=json.load(open('data/paper-airplanes.json'))['specs']
def esc(t): return html.escape(str(t))
def bbox(pts):
    xs=[p['x'] for p in pts]; ys=[p['y'] for p in pts]
    return min(xs),min(ys),max(xs),max(ys)
def fit(pts,W,H,pad,ox,oy):
    minx,miny,maxx,maxy=bbox(pts)
    bw=(maxx-minx)or 1; bh=(maxy-miny)or 1
    sc=min((W-2*pad)/bw,(H-2*pad)/bh)
    offx=ox+(W-bw*sc)/2-minx*sc; offy=oy+(H-bh*sc)/2-miny*sc
    return lambda x,y:(offx+x*sc,offy+y*sc)
def short(n): return re.sub(r'\s*\(.*?\)','',n).strip()

W=680; cols=3; cw=W//cols
cellW=cw; silH=104; rowH=196; top=54
rows=(len(specs)+cols-1)//cols
H=top+rows*rowH+8
out=[f'<svg width="100%" viewBox="0 0 {W} {H}" role="img" xmlns="http://www.w3.org/2000/svg">']
out.append('<title>Specimen index of nine paper airplane planforms</title>')
out.append('<desc>Top-view silhouettes of nine paper airplanes, each labelled with its name and the category it wins: fastest, longest distance, best cruiser, highest glide ratio, most durable, ring-wing, aerobatic, boomerang, and walkalong glider.</desc>')
out.append(f'<text x="40" y="30" class="th">The best paper airplanes — one per discipline</text>')
out.append(f'<text x="40" y="46" class="ts">top-view planforms · full plates in the field guide</text>')
for i,sp in enumerate(specs):
    r=i//cols; c=i%cols
    x0=c*cw; y0=top+r*rowH
    cat=sp['category'].split('(')[0].split('—')[0].split('/')[0].strip()
    m=fit(sp['diagram']['top_view_outline'],cellW,silH,20,x0,y0+18)
    pts=sp['diagram']['top_view_outline']
    seg=[]
    for k,p in enumerate(pts):
        X,Y=m(p['x'],p['y']); seg.append(('M' if k==0 else 'L')+f'{X:.1f} {Y:.1f}')
    path=' '.join(seg)+' Z'
    cx=x0+cw/2
    out.append(f'<text x="{x0+16:.0f}" y="{y0+14:.0f}" class="ts">{i+1:02d}</text>')
    out.append(f'<path d="{path}" fill="none" stroke="var(--color-text-primary)" stroke-width="1.6" stroke-linejoin="round"/>')
    out.append(f'<text x="{cx:.0f}" y="{y0+silH+38:.0f}" text-anchor="middle" class="t">{esc(short(sp["name"]))}</text>')
    out.append(f'<text x="{cx:.0f}" y="{y0+silH+56:.0f}" text-anchor="middle" class="ts">{esc(cat)}</text>')
out.append('</svg>')
open('diagrams/paper-index.svg','w').write(''.join(out))
print('wrote diagrams/paper-index.svg  H=',H,' bytes=',len(''.join(out)))
