# Diego Sebastián Aliaga Damián
# 2024200481M
# Tema 96: Fintech y financiamiento participativo (crowdfunding) en el Perú: oferta y condiciones
# Fecha: 2026-11-24
"""Centro de mando: terminal 3D con el replay histórico de la base (componente propio en WebGL, sin librerías)."""
from __future__ import annotations

import streamlit as st
import streamlit.components.v1 as components

import compartido as C
import tema as T
import terminal_datos as TD

terminal = components.declare_component("fincrowd_terminal", path=str(C.RAIZ / "dashboard" / "terminal"))


@st.cache_data(show_spinner=False)
def _paquete() -> dict:
    return TD.paquete(C.base(), C.resultados(), T.NEON_PLATAFORMA, T.NEON_SERIE)


def pagina() -> None:
    T.encabezado_pagina("Centro de mando",
                        "La historia del crowdfunding peruano mes a mes, en 3D y con los datos reales del estudio.",
                        "deployed_code", T.TURQUESA, "Terminal 3D · Replay histórico")
    st.html("<style>[data-testid='stMainBlockContainer'] { max-width: 1720px; padding: 1.6rem 1.6rem 2rem; }</style>")
    st.caption("**Cómo usarlo:** pulsa *Contar la historia* para un recorrido guiado de un minuto, o mueve la línea de tiempo: todos "
               "los paneles cambian juntos. La superficie 3D se gira arrastrando y se lee pasando el cursor.")
    terminal(datos=_paquete(), key="terminal_3d", default=None)
    with st.expander("¿Qué es dato y qué es cálculo en esta página?", icon=":material/help:"):
        st.markdown(
            "- **Observado (SMV):** montos, proyectos y receptores del portal de proyectos del FPF. Son una *cota inferior*: los "
            "meses que el portal no devolvió no se rellenan.\n"
            "- **Observado (BCRP):** las TEA de bancos y cajas. Son referencia del crédito tradicional, **no** el precio del FPF.\n"
            "- **Cálculo:** la superficie *Costo del crédito* es la fórmula de la cuota del sistema francés evaluada para cada "
            "tasa y plazo. No contiene ninguna tasa del FPF, porque la SMV no la publica.\n"
            "- **Descriptivo:** la franja del replay es la media ± 1 desviación de los 12 meses anteriores. No es un pronóstico ni "
            "una señal de inversión.\n"
            "- **Registro:** la consola repite líneas reales de `log_ejecucion.txt` (7 y 8 de noviembre de 2026); no consulta nada en vivo.")
    T.nota("Atajos del teclado dentro de la terminal: espacio (reproducir o pausar), ← → (mes), 1-3 (superficie), R (historia), "
           "F (pantalla completa). No depende de los filtros globales: muestra la base completa desde enero de 2022.")
