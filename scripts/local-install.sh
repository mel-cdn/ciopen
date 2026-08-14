#!/usr/bin/env bash

set -e -u

echo "> Cleaning previous build artifacts..."
rm -rf dist build src/ciopen.egg-info

echo "> Building package..."
python -m pip install --quiet build
python -m build

echo "> Installing built wheel..."
python -m pip install --force-reinstall dist/*.whl

echo "> Done! Try:"
echo "    ciopen --help"
echo "    ciopen jira set-base-url https://your-org.atlassian.net"
