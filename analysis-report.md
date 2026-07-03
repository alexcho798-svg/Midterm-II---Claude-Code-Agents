# Reporte de Exploracion Inicial - latam_finanzas_2025

Dataset: encuesta financiera a 500 profesionales jovenes de Latinoamerica.

Prompt usado

I'm starting a data analysis project. The dataset is at data/latam_finanzas_2025.csv
and it contains survey responses from 500 young professionals across Latin America.

Before I touch the data, I need to understand what I'm working with. Please:

1. Read the file and print the number of rows and columns
2. List every column with its name and data type
3. Count the missing values in each column and show them sorted from most to least
4. Show the basic statistics for all numeric columns (min, max, mean, median, std)
5. For each categorical column (pais, industria, ocupacion, meta_financiera,
   tiene_tarjeta_credito, tiene_cuenta_ahorro, tiene_deuda), show the unique 
   values and how many times each appears

Save the script that does this to scripts/01_explore.py
```
After the output, ask yourself:
Do the unique values look clean? Any typos or inconsistencies?
Which columns have missing values and how many?
Do the min/max values make sense for each column?

## 1. Dimensiones

- Filas: 500
- Columnas: 21

## . Valores faltantes

Solo una columna tiene valores nulos:

| Columna         | Faltantes | % |
| gasto_salud_usd | 33        | 6.6% |

## 4. Estadisticas de columnas numericas

| Columna                      | min    | max       | mean     | median  | std      |
|------------------------------|--------|---------- |----------|---      |---       |
| edad                         | 18.00  | 32.00     | 24.96    | 25.00   | 4.22     |
| ingreso_mensual_usd          | 300.00 | 2,874.49  | 1,016.80 | 960.34  | 376.81   |
| gasto_vivienda_usd           | 55.61  | 796.33    | 290.32   | 267.87  | 125.03   |
| gasto_alimentacion_usd       | 60.00  | 741.66    | 242.61   | 227.78  | 102.79   |
| gasto_transporte_usd         | 20.00  | 300.58    | 102.19   | 94.57   | 49.31    |
| gasto_entretenimiento_usd    | 10.00  | 410.21    | 88.56    | 79.05   | 50.25    |
| gasto_educacion_usd          | 10.37  | 211.31    | 82.18    | 80.32   | 33.85    |
| gasto_salud_usd              | 0.00   | 150.23    | 49.88    | 45.66   | 28.61    |
| ahorro_mensual_usd           | -160.02| 451.38    | 99.00    | 92.44   | 95.59    |
| deuda_total_usd              | 0.00   | 10,918.73 | 1,849.69 | 0.00    | 2,565.57 |
| horas_herramientas_ia_semana | 0.00   | 16.10     | 5.41     | 5.20    | 2.70     |
| satisfaccion_financiera      | 1.00   | 5.00      | 2.48     | 2.00    | 0.62     |

## 5. Columnas categoricas

**pais** (6 valores): Mexico 150, Colombia 80, Argentina 70, Chile 70, Brasil 65, Peru 65

**industria**:
- Cruda (13 valores, con inconsistencias): Finanzas 66, Ingenieria 53, Ventas 51, Salud 49, Marketing 49, Tecnologia 47, Educacion 45, Diseno 45, Recursos Humanos 44, Retail 41, Tecnologia (sin tilde) 5, tech 3, TECNOLOGIA (mayusculas) 2
- Limpia (10 valores): Finanzas 66, Tecnologia 57, Ingenieria 53, Ventas 51, Salud 49, Marketing 49, Educacion 45, Diseno 45, Recursos Humanos 44, Retail 41

**ocupacion** (10 valores): Disenador Grafico 56, Ingeniero 55, Community Manager 52, Gerente de Proyectos 51, Contador 50, Analista Financiero 50, Representante de Ventas 49, Coordinador de Marketing 47, Especialista en RRHH 47, Docente 43

**meta_financiera** (8 valores): Pagar deudas 81, Invertir en bolsa 75, Ahorrar para retiro 68, Ahorrar para viaje 61, Comprar casa 61, Emprender un negocio 58, Estudiar posgrado 52, Fondo de emergencia 44

**tiene_tarjeta_credito**: Si 284, No 216

**tiene_cuenta_ahorro**: Si 362, No 138

**tiene_deuda**: No 266, Si 234

Phase 2

promt usado

Based on the exploration, I've identified some data quality issues.
Please help me clean the dataset.

Using the file data/latam_finanzas_2025_clean.csv:

1. Check the 'industria' column for inconsistent values (spelling variations,
   different capitalizations, abbreviations for the same industry) and 
   standardize them. Show me all unique values before and after the fix.

2. For missing values in numeric columns: show me the percentage missing
   for each column and suggest whether to fill them with the median, 
   drop the rows, or leave them — then apply your recommendation.

3. Check 'ahorro_mensual_usd' for negative values. How many are there?
   These are valid (spending more than earning) — do NOT remove them,
   but flag them in a new boolean column called 'ahorro_negativo'.

4. Save the clean dataset to data/latam_finanzas_clean.csv
5. Print a summary: rows before vs. after, changes made   
6.. Also replace all the words where is a Ã© ,Ã³ etc with a letter with a valid letter for example instead MÃ³xico it must say Mexico.

Save the script to scripts/02_clean.py

## . Hallazgos y calidad de datos


### Valores unicos / inconsistencias
- `industria` tenia "Tecnologia" repartida en 4 variantes (`Tecnologia`, `Tecnologia` sin tilde, `tech`, `TECNOLOGIA`) por errores de captura/mayusculas. - El resto de columnas categoricas (`pais`, `ocupacion`, `meta_financiera`, `tiene_tarjeta_credito`, `tiene_cuenta_ahorro`, `tiene_deuda`) estan limpias, sin typos ni variantes.
- No se encontraron espacios en blanco al inicio/final en columnas de texto, ni IDs o filas duplicadas.

### Valores faltantes
- Unica columna con nulos: `gasto_salud_usd` (33 filas, 6.6%). El resto del dataset esta completo.

### Rangos min/max
- `ahorro_mensual_usd` tiene un minimo de **-160.02**: plausible (mes en que el gasto supero el ingreso), pero se debe confirmar que no sea un error de signo antes de usarlo en calculos agregados.
- `deuda_total_usd` va de 0 a **10,918.73**, con mediana 0 y media 1,849.69: fuertemente sesgada a la derecha, consistente con que 266/500 personas no tienen deuda (`tiene_deuda` = No). Preferir mediana/percentiles sobre la media para resumir esta columna.
- `edad` (18-32) y `satisfaccion_financiera` (1-5) tienen rangos acotados y razonables, sin valores fuera de rango.

###Filas y columnas afectadas 
Al principio se estandarizaron las categorías en 57 rows, después agregue la columna ahorro negativo, para mayor agilidad al buscar los datos, y rellene gasto_Salud (la columna con valores nulos) con la mediana de los valores, en total 91 rows fueron modificadas.

use la mediana puesto que una de las filas ya estaba usando ese método y Claude apoyo esa idea, además que estandarice los datos por estética y mayor facilidad al buscar datos

Phase 2.5

Promt usado

---
name: country-profiler
description: Use PROACTIVELY whenever the user asks for a statistical profile, summary, breakdown, or analysis of one or more Latin American countries from the finance dataset (data/latam_finanzas_clean.csv). Triggers on requests like "perfil de México", "analiza Argentina", "dame las estadísticas de Chile", "compara Perú y Brasil", "resumen financiero de Colombia", or any request to profile/summarize/compare countries in the dataset. Also triggers when the user asks to run this for "todos los países" or lists multiple country names together. Returns a Markdown section per country covering sample size, income stats, housing burden, spending breakdown, savings, and AI tool usage.
---
You are a data analyst assistant. When given a country name, read
`data/latam_finanzas_clean.csv` and produce a Markdown section with:
1. Sample size and age range for this country
2. Income: median, mean, min, max, standard deviation (USD)
3. Housing burden: average gasto_vivienda_usd as % of ingreso_mensual_usd
4. Spending breakdown: average % of income for each gasto_* column
5. Savings: average ahorro_mensual_usd and % of respondents with negative savings
6. AI tools: average horas_herramientas_ia_semana and average satisfaccion_financiera

Use the country name as the Markdown section header (## País: [name]).
Save the supporting Python script as scripts/country_[name].py.

If multiple countries are requested at once, invoke this profile process for each country in parallel and combine all sections into a single Markdown file.


Which country has the highest housing burden? Does it match what you expected? Argentina 

Phase 4

Prompt usado 

I now have a clean dataset at data/latam\_finanzas\_clean.csv and six country
profiles already generated in scripts/country\_profiles.md.

Please run the following analyses and show the results as formatted tables.
For analyses 1 and 6, you may reference the country profiles already generated
rather than recomputing from scratch.

1. INCOME BY COUNTRY
   Reference the country profiles. Confirm and format the median income,
   mean income, min, max, and standard deviation for each country.
   Sort from highest to lowest median.

2. AGE VS. SAVINGS
   Create age groups: 18-22, 23-25, 26-28, 29-32.
   For each group: average monthly savings and average savings rate 
   (savings / income as a percentage).

   INCOME BY INDUSTRY
   Create a group for each industry and calculate wich industry have more income per country

3. SPENDING BREAKDOWN
   For the full sample, calculate the average percentage of income spent on:
   housing, food, transport, entertainment, education, and healthcare.
   Show as a table sorted from highest to lowest percentage.

4. CREDIT CARD HOLDERS VS NON-HOLDERS
   Compare the two groups on: average income, food spending, entertainment 
   spending, and savings. Calculate the percentage difference for each.

5. AI TOOL USAGE VS FINANCIAL SATISFACTION
   Create three groups: Low (0-3 hours/week), Medium (4-10), High (11+).
   For each group: count of respondents, average satisfaction score, 
   and average income. Also calculate the Pearson correlation between 
   horas\_herramientas\_ia\_semana and satisfaccion\_financiera.

6. HOUSING BURDEN BY COUNTRY
   Reference the country profiles. Confirm and format the average housing
   expense as % of income for each country, sorted from highest to lowest.

Save the script to scripts/03\_analyse.py
```
Quiero dar a notar que Brasil tiene el mayor ingreso y que la profesion de educador es de las mejores pagadas, me esperaba que el housing fuera lo que mas se gasta del sueldo de los profesionistas.

Cosas a destacar

1.- Argentina tiene la mayor carga de vivienda pero el menor % de ahorro negativo
2.- Titulares de tarjeta gastan notablemente más en entretenimiento y comida, no solo por tener mayor ingreso
3.- Clara tendencia creciente: mayor edad → mayor tasa de ahorro

Phase 4.

Using data/latam\_finanzas\_clean.csv, create the following 5 charts.
Save each as a PNG in the charts/ folder with the filenames shown.
Use a professional color palette (not the default matplotlib colors).
All charts must have: a clear title, labelled axes, and a source note 
"Source: Encuesta de Bienestar Financiero LatAm 2025, Futuro Digital LatAm".

1. charts/01\_income\_by\_country.png
   Box plot showing the income distribution for each country.
   Sort countries by median income (highest on top for a horizontal box plot).

2. charts/02\_age\_vs\_savings.png
   Scatter plot: age on x-axis, monthly savings on y-axis.
   Add a trend line (linear regression). Color points by country.

3. charts/03\_spending\_breakdown.png
   Horizontal bar chart showing the average % of income spent on each 
   expense category (housing, food, transport, entertainment, education, health).
   Sort from highest to lowest percentage.

4. charts/04\_satisfaction\_by\_ai\_usage.png
   Bar chart with three bars: Low / Medium / High AI tool users.
   Y-axis: average financial satisfaction score (1–5).
   Show the exact average value on top of each bar.

5. charts/05\_housing\_burden\_by\_country.png
   Horizontal bar chart: average housing cost as % of income, one bar per country.
   Sort from highest to lowest. Use a red-to-green color gradient 
   (high burden = red, low burden = green).

Save the script to scripts/04\_visualise.py

Phase 5

Prompt usado

I have completed the statistical analysis and created the visualisations.
Now I need to translate the numbers into clear, actionable insights for 
a non-technical audience — specifically the leadership team of a nonprofit 
that designs financial literacy programmes.

Example: “Respondents under 25 save an average of 6% of their income,
compared to 15% for those aged 28–32. This sharp increase suggests that
the 18–25 age group would benefit most from early intervention — specifi
cally, content about building a savings habit before expenses compound.”

For each of these 6 findings, write 3–4 sentences in plain language:
- What the data shows (the fact)
- Why it matters for a financial literacy programme (the implication)
- One specific programme recommendation based on this finding

Finding 1: Income differences across Latin American countries
Finding 2: The relationship between age and savings behaviour
Finding 3: Where the biggest expense categories are
Finding 4: How credit card holders differ from non-holders
Finding 5: The relationship between AI tool usage and financial satisfaction
Finding 6: Housing burden differences by country

Write these as they would appear in an executive report — professional,
concise, and evidence-based. Use specific numbers from the analysis.

REMEMBER that need to be clear enough for someone who has never seen the data. 

The reports are in another executive-summary.md

Los reportes son suficientemente claros, una persona sin nada de información podría entenderlo y sin duda proporciona buenas soluciones y acciones

Phase 6

Prompt usado

I now have all the analysis, charts, and interpretations for the project.
Please write the complete executive report as a Markdown file.

Save it to analysis-report.md in the project root.

The report must include these sections exactly:

# Datos que Hablan: Bienestar Financiero de Jóvenes Profesionales en América Latina
## Informe Ejecutivo — Futuro Digital LatAm, 2025

### 1. Resumen Ejecutivo
A 200-word summary of the 3 most important findings and 2 key recommendations.
Written for a reader who will only read this section.

### 2. Metodología
- Dataset: Encuesta de Bienestar Financiero 2025
- Sample: 500 respondents, 6 countries, ages 18–32
- Data collection and processing approach
- Data quality issues found and how they were resolved (from Phase 2)

### 3. Perfil de la Muestra
Describe who the 500 respondents are: countries represented, age distribution,
industries, occupations. Use specific numbers.

### 4. Hallazgos
One subsection per analysis from Phase 3.
Each subsection: the statistical finding + the plain-language interpretation
from Phase 5 + a reference to the relevant chart (e.g. "see Figure 1").

### 5. Recomendaciones
3–5 numbered recommendations for the financial literacy programme.
Each recommendation must cite at least one specific finding.

### 6. Conclusión
100 words. What does this data tell us about the state of financial wellness
among young Latin American professionals?

Use professional Markdown: headers, tables, bold for key numbers,
chart references as image links where appropriate.

Reporte generado

# Datos que Hablan: Bienestar Financiero de Jóvenes Profesionales en América Latina
## Informe Ejecutivo — Futuro Digital LatAm, 2025

---

### 1. Resumen Ejecutivo

Esta encuesta a 500 profesionales jóvenes (18–32 años) en seis países de América Latina revela tres patrones centrales. Primero, el **ahorro es un hábito que se aprende con la edad**: quienes tienen entre 18 y 22 años ahorran apenas el **5.7%** de su ingreso, mientras que el grupo de 29 a 32 años ahorra el **15.5%** — casi el triple. Segundo, **vivienda y alimentación consumen más de la mitad del ingreso** (28.5% y 23.8% respectivamente), dejando poco margen para el ahorro discrecional, especialmente en Argentina y Chile, donde la vivienda supera el 32% del ingreso. Tercero, existen **brechas económicas marcadas entre países**: el ingreso mediano en Brasil ($1,458) casi duplica al de Argentina ($798), por lo que un programa único para toda la región no será igualmente relevante en todos los mercados.

Dos recomendaciones concentran el mayor impacto potencial: (1) diseñar una intervención temprana de hábito de ahorro dirigida a los 18–25 años, el segmento más numeroso (57% de la muestra) y el que más se beneficiaría de actuar antes de que los gastos se acumulen; y (2) localizar el contenido del programa por país, con módulos específicos de estrategia de vivienda en Argentina y Chile, donde la carga habitacional es estructuralmente más alta.

---

### 2. Metodología

- **Dataset:** Encuesta de Bienestar Financiero 2025 (Futuro Digital LatAm)
- **Muestra:** 500 encuestados, 6 países, edades entre 18 y 32 años
- **Recolección y procesamiento:** los datos se recibieron como un archivo CSV único con 21 variables por respuesta (demográficas, de ingreso, gasto por categoría, ahorro, deuda, tenencia de productos financieros, meta financiera y uso de herramientas de IA). El procesamiento se realizó en Python (pandas) en tres etapas: exploración inicial (`scripts/01_explore.py`), limpieza (`scripts/02_clean.py`) y análisis estadístico (`scripts/03_analyse.py`), con visualizaciones generadas en `scripts/04_visualise.py`.
- **Calidad de datos — problemas encontrados y resueltos (Fase 2):**

| Problema | Alcance | Resolución |
|---|---|---|
| Categorías inconsistentes en `industria` (variantes de "Tecnología": mayúsculas, sin tilde, abreviatura "tech") | 10 de 500 filas | Se estandarizaron a una sola categoría mediante normalización de texto (minúsculas, sin acentos, mapeo de sinónimos) |
| Valores faltantes en `gasto_salud_usd` | 33 filas (6.6%) | Imputados con la mediana de la columna ($45.66 USD), por ser el porcentaje de faltantes bajo y la mediana robusta ante sesgo |
| Ahorro mensual negativo (`ahorro_mensual_usd` < 0) | 74 filas (14.8%) | Son datos válidos (gasto mayor al ingreso ese mes); se conservaron y se marcaron con la columna booleana `ahorro_negativo` en lugar de eliminarse |
| Texto con acentos/caracteres mal codificados en columnas de texto | 1,574 valores en 8 columnas | Normalizados a ASCII plano (ej. "México" → "Mexico") |
| Duplicados y espacios en blanco | 0 encontrados | No requirió acción |

El dataset limpio final (500 filas × 22 columnas, tras añadir `ahorro_negativo`) se guardó en `data/latam_finanzas_clean.csv` y es la fuente de todos los análisis de este informe.

---

### 3. Perfil de la Muestra

La muestra está compuesta por **500 profesionales jóvenes** distribuidos en **6 países**:

| País | Encuestados | % de la muestra |
|---|---|---|
| México | 150 | 30.0% |
| Colombia | 80 | 16.0% |
| Argentina | 70 | 14.0% |
| Chile | 70 | 14.0% |
| Brasil | 65 | 13.0% |
| Perú | 65 | 13.0% |

**Edad:** el rango es de 18 a 32 años, con una edad mediana de 25 años (promedio 24.96, desviación estándar 4.2). La distribución por grupo etario:

| Grupo de edad | Encuestados | % de la muestra |
|---|---|---|
| 18–22 | 162 | 32.4% |
| 23–25 | 123 | 24.6% |
| 26–28 | 87 | 17.4% |
| 29–32 | 128 | 25.6% |

Casi un tercio de la muestra (32.4%) tiene entre 18 y 22 años, y más de la mitad (57.0%) tiene 25 años o menos.

**Industria:** los encuestados provienen de 10 sectores, liderados por Finanzas (66), Tecnología (57) e Ingeniería (53); le siguen Ventas (51), Salud (49), Marketing (49), Educación (45), Diseño (45), Recursos Humanos (44) y Retail (41).

**Ocupación:** las ocupaciones más comunes son Diseñador Gráfico (56), Ingeniero (55), Community Manager (52), Gerente de Proyectos (51), Contador (50) y Analista Financiero (50), seguidas de Representante de Ventas (49), Coordinador de Marketing (47), Especialista en RRHH (47) y Docente (43).

**Productos financieros:** el 56.8% (284/500) tiene tarjeta de crédito, el 72.4% (362/500) tiene cuenta de ahorro, y el 46.8% (234/500) reporta tener deuda actualmente.

---

### 4. Hallazgos

#### 4.1 Diferencias de ingreso entre países

El ingreso mensual mediano varía de **$798 USD en Argentina a $1,458 USD en Brasil** — casi el doble. Brasil también presenta la mayor dispersión interna de ingresos (desviación estándar de $592, frente a $189–$290 en el resto), lo que indica una muestra brasileña mucho más heterogénea en términos económicos.

| País | Mediana | Media | Mín | Máx | Desv. estándar |
|---|---|---|---|---|---|
| Brasil | $1,458 | $1,388 | $300 | $2,874 | $592 |
| Chile | $1,246 | $1,245 | $575 | $1,861 | $290 |
| México | $1,067 | $1,042 | $300 | $1,693 | $287 |
| Colombia | $857 | $849 | $405 | $1,363 | $189 |
| Perú | $822 | $818 | $362 | $1,342 | $208 |
| Argentina | $798 | $766 | $373 | $1,343 | $204 |

*Ver Figura 1 (`charts/01_income_by_country.png`).*

Estas diferencias implican que un currículo único, calibrado con un solo nivel de ingreso "promedio regional", resultará irrelevante en algunos mercados e inaccesible en otros. **Recomendación derivada:** localizar los ejemplos y umbrales de presupuesto del programa por país, y considerar contenido segmentado en Brasil dada su alta dispersión interna.

#### 4.2 Relación entre edad y comportamiento de ahorro

La tasa de ahorro casi se triplica con la edad: el grupo de 18–22 años ahorra en promedio **$61/mes (5.7% del ingreso)**, mientras que el grupo de 29–32 años ahorra **$154/mes (15.5%)**.

| Grupo de edad | Ahorro mensual promedio | Tasa de ahorro promedio | n |
|---|---|---|---|
| 18–22 | $60.80 | 5.72% | 162 |
| 23–25 | $76.48 | 8.32% | 123 |
| 26–28 | $120.98 | 11.72% | 87 |
| 29–32 | $154.07 | 15.52% | 128 |

*Ver Figura 2 (`charts/02_age_vs_savings.png`).*

Dado que el hábito de ahorro se fortalece con el tiempo y este segmento joven representa más de la mitad de la muestra, intervenir temprano tiene un efecto compuesto de largo plazo. **Recomendación derivada:** priorizar un módulo de "hábito de ahorro" para el segmento de 18–25 años, antes de que los gastos se acumulen.

#### 4.3 Dónde se concentra el gasto

Vivienda (**28.5%** del ingreso) y alimentación (**23.8%**) son, por mucho, las categorías de mayor peso, sumando más de la mitad del ingreso mensual promedio. Le siguen transporte (10.1%), entretenimiento (8.7%), educación (8.5%) y salud (4.9%), la categoría más pequeña.

| Categoría | % promedio del ingreso |
|---|---|
| Vivienda | 28.5% |
| Alimentación | 23.8% |
| Transporte | 10.1% |
| Entretenimiento | 8.7% |
| Educación | 8.5% |
| Salud | 4.9% |

*Ver Figura 3 (`charts/03_spending_breakdown.png`).*

Como vivienda y alimentación son mayormente gastos no discrecionales, consejos genéricos de "gastar menos" tendrán poco efecto: la palanca real está en cómo se gestionan específicamente estas dos categorías. **Recomendación derivada:** construir el currículo base alrededor de estrategias concretas de vivienda (ej. compartir gastos, relación renta/ingreso) y planificación inteligente de alimentación.

#### 4.4 Titulares de tarjeta de crédito frente a no titulares

Los titulares de tarjeta de crédito ganan apenas **1.5% más** que los no titulares en promedio — una diferencia casi nula — pero gastan **16.1% más en alimentación** y **17.2% más en entretenimiento**. A pesar de este mayor gasto, ahorran **6.7% más**, lo que indica que la tarjeta cambia el comportamiento de gasto de forma independiente del nivel de ingreso.

| Grupo | Ingreso promedio | Gasto en alimentación | Gasto en entretenimiento | Ahorro promedio |
|---|---|---|---|---|
| Con tarjeta de crédito | $1,023 | $258 | $95 | $102 |
| Sin tarjeta de crédito | $1,008 | $222 | $81 | $95 |
| Diferencia % | +1.5% | +16.1% | +17.2% | +6.7% |

*(Este hallazgo se presenta como tabla; no tiene gráfico dedicado entre las 5 visualizaciones del proyecto — ver tabla completa en `scripts/03_analyse.py`, sección 4.)*

Como el ingreso no explica esta diferencia, el foco del programa para este grupo debe ser el comportamiento, no la generación de ingresos. **Recomendación derivada:** para titulares de tarjeta, incluir un módulo de conciencia de gasto discrecional ("conoce tu fuga") en alimentación y entretenimiento.

#### 4.5 Uso de herramientas de IA y satisfacción financiera

La satisfacción financiera aumenta con el uso de herramientas de IA: el grupo de uso bajo (0–3 hrs/semana, 150 personas) reporta 2.11 sobre 5, el de uso medio (4–10 hrs/semana, 335 personas) reporta 2.60, y el de uso alto (11+ hrs/semana, solo 15 personas) reporta 3.53. La correlación de Pearson entre horas de uso y satisfacción es **r = 0.571** (moderada-positiva).

| Grupo de uso de IA | n | Satisfacción promedio | Ingreso promedio |
|---|---|---|---|
| Bajo (0–3 hrs) | 150 | 2.11 | $776 |
| Medio (4–10 hrs) | 335 | 2.60 | $1,085 |
| Alto (11+ hrs) | 15 | 3.53 | $1,895 |

*Ver Figura 4 (`charts/04_satisfaction_by_ai_usage.png`).*

Sin embargo, el grupo de uso alto también tiene el ingreso más alto por un amplio margen y es una submuestra muy pequeña (15 personas), por lo que esta relación probablemente refleja acceso a herramientas más que un efecto causal directo del uso de IA sobre la satisfacción. **Recomendación derivada:** tratar esto como una brecha de acceso, no como causalidad comprobada, e introducir alfabetización básica en herramientas de presupuesto con IA para participantes de menores ingresos.

#### 4.6 Carga de vivienda por país

El costo de vivienda como porcentaje del ingreso varía de **24.6% en Perú a 34.1% en Argentina**, con Argentina y Chile superando el umbral de asequibilidad del 30% comúnmente citado en literatura de vivienda.

| País | Vivienda (% del ingreso) |
|---|---|
| Argentina | 34.1% |
| Chile | 32.6% |
| México | 28.1% |
| Brasil | 26.9% |
| Colombia | 25.4% |
| Perú | 24.6% |

*Ver Figura 5 (`charts/05_housing_burden_by_country.png`).*

En Argentina y Chile, la presión de vivienda es una restricción estructural: ninguna habilidad de presupuesto puede compensar por completo un costo fijo que ya es inasequible. **Recomendación derivada:** para estos dos países, incluir un módulo dedicado de estrategia de vivienda (vivienda compartida, negociación de renta, navegación de subsidios), en lugar de tratar la vivienda como un gasto discrecional más.

---

### 5. Recomendaciones

1. **Priorizar un módulo de hábito de ahorro temprano para el segmento de 18–25 años.** Este grupo ahorra apenas 5.7%–8.3% de su ingreso frente al 15.5% del grupo de 29–32 años (Hallazgo 4.2), y representa el 57% de la muestra — el mayor alcance potencial del programa.

2. **Construir el currículo base alrededor de vivienda y alimentación, no de categorías de gasto genéricas.** Estas dos categorías consumen más de la mitad del ingreso promedio (Hallazgo 4.3), por lo que son la palanca de mayor impacto real sobre las finanzas de los participantes.

3. **Localizar el contenido por país, con un módulo específico de estrategia de vivienda para Argentina y Chile.** El ingreso mediano varía casi al doble entre países (Hallazgo 4.1), y la carga de vivienda en Argentina (34.1%) y Chile (32.6%) supera el umbral de asequibilidad del 30% (Hallazgo 4.6).

4. **Incluir un módulo de conciencia de gasto discrecional para titulares de tarjeta de crédito.** Este grupo gasta 16–17% más en alimentación y entretenimiento sin una diferencia significativa de ingreso (Hallazgo 4.4), lo que apunta a un problema de comportamiento, no de capacidad económica.

5. **Incorporar alfabetización básica en herramientas de presupuesto con IA, dirigida a participantes de menor ingreso.** El uso de estas herramientas está asociado con mayor satisfacción financiera (r=0.571, Hallazgo 4.5), pero su adopción parece concentrada en el segmento de mayores ingresos, dejando una brecha de acceso por cerrar.

---

### 6. Conclusión

Los datos muestran una población financieramente activa pero desigualmente preparada: el ahorro es un músculo que se desarrolla con la edad, no algo con lo que los jóvenes de 18–25 años ya cuenten, y los costos fijos de vivienda y alimentación —agravados en países como Argentina y Chile— limitan cuánto puede lograr la educación financiera por sí sola. El bienestar financiero de esta generación no depende solo de mejores hábitos individuales, sino de programas que reconozcan las diferencias estructurales entre países, edades y niveles de acceso a herramientas financieras.
