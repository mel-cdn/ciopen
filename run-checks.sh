#!/usr/bin/env bash

set -e -u

echo "> Installing Python dependencies..."
pip install -e ".[dev]"

echo "> Installing pre-commit..."
pre-commit install
pre-commit install --hook-type commit-msg
pre-commit run --all-files

echo "> Running tests..."
./run-tests.sh

echo "> Running integration tests..."
export PYTHONPATH=src
python -m pytest tests/integration

echo "> Done!"
