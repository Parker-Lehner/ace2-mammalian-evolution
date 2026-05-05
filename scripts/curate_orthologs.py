#!/usr/bin/env python3
"""Apply conservative ACE2 ortholog curation rules to raw NCBI FASTA records."""

from __future__ import annotations

import csv
import re
from collections import OrderedDict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RAW_FASTA = ROOT / "data" / "raw" / "ncbi" / "ncbi_ace2_mammalia_raw.faa"
RAW_META = ROOT / "data" / "raw" / "ncbi" / "ncbi_ace2_mammalia_raw_metadata.tsv"
OUT_FASTA = ROOT / "data" / "processed" / "ace2_mammalia_curated.faa"
OUT_META = ROOT / "data" / "processed" / "ace2_mammalia_curated_metadata.tsv"
REJECTS = ROOT / "data" / "interim" / "ace2_mammalia_rejected.tsv"


def parse_fasta(path: Path) -> list[dict[str, str]]:
    records: list[dict[str, str]] = []
    header = None
    seq_parts: list[str] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith(">"):
            if header:
                records.append({"header": header, "sequence": "".join(seq_parts)})
            header = line[1:].strip()
            seq_parts = []
        elif line.strip():
            seq_parts.append(line.strip())
    if header:
        records.append({"header": header, "sequence": "".join(seq_parts)})
    return records


def accession(header: str) -> str:
    return header.split()[0].split("|")[-1]


def species_from_header(header: str) -> str:
    match = re.search(r"\[([A-Z][A-Za-z0-9_. -]+)\]$", header)
    return match.group(1) if match else ""


def is_reject(header: str, seq: str) -> str:
    lower = header.lower()
    if "partial" in lower:
        return "partial_header"
    if "pseudogene" in lower:
        return "pseudogene_header"
    if "angiotensin-converting enzyme 2" not in lower and "ace2" not in lower:
        return "not_named_ace2"
    if len(seq) < 650:
        return "too_short"
    if len(seq) > 950:
        return "too_long"
    invalid = sorted(set(seq) - set("ABCDEFGHIKLMNPQRSTVWXYZUO*-"))
    if invalid:
        return f"invalid_residues:{''.join(invalid)}"
    return ""


def sanitize_id(text: str) -> str:
    return re.sub(r"[^A-Za-z0-9_.-]+", "_", text).strip("_")


def main() -> int:
    if not RAW_FASTA.exists():
        raise SystemExit(f"Missing {RAW_FASTA}; run `make fetch-ncbi-ace2` first.")
    records = parse_fasta(RAW_FASTA)
    meta_by_accession = {}
    if RAW_META.exists():
        with RAW_META.open(encoding="utf-8") as handle:
            for row in csv.DictReader(handle, delimiter="\t"):
                meta_by_accession[row["accession"]] = row

    kept: OrderedDict[str, dict[str, str]] = OrderedDict()
    rejects: list[dict[str, str]] = []
    for rec in records:
        acc = accession(rec["header"])
        species = species_from_header(rec["header"])
        reason = is_reject(rec["header"], rec["sequence"])
        if not species:
            reason = reason or "missing_species_name"
        if reason:
            rejects.append({"accession": acc, "species": species, "reason": reason, "header": rec["header"]})
            continue
        current = kept.get(species)
        if current is None or len(rec["sequence"]) > len(current["sequence"]):
            kept[species] = {**rec, "accession": acc, "species": species}

    OUT_FASTA.parent.mkdir(parents=True, exist_ok=True)
    with OUT_FASTA.open("w", encoding="utf-8") as fasta, OUT_META.open("w", newline="", encoding="utf-8") as meta:
        writer = csv.DictWriter(
            meta,
            fieldnames=["sequence_id", "accession", "scientific_name", "sequence_length", "header", "source_db", "retrieved_at_utc"],
            delimiter="\t",
        )
        writer.writeheader()
        for species, rec in kept.items():
            seq_id = f"{sanitize_id(species)}|{rec['accession']}"
            fasta.write(f">{seq_id} {rec['header']}\n")
            seq = rec["sequence"].replace("*", "")
            for i in range(0, len(seq), 80):
                fasta.write(seq[i : i + 80] + "\n")
            raw = meta_by_accession.get(rec["accession"], {})
            writer.writerow(
                {
                    "sequence_id": seq_id,
                    "accession": rec["accession"],
                    "scientific_name": species,
                    "sequence_length": len(seq),
                    "header": rec["header"],
                    "source_db": raw.get("source_db", "NCBI RefSeq protein via E-utilities"),
                    "retrieved_at_utc": raw.get("retrieved_at_utc", ""),
                }
            )

    REJECTS.parent.mkdir(parents=True, exist_ok=True)
    with REJECTS.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["accession", "species", "reason", "header"], delimiter="\t")
        writer.writeheader()
        writer.writerows(rejects)

    print(f"Kept {len(kept)} one-per-species ACE2 records in {OUT_FASTA}")
    print(f"Rejected {len(rejects)} records in {REJECTS}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
