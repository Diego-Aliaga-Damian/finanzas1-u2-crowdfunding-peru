// Traducido automáticamente de articulo/secciones/05_resultados.tex por herramientas/articulo/generar_typst.py.
// Para cambiar el texto, edita el .tex y vuelve a ejecutar el script (o edita aquí y deja de regenerar).
#import "../generado/cifras.typ": cifra
#import "../generado/tablas.typ": *
#import "../estilo.typ": *

= Resultados

== Verificación de la muestra

La @tab-muestra compara los datos disponibles de cada variable con el mínimo. Las series de tiempo tienen #cifra("muSeriesObs") meses por variable (#cifra("muSeriesDatos") datos frente a #cifra("muSeriesMin") exigidos), el logit usa #cifra("muProyObs") proyectos y la comparación de rentabilidad, #cifra("muCompObs") o más empresas-trimestre. Los estados financieros de las plataformas, por sí solos, tienen #cifra("muFpfObs") trimestres por variable y no llegan al mínimo; por eso solo describen, y la inferencia se hace con todas las empresas supervisadas.

#tabla_apa(t9_verificacion_muestra,
  titulo: [Verificación del tamaño de la muestra por variable],
  nota: [Datos válidos (no faltantes) de la variable con menos datos en cada bloque. obs. = observaciones. El último bloque es solo descriptivo. Elaboración propia con datos de la SMV @smvsimv2026 @smvodata2026 y del BCRP @bcrpdata2026.],
) <tab-muestra>

#resultado[Todas las variables que entran en un modelo cumplen el mínimo de 1 000 observaciones o 60 periodos.]

== Evolución y estructura de la oferta

De #cifra("plataformasAutorizadas") sociedades administradoras, solo #cifra("plataformasConFinanciamiento") financiaron proyectos (@tab-plataformas del Anexo). #cifra("nombreLider") financió #cifra("proyFinLider") proyectos por S/~#cifra("montoLider") millones, el #cifra("participacionLider")~% del total. El monto anual pasó de S/~#cifra("monto2022") millones en 2022 a S/~#cifra("monto2025") millones en 2025 (@tab-anual y @fig-monto), y entre enero y septiembre de 2026 sumó S/~#cifra("monto2026") millones, #cifra("varMonto2026")~% más que en los mismos meses de 2025. La expansión vino sobre todo del tamaño de los proyectos, cuyo monto medio subió de S/~#cifra("montoMedio2022") mil a S/~#cifra("montoMedio2026") mil. El índice de Herfindahl-Hirschman pasó de #cifra("hhi2022") a #cifra("hhi2025") en 2025.

#tabla_apa(t2_oferta_anual,
  titulo: [Oferta anual de financiamiento participativo financiero, 2022-2026],
  nota: [La variación de 2026 compara enero-septiembre con los mismos meses de 2025. Los montos están en soles corrientes; los agregados excluyen los meses no obtenidos, por lo que son una cota inferior. Elaboración propia con datos de la #cite(<smvsimv2026>, form: "prose").],
) <tab-anual>

#figura_apa(image("/salidas/figuras/f1_monto_mensual_por_plataforma.png", width: 78%),
  titulo: [Monto financiado mensual mediante plataformas de financiamiento participativo financiero, por plataforma (S/ millones corrientes)],
  nota: [La línea vertical marca diciembre de 2025, primer mes completo tras la modificación del reglamento. Elaboración propia con datos de la #cite(<smvsimv2026>, form: "prose").],
) <fig-monto>

#resultado[El FPF creció con rapidez, pero casi todo el monto pasa por una sola plataforma.]

== Rentabilidad de las administradoras

De las plataformas que financiaron proyectos, solo #cifra("nombreLider") obtiene utilidades, desde #cifra("primerAnioUtilidadLider"), con un ROA de #cifra("roaLider2025")~% en 2025; sus ingresos equivalen a una mediana de #cifra("costoMediana")~% del monto que financia (@tab-financieros del Anexo). La mediana del ROA trimestral de las plataformas es #cifra("empRoaMedFpf")~%, frente a #cifra("empRoaMedResto")~% de los demás intermediarios. Al controlar el tamaño y el trimestre, la diferencia es de #cifra("empRoa") puntos y no es significativa ($p #cifra("empRoaPRel")$); tampoco lo es frente a todas las empresas ($p #cifra("empRoaTodasPRel")$; @tab-rentabilidad). El tamaño sí se asocia con más rentabilidad (#cifra("empRoaTam")\; $p #cifra("empRoaTamPRel")$).

#tabla_apa(t15_rentabilidad_empresas,
  titulo: [Rentabilidad y capital de las plataformas frente a otras empresas supervisadas por la SMV],
  nota: [Mínimos cuadrados con efectos de trimestre (no mostrados) y errores agrupados por empresa. ROA y patrimonio/activo en porcentaje, acotados a los percentiles 1 y 99. Con cinco plataformas, la prueba tiene poca potencia. Elaboración propia con datos de la API OData de la SMV @smvodata2026.],
) <tab-rentabilidad>

#resultado[Las plataformas rinden menos que los demás intermediarios en la mediana, pero la diferencia no es significativa al controlar el tamaño.]

== Condiciones del crédito tradicional

Las tasas del crédito tradicional son altas y heterogéneas (@fig-tasas y @tab-segmentos del Anexo). Entre 2022 y 2026, la TEA de los bancos a pequeña y microempresa de hasta 360 días pasó de #cifra("teaBcosPyme2022")~% a #cifra("teaBcosPyme2026")~%, y la de consumo, de #cifra("teaBcosConsumo2022")~% a #cifra("teaBcosConsumo2026")~%. En las cajas municipales se mantuvo entre #cifra("teaCmacPymeMin")~% y #cifra("teaCmacPymeMax")~%, y en las rurales, entre #cifra("teaCracPymeMin")~% y #cifra("teaCracPymeMax")~%.

#figura_apa(image("/salidas/figuras/f3_tasas_credito_tradicional.png", width: 78%),
  titulo: [Tasas activas promedio del crédito tradicional en moneda nacional por segmento],
  nota: [Tasas efectivas anuales de préstamos de hasta 360 días. Elaboración propia con datos de #cite(<bcrpdata2026>, form: "prose").],
) <fig-tasas>

#resultado[El crédito tradicional comparable cuesta al menos #cifra("teaCmacPymeMin")~% anual en promedio. No hay una tasa del FPF publicada con la cual compararlo.]

== Estacionariedad

En niveles, la prueba ADF no rechaza la raíz unitaria en ninguna de las #cifra("raizN") series; en primeras diferencias la rechaza en todas (@tab-raiz). El monto del FPF pasa de $p #cifra("adfFpfPRel")$ a $p #cifra("adfFpfDifPRel")$. La KPSS confirma el resultado, salvo en la tasa de consumo y en el IPC, que quedan con reserva. Con la prueba de Zivot-Andrews, #cifra("zaQuiebres") tasas son estacionarias alrededor de un quiebre, entre ellas la de los bancos a pymes (#cifra("zaBancosMes")).

#tabla_apa(t10_raiz_unitaria,
  titulo: [Pruebas de raíz unitaria (69 meses)],
  nota: [ADF y KPSS con constante; los valores $p$ de la KPSS están acotados a [0.01; 0.10]. Zivot-Andrews con cambio de nivel; entre paréntesis, el primer mes del nuevo nivel. Elaboración propia con datos de la #cite(<smvsimv2026>, form: "prose") y de #cite(<bcrpdata2026>, form: "prose").],
) <tab-raiz>

#resultado[Las series son integradas de orden uno según la ADF. Corresponde probar cointegración y, si no la hay, modelar las diferencias.]

== Relación de largo plazo

Con 69 meses, Engle-Granger no rechaza la ausencia de cointegración en ningún par (el menor valor $p$ es #cifra("egParesPMin")) ni en el sistema con las cuatro tasas ($p #cifra("egSistemaPRel")$). La traza de Johansen tampoco supera su valor crítico: #cifra("johParesMax") en el par más cercano, frente a #cifra("johBancosVC"), y #cifra("johSistema") en el sistema, frente a #cifra("johSistemaVC") (@tab-cointegracion). Ninguna prueba de Granger es significativa (menor $p #cifra("grangerPMinRel")$). Con solo los #cifra("mesesActividadFPF") meses de actividad, Engle-Granger sí rechaza con la tasa de los bancos a pymes ($p #cifra("egBancosActivosPRel")$) y con el sistema ($p #cifra("egSistemaActivosPRel")$), de modo que la conclusión depende de la muestra.

#tabla_apa(t11_cointegracion,
  titulo: [Pruebas de cointegración y de causalidad de Granger (69 meses)],
  nota: [Hipótesis nula: no hay cointegración. Johansen: traza para $r = 0$ con constante. Granger en primeras diferencias con un rezago. La columna de 52 meses es una sensibilidad por debajo de 60 periodos. Elaboración propia con datos de la #cite(<smvsimv2026>, form: "prose") y de #cite(<bcrpdata2026>, form: "prose").],
) <tab-cointegracion>

#resultado[No hay evidencia robusta de una relación estable de largo plazo entre el monto del FPF y las tasas del crédito tradicional.]

== Relación de corto plazo

En el modelo con variables de impulso, ninguna tasa es significativa y las cuatro tampoco lo son en conjunto ($p #cifra("cpConWaldPRel")$; @tab-corto). Sin los impulsos, la tasa de las cajas municipales sale significativa ($p #cifra("cpSinCmacPRel")$), pero depende de un solo salto que se revierte al mes siguiente. El único efecto estable es el del propio rezago ($phi.alt = #cifra("cpConPhi")$, $p #cifra("cpConPhiPRel")$): un mes alto tiende a ser seguido por uno más bajo. Los diagnósticos no detectan autocorrelación, heterocedasticidad, mala especificación ni inestabilidad; los residuos no son normales ($p #cifra("cpConJbPRel")$), por lo que la inferencia es asintótica. Solo con los meses de actividad, las tasas son significativas en conjunto ($p #cifra("cpActivosWaldPRel")$), aunque ninguna lo es por separado.

#tabla_apa(t12_corto_plazo_hac,
  titulo: [Modelo de corto plazo del monto del FPF con errores HAC],
  nota: [Variable dependiente: primera diferencia de asinh del monto mensual en millones de soles de diciembre de 2021. Valores $p$ con errores HAC. Los impulsos valen uno en un solo mes. Elaboración propia con datos de la #cite(<smvsimv2026>, form: "prose") y de #cite(<bcrpdata2026>, form: "prose").],
) <tab-corto>

#resultado[En el corto plazo, los cambios de las tasas tradicionales no explican los del monto del FPF con los 67 cambios mensuales disponibles.]

== Modificación del reglamento (H1)

La mediana mensual pasó de S/~#cifra("hUnoMedianaAntes") millones antes de la modificación a S/~#cifra("hUnoMedianaDespues") millones después ($U = #cifra("hUnoU")$, $p #cifra("hUnoPRel")$), pero esa comparación no descuenta la tendencia. Al hacerlo, el nivel y la pendiente posteriores son menores que los que proyectaba la tendencia previa en escala asinh (#cifra("refAsinhNivel"), $p #cifra("refAsinhNivelPRel")$; #cifra("refAsinhPend"), $p #cifra("refAsinhPendPRel")$). Con errores AR(1) ninguno de los dos es significativo por separado, aunque sí en conjunto ($p #cifra("refArWaldPRel")$), y en millones de soles no hay cambio ($p #cifra("refLinWaldPRel")$; @tab-reforma y @fig-reforma). Además, #cifra("refPlacebos") de #cifra("refPlacebosN") cortes ficticios anteriores también resultan significativos.

#tabla_apa(t13_reforma_segmentada,
  titulo: [Regresión segmentada del monto mensual en la modificación del reglamento],
  nota: [Los modelos (1) y (2) usan asinh del monto en millones de soles de diciembre de 2021; el (3), el monto sin transformar. MCG AR(1) = mínimos cuadrados generalizados con errores autorregresivos. Elaboración propia con datos de la #cite(<smvsimv2026>, form: "prose") y de #cite(<bcrpdata2026>, form: "prose").],
) <tab-reforma>

#figura_apa(image("/salidas/figuras/f5_reforma_segmentada.png", width: 86%),
  titulo: [Monto mensual financiado y regresión segmentada en la modificación del reglamento],
  nota: [La línea discontinua prolonga la tendencia previa a diciembre de 2025. Elaboración propia con datos de la #cite(<smvsimv2026>, form: "prose") y de #cite(<bcrpdata2026>, form: "prose").],
) <fig-reforma>

#resultado[H1 se cumple solo como descripción de niveles. No hay evidencia de un efecto positivo de la modificación del reglamento.]

== Acceso por tipo de receptor (H2)

Se financió el #cifra("colocacionEmp")~% de los #cifra("publicadosEmp") proyectos empresariales y el #cifra("colocacionPer")~% de los #cifra("publicadosPer") personales (@tab-condiciones del Anexo). En el logit, la razón de momios de un proyecto empresarial es #cifra("logUnoOr") ($p #cifra("logUnoPRel")$), un efecto marginal de #cifra("logUnoEfecto") puntos porcentuales. Al controlar la plataforma y el año baja a #cifra("logTresOr") (IC 95~% [#cifra("logTresInf")\; #cifra("logTresSup")], $p #cifra("logTresPRel")$), con un efecto de #cifra("logTresEfecto") puntos y un intervalo que casi llega a cero (@tab-logit). La cautela es necesaria porque el #cifra("pctEmpresarialPrincipal")~% de los empresariales es de #cifra("nombreLider") y el #cifra("pctPersonalPrincipal")~% de los personales, de #cifra("principalPersonal"). Dentro de #cifra("nombreLider"), la prueba exacta de Fisher no es significativa ($p #cifra("hDosFisherPRel")$). La colocación también mejora con los años (#cifra("logAnioOr")\; $p #cifra("logAnioPRel")$).

#tabla_apa(t14_logit_colocacion,
  titulo: [Logit de la colocación de los proyectos publicados],
  nota: [Razones de momios con intervalos de confianza al 95~%. El efecto marginal es el promedio de la muestra. Supone proyectos independientes. Elaboración propia con datos de la #cite(<smvsimv2026>, form: "prose").],
) <tab-logit>

#resultado[Los proyectos empresariales se colocan más, pero buena parte de la ventaja refleja la plataforma y el año.]
