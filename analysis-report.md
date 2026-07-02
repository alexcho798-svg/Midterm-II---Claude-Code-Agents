# Reporte de Exploracion Inicial - latam_finanzas_2025

Dataset: encuesta financiera a 500 profesionales jovenes de Latinoamerica.

- Datos crudos: `data/latam_finanzas_2025.csv`
- Datos limpios: `data/latam_finanzas_2025_clean.csv`
- Scripts: `scripts/01_explore.py`, `scripts/02_clean.py`

## 1. Dimensiones

- Filas: 500
- Columnas: 21

## 2. Columnas y tipos de dato

| Columna | Tipo |
|---|---|
| id | int64 |
| nombre | str |
| pais | str |
| edad | int64 |
| ocupacion | str |
| industria | str |
| ingreso_mensual_usd | float64 |
| gasto_vivienda_usd | float64 |
| gasto_alimentacion_usd | float64 |
| gasto_transporte_usd | float64 |
| gasto_entretenimiento_usd | float64 |
| gasto_educacion_usd | float64 |
| gasto_salud_usd | float64 |
| ahorro_mensual_usd | float64 |
| tiene_tarjeta_credito | str |
| tiene_cuenta_ahorro | str |
| tiene_deuda | str |
| deuda_total_usd | float64 |
| meta_financiera | str |
| horas_herramientas_ia_semana | float64 |
| satisfaccion_financiera | int64 |

## 3. Valores faltantes

Solo una columna tiene valores nulos:

| Columna | Faltantes | % |
|---|---|---|
| gasto_salud_usd | 33 | 6.6% |

Pendiente decidir estrategia (imputar con mediana, dejar como NaN, o excluir en analisis puntuales).

## 4. Estadisticas de columnas numericas

| Columna | min | max | mean | median | std |
|---|---|---|---|---|---|
| edad | 18.00 | 32.00 | 24.96 | 25.00 | 4.22 |
| ingreso_mensual_usd | 300.00 | 2,874.49 | 1,016.80 | 960.34 | 376.81 |
| gasto_vivienda_usd | 55.61 | 796.33 | 290.32 | 267.87 | 125.03 |
| gasto_alimentacion_usd | 60.00 | 741.66 | 242.61 | 227.78 | 102.79 |
| gasto_transporte_usd | 20.00 | 300.58 | 102.19 | 94.57 | 49.31 |
| gasto_entretenimiento_usd | 10.00 | 410.21 | 88.56 | 79.05 | 50.25 |
| gasto_educacion_usd | 10.37 | 211.31 | 82.18 | 80.32 | 33.85 |
| gasto_salud_usd | 0.00 | 150.23 | 49.88 | 45.66 | 28.61 |
| ahorro_mensual_usd | -160.02 | 451.38 | 99.00 | 92.44 | 95.59 |
| deuda_total_usd | 0.00 | 10,918.73 | 1,849.69 | 0.00 | 2,565.57 |
| horas_herramientas_ia_semana | 0.00 | 16.10 | 5.41 | 5.20 | 2.70 |
| satisfaccion_financiera | 1.00 | 5.00 | 2.48 | 2.00 | 0.62 |

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

## 6. Hallazgos y calidad de datos

### Valores unicos / inconsistencias
- `industria` tenia "Tecnologia" repartida en 4 variantes (`Tecnologia`, `Tecnologia` sin tilde, `tech`, `TECNOLOGIA`) por errores de captura/mayusculas. **Corregido** en `data/latam_finanzas_2025_clean.csv` via `scripts/02_clean.py`, quedando 10 categorias en vez de 13.
- El resto de columnas categoricas (`pais`, `ocupacion`, `meta_financiera`, `tiene_tarjeta_credito`, `tiene_cuenta_ahorro`, `tiene_deuda`) estan limpias, sin typos ni variantes.
- No se encontraron espacios en blanco al inicio/final en columnas de texto, ni IDs o filas duplicadas.

### Valores faltantes
- Unica columna con nulos: `gasto_salud_usd` (33 filas, 6.6%). El resto del dataset esta completo.

### Rangos min/max
- `ahorro_mensual_usd` tiene un minimo de **-160.02**: plausible (mes en que el gasto supero el ingreso), pero se debe confirmar que no sea un error de signo antes de usarlo en calculos agregados.
- `deuda_total_usd` va de 0 a **10,918.73**, con mediana 0 y media 1,849.69: fuertemente sesgada a la derecha, consistente con que 266/500 personas no tienen deuda (`tiene_deuda` = No). Preferir mediana/percentiles sobre la media para resumir esta columna.
- `edad` (18-32) y `satisfaccion_financiera` (1-5) tienen rangos acotados y razonables, sin valores fuera de rango.

## 7. Estado de limpieza

- [x] Estandarizar categorias de `industria`
- [ ] Definir estrategia para los 33 nulos de `gasto_salud_usd`
- [ ] Confirmar si los valores negativos de `ahorro_mensual_usd` son intencionales
