#!/usr/bin/env bash
# Regenerate every guide, diagram, and derived artifact from the verified data.
# All generators are pure (data in -> HTML/SVG out) and run from the repo root.
set -euo pipefail
cd "$(dirname "$0")"

python3 scripts/build_digest.py          # data/paper-airplanes.json -> data/paper-digest.txt
python3 scripts/build_paper_guide.py     # -> guides/paper-airplanes.html
python3 scripts/build_paper_index_svg.py # -> diagrams/paper-index.svg
python3 scripts/build_drone_guide.py     # data/drone-concepts.json -> guides/drones.html
python3 scripts/build_vtol_diagram.py    # -> diagrams/efficient-vtol.svg
python3 scripts/build_drone_workflow.py  # data/paper-digest.txt -> scripts/paper_to_drone.workflow.js

echo "done — open guides/paper-airplanes.html and guides/drones.html"
