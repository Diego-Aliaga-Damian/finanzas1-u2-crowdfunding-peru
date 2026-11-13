# Diego Sebastián Aliaga Damián
# 2024200481M
# Tema 96: Fintech y financiamiento participativo (crowdfunding) en el Perú: oferta y condiciones
# Fecha de extracción: 2026-11-07 (censo) y 2026-11-08 (reanudación)
"""Pruebas de la interfaz del dashboard con el simulador oficial de Streamlit (AppTest): cada página se renderiza
sin excepciones y los filtros globales cambian los KPI con las cifras del artículo. Se omiten si Streamlit no
está instalado (sus dependencias están en dashboard/requirements.txt)."""
import re

import pandas as pd
import pytest

from conftest import RAIZ

testing = pytest.importorskip("streamlit.testing.v1")
pytest.importorskip("plotly")

DASHBOARD = RAIZ / "dashboard"
PAGINAS = ["inicio", "oferta", "plataformas", "acceso", "credito", "sensibilidad", "simulador", "datos_extraccion",
           "productos", "reproducibilidad"]


def _render(dir_dashboard: str, modulo: str) -> None:
    import importlib
    import sys
    sys.path.insert(0, dir_dashboard)
    import compartido as C
    import tema as T
    T.aplicar_tema()
    C.iniciar_filtros()
    importlib.import_module(f"vistas.{modulo}").pagina()


def _kpis(at) -> dict[str, tuple[str, str]]:
    html = " ".join(h.proto.body for h in at.get("html") if "fc-kpis" in h.proto.body)
    patron = (r'fc-kpi-et">([^<]+)</div>\s*<div class="fc-kpi-va">([^<]+)</div>'
              r'(?:<div class="fc-kpi-de [a-z]+"><span class="fc-ic"[^>]*>[a-z_]+</span>([^<]+))?')
    return {et: (va.replace(" ", " "), (de or "").replace(" ", " ")) for et, va, de in re.findall(patron, html)}


@pytest.mark.parametrize("modulo", PAGINAS)
def test_cada_pagina_se_renderiza_sin_errores(modulo):
    at = testing.AppTest.from_function(_render, args=(str(DASHBOARD), modulo), default_timeout=90)
    at.run()
    assert not at.exception, [e.value for e in at.exception]


def test_filtros_globales_actualizan_los_kpi_con_cifras_del_articulo():
    t2 = pd.read_csv(RAIZ / "salidas" / "tablas" / "t2_oferta_anual.csv").set_index("anio")
    at = testing.AppTest.from_file(str(DASHBOARD / "app.py"), default_timeout=90)
    at.run()
    assert not at.exception
    at.button_group(key=f"w_atajo_{at.session_state['g_ver']}").set_value("2025").run()
    assert at.session_state["g_periodo"] == ("2025-01", "2025-12")
    monto, delta = _kpis(at)["Monto financiado"]
    assert monto == f"S/ {t2.loc[2025, 'monto_soles'] / 1e6:.2f} M"
    assert delta == f"+{t2.loc[2025, 'var_interanual_monto_pct']:.1f} %"
    # El grupo «Líder» deja solo la plataforma líder; el periodo se conserva
    at.button_group(key=f"w_grupo_{at.session_state['g_ver']}").set_value("Líder").run()
    assert at.session_state["g_plataformas"] == ["Inversiones.io"] and at.session_state["g_periodo"] == ("2025-01", "2025-12")
    # Mover el periodo en la barra lateral desmarca el atajo
    at.select_slider(key=f"f_periodo_{at.session_state['g_ver']}").set_range("2024-01", "2024-12").run()
    assert at.session_state["g_atajo"] == "Personalizado" and at.session_state["g_periodo"] == ("2024-01", "2024-12")
    # Restablecer vuelve al estado inicial
    next(b for b in at.get("button") if "Restablecer" in str(b.label)).click().run()
    assert at.session_state["g_periodo"] == ("2022-01", "2026-09") and len(at.session_state["g_plataformas"]) == 6
    assert not at.exception
