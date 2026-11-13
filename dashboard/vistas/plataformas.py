# Diego Sebastián Aliaga Damián
# 2024200481M
# Tema 96: Fintech y financiamiento participativo (crowdfunding) en el Perú: oferta y condiciones
# Fecha: 2026-11-13
"""Plataformas: situación financiera de las sociedades administradoras (estados financieros de la SMV)."""
from __future__ import annotations

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

import compartido as C
import datos as D
import tema as T


def pagina() -> None:
    r, t = C.resultados(), C.tablas()
    lider = r["plataforma_lider"]
    T.encabezado_pagina("Sociedades administradoras: pequeñas y solo una rentable",
                        "Estados financieros trimestrales publicados por la SMV (API OData).", "domain", T.VIOLETA,
                        "Módulo 2 · Plataformas")
    desde, hasta, plataformas = C.filtros()
    T.chips_filtros(desde, hasta, plataformas, len(D.PLATAFORMAS), [("info", "Años completos de los EEFF dentro del periodo")])
    if not plataformas:
        T.aviso("Elige al menos una plataforma en la barra lateral.", "filter_alt_off", T.CORAL)
        return
    a0, a1 = int(desde[:4]), int(hasta[:4])
    t3 = t["t3_plataformas_financieros"]
    t3f = t3[t3.plataforma.isin(plataformas) & t3.anio.between(a0, a1)]
    t3b = t["t3b_plataformas_trimestral"]
    t3bf = t3b[t3b.plataforma.isin(plataformas) & t3b.anio.between(a0, a1)]
    roa_lider = t3[(t3.plataforma == lider)].dropna(subset=["roa_pct"]).sort_values("anio")
    ultimo_completo = roa_lider[roa_lider.anio <= 2025].iloc[-1] if len(roa_lider) else None
    t1 = t["t1_plataformas"]
    ci = r["costo_intermediacion_lider"]
    T.kpis([
        {"etiqueta": f"ROA anualizado de {lider} ({int(ultimo_completo.anio)})" if ultimo_completo is not None else "ROA de la líder",
         "valor": C.pct(ultimo_completo.roa_pct) if ultimo_completo is not None else "—", "icono": "trending_up",
         "color": T.ESMERALDA, "insignia": "articulo", "ayuda": "Utilidad de los trimestres disponibles llevada a 4, sobre el activo medio."},
        {"etiqueta": "Ingresos / monto financiado (mediana trimestral)", "valor": f"{C.num(ci['mediana_trimestral_pct'], 2)} %",
         "icono": "percent", "color": T.TURQUESA, "insignia": "referencia",
         "sub": f"{lider}, {ci['trimestres']} trimestres", "ayuda": "Lo que retiene la plataforma; no es la tasa del receptor."},
        {"etiqueta": "Sociedades con estados financieros", "valor": f"{int((t1.trimestres_eeff > 0).sum())} de {len(t1)}",
         "icono": "description", "color": T.AZUL, "insignia": "observado", "sub": f"{int(t1.trimestres_eeff.sum())} trimestres en total"},
        {"etiqueta": "Sociedades con ROA positivo en 2025", "valor": str(int((t3[t3.anio == 2025].roa_pct > 0).sum())),
         "icono": "savings", "color": T.AMARILLO, "insignia": "articulo",
         "sub": f"de {int(t3[t3.anio == 2025].roa_pct.notna().sum())} con datos en 2025"},
    ])

    c1, c2 = st.columns(2, gap="medium")
    with c1, st.container(key="tarjeta-roa"):
        T.seccion("ROA anualizado por año", "bar_chart", T.ESMERALDA, "Utilidad neta sobre el activo medio (%).")
        roa = t3f.dropna(subset=["roa_pct"])
        if roa.empty:
            T.aviso("Sin datos de ROA para la selección.", "info", T.AZUL)
        else:
            fig = go.Figure()
            for p in [x for x in D.PLATAFORMAS if x in set(roa.plataforma)]:
                g = roa[roa.plataforma == p]
                fig.add_bar(x=g.anio.astype(str), y=g.roa_pct, name=p, marker_color=T.COLOR_PLATAFORMA[p],
                            customdata=g.trimestres, hovertemplate=f"{p}: %{{y:.1f}} % (%{{customdata}} trim.)<extra></extra>")
            fig.add_hline(y=0, line=dict(color=T.TINTA_3, width=1))
            fig.update_layout(barmode="group", yaxis_title="ROA (%)", hovermode="x unified")
            T.figura(fig, "fincrowd_roa", 360, roa.set_index(["plataforma", "anio"])[["trimestres", "roa_pct"]])
    with c2, st.container(key="tarjeta-f4"):
        T.seccion(f"Ingresos de {lider} / monto financiado", "percent", T.TURQUESA,
                  "Por trimestre (%). Es lo que retiene la plataforma, no la tasa que paga el receptor.",
                  extra=T.insignia("referencia"))
        f4 = C.figuras()["f4_costo_intermediacion_implicito"]
        fig = go.Figure()
        fig.add_scatter(x=f4.trimestre, y=f4.costo_intermediacion_pct, mode="lines+markers",
                        line=dict(color=T.COLOR_PLATAFORMA[lider], width=2.4, shape="spline"), marker=dict(size=7),
                        fill="tozeroy", fillcolor="rgba(37,99,235,0.07)", name=lider,
                        hovertemplate="%{x}: %{y:.2f} %<extra></extra>")
        fig.add_hline(y=ci["mediana_trimestral_pct"], line=dict(color=T.VIOLETA, dash="dot", width=1.4),
                      annotation_text=f"mediana {C.num(ci['mediana_trimestral_pct'], 2)} %", annotation_position="top left",
                      annotation_font=dict(color=T.OSCURO[T.VIOLETA], size=11))
        fig.update_layout(yaxis_title="%", showlegend=False)
        T.figura(fig, "fincrowd_ingresos_monto", 360, f4.set_index("trimestre"))

    with st.container(key="tarjeta-activo"):
        T.seccion("Tamaño de las sociedades: activo total por trimestre", "account_balance_wallet", T.AZUL,
                  "Miles de soles; escala corregida según el supuesto S5 del artículo.")
        act = t3bf.dropna(subset=["activo_miles"])
        if act.empty:
            T.aviso("Sin estados financieros para la selección.", "info", T.AZUL)
        else:
            fig = go.Figure()
            for p in [x for x in D.PLATAFORMAS if x in set(act.plataforma)]:
                g = act[act.plataforma == p].sort_values("trimestre")
                fig.add_scatter(x=g.trimestre, y=g.activo_miles, name=p, mode="lines+markers",
                                line=dict(color=T.COLOR_PLATAFORMA[p], width=2.2), marker=dict(size=6),
                                hovertemplate=f"{p}: S/ %{{y:,.0f}} mil<extra></extra>")
            fig.update_layout(yaxis_title="S/ miles", hovermode="x unified",
                              xaxis=dict(type="category", categoryorder="category ascending"))
            T.figura(fig, "fincrowd_activo_trimestral", 360,
                     act.pivot_table(index="trimestre", columns="plataforma", values="activo_miles"))

    with st.container(key="tarjeta-t3"):
        T.seccion("Indicadores financieros por año", "table_chart", T.VIOLETA, extra=T.insignia("articulo"))
        st.dataframe(pd.DataFrame({
            "Plataforma": t3f.plataforma, "Año": t3f.anio.astype(str), "Trimestres": t3f.trimestres,
            "Activo al cierre (S/ miles)": t3f.activo_cierre_miles.map(C.num),
            "Patrimonio al cierre (S/ miles)": t3f.patrimonio_cierre_miles.map(C.num),
            "Ingresos (S/ miles)": t3f.ingresos_miles.map(C.num), "Utilidad neta (S/ miles)": t3f.utilidad_miles.map(C.num),
            "ROA anualizado (%)": t3f.roa_pct.map(lambda x: C.num(x, 1)),
            "Ingresos / monto (%)": t3f.costo_intermediacion_pct.map(lambda x: C.num(x, 1))}), hide_index=True)
        T.nota("Fuente: SMV (API OData y SIMV). Tabla 3 del artículo. En los registros hechos en soles en lugar de miles, la "
               "escala se corrigió solo si la empresa tenía trimestres de referencia; si no, los saldos se omiten (—). "
               "Ingresos / monto solo se calcula en años con al menos S/ 1 M financiados.")
