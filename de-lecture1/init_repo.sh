#!/bin/bash
set -euo pipefail      # stop on error, on unset variable, on failed pipe

echo "Initialising project layout…"
mkdir -p theory code-alongs explorations data/raw data/processed
touch theory/.gitkeep code-alongs/.gitkeep data/raw/.gitkeep

for i in {1..5}; do
    echo "notes for session $i" > "explorations/session$i.md"
done

echo "Done. Structure:"
ls -R . | head -30

