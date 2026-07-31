#!/bin/bash
# Lecture 1.3 — bootstrap a Python project the way we will do it all course.
# Run with:  bash pythonvenv.sh
#
# A virtual environment keeps this project's packages out of your system Python,
# so "it works on my machine" has a chance of also being true on someone else's.

set -euo pipefail

PY=${PYTHON:-python3}

echo "→ using $($PY --version)"

if [ -d venv ]; then
  echo "→ venv already exists, reusing it"
else
  echo "→ creating venv/"
  "$PY" -m venv venv
fi

# shellcheck disable=SC1091
source venv/bin/activate
echo "→ active interpreter: $(which python)"

echo "→ upgrading pip"
python -m pip install --quiet --upgrade pip

echo "→ installing project dependencies"
pip install --quiet dbt-core pandas requests

echo "→ freezing exact versions to requirements.txt"
pip freeze > requirements.txt
head -5 requirements.txt

cat <<'EOF'

✔ Done.
  activate later with:   source venv/bin/activate
  leave it with:         deactivate
  reinstall elsewhere:   pip install -r requirements.txt

Remember: commit requirements.txt, never commit venv/ (add it to .gitignore).
EOF
