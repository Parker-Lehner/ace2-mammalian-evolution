#!/usr/bin/env python3
"""Prune the ACE2 QC tree to taxa retained in the codon selection alignment."""

from __future__ import annotations

import csv
from pathlib import Path

from Bio import Phylo


ROOT = Path(__file__).resolve().parents[1]
CODON_ALIGNMENT = ROOT / "data" / "processed" / "ace2_mammalia_codon_aligned.fna"
SOURCE_TREE = ROOT / "results" / "trees" / "ace2_mammalia.treefile"
OUT_TREE = ROOT / "results" / "selection" / "ace2_mammalia_codon_pruned.treefile"
OUT_REPORT = ROOT / "results" / "selection" / "ace2_mammalia_codon_pruned_tree_report.tsv"


def fasta_ids(path: Path) -> set[str]:
    ids = set()
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith(">"):
            ids.add(line[1:].split()[0])
    return ids


def main() -> int:
    if not CODON_ALIGNMENT.exists():
        raise SystemExit("Missing codon alignment; run `make codon-align` first.")
    if not SOURCE_TREE.exists():
        raise SystemExit("Missing ACE2 tree; run `make tree` first.")

    keep = fasta_ids(CODON_ALIGNMENT)
    tree = Phylo.read(SOURCE_TREE, "newick")
    terminal_names = {terminal.name for terminal in tree.get_terminals()}
    missing_from_tree = sorted(keep - terminal_names)
    extra_in_tree = sorted(terminal_names - keep)

    for name in extra_in_tree:
        tree.prune(name)

    OUT_TREE.parent.mkdir(parents=True, exist_ok=True)
    Phylo.write(tree, OUT_TREE, "newick")
    with OUT_REPORT.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["metric", "value"], delimiter="\t")
        writer.writeheader()
        writer.writerow({"metric": "codon_alignment_taxa", "value": len(keep)})
        writer.writerow({"metric": "source_tree_taxa", "value": len(terminal_names)})
        writer.writerow({"metric": "pruned_tree_taxa", "value": len(tree.get_terminals())})
        writer.writerow({"metric": "extra_taxa_pruned_from_tree", "value": len(extra_in_tree)})
        writer.writerow({"metric": "codon_taxa_missing_from_tree", "value": len(missing_from_tree)})
        writer.writerow({"metric": "extra_taxa_names", "value": ",".join(extra_in_tree)})
        writer.writerow({"metric": "missing_taxa_names", "value": ",".join(missing_from_tree)})

    if missing_from_tree:
        raise SystemExit(f"Codon alignment has taxa missing from tree: {', '.join(missing_from_tree)}")
    print(f"Wrote {OUT_TREE}")
    print(f"Wrote {OUT_REPORT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
