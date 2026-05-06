# Supplementary Information

Manuscript title: Ecological and Lineage-Associated Molecular Evolution of ACE2 Across Mammals

Journal target: Journal of Molecular Evolution

Author: Parker Lehner

Affiliation: Independent Researcher, St. James, New York, USA

Corresponding email: lehnerparker@gmail.com

## Overview

This supplementary file documents the tables supplied with the public-data ACE2 molecular evolution analysis. Each table is tab-delimited and is included to support data provenance, reproducibility, model interpretation, or manuscript claim traceability. No private or course-only data are required for the manuscript claims.

## Supplementary Table S1. Curated mammalian ACE2 metadata

File: `ace2_mammalia_curated_metadata.tsv`

Rows: 244; columns: sequence_id, accession, scientific_name, sequence_length, header, source_db, retrieved_at_utc.

Purpose and contents: Lists sequence identifiers, accessions, species names, sequence lengths, headers, source databases, and retrieval dates.

Relevance to manuscript claims: Documents public data provenance and supports the 244-protein dataset count.

Methods connection and reproducibility role: This table links the manuscript narrative to an auditable analysis artifact, allowing reviewers to trace reported counts, filtering decisions, model outputs, or residue mappings back to the local workflow output.

## Supplementary Table S2. Protein alignment quality control

File: `ace2_alignment_qc.tsv`

Rows: 244; columns: sequence_id, alignment_length, ungapped_length, gap_fraction, missing_fraction, qc_flag.

Purpose and contents: Reports alignment length, ungapped length, gap fraction, missing fraction, and QC flags for retained proteins.

Relevance to manuscript claims: Supports sequence-quality filtering and the distinction between protein-level and codon-level analyses.

Methods connection and reproducibility role: This table links the manuscript narrative to an auditable analysis artifact, allowing reviewers to trace reported counts, filtering decisions, model outputs, or residue mappings back to the local workflow output.

## Supplementary Table S3. Codon-alignment eligibility

File: `ace2_codon_alignment_status.tsv`

Rows: 244; columns: sequence_id, status, protein_ungapped_length, translated_cds_length, codon_alignment_length, internal_stop_codons, ambiguous_codons.

Purpose and contents: Summarizes CDS translation checks, codon-alignment length, internal stop codons, ambiguous codons, and inclusion status.

Relevance to manuscript claims: Supports the final 238-taxon codon dataset and the exclusion of 6 problematic CDS records.

Methods connection and reproducibility role: This table links the manuscript narrative to an auditable analysis artifact, allowing reviewers to trace reported counts, filtering decisions, model outputs, or residue mappings back to the local workflow output.

## Supplementary Table S4. Codon-pruned tree report

File: `ace2_mammalia_codon_pruned_tree_report.tsv`

Rows: 7; columns: metric, value.

Purpose and contents: Reports tree/taxon matching metrics for the codon-level selection dataset.

Relevance to manuscript claims: Documents that tree and alignment taxon sets matched for codon-model analyses.

Methods connection and reproducibility role: This table links the manuscript narrative to an auditable analysis artifact, allowing reviewers to trace reported counts, filtering decisions, model outputs, or residue mappings back to the local workflow output.

## Supplementary Table S5. Human ACE2 coordinate map

File: `human_ace2_alignment_coordinate_map.tsv`

Rows: 978; columns: alignment_column_1based, human_ace2_position, human_residue, annotation.

Purpose and contents: Maps alignment columns to human ACE2 residue positions and annotations where available.

Relevance to manuscript claims: Provides the coordinate framework used for residue interpretation and figure mapping.

Methods connection and reproducibility role: This table links the manuscript narrative to an auditable analysis artifact, allowing reviewers to trace reported counts, filtering decisions, model outputs, or residue mappings back to the local workflow output.

## Supplementary Table S6. Site-level selection summary

File: `ace2_selection_site_summary.tsv`

Rows: 978; columns: alignment_site, human_ace2_position, human_residue, domain, feature_annotation, fubar_alpha, fubar_beta, fubar_posterior_positive....

Purpose and contents: Contains FUBAR, MEME, overlap, residue, domain, and annotation fields for ACE2 alignment positions.

Relevance to manuscript claims: Supports the 28 FUBAR, 95 MEME p <= 0.05, and 23 overlap-site counts.

Methods connection and reproducibility role: This table links the manuscript narrative to an auditable analysis artifact, allowing reviewers to trace reported counts, filtering decisions, model outputs, or residue mappings back to the local workflow output.

## Supplementary Table S7. BUSTED foreground evidence

File: `phase5_busted_evidence.tsv`

Rows: 4; columns: foreground_group, lrt, p_value, significant, interpretation.

Purpose and contents: Reports BUSTED likelihood-ratio statistics, p-values, significance, and interpretation by foreground group.

Relevance to manuscript claims: Supports the primary foreground-associated episodic selection results.

Methods connection and reproducibility role: This table links the manuscript narrative to an auditable analysis artifact, allowing reviewers to trace reported counts, filtering decisions, model outputs, or residue mappings back to the local workflow output.

## Supplementary Table S8. aBSREL branch candidates

File: `phase5_absrel_significant_branches.tsv`

Rows: 7; columns: foreground_group, branch, corrected_p_value, uncorrected_p_value, lrt, interpretation.

Purpose and contents: Lists significant branch candidates, corrected p-values, uncorrected p-values, likelihood-ratio statistics, and interpretation fields.

Relevance to manuscript claims: Supports branch-level prioritization of Mesoplodon mirus and Leptonychotes weddellii.

Methods connection and reproducibility role: This table links the manuscript narrative to an auditable analysis artifact, allowing reviewers to trace reported counts, filtering decisions, model outputs, or residue mappings back to the local workflow output.

## Supplementary Table S9. Reduced fixed-branch PAML summary

File: `reduced_fixed_paml_branch_site_summary.tsv`

Rows: 4; columns: foreground_group, alt_lnL, null_lnL, lrt_stat, df, p_value_chi2_df1, alt_np, null_np....

Purpose and contents: Reports alternative/null likelihoods, LRT statistics, p-values, BEB-site fields, and warnings.

Relevance to manuscript claims: Provides secondary model-family support for the same foreground categories as BUSTED.

Methods connection and reproducibility role: This table links the manuscript narrative to an auditable analysis artifact, allowing reviewers to trace reported counts, filtering decisions, model outputs, or residue mappings back to the local workflow output.

## Supplementary Table S10. Candidate-site enrichment summary

File: `candidate_site_enrichment_summary.tsv`

Rows: 6; columns: foreground_group, foreground_size, background_size, candidate_distinguishing, candidate_not_distinguishing, noncandidate_distinguishing, noncandidate_not_distinguishing, odds_ratio_haldane....

Purpose and contents: Reports foreground/background counts, odds ratios, Fisher p-values, BH-FDR values, and interpretation.

Relevance to manuscript claims: Documents exploratory enrichment trends and their limited evidentiary status.

Methods connection and reproducibility role: This table links the manuscript narrative to an auditable analysis artifact, allowing reviewers to trace reported counts, filtering decisions, model outputs, or residue mappings back to the local workflow output.
