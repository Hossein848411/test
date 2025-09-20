#!/usr/bin/env bash
set -euo pipefail

echo "=== Build start: $(date) ==="

# Ensure scripts installed in /python312/bin are callable (fix pip warnings)
# Add python312 bin to PATH temporarily for this build
export PATH="/python312/bin:$PATH"
echo "PATH updated: $PATH"

# Use python -m pip to avoid script-location issues and ensure correct pip
python3 -m ensurepip --upgrade || true
python3 -m pip install --upgrade pip setuptools wheel

# Install dependencies (suppress script-location warnings if desired)
# You can add --no-warn-script-location to suppress that particular warning.
python3 -m pip install -r requirements.txt --no-warn-script-location

# Collect static files (no DB required)
echo "Collecting static files..."
python3 manage.py collectstatic --noinput || {
  echo "collectstatic failed — continuing (may not be required in build)"
}

# Optionally run migrations only when explicitly allowed and DB is reachable.
if [ "${RUN_MIGRATIONS:-0}" = "1" ]; then
  echo "RUN_MIGRATIONS=1 -> attempting migrations..."
  python3 manage.py migrate --noinput
else
  echo "Skipping migrations in build (RUN_MIGRATIONS != 1)."
fi

echo "=== Build finished: $(date) ==="
