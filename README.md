# 20.440 Final Project: Host–Microbiome Interactions in the Human Colon

**Tracy Chen & Eden Fleshler** | MIT 20.440 Analysis of Biological Networks

## Overview

Single-cell RNA-seq and 16S microbiome analysis of the human colon, examining how gut microbial composition relates to mucosal immune cell states across colon regions (Caecum, Transverse, Sigmoid).

## Notebook

`20440_project.ipynb`: full analysis including UMAPs, IgA/IgG plasma cell marker gene dot plots, pathway scoring, and MOFA+ multi-omics factor analysis.

## Data

Large files (`Colon_cell_atlas.h5ad`, `Colon_immune_counts.mtx`) are excluded from this repo due to size. Download from the [Gut Cell Atlas](https://www.gutcellatlas.org/) (James et al. 2020).

| File | Description |
|------|-------------|
| `data/16s_microbiome_composition.csv` | 16S taxonomic composition per sample |
| `data/Colon_immune_metadata.csv` | Cell-level metadata (donor, region, cell type, clonotype) |
| `data/Colon_immune_gene_names.csv` | Gene name list for sparse counts matrix |
| `data/metagenomics_taxa.csv` | Merged MetaPhlAn taxonomic profiles |
| `data/supplemental_data_edited.xlsx` | Plasma IgA/IgG antibody data (Jäger et al. 2021) |

## Reference

James, K.R., Gomes, T., Elmentaite, R. et al. Distinct microbial and immune niches of the human colon. *Nat Immunol* 21, 343–353 (2020). https://doi.org/10.1038/s41590-020-0602-z
