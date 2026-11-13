# Diego Sebastián Aliaga Damián
# 2024200481M
# Tema 96: Fintech y financiamiento participativo (crowdfunding) en el Perú: oferta y condiciones
# Fecha: 2026-11-13
"""Datos y extracción: fuentes, cobertura del portal, base procesada para explorar y diccionario de variables."""
from __future__ import annotations

import re

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

import compartido as C
import datos as D
import tema as T


def _mapa_cobertura(v: pd.DataFrame) -> None:
    cob = D.cobertura(v).reindex([p for p in reversed(D.PLATAFORMAS) if p in set(v.plataforma)])
    codigos = {"con_registros": 2, "sin_registros": 1, "no_obtenido": 0}
    z = cob.apply(lambda c: c.map(codigos)).astype(float)
    texto = cob.apply(lambda c: c.map(D.ESTADOS))
    fig = go.Figure(go.Heatmap(
        z=z.to_numpy(), x=[D.etiqueta_mes(p) for p in cob.columns], y=cob.index, text=texto.to_numpy(), xgap=1.5, ygap=3,
        colorscale=[[0, T.CORAL], [0.333, T.CORAL], [0.333, "#E2E8F0"], [0.666, "#E2E8F0"], [0.666, T.ESMERALDA], [1, T.ESMERALDA]],
        zmin=-0.5, zmax=2.5, showscale=False, hovertemplate="<b>%{y}</b> · %{x}<br>%{text}<extra></extra>"))
    T.eje_meses(fig, list(cob.columns))
    for est, nombre in D.ESTADOS.items():  # leyenda manual
        fig.add_scatter(x=[None], y=[None], mode="markers", name=nombre, marker=dict(size=11, symbol="square", color=T.COLOR_ESTADO[est] if est != "sin_registros" else "#E2E8F0"))
    fig.update_layout(yaxis=dict(showgrid=False), margin=dict(l=6, t=34))
    T.figura(fig, "fincrowd_cobertura_portal", 300, cob)


def pagina() -> None:
    r, cif = C.resultados(), C.cifras()
    T.encabezado_pagina("Datos y extracción automatizada",
                        "Dos vías automatizadas: interfaces de programación (API) y rastreo programático de un portal institucional.",
                        "database", T.TURQUESA, "Evidencia · Datos")
    T.hallazgos([
        {"titulo": "BCRP · BCRPData (API)", "icono": "api", "color": T.AZUL, "insignia": "observado",
         "texto": "10 series mensuales: TEA de pequeña y microempresa y de consumo por tipo de entidad y plazo, TAMN e IPC.<br>"
                  "<code>estadisticas.bcrp.gob.pe/estadisticas/series/api/</code>"},
        {"titulo": "SMV · OData (API)", "icono": "account_tree", "color": T.VIOLETA, "insignia": "observado",
         "texto": "Estados financieros trimestrales de las sociedades administradoras de plataformas.<br>"
                  "<code>mvnet.smv.gob.pe/SMV.OData.Api/api/InfFinanciera</code>"},
        {"titulo": "SMV · SIMV «Información de Proyectos» (scraping)", "icono": "travel_explore", "color": T.ESMERALDA,
         "insignia": "observado",
         "texto": "Proyectos publicados, financiados y monto por plataforma, mes y tipo de receptor.<br>"
                  "<code>smv.gob.pe/SIMV/Frm_ProyectosFPF</code>"},
    ])
    d = C.base()
    ok_hash, h = C.integridad()
    k = D.resumen(d)
    T.kpis([
        {"etiqueta": "Filas del panel plataforma-mes", "valor": C.num(len(d)), "icono": "table_rows", "color": T.AZUL,
         "sub": f"{d.shape[1] - 4} columnas de la base · {d.plataforma.nunique()} plataformas"},
        {"etiqueta": "Periodo", "valor": f"{d.periodo.min()} a {d.periodo.max()}", "icono": "date_range", "color": T.TURQUESA,
         "sub": f"{d.periodo.nunique()} meses"},
        {"etiqueta": "Cobertura del portal", "valor": C.pct(k["cobertura_pct"]), "icono": "travel_explore", "color": T.AMARILLO,
         "insignia": "cota", "sub": f"{k['filas_obtenidas']} de {k['filas']} plataforma-mes"},
        {"etiqueta": "Solicitudes HTTP 200", "valor": cif.get("solicitudesHTTP", "—"), "icono": "cloud_done", "color": T.VIOLETA,
         "sub": "registradas en los logs de extracción"},
        {"etiqueta": "Integridad (SHA-256)", "valor": "Coincide" if ok_hash else "No coincide", "icono": "fingerprint",
         "color": T.ESMERALDA if ok_hash else T.CORAL, "sub": h[:12] + "…"},
    ])

    desde, hasta, plataformas = C.filtros()
    with st.container(key="tarjeta-cobertura-mapa"):
        T.seccion("Respuesta del portal por plataforma y mes", "grid_on", T.ESMERALDA,
                  "Sin registros = el portal respondió sin proyectos (cuenta como cero). No obtenido = no se pudo leer "
                  "(no se imputa).", extra=T.insignia("filtros"))
        if plataformas:
            _mapa_cobertura(C.vista_filtrada())

    with st.container(key="tarjeta-explorar"):
        T.seccion("Explorar la base procesada", "manage_search", T.AZUL, extra=T.insignia("filtros"))
        T.chips_filtros(desde, hasta, plataformas, len(D.PLATAFORMAS))
        estados = st.pills("Estado de la consulta", list(D.ESTADOS), selection_mode="multi", default=list(D.ESTADOS),
                           format_func=D.ESTADOS.get, key="w_estados")
        original = pd.read_csv(D.CSV_BASE, dtype={"periodo": str, "ruc": str, "empresa_id_simv": str})
        vista = original[original.plataforma.isin(plataformas) & original.estado_simv.isin(estados or [])
                         & original.periodo.between(desde, hasta)]
        st.dataframe(vista, hide_index=True, height=360)
        c1, c2 = st.columns(2)
        c1.download_button(f"Descargar la vista filtrada ({len(vista)} filas, CSV)", vista.to_csv(index=False).encode("utf-8-sig"),
                           "fincrowd_base_filtrada.csv", "text/csv", icon=":material/filter_alt:", type="tertiary")
        c2.download_button("Descargar la base procesada completa (CSV)", D.CSV_BASE.read_bytes(),
                           D.CSV_BASE.name, "text/csv", icon=":material/download:", type="tertiary")
        T.nota("La tabla muestra la base tal como está en datos_procesados/ (sin los ceros que el análisis asigna a los tipos de "
               "receptor no reportados en meses observados).")

    c1, c2 = st.columns(2, gap="medium")
    with c1, st.expander("Diccionario de variables", icon=":material/menu_book:"):
        filas = [l for l in (D.RAIZ / "diccionario_variables.md").read_text(encoding="utf-8").splitlines()
                 if re.match(r"^\| \d+ \|", l)]
        dic = pd.DataFrame([[x.strip().strip("`") for x in f.strip("|").split("|")][1:6] for f in filas],
                           columns=["Variable", "Definición", "Unidad", "Frecuencia", "Fuente"])
        st.dataframe(dic, hide_index=True)
    with c2, st.expander("Demostración en vivo de la extracción", icon=":material/play_circle:"):
        st.code("python codigo/02_scraping_web.py --demo      # 3 solicitudes al portal de la SMV (≈ 15 s)\n"
                "python codigo/auditoria.py --en-vivo          # coteja 10 filas al azar con BCRP y SMV", language="bash")
        st.write("Ninguno de los dos comandos modifica los datos crudos.")
