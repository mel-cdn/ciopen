#!/usr/bin/env bash

set -e -u

echo "> Installing Python dependencies..."
pipenv install --dev

echo "> Installing pre-commit..."
pre-commit install
pre-commit install --hook-type commit-msg
pre-commit run --all-files

echo "> Running tests..."
./run-tests.sh

echo "> Done!"
