# Reproducibility

This release is designed to preserve the exact evidence supporting the manuscript. The fastest audit path is:

1. Inspect `results/evidence_traceability.tsv`.
2. Confirm manuscript values against `results/`.
3. Inspect `data/processed/` for taxon metadata, alignment QC, codon status, and human ACE2 coordinate mapping.
4. Use `scripts/` and `environment.yml` for full reruns where the complete local bioinformatics toolchain is available.

The current manuscript uses BUSTED as the primary foreground-selection evidence, aBSREL as branch-level prioritization, reduced fixed-branch PAML as sensitivity evidence, and enrichment tests as exploratory prioritization.
