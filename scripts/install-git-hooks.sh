#!/bin/sh
set -eu

mkdir -p .git/hooks
cp git-hooks/pre-commit .git/hooks/pre-commit
chmod +x .git/hooks/pre-commit
chmod +x scripts/bump_pyproject_version.py

echo "Installed pre-commit hook: auto-bumps pyproject.toml patch version on commit."
