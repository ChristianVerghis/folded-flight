export const meta = {
  name: 'paper-airplane-field-guide',
  description: 'Research + verify the best paper airplanes across categories, returning buildable specs and normalized geometry for diagramming',
  phases: [
    { title: 'Research', detail: 'one expert agent per design (fold steps, geometry, aero)' },
    { title: 'Verify', detail: 'adversarially check folds and facts, correct errors' },
    { title: 'Critic', detail: 'find any missing best-category' },
  ],
}

const COORD = `COORDINATE CONVENTIONS (critical — I will render these directly as SVG):
- top_view_outline: the finished plane's planform seen from ABOVE, as an ordered list of {x,y} points tracing the outline clockwise. Box is 0..100 in both axes. Nose points UP: nose tip near y=0, tail near y=100. Symmetric about x=50. Include the fuselage keel and both wings so the silhouette reads correctly.
- crease_lines: the fold lines drawn on the FLAT unfolded sheet (same 0..100 box, sheet portrait: x=0..100 width, y=0..100 length). type = valley | mountain | cut | centerline. This is the crease pattern.
- side_profile: the plane seen from the SIDE, ordered {x,y} points. Nose at LEFT (x=0), tail at RIGHT (x=100), y is height (0 = bottom). Show the dihedral/keel silhouette.
- cg_point: approximate center of gravity in the top_view box.
Give real, sensible coordinates — an experienced folder should recognize the shape.`

const SPEC_SCHEMA = {
  type: 'object', additionalProperties: false,
  required: ['name','category','difficulty','paper','why_best','fold_steps','geometry','flight','diagram','fun_fact'],
  properties: {
    name: { type: 'string' },
    aka: { type: 'string' },
    category: { type: 'string', description: 'the "best" dimension this design wins, e.g. fastest, longest distance' },
    origin: { type: 'string', description: 'designer / historical origin if known' },
    difficulty: { type: 'string', enum: ['easy','medium','hard'] },
    paper: { type: 'string', description: 'recommended paper, e.g. A4 80gsm or US Letter' },
    why_best: { type: 'string', description: '1-3 sentences: the aerodynamic reason this design excels at its category' },
    fold_steps: { type: 'array', items: { type: 'object', additionalProperties: false, required: ['n','text'], properties: { n: { type: 'integer' }, text: { type: 'string' } } } },
    geometry: { type: 'object', additionalProperties: false, required: ['wingspan','dihedral','aspect','cg','notes'],
      properties: { wingspan: { type: 'string' }, dihedral: { type: 'string' }, aspect: { type: 'string' }, cg: { type: 'string' }, notes: { type: 'string' } } },
    flight: { type: 'object', additionalProperties: false, required: ['throw','speed','glide','behavior'],
      properties: { throw: { type: 'string' }, speed: { type: 'string' }, glide: { type: 'string' }, behavior: { type: 'string' } } },
    diagram: { type: 'object', additionalProperties: false, required: ['top_view_outline','crease_lines','side_profile','cg_point','features'],
      properties: {
        top_view_outline: { type: 'array', items: { type: 'object', additionalProperties: false, required: ['x','y'], properties: { x: { type: 'number' }, y: { type: 'number' } } } },
        crease_lines: { type: 'array', items: { type: 'object', additionalProperties: false, required: ['x1','y1','x2','y2','type'], properties: { x1: { type: 'number' }, y1: { type: 'number' }, x2: { type: 'number' }, y2: { type: 'number' }, type: { type: 'string', enum: ['valley','mountain','cut','centerline'] } } } },
        side_profile: { type: 'array', items: { type: 'object', additionalProperties: false, required: ['x','y'], properties: { x: { type: 'number' }, y: { type: 'number' } } } },
        cg_point: { type: 'object', additionalProperties: false, required: ['x','y'], properties: { x: { type: 'number' }, y: { type: 'number' } } },
        features: { type: 'array', items: { type: 'string' }, description: 'short labeled callouts, e.g. "swept nose", "winglets up", "long keel"' },
      } },
    fun_fact: { type: 'string' },
  },
}

const VERIFY_SCHEMA = {
  type: 'object', additionalProperties: false,
  required: ['verdict','issues','corrected_spec'],
  properties: {
    verdict: { type: 'string', enum: ['confirmed','corrected','rejected'] },
    issues: { type: 'array', items: { type: 'string' } },
    corrected_spec: SPEC_SCHEMA,
  },
}

const CRITIC_SCHEMA = {
  type: 'object', additionalProperties: false, required: ['missing'],
  properties: { missing: { type: 'array', items: { type: 'object', additionalProperties: false, required: ['name','category','reason'], properties: { name: { type: 'string' }, category: { type: 'string' }, reason: { type: 'string' } } } } },
}

const DESIGNS = [
  { key: 'dart', brief: 'The classic needle Dart — the FASTEST paper airplane: sharp swept nose, small wings, thrown hard and flat.' },
  { key: 'record_glider', brief: "The world-record DISTANCE plane — John Collins's 'Suzanne' style glider (record thrown by Joe Ayoob). A glide+transition design, thrown very hard.  Verify the current Guinness distance record holder & figures." },
  { key: 'nakamura_cruiser', brief: 'The Nakamura Lock glider — the best CRUISER / most stable slow floater with a locking nose, gentle long glides.' },
  { key: 'sailplane', brief: 'A high-aspect-ratio GLIDER optimised for the MOST AERODYNAMIC / highest glide ratio (long thin wings, e.g. a paper sailplane / "Sea Glider" type).' },
  { key: 'bulldog', brief: 'The Bulldog Dart / heavy-nose STUNT plane — MOST DURABLE & robust, blunt reinforced nose that survives crashes and does stunts.' },
  { key: 'ring_tube', brief: 'The HOLLOW ring-wing / hoop / tube glider — a cylinder or hoop that flies (annular wing). Explain why the tube flies.' },
  { key: 'harrier', brief: 'An AEROBATIC / stunt glider (e.g. The Harrier) that can loop, with adjustable elevons at the trailing edge.' },
  { key: 'boomerang', brief: 'A BOOMERANG / returning paper plane that circles back to the thrower.' },
  { key: 'tumblewing', brief: 'The Tumblewing WALKALONG glider — a novel design that hovers on the ridge lift of a moving board held behind it. Imaginative category.' },
]

phase('Research')
const results = await pipeline(
  DESIGNS,
  d => agent(
    `You are a world-class paper-airplane (paper aircraft / origami aerodynamics) expert. Produce an accurate, BUILDABLE spec for this design. Use web search/fetch to confirm fold sequences and any factual claims (designers, dates, records).

DESIGN: ${d.brief}

Requirements:
- fold_steps: a correct, ordered, followable sequence from a flat sheet to finished plane. Be specific (which corner to which line). 6-12 steps typical.
- why_best: the real aerodynamic reason it wins its category (CG position, wing loading, aspect ratio, dihedral, Reynolds number, etc.).
- geometry + flight: concrete, sensible values.
- diagram: fill ALL geometry fields with real coordinates.

${COORD}

Return ONLY the structured spec.`,
    { label: `research:${d.key}`, phase: 'Research', schema: SPEC_SCHEMA }
  ),
  (spec, d) => agent(
    `Adversarially verify this paper-airplane spec. Be a skeptic.

1. FOLD CHECK: mentally fold a flat sheet following fold_steps in order. Do they actually yield the described planform (matching top_view_outline)? Are any steps missing, out of order, or impossible? 
2. FACT CHECK: verify designer/origin, and any record claims, against reality (use web search). The distance-record facts especially must be correct.
3. GEOMETRY CHECK: are the diagram coordinates coherent (nose up in top view, symmetric about x=50, side profile nose-left, CG in a sane spot)? Fix obviously wrong points.

Return verdict (confirmed if essentially right, corrected if you fixed things, rejected only if hopeless), a list of issues found, and corrected_spec = the full, corrected spec (return the whole spec even if unchanged).

SPEC TO VERIFY:
${JSON.stringify(spec)}`,
    { label: `verify:${d.key}`, phase: 'Verify', schema: VERIFY_SCHEMA }
  ).then(v => ({ ...v, key: d.key }))
)

const clean = results.filter(Boolean).filter(v => v.verdict !== 'rejected')
const specs = clean.map(v => v.corrected_spec)
const allIssues = clean.flatMap(v => (v.issues || []).map(i => `[${v.key}] ${i}`))

phase('Critic')
const critic = await agent(
  `Here are ${specs.length} paper-airplane designs covering these categories: ${specs.map(s => s.category).join('; ')}.
The user wanted the "best" across many forms: most aerodynamic, fastest, most durable, cruiser, hollow, etc. — imaginative coverage.
Name any genuinely distinct "best" category or iconic design that is MISSING and would round out a definitive field guide (max 3). If coverage is already excellent, return an empty list.`,
  { schema: CRITIC_SCHEMA }
)

return { specs, issues: allIssues, missing: critic.missing }
