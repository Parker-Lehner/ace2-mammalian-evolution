#!/usr/bin/env python3
"""Fetch public NCBI protein FASTA records for ACE2 project setup.

This script intentionally records query terms, retrieval dates, and source URLs.
It uses NCBI E-utilities through the standard library so the bootstrap pipeline
works before the full conda environment is installed.
"""

from __future__ import annotations

import argparse
import csv
import json
import time
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EUTILS = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"
EMAIL = "parkerlehner@example.com"
TOOL = "ace2-evolution-gbe"


def get_json(endpoint: str, params: dict[str, str]) -> dict:
    params = {**params, "tool": TOOL, "email": EMAIL, "retmode": "json"}
    url = f"{EUTILS}/{endpoint}?{urllib.parse.urlencode(params)}"
    with urllib.request.urlopen(url, timeout=60) as handle:
        return json.loads(handle.read().decode("utf-8"))


def get_text(endpoint: str, params: dict[str, str]) -> str:
    params = {**params, "tool": TOOL, "email": EMAIL}
    url = f"{EUTILS}/{endpoint}?{urllib.parse.urlencode(params)}"
    with urllib.request.urlopen(url, timeout=120) as handle:
        return handle.read().decode("utf-8")


def parse_fasta(text: str) -> list[dict[str, str]]:
    records: list[dict[str, str]] = []
    header = None
    seq_parts: list[str] = []
    for line in text.splitlines():
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


def accession_from_header(header: str) -> str:
    token = header.split()[0]
    if "|" in token:
        parts = [p for p in token.split("|") if p]
        return parts[-1]
    return token


def write_fasta(records: list[dict[str, str]], path: Path) -> None:
    with path.open("w", encoding="utf-8") as handle:
        for rec in records:
            handle.write(f">{rec['header']}\n")
            seq = rec["sequence"]
            for i in range(0, len(seq), 80):
                handle.write(seq[i : i + 80] + "\n")


def fetch_human_reference() -> None:
    outdir = ROOT / "data" / "raw" / "ncbi"
    outdir.mkdir(parents=True, exist_ok=True)
    accession = "NP_001358344.1"
    fasta = get_text("efetch.fcgi", {"db": "protein", "id": accession, "rettype": "fasta", "retmode": "text"})
    path = outdir / "human_ACE2_NP_001358344.1.faa"
    path.write_text(fasta, encoding="utf-8")
    meta = {
        "accession": accession,
        "db": "protein",
        "retrieved_at_utc": datetime.now(timezone.utc).isoformat(),
        "source": "NCBI E-utilities efetch",
    }
    (outdir / "human_ACE2_NP_001358344.1.metadata.json").write_text(json.dumps(meta, indent=2), encoding="utf-8")
    print(f"Wrote {path}")


def fetch_ace2_mammals(retmax: int) -> None:
    outdir = ROOT / "data" / "raw" / "ncbi"
    outdir.mkdir(parents=True, exist_ok=True)
    query = 'ACE2[Gene Name] AND Mammalia[Organism] AND srcdb_refseq[PROP] NOT partial[Title]'
    search = get_json("esearch.fcgi", {"db": "protein", "term": query, "retmax": str(retmax), "sort": "relevance"})
    ids = search.get("esearchresult", {}).get("idlist", [])
    if not ids:
        raise SystemExit(f"No NCBI protein IDs returned for query: {query}")
    fasta_parts: list[str] = []
    batch_size = 100
    for i in range(0, len(ids), batch_size):
        batch = ids[i : i + batch_size]
        time.sleep(0.4)
        fasta_parts.append(
            get_text("efetch.fcgi", {"db": "protein", "id": ",".join(batch), "rettype": "fasta", "retmode": "text"})
        )
    fasta = "\n".join(fasta_parts)
    records = parse_fasta(fasta)
    fasta_path = outdir / "ncbi_ace2_mammalia_raw.faa"
    write_fasta(records, fasta_path)

    metadata_path = outdir / "ncbi_ace2_mammalia_raw_metadata.tsv"
    with metadata_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=["accession", "protein_id", "header", "sequence_length", "source_db", "retrieved_at_utc", "query"],
            delimiter="\t",
        )
        writer.writeheader()
        now = datetime.now(timezone.utc).isoformat()
        for protein_id, rec in zip(ids, records):
            writer.writerow(
                {
                    "accession": accession_from_header(rec["header"]),
                    "protein_id": protein_id,
                    "header": rec["header"],
                    "sequence_length": len(rec["sequence"]),
                    "source_db": "NCBI RefSeq protein via E-utilities",
                    "retrieved_at_utc": now,
                    "query": query,
                }
            )

    print(f"Wrote {len(records)} raw ACE2 mammalian protein records to {fasta_path}")
    print(f"Wrote metadata to {metadata_path}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=["human-reference", "ace2-mammals"], required=True)
    parser.add_argument("--retmax", type=int, default=250)
    args = parser.parse_args()
    if args.mode == "human-reference":
        fetch_human_reference()
    else:
        fetch_ace2_mammals(args.retmax)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
