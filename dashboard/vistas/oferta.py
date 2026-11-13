# Diego Sebastián Aliaga Damián
# 2024200481M
# Tema 96: Fintech y financiamiento participativo (crowdfunding) en el Perú: oferta y condiciones
# Fecha: 2026-11-13
"""Oferta: evolución del monto, comparación entre dos periodos, oferta anual y plataformas."""
from __future__ import annotations

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

import compartido as C
import datos as D
import tema as T
from vistas import graficos as G

FILAS = [("monto", "Monto financiado (S/ M)", lambda x: C.num(x / 1e6, 2), "pct"),
         ("monto_mensual", "Monto mensual promedio (S/ M)", lambda x: C.num(x / 1e6, 2), "pct"),
         ("publicados", "Proyectos publicados", C.num, "pct"),
         ("financiados", "Proyectos financiados", C.num, "pct"),
         ("colocacion_pct", "Tasa de colocación (%)", lambda x: C.num(x, 1), "pp"),
         ("monto_medio", "Monto medio por proyecto (S/ miles)", lambda x: C.num(x / 1e3, 1), "pct"),
         ("plataformas_activas", "Plataformas con financiamiento", C.num, "dif"),
         ("hhi", "IHH", C.num, "dif"),
         ("empresarial_pct", "Proyectos empresariales (% del monto)", lambda x: C.num(x, 1), "pp")]


def _comparar(plataformas: list[str]) -> None:
    ps = [p for p in C.todos_los_periodos() if p >= "2022-01"]
    with st.container(key="tarjeta-comparar"):
        T.seccion("Comparar dos periodos", "compare_arrows", T.TURQUESA,
                  "Elige dos ventanas; se usan las plataformas del filtro global.")
        c1, c2 = st.columns(2, gap="large")
        a = c1.select_slider("Periodo A", ps, value=("2024-01", "2024-12"), key="w_cmp_a")
        b = c2.select_slider("Periodo B", ps, value=("2025-01", "2025-12"), key="w_cmp_b")
        base = C.base()
        ka = D.resumen(D.filtrar(base, a[0], a[1], plataformas))
        kb = D.resumen(D.filtrar(base, b[0], b[1], plataformas))
        for k in (ka, kb):
            k["monto_mensual"] = k["monto"] / k["meses"] if k["meses"] else float("nan")
        filas = []
        for clave, nombre, fmt, tipo in FILAS:
            va, vb = ka[clave], kb[clave]
            if tipo == "pct":
                d = D.variacion(vb, va)
                txt = f"{'+' if d > 0 else ''}{C.num(d, 1)} %" if pd.notna(d) else "—"
            else:
                d = vb - va if pd.notna(va) and pd.notna(vb) else float("nan")
                txt = (f"{'+' if d > 0 else ''}{C.num(d, 1 if tipo == 'pp' else 0)}{' p. p.' if tipo == 'pp' else ''}"
                       if pd.notna(d) else "—")
            filas.append({"Indicador": nombre, "A": fmt(va), "B": fmt(vb), "Variación": txt})
        c1, c2 = st.columns([1.15, 1], gap="large")
        c1.caption(f"A = {a[0]} a {a[1]} ({ka['meses']} meses) · B = {b[0]} a {b[1]} ({kb['meses']} meses)")
        c1.dataframe(pd.DataFrame(filas), hide_index=True, height=360,
                     column_config={"Indicador": st.column_config.TextColumn(width="medium")})
        if ka["meses"] != kb["meses"]:
            c1.caption(f"Los periodos tienen distinta duración ({ka['meses']} y {kb['meses']} meses): compara el monto "
                       "mensual promedio, no el total.")
        pa = D.participacion(D.filtrar(base, a[0], a[1], plataformas)).set_index("plataforma").monto
        pb = D.participacion(D.filtrar(base, b[0], b[1], plataformas)).set_index("plataforma").monto
        orden = [p for p in D.PLATAFORMAS if pa.get(p, 0) > 0 or pb.get(p, 0) > 0]
        with c2:
            if not orden:
                T.aviso("Ninguna plataforma financió proyectos en esos periodos.", "info", T.AZUL)
            else:
                fig = go.Figure()
                fig.add_bar(x=orden, y=[pa.get(p, 0) / 1e6 for p in orden], name=f"A ({a[0]} a {a[1]})",
                            marker_color="#93C5FD", hovertemplate="A: S/ %{y:.2f} M<extra></extra>")
                fig.add_bar(x=orden, y=[pb.get(p, 0) / 1e6 for p in orden], name=f"B ({b[0]} a {b[1]})",
                            marker_color=T.AZUL, hovertemplate="B: S/ %{y:.2f} M<extra></extra>")
                fig.update_layout(barmode="group", yaxis_title="S/ millones", hovermode="x unified")
                T.figura(fig, "fincrowd_comparacion_periodos", 330,
                         pd.DataFrame({"A": pa.reindex(orden).fillna(0), "B": pb.reindex(orden).fillna(0)}).rename_axis("plataforma"))


def _anual(v: pd.DataFrame) -> None:
    with st.container(key="tarjeta-anual"):
        T.seccion("Oferta anual con tus filtros", "table_chart", T.AZUL, extra=T.insignia("filtros"))
        a = D.por_anio(v)
        a = a[a.publicados + a.financiados > 0]
        if a.empty:
            T.aviso("Sin proyectos en la selección actual.", "info", T.AZUL)
        else:
            meses = v.groupby("anio").periodo.nunique()
            tabla = pd.DataFrame({
                "Año": [f"{x} ({meses[x]} m)" if meses[x] < 12 else str(x) for x in a.anio],
                "Publicados": a.publicados.map(C.num), "Financiados": a.financiados.map(C.num),
                "Colocación (%)": a.colocacion_pct.map(lambda x: C.num(x, 1)),
                "Monto (S/ M)": (a.monto / 1e6).map(lambda x: C.num(x, 2)),
                "Monto medio (S/ miles)": (a.monto_medio / 1e3).map(lambda x: C.num(x, 1)),
                "Empresarial (% del monto)": a.empresarial_pct.map(lambda x: C.num(x, 1)),
                "IHH": a.hhi.map(C.num), "Plataformas activas": a.plataformas_activas})
            st.dataframe(tabla, hide_index=True)
            st.download_button("Descargar (CSV)", a.to_csv(index=False).encode("utf-8-sig"), "fincrowd_oferta_anual.csv",
                               "text/csv", icon=":material/download:", type="tertiary", key="csv_anual")
        with st.expander("Tabla 2 del artículo (fija: todas las plataformas, años completos)", icon=":material/verified:"):
            t2 = C.tablas()["t2_oferta_anual"]
            st.dataframe(pd.DataFrame({
                "Año": [f"{x} (ene-sep)" if m < 12 else str(x) for x, m in zip(t2.anio, t2.meses)],
                "Publicados": t2.proyectos_publicados.map(C.num), "Financiados": t2.proyectos_financiados.map(C.num),
                "Colocación (%)": t2.tasa_colocacion_pct.map(lambda x: C.num(x, 1)),
                "Monto (S/ M)": (t2.monto_soles / 1e6).map(lambda x: C.num(x, 2)),
                "Var. interanual (%)": t2.var_interanual_monto_pct.map(lambda x: C.num(x, 1)),
                "Monto medio (S/ miles)": (t2.monto_promedio_proyecto_soles / 1e3).map(lambda x: C.num(x, 1)),
                "Empresarial (% del monto)": t2.participacion_empresarial_pct.map(lambda x: C.num(x, 1)),
                "IHH": t2.hhi.map(C.num)}), hide_index=True)
            T.nota("La variación de 2026 compara enero-septiembre con los mismos meses de 2025. Los agregados excluyen los "
                   "meses no obtenidos del portal, por lo que son una cota inferior. IHH máximo: 10 000.")


def _plataformas() -> None:
    with st.container(key="tarjeta-t1"):
        T.seccion("Las seis sociedades administradoras", "domain", T.VIOLETA, extra=T.insignia("articulo"))
        t1 = C.tablas()["t1_plataformas"]
        st.dataframe(pd.DataFrame({
            "Plataforma": t1.plataforma, "Lista SIMV": t1.lista_simv.str.capitalize(),
            "Meses obtenidos": [f"{a}/{b}" for a, b in zip(t1.meses_obtenidos_simv, t1.meses_periodo)],
            "Periodo con financiamiento": [f"{a} a {b}" if pd.notna(a) else "—" for a, b in
                                           zip(t1.primer_mes_financiamiento, t1.ultimo_mes_financiamiento)],
            "Proyectos financiados": t1.proyectos_financiados.map(C.num),
            "Monto (S/ M)": (t1.monto_financiado_soles / 1e6).map(lambda x: C.num(x, 2)),
            "Participación (%)": t1.participacion_monto_pct}), hide_index=True,
            column_config={"Participación (%)": st.column_config.ProgressColumn("Participación (%)", format="%.1f %%",
                                                                                min_value=0, max_value=100, color="#2563EB")})
        T.nota("Fuente: SMV (SIMV). Tabla 1 del artículo.")


def pagina() -> None:
    T.encabezado_pagina("Oferta: crecimiento rápido y muy concentrado",
                        "Proyectos publicados y financiados y monto canalizado por las plataformas autorizadas por la SMV.",
                        "monitoring", T.AZUL, "Módulo 1 · Oferta")
    desde, hasta, plataformas = C.filtros()
    T.chips_filtros(desde, hasta, plataformas, len(D.PLATAFORMAS))
    if not plataformas:
        T.aviso("Elige al menos una plataforma en la barra lateral.", "filter_alt_off", T.CORAL)
        return
    v = C.vista_filtrada()
    k = D.resumen(v)
    T.kpis([
        {"etiqueta": "Monto financiado", "valor": C.soles_m(k["monto"]), "icono": "payments", "color": T.AZUL,
         "insignia": "cota" if (v.estado_simv == "no_obtenido").any() else None,
         "sub": f"{k['meses']} meses en la ventana"},
        {"etiqueta": "Proyectos publicados", "valor": C.num(k["publicados"]), "icono": "campaign", "color": T.TURQUESA},
        {"etiqueta": "Proyectos financiados", "valor": C.num(k["financiados"]), "icono": "rocket_launch", "color": T.ESMERALDA,
         "sub": f"colocación {C.pct(k['colocacion_pct'])}"},
        {"etiqueta": "Peso de los proyectos empresariales", "valor": C.pct(k["empresarial_pct"]), "icono": "storefront",
         "color": T.VIOLETA, "sub": "del monto financiado"},
    ])
    G.monto_por_plataforma(v, desde, hasta, "oferta", permitir_real=True)
    _comparar(plataformas)
    _anual(v)
    _plataformas()
