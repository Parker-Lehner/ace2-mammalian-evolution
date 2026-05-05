#!/usr/bin/env python3
"""Write the manuscript claim-to-evidence map used before journal submission."""

from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "manuscript" / "claim_map.tsv"


CLAIMS = [
    (
        "ACE2 domain-scale architecture is conserved across mammals",
        "Generated sequence/domain metrics and alignment/domain annotations",
        "Do not claim until curated >=120 species and domain annotation QC pass.",
    ),
    (
        "Aquatic/diving ecology is not expected to produce myoglobin-like whole-protein convergence in ACE2",
        "PGLS/OU models plus myoglobin literature benchmark",
        "Frame as tested hypothesis; retain null models.",
    ),
    (
        "Residue-level ACE2 evolution may occur in functional regions despite broad architectural constraint",
        "MEME/FUBAR/PAML outputs and structural residue maps",
        "Only call adaptive when selection model and residue context support it.",
    ),
    (
        "Ecological gradients may explain ACE2 evolution better than binary habitat coding",
        "Model comparison using dive depth, dive duration, body mass, foraging depth",
        "Requires curated trait sources; no imputation without citation.",
    ),
    (
        "Pathway-level adaptation may distribute signal across RAS/hypoxia/water-balance genes",
        "Light pathway-gene ortholog/selection screen",
        "Secondary analysis; not main burden of proof.",
    ),
]


def main() -> int:
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["claim", "required_evidence", "submission_guardrail"], delimiter="\t")
        writer.writeheader()
        for claim, evidence, guardrail in CLAIMS:
            writer.writerow({"claim": claim, "required_evidence": evidence, "submission_guardrail": guardrail})
    print(f"Wrote {OUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
