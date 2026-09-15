# folded-flight

**From paper airplanes to 3D-printed drones — a two-volume aerodynamics field guide.**

## What it is

Two self-contained HTML guides, generated from hand-checked JSON data by a small set of dependency-free Python scripts:

- **Volume I — `guides/paper-airplanes.html`.** Nine paper airplanes, one per discipline (fastest, farthest, best cruiser, highest glide ratio, most durable, ring-wing, aerobatic, boomerang, walkalong). Each plate has a plan view, side elevation, crease pattern, full fold sequence, geometry and flight tables, and the aerodynamic reason the design wins its category.
- **Volume II — `guides/drones.html`.** Nine 3D-printable drone concepts, each derived from one paper-airplane principle and rated on whether that principle survives the jump from paper-plane Reynolds numbers (Re ~30,000-50,000) to drone cruise (Re ~100,000-500,000). It closes with a ranked list of thirteen efficiency levers for a printed tri-tiltrotor VTOL.

Both volumes are plain HTML with inline SVG. Open them in a browser; nothing else is needed.

The thread that ties the volumes together is a single finding about what transfers across scale:

| Transfers? | What | Why |
|---|---|---|
| Fully | Mass placement: battery as forward ballast to set the CG | Pure rigid-body statics; Reynolds-independent. Place the heavy parts you already carry so the CG sits ahead of the neutral point (roughly 5-15 % static margin). No dead lead. |
| Even better at scale | High-aspect-ratio wing (Sea Glider / Paperang lineage) | Long slender wings raise L/D more at drone Re, not less. |
| Does not transfer | Swept deltas, stubby low-aspect wings, ring/annular wings | They only work because a slow paper plane tolerates flow separation; scaled up they are just drag. |

## Why I built it

The project started from a simple question, *what are the best paper airplanes, and why?*, and I wanted a defensible answer rather than a listicle. Once the paper-airplane data existed with normalised geometry, the natural follow-up was whether any of those folded-paper lessons hold for the 3D-printed fixed-wing and VTOL drones I am interested in building. Volume II is that follow-up: it takes each paper principle seriously, works out the Reynolds-number consequences, and says plainly which ideas scale and which do not. Everything is rendered from structured data so the diagrams always match the specs and the whole thing can be regenerated with one command.

## Status

As of 2026-09-15:

- **Volume I (paper airplanes): complete.** All nine designs have fold sequences, geometry, flight notes, and rendered plates. Content was finalised 2026-06-30.
- **Volume II (drones): complete.** All nine concepts and the 13-lever VTOL efficiency ranking are written up and rendered. Content was finalised 2026-06-30.
- **Not started:** the critic pass in each workflow suggested extra entries that were never written up. For Volume I: a maximum-time-aloft floater, a catapult-launched glider, and an autorotating whirlybird. For Volume II: field-adjustable trim tabs, flat-plate camber and leading-edge shaping, and spin-resistant planform geometry. These are recorded under `missing` in the two data files and listed at the end of each guide.
- The project is otherwise archived: `./build.sh` regenerates every output byte-for-byte from the tracked data, and no further content work is planned.

None of the drone concepts have been built or flown. They are design studies with stated assumptions, not tested aircraft.

## Contents

### Volume I — the nine paper airplanes ([`guides/paper-airplanes.html`](guides/paper-airplanes.html))

| # | Design | Best at |
|---|--------|---------|
| 01 | The Needle Dart | fastest / flattest trajectory |
| 02 | Suzanne (Collins/Ayoob) | longest distance (former Guinness holder) |
| 03 | Nakamura Lock | best cruiser / most stable float |
| 04 | Sea Glider | highest glide ratio |
| 05 | The Bulldog Dart | most durable / crash-proof |
| 06 | Ring-Wing Glider | hollow novelty (NASA JPL hoop) |
| 07 | The Harrier | best aerobatic looper |
| 08 | Boomerang glider | returns to the thrower |
| 09 | The Tumblewing | walkalong glider (hovers on ridge lift) |

Specimen index of all nine planforms: [`diagrams/paper-index.svg`](diagrams/paper-index.svg). Source data: [`data/paper-airplanes.json`](data/paper-airplanes.json).

### Volume II — the nine drone concepts ([`guides/drones.html`](guides/drones.html))

| # | Concept | Type | Borrows | Scales? |
|---|---------|------|---------|---------|
| 01 | Keelhaul | pusher fixed-wing | Dart nose-mass, battery-as-ballast CG | partial |
| 02 | Albatross-12 | high-AR quadplane VTOL | Sea Glider slender wing | fully |
| 03 | Torus "Halo" | ducted box-wing VTOL | ring-wing to ducts + closed wing | partial |
| 04 | HAR-1 "Mantis" | tailless flying-wing tri-tiltrotor | Harrier elevons / tailless | partial |
| 05 | Samara-1 | monocopter | Tumblewing / samara autorotation | partial |
| 06 | Suzanne-V "Vireo" | quad-tiltrotor VTOL sailplane | two-phase climb-then-glide | partial |
| 07 | Polyhedra P1 | passively-stable pusher glider | dihedral + washout stability | partial (easiest build) |
| 08 | Nakamura Locke | snap-lock tri-tiltrotor cruiser | self-locking structure + forward CG | partial |
| 09 | DEP-1 "Bellwether" | blown-wing quad-tiltrotor | distributed propulsion over the wing | partial |

### Making the tiltrotor VTOL more efficient

The top of the ranked list, by impact-per-cost across hover, cruise, structure, transition, and propulsion:

1. Minimise disk loading: the biggest rotor discs the frame allows, roughly 20-25 % less hover power (hover)
2. Drive airframe mass fraction down: LW-PLA, carbon spar, selective infill (all phases)
3. Weight-on-wing cruise: tilt fully horizontal, cruise-matched prop, stop or fold the tail rotor (cruise)
4. Match blade solidity, twist, and RPM to the low-Re rotor regime (hover)
5. Unidirectional carbon spar and boom; printed parts only as shear web and connectors (all)
6. Flight scheduling: rush the transition corridor, cruise at best-L/D speed (all)
7. Match motor Kv and cell count so hover sits at 50-65 % throttle (hover)
8. Higher-aspect wing: span extension or taper (cruise)

The full 13-lever list with mechanism, cost, and printable implementation is in [`guides/drones.html`](guides/drones.html) and [`data/drone-concepts.json`](data/drone-concepts.json). The annotated tri-tiltrotor diagram is [`diagrams/efficient-vtol.svg`](diagrams/efficient-vtol.svg).

### Repository layout

```
folded-flight/
├── README.md
├── LICENSE                     # MIT — scripts
├── LICENSE-docs.md             # CC BY 4.0 — guide text, data, figures
├── project.yml                 # local project manifest (metadata only)
├── build.sh                    # regenerate everything (data -> guides/diagrams)
├── data/
│   ├── paper-airplanes.json    # 9 paper designs (folds, geometry, flight) + review notes
│   ├── drone-concepts.json     # 9 drone concepts + 13 ranked VTOL levers + review notes
│   └── paper-digest.txt        # generated: one-line-per-design digest
├── guides/
│   ├── paper-airplanes.html    # Vol I (generated)
│   └── drones.html             # Vol II (generated)
├── diagrams/
│   ├── paper-index.svg         # generated: specimen index of all 9 planforms
│   └── efficient-vtol.svg      # generated: annotated tri-tiltrotor diagram
└── scripts/
    ├── build_digest.py
    ├── build_paper_guide.py
    ├── build_paper_index_svg.py
    ├── build_drone_guide.py
    ├── build_vtol_diagram.py
    ├── build_drone_workflow.py       # emits paper_to_drone.workflow.js
    ├── paper_field_guide.workflow.js # Vol I research + verify workflow (prompts + schemas)
    └── paper_to_drone.workflow.js    # generated: Vol II design + verify workflow
```

The `data/*.json` files are the source of truth. Everything under `guides/`, `diagrams/`, plus `data/paper-digest.txt` and `scripts/paper_to_drone.workflow.js`, is generated and tracked so the repo is browsable without running anything.

## How it's built

### Pipeline

All generators are pure functions of the JSON data and use only the Python 3 standard library. `build.sh` runs them in order from the repo root:

| Script | Reads | Writes |
|---|---|---|
| `scripts/build_digest.py` | `data/paper-airplanes.json` | `data/paper-digest.txt` |
| `scripts/build_paper_guide.py` | `data/paper-airplanes.json` | `guides/paper-airplanes.html` |
| `scripts/build_paper_index_svg.py` | `data/paper-airplanes.json` | `diagrams/paper-index.svg` |
| `scripts/build_drone_guide.py` | `data/drone-concepts.json` | `guides/drones.html` |
| `scripts/build_vtol_diagram.py` | `data/drone-concepts.json` | `diagrams/efficient-vtol.svg` |
| `scripts/build_drone_workflow.py` | `data/paper-digest.txt` | `scripts/paper_to_drone.workflow.js` |

Plan views, side elevations, crease patterns, and component/CG markers are drawn directly from each design's normalised 0-100 coordinate geometry in the JSON, so the figures cannot drift from the specs.

To regenerate:

```bash
./build.sh
```

Requires Python 3. The build is deterministic; `./build.sh && git diff --exit-code` passes on a clean checkout.

### How the content was produced

The design specs were drafted with AI assistance and then cross-checked, using the two workflow definitions in `scripts/*.workflow.js`. Each workflow is a set of prompts and JSON schemas run against a multi-agent runner (not included in this repo; the files reference `agent`, `parallel`, `pipeline`, and `phase` primitives supplied by that runner). The structure was:

1. **Fan-out.** One agent per design or concept produces a structured spec: fold steps or engineering design, plus normalised diagram geometry.
2. **Review pass.** A second agent re-checks each spec. For paper planes: re-fold the sequence step by step, confirm it yields the drawn planform, and fact-check designers and records. For drones: check Reynolds scaling, CG and static-margin reasoning, printability, and whether efficiency figures are quantitatively defensible.
3. **Critic.** A final agent flags categories worth adding.

The review pass is recorded, not just claimed: both data files carry an `issues` array (63 entries each) listing what was checked, what passed, and what was changed. Corrections it forced include:

- Fixed the Bulldog Dart fold order (the paper flips mid-sequence) and reversed the claim that it wants a hard throw (it prefers a soft one).
- Corrected the paper-airplane distance-record chain: Suzanne (69.14 m, 2012), then 77.13 m (2022), then the current 88.31 m (Boeing engineers, December 2022).
- Corrected static margin to `(neutral point - CG) / MAC` for tailed layouts; the wing aerodynamic centre is only the neutral point for a tailless wing.
- Rejected a physically impossible battery spec (a 500 g pack claimed at 178 Wh, about twice the best real LiPo energy density) and re-derived the range figures that depended on it.
- Flagged that a TPU living hinge cannot be co-printed into a PLA/PETG surface on a single-nozzle printer.
- Downgraded several efficiency percentages to defensible ranges.

The review was a second model pass with web lookups for facts, not an independent human engineering review, and nothing has been physically folded to spec, printed, or flown as part of this project. Treat the numbers as reasoned estimates.

### Sources and credits

Paper designs and facts draw on Fold'N'Fly, NASA JPL's "Ring Wing Glider" activity, John M. Collins (*The New World Champion Paper Airplane Book*; the tumblewing), Slater Harrison / ScienceToyMaker (walkalong gliding), Art of Manliness (Bulldog Dart), and Guinness World Records (distance). Drone concepts are original syntheses grounded in standard UAV aerodynamics (momentum theory for hover, L/D for cruise).

## License

- **Guide text, data, and figures** (`guides/`, `data/`, `diagrams/`, and the prose in this README) are licensed under [Creative Commons Attribution 4.0 International (CC BY 4.0)](https://creativecommons.org/licenses/by/4.0/). See [`LICENSE-docs.md`](LICENSE-docs.md). Attribution: Christian Verghis.
- **Scripts** (`scripts/`, `build.sh`) are licensed under the [MIT License](LICENSE).
