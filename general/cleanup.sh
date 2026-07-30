#!/usr/bin/env bash
set -euo pipefail

echo "Cleaning Node.js artifacts..."
find . -type d \( \
    -name node_modules -o \
    -name .next -o \
    -name dist -o \
    -name build -o \
    -name coverage \
\) -prune -exec rm -rf {} +

echo "Cleaning Python artifacts..."
find . -type d \( \
    -name __pycache__ -o \
    -name .pytest_cache -o \
    -name .mypy_cache -o \
    -name .ruff_cache -o \
    -name .tox -o \
    -name .nox -o \
    -name .venv -o \
    -name venv -o \
    -name env \
\) -prune -exec rm -rf {} +

find . -type f \( \
    -name "*.pyc" -o \
    -name "*.pyo" -o \
    -name ".coverage" \
\) -delete

echo "Done."
