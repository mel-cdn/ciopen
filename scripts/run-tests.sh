#!/usr/bin/env bash

set -e

THRESHOLD=100

export PYTHONPATH=src
export DISABLE_CACHE=True

echo "> Running unit tests with coverage threshold: $THRESHOLD%"
python -m pytest \
  --cov-config=.coveragerc \
  --cov=ciopen \
  --no-cov-on-fail \
  --cov-fail-under=$THRESHOLD \
  --cov-branch \
  --cov-report=term \
  --cov-report=html:tmp/htmlcov \
  --cov-report=xml:tmp/coverage.xml \
  --junitxml=tmp/junit/junit.xml \
  tests/unit

echo "> Done!"
