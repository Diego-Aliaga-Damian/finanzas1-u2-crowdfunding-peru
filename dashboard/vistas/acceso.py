# Diego Sebastián Aliaga Damián
# 2024200481M
# Tema 96: Fintech y financiamiento participativo (crowdfunding) en el Perú: oferta y condiciones
# Fecha: 2026-11-13
"""Acceso por tipo de receptor (H2) y monto antes y después de la reforma de 2025 (H1)."""
from __future__ import annotations

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

import compartido as C
import datos as D
import tema as T
from vistas import graficos as G


def pagina() -> None:
    r = C.resultados()
    h1, ht, h2 = r["h1"], r["h1_tendencia"], r["h2"]
    T.encabezado_pagina("Acceso por tipo de receptor y la reforma de 2025",
                        "¿Se financian más los proyectos empresariales? ¿Creció el monto por la modificación del reglamento?",
                        "balance", T.ESMERALDA, "Módulo 3 · Acceso y reforma")
    desde, hasta, plataformas = C.filtros()

    with st.container(key="tarjeta-t4"):
        T.seccion("Tasa de colocación por tipo de receptor", "groups", T.ESMERALDA,
                  "Proyectos financiados entre publicados, con intervalos de Wilson al 95 %.", extra=T.insignia("articulo"))
        t4 = C.tablas()["t4_condiciones_por_receptor"].dropna(subset=["tasa_colocacion_pct"])
        fig = go.Figure()
        for tipo, color in (("Empresarial", T.AZUL), ("Personal", T.CORAL)):
            g = t4[t4.tipo_receptor == tipo]
            fig.add_bar(x=g.periodo, y=g.tasa_colocacion_pct, name=tipo, marker_color=color,
                        customdata=g[["proyectos_financiados", "proyectos_publicados", "ic95_inferior", "ic95_superior"]].to_numpy(),
                        error_y=dict(type="data", symmetric=False, array=g.ic95_superior - g.tasa_colocacion_pct,
                                     arrayminus=g.tasa_colocacion_pct - g.ic95_inferior, color=T.TINTA_2, thickness=1.4),
                        hovertemplate=f"<b>{tipo}</b>: %{{y:.1f}} %<br>%{{customdata[0]:.0f}} de %{{customdata[1]:.0f}}"
                                      "<br>IC 95 %: [%{customdata[2]:.1f}; %{customdata[3]:.1f}]<extra></extra>")
        fig.update_layout(barmode="group", yaxis=dict(title="Tasa de colocación (%)", range=[0, 105]))
        T.figura(fig, "fincrowd_colocacion_receptor", 340, t4.set_index(["periodo", "tipo_receptor"]))
        T.nota("Después de la reforma no se publicó ningún proyecto personal. Fuente: SMV (SIMV). Tabla 4 del artículo.")

    if plataformas:
        v = C.vista_filtrada()
        ct = D.colocacion_por_tipo(v).set_index("tipo_receptor")
        T.chips_filtros(desde, hasta, plataformas, len(D.PLATAFORMAS))
        T.kpis([{"etiqueta": f"Colocación {tipo.lower()} (tu selección)", "valor": C.pct(ct.loc[tipo, "colocacion_pct"]),
                 "icono": ic, "color": color, "insignia": "filtros",
                 "sub": f"{C.num(ct.loc[tipo, 'financiados'])} de {C.num(ct.loc[tipo, 'publicados'])} proyectos"}
                for tipo, ic, color in (("Empresarial", "storefront", T.AZUL), ("Personal", "person", T.CORAL))]
               + [{"etiqueta": "Monto medio empresarial (tu selección)",
                   "valor": f"S/{C.NBSP}{C.num(ct.loc['Empresarial', 'monto_medio'] / 1e3, 1)} mil", "icono": "request_quote",
                   "color": T.VIOLETA, "insignia": "filtros"},
                  {"etiqueta": "Monto medio personal (tu selección)",
                   "valor": f"S/{C.NBSP}{C.num(ct.loc['Personal', 'monto_medio'] / 1e3, 1)} mil", "icono": "request_quote",
                   "color": T.AMARILLO, "insignia": "filtros"}])

    c1, c2 = st.columns(2, gap="medium")
    with c1, st.container(key="tarjeta-h2"):
        T.seccion("H2 · Colocación por tipo de receptor", "science", T.AZUL, extra=T.insignia("articulo"))
        st.markdown(
            f"- Empresariales **{C.pct(h2['colocacion_empresarial_pct'])}** y personales **{C.pct(h2['colocacion_personal_pct'])}** "
            f"(z = {C.num(h2['z'], 2)}, p {C.p_txt(h2['p_valor'])}).\n"
            f"- El {C.pct(h2['pct_empresarial_en_principal'])} de los empresariales es de {h2['plataforma_principal_empresarial']} "
            f"y el {C.pct(h2['pct_personal_en_principal'])} de los personales, de {h2['plataforma_principal_personal']}.\n"
            f"- Dentro de la líder: {h2['dentro_lider']['financiados_per']} de {h2['dentro_lider']['publicados_per']} personales "
            f"financiados; Fisher p {C.p_txt(h2['dentro_lider']['p_valor_fisher'])} (OR = {C.num(h2['dentro_lider']['odds_ratio'], 2)}).")
        T.aviso("<b>Conclusión:</b> la diferencia refleja el modelo de negocio de cada plataforma, no el tipo de receptor.",
                "lightbulb", T.AZUL)
    with c2, st.container(key="tarjeta-h1"):
        T.seccion("H1 · Monto mensual antes y después de la reforma", "gavel", T.VIOLETA, extra=T.insignia("articulo"))
        st.markdown(
            f"- Mediana: {C.soles_m(h1['mediana_antes_soles'])} → **{C.soles_m(h1['mediana_despues_soles'])}** "
            f"(U = {C.num(h1['U'])}, p {C.p_txt(h1['p_valor_unilateral'])}).\n"
            f"- Pero {len(ht['cortes_placebo'])} cortes ficticios anteriores también dan p ≤ {ht['p_placebo_max']:.1e}.\n"
            f"- Crecimiento interanual mediano: {C.num(ht['interanual_mediana_antes_pct'])} % antes y "
            f"{C.num(ht['interanual_mediana_despues_pct'])} % después; {ht['meses_despues_sobre_tendencia']} de "
            f"{ht['meses_despues']} meses superan la tendencia previa.")
        T.aviso("<b>Conclusión:</b> el monto es mayor después de la reforma, pero la diferencia no es atribuible a la norma.",
                "lightbulb", T.VIOLETA)

    if plataformas:
        with st.container(key="tarjeta-f2"):
            T.seccion("Proyectos publicados y financiados por mes", "stacked_line_chart", T.CORAL,
                      "Con la colocación móvil de 12 meses (eje derecho).", extra=T.insignia("filtros"))
            G.publicados_financiados(v, desde, hasta, "acceso")
            T.nota("Sin filtros coincide con la Figura 2 del artículo. Los meses en que ninguna plataforma tiene registros "
                   "quedan vacíos. Fuente: SMV (SIMV).")
