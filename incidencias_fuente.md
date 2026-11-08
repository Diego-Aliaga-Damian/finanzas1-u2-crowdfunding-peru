# Registro de incidencias de las fuentes (numeral 2.4.3)

**Estudiante:** Diego Sebastián Aliaga Damián · **Matrícula:** 2024200481M · **Tema N.º 96**

Este archivo registra los problemas técnicos de las fuentes y las decisiones tomadas. **No se ha solicitado sustitución de fuente**: las dos vías exigidas (API y scraping) funcionan. Las incidencias limitan la cobertura, no la existencia de las vías.

---

## Incidencia 1 · SMV, portal SIMV: plataformas retiradas sin grilla de resultados

| Campo | Detalle |
|---|---|
| Fuente | SMV, Sistema de Información del Mercado de Valores (SIMV), «Información de Proyectos» FPF |
| URL | https://www.smv.gob.pe/SIMV/Frm_ProyectosFPF?data=785FE29A0201FCD759A08F94A0F74DBB4FD1B4D805 |
| Fecha y hora | 2026-11-07, entre las 19:12 y las 19:16 (diagnóstico) y durante el censo (ver `log_ejecucion.txt`, líneas `SIMV \| INCIDENCIA`) |
| Método y código HTTP | POST (postback ASP.NET) · **HTTP 200** |
| Plataformas afectadas | Las tres de la lista «Retiradas»: Afluenta Perú (id 181125), Inversiones Neurona (184758) y Proyecto Crowd (184550) |
| Mensaje o comportamiento del portal | De forma **intermitente**, el formulario devuelto **confirma la consulta** (plataforma, año y mes seleccionados; casilla «Retiradas» marcada), pero **no muestra la grilla** de resultados ni el mensaje «No se encontraron registros». No hay advertencia visible. Para las plataformas vigentes, la misma consulta sí devuelve la grilla |
| robots.txt | www.smv.gob.pe no publica robots.txt propio (la ruta redirige con 301 a https://www.gob.pe/smv); no hay reglas que prohíban /SIMV/ (evidencia en `datos_crudos/robots/`) |
| Evidencia | Respuestas guardadas en `datos_crudos/smv_simv/incidencias/*_no_valida.html` |
| Captura de pantalla | `docs/captura_simv_afluenta_2022-06.png` (2026-11-07, 19:40). En el navegador, la misma consulta (Afluenta, junio de 2022, casilla «Retiradas») **sí muestra la grilla**: préstamos personales, 31 publicados, 14 financiados, S/ 62 143. Se usa solo como evidencia, no como dato |

**Diagnóstico realizado** (unas 20 solicitudes con pausas de 3 s, sin evadir ninguna protección):
1. Envío del formulario completo, tal como lo serializa un navegador (incluidos `ctl00$rbNuevo`, `ctl00$txtSearch`, `ctl00$hdfArticulo`): sin grilla.
2. Repetición exacta de la secuencia que en un sondeo exploratorio anterior (mismo día, Fase II) sí devolvió datos de Afluenta: sin grilla.
3. Revisión del JavaScript de la página: solo valida campos en el navegador; no rellena campos ocultos ni usa postback asíncrono (no hay `PageRequestManager`).

**Antecedente:** en un sondeo exploratorio de la Fase II (2026-11-07), el portal devolvió la grilla para Afluenta en tres meses (2022-06: préstamos personales, 31 publicados, 14 financiados, S/ 62 143; 2023-06: 1/0/0; 2024-01: 0/0/0). Eso indica que **los datos existen en la fuente**, pero que el acceso automatizado a las plataformas retiradas no es estable. Ese sondeo **no forma parte de la base**.

**Resultado medido en el censo (2026-11-07, de 19:17 a 20:06):**
- 815 solicitudes, todas con **HTTP 200**; ninguna señal de bloqueo.
- Plataformas vigentes: Inversiones.io 69/69 meses, Prestopolis 69/69 y Securite 68/69 (falta 2024-05 tras 2 intentos).
- Plataformas retiradas: Afluenta 33/69, Inversiones Neurona 39/69 y Proyecto Crowd 0/69 (omitida tras 2 meses sin grilla).
- Patrón: reutilizando el estado del formulario acertaron 11 de 113 intentos (≈ 10 %); con estado recién cargado (GET más la casilla «Retiradas»), 61 de 127 (≈ 48 %). La falla es intermitente, no permanente.
- El portal fija las cookies `ASP.NET_SessionId` y las de su firewall de aplicaciones (`HWWAFSESID`, `HWWAFSESTIME`). La hipótesis más probable es un balanceo entre servidores que no comparten el estado de sesión. **No se intentó manipular el firewall.**
- Cambio aplicado en `02_scraping_web.py`: para las retiradas se carga un estado nuevo antes de cada intento, con un máximo de 3 intentos por mes.

**Pasada de recuperación (`--reanudar`, 2026-11-08, de 13:29 a 14:21):** con estado recién cargado antes de cada intento y hasta 3 intentos por mes.
- 836 solicitudes, todas con **HTTP 200**; ninguna señal de bloqueo.
- Recuperados: Securite 1 mes (queda completa, 69/69), Afluenta 25 (58/69), Inversiones Neurona 22 (61/69) y Proyecto Crowd 48 (48/69).
- **Cobertura final: 374 de 414 plataforma-mes (90,3 %).** Siguen sin obtenerse 40 meses, todos de plataformas retiradas (Afluenta 11, Neurona 8 y Proyecto Crowd 21), tras 3 intentos cada uno. En la base procesada figuran como `estado_simv = no_obtenido` y nunca se imputan.

**Validación externa de la cobertura:** los totales anuales de la base coinciden con las cifras de la SMV citadas en prensa (usadas solo como contraste, no como datos):

| Año | Proyectos financiados (base) | SMV (prensa) | Monto financiado (base) | SMV (prensa) |
|---|---|---|---|---|
| 2024 | 252 | 253 | S/ 54,28 M | S/ 54,5 M |
| 2025 | 432 | 432 | S/ 120,28 M | S/ 120,3 M |

La cobertura que falta pesa muy poco en esos años: en 2024, 1 proyecto y unos S/ 0,22 M.

**Decisión y efecto en el estudio:**
- El censo mensual del SIMV cubre las **plataformas vigentes** (Inversiones.io, Prestopolis y Securite).
- Las plataformas retiradas se caracterizan con sus **estados financieros trimestrales** (API OData de la SMV, vía 1), que sí están completos para las seis.
- Los totales del FPF del SIMV son, por tanto, una **cota inferior** del sistema en los periodos en que operaron plataformas hoy retiradas. Se declarará como limitación en el artículo.
- El script `02_scraping_web.py --reanudar` reintenta solo las consultas faltantes, por si el portal vuelve a responder antes de la entrega.

**Docente informado (2026-11-07):** está de acuerdo con este tratamiento, sin sustitución de fuente.

---

## Fuentes evaluadas y descartadas antes de declararse (Fase I)

No forman parte de la base y no requieren sustitución. Se registran por transparencia.

| Fuente | URL | Fecha | HTTP / mensaje | Motivo |
|---|---|---|---|---|
| SBS, tasas activas por tipo de crédito y empresa | https://www.sbs.gob.pe/app/pp/EstadisticasSAEEPortal/Paginas/TIActivaTipoCreditoEmpresa.aspx?tip=B | 2026-11-07 | HTTP 200 con desafío anti-bot (`/_Incapsula_Resource`, 212 bytes) | Protección anti-bot: eludirla está prohibido |
| BCRP, Reporte de Estabilidad Financiera (PDF) | https://www.bcrp.gob.pe/docs/Publicaciones/Reporte-Estabilidad-Financiera/2025/mayo/ref-mayo-2025.pdf | 2026-11-07 | HTTP 200 con página «Pardon Our Interruption» (no es PDF) | Protección anti-bot |
| Datos Abiertos, API CKAN `package_search` (endpoint del temario) | https://www.datosabiertos.gob.pe/api/3/action/package_search | 2026-11-07 | HTTP 404 | Endpoint inexistente; además, no hay datasets de crowdfunding |

## Incidencias propias durante los sondeos (transparencia ética)

- **Datos Abiertos:** 7 consultas a la API espaciadas 1,2 s antes de leer su `Crawl-delay: 10`, y 1 solicitud a `/search/` (ruta prohibida por su robots.txt). Las consultas posteriores respetaron 10,5 s.
- **Scimago:** 1 solicitud a `journalrank.php?out=xls` (ruta prohibida por su robots.txt) antes de leerlo; respondió 403. No se repitió.
- **SIMV-SMV:** unas 20 solicitudes de diagnóstico de la Incidencia 1, con pausas de 3 s.
