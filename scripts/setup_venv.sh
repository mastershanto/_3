#!/usr/bin/env bash
set -euo pipefail

# Usage: ./scripts/setup_venv.sh [venv-name]
# Defaults to .venv

VENV_NAME=${1:-.venv}
PYTHON=${2:-${PYTHON:-/opt/homebrew/bin/python3.14}}

if ! command -v "$PYTHON" >/dev/null 2>&1; then
  echo "Python 3.14 not found at $PYTHON"
  echo "Try installing with Homebrew: brew install python@3.14"
  echo "Or use a different python binary: ./scripts/setup_venv.sh myenv /usr/bin/python3"
  exit 1
fi

echo "Using python: $($PYTHON --version)"

# Create venv
$PYTHON -m venv "$VENV_NAME"

# Activate and upgrade pip
# Note: activation is done by the user, this script just runs the installation using the created venv
source "$VENV_NAME/bin/activate"
python -m pip install --upgrade pip setuptools wheel

# Install dependencies
if [ -f requirements.txt ]; then
  python -m pip install -r requirements.txt
  echo "\nInstalled packages (pip freeze):"
  python -m pip freeze | sed -n '1,200p'
else
  echo "requirements.txt not found. Skipping installation."
fi

echo "Virtual environment created at $VENV_NAME"
echo "Activate it with: source $VENV_NAME/bin/activate"

