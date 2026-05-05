#!/usr/bin/env python3
"""Report coverage of priority aquatic/diving/terrestrial target species."""

from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TARGETS = ROOT / "config" / "target_species.tsv"
META = ROOT / "data" / "processed" / "ace2_mammalia_curated_metadata.tsv"
OUT = ROOT / "results" / "qc" / "target_species_coverage.tsv"


def main() -> int:
    if not META.exists():
        raise SystemExit("Run `make curate-sequences` before target coverage.")
    with META.open(encoding="utf-8") as handle:
        species = {row["scientific_name"] for row in csv.DictReader(handle, delimiter="\t")}
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with TARGETS.open(encoding="utf-8") as inp, OUT.open("w", newline="", encoding="utf-8") as out:
        reader = csv.DictReader(inp, delimiter="\t")
        fieldnames = reader.fieldnames + ["present_in_curated_ace2", "fallback_needed"]  # type: ignore[operator]
        writer = csv.DictWriter(out, fieldnames=fieldnames, delimiter="\t")
        writer.writeheader()
        for row in reader:
            present = row["scientific_name"] in species
            row["present_in_curated_ace2"] = "yes" if present else "no"
            row["fallback_needed"] = "no" if present else "yes_ensembl_or_uniprot"
            writer.writerow(row)
    print(f"Wrote {OUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
