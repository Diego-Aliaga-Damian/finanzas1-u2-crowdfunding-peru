# Diego Sebastián Aliaga Damián
# 2024200481M
# Tema 96: Fintech y financiamiento participativo (crowdfunding) en el Perú: oferta y condiciones
# Fecha: 2026-11-13
"""Crédito tradicional: tasas observadas del BCRP, qué es comparable con el FPF y la asociación exploratoria E1."""
from __future__ import annotations

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

import compartido as C
import datos as D
import tema as T

PRINCIPALES = ["tea_bcos_pyme_360", "tea_cmac_pyme_360", "tea_crac_pyme_360", "tea_bcos_consumo_360"]


def pagina() -> None:
    r, t = C.resultados(), C.tablas()
    T.encabezado_pagina("Frente al crédito tradicional",
                        "Tasas activas promedio en moneda nacional por segmento, publicadas por el BCRP.",
                        "account_balance", T.AMARILLO, "Módulo 4 · Comparación financiera")
    T.aviso("<b>Estas son tasas del crédito tradicional (bancos y cajas), no del financiamiento participativo.</b> La SMV no "
            "publica la tasa ni el plazo de cada operación de FPF, por lo que su precio no se observa y no se compara con "
            "estas series. Sirven solo como referencia del costo del crédito en el mismo periodo.", "warning", T.AMARILLO)
    desde, hasta, _ = C.filtros()
    T.chips_filtros(desde, hasta, list(D.PLATAFORMAS), len(D.PLATAFORMAS), [("info", "El filtro de plataformas no aplica")])
    bcrp = D.tasas_bcrp(C.base())
    v = bcrp[(bcrp.index >= desde) & (bcrp.index <= hasta)]
    fin = v.index[-1]
    previo = D.desplazar(fin, -12)
    T.kpis([{"etiqueta": D.SERIES_BCRP[s], "valor": C.pct(v.loc[fin, s]),
             "icono": "account_balance" if "bcos" in s else "savings", "color": T.COLOR_SERIE[s], "insignia": "observado",
             "delta": (v.loc[fin, s] - bcrp.loc[previo, s]) if previo in bcrp.index else float("nan"),
             "delta_txt": (f"{'+' if v.loc[fin, s] - bcrp.loc[previo, s] > 0 else ''}{C.num(v.loc[fin, s] - bcrp.loc[previo, s], 1)}"
                           f"{C.NBSP}p.{C.NBSP}p." if previo in bcrp.index else "sin dato un año antes"),
             "delta_ref": f"TEA de {C.mes_txt(fin)} frente a {C.mes_txt(previo)}" if previo in bcrp.index else "",
             "sentido": "neutro"} for s in PRINCIPALES])

    with st.container(key="tarjeta-tasas"):
        T.seccion("Tasas efectivas anuales del crédito tradicional", "show_chart", T.AMARILLO, extra=T.insignia("observado"))
        elegidas = st.multiselect("Series del BCRP", list(D.SERIES_BCRP), default=PRINCIPALES, format_func=D.SERIES_BCRP.get,
                                  key="w_series")
        if elegidas:
            fig = go.Figure()
            x = T.eje_meses(fig, list(v.index))
            for s in elegidas:
                fig.add_scatter(x=x, y=v[s], name=D.SERIES_BCRP[s], mode="lines", line=dict(color=T.COLOR_SERIE[s], width=2.2),
                                hovertemplate=f"{D.SERIES_BCRP[s]}: %{{y:.2f}} %<extra></extra>")
            fig.update_layout(yaxis_title="TEA (%)", hovermode="x unified", legend=dict(y=1.02))
            if desde <= D.QUIEBRE_TEA <= hasta:
                T.marcar_mes(fig, D.etiqueta_mes(D.QUIEBRE_TEA), f"Salto de {C.num(r['salto_tea_bcos_pyme_2025_03_pp'], 1)} p. p.",
                             T.OSCURO[T.AMARILLO], "left")
            if desde <= D.REFORMA <= hasta:
                T.marcar_mes(fig, D.etiqueta_mes(D.REFORMA), "Reforma FPF", T.VIOLETA)
            T.figura(fig, "fincrowd_tasas_bcrp", 420, v[elegidas])
        T.nota(f"La serie bancaria de pequeña y microempresa de hasta 360 días sube {C.num(r['salto_tea_bcos_pyme_2025_03_pp'], 1)} "
               "puntos porcentuales en marzo de 2025, sin un movimiento parecido en las cajas ni en el consumo; el BCRP no "
               "publica la causa. Fuente: BCRP (BCRPData).")

    with st.container(key="tarjeta-t6"):
        T.seccion("¿Qué es comparable?", "rule", T.CORAL, extra=T.insignia("articulo"))
        st.dataframe(t["t6_comparabilidad"], hide_index=True, height=330)
        T.nota("Tabla 6 del artículo.")
    with st.container(key="tarjeta-e1"):
        T.seccion("E1 · Asociación exploratoria", "scatter_plot", T.VIOLETA,
                  "Spearman entre cambios mensuales del monto FPF y de cada tasa, con IC 95 % por bloques.",
                  extra=T.insignia("articulo"))
        t8 = t["t8_sensibilidad"]
        e1 = t8[t8.contraste.str.startswith("E1")].copy()
        e1["serie"] = e1.contraste.str.replace(r"^E1: Δ monto FPF vs Δ TEA ", "", regex=True)
        e1[["lo", "hi"]] = pd.DataFrame(e1.detalle.map(D.intervalo_detalle).tolist(), index=e1.index)
        e1 = e1.iloc[::-1]
        fig = go.Figure()
        fig.add_scatter(x=e1.valor, y=e1.serie, mode="markers", marker=dict(size=10, color=T.VIOLETA),
                        error_x=dict(type="data", symmetric=False, array=e1.hi - e1.valor, arrayminus=e1.valor - e1.lo,
                                     color="#C4B5FD", thickness=2.2, width=0),
                        customdata=e1[["p_valor", "lo", "hi"]].to_numpy(),
                        hovertemplate="<b>%{y}</b><br>rho = %{x:.2f}<br>IC 95 %: [%{customdata[1]:.2f}; %{customdata[2]:.2f}]"
                                      "<br>p = %{customdata[0]:.3f}<extra></extra>")
        fig.add_vline(x=0, line=dict(color=T.TINTA_3, dash="dot", width=1))
        fig.update_layout(xaxis=dict(title="rho de Spearman", range=[-0.6, 0.4], showgrid=True, gridcolor=T.GRILLA),
                          yaxis=dict(showgrid=False), showlegend=False, margin=dict(l=6, t=10))
        T.figura(fig, "fincrowd_e1_spearman", 340, e1.set_index("serie")[["valor", "lo", "hi", "p_valor"]])
        e1r = r["e1"]
        T.nota(f"Ninguna de las {len(e1r)} correlaciones es significativa (menor p = "
               f"{min(x['p_valor'] for x in e1r.values()):.3f}). Asociación no implica causalidad.")

    with st.container(key="tarjeta-t7"):
        T.seccion("Monto medio del FPF y tasas del crédito tradicional por periodo", "table_chart", T.AZUL,
                  "Se muestran lado a lado como contexto; el monto medio no es un precio.", extra=T.insignia("articulo"))
        t7 = t["t7_comparacion_segmentos"]
        st.dataframe(pd.DataFrame({
            "Periodo": t7.periodo,
            "FPF empresarial: monto medio (S/ miles)": (t7.fpf_empresarial_monto_medio_soles / 1e3).map(lambda x: C.num(x, 1)),
            "FPF personal: monto medio (S/ miles)": (t7.fpf_personal_monto_medio_soles / 1e3).map(lambda x: C.num(x, 1)),
            **{f"{D.SERIES_BCRP[c]} (TEA %)": t7[f"{c}_media"].map(lambda x: C.num(x, 1))
               for c in ("tamn", *PRINCIPALES)}}), hide_index=True)
        T.nota("Tabla 7 del artículo. 2025 se divide en enero-febrero y marzo-diciembre por el salto de la TEA bancaria pyme.")
