#!/usr/bin/env python3
"""Compute conservative ACE2 sequence metrics for comparative modeling."""

from __future__ import annotations

import csv
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
FASTA = ROOT / "data" / "processed" / "ace2_mammalia_curated.faa"
META = ROOT / "data" / "processed" / "ace2_mammalia_curated_metadata.tsv"
OUT = ROOT / "data" / "processed" / "ace2_evolutionary_metrics.tsv"


HYDROPHOBIC = set("AILMFWYV")
POLAR = set("STNQ")
CHARGED = set("KRHDE")


def parse_fasta(path: Path) -> dict[str, str]:
    records = {}
    header = None
    parts = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith(">"):
            if header:
                records[header.split()[0]] = "".join(parts)
            header = line[1:].strip()
            parts = []
        elif line.strip():
            parts.append(line.strip())
    if header:
        records[header.split()[0]] = "".join(parts)
    return records


def fraction(seq: str, residues: set[str]) -> float:
    return sum(1 for aa in seq if aa in residues) / len(seq) if seq else 0.0


def net_charge(seq: str) -> int:
    counts = Counter(seq)
    return counts["K"] + counts["R"] + counts["H"] - counts["D"] - counts["E"]


def domain_lengths(seq: str) -> tuple[int, int, int]:
    """Approximate human ACE2-coordinate domains for exploratory metrics.

    These are intentionally coarse and must be replaced by coordinate-mapped
    domain annotations for final functional claims.
    """
    peptidase = min(len(seq), 615)
    collectrin = max(0, min(len(seq), 740) - 616)
    membrane_tail = max(0, len(seq) - 740)
    return peptidase, collectrin, membrane_tail


def main() -> int:
    if not FASTA.exists() or not META.exists():
        raise SystemExit("Run `make curate-sequences` before computing metrics.")
    seqs = parse_fasta(FASTA)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with META.open(encoding="utf-8") as inp, OUT.open("w", newline="", encoding="utf-8") as out:
        writer = csv.DictWriter(
            out,
            fieldnames=[
                "scientific_name",
                "sequence_id",
                "length",
                "net_charge_simple",
                "frac_hydrophobic",
                "frac_polar",
                "frac_charged",
                "approx_peptidase_length",
                "approx_collectrin_like_length",
                "approx_membrane_tail_length",
            ],
            delimiter="\t",
        )
        writer.writeheader()
        for row in csv.DictReader(inp, delimiter="\t"):
            seq_id = row["sequence_id"]
            seq = seqs.get(seq_id, "")
            pep, coll, tail = domain_lengths(seq)
            writer.writerow(
                {
                    "scientific_name": row["scientific_name"],
                    "sequence_id": seq_id,
                    "length": len(seq),
                    "net_charge_simple": net_charge(seq),
                    "frac_hydrophobic": f"{fraction(seq, HYDROPHOBIC):.6f}",
                    "frac_polar": f"{fraction(seq, POLAR):.6f}",
                    "frac_charged": f"{fraction(seq, CHARGED):.6f}",
                    "approx_peptidase_length": pep,
                    "approx_collectrin_like_length": coll,
                    "approx_membrane_tail_length": tail,
                }
            )
    print(f"Wrote {OUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
