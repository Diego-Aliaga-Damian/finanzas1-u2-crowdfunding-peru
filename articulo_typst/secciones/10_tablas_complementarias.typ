// Traducido automáticamente de articulo/secciones/10_tablas_complementarias.tex por herramientas/articulo/generar_typst.py.
// Para cambiar el texto, edita el .tex y vuelve a ejecutar el script (o edita aquí y deja de regenerar).
#import "../generado/cifras.typ": cifra
#import "../generado/tablas.typ": *
#import "../estilo.typ": *

== Tablas complementarias

#tabla_apa_fija(t1_plataformas,
  titulo: [Sociedades administradoras de plataformas de financiamiento participativo financiero, 2021-2026],
  nota: [«Meses obtenidos» son las consultas válidas al portal sobre 69 posibles. EEFF = estados financieros presentados a la SMV. Elaboración propia con datos de la #cite(<smvsimv2026>, form: "prose") y de la API OData de la SMV @smvodata2026.],
) <tab-plataformas>

#tabla_apa_fija(t3_plataformas_financieros,
  titulo: [Indicadores financieros de las sociedades administradoras por año],
  nota: [Montos en miles de soles. El ROA anualiza la utilidad de los trimestres disponibles. En los registros reportados en soles, la escala se corrigió solo cuando la empresa tenía trimestres de referencia; si no los tenía, los saldos se omiten (—). Elaboración propia con datos de la API OData de la SMV @smvodata2026 y de la #cite(<smvsimv2026>, form: "prose").],
) <tab-financieros>

#tabla_apa_fija(t4_condiciones_por_receptor,
  titulo: [Condiciones de acceso y de monto por tipo de receptor, antes y después de la modificación del reglamento],
  nota: [El periodo empieza en #cifra("inicioFPF")\; «después» comprende de diciembre de 2025 a septiembre de 2026. Los intervalos de Wilson suponen proyectos independientes. Elaboración propia con datos de la #cite(<smvsimv2026>, form: "prose").],
) <tab-condiciones>

#tabla_apa_fija(t7_comparacion_segmentos,
  titulo: [Monto medio de los proyectos de financiamiento participativo y tasas del crédito tradicional por periodo],
  nota: [Las tasas son promedios simples de las tasas efectivas anuales mensuales. El año 2025 se divide por el salto de la tasa bancaria de pequeña y microempresa en marzo. Los montos medios del FPF y las tasas no miden el mismo concepto; se presentan juntos como contexto y no como comparación de precios. Elaboración propia con datos de la #cite(<smvsimv2026>, form: "prose") y de #cite(<bcrpdata2026>, form: "prose").],
) <tab-segmentos>

#tabla_apa_fija(t8_sensibilidad,
  titulo: [Pruebas no paramétricas y análisis de sensibilidad],
  nota: [M = millones de soles. E1 usa primeras diferencias mensuales. Elaboración propia con datos de la SMV @smvsimv2026 @smvodata2026 y del BCRP @bcrpdata2026.],
) <tab-sensibilidad>
