# Diego Sebastián Aliaga Damián
# 2024200481M
# Tema 96: Fintech y financiamiento participativo (crowdfunding) en el Perú: oferta y condiciones
# Fecha: 2026-11-13
"""Productos y descargas: artículo (LaTeX y Typst), Beamer, pósteres y repositorio."""
from __future__ import annotations

import streamlit as st

import compartido as C
import tema as T

PRODUCTOS = [
    ("Artículo (LaTeX)", "Aliaga_Damian_articulo_FPF_Peru.pdf", "article", T.AZUL,
     "Versión principal del artículo en formato APA, compilada con pdflatex y biber."),
    ("Artículo (Typst)", "Aliaga_Damian_articulo_FPF_Peru_typst.pdf", "description", T.VIOLETA,
     "El mismo artículo generado con Typst a partir de las mismas cifras, tablas y referencias."),
    ("Beamer para proyectar", "Aliaga_Damian_beamer.pdf", "slideshow", T.CORAL,
     "Diapositivas 16:9 para la exposición."),
    ("Beamer para imprimir", "Aliaga_Damian_beamer_para_imprimir.pdf", "print", T.AMARILLO,
     "Una diapositiva por hoja A4 en horizontal."),
    ("Póster del artículo (A0)", "Aliaga_Damian_poster_articulo.pdf", "photo_size_select_large", T.ESMERALDA,
     "Póster académico con los resultados principales."),
    ("20 pósteres del estado del arte", "Aliaga_Damian_posteres_20_articulos.zip", "folder_zip", T.TURQUESA,
     "Un póster A1 por cada artículo revisado (ZIP)."),
]


def pagina() -> None:
    T.encabezado_pagina("Productos y descargas", "Todo se genera con el código del repositorio a partir de los mismos datos.",
                        "download", T.CORAL, "Evidencia · Productos")
    for fila in (PRODUCTOS[:3], PRODUCTOS[3:]):
        cols = st.columns(3, gap="medium")
        for col, (titulo, archivo, ic, color, texto) in zip(cols, fila):
            ruta = C.DESCARGAS / archivo
            with col, st.container(key=f"tarjeta-prod-{archivo.split('.')[0]}"):
                tam = f"{ruta.stat().st_size / 1e6:.1f} MB" if ruta.exists() else "no disponible"
                st.html(f'<div class="fc-hall-top" style="--s:{T.SUAVE[color]};--o:{T.OSCURO[color]}"><span class="fc-hall-ic">'
                        f'{T.icono(ic)}</span><span class="fc-chip">{T.icono("draft")}{T.e(tam)}</span></div>'
                        f'<div class="fc-hall-t">{T.e(titulo)}</div><div class="fc-hall-x">{T.e(texto)}</div>')
                if ruta.exists():
                    st.download_button("Descargar", ruta.read_bytes(), file_name=archivo, key=f"dl_{archivo}",
                                       mime="application/zip" if archivo.endswith(".zip") else "application/pdf",
                                       icon=":material/download:", width="stretch")
                else:
                    st.caption("Compílalo y ejecuta herramientas/productos/preparar_dashboard.py.")
    with st.container(key="tarjeta-repo"):
        T.seccion("Repositorio completo", "code", T.AZUL, "Código, datos crudos y procesados, salidas, artículo y productos.")
        st.link_button("Abrir en GitHub", C.REPOSITORIO, icon=":material/open_in_new:", type="primary")
