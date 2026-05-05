#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SCRIPT="$ROOT/scripts/run_comparative_models.R"

if ! command -v Rscript >/dev/null 2>&1; then
  echo "Rscript is not installed. Create the environment from environment.yml, then rerun." >&2
  exit 2
fi

Rscript "$SCRIPT"
