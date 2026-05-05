#!/usr/bin/env python3
"""Fetch UniProt fallback ACE2-like records for priority taxa missing from RefSeq."""

from __future__ import annotations

import csv
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
COVERAGE = ROOT / "results" / "qc" / "target_species_coverage.tsv"
OUT_FASTA = ROOT / "data" / "raw" / "uniprot" / "uniprot_ace2_fallback.faa"
OUT_META = ROOT / "data" / "raw" / "uniprot" / "uniprot_ace2_fallback_metadata.tsv"


def uniprot_search(species: str) -> list[dict[str, str]]:
    query = f'(gene:ACE2) AND (organism_name:"{species}")'
    params = {
        "query": query,
        "fields": "accession,reviewed,protein_name,organism_name,length,sequence",
        "format": "tsv",
        "size": "5",
    }
    url = "https://rest.uniprot.org/uniprotkb/search?" + urllib.parse.urlencode(params)
    with urllib.request.urlopen(url, timeout=60) as handle:
        text = handle.read().decode("utf-8")
    lines = [line for line in text.splitlines() if line.strip()]
    if len(lines) < 2:
        return []
    reader = csv.DictReader(lines, delimiter="\t")
    return list(reader)


def choose_record(rows: list[dict[str, str]]) -> dict[str, str] | None:
    if not rows:
        return None
    def score(row: dict[str, str]) -> tuple[int, int, int]:
        reviewed = 1 if row.get("Reviewed", "").lower() == "reviewed" else 0
        name = row.get("Protein names", "").lower()
        ace2_like = 1 if "angiotensin-converting enzyme 2" in name or "ace2" in name else 0
        length = int(row.get("Length") or 0)
        length_ok = 1 if 650 <= length <= 950 else 0
        return (reviewed, ace2_like + length_ok, length)
    return sorted(rows, key=score, reverse=True)[0]


def review_status(row: dict[str, str]) -> str:
    name = row.get("Protein names", "").lower()
    length = int(row.get("Length") or 0)
    name_ok = "angiotensin-converting enzyme 2" in name or "ace2" in name
    length_ok = 650 <= length <= 950
    if name_ok and length_ok:
        return "retrieved_candidate_high_confidence_manual_review_required"
    if length_ok:
        return "retrieved_candidate_name_ambiguous_manual_review_required"
    return "retrieved_candidate_length_or_name_suspect_manual_review_required"


def main() -> int:
    if not COVERAGE.exists():
        raise SystemExit("Run `make qc` before UniProt fallback retrieval.")
    OUT_FASTA.parent.mkdir(parents=True, exist_ok=True)
    missing = []
    with COVERAGE.open(encoding="utf-8") as handle:
        for row in csv.DictReader(handle, delimiter="\t"):
            if row["fallback_needed"].startswith("yes"):
                missing.append(row)

    retrieved = []
    with OUT_FASTA.open("w", encoding="utf-8") as fasta:
        for row in missing:
            records = uniprot_search(row["scientific_name"])
            chosen = choose_record(records)
            if not chosen:
                retrieved.append({**row, "uniprot_accession": "", "status": "not_found", "reviewed": "", "length": "", "protein_name": "", "organism": ""})
                continue
            accession = chosen["Entry"]
            seq = chosen["Sequence"]
            header = f"{row['scientific_name'].replace(' ', '_')}|{accession} {chosen['Protein names']} [{chosen['Organism']}]"
            fasta.write(f">{header}\n")
            for i in range(0, len(seq), 80):
                fasta.write(seq[i : i + 80] + "\n")
            retrieved.append(
                {
                    **row,
                    "uniprot_accession": accession,
                    "status": review_status(chosen),
                    "reviewed": chosen["Reviewed"],
                    "length": chosen["Length"],
                    "protein_name": chosen["Protein names"],
                    "organism": chosen["Organism"],
                }
            )

    with OUT_META.open("w", newline="", encoding="utf-8") as meta:
        fieldnames = [
            "scientific_name",
            "common_name",
            "group",
            "priority",
            "uniprot_accession",
            "status",
            "reviewed",
            "length",
            "protein_name",
            "organism",
            "retrieved_at_utc",
        ]
        writer = csv.DictWriter(meta, fieldnames=fieldnames, delimiter="\t")
        writer.writeheader()
        now = datetime.now(timezone.utc).isoformat()
        for row in retrieved:
            writer.writerow({key: row.get(key, "") for key in fieldnames[:-1]} | {"retrieved_at_utc": now})

    print(f"Wrote {OUT_FASTA}")
    print(f"Wrote {OUT_META}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
