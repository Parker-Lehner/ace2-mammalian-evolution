#!/usr/bin/env python3
"""Create a vector ACE2 domain/selection-site figure from local outputs."""

from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SUMMARY = ROOT / "results" / "selection" / "ace2_selection_site_summary.tsv"
OUT = ROOT / "results" / "figures" / "ace2_selection_domain_map.svg"

WIDTH = 1500
HEIGHT = 620
LEFT = 110
RIGHT = 80
TRACK_Y = 180
TRACK_H = 44
PROTEIN_LEN = 805


def x_for_position(position: int) -> float:
    return LEFT + (position - 1) / (PROTEIN_LEN - 1) * (WIDTH - LEFT - RIGHT)


def svg_escape(text: str) -> str:
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def domain_color(domain: str) -> str:
    return {
        "signal_peptide_or_n_terminal": "#8a8f98",
        "peptidase_domain": "#2f6fbb",
        "collectrin_like_region": "#2f9b77",
        "membrane_proximal_or_transmembrane": "#b66b2d",
    }.get(domain, "#666666")


def main() -> int:
    if not SUMMARY.exists():
        raise SystemExit("Missing selection summary; run `make selection-summary` first.")
    rows = []
    with SUMMARY.open(encoding="utf-8") as handle:
        for row in csv.DictReader(handle, delimiter="\t"):
            if row["both_fubar_0_90_and_meme_0_10"] == "true" and row["human_ace2_position"]:
                rows.append(row)

    OUT.parent.mkdir(parents=True, exist_ok=True)
    domains = [
        ("N-terminal/signal", 1, 17, "#8a8f98"),
        ("Peptidase domain", 18, 615, "#2f6fbb"),
        ("Collectrin-like region", 616, 739, "#2f9b77"),
        ("Membrane-proximal/TM", 740, 768, "#b66b2d"),
        ("C-terminal tail", 769, 805, "#6a737d"),
    ]

    lines = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{HEIGHT}" viewBox="0 0 {WIDTH} {HEIGHT}" role="img" aria-labelledby="title desc">',
        "<title id=\"title\">ACE2 candidate selection sites mapped to human ACE2 protein coordinates</title>",
        "<desc id=\"desc\">Domain map showing FUBAR and MEME overlap sites across human ACE2 coordinates.</desc>",
        "<rect width=\"100%\" height=\"100%\" fill=\"#ffffff\"/>",
        "<text x=\"110\" y=\"70\" font-family=\"Arial, Helvetica, sans-serif\" font-size=\"34\" font-weight=\"700\" fill=\"#20242a\">ACE2 residue-level selection screen mapped to human coordinates</text>",
        "<text x=\"110\" y=\"108\" font-family=\"Arial, Helvetica, sans-serif\" font-size=\"19\" fill=\"#4a515b\">Sites shown meet both exploratory thresholds: FUBAR posterior &gt;= 0.90 and MEME p &lt;= 0.10. Functional interpretation requires structural/literature review.</text>",
    ]

    for label, start, end, color in domains:
        x1 = x_for_position(start)
        x2 = x_for_position(end)
        lines.append(f'<rect x="{x1:.1f}" y="{TRACK_Y}" width="{x2-x1:.1f}" height="{TRACK_H}" rx="5" fill="{color}" opacity="0.88"/>')
        label_x = (x1 + x2) / 2
        lines.append(f'<text x="{label_x:.1f}" y="{TRACK_Y + 77}" text-anchor="middle" font-family="Arial, Helvetica, sans-serif" font-size="16" fill="#20242a">{svg_escape(label)}</text>')
        lines.append(f'<text x="{label_x:.1f}" y="{TRACK_Y + 99}" text-anchor="middle" font-family="Arial, Helvetica, sans-serif" font-size="13" fill="#59606a">{start}-{end}</text>')

    for tick in [1, 100, 200, 300, 400, 500, 600, 700, 805]:
        x = x_for_position(tick)
        lines.append(f'<line x1="{x:.1f}" y1="{TRACK_Y - 11}" x2="{x:.1f}" y2="{TRACK_Y - 2}" stroke="#20242a" stroke-width="1"/>')
        lines.append(f'<text x="{x:.1f}" y="{TRACK_Y - 20}" text-anchor="middle" font-family="Arial, Helvetica, sans-serif" font-size="13" fill="#20242a">{tick}</text>')

    label_offsets = {}
    for row in rows:
        pos = int(row["human_ace2_position"])
        x = x_for_position(pos)
        label_offsets[pos] = label_offsets.get(pos, 0) + 1
        y_top = 340 + (label_offsets[pos] - 1) * 18
        color = "#d13f31" if row["feature_annotation"] else domain_color(row["domain"])
        radius = 7 if row["feature_annotation"] else 5
        lines.append(f'<line x1="{x:.1f}" y1="{TRACK_Y + TRACK_H}" x2="{x:.1f}" y2="{y_top}" stroke="{color}" stroke-width="2" opacity="0.82"/>')
        lines.append(f'<circle cx="{x:.1f}" cy="{TRACK_Y + TRACK_H + 3}" r="{radius}" fill="{color}" stroke="#ffffff" stroke-width="2"/>')
        label = f'{row["human_residue"]}{pos}'
        if row["feature_annotation"]:
            label += "*"
        lines.append(f'<text x="{x:.1f}" y="{y_top + 20}" text-anchor="middle" font-family="Arial, Helvetica, sans-serif" font-size="14" fill="#20242a">{svg_escape(label)}</text>')

    legend_y = 520
    legend = [
        ("#d13f31", "Provisional functional feature overlap"),
        ("#2f6fbb", "Peptidase-domain candidate"),
        ("#2f9b77", "Collectrin-like candidate"),
        ("#b66b2d", "Membrane-proximal/TM candidate"),
    ]
    x = 110
    for color, label in legend:
        lines.append(f'<circle cx="{x}" cy="{legend_y}" r="7" fill="{color}"/>')
        lines.append(f'<text x="{x + 15}" y="{legend_y + 5}" font-family="Arial, Helvetica, sans-serif" font-size="15" fill="#20242a">{svg_escape(label)}</text>')
        x += 330

    lines.append('<text x="110" y="575" font-family="Arial, Helvetica, sans-serif" font-size="13" fill="#59606a">Asterisk marks overlap with provisional residue annotation in config/residue_annotations.tsv. Coordinates are human ACE2 positions.</text>')
    lines.append("</svg>")
    OUT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {OUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
