# Initial Exploration Report - latam_finanzas_2025

Dataset: financial survey of 500 young professionals from Latin America.

Prompt used

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

## 1. Dimensions

- Rows: 500
- Columns: 21

## . Missing values

Only one column has null values:

| Column          | Missing | % |
| gasto_salud_usd | 33        | 6.6% |

## 4. Numeric column statistics

| Column                        | min    | max       | mean     | median  | std      |
|--------------------------------|--------|---------- |----------|---      |---       |
| edad (age)                     | 18.00  | 32.00     | 24.96    | 25.00   | 4.22     |
| ingreso_mensual_usd (monthly income) | 300.00 | 2,874.49  | 1,016.80 | 960.34  | 376.81   |
| gasto_vivienda_usd (housing spend)   | 55.61  | 796.33    | 290.32   | 267.87  | 125.03   |
| gasto_alimentacion_usd (food spend)  | 60.00  | 741.66    | 242.61   | 227.78  | 102.79   |
| gasto_transporte_usd (transport spend) | 20.00  | 300.58    | 102.19   | 94.57   | 49.31    |
| gasto_entretenimiento_usd (entertainment spend) | 10.00  | 410.21    | 88.56    | 79.05   | 50.25    |
| gasto_educacion_usd (education spend)  | 10.37  | 211.31    | 82.18    | 80.32   | 33.85    |
| gasto_salud_usd (health spend)         | 0.00   | 150.23    | 49.88    | 45.66   | 28.61    |
| ahorro_mensual_usd (monthly savings)   | -160.02| 451.38    | 99.00    | 92.44   | 95.59    |
| deuda_total_usd (total debt)           | 0.00   | 10,918.73 | 1,849.69 | 0.00    | 2,565.57 |
| horas_herramientas_ia_semana (AI tool hours/week) | 0.00   | 16.10     | 5.41     | 5.20    | 2.70     |
| satisfaccion_financiera (financial satisfaction) | 1.00   | 5.00      | 2.48     | 2.00    | 0.62     |

## 5. Categorical columns

**pais (country)** (6 values): Mexico 150, Colombia 80, Argentina 70, Chile 70, Brazil 65, Peru 65

**industria (industry)**:
- Raw (13 values, with inconsistencies): Finance 66, Engineering 53, Sales 51, Health 49, Marketing 49, Technology 47, Education 45, Design 45, Human Resources 44, Retail 41, Technology (no accent) 5, tech 3, TECHNOLOGY (uppercase) 2
- Clean (10 values): Finance 66, Technology 57, Engineering 53, Sales 51, Health 49, Marketing 49, Education 45, Design 45, Human Resources 44, Retail 41

**ocupacion (occupation)** (10 values): Graphic Designer 56, Engineer 55, Community Manager 52, Project Manager 51, Accountant 50, Financial Analyst 50, Sales Representative 49, Marketing Coordinator 47, HR Specialist 47, Teacher 43

**meta_financiera (financial goal)** (8 values): Pay off debt 81, Invest in stock market 75, Save for retirement 68, Save for travel 61, Buy a house 61, Start a business 58, Graduate studies 52, Emergency fund 44

**tiene_tarjeta_credito (has credit card)**: Yes 284, No 216

**tiene_cuenta_ahorro (has savings account)**: Yes 362, No 138

**tiene_deuda (has debt)**: No 266, Yes 234

Phase 2

Prompt used

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

## . Findings and data quality


### Unique values / inconsistencies
- `industria` had "Tecnologia" (Technology) split across 4 variants (`Tecnologia`, `Tecnologia` without accent, `tech`, `TECNOLOGIA`) due to capture errors/capitalization. - The rest of the categorical columns (`pais`, `ocupacion`, `meta_financiera`, `tiene_tarjeta_credito`, `tiene_cuenta_ahorro`, `tiene_deuda`) are clean, with no typos or variants.
- No leading/trailing whitespace was found in text columns, nor duplicate IDs or rows.

### Missing values
- Only column with nulls: `gasto_salud_usd` (33 rows, 6.6%). The rest of the dataset is complete.

### Min/max ranges
- `ahorro_mensual_usd` has a minimum of **-160.02**: plausible (a month where spending exceeded income), but it should be confirmed that it's not a sign error before using it in aggregate calculations.
- `deuda_total_usd` ranges from 0 to **10,918.73**, with a median of 0 and mean of 1,849.69: strongly right-skewed, consistent with 266/500 people having no debt (`tiene_deuda` = No). Prefer median/percentiles over the mean to summarize this column.
- `edad` (age, 18-32) and `satisfaccion_financiera` (financial satisfaction, 1-5) have bounded, reasonable ranges, with no out-of-range values.

### Rows and columns affected 
At first the categories were standardized across 57 rows, then I added the negative savings column, for greater agility when searching the data, and filled gasto_salud (the column with null values) with the median of the values; in total 91 rows were modified.

I used the median since one of the rows was already using that method and Claude supported that idea, and also I standardized the data for aesthetics and easier data searching

Phase 2.5

Prompt used

---
name: country-profiler
description: Use PROACTIVELY whenever the user asks for a statistical profile, summary, breakdown, or analysis of one or more Latin American countries from the finance dataset (data/latam_finanzas_clean.csv). Triggers on requests like "profile of Mexico", "analyze Argentina", "give me the statistics for Chile", "compare Peru and Brazil", "financial summary of Colombia", or any request to profile/summarize/compare countries in the dataset. Also triggers when the user asks to run this for "all countries" or lists multiple country names together. Returns a Markdown section per country covering sample size, income stats, housing burden, spending breakdown, savings, and AI tool usage.
---
You are a data analyst assistant. When given a country name, read
`data/latam_finanzas_clean.csv` and produce a Markdown section with:
1. Sample size and age range for this country
2. Income: median, mean, min, max, standard deviation (USD)
3. Housing burden: average gasto_vivienda_usd as % of ingreso_mensual_usd
4. Spending breakdown: average % of income for each gasto_* column
5. Savings: average ahorro_mensual_usd and % of respondents with negative savings
6. AI tools: average horas_herramientas_ia_semana and average satisfaccion_financiera

Use the country name as the Markdown section header (## Country: [name]).
Save the supporting Python script as scripts/country_[name].py.

If multiple countries are requested at once, invoke this profile process for each country in parallel and combine all sections into a single Markdown file.


Which country has the highest housing burden? Does it match what you expected? Argentina 

Phase 4

Prompt used 

I now have a clean dataset at data/latam_finanzas_clean.csv and six country
profiles already generated in scripts/country_profiles.md.

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
   horas_herramientas_ia_semana and satisfaccion_financiera.

6. HOUSING BURDEN BY COUNTRY
   Reference the country profiles. Confirm and format the average housing
   expense as % of income for each country, sorted from highest to lowest.

Save the script to scripts/03_analyse.py
```
I want to point out that Brazil has the highest income and that the teaching profession is among the best paid; I expected housing to be the biggest expense out of professionals' salaries.

Things to highlight

1.- Argentina has the highest housing burden but the lowest % of negative savings
2.- Credit card holders spend noticeably more on entertainment and food, not just because of higher income
3.- Clear upward trend: higher age → higher savings rate

Phase 4.

Using data/latam_finanzas_clean.csv, create the following 5 charts.
Save each as a PNG in the charts/ folder with the filenames shown.
Use a professional color palette (not the default matplotlib colors).
All charts must have: a clear title, labelled axes, and a source note 
"Source: Encuesta de Bienestar Financiero LatAm 2025, Futuro Digital LatAm".

1. charts/01_income_by_country.png
   Box plot showing the income distribution for each country.
   Sort countries by median income (highest on top for a horizontal box plot).

2. charts/02_age_vs_savings.png
   Scatter plot: age on x-axis, monthly savings on y-axis.
   Add a trend line (linear regression). Color points by country.

3. charts/03_spending_breakdown.png
   Horizontal bar chart showing the average % of income spent on each 
   expense category (housing, food, transport, entertainment, education, health).
   Sort from highest to lowest percentage.

4. charts/04_satisfaction_by_ai_usage.png
   Bar chart with three bars: Low / Medium / High AI tool users.
   Y-axis: average financial satisfaction score (1–5).
   Show the exact average value on top of each bar.

5. charts/05_housing_burden_by_country.png
   Horizontal bar chart: average housing cost as % of income, one bar per country.
   Sort from highest to lowest. Use a red-to-green color gradient 
   (high burden = red, low burden = green).

Save the script to scripts/04_visualise.py

Phase 5

Prompt used

I have completed the statistical analysis and created the visualisations.
Now I need to translate the numbers into clear, actionable insights for 
a non-technical audience — specifically the leadership team of a nonprofit 
that designs financial literacy programmes.

Example: "Respondents under 25 save an average of 6% of their income,
compared to 15% for those aged 28–32. This sharp increase suggests that
the 18–25 age group would benefit most from early intervention — specifi
cally, content about building a savings habit before expenses compound."

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

The reports are clear enough, someone with no background information at all could understand them, and they definitely provide good solutions and actions

Phase 6

Prompt used

I now have all the analysis, charts, and interpretations for the project.
Please write the complete executive report as a Markdown file.

Save it to analysis-report.md in the project root.

The report must include these sections exactly:

# Data That Speaks: Financial Wellness of Young Professionals in Latin America
## Executive Report — Futuro Digital LatAm, 2025

### 1. Executive Summary
A 200-word summary of the 3 most important findings and 2 key recommendations.
Written for a reader who will only read this section.

### 2. Methodology
- Dataset: 2025 Financial Wellness Survey
- Sample: 500 respondents, 6 countries, ages 18–32
- Data collection and processing approach
- Data quality issues found and how they were resolved (from Phase 2)

### 3. Sample Profile
Describe who the 500 respondents are: countries represented, age distribution,
industries, occupations. Use specific numbers.

### 4. Findings
One subsection per analysis from Phase 3.
Each subsection: the statistical finding + the plain-language interpretation
from Phase 5 + a reference to the relevant chart (e.g. "see Figure 1").

### 5. Recommendations
3–5 numbered recommendations for the financial literacy programme.
Each recommendation must cite at least one specific finding.

### 6. Conclusion
100 words. What does this data tell us about the state of financial wellness
among young Latin American professionals?

Use professional Markdown: headers, tables, bold for key numbers,
chart references as image links where appropriate.

Report generated

# Data That Speaks: Financial Wellness of Young Professionals in Latin America
## Executive Report — Futuro Digital LatAm, 2025

---

### 1. Executive Summary

This survey of 500 young professionals (ages 18–32) across six Latin American countries reveals three central patterns. First, **saving is a habit learned with age**: those aged 18 to 22 save only **5.7%** of their income, while the 29-to-32 age group saves **15.5%** — nearly triple. Second, **housing and food consume more than half of income** (28.5% and 23.8% respectively), leaving little room for discretionary savings, especially in Argentina and Chile, where housing exceeds 32% of income. Third, there are **marked economic gaps between countries**: median income in Brazil ($1,458) is nearly double that of Argentina ($798), meaning a single program for the entire region will not be equally relevant across all markets.

Two recommendations carry the greatest potential impact: (1) design an early savings-habit intervention aimed at the 18–25 age group, the largest segment (57% of the sample) and the one that would benefit most from acting before expenses accumulate; and (2) localize program content by country, with dedicated housing-strategy modules in Argentina and Chile, where the housing burden is structurally higher.

---

### 2. Methodology

- **Dataset:** 2025 Financial Wellness Survey (Futuro Digital LatAm)
- **Sample:** 500 respondents, 6 countries, ages 18 to 32
- **Collection and processing:** the data was received as a single CSV file with 21 variables per response (demographic, income, spending by category, savings, debt, financial product ownership, financial goal, and AI tool usage). Processing was done in Python (pandas) in three stages: initial exploration (`scripts/01_explore.py`), cleaning (`scripts/02_clean.py`), and statistical analysis (`scripts/03_analyse.py`), with visualizations generated in `scripts/04_visualise.py`.
- **Data quality — issues found and resolved (Phase 2):**

| Issue | Scope | Resolution |
|---|---|---|
| Inconsistent categories in `industria` ("Technology" variants: uppercase, no accent, abbreviation "tech") | 10 of 500 rows | Standardized into a single category through text normalization (lowercase, no accents, synonym mapping) |
| Missing values in `gasto_salud_usd` | 33 rows (6.6%) | Imputed with the column median ($45.66 USD), since the missing percentage was low and the median is robust to skew |
| Negative monthly savings (`ahorro_mensual_usd` < 0) | 74 rows (14.8%) | Valid data (spending exceeded income that month); kept and flagged with the boolean column `ahorro_negativo` instead of being removed |
| Text with accented/mis-encoded characters in text columns | 1,574 values across 8 columns | Normalized to plain ASCII (e.g. "México" → "Mexico") |
| Duplicates and whitespace | 0 found | No action required |

The final clean dataset (500 rows × 22 columns, after adding `ahorro_negativo`) was saved to `data/latam_finanzas_clean.csv` and is the source for all analyses in this report.

---

### 3. Sample Profile

The sample consists of **500 young professionals** distributed across **6 countries**:

| Country | Respondents | % of sample |
|---|---|---|
| Mexico | 150 | 30.0% |
| Colombia | 80 | 16.0% |
| Argentina | 70 | 14.0% |
| Chile | 70 | 14.0% |
| Brazil | 65 | 13.0% |
| Peru | 65 | 13.0% |

**Age:** the range is 18 to 32 years, with a median age of 25 (mean 24.96, standard deviation 4.2). Distribution by age group:

| Age group | Respondents | % of sample |
|---|---|---|
| 18–22 | 162 | 32.4% |
| 23–25 | 123 | 24.6% |
| 26–28 | 87 | 17.4% |
| 29–32 | 128 | 25.6% |

Nearly a third of the sample (32.4%) is between 18 and 22 years old, and more than half (57.0%) is 25 or younger.

**Industry:** respondents come from 10 sectors, led by Finance (66), Technology (57), and Engineering (53); followed by Sales (51), Health (49), Marketing (49), Education (45), Design (45), Human Resources (44), and Retail (41).

**Occupation:** the most common occupations are Graphic Designer (56), Engineer (55), Community Manager (52), Project Manager (51), Accountant (50), and Financial Analyst (50), followed by Sales Representative (49), Marketing Coordinator (47), HR Specialist (47), and Teacher (43).

**Financial products:** 56.8% (284/500) have a credit card, 72.4% (362/500) have a savings account, and 46.8% (234/500) report currently having debt.

---

### 4. Findings

#### 4.1 Income differences across countries

Median monthly income ranges from **$798 USD in Argentina to $1,458 USD in Brazil** — nearly double. Brazil also shows the greatest internal income dispersion (standard deviation of $592, versus $189–$290 in the rest), indicating a much more economically heterogeneous Brazilian sample.

| Country | Median | Mean | Min | Max | Std. Dev. |
|---|---|---|---|---|---|
| Brazil | $1,458 | $1,388 | $300 | $2,874 | $592 |
| Chile | $1,246 | $1,245 | $575 | $1,861 | $290 |
| Mexico | $1,067 | $1,042 | $300 | $1,693 | $287 |
| Colombia | $857 | $849 | $405 | $1,363 | $189 |
| Peru | $822 | $818 | $362 | $1,342 | $208 |
| Argentina | $798 | $766 | $373 | $1,343 | $204 |

*See Figure 1 (`charts/01_income_by_country.png`).*

These differences mean that a single curriculum, calibrated to one "regional average" income level, will be irrelevant in some markets and inaccessible in others. **Resulting recommendation:** localize the program's budget examples and thresholds by country, and consider segmented content for Brazil given its high internal dispersion.

#### 4.2 Relationship between age and savings behavior

The savings rate nearly triples with age: the 18–22 age group saves on average **$61/month (5.7% of income)**, while the 29–32 group saves **$154/month (15.5%)**.

| Age group | Average monthly savings | Average savings rate | n |
|---|---|---|---|
| 18–22 | $60.80 | 5.72% | 162 |
| 23–25 | $76.48 | 8.32% | 123 |
| 26–28 | $120.98 | 11.72% | 87 |
| 29–32 | $154.07 | 15.52% | 128 |

*See Figure 2 (`charts/02_age_vs_savings.png`).*

Since the savings habit strengthens over time and this young segment represents more than half the sample, intervening early has a long-term compounding effect. **Resulting recommendation:** prioritize a "savings habit" module for the 18–25 age segment, before expenses accumulate.

#### 4.3 Where spending is concentrated

Housing (**28.5%** of income) and food (**23.8%**) are by far the heaviest categories, together accounting for more than half of average monthly income. They are followed by transport (10.1%), entertainment (8.7%), education (8.5%), and health (4.9%), the smallest category.

| Category | Average % of income |
|---|---|
| Housing | 28.5% |
| Food | 23.8% |
| Transport | 10.1% |
| Entertainment | 8.7% |
| Education | 8.5% |
| Health | 4.9% |

*See Figure 3 (`charts/03_spending_breakdown.png`).*

Since housing and food are mostly non-discretionary expenses, generic "spend less" advice will have little effect: the real lever is how these two categories are specifically managed. **Resulting recommendation:** build the core curriculum around concrete housing strategies (e.g. cost-sharing, rent-to-income ratio) and smart food planning.

#### 4.4 Credit card holders vs. non-holders

Credit card holders earn only **1.5% more** than non-holders on average — an almost negligible difference — but spend **16.1% more on food** and **17.2% more on entertainment**. Despite this higher spending, they save **6.7% more**, indicating that the card changes spending behavior independently of income level.

| Group | Average income | Food spending | Entertainment spending | Average savings |
|---|---|---|---|---|
| With credit card | $1,023 | $258 | $95 | $102 |
| Without credit card | $1,008 | $222 | $81 | $95 |
| % difference | +1.5% | +16.1% | +17.2% | +6.7% |

*(This finding is presented as a table; it does not have a dedicated chart among the project's 5 visualizations — see the full table in `scripts/03_analyse.py`, section 4.)*

Since income does not explain this difference, the program's focus for this group should be behavior, not income generation. **Resulting recommendation:** for credit card holders, include a discretionary-spending awareness module ("know your leak") for food and entertainment.

#### 4.5 AI tool usage and financial satisfaction

Financial satisfaction increases with AI tool usage: the low-usage group (0–3 hrs/week, 150 people) reports 2.11 out of 5, the medium-usage group (4–10 hrs/week, 335 people) reports 2.60, and the high-usage group (11+ hrs/week, only 15 people) reports 3.53. The Pearson correlation between hours of use and satisfaction is **r = 0.571** (moderate-positive).

| AI usage group | n | Average satisfaction | Average income |
|---|---|---|---|
| Low (0–3 hrs) | 150 | 2.11 | $776 |
| Medium (4–10 hrs) | 335 | 2.60 | $1,085 |
| High (11+ hrs) | 15 | 3.53 | $1,895 |

*See Figure 4 (`charts/04_satisfaction_by_ai_usage.png`).*

However, the high-usage group also has the highest income by a wide margin and is a very small subsample (15 people), so this relationship likely reflects access to tools rather than a direct causal effect of AI usage on satisfaction. **Resulting recommendation:** treat this as an access gap, not proven causation, and introduce basic literacy in AI budgeting tools for lower-income participants.

#### 4.6 Housing burden by country

Housing cost as a percentage of income ranges from **24.6% in Peru to 34.1% in Argentina**, with Argentina and Chile exceeding the 30% affordability threshold commonly cited in housing literature.

| Country | Housing (% of income) |
|---|---|
| Argentina | 34.1% |
| Chile | 32.6% |
| Mexico | 28.1% |
| Brazil | 26.9% |
| Colombia | 25.4% |
| Peru | 24.6% |

*See Figure 5 (`charts/05_housing_burden_by_country.png`).*

In Argentina and Chile, housing pressure is a structural constraint: no budgeting skill can fully offset a fixed cost that is already unaffordable. **Resulting recommendation:** for these two countries, include a dedicated housing-strategy module (shared housing, rent negotiation, subsidy navigation), rather than treating housing as just another discretionary expense.

---

### 5. Recommendations

1. **Prioritize an early savings-habit module for the 18–25 age segment.** This group saves only 5.7%–8.3% of its income compared to 15.5% for the 29–32 group (Finding 4.2), and represents 57% of the sample — the program's greatest potential reach.

2. **Build the core curriculum around housing and food, not generic spending categories.** These two categories consume more than half of average income (Finding 4.3), making them the highest-impact real lever on participants' finances.

3. **Localize content by country, with a specific housing-strategy module for Argentina and Chile.** Median income varies by nearly double between countries (Finding 4.1), and the housing burden in Argentina (34.1%) and Chile (32.6%) exceeds the 30% affordability threshold (Finding 4.6).

4. **Include a discretionary-spending awareness module for credit card holders.** This group spends 16–17% more on food and entertainment with no significant income difference (Finding 4.4), pointing to a behavioral rather than economic-capacity issue.

5. **Introduce basic literacy in AI budgeting tools, aimed at lower-income participants.** Use of these tools is associated with higher financial satisfaction (r=0.571, Finding 4.5), but adoption appears concentrated in the higher-income segment, leaving an access gap to close.

---

### 6. Conclusion

The data shows a financially active but unevenly prepared population: saving is a muscle that develops with age, not something 18–25 year-olds already have, and fixed housing and food costs — worsened in countries like Argentina and Chile — limit how much financial education alone can achieve. This generation's financial wellbeing depends not only on better individual habits, but on programs that recognize the structural differences between countries, ages, and levels of access to financial tools.
