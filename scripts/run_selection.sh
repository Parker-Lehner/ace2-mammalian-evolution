#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CODON="$ROOT/data/processed/ace2_mammalia_codon_aligned.fna"
TREE="$ROOT/results/trees/ace2_mammalia.treefile"
SELECTION_TREE="$ROOT/results/selection/ace2_mammalia_codon_pruned.treefile"

if ! command -v hyphy >/dev/null 2>&1; then
  echo "HyPhy is not installed. Create the environment from environment.yml, then rerun." >&2
  exit 2
fi

if [[ ! -s "$CODON" ]]; then
  echo "Missing codon alignment: $CODON. Back-translate protein alignment before selection tests." >&2
  exit 2
fi

if [[ ! -s "$TREE" ]]; then
  echo "Missing ACE2 tree: $TREE. Run make tree first." >&2
  exit 2
fi

if [[ ! -s "$SELECTION_TREE" ]]; then
  python "$ROOT/scripts/prune_tree_for_selection.py"
fi

mkdir -p "$ROOT/results/selection/hyphy_meme" "$ROOT/results/selection/hyphy_fubar"
hyphy meme --alignment "$CODON" --tree "$SELECTION_TREE" --output "$ROOT/results/selection/hyphy_meme/ace2_meme.json"
hyphy fubar --alignment "$CODON" --tree "$SELECTION_TREE" --output "$ROOT/results/selection/hyphy_fubar/ace2_fubar.json"
echo "Wrote HyPhy MEME/FUBAR outputs"
