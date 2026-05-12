# 20.440 Final Project: Host–Microbiome Interactions in the Human Colon

**Tracy Chen & Eden Fleshler** | MIT 20.440 Analysis of Biological Networks

---

## Project Objective

We investigate how gut microbial composition and functional gene content relate to mucosal immune cell states in the healthy human colon. Specifically, we ask whether regional variation along the colon axis (Caecum → Transverse → Sigmoid) is reflected in both the B cell compartment (scRNA-seq) and the bacterial community (16S rRNA / shotgun metagenomics), and whether these two layers share common sources of variance (MOFA+ integration).

---

## Data

Large files are excluded from this repo due to size. Download them into `data/` before running the notebook.

| File | Size | Source |
|------|------|--------|
| `data/Colon_cell_atlas.h5ad` | ~2 GB | [Gut Cell Atlas](https://www.gutcellatlas.org/) — direct: https://cellgeni.cog.sanger.ac.uk/gutcellatlas/Colon_cell_atlas.h5ad |
| `data/Colon_immune_counts.mtx` | ~500 MB | Same Gut Cell Atlas download page |

Included data files:

| File | Description |
|------|-------------|
| `data/16s_microbiome_composition.csv` | 16S taxonomic composition per sample |
| `data/Colon_immune_metadata.csv` | Cell-level metadata (donor, region, cell type, clonotype) |
| `data/Colon_immune_gene_names.csv` | Gene name list for sparse counts matrix |
| `data/supplemental_data_edited.xlsx` | Supplemental tables from James et al. 2020 (16S abundances, plasma antibody titers) |
| `data/eggnog_annotations.tsv` | Merged eggNOG functional annotations across donors and isotypes — **not in repo**, generate with `python build_eggnog_annotations.py` (requires `eggnog/` source files) |
| `data/metagenomics_taxa.csv` | Merged MetaPhlAn taxonomic profiles |
| `humann/` | HUMAnN 3/4 per-sample outputs (gene families, pathway abundances, MetaPhlAn profiles) |

---

## Environment Setup

```bash
# scRNA-seq / scanpy (for 20440_project.ipynb)
conda activate scanpy   # Python 3.11, anndata/scanpy stack

# HUMAnN metagenomics (for humann/ pipeline outputs)
conda activate humann

# Launch Jupyter from the project root
jupyter notebook
```

Key packages: `scanpy`, `anndata`, `pandas`, `numpy`, `scipy`, `seaborn`, `matplotlib`, `mofapy2`

---

## Analysis Script

### `20440_project.ipynb`

Single notebook containing all analyses (Tracy Chen & Eden Fleshler). Covers scRNA-seq immune profiling of 41,650 colon cells (UMAPs, B/T cell subtype proportions, IgA/IgG plasma cell marker genes, Th1/Th17 pathway scores), 16S microbiome diversity and phylum composition per colon region, IgA vs IgG functional annotation comparison from eggNOG-mapped metagenomes, and MOFA+ multi-omics factor analysis integrating five views (B cell proportions, T cell proportions, B/T cell pathway scores, bacterial 16S CLR).

---

## Metagenomics Pipeline (HPC — run prior to the notebook)

These SLURM batch scripts were used to process raw shotgun metagenomics reads on a Linux cluster. They produced the assemblies and eggNOG annotations that underlie `eggnog_annotations.tsv`.

### Step 1: Assembly with MEGAHIT

```bash
#!/bin/bash
#SBATCH --job-name=megahit_batch
#SBATCH --array=0-25
#SBATCH --cpus-per-task=16
#SBATCH --mem=64G
#SBATCH --time=12:00:00
#SBATCH --output=logs/megahit_%A_%a.out

conda activate megahit_env

BASE_DIR="/home/fleshler/20.440"
DATA_DIR="${BASE_DIR}/metagenomics"

IDS=($(ls ${DATA_DIR}/ERR*_1.fastq.gz | xargs -n 1 basename | sed 's/_1.fastq.gz//' | sort | uniq))
CURRENT_ID=${IDS[$SLURM_ARRAY_TASK_ID]}

OUTDIR="${BASE_DIR}/assemblies/${CURRENT_ID}_assembly"
R1="${DATA_DIR}/${CURRENT_ID}_1.fastq.gz"
R2="${DATA_DIR}/${CURRENT_ID}_2.fastq.gz"

echo "Processing: $CURRENT_ID"

megahit -1 $R1 -2 $R2 \
    -o $OUTDIR \
    --presets meta-sensitive \
    -t $SLURM_CPUS_PER_TASK

echo "Finished assembly for $CURRENT_ID"
```

### Step 2: Functional annotation with eggNOG-mapper

```bash
#!/bin/bash
#SBATCH --job-name=eggnog_array
#SBATCH --cpus-per-task=16
#SBATCH --mem=64G
#SBATCH --time=12:00:00
#SBATCH --array=0-15

conda activate eggnog_env

BASE_DIR="/home/fleshler/20.440"
DB_DIR="${BASE_DIR}/eggnog_db"
OUT_DIR="${BASE_DIR}/functional_analysis/results"
mkdir -p $OUT_DIR

IDS=($(ls ${BASE_DIR}/metagenomics/ERR*_1.fastq.gz | xargs -n 1 basename | sed 's/_1.fastq.gz//' | sort | uniq))
CURRENT_ID=${IDS[$SLURM_ARRAY_TASK_ID]}

INPUT_FASTA="${BASE_DIR}/assemblies/${CURRENT_ID}_assembly/final.contigs.fa"

if [ ! -f "$INPUT_FASTA" ]; then
    echo "Error: Assembly not found for ${CURRENT_ID}"
    exit 1
fi

emapper.py \
    --resume \
    -i "$INPUT_FASTA" \
    -o "${CURRENT_ID}_annotated" \
    --output_dir "$OUT_DIR" \
    --data_dir "$DB_DIR" \
    -m diamond \
    --cpu "$SLURM_CPUS_PER_TASK" \
    --override

echo "Finished annotation for ${CURRENT_ID}"
```

---

## Generated Figures

| File | Description |
|------|-------------|
| `iga_plasma_dotplot_fig5a.pdf` | Dot plot of IgA plasma cell marker genes by region |

---

## References

1. James, K.R., Gomes, T., Elmentaite, R. et al. Distinct microbial and immune niches of the human colon. *Nat Immunol* **21**, 343–353 (2020). https://doi.org/10.1038/s41590-020-0602-z

2. Argelaguet, R. et al. MOFA+: a statistical framework for comprehensive integration of multi-modal single-cell data. *Genome Biol* **21**, 111 (2020). https://doi.org/10.1186/s13059-020-02015-1

3. Li, D. et al. MEGAHIT: An ultra-fast single-node solution for large and complex metagenomics assembly via succinct de Bruijn graph. *Bioinformatics* **31**, 1674–1676 (2015). https://doi.org/10.1093/bioinformatics/btv033

4. Cantalapiedra, C.P. et al. eggNOG-mapper v2: functional annotation, orthology assignments, and domain prediction at the metagenomic scale. *Mol Biol Evol* **38**, 5825–5829 (2021). https://doi.org/10.1093/molbev/msab293

5. Franzosa, E.A. et al. Species-level functional profiling of metagenomes and metatranscriptomes. *Nat Methods* **15**, 962–968 (2018). https://doi.org/10.1038/s41592-018-0176-y (HUMAnN)
