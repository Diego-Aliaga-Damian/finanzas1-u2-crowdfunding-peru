// Diego Sebastián Aliaga Damián · 2024200481M
// Tema 96: Fintech y financiamiento participativo (crowdfunding) en el Perú: oferta y condiciones
// Funciones de tablas y figuras con formato APA 7 (número en negrita, título en cursiva arriba y nota debajo).

#let nota_apa(nota) = {
  v(4pt)
  align(left, block(width: 100%, {
    set text(size: 10pt)
    set par(leading: 0.55em, first-line-indent: 0pt, justify: false)
    [_Nota._ #nota]
  }))
}

#let tabla_apa(cuerpo, titulo: [], nota: none) = figure(
  kind: table,
  supplement: [Tabla],
  placement: auto,
  caption: figure.caption(position: top, titulo),
  block(width: 100%, {
    set text(size: 9.5pt, hyphenate: true)  // con columnas angostas, las palabras largas deben poder dividirse
    set par(leading: 0.5em, first-line-indent: 0pt, justify: false)
    cuerpo
    if nota != none { nota_apa(nota) }
  }),
)

#let figura_apa(imagen, titulo: [], nota: none) = figure(
  kind: image,
  supplement: [Figura],
  placement: auto,
  caption: figure.caption(position: top, titulo),
  block(width: 100%, {
    align(center, imagen)
    if nota != none { nota_apa(nota) }
  }),
)
