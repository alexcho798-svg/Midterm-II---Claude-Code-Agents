"""Clean and standardize data/latam_finanzas_2025_clean.csv.

Steps:
1. Standardize 'industria' (spelling variants, capitalization, abbreviations).
2. Handle missing values in numeric columns (median fill where appropriate).
3. Flag negative 'ahorro_mensual_usd' values in a new 'ahorro_negativo' column
   (kept, not removed - negative savings is a valid survey outcome).
4. Repair mojibake (e.g. "MÃ³xico") and strip accents to plain ASCII
   (e.g. "México" -> "Mexico") across all text columns.
5. Save the result to data/latam_finanzas_clean.csv.
"""

import unicodedata

import pandas as pd

INPUT_PATH = "data/latam_finanzas_2025_clean.csv"
OUTPUT_PATH = "data/latam_finanzas_clean.csv"

# Known abbreviations/synonyms that don't collapse via simple
# lowercase + accent-stripping (e.g. "tech" vs "tecnologia").
INDUSTRIA_SYNONYMS = {
    "tech": "tecnologia",
}

TEXT_COLUMNS = [
    "nombre",
    "pais",
    "ocupacion",
    "industria",
    "tiene_tarjeta_credito",
    "tiene_cuenta_ahorro",
    "tiene_deuda",
    "meta_financiera",
]


def strip_accents(text: str) -> str:
    nfkd = unicodedata.normalize("NFKD", text)
    return "".join(c for c in nfkd if not unicodedata.combining(c))


def repair_mojibake(text: str) -> str:
    """Fix UTF-8 bytes that were mis-decoded as Latin-1/cp1252 (e.g. 'Ã³' -> 'ó')."""
    if "Ã" in text or "Â" in text:
        try:
            return text.encode("latin1").decode("utf-8")
        except (UnicodeDecodeError, UnicodeEncodeError):
            return text
    return text


def clean_text_value(value):
    if not isinstance(value, str):
        return value
    fixed = repair_mojibake(value)
    return strip_accents(fixed)


def normalize_key(value: str) -> str:
    key = strip_accents(value).lower().strip()
    return INDUSTRIA_SYNONYMS.get(key, key)


def standardize_industria(df: pd.DataFrame) -> pd.DataFrame:
    before_unique = sorted(df["industria"].unique().tolist())
    counts = df["industria"].value_counts()

    # Group values by normalized key, canonical label = most frequent
    # original spelling within that group.
    key_to_values = {}
    for val in before_unique:
        key_to_values.setdefault(normalize_key(val), []).append(val)

    canonical_map = {}
    for key, variants in key_to_values.items():
        canonical = max(variants, key=lambda v: counts[v])
        for v in variants:
            canonical_map[v] = canonical

    df["industria"] = df["industria"].map(canonical_map)
    after_unique = sorted(df["industria"].unique().tolist())

    print("=" * 80)
    print("1. STANDARDIZING 'industria'")
    print("=" * 80)
    print(f"Unique values BEFORE ({len(before_unique)}): {before_unique}")
    print(f"Unique values AFTER  ({len(after_unique)}): {after_unique}")
    changed = {k: v for k, v in canonical_map.items() if k != v}
    if changed:
        print("Mappings applied:")
        for old, new in changed.items():
            print(f"  '{old}' -> '{new}'")
    else:
        print("No inconsistencies found - column was already standardized.")

    return df


def handle_missing_numeric(df: pd.DataFrame) -> tuple[pd.DataFrame, dict]:
    print()
    print("=" * 80)
    print("2. MISSING VALUES IN NUMERIC COLUMNS")
    print("=" * 80)

    numeric_cols = df.select_dtypes(include="number").columns
    fill_log = {}
    for col in numeric_cols:
        n_missing = df[col].isnull().sum()
        pct = n_missing / len(df) * 100
        if n_missing == 0:
            continue
        if pct < 10:
            strategy = "fill with median"
            median_val = df[col].median()
            df[col] = df[col].fillna(median_val)
            fill_log[col] = (n_missing, pct, strategy, median_val)
        elif pct < 40:
            strategy = "fill with median (borderline, kept to avoid losing rows)"
            median_val = df[col].median()
            df[col] = df[col].fillna(median_val)
            fill_log[col] = (n_missing, pct, strategy, median_val)
        else:
            strategy = "leave as NaN (too much missing to impute reliably)"
            fill_log[col] = (n_missing, pct, strategy, None)

        print(f"{col}: {n_missing} missing ({pct:.1f}%) -> {strategy}"
              + (f" (median={median_val:.2f})" if fill_log[col][3] is not None else ""))

    if not fill_log:
        print("No missing values found in numeric columns.")

    return df, fill_log


def flag_negative_savings(df: pd.DataFrame) -> int:
    print()
    print("=" * 80)
    print("3. FLAGGING NEGATIVE 'ahorro_mensual_usd'")
    print("=" * 80)
    df["ahorro_negativo"] = df["ahorro_mensual_usd"] < 0
    n_negative = int(df["ahorro_negativo"].sum())
    print(f"{n_negative} rows have negative savings (kept as-is, flagged in 'ahorro_negativo').")
    return n_negative


def fix_encoding(df: pd.DataFrame) -> int:
    print()
    print("=" * 80)
    print("4. FIXING MOJIBAKE / ACCENTED CHARACTERS")
    print("=" * 80)
    n_changed = 0
    for col in TEXT_COLUMNS:
        if col not in df.columns:
            continue
        cleaned = df[col].map(clean_text_value)
        n_changed += (cleaned != df[col]).sum()
        df[col] = cleaned
    print(f"{n_changed} text values repaired/normalized to plain ASCII across {len(TEXT_COLUMNS)} columns.")
    return n_changed


def main():
    df = pd.read_csv(INPUT_PATH)
    rows_before = len(df)

    df = standardize_industria(df)
    df, fill_log = handle_missing_numeric(df)
    n_negative = flag_negative_savings(df)
    n_text_changed = fix_encoding(df)

    df.to_csv(OUTPUT_PATH, index=False, encoding="utf-8")

    rows_after = len(df)

    print()
    print("=" * 80)
    print("5. SUMMARY")
    print("=" * 80)
    print(f"Rows before: {rows_before}")
    print(f"Rows after:  {rows_after}")
    print()
    print("Changes made:")
    print("  - Standardized 'industria' spelling/casing/abbreviation variants.")
    if fill_log:
        for col, (n_missing, pct, strategy, median_val) in fill_log.items():
            print(f"  - '{col}': {n_missing} missing values ({pct:.1f}%) -> {strategy}.")
    else:
        print("  - No missing numeric values found.")
    print(f"  - Added 'ahorro_negativo' boolean column ({n_negative} rows flagged True).")
    print(f"  - Repaired/normalized {n_text_changed} text values (mojibake + accents -> ASCII).")
    print(f"\nSaved clean dataset to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
