# Comparative Evolutionary Genomics of ACE2 Reveals Ecological and Lineage-Associated Selection Patterns Across Mammals

This repository contains the public-data analysis package for a planned Journal of Molecular Evolution Article on mammalian ACE2 molecular evolution.

## Author

Parker Lehner  
Independent Researcher, St. James, New York, USA  
Correspondence: lehnerparker@gmail.com

## Claim Boundary

Supported: mammalian ACE2 is broadly conserved but shows ecological and lineage-associated molecular evolutionary heterogeneity.

Not supported: ACE2-driven aquatic/diving causality, viral adaptation inferred from Q24/D30 alone, or fixed-branch PAML as primary proof.

## Repository Contents

- `data/`: public sequence metadata, raw public retrieval outputs, processed coordinate/QC tables
- `results/`: site-level, BUSTED/aBSREL, reduced PAML sensitivity, enrichment, and traceability tables
- `figures/`: source SVG figures
- `scripts/`: retrieval, curation, analysis, figure, and package-generation scripts
- `manuscript/`: manuscript source and BibTeX bibliography

## Reproducibility

Use `make status` for a lightweight environment check. Full reruns require MAFFT, IQ-TREE, HyPhy, PAML, Python, and R packages documented in `environment.yml`. Computationally expensive outputs are archived in `results/`.

## Citation

The repository is Zenodo-ready but does not yet have a DOI. After Zenodo archival, cite the DOI listed in `CITATION.cff`.

## License

Code and documentation are released under the MIT License. Public biological sequence records retain their original database terms.
