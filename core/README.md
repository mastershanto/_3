# complete_ai_engineering_bootcamp

This repository contains course materials and examples for the Complete AI Engineering Bootcamp.

## Setting up Python dependencies (recommended)

Homebrew-managed Python (and some Linux/system Python installs) enable PEP 668 (externally managed environments). This prevents `pip` from making system-wide changes to packages, and will surface the error shown below when you try `pip install -r requirements.txt` from the system Python:

```bash
error: externally-managed-environment

× This environment is externally managed
╰─> To install Python packages system-wide, try brew install
	xyz, where xyz is the package you are trying to
	install.
```

To fix this, create a virtual environment and install packages there:

```bash
# from project root
/opt/homebrew/bin/python3.14 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip wheel setuptools
python -m pip install -r requirements.txt
```

Alternatively, use the helper script:

```bash
# ./scripts/setup_venv.sh
chmod +x scripts/setup_venv.sh
./scripts/setup_venv.sh
```

Train and test the linear regression model using `linear_regrassion.py`:

```bash
# Train and create a plot of predictions
python linear_regrassion.py --mode train --plot

# Make predictions (samples from test set)
python linear_regrassion.py --mode predict --n-samples 5
```
To activate the venv (if you created `.venv`):

```bash
source .venv/bin/activate
# or from the helper script
chmod +x scripts/activate_venv.sh
./scripts/activate_venv.sh
```

If you prefer Conda for environments, create a Conda environment instead (avoid using `base`):

```bash
conda create -n myenv python=3.14
conda activate myenv
python -m pip install -r requirements.txt
```

NOTE: If you are using a Conda base environment (your shell prompt shows `(base)`), deactivate it first with:

```bash
conda deactivate
# or
source deactivate
```

This ensures the venv uses Homebrew's Python 3.14.

If you prefer a different setup:

- Use `pipx` for installing Python CLI apps: `brew install pipx && pipx install <app>`
- Use `--break-system-packages` with pip only if you understand the risk: `pip install --break-system-packages -r requirements.txt` (not recommended)

