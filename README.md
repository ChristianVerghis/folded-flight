# folded-flight

**From paper airplanes to 3D-printed drones — a two-volume aerodynamics field guide.**

This project starts from a simple question — *what are the best paper airplanes, and why?* — and follows it all the way to *what does folded paper actually teach us about designing real, 3D-printed drones?* Every design here was generated and then **adversarially verified** by a multi-agent workflow (fold sequences re-folded, facts fact-checked, physics stress-tested for scale), so the guides are honest rather than plausible-sounding.

Two rendered guides (standalone, self-contained HTML — just open them in a browser):

- **`guides/paper-airplanes.html`** — Volume I: nine paper airplanes, one per discipline (fastest, farthest, longest-floating, most durable, and stranger), each with a plan view, side elevation, crease pattern, fold sequence, and spec table.
- **`guides/drones.html`** — Volume II: nine 3D-printable drone concepts derived from those paper principles, plus a ranked list of efficiency upgrades for a tiltrotor VTOL.

> Also published as Claude artifacts:
> [Vol I — paper airplanes](https://claude.ai/code/artifact/5a056dfb-4665-451a-811e-b1e2827d50b8) ·
> [Vol II — drones](https://claude.ai/code/artifact/990fc8ce-704e-45b1-b64e-9cdb06de4efe)

---

## The one finding that matters

The trap in "borrow from paper airplanes" is **Reynolds number**. Paper planes fly at Re ≈ 30,000–50,000; real 3D-printed drones cruise at Re ≈ 100,000–500,000, where the boundary-layer physics is different. Volume II rates every concept on this, and the pattern is clean:

| Transfers? | What | Why |
|---|---|---|
| ✅ **Fully** | **Mass placement** — battery-as-forward-ballast to set the CG | Pure rigid-body statics; Reynolds-independent. This is the real meaning of "weighted components": place the heavy parts you already carry so the CG sits ahead of the neutral point (~5–15 % static margin). No dead lead. |
| ✅ **Even better at scale** | **High-aspect-ratio wing** (Sea Glider / Paperang) | Long slender wings raise L/D *more* at drone Re, not less. |
| ❌ **Does not transfer** | Swept deltas, stubby low-aspect wings, ring/annular wings | They only work because a slow paper plane tolerates flow separation; scaled up they are just drag. |

## Volume I — the nine paper airplanes

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

## Volume II — the nine drone concepts

| # | Concept | Type | Borrows | Scales? |
|---|---------|------|---------|---------|
| 01 | **Keelhaul** | pusher fixed-wing | Dart nose-mass → battery-as-ballast CG | partial |
| 02 | **Albatross-12** | high-AR quadplane VTOL | Sea Glider slender wing | ✅ fully |
| 03 | **Torus "Halo"** | ducted box-wing VTOL | ring-wing → ducts + closed wing | partial |
| 04 | **HAR-1 "Mantis"** | tailless flying-wing tri-tiltrotor | Harrier elevons / tailless | partial |
| 05 | **Samara-1** | monocopter | Tumblewing / samara autorotation | partial |
| 06 | **Suzanne-V "Vireo"** | quad-tiltrotor VTOL sailplane | two-phase climb-then-glide | partial |
| 07 | **Polyhedra P1** | passively-stable pusher glider | dihedral + washout stability | partial *(easiest build)* |
| 08 | **Nakamura Locke** | snap-lock tri-tiltrotor cruiser | self-locking structure + forward CG | partial |
| 09 | **DEP-1 "Bellwether"** | blown-wing quad-tiltrotor | distributed propulsion over the wing | partial |

## Making the tiltrotor VTOL more efficient (top of the ranked list)

Ranked by impact-per-cost across hover, cruise, structure, transition, and propulsion:

1. **Minimize disk loading** — biggest rotor discs the frame allows → ~20–25 % less hover power *(hover)*
2. **Drive airframe mass fraction down** — LW-PLA + carbon spar + selective infill *(all phases)*
3. **Weight-on-wing cruise** — tilt fully horizontal, cruise-matched prop, **stop/fold the tail rotor** *(cruise)*
4. **Match blade solidity / twist / RPM** to the low-Re rotor regime *(hover)*
5. **Unidirectional carbon spar/boom**, printed parts only as shear web & connectors *(all)*
6. **Flight scheduling** — rush the transition corridor, cruise at best-L/D speed *(all)*
7. **Match motor Kv + cell count** so hover sits at 50–65 % throttle *(hover)*
8. **Higher-aspect wing** — span extension / taper *(cruise)*

…full 13-lever list with mechanism, cost, and printable implementation is in `guides/drones.html` and `data/drone-concepts.json`.

---

## Repository layout

```
folded-flight/
├── README.md
├── project.yml                 # ~/dev/dashboard manifest
├── build.sh                    # regenerate everything (data -> guides/diagrams)
├── data/
│   ├── paper-airplanes.json    # 9 verified paper designs (folds, geometry, flight)
│   ├── drone-concepts.json     # 9 verified drone concepts + 13 ranked VTOL levers
│   └── paper-digest.txt        # compact digest that grounds the drone workflow
├── guides/
│   ├── paper-airplanes.html    # Vol I (generated)
│   └── drones.html             # Vol II (generated)
├── diagrams/
│   ├── paper-index.svg         # specimen index of all 9 planforms
│   └── efficient-vtol.svg      # annotated "6 changes" tri-tiltrotor diagram
└── scripts/
    ├── build_digest.py
    ├── build_paper_guide.py
    ├── build_paper_index_svg.py
    ├── build_drone_guide.py
    ├── build_vtol_diagram.py
    ├── build_drone_workflow.py       # emits the drone-design workflow (below)
    ├── paper_field_guide.workflow.js # the Vol I research+verify workflow
    └── paper_to_drone.workflow.js    # the Vol II design+verify workflow
```

The `guides/*.html`, `diagrams/*.svg`, `data/paper-digest.txt`, and `scripts/paper_to_drone.workflow.js` are **generated**. The `data/*.json` files are the canonical, hand-verified source of truth.

## Rebuilding

Everything is pure functions of the JSON data. From the repo root:

```bash
./build.sh
```

Requires only Python 3 (standard library — no dependencies). The diagrams are drawn directly from each design's normalized geometry, so they always match the data.

## How the designs were made (methodology)

Both volumes came out of deterministic multi-agent **workflows** (see `scripts/*.workflow.js`):

1. **Fan-out** — one agent per design/concept, each producing a structured spec (fold steps or engineering design + normalized diagram geometry).
2. **Adversarial verify** — a second agent re-checks each one: for paper planes, mentally re-folding the sequence and fact-checking records; for drones, stress-testing Reynolds-scaling, CG/static-margin soundness, printability, and whether efficiency claims are quantitatively defensible.
3. **Critic** — flags missing categories worth adding.

That verification pass did real work. Among the corrections it forced:

- Fixed the **Bulldog Dart** fold order (it flips the paper mid-sequence) and corrected the claim that it likes a hard throw (it prefers a soft one).
- Corrected the paper-plane **distance-record chain**: Suzanne (69.14 m, 2012) → 77.13 m (2022) → current 88.31 m (Boeing engineers, 2022).
- Corrected **static margin** to `(neutral-point − CG)/MAC` for tailed layouts (the wing AC is only the neutral point for a *tailless* wing).
- Flagged that a **TPU living hinge cannot be co-printed** into a PLA/PETG surface on a single-nozzle printer.
- Downgraded several hand-wavy efficiency percentages to defensible ranges.

## Sources & credits

Paper designs and facts draw on Fold'N'Fly, NASA JPL's "Ring Wing Glider" activity, John M. Collins (*The New World Champion Paper Airplane Book*, the tumblewing), Slater Harrison / ScienceToyMaker (walkalong gliding), Art of Manliness (Bulldog Dart), and Guinness World Records (distance). Drone concepts are original syntheses grounded in standard UAV aerodynamics (momentum theory for hover, L/D for cruise).

*Built with Claude Code.*
