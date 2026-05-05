# Comparative Evolutionary Genomics of ACE2 Reveals Ecological and Lineage-Associated Selection Patterns Across Mammals

Running title: Comparative mammalian ACE2 evolution

Article type: Article

Target journal: Journal of Molecular Evolution

Author: Parker Lehner

Corresponding author: Parker Lehner; Independent Researcher, St. James, New York, USA; lehnerparker@gmail.com; ORCID: none

## Abstract

Angiotensin-converting enzyme 2 (ACE2) is a conserved mammalian protein whose evolutionary history must be interpreted against strong structural and physiological constraint. We assembled a public mammalian ACE2 dataset containing 244 curated protein records and 238 codon-level taxa to test whether ecological foregrounds show localized molecular evolutionary heterogeneity rather than broad domain-scale remodeling. Site-level screens identified 28 FUBAR candidate positive-selection sites, 95 MEME sites at p <= 0.05, and 23 FUBAR/MEME overlap sites. Two overlap residues, Q24 and D30, map to provisional receptor-interface annotations but are treated as structural candidates rather than evidence of viral adaptation. HyPhy BUSTED detected significant episodic diversifying selection on cetacean, deep-diving, aquatic, and marine foreground branch sets, with likelihood-ratio statistics from 48.417 to 68.928 and p-values from 1.53e-11 to 5.55e-16. aBSREL prioritized Mesoplodon mirus and Leptonychotes weddellii as branch-level candidates, while reduced fixed-branch PAML analyses supported the same foreground categories as sensitivity evidence. These results support a bounded conclusion: mammalian ACE2 remains architecturally conserved but shows ecological and lineage-associated molecular evolutionary heterogeneity.

Abstract word count: 165

## Keywords

ACE2; molecular evolution; episodic diversifying selection; marine mammals; codon models; comparative genomics

## Introduction

Angiotensin-converting enzyme 2 (ACE2) was discovered as an ACE-related carboxypeptidase with conserved enzymatic and membrane-associated features (Donoghue et al. 2000; Tipnis et al. 2000). Structural work has shown that ACE2 contains a catalytic peptidase domain with conformational dynamics relevant to ligand binding and catalysis (Towler et al. 2004). Comparative studies of ACE2 have also emphasized conservation across vertebrates while identifying residue-level variation relevant to receptor-interface biology (Damas et al. 2020). These properties make ACE2 a useful system for testing how a constrained mammalian protein can retain broad architecture while exhibiting localized evolutionary heterogeneity.

Marine and diving mammals provide an ecological frame for examining such heterogeneity, but ACE2 is not a myoglobin-like oxygen-storage protein. Myoglobin evolution provides a benchmark for repeated molecular changes associated with diving capacity (Mirceta et al. 2013), whereas ACE2 has primary roles in peptide metabolism and membrane-associated physiology. A defensible molecular-evolution test should therefore avoid assuming that ACE2 mediates diving adaptation and instead ask whether ecological foreground branches show statistically detectable episodic selection or residue-level heterogeneity.

Here, we rebuild the ACE2 analysis as a focused molecular evolution study. We use public mammalian ACE2 ortholog data, site-level codon models, foreground branch tests, branch-level episodic selection scans, and conservative residue/domain annotation. The central hypothesis is that ACE2 remains broadly conserved but may show foreground-associated molecular evolutionary heterogeneity concentrated at particular branches and residues. The analysis explicitly separates supported statistical findings from mechanistic hypotheses requiring functional validation.

## Results

### Public mammalian ACE2 dataset and coordinate framework

The final curated dataset contained 244 mammalian ACE2 protein records. Codon-level analyses retained 238 taxa after excluding 6 records with ambiguous codons or internal stop-codon issues. Human ACE2 coordinate mapping provided a common numbering system for integrating site-level, branch-level, and domain annotations (Fig. 1; Online Resource 1). These filters produced a dataset suitable for comparative molecular evolution while retaining accession-level traceability.

### Site-level screens identify localized ACE2 heterogeneity

FUBAR identified 28 candidate positive-selection sites at posterior probability >= 0.90 (Murrell et al. 2013), while MEME identified 95 sites at p <= 0.05 and 114 sites at p <= 0.10 (Murrell et al. 2012). Under the exploratory overlap threshold, 23 sites were supported by both FUBAR and MEME. Two overlap residues, Q24 and D30 in human ACE2 coordinates, mapped to provisional receptor-interface annotations. These residues are candidates for structural follow-up, not evidence of viral adaptation by themselves (Fig. 2; Online Resource 2).

### Ecological foregrounds show episodic molecular evolutionary heterogeneity

HyPhy BUSTED detected significant episodic diversifying selection on each tested ecological foreground branch set (Murrell et al. 2015). The foreground results were: cetacean LRT = 48.417, p = 1.53e-11; deep diving LRT = 68.928, p = 5.55e-16; aquatic LRT = 65.846, p = 2.50e-15; marine LRT = 65.659, p = 2.78e-15. Because cetacean, aquatic, marine, and deep-diving labels are biologically overlapping, these results are interpreted as concordant support for foreground-associated ACE2 molecular evolutionary heterogeneity rather than four independent demonstrations of a single adaptive mechanism (Fig. 3; Online Resource 3).

### Branch-level candidates and sensitivity analyses prioritize follow-up

aBSREL identified branch-level episodic-selection candidates within foreground analyses (Smith et al. 2015). Mesoplodon mirus was detected across aquatic, cetacean, deep-diving, and marine foreground configurations, with LRT values near 167 in parsed outputs. Leptonychotes weddellii was detected in aquatic, deep-diving, and marine foreground contexts, with corrected p-values near 0.01 and LRT values near 15. These lineages are prioritized for follow-up verification rather than treated as proof of functional adaptation (Fig. 4).

Reduced fixed-branch PAML branch-site analyses supported the same foreground categories as a sensitivity layer (Yang 1998). The reduced PAML tests were: cetacean LRT = 31.904, p = 1.62e-08; deep diving LRT = 31.126, p = 2.42e-08; aquatic LRT = 22.213, p = 2.44e-06; marine LRT = 22.213, p = 2.44e-06. Because these tests used a reduced fixed-branch framework, they are reported as supporting evidence rather than the primary proof. Candidate-site enrichment was also exploratory: the strongest trend was observed for cetaceans, with odds ratio = 4.561, raw Fisher p = 1.29e-02, and BH-FDR = 0.0773 (Benjamini and Hochberg 1995). These prioritization results do not establish ecological adaptation independently (Fig. 5; Online Resource 4).

## Discussion

This analysis supports a bounded model of ACE2 evolution: mammalian ACE2 retains broad structural conservation while showing localized ecological and lineage-associated molecular evolutionary heterogeneity. This pattern is plausible for a protein under strong physiological constraint. Conservation at the domain scale does not preclude episodic shifts at particular branches or residues, especially when selection is heterogeneous across lineages.

The strongest statistical support comes from HyPhy BUSTED, which detected significant episodic diversifying selection across related ecological foreground definitions. The reduced PAML analyses support the same direction as a sensitivity layer, while aBSREL identifies candidate lineages for follow-up. These results should be read as evidence of molecular evolutionary heterogeneity, not as proof of an ACE2-driven aquatic or diving mechanism.

The residue-level results require similar caution. Q24 and D30 are interesting because they overlap FUBAR/MEME support and receptor-interface annotations, and mammalian ACE2 receptor-interface variation has been discussed in comparative structural studies (Damas et al. 2020). However, receptor-interface location alone cannot establish viral adaptation or host-susceptibility evolution. Functional assays, structural modeling, and independent comparative datasets would be required for such claims.

The principal limitations are the single-gene scope, partially overlapping ecological labels, provisional binary ecology coding, absence of functional validation, and reliance on public sequence annotations. These limitations do not invalidate the foreground-selection signal, but they constrain the biological interpretation. The appropriate conclusion is that ACE2 shows foreground-associated molecular evolutionary heterogeneity under structural constraint.

## Materials and Methods

### Sequence curation and coordinate mapping

Public mammalian ACE2 protein and coding-sequence records were curated from NCBI/RefSeq-style sources. Records were screened to remove non-mammalian entries, duplicate isoforms where a primary ortholog was available, fragments, likely pseudogenes, and records failing codon-level quality checks. Protein alignments and human-coordinate maps from the validated project workflow were used to integrate residue-level and domain-level annotations.

### Site-level selection analyses

Codon-level site analyses used FUBAR and MEME. FUBAR candidates were summarized at posterior probability >= 0.90. MEME candidates were summarized at p <= 0.05 for the main site-level screen and p <= 0.10 for exploratory overlap with FUBAR. Candidate sites were mapped to human ACE2 coordinates and provisional ACE2 domain annotations.

### Foreground and branch-level selection analyses

Ecological foregrounds were defined as cetacean, deep-diving, aquatic, and marine branch sets. Because these categories overlap biologically, they were treated as related foreground codings rather than independent ecological replicates. BUSTED was used as the primary gene-wide foreground-selection test. aBSREL was used to identify branch-level episodic-selection candidates. Reduced fixed-branch PAML branch-site tests were used as sensitivity evidence. Likelihood-ratio tests used df = 1, and multiple-testing interpretation was bounded by Benjamini-Hochberg false-discovery control where applicable.

### Candidate-site enrichment

Candidate-site enrichment screens tested whether FUBAR/MEME overlap sites were enriched for foreground-distinguishing residue states relative to noncandidate ACE2 sites. These tests were treated as exploratory prioritization because they depend on foreground coding and residue-state summaries and do not independently demonstrate adaptation.

## Data Availability

All analyses are based on public ACE2 sequence records and generated workflow outputs. The repository is prepared for private GitHub staging under `ace2-mammalian-evolution` and Zenodo archival before submission. Before journal upload, replace this sentence with the final GitHub URL and Zenodo DOI.

## Statements and Declarations

Funding: This work was self-funded.

Competing interests: The author declares no competing interests.

Ethics approval: Not applicable; this study used public sequence data only and did not involve new human or animal subjects research.

Use of AI tools: AI-assisted tools were used to help organize, format, and draft package materials from existing analysis outputs. Parker Lehner remains responsible for all scientific claims, analysis verification, citations, data provenance, and final manuscript content.

## Author Contributions

Parker Lehner: conceptualization, data curation, formal analysis, investigation, visualization, writing - original draft, and writing - review and editing.

## Acknowledgments

Acknowledgments will be finalized after scientific review. Former professor and graduate-student reviewers may be acknowledged if they provide substantial feedback and consent to being named.

# References

Benjamini Y, Hochberg Y (1995) Controlling the false discovery rate: a practical and powerful approach to multiple testing. Journal of the Royal Statistical Society: Series B 57:289-300. https://doi.org/10.1111/j.2517-6161.1995.tb02031.x

Damas J, Hughes GM, Keough KC, Painter CA, Persky NS, Corbo M, Hiller M, Koepfli KP, Pfenning AR, Zhao H et al (2020) Broad host range of SARS-CoV-2 predicted by comparative and structural analysis of ACE2 in vertebrates. Proceedings of the National Academy of Sciences of the United States of America 117:22311-22322. https://doi.org/10.1073/pnas.2010146117

Donoghue M, Hsieh F, Baronas E, Godbout K, Gosselin M, Stagliano N, Donovan M, Woolf B, Robison K, Jeyaseelan R, Breitbart RE, Acton S (2000) A novel angiotensin-converting enzyme-related carboxypeptidase (ACE2) converts angiotensin I to angiotensin 1-9. Circulation Research 87:E1-E9. https://doi.org/10.1161/01.RES.87.5.e1

Kosakovsky Pond SL, Frost SDW (2005) Not so different after all: a comparison of methods for detecting amino acid sites under selection. Molecular Biology and Evolution 22:1208-1222. https://doi.org/10.1093/molbev/msi105

Mirceta S, Signore AV, Burns JM, Cossins AR, Campbell KL, Berenbrink M (2013) Evolution of mammalian diving capacity traced by myoglobin net surface charge. Science 340:1234192. https://doi.org/10.1126/science.1234192

Murrell B, Moola S, Mabona A, Weighill T, Sheward D, Kosakovsky Pond SL, Scheffler K (2013) FUBAR: a fast, unconstrained Bayesian approximation for inferring selection. Molecular Biology and Evolution 30:1196-1205. https://doi.org/10.1093/molbev/mst030

Murrell B, Weaver S, Smith MD, Wertheim JO, Murrell S, Aylward A, Eren K, Pollner T, Martin DP, Smith DM, Scheffler K, Kosakovsky Pond SL (2015) Gene-wide identification of episodic selection. Molecular Biology and Evolution 32:1365-1371. https://doi.org/10.1093/molbev/msv035

Murrell B, Wertheim JO, Moola S, Weighill T, Scheffler K, Kosakovsky Pond SL (2012) Detecting individual sites subject to episodic diversifying selection. PLoS Genetics 8:e1002764. https://doi.org/10.1371/journal.pgen.1002764

Smith MD, Wertheim JO, Weaver S, Murrell B, Scheffler K, Kosakovsky Pond SL (2015) Less is more: an adaptive branch-site random effects model for efficient detection of episodic diversifying selection. Molecular Biology and Evolution 32:1342-1353. https://doi.org/10.1093/molbev/msv022

Tipnis SR, Hooper NM, Hyde R, Karran E, Christie G, Turner AJ (2000) A human homolog of angiotensin-converting enzyme. Cloning and functional expression as a captopril-insensitive carboxypeptidase. Journal of Biological Chemistry 275:33238-33243. https://doi.org/10.1074/jbc.M002615200

Towler P, Staker B, Prasad SG, Menon S, Tang J, Parsons T, Ryan D, Fisher M, Williams D, Dales NA, Patane MA, Pantoliano MW (2004) ACE2 X-ray structures reveal a large hinge-bending motion important for inhibitor binding and catalysis. Journal of Biological Chemistry 279:17996-18007. https://doi.org/10.1074/jbc.M311191200

Yang Z (1998) Likelihood ratio tests for detecting positive selection and application to primate lysozyme evolution. Molecular Biology and Evolution 15:568-573. https://doi.org/10.1093/oxfordjournals.molbev.a025957


## Figure Captions

Fig. 1 Dataset curation and analysis workflow. Public mammalian ACE2 records were filtered into protein and codon-level datasets, then analyzed through coordinate mapping, site-level selection screens, foreground tests, branch-level tests, and sensitivity analyses

Fig. 2 ACE2 residue-level candidate landscape. FUBAR/MEME overlap sites are mapped to human ACE2 coordinates and broad protein regions. Q24 and D30 are highlighted as receptor-interface candidates but are not interpreted as evidence of viral adaptation

Fig. 3 Ecological foreground selection tests. HyPhy BUSTED provides the primary foreground-selection evidence, while reduced fixed-branch PAML is shown as sensitivity evidence. Foreground categories overlap biologically and are not independent mechanisms

Fig. 4 Branch-level candidates and enrichment trends. aBSREL candidate branches and candidate-site enrichment trends prioritize follow-up lineages and residues. These patterns do not establish a physiological mechanism

Fig. 5 Evidence integration and claim boundaries. The matrix separates primary BUSTED evidence, branch-level candidates, PAML sensitivity evidence, exploratory enrichment, and the bounded claim permitted by the current data
