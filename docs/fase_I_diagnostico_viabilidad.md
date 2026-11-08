# Fase I — Diagnóstico de viabilidad de datos

**Tema N.º 96:** Fintech y financiamiento participativo (crowdfunding) en el Perú: oferta y condiciones
**Objetivo del temario:** "Caracterizar la oferta de financiamiento participativo y comparar sus condiciones con las del sistema tradicional."
**Fecha de los sondeos:** 2026-11-07 · **User-Agent usado:** `UNCP-Finanzas1-Investigacion/0.1 (estudiante; sondeo de viabilidad)`
**Numerales aplicables:** 2.4.1 (vías, tamaño, variables, integrabilidad), 2.4.3 (descarga programática y sustitución), 2.4.8 (ética del scraping), 2.2 y 2.3 (artículo).

> Todo lo marcado como **verificado** se comprobó con solicitudes reales en esta fecha. Lo marcado como **estimado** o **por verificar** no debe tomarse como hecho. Los sondeos fueron exploratorios: los scripts definitivos (Fase III) generarán su propio log.

---

## 1. Conclusión ejecutiva

1. **Sí existe una fuente oficial de la oferta de crowdfunding, y es extraíble por script.** El portal SIMV de la SMV publica, en *Financiamiento Participativo Financiero → Información de Proyectos*, datos **por plataforma, mes, modalidad y tipo de receptor**: proyectos publicados, proyectos financiados y monto total financiado (S/). Es un formulario ASP.NET; se consulta con `requests` + `BeautifulSoup` (manejo de `__VIEWSTATE` y postback). **Esta es la vía 2 (scraping)** y coincide con lo que sugiere el temario ("SMV […] HTML/PDF por script").
2. **La vía API es sólida.** BCRPData entrega las tasas activas del sistema tradicional por modalidad (bancos, cajas municipales y cajas rurales; pyme y consumo; ≤360 y >360 días). La **API OData de la SMV** entrega los estados financieros trimestrales de las 6 sociedades administradoras de plataformas (PFP).
3. **Brecha principal.** En las fuentes oficiales revisadas **no aparecen la tasa ofrecida, el plazo ni el sector del solicitante por operación de crowdfunding**. Tres de las seis variables sugeridas por el temario no pueden obtenerse de forma oficial y automatizada. La comparación de "condiciones" debe reformularse, y conviene que el docente la valide.
4. **Escenario seleccionado: B (panel de plataformas y series agregadas).** Se descarta A (no hay datos oficiales por operación). C aplica solo a la dimensión de precio (tasa y plazo) del crowdfunding.
5. **Mínimos de tamaño:** el panel plataforma×mes probablemente **no llega a 1 000 filas** (estimado: cientos). La base cumple por la vía de la serie temporal: **60 meses o más** si FECHA_INICIO es anterior o igual a 2021-10. Esto coincide con el criterio alternativo del temario ("panel 2021-2025 con 6 variables"). Hay que confirmarlo con el docente.

---

## 2. Matriz de disponibilidad de fuentes (verificada el 2026-11-07)

| # | Institución | Dataset o registro | URL o endpoint oficial | Tipo de extracción | Variables disponibles | Frecuencia | Periodo | N.º de registros verificables | Unidad de análisis | Llave de integración | Restricciones | Estado de viabilidad |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | SMV | Información de Proyectos FPF (SIMV) | `https://www.smv.gob.pe/SIMV/Frm_ProyectosFPF?data=785FE29A0201FCD759A08F94A0F74DBB4FD1B4D805` | **Scraping HTML** (formulario ASP.NET, POST con `__VIEWSTATE`; filtros: plataforma, año, mes, casilla "retiradas") | Modalidad (p. ej., PRÉSTAMOS), tipo (EMPRESARIAL/PERSONAL), proyectos publicados, proyectos financiados, monto total financiado (S/) | Mensual | Años en el filtro: 2020-2026. **Inicio real por verificar** (la prensa ubica la primera autorización en abril de 2022) | **Verificado:** 1 consulta con datos (Inversiones.io, jun-2025: empresarial 36/31/S/ 10 106 257; personal 3/2/S/ 534 072). **Estimado:** cientos de filas plataforma×mes×tipo | Plataforma-mes-tipo | `periodo` (AAAA-MM); plataforma→RUC | Sin robots.txt propio (`/robots.txt` redirige a gob.pe/smv). 6 plataformas: 3 vigentes y 3 retiradas. Las consultas a Afluenta (dic-2022, jun-2021) no devolvieron filas: falta aclarar si es ausencia real o un detalle del formulario | **VIABLE: vía 2, núcleo del estudio** |
| 2 | SMV | API OData, información financiera (PrincipalCuentaSMV) | `https://mvnet.smv.gob.pe/SMV.OData.Api/api/InfFinanciera/PrincipalCuentaSMV?sEjercicio={AAAA}&sPeriodo={1-4}&sTipoInf=I` | **API REST (JSON)** | RPJ, TipoEmpresa, NombreEmpresa, RUC, CIIU, Moneda, ActivoTotal, PasivoTotal, PatrimonioTotal, TotalIngreso, UtilidadNeta, FechaRegistro (miles de S/) | Trimestral | PFP: 2022-T2 a 2026-T2 | **Verificado:** 26 consultas (2020-T1 a 2026-T2), todas HTTP 200; **49 filas PFP, 6 RUC** | Plataforma-trimestre | `RUC` + trimestre | Sin documentación pública (swagger 404); parámetros tomados del recurso publicado en Datos Abiertos; no requiere clave | **VIABLE: vía 1 (complemento de oferta)** |
| 3 | BCRP | BCRPData, tasas activas por modalidad y TAMN | `https://estadisticas.bcrp.gob.pe/estadisticas/series/api/{códigos}/json/{inicio}/{fin}` | **API REST (JSON)** | Verificadas: PN07807NM (TAMN); PN07843NM/PN07844NM (bancos, MN, pyme ≤360/>360 d); PN07846NM/PN07847NM (bancos, MN, consumo ≤360/>360 d); PN07861NM/PN07862NM (cajas municipales, MN, pyme); PN07879NM/PN07880NM (cajas rurales, MN, pyme); PN07849NM (promedio de estructura constante) | Mensual | Bancos: ago-2010 a oct-2026; cajas: jul-2010 a sep-2026; TAMN: feb-1992 a oct-2026 | **Verificado:** nombre oficial y valor de ene-2021 por API (p. ej., TAMN = 12.0323; bancos pyme ≤360 d = 31.11) | Sistema-mes | `periodo` (AAAA-MM) | Responde con `content-type: text/html` y codificación mixta (hay que decodificar con cuidado); `estadisticas.bcrp.gob.pe/robots.txt` no existe (404) | **VIABLE: vía 1, núcleo de la comparación** |
| 4 | PCM: Datos Abiertos | API CKAN `package_search` (endpoint del temario) | `https://www.datosabiertos.gob.pe/api/3/action/package_search` | API | — | — | — | **HTTP 404** en 7 consultas | — | — | robots.txt: `Crawl-delay: 10`, `Disallow: /search/` | **NO VIABLE tal como figura en el temario.** `package_list` y `package_show` sí responden (HTTP 200). **Ningún dataset de crowdfunding** entre 3 657 |
| 5 | PRODUCE (vía Datos Abiertos) | Acceso de las MIPYME al crédito en el sistema financiero formal, 2024 | `https://www.datosabiertos.gob.pe/sites/default/files/financiamiento_2024_rev_rest.csv` | Descarga programática (CSV) | tamaño, CIIU, sector, ubigeo, contribuyente, nrotrab, saldo_miles_soles, exporta, ventas_prom, año (empresa anonimizada) | Anual | **Solo 2024** | **Verificado:** 133 894 973 bytes, cabecera leída; filas sin contar | Empresa | año, sector | Crawl-delay 10; un solo año; sin tasas | **De reserva** (técnicamente viable, poca pertinencia) |
| 6 | SBS | Tasas activas por tipo de crédito y empresa; Boletín `stats_net` | `https://www.sbs.gob.pe/app/pp/EstadisticasSAEEPortal/Paginas/TIActivaTipoCreditoEmpresa.aspx?tip=B` | Scraping o descarga | (TEA por tipo de crédito y entidad) | Diaria o mensual | — | **Bloqueo:** respuesta de 212 bytes con desafío Incapsula (`/_Incapsula_Resource`). `stats_net` respondió a la 1.ª solicitud y bloqueó las siguientes | Entidad-día | fecha + entidad | Protección anti-bot: **eludirla está prohibido** | **NO VIABLE.** No se declara: no se necesita sustitución |
| 7 | BCRP | Reporte de Estabilidad Financiera (PDF) | `https://www.bcrp.gob.pe/docs/Publicaciones/Reporte-Estabilidad-Financiera/2025/mayo/ref-mayo-2025.pdf` | Descarga programática (PDF) | No verificadas | Semestral | — | **HTTP 200, pero no es PDF:** página "Pardon Our Interruption" (5 996 bytes) | — | — | Bloqueo anti-bot | **NO VIABLE** |
| 8 | SMV | Documentos institucionales (`ConsultasP8`) | `https://www.smv.gob.pe/ConsultasP8/documento.aspx?vidDoc={…}` | Descarga programática (PDF) | El Informe de Evaluación Institucional del 1S-2025 no trae cifras de FPF | — | — | Descarga correcta (`application/pdf`) | — | — | — | Técnicamente viable; **sin datos FPF útiles** |
| 9 | SMV, portal OpenData | Empresas inscritas (servicio WCF/SOAP) | `https://mvnet.smv.gob.pe/SMV.OpenData.wsGen/SMV.ServiciosOpenData.WCF.ServiceEmpresas.svc/ssl?wsdl` | API SOAP | Razón social, fecha y resolución de inscripción, sección de registro, web | Evento | — | Solo se leyeron los metadatos | Empresa | RUC | Licencia ODbL | **Por verificar** (útil para las fechas de autorización) |
| 10 | Plataformas privadas | Web de Inversiones.io y otras | `https://inversiones.io` | Scraping | — | — | — | El sitemap tiene 135 URL y **ninguna de proyectos** (solo noticias) | — | — | No son fuente oficial; los proyectos no son públicos en el sitemap | **NO RECOMENDADO** |

**Plataformas identificadas (fuentes 1 y 2, verificadas):**

| RUC | Sociedad administradora | Estado en el SIMV | Trimestres con EEFF en OData |
|---|---|---|---|
| 20605667351 | Inversiones.io Perú SAPFPF S.A.C. | Vigente | 17 (2022-T2 a 2026-T2) |
| 20612782513 | Prestopolis SAPFPF S.A.C. | Vigente | 7 |
| 20614384213 | Securite SAPFPF S.A.C. | Vigente | 1 (2026-T2) |
| 20566550939 | Afluenta Perú SAPFPF S.A.C. | Retirada | 10 |
| 20610079394 | Inversiones Neurona S.A.C. SAPFP | Retirada | 9 |
| 20610205501 | Proyecto Crowd PFPF S.A.C. | Retirada | 5 |

**Cifras de contexto que NO deben entrar a la base:** la prensa atribuye a la SMV estas cifras: 2024, S/ 54,5 millones en 253 proyectos; 2025, S/ 120,3 millones en 432 proyectos; plazo promedio de 217 y 201 días. Se pueden citar en la introducción (con APA), pero **no son datos extraídos** y sus promedios no cuadran con los totales (S/ 120,3 M ÷ 432 ≈ S/ 278 500, no S/ 267 960). Sirven, además, para contrastar los totales que produzca el scraping del SIMV.

---

## 3. Evaluación de escenarios

| Escenario | Qué exigiría | Evidencia encontrada | Dictamen |
|---|---|---|---|
| **A.** Datos por operación individual | Registro oficial por proyecto con tasa, plazo, monto y sector | El SIMV publica agregados mensuales por plataforma, no proyectos. Las webs privadas no exponen proyectos públicamente. No se halló ningún registro oficial por operación | **Descartado** |
| **B.** Panel de plataformas o series agregadas | Serie o panel oficial con cobertura suficiente | SIMV: plataforma×mes×tipo (montos y proyectos). OData: plataforma×trimestre (EEFF). BCRP: tasas mensuales de 2010 a 2026 | **Seleccionado**, con la brecha de tasa y plazo documentada |
| **C.** Información insuficiente | — | Solo aplica a la dimensión de precio del crowdfunding (tasa ofrecida y plazo por operación) | Parcial: se declara como limitación, no como bloqueo |

> **No se convertirán agregados en operaciones ficticias.** El panel se analiza en su unidad real (plataforma-mes y plataforma-trimestre).

---

## 4. Variables obtenibles realmente

| Variable | Fuente | ¿Verificada? | Unidad | Observación |
|---|---|---|---|---|
| Número de plataformas (autorizadas, con EEFF o con proyectos en el mes) | SIMV y OData | Sí | conteo | Entrada y salida de 6 plataformas |
| Proyectos publicados | SIMV | Sí | conteo/mes | Por plataforma y tipo |
| Proyectos financiados | SIMV | Sí | conteo/mes | — |
| Monto financiado | SIMV | Sí | S/ corrientes | — |
| Tasa de éxito = financiados ÷ publicados | Derivada | — | % | Indicador de acceso |
| Monto promedio por proyecto = monto ÷ financiados | Derivada | — | S/ | "Ticket" promedio |
| Tipo de receptor (empresarial/personal) y modalidad | SIMV | Sí | categórica | Sustituto **parcial** del "sector" |
| Activo, pasivo, patrimonio, ingresos y utilidad de las plataformas | OData | Sí | miles de S/ | Tamaño y sostenibilidad de la oferta |
| Ingreso de la plataforma ÷ monto financiado | Derivada (OData + SIMV) | — | % | Aproximación al **costo de intermediación**; no es la tasa del prestatario |
| TEA bancos, cajas municipales y cajas rurales (pyme, consumo; ≤/>360 d) y TAMN | BCRP | Sí | % TEA | Tasa del sistema tradicional |
| **Tasa ofrecida del crowdfunding** | — | **No encontrada** | — | Brecha |
| **Plazo por operación** | — | **No encontrado** | — | Brecha (los límites normativos sí están en el Reglamento) |
| **Sector del solicitante** | — | **No encontrado** | — | Brecha |

**Cumplimiento del 2.4.1 con estas variables:** 6 columnas o más ✔; 4 sustantivas o más ✔ (proyectos financiados, monto, número de plataformas, TEA bancaria, etc.); 1 o más de cada fuente ✔; llave `periodo` ✔.

---

## 5. Riesgos principales

### Metodológicos
| ID | Riesgo | Efecto | Mitigación |
|---|---|---|---|
| M1 | No hay tasa, plazo ni sector oficiales del crowdfunding | La comparación de "condiciones" queda incompleta (C3) | Reformular "condiciones" como acceso, monto, tipo de receptor y costo de intermediación, más los límites normativos (50/500/1 000 UIT; plazo máximo para proyectos personales). Validarlo con el docente |
| M2 | Comparabilidad de tasas: la TEA bancaria promedia prestatarios, riesgos y garantías distintos | Comparaciones engañosas | Usar MN y el tramo ≤360 d; tabla explícita de diferencias (moneda, plazo, riesgo, garantía, costos, TCEA no disponible) |
| M3 | Pocas plataformas (6 en total, 2 a 4 activas a la vez) | Inferencia estadística débil | Análisis descriptivo, tendencias, concentración (HHI), comparación antes y después; nada de regresiones artificiales |
| M4 | "No se encontraron registros" en el SIMV: ¿es cero o es faltante? | Sesgo en los totales | Regla documentada: cero solo con la plataforma autorizada y una respuesta válida; si no, faltante. Contrastar con las cifras anuales atribuidas a la SMV |
| M5 | Quiebre regulatorio (Res. SMV 019-2025-SMV/01, noviembre de 2025) | Cambio de nivel en montos | Usarlo como corte analítico antes y después |
| M6 | Estado del arte de 4 años con poca literatura peruana sobre FPF | Dificultad para reunir 20 referencias Q1/Q2 pertinentes | Literatura internacional sobre *lending-based crowdfunding* y fintech, 2022-2026 |

### Técnicos
| ID | Riesgo | Mitigación |
|---|---|---|
| T1 | El SIMV es ASP.NET con ViewState y podría adoptar protección anti-bot | Guardar cada HTML crudo; pausa de 3 s; caché; no reconsultar meses ya válidos; demo en vivo con 1 consulta |
| T2 | Respuestas "HTTP 200" que no son datos (BCRP-REF devolvió 200 con una página anti-bot) | **Validar el contenido** (tabla `grdTodos`, JSON con `config`, firma `%PDF`) antes de guardar; nunca sobrescribir crudos válidos |
| T3 | La API OData de la SMV no tiene documentación pública | Declarar los parámetros y guardar el JSON crudo; pruebas con respuestas simuladas |
| T4 | Revisiones de las fuentes vivas | FECHA_CORTE congelada, hash del archivo entregado y log con hora (2.4.5) |
| T5 | Python 3.14.7 en tu equipo: algunas librerías pueden no tener *wheels* | Probar `pandera` y `kaleido` en la Fase III; si fallan, usar un entorno con Python 3.12 |
| T6 | Internet del aula durante la demo | Plan B: consulta corta, log previo y crudo en caché (sin presentarlo como ejecución en vivo) |

### De calendario
| ID | Riesgo | Mitigación |
|---|---|---|
| K1 | La fecha de exposición de la U-II figura como **2025-12-09** en el Excel (2025 es un martes, igual que la U-I; en 2026 el 09-12 cae miércoles) | Confirmar. Si es el 08-12-2026, el EXANTE vence el 06-12 a las 23:59; si es el 09-12-2026, el 07-12 a las 23:59. La sustitución de fuente vence 5 días antes (01-12 o 02-12) |
| K2 | 3 commits en fechas distintas | Crear el repositorio esta semana y hacer commits reales por fase |
| K3 | Carga de la Carpeta N.º 1: 20 artículos, 20 traducciones, 20 pósteres y 20 plantillas | Elegir los 20 artículos dentro del mismo estado del arte para que cuenten también como referencias |

---

## 6. Arquitectura recomendada

```
Vía 1: API (01_extraccion_api.py)
  ├─ BCRPData  → 9 series mensuales de tasas (2021-01 … FECHA_CORTE)
  └─ SMV OData → EEFF trimestrales (filtrar TipoEmpresa = SAPFPF en 03)
Vía 2: scraping (02_scraping_web.py)
  └─ SMV SIMV «Información de Proyectos» → 6 plataformas × mes
       GET (ViewState) → POST (plataforma, año, mes) → validar tabla → guardar HTML → parsear
03_limpieza_datos.py
  ├─ Panel plataforma-mes-tipo (SIMV) + correspondencia nombre→RUC (OData)
  ├─ Panel plataforma-trimestre (OData)
  └─ Base mensual integrada por `periodo` → datos_procesados_2024200481M.csv
04_analisis.py → /salidas (tablas .csv/.tex, figuras .png/.pdf)
```

**Periodo propuesto:** FECHA_INICIO = 2021-01 (año del Reglamento FPF, Res. 045-2021-SMV/02) y FECHA_CORTE = 2026-09 (último mes completo común a las fuentes; falta verificar el rezago de publicación del SIMV). Resultado: **69 meses**.

**Por qué esta arquitectura:** las tres fuentes son oficiales, públicas, sin clave y extraíbles por script. Cada una alimenta al menos un resultado (sin fuentes decorativas). Y la vía 2 es precisamente la que propone el temario.

---

## 7. Decisiones que debes tomar

| ID | Decisión | Recomendación |
|---|---|---|
| D-1 | Confirmar con el docente la fecha de exposición de la U-II | **Resuelto (2026-11-07):** entrega fija el 2026-12-06 a las 23:59; la exposición puede cambiar |
| D-2 | Aprobar el **Escenario B** y las vías: API = BCRPData + SMV-OData; scraping = SMV-SIMV | Aprobar |
| D-3 | Consultar al docente si se aceptan variables sustitutas para "tasa ofrecida, plazo y sector" | **Resuelto:** el docente acepta las variables sustitutas |
| D-4 | Periodo 2021-01 a 2026-09 frente a la regla de "estado del arte de 4 años" | **Resuelto:** el docente acepta el panel 2021-01 a 2026-09 |
| D-5 | Ventana bibliográfica: ¿2022-2026 o 2023-2026? ¿Las fuentes normativas y de datos cuentan dentro de las 20 referencias? | **Resuelto:** 2023-2026; las normas y las fuentes de datos no cuentan en el estado del arte |

---

## Anexo A. Borrador de consulta al docente (enviarlo tú, por ADESA o por el grupo del curso)

> Estimado Dr. Machacuay:
>
> Soy Diego Sebastián Aliaga Damián (2024200481M), tema N.º 96 de la Unidad II. Le escribo para confirmar cuatro puntos antes de construir la base de datos:
>
> 1. **Fecha de exposición.** En el Excel de asignación figura 09/12/2025. ¿La fecha correcta es el martes 08/12/2026 o el miércoles 09/12/2026?
> 2. **Variables.** La SMV publica en su portal SIMV, por plataforma y por mes, los proyectos publicados, los proyectos financiados y el monto financiado. No publica la tasa, el plazo ni el sector de cada operación. ¿Puedo reemplazar "tasa ofrecida, plazo y sector del solicitante" por: proyectos financiados, monto financiado, tipo de receptor (empresarial/personal), tasa de éxito, indicadores financieros de las plataformas (SMV) y tasas activas comparables del BCRP?
> 3. **Periodo.** Propongo una serie mensual de enero de 2021 a septiembre de 2026 (69 meses), según el criterio de 60 periodos mensuales del numeral 2.4.1. ¿Es compatible con la regla del estado del arte de 4 años, o esa regla aplica solo a la literatura?
> 4. **Estado del arte.** ¿La ventana de 4 años es 2022-2026 o 2023-2026? ¿Las normas (DU 013-2020, Res. SMV 045-2021) y las fuentes de datos cuentan dentro de las 20 referencias?
>
> Las vías serán API (BCRPData y API OData de la SMV) y scraping (portal SIMV de la SMV). Le comento además que el endpoint CKAN `package_search` de Datos Abiertos que figura en el temario devuelve HTTP 404.
>
> Atentamente,
> Diego Sebastián Aliaga Damián

---

## Anexo B. Registro de los sondeos de la Fase I (transparencia)

| Host | Solicitudes (aprox.) | Resultado | Nota ética |
|---|---|---|---|
| estadisticas.bcrp.gob.pe | 6 | HTTP 200 (API y catálogo); robots.txt 404 | — |
| mvnet.smv.gob.pe | ~40 | HTTP 200 en la API (26/26); 404/403 en rutas de documentación | Pausas de 1,2 a 1,5 s |
| www.smv.gob.pe (SIMV, ConsultasP8) | ~14 | HTTP 200 | Pausas de 2 a 3 s |
| www.datosabiertos.gob.pe | ~16 | 404 (package_search), 200 (package_list/show, CSV parcial) | **Incidencia propia:** las primeras 7 consultas a la API se espaciaron 1,2 s, antes de leer el `Crawl-delay: 10`, y se hizo **1 solicitud a `/search/`**, ruta prohibida por robots.txt. Las siguientes respetaron 10,5 s. No se repetirá en los scripts |
| www.sbs.gob.pe | 6 | 1.ª respuesta normal; luego desafío Incapsula | Sin intentos de evasión |
| www.bcrp.gob.pe | 1 (+1 del lector web) | Página anti-bot | Sin intentos de evasión |
| gob.pe | 4 | HTTP 200 | — |
| inversiones.io, afluenta.pe, prestopolis.com, securite.pe | 6 | Solo robots.txt y sitemap | No se rastreó contenido |
