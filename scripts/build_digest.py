# -*- coding: utf-8 -*-
"""Build the compact paper-design digest that grounds the drone-design workflow.
Reads the verified paper-airplane specs and emits a one-line-per-design summary
(name, category, aerodynamic rationale, key geometry). Run from the repo root."""
import json
s = json.load(open('data/paper-airplanes.json'))['specs']
lines = []
for x in s:
    g = x['geometry']
    lines.append(
        f"- {x['name']} [{x['category'].split('(')[0].strip()}]: {x['why_best']} "
        f"| span {g['wingspan']}; dihedral {g['dihedral']}; aspect {g['aspect']}; CG {g['cg']}."
    )
digest = '\n'.join(lines)
open('data/paper-digest.txt', 'w').write(digest)
print(f'wrote data/paper-digest.txt  {len(digest)} chars')
