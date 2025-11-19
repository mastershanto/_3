#!/usr/bin/env bash

VENV=${1:-.venv}

if [ ! -d "$VENV" ]; then
  echo "Virtual environment $VENV does not exist. Run ./scripts/setup_venv.sh first."
  exit 1
fi

# Deactivate conda if active (avoid mixing envs)
if command -v conda >/dev/null 2>&1 && [ -n "$CONDA_PREFIX" ]; then
  echo "Deactivating conda base environment to avoid conflicts"
  conda deactivate || true
fi

source "$VENV/bin/activate"

