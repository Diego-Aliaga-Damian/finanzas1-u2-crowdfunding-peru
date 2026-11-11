# Matriz de cumplimiento — Finanzas I (055D), Unidad II

**Estudiante:** Diego Sebastián Aliaga Damián · **Matrícula:** 2024200481M
**Tema N.º 96:** Fintech y financiamiento participativo (crowdfunding) en el Perú: oferta y condiciones
**Documento rector:** *Consigna y rúbrica de evaluación*, Finanzas I, UNCP, 2026-II (16 págs.) · *TEMARIO.xlsx* (hojas «Unidad II», «Fuentes», «Asignación»)
**Versión:** 1.0 — 2026-11-07 (Fase I). Documento vivo: se actualiza en cada fase.

> **Regla de lectura.** "Requisito literal" reproduce el texto de la consigna (entre comillas). Ningún requisito figura como *Cumplido* sin evidencia verificable. En la Fase I solo se verificaron fuentes; todo lo demás está *Pendiente*.
>
> **Riesgo:** CRÍTICO = causal de nota cero o de no evaluación · ALTO = tope o descenso de nivel en C4, o descuento de puntos · MEDIO = descenso de nivel en C1, C2, C3, C5 o C6 · BAJO = forma.

---

## A. Plazos, entrega y organización

| N.º | Numeral | Requisito literal | Carácter | Evidencia a generar | Ubicación | Estado | Riesgo | Verificación |
|---|---|---|---|---|---|---|---|---|
| A1 | 2.3 | "una carpeta comprimida nombrada […] APELLIDOS_NOMBRES_UNIDAD-II.zip" | Obligatorio | `ALIAGA_DAMIAN_DIEGO_SEBASTIAN_UNIDAD-II.zip` | Raíz de la entrega | Pendiente | CRÍTICO ("Entregar sin respetar la organización de archivos solicitada") | El script de auditoría comprueba el nombre exacto |
| A2 | 2.5 | "La carpeta general lleva los NOMBRES Y APELLIDOS completos del estudiante y, dentro de ella, estas tres subcarpetas" | Obligatorio | Carpeta general y 3 subcarpetas (N.º 1 Productos, N.º 2 Desarrollo, N.º 3 Base de datos y código), cada una con nombre completo | ZIP | Pendiente | CRÍTICO ("Carpetas sin nombres y apellidos completos: el trabajo no se revisa") | Auditoría de estructura y checklist 2.5 |
| A3 | 2.5 | Subcarpetas internas: "/codigo", "/datos_crudos", "/datos_procesados", "/salidas" | Obligatorio | Nombres literales, sin sufijos | Carpeta N.º 3 | Pendiente | CRÍTICO (organización de archivos) | Comparación exacta de nombres en la auditoría |
| A4 | 2.3 (tabla) | EXANTE: "Dos días antes de la exposición, hasta las 23:59 […] Si no la sube, obtiene nota cero (0)" | Obligatorio | Subida a ADESA y captura con fecha y hora | ADESA | Pendiente. **Entrega fija: 2026-12-06, 23:59** (confirmada por el docente el 2026-11-07); la fecha de exposición puede cambiar | CRÍTICO | Captura de confirmación de ADESA |
| A5 | 2.3 (tabla) | "Carpeta N.º 3 completa […] Sin esta carpeta completa el artículo no entra en evaluación" | Obligatorio | Carpeta N.º 3 completa dentro del EXANTE | ZIP | Pendiente | CRÍTICO | Checklist automatizado y revisión manual |
| A6 | 2.3 (tabla) | EXPOST: "Sube el artículo que elaboró. Si no lo sube, se le descuentan 5 puntos" | Obligatorio | Artículo PDF en el grupo de WhatsApp el día de la exposición, hasta las 23:59 | WhatsApp del curso | Pendiente | ALTO (−5 puntos) | Captura del envío |
| A7 | 2.3 (tabla) | "Ficha de evaluación impresa (documento aparte publicado en ADESA), con nombres y apellidos y la unidad" | Obligatorio | Ficha impresa con el enlace de GitHub (2.4.4) | Físico | Pendiente; falta descargar la ficha de ADESA | ALTO | Revisión física antes de salir |
| A8 | 2.1 | "Los artículos que no se presenten en la fecha y hora indicadas no se evalúan: nota cero (0)" | Obligatorio | Cronograma con margen de 48 h | — | Pendiente | CRÍTICO | Calendario con alarmas |
| A9 | 2.4.3 | Sustitución de fuente: solicitud "con una antelación mínima de cinco (5) días calendario respecto de la entrega EXANTE" | Condicional | `incidencias_fuente.md` y solicitud escrita | Carpeta N.º 3 | **No aplica**: las dos vías funcionan. La incidencia de las plataformas retiradas del SIMV está documentada en `incidencias_fuente.md`, y el docente aceptó tratarla sin sustitución (2026-11-07) | ALTO si llegara a ser necesaria | Revisar en cada fase |

## B. Artículo científico (journal)

| N.º | Numeral | Requisito literal | Carácter | Evidencia a generar | Ubicación | Estado | Riesgo | Verificación |
|---|---|---|---|---|---|---|---|---|
| B1 | 2.2 (1) | "Título, en español y en inglés" | Obligatorio | Portada bilingüe | Journal | Pendiente | MEDIO (C1) | Lista de 12 partes |
| B2 | 2.2 (2) | "Autor" | Obligatorio | Autor, afiliación UNCP y correo institucional | Journal | Pendiente | MEDIO | Idem |
| B3 | 2.2 (3) | "Resumen y palabras clave" | Obligatorio | Resumen de 150 a 250 palabras y 3 a 5 palabras clave | Journal | Pendiente | MEDIO | Idem |
| B4 | 2.2 (4) | "Abstract y keywords" | Obligatorio | Versión en inglés | Journal | Pendiente | MEDIO | Idem |
| B5 | 2.2 (5) | "Introducción" | Obligatorio | Problema, objetivo y aporte | Journal | Pendiente | MEDIO | Idem |
| B6 | 2.2 (6) | "Antecedentes o desarrollo" | Obligatorio | Estado del arte (4 años) y marco regulatorio FPF | Journal | Pendiente | MEDIO | Idem |
| B7 | 2.2 (7) | "Materiales y métodos, con la subsección de fuentes de datos y procedimiento de extracción" | Obligatorio | Subsección explícita: endpoints, selectores, pausas, User-Agent, robots.txt, fechas | Journal | Pendiente | ALTO (C3/C4) | Contrastar con el README y los scripts |
| B8 | 2.2 (8) | "Resultados" | Obligatorio | Tablas y figuras importadas desde `/salidas` | Journal | Pendiente | ALTO | Cada cifra se rastrea a un archivo de `/salidas` |
| B9 | 2.2 (9) | "Discusión" | Obligatorio | Contraste con la literatura | Journal | Pendiente | MEDIO | Coherencia entre resultados, discusión y conclusiones |
| B10 | 2.2 (10) | "Conclusiones" | Obligatorio | Responden a cada objetivo | Journal | Pendiente | MEDIO | Idem |
| B11 | 2.2 (11) | "Referencias bibliográficas: mínimo 20, en APA 7.ª ed." | Obligatorio | 20 o más referencias verificadas (DOI), todas citadas en el texto | Journal | En curso (Fase II-B: 40 referencias 2023-2026 con DOI verificado en Crossref; falta citarlas) | MEDIO (C2 nivel 1 si son menos de 20) | Script que cruza `\cite` con el .bib |
| B12 | 2.2 (12) | "Anexo de datos y código: repositorio, endpoints, diccionario de variables, fecha de corte y hash de verificación" | Obligatorio | Anexo generado a partir del README y del diccionario | Journal | Pendiente | ALTO | Hash del anexo igual al del README y al del archivo |
| B13 | 2.3 | "El artículo tiene un mínimo de 25 y un máximo de 30 páginas" | Obligatorio | PDF de 25 a 30 págs. | Journal | Pendiente | MEDIO (C1) | Conteo automático de páginas del PDF |
| B14 | 2.3 | "Se redacta íntegramente con formato APA 7.ª edición" | Obligatorio | Plantilla `apa7` y `biblatex-apa` | Journal | Pendiente | MEDIO (C2) | Revisión de citas, tablas y figuras |
| B15 | 2.3 | "El artículo (journal), el Beamer y los pósteres se elaboran en LaTeX" | Obligatorio | Fuentes .tex que compilan | Carpeta N.º 2 | Pendiente | ALTO (C1) | Compilación limpia |
| B16 | 2.5 (recuadro) y C2 | "El review de papers se hace con un estado del arte de 4 años" / C2 nivel 1: "estado del arte fuera del rango de 4 años" | Obligatorio | Literatura dentro de la ventana | Journal | **Confirmado por el docente: 2023-2026.** Las normas y las fuentes de datos no cuentan en el estado del arte | MEDIO (C2 cae a 1) | Filtro por año en el .bib |
| B17 | 2.1 | "Turnitin con un índice de similitud máximo de 10 % […] REV2, dentro de las 48 horas" | Obligatorio | Redacción propia y paráfrasis | Journal | Pendiente | CRÍTICO (cero si no se subsana) | Revisión previa de similitud, si se dispone de herramienta |
| B18 | 2.1 / «Sobre el uso de IA» | "Se permite el uso de IA de manera ética y sin excesos […] más del 70 % […] la nota es cero (0)" | Obligatorio | Declaración de uso de IA y redacción propia | Journal | Pendiente | CRÍTICO | Autorrevisión; la defensa oral lo valida |
| B19 | 2.4.6 (Bloque B) | "Una tabla o figura del artículo no se regenera con 04_analisis" → "Se anula ese resultado" | Obligatorio | Tablas y figuras solo desde `/salidas` | Journal | En curso: 04 genera 8 tablas (CSV y LaTeX) y 4 figuras (PNG y PDF), con regeneración verificada; falta usarlas en el artículo | ALTO | Hash de `/salidas` antes y después de reejecutar |
| B20 | 2.4.8 | "Se cita la fuente de los datos en APA 7.ª edición, indicando la institución, el año, el nombre de la base, la fecha de consulta y la URL o endpoint" | Obligatorio | Referencias APA de BCRPData, SMV-OData y SMV-SIMV | Journal | Pendiente | MEDIO (C6) | Lista de fuentes contra referencias |
| B21 | 2.4.4 | "Si el tema exige aleatoriedad […] se fija la semilla con los cuatro últimos dígitos del código de matrícula" | Condicional | Semilla `0481` (de 2024200481M) declarada en el artículo | Código y journal | No aplica salvo bootstrap o Monte Carlo | MEDIO | Búsqueda de `seed` en el código |

## C. Póster científico del artículo

| N.º | Numeral | Requisito literal | Carácter | Evidencia a generar | Ubicación | Estado | Riesgo | Verificación |
|---|---|---|---|---|---|---|---|---|
| C1 | 2.2 | Contenido: "1. Título del paper · 2. Autor del artículo · 3. Autor elaborador del póster · 4. Contexto · 5. Problema · 6. Objetivo · 7. Metodología · 8. Resultados · 9. Conclusiones · 10. Fuente de datos y código QR del repositorio de extracción" | Obligatorio | Póster en LaTeX con los 10 elementos | Carpetas N.º 1 (PDF) y N.º 2 (.tex) | Pendiente | MEDIO (C1) | Lista de 10 elementos y prueba de lectura del QR |
| C2 | 2.4.4 | El enlace del repositorio se consigna "en el póster mediante código QR" | Obligatorio | QR que apunta al repositorio | Póster | Pendiente | MEDIO | Escaneo con el teléfono |

## D. Beamer, exposición y defensa

| N.º | Numeral | Requisito literal | Carácter | Evidencia a generar | Ubicación | Estado | Riesgo | Verificación |
|---|---|---|---|---|---|---|---|---|
| D1 | 2.5 | "Beamer en LaTeX, máximo 10 diapositivas, en PDF" | Obligatorio | Beamer de 10 diapositivas o menos | Carpetas N.º 1 y N.º 2 | Pendiente | MEDIO (C1) | Conteo de páginas del PDF |
| D2 | 2.3 | "El estudiante imprime su Beamer para cada uno de sus compañeros; de no hacerlo no expone, con nota cero (0)" | Obligatorio | Copias impresas para todos los compañeros (confirmar número en ADESA) | Físico | Pendiente | CRÍTICO | Conteo de copias |
| D3 | 2.3 | "La disertación dura aproximadamente 12 minutos; de ellos, 3 minutos se destinan obligatoriamente a la demostración en vivo de la extracción" | Obligatorio | Guion y demostración en vivo ensayada | Aula | Pendiente | ALTO (C5) | Ensayos cronometrados |
| D4 | 2.3 | "La exposición es individual y con ropa formal" | Obligatorio | — | Aula | Pendiente | CRÍTICO | — |
| D5 | 2.4.6 (A5) y «Sobre el uso de IA» | Explicar "qué hace cada bloque de su código, por qué eligió ese endpoint o ese selector, y qué ocurriría si cambiara un parámetro" | Obligatorio | Banco de preguntas y simulacro | Defensa | Pendiente | CRÍTICO ("No poder explicar el propio código") | Simulacro de evaluación |
| D6 | 2.4.6 | "Cuando la fuente exija una clave que el docente no posea, el estudiante ejecuta la extracción en vivo" | Condicional | — | — | No aplica: BCRPData y SMV no exigen clave | BAJO | — |

## E. Materiales complementarios (Carpetas N.º 1 y N.º 2)

> Cantidad: la tabla del 2.5 dice "20 en la Unidad I, 20 en la Unidad II" y el recuadro dice "10 en la Unidad I y 20 en la Unidad II". **Para la Unidad II ambos textos coinciden: 20.** La discrepancia solo afecta a la Unidad I.

| N.º | Numeral | Requisito literal | Carácter | Evidencia a generar | Ubicación | Estado | Riesgo | Verificación |
|---|---|---|---|---|---|---|---|---|
| E1 | 2.5 N.º 1 | "Artículo (journal) en LaTeX, en PDF" | Obligatorio | PDF | Carpeta N.º 1 | Pendiente | ALTO | Auditoría del ZIP |
| E2 | 2.5 N.º 1 | "Beamer en LaTeX, máximo 10 diapositivas, en PDF" | Obligatorio | PDF | Carpeta N.º 1 | Pendiente | ALTO | Idem |
| E3 | 2.5 N.º 1 | "Un póster del artículo en LaTeX, en PDF" | Obligatorio | PDF | Carpeta N.º 1 | Pendiente | ALTO | Idem |
| E4 | 2.5 N.º 1 | "Pósteres en español (PDF): […] 20 en la Unidad II" | Obligatorio | 20 pósteres | Carpeta N.º 1 | Pendiente | MEDIO (C1, 3 o más requisitos) | Conteo automático |
| E5 | 2.5 N.º 1 | "Artículos en inglés de journals Q1 y Q2, Scopus y WoS: […] 20 en la Unidad II" | Obligatorio | 20 PDF originales con su cuartil verificado | Carpeta N.º 1 | En curso: 20 candidatos con DOI verificado; **cuartil SJR e indexación WoS por verificar manualmente** | MEDIO | Tabla de verificación: SJR (Scopus) y Master Journal List (WoS) |
| E6 | 2.5 N.º 1 | "Los mismos artículos traducidos al español" | Obligatorio | 20 traducciones | Carpeta N.º 1 | Pendiente | MEDIO | Emparejamiento 1 a 1 por nombre de archivo |
| E7 | 2.5 N.º 2 | "Un journal de su artículo (template)" | Obligatorio | Fuente .tex | Carpeta N.º 2 | Pendiente | MEDIO | Compila |
| E8 | 2.5 N.º 2 | "Un póster de su artículo (template)" | Obligatorio | Fuente .tex | Carpeta N.º 2 | Pendiente | MEDIO | Compila |
| E9 | 2.5 N.º 2 | "Un Beamer de su artículo (template)" | Obligatorio | Fuente .tex | Carpeta N.º 2 | Pendiente | MEDIO | Compila |
| E10 | 2.5 N.º 2 | "Templates de los pósteres en español, en el número exigido por la unidad" | Obligatorio | 20 fuentes .tex | Carpeta N.º 2 | Pendiente | MEDIO | Conteo y compilación por lote |

## F. Base de datos (2.4.1)

| N.º | Numeral | Requisito literal | Carácter | Evidencia a generar | Ubicación | Estado | Riesgo | Verificación |
|---|---|---|---|---|---|---|---|---|
| F1 | 2.4.1 | "Unidad II: Las dos vías son obligatorias: al menos una API y al menos un scraping o descarga programática" | Obligatorio | API: BCRPData y SMV-OData · Scraping: SMV-SIMV «Información de Proyectos» | `/codigo` | **Implementadas y ejecutadas:** 01 (API: BCRPData y SMV-OData) y 02 (scraping del SIMV), con HTTP registrado en el log | ALTO (sin las dos vías, C4 tiene un tope de nivel 2) | Log con HTTP de ambas vías |
| F2 | 2.4.1 | "Tamaño mínimo: 1 000 observaciones o, si son series de tiempo, un histórico no menor a 60 periodos mensuales" · Temario: "≥1 000 operaciones o panel 2021-2025 con 6 variables" | Obligatorio | Base mensual de 60 periodos o más | `/datos_procesados` | **Aceptado por el docente (2026-11-07):** panel mensual de 2021-01 a 2026-09 (69 periodos) | ALTO (C4 nivel 1: "la base es menor a los mínimos") | `04_analisis` y la auditoría cuentan los periodos |
| F3 | 2.4.1 | "al menos 6 columnas, de las cuales por lo menos 4 son variables sustantivas […] y al menos 1 proviene de cada fuente utilizada" | Obligatorio | Columnas de SIMV, de OData y de BCRP | `/datos_procesados` | Cumplido en el panel de 03: 35 columnas (SIMV 9, EEFF 6, BCRP 10, más llaves y control); validación con Pandera pendiente (Fase IV) | ALTO | Validación del esquema con Pandera |
| F4 | 2.4.1 | "llave común declarada […] Queda prohibida la fuente decorativa: cada fuente debe aparecer en al menos un resultado" | Obligatorio | Llave `periodo` (AAAA-MM) y `RUC + trimestre`; matriz fuente→resultado | README y artículo | Cumplido en 04: SIMV → F1, F2, T1, T2, T4, T5; SMV-OData → T1, T3, F4; BCRP → F3, T7, T8 | ALTO (fuente decorativa: tope de nivel 2) | Matriz fuente × tabla/figura en la auditoría |
| F5 | 2.4.1 | "datos_crudos_<código>.csv (tal como sale de la fuente, sin editar) y datos_procesados_<código>.csv" | Obligatorio | `datos_crudos_2024200481M_*.csv`, `datos_procesados_2024200481M.csv`, más las respuestas originales (JSON/HTML) | `/datos_crudos`, `/datos_procesados` | Generados: crudos de 01 y 02 (originales JSON/HTML y CSV) y procesado de 03 | ALTO | Nombres exactos y hash de los crudos |
| F6 | 2.4.1 | "diccionario_variables.xlsx o .md: nombre de la variable, definición, unidad de medida, frecuencia, fuente exacta y URL o endpoint" | Obligatorio | `diccionario_variables.md` (formato admitido por la consigna) | Carpeta N.º 3 | Generado por 03: 35 variables, cada una con definición, unidad, frecuencia, fuente y endpoint | ALTO (documentación) | Columnas obligatorias comprobadas por script |
| F7 | 2.4.1 y 2.4.5 | "FECHA_INICIO y FECHA_CORTE […] como constantes, no como fechas dinámicas" | Obligatorio | Constantes al inicio de 01 y 02 | `/codigo` | Pendiente (propuesta: 2021-01 a 2026-09) | ALTO | Búsqueda de `date.today`/`now` en los scripts |
| F8 | 2.4.1 | "No se aceptan datasets preexistentes de Kaggle, de repositorios de terceros, de trabajos de ciclos anteriores ni descargados a mano" | Obligatorio | Todo dato proviene de 01 y 02 | — | Cumplible | CRÍTICO | Trazabilidad de la fila al crudo y del crudo al log |
| F9 | 2.1 | "Ningún trabajo se evalúa con datos transcritos a mano, copiados de otro trabajo, simulados o inventados, ni con descargas manuales" | Obligatorio | Las cifras de prensa no entran a la base | — | Cumplible | CRÍTICO | Revisión de que ninguna cifra esté tecleada en el código |

## G. Código, documentación y repositorio (2.4.2 a 2.4.5)

| N.º | Numeral | Requisito literal | Carácter | Evidencia a generar | Ubicación | Estado | Riesgo | Verificación |
|---|---|---|---|---|---|---|---|---|
| G1 | 2.4.2 | `01_extraccion_api.py`: "Consumo de la API, con el endpoint declarado, parámetros, manejo de errores y guardado del crudo" | Obligatorio | Script | `/codigo` | Implementado y ejecutado (24 solicitudes, HTTP 200) | CRÍTICO (sin código: cero) | pytest con respuestas simuladas |
| G2 | 2.4.2 | `02_scraping_web.py`: "selectores usados, paginación, pausas entre solicitudes, User-Agent y guardado del crudo" | Obligatorio | Script (ASP.NET: `__VIEWSTATE`, postback) | `/codigo` | Implementado y ejecutado, con modos `--demo` (exposición) y `--reanudar` | CRÍTICO | pytest con HTML guardado |
| G3 | 2.4.2 | `03_limpieza_datos.py`: "Depuración, tipificación, tratamiento de faltantes y outliers, unión de las fuentes por la llave común" | Obligatorio | Script | `/codigo` | Implementado y ejecutado: panel de 414 filas; verificación celda por celda contra los crudos sin diferencias | ALTO | Pandera y pruebas de unión |
| G4 | 2.4.2 | `04_analisis.py`: "tablas y figuras del artículo, generadas desde el archivo procesado y guardadas en /salidas" | Obligatorio | Script | `/codigo` | Implementado: 8 tablas y 4 figuras; regeneración idéntica verificada por la auditoría (30/30 archivos) | ALTO | Reejecución con comparación de hashes de `/salidas` |
| G5 | 2.4.2 | README.md: "Nombres y apellidos, código de matrícula, tema del temario, fuentes y endpoints, fecha de corte, orden de ejecución, versión del lenguaje y de las librerías, hash SHA-256 del archivo procesado y enlace del repositorio" | Obligatorio | README con los 9 elementos | Carpeta N.º 3 | En curso: los 9 elementos presentes, incluido el SHA-256 del procesado; se actualizará con 04 y con el hash final | ALTO | Lista de 9 elementos |
| G6 | 2.4.2 | requirements.txt: "Versiones exactas de las librerías utilizadas" | Obligatorio | `pip freeze` filtrado y con `==` | Carpeta N.º 3 | Pendiente | ALTO | Instalación en un entorno limpio |
| G7 | 2.4.2 y 2.4.6 | ".env.example […] la ausencia del archivo .env.example, sí cuenta como documentación incompleta" | Obligatorio | `.env.example` aunque no haya claves (p. ej., contacto del User-Agent y pausa) | Carpeta N.º 3 | Pendiente | ALTO | Existencia del archivo |
| G8 | 2.4.2 | log_ejecucion.txt: "fecha y hora de cada extracción, número de filas descargadas y código de respuesta HTTP" | Obligatorio | Log generado por `logging` | Carpeta N.º 3 | Generado: fecha y hora, HTTP, filas y SHA-256 de cada extracción | ALTO | La auditoría valida el formato de cada línea |
| G9 | 2.4.2 | incidencias_fuente.md "(solo si aplica)" | Condicional | Registro de fuentes descartadas (SBS, REF-BCRP) | Carpeta N.º 3 | Creado: incidencia de las plataformas retiradas (aceptada por el docente), fuentes descartadas e incidencias propias | BAJO | — |
| G10 | 2.4.2 | "Las cuatro primeras líneas de cada archivo de código deben ser comentarios con: (1) nombres y apellidos completos, (2) código de matrícula, (3) tema y número del temario, y (4) fecha de extracción" | Obligatorio | Encabezado en 01 a 04 y en los módulos auxiliares | `/codigo` | Pendiente | MEDIO | Prueba automática de las 4 líneas |
| G11 | 2.4.2 | "Los nombres de archivo de los datos llevan el código de matrícula" | Obligatorio | Sufijo `2024200481M` | Carpeta N.º 3 | Pendiente | MEDIO | Patrón de nombres en la auditoría |
| G12 | 2.4.4 | "No se aceptan rutas absolutas del computador del estudiante (C:\Users\...)" | Obligatorio | `pathlib` relativo a la raíz del proyecto | `/codigo` | Pendiente | ALTO (Bloque B) | Búsqueda de `C:\` y `/Users/` |
| G13 | 2.4.4 | "Toda clave o token de API se declara como variable de entorno" | Obligatorio | Variables mediante `.env` | `/codigo` | Pendiente | MEDIO | Búsqueda de secretos |
| G14 | 2.4.4 | "El código debe estar comentado en español, explicando qué hace cada bloque" | Obligatorio | Comentarios por bloque | `/codigo` | Pendiente | MEDIO | Revisión |
| G15 | 2.4.4 | "El repositorio GitHub es obligatorio (público o con acceso concedido al docente) […] como mínimo tres commits en fechas distintas" | Obligatorio | Repositorio con commits reales desde noviembre de 2026 | GitHub | **Cumplido el mínimo:** repositorio público (https://github.com/Diego-Aliaga-Damian/finanzas1-u2-crowdfunding-peru) con commits en 3 fechas distintas: `9d68b50` (2026-11-07), `fedbd0f` (2026-11-08) y `5352138` (2026-11-09); un commit por día | ALTO (también es indicio de duplicidad, 2.4.7) | `git log --format=%ad` con 3 fechas distintas o más |
| G16 | 2.4.5 | "El hash SHA-256 declarado en el README se coteja contra el archivo entregado" / "coincidencia de valores en al menos el 95 % de las celdas" | Obligatorio | Hash y script de verificación de equivalencia | Carpeta N.º 3 | Pendiente | CRÍTICO (Bloque A3) | Recalcular el hash del ZIP final |
| G17 | 2.4.5 | "Los datos crudos se entregan tal como salieron de la fuente; […] no se editan bajo ninguna circunstancia" | Obligatorio | Crudos inmutables (escritura atómica y sin sobrescribir los válidos) | `/datos_crudos` | Pendiente | CRÍTICO (Bloque A2) | Hash de los crudos registrado en el log |
| G18 | 2.5 (lista) | "El código se ejecutó de principio a fin en una carpeta limpia y volvió a generar la base" | Obligatorio | Prueba en un clon limpio | — | Pendiente | ALTO | Ejecución desde un `git clone` nuevo |

## H. Verificación de autenticidad (2.4.6, Bloque A: faltas eliminatorias)

| N.º | Verificación del docente | Hallazgo eliminatorio | Riesgo | Control preventivo |
|---|---|---|---|---|
| H1 | Cotejo de 10 observaciones al azar con la fuente en vivo | "Un dato que no existe en la fuente […] invalida toda la base" | CRÍTICO | Script `verificar_muestra.py`: 10 filas al azar contrastadas en vivo con la SMV y el BCRP |
| H2 | Coincidencia entre código y datos | "Datos editados a mano, pegados o alterados en Excel" | CRÍTICO | Comparar la reejecución con el entregable (95 % de celdas o más) |
| H3 | Integridad: hash SHA-256 | "Hash que no corresponde al archivo entregado" | CRÍTICO | Calcular el hash como último paso antes de comprimir |
| H4 | Origen de la base | "Base descargada manualmente, tomada de terceros" | CRÍTICO | Toda base nace de 01 y 02 |
| H5 | Defensa oral y extracción en vivo | "No poder explicar el propio código" | CRÍTICO | Simulacros (Fase XIII) |
| H6 | Duplicidad (2.4.7) | "Bases o scripts sustancialmente idénticos" | CRÍTICO | Código propio, commits graduales, nombres de variables propios |
| H7 | Ausencia del código de extracción | "No adjuntar los scripts" | CRÍTICO | Auditoría de existencia |

## I. Ética y legalidad del scraping (2.4.8) y criterio C6

| N.º | Requisito literal | Evidencia | Estado | Riesgo |
|---|---|---|---|---|
| I1 | "Se rastrea únicamente información pública. Está prohibido extraer datos personales protegidos por la Ley N.º 29733" | La tabla SIMV es agregada (plataforma, mes, modalidad); no tiene nombres de receptores | Verificado en Fase I | CRÍTICO (C6 = 0) |
| I2 | "Se respetan el archivo robots.txt y los términos de uso del portal" | robots.txt de cada host guardado en `/datos_crudos/robots/` con fecha | Pendiente (falta revisar los términos de uso del SIMV) | ALTO (C6 nivel 1) |
| I3 | "Se incluye una pausa mínima de 1 segundo entre solicitudes y un User-Agent identificable" | Pausa de 3 s en la SMV y de 10 s o más en Datos Abiertos (Crawl-delay 10); UA con nombre del proyecto y contacto institucional | Pendiente | ALTO (C6 nivel 1) |
| I4 | C6 nivel 4: "Usa la IA de manera ética y declarada" | Declaración de IA en el artículo y en el README | Pendiente | MEDIO |

---

## Causales de nota cero aplicables a la Unidad II (consolidado)

1. Entregar fuera de la fecha u hora (EXANTE) o no subir el EXANTE. *(2.1, 2.3, 2.5)*
2. Carpetas sin nombres y apellidos completos, o sin la organización de archivos solicitada. *(2.5)*
3. Carpeta N.º 3 incompleta: "el artículo no entra en evaluación". *(2.3)*
4. Presentarse sin ropa formal o sin el Beamer impreso para los compañeros. *(2.3, 2.5)*
5. Similitud mayor al 10 % no subsanada en REV2. *(2.1)*
6. Uso de IA no humanizada en más del 70 %, o no poder explicar el propio código. *(2.1, «Sobre el uso de IA», 2.4.6-A5)*
7. Datos no reales, no verificables, que no coinciden con la salida del código, editados a mano o de origen manual o de terceros. *(2.4, 2.4.6-A1 a A4)*
8. No adjuntar el código de extracción. *(2.4.6-A7)*
9. Duplicidad según el 2.4.7 (incluido un historial de commits inexistente o concentrado en un solo commit). *(2.4.6-A6)*
10. Extracción de datos personales protegidos (C6 = 0). *(2.4.8)*

**Descuentos no eliminatorios:** EXPOST no subido (−5 puntos); una sola vía sin autorización (C4 con tope de nivel 2); fuente decorativa (C4 con tope de nivel 2); falta de documentación (C4 con tope de nivel 3 si faltan 1 o 2 elementos, de nivel 2 si faltan 3 o más).
