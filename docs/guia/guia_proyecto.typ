// Guía completa del proyecto: qué se hizo, cómo y por qué (explicación desde cero).
// Compilación (desde la raíz del proyecto): typst compile docs/guia/guia_proyecto.typ --root .

#let marino = rgb("#1B3A6B")
#let azul = rgb("#2E6DB4")
#let celeste = rgb("#EEF3FA")
#let dorado = rgb("#C9A227")
#let gris = rgb("#4A5568")
#let verde = rgb("#047857")
#let verdesuave = rgb("#ECFDF5")
#let coral = rgb("#BE123C")
#let coralsuave = rgb("#FFF1F2")
#let ambar = rgb("#B45309")
#let ambarsuave = rgb("#FFFBEB")

#set document(title: "Guía completa del proyecto FPF Perú", author: "Diego Sebastián Aliaga Damián")
#set page(paper: "a4", margin: (top: 2.4cm, bottom: 2.2cm, x: 2.2cm),
  header: context {
    if here().page() > 1 {
      set text(size: 8.5pt, fill: gris)
      grid(columns: (1fr, auto), [Guía completa del proyecto · Fintech y crowdfunding en el Perú], [Página #counter(page).display()])
      v(-5pt)
      line(length: 100%, stroke: 0.4pt + rgb("#C9D3E1"))
    }
  })
#set text(font: ("Calibri", "Segoe UI", "Arial"), size: 11pt, lang: "es", region: "pe")
#set par(justify: true, leading: 0.68em, spacing: 1.05em)
#set heading(numbering: "1.1")
#show heading.where(level: 1): it => {
  pagebreak(weak: true)
  block(below: 1em, {
    text(size: 10pt, fill: azul, weight: "bold", tracking: 0.08em)[CAPÍTULO #counter(heading).display("1")]
    v(-4pt)
    text(size: 20pt, fill: marino, weight: "bold", it.body)
    v(-6pt)
    line(length: 3cm, stroke: 1.4pt + dorado)
  })
}
#show heading.where(level: 2): it => block(above: 1.4em, below: 0.7em,
  text(size: 13.5pt, fill: marino, weight: "bold")[#counter(heading).display() #h(0.3em) #it.body])
#show heading.where(level: 3): it => block(above: 1.1em, below: 0.5em, text(size: 11.5pt, fill: azul, weight: "bold", it.body))
#show raw: set text(font: ("Consolas", "Courier New"), size: 9.5pt)
#show raw.where(block: true): it => block(width: 100%, fill: rgb("#F4F6FA"), inset: 9pt, radius: 3pt,
  stroke: (left: 2.5pt + azul), text(size: 8.4pt, it))
#show link: set text(fill: azul)
#set table(stroke: (_, y) => if y == 0 { (top: 0.8pt + marino, bottom: 0.8pt + marino) } else { (bottom: 0.3pt + rgb("#D5DCE6")) },
  fill: (_, y) => if y == 0 { celeste }, inset: (x: 6pt, y: 5pt))
#show table.cell.where(y: 0): set text(weight: "bold", fill: marino)
#show table: set text(size: 9.5pt)
#show table: set par(justify: false)

#let caja(titulo, cuerpo, color: azul, fondo: celeste) = block(width: 100%, fill: fondo, inset: 10pt, radius: 3pt,
  stroke: (left: 3pt + color), breakable: true,
  [#text(weight: "bold", fill: color)[#titulo] \ #cuerpo])
#let idea(c) = caja("En pocas palabras", c)
#let ojo(c) = caja("Atención", c, color: coral, fondo: coralsuave)
#let bien(c) = caja("Verificado", c, color: verde, fondo: verdesuave)
#let nota(c) = caja("Nota", c, color: ambar, fondo: ambarsuave)

// ============================================================================ PORTADA
#page(header: none, margin: 0pt)[
  #block(width: 100%, height: 9.5cm, fill: marino, inset: (x: 2.2cm, y: 1.8cm), {
    set text(fill: white)
    grid(columns: (auto, 1fr, auto), align: horizon,
      box(fill: white, inset: 5pt, radius: 4pt, image("/productos/posteres_articulos/img/logo_uncp.png", height: 1.6cm)),
      align(center)[#text(size: 13pt, weight: "bold")[Universidad Nacional del Centro del Perú] \ #text(size: 10.5pt)[Facultad de Economía · Finanzas I (055D) · Unidad II · 2026-II]],
      box(fill: white, inset: 5pt, radius: 4pt, image("/productos/posteres_articulos/img/logo_facultad.png", height: 1.6cm)))
    v(1.2cm)
    text(size: 11pt, tracking: 0.12em, weight: "bold", fill: rgb("#E8C766"))[GUÍA COMPLETA DEL PROYECTO]
    v(0.2cm)
    text(size: 25pt, weight: "bold")[Todo lo que se hizo, explicado desde cero]
  })
  #block(width: 100%, inset: (x: 2.2cm, y: 1.2cm), {
    text(size: 15pt, weight: "bold", fill: marino)[Fintech y financiamiento participativo (crowdfunding) en el Perú: oferta y condiciones, 2022-2026]
    v(0.5cm)
    grid(columns: (auto, 1fr), column-gutter: 1em, row-gutter: 0.6em,
      text(fill: gris)[Estudiante], [Diego Sebastián Aliaga Damián (2024200481M)],
      text(fill: gris)[Tema], [N.º 96 del temario],
      text(fill: gris)[Docente], [Dr. Ciro Iván Machacuay Meza],
      text(fill: gris)[Entrega], [6 de diciembre de 2026, 23:59 (carpeta EXANTE)],
      text(fill: gris)[Repositorio], link("https://github.com/Diego-Aliaga-Damian/finanzas1-u2-crowdfunding-peru")[github.com/Diego-Aliaga-Damian/finanzas1-u2-crowdfunding-peru],
      text(fill: gris)[Dashboard], link("https://fincrowd-peru-diego-aliaga.streamlit.app/")[fincrowd-peru-diego-aliaga.streamlit.app],
      text(fill: gris)[Fecha de la guía], [17 de noviembre de 2026],
    )
    v(0.8cm)
    caja("Para qué sirve esta guía", [Explica, paso a paso y sin dar nada por sabido, cada parte del trabajo: de dónde salen los datos, qué hace cada script, cómo se calculó cada resultado, cómo se armaron el artículo, los pósteres, el Beamer y el dashboard, qué se verificó y qué falta. Sirve para estudiar el proyecto, para defenderlo en la exposición (la consigna exige explicar el código) y para retomarlo sin depender de nadie.])
    v(0.4cm)
    text(size: 9.5pt, fill: gris)[Elaborada con apoyo de Claude (Anthropic), el asistente de IA que acompañó el desarrollo del proyecto. Las cifras provienen de los archivos del repositorio y se cotejaron con las salidas del análisis.]
  })
]

// ============================================================================ ÍNDICE
#page(header: none)[
  #text(size: 20pt, weight: "bold", fill: marino)[Contenido]
  #v(-4pt)
  #line(length: 3cm, stroke: 1.4pt + dorado)
  #v(0.4cm)
  #show outline.entry.where(level: 1): it => { v(0.35em); strong(it) }
  #outline(title: none, depth: 2, indent: 1.2em)
]

// ============================================================================ 1
= El proyecto en una página

== La pregunta y los objetivos
El trabajo responde una pregunta: *¿cómo es la oferta de financiamiento participativo financiero (FPF, el crowdfunding regulado por la SMV) en el Perú entre 2022 y 2026, y cómo se comparan sus condiciones con las del crédito tradicional de bancos y cajas?*

Para responderla se plantearon cuatro objetivos específicos:
+ *Oferta:* describir su evolución y estructura (plataformas, proyectos, montos, tipo de receptor, concentración).
+ *Plataformas:* caracterizar la situación financiera de las sociedades administradoras y aproximar su costo de intermediación.
+ *Acceso y reforma:* medir las condiciones de acceso por tipo de receptor y contrastarlas antes y después de la modificación del reglamento de noviembre de 2025.
+ *Comparación:* situar esas condiciones frente a las del crédito tradicional en segmentos equivalentes.

Y dos hipótesis, más una relación exploratoria:
- *H1:* el monto mensual financiado es mayor después de la modificación del reglamento.
- *H2:* la tasa de colocación (financiados ÷ publicados) difiere entre proyectos empresariales y personales.
- *E1 (exploratoria):* los cambios mensuales del monto se asocian con los de las tasas del crédito tradicional.

== Los resultados principales
#table(columns: (1.3fr, 2.2fr),
  [Tema], [Resultado],
  [Base de datos], [Panel de *414 observaciones plataforma-mes* (6 plataformas × 69 meses, de enero de 2021 a septiembre de 2026) y 35 columnas, construido con 2 API y 1 rastreo web. Cobertura del portal: 90.3 % (374 de 414).],
  [Crecimiento], [El monto anual pasó de *S/ 6.46 millones* (2022) a *S/ 120.28 millones* (2025). En enero-septiembre de 2026 sumó S/ 104.71 millones, 14.7 % más que en los mismos meses de 2025.],
  [Concentración], [De 6 sociedades administradoras, solo *3 financiaron proyectos*, y *Inversiones.io reúne el 98.5 %* del monto. El índice de Herfindahl-Hirschman (IHH) pasó de 8 882 (2022) a 9 977 (2025), cerca del máximo de 10 000.],
  [Acceso (H2)], [Proyectos empresariales financiados en el *89.5 %* de los casos y personales en el *51.4 %* (z = 14.88, p < 0.001). Pero dentro de la plataforma líder la diferencia *no es significativa* (Fisher p = 0.127): la brecha refleja el modelo de negocio de cada plataforma.],
  [Reforma (H1)], [La mediana mensual sube de S/ 3.32 M a *S/ 11.37 M* (U = 387, p < 0.001), pero 5 cortes placebo también salen significativos y el crecimiento interanual cae de 169 % a 27 %: *la diferencia no es atribuible a la norma*.],
  [Rentabilidad], [Solo la líder es rentable: ROA anualizado de *30.9 %* en 2025. Sus ingresos equivalen a una mediana de *5.27 %* del monto que financia por trimestre (no es una tasa de interés).],
  [Crédito tradicional], [La TEA bancaria a pequeña y microempresa (≤ 360 días) promedió 36.0 % en 2022 y 54.4 % en 2026, con un salto de 19.3 puntos en marzo de 2025.],
  [Comparación (E1)], [Con 8 tasas comparadoras, ninguna correlación con el monto del FPF es significativa (menor p = 0.116). Como la SMV *no publica la tasa ni el plazo* de cada operación, el precio del FPF no se puede comparar con el del crédito tradicional.],
)

== Lo que se entregó
#table(columns: (1.4fr, 2fr),
  [Producto], [Dónde está],
  [Base de datos y código (4 scripts, crudos, procesado, salidas, documentación)], [Repositorio y carpeta N.º 3 de la entrega],
  [Artículo científico en LaTeX (26 páginas, APA 7, dos columnas)], [`articulo/articulo.pdf`],
  [El mismo artículo en Typst (26 páginas)], [`articulo_typst/articulo.pdf`],
  [Beamer de 10 diapositivas y su versión para imprimir], [`productos/beamer/`],
  [Póster del artículo (A0)], [`productos/poster_articulo/`],
  [20 pósteres en español de los artículos del estado del arte (A1)], [`productos/posteres_articulos/pdf/`],
  [Dashboard interactivo FinCrowd Perú (12 páginas)], [fincrowd-peru-diego-aliaga.streamlit.app],
  [Carpeta de entrega con la estructura de la consigna], [`entregas/DIEGO_SEBASTIAN_ALIAGA_DAMIAN/`],
  [16 de los 20 artículos en inglés (PDF)], [`entregas/Carpeta_1_articulos/1_originales_ingles/`],
)

// ============================================================================ 2
= Conceptos básicos para entender todo lo demás

== Del tema
- *Financiamiento participativo financiero (FPF):* modalidad de crowdfunding regulada en el Perú por el Decreto de Urgencia N.º 013-2020 y el reglamento de la SMV (2021, modificado en noviembre de 2025). Una plataforma publica proyectos de empresas o personas y muchos inversionistas ponen el dinero esperando un retorno.
- *Sociedad administradora (plataforma):* la empresa autorizada por la SMV que opera la plataforma. En el periodo hubo 6: Inversiones.io, Prestopolis y Securite (vigentes) y Afluenta, Inversiones Neurona y Proyecto Crowd (retiradas).
- *Receptor:* quien pide el dinero. Puede ser empresarial (una empresa) o personal (una persona).
- *Tasa de colocación:* de cada 100 proyectos publicados, cuántos se financiaron.
- *TEA:* tasa efectiva anual de un préstamo. Las del estudio son promedios del crédito tradicional publicados por el BCRP; no son tasas del FPF.

== De datos y programación
- *API (interfaz de programación):* un servicio que entrega datos en un formato que un programa entiende (JSON). Se le pide algo con una dirección web (endpoint) y responde con los datos.
- *Web scraping (rastreo):* un programa que abre una página web como lo haría un navegador, llena el formulario y lee la tabla que aparece.
- *Panel plataforma-mes:* una tabla con una fila por cada plataforma en cada mes. Aquí, 6 × 69 = 414 filas.
- *Hash SHA-256:* una "huella digital" de 64 caracteres que cambia si el archivo cambia aunque sea en un byte. Sirve para demostrar que la base entregada es la misma que se analizó.
- *Git y GitHub:* Git guarda el historial de cambios del proyecto (cada "commit" es una foto con fecha); GitHub lo publica en internet.
- *pytest:* herramienta que ejecuta pruebas automáticas para comprobar que el código hace lo que debe.
- *LaTeX y Typst:* lenguajes para escribir documentos con calidad de imprenta. La consigna exige LaTeX; Typst es una alternativa moderna que se agregó como versión adicional.
- *Streamlit:* librería de Python para crear páginas web interactivas (el dashboard) a partir de código.

// ============================================================================ 3
= Línea de tiempo del trabajo
El proyecto se desarrolló por fases, con un commit (foto del avance) por día en GitHub:

#table(columns: (auto, auto, 1fr),
  [Fecha], [Commit], [Qué se hizo],
  [07-nov-2026], [`9d68b50`], [Fases I a III: diagnóstico de fuentes, diseño de la investigación, búsqueda de antecedentes y extracción por API (BCRP y SMV OData).],
  [08-nov-2026], [`fedbd0f`], [Fase III: rastreo del portal SIMV (censo y reanudación), limpieza e integración de la base.],
  [09-nov-2026], [`5352138`], [Fase IV: auditoría automatizada y pruebas con respuestas simuladas.],
  [10-nov-2026], [`ce8e9f3`], [Fase V: análisis financiero, tablas y figuras del artículo.],
  [11-nov-2026], [`0a69dc1`], [Fase VIII: plantilla del artículo, Materiales y métodos, auditoría metodológica y sus correcciones.],
  [12-nov-2026], [`7074d13`], [Borrador completo del artículo (30 páginas).],
  [13-nov-2026], [`2425062`, `2bd886b`], [20 pósteres, Beamer, póster del artículo; dashboard FinCrowd Perú, versión Typst y pruebas del dashboard.],
  [14-nov-2026], [`b9f7ef1`], [Artículo con diseño de revista y dashboard más fácil de leer.],
  [14 a 15-nov], [—], [Descarga de 16 de los 20 artículos y carpeta de entrega (fuera de GitHub por derechos de autor).],
)

// ============================================================================ 4
= Cómo está organizado el proyecto
Todo vive en la carpeta `Finanzas_UII_Crowdfunding` de tu Escritorio, que es una copia del repositorio de GitHub más algunas carpetas locales.

```
Finanzas_UII_Crowdfunding/
├─ codigo/              los 4 scripts obligatorios + comun.py + auditoria.py
├─ datos_crudos/        respuestas originales de las fuentes, sin editar
├─ datos_procesados/    datos_procesados_2024200481M.csv (la base del estudio)
├─ salidas/             tablas, figuras, cifras (resultados_04.json) y reportes
├─ pruebas/             pruebas automáticas (pytest) y recortes de respuestas reales
├─ articulo/            el artículo en LaTeX (articulo.tex, secciones/, generado/)
├─ articulo_typst/      el mismo artículo en Typst
├─ productos/           Beamer, póster del artículo y los 20 pósteres
├─ dashboard/           el dashboard FinCrowd Perú (Streamlit)
├─ herramientas/        scripts de apoyo: bibliografía, artículo, pósteres, entrega
├─ docs/                diagnóstico, diseño, antecedentes, matriz de cumplimiento, esta guía
├─ entregas/            carpeta de entrega y artículos de terceros (NO se sube a GitHub)
├─ README.md            ficha del proyecto: fuentes, ejecución, hash, estructura
├─ diccionario_variables.md, incidencias_fuente.md, log_ejecucion.txt
└─ requirements.txt, .env.example, pytest.ini, .gitignore, .gitattributes
```

#idea[La regla que ordena todo: *los datos crudos nunca se editan*. Todo lo demás (base procesada, tablas, figuras, cifras del artículo, dashboard) se genera con código a partir de ellos, de modo que cualquiera puede repetirlo y obtener lo mismo.]

// ============================================================================ 5
= Fase I: elegir las fuentes de datos
La consigna (numeral 2.4.1) exige construir la base con *dos vías automatizadas*: al menos una API de una fuente oficial y un rastreo web (scraping) de un portal institucional. Antes de programar se evaluó qué fuentes servían (`docs/fase_I_diagnostico_viabilidad.md`).

== Fuentes elegidas
#table(columns: (auto, 1.2fr, 2fr),
  [Vía], [Fuente], [Qué aporta],
  [API], [BCRP · BCRPData], [10 series mensuales: tasas activas (TEA) de bancos, cajas municipales y cajas rurales para pequeña y microempresa y consumo, la TAMN y el IPC.],
  [API], [SMV · API OData], [Estados financieros trimestrales de las sociedades administradoras: activo, pasivo, patrimonio, ingresos y utilidad.],
  [Scraping], [SMV · portal SIMV, «Información de Proyectos» FPF], [Proyectos publicados, financiados y monto por plataforma, mes y tipo de receptor. Es la única fuente oficial de la actividad del FPF.],
)

== Fuentes descartadas
- *SBS (tasas por entidad):* el portal tiene protección anti-bot (Incapsula). La consigna prohíbe eludirla, así que se descartó y se usaron las tasas del BCRP.
- *Scimago:* no se accede de forma automatizada; el cuartil de las revistas se verifica a mano.
Las decisiones están documentadas en `incidencias_fuente.md`.

== Parámetros congelados
El periodo se fijó como constantes al inicio de los scripts 01, 02 y 03 (numeral 2.4.5): `FECHA_INICIO = "2021-01"` y `FECHA_CORTE = "2026-09"`. No dependen de la fecha del día, así que el resultado no cambia al volver a ejecutar.

// ============================================================================ 6
= Extracción por API: `01_extraccion_api.py`
== Qué hace
Descarga las dos API y guarda las respuestas tal como llegan (crudos) más un CSV legible de cada una.

== BCRPData (Banco Central de Reserva del Perú)
- *Endpoint:* `https://estadisticas.bcrp.gob.pe/estadisticas/series/api/{códigos}/json/{inicio}/{fin}`. Se piden las 10 series en una sola solicitud, separando los códigos con guiones; el periodo va como `2021-1` a `2026-9`.
- *Series:* PN07807NM (TAMN); PN07843NM y PN07844NM (bancos, pyme ≤ 360 y > 360 días); PN07846NM y PN07847NM (bancos, consumo); PN07861NM y PN07862NM (cajas municipales, pyme); PN07879NM y PN07880NM (cajas rurales, pyme); PN38705PM (IPC de Lima, dic. 2021 = 100).
- *Validación por nombre:* cada código va acompañado de palabras que deben aparecer en el nombre oficial que devuelve el BCRP (por ejemplo, "cajas municipales", "Pequeña y Microempresa", "Hasta 360"). Si un código cambiara de significado, el script lo detecta y no guarda nada.
- *Salidas:* `datos_crudos/bcrp/bcrp_series_mensuales.json` y `datos_crudos_2024200481M_bcrp.csv`.

== API OData de la SMV
- *Endpoint:* `https://mvnet.smv.gob.pe/SMV.OData.Api/api/InfFinanciera/PrincipalCuentaSMV` con los parámetros `sEjercicio` (año), `sPeriodo` (trimestre 1-4) y `sTipoInf=I` (información individual, no consolidada).
- Se consulta un trimestre por solicitud, de 2021-T1 a 2026-T3 (23 trimestres).
- *Validación:* la respuesta debe traer `ResponseCode = "OK"`, una lista `data` y las columnas necesarias (RUC, nombre, ejercicio, trimestre, moneda, activo, pasivo, patrimonio, ingreso y utilidad).
- *Salidas:* un JSON por trimestre en `datos_crudos/smv_odata/` y `datos_crudos_2024200481M_smv_odata.csv`.

== Protecciones comunes (`comun.py`)
- *User-Agent identificable* y *pausa mínima de 1 s* entre solicitudes (la consigna lo exige).
- *Guardado atómico:* el archivo nuevo se escribe aparte y solo reemplaza al anterior si la descarga es válida. Una descarga fallida o vacía nunca borra un crudo bueno.
- *Log:* cada solicitud queda en `log_ejecucion.txt` con fecha, hora, código HTTP, filas y SHA-256 del archivo guardado.

// ============================================================================ 7
= Rastreo del portal SIMV: `02_scraping_web.py`
== Cómo funciona la página
El portal «Información de Proyectos» es un formulario ASP.NET. Para obtener los datos de una plataforma en un mes hay que hacer lo mismo que una persona en el navegador:
+ *GET* de la página: devuelve el formulario con campos ocultos (`__VIEWSTATE`, `__EVENTVALIDATION`), que guardan el "estado" de la página.
+ Para ver las plataformas retiradas se marca la casilla *Retiradas* (un postback que recarga la lista).
+ *POST* con la plataforma, el año, el mes y el botón *Buscar*: el portal responde con la grilla de resultados.

== Campos y selectores (lo que te pueden preguntar)
#table(columns: (1.2fr, 2fr),
  [Elemento], [Nombre en la página],
  [Plataforma], [`ctl00$MainContent$cboDenominacionSocial`],
  [Año / mes], [`ctl00$MainContent$lisAnio` / `ctl00$MainContent$lisMes`],
  [Casilla de retiradas], [`ctl00$MainContent$cbxRetiradas`],
  [Botón], [`ctl00$MainContent$cbBuscar`],
  [Grilla de resultados], [`table#MainContent_grdTodos`],
  [Modalidad (préstamos o valores)], [`span[id^="MainContent_grdTodos_lblCabDato3_"]`],
  [Filas de cada modalidad], [`table[id^="MainContent_grdTodos_grdDetalle_"] tr > td`: tipo de receptor, publicados, financiados, monto],
)

== Cómo se asegura que cada dato es correcto
- *Validación de "eco":* una respuesta solo se guarda si trae la grilla *y* si el formulario devuelto confirma la plataforma, el año y el mes pedidos. Así nunca se guarda por error el resultado de otra consulta.
- Cada respuesta se guarda como HTML original (`datos_crudos/smv_simv/{id}_{AAAA}_{MM}.html`); el CSV `datos_crudos_2024200481M_smv_simv.csv` es la lectura literal de cada grilla.
- *Ética (2.4.8):* pausa de 3 s entre solicitudes, robots.txt verificado y guardado, y detención automática tras 5 fallos seguidos.

== La incidencia de las plataformas retiradas
Para las tres plataformas retiradas, el portal a veces confirmaba la consulta pero *no mostraba la grilla*. Se diagnosticó sin eludir ninguna protección: era una falla intermitente (probablemente un balanceo entre servidores que no comparten la sesión). La solución fue cargar un estado nuevo antes de cada intento, con hasta 3 intentos por mes.
- Censo (7-nov): 815 solicitudes, todas con HTTP 200. Reanudación (8-nov): 836 solicitudes, todas con HTTP 200.
- *Cobertura final: 374 de 414 plataforma-mes (90.3 %).* Los 40 meses faltantes son de plataformas retiradas y figuran como `no_obtenido`; nunca se rellenan con estimaciones.
- *Validación externa:* los totales coinciden con las cifras de la SMV citadas en prensa (2025: 432 proyectos y S/ 120.28 M en la base, frente a 432 y S/ 120.3 M).
- El docente aceptó este tratamiento el 7 de noviembre, sin sustitución de fuente.

== Modos de uso
```
python codigo/02_scraping_web.py              # censo completo (6 plataformas × 69 meses)
python codigo/02_scraping_web.py --reanudar   # solo consulta lo que falta
python codigo/02_scraping_web.py --demo       # demostración en vivo: 3 solicitudes, ≈ 15 s
```
#nota[El modo `--demo` es el que conviene usar en los *3 minutos de extracción en vivo* de la exposición: hace 3 consultas reales, escribe en `salidas/demo/` y no toca los crudos.]

// ============================================================================ 8
= Limpieza e integración: `03_limpieza_datos.py`
Este script no usa internet: lee los tres CSV crudos y construye la base procesada.

== Pasos
+ *Estados financieros (SMV):* solo las sociedades administradoras de FPF, en miles de soles; cada trimestre se asigna a su mes de cierre (marzo, junio, septiembre, diciembre). Los demás meses quedan vacíos: no se interpola.
+ *SIMV:* los textos se convierten a números; los préstamos se separan por tipo de receptor (`_emp`, `_per`) y la modalidad valores va aparte (`_valores`). La fila TOTAL del portal se usa solo como control.
+ *BCRP:* "Ene.2021" pasa a "2021-01" y "n.d." a vacío; el valor de cada mes se repite para todas las plataformas.
+ *Integración:* panel balanceado de 6 plataformas × 69 meses, con llave `ruc` + `periodo`. La variable `estado_simv` distingue `con_registros` (107), `sin_registros` (267, el portal respondió que no hubo proyectos y cuenta como cero) y `no_obtenido` (40, no se pudo leer).

== Controles automáticos (todos aprobados)
- Identidad contable activo = pasivo + patrimonio en 52 de 52 trimestres.
- Las 6 plataformas del SIMV se cruzan una a una con la API de la SMV por razón social.
- En las 107 consultas con registros, el TOTAL del portal es igual a la suma de los tipos de receptor.
- Las 10 series del BCRP están completas para los 69 meses.
- Los valores atípicos (regla de Tukey, 3 veces el rango intercuartílico) se identifican y se conservan, porque son datos oficiales.

== Resultados del script
- `datos_procesados/datos_procesados_2024200481M.csv`: *414 filas y 35 columnas*.
- `diccionario_variables.md`: nombre, definición, unidad, frecuencia, fuente y endpoint de cada variable.
- `salidas/reporte_limpieza.md`: los controles y las transformaciones.
- *SHA-256 de la base:* `cd48b21f22844cff650f5257a324b632d5afac7a009dbaceebe7456e9a7e1b8c`.

// ============================================================================ 9
= Análisis: `04_analisis.py`
Lee solo la base procesada y genera en `salidas/` las 15 tablas y 5 figuras del artículo, más `resultados_04.json` (todas las cifras clave) y `manifiesto_salidas.csv` (el SHA-256 de cada salida). Dos ejecuciones producen archivos idénticos byte a byte.

== Supuestos declarados
- *S1:* los ingresos y la utilidad de la SMV son flujos trimestrales, no acumulados.
- *S2:* los meses no obtenidos no se imputan; por eso los montos son una *cota inferior* (el valor real puede ser algo mayor). Los meses sin registros cuentan como cero.
- *S3:* la tasa de colocación se calcula sobre sumas del periodo, no mes a mes, porque un proyecto puede financiarse en un mes posterior al de su publicación.
- *S4:* asociación no implica causalidad. H1 y E1 son evidencia descriptiva.
- *S5:* algunos estados financieros se registraron en soles en lugar de miles. Se corrigen solo si la empresa tiene otros trimestres de referencia (S5a); si no, sus saldos no se usan (S5b).

== Indicadores
- *Tasa de colocación* = financiados ÷ publicados × 100.
- *IHH* = suma de las participaciones al cuadrado (en %). Va de casi 0 a 10 000 (una sola plataforma).
- *ROA* = utilidad anualizada ÷ activo medio × 100 (si el año tiene menos de 4 trimestres, se lleva a 4).
- *Ingresos ÷ monto financiado:* cuánto ingresa la plataforma por cada sol que ayuda a financiar (solo trimestres completos y años con al menos S/ 1 millón financiado).

== Las pruebas estadísticas, explicadas
#table(columns: (auto, 1.4fr, 2fr),
  [Prueba], [Qué compara], [Resultado e interpretación],
  [H1 · Mann-Whitney], [Monto mensual en los 42 meses previos frente a los 10 posteriores a diciembre de 2025.], [Mediana de S/ 3.32 M a S/ 11.37 M, p < 0.001; IC 95 % bootstrap de la diferencia: S/ 5.63 a 11.27 M (10 000 réplicas, semilla 0481).],
  [H1 · placebo], [La misma prueba con 5 fechas ficticias anteriores (2023-06 a 2025-06).], [Todas salen significativas: la prueba "detecta" cambios aunque no haya reforma. Por eso la diferencia no se atribuye a la norma.],
  [H1 · tendencia], [Crecimiento interanual antes y después; meses sobre la tendencia previa.], [Crecimiento de 169 % a 27 %; 0 de 10 meses superan la tendencia previa (8.9 % mensual, R² = 0.81).],
  [H2 · z de proporciones], [Colocación empresarial frente a personal (todo el periodo).], [89.5 % frente a 51.4 %, z = 14.88, p < 0.001; intervalos de Wilson al 95 %.],
  [H2 · Fisher], [Lo mismo, pero solo dentro de la plataforma líder.], [9 de 12 personales financiados; OR = 2.84, p = 0.127: no significativa. La brecha la explica el modelo de cada plataforma.],
  [E1 · Spearman], [Cambios mensuales del monto frente a cambios de 8 tasas, con bootstrap por bloques de 3 meses.], [Coeficientes de −0.22 a 0.01; ninguno significativo (menor p = 0.116).],
)

== Tablas y figuras que produce
#table(columns: (auto, 1fr),
  [En el artículo], [Contenido],
  [Tabla 1], [Comparabilidad entre el FPF y el crédito tradicional (qué se puede y qué no se puede comparar).],
  [Tabla 2], [Las 6 sociedades administradoras: meses obtenidos, periodo de actividad, proyectos, monto y participación.],
  [Tabla 3], [Oferta anual: plataformas activas, publicados, financiados, colocación, monto, variación, monto medio, IHH.],
  [Tabla 4], [Indicadores financieros por plataforma y año (activo, patrimonio, ingresos, utilidad, ROA, ingresos ÷ monto).],
  [Tabla 5], [Acceso y monto por tipo de receptor, antes y después de la reforma, con intervalos de Wilson.],
  [Tabla 6], [Contrastes de H1 y H2.],
  [Tabla 7], [Monto medio del FPF y tasas del crédito tradicional por periodo.],
  [Tabla 8], [Análisis de sensibilidad (18 variantes).],
  [Figuras 1 a 4], [Monto mensual por plataforma; publicados, financiados y colocación móvil; ingresos ÷ monto de la líder; tasas del crédito tradicional.],
)
#nota[Las tablas del artículo se numeran por orden de aparición. Los archivos de `salidas/tablas/` conservan su nombre de origen (por ejemplo, la Tabla 1 del artículo es `t6_comparabilidad`).]

// ============================================================================ 10
== Las pruebas econométricas, explicadas
Están en `codigo/econometria.py` y siguen la secuencia de tu trabajo de la Unidad I. Antes de estimar se verifica que *cada variable* tenga al menos 1 000 observaciones o 60 periodos.
#table(columns: (1.3fr, 1.6fr, 2fr),
  [Prueba], [Qué pregunta], [Qué salió],
  [ADF, KPSS y Zivot-Andrews], [¿La serie tiene raíz unitaria (no es estacionaria)?], [Las 7 series son I(1) según la ADF. Tres tasas son estacionarias alrededor de un quiebre (Zivot-Andrews).],
  [Engle-Granger y Johansen], [¿El monto del FPF y las tasas comparten una relación de largo plazo?], [Con 69 meses, no. Con solo los 52 meses de actividad, Engle-Granger sí rechaza con la tasa de los bancos a pymes.],
  [Granger], [¿Los cambios de una serie ayudan a predecir los de la otra?], [No en ningún sentido (menor p = 0.099).],
  [Corto plazo con errores HAC], [¿Los cambios de las tasas explican los del monto?], [No en conjunto (p = 0.595). Sin los impulsos, la tasa de cajas municipales sale significativa por un solo mes atípico.],
  [Regresión segmentada], [¿Cambió el nivel o la pendiente con la reforma?], [No hay efecto positivo; 3 de 5 cortes ficticios también son significativos.],
  [Logit], [¿Un proyecto empresarial se coloca más?], [Sí (razón 8.11), pero baja a 3.10 al controlar la plataforma y el año.],
  [Panel de empresas], [¿Las plataformas rinden distinto que otros intermediarios?], [La diferencia no es significativa al controlar el tamaño (p = 0.874).],
)
- *asinh:* seno hiperbólico inverso. Se comporta como el logaritmo, pero admite los meses con cero.
- *HAC (Newey-West):* errores estándar válidos aunque haya autocorrelación y varianza cambiante.
- *Impulso:* variable que vale 1 en un solo mes; aísla un dato atípico para que no decida el resultado.
- *Razón de momios:* cuántas veces mayores son las posibilidades de financiarse. Un valor de 1 significa que no hay diferencia.
- Las pruebas son *asociativas*: no demuestran causa y efecto, y «no significativo» no quiere decir «no existe relación».

= Verificación: pruebas, auditoría y reproducibilidad
== Pruebas automáticas (pytest)
Se ejecutan con `python -m pytest` y no necesitan internet: usan recortes de respuestas reales guardados en `pruebas/fixtures/`.
- *47 pruebas del núcleo:* extracción por API, scraping, limpieza y base procesada, análisis y econometría. Una de ellas vuelve a ejecutar `04_analisis.py` y comprueba que todas las salidas son idénticas.
- *35 pruebas del dashboard:* que sus cálculos sin filtros reproduzcan las tablas del artículo, que los filtros funcionen, que cada página cargue sin errores y que el Centro de mando 3D muestre exactamente los datos de la base.
- *Total: 82 pruebas, todas aprobadas.*

== Auditoría automatizada (`codigo/auditoria.py`)
Revisa los requisitos de la consigna (numerales 2.4.1, 2.4.2, 2.4.5, 2.4.6 y 2.4.8) y escribe `salidas/reporte_auditoria.md`. Cada control sale como cumple, no cumple o no ejecutado; un control no ejecutado nunca cuenta como cumplido. Con `--en-vivo` además coteja 10 filas al azar con el BCRP y la SMV. Último resultado: *48 controles cumplidos, 0 incumplidos*.

== Por qué el trabajo es reproducible
- El hash SHA-256 de la base está en el README y en `resultados_04.json`, y el dashboard lo recalcula cada vez que se abre.
- Cada salida tiene su hash en `manifiesto_salidas.csv`.
- Las cifras del artículo no se escriben a mano: se generan desde `resultados_04.json`.
- Los procedimientos aleatorios usan la semilla 0481 (los cuatro últimos dígitos de la matrícula).

#bien[Además se comprobó que la carpeta N.º 3 de la entrega funciona sola: dentro de esa copia, sin el resto del proyecto, las 37 pruebas del núcleo pasan.]

// ============================================================================ 11
= Estado del arte: los 20 artículos
== Cómo se eligieron
La consigna pide un estado del arte de 4 años (el docente confirmó 2023-2026) con 20 artículos en inglés de revistas Q1 o Q2 indexadas en Scopus y WoS. La búsqueda se hizo con scripts reproducibles (`herramientas/literatura/`):
+ Búsqueda en OpenAlex con palabras clave del tema (crowdfunding, P2P lending, fintech credit, regulación).
+ Selección de un núcleo de 20 por pertinencia para los cuatro objetivos.
+ Verificación de cada DOI en Crossref (autores, título, revista, año).
+ Generación automática de la bibliografía (`articulo/referencias.bib`) en formato APA 7.

El artículo cita 30 referencias: los 20 artículos, más normas (Decreto de Urgencia, resoluciones de la SMV), las fuentes de datos y notas de prensa. La justificación de cada artículo está en `docs/fase_II_B_antecedentes.md`.

== Lista
#table(columns: (auto, 1.6fr, 1.6fr, auto),
  [N.º], [Autores (año)], [Revista], [PDF],
  [01], [Braggion et al. (2025)], [Journal of Financial Economics], [Sí],
  [02], [Hau et al. (2024)], [The Journal of Finance], [Falta],
  [03], [Kim y Stähler (2026)], [Journal of Economics and Business], [Sí (doc. de trabajo)],
  [04], [Serfes et al. (2025)], [Journal of Banking & Finance], [Sí],
  [05], [Chu y Wei (2024)], [Journal of Financial and Quantitative Analysis], [Falta],
  [06], [Vives y Ye (2025)], [Journal of Financial Economics], [Sí],
  [07], [Eid et al. (2024)], [The British Accounting Review], [Sí (manuscrito aceptado)],
  [08], [Beaumont et al. (2026)], [The Review of Financial Studies], [Sí (versión de autores)],
  [09], [Ben Naceur et al. (2026)], [J. of Int. Financial Management & Accounting], [Falta],
  [10], [Onorato et al. (2024)], [Research in Int. Business and Finance], [Sí],
  [11], [Pampurini et al. (2024)], [Finance Research Letters], [Sí],
  [12], [Fasano et al. (2026)], [Journal of Economics and Business], [Sí],
  [13], [Ran et al. (2025)], [Management Science], [Sí (versión de autores)],
  [14], [Lazos (2025)], [Technological Forecasting and Social Change], [Sí],
  [15], [Danisewicz y Elard (2023)], [Journal of Banking & Finance], [Sí],
  [16], [Fareed y Viotto (2025)], [Finance Research Letters], [Sí],
  [17], [Morello (2025)], [Common Market Law Review], [Sí],
  [18], [Alvarez-Franco et al. (2026)], [J. of Economics, Finance and Admin. Science], [Sí],
  [19], [Miglo (2025)], [Journal of Economic Studies], [Sí (preprint SSRN)],
  [20], [Ma et al. (2023)], [Global Finance Journal], [Sí],
)

== Cómo se consiguieron los PDF
- 4 se descargaron con un script desde versiones de acceso abierto (OpenAlex): 01, 07, 08 y 13.
- 12 se descargaron con tu Chrome (las editoriales bloquean los programas, pero no a un navegador). En ScienceDirect tú resolviste el CAPTCHA: los CAPTCHA no se resuelven de forma automática.
- Cada PDF se verificó leyendo su primera página antes de renombrarlo como `NN_Apellido_Año.pdf`.
- El 17 era Larios-Hernández (2025), cerrado; el 25 de noviembre se reemplazó por Morello (2025), que estaba en la reserva y cuyo PDF conseguiste tú.
- *Faltan 3:* 02, 05 y 09. Los tres tienen una versión libre de los autores (SSRN o repositorio de UCLouvain); los enlaces están en `LEEME_articulos.md`.

#ojo[Los PDF de terceros tienen derechos de autor: están en `entregas/`, que no se sube a GitHub ni al dashboard.]

// ============================================================================ 12
= El artículo científico
== Estructura (numeral 2.2 de la consigna)
Título en español e inglés; resumen y palabras clave; abstract y keywords; introducción; antecedentes (marco normativo y estado del arte); materiales y métodos; resultados; discusión; conclusiones; declaración de uso de IA; referencias en APA 7 y anexo de datos y código (repositorio, endpoints, diccionario, fecha de corte y hash).

== Cifras automáticas
Ninguna cifra del texto se tecleó. El script `herramientas/articulo/generar_insumos_articulo.py` lee `salidas/resultados_04.json` y las tablas, y escribe `articulo/generado/cifras.tex` con 246 cifras. En el texto se escribe, por ejemplo, `\cifra{monto2025}` y LaTeX coloca "120.28". Si los datos cambiaran, basta con volver a ejecutar el análisis y el script.

== Diseño
Se rediseñó tomando como modelo una revista internacional (plantilla de _Geophysical Journal International_), conservando APA 7:
- *Página 1:* cabecera con los logos de la UNCP y la Facultad, título, autor, filiación, datos del trabajo y un recuadro con el Resumen y el Abstract lado a lado.
- *Dos columnas*, letra capital al inicio, recuadros de "Puntos clave" y "Abreviaturas", encabezados corridos y pie con los datos del curso.
- *APA 7:* citas y referencias (biblatex-apa), niveles de título, tablas y figuras con "Tabla N" en negrita y título en cursiva arriba y "Nota." debajo, Times de 12 puntos y sangría de 1.27 cm.
- *26 páginas* (la consigna pide de 25 a 30).

#ojo[El cuerpo usa *interlineado 1.5* para que se lea bien en dos columnas. APA 7 pide doble espacio en trabajos de estudiante; si el docente lo exige al pie de la letra, se vuelve a doble espacio cambiando una línea (`\setstretch{2}`).]

== La versión Typst
`herramientas/articulo/generar_typst.py` traduce automáticamente las secciones de LaTeX a Typst y genera las mismas cifras, tablas, anexo y bibliografía. La plantilla (`articulo_typst/articulo.typ` y `estilo.typ`) reproduce el mismo diseño. Resultado: 26 páginas.

== Cómo se compila
```
python herramientas/articulo/generar_insumos_articulo.py   # cifras y anexos de LaTeX
cd articulo
pdflatex articulo.tex ; biber articulo ; pdflatex articulo.tex ; pdflatex articulo.tex
cd ..
python herramientas/articulo/generar_typst.py              # versión Typst
typst compile articulo_typst/articulo.typ --root .
```

// ============================================================================ 13
= Pósteres y Beamer
== Los 20 pósteres del estado del arte
- Tamaño A1, tres columnas, colores verde y dorado de la UNCP, con los logos de la universidad y la facultad.
- Una plantilla común (`productos/posteres_articulos/plantilla_poster.tex`) y un archivo de contenido por artículo (`articulos/*.tex`): pregunta, datos y método, hallazgos, aporte al estudio, una figura propia, la referencia completa con su código QR y la declaración de IA.
- Se compilan todos con `python herramientas/posteres/generar_posteres.py`.

== El póster del artículo
Tamaño A0, con los elementos que pide la consigna, los dos logos, el código QR del repositorio y las fuentes en APA (`productos/poster_articulo/poster_articulo.tex`). Incluye la verificación de la muestra, la regresión segmentada de la reforma y una tabla con las pruebas econométricas principales.

== El Beamer
- *10 diapositivas* (el máximo que permite la consigna), formato 16:9, colores rojo y negro de la Facultad de Economía con su logo, tomando como base tu Beamer anterior: portada, problema e hipótesis, datos y muestra, demostración en vivo, oferta, metodología econométrica, largo plazo, corto plazo, reforma con acceso y rentabilidad, y conclusiones.
- *Versión para imprimir:* una diapositiva por hoja A4 horizontal (`beamer_impresion.tex`), porque la consigna exige llevar el Beamer impreso para cada compañero.
- Se compilan con `python herramientas/productos/compilar_productos.py`.

// ============================================================================ 14
= El dashboard FinCrowd Perú
== Qué es
Una página web interactiva hecha con Streamlit que reúne los datos, los resultados y todos los productos. El docente permitió entregarlo como enlace. Está publicado gratis en Streamlit Community Cloud: #link("https://fincrowd-peru-diego-aliaga.streamlit.app/")[fincrowd-peru-diego-aliaga.streamlit.app].

== Las 12 páginas
#table(columns: (1.3fr, 2.4fr),
  [Página], [Qué muestra],
  [Inicio], [El estudio en una frase, guía de 4 pasos, filtros, 6 tarjetas KPI con variación y minigráfico, evolución del monto, participación e IHH, hallazgos, calidad de los datos y accesos.],
  [Centro de mando 3D], [Terminal animada: superficie 3D, replay mes a mes, flujo del dinero, tablero del mes y el registro real de la extracción.],
  [Oferta y crecimiento], [Monto por plataforma (mensual, trimestral o anual; soles corrientes o reales), comparación de dos periodos, oferta anual y las 6 plataformas.],
  [Plataformas y rentabilidad], [ROA por año, ingresos ÷ monto de la líder, activo por trimestre y la tabla de indicadores.],
  [¿A quién se financia?], [Colocación por tipo de receptor con intervalos, H1 y H2 y la serie de publicados y financiados.],
  [Frente a bancos y cajas], [Tasas del BCRP (seleccionables), qué es comparable, la asociación E1 y la tabla por periodos.],
  [Pruebas econométricas], [Las tablas T9 a T15 del artículo: muestra, estacionariedad, largo y corto plazo, reforma, colocación y rentabilidad.],
  [¿Son sólidos los resultados?], [Las variantes de H1 con sus intervalos y la tabla de sensibilidad completa.],
  [Simulador de préstamo], [Cuota y costo de un préstamo con una tasa supuesta del FPF frente a la TEA observada de bancos o cajas.],
  [Datos y fuentes], [Las 3 fuentes, el mapa de respuestas del portal por mes y la base para explorar y descargar.],
  [Descargas], [El artículo (LaTeX y Typst), el Beamer, el póster y los 20 pósteres.],
  [Cómo se reproduce], [Comandos, hash de la base, reporte de auditoría y pruebas.],
)

== Cómo se usa
- *Filtros globales* (barra lateral): periodo y plataformas. Se mantienen al cambiar de página. Atajos en el inicio: Todo, 2024, 2025, 2026, últimos 12 meses y tras la reforma.
- *Etiquetas de colores:* indican la naturaleza de cada cifra: Observado (fuente oficial), Resultado del artículo (fijo), Responde a los filtros, Cota inferior, Referencia (no es un precio) e Hipotético (supuesto del usuario).
- Cada página empieza con un recuadro "En pocas palabras" y cada gráfico tiene "¿Cómo leer este gráfico?". En la barra lateral hay un *glosario* de 15 términos.
- Cada gráfico se puede descargar como imagen (PNG) y sus datos como CSV.

== El Centro de mando 3D
Es una página con estilo de terminal financiera. *Repite* los datos históricos mes a mes (enero de 2022 a septiembre de 2026); no es una transmisión en vivo. Todos los paneles se mueven juntos con la misma línea de tiempo.
- *Superficie "Costo del crédito":* cuánto interés se paga por cada S/ 100 según la TEA y el plazo. Es la fórmula del simulador evaluada en 41 tasas × 30 plazos; se rotula *Cálculo*. Las líneas de colores son las TEA *observadas* de bancos y cajas (BCRP) en el mes del replay.
- *"Monto del crowdfunding":* una columna por mes observado (SMV). Donde no hay dato, no hay columna.
- *"Tasas de bancos y cajas":* una cinta por cada una de las 9 series del BCRP. No se unen entre sí porque son categorías distintas.
- *Replay:* barras por plataforma y una franja descriptiva (media ± 1 desviación de los 12 meses *anteriores*). No es un pronóstico ni una señal de inversión.
- *¿Por dónde pasa el dinero?:* cada punto equivale a S/ 500 mil de los últimos 12 meses.
- *Consola:* una muestra de 150 líneas reales de `log_ejecucion.txt`, con su número de línea para comprobarlas.
- *Contar la historia:* recorrido guiado de 6 momentos, con cifras calculadas de la base y de `resultados_04.json`.
- *Atajos:* espacio (reproducir o pausar), flechas (mes), 1 a 3 (superficie), R (historia), F (pantalla completa).
El motor 3D no usa librerías externas. Si el navegador no tiene WebGL2, dibuja la misma escena en líneas.

El dashboard tiene modo *noche y día*: sigue el tema del sistema de quien lo abre y se cambia en el menú de los tres puntos (arriba a la derecha).

== El simulador, con sus fórmulas
- Tasa mensual equivalente: TEM = (1 + TEA)^(1/12) − 1.
- Cuota fija (sistema francés): cuota = monto × TEM ÷ (1 − (1 + TEM)^(−n)), con n meses.
- Costo efectivo anual con comisión: la tasa que iguala lo recibido (monto − comisión) con el valor actual de las cuotas, llevada a un año.
- La tasa del FPF es siempre *hipotética* (la SMV no la publica); la de bancos y cajas es *observada* (BCRP).

== Cómo está construido
#table(columns: (auto, 1fr),
  [Archivo], [Función],
  [`dashboard/app.py`], [Configuración, menú de 12 páginas y filtros de la barra lateral.],
  [`dashboard/datos.py`], [Cálculos sin Streamlit, con las mismas reglas que `04_analisis.py`: sin filtros reproduce exactamente las tablas del artículo.],
  [`dashboard/compartido.py`], [Carga de datos en memoria, estado de los filtros, glosario y formatos numéricos.],
  [`dashboard/tema.py`], [Diseño: paletas de noche y día, tipografía, tarjetas, etiquetas, recuadros y estilo de los gráficos.],
  [`dashboard/terminal_datos.py`], [Prepara los datos del Centro de mando (sin Streamlit, con pruebas).],
  [`dashboard/terminal/`], [La terminal en HTML, CSS y JavaScript: `superficie.js` (motor 3D en WebGL), `paneles.js` (replay, flujo, tablero y consola), `principal.js` (coordina todo) y `util.js`.],
  [`dashboard/vistas/*.py`], [Una página por archivo.],
)
El dashboard solo *lee* archivos del repositorio: no modifica la base ni consulta las fuentes en vivo.

== Publicación y mantenimiento
- Cada `git push` a la rama `main` actualiza la versión publicada en 2 o 3 minutos.
- Si nadie lo abre en un tiempo, *se duerme*: al abrir el enlace aparece el botón "Yes, get this app back up!" y vuelve en unos 30 segundos. Conviene abrirlo unos minutos antes de la revisión.
- Para verlo en tu computadora: `streamlit run dashboard/app.py` (se abre en http://localhost:8501).

// ============================================================================ 15
= La carpeta de entrega
== Estructura (numerales 2.3 y 2.5)
```
entregas/DIEGO_SEBASTIAN_ALIAGA_DAMIAN/
├─ LEEME.txt
├─ N1_Productos_Diego_Sebastian_Aliaga_Damian/
│  ├─ artículo LaTeX y Typst, Beamer (proyectar e imprimir), póster del artículo
│  ├─ Posteres_20_articulos_espanol/       20 de 20
│  ├─ Articulos_20_ingles_Q1_Q2/           16 de 20
│  ├─ Articulos_20_traducidos_espanol/      0 de 20
│  └─ Dashboard_FinCrowd_Peru (.url y .txt con el enlace)
├─ N2_Desarrollo_Diego_Sebastian_Aliaga_Damian/
│  └─ templates: journal LaTeX, póster, Beamer, 20 pósteres, journal Typst y código del dashboard
└─ N3_Base_de_datos_y_codigo_Diego_Sebastian_Aliaga_Damian/
   └─ codigo/, datos_crudos/, datos_procesados/, salidas/, diccionario, README, requirements,
      .env.example, log, incidencias, enlace de GitHub y pruebas/
```
- La carpeta general lleva "NOMBRES Y APELLIDOS completos"; el ZIP se llamará `ALIAGA_DAMIAN_DIEGO_SEBASTIAN_UNIDAD-II.zip` ("APELLIDOS_NOMBRES").
- Los nombres van sin tildes para evitar problemas al descomprimir en otras computadoras.

== Cómo se rearma
La carpeta la arma un script, así que no hay que copiar nada a mano. Cuando agregues traducciones o artículos en `entregas/Carpeta_1_articulos/` (originales en `1_originales_ingles/`, traducciones en `2_traducciones_espanol/` con el sufijo `_es`):
```
python herramientas/entrega/armar_entrega.py          # rearma y muestra qué falta
python herramientas/entrega/armar_entrega.py --zip    # además crea el ZIP final
```

// ============================================================================ 16
= Git, GitHub y lo que no se sube
- *Un commit por día:* tu regla. Cada commit tiene la fecha real; nunca se falsificaron fechas.
- *Qué no se sube* (archivo `.gitignore`): los PDF que se regeneran (artículo, pósteres, Beamer), los archivos intermedios de LaTeX, la carpeta `entregas/` (artículos con derechos de autor y la carpeta de entrega), el entorno `.venv/` y cualquier `.env` con datos privados.
- *`.gitattributes`:* los datos se guardan sin convertir los fines de línea, para que el hash SHA-256 sea el mismo en Windows, Linux o Mac.
- *Qué sí se sube a propósito:* `dashboard/descargas/` (los PDF que ofrece el dashboard publicado).

// ============================================================================ 17
= Cómo defender el código en la exposición
La consigna dice que durante la disertación debes explicar qué hace cada bloque del código, por qué elegiste ese endpoint o ese selector, y qué ocurriría si cambiara un parámetro. No poder explicarlo equivale a una penalización. Estas son las preguntas más probables y cómo responderlas.

#table(columns: (1.2fr, 2.2fr),
  [Pregunta], [Respuesta],
  [¿Por qué esas fuentes?], [Son oficiales y públicas. El BCRP da las tasas del crédito tradicional por segmento; la API de la SMV, los estados financieros de las plataformas; y el portal SIMV es la única fuente oficial de proyectos y montos del FPF por plataforma y mes.],
  [¿Por qué una sola solicitud al BCRP?], [El endpoint acepta varios códigos separados por guiones. Así se hace 1 solicitud en vez de 10 y se respeta la pausa.],
  [¿Qué pasa si cambio `FECHA_CORTE`?], [Cambia el periodo de toda la base: el BCRP devuelve más o menos meses, la SMV más o menos trimestres y el scraping más o menos consultas. Por eso está congelada en los scripts 01, 02 y 03, y la auditoría verifica que coincidan.],
  [¿Qué significa `sTipoInf=I`?], [Pide la información financiera *individual* de cada empresa, no la consolidada. Si se pidiera la consolidada, las cifras podrían incluir otras empresas del mismo grupo y ya no medirían solo a la plataforma.],
  [¿Por qué se usa `__VIEWSTATE`?], [El portal es un formulario ASP.NET: sin los campos ocultos que devuelve la página, el servidor rechaza el POST o devuelve otra cosa.],
  [¿Por qué el selector `table#MainContent_grdTodos`?], [Es el identificador de la tabla de resultados. Si no aparece, la respuesta no se guarda (posible error o bloqueo).],
  [¿Por qué la pausa de 3 s?], [La consigna exige al menos 1 s; con 3 s se reduce la carga sobre el portal. Si se baja, aumenta el riesgo de bloqueo.],
  [¿Qué es la validación de "eco"?], [Comprobar que el formulario devuelto tiene la misma plataforma, año y mes pedidos. Evita guardar datos de otra consulta.],
  [¿Por qué no se imputan los meses faltantes?], [Inventar datos rompería la autenticidad. Se declaran como cota inferior y T8 mide cuánto podrían cambiar los resultados (como máximo 1.7 % del monto anual).],
  [¿Cómo sé que la base no se alteró?], [Con el hash SHA-256: se recalcula y se compara con el del README. Si cambia un solo byte, el hash es distinto.],
  [¿Por qué las pruebas placebo?], [Porque el monto ya crecía antes de la reforma. Si fechas ficticias también "detectan" un cambio, la prueba no puede atribuirlo a la norma.],
)
#nota[Ensaya la demostración en vivo con `python codigo/02_scraping_web.py --demo` (≈ 15 s) y, si alcanza el tiempo, `python codigo/auditoria.py --en-vivo` para mostrar el cotejo con las fuentes.]

// ============================================================================ 18
= Lo que falta y recomendaciones
== Pendiente
#table(columns: (auto, 1.4fr, 2fr),
  [], [Tarea], [Cómo],
  [☐], [Conseguir 3 artículos (02, 05, 09)], [Biblioteca de la UNCP o versión de los autores. Si alguno no aparece, reemplazarlo por otro de la reserva (cambia también el artículo, el póster y la bibliografía).],
  [☐], [Traducir los 20 artículos al español (PDF)], [Google Translate, pestaña "Documentos". Guardarlos en `entregas/Carpeta_1_articulos/2_traducciones_espanol/` con el sufijo `_es`.],
  [☐], [Verificar el cuartil Q1/Q2 de cada revista], [En SJR (scimagojr.com) y su indexación en WoS (mjl.clarivate.com).],
  [☐], [*Reescribir el texto con tus palabras*], [Las secciones del artículo están marcadas como borrador asistido por IA. La consigna exige humanizar el contenido (similitud de 10 % como máximo) y castiga con nota cero el uso excesivo de IA no humanizada.],
  [☑], [Actualizar el estado del README], [Hecho el 17 de noviembre: estado «completo», enlace del dashboard y estructura con el artículo, el Typst, los productos y el dashboard.],
  [☐], [Armar el ZIP final y subirlo], [`armar_entrega.py --zip` y subir a ADESA antes del 6 de diciembre a las 23:59.],
  [☐], [Guardar la captura de la aceptación del docente], [Sobre la entrega por enlace y la incidencia del portal.],
  [☐], [Día de la exposición], [Ropa formal, Beamer impreso para cada compañero, ficha de evaluación impresa, abrir el dashboard minutos antes y subir el artículo al grupo (EXPOST) ese mismo día.],
)

== Recomendaciones
- Si cambias algo del texto del artículo, edita los `.tex` de `articulo/secciones/` y vuelve a compilar; luego regenera la versión Typst y actualiza el dashboard con `preparar_dashboard.py`.
- Ante cualquier duda de la consigna, la matriz `docs/matriz_cumplimiento_unidad_II.md` cita cada requisito literal con su estado.

// ============================================================================ 19
= Comandos de referencia
```
# Entorno
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt

# Datos y análisis
python codigo/01_extraccion_api.py
python codigo/02_scraping_web.py            (--reanudar | --demo)
python codigo/03_limpieza_datos.py
python codigo/04_analisis.py

# Verificación
python -m pytest
python codigo/auditoria.py                  (--en-vivo)

# Productos
python herramientas/articulo/generar_insumos_articulo.py
python herramientas/articulo/generar_typst.py
python herramientas/productos/compilar_productos.py
python herramientas/posteres/generar_posteres.py
python herramientas/productos/preparar_dashboard.py

# Dashboard y entrega
streamlit run dashboard/app.py
python herramientas/entrega/armar_entrega.py   (--zip)
```

// ============================================================================ GLOSARIO
= Glosario
#table(columns: (auto, 1fr),
  [Término], [Significado],
  [Cota inferior], [El valor real puede ser algo mayor porque hay meses que no se pudieron leer y no se rellenaron.],
  [Bootstrap], [Repetir un cálculo miles de veces con muestras al azar de los propios datos para estimar un intervalo de confianza.],
  [Intervalo de confianza (IC 95 %)], [Rango donde probablemente está el valor verdadero.],
  [Valor p], [Probabilidad de ver una diferencia así por azar si en realidad no hubiera diferencia. Menor que 0.05: significativa.],
  [Mann-Whitney], [Prueba que compara dos grupos sin suponer que los datos siguen una distribución normal.],
  [Prueba exacta de Fisher], [Compara proporciones cuando hay pocos casos.],
  [Spearman], [Correlación basada en el orden de los datos (de −1 a 1).],
  [IHH], [Índice de concentración de un mercado: 10 000 = una sola empresa.],
  [ROA], [Rentabilidad sobre activos: utilidad ÷ activo.],
  [TEA, TEM, TAMN], [Tasa efectiva anual, tasa efectiva mensual y tasa activa promedio en moneda nacional.],
  [UIT], [Unidad impositiva tributaria; el reglamento del FPF fija sus límites en UIT.],
  [Endpoint], [Dirección web de una API a la que se le piden datos.],
  [JSON, HTML, CSV], [Formatos de archivo: datos estructurados, páginas web y tablas de texto.],
  [ViewState], [Campo oculto de los formularios ASP.NET que guarda el estado de la página.],
  [SHA-256], [Huella digital de un archivo.],
  [Commit, push], [Guardar una foto del proyecto en Git y subirla a GitHub.],
)
