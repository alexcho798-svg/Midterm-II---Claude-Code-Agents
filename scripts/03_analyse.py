"""Deeper analyses on data/latam_finanzas_clean.csv.

Analyses 1 and 6 confirm/reformat numbers already computed per-country in
country-profiles.md; they are recomputed here directly from the CSV as a
cross-check, grouped in one pass instead of six separate per-country scripts.
"""

import pandas as pd

CSV_PATH = "data/latam_finanzas_clean.csv"

GASTO_COLUMNS = {
    "gasto_vivienda_usd": "housing",
    "gasto_alimentacion_usd": "food",
    "gasto_transporte_usd": "transport",
    "gasto_entretenimiento_usd": "entertainment",
    "gasto_educacion_usd": "education",
    "gasto_salud_usd": "healthcare",
}

AGE_BINS = [18, 23, 26, 29, 33]
AGE_LABELS = ["18-22", "23-25", "26-28", "29-32"]

AI_BINS = [0, 4, 11, float("inf")]
AI_LABELS = ["Low (0-3)", "Medium (4-10)", "High (11+)"]


def print_table(df, title):
    print()
    print("=" * 80)
    print(title)
    print("=" * 80)
    print(df.to_markdown(index=False))


def income_by_country(df):
    stats = (
        df.groupby("pais")["ingreso_mensual_usd"]
        .agg(median_income="median", mean_income="mean", min_income="min",
             max_income="max", std_income="std")
        .round(2)
        .sort_values("median_income", ascending=False)
        .reset_index()
        .rename(columns={"pais": "country"})
    )
    print_table(stats, "1. INCOME BY COUNTRY (sorted by median, high to low)")
    return stats


def age_vs_savings(df):
    df = df.copy()
    df["age_group"] = pd.cut(df["edad"], bins=AGE_BINS, labels=AGE_LABELS, right=False)
    df["savings_rate_pct"] = df["ahorro_mensual_usd"] / df["ingreso_mensual_usd"] * 100

    result = (
        df.groupby("age_group", observed=True)
        .agg(
            avg_monthly_savings=("ahorro_mensual_usd", "mean"),
            avg_savings_rate_pct=("savings_rate_pct", "mean"),
            n=("ahorro_mensual_usd", "size"),
        )
        .round(2)
        .reset_index()
    )
    print_table(result, "2. AGE VS. SAVINGS")
    return result


def income_by_industry(df):
    by_industry = (
        df.groupby("industria")["ingreso_mensual_usd"]
        .mean()
        .round(2)
        .sort_values(ascending=False)
        .reset_index()
        .rename(columns={"industria": "industry", "ingreso_mensual_usd": "avg_income"})
    )
    print_table(by_industry, "2b. AVERAGE INCOME BY INDUSTRY (overall, high to low)")

    pivot = df.pivot_table(
        index="pais", columns="industria", values="ingreso_mensual_usd", aggfunc="mean"
    )
    top_industry = pivot.idxmax(axis=1)
    top_income = pivot.max(axis=1).round(2)
    top_by_country = (
        pd.DataFrame({"country": top_industry.index, "top_industry": top_industry.values,
                       "avg_income_usd": top_income.values})
        .sort_values("avg_income_usd", ascending=False)
        .reset_index(drop=True)
    )
    print_table(top_by_country, "2c. HIGHEST-PAYING INDUSTRY PER COUNTRY")
    return by_industry, top_by_country


def spending_breakdown(df):
    pct_of_income = pd.DataFrame(
        {
            label: [(df[col] / df["ingreso_mensual_usd"] * 100).mean()]
            for col, label in GASTO_COLUMNS.items()
        }
    ).T.reset_index()
    pct_of_income.columns = ["category", "avg_pct_of_income"]
    pct_of_income["avg_pct_of_income"] = pct_of_income["avg_pct_of_income"].round(2)
    pct_of_income = pct_of_income.sort_values("avg_pct_of_income", ascending=False).reset_index(drop=True)
    print_table(pct_of_income, "3. SPENDING BREAKDOWN (avg % of income, full sample)")
    return pct_of_income


def credit_card_comparison(df):
    groups = df.groupby("tiene_tarjeta_credito").agg(
        avg_income=("ingreso_mensual_usd", "mean"),
        avg_food_spending=("gasto_alimentacion_usd", "mean"),
        avg_entertainment_spending=("gasto_entretenimiento_usd", "mean"),
        avg_savings=("ahorro_mensual_usd", "mean"),
    ).round(2)

    holders = groups.loc["Si"]
    non_holders = groups.loc["No"]
    pct_diff = ((holders - non_holders) / non_holders * 100).round(1)

    result = groups.reset_index().rename(columns={"tiene_tarjeta_credito": "group"})
    result["group"] = result["group"].map({"Si": "Has credit card", "No": "No credit card"})

    diff_row = pd.DataFrame([{
        "group": "% difference (holder vs non-holder)",
        "avg_income": pct_diff["avg_income"],
        "avg_food_spending": pct_diff["avg_food_spending"],
        "avg_entertainment_spending": pct_diff["avg_entertainment_spending"],
        "avg_savings": pct_diff["avg_savings"],
    }])
    result = pd.concat([result, diff_row], ignore_index=True)

    print_table(result, "4. CREDIT CARD HOLDERS VS NON-HOLDERS")
    return result


def ai_usage_vs_satisfaction(df):
    df = df.copy()
    df["ai_usage_group"] = pd.cut(
        df["horas_herramientas_ia_semana"], bins=AI_BINS, labels=AI_LABELS, right=False
    )

    result = (
        df.groupby("ai_usage_group", observed=True)
        .agg(
            n=("satisfaccion_financiera", "size"),
            avg_satisfaction=("satisfaccion_financiera", "mean"),
            avg_income=("ingreso_mensual_usd", "mean"),
        )
        .round(2)
        .reset_index()
    )
    print_table(result, "5. AI TOOL USAGE VS FINANCIAL SATISFACTION")

    corr = df["horas_herramientas_ia_semana"].corr(df["satisfaccion_financiera"])
    print(f"\nPearson correlation (horas_herramientas_ia_semana vs satisfaccion_financiera): {corr:.3f}")
    return result, corr


def housing_burden_by_country(df):
    df = df.copy()
    df["housing_pct"] = df["gasto_vivienda_usd"] / df["ingreso_mensual_usd"] * 100
    result = (
        df.groupby("pais")["housing_pct"]
        .mean()
        .round(2)
        .sort_values(ascending=False)
        .reset_index()
        .rename(columns={"pais": "country", "housing_pct": "avg_housing_pct_of_income"})
    )
    print_table(result, "6. HOUSING BURDEN BY COUNTRY (sorted high to low)")
    return result


def main():
    df = pd.read_csv(CSV_PATH)

    income_by_country(df)
    age_vs_savings(df)
    income_by_industry(df)
    spending_breakdown(df)
    credit_card_comparison(df)
    ai_usage_vs_satisfaction(df)
    housing_burden_by_country(df)


if __name__ == "__main__":
    main()
