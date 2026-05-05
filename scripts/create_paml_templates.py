#!/usr/bin/env python3
"""Create PAML branch-site foreground template files for planned ACE2 tests."""

from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
META = ROOT / "data" / "processed" / "ace2_mammalia_curated_metadata.tsv"
TARGETS = ROOT / "config" / "target_species.tsv"
OUTDIR = ROOT / "results" / "selection" / "paml" / "templates"


FOREGROUNDS = {
    "aquatic_required": lambda r: r.get("habitat_class") == "aquatic",
    "cetacean": lambda r: r.get("group") == "cetacean",
    "pinniped": lambda r: r.get("group") == "pinniped",
    "sirenian": lambda r: r.get("group") == "sirenian",
    "deep_diver": lambda r: r.get("diving_class") == "deep_diver",
}


def load_sequence_ids() -> dict[str, str]:
    with META.open(encoding="utf-8") as handle:
        return {row["scientific_name"]: row["sequence_id"] for row in csv.DictReader(handle, delimiter="\t")}


def match_sequence_id(target_name: str, seq_ids: dict[str, str]) -> str:
    if target_name in seq_ids:
        return seq_ids[target_name]
    target_parts = target_name.split()
    if len(target_parts) < 2:
        return ""
    target_binomial = " ".join(target_parts[:2])
    matches = [
        seq_id for scientific_name, seq_id in seq_ids.items()
        if scientific_name == target_binomial
        or scientific_name.startswith(target_binomial + " ")
        or target_binomial.startswith(scientific_name + " ")
    ]
    if len(matches) == 1:
        return matches[0]
    return ""


def main() -> int:
    if not META.exists():
        raise SystemExit("Missing curated metadata; run `make curate-sequences` first.")
    seq_ids = load_sequence_ids()
    targets = []
    with TARGETS.open(encoding="utf-8") as handle:
        for row in csv.DictReader(handle, delimiter="\t"):
            sequence_id = match_sequence_id(row["scientific_name"], seq_ids)
            if sequence_id:
                row["sequence_id"] = sequence_id
                targets.append(row)
    OUTDIR.mkdir(parents=True, exist_ok=True)
    summary_rows = []
    for name, pred in FOREGROUNDS.items():
        foreground = [row for row in targets if pred(row)]
        path = OUTDIR / f"{name}_foreground_taxa.txt"
        path.write_text("\n".join(row["sequence_id"] for row in foreground) + ("\n" if foreground else ""), encoding="utf-8")
        ctl = OUTDIR / f"{name}_codeml_template.ctl"
        ctl.write_text(
            "\n".join(
                [
                    "seqfile = ../../../data/processed/ace2_mammalia_codon_aligned.fna",
                    "treefile = TREE_WITH_FOREGROUND_LABELS_REQUIRED.nwk",
                    f"outfile = ../{name}_branch_site.out",
                    "noisy = 3",
                    "verbose = 1",
                    "runmode = 0",
                    "seqtype = 1",
                    "CodonFreq = 2",
                    "model = 2",
                    "NSsites = 2",
                    "fix_omega = 0",
                    "omega = 1.5",
                    "cleandata = 1",
                    "",
                    "# This is a template. Label foreground branches in the tree with #1 before running codeml.",
                ]
            ),
            encoding="utf-8",
        )
        summary_rows.append({"foreground": name, "taxa_count": len(foreground), "taxa_file": str(path.relative_to(ROOT)), "ctl_template": str(ctl.relative_to(ROOT))})
    summary = OUTDIR / "paml_template_summary.tsv"
    with summary.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["foreground", "taxa_count", "taxa_file", "ctl_template"], delimiter="\t")
        writer.writeheader()
        writer.writerows(summary_rows)
    print(f"Wrote PAML templates under {OUTDIR}")
    print(f"Wrote {summary}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
