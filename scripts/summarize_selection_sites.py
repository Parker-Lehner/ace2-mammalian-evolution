#!/usr/bin/env python3
"""Summarize HyPhy FUBAR/MEME outputs against human ACE2 coordinates."""

from __future__ import annotations

import csv
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
FUBAR = ROOT / "results" / "selection" / "hyphy_fubar" / "ace2_fubar.json"
MEME = ROOT / "results" / "selection" / "hyphy_meme" / "ace2_meme.json"
COORDS = ROOT / "data" / "processed" / "human_ace2_alignment_coordinate_map.tsv"
OUT_TSV = ROOT / "results" / "selection" / "ace2_selection_site_summary.tsv"
OUT_MD = ROOT / "results" / "selection" / "ace2_selection_site_summary.md"


def domain_for_position(position: str) -> str:
    if not position:
        return "alignment_gap_relative_to_human"
    pos = int(position)
    if pos < 18:
        return "signal_peptide_or_n_terminal"
    if 18 <= pos <= 615:
        return "peptidase_domain"
    if 616 <= pos <= 805:
        if 740 <= pos <= 768:
            return "membrane_proximal_or_transmembrane"
        return "collectrin_like_region"
    return "outside_human_reference"


def load_coords() -> dict[int, dict[str, str]]:
    with COORDS.open(encoding="utf-8") as handle:
        return {
            int(row["alignment_column_1based"]): row
            for row in csv.DictReader(handle, delimiter="\t")
        }


def load_hyphy() -> tuple[list[list[float]], list[list[float]]]:
    with FUBAR.open(encoding="utf-8") as handle:
        fubar = json.load(handle)["MLE"]["content"]["0"]
    with MEME.open(encoding="utf-8") as handle:
        meme = json.load(handle)["MLE"]["content"]["0"]
    if len(fubar) != len(meme):
        raise SystemExit(f"FUBAR/MEME site counts differ: {len(fubar)} vs {len(meme)}")
    return fubar, meme


def main() -> int:
    for path in [FUBAR, MEME, COORDS]:
        if not path.exists():
            raise SystemExit(f"Missing required file: {path}")
    coords = load_coords()
    fubar, meme = load_hyphy()
    OUT_TSV.parent.mkdir(parents=True, exist_ok=True)

    rows = []
    for index, (fubar_row, meme_row) in enumerate(zip(fubar, meme, strict=True), start=1):
        coord = coords.get(index, {})
        human_position = coord.get("human_ace2_position", "")
        fubar_pos = float(fubar_row[4])
        fubar_neg = float(fubar_row[3])
        fubar_bayes_factor = float(fubar_row[5])
        meme_p = float(meme_row[6])
        rows.append(
            {
                "alignment_site": index,
                "human_ace2_position": human_position,
                "human_residue": coord.get("human_residue", ""),
                "domain": domain_for_position(human_position),
                "feature_annotation": coord.get("annotation", ""),
                "fubar_alpha": f"{float(fubar_row[0]):.6g}",
                "fubar_beta": f"{float(fubar_row[1]):.6g}",
                "fubar_posterior_positive": f"{fubar_pos:.6g}",
                "fubar_posterior_negative": f"{fubar_neg:.6g}",
                "fubar_bayes_factor_positive": f"{fubar_bayes_factor:.6g}",
                "meme_lrt": f"{float(meme_row[5]):.6g}",
                "meme_p_value": f"{meme_p:.6g}",
                "meme_branches_under_selection": f"{float(meme_row[7]):.6g}",
                "fubar_positive_ge_0_90": str(fubar_pos >= 0.90).lower(),
                "meme_positive_p_le_0_10": str(meme_p <= 0.10).lower(),
                "meme_positive_p_le_0_05": str(meme_p <= 0.05).lower(),
                "both_fubar_0_90_and_meme_0_10": str(fubar_pos >= 0.90 and meme_p <= 0.10).lower(),
            }
        )

    with OUT_TSV.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()), delimiter="\t")
        writer.writeheader()
        writer.writerows(rows)

    fubar_sites = [row for row in rows if row["fubar_positive_ge_0_90"] == "true"]
    meme_010_sites = [row for row in rows if row["meme_positive_p_le_0_10"] == "true"]
    meme_005_sites = [row for row in rows if row["meme_positive_p_le_0_05"] == "true"]
    overlap_sites = [row for row in rows if row["both_fubar_0_90_and_meme_0_10"] == "true"]
    annotated_overlap = [row for row in overlap_sites if row["feature_annotation"]]

    with OUT_MD.open("w", encoding="utf-8") as handle:
        handle.write("# ACE2 Selection Site Summary\n\n")
        handle.write("This is an analysis summary, not a manuscript interpretation. Functional claims still require manual literature/structure review.\n\n")
        handle.write(f"- Sites analyzed: {len(rows)}\n")
        handle.write(f"- FUBAR posterior positive >= 0.90: {len(fubar_sites)}\n")
        handle.write(f"- MEME p <= 0.10: {len(meme_010_sites)}\n")
        handle.write(f"- MEME p <= 0.05: {len(meme_005_sites)}\n")
        handle.write(f"- FUBAR/MEME overlap using FUBAR >= 0.90 and MEME p <= 0.10: {len(overlap_sites)}\n")
        handle.write(f"- Overlap sites with provisional feature annotations: {len(annotated_overlap)}\n")
        handle.write(f"- Full table: `{OUT_TSV.relative_to(ROOT)}`\n\n")
        if overlap_sites:
            handle.write("## Overlap Sites\n\n")
            handle.write("| Alignment site | Human ACE2 position | Residue | Domain | Feature | FUBAR posterior | MEME p |\n")
            handle.write("| --- | --- | --- | --- | --- | ---: | ---: |\n")
            for row in overlap_sites:
                handle.write(
                    f"| {row['alignment_site']} | {row['human_ace2_position']} | {row['human_residue']} | "
                    f"{row['domain']} | {row['feature_annotation']} | {row['fubar_posterior_positive']} | {row['meme_p_value']} |\n"
                )

    print(f"Wrote {OUT_TSV}")
    print(f"Wrote {OUT_MD}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
