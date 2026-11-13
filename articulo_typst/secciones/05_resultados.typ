// Traducido automáticamente de articulo/secciones/05_resultados.tex por herramientas/articulo/generar_typst.py.
// Para cambiar el texto, edita el .tex y vuelve a ejecutar el script (o edita aquí y deja de regenerar).
#import "../generado/cifras.typ": cifra
#import "../generado/tablas.typ": *
#import "../estilo.typ": *

= Resultados

== Evolución y estructura de la oferta

En el periodo, #cifra("plataformasAutorizadas") sociedades administradoras registraron información ante la SMV, pero solo #cifra("plataformasConFinanciamiento") financiaron proyectos (@tab-plataformas). La oferta descansa en una sola plataforma: #cifra("nombreLider") financió #cifra("proyFinLider") proyectos por S/~#cifra("montoLider") millones, el #cifra("participacionLider")~% del monto del periodo, y registró financiamiento en #cifra("mesesFinLider") meses seguidos desde #cifra("inicioLider"). #cifra("nombreTercera"), que solo atendió proyectos personales, financió #cifra("proyFinTercera") proyectos hasta #cifra("finTercera") y hoy figura entre las plataformas retiradas; #cifra("nombreSegunda") empezó a financiar en #cifra("inicioSegunda") y suma #cifra("proyFinSegunda") proyectos. Las otras tres sociedades presentaron estados financieros, pero no registran proyectos financiados en los meses obtenidos.

#tabla_apa(t1_plataformas,
  titulo: [Sociedades administradoras de plataformas de financiamiento participativo financiero, 2021-2026],
  nota: [«Meses obtenidos» son las consultas válidas al portal sobre 69 posibles. EEFF = estados financieros presentados a la SMV. Elaboración propia con datos de la #cite(<smvsimv2026>, form: "prose") y de la API OData de la SMV @smvodata2026.],
) <tab-plataformas>

El mercado creció con rapidez (@tab-anual). El monto financiado pasó de S/~#cifra("monto2022") millones en 2022 a S/~#cifra("monto2025") millones en 2025, y entre enero y septiembre de 2026 sumó S/~#cifra("monto2026") millones, #cifra("varMonto2026")~% más que en los mismos meses de 2025. Los proyectos financiados pasaron de #cifra("proyFin2022") a #cifra("proyFin2025") por año, pero el monto medio por proyecto creció todavía más, de S/~#cifra("montoMedio2022") mil en 2022 a S/~#cifra("montoMedio2026") mil en 2026: el mercado se expandió sobre todo por el tamaño de los proyectos. Al mismo tiempo, el financiamiento se volvió casi exclusivamente empresarial (de #cifra("partEmp2022")~% a #cifra("partEmp2026")~% del monto) y muy concentrado: el índice de Herfindahl-Hirschman pasó de #cifra("hhi2022") en 2022 a #cifra("hhi2025") en 2025, cerca de su máximo de 10 000.

#tabla_apa(t2_oferta_anual,
  titulo: [Oferta anual de financiamiento participativo financiero, 2022-2026],
  nota: [La variación de 2026 compara enero-septiembre con los mismos meses de 2025. Los montos están en soles corrientes; los agregados excluyen los meses no obtenidos, por lo que son una cota inferior. Elaboración propia con datos de la #cite(<smvsimv2026>, form: "prose").],
) <tab-anual>

La mediana del monto mensual pasó de S/~#cifra("medianaMensual2023") millones en 2023 a S/~#cifra("medianaMensual2025") millones en 2025 y a S/~#cifra("medianaMensual2026") millones en 2026 (@fig-monto), y la tasa de colocación subió del #cifra("colocacion2022")~% de los proyectos publicados en 2022 al #cifra("colocacion2026")~% en 2026 (@fig-colocacion).

#figura_apa(image("/salidas/figuras/f1_monto_mensual_por_plataforma.png", width: 80%),
  titulo: [Monto financiado mensual mediante plataformas de financiamiento participativo financiero, por plataforma (S/ millones corrientes)],
  nota: [La línea vertical marca diciembre de 2025, primer mes completo tras la modificación del reglamento. Elaboración propia con datos de la #cite(<smvsimv2026>, form: "prose").],
) <fig-monto>

#figura_apa(image("/salidas/figuras/f2_publicados_financiados_colocacion.png", width: 65%),
  titulo: [Proyectos publicados y financiados por mes y tasa de colocación móvil de 12 meses],
  nota: [La tasa de colocación móvil divide los proyectos financiados entre los publicados en los últimos 12 meses. Elaboración propia con datos de la #cite(<smvsimv2026>, form: "prose").],
) <fig-colocacion>

== Situación financiera de las sociedades administradoras

Las administradoras son empresas pequeñas en relación con lo que intermedian (@tab-financieros). #cifra("nombreLider") cerró 2025 con activos de S/~#cifra("activoLider2025") mil y un patrimonio de S/~#cifra("patrimonioLider2025") mil, en el año en que el mercado que lidera financió S/~#cifra("monto2025") millones. La diferencia de escala es coherente con un modelo en el que la plataforma pone en contacto a inversionistas y receptores sin financiar los proyectos con su propio balance. Sus ingresos subieron de S/~#cifra("ingresosLider2022") mil en 2022 a S/~#cifra("ingresosLider2025") mil en 2025, y desde #cifra("primerAnioUtilidadLider") obtiene utilidades, con un ROA anualizado de #cifra("roaLider2024")~% en 2024, #cifra("roaLider2025")~% en 2025 y #cifra("roaLider2026")~% en 2026. Las demás sociedades muestran otra situación: en #cifra("aniosOtrasPerdida") de sus #cifra("aniosOtras") años con información cerraron con pérdidas.

#tabla_apa(t3_plataformas_financieros,
  titulo: [Indicadores financieros de las sociedades administradoras por año],
  nota: [Montos en miles de soles. El ROA anualiza la utilidad de los trimestres disponibles. En los registros reportados en soles, la escala se corrigió solo cuando la empresa tenía trimestres de referencia; si no los tenía, los saldos se omiten (—). El cociente de ingresos sobre monto financiado solo se calcula con todos los meses del portal obtenidos y al menos S/~1 millón financiado en el año. Elaboración propia con datos de la API OData de la SMV @smvodata2026 y de la #cite(<smvsimv2026>, form: "prose").],
) <tab-financieros>

Los ingresos de #cifra("nombreLider") equivalen a entre #cifra("costoAnualLiderMin")~% y #cifra("costoAnualLiderMax")~% del monto que financió en cada año, y la mediana trimestral es de #cifra("costoMediana")~% en #cifra("costoTrimestres") trimestres (@fig-costo). Este cociente indica cuánto retiene la plataforma por cada sol que intermedia; no es la tasa que paga el receptor ni la rentabilidad del inversionista.

#figura_apa(image("/salidas/figuras/f4_costo_intermediacion_implicito.png", width: 80%),
  titulo: [Ingresos trimestrales de la plataforma líder como porcentaje del monto financiado en el trimestre],
  nota: [Solo se incluyen los trimestres con los tres meses del portal obtenidos. Elaboración propia con datos de la API OData de la SMV @smvodata2026 y de la #cite(<smvsimv2026>, form: "prose").],
) <fig-costo>

== Condiciones de acceso y de monto por tipo de receptor

En todo el periodo se publicaron #cifra("publicadosEmp") proyectos empresariales y #cifra("publicadosPer") personales (@tab-condiciones). Los empresariales se financiaron con más frecuencia (#cifra("colocacionEmp")~%, IC 95~% [#cifra("icEmpInf"); #cifra("icEmpSup")]) que los personales (#cifra("colocacionPer")~%, IC 95~% [#cifra("icPerInf"); #cifra("icPerSup")]) y por montos mucho mayores: S/~#cifra("montoMedioEmp") mil por proyecto frente a S/~#cifra("montoMedioPer") mil. Tras la modificación del reglamento, la colocación empresarial pasó de #cifra("colocacionEmpAntes")~% a #cifra("colocacionEmpDespues")~% y el monto medio, de S/~#cifra("montoMedioEmpAntes") mil a S/~#cifra("montoMedioEmpDespues") mil; en ese lapso no se publicó ningún proyecto personal.

#tabla_apa(t4_condiciones_por_receptor,
  titulo: [Condiciones de acceso y de monto por tipo de receptor, antes y después de la modificación del reglamento],
  nota: [El periodo empieza en #cifra("inicioFPF"); «después» comprende de diciembre de 2025 a septiembre de 2026. Los intervalos de Wilson suponen proyectos independientes. Elaboración propia con datos de la #cite(<smvsimv2026>, form: "prose").],
) <tab-condiciones>

La diferencia entre receptores es significativa en el agregado (H2: $z = #cifra("hDosZ")$, $p #cifra("hDosPRel")$), pero no puede atribuirse al tipo de receptor (@tab-contrastes). El #cifra("pctEmpresarialPrincipal")~% de los proyectos empresariales es de #cifra("nombreLider") y el #cifra("pctPersonalPrincipal")~% de los personales, de #cifra("principalPersonal"), de modo que la comparación enfrenta, en la práctica, dos plataformas con modelos de negocio distintos. Dentro de #cifra("nombreLider"), que atendió ambos tipos, se financiaron #cifra("perLiderFin") de sus #cifra("perLiderPub") proyectos personales, y la diferencia con los empresariales no es significativa (prueba exacta de Fisher, $"OR" = #cifra("hDosFisherOR")$, $p #cifra("hDosFisherPRel")$).

En cuanto a H1, la mediana del monto mensual pasó de S/~#cifra("hUnoMedianaAntes") millones antes de la modificación a S/~#cifra("hUnoMedianaDespues") millones después ($U = #cifra("hUnoU")$, $p #cifra("hUnoPRel")$; IC 95~% de la diferencia: S/~#cifra("hUnoICinf") a #cifra("hUnoICsup") millones). El resultado se mantiene con el corte en noviembre de 2025, en soles constantes, con la cota superior de los meses no obtenidos y solo con la plataforma líder, y deja de ser significativo sin ella ($p #cifra("hUnoPSinLiderRel")$; @tab-sensibilidad). Sin embargo, los controles de tendencia muestran que esta diferencia no puede atribuirse a la modificación: los #cifra("placeboN") cortes ficticios anteriores a ella también dan $p #cifra("placeboPMaxRel")$; el crecimiento interanual mediano bajó de #cifra("interanualAntes")~% a #cifra("interanualDespues")~%, y ninguno de los #cifra("mesesDespues") meses posteriores superó la tendencia previa, que suponía un crecimiento de #cifra("crecMensualPrevio")~% mensual ($R^2 = #cifra("rDosTendencia")$). El monto es mayor después del cambio normativo, pero esa diferencia es coherente con el crecimiento que el mercado ya traía, y ese crecimiento se desaceleró.

#tabla_apa(t5_contrastes_h1_h2,
  titulo: [Contrastes de las hipótesis H1 y H2],
  nota: [OR = razón de probabilidades. La prueba U es unilateral (después mayor que antes); la prueba _z_ y la de Fisher son bilaterales. Elaboración propia con datos de la #cite(<smvsimv2026>, form: "prose").],
) <tab-contrastes>

== Condiciones del crédito tradicional en segmentos comparables

Las tasas del crédito tradicional son altas y heterogéneas (@fig-tasas y @tab-segmentos). La TEA de los préstamos bancarios a pequeña y microempresa de hasta 360 días promedió #cifra("teaBcosPyme2022")~% en 2022 y #cifra("teaBcosPyme2026")~% en 2026, con un salto de #cifra("saltoTEA") puntos porcentuales en marzo de 2025. En las cajas municipales se mantuvo entre #cifra("teaCmacPymeMin")~% y #cifra("teaCmacPymeMax")~%, y en las cajas rurales, entre #cifra("teaCracPymeMin")~% y #cifra("teaCracPymeMax")~%. El crédito bancario de consumo de hasta 360 días subió de #cifra("teaBcosConsumo2022")~% a #cifra("teaBcosConsumo2026")~%, mientras que la TAMN, que promedia todo el crédito bancario, osciló entre #cifra("teaTamnMin")~% y #cifra("teaTamnMax")~%. En ese mismo lapso, el monto medio de los proyectos empresariales del FPF pasó de S/~#cifra("fpfEmpPrimero") mil a S/~#cifra("fpfEmpUltimo") mil.

#figura_apa(image("/salidas/figuras/f3_tasas_credito_tradicional.png", width: 80%),
  titulo: [Tasas activas promedio del crédito tradicional en moneda nacional por segmento],
  nota: [Tasas efectivas anuales de préstamos de hasta 360 días. Elaboración propia con datos de #cite(<bcrpdata2026>, form: "prose").],
) <fig-tasas>

#tabla_apa(t7_comparacion_segmentos,
  titulo: [Monto medio de los proyectos de financiamiento participativo y tasas del crédito tradicional por periodo],
  nota: [Las tasas son promedios simples de las tasas efectivas anuales mensuales. El año 2025 se divide por el salto de la tasa bancaria de pequeña y microempresa en marzo. Los montos medios del FPF y las tasas no son medidas del mismo concepto: se presentan juntos como contexto, no como comparación de precios. Elaboración propia con datos de la #cite(<smvsimv2026>, form: "prose") y de #cite(<bcrpdata2026>, form: "prose").],
) <tab-segmentos>

Por último, no se encontró asociación entre los cambios mensuales del monto financiado y los de las tasas tradicionales (E1). Con los #cifra("eUnoN") comparadores, los coeficientes de Spearman van de #cifra("eUnoRhoMin") a #cifra("eUnoRhoMax"), y ninguno es significativo: el menor valor $p$ es #cifra("eUnoPMin") (@tab-sensibilidad).

#tabla_apa(t8_sensibilidad,
  titulo: [Análisis de sensibilidad],
  nota: [M = millones de soles. E1 usa primeras diferencias mensuales. Elaboración propia con datos de la SMV @smvsimv2026 @smvodata2026 y del BCRP @bcrpdata2026.],
) <tab-sensibilidad>
