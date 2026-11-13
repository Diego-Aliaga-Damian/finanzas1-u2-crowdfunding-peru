# Diego Sebastián Aliaga Damián
# 2024200481M
# Tema 96: Fintech y financiamiento participativo (crowdfunding) en el Perú: oferta y condiciones
# Fecha: 2026-11-13
"""Gráficos compartidos entre páginas (misma lógica y mismos colores en todo el dashboard)."""
from __future__ import annotations

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

import datos as D
import tema as T


def monto_por_plataforma(v: pd.DataFrame, desde: str, hasta: str, clave: str, permitir_real: bool = False) -> None:
    """Barras apiladas del monto financiado por plataforma, con agrupación mensual, trimestral o anual."""
    with st.container(key=f"tarjeta-monto-{clave}"):
        c1, c2, c3 = st.columns([2.2, 1.5, 1.2] if permitir_real else [3, 1.5, 0.01], vertical_alignment="bottom")
        with c1:
            T.seccion("Evolución del monto financiado", "monitoring", T.AZUL,
                      "Monto por plataforma; la línea punteada marca el primer mes completo tras la reforma de 2025.")
        nivel = c2.segmented_control("Agrupar por", ["Mensual", "Trimestral", "Anual"], default="Mensual",
                                     key=f"w_nivel_{clave}", label_visibility="collapsed") or "Mensual"
        real = False
        if permitir_real:
            real = (c3.segmented_control("Unidad", ["Corrientes", "Reales"], default="Corrientes", key=f"w_real_{clave}",
                                         label_visibility="collapsed",
                                         help="Reales: soles de diciembre de 2021, deflactados con el IPC (como en la Tabla 2).")
                    == "Reales")
        m = D.mensual_por_plataforma(v, real=real)
        if m.empty or m.to_numpy().sum() == 0:
            T.aviso("No hay montos financiados en la selección actual.", "info", T.AZUL)
            return
        m = m[[p for p in D.PLATAFORMAS if p in m.columns and m[p].sum() > 0]]
        g = D.agrupar(m, nivel) / 1e6
        fig = go.Figure()
        x = T.eje_meses(fig, list(g.index)) if nivel == "Mensual" else list(g.index)
        for p in g.columns:
            fig.add_bar(x=x, y=g[p], name=p, marker_color=T.COLOR_PLATAFORMA[p], marker_line_width=0,
                        hovertemplate=f"{p}: S/ %{{y:.2f}} M<extra></extra>")
        fig.add_scatter(x=x, y=g.sum(axis=1), name="Total", mode="lines+markers" if nivel != "Mensual" else "lines",
                        line=dict(color=T.TINTA, width=1.6), hovertemplate="<b>Total: S/ %{y:.2f} M</b><extra></extra>",
                        visible="legendonly")
        unidad = "S/ millones de dic-2021" if real else "S/ millones corrientes"
        fig.update_layout(barmode="stack", yaxis_title=unidad, hovermode="x unified", legend=dict(traceorder="normal"))
        if nivel == "Mensual" and desde <= D.REFORMA <= hasta:
            T.marcar_mes(fig, D.etiqueta_mes(D.REFORMA), "Reforma 2025", T.VIOLETA, "left")
        datos = (g * 1e6).round(0).rename_axis("periodo")
        T.figura(fig, f"fincrowd_monto_{clave}", 390, datos)
        T.nota(f"{unidad.capitalize()}. Solo meses con registros en el portal de la SMV (los no obtenidos no se imputan). "
               "Fuente: SMV (SIMV).")


def publicados_financiados(v: pd.DataFrame, desde: str, hasta: str, clave: str) -> None:
    """Proyectos publicados y financiados por mes y colocación móvil de 12 meses (como la Figura 2)."""
    s = D.mensual_sistema(v)
    s = s[s.index >= (s[s.monto_financiado_total > 0].index.min() if (s.monto_financiado_total > 0).any() else s.index.min())]
    fig = go.Figure()
    x = T.eje_meses(fig, list(s.index))
    fig.add_scatter(x=x, y=s.proy_publicados_total, name="Publicados", line=dict(color=T.AZUL, width=2.2),
                    hovertemplate="Publicados: %{y:.0f}<extra></extra>")
    fig.add_scatter(x=x, y=s.proy_financiados_total, name="Financiados", line=dict(color=T.CORAL, width=2.2),
                    fill="tozeroy", fillcolor="rgba(251,113,133,0.08)", hovertemplate="Financiados: %{y:.0f}<extra></extra>")
    fig.add_scatter(x=x, y=s.colocacion_12m_pct, name="Colocación móvil 12 m (%)", yaxis="y2",
                    line=dict(color=T.ESMERALDA, width=2, dash="dot"), hovertemplate="Colocación 12 m: %{y:.1f} %<extra></extra>")
    fig.update_layout(hovermode="x unified", yaxis=dict(title="Proyectos por mes"),
                      yaxis2=dict(title="Colocación (%)", overlaying="y", side="right", showgrid=False, range=[0, 105],
                                  tickmode="linear", tick0=0, dtick=20))
    if desde <= D.REFORMA <= hasta:
        T.marcar_mes(fig, D.etiqueta_mes(D.REFORMA), "Reforma 2025", T.VIOLETA, "left")
    T.figura(fig, f"fincrowd_publicados_financiados_{clave}", 380,
             s[["proy_publicados_total", "proy_financiados_total", "colocacion_12m_pct"]])
