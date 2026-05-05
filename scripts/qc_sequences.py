#!/usr/bin/env python3
"""Generate sequence QC summaries for curated ACE2 proteins."""

from __future__ import annotations

import csv
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
FASTA = ROOT / "data" / "processed" / "ace2_mammalia_curated.faa"
OUT = ROOT / "results" / "qc" / "ace2_sequence_qc.tsv"
SUMMARY = ROOT / "results" / "qc" / "ace2_sequence_qc_summary.md"


def parse_fasta(path: Path) -> list[tuple[str, str]]:
    records = []
    header = None
    parts = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith(">"):
            if header:
                records.append((header, "".join(parts)))
            header = line[1:].strip()
            parts = []
        elif line.strip():
            parts.append(line.strip())
    if header:
        records.append((header, "".join(parts)))
    return records


def net_charge(seq: str) -> int:
    residues = Counter(seq)
    return residues["K"] + residues["R"] + residues["H"] - residues["D"] - residues["E"]


def main() -> int:
    if not FASTA.exists():
        raise SystemExit(f"Missing {FASTA}; run `make curate-sequences` first.")
    records = parse_fasta(FASTA)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    lengths = []
    with OUT.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=["sequence_id", "length", "net_charge_simple", "ambiguous_count", "gap_count", "qc_flag"],
            delimiter="\t",
        )
        writer.writeheader()
        for header, seq in records:
            sequence_id = header.split()[0]
            ambiguous_count = sum(1 for aa in seq if aa in "XBZJUO")
            gap_count = seq.count("-")
            flag = "pass"
            if len(seq) < 650 or len(seq) > 950:
                flag = "length_outlier"
            elif ambiguous_count:
                flag = "ambiguous_residues"
            lengths.append(len(seq))
            writer.writerow(
                {
                    "sequence_id": sequence_id,
                    "length": len(seq),
                    "net_charge_simple": net_charge(seq),
                    "ambiguous_count": ambiguous_count,
                    "gap_count": gap_count,
                    "qc_flag": flag,
                }
            )
    if lengths:
        text = [
            "# ACE2 Sequence QC Summary",
            "",
            f"- Records: {len(lengths)}",
            f"- Minimum length: {min(lengths)}",
            f"- Maximum length: {max(lengths)}",
            f"- Mean length: {sum(lengths) / len(lengths):.1f}",
            f"- QC table: `{OUT.relative_to(ROOT)}`",
        ]
    else:
        text = ["# ACE2 Sequence QC Summary", "", "No records available."]
    SUMMARY.write_text("\n".join(text) + "\n", encoding="utf-8")
    print(f"Wrote {OUT}")
    print(f"Wrote {SUMMARY}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
