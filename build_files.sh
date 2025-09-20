#!/usr/bin/env bash
set -euo pipefail

echo "=== Build start: $(date) ==="

# Ensure pip exists (safe) and upgrade tooling
python3 -m ensurepip --upgrade || true
python3 -m pip install --upgrade pip setuptools wheel

# Install dependencies
echo "Installing requirements..."
pip3 install -r requirements.txt

# Collect static files (no DB required)
echo "Collecting static files..."
python3 manage.py collectstatic --noinput || {
  echo "collectstatic failed — continuing (some projects may not need collectstatic at build time)"
}

# Optional: run migrations only when explicitly allowed and when DB is available.
# To run migrations during build, set environment variable RUN_MIGRATIONS=1 in Vercel.
if [ "${RUN_MIGRATIONS:-0}" = "1" ]; then
  echo "RUN_MIGRATIONS=1 -> attempting migrations..."

  # Try to run migrations. If DB is unreachable, fail loudly so you can fix config.
  python3 manage.py migrate --noinput
else
  echo "Skipping migrations in build (RUN_MIGRATIONS != 1)."
fi

echo "=== Build finished: $(date) ==="
