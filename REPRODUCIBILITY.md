# Reproducibility

This repository preserves the public-data analysis package for `Ecological and Lineage-Associated Molecular Evolution of ACE2 Across Mammals`.

## Minimum Checks

```bash
make status
```

## Full Workflow

The workflow uses public sequence records, curated metadata, alignment QC, codon-status checks, human ACE2 coordinate mapping, HyPhy selection models, reduced PAML checks, and figure-generation scripts. Some full reruns require local installations of MAFFT, IQ-TREE, HyPhy, PAML, Python, and R packages specified in `environment.yml`.

## Traceability

Manuscript numerical claims are traceable to tab-delimited files in `results/` and `data/processed/`. Supplementary table descriptions are provided in `supplement/Supplementary_Information_JME.md`.
