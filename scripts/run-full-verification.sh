#!/bin/sh
set -eu

ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
cd "$ROOT"

scripts/check-upstream-example-parity.py
scripts/check-upstream-manual-parity.py

echo "full breakble-tcolorbox verification passed."
