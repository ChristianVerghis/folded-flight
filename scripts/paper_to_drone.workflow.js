export const meta = {
  name: 'paper-to-drone-design',
  description: 'Translate verified paper-airplane principles into buildable 3D-printed drone concepts (with weighted-component placement) and rank VTOL efficiency levers',
  phases: [
    { title: 'Concepts', detail: 'design one 3D-printed drone concept per paper principle' },
    { title: 'Verify', detail: 'adversarially check Reynolds scaling, CG/static margin, printability' },
    { title: 'VTOL levers', detail: 'efficiency sweep across 5 engineering categories, ranked' },
    { title: 'Critic', detail: 'find missing high-value concepts' },
  ],
}

const DIGEST = "- The Needle Dart [fastest]: Speed comes from very high wing loading and a very low aspect ratio. Nearly all the paper's mass is stacked into layered folds along the deeply swept nose and keel, so weight is high while the exposed wing planform is tiny \u2014 the plane must fly fast to generate enough lift, giving a high stall speed and a fast, flat trajectory. The sharp swept-delta leading edge keeps flow attached and drag low at the low Reynolds numbers (~30,000-50,000) of a hand-thrown plane, and the deep centerline keel acts as a fixed vertical fin plus a nose ballast that pulls the CG well forward (~45-50% of length) for strong pitch stability. Stiff, small, low-camber wings resist deforming under a hard flat throw, so it converts arm speed directly into range rather than lift-induced climb-and-stall. | span ~120 mm (folded) from an A4/Letter sheet \u2014 roughly half the sheet width; a deliberately small span; dihedral 3-6 degrees, near-flat. Just enough for roll stability without adding drag or lift that would balloon the fast trajectory; aspect Very low, ~1.0-1.3 (short stubby wings). Low AR keeps induced-drag geometry compact and the wing stiff at speed; CG Forward, ~45-50% of body length back from the nose tip. Heavy layered nose + keel place mass ahead of the aerodynamic center for strong static pitch stability.\n- Suzanne (Collins/Ayoob distance glider) [longest distance]: Suzanne wins distance by being a two-phase flyer rather than a dart: a hard, up-angled launch turns muscle into altitude, then the forward CG and low-wing-loading planform convert that altitude into a long, flat, self-stabilizing glide, with the progressive dihedral keeping it stable across the whole launch-to-glide speed range. | span ~135-145 mm folded span (from a 210mm-wide A4 sheet); broad, deep wing; dihedral Progressive/variable: ~165 deg included angle near the nose root, ~155 deg at mid-wing (tips slightly up). Roughly 7-12 deg of net upsweep; aspect Low, ~1.6-2.0 (short, deep wing) \u2014 high area for low wing loading and float; CG Forward, ~28-32% of body length from the nose, set by the dense multi-layer blunt nose.\n- Nakamura Lock [Best cruiser / most stable slow floater]: The signature nose lock stacks and pins several paper layers at the front, concentrating mass forward so the CG sits well ahead of the wing's aerodynamic center \u2014 the strong static-stability margin that makes it self-correct instead of pitching or diving. That forward mass is paired with a broad, blunt, relatively low-loaded wing and a natural shallow dihedral (from folding-in-half then unfolding the wings to a Y), giving good roll stability and slow, floaty flight. At the low speeds and small chord of a paper plane (Reynolds number roughly 20,000-40,000) a plane that flies slowly and holds a steady low angle of attack simply glides farther; the Nakamura Lock's locked, non-crumpling nose keeps that CG and airfoil shape intact throw after throw, which is why it out-cruises flimsier dart designs. | span approx 14 cm (about 66% of the A4 width, tip to tip with wings level); dihedral shallow, about 8-12 degrees per wing (gentle Y) for roll stability without excess drag; aspect low-to-moderate, roughly 2.2 (broad chord, span ~14 cm, mean chord ~6.5 cm) \u2014 favors slow, stable, floaty glide over speed; CG well forward, about 28-32% of body length back from the blunt nose, held there by the stacked locked nose layers.\n- Sea Glider (High-Aspect-Ratio Paper Sailplane) [highest glide ratio]: Glide ratio equals lift-to-drag ratio, and at gliding speed the dominant loss is induced (lift-related) drag, whose coefficient falls in proportion to aspect ratio at a given wing area. The Sea Glider's long, thin, near-triangular wings give a high aspect ratio and a large area for very little mass, so wing loading is low, sink rate is small, and the plane trims to a slow, flat, efficient glide. The rolled leading-edge hem does double duty: it moves the CG forward to roughly the wing's quarter-chord for pitch stability, and it stiffens the leading edge so the airfoil holds a clean shape. Slight dihedral plus upturned winglets add roll/yaw stability and cut wingtip vortex drag, keeping the glide straight instead of spiralling. (Purpose-built high-aspect paper gliders in this family, like the Paperang, reach 12:1+; the simple Sea Glider glides well but a bit short of that.) | span approx 26-27 cm effective tip-to-tip. (The A4-derived square is 210x210 mm, so its raw diagonal is ~29.7 cm; folding down the keel and folding up the outer ~2 cm winglets reduces the flat span to roughly 26 cm.); dihedral 5-10 degrees (shallow up-Y) plus near-vertical winglets on the outer ~2 cm; aspect high for a paper plane, effective span-squared/area roughly 4-5 (long thin swept planform); this is what drives the low induced drag; CG far forward, ~18-22% of body length back from the nose, set by the rolled leading-edge hem \u2014 near the wing's quarter-chord.\n- The Bulldog Dart [most durable / crash-proof distance dart]: Folding the sharp point down and then folding the plane in on itself buries several paper layers into a short blunt nose, driving CG forward (roughly the front quarter to third of the body length, ahead of the aerodynamic center) for strong pitch stability. The layered blunt tip has no fragile point to crumple, so it spreads crash loads and survives head-on impacts. The heavy nose means it is a fast, penetrating flyer best given a gentle, level throw \u2014 thrown too hard it noses straight into the ground. | span ~14 cm span on Letter/A4 (each wing ~6 cm from spine); overall body length ~24 cm; dihedral shallow, ~5-8 deg upward Y for roll stability without sacrificing speed; aspect low, ~2.0-2.5 (short broad delta-ish wings) \u2014 rigid, crash-tolerant, forgiving at low Reynolds number; CG far forward, roughly the front quarter to third of body length back from the blunt nose (~25-30%), set by the tucked multi-layer nose.\n- The Ring-Wing Glider (Hollow Hoop / Tube Glider) [most surprising / novelty flyer \u2014 the design that flies best with no flat wing at all]: It flies because a hoop is a closed (annular) wing: the leading rim generates lift like a very short-chord wing bent into a full circle, and because the wing has no free tips, there is no distinct pair of trailing tip vortices \u2014 spanwise flow simply chases itself around the ring, which keeps induced losses tame at its tiny scale. The thick multi-fold band at the leading edge concentrates mass well ahead of the ring's aerodynamic center, so CG sits forward (~30-35% of body length) giving strong pitch stability \u2014 the nose-heavy rim keeps pointing into the airflow. The circular cross-section is inherently roll- and yaw-neutral (axisymmetric), so it self-stabilizes about its flight axis and resists tumbling; any slight spin off the fingers only reinforces gyroscopic axial stability. At the low Reynolds numbers of a hand-thrown toy (~2-4x10^4) a smooth low-camber ring avoids the leading-edge separation that stalls flat paper wings, so it settles into a steady, straight glide rather than diving or pitching. | span Ring diameter ~9 cm (the 'span' is the full hoop circumference, ~28 cm); dihedral 0 deg \u2014 a closed axisymmetric ring has no dihedral; roll stability comes from circular symmetry, not wing angle; aspect Very low effective aspect ratio (~1, approximate); the closed loop caps the tips so it does not spawn the usual pair of strong trailing tip vortices; CG ~30-35% of body length from the front rim; the double (optionally triple) 1/2-inch fold puts mass well ahead of the aerodynamic center.\n- The Harrier (Aerobatic Loop Glider) [best aerobatic looper]: Its looping ability comes from three things working together: a very forward CG (the nose is folded under itself two-to-three times, stacking mass ahead of the wing) which gives strong pitch stability and lets the tail carry a large up-trim without stalling; a low-aspect-ratio, moderately-loaded delta-ish wing that tolerates the high angle of attack of a loop without tip-stalling; and cut, adjustable trailing-edge elevons that add reflex (up-deflection) to create a nose-up pitching moment. Thrown hard and slightly up, the up-elevons plus forward CG convert that speed energy into a tight vertical loop; bend the elevons down and the same airframe reverts to a clean flat glide. The forward CG also keeps it recoverable \u2014 it noses back to level after the loop instead of tumbling. | span ~140 mm (folded from a Letter/A4 sheet started landscape); each wing ~60 mm semi-span from the keel; dihedral Slight positive, ~8-12 degrees (tips ~10 mm above roots) for roll recovery through the loop; aspect Low, ~2.0-2.5 (short, deep delta-dart wing) \u2014 resists tip stall at the high AoA a loop demands; CG Well forward: ~25-30% of body length from the nose, set by the multi-layer folded nose stack.\n- The Returning Boomerang Glider [best returning flight]: The return is a trimmed climbing loop, not real boomerang gyroscopics. A hard ~40-degree upward throw gives it enough kinetic energy to pull vertical; slight up-elevator (raised trailing edge) forces a continuous pitch-up so the flight path arcs over the top. Strong ~15-degree dihedral plus upturned wingtip winglets make it extremely roll-stable and add a touch of yaw damping, so instead of spiraling off it holds a tight, repeatable loop. CG sits ~25% back from the leading edge \u2014 far enough forward to be pitch-stable, far enough aft that modest elevator deflection commands the big pitch rate needed to close the loop. Low wing loading (light paper, broad wing) and the low-Reynolds regime (~30,000) mean it flies slowly enough that the loop diameter stays small (roughly 4-6 m), bringing it back to the thrower's hand. | span approx. 20 cm (each wing ~9 cm semi-span from a folded A4); dihedral ~15 degrees (strong, for roll stability and a controlled loop); aspect low, ~4:1 (broad wing, short span typical of a folded dart-glider hybrid); CG ~25% of wing chord back from the leading edge, held forward by the multi-layer folded nose.\n- The Tumblewing (Walkalong Glider) [most imaginative / hovers on ridge lift]: The tumblewing wins the \"imaginative\" category because it does not glide at all - it autorotates. Cut low across the wind, the wing continuously spins about its long (spanwise) axis, alternately flying and stalling each half-turn so that lift is generated Flettner/Magnus-style like a spinning rotor rather than by a fixed airfoil. Because it carries zero ballast, its wing loading is extraordinarily low (its flight is \"more akin to confetti\"), so a gentle updraft can support it. That is what makes it a walkalong glider: the pilot walks behind it holding a paddle tilted ~30 degrees, and the ridge lift (deflected updraft) off the moving board sustains the tumbling wing indefinitely. The tiny chord and slow speed put it at very low Reynolds number where the alternating-stall rotor mechanism, not smooth attached flow, is what keeps it aloft. Upturned winglets at each end kill spanwise drift and lock the spin axis straight so it tumbles in place instead of veering off. | span 16 cm span (the long dimension) x 4 cm chord (the short dimension); winglets ~1 cm tall at each tip; dihedral none in the fixed sense - a very slight spanwise arc (a few degrees) to keep the spin axis straight; the wing rotates continuously about its spanwise axis; aspect planform aspect ratio roughly 1:4 (span:chord ~4). This is a rotor wing, so effective aspect ratio is not the operative parameter - spin rate and wing loading are; CG CG sits on the centerline at the geometric center of the strip; there is deliberately NO nose ballast, giving near-zero wing loading.";

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
