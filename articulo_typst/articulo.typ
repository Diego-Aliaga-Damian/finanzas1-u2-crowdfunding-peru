// Diego Sebastián Aliaga Damián
// 2024200481M
// Tema 96: Fintech y financiamiento participativo (crowdfunding) en el Perú: oferta y condiciones
// Versión Typst del artículo: diseño de revista académica a dos columnas (cabecera con logos, recuadro de resumen
// bilingüe, puntos clave, abreviaturas, encabezados corridos y tablas y figuras a todo el ancho) con normas APA 7
// (citas y referencias, niveles de título, tablas y figuras), igual que la versión LaTeX. Las secciones se traducen
// desde articulo/secciones/*.tex y las cifras, tablas y anexos se generan con herramientas/articulo/generar_typst.py.
// Compilación (desde la raíz del proyecto):
//   python herramientas/articulo/generar_typst.py
//   typst compile articulo_typst/articulo.typ --root .
#import "generado/cifras.typ": cifra
#import "generado/anexo.typ": *
#import "estilo.typ": *
#import "secciones/01_resumen_abstract.typ": resumenes

#set document(title: "Fintech y financiamiento participativo (crowdfunding) en el Perú: oferta y condiciones, 2022-2026",
              author: "Diego Sebastián Aliaga Damián")

#let pie = text(size: 8.5pt, fill: gristexto)[Finanzas I (055D) · Facultad de Economía · Universidad Nacional del Centro del Perú · 2026-II]
#let separador = box(height: 9pt, baseline: 1.5pt, line(angle: 90deg, length: 9pt, stroke: 0.6pt + grislinea))

// A4 a dos columnas. Encabezado: en la página 1, la línea de la revista; en las pares, número y autor; en las
// impares, título corto y número; con una línea fina debajo. Pie con los datos del curso.
#set page(paper: "a4", margin: (top: 2.5cm, bottom: 2.6cm, inside: 2cm, outside: 2cm), columns: 2,
  header-ascent: 35%, footer-descent: 40%,
  header: context {
    let n = here().page()
    set text(size: 10pt)
    if n == 1 {
      text(fill: gristexto)[_Finanzas I (055D), UNCP_ (2026) *Unidad II*, 1–#counter(page).final().first()]
    } else {
      let numero = text(size: 13pt, weight: "bold", fill: marino)[#n]
      if calc.even(n) {
        [#numero #h(0.6em) #separador #h(0.6em) #text(fill: gristexto, style: "italic")[D. S. Aliaga Damián]]
      } else {
        align(right)[#text(fill: gristexto, style: "italic")[Fintech y financiamiento participativo en el Perú] #h(0.6em) #separador #h(0.6em) #numero]
      }
      v(-4pt)
      line(length: 100%, stroke: 0.5pt + grislinea)
    }
  },
  footer: align(center, pie))
#set columns(gutter: 0.85cm)
// Times New Roman de 12 puntos, interlineado de 1,5 y sangría de 1,27 cm (APA 7)
#set text(font: "Times New Roman", size: 12pt, lang: "es", region: "pe")
#set par(leading: 1.5em, spacing: 1.5em, justify: true, first-line-indent: (amount: 1.27cm, all: true))
#set list(indent: 0.6cm)
#set enum(indent: 0.6cm)
#show link: set text(fill: azulmedio)
#show cite: set text(fill: marino)

// Títulos APA: nivel 1 centrado y en negrita (en marino, con filete dorado); nivel 2 a la izquierda en negrita;
// nivel 3 en negrita cursiva
#show heading: set par(justify: false)
#show heading.where(level: 1): it => block(above: 1.8em, below: 1.2em, width: 100%, align(center, {
  text(size: 13.5pt, weight: "bold", fill: marino, it.body)
  v(-2pt)
  line(length: 1.8cm, stroke: 1.1pt + dorado)
}))
#show heading.where(level: 2): it => block(above: 1.4em, below: 0.7em, text(size: 12pt, weight: "bold", fill: marino, it.body))
#show heading.where(level: 3): it => block(above: 1.2em, below: 0.6em,
  text(size: 12pt, weight: "bold", style: "italic", fill: azulmedio, it.body))

// Tablas y figuras: «Tabla N» en negrita (marino) y el título en cursiva, ambos arriba y alineados a la izquierda
#set figure(gap: 6pt)
#show figure.caption: it => block(width: 100%, {
  set par(first-line-indent: 0pt, justify: false, leading: 0.55em)
  set text(size: 12pt)
  align(left)[#text(fill: marino, weight: "bold")[#it.supplement #context it.counter.display(it.numbering)] \ #emph(it.body)]
})
#show figure: set block(above: 1.5em, below: 1.5em)

// ---------------------------------------------------------------- Bloque de título (a todo el ancho)
#place(top, scope: "parent", float: true, clearance: 18pt, {
  set par(first-line-indent: 0pt, justify: false, leading: 0.5em)
  // Cabecera con los logos de la universidad y de la facultad
  grid(columns: (auto, 1fr, auto), align: (left + horizon, center + horizon, right + horizon),
    image("/productos/posteres_articulos/img/logo_uncp.png", height: 1.55cm),
    [#text(size: 14.5pt, weight: "bold", fill: marino)[Universidad Nacional del Centro del Perú] \
     #text(size: 10.5pt, fill: gristexto)[Facultad de Economía · Finanzas I (055D) · Unidad II · Semestre 2026-II]],
    image("/productos/posteres_articulos/img/logo_facultad.png", height: 1.55cm))
  v(6pt)
  line(length: 100%, stroke: 2pt + marino)
  v(-8.2pt)
  line(length: 100%, stroke: 0.8pt + dorado)
  v(14pt)
  text(size: 10.5pt, weight: "bold", fill: azulmedio, tracking: 0.04em)[ARTÍCULO DE INVESTIGACIÓN]
  v(7pt)
  text(size: 20pt, weight: "bold", fill: marino)[Fintech y financiamiento participativo (crowdfunding) en el Perú: oferta y condiciones, 2022-2026]
  v(9pt)
  text(size: 14pt, style: "italic", fill: gristexto)[Fintech and Crowdfunding in Peru: Supply and Financing Terms, 2022-2026]
  v(13pt)
  text(size: 14pt)[Diego Sebastián Aliaga Damián#super(text(fill: azulmedio)[1])]
  v(3pt)
  text(size: 10pt)[#super[1] _Facultad de Economía, Universidad Nacional del Centro del Perú, Huancayo, Perú_]
  v(9pt)
  {
    set text(size: 10pt, fill: gristexto)
    let dato(etiqueta, valor) = [#text(fill: azulmedio, weight: "bold")[#etiqueta] #valor]
    [#dato[Código de matrícula][2024200481M] #h(1.5em) #dato[Tema][N.#super[o]~96] #h(1.5em) #dato[Fecha de entrega][6 de diciembre de 2026] \
     #dato[Docente][Dr. Ciro Iván Machacuay Meza]]
  }
  v(12pt)
  block(width: 100%, fill: celeste, radius: 3pt, inset: (x: 11pt, y: 10pt), stroke: (left: 3pt + marino),
        grid(columns: (1fr, 1fr), column-gutter: 1.3em, ..resumenes))
})

#include "secciones/01_puntos_clave.typ"
#include "secciones/02_introduccion.typ"
#include "secciones/03_antecedentes.typ"
#include "secciones/04_materiales_metodos.typ"
#include "secciones/05_resultados.typ"
#include "secciones/06_discusion.typ"
#include "secciones/07_conclusiones.typ"
#include "secciones/08_declaracion_ia.typ"

// ---------------------------------------------------------------- Referencias (APA 7, sangría francesa)
= Referencias
#{
  set par(first-line-indent: 0pt, justify: false, leading: 0.7em)
  bibliography("generado/referencias.bib", title: none, style: "apa")
}

// ---------------------------------------------------------------- Anexo (a una columna: tablas largas)
#page(columns: 1)[
  = Anexo. Datos y código
  #{
    set text(size: 11pt)
    set par(leading: 0.6em, first-line-indent: 0pt, justify: false)
    set table(fill: (_, y) => if y > 0 and calc.even(y) { celestefila })
    [== Repositorio, fechas y verificación]
    anexo_reproducibilidad
    [== Fuentes, endpoints y parámetros de extracción]
    anexo_endpoints
    [== Diccionario de variables]
    anexo_diccionario
  }
]
