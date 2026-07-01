# -*- coding: utf-8 -*-
import json, html, re
D=json.load(open('data/drone-concepts.json'))
concepts=D['concepts']; levers=sorted(D['vtol_levers'],key=lambda x:x['rank']); missing=D.get('missing',[])

INK='#17232F'; SOFT='#5A6B7A'; TINT='#DCE5EE'; CENT='#9AAAB9'
ACC='#D9701E'; BLU='#2E6FB7'; GRN='#2E7D5B'; RED='#B23A2E'
def esc(t): return html.escape(str(t))
def bbox(pts):
    xs=[p['x'] for p in pts]; ys=[p['y'] for p in pts]; return min(xs),min(ys),max(xs),max(ys)
def fit(pts,W,H,pad,invert=False,domain=None):
    minx,miny,maxx,maxy=domain if domain else bbox(pts)
    bw=(maxx-minx)or 1; bh=(maxy-miny)or 1
    sc=min((W-2*pad)/bw,(H-2*pad)/bh)
    offx=(W-bw*sc)/2-minx*sc; offy=(H-bh*sc)/2-miny*sc
    def m(x,y):
        yy=(miny+maxy-y) if invert else y
        return offx+x*sc, offy+yy*sc
    return m,(minx,miny,maxx,maxy)
def ppath(pts,m):
    seg=[]
    for i,p in enumerate(pts):
        X,Y=m(p['x'],p['y']); seg.append(('M' if i==0 else 'L')+f'{X:.1f} {Y:.1f}')
    return ' '.join(seg)+' Z'
def cg_marker(cx,cy,r=6.5):
    return (f'<path d="M{cx:.1f} {cy:.1f} L{cx:.1f} {cy-r:.1f} A{r} {r} 0 0 1 {cx+r:.1f} {cy:.1f} Z" fill="{INK}"/>'
            f'<path d="M{cx:.1f} {cy:.1f} L{cx:.1f} {cy+r:.1f} A{r} {r} 0 0 1 {cx-r:.1f} {cy:.1f} Z" fill="{INK}"/>'
            f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r}" fill="none" stroke="{INK}" stroke-width="1.2"/>')
def caption(W,H,txt):
    return (f'<line x1="14" y1="{H-30}" x2="{W-14}" y2="{H-30}" stroke="{INK}" stroke-width="0.6" opacity="0.35"/>'
            f'<text x="14" y="{H-13}" class="cap">{esc(txt)}</text>')
def svg_open(W,H,label):
    return (f'<svg viewBox="0 0 {W} {H}" width="100%" role="img" aria-label="{esc(label)}" '
            f'preserveAspectRatio="xMidYMid meet" xmlns="http://www.w3.org/2000/svg">')
MASS={'heavy':(ACC,7.0),'medium':(BLU,5.0),'light':(SOFT,3.8)}
def panel_plan(sp,W=250,H=300):
    dg=sp['diagram']; outline=dg['top_view_outline']
    m,dom=fit(outline,W,H,32); minx,miny,maxx,maxy=dom
    nx,ny=m(50,miny); tx,ty=m(50,maxy)
    out=[svg_open(W,H,'Plan view — '+sp['name'])]
    out.append(f'<line x1="{nx:.1f}" y1="{ny:.1f}" x2="{tx:.1f}" y2="{ty:.1f}" stroke="{CENT}" stroke-width="1" stroke-dasharray="2 4"/>')
    out.append(f'<path d="{ppath(outline,m)}" fill="{TINT}" stroke="{INK}" stroke-width="1.6" stroke-linejoin="round"/>')
    for i,c in enumerate(dg['components'],1):
        col,r=MASS.get(c['mass_hint'],(SOFT,4)); X,Y=m(c['x'],c['y'])
        out.append(f'<circle cx="{X:.1f}" cy="{Y:.1f}" r="{r}" fill="{col}" fill-opacity="0.9" stroke="#fff" stroke-width="0.8"/>')
        out.append(f'<text x="{X:.1f}" y="{Y+2.6:.1f}" text-anchor="middle" class="dot">{i}</text>')
    cgx,cgy=m(dg['cg_point']['x'],dg['cg_point']['y'])
    out.append(cg_marker(cgx,cgy))
    out.append(f'<text x="{cgx+10:.1f}" y="{cgy+3:.1f}" class="ann">CG</text>')
    out.append(caption(W,H,'PLAN / mass map + CG'))
    out.append('</svg>'); return ''.join(out)
def panel_elev(sp,W=250,H=190):
    side=sp['diagram']['side_profile']; m,dom=fit(side,W,H,30,invert=True)
    out=[svg_open(W,H,'Side elevation — '+sp['name'])]
    out.append(f'<path d="{ppath(side,m)}" fill="{TINT}" stroke="{INK}" stroke-width="1.6" stroke-linejoin="round"/>')
    out.append(f'<text x="16" y="24" class="ann">◄ nose</text>')
    out.append(caption(W,H,'ELEVATION / side view'))
    out.append('</svg>'); return ''.join(out)

REV={'scales':(GRN,'scales to drone Re'),'partially-scales':(ACC,'partially scales'),'does-not-scale':(RED,'does not scale')}
DIFF={'easy':(GRN,'easy'),'medium':(ACC,'medium'),'hard':(RED,'hard')}
PH={'hover':BLU,'cruise':GRN,'transition':ACC,'all':SOFT}
def short(n): return re.sub(r'\s*\(.*?\)','',re.sub(r'\s+—.*$','',n)).strip()

P=[]
P.append('<title>Paper to printed drones — field guide vol. II</title>')
P.append('''<style>
:root{--ink:#17232F;--soft:#5A6B7A;--paper:#E7ECF1;--panel:#FAFCFE;--acc:#D9701E;--line:#C7D2DC;
 --blu:#2E6FB7;--grn:#2E7D5B;--red:#B23A2E;
 --sans:"Helvetica Neue",Arial,system-ui,sans-serif;--mono:ui-monospace,"SF Mono","Cascadia Code",Menlo,Consolas,monospace;}
*{box-sizing:border-box}
.wrap{max-width:1120px;margin:0 auto;padding:38px 22px 90px;color:var(--ink);background:var(--paper);
 font-family:var(--sans);line-height:1.65;font-size:16.5px;-webkit-font-smoothing:antialiased;
 background-image:linear-gradient(var(--line) 1px,transparent 1px),linear-gradient(90deg,var(--line) 1px,transparent 1px);
 background-size:26px 26px;background-position:-1px -1px}
.eyebrow{font-family:var(--mono);text-transform:uppercase;letter-spacing:.16em;font-size:.7rem;color:var(--soft)}
a{color:var(--ink);text-decoration:none;border-bottom:1.5px solid var(--acc)}
a:hover{color:var(--acc)}
:focus-visible{outline:2px solid var(--acc);outline-offset:2px}
.title-block{display:grid;grid-template-columns:1fr auto;border:1.5px solid var(--ink);background:var(--panel)}
.tb-main{padding:26px 28px;border-right:1.5px solid var(--ink)}
.tb-main h1{font-size:clamp(1.9rem,4.4vw,3rem);line-height:1.03;margin:.35rem 0 .5rem;letter-spacing:-.015em;font-weight:800;text-wrap:balance}
.tb-main p{margin:0;max-width:64ch;color:#243240}
.tb-meta{display:grid;min-width:200px}
.tb-cell{padding:12px 18px;border-bottom:1px solid var(--line);font-family:var(--mono);font-size:.82rem}
.tb-cell:last-child{border-bottom:none}
.tb-cell b{display:block;font-size:.66rem;letter-spacing:.14em;text-transform:uppercase;color:var(--soft);font-weight:500;margin-bottom:3px}
.section-label{font-family:var(--mono);text-transform:uppercase;letter-spacing:.18em;font-size:.74rem;color:var(--soft);margin:44px 0 16px;display:flex;align-items:center;gap:14px}
.section-label::after{content:"";flex:1;height:1px;background:var(--line)}
.lead-note{background:var(--panel);border:1px solid var(--line);border-left:3px solid var(--acc);padding:16px 20px;margin-bottom:8px;max-width:78ch}
.lead-note b{color:var(--acc)}
/* transfer matrix */
.matrix{width:100%;border-collapse:collapse;background:var(--panel);border:1px solid var(--line);font-size:.92rem;overflow:hidden}
.matrix th{font-family:var(--mono);text-transform:uppercase;letter-spacing:.1em;font-size:.64rem;color:var(--soft);
 text-align:left;padding:11px 14px;border-bottom:1.5px solid var(--line);font-weight:500}
.matrix td{padding:11px 14px;border-bottom:1px solid var(--line);vertical-align:top}
.matrix tr:last-child td{border-bottom:none}
.matrix td.p{font-weight:600;white-space:nowrap}
.tag{font-family:var(--mono);font-size:.66rem;text-transform:uppercase;letter-spacing:.06em;padding:3px 8px;border-radius:2px;color:#fff;white-space:nowrap}
.mtable-wrap{overflow-x:auto}
/* plate */
.plate{margin-top:26px;border:1px solid var(--line);background:var(--panel)}
.plate-hd{display:flex;flex-wrap:wrap;align-items:baseline;gap:9px 14px;padding:18px 22px 12px;border-bottom:1px solid var(--line)}
.plate-hd .pn{font-family:var(--mono);font-size:1.05rem;color:var(--acc);font-weight:700}
.plate-hd h2{font-size:clamp(1.3rem,2.5vw,1.65rem);margin:0;font-weight:750;letter-spacing:-.01em}
.plate-hd .dt{font-family:var(--mono);font-size:.72rem;color:var(--soft);flex-basis:100%;margin-top:2px}
.pill{font-family:var(--mono);font-size:.66rem;text-transform:uppercase;letter-spacing:.06em;padding:3px 9px;border-radius:2px;color:#fff}
.plate-body{padding:20px 22px 24px}
.oneliner{font-size:1.06rem;font-style:italic;color:#1f2c38;max-width:74ch;margin:0 0 20px}
.pgrid{display:grid;grid-template-columns:minmax(220px,300px) 1fr;gap:26px}
@media(max-width:760px){.pgrid{grid-template-columns:1fr}}
.draw{display:flex;flex-direction:column;gap:12px}
.panel{border:1px solid var(--line);background-image:linear-gradient(rgba(90,107,122,.09) 1px,transparent 1px),linear-gradient(90deg,rgba(90,107,122,.09) 1px,transparent 1px);background-size:15px 15px}
text.cap{font-family:var(--mono);font-size:9px;letter-spacing:.1em;fill:var(--soft);text-transform:uppercase}
text.ann{font-family:var(--mono);font-size:9.5px;fill:var(--ink)}
text.dot{font-family:var(--mono);font-size:8px;fill:#fff;font-weight:700}
.massmap{list-style:none;margin:2px 0 0;padding:0;font-family:var(--mono);font-size:.72rem;color:#2a3846}
.massmap li{display:flex;gap:8px;padding:2px 0;line-height:1.35}
.massmap .n{color:var(--acc);font-weight:700;min-width:14px}
.massmap .m{margin-left:auto;color:var(--soft)}
.facts{display:flex;flex-wrap:wrap;gap:6px;margin:0 0 16px}
.facts span{font-family:var(--mono);font-size:.72rem;background:var(--paper);border:1px solid var(--line);padding:4px 9px;border-radius:2px}
.facts span b{color:var(--soft);font-weight:500}
.block{margin:0 0 14px}
.block h4{font-family:var(--mono);text-transform:uppercase;letter-spacing:.12em;font-size:.68rem;color:var(--acc);margin:0 0 4px;font-weight:600}
.block p{margin:0;font-size:.94rem;color:#1f2c38}
.re{border-left:3px solid var(--line);padding-left:12px}
/* levers */
.levers{display:flex;flex-direction:column;gap:0;border:1px solid var(--line);background:var(--panel)}
.lever{display:grid;grid-template-columns:38px 1fr;gap:0;border-bottom:1px solid var(--line)}
.lever:last-child{border-bottom:none}
.lever .rk{font-family:var(--mono);font-size:1rem;font-weight:700;color:var(--acc);padding:16px 0 0;text-align:center;border-right:1px solid var(--line);background:var(--paper)}
.lever .body{padding:14px 18px}
.lever .top{display:flex;flex-wrap:wrap;align-items:baseline;gap:8px 12px;margin-bottom:6px}
.lever .nm{font-weight:600;font-size:1rem}
.lever .meta{display:flex;gap:6px;margin-left:auto}
.chip{font-family:var(--mono);font-size:.62rem;text-transform:uppercase;letter-spacing:.05em;padding:2px 7px;border-radius:2px;color:#fff}
.lever .imp{font-size:.93rem;color:#1f2c38;margin:0 0 5px}
.lever .impl{font-family:var(--mono);font-size:.76rem;color:var(--soft);margin:0}
.lever .impl b{color:#2a3846;font-weight:500}
.future{display:grid;grid-template-columns:repeat(auto-fit,minmax(250px,1fr));gap:14px}
.ghost{border:1.5px dashed var(--line);padding:18px}
.ghost .n{font-family:var(--mono);font-size:.7rem;color:var(--soft)}
.ghost h4{margin:6px 0 8px;font-size:1rem}
.ghost p{margin:0;font-size:.88rem;color:#2a3846}
.foot{margin-top:46px;font-size:.9rem}
.foot h3{font-family:var(--mono);text-transform:uppercase;letter-spacing:.14em;font-size:.72rem;color:var(--soft);margin:22px 0 8px;font-weight:600}
.method{font-family:var(--mono);font-size:.78rem;color:var(--soft);line-height:1.6}
@media(max-width:720px){.title-block{grid-template-columns:1fr}.tb-main{border-right:none;border-bottom:1.5px solid var(--ink)}.tb-meta{grid-template-columns:repeat(3,1fr)}.tb-cell{border-bottom:none;border-right:1px solid var(--line)}}
@media(prefers-reduced-motion:reduce){*{transition:none!important}}
</style>''')

P.append('<div class="wrap">')
P.append(f'''<div class="title-block">
 <div class="tb-main">
  <div class="eyebrow">field guide · volume II · paper principles → printed drones</div>
  <h1>From folded paper<br>to printed drones</h1>
  <p>Nine future 3D-printed drone concepts, each borrowing one lesson from the paper field guide — and each stress-tested for the awkward truth: paper flies at Reynolds ~30,000, real drones cruise 5–15× higher, so the mass tricks transfer and most of the shape tricks don't. Ends with a ranked list of what actually makes the tiltrotor VTOL more efficient.</p>
 </div>
 <div class="tb-meta">
  <div class="tb-cell"><b>concepts</b>09 verified</div>
  <div class="tb-cell"><b>vtol levers</b>{len(levers)} ranked</div>
  <div class="tb-cell"><b>check</b>Reynolds + CG + printability</div>
 </div>
</div>''')

# transfer matrix
P.append('<div class="section-label">what transfers, what doesn’t</div>')
P.append('<div class="lead-note">The single idea that survives the jump to drone scale is <b>mass placement</b>: putting the battery forward to set the centre of gravity is rigid-body statics — completely Reynolds-independent. Most paper <b>aerodynamics</b> (swept deltas, stubby low-aspect wings, ring wings) only work because a paper plane’s boundary layer is forgiving at low speed; scaled up they just add drag. The exception is the <b>high-aspect wing</b>, which helps even more at drone scale.</div>')
P.append('<div class="mtable-wrap"><table class="matrix"><thead><tr><th>concept</th><th>borrowed principle</th><th>scales?</th><th>the honest verdict</th></tr></thead><tbody>')
for c in concepts:
    col,lab=REV.get(c['reynolds_verdict'],(SOFT,c['reynolds_verdict']))
    note=c['reynolds_note'].split('. ')[0]
    if len(note)>160: note=note[:157]+'…'
    P.append(f'<tr><td class="p">{esc(short(c["name"]))}</td><td>{esc(c["principle"].split(". ")[0][:120])}</td>'
             f'<td><span class="tag" style="background:{col}">{esc(lab)}</span></td><td>{esc(note)}</td></tr>')
P.append('</tbody></table></div>')

# concept plates
P.append('<div class="section-label">concept plates</div>')
for i,c in enumerate(concepts,1):
    rcol,rlab=REV.get(c['reynolds_verdict'],(SOFT,c['reynolds_verdict']))
    dcol,dlab=DIFF.get(c['build_difficulty'],(SOFT,c['build_difficulty']))
    P.append(f'<section class="plate" id="c{i}"><div class="plate-hd">')
    P.append(f'<span class="pn">{i:02d}</span><h2>{esc(short(c["name"]))}</h2>')
    P.append(f'<span class="pill" style="background:{rcol}">{esc(rlab)}</span>')
    P.append(f'<span class="pill" style="background:{dcol}">build: {esc(dlab)}</span>')
    P.append(f'<span class="dt">{esc(c["drone_type"])}</span></div>')
    P.append('<div class="plate-body">')
    P.append(f'<p class="oneliner">{esc(c["one_liner"])}</p>')
    P.append('<div class="pgrid"><div class="draw">')
    P.append(f'<div class="panel">{panel_plan(c)}</div>')
    P.append(f'<div class="panel">{panel_elev(c)}</div>')
    P.append('<ol class="massmap">')
    for k,comp in enumerate(c['diagram']['components'],1):
        P.append(f'<li><span class="n">{k}</span><span>{esc(comp["label"])}</span><span class="m">{esc(comp["mass_hint"])}</span></li>')
    P.append('</ol></div><div>')
    ks=c['key_specs']
    P.append('<div class="facts">'
             f'<span><b>span</b> {esc(ks["span"])}</span><span><b>AR</b> {esc(ks["aspect"])}</span>'
             f'<span><b>AUW</b> {esc(ks["auw"])}</span></div>')
    P.append(f'<div class="facts"><span><b>cruise</b> {esc(ks["cruise"])}</span></div>')
    P.append(f'<div class="facts"><span><b>hover</b> {esc(ks["hover"])}</span></div>')
    P.append(f'<div class="block"><h4>paper lineage</h4><p>{esc(c["paper_lineage"])}</p></div>')
    P.append(f'<div class="block re"><h4>reynolds reality</h4><p>{esc(c["reynolds_note"])}</p></div>')
    P.append(f'<div class="block"><h4>efficiency gain</h4><p>{esc(c["efficiency_gain"])}</p></div>')
    P.append(f'<div class="block"><h4>weighted components / CG</h4><p>{esc(c["weighted_components"])}</p></div>')
    P.append(f'<div class="block"><h4>how it prints</h4><p>{esc(c["realization_3dprint"])}</p></div>')
    P.append(f'<div class="block"><h4>tradeoffs</h4><p>{esc(c["tradeoffs"])}</p></div>')
    P.append('</div></div>')  # pgrid
    P.append('</div></section>')

# levers
P.append('<div class="section-label">making the tiltrotor VTOL more efficient — ranked</div>')
P.append('<div class="lead-note">Gathered across five engineering fronts (hover, cruise, structure, transition, propulsion), de-duplicated, and sanity-checked against momentum theory, then ranked by <b>impact per unit cost</b>. The top of the list is where your build time and grams buy the most.</div>')
P.append('<div class="levers">')
for l in levers:
    pcol=PH.get(l['phase'],SOFT)
    prcol={'high':RED,'medium':ACC,'low':SOFT}.get(l['priority'],SOFT)
    P.append(f'<div class="lever"><div class="rk">{l["rank"]}</div><div class="body">'
             f'<div class="top"><span class="nm">{esc(l["name"])}</span>'
             f'<span class="meta"><span class="chip" style="background:{pcol}">{esc(l["phase"])}</span>'
             f'<span class="chip" style="background:{prcol}">{esc(l["priority"])} priority</span></span></div>'
             f'<p class="imp"><b>{esc(l["impact"])}</b></p>'
             f'<p class="impl">mechanism — {esc(l["mechanism"])}</p>'
             f'<p class="impl" style="margin-top:4px">print it — <b>{esc(l["printable_implementation"])}</b> · cost: {esc(l["cost"])}</p>'
             '</div></div>')
P.append('</div>')

# future
if missing:
    P.append('<div class="section-label">principles still on the bench</div>')
    P.append('<div class="future">')
    for j,m in enumerate(missing,1):
        P.append(f'<div class="ghost"><div class="n">proposed · {j:02d}</div><h4>{esc(m["name"])}</h4><p>{esc(m["why"])}</p></div>')
    P.append('</div>')

P.append('<div class="foot">')
P.append('<h3>method</h3>')
P.append('<p class="method">Each concept was designed by a dedicated engineering agent grounded in the nine verified paper designs, then adversarially reviewed by a second agent for Reynolds-number scaling, static-margin/CG soundness, printability, and quantitative honesty. That review rewrote real errors — e.g. correcting static margin to (neutral-point − CG)/MAC for tailed layouts, flagging that a TPU living hinge cannot be co-printed into a PLA/PETG surface on a single nozzle, and downgrading hand-wavy efficiency percentages to defensible ranges. Every diagram is generated from the reviewed geometry.</p>')
P.append('<p class="method" style="margin-top:10px">Companion to volume I — the paper-airplane field guide.</p>')
P.append('</div>')
P.append('</div>')
open('guides/drones.html','w').write('\n'.join(P))
print('wrote guides/drones.html', len('\n'.join(P)),'bytes ·', len(concepts),'concepts ·', len(levers),'levers')
