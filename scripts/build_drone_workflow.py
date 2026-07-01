# -*- coding: utf-8 -*-
import json
digest = open('data/paper-digest.txt').read()
DIGEST_JS = json.dumps(digest)

JS = r'''export const meta = {
  name: 'paper-to-drone-design',
  description: 'Translate verified paper-airplane principles into buildable 3D-printed drone concepts (with weighted-component placement) and rank VTOL efficiency levers',
  phases: [
    { title: 'Concepts', detail: 'design one 3D-printed drone concept per paper principle' },
    { title: 'Verify', detail: 'adversarially check Reynolds scaling, CG/static margin, printability' },
    { title: 'VTOL levers', detail: 'efficiency sweep across 5 engineering categories, ranked' },
    { title: 'Critic', detail: 'find missing high-value concepts' },
  ],
}

const DIGEST = %DIGEST%;

const COORD = `COORDINATES (I render these directly): work in a 0..100 box both axes.
- top_view_outline: planform seen from ABOVE, ordered {x,y}, nose UP (nose near y=0, tail near y=100), symmetric about x=50.
- side_profile: seen from the SIDE, ordered {x,y}, nose at LEFT (x=0), tail RIGHT (x=100), y = height (0 bottom).
- components: each weighted/major component as {label, x, y, mass_hint} placed in the TOP-VIEW box (battery, flight controller, motor(s), servo, payload, GPS, etc.). mass_hint = heavy | medium | light.
- cg_point {x,y}: resulting centre of gravity in the top-view box. It MUST sit ahead of (lower y than) the wing's aerodynamic centre for static stability — say so in weighted_components.`

const CONCEPT_SCHEMA = {
  type: 'object', additionalProperties: false,
  required: ['name','one_liner','paper_lineage','drone_type','principle','reynolds_verdict','reynolds_note','realization_3dprint','weighted_components','efficiency_gain','tradeoffs','key_specs','build_difficulty','diagram'],
  properties: {
    name: { type: 'string' },
    one_liner: { type: 'string', description: 'short tagline' },
    paper_lineage: { type: 'string', description: 'which paper design(s) and the exact principle borrowed' },
    drone_type: { type: 'string', description: 'e.g. tri-tiltrotor VTOL, tailless flying-wing VTOL, ducted box-wing, monocopter' },
    principle: { type: 'string', description: 'the transferable aerodynamic/structural idea, stated crisply' },
    reynolds_verdict: { type: 'string', enum: ['scales','partially-scales','does-not-scale'] },
    reynolds_note: { type: 'string', description: 'honest note on whether the paper-scale (Re~30k) effect survives at drone Re (~1e5-5e5)' },
    realization_3dprint: { type: 'string', description: 'concrete print approach: materials (LW-PLA/PETG/TPU/carbon spar), structure, hinges, joints' },
    weighted_components: { type: 'string', description: 'WHERE the heavy components go and why (CG/static-margin reasoning)' },
    efficiency_gain: { type: 'string', description: 'what improves + rough magnitude + the physics' },
    tradeoffs: { type: 'string' },
    key_specs: { type: 'object', additionalProperties: false, required: ['span','aspect','auw','cruise','hover'],
      properties: { span: { type: 'string' }, aspect: { type: 'string' }, auw: { type: 'string', description: 'all-up weight estimate' }, cruise: { type: 'string' }, hover: { type: 'string' } } },
    build_difficulty: { type: 'string', enum: ['easy','medium','hard'] },
    diagram: { type: 'object', additionalProperties: false, required: ['top_view_outline','side_profile','components','cg_point'],
      properties: {
        top_view_outline: { type: 'array', items: { type: 'object', additionalProperties: false, required: ['x','y'], properties: { x: { type: 'number' }, y: { type: 'number' } } } },
        side_profile: { type: 'array', items: { type: 'object', additionalProperties: false, required: ['x','y'], properties: { x: { type: 'number' }, y: { type: 'number' } } } },
        components: { type: 'array', items: { type: 'object', additionalProperties: false, required: ['label','x','y','mass_hint'], properties: { label: { type: 'string' }, x: { type: 'number' }, y: { type: 'number' }, mass_hint: { type: 'string', enum: ['heavy','medium','light'] } } } },
        cg_point: { type: 'object', additionalProperties: false, required: ['x','y'], properties: { x: { type: 'number' }, y: { type: 'number' } } },
      } },
  },
}

const VERIFY_SCHEMA = {
  type: 'object', additionalProperties: false, required: ['verdict','issues','corrected'],
  properties: {
    verdict: { type: 'string', enum: ['confirmed','corrected','rejected'] },
    issues: { type: 'array', items: { type: 'string' } },
    corrected: CONCEPT_SCHEMA,
  },
}

const LEVER_ITEM = {
  type: 'object', additionalProperties: false, required: ['name','mechanism','impact','cost','printable_implementation','priority','phase'],
  properties: {
    name: { type: 'string' },
    mechanism: { type: 'string', description: 'the physics' },
    impact: { type: 'string', description: 'hover vs cruise vs range, rough magnitude' },
    cost: { type: 'string', description: 'weight / complexity / money' },
    printable_implementation: { type: 'string' },
    priority: { type: 'string', enum: ['high','medium','low'] },
    phase: { type: 'string', enum: ['hover','cruise','transition','all'] },
  },
}
const LEVERS_SCHEMA = { type: 'object', additionalProperties: false, required: ['levers'], properties: { levers: { type: 'array', items: LEVER_ITEM } } }
const RANKED_ITEM = { type: 'object', additionalProperties: false, required: ['rank','name','mechanism','impact','cost','printable_implementation','priority','phase'],
  properties: { rank: { type: 'integer' }, name: { type: 'string' }, mechanism: { type: 'string' }, impact: { type: 'string' }, cost: { type: 'string' }, printable_implementation: { type: 'string' }, priority: { type: 'string', enum: ['high','medium','low'] }, phase: { type: 'string', enum: ['hover','cruise','transition','all'] } } }
const RANKED_SCHEMA = { type: 'object', additionalProperties: false, required: ['levers'], properties: { levers: { type: 'array', items: RANKED_ITEM } } }
const CRITIC_SCHEMA = { type: 'object', additionalProperties: false, required: ['missing'], properties: { missing: { type: 'array', items: { type: 'object', additionalProperties: false, required: ['name','why'], properties: { name: { type: 'string' }, why: { type: 'string' } } } } } }

const CONCEPTS = [
  { key: 'cg_ballast', brief: "WEIGHTED-NOSE principle (Needle Dart / Nakamura forward CG): treat the battery as structural nose ballast. Design a printed fuselage whose dense nose bay sets a forward CG and correct static margin. This is the core 'weighted 3D-printed components' idea, applied to a general fixed-wing / the tiltrotor VTOL." },
  { key: 'high_ar_wing', brief: "HIGH-ASPECT-RATIO cruise wing (Sea Glider / Edmond Hui Paperang, >12:1 glide): a long slender printed wing with a carbon spar to raise cruise L/D and range on a VTOL. Address how long wings complicate hover roll control." },
  { key: 'ducted_boxwing', brief: "RING-WING / annular principle (Ring-Wing Glider): ducted/shrouded rotors + a closed box-wing to cut induced drag and raise static thrust & prop safety. CRITICAL: verify whether the paper ring-wing (Re~30k) benefit is real at drone Re, and whether ducts/box-wing help at drone scale (they do for different reasons)." },
  { key: 'tailless_flywing', brief: "TAILLESS / elevon principle (The Harrier): a tailless flying-wing VTOL with reflex airfoil and elevons, cutting tail weight and wetted area. Trade CG sensitivity for efficiency." },
  { key: 'autorotation_recovery', brief: "AUTOROTATION / samara principle (Tumblewing walkalong + maple-seed): passive safe descent on power loss, and/or a monocopter (single powered blade) that hovers with one actuator for extreme simplicity/efficiency. Explain autorotative energy recovery." },
  { key: 'energy_glide_profile', brief: "TWO-PHASE ENERGY MANAGEMENT (Suzanne: launch-energy then glide): a VTOL mission profile that climbs on rotors, stops/feathers props, and glides (dead-stick) for range; optional regenerative descent. Efficiency is in the flight profile, not just the airframe." },
  { key: 'passive_stability', brief: "PASSIVE STABILITY (dihedral + washout, seen across the gliders): a printed polyhedral wing with built-in dihedral and washout so the airframe is naturally stable, reducing active-control energy and improving gust rejection." },
  { key: 'snapfit_structure', brief: "SELF-LOCKING STRUCTURE (Nakamura lock): a 3D-print methodology — snap-fit self-locking joints, print-in-place TPU living hinges (for the tilt mechanism), and layered/gyroid stiffening — plus a principled rule for placing weighted components for best stiffness-to-weight and CG." },
  { key: 'blown_wing', brief: "DISTRIBUTED PROPULSION / BLOWN WING (prop-wash over wing): the wing tilt-rotors blow over the wing to raise CLmax, shrinking the wing and easing the hover-to-cruise transition (distributed electric propulsion). Assess efficiency honestly." },
]

phase('Concepts')
const conceptResults = await pipeline(
  CONCEPTS,
  c => agent(
    `You are a senior UAV / aircraft design engineer. Use these VERIFIED paper-airplane design principles as inspiration (each includes the real aerodynamic rationale):

${DIGEST}

Develop the following into a concrete, BUILDABLE 3D-printed drone concept. Be quantitative and physically honest. IMPORTANT scaling reality: paper planes fly at Reynolds ~30,000-50,000; real 3D-printed drones cruise at Re ~ 100,000-500,000, so some low-Re tricks do NOT transfer. State the truth in reynolds_verdict/reynolds_note.

CONCEPT: ${c.brief}

Emphasise (a) WHERE the weighted components go and the CG/static-margin logic, and (b) how it is actually printed (LW-PLA, PETG, TPU hinges, carbon spar). ${COORD}

Return only the structured concept.`,
    { label: `design:${c.key}`, phase: 'Concepts', schema: CONCEPT_SCHEMA }
  ),
  (spec, c) => agent(
    `Adversarially verify this 3D-printed drone concept as a skeptical aerospace engineer. Be harsh but fair.
1. REYNOLDS/SCALING: does the borrowed paper principle actually improve efficiency at DRONE Reynolds numbers, or is it a low-Re artifact? Correct any overclaim.
2. STABILITY: is the weighted-component placement / CG physically sound (CG ahead of the neutral point, sane static margin ~5-15%)? Check the diagram cg_point vs the wing position.
3. PRINTABILITY & WEIGHT: is it realistically 3D-printable at the claimed all-up weight? Flag fantasy.
4. EFFICIENCY CLAIMS: are they quantitatively plausible (momentum theory for hover, L/D for cruise), not hand-wavy?
5. GEOMETRY: are diagram coords coherent (nose-up top view symmetric about x=50; nose-left side view; components sensible)?
Fix problems. Return verdict, a list of issues, and corrected = the full corrected concept (return it whole even if unchanged).

CONCEPT:
${JSON.stringify(spec)}`,
    { label: `verify:${c.key}`, phase: 'Verify', schema: VERIFY_SCHEMA }
  ).then(v => ({ ...v, key: c.key }))
)

const concepts = conceptResults.filter(Boolean).filter(v => v.verdict !== 'rejected').map(v => v.corrected)
const issues = conceptResults.filter(Boolean).flatMap(v => (v.issues || []).map(i => `[${v.key}] ${i}`))

phase('VTOL levers')
const CATS = [
  'hover / rotor & disk-loading efficiency',
  'cruise aerodynamics, wing & L/D',
  'structure, weight fraction & 3D-printing',
  'VTOL transition & flight profile / energy management',
  'propulsion, motor/prop matching & electronics energy',
]
const leverSets = await parallel(CATS.map(cat => () => agent(
  `You are optimising a 3D-PRINTED TRI-TILTROTOR VTOL: a fixed wing with two wing-mounted tilt-rotors + one tail rotor, motors tilting from vertical (hover) to horizontal (cruise). Focus ONLY on this category: "${cat}".
List the highest-impact EFFICIENCY levers in this category. For each give: mechanism (physics), impact (say whether it helps hover, cruise, transition, or range, with a rough magnitude), cost (weight/complexity/money), printable_implementation, priority, and phase. Be concrete and quantitative; note any Reynolds/scale caveat. Return 3-5 strong levers.`,
  { label: `levers:${cat.split(' ')[0]}`, phase: 'VTOL levers', schema: LEVERS_SCHEMA }
)))
const allLevers = leverSets.filter(Boolean).flatMap(s => s.levers)

const ranked = await agent(
  `Here are candidate efficiency levers for a 3D-printed tri-tiltrotor VTOL, gathered across engineering categories. Dedupe overlapping ones, SANITY-CHECK the physics (reject or fix anything that violates momentum theory / energy reasoning or that won't actually help at drone scale), and return the FINAL ranked list, highest impact-per-cost first (rank starting at 1). Keep the 10-14 strongest. Each keeps crisp impact + priority + phase.

CANDIDATES:
${JSON.stringify(allLevers)}`,
  { label: 'rank + verify levers', phase: 'VTOL levers', schema: RANKED_SCHEMA }
)

phase('Critic')
const critic = await agent(
  `These future 3D-printed drone concepts were derived from paper-airplane principles: ${concepts.map(c => c.name + ' — ' + c.drone_type).join('; ')}.
Name up to 3 genuinely distinct, high-value concepts or principles that are MISSING and would round out "what paper flight teaches real 3D-printed drone design". Empty list if coverage is already excellent.`,
  { schema: CRITIC_SCHEMA }
)

return { concepts, vtol_levers: ranked.levers, issues, missing: critic.missing }
'''

JS = JS.replace('%DIGEST%', DIGEST_JS)
open('scripts/paper_to_drone.workflow.js','w').write(JS)
print('wrote scripts/paper_to_drone.workflow.js', len(JS), 'bytes')
