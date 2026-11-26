// Traducido automáticamente de articulo/secciones/01_puntos_clave.tex por herramientas/articulo/generar_typst.py.
// Para cambiar el texto, edita el .tex y vuelve a ejecutar el script (o edita aquí y deja de regenerar).
#import "../generado/cifras.typ": cifra
#import "../generado/tablas.typ": *
#import "../estilo.typ": *

#puntos_clave((
  [En todas las variables de las pruebas econométricas se alcanza el tamaño mínimo de muestra: #cifra("muSeriesObs") meses para las series de tiempo, #cifra("muProyObs") proyectos para el logit y #cifra("muCompObs") observaciones empresa-trimestre para comparar la rentabilidad.],
  [El monto anual del FPF subió de S/~#cifra("monto2022") millones en 2022 a S/~#cifra("monto2025") millones en 2025. Una sola plataforma reúne el #cifra("participacionLider")~% del monto.],
  [Con #cifra("muSeriesObs") meses de datos, el FPF no está cointegrado con las tasas de bancos y cajas, y en el corto plazo las tasas tampoco son significativas en conjunto.],
  [No se encuentra un efecto positivo de la modificación del reglamento de 2025 sobre el monto, que ya crecía antes y después perdió ritmo.],
  [Los proyectos empresariales logran financiarse con más frecuencia, aunque la ventaja disminuye cuando se controla por plataforma y año.],
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
