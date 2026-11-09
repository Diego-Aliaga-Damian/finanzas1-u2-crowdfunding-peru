# Fase II — Diseño de investigación

**Tema N.º 96:** Fintech y financiamiento participativo (crowdfunding) en el Perú: oferta y condiciones
**Estudiante:** Diego Sebastián Aliaga Damián (2024200481M) · **Versión:** 1.0 — 2026-11-07
**Numerales aplicables:** 2.2 (Introducción, Antecedentes, Materiales y métodos), 2.4.1 (variables, tamaño e integrabilidad), 2.4.4 (semilla), rúbrica C3 ("El objetivo, los datos y los resultados son coherentes entre sí").

> Este diseño se apoya **solo en datos verificados** en las Fases I y II. Si algo depende de la respuesta del docente, se marca como **[confirmar]**. Toda cita bibliográfica queda pendiente hasta la Fase II-B (antecedentes con DOI verificado), de modo que este documento no contiene referencias sin verificar.

---

## Decisiones del docente (comunicadas por el estudiante el 2026-11-07)

| Consulta | Respuesta |
|---|---|
| Fechas | **Entrega fija: 2026-12-06, 23:59.** La fecha de exposición no es segura (suele cambiar) |
| Variables sustitutas de "tasa ofrecida, plazo y sector" | **Aceptadas** (sección 9) |
| Panel mensual 2021-01 a 2026-09 para el mínimo de 60 periodos | **Aceptado** (secciones 10 y 11) |
| Ventana del estado del arte | **2023-2026**; las normas y las fuentes de datos no cuentan en el estado del arte |
| Plataformas retiradas del SIMV como incidencia, cubiertas con los EEFF de la SMV | **De acuerdo**, sin sustitución de fuente |

## 0. Hallazgos nuevos que condicionan el diseño (verificados el 2026-11-07)

| Hallazgo | Evidencia | Consecuencia para el diseño |
|---|---|---|
| El SIMV distingue **"sin registros"** de un **cero reportado** | Inversiones.io (mar-jun 2022): "No se encontraron registros". Securite (jun-2026): filas con 0 | Regla de codificación: "sin registros" = faltante; 0 reportado = 0 |
| Primeros datos FPF hallados: **jun-2022** (Afluenta, préstamos personales: 31 publicados, 14 financiados, S/ 62 143) | Consulta SIMV | La serie FPF tiene **~52 meses** hasta 2026-09: **menos de 60** |
| Inversiones.io: primeros datos hallados en dic-2022 (9/9/S/ 1 116 747); sep-2026: 44/43/S/ 13 658 108 | Consulta SIMV | Plataforma líder; su peso exige un análisis de sensibilidad |
| **Oct-2026 aún no está publicado** en el SIMV | Inversiones.io, 2026-10: sin registros | **FECHA_CORTE = 2026-09** (rezago de ~1 mes) |
| Modalidad observada: solo **PRÉSTAMOS** (no apareció financiamiento con valores) | Todas las consultas con datos | La "modalidad" casi no varía; el contraste útil es **empresarial frente a personal** |
| El "Reglamento Interno" en el SIMV no tiene registros para Inversiones.io | Consulta SIMV | **No hay fuente oficial de tasas ni comisiones FPF**: brecha confirmada |
| El BCRP no publica, en su catálogo mensual, volúmenes de crédito a pyme; sí tiene el IPC (`PN38705PM`, ene-1991 a oct-2026) | Catálogo BCRPData | No se compara la escala con el BCRP; el IPC permite deflactar (**confirmado por API el 2026-11-07**: «Índice de precios Lima Metropolitana, índice dic. 2021 = 100») |

---

## 1. Título

- **Español:** Fintech y financiamiento participativo (crowdfunding) en el Perú: oferta y condiciones, 2022-2026
- **Inglés:** Fintech and crowdfunding in Peru: supply and financing terms, 2022-2026

Se conserva literalmente el título del temario y se añade el periodo, para que nadie pueda considerar el trabajo "ajeno al tema asignado" (C3, nivel 0).

---

## 2. Identificación y formulación del problema

**Situación observada.** Desde el Decreto de Urgencia N.º 013-2020 y su reglamento (Resolución SMV N.º 045-2021-SMV/02), el financiamiento participativo financiero (FPF) es una actividad regulada y supervisada por la SMV. Solo pueden ejercerla sociedades administradoras autorizadas. Entre 2022 y 2026 hubo **seis** sociedades administradoras con información financiera ante la SMV; en 2026 solo **tres** figuran como vigentes (verificado en OData y SIMV). En noviembre de 2025 la Resolución SMV N.º 019-2025-SMV/01 modificó el reglamento: ampliaron los límites de financiamiento y cambiaron otras condiciones (el texto oficial se verificará al redactar).

Mientras tanto, el crédito tradicional a la pequeña y microempresa tiene costos efectivos altos. En enero de 2021 la TEA promedio en MN para préstamos pyme de hasta 360 días era de **31,1 %** en bancos, **33,7 %** en cajas municipales y **41,4 %** en cajas rurales; en consumo bancario de hasta 360 días era de **53,6 %** (BCRPData, verificado). Esto justifica preguntarse si el FPF constituye una oferta alternativa y en qué condiciones.

**Problema de conocimiento.** La información pública sobre el FPF peruano está dispersa: hay agregados anuales citados por la prensa y formularios por plataforma y mes en el SIMV. No se ha encontrado una caracterización sistemática, construida con datos oficiales reproducibles, que describa la oferta (plataformas, proyectos, montos, concentración, solidez de las administradoras) ni que la sitúe frente a las condiciones del crédito tradicional en segmentos comparables. **[La ausencia de estudios se comprobará en la Fase II-B; hasta entonces es una hipótesis de trabajo.]**

**Formulación.** ¿Cómo se caracteriza la oferta de FPF en el Perú entre 2022 y 2026 y cómo se comparan sus condiciones observables con las del sistema crediticio tradicional?

---

## 3. Preguntas de investigación

**Pregunta general (PG).** ¿Cómo se caracteriza la oferta de financiamiento participativo financiero en el Perú entre 2022 y 2026, y cómo se comparan sus condiciones observables con las del sistema crediticio tradicional?

| ID | Pregunta específica | Fuente principal |
|---|---|---|
| PE1 | ¿Cómo evolucionaron el número de plataformas activas, los proyectos publicados y financiados y el monto financiado, y qué tan concentrada está la oferta entre plataformas? | SMV-SIMV |
| PE2 | ¿Qué tamaño, ingresos, rentabilidad y solvencia tienen las sociedades administradoras que conforman la oferta? | SMV-OData |
| PE3 | ¿Qué condiciones de acceso y de monto presenta el FPF (tasa de colocación, monto promedio por proyecto) según el tipo de receptor, y cambiaron tras la modificación regulatoria de noviembre de 2025? | SMV-SIMV |
| PE4 | ¿Cómo se sitúan esas condiciones frente a las del crédito tradicional en los segmentos comparables (pyme y consumo, MN, hasta 360 días), dados los límites de comparabilidad? | BCRP + SMV-SIMV + SMV-OData |

## 4. Objetivos

**Objetivo general (OG).** Caracterizar la oferta de financiamiento participativo financiero en el Perú entre 2022 y 2026 y comparar sus condiciones observables con las del sistema crediticio tradicional. *(Reproduce el objetivo del temario, con el periodo explícito.)*

| ID | Objetivo específico | Responde a |
|---|---|---|
| OE1 | Describir la evolución y la estructura de la oferta de FPF: plataformas, proyectos, montos, tipo de receptor y concentración | PE1 |
| OE2 | Caracterizar la situación financiera de las sociedades administradoras y estimar su costo de intermediación implícito | PE2 |
| OE3 | Medir las condiciones de acceso y de monto del FPF por tipo de receptor y contrastarlas antes y después de la reforma de 2025 | PE3 |
| OE4 | Comparar las condiciones del FPF con las del crédito tradicional en segmentos equivalentes y cuantificar, mediante simulación, escenarios de costo para el receptor | PE4 |

---

## 5. Justificación

- **Teórica.** El FPF es un caso de intermediación sin balance: la plataforma conecta inversionistas y receptores sin asumir el riesgo crediticio. Contrastar su oferta con la de los intermediarios tradicionales permite discutir, con evidencia local, los enfoques sobre asimetría de información, racionamiento del crédito y complementariedad o sustitución entre fintech y banca. *(Las referencias teóricas se fijarán en la Fase II-B.)*
- **Económica.** El costo del crédito pyme y de consumo en el Perú es elevado (verificado en BCRP). Saber si el FPF amplía la oferta, a quién atiende y con qué escala es relevante para el emprendedor, para el inversionista y para el regulador, sobre todo después de la reforma de 2025.
- **Metodológica.** Se construye por primera vez, para este tema, una base **oficial y reproducible**: API (BCRPData y SMV-OData) y *scraping* de formularios ASP.NET de la SMV. Incluye hash, log HTTP y pruebas automatizadas. Así, la evidencia sobre el FPF deja de depender de cifras sueltas citadas en prensa.

---

## 6. Marco conceptual (definiciones operativas)

| Concepto | Definición que usará el estudio |
|---|---|
| Financiamiento participativo financiero (FPF) | Actividad regulada por la SMV en la que, mediante una plataforma, se pone en contacto a personas que buscan financiamiento (receptores) con inversionistas, bajo la modalidad de **préstamos** o de **valores**. Se excluye el crowdfunding de **donación** o de **recompensa**, que no es FPF ni lo supervisa la SMV |
| Sociedad administradora (SAPFPF) | Sociedad anónima autorizada por la SMV para gestionar la plataforma; es la unidad de la **oferta** |
| Proyecto empresarial / personal | Clasificación del SIMV según el receptor sea persona jurídica o persona natural con fines empresariales, o persona natural con fines personales **[confirmar la definición en el Reglamento]** |
| Proyecto publicado / financiado | Lo que la SMV registra por plataforma y mes en el SIMV |
| Oferta de FPF | Capacidad y actividad de colocación de las plataformas autorizadas: número de plataformas activas, proyectos y montos financiados, concentración y solidez de las administradoras |
| Condiciones observables del FPF | Acceso (tasa de colocación), escala (monto promedio por proyecto), tipo de receptor, costo de intermediación implícito y límites normativos. **No incluyen** la tasa ni el plazo por operación (no publicados) |
| Sistema crediticio tradicional | Bancos, cajas municipales (CMAC) y cajas rurales (CRAC) supervisados por la SBS, según las tasas promedio que publica el BCRP |
| TEA | Tasa efectiva anual: $(1+i_m)^{12}-1$ |
| TEM | Tasa efectiva mensual equivalente: $(1+TEA)^{1/12}-1$ |
| Tasa nominal (TNA) | $TNA = m \cdot i_m$; no se confunde con la TEA |
| TCEA | Costo efectivo anual con comisiones y seguros. **No se calculará** para el FPF ni para la banca, porque faltan esos costos |

---

## 7. Antecedentes académicos: plan para la Fase II-B

No se cita ningún trabajo sin verificarlo. En la siguiente etapa se hará:

1. **Ventana:** 2023-2026 (**confirmada por el docente**; las normas y las fuentes de datos no cuentan en el estado del arte).
2. **Líneas de búsqueda:** (a) préstamos P2P o *marketplace lending* frente a la banca (sustitución o complementariedad, selección de prestatarios); (b) crowdfunding y acceso al financiamiento de pymes; (c) fintech en América Latina y economías emergentes; (d) regulación del crowdfunding; (e) costos y precios del crédito fintech frente al bancario; (f) estudios sobre el Perú (SMV, BCRP, universidades).
3. **Verificación:** DOI, autores, año y título con la API de Crossref u OpenAlex; cuartil en SJR (Scopus) e indexación en la Master Journal List (WoS). Se registra todo en una tabla de verificación.
4. **Doble uso:** los 20 artículos Q1/Q2 exigidos en la Carpeta N.º 1 se elegirán dentro del mismo estado del arte, para que también sean referencias citadas.

---

## 8. Hipótesis

El estudio es **descriptivo y comparativo**. Solo se formulan hipótesis donde los datos permiten un contraste:

| ID | Hipótesis | Contraste | Advertencia |
|---|---|---|---|
| H1 | El monto mensual financiado mediante FPF es mayor después de la modificación del reglamento (dic-2025 a sep-2026) que antes (jun-2022 a nov-2025) | U de Mann-Whitney e IC bootstrap de la diferencia de medianas | Comparación antes y después, **no causal**: coincide con una tendencia previa y con otros factores |
| H2 | La tasa de colocación (financiados ÷ publicados) difiere entre proyectos empresariales y personales | Prueba de dos proporciones e IC de Wilson | Los proyectos no son independientes entre plataformas; resultado descriptivo |
| E1 *(exploratoria, sin hipótesis)* | ¿Se asocian los cambios mensuales del monto FPF con los cambios de la TEA pyme tradicional? | Spearman sobre primeras diferencias, con IC por bootstrap de bloques | Pocos datos y tendencias comunes; **nunca se interpretará como causalidad** |

---

## 9. Operacionalización de variables

### 9.1 Variables observadas (entran a `datos_procesados`)

| Variable (nombre normalizado) | Dimensión | Definición operacional | Unidad | Escala | Fuente / endpoint | Frecuencia |
|---|---|---|---|---|---|---|
| `periodo` | Llave | Año-mes (AAAA-MM) | — | Fecha | Todas | Mensual |
| `ruc`, `plataforma` | Llave | RUC y razón social de la SAPFPF | — | Nominal | SMV-OData (RUC); SIMV (nombre) | — |
| `estado_registro` | Control | `no_autorizada` / `sin_registro` / `reportado` | — | Nominal | Derivado del SIMV y del OData | Mensual |
| `proy_publicados_emp`, `proy_publicados_per` | Oferta | Proyectos publicados en el mes (empresariales / personales) | proyectos | Razón | SMV-SIMV `Frm_ProyectosFPF` | Mensual |
| `proy_financiados_emp`, `proy_financiados_per` | Oferta | Proyectos financiados en el mes | proyectos | Razón | SMV-SIMV | Mensual |
| `monto_financiado_emp`, `monto_financiado_per` | Oferta | Monto total financiado en el mes | S/ corrientes | Razón | SMV-SIMV | Mensual |
| `activo_total`, `pasivo_total`, `patrimonio_total` | Solidez | Saldo al cierre del trimestre | miles de S/ | Razón | SMV-OData `PrincipalCuentaSMV` | Trimestral |
| `ingresos_totales`, `utilidad_neta` | Desempeño | Flujo del periodo. **Evidencia preliminar (2026-11-07): NO es acumulado del año** (los valores bajan dentro de un mismo año, p. ej., Inversiones.io 2023: 168, 352, 213, 203); confirmar con el diccionario de datos de la SMV | miles de S/ | Razón | SMV-OData | Trimestral |
| `tea_bcos_pyme_360` | Tradicional | Bancos, MN, pequeña y microempresa, préstamos ≤360 d | % TEA | Razón | BCRP `PN07843NM` | Mensual |
| `tea_bcos_pyme_mas360` | Tradicional | Ídem, >360 d | % TEA | Razón | BCRP `PN07844NM` | Mensual |
| `tea_cmac_pyme_360` / `_mas360` | Tradicional | CMAC, MN, pyme ≤360 / >360 d | % TEA | Razón | BCRP `PN07861NM` / `PN07862NM` | Mensual |
| `tea_crac_pyme_360` / `_mas360` | Tradicional | CRAC, MN, pyme ≤360 / >360 d | % TEA | Razón | BCRP `PN07879NM` / `PN07880NM` | Mensual |
| `tea_bcos_consumo_360` / `_mas360` | Tradicional | Bancos, MN, consumo ≤360 / >360 d | % TEA | Razón | BCRP `PN07846NM` / `PN07847NM` | Mensual |
| `tamn` | Tradicional | Tasa activa promedio en MN | % TEA | Razón | BCRP `PN07807NM` | Mensual |
| `ipc` *(opcional)* | Deflactor | Índice de precios al consumidor | índice | Razón | BCRP `PN38705PM` (confirmado por API; dic. 2021 = 100) | Mensual |

**Fuentes que aportan columnas sustantivas:** SIMV (6 columnas), OData (5), BCRP (9 o 10). Se cumple el 2.4.1: 6 columnas o más, 4 sustantivas o más y al menos 1 por fuente.

### 9.2 Indicadores derivados (se calculan en `04_analisis.py` y van a `/salidas`, **no** a `datos_procesados`)

| Indicador | Fórmula | Objetivo |
|---|---|---|
| Plataformas activas | N.º de plataformas con `monto_financiado > 0` en el mes | OE1 |
| Monto total y móvil de 12 meses | $\sum_i monto_{i,t}$; $\sum_{k=0}^{11} M_{t-k}$ | OE1 |
| Variación interanual | $M^{12}_t / M^{12}_{t-12} - 1$ | OE1 |
| Participación e HHI | $s_{i,t}=monto_{i,t}/M_t$; $HHI_t=\sum_i (100\,s_{i,t})^2$ | OE1 |
| Tasa de colocación | $\text{financiados}/\text{publicados}$ por tipo, **sobre sumas anuales o móviles de 12 meses**: en 16 plataforma-mes los financiados superan a los publicados, porque un proyecto puede financiarse en un mes posterior al de su publicación (hallazgo de la Fase IV) | OE3, H2 |
| Monto promedio por proyecto | $\text{monto}/\text{financiados}$ por tipo | OE3, OE4 |
| Ingresos trimestrales desacumulados | $I_q - I_{q-1}$ dentro del ejercicio (si son acumulados) | OE2 |
| Costo de intermediación implícito | $\text{ingresos trimestrales}_{i} \times 1000 / \sum_{t\in q} monto_{i,t}$ | OE2, OE4 |
| ROA, apalancamiento | utilidad/activo; pasivo/patrimonio | OE2 |
| Brecha entre segmentos tradicionales | p. ej., $TEA_{CRAC} - TEA_{bancos}$ | OE4 |

> **Principio de verificabilidad:** `datos_procesados` contiene **solo valores que existen en la fuente** (renombrados, tipificados y con la unidad documentada). Así, cualquier fila elegida al azar por el docente (Bloque A-1) puede cotejarse en vivo. Los indicadores construidos viven en `/salidas` y se regeneran con `04_analisis.py`.

---

## 10. Unidad de análisis, población y muestra

| Elemento | Definición |
|---|---|
| Unidad de análisis principal | **Plataforma-mes** (SAPFPF *i*, mes *t*) |
| Unidades auxiliares | Plataforma-trimestre (estados financieros); sistema-mes (tasas del BCRP) |
| Población | Todas las sociedades administradoras con información en la SMV entre 2022 y 2026: **6** (3 vigentes y 3 retiradas). Crédito tradicional: bancos, CMAC y CRAC según los promedios del BCRP |
| Muestra | **No hay muestreo:** censo de las plataformas con datos publicados |
| Base procesada | Panel balanceado de 6 plataformas × 69 meses (2021-01 a 2026-09) = **414 filas**, con `estado_registro` para distinguir los meses sin actividad. (**formato aceptado por el docente**, 2026-11-07) |

---

## 11. Periodo de estudio

| Parámetro | Valor propuesto | Justificación |
|---|---|---|
| `FECHA_INICIO` | **2021-01** | Año de publicación del reglamento FPF (mayo de 2021); da 69 periodos mensuales, por encima del mínimo de 60 del 2.4.1, y coincide con el "panel 2021-2025" del temario |
| `FECHA_CORTE` | **2026-09** | Último mes publicado en el SIMV (oct-2026 aún sin registros); el BCRP tiene datos hasta sep/oct-2026 |
| Ventana efectiva del FPF | jun-2022 a sep-2026 (~52 meses) | Primeros registros verificados del SIMV **[delimitar con el censo de la Fase III]** |
| Corte regulatorio | nov-2025 / dic-2025 | Resolución SMV N.º 019-2025-SMV/01; se prueban ambos cortes como sensibilidad |

**Riesgo explícito:** el FPF tiene menos de 60 meses de datos porque la actividad empezó a mediados de 2022. Se cumple el mínimo por la **dimensión temporal de la base** (69 periodos), no por la del FPF. Se documenta en el artículo; **el docente aceptó este formato el 2026-11-07**.

---

## 12. Estrategia de comparación financiera

### 12.1 Emparejamiento de segmentos

| FPF (SIMV) | Comparador tradicional principal | Sensibilidad |
|---|---|---|
| Proyectos **empresariales** (préstamos) | TEA pyme MN ≤360 d: bancos (`PN07843NM`), CMAC (`PN07861NM`), CRAC (`PN07879NM`) | Los mismos segmentos a >360 d |
| Proyectos **personales** (préstamos) | TEA consumo MN ≤360 d, bancos (`PN07846NM`) | Consumo >360 d (`PN07847NM`) |

*Por qué ≤360 d como base:* es la referencia de plazo más cercana a préstamos de corta duración. Se justificará en la redacción con la normativa y con la literatura, no con cifras de prensa; la prueba con >360 d cubre el error de esta elección.

### 12.2 Matriz de comparabilidad (se publicará como tabla del artículo)

| Dimensión | FPF | Crédito tradicional (BCRP) | ¿Comparable? |
|---|---|---|---|
| Moneda | Soles (SIMV en S/) | MN | Sí |
| Plazo | No publicado por operación | Tramos ≤360 / >360 d | Parcial: supuesto declarado |
| Precio (tasa) | **No observado** | TEA promedio | **No:** se usan escenarios del simulador |
| Costos adicionales | Ingreso de la plataforma ÷ monto (aproximación) | Comisiones no incluidas en la TEA | Parcial; no se calcula TCEA |
| Riesgo del prestatario | No observado (selección de la plataforma) | Promedio de toda la cartera | No: se advierte |
| Garantías | No observadas | No observadas | No |
| Regulador | SMV | SBS | Diferencia institucional que se discute |

### 12.3 Qué se compara y qué no

- **Se compara:** el nivel y la evolución de las condiciones tradicionales (BCRP) frente a la evolución de la oferta y del acceso del FPF; el monto promedio por proyecto del FPF frente a los límites normativos; el costo de intermediación implícito de las plataformas frente a las brechas entre segmentos tradicionales.
- **Se simula (Fase VII):** para un préstamo de monto *P* y plazo *n*, la cuota $C = P\,\dfrac{i(1+i)^n}{(1+i)^n-1}$ y el costo total con la TEM tradicional observada, frente a escenarios FPF **hipotéticos** que introduce el usuario. También se calcula la **tasa de indiferencia**, a la que el FPF iguala el costo tradicional. Cada escenario se etiquetará como *hipotético*.
- **No se afirma:** que el FPF sea "más barato" o "más caro", porque falta su tasa oficial.

---

## 13. Métodos estadísticos por objetivo

| Objetivo | Método | Salida prevista | Fuentes que participan |
|---|---|---|---|
| OE1 | Estadística descriptiva (totales, mediana, RIC), variación interanual con sumas móviles, participaciones e HHI | **F1** monto mensual por plataforma (con la línea de la reforma); **F2** publicados frente a financiados; **F3** HHI y participación del líder; **T1** plataformas y periodos de actividad; **T2** descriptivos por año y tipo | SIMV (+ OData en T1) |
| OE2 | Ratios financieros con ingresos desacumulados; costo de intermediación implícito | **T3** indicadores por plataforma-año; **F4** costo implícito por trimestre | OData + SIMV |
| OE3 | Tasa de colocación con IC de Wilson; H2 (dos proporciones); H1 (Mann-Whitney e IC bootstrap, B = 10 000) | **T4** condiciones por tipo de receptor; **T5** contrastes H1 y H2 | SIMV |
| OE4 | Descriptivos de la TEA por segmento y periodo; brechas; E1 (Spearman en diferencias, bootstrap de bloques); escenarios del simulador | **F5** TEA tradicional por segmento; **T6** matriz de comparabilidad; **T7** comparación por segmento; **F6** escenarios de costo (hipotéticos) | BCRP + SIMV + OData |
| Robustez | Corte nov frente a dic de 2025; excluir a la plataforma líder; ≤360 frente a >360 d; valores nominales frente a reales (IPC); "sin registro" como faltante frente a 0 | **T8** sensibilidad | Todas |

- **Semilla:** `0481`, los cuatro últimos dígitos de la matrícula 2024200481M (2.4.4), para todo bootstrap.
- **Lo que no se hará:** regresiones de panel, modelos predictivos ni *machine learning*. Con 6 plataformas y unos 52 meses de FPF, no aportarían evidencia válida.
- **Cada fuente participa en al menos un resultado:** SIMV → F1, F2, F3, T2, T4, T5; OData → T1, T3, F4; BCRP → F5, T7. No hay fuentes decorativas.

---

## 14. Matriz de consistencia (resumen)

| Problema | Objetivo | Hipótesis | Variables | Método | Resultado |
|---|---|---|---|---|---|
| ¿Cómo es la oferta de FPF? | OE1 | — | Proyectos y montos (SIMV) | Descriptivo, HHI | F1-F3, T1-T2 |
| ¿Qué solidez tienen las plataformas? | OE2 | — | EEFF (OData) | Ratios | T3, F4 |
| ¿Qué condiciones de acceso y monto ofrece? ¿Cambió con la reforma? | OE3 | H1, H2 | Proyectos y montos por tipo | Mann-Whitney, proporciones, bootstrap | T4-T5 |
| ¿Cómo se comparan con el crédito tradicional? | OE4 | E1 (exploratoria) | TEA BCRP + SIMV + OData | Descriptivo, Spearman, simulación | F5-F6, T6-T7 |

---

## 15. Limitaciones

1. **No hay tasa ni plazo oficiales por operación FPF:** la comparación de precios se limita a escenarios y aproximaciones.
2. **Pocas unidades:** 6 plataformas y 2 a 4 activas a la vez. La plataforma líder domina; se hace sensibilidad sin ella.
3. **Ventana corta del FPF:** unos 52 meses, y menos de 12 después de la reforma.
4. **Datos agregados:** no se observa el riesgo, el sector ni las garantías del receptor.
5. **Comparadores tradicionales promedio:** mezclan prestatarios heterogéneos; no son el costo de un prestatario equivalente.
6. **Fuentes vivas:** posibles revisiones; se mitiga congelando FECHA_CORTE, con hash y con log.
7. **Asociación no es causalidad:** H1 y E1 se interpretan solo como evidencia descriptiva.

## 16. Consideraciones éticas

- Solo datos **públicos y agregados**: no hay nombres de receptores ni de inversionistas (Ley N.º 29733).
- Se respetan robots.txt y términos de uso, con pausas de 3 s o más (10 s en Datos Abiertos), User-Agent identificable y **ninguna evasión** de protecciones anti-bot (SBS y REF-BCRP quedan descartados por eso).
- Los crudos no se editan; las cifras de prensa no entran a la base.
- Las fuentes de datos se citan en APA 7 con fecha de consulta y endpoint.
- Habrá una declaración de uso de IA en el artículo y en el README, y las incidencias de los sondeos de la Fase I quedan registradas.

---

## 17. Implicaciones para la Fase III (especificación preliminar)

1. `01_extraccion_api.py`: BCRPData (9 series + IPC) y SMV-OData (ejercicios 2021-2026, periodos 1-4). Guarda el JSON crudo y valida `config` y `data`.
2. `02_scraping_web.py`: SIMV `Frm_ProyectosFPF`, con 6 plataformas × meses de 2021-01 a 2026-09. Para las retiradas, primero marca la casilla con su postback y después busca. Valida la tabla `MainContent_grdTodos` antes de guardar. Pausa de 3 s. Unas 400 consultas, que se ejecutan una sola vez con caché; la demo en vivo usa 1 o 2 consultas.
3. `03_limpieza_datos.py`: correspondencia nombre→RUC usando el propio OData; panel de 414 filas; `estado_registro`; asignación del trimestre al mes de cierre.
4. Pruebas: HTML y JSON guardados como *fixtures*; Pandera para el esquema del panel.

## 18. Puntos que se suman a la consulta al docente

Al borrador del Anexo A de la Fase I se recomienda **reemplazar el punto 3** por este texto:

> 3. **Periodo y tamaño.** El SIMV de la SMV muestra registros de proyectos FPF desde junio de 2022, de modo que la actividad tiene unos 52 meses al corte de septiembre de 2026. Propongo una base mensual en panel (6 plataformas × 69 meses, de enero de 2021 a septiembre de 2026). Las tasas del sistema tradicional (BCRP) cubren todo el periodo; los datos FPF cubren desde su primer registro. ¿Acepta este formato para cumplir el mínimo de 60 periodos mensuales?
