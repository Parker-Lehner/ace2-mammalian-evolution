#!/usr/bin/env python3
"""Retrieve candidate CDS records linked to curated ACE2 protein accessions."""

from __future__ import annotations

import csv
import argparse
import json
import sys
import time
import urllib.parse
import urllib.request
from http.client import IncompleteRead
from json import JSONDecodeError
from urllib.error import HTTPError, URLError
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
META = ROOT / "data" / "processed" / "ace2_mammalia_curated_metadata.tsv"
OUT_FASTA = ROOT / "data" / "raw" / "ncbi" / "ace2_candidate_cds.fna"
OUT_STATUS = ROOT / "data" / "processed" / "ace2_cds_retrieval_status.tsv"
EUTILS = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"
EMAIL = "parkerlehner@example.com"
TOOL = "ace2-evolution-gbe"


GENETIC_CODE = {
    "TTT": "F", "TTC": "F", "TTA": "L", "TTG": "L", "TCT": "S", "TCC": "S", "TCA": "S", "TCG": "S",
    "TAT": "Y", "TAC": "Y", "TAA": "*", "TAG": "*", "TGT": "C", "TGC": "C", "TGA": "*", "TGG": "W",
    "CTT": "L", "CTC": "L", "CTA": "L", "CTG": "L", "CCT": "P", "CCC": "P", "CCA": "P", "CCG": "P",
    "CAT": "H", "CAC": "H", "CAA": "Q", "CAG": "Q", "CGT": "R", "CGC": "R", "CGA": "R", "CGG": "R",
    "ATT": "I", "ATC": "I", "ATA": "I", "ATG": "M", "ACT": "T", "ACC": "T", "ACA": "T", "ACG": "T",
    "AAT": "N", "AAC": "N", "AAA": "K", "AAG": "K", "AGT": "S", "AGC": "S", "AGA": "R", "AGG": "R",
    "GTT": "V", "GTC": "V", "GTA": "V", "GTG": "V", "GCT": "A", "GCC": "A", "GCA": "A", "GCG": "A",
    "GAT": "D", "GAC": "D", "GAA": "E", "GAG": "E", "GGT": "G", "GGC": "G", "GGA": "G", "GGG": "G",
}


RETRY_EXCEPTIONS = (HTTPError, URLError, TimeoutError, IncompleteRead, JSONDecodeError)


def read_url_with_retries(url: str, attempts: int = 4) -> str:
    last_error = None
    for attempt in range(1, attempts + 1):
        try:
            with urllib.request.urlopen(url, timeout=90) as handle:
                return handle.read().decode("utf-8")
        except RETRY_EXCEPTIONS as exc:
            last_error = exc
            time.sleep(min(8, attempt * 2))
    raise last_error  # type: ignore[misc]


def eutils_text(endpoint: str, params: dict[str, str]) -> str:
    params = {**params, "tool": TOOL, "email": EMAIL}
    url = f"{EUTILS}/{endpoint}?{urllib.parse.urlencode(params)}"
    return read_url_with_retries(url)


def eutils_json(endpoint: str, params: dict[str, str]) -> dict:
    params = {**params, "tool": TOOL, "email": EMAIL, "retmode": "json"}
    url = f"{EUTILS}/{endpoint}?{urllib.parse.urlencode(params)}"
    last_error = None
    for attempt in range(1, 5):
        try:
            return json.loads(read_url_with_retries(url, attempts=1))
        except JSONDecodeError as exc:
            last_error = exc
            time.sleep(min(8, attempt * 2))
    raise last_error  # type: ignore[misc]


def parse_fasta(text: str) -> list[tuple[str, str]]:
    records = []
    header = None
    parts = []
    for line in text.splitlines():
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


def translate(cds: str) -> str:
    seq = cds.upper().replace("U", "T")
    aas = []
    for i in range(0, len(seq) - 2, 3):
        codon = seq[i : i + 3]
        aas.append(GENETIC_CODE.get(codon, "X"))
    protein = "".join(aas)
    return protein[:-1] if protein.endswith("*") else protein


def best_cds_for_protein(accession: str, protein_len: int) -> tuple[str, str, str]:
    """Return status, nucleotide header, nucleotide sequence."""
    try:
        link = eutils_json("elink.fcgi", {"dbfrom": "protein", "db": "nuccore", "id": accession})
        ids = []
        for linkset in link.get("linksets", []):
            for linkdb in linkset.get("linksetdbs", []):
                for item in linkdb.get("links", []):
                    if isinstance(item, dict):
                        ids.append(str(item.get("id", "")))
                    else:
                        ids.append(str(item))
        ids = [item for item in ids if item]
        if not ids:
            return "no_nuccore_link", "", ""
        # Try a few linked nucleotide records. fasta_cds_na can return multiple CDSs.
        for nucleotide_id in ids[:5]:
            time.sleep(0.34)
            fasta = eutils_text(
                "efetch.fcgi",
                {"db": "nuccore", "id": nucleotide_id, "rettype": "fasta_cds_na", "retmode": "text"},
            )
            for header, seq in parse_fasta(fasta):
                h = header.lower()
                translated = translate(seq)
                length_ok = abs(len(translated) - protein_len) <= 5
                header_ok = accession.lower() in h or "ace2" in h or "angiotensin-converting enzyme 2" in h
                if length_ok and header_ok:
                    return "retrieved_candidate_qc_pass", header, seq
        return "linked_nuccore_no_matching_cds", "", ""
    except Exception as exc:  # noqa: BLE001
        return f"error:{type(exc).__name__}", "", ""


def read_existing_status() -> dict[str, dict[str, str]]:
    if not OUT_STATUS.exists():
        return {}
    with OUT_STATUS.open(encoding="utf-8") as handle:
        return {row["accession"]: row for row in csv.DictReader(handle, delimiter="\t")}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--retry-failures", action="store_true", help="Retry only accessions that are not already QC-passing.")
    args = parser.parse_args()

    if not META.exists():
        raise SystemExit("Missing curated ACE2 metadata; run `make curate-sequences` first.")
    OUT_FASTA.parent.mkdir(parents=True, exist_ok=True)
    OUT_STATUS.parent.mkdir(parents=True, exist_ok=True)
    rows = list(csv.DictReader(META.open(encoding="utf-8"), delimiter="\t"))
    existing = read_existing_status() if args.retry_failures else {}
    if args.retry_failures and not existing:
        raise SystemExit("No existing CDS status table found for --retry-failures.")
    rows_to_fetch = [
        row for row in rows
        if not args.retry_failures or existing.get(row["accession"], {}).get("cds_status") != "retrieved_candidate_qc_pass"
    ]
    now = datetime.now(timezone.utc).isoformat()
    status_by_accession = dict(existing)
    fasta_mode = "a" if args.retry_failures else "w"
    with OUT_FASTA.open(fasta_mode, encoding="utf-8") as fasta:
        for index, row in enumerate(rows_to_fetch, start=1):
            status_text, header, seq = best_cds_for_protein(row["accession"], int(row["sequence_length"]))
            if seq:
                clean_header = " ".join(header.split())
                fasta.write(f">{row['sequence_id']} cds_source={clean_header}\n")
                for i in range(0, len(seq), 80):
                    fasta.write(seq[i : i + 80] + "\n")
            status_by_accession[row["accession"]] = {
                "sequence_id": row["sequence_id"],
                "accession": row["accession"],
                "scientific_name": row["scientific_name"],
                "protein_length": row["sequence_length"],
                "cds_status": status_text,
                "cds_header": header,
                "cds_length": str(len(seq)),
                "retrieved_at_utc": now,
            }
            if index % 10 == 0 or seq or status_text.startswith("error:"):
                print(f"[{index}/{len(rows_to_fetch)}] {row['accession']} {status_text}", file=sys.stderr, flush=True)

    with OUT_STATUS.open("w", newline="", encoding="utf-8") as status:
        writer = csv.DictWriter(
            status,
            fieldnames=["sequence_id", "accession", "scientific_name", "protein_length", "cds_status", "cds_header", "cds_length", "retrieved_at_utc"],
            delimiter="\t",
        )
        writer.writeheader()
        for row in rows:
            writer.writerow(status_by_accession[row["accession"]])
    print(f"Wrote {OUT_FASTA}")
    print(f"Wrote {OUT_STATUS}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
