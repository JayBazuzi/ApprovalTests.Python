#! /usr/bin/env bash
set -euo pipefail

command -v uv >/dev/null || { echo "Install uv. https://docs.astral.sh/uv/getting-started/installation/" >&2; exit 1; }
uv venv --seed --quiet
uv pip install -r requirements.txt --quiet


LOG_FILE=$(mktemp -t approvaltests_run_tests.XXXXXX.log)

run_step() {
    local display_name="$1"
    shift
    if "${@}" > "$LOG_FILE" 2>&1; then
        echo "✅ $display_name PASSED"
    else
        echo "❌ $display_name FAILED" && cat "$LOG_FILE" && rm -f "$LOG_FILE" && exit 1
    fi
}

run_step "run unit tests" uv run pytest --junitxml=test-reports/report.xml
run_step "run mypy" uv run mypy .
run_step "run integration tests" uv run test__mypy_accepts_our_packages.py

rm -f "$LOG_FILE"
