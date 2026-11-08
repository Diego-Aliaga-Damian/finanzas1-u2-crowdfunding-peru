# Fase II-B — Antecedentes académicos y estado del arte

**Tema N.º 96** · **Fecha de búsqueda y verificación:** 2026-11-07 · **Versión:** 1.0
**Numerales aplicables:** 2.2 (6) "Antecedentes o desarrollo" y (11) "Referencias bibliográficas: mínimo 20, en APA 7.ª ed."; 2.5 "estado del arte de 4 años" y Carpeta N.º 1: "Artículos en inglés de journals Q1 y Q2, Scopus y WoS: […] 20 en la Unidad II"; C2 nivel 1: "menos de 20 referencias o estado del arte fuera del rango de 4 años".

> **Qué está verificado y qué no.** Cada DOI de este documento **resuelve en Crossref**, y su título coincide con OpenAlex en los 45 casos. Los hallazgos resumidos proceden **solo de resúmenes oficiales** (OpenAlex). Cuando no hubo resumen se indica **"pendiente de lectura"**. **El cuartil SJR y la indexación en WoS NO están verificados**: Scimago restringe el acceso automatizado, así que debes comprobarlos tú (sección 6). Leer los textos completos sigue siendo tarea tuya: la defensa oral puede preguntar por cualquier autor citado.

---

## 1. Protocolo de búsqueda (reproducible)

| Paso | Detalle | Resultado |
|---|---|---|
| Bases | OpenAlex (búsqueda), Crossref (verificación del DOI, autores, año, revista, ISSN), Semantic Scholar (resúmenes faltantes) | — |
| Scripts | `herramientas/literatura/01_buscar_openalex.py` … `04_completar_resumenes.py` (respuestas crudas en `herramientas/literatura/crudos/`) | Reproducibles |
| Filtros | `publication_year:2022-2026`, `type:article`, `language:en`; 2.ª pasada solo con revistas del núcleo científico (`is_core:true`) | — |
| Líneas | (a) fintech/P2P frente a la banca · (b) crowdfunding y fintech para pymes · (c) América Latina y emergentes · (d) regulación · (e) precios, riesgo y plataformas · (f) Perú | 23 consultas |
| Identificación | 1.ª pasada: 143 registros únicos con DOI; 2.ª pasada (núcleo): 257 registros de 178 revistas | 400 |
| Cribado por título y pertinencia | Se excluyen las aplicaciones de *machine learning* sin componente financiero, el crowdfunding de donación, recompensa o arte, cripto/blockchain y las revistas fuera del núcleo | **45** preseleccionados |
| Elegibilidad | Verificación en Crossref: **45/45** con DOI válido y título coincidente; Crossref corrige el año en varios casos | 45 |
| Inclusión | **Núcleo: 20** (2023-2026, inglés, revista del núcleo) · **Reserva: 18** (2023-2026) · **5 de 2022** (fuera de la ventana estricta) · **2 de contexto peruano** | — |

**Ventana confirmada por el docente (2026-11-07): 2023-2026.** Las normas y las fuentes de datos no cuentan en el estado del arte. Los artículos de 2022 quedan fuera del estado del arte.

---

## 2. Núcleo de 20 artículos (candidatos para la Carpeta N.º 1 y para el estado del arte)

Abreviaturas de los objetivos: OE1 oferta · OE2 plataformas · OE3 acceso y reforma · OE4 comparación con la banca. **AA** = acceso abierto según OpenAlex.

| # | Referencia (datos de Crossref; formato APA final con biblatex-apa) | Línea | Hallazgo (según el resumen) | Aporte al estudio | AA |
|---|---|---|---|---|---|
| 1 | Braggion, F., Manconi, A., Pavanini, N., & Zhu, H. (2025). The value of financial intermediation: Evidence from online debt crowdfunding. *Journal of Financial Economics, 172*, 104113. https://doi.org/10.1016/j.jfineco.2025.104113 | b | Las plataformas de deuda que dejan el esquema P2P puro y adoptan rasgos de intermediario elevan el excedente del prestamista, el beneficio de la plataforma y el crédito otorgado, pero exponen al inversionista a riesgo de liquidez | Marco de la plataforma como intermediario (OE1, OE2) | híbrido |
| 2 | Ghasemi, E., Vafai, N., & Sheikh-Zadeh, A. (2024). Overcharged or fair play? Exploring interest rates and profitability in debt-based crowdfunding. *Journal of Business Venturing Insights, 22*, e00508. https://doi.org/10.1016/j.jbvi.2024.e00508 | e | **Pendiente de lectura** (resumen no disponible por API) | Tasas y rentabilidad del crowdfunding de deuda (OE4) | cerrado |
| 3 | Kim, J.-H., & Stähler, F. (2026). The impact of peer-to-peer lending on small business loans. *Journal of Economics and Business, 141*, 106307. https://doi.org/10.1016/j.jeconbus.2026.106307 | a | Modelo: el prestatario elige entre banco y plataforma; la entrada genera un efecto de sustitución y otro de expansión. Con la entrada escalonada de LendingClub (2009-2017), cayeron los préstamos bancarios a pequeñas empresas, sobre todo en zonas de ingreso bajo | Sustitución frente a complemento (OE4) | híbrido |
| 4 | Serfes, K., Wu, K., & Avramidis, P. (2025). FinTech vs. bank: The impact of lending technology on credit market competition. *Journal of Banking & Finance, 170*, 107338. https://doi.org/10.1016/j.jbankfin.2024.107338 | a | Las fintech ofrecen sobre todo crédito sin garantía a proyectos de **corto plazo**, y la banca crédito con garantía a proyectos de largo plazo; el mercado se segmenta según la tecnología de evaluación y el colateral | **Sustenta el comparador ≤360 d** (OE4) | híbrido |
| 5 | Chu, Y., & Wei, J. (2024). Fintech lending and credit market competition. *Journal of Financial and Quantitative Analysis, 59*(5), 2199-2225. https://doi.org/10.1017/s0022109023000698 | a | El crédito fintech reduce en promedio las tasas esperadas, pero puede empeorar el acceso de los buenos prestatarios y la eficiencia asignativa | Precio y acceso (OE4) | cerrado |
| 6 | Vives, X., & Ye, Z. (2025). Fintech entry, lending market competition, and welfare. *Journal of Financial Economics, 168*, 104040. https://doi.org/10.1016/j.jfineco.2025.104040 | a | Las fintech entran por su flexibilidad de precios; **más concentración bancaria implica más volumen fintech**; la tasa fintech es mayor o menor que la bancaria según su costo de fondeo y la conveniencia que ofrecen | Sustenta E1 y la ambigüedad del precio (OE4) | híbrido |
| 7 | Eid, N., Yang, J., & Duygun, M. (2024). Bridging the credit gap: The influence of regional bank structure on the expansion of peer-to-peer lending. *The British Accounting Review, 56*(6), 101448. https://doi.org/10.1016/j.bar.2024.101448 | a | El P2P crece más donde la banca atiende menos (estimación IV) y se asocia con menor riesgo de impago | Complementariedad territorial (OE1, OE4) | híbrido |
| 8 | Beaumont, P., Tang, H., & Vansteenberghe, E. (2026). Collateral effects: The role of FinTech in small business lending. *The Review of Financial Studies, 39*(7), 2064-2114. https://doi.org/10.1093/rfs/hhaf080 | b | En Francia, tras recibir un préstamo fintech, el crédito bancario de la empresa aumenta un 13 %, porque los activos financiados sirven de colateral | Complementariedad (OE4) | híbrido |
| 9 | Ben Naceur, S., Candelon, B., Elekdag, S., & Emrullahu, D. (2026). Is FinTech eating the bank's lunch? *Journal of International Financial Management & Accounting, 37*(1), 225-246. https://doi.org/10.1111/jifm.12242 **[Crossref registra "Naceur, Sami Ben": verificar el apellido en el PDF]** | a | Con más de 10 000 instituciones de 57 países: la presencia fintech reduce la rentabilidad de las instituciones tradicionales (hipótesis de sustitución); los modelos P2P y de balance tienen efectos distintos | Sustitución en el plano internacional (OE4) | bronce |
| 10 | Onorato, G., Pampurini, F., & Quaranta, A. G. (2024). Lending activity efficiency. A comparison between fintech firms and the banking sector. *Research in International Business and Finance, 68*, 102185. https://doi.org/10.1016/j.ribaf.2023.102185 | a | En Italia (2021), los bancos son más eficientes que las fintech de crédito (SDEA) | Desempeño de las plataformas (OE2) | híbrido |
| 11 | Pampurini, F., Pezzola, A., & Quaranta, A. G. (2024). Lending business models and FinTechs efficiency. *Finance Research Letters, 65*, 105519. https://doi.org/10.1016/j.frl.2024.105519 | e | La eficiencia de las fintech de crédito depende sobre todo del ROA y del ratio costo/ingreso | **Sustenta los indicadores de OE2** (ROA) | híbrido |
| 12 | Fasano, M., Nania, I., & Staglianò, R. (2026). Predicting repayment delays in Italian real estate crowdfunding: Evidence from a machine learning approach. *Journal of Economics and Business*, 106343. https://doi.org/10.1016/j.jeconbus.2026.106343 *(publicación anticipada, sin volumen)* | e | Con datos por proyecto de una plataforma italiana de préstamos inmobiliarios, predice los retrasos de pago desde la teoría de la selección adversa y la señalización | Riesgo en el crowdfunding inmobiliario (contexto peruano, OE3) | híbrido |
| 13 | Ran, Z., Rau, P. R., & Ziegler, T. (2025). Sometimes, always, never: Regulatory clarity and the development of digital financing. *Management Science, 71*(9), 8027-8071. https://doi.org/10.1287/mnsc.2023.01538 | d | Las regulaciones claras y explícitas **aumentan el volumen de crowdfunding de deuda** y la creación de **nuevas plataformas**, con poco efecto en el de capital (diferencias en diferencias, muestra global) | **Sustenta H1** y la entrada y salida de plataformas (OE1, OE3) | verde |
| 14 | Lazos, A. (2025). When policy makers want to protect investors in equity crowdfunding: Does it have regional implications? *Technological Forecasting and Social Change, 215*, 124119. https://doi.org/10.1016/j.techfore.2025.124119 | d | En el Reino Unido, los topes de inversión para no acreditados aumentan la probabilidad de financiar empresas de regiones desfavorecidas | Efectos de los límites normativos (OE3) | híbrido |
| 15 | Danisewicz, P., & Elard, I. (2023). The real effects of financial technology: Marketplace lending and personal bankruptcy. *Journal of Banking & Finance, 155*, 106986. https://doi.org/10.1016/j.jbankfin.2023.106986 | a | Un fallo judicial sobre préstamos por encima del límite de usura redujo el crédito de *marketplace* y aumentó las quiebras personales en hogares de bajos ingresos | Acceso del segmento personal y reglas de precio (OE3, OE4) | híbrido |
| 16 | Fareed, F., & Viotto, J. (2025). Crowdfunding platforms and financial inclusion: Fulfilled promise or disillusion? *Finance Research Letters, 73*, 106642. https://doi.org/10.1016/j.frl.2024.106642 | b | En países en desarrollo, las plataformas amplían el acceso a más prestatarios, pero no mejoran la atención a los más vulnerables y **las tasas no cambian** | Acceso frente a precio (OE3, OE4) | híbrido |
| 17 | Larios-Hernandez, G. J. (2025). Facilitating new financial services in Latin America: An exploratory analysis of the sandbox model. *Journal of Small Business & Entrepreneurship, 37*(3), 439-465. https://doi.org/10.1080/08276331.2024.2389505 | c | Los *sandboxes* latinoamericanos siguen un enfoque fragmentado y gradual, centrado en pagos, inversión y **crédito** | Contexto regulatorio regional | cerrado |
| 18 | Alvarez-Franco, P. B., Castañeda, V. C., Agudelo Zuluaga, D. I., & Diaz, J. M. (2026). Determinants of digital financial inclusion in Latin America and the Caribbean. *Journal of Economics, Finance and Administrative Science, 31*(62), 210-227. https://doi.org/10.1108/jefas-09-2024-0280 | c | Con el Global Findex 2021 (15 países, modelo probit): la edad, la educación, el género y el ingreso determinan la inclusión financiera digital | Contexto de la demanda en ALC (revista de la U. ESAN, Perú) | diamante |
| 19 | Miglo, A. (2025). Crowdfunding, asymmetric information and pecking order. *Journal of Economic Studies, 52*(6), 1156-1170. https://doi.org/10.1108/jes-03-2024-0194 | b | Teoría: con información asimétrica, el crowdfunding suele quedar **al final del orden jerárquico** de financiamiento, lo que explica sus volúmenes pequeños frente al tradicional *(modelo de crowdfunding de recompensa)* | Marco teórico (justificación) | verde |
| 20 | Ma, Q., Xu, L., Anwar, S., & Lu, Z. (2023). Banking competition and the use of shadow credit: Evidence from lending marketplaces. *Global Finance Journal, 58*, 100884. https://doi.org/10.1016/j.gfj.2023.100884 | a | En China, quienes vienen de mercados bancarios concentrados y usan *marketplaces* tienen mejor calidad crediticia: los prestatarios migran cuando la banca está concentrada | Sustitución condicionada a la estructura bancaria (OE4) | híbrido |

**Revistas distintas en el núcleo:** 16. **Acceso abierto:** 17 de 20 tienen una versión abierta según OpenAlex (híbrido, verde, bronce o diamante); 3 están cerradas (n.º 2, 5 y 17). Las cerradas se obtienen por la biblioteca de la UNCP o por la versión del autor.

---

## 3. Síntesis del estado del arte (base para la sección "Antecedentes" del artículo)

1. **¿Sustituto o complemento de la banca?** La evidencia está dividida y depende del contexto. Kim y Stähler (2026) y Ben Naceur et al. (2026) encuentran **sustitución**: menos crédito bancario a pequeñas empresas y menor rentabilidad de las instituciones tradicionales. Beaumont et al. (2026) y Eid et al. (2024) encuentran **complementariedad**: el crédito fintech facilita el bancario o cubre zonas desatendidas. Ma et al. (2023) y Vives y Ye (2025) relacionan el uso del crédito alternativo con la **concentración bancaria**.
2. **Precio y segmentación.** La teoría no predice que el crédito fintech o de plataforma sea siempre más barato. Chu y Wei (2024) obtienen tasas esperadas menores; Vives y Ye (2025), tasas mayores o menores según el costo de fondeo y la conveniencia; Fareed y Viotto (2025) no encuentran cambios en las tasas. Serfes et al. (2025) muestran que la fintech se especializa en crédito **sin garantía y de corto plazo**, lo que respalda comparar con el tramo **≤360 días**.
3. **La plataforma como intermediario y su desempeño.** Braggion et al. (2025) explican por qué las plataformas de deuda adoptan rasgos de intermediario. Onorato et al. (2024) y Pampurini et al. (2024) miden la eficiencia de las fintech de crédito con ROA y costos, lo que fundamenta el OE2. Fasano et al. (2026) estudian el riesgo de los préstamos inmobiliarios por plataforma, relevante porque el FPF peruano se orienta al sector inmobiliario (dato de prensa, por confirmar en la literatura).
4. **Regulación.** Ran, Rau y Ziegler (2025) asocian la **claridad regulatoria** con más crowdfunding de deuda y con la entrada de plataformas. Esto fundamenta H1 (la reforma de noviembre de 2025) y el análisis de entrada y salida. Lazos (2025) y Danisewicz y Elard (2023) muestran que los topes y las reglas de precio cambian el acceso. Larios-Hernandez (2025) describe la regulación experimental en América Latina.
5. **Vacío.** Ninguno de los trabajos verificados analiza el FPF **peruano** con datos oficiales de la SMV. La literatura peruana hallada es descriptiva y no está en el núcleo (sección 5). **[Para cerrar este punto: búsqueda complementaria en SciELO, Redalyc y ALICIA-CONCYTEC]**.

**Implicaciones para el diseño:** (i) Serfes et al. respaldan el comparador ≤360 d; (ii) Vives y Ye fundamentan la asociación exploratoria E1; (iii) Ran et al. fundamentan H1; (iv) Pampurini et al. y Onorato et al. fundamentan los indicadores de OE2. Ninguna de estas conclusiones obliga a cambiar el diseño de la Fase II.

---

## 4. Reserva verificada (DOI en Crossref)

**2023-2026:** Kräussl et al. (2024, *J. Banking & Finance*, 10.1016/j.jbankfin.2024.107124) · Kgoroeadira et al. (2023, *J. Int. Financial Markets, Inst. & Money*, 10.1016/j.intfin.2023.101882) · Tian et al. (2023, *China Economic Review*, 10.1016/j.chieco.2023.101944) · Kutzbach y Pogach (2024, *J. Financial Intermediation*, 10.1016/j.jfi.2024.101101) · Cornelli et al. (2024, *J. Financial Stability*, 10.1016/j.jfs.2024.101290) · Tran et al. (2026, *J. Financial Stability*, 10.1016/j.jfs.2026.101541) · Hau et al. (2024, *J. of Finance*, 10.1111/jofi.13384) · Ghosh et al. (2026, *J. of Finance*, 10.1111/jofi.70003) · Adbi y Natarajan (2023, *Strategic Entrepreneurship J.*, 10.1002/sej.1470) · Morello (2025, *Common Market Law Review*, 10.54648/cola2025039) · Tipaldi et al. (2026, *Int. Review of Financial Analysis*, 10.1016/j.irfa.2026.105101) · Wang et al. (2023, *Information Systems Research*, 10.1287/isre.2022.1154) · Li et al. (2024, *Applied Economics*, 10.1080/00036846.2023.2200230) · Luo et al. (2025, *British Accounting Review*, 10.1016/j.bar.2025.101583) · Van Tassel (2023, *Small Business Economics*, 10.1007/s11187-022-00622-9) · Halim (2024, *Research in Globalization*, 10.1016/j.resglo.2024.100238) · Griffiths et al. (2025, *Int. J. of Emerging Markets*, 10.1108/ijoem-04-2024-0678) · Al-Assaf et al. (2025, *Discover Sustainability*, 10.1007/s43621-025-01597-9).

**2022 (fuera de la ventana confirmada; no se usan en el estado del arte):** Bejar et al. (2022, *Latin American J. of Central Banking*, 10.1016/j.latcb.2022.100061, fintech y competencia bancaria en ALC) · Velazquez et al. (2022, *J. Risk and Financial Management*, 10.3390/jrfm15020062, fintech e inclusión en el **Perú**) · Kowalewski y Pisany (2022, *IRFA*, 10.1016/j.irfa.2022.102116) · Stefanelli et al. (2022, *J. Innovation & Knowledge*, 10.1016/j.jik.2022.100278) · Salas Quenta et al. (2022, *Quipukamayoc*, 10.15381/quipu.v30i63.24043, **Perú**).

## 5. Contexto peruano (no entra en las 20; sí puede citarse)

- López Aquise, K. A. (2026). Sandbox regulatorio y fintech en Perú: ¿Innovación financiera o barrera invisible? *Revista e-mercatoria, 25*(2), 247-265. https://doi.org/10.18601/16923960.v25n2.09
- Mejia-Trujillo, S., Hidalgo-Castilla, R. D., Ruiz-Ruiz, M. F., Flores-Perez, A., Quiroz-Flores, J., & Collao-Diaz, M. (2023). Characterization of the Fintech industry for the Peruvian market. *International Journal of Trade, Economics and Finance*, 74-79. https://doi.org/10.18178/ijtef.2023.14.4.759 *(Crossref no registra el volumen; el DOI sugiere 14(4))*

**Cuenta de referencias posibles en la ventana 2023-2026:** 20 del núcleo + 18 de reserva + 2 peruanas = **40 verificadas**. El mínimo de 20 está cubierto con holgura, antes de añadir normas y fuentes de datos.

---

## 6. Verificación de cuartil e indexación (tarea para ti, unos 20 minutos)

Scimago prohíbe en su robots.txt las descargas automatizadas (`Disallow: /*out=xls`) y bloquea a los agentes de IA, así que **la verificación es manual, en tu navegador**. Para cada revista: (1) en **scimagojr.com**, busca el ISSN y anota el **cuartil 2024** de la categoría más afín (Finance; Economics and Econometrics; Business and International Management); (2) en **mjl.clarivate.com**, busca el ISSN y anota la colección WoS (SCIE, SSCI o ESCI).

**Orden sugerido:** primero las 6 marcadas con ⚠, que son las que podrían no alcanzar Q1/Q2 o no estar en WoS. Las otras 10 son revistas de primer nivel en finanzas y gestión, pero igual hay que anotar su dato.

| # | Revista | ISSN | Núcleo | Scimago | WoS (MJL) | SJR 2024 (cuartil, categoría) | WoS (colección) |
|---|---|---|---|---|---|---|---|
| 1 | ⚠ Journal of Business Venturing Insights | 2352-6734 | 2 | [abrir](https://www.scimagojr.com/journalsearch.php?q=23526734) | [abrir](https://mjl.clarivate.com/search-results?issn=2352-6734) | **Q1** (verificado por el estudiante, 2026-11-07) | pendiente |
| 2 | ⚠ Journal of Economics and Business | 0148-6195 | 3, 12 | [abrir](https://www.scimagojr.com/journalsearch.php?q=01486195) | [abrir](https://mjl.clarivate.com/search-results?issn=0148-6195) | **Q1** (verificado por el estudiante, 2026-11-07) | pendiente |
| 3 | ⚠ Journal of International Financial Management & Accounting | 0954-1314 | 9 | [abrir](https://www.scimagojr.com/journalsearch.php?q=09541314) | [abrir](https://mjl.clarivate.com/search-results?issn=0954-1314) | **Q1** (verificado por el estudiante, 2026-11-07) | pendiente |
| 4 | ⚠ Journal of Small Business & Entrepreneurship | 0827-6331 | 17 | [abrir](https://www.scimagojr.com/journalsearch.php?q=08276331) | [abrir](https://mjl.clarivate.com/search-results?issn=0827-6331) | **Q2** (verificado por el estudiante, 2026-11-07) | pendiente |
| 5 | ⚠ Journal of Economics, Finance and Administrative Science | 2077-1886 | 18 | [abrir](https://www.scimagojr.com/journalsearch.php?q=20771886) | [abrir](https://mjl.clarivate.com/search-results?issn=2077-1886) | **Q2** (verificado por el estudiante, 2026-11-07) | pendiente |
| 6 | ⚠ Journal of Economic Studies | 0144-3585 | 19 | [abrir](https://www.scimagojr.com/journalsearch.php?q=01443585) | [abrir](https://mjl.clarivate.com/search-results?issn=0144-3585) | **Q1** (verificado por el estudiante, 2026-11-07) | pendiente |
| 7 | Journal of Financial Economics | 0304-405X | 1, 6 | [abrir](https://www.scimagojr.com/journalsearch.php?q=0304405X) | [abrir](https://mjl.clarivate.com/search-results?issn=0304-405X) | | |
| 8 | Journal of Banking & Finance | 0378-4266 | 4, 15 | [abrir](https://www.scimagojr.com/journalsearch.php?q=03784266) | [abrir](https://mjl.clarivate.com/search-results?issn=0378-4266) | | |
| 9 | Journal of Financial and Quantitative Analysis | 0022-1090 | 5 | [abrir](https://www.scimagojr.com/journalsearch.php?q=00221090) | [abrir](https://mjl.clarivate.com/search-results?issn=0022-1090) | | |
| 10 | The British Accounting Review | 0890-8389 | 7 | [abrir](https://www.scimagojr.com/journalsearch.php?q=08908389) | [abrir](https://mjl.clarivate.com/search-results?issn=0890-8389) | | |
| 11 | The Review of Financial Studies | 0893-9454 | 8 | [abrir](https://www.scimagojr.com/journalsearch.php?q=08939454) | [abrir](https://mjl.clarivate.com/search-results?issn=0893-9454) | | |
| 12 | Research in International Business and Finance | 0275-5319 | 10 | [abrir](https://www.scimagojr.com/journalsearch.php?q=02755319) | [abrir](https://mjl.clarivate.com/search-results?issn=0275-5319) | | |
| 13 | Finance Research Letters | 1544-6123 | 11, 16 | [abrir](https://www.scimagojr.com/journalsearch.php?q=15446123) | [abrir](https://mjl.clarivate.com/search-results?issn=1544-6123) | | |
| 14 | Management Science | 0025-1909 | 13 | [abrir](https://www.scimagojr.com/journalsearch.php?q=00251909) | [abrir](https://mjl.clarivate.com/search-results?issn=0025-1909) | | |
| 15 | Technological Forecasting and Social Change | 0040-1625 | 14 | [abrir](https://www.scimagojr.com/journalsearch.php?q=00401625) | [abrir](https://mjl.clarivate.com/search-results?issn=0040-1625) | | |
| 16 | Global Finance Journal | 1044-0283 | 20 | [abrir](https://www.scimagojr.com/journalsearch.php?q=10440283) | [abrir](https://mjl.clarivate.com/search-results?issn=1044-0283) | | |

**Qué anotar:**
- **Scimago:** en la ficha de la revista, el recuadro *Quartiles* muestra un cuartil por categoría y por año. Anota el de **2024** en la categoría más afín (Finance; Economics and Econometrics; Business and International Management; Strategy and Management). Si en alguna categoría afín es Q1 o Q2, la revista cumple.
- **MJL:** anota la colección de la Web of Science Core Collection: SSCI, SCIE o ESCI. Si la ficha pide iniciar sesión, la cuenta gratuita de Clarivate basta.
- **Duda abierta:** ESCI es parte de la WoS Core Collection, pero la consigna no dice si basta. Si alguna revista solo está en ESCI, se puede reemplazar por la reserva para no correr riesgos.

**Regla:** si una revista resulta Q3/Q4 o no figura en WoS, su artículo se reemplaza con la reserva (sección 4), que ya está verificada en Crossref.

---

## 7. Incidencias de esta fase

- **Scimago:** 1 solicitud a `journalrank.php?out=xls`, ruta prohibida por su robots.txt, hecha antes de leerlo. Respondió 403 (Cloudflare). No se repitió ni se intentará otra vía automatizada.
- **Semantic Scholar:** 2 respuestas 429 (límite de solicitudes). No se reintentó en bucle.
- **Metadatos discrepantes** corregidos con Crossref: varios años de OpenAlex (p. ej., Kim y Stähler: 2022 → 2026; Chu y Wei: 2023 → 2024; Beaumont et al.: 2022 → 2026).

## 8. Próximos pasos

1. Verificar cuartiles e indexación (sección 6) y reemplazar los que no califiquen.
2. Obtener los 20 PDF: los de acceso abierto desde su enlace oficial; los cerrados por la biblioteca de la UNCP o por la versión del autor. Luego, las traducciones.
3. Fase VIII: generar el `.bib` desde Crossref (negociación de contenido por DOI) para que biblatex-apa produzca el formato APA 7, con títulos en tipo oración.
