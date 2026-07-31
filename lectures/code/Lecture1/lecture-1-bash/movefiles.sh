#!/bin/bash
# Lecture 1.3 — the demo we did together, as a script.
# Create a folder, write a file, move it somewhere else, clean up.
# Run with:  bash movefiles.sh

set -euo pipefail   # stop on the first error instead of ploughing on

WORKDIR="folder1"
TARGET="folder2"

echo "→ resetting $WORKDIR and $TARGET"
rm -rf "$WORKDIR" "$TARGET"          # -rf never asks: read this line twice
mkdir -p "$WORKDIR" "$TARGET"

echo "→ creating two files in $WORKDIR"
echo "hello from bash, $(date -u +%FT%TZ)" > "$WORKDIR/hello.txt"
printf 'id,city,pm25\n1,Goteborg,7\n' > "$WORKDIR/readings.csv"

echo "→ before the move"
ls -al "$WORKDIR"

echo "→ moving *.txt and *.csv into $TARGET"
mv "$WORKDIR"/*.txt "$WORKDIR"/*.csv "$TARGET"/

echo "→ after the move"
ls -al "$TARGET"
wc -l "$TARGET"/readings.csv

echo "→ removing $WORKDIR"
rm -rf "$WORKDIR"

echo "✔ done. $TARGET now holds $(ls "$TARGET" | wc -l) files."
