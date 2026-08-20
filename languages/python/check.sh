#!/bin/bash

set -euo pipefail
# set -x

start=$(date +%s)

# Prevent Python from creating __pycache__ folders entirel
export PYTHONDONTWRITEBYTECODE=1

black .
ruff check . --no-cache
pytest -v -p no:cacheprovider

echo
echo "All checks passed successfully at $(date +'%H:%M:%S %d.%m')"
end=$(date +%s)
elapsed=$((end - start))
echo "Elapsed time: ${elapsed} seconds"
