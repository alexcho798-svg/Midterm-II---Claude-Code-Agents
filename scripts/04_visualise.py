"""Generate the 5 required charts from data/latam_finanzas_clean.csv."""

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

CSV_PATH = "data/latam_finanzas_clean.csv"
CHARTS_DIR = "charts"
SOURCE_NOTE = "Source: Encuesta de Bienestar Financiero LatAm 2025, Futuro Digital LatAm"

# Professional, muted qualitative palette (not matplotlib defaults).
PALETTE = ["#2C3E50", "#18BC9C", "#E67E22", "#C0392B", "#8E44AD", "#2980B9"]

GASTO_COLUMNS = {
    "gasto_vivienda_usd": "Housing",
    "gasto_alimentacion_usd": "Food",
    "gasto_transporte_usd": "Transport",
    "gasto_entretenimiento_usd": "Entertainment",
    "gasto_educacion_usd": "Education",
    "gasto_salud_usd": "Healthcare",
}

AI_BINS = [0, 4, 11, float("inf")]
AI_LABELS = ["Low (0-3)", "Medium (4-10)", "High (11+)"]


def add_source_note(fig):
    fig.text(0.5, 0.01, SOURCE_NOTE, ha="center", fontsize=8, color="gray", style="italic")


def save(fig, filename):
    fig.tight_layout(rect=[0, 0.04, 1, 1])
    path = f"{CHARTS_DIR}/{filename}"
    fig.savefig(path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"Saved {path}")


def country_color_map(countries):
    return {country: PALETTE[i % len(PALETTE)] for i, country in enumerate(sorted(countries))}


def chart_income_by_country(df, colors):
    median_income = df.groupby("pais")["ingreso_mensual_usd"].median().sort_values()
    order = median_income.index.tolist()

    fig, ax = plt.subplots(figsize=(9, 6))
    bar_colors = [colors[c] for c in order]
    ax.barh(order, median_income.values, color=bar_colors)

    for i, v in enumerate(median_income.values):
        ax.text(v + 20, i, f"${v:,.0f}", va="center", fontsize=11, fontweight="bold")

    ax.set_title("Median Monthly Income by Country", fontsize=16, fontweight="bold")
    ax.set_xlabel("Median Monthly Income (USD)")
    ax.set_ylabel("")
    ax.grid(axis="x", linestyle="--", alpha=0.4)
    ax.set_xlim(0, median_income.values.max() * 1.15)

    add_source_note(fig)
    save(fig, "01_income_by_country.png")


def chart_age_vs_savings(df, colors):
    fig, ax = plt.subplots(figsize=(9, 6))

    for country, group in df.groupby("pais"):
        ax.scatter(
            group["edad"], group["ahorro_mensual_usd"],
            label=country, color=colors[country], alpha=0.7, s=35, edgecolor="white", linewidth=0.3,
        )

    slope, intercept = np.polyfit(df["edad"], df["ahorro_mensual_usd"], 1)
    x_line = np.array([df["edad"].min(), df["edad"].max()])
    ax.plot(x_line, slope * x_line + intercept, color="black", linestyle="--", linewidth=2, label="Trend line")

    ax.set_title("Age vs. Monthly Savings", fontsize=14, fontweight="bold")
    ax.set_xlabel("Age")
    ax.set_ylabel("Monthly Savings (USD)")
    ax.grid(alpha=0.3)
    ax.legend(title="Country", loc="upper left", fontsize=8)

    add_source_note(fig)
    save(fig, "02_age_vs_savings.png")


def chart_spending_breakdown(df):
    pct = {
        label: (df[col] / df["ingreso_mensual_usd"] * 100).mean()
        for col, label in GASTO_COLUMNS.items()
    }
    series = pd.Series(pct).sort_values(ascending=True)  # ascending so highest ends up on top

    fig, ax = plt.subplots(figsize=(9, 6))
    ax.barh(series.index, series.values, color=PALETTE[1])

    for i, v in enumerate(series.values):
        ax.text(v + 0.3, i, f"{v:.1f}%", va="center", fontsize=9)

    ax.set_title("Average Spending as % of Income by Category", fontsize=14, fontweight="bold")
    ax.set_xlabel("% of Monthly Income")
    ax.set_ylabel("Expense Category")
    ax.grid(axis="x", linestyle="--", alpha=0.4)

    add_source_note(fig)
    save(fig, "03_spending_breakdown.png")


def chart_satisfaction_by_ai_usage(df):
    df = df.copy()
    df["ai_usage_group"] = pd.cut(
        df["horas_herramientas_ia_semana"], bins=AI_BINS, labels=AI_LABELS, right=False
    )
    avg_satisfaction = df.groupby("ai_usage_group", observed=True)["satisfaccion_financiera"].mean()

    bar_colors = ["#a8dadc", "#457b9d", "#1d3557"]  # light -> dark sequential (ordinal groups)

    fig, ax = plt.subplots(figsize=(8, 6))
    bars = ax.bar(avg_satisfaction.index.astype(str), avg_satisfaction.values, color=bar_colors)

    for bar, value in zip(bars, avg_satisfaction.values):
        ax.text(bar.get_x() + bar.get_width() / 2, value + 0.05, f"{value:.2f}",
                ha="center", fontsize=10, fontweight="bold")

    ax.set_title("Financial Satisfaction by AI Tool Usage", fontsize=14, fontweight="bold")
    ax.set_xlabel("AI Tool Usage Group (hours/week)")
    ax.set_ylabel("Average Financial Satisfaction (1-5)")
    ax.set_ylim(0, 5)
    ax.grid(axis="y", linestyle="--", alpha=0.4)

    add_source_note(fig)
    save(fig, "04_satisfaction_by_ai_usage.png")


def chart_housing_burden_by_country(df):
    df = df.copy()
    df["housing_pct"] = df["gasto_vivienda_usd"] / df["ingreso_mensual_usd"] * 100
    series = df.groupby("pais")["housing_pct"].mean().sort_values(ascending=True)  # highest on top

    norm = plt.Normalize(series.values.min(), series.values.max())
    cmap = plt.get_cmap("RdYlGn_r")  # high value -> red, low value -> green
    bar_colors = [cmap(norm(v)) for v in series.values]

    fig, ax = plt.subplots(figsize=(9, 6))
    ax.barh(series.index, series.values, color=bar_colors)

    for i, v in enumerate(series.values):
        ax.text(v + 0.3, i, f"{v:.1f}%", va="center", fontsize=9)

    ax.set_title("Average Housing Cost as % of Income by Country", fontsize=14, fontweight="bold")
    ax.set_xlabel("Housing Cost (% of Monthly Income)")
    ax.set_ylabel("Country")
    ax.grid(axis="x", linestyle="--", alpha=0.4)

    add_source_note(fig)
    save(fig, "05_housing_burden_by_country.png")


def main():
    df = pd.read_csv(CSV_PATH)
    colors = country_color_map(df["pais"].unique())

    chart_income_by_country(df, colors)
    chart_age_vs_savings(df, colors)
    chart_spending_breakdown(df)
    chart_satisfaction_by_ai_usage(df)
    chart_housing_burden_by_country(df)


if __name__ == "__main__":
    main()
