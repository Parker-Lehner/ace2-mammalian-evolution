#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
IN="$ROOT/results/alignments/ace2_mammalia_aligned.faa"
OUTDIR="$ROOT/results/trees"

if command -v iqtree2 >/dev/null 2>&1; then
  IQTREE=iqtree2
elif command -v iqtree >/dev/null 2>&1; then
  IQTREE=iqtree
else
  echo "IQ-TREE is not installed. Create the environment from environment.yml, then rerun." >&2
  exit 2
fi

mkdir -p "$OUTDIR"
MODEL="${IQTREE_MODEL:-LG+R7}"
BOOTSTRAPS="${IQTREE_BOOTSTRAPS:-1000}"
ALRT="${IQTREE_ALRT:-1000}"
NINIT="${IQTREE_NINIT:-10}"
NSTOP="${IQTREE_NSTOP:-10}"
"$IQTREE" -s "$IN" -m "$MODEL" -B "$BOOTSTRAPS" -alrt "$ALRT" -nt AUTO -ninit "$NINIT" -nstop "$NSTOP" -pre "$OUTDIR/ace2_mammalia"
echo "Wrote IQ-TREE outputs under $OUTDIR"
