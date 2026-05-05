#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
IN="$ROOT/data/processed/ace2_mammalia_curated.faa"
OUT="$ROOT/results/alignments/ace2_mammalia_aligned.faa"
LOG="$ROOT/logs/mafft_ace2.log"

if ! command -v mafft >/dev/null 2>&1; then
  echo "MAFFT is not installed. Create the environment from environment.yml, then rerun." >&2
  exit 2
fi

mkdir -p "$(dirname "$OUT")" "$(dirname "$LOG")"
mafft --maxiterate 1000 --localpair "$IN" > "$OUT" 2> "$LOG"
echo "Wrote $OUT"
