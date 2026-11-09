# Reporte de auditoría automatizada

- Fecha y hora: 2026-11-09 12:18:38
- Commit de referencia: `fedbd0f` (los cambios no confirmados también se auditan)
- Modo: local + cotejo en vivo
- Resultado: ✅ 44 cumplen · ❌ 0 no cumplen · ⏳ 2 no ejecutados

> Regla de autenticidad: un control marcado ⏳ no se ejecutó y no cuenta como cumplido.

## 1. Estructura y documentación

| Estado | Control | Numeral | Evidencia |
|---|---|---|---|
| ✅ | Script `01_extraccion_api.py` | 2.4.2 | presente |
| ✅ | Script `02_scraping_web.py` | 2.4.2 | presente |
| ✅ | Script `03_limpieza_datos.py` | 2.4.2 | presente |
| ⏳ | Script `04_analisis.py` | 2.4.2 | pendiente: se escribe en la Fase V |
| ✅ | Archivo `README.md` | 2.4.2 | 6,179 bytes |
| ✅ | Archivo `requirements.txt` | 2.4.2 | 664 bytes |
| ✅ | Archivo `.env.example` | 2.4.2 | 424 bytes |
| ✅ | Archivo `log_ejecucion.txt` | 2.4.2 | 482,065 bytes |
| ✅ | Archivo `diccionario_variables.md` | 2.4.2 | 9,095 bytes |
| ✅ | Archivo `incidencias_fuente.md` | 2.4.2 | 7,382 bytes |
| ✅ | Crudo `datos_crudos_2024200481M_bcrp.csv` | 2.4.1 | 690 filas |
| ✅ | Crudo `datos_crudos_2024200481M_smv_odata.csv` | 2.4.1 | 6,001 filas |
| ✅ | Crudo `datos_crudos_2024200481M_smv_simv.csv` | 2.4.1 | 536 filas |
| ✅ | Procesado `datos_procesados_2024200481M.csv` | 2.4.1 | presente |
| ✅ | Encabezado obligatorio de 4 líneas en cada archivo de código | 2.4.2 | 5/5 archivos |
| ✅ | Sin rutas absolutas del equipo en el código | 2.4.4 | ninguna |
| ✅ | requirements.txt con versiones exactas | 2.4.2 | 27 librerías con `==` |
| ✅ | .env.example sin claves ni valores reales | 2.4.4 | 2 variables, todas vacías |

## 2. Mínimos de la base

| Estado | Control | Numeral | Evidencia |
|---|---|---|---|
| ✅ | Histórico de al menos 60 periodos mensuales | 2.4.1 | 69 meses (2021-01 a 2026-09); 414 filas |
| ✅ | Al menos 6 columnas | 2.4.1 | 35 columnas |
| ✅ | Al menos 4 variables sustantivas | 2.4.1 | 24 sustantivas |
| ✅ | Al menos 1 variable de cada fuente | 2.4.1 | SMV-SIMV (scraping): 9; SMV-OData (API): 5; BCRP (API): 10 |
| ✅ | Dos vías de extracción ejecutadas (API y scraping) | 2.4.1 | API: 48 respuestas HTTP 200 · scraping: 1651 respuestas HTTP 200 (según el log) |

## 3. Autenticidad (controles locales del Bloque A)

| Estado | Control | Numeral | Evidencia |
|---|---|---|---|
| ✅ | 03 regenera la base entregada desde los crudos | 2.4.5 / A2 | bytes idénticos: sí; celdas iguales: 100.0 %; columnas =; filas = |
| ✅ | SHA-256 del README = hash del archivo entregado | 2.4.5 / A3 | declarado cd48b21f2284… · real cd48b21f2284… |
| ✅ | Cada valor de la base coincide con su crudo (SIMV, EEFF y BCRP) | 2.4.6 / A1-A2 | 1,406/1,406 valores idénticos |
| ✅ | Sin imputaciones: meses sin registros o no obtenidos quedan vacíos | 2.1 / A2 | 0 celdas con valor donde debería estar vacío |
| ✅ | Scripts de extracción presentes | 2.4.6 / A7 | 01 y 02 presentes |

## 4. Integridad de los crudos

| Estado | Control | Numeral | Evidencia |
|---|---|---|---|
| ✅ | SHA-256 de cada respuesta original registrado en el log | 2.4.5 | 398/398 archivos |
| ✅ | Cada HTML del SIMV trae la grilla y confirma su consulta | 2.4.6 | 374/374 válidos |
| ✅ | Los 3 CSV crudos se reconstruyen idénticos desde los originales | 2.4.5 | 3/3 idénticos |

## 5. Calidad de la base procesada

| Estado | Control | Numeral | Evidencia |
|---|---|---|---|
| ✅ | Esquema Pandera: tipos, dominios, rangos y llave única | 2.4.2 | 35 columnas validadas |
| ✅ | Sin duplicados en la llave ruc + periodo | 2.4.2 | 0 duplicados |
| ✅ | EEFF solo en meses de cierre de trimestre (no se interpola) | 2.4.2 | 0 filas fuera de mar/jun/sep/dic |
| ✅ | Valores SIMV presentes solo cuando estado_simv = con_registros | 2.4.2 | 0 filas incoherentes |
| ✅ | Faltantes identificados y explicados | 2.4.2 | 16 columnas con faltantes; máximo 97.6 % (meses sin registros, no obtenidos o fuera del cierre trimestral; detalle en reporte_limpieza.md) |

## 6. Consistencia de fechas

| Estado | Control | Numeral | Evidencia |
|---|---|---|---|
| ✅ | FECHA_INICIO y FECHA_CORTE constantes e idénticas en 01, 02 y 03 | 2.4.5 | {('2021-01', '2026-09')} |
| ✅ | La base cubre exactamente la ventana declarada | 2.4.5 | 2021-01 a 2026-09 |
| ✅ | Las fechas de extracción del encabezado figuran en el log | 2.4.2 / 2.4.5 | fechas con solicitudes en el log: ['2026-11-07', '2026-11-08'] |

## 7. Ética de la extracción

| Estado | Control | Numeral | Evidencia |
|---|---|---|---|
| ✅ | User-Agent identificable en cada corrida de extracción | 2.4.8 | 4/4 corridas con User-Agent del proyecto |
| ✅ | Pausa mínima de 1 s entre solicitudes (medida en el log) | 2.4.8 | 1,724 intervalos; mínimo 3 s; mediana 4 s (resolución del log: 1 s) |
| ✅ | Evidencia de robots.txt del portal rastreado | 2.4.8 | www.smv.gob.pe no publica un robots.txt propio (la ruta redirige a otra página); no hay reglas que prohíban la ruta /SIM |
| ✅ | Códigos HTTP registrados en el log | 2.4.2 | 1,728 solicitudes: HTTP 200 = 1,728 |

## 8. Tablas y figuras

| Estado | Control | Numeral | Evidencia |
|---|---|---|---|
| ⏳ | Las tablas y figuras del artículo se regeneran con 04_analisis.py | 2.4.6 / B | no ejecutado: 04_analisis.py se escribe en la Fase V |

## 9. Cotejo en vivo con la fuente

| Estado | Control | Numeral | Evidencia |
|---|---|---|---|
| ✅ | BCRP en vivo: 10 filas al azar × 10 series | 2.4.6 / A1 | 100/100 valores iguales a la API hoy |
| ✅ | SIMV en vivo: 10 plataforma-mes al azar (préstamos, ambos tipos) | 2.4.6 / A1 | 10/10 filas cotejadas; 54/54 valores iguales al portal hoy |
