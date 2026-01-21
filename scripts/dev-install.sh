#!/bin/bash
# Dev install script for geodesk-py
# Builds the C++ extension and installs into a fresh venv

set -e

cd "$(dirname "$0")/.."

echo "==> Removing old build artifacts..."
rm -rf .venv _skbuild build

echo "==> Building and installing with uv sync..."
uv sync --no-editable --reinstall-package geodesk

echo "==> Done! Activate with: source .venv/bin/activate"
