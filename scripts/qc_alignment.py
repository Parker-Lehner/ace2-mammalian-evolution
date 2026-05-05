#!/usr/bin/env python3
"""QC MAFFT protein alignment for ACE2."""

from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ALIGNMENT = ROOT / "results" / "alignments" / "ace2_mammalia_aligned.faa"
OUT = ROOT / "results" / "qc" / "ace2_alignment_qc.tsv"
SUMMARY = ROOT / "results" / "qc" / "ace2_alignment_qc_summary.md"


def parse_fasta(path: Path) -> list[tuple[str, str]]:
    records: list[tuple[str, str]] = []
    header = None
    parts: list[str] = []
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


def main() -> int:
    if not ALIGNMENT.exists():
        raise SystemExit(f"Missing alignment: {ALIGNMENT}. Run `make align` first.")
    records = parse_fasta(ALIGNMENT)
    if not records:
        raise SystemExit("Alignment contains no records.")
    aln_lengths = {len(seq) for _, seq in records}
    if len(aln_lengths) != 1:
        raise SystemExit(f"Alignment records have inconsistent lengths: {sorted(aln_lengths)[:10]}")
    aln_len = aln_lengths.pop()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    flags = []
    with OUT.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=[
                "sequence_id",
                "alignment_length",
                "ungapped_length",
                "gap_fraction",
                "missing_fraction",
                "qc_flag",
            ],
            delimiter="\t",
        )
        writer.writeheader()
        for header, seq in records:
            seq_id = header.split()[0]
            gaps = seq.count("-")
            missing = sum(1 for aa in seq if aa.upper() in {"X", "?", "*"})
            ungapped = aln_len - gaps
            gap_fraction = gaps / aln_len if aln_len else 1
            missing_fraction = missing / aln_len if aln_len else 1
            flag = "pass"
            if ungapped < 650 or ungapped > 950:
                flag = "ungapped_length_outlier"
            elif gap_fraction > 0.25:
                flag = "gap_heavy"
            elif missing_fraction > 0.05:
                flag = "missing_heavy"
            flags.append(flag)
            writer.writerow(
                {
                    "sequence_id": seq_id,
                    "alignment_length": aln_len,
                    "ungapped_length": ungapped,
                    "gap_fraction": f"{gap_fraction:.6f}",
                    "missing_fraction": f"{missing_fraction:.6f}",
                    "qc_flag": flag,
                }
            )
    counts = {flag: flags.count(flag) for flag in sorted(set(flags))}
    lines = [
        "# ACE2 Alignment QC Summary",
        "",
        f"- Records: {len(records)}",
        f"- Alignment length: {aln_len}",
        f"- QC flags: {counts}",
        f"- QC table: `{OUT.relative_to(ROOT)}`",
    ]
    SUMMARY.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {OUT}")
    print(f"Wrote {SUMMARY}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
