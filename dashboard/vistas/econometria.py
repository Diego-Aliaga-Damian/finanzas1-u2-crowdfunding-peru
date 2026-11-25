# Diego Sebastián Aliaga Damián
# 2024200481M
# Tema 96: Fintech y financiamiento participativo (crowdfunding) en el Perú: oferta y condiciones
# Fecha: 2026-11-25
"""Pruebas econométricas del artículo (T9-T15): se leen de salidas/tablas y no se recalculan."""
from __future__ import annotations

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

import compartido as C
import datos as D
import tema as T


def _p(x, kpss: bool = False) -> str:
    if pd.isna(x):
        return "—"
    if kpss and (x <= 0.01 or x >= 0.10):
        return "≤ 0.010" if x <= 0.01 else "≥ 0.100"
    return "< 0.001" if x < 0.001 else f"{x:.3f}"


def _modelos(t: pd.DataFrame, titulos: dict[int, str], dec: int = 3, valor: str = "coef") -> pd.DataFrame:
    filas = {}
    for v in dict.fromkeys(t.nombre):
        g = t[t.nombre == v].set_index("modelo")
        filas[v] = {f"{titulos[k]}{s}": (x if k in g.index else "—") for k in titulos for s, x in (
            ("", C.num(g[valor].get(k), dec) if k in g.index else "—"), (" · p", _p(g.p.get(k)) if k in g.index else "—"))}
    return pd.DataFrame(filas).T.rename_axis("Variable").reset_index()


def _tarjeta(clave: str, titulo: str, ic: str, color: str, sub: str, tabla: pd.DataFrame, crudo: pd.DataFrame, archivo: str, conclusion: str) -> None:
    with st.container(key=f"tarjeta-ec-{clave}"):
        T.seccion(titulo, ic, color, sub, extra=T.insignia("articulo"))
        T.aviso(f"<b>Resultado.</b> {conclusion}", "lightbulb", color)
        st.dataframe(tabla, hide_index=True)
        st.download_button("Descargar sin redondear (CSV)", crudo.to_csv(index=False).encode("utf-8-sig"), f"{archivo}.csv", "text/csv",
                           icon=":material/download:", type="tertiary", key=f"csv_{archivo}")


def pagina() -> None:
    t, ec = C.tablas(), C.resultados()["econometria"]
    cp, lg, rf, em = ec["corto_plazo"]["2"], ec["logit"], ec["reforma"], ec["empresas"]
    T.encabezado_pagina("Pruebas econométricas", "Estacionariedad, largo plazo, corto plazo, reforma, colocación y rentabilidad.",
                        "functions", T.AZUL, "Módulo 6 · Econometría")
    T.respuesta("Con 69 meses <b>no hay evidencia robusta de cointegración</b> entre el monto del crowdfunding y las tasas de bancos y cajas, y en el corto plazo "
                "las tasas <b>no son significativas en conjunto</b>. La reforma de 2025 <b>no muestra un efecto positivo</b>. Los proyectos "
                "empresariales se colocan más, pero la ventaja se reduce al controlar la plataforma y el año.")
    st.html(T.chips([("verified", "Resultados fijos del artículo (no dependen de los filtros)")]))
    series = next(f for f in ec["muestra"] if f["criterio"] == "periodos")
    T.kpis([
        {"etiqueta": "Datos por variable (series de tiempo)", "valor": f"{series['datos_por_variable']} meses", "icono": "dataset", "color": T.AZUL,
         "sub": "mínimo: 60 periodos por variable", "insignia": "articulo"},
        {"etiqueta": "Proyectos en el logit", "valor": C.num(lg["1"]["n"]), "icono": "inventory_2", "color": T.TURQUESA,
         "sub": "mínimo: 1 000 observaciones por variable", "insignia": "articulo"},
        {"etiqueta": "Tasas en el corto plazo (p conjunta)", "valor": _p(cp["wald_tasas_p"]), "icono": "query_stats", "color": T.VIOLETA,
         "sub": f"modelo con impulsos, N = {C.num(cp['n'])}", "insignia": "articulo"},
        {"etiqueta": "Razón de momios empresarial", "valor": f"{C.num(lg['1']['coef']['empresarial']['razon'], 2)} → {C.num(lg['3']['coef']['empresarial']['razon'], 2)}",
         "icono": "balance", "color": T.ESMERALDA, "sub": "sin y con control de plataforma y año", "insignia": "articulo"},
    ])
    pest = st.tabs(["Muestra", "Estacionariedad", "Largo plazo", "Corto plazo", "Reforma", "Colocación", "Rentabilidad"])
    with pest[0]:
        x = t["t9_verificacion_muestra"]
        _tarjeta("muestra", "Verificación del tamaño de la muestra", "fact_check", T.AZUL, "Al menos 1 000 observaciones o 60 periodos por cada variable.",
                 pd.DataFrame({"Bloque": x.bloque, "Unidad": x.unidad, "Variables": x.variables, "Datos por variable": x.datos_por_variable.map(C.num),
                               "Mínimo": [f"{C.num(a)} {b}" for a, b in zip(x.minimo_por_variable, x.criterio)], "Datos totales": x.datos_totales.map(C.num),
                               "¿Cumple?": x.cumple.map({True: "Sí", False: "No (solo descriptivo)"})}), x, "t9_verificacion_muestra",
                 "Todas las variables que entran en un modelo cumplen. Los estados financieros de las plataformas, por sí solos, no: solo describen.")
    with pest[1]:
        x = t["t10_raiz_unitaria"]
        _tarjeta("raiz", "Raíz unitaria", "show_chart", T.VIOLETA, "ADF: H0 raíz unitaria. KPSS: H0 estacionaria. Zivot-Andrews admite un quiebre.",
                 pd.DataFrame({"Variable": x.nombre, "ADF en nivel (p)": x.adf_nivel_p.map(_p), "ADF en diferencia (p)": x.adf_dif_p.map(_p),
                               "KPSS en nivel (p)": x.kpss_nivel_p.map(lambda p: _p(p, True)), "KPSS en diferencia (p)": x.kpss_dif_p.map(lambda p: _p(p, True)),
                               "Zivot-Andrews (p)": x.za_p.map(_p), "Quiebre": x.za_quiebre, "Conclusión": x.conclusion}), x, "t10_raiz_unitaria",
                 "Las siete series son integradas de orden uno según la ADF.")
    with pest[2]:
        x = t["t11_cointegracion"]
        _tarjeta("coint", "Cointegración y causalidad de Granger", "link", T.TURQUESA, "H0: no hay cointegración.",
                 pd.DataFrame({"Relación": x.relacion, "Engle-Granger (p)": x.engle_granger_p.map(_p), "Con 52 meses (p)": x.engle_granger_p_52.map(_p),
                               "Johansen: traza": x.johansen_traza.map(lambda v: C.num(v, 2)), "Valor crítico 5 %": x.johansen_vc5.map(lambda v: C.num(v, 2)),
                               "Granger TEA → FPF (p)": x.granger_tasa_a_fpf_p.map(_p), "Granger FPF → TEA (p)": x.granger_fpf_a_tasa_p.map(_p),
                               "Conclusión": x.conclusion}), x, "t11_cointegracion",
                 "No hay evidencia robusta de una relación estable de largo plazo. Con solo los 52 meses de actividad, Engle-Granger sí rechaza en dos casos.")
    with pest[3]:
        x = t["t12_corto_plazo_hac"]
        _tarjeta("corto", "Modelo de corto plazo con errores HAC", "query_stats", T.AZUL, "Variable dependiente: cambio mensual de asinh del monto real.",
                 _modelos(x, {1: "(1) Sin impulsos", 2: "(2) Con impulsos", 3: "(3) Solo con actividad"}), x, "t12_corto_plazo_hac",
                 "Los cambios de las tasas tradicionales no explican los del monto del FPF con los 67 cambios mensuales disponibles.")
    with pest[4]:
        x, a = t["t13_reforma_segmentada"], C.figuras()["f5_reforma_segmentada"]
        a = a.rename(columns={a.columns[0]: "periodo"})
        fig = go.Figure()
        ej = T.eje_meses(fig, list(a.periodo))
        fig.add_scatter(x=ej, y=a.monto_real, mode="markers", name="Observado", marker=dict(size=6, color=T.TINTA_3), hovertemplate="%{x}: S/ %{y:.2f} M<extra></extra>")
        fig.add_scatter(x=ej, y=a.ajuste_asinh, name="Ajuste (asinh)", line=dict(color=T.AZUL, width=2.2), hovertemplate="Ajuste: S/ %{y:.2f} M<extra></extra>")
        corte = list(a.periodo).index(D.REFORMA)
        fig.add_scatter(x=ej[corte:], y=a.sin_reforma_asinh[corte:], name="Tendencia previa", line=dict(color=T.CORAL, width=2, dash="dash"),
                        hovertemplate="Tendencia previa: S/ %{y:.2f} M<extra></extra>")
        T.marcar_mes(fig, D.etiqueta_mes(D.REFORMA), "Reforma 2025", T.VIOLETA, "left")
        fig.update_layout(yaxis_title="S/ millones de dic. 2021", hovermode="x unified")
        with st.container(key="tarjeta-ec-fig"):
            T.seccion("Regresión segmentada en diciembre de 2025", "timeline", T.CORAL)
            T.figura(fig, "fincrowd_reforma_segmentada", 340, a.set_index("periodo"),
                     leer="Los puntos son los montos reales de cada mes. La línea azul es el ajuste antes y después de la reforma; la punteada prolonga lo que "
                          "venía pasando. Si la reforma hubiera impulsado el monto, los puntos estarían por encima de la línea punteada.")
        _tarjeta("reforma", "Coeficientes", "gavel", T.CORAL, f"Además, {rf['placebos_significativos']} de {len(rf['placebos'])} cortes ficticios también son significativos.",
                 _modelos(x, {1: "(1) asinh, HAC", 2: "(2) asinh, MCG AR(1)", 3: "(3) S/ millones, HAC"}), x, "t13_reforma_segmentada",
                 "H1 se cumple solo como descripción de niveles: no hay evidencia de un efecto positivo de la reforma.")
    with pest[5]:
        x = t["t14_logit_colocacion"]
        _tarjeta("logit", "Logit de la colocación (razones de momios)", "balance", T.ESMERALDA, "Un registro por proyecto publicado.",
                 _modelos(x[x.variable != "const"], {1: "(1) Receptor", 2: "(2) + plataforma", 3: "(3) + plataforma y año"}, 2, "razon"), x, "t14_logit_colocacion",
                 "Los proyectos empresariales se colocan más, pero buena parte de la ventaja refleja la plataforma y el año.")
    with pest[6]:
        x = t["t15_rentabilidad_empresas"]
        _tarjeta("empresas", "Rentabilidad frente a otras empresas supervisadas", "account_balance", T.AMARILLO,
                 f"Mediana del ROA trimestral: {C.num(em['1']['mediana_fpf'], 1)} % en las plataformas y {C.num(em['1']['mediana_resto'], 1)} % en los demás intermediarios.",
                 _modelos(x, {1: "(1) ROA, intermediarios", 2: "(2) ROA, todas", 3: "(3) Patrimonio/activo"}, 2), x, "t15_rentabilidad_empresas",
                 "La diferencia de rentabilidad no es significativa al controlar el tamaño. Con cinco plataformas, la prueba tiene poca potencia.")
    T.nota("Las pruebas son asociativas, no causales. Cálculos: codigo/econometria.py y codigo/04_analisis.py (statsmodels). "
           "Fuentes: SMV (SIMV y API OData) y BCRP (BCRPData).")
