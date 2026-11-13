# Diego Sebastián Aliaga Damián
# 2024200481M
# Tema 96: Fintech y financiamiento participativo (crowdfunding) en el Perú: oferta y condiciones
# Fecha: 2026-11-13
"""FinCrowd Perú: dashboard interactivo del proyecto (entrega por enlace autorizada por el docente).

Lee solo archivos del repositorio (base procesada, salidas de 04_analisis.py y productos en PDF); no consulta las
fuentes en vivo ni modifica ningún archivo. Los cálculos están en datos.py (probados en pruebas/test_dashboard.py),
la identidad visual en tema.py y cada página en vistas/.
Ejecución local (desde la raíz del proyecto):  streamlit run dashboard/app.py
Publicación: Streamlit Community Cloud, con dashboard/app.py como archivo principal.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import streamlit as st  # noqa: E402

st.set_page_config(page_title="FinCrowd Perú · Financiamiento participativo 2022-2026", page_icon=":material/insights:",
                   layout="wide", initial_sidebar_state="expanded")

import compartido as C  # noqa: E402
import datos as D  # noqa: E402
import tema as T  # noqa: E402
from vistas import (acceso, credito, datos_extraccion, inicio, oferta, plataformas, productos,  # noqa: E402
                    reproducibilidad, sensibilidad, simulador)

T.aplicar_tema()
C.iniciar_filtros()

P = {"inicio": st.Page(inicio.pagina, title="Inicio", icon=":material/space_dashboard:", default=True),
     "oferta": st.Page(oferta.pagina, title="Oferta", icon=":material/monitoring:", url_path="oferta"),
     "plataformas": st.Page(plataformas.pagina, title="Plataformas", icon=":material/domain:", url_path="plataformas"),
     "acceso": st.Page(acceso.pagina, title="Acceso y reforma", icon=":material/balance:", url_path="acceso"),
     "credito": st.Page(credito.pagina, title="Crédito tradicional", icon=":material/account_balance:",
                        url_path="credito-tradicional"),
     "sensibilidad": st.Page(sensibilidad.pagina, title="Sensibilidad", icon=":material/tune:", url_path="sensibilidad"),
     "simulador": st.Page(simulador.pagina, title="Simulador", icon=":material/calculate:", url_path="simulador"),
     "datos": st.Page(datos_extraccion.pagina, title="Datos y extracción", icon=":material/database:", url_path="datos"),
     "productos": st.Page(productos.pagina, title="Productos y descargas", icon=":material/download:", url_path="productos"),
     "reproducibilidad": st.Page(reproducibilidad.pagina, title="Reproducibilidad", icon=":material/sync_alt:",
                                 url_path="reproducibilidad")}
C.PAGINAS.update(P)

navegacion = st.navigation({"Panorama": [P["inicio"]],
                            "Análisis": [P["oferta"], P["plataformas"], P["acceso"], P["credito"], P["sensibilidad"]],
                            "Herramientas": [P["simulador"]],
                            "Evidencia": [P["datos"], P["productos"], P["reproducibilidad"]]}, expanded=True)
st.logo(str(C.IMG_MARCA), size="large", icon_image=str(C.IMG_ICONO))

with st.sidebar:
    st.html(f'<div class="fc-side-tit">{T.icono("tune", 16)}Filtros globales</div>')
    ps = C.todos_los_periodos()
    k_periodo, k_plataformas = C.clave("f_periodo"), C.clave("f_plataformas")
    st.select_slider("Periodo", options=ps, value=st.session_state["g_periodo"], key=k_periodo,
                     on_change=C.periodo_a_mano, args=(k_periodo,),
                     help="Se aplica a todas las páginas que muestran la insignia «Responde a los filtros».")
    st.pills("Plataformas", list(D.PLATAFORMAS), selection_mode="multi", default=st.session_state["g_plataformas"],
             key=k_plataformas, on_change=C.plataformas_a_mano, args=(k_plataformas,))
    st.button("Restablecer filtros", icon=":material/restart_alt:", on_click=C.restablecer, type="tertiary")
    st.html(f"""<div class="fc-side-pie">Las pruebas del artículo (H1, H2, E1) y sus tablas son fijas: no cambian con los
filtros.<br><br><b>Diego Sebastián Aliaga Damián</b><br>Finanzas I · Facultad de Economía · UNCP · 2026-II</div>""")
    st.link_button("Código en GitHub", C.REPOSITORIO, icon=":material/code:", type="tertiary")

navegacion.run()
