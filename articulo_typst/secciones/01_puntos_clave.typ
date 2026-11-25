// Traducido automáticamente de articulo/secciones/01_puntos_clave.tex por herramientas/articulo/generar_typst.py.
// Para cambiar el texto, edita el .tex y vuelve a ejecutar el script (o edita aquí y deja de regenerar).
#import "../generado/cifras.typ": cifra
#import "../generado/tablas.typ": *
#import "../estilo.typ": *

#puntos_clave((
  [Cada variable de las pruebas econométricas cumple el mínimo de la muestra: #cifra("muSeriesObs") meses en las series de tiempo, #cifra("muProyObs") proyectos en el logit y #cifra("muCompObs") empresas-trimestre en la comparación de rentabilidad.],
  [El monto anual del FPF subió de S/~#cifra("monto2022") millones en 2022 a S/~#cifra("monto2025") millones en 2025. Una sola plataforma reúne el #cifra("participacionLider")~% del monto.],
  [Con #cifra("muSeriesObs") meses no hay cointegración entre el FPF y las tasas de bancos y cajas, y en el corto plazo las tasas no son significativas en conjunto.],
  [La modificación del reglamento de 2025 no muestra un efecto positivo en el monto: este ya venía creciendo y luego se desaceleró.],
  [Los proyectos empresariales se colocan más, pero la ventaja se reduce al controlar la plataforma y el año.],
  [Mientras no se publiquen la tasa y el plazo por operación, el precio del FPF no se puede comparar con el del crédito tradicional.],
))

#abreviaturas((
  ("ADF", [Prueba de Dickey-Fuller aumentada]),
  ("API", [Interfaz de programación de aplicaciones]),
  ("BCRP", [Banco Central de Reserva del Perú]),
  ("EEFF", [Estados financieros]),
  ("FPF", [Financiamiento participativo financiero]),
  ("HAC", [Errores robustos a heterocedasticidad y autocorrelación]),
  ("IHH", [Índice de Herfindahl-Hirschman]),
  ("IPC", [Índice de precios al consumidor]),
  ("KPSS", [Prueba de Kwiatkowski, Phillips, Schmidt y Shin]),
  ("MCG", [Mínimos cuadrados generalizados]),
  ("ROA", [Rentabilidad sobre activos]),
  ("SIMV", [Sistema de Información del Mercado de Valores]),
  ("SMV", [Superintendencia del Mercado de Valores]),
  ("TAMN", [Tasa activa promedio en moneda nacional]),
  ("TEA", [Tasa efectiva anual]),
  ("UIT", [Unidad impositiva tributaria]),
))
