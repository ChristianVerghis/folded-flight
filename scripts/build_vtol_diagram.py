# -*- coding: utf-8 -*-
import textwrap
P='var(--color-text-primary)'
S='var(--color-text-secondary)'
AMB='#D9701E'
BLU='#2E6FB7'
def esc(t):
    import html; return html.escape(str(t))

W=680
o=[f'<svg width="100%" viewBox="0 0 {W} 690" role="img" xmlns="http://www.w3.org/2000/svg">']
o.append('<title>A more efficient tri-tiltrotor VTOL — six annotated changes</title>')
o.append('<desc>Top view of a tri-tiltrotor VTOL (two wing tilt-rotors plus a tail rotor) marked with six efficiency changes: larger rotor discs for low disk loading, a higher-aspect low-Reynolds wing, a light LW-PLA and carbon structure, the battery placed forward as ballast to set the centre of gravity, folding the tail rotor in cruise, and flying weight-on-wing while minimizing transition time.</desc>')
o.append(f'<text x="40" y="30" class="th">A more efficient tri-tiltrotor — six changes that pay off</text>')
o.append(f'<text x="40" y="49" class="ts">same layout as your photo · numbers keyed to the notes below</text>')

def stroke(w=1.6,dash=None,fill='none'):
    d=f' stroke-dasharray="{dash}"' if dash else ''
    return f' fill="{fill}" stroke="{P}" stroke-width="{w}"{d}'

# airframe
o.append(f'<rect x="317" y="115" width="46" height="320" rx="23"{stroke()}/>')            # fuselage
o.append(f'<rect x="120" y="248" width="440" height="42" rx="12"{stroke()}/>')             # wing
o.append(f'<line x1="140" y1="269" x2="540" y2="269" stroke="{S}" stroke-width="1" stroke-dasharray="3 4"/>')  # spar/AC line
# front rotors
for cx in (184,496):
    o.append(f'<rect x="{cx-4}" y="210" width="8" height="42"{stroke(1.3)}/>')
    o.append(f'<ellipse cx="{cx}" cy="200" rx="58" ry="14"{stroke(1.3,dash="4 3")}/>')
    o.append(f'<circle cx="{cx}" cy="210" r="7"{stroke(1.4)}/>')
# tail rotor (dashed = stops/folds in cruise)
o.append(f'<rect x="336" y="435" width="8" height="30"{stroke(1.3)}/>')
o.append(f'<ellipse cx="340" cy="480" rx="46" ry="12"{stroke(1.3,dash="2 4")}/>')
o.append(f'<circle cx="340" cy="470" r="7"{stroke(1.4)}/>')
# battery (forward mass)
o.append(f'<rect x="330" y="140" width="20" height="34" rx="3" fill="{AMB}" opacity="0.85"/>')
# CG marker
cx,cy=340,260;r=7
o.append(f'<path d="M{cx} {cy} L{cx} {cy-r} A{r} {r} 0 0 1 {cx+r} {cy} Z" fill="{P}"/>')
o.append(f'<path d="M{cx} {cy} L{cx} {cy+r} A{r} {r} 0 0 1 {cx-r} {cy} Z" fill="{P}"/>')
o.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{P}" stroke-width="1.2"/>')
o.append(f'<text x="{cx+11}" y="{cy+3}" class="ts">CG</text>')

# numbered bubbles on diagram
bubbles=[('1',184,200),('2',430,269),('3',340,365),('4',340,157),('5',340,480),('6',250,269)]
for n,bx,by in bubbles:
    o.append(f'<circle cx="{bx}" cy="{by}" r="12" fill="{AMB}"/>')
    o.append(f'<text x="{bx}" y="{by+4}" text-anchor="middle" class="ts" style="fill:#fff;font-weight:500">{n}</text>')

# legend below, two columns
notes=[
 ('1','Largest rotor discs the airframe allows — low disk loading cuts hover power roughly 20–25%.'),
 ('2','Higher-aspect wing with a low-Reynolds laminar airfoil — the cruise-efficiency win that actually scales up from paper.'),
 ('3','LW-PLA shell over a carbon spar — drives the airframe mass fraction down; helps every phase.'),
 ('4','Battery placed forward as ballast — component mass sets the CG, so no dead lead and near-zero trim drag.'),
 ('5','Stop and fold the tail rotor in cruise — removes its drag once the wing carries the weight.'),
 ('6','Weight-on-wing cruise, and rush the hover→cruise transition — minimize time in the power-hungry regime.'),
]
o.append(f'<line x1="40" y1="512" x2="640" y2="512" stroke="{S}" stroke-width="0.75" opacity="0.5"/>')
colx=[40,360]; colw=270
y0=536
for i,(n,txt) in enumerate(notes):
    col=i//3; row=i%3
    x=colx[col]; y=y0+row*56
    o.append(f'<circle cx="{x+9}" cy="{y-4}" r="9" fill="{AMB}"/>')
    o.append(f'<text x="{x+9}" y="{y}" text-anchor="middle" class="ts" style="fill:#fff;font-weight:500">{n}</text>')
    lines=textwrap.wrap(txt, 40)
    for j,ln in enumerate(lines[:3]):
        o.append(f'<text x="{x+26}" y="{y-6+j*15}" class="ts">{esc(ln)}</text>')
o.append('</svg>')
open('diagrams/efficient-vtol.svg','w').write(''.join(o))
print('wrote diagrams/efficient-vtol.svg', len(''.join(o)))
