"""Generate a financial profile for Chile from data/latam_finanzas_clean.csv."""

import pandas as pd

CSV_PATH = "data/latam_finanzas_clean.csv"
COUNTRY = "Chile"

GASTO_COLUMNS = [
    "gasto_vivienda_usd",
    "gasto_alimentacion_usd",
    "gasto_transporte_usd",
    "gasto_entretenimiento_usd",
    "gasto_educacion_usd",
    "gasto_salud_usd",
]


def main():
    df = pd.read_csv(CSV_PATH)
    sub = df[df["pais"] == COUNTRY]

    n = len(sub)
    age_min, age_max = sub["edad"].min(), sub["edad"].max()

    income = sub["ingreso_mensual_usd"]
    housing_pct = (sub["gasto_vivienda_usd"] / sub["ingreso_mensual_usd"] * 100).mean()

    spend_pct = {
        col: (sub[col] / sub["ingreso_mensual_usd"] * 100).mean() for col in GASTO_COLUMNS
    }

    avg_savings = sub["ahorro_mensual_usd"].mean()
    pct_negative_savings = sub["ahorro_negativo"].mean() * 100

    avg_ai_hours = sub["horas_herramientas_ia_semana"].mean()
    avg_satisfaction = sub["satisfaccion_financiera"].mean()

    lines = []
    lines.append(f"## País: {COUNTRY}\n")

    lines.append("### 1. Tamaño de muestra y edad")
    lines.append(f"- Encuestados: {n}")
    lines.append(f"- Rango de edad: {age_min} - {age_max} años\n")

    lines.append("### 2. Ingreso (USD)")
    lines.append(f"- Mediana: {income.median():,.2f}")
    lines.append(f"- Media: {income.mean():,.2f}")
    lines.append(f"- Min: {income.min():,.2f}")
    lines.append(f"- Max: {income.max():,.2f}")
    lines.append(f"- Desviación estándar: {income.std():,.2f}\n")

    lines.append("### 3. Carga de vivienda")
    lines.append(f"- gasto_vivienda_usd promedio como % del ingreso: {housing_pct:.1f}%\n")

    lines.append("### 4. Desglose de gasto (% promedio del ingreso)")
    for col, pct in spend_pct.items():
        label = col.replace("gasto_", "").replace("_usd", "")
        lines.append(f"- {label}: {pct:.1f}%")
    lines.append("")

    lines.append("### 5. Ahorro")
    lines.append(f"- ahorro_mensual_usd promedio: {avg_savings:,.2f}")
    lines.append(f"- % con ahorro negativo: {pct_negative_savings:.1f}%\n")

    lines.append("### 6. Uso de IA y satisfacción")
    lines.append(f"- Horas promedio de herramientas de IA por semana: {avg_ai_hours:.1f}")
    lines.append(f"- Satisfacción financiera promedio (1-5): {avg_satisfaction:.2f}")

    output = "\n".join(lines)
    print(output)


if __name__ == "__main__":
    main()
