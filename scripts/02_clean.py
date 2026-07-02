"""Clean and standardize data/latam_finanzas_2025.csv.

Reads the raw survey export, fixes known data-quality issues, and writes a
cleaned copy. The raw file is left untouched so it remains available as a
reference / audit trail.

Issues fixed:
- `industria`: "Tecnologia" (missing accent), "tech" (English abbreviation),
  and "TECNOLOGIA" (all caps) are variants of "Tecnologia" that were split
  into separate categories. They are merged into a single canonical value.
"""

import pandas as pd

RAW_PATH = "data/latam_finanzas_2025.csv"
CLEAN_PATH = "data/latam_finanzas_2025_clean.csv"

INDUSTRIA_MAP = {
    "Tecnologia": "Tecnología",
    "tech": "Tecnología",
    "TECNOLOGÍA": "Tecnología",
}


def main():
    df = pd.read_csv(RAW_PATH)

    before_counts = df["industria"].value_counts()
    n_fixed = df["industria"].isin(INDUSTRIA_MAP).sum()

    df["industria"] = df["industria"].replace(INDUSTRIA_MAP)

    after_counts = df["industria"].value_counts()

    print(f"Standardized {n_fixed} 'industria' values to 'Tecnología':")
    for old_val in INDUSTRIA_MAP:
        if old_val in before_counts.index:
            print(f"  '{old_val}' ({before_counts[old_val]} rows) -> 'Tecnología'")

    print(f"\n'industria' categories before: {df['industria'].nunique() + len(INDUSTRIA_MAP)}")
    print(f"'industria' categories after:  {after_counts.index.nunique()}")

    df.to_csv(CLEAN_PATH, index=False, encoding="utf-8")
    print(f"\nSaved cleaned dataset to {CLEAN_PATH} ({df.shape[0]} rows, {df.shape[1]} columns)")


if __name__ == "__main__":
    main()
