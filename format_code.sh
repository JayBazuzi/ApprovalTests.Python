#! /bin/bash
set -euo pipefail

command -v uv >/dev/null || { echo "Install uv. https://docs.astral.sh/uv/getting-started/installation/" >&2; exit 1; }
uv venv --seed --quiet

uv pip install isort black
uv run isort .
uv run black .
