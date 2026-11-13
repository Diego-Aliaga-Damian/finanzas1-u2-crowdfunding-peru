# Diego Sebastián Aliaga Damián
# 2024200481M
# Tema 96: Fintech y financiamiento participativo (crowdfunding) en el Perú: oferta y condiciones
# Fecha: 2026-11-13
"""Sensibilidad: variantes de H1, cortes placebo, control de tendencia y la tabla T8 completa."""
from __future__ import annotations

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

import compartido as C
import datos as D
import tema as T


def pagina() -> None:
    r, t8 = C.resultados(), C.tablas()["t8_sensibilidad"]
    ht = r["h1_tendencia"]
    T.encabezado_pagina("Análisis de sensibilidad", "¿Se sostienen los resultados si cambian los supuestos?",
                        "tune", T.VIOLETA, "Módulo 5 · Robustez")
    st.html(T.chips([("verified", "Resultados fijos del artículo (no dependen de los filtros)")]))

    T.kpis([
        {"etiqueta": "Variantes de H1 con p < 0.05", "icono": "check_circle", "color": T.ESMERALDA, "insignia": "articulo",
         "valor": f"{int(((t8.contraste.str.startswith('H1:') | t8.contraste.str.startswith('H1 base')) & (t8.p_valor < 0.05)).sum())} de "
                  f"{int((t8.contraste.str.startswith('H1:') | t8.contraste.str.startswith('H1 base')).sum())}",
         "sub": "la excepción: la serie sin la plataforma líder"},
        {"etiqueta": "Cortes placebo significativos", "icono": "science", "color": T.CORAL, "insignia": "articulo",
         "valor": f"{len(ht['cortes_placebo'])} de {len(ht['cortes_placebo'])}",
         "sub": f"p entre {ht['p_placebo_min']:.1e} y {ht['p_placebo_max']:.1e}"},
        {"etiqueta": "Crecimiento interanual mediano", "icono": "trending_down", "color": T.AMARILLO, "insignia": "articulo",
         "valor": f"{C.num(ht['interanual_mediana_antes_pct'])} % → {C.num(ht['interanual_mediana_despues_pct'])} %",
         "sub": f"antes y después de la reforma (p = {ht['interanual_p']:.3f})"},
        {"etiqueta": "Meses posteriores sobre la tendencia previa", "icono": "show_chart", "color": T.AZUL, "insignia": "articulo",
         "valor": f"{ht['meses_despues_sobre_tendencia']} de {ht['meses_despues']}",
         "sub": f"tendencia previa {C.num(ht['crecimiento_mensual_previo_pct'], 1)} % mensual (R² {C.num(ht['r2_tendencia_previa'], 2)})"},
    ])

    with st.container(key="tarjeta-forest"):
        T.seccion("H1 con distintos supuestos: diferencia de medianas (después − antes)", "align_horizontal_center", T.VIOLETA,
                  "S/ millones por mes, con IC 95 % bootstrap. En verde, p < 0.05.")
        h = t8[t8.detalle.str.contains("diferencia", na=False)].copy()
        h["dif"] = h.detalle.map(D.diferencia_detalle)
        h[["lo", "hi"]] = pd.DataFrame(h.detalle.map(D.intervalo_detalle).tolist(), index=h.index)
        h["nombre"] = h.contraste.str.replace(r"^H1( base)?:\s*", "", regex=True).map(lambda x: x[:1].upper() + x[1:])
        h = h.iloc[::-1]
        colores = [T.ESMERALDA if p < 0.05 else T.CORAL for p in h.p_valor]
        fig = go.Figure()
        fig.add_scatter(x=h.dif, y=h.nombre, mode="markers", marker=dict(size=12, color=colores, line=dict(color="white", width=1.5)),
                        error_x=dict(type="data", symmetric=False, array=h.hi - h.dif, arrayminus=h.dif - h.lo,
                                     color="#CBD5E1", thickness=3, width=0),
                        customdata=h[["p_valor", "lo", "hi", "valor"]].to_numpy(),
                        hovertemplate="<b>%{y}</b><br>Diferencia: S/ %{x:.2f} M<br>IC 95 %: [%{customdata[1]:.2f}; "
                                      "%{customdata[2]:.2f}]<br>U = %{customdata[3]:.0f}, p = %{customdata[0]:.2g}<extra></extra>")
        fig.add_vline(x=0, line=dict(color=T.TINTA_3, dash="dot", width=1))
        fig.update_layout(xaxis=dict(title="Diferencia de medianas (S/ millones)", showgrid=True, gridcolor=T.GRILLA),
                          yaxis=dict(showgrid=False), showlegend=False, margin=dict(l=6, t=10))
        T.figura(fig, "fincrowd_sensibilidad_h1", 330, h.set_index("nombre")[["dif", "lo", "hi", "valor", "p_valor"]])
        T.aviso("El resultado de H1 se sostiene con otro corte, en soles constantes y con la cota de los meses no obtenidos, "
                "pero <b>desaparece sin la plataforma líder</b>, y los cortes placebo y el control de tendencia muestran que "
                "la diferencia no es atribuible a la reforma.", "lightbulb", T.VIOLETA)

    with st.container(key="tarjeta-t8"):
        T.seccion("Tabla 8 completa", "table_chart", T.AZUL, extra=T.insignia("articulo"))
        st.dataframe(pd.DataFrame({"Análisis": t8.contraste, "Estadístico": t8.estadistico,
                                   "Valor": [C.num(v, 0 if e == "meses" else 2) for v, e in zip(t8.valor, t8.estadistico)],
                                   "p": t8.p_valor.map(lambda x: "—" if pd.isna(x) else C.p_txt(x).replace("= ", "")),
                                   "Detalle": t8.detalle}), hide_index=True, height=560)
        st.download_button("Descargar T8 (CSV)", t8.to_csv(index=False).encode("utf-8-sig"), "t8_sensibilidad.csv", "text/csv",
                           icon=":material/download:", type="tertiary")
        T.nota("M = millones de soles. E1 usa primeras diferencias mensuales con 8 comparadores (ver Crédito tradicional).")
