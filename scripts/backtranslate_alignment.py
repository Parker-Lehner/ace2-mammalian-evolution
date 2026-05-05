#!/usr/bin/env python3
"""Back-translate ACE2 protein alignment using retrieved candidate CDS records."""

from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PROT_ALN = ROOT / "results" / "alignments" / "ace2_mammalia_aligned.faa"
CDS_FASTA = ROOT / "data" / "raw" / "ncbi" / "ace2_candidate_cds.fna"
OUT = ROOT / "data" / "processed" / "ace2_mammalia_codon_aligned.fna"
STATUS = ROOT / "data" / "processed" / "ace2_codon_alignment_status.tsv"


CODE = {
    "TTT": "F", "TTC": "F", "TTA": "L", "TTG": "L", "TCT": "S", "TCC": "S", "TCA": "S", "TCG": "S",
    "TAT": "Y", "TAC": "Y", "TAA": "*", "TAG": "*", "TGT": "C", "TGC": "C", "TGA": "*", "TGG": "W",
    "CTT": "L", "CTC": "L", "CTA": "L", "CTG": "L", "CCT": "P", "CCC": "P", "CCA": "P", "CCG": "P",
    "CAT": "H", "CAC": "H", "CAA": "Q", "CAG": "Q", "CGT": "R", "CGC": "R", "CGA": "R", "CGG": "R",
    "ATT": "I", "ATC": "I", "ATA": "I", "ATG": "M", "ACT": "T", "ACC": "T", "ACA": "T", "ACG": "T",
    "AAT": "N", "AAC": "N", "AAA": "K", "AAG": "K", "AGT": "S", "AGC": "S", "AGA": "R", "AGG": "R",
    "GTT": "V", "GTC": "V", "GTA": "V", "GTG": "V", "GCT": "A", "GCC": "A", "GCA": "A", "GCG": "A",
    "GAT": "D", "GAC": "D", "GAA": "E", "GAG": "E", "GGT": "G", "GGC": "G", "GGA": "G", "GGG": "G",
}


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


def parse_alignment(path: Path) -> list[tuple[str, str]]:
    records = []
    header = None
    parts = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith(">"):
            if header:
                records.append((header.split()[0], "".join(parts)))
            header = line[1:].strip()
            parts = []
        elif line.strip():
            parts.append(line.strip())
    if header:
        records.append((header.split()[0], "".join(parts)))
    return records


def translate(cds: str) -> str:
    seq = cds.upper().replace("U", "T")
    aas = []
    for i in range(0, len(seq) - 2, 3):
        aas.append(CODE.get(seq[i : i + 3], "X"))
    prot = "".join(aas)
    return prot[:-1] if prot.endswith("*") else prot


def codon_qc(codon_alignment: list[str]) -> tuple[int, int]:
    internal_stops = 0
    ambiguous_codons = 0
    for codon in codon_alignment:
        if codon == "---":
            continue
        if "-" in codon or len(codon) != 3 or any(base not in "ACGT" for base in codon):
            ambiguous_codons += 1
            continue
        if CODE.get(codon, "X") == "*":
            internal_stops += 1
    return internal_stops, ambiguous_codons


def main() -> int:
    if not PROT_ALN.exists():
        raise SystemExit("Run `make align` before codon alignment.")
    if not CDS_FASTA.exists():
        raise SystemExit("Run `make fetch-cds` before codon alignment.")
    protein_alignment = parse_alignment(PROT_ALN)
    cds = parse_fasta(CDS_FASTA)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    kept = 0
    with OUT.open("w", encoding="utf-8") as out, STATUS.open("w", newline="", encoding="utf-8") as status:
        writer = csv.DictWriter(
            status,
            fieldnames=[
                "sequence_id",
                "status",
                "protein_ungapped_length",
                "translated_cds_length",
                "codon_alignment_length",
                "internal_stop_codons",
                "ambiguous_codons",
            ],
            delimiter="\t",
        )
        writer.writeheader()
        for seq_id, aln_protein in protein_alignment:
            ungapped = aln_protein.replace("-", "")
            seq_cds = cds.get(seq_id, "").upper().replace("U", "T")
            translated = translate(seq_cds) if seq_cds else ""
            if not seq_cds:
                writer.writerow({"sequence_id": seq_id, "status": "missing_cds", "protein_ungapped_length": len(ungapped), "translated_cds_length": 0, "codon_alignment_length": 0, "internal_stop_codons": 0, "ambiguous_codons": 0})
                continue
            if abs(len(translated) - len(ungapped)) > 5:
                writer.writerow({"sequence_id": seq_id, "status": "translation_length_mismatch", "protein_ungapped_length": len(ungapped), "translated_cds_length": len(translated), "codon_alignment_length": 0, "internal_stop_codons": 0, "ambiguous_codons": 0})
                continue
            codons = [seq_cds[i : i + 3] for i in range(0, len(seq_cds) - 2, 3)]
            codon_i = 0
            codon_aln = []
            for aa in aln_protein:
                if aa == "-":
                    codon_aln.append("---")
                else:
                    if codon_i >= len(codons):
                        codon_aln = []
                        break
                    codon_aln.append(codons[codon_i])
                    codon_i += 1
            if not codon_aln:
                writer.writerow({"sequence_id": seq_id, "status": "backtranslation_failed", "protein_ungapped_length": len(ungapped), "translated_cds_length": len(translated), "codon_alignment_length": 0, "internal_stop_codons": 0, "ambiguous_codons": 0})
                continue
            internal_stops, ambiguous_codons = codon_qc(codon_aln)
            if internal_stops:
                writer.writerow({"sequence_id": seq_id, "status": "excluded_internal_stop", "protein_ungapped_length": len(ungapped), "translated_cds_length": len(translated), "codon_alignment_length": 0, "internal_stop_codons": internal_stops, "ambiguous_codons": ambiguous_codons})
                continue
            if ambiguous_codons:
                writer.writerow({"sequence_id": seq_id, "status": "excluded_ambiguous_codon", "protein_ungapped_length": len(ungapped), "translated_cds_length": len(translated), "codon_alignment_length": 0, "internal_stop_codons": internal_stops, "ambiguous_codons": ambiguous_codons})
                continue
            aligned = "".join(codon_aln)
            out.write(f">{seq_id}\n")
            for i in range(0, len(aligned), 90):
                out.write(aligned[i : i + 90] + "\n")
            kept += 1
            writer.writerow({"sequence_id": seq_id, "status": "codon_alignment_pass", "protein_ungapped_length": len(ungapped), "translated_cds_length": len(translated), "codon_alignment_length": len(aligned), "internal_stop_codons": internal_stops, "ambiguous_codons": ambiguous_codons})
    if kept == 0:
        OUT.unlink(missing_ok=True)
        raise SystemExit("No sequences passed codon back-translation QC; see status table.")
    print(f"Wrote {kept} codon-aligned sequences to {OUT}")
    print(f"Wrote {STATUS}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
