# Validation entrypoint; mirrors .github/workflows/ci.yml. Needs Python 3.10+ and Gitleaks 8.30.1.
export GITLEAKS_BINARY := env("GITLEAKS_BINARY", `command -v gitleaks || true`)
export PYTHONDONTWRITEBYTECODE := "1"

# List available recipes
default:
    @just --list

# Run everything CI runs: tests, docs validation, working-tree and history secret scans
check: _require-gitleaks test
    python3 scripts/check_docs.py
    python3 scripts/check_secrets.py --working-tree
    python3 scripts/check_secrets.py --history

# Run the standard-library tests, including native Gitleaks canaries
test: _require-gitleaks
    python3 -m unittest discover -s tests -v

[private]
_require-gitleaks:
    @test -x "$GITLEAKS_BINARY" || { echo "Gitleaks 8.30.1 not found: put it on PATH or set GITLEAKS_BINARY" >&2; exit 1; }
