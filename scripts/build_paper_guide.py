# -*- coding: utf-8 -*-
import json, html, re

DATA = json.load(open('data/paper-airplanes.json'))
specs = DATA['specs']
missing = DATA.get('missing', [])

INK   = '#17232F'
SOFT  = '#5A6B7A'
TINT  = '#DCE5EE'
CENT  = '#9AAAB9'
VALLEY= '#2E6FB7'
MOUNT = '#C0392B'
ACC   = '#D9701E'

def esc(t): return html.escape(str(t))

def bbox(pts):
    xs=[p['x'] for p in pts]; ys=[p['y'] for p in pts]
    return min(xs),min(ys),max(xs),max(ys)

def fit(pts, W, H, pad, invert=False, domain=None):
    minx,miny,maxx,maxy = domain if domain else bbox(pts)
    bw=(maxx-minx) or 1; bh=(maxy-miny) or 1
    sc=min((W-2*pad)/bw,(H-2*pad)/bh)
    offx=(W-bw*sc)/2 - minx*sc
    offy=(H-bh*sc)/2 - miny*sc
    def m(x,y):
        yy=(miny+maxy - y) if invert else y
        return offx + x*sc, offy + yy*sc
    return m,(minx,miny,maxx,maxy)

def ppath(pts,m):
    seg=[]
    for i,p in enumerate(pts):
        X,Y=m(p['x'],p['y'])
        seg.append(('M' if i==0 else 'L')+f'{X:.1f} {Y:.1f}')
    return ' '.join(seg)+' Z'

def cg_marker(cx,cy,r=6.5):
    # standard centre-of-gravity balance symbol: circle with two filled opposite quadrants
    q1=f'<path d="M{cx:.1f} {cy:.1f} L{cx:.1f} {cy-r:.1f} A{r} {r} 0 0 1 {cx+r:.1f} {cy:.1f} Z" fill="{INK}"/>'
    q2=f'<path d="M{cx:.1f} {cy:.1f} L{cx:.1f} {cy+r:.1f} A{r} {r} 0 0 1 {cx-r:.1f} {cy:.1f} Z" fill="{INK}"/>'
    circ=f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r}" fill="none" stroke="{INK}" stroke-width="1.2"/>'
    return q1+q2+circ

def caption(W,H,txt):
    return (f'<line x1="14" y1="{H-30}" x2="{W-14}" y2="{H-30}" stroke="{INK}" stroke-width="0.6" opacity="0.35"/>'
            f'<text x="14" y="{H-13}" class="cap">{esc(txt)}</text>')

def svg_open(W,H,label):
    return (f'<svg viewBox="0 0 {W} {H}" width="100%" role="img" aria-label="{esc(label)}" '
            f'preserveAspectRatio="xMidYMid meet" xmlns="http://www.w3.org/2000/svg">')

def panel_plan(sp, W=250, H=300):
    dg=sp['diagram']; outline=dg['top_view_outline']
    m,dom=fit(outline,W,H,30)
    minx,miny,maxx,maxy=dom
    path=ppath(outline,m)
    cgx,cgy=m(dg['cg_point']['x'],dg['cg_point']['y'])
    # centreline nose->tail at x=50
    nx,ny=m(50,miny); tx,ty=m(50,maxy)
    out=[svg_open(W,H,'Plan view — '+sp['name'])]
    out.append(f'<line x1="{nx:.1f}" y1="{ny:.1f}" x2="{tx:.1f}" y2="{ty:.1f}" stroke="{CENT}" stroke-width="1" stroke-dasharray="2 4"/>')
    out.append(f'<path d="{path}" fill="{TINT}" stroke="{INK}" stroke-width="1.6" stroke-linejoin="round"/>')
    out.append(cg_marker(cgx,cgy))
    out.append(f'<text x="{cgx+11:.1f}" y="{cgy+3:.1f}" class="ann">CG</text>')
    out.append(caption(W,H,'PLAN / top view'))
    out.append('</svg>')
    return ''.join(out)

def panel_elev(sp, W=250, H=210):
    dg=sp['diagram']; side=dg['side_profile']
    m,dom=fit(side,W,H,30,invert=True)
    path=ppath(side,m)
    out=[svg_open(W,H,'Side elevation — '+sp['name'])]
    # nose direction arrow
    out.append(f'<path d="{path}" fill="{TINT}" stroke="{INK}" stroke-width="1.6" stroke-linejoin="round"/>')
    out.append(f'<text x="16" y="24" class="ann">◄ nose</text>')
    out.append(caption(W,H,'ELEVATION / side view'))
    out.append('</svg>')
    return ''.join(out)

STYLE={'valley':(VALLEY,'5 3'),'mountain':(MOUNT,'7 3 1.5 3'),'cut':(INK,None),'centerline':(CENT,'1 4')}
def panel_crease(sp, W=250, H=300):
    dg=sp['diagram']; lines=dg['crease_lines']
    m,dom=fit([{'x':0,'y':0},{'x':100,'y':100}],W,H,30,domain=(0,0,100,100))
    # sheet rectangle
    c=[m(0,0),m(100,0),m(100,100),m(0,100)]
    rect='M'+' L'.join(f'{x:.1f} {y:.1f}' for x,y in c)+' Z'
    out=[svg_open(W,H,'Crease pattern — '+sp['name'])]
    out.append(f'<path d="{rect}" fill="#FFFFFF" stroke="{INK}" stroke-width="1.4"/>')
    for ln in lines:
        col,dash=STYLE.get(ln['type'],(INK,None))
        x1,y1=m(ln['x1'],ln['y1']); x2,y2=m(ln['x2'],ln['y2'])
        da=f' stroke-dasharray="{dash}"' if dash else ''
        w=2.0 if ln['type']=='cut' else 1.4
        out.append(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{col}" stroke-width="{w}"{da}/>')
    out.append(caption(W,H,'CREASE PATTERN / flat sheet'))
    out.append('</svg>')
    return ''.join(out)

def mini(sp, W=110, H=132):
    outline=sp['diagram']['top_view_outline']
    m,dom=fit(outline,W,H,14)
    path=ppath(outline,m)
    return (f'<svg viewBox="0 0 {W} {H}" width="100%" aria-hidden="true" xmlns="http://www.w3.org/2000/svg">'
            f'<path d="{path}" fill="{TINT}" stroke="{INK}" stroke-width="1.3" stroke-linejoin="round"/></svg>')

def short(name):
    n=re.sub(r'\s*\(.*?\)','',name).strip()
    return n

DIFF={'easy':('#2E7D5B','easy'),'medium':('#B07908','medium'),'hard':('#B23A2E','hard')}

# ---------------- build HTML ----------------
P=[]
P.append('<title>Paper aircraft — a field guide</title>')
P.append('''<style>
:root{
 --ink:#17232F; --soft:#5A6B7A; --paper:#E7ECF1; --panel:#FAFCFE;
 --acc:#D9701E; --line:#C7D2DC; --valley:#2E6FB7; --mount:#C0392B;
 --sans:"Helvetica Neue",Arial,system-ui,sans-serif;
 --mono:ui-monospace,"SF Mono","Cascadia Code",Menlo,Consolas,monospace;
}
*{box-sizing:border-box}
.wrap{max-width:1120px;margin:0 auto;padding:38px 22px 90px;color:var(--ink);
 background:var(--paper);font-family:var(--sans);line-height:1.65;font-size:16.5px;
 -webkit-font-smoothing:antialiased}
.wrap{background-image:linear-gradient(var(--line) 1px,transparent 1px),linear-gradient(90deg,var(--line) 1px,transparent 1px);
 background-size:26px 26px;background-position:-1px -1px;background-blend-mode:normal}
.sheet{background:var(--panel);border:1px solid var(--line)}
.eyebrow{font-family:var(--mono);text-transform:uppercase;letter-spacing:.16em;font-size:.7rem;color:var(--soft)}
.acc{color:var(--acc)}
a{color:var(--ink);text-decoration:none;border-bottom:1.5px solid var(--acc)}
a:hover{color:var(--acc)}
:focus-visible{outline:2px solid var(--acc);outline-offset:2px}

/* masthead / title block */
.title-block{display:grid;grid-template-columns:1fr auto;gap:0;border:1.5px solid var(--ink);background:var(--panel)}
.tb-main{padding:26px 28px;border-right:1.5px solid var(--ink)}
.tb-main h1{font-size:clamp(1.9rem,4.6vw,3.1rem);line-height:1.02;margin:.35rem 0 .5rem;
 letter-spacing:-.015em;font-weight:800;text-wrap:balance}
.tb-main p{margin:0;max-width:60ch;color:#243240}
.tb-meta{display:grid;grid-template-rows:repeat(3,1fr);min-width:190px}
.tb-cell{padding:12px 18px;border-bottom:1px solid var(--line);font-family:var(--mono);font-size:.82rem}
.tb-cell:last-child{border-bottom:none}
.tb-cell b{display:block;font-family:var(--mono);font-size:.66rem;letter-spacing:.14em;
 text-transform:uppercase;color:var(--soft);font-weight:500;margin-bottom:3px}
.tb-num{font-variant-numeric:tabular-nums}

/* legend */
.legend{display:flex;flex-wrap:wrap;gap:22px;align-items:center;margin:22px 0 30px;
 padding:12px 18px;background:var(--panel);border:1px solid var(--line);font-family:var(--mono);font-size:.78rem}
.legend span{display:inline-flex;align-items:center;gap:9px}
.swatch{width:34px;height:0;border-top-width:2.4px;border-top-style:solid;display:inline-block}

/* index */
.section-label{font-family:var(--mono);text-transform:uppercase;letter-spacing:.18em;font-size:.74rem;
 color:var(--soft);margin:40px 0 14px;display:flex;align-items:center;gap:14px}
.section-label::after{content:"";flex:1;height:1px;background:var(--line)}
.index{display:grid;grid-template-columns:repeat(auto-fill,minmax(128px,1fr));gap:12px}
.chip{display:block;background:var(--panel);border:1px solid var(--line);padding:10px 10px 12px;
 transition:transform .12s ease,border-color .12s ease}
.chip:hover{transform:translateY(-3px);border-color:var(--acc)}
.chip .n{font-family:var(--mono);font-size:.7rem;color:var(--acc);font-variant-numeric:tabular-nums}
.chip .nm{font-size:.82rem;font-weight:600;line-height:1.2;margin-top:4px}
.chip .ct{font-family:var(--mono);font-size:.64rem;color:var(--soft);margin-top:3px;line-height:1.3}

/* plate */
.plate{margin-top:30px;border:1px solid var(--line);background:var(--panel)}
.plate-hd{display:flex;flex-wrap:wrap;align-items:baseline;gap:10px 16px;padding:20px 24px 14px;border-bottom:1px solid var(--line)}
.plate-hd .pn{font-family:var(--mono);font-size:1.05rem;color:var(--acc);font-weight:700;font-variant-numeric:tabular-nums}
.plate-hd h2{font-size:clamp(1.35rem,2.6vw,1.75rem);margin:0;font-weight:750;letter-spacing:-.01em}
.plate-hd .aka{font-family:var(--mono);font-size:.76rem;color:var(--soft)}
.pill{font-family:var(--mono);font-size:.68rem;text-transform:uppercase;letter-spacing:.08em;
 padding:3px 9px;border-radius:2px;border:1px solid currentColor;font-weight:600}
.badge{font-family:var(--mono);font-size:.7rem;background:var(--acc);color:#fff;padding:4px 10px;border-radius:2px;letter-spacing:.02em}
.plate-body{padding:20px 24px 26px}
.lead{font-size:1.02rem;max-width:74ch;margin:0 0 20px;color:#1f2c38}
.lead b{color:var(--acc);font-weight:600}

.drawings{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:14px;margin-bottom:24px}
.panel{background:var(--panel);border:1px solid var(--line);position:relative;
 background-image:linear-gradient(rgba(90,107,122,.09) 1px,transparent 1px),linear-gradient(90deg,rgba(90,107,122,.09) 1px,transparent 1px);
 background-size:15px 15px}
.panel svg{display:block}
text.cap{font-family:var(--mono);font-size:9px;letter-spacing:.1em;fill:var(--soft);text-transform:uppercase}
text.ann{font-family:var(--mono);font-size:9.5px;fill:var(--ink)}

.cols{display:grid;grid-template-columns:1.15fr .85fr;gap:30px}
.folds{margin:0;padding:0;list-style:none;counter-reset:f}
.folds li{counter-increment:f;position:relative;padding:0 0 12px 40px;font-size:.95rem}
.folds li::before{content:counter(f,decimal-leading-zero);position:absolute;left:0;top:1px;
 font-family:var(--mono);font-size:.74rem;color:var(--acc);font-weight:700;
 border:1px solid var(--line);border-radius:50%;width:26px;height:26px;display:grid;place-items:center}
h3.sub{font-family:var(--mono);text-transform:uppercase;letter-spacing:.14em;font-size:.72rem;
 color:var(--soft);margin:0 0 14px;font-weight:600}
.spec{width:100%;border-collapse:collapse;font-family:var(--mono);font-size:.8rem}
.spec th{text-align:left;color:var(--soft);font-weight:500;padding:5px 10px 5px 0;
 vertical-align:top;white-space:nowrap;width:1%}
.spec td{padding:5px 0;vertical-align:top;color:#1f2c38}
.spec tr+tr th,.spec tr+tr td{border-top:1px dashed var(--line)}
.feat{display:flex;flex-wrap:wrap;gap:6px;margin:16px 0}
.feat span{font-family:var(--mono);font-size:.7rem;background:var(--paper);border:1px solid var(--line);
 padding:3px 8px;border-radius:2px;color:#2a3846}
.fact{margin-top:16px;padding:12px 16px;border-left:3px solid var(--acc);background:var(--paper);font-size:.92rem}
.fact b{font-family:var(--mono);font-size:.66rem;letter-spacing:.14em;text-transform:uppercase;color:var(--acc);display:block;margin-bottom:4px}

/* future + refs */
.future{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:14px}
.ghost{border:1.5px dashed var(--line);background:transparent;padding:18px 18px 20px}
.ghost .n{font-family:var(--mono);font-size:.7rem;color:var(--soft)}
.ghost h4{margin:6px 0 8px;font-size:1.02rem}
.ghost p{margin:0;font-size:.88rem;color:#2a3846}
.foot{margin-top:46px;font-size:.9rem;color:#2a3846}
.foot h3.sub{margin-top:22px}
.method{font-family:var(--mono);font-size:.78rem;color:var(--soft);line-height:1.6}
@media (max-width:720px){.title-block{grid-template-columns:1fr}.tb-main{border-right:none;border-bottom:1.5px solid var(--ink)}
 .tb-meta{grid-template-rows:none;grid-template-columns:repeat(3,1fr)}.tb-cell{border-bottom:none;border-right:1px solid var(--line)}
 .cols{grid-template-columns:1fr;gap:22px}}
@media (prefers-reduced-motion:reduce){*{transition:none!important}}
</style>''')

P.append('<div class="wrap">')
# masthead
P.append(f'''<div class="title-block">
 <div class="tb-main">
  <div class="eyebrow">aerodynamics of folded paper · drawing set</div>
  <h1>Paper aircraft:<br>a field guide</h1>
  <p>Nine flyers, each the best at one thing — fastest, farthest, longest-floating, most crash-proof, and stranger still. Every plate carries a plan, a side elevation, the crease pattern, and a full fold sequence.</p>
 </div>
 <div class="tb-meta">
  <div class="tb-cell"><b>designs</b><span class="tb-num">09 plates</span></div>
  <div class="tb-cell"><b>scope</b>speed · distance · float · stunt · novelty</div>
  <div class="tb-cell"><b>status</b>fold + fact verified</div>
 </div>
</div>''')

# legend
P.append(f'''<div class="legend">
 <span><span class="swatch" style="border-top-color:{VALLEY};border-top-style:dashed"></span>valley fold (fold toward you)</span>
 <span><span class="swatch" style="border-top-color:{MOUNT};border-top-style:dashed"></span>mountain fold (fold away)</span>
 <span><span class="swatch" style="border-top-color:{INK};border-top-style:solid"></span>cut / edge</span>
 <span><span class="swatch" style="border-top-color:{CENT};border-top-style:dotted"></span>centerline</span>
 <span>⊕ = centre of gravity</span>
</div>''')

# index
P.append('<div class="section-label">specimen index</div>')
P.append('<div class="index">')
for i,sp in enumerate(specs,1):
    cat=sp['category'].split('(')[0].split('—')[0].split('/')[0].strip()
    P.append(f'<a class="chip" href="#p{i}"><div class="n">{i:02d}</div>{mini(sp)}'
             f'<div class="nm">{esc(short(sp["name"]))}</div><div class="ct">{esc(cat)}</div></a>')
P.append('</div>')

# plates
for i,sp in enumerate(specs,1):
    dcol,dlab=DIFF.get(sp['difficulty'],(SOFT,sp['difficulty']))
    cat=sp['category'].strip()
    aka=sp.get('aka','')
    P.append(f'<section class="plate" id="p{i}">')
    P.append('<div class="plate-hd">')
    P.append(f'<span class="pn">{i:02d}</span><h2>{esc(short(sp["name"]))}</h2>')
    if aka: P.append(f'<span class="aka">a.k.a. {esc(aka)}</span>')
    P.append(f'<span class="badge">{esc(cat)}</span>')
    P.append(f'<span class="pill" style="color:{dcol}">{esc(dlab)}</span>')
    P.append('</div>')
    P.append('<div class="plate-body">')
    P.append(f'<p class="lead">{esc(sp["why_best"])}</p>')
    # drawings
    P.append('<div class="drawings">')
    P.append(f'<div class="panel">{panel_plan(sp)}</div>')
    P.append(f'<div class="panel">{panel_elev(sp)}</div>')
    P.append(f'<div class="panel">{panel_crease(sp)}</div>')
    P.append('</div>')
    # cols
    P.append('<div class="cols"><div>')
    P.append('<h3 class="sub">fold sequence</h3><ol class="folds">')
    for st in sp['fold_steps']:
        P.append(f'<li>{esc(st["text"])}</li>')
    P.append('</ol></div><div>')
    P.append('<h3 class="sub">specification</h3><table class="spec"><tbody>')
    g=sp['geometry']; f=sp['flight']
    rows=[('paper',sp['paper']),('wingspan',g['wingspan']),('dihedral',g['dihedral']),
          ('aspect',g['aspect']),('C.G.',g['cg']),('throw',f['throw']),
          ('speed',f['speed']),('glide',f['glide']),('behaviour',f['behavior'])]
    for k,v in rows:
        P.append(f'<tr><th>{esc(k)}</th><td>{esc(v)}</td></tr>')
    P.append('</tbody></table>')
    feats=sp['diagram'].get('features',[])
    if feats:
        P.append('<div class="feat">'+''.join(f'<span>{esc(x)}</span>' for x in feats)+'</div>')
    P.append(f'<div class="fact"><b>field note</b>{esc(sp["fun_fact"])}</div>')
    if sp.get('origin'):
        P.append(f'<p class="method" style="margin-top:14px">origin — {esc(sp["origin"])}</p>')
    P.append('</div></div>')  # cols
    P.append('</div></section>')

# future
if missing:
    P.append('<div class="section-label">plates not yet drawn</div>')
    P.append('<div class="future">')
    for j,mz in enumerate(missing,1):
        P.append(f'<div class="ghost"><div class="n">proposed · {sp0 if False else j:02d}</div>'
                 f'<h4>{esc(mz["name"])}</h4><p>{esc(mz["reason"])}</p></div>')
    P.append('</div>')

# footer / method
P.append('<div class="foot">')
P.append('<h3 class="sub">how this guide was made</h3>')
P.append('<p class="method">Nine designs were each researched by a dedicated agent, then adversarially verified — a second agent mentally re-folded every sequence to confirm it produces the drawn shape, and fact-checked designers, origins, and records. The distance-record chain was corrected in the process: John Collins&rsquo; glider &ldquo;Suzanne&rdquo; (thrown by Joe Ayoob, 69.14 m / 226 ft 10 in, 2012) was the first glider to hold the record, later broken to 77.13 m (2022, Chee Yie Jian / Kim Kyu Tae) and then to the current 88.31 m (Dec 2022, Boeing engineers Ruble, Jensen &amp; Erickson). Drawings are generated directly from each verified design&rsquo;s geometry.</p>')
P.append('<h3 class="sub">references</h3>')
P.append('<p class="method">Fold&rsquo;N&rsquo;Fly (foldnfly.com) · NASA JPL &ldquo;Ring Wing Glider&rdquo; activity · John M. Collins, <em>The New World Champion Paper Airplane Book</em> · Slater Harrison / ScienceToyMaker (tumblewing &amp; walkalong gliding) · Art of Manliness (Bulldog Dart) · Guinness World Records (distance).</p>')
P.append('</div>')

P.append('</div>')  # wrap

open('guides/paper-airplanes.html','w').write('\n'.join(P))
print('wrote guides/paper-airplanes.html', len('\n'.join(P)), 'bytes')
