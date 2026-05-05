#!/usr/bin/env python3
"""Map ACE2 alignment columns to human ACE2 residue coordinates."""

from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ALIGNMENT = ROOT / "results" / "alignments" / "ace2_mammalia_aligned.faa"
ANNOT = ROOT / "config" / "residue_annotations.tsv"
OUT = ROOT / "data" / "processed" / "human_ace2_alignment_coordinate_map.tsv"


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


def load_annotations() -> dict[int, list[str]]:
    out: dict[int, list[str]] = {}
    if not ANNOT.exists():
        return out
    with ANNOT.open(encoding="utf-8") as handle:
        for row in csv.DictReader(handle, delimiter="\t"):
            pos = int(row["human_ace2_position"])
            out.setdefault(pos, []).append(f"{row['feature']}:{row['class']}")
    return out


def main() -> int:
    if not ALIGNMENT.exists():
        raise SystemExit(f"Missing alignment: {ALIGNMENT}. Run `make align` first.")
    records = parse_fasta(ALIGNMENT)
    human = None
    for header, seq in records:
        if "Homo_sapiens|" in header or "Homo sapiens" in header:
            human = (header, seq)
            break
    if human is None:
        raise SystemExit("Human ACE2 sequence was not found in alignment; cannot map coordinates.")
    annotations = load_annotations()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    residue = 0
    with OUT.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=["alignment_column_1based", "human_ace2_position", "human_residue", "annotation"],
            delimiter="\t",
        )
        writer.writeheader()
        for i, aa in enumerate(human[1], start=1):
            if aa != "-":
                residue += 1
                pos = str(residue)
                annotation = ";".join(annotations.get(residue, []))
            else:
                pos = ""
                annotation = ""
            writer.writerow(
                {
                    "alignment_column_1based": i,
                    "human_ace2_position": pos,
                    "human_residue": aa,
                    "annotation": annotation,
                }
            )
    print(f"Wrote {OUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
