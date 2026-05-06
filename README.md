# Ecological and Lineage-Associated Molecular Evolution of ACE2 Across Mammals

This repository contains the public-data analysis package for a Journal of Molecular Evolution Article on mammalian ACE2 molecular evolution.

## Author

Parker Lehner  
Independent Researcher, St. James, New York, USA  
Correspondence: lehnerparker@gmail.com

## Claim Boundary

Supported: mammalian ACE2 is broadly conserved while showing ecological and lineage-associated molecular evolutionary heterogeneity.

Not inferred: direct aquatic/diving causality, viral adaptation from Q24/D30 alone, or fixed-branch PAML as primary proof.

## Repository Contents

- `data/processed/`: public sequence metadata, codon status, alignment QC, and coordinate maps.
- `results/`: site-level, BUSTED/aBSREL, reduced PAML, enrichment, and traceability tables.
- `figures/`: source SVG figures.
- `scripts/`: reproducible analysis scripts retained from the project workflow.
- `manuscript/`: final manuscript source and BibTeX bibliography.
- `supplement/`: supplementary table documentation and tab-delimited table files.

## Reproducibility

Use `make status` for a lightweight environment check. Full reruns require MAFFT, IQ-TREE, HyPhy, PAML, Python, and R packages documented in `environment.yml`. Computationally expensive outputs are archived in `results/`.

## Data Availability

The GitHub repository is available at https://github.com/Parker-Lehner/ace2-mammalian-evolution. A versioned Zenodo archive will be created before publication, and the DOI will be added to the accepted version.

## License

Code and documentation are released under the MIT License. Public biological sequence records retain their original database terms.
