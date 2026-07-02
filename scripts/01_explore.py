"""Initial exploration of data/latam_finanzas_2025.csv."""

import pandas as pd

CSV_PATH = "data/latam_finanzas_2025.csv"

CATEGORICAL_COLUMNS = [
    "pais",
    "industria",
    "ocupacion",
    "meta_financiera",
    "tiene_tarjeta_credito",
    "tiene_cuenta_ahorro",
    "tiene_deuda",
]


def main():
    df = pd.read_csv(CSV_PATH)

    print("=" * 80)
    print("1. SHAPE")
    print("=" * 80)
    print(f"Rows: {df.shape[0]}")
    print(f"Columns: {df.shape[1]}")

    print()
    print("=" * 80)
    print("2. COLUMNS AND DATA TYPES")
    print("=" * 80)
    for col, dtype in df.dtypes.items():
        print(f"{col:<30} {dtype}")

    print()
    print("=" * 80)
    print("3. MISSING VALUES (most to least)")
    print("=" * 80)
    missing = df.isnull().sum().sort_values(ascending=False)
    missing = missing[missing > 0]
    if missing.empty:
        print("No missing values in any column.")
    else:
        for col, count in missing.items():
            pct = count / len(df) * 100
            print(f"{col:<30} {count:>5}  ({pct:.1f}%)")

    print()
    print("=" * 80)
    print("4. NUMERIC COLUMN STATISTICS")
    print("=" * 80)
    numeric_df = df.select_dtypes(include="number")
    stats = pd.DataFrame(
        {
            "min": numeric_df.min(),
            "max": numeric_df.max(),
            "mean": numeric_df.mean(),
            "median": numeric_df.median(),
            "std": numeric_df.std(),
        }
    )
    pd.set_option("display.width", 120)
    pd.set_option("display.float_format", lambda x: f"{x:,.2f}")
    print(stats)

    print()
    print("=" * 80)
    print("5. CATEGORICAL COLUMN VALUE COUNTS")
    print("=" * 80)
    for col in CATEGORICAL_COLUMNS:
        if col not in df.columns:
            print(f"\n[!] Column '{col}' not found in dataset, skipping.")
            continue
        print(f"\n--- {col} ({df[col].nunique(dropna=True)} unique values) ---")
        counts = df[col].value_counts(dropna=False)
        for val, count in counts.items():
            label = "<MISSING>" if pd.isna(val) else val
            print(f"  {label:<35} {count}")


if __name__ == "__main__":
    main()
