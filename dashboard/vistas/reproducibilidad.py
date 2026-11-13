# Diego Sebastián Aliaga Damián
# 2024200481M
# Tema 96: Fintech y financiamiento participativo (crowdfunding) en el Perú: oferta y condiciones
# Fecha: 2026-11-13
"""Reproducibilidad: cómo regenerar todo, integridad de la base, pruebas y reporte de auditoría."""
from __future__ import annotations

import streamlit as st

import compartido as C
import tema as T


def pagina() -> None:
    T.encabezado_pagina("Reproducibilidad y verificación", "Cualquier persona puede volver a generar la base, las tablas y el artículo.",
                        "sync_alt", T.ESMERALDA, "Evidencia · Reproducibilidad")
    r, aud = C.resultados(), C.auditoria()
    ok_hash, h = C.integridad()
    c1, c2 = st.columns([1.15, 1], gap="medium")
    with c1, st.container(key="tarjeta-pasos"):
        T.seccion("Pasos", "format_list_numbered", T.AZUL)
        st.code("git clone " + C.REPOSITORIO + ".git\ncd finanzas1-u2-crowdfunding-peru\n"
                "python -m venv .venv && .venv\\Scripts\\activate\npip install -r requirements.txt\n"
                "python codigo/03_limpieza_datos.py      # vuelve a generar la base desde los crudos\n"
                "python codigo/04_analisis.py            # vuelve a generar tablas, figuras y cifras\n"
                "python -m pytest                        # pruebas automatizadas (incluye el dashboard)\n"
                "python codigo/auditoria.py --en-vivo    # auditoría y cotejo con las fuentes\n"
                "streamlit run dashboard/app.py          # este dashboard", language="bash")
    with c2, st.container(key="tarjeta-verif"):
        T.seccion("Verificaciones", "verified_user", T.ESMERALDA)
        T.estado([
            {"titulo": "SHA-256 de la base procesada", "icono": "fingerprint", "nivel": "ok" if ok_hash else "error",
             "texto": f"<code>{h}</code>", "valor": "Coincide" if ok_hash else "No coincide"},
            {"titulo": "Auditoría automatizada", "icono": "fact_check",
             "nivel": "ok" if aud.get("no_cumplen") == 0 and aud.get("no_ejecutados") == 0 else "aviso",
             "texto": f"Último reporte: {aud.get('fecha', '—')}; {aud.get('no_cumplen', '—')} no cumplen y "
                      f"{aud.get('no_ejecutados', '—')} sin ejecutar.", "valor": f"{aud.get('cumplen', '—')} OK"},
            {"titulo": "Pruebas automatizadas", "icono": "bug_report", "nivel": "info",
             "texto": "Definidas en pruebas/; se ejecutan con pytest (el dashboard no las corre en línea).",
             "valor": f"{C.pruebas_definidas()} pruebas"},
            {"titulo": "Dashboard frente al artículo", "icono": "rule", "nivel": "info",
             "texto": "pruebas/test_dashboard.py comprueba que, sin filtros, los cálculos del dashboard reproducen T2, T4, F1 y F2.",
             "valor": "test_dashboard"},
        ])
    if aud:
        with st.expander("Reporte completo de la última auditoría", icon=":material/fact_check:"):
            st.markdown(aud["texto"])
