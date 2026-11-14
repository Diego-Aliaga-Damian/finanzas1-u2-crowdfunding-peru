// Diego Sebastián Aliaga Damián · 2024200481M
// Tema 96: Fintech y financiamiento participativo (crowdfunding) en el Perú: oferta y condiciones
// Paleta y componentes del diseño de revista (igual que la versión LaTeX) con formato APA 7: recuadros de resumen,
// puntos clave y abreviaturas; letra capital; tablas y figuras a todo el ancho (número en negrita, título en
// cursiva arriba y nota debajo).

// Paleta: azul marino institucional con acento dorado
#let marino = rgb("#1B3A6B")
#let azulmedio = rgb("#2E6DB4")
#let celeste = rgb("#EEF3FA")
#let celestefila = rgb("#F4F7FC")
#let dorado = rgb("#C9A227")
#let gristexto = rgb("#4A5568")
#let grislinea = rgb("#C9D3E1")

// Recuadro de Resumen o Abstract del bloque de título (letra de 10 pt e interlineado sencillo, como en las revistas)
#let resumen_bloque(titulo: [], cuerpo) = block(width: 100%, {
  set text(size: 10pt)
  set par(leading: 0.55em, spacing: 0.7em, first-line-indent: 0pt, justify: true)
  text(fill: marino, weight: "bold", upper(titulo))
  v(2pt)
  cuerpo
})

#let palabras_clave(etiqueta, palabras) = block(above: 0.9em, [#text(fill: marino, weight: "bold")[#etiqueta:] #palabras])

// Puntos clave: barra de título en marino y fondo celeste con filete izquierdo
#let puntos_clave(items) = block(width: 100%, above: 0.4em, below: 1.2em, breakable: true, {
  block(width: 100%, fill: marino, inset: (x: 8pt, y: 5pt), radius: (top: 2pt), below: 0pt,
        text(fill: white, weight: "bold", size: 10.5pt)[Puntos clave])
  block(width: 100%, fill: celeste, inset: (left: 9pt, right: 8pt, y: 7pt), radius: (bottom: 2pt), above: 0pt,
        stroke: (left: 3pt + marino), {
    set text(size: 10.5pt)
    set par(leading: 0.62em, first-line-indent: 0pt, justify: true)
    list(marker: text(fill: azulmedio, size: 7pt)[■], spacing: 0.75em, indent: 0pt, body-indent: 0.55em, ..items)
  })
})

// Abreviaturas: recuadro con borde fino y la sigla en marino
#let abreviaturas(pares) = block(width: 100%, above: 0.2em, below: 1.3em, breakable: true, stroke: 0.6pt + grislinea,
  radius: 2pt, clip: true, {
  block(width: 100%, fill: celeste, inset: (x: 8pt, y: 5pt), below: 0pt,
        text(fill: marino, weight: "bold", size: 10.5pt)[Abreviaturas])
  block(width: 100%, inset: (x: 8pt, y: 6pt), above: 0pt, {
    set text(size: 9.5pt)
    set par(leading: 0.5em, first-line-indent: 0pt, justify: false)
    grid(columns: (auto, 1fr), column-gutter: 8pt, row-gutter: 5pt,
         ..pares.map(((sigla, texto)) => (text(fill: marino, weight: "bold", sigla), texto)).flatten())
  })
})

// Letra inicial destacada (inicial elevada) al comienzo de la introducción
#let letra_capital(letra, resto) = [#text(size: 2.6em, fill: marino, weight: "bold", top-edge: "cap-height", letra)#smallcaps(resto)]

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
  scope: "parent",  // a todo el ancho de la página, sobre las dos columnas
  caption: figure.caption(position: top, titulo),
  block(width: 100%, {
    set text(size: 9.5pt, hyphenate: true)  // con columnas angostas, las palabras largas deben poder dividirse
    set par(leading: 0.5em, first-line-indent: 0pt, justify: false)
    // Filas alternadas en celeste y filetes en marino (APA 7 admite filetes horizontales y sombreado discreto)
    set table(fill: (_, y) => if y > 0 and calc.even(y) { celestefila }, inset: (x: 3.5pt, y: 3.4pt))
    set table.hline(stroke: marino)
    cuerpo
    if nota != none { nota_apa(nota) }
  }),
)

#let figura_apa(imagen, titulo: [], nota: none) = figure(
  kind: image,
  supplement: [Figura],
  placement: auto,
  scope: "parent",
  caption: figure.caption(position: top, titulo),
  block(width: 100%, {
    align(center, imagen)
    if nota != none { nota_apa(nota) }
  }),
)
