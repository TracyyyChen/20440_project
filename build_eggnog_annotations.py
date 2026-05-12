"""
Rebuilds data/eggnog_annotations.tsv from the per-donor/isotype eggNOG output
files in eggnog/.  Run once before opening 20440_project.ipynb:

    python build_eggnog_annotations.py
"""
import os
import pandas as pd

EGGNOG_DIR = "eggnog"
OUT_PATH = "data/eggnog_annotations.tsv"
AFFILIATION = "MIT"

# filename prefix → (donor, isotype)
SAMPLES = {
    "290B_IgA": ("290B", "IgA"),
    "290B_IgG": ("290B", "IgG"),
    "298C_IgA": ("298C", "IgA"),
    "298C_IgG": ("298C", "IgG"),
    "302C_IgA": ("302C", "IgA"),
    "302C_IgG": ("302C", "IgG"),
}

chunks = []
for prefix, (donor, isotype) in SAMPLES.items():
    fname = f"{prefix}_Aggregated_with_Regions.tsv"
    fpath = os.path.join(EGGNOG_DIR, fname)
    if not os.path.exists(fpath):
        print(f"WARNING: {fpath} not found — skipping")
        continue

    df = pd.read_csv(fpath, sep="\t", comment="#", dtype=str)
    raw_text = df.apply(lambda row: " ".join(row.fillna("-").values), axis=1)
    chunks.append(pd.DataFrame({
        "donor": donor,
        "isotype": isotype,
        "affiliation": AFFILIATION,
        "raw_text": raw_text,
    }))
    print(f"  {fname}: {len(df):,} rows")

out = pd.concat(chunks, ignore_index=True)
out.to_csv(OUT_PATH, sep="\t", index=False)
print(f"\nWrote {len(out):,} rows to {OUT_PATH}")
