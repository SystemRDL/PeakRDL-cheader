#!/bin/bash

set -e

cd "$(dirname "$0")"

# Initialize venv
python3 -m venv .venv
source .venv/bin/activate

# Install test dependencies
pip install -U pip setuptools wheel
pip install peakrdl
pip install -r requirements.txt

# Install dut
pip install -U ../

# Run unit tests
pytest -n auto --cov=peakrdl_cheader

# Generate coverage report
coverage html -i -d htmlcov

# Run lint
pylint --rcfile pylint.rc ../src/peakrdl_cheader

# Run static type checking
mypy ../src/peakrdl_cheader
