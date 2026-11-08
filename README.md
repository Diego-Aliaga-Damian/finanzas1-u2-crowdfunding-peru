# Fintech y financiamiento participativo (crowdfunding) en el Perú: oferta y condiciones

**Finanzas I (055D) · Unidad II · Facultad de Economía · Universidad Nacional del Centro del Perú · 2026-II**

| Dato | Valor |
|---|---|
| Estudiante | Diego Sebastián Aliaga Damián |
| Código de matrícula | 2024200481M |
| Tema del temario | N.º 96: Fintech y financiamiento participativo (crowdfunding) en el Perú: oferta y condiciones |
| Docente | Dr. Ciro Iván Machacuay Meza |
| Repositorio | https://github.com/Diego-Aliaga-Damian/finanzas1-u2-crowdfunding-peru |

> **Estado: en construcción (Fase III).** Este README se completa en cada fase. Lo que todavía no existe figura como *pendiente*.

## Objetivo

Caracterizar la oferta de financiamiento participativo financiero (FPF) en el Perú y comparar sus condiciones con las del sistema crediticio tradicional, entre 2022 y 2026.

## Fuentes y endpoints (numeral 2.4.1: dos vías obligatorias)

| Vía | Institución y base | Endpoint o URL | Script | Estado |
|---|---|---|---|---|
| API | BCRP, BCRPData (series mensuales) | `https://estadisticas.bcrp.gob.pe/estadisticas/series/api/{códigos}/json/{inicio}/{fin}` | `01_extraccion_api.py` | Implementado |
| API | SMV, API OData de información financiera de empresas supervisadas | `https://mvnet.smv.gob.pe/SMV.OData.Api/api/InfFinanciera/PrincipalCuentaSMV?sEjercicio={AAAA}&sPeriodo={1-4}&sTipoInf=I` | `01_extraccion_api.py` | Implementado |
| Scraping | SMV, portal SIMV, «Información de Proyectos» de FPF | `https://www.smv.gob.pe/SIMV/Frm_ProyectosFPF?data=785FE29A0201FCD759A08F94A0F74DBB4FD1B4D805` | `02_scraping_web.py` | Pendiente |

Series del BCRP: PN07807NM (TAMN); PN07843NM y PN07844NM (bancos, pyme ≤360 d y >360 d); PN07846NM y PN07847NM (bancos, consumo ≤360 d y >360 d); PN07861NM y PN07862NM (cajas municipales, pyme); PN07879NM y PN07880NM (cajas rurales, pyme); PN38705PM (IPC de Lima Metropolitana, dic. 2021 = 100).

## Parámetros congelados de la consulta (numeral 2.4.5)

- `FECHA_INICIO = 2021-01`
- `FECHA_CORTE = 2026-09`

Están declarados como constantes al inicio de los scripts, no como fechas dinámicas.

## Requisitos

- Python 3.14.7; versiones exactas de las librerías en `requirements.txt`.
- Ninguna fuente exige clave de API. `.env.example` es una plantilla opcional (contacto del User-Agent y pausa).

## Ejecución (Windows · PowerShell o terminal de VS Code)

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python codigo\01_extraccion_api.py
```

Orden completo de ejecución: `01_extraccion_api.py` → `02_scraping_web.py` (pendiente) → `03_limpieza_datos.py` (pendiente) → `04_analisis.py` (pendiente).

## Estructura

```
codigo/            scripts 01-04 y comun.py (funciones compartidas)
datos_crudos/      respuestas originales (JSON/HTML) y CSV crudos, sin editar
datos_procesados/  datos_procesados_2024200481M.csv (pendiente)
salidas/           tablas y figuras generadas por 04_analisis.py (pendiente)
pruebas/           pruebas automatizadas (pendiente)
docs/              matriz de cumplimiento, diagnóstico (Fase I), diseño y antecedentes (Fase II)
herramientas/      búsqueda bibliográfica reproducible (no forma parte de la base de datos)
log_ejecucion.txt  fecha y hora, código HTTP, filas y SHA-256 de cada extracción
```

## Integridad y reproducibilidad

- Cada crudo se registra con su SHA-256 en `log_ejecucion.txt`.
- Los crudos se escriben de forma atómica: una descarga fallida o vacía nunca reemplaza un crudo válido.
- Los datos se versionan sin conversión de fines de línea (`.gitattributes`), para que el hash coincida en cualquier sistema operativo.
- **SHA-256 de `datos_procesados_2024200481M.csv`: pendiente** (se declarará cuando exista el archivo).

## Ética de la extracción (numeral 2.4.8)

Solo información pública y agregada, sin datos personales (Ley N.º 29733). User-Agent identificable, pausa de 1 s o más entre solicitudes (3 s en el portal SIMV) y respeto de robots.txt y de las protecciones anti-bot: las fuentes que las aplican se descartaron, no se eludieron.

## Uso de inteligencia artificial

El proyecto se desarrolla con apoyo de un asistente de IA (Claude, de Anthropic) para escribir y depurar código, buscar y verificar fuentes y redactar documentación. Las decisiones metodológicas, la verificación de los resultados y la defensa del trabajo son responsabilidad del estudiante.
