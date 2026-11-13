// Diego Sebastián Aliaga Damián
// 2024200481M
// Tema 96: Fintech y financiamiento participativo (crowdfunding) en el Perú: oferta y condiciones
// Versión Typst del artículo (formato APA 7). Las secciones se traducen desde articulo/secciones/*.tex y las cifras,
// tablas y anexos se generan con herramientas/articulo/generar_typst.py. Compilación (desde la raíz del proyecto):
//   python herramientas/articulo/generar_typst.py
//   typst compile articulo_typst/articulo.typ --root .
#import "generado/cifras.typ": cifra
#import "generado/anexo.typ": *
#import "estilo.typ": *

#set document(title: "Fintech y financiamiento participativo (crowdfunding) en el Perú: oferta y condiciones, 2022-2026",
              author: "Diego Sebastián Aliaga Damián")
// APA 7: A4, márgenes de 2,54 cm, Times New Roman 12, doble espacio y número de página arriba a la derecha
#set page(paper: "a4", margin: 2.54cm,
          header: context align(right, text(size: 12pt, counter(page).display())), header-ascent: 45%)
#set text(font: "Times New Roman", size: 12pt, lang: "es", region: "pe")
#set par(leading: 1.25em, spacing: 1.25em, justify: true, first-line-indent: (amount: 1.27cm, all: true))
#set list(indent: 0.6cm)
#set enum(indent: 0.6cm)

// Títulos APA: nivel 1 centrado y en negrita; nivel 2 a la izquierda en negrita; nivel 3 en negrita cursiva
#show heading: set text(size: 12pt)
#show heading.where(level: 1): it => block(above: 1.4em, below: 1.25em, width: 100%, align(center, strong(it.body)))
#show heading.where(level: 2): it => block(above: 1.4em, below: 1.25em, strong(it.body))
#show heading.where(level: 3): it => block(above: 1.4em, below: 1.25em, strong(emph(it.body)))

// Tablas y figuras: «Tabla N» en negrita y el título en cursiva, ambos arriba y alineados a la izquierda
#set figure(gap: 6pt)
#show figure.caption: it => block(width: 100%, {
  set par(first-line-indent: 0pt, justify: false, leading: 0.6em)
  set text(size: 12pt)
  align(left)[#strong[#it.supplement #context it.counter.display(it.numbering)] \ #emph(it.body)]
})
#show figure: set block(above: 1.4em, below: 1.4em)

// ---------------------------------------------------------------- Portada (estudiante, APA 7)
#page(header: context align(right, text(size: 12pt, counter(page).display())))[
  #set par(first-line-indent: 0pt, justify: false)
  #v(3cm)
  #align(center)[
    #strong[Fintech y financiamiento participativo (crowdfunding) en el Perú: oferta y condiciones, 2022-2026]
    #v(12pt)
    #strong[#emph[Fintech and Crowdfunding in Peru: Supply and Financing Terms, 2022-2026]]
    #v(2cm)
    Diego Sebastián Aliaga Damián \
    Código de matrícula 2024200481M
    #v(12pt)
    Facultad de Economía, Universidad Nacional del Centro del Perú \
    Finanzas I (055D), Unidad II, tema N.#super[o]~96 \
    Dr. Ciro Iván Machacuay Meza \
    6 de diciembre de 2026
  ]
]

#include "secciones/01_resumen_abstract.typ"
#include "secciones/02_introduccion.typ"
#include "secciones/03_antecedentes.typ"
#include "secciones/04_materiales_metodos.typ"
#include "secciones/05_resultados.typ"
#include "secciones/06_discusion.typ"
#include "secciones/07_conclusiones.typ"
#include "secciones/08_declaracion_ia.typ"

// ---------------------------------------------------------------- Referencias
#pagebreak()
= Referencias
#{
  set par(first-line-indent: 0pt, justify: false)
  bibliography("generado/referencias.bib", title: none, style: "apa")
}

// ---------------------------------------------------------------- Anexo
#pagebreak()
= Anexo. Datos y código
#{
  set text(size: 9.5pt)
  set par(leading: 0.55em, first-line-indent: 0pt, justify: false)
  [== Repositorio, fechas y verificación]
  anexo_reproducibilidad
  [== Fuentes, endpoints y parámetros de extracción]
  anexo_endpoints
  [== Diccionario de variables]
  set text(size: 8pt)
  anexo_diccionario
}
