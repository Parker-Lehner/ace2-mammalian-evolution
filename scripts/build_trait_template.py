#!/usr/bin/env python3
"""Create a curation-ready ecological trait table from curated sequence metadata."""

from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
META = ROOT / "data" / "processed" / "ace2_mammalia_curated_metadata.tsv"
TARGETS = ROOT / "config" / "target_species.tsv"
OUT = ROOT / "data" / "processed" / "mammal_ecology_traits_template.tsv"


def read_targets() -> dict[str, dict[str, str]]:
    if not TARGETS.exists():
        return {}
    with TARGETS.open(encoding="utf-8") as handle:
        return {row["scientific_name"]: row for row in csv.DictReader(handle, delimiter="\t")}


def main() -> int:
    if not META.exists():
        raise SystemExit(f"Missing {META}; run `make curate-sequences` first.")
    targets = read_targets()
    fields = [
        "scientific_name",
        "common_name",
        "habitat_class",
        "diving_class",
        "max_dive_depth_m",
        "max_dive_duration_min",
        "foraging_depth_m",
        "body_mass_kg",
        "oxygen_storage_proxy",
        "trait_source_citation",
        "trait_source_url",
        "trait_notes",
    ]
    OUT.parent.mkdir(parents=True, exist_ok=True)
    seen = set()
    with META.open(encoding="utf-8") as inp, OUT.open("w", newline="", encoding="utf-8") as out:
        writer = csv.DictWriter(out, fieldnames=fields, delimiter="\t")
        writer.writeheader()
        for row in csv.DictReader(inp, delimiter="\t"):
            species = row["scientific_name"]
            if species in seen:
                continue
            seen.add(species)
            target = targets.get(species, {})
            writer.writerow(
                {
                    "scientific_name": species,
                    "common_name": target.get("common_name", ""),
                    "habitat_class": target.get("habitat_class", "unknown"),
                    "diving_class": target.get("diving_class", "unknown"),
                    "max_dive_depth_m": "",
                    "max_dive_duration_min": "",
                    "foraging_depth_m": "",
                    "body_mass_kg": "",
                    "oxygen_storage_proxy": "",
                    "trait_source_citation": "NEEDS_CURATION",
                    "trait_source_url": "",
                    "trait_notes": "Populate from primary literature or citable trait database before modeling.",
                }
            )
    print(f"Wrote trait curation template: {OUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
