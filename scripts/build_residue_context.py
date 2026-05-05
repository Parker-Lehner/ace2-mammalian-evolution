#!/usr/bin/env python3
"""Build residue-variation context for ACE2 selection candidate sites."""

from __future__ import annotations

import csv
import math
from collections import Counter, defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PROTEIN_ALIGNMENT = ROOT / "results" / "alignments" / "ace2_mammalia_aligned.faa"
SELECTION_SUMMARY = ROOT / "results" / "selection" / "ace2_selection_site_summary.tsv"
METADATA = ROOT / "data" / "processed" / "ace2_mammalia_curated_metadata.tsv"
TARGETS = ROOT / "config" / "target_species.tsv"
OUT_TSV = ROOT / "results" / "selection" / "ace2_candidate_residue_context.tsv"
OUT_MD = ROOT / "results" / "selection" / "ace2_candidate_residue_context.md"


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


def load_metadata() -> dict[str, dict[str, str]]:
    with METADATA.open(encoding="utf-8") as handle:
        return {row["sequence_id"]: row for row in csv.DictReader(handle, delimiter="\t")}


def target_match(scientific_name: str, targets: list[dict[str, str]]) -> dict[str, str] | None:
    for row in targets:
        target = row["scientific_name"]
        if scientific_name == target or scientific_name.startswith(target + " ") or target.startswith(scientific_name + " "):
            return row
    return None


def load_target_labels(metadata: dict[str, dict[str, str]]) -> dict[str, dict[str, str]]:
    with TARGETS.open(encoding="utf-8") as handle:
        targets = list(csv.DictReader(handle, delimiter="\t"))
    labels = {}
    for seq_id, row in metadata.items():
        target = target_match(row["scientific_name"], targets)
        if target:
            labels[seq_id] = target
    return labels


def entropy(counter: Counter[str]) -> float:
    total = sum(counter.values())
    if total == 0:
        return 0.0
    return -sum((count / total) * math.log2(count / total) for count in counter.values() if count)


def format_counts(counter: Counter[str], limit: int = 8) -> str:
    return ";".join(f"{res}:{count}" for res, count in counter.most_common(limit))


def format_target_residues(alignment: dict[str, str], labels: dict[str, dict[str, str]], column_index: int, habitat: str) -> str:
    rows = []
    for seq_id, label in labels.items():
        if label["habitat_class"] != habitat or seq_id not in alignment:
            continue
        residue = alignment[seq_id][column_index]
        rows.append(f"{label['scientific_name']}={residue}")
    return ";".join(sorted(rows))


def main() -> int:
    for path in [PROTEIN_ALIGNMENT, SELECTION_SUMMARY, METADATA, TARGETS]:
        if not path.exists():
            raise SystemExit(f"Missing required file: {path}")

    alignment = parse_fasta(PROTEIN_ALIGNMENT)
    metadata = load_metadata()
    labels = load_target_labels(metadata)
    selection_rows = []
    with SELECTION_SUMMARY.open(encoding="utf-8") as handle:
        for row in csv.DictReader(handle, delimiter="\t"):
            if row["both_fubar_0_90_and_meme_0_10"] == "true":
                selection_rows.append(row)

    rows = []
    for row in selection_rows:
        site = int(row["alignment_site"])
        column_index = site - 1
        residues = Counter(seq[column_index] for seq in alignment.values() if column_index < len(seq) and seq[column_index] != "-")
        target_residues = Counter(
            alignment[seq_id][column_index]
            for seq_id in labels
            if seq_id in alignment and alignment[seq_id][column_index] != "-"
        )
        total = sum(residues.values())
        human_residue = row["human_residue"]
        human_count = residues.get(human_residue, 0)
        rows.append(
            {
                "alignment_site": row["alignment_site"],
                "human_ace2_position": row["human_ace2_position"],
                "human_residue": human_residue,
                "domain": row["domain"],
                "feature_annotation": row["feature_annotation"],
                "fubar_posterior_positive": row["fubar_posterior_positive"],
                "meme_p_value": row["meme_p_value"],
                "species_with_residue": total,
                "distinct_residue_states": len(residues),
                "shannon_entropy": f"{entropy(residues):.4f}",
                "human_residue_frequency": f"{(human_count / total) if total else 0:.4f}",
                "top_residue_counts_all_taxa": format_counts(residues),
                "target_residue_counts": format_counts(target_residues),
                "target_aquatic_residues": format_target_residues(alignment, labels, column_index, "aquatic"),
                "target_semiaquatic_residues": format_target_residues(alignment, labels, column_index, "semiaquatic"),
                "target_terrestrial_residues": format_target_residues(alignment, labels, column_index, "terrestrial"),
            }
        )

    OUT_TSV.parent.mkdir(parents=True, exist_ok=True)
    with OUT_TSV.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()), delimiter="\t")
        writer.writeheader()
        writer.writerows(rows)

    domain_counts = Counter(row["domain"] for row in rows)
    feature_counts = Counter(row["feature_annotation"] or "unannotated" for row in rows)
    with OUT_MD.open("w", encoding="utf-8") as handle:
        handle.write("# ACE2 Candidate Residue Context\n\n")
        handle.write("This table adds residue-variation context to FUBAR/MEME overlap sites. It is designed for prioritization and figure building, not as final functional proof.\n\n")
        handle.write(f"- Candidate overlap sites summarized: {len(rows)}\n")
        handle.write(f"- Target species with habitat labels matched: {len(labels)}\n")
        handle.write("- Domain distribution: " + ", ".join(f"{k}={v}" for k, v in sorted(domain_counts.items())) + "\n")
        handle.write("- Feature distribution: " + ", ".join(f"{k}={v}" for k, v in sorted(feature_counts.items())) + "\n")
        handle.write(f"- Full table: `{OUT_TSV.relative_to(ROOT)}`\n\n")
        handle.write("## Highest-Priority Manual Review Sites\n\n")
        handle.write("| Human position | Residue | Domain | Feature | Residue states | Human residue frequency | FUBAR posterior | MEME p |\n")
        handle.write("| ---: | --- | --- | --- | ---: | ---: | ---: | ---: |\n")
        priority = sorted(rows, key=lambda r: (r["feature_annotation"] == "", float(r["meme_p_value"])))
        for row in priority[:12]:
            handle.write(
                f"| {row['human_ace2_position']} | {row['human_residue']} | {row['domain']} | "
                f"{row['feature_annotation'] or 'unannotated'} | {row['distinct_residue_states']} | "
                f"{row['human_residue_frequency']} | {row['fubar_posterior_positive']} | {row['meme_p_value']} |\n"
            )

    print(f"Wrote {OUT_TSV}")
    print(f"Wrote {OUT_MD}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
