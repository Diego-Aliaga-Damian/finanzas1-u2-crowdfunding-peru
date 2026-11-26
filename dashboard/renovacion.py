# Diego Sebastián Aliaga Damián
# 2024200481M
# Tema 96: Fintech y financiamiento participativo (crowdfunding) en el Perú: oferta y condiciones
# Fecha: 2026-11-25
"""Publicación sin reinicio: Streamlit Cloud cambia los archivos con la aplicación en marcha, y sin esto quedan en memoria
los módulos y los datos anteriores. app.py llama a renovar() antes de importar los demás módulos."""
from __future__ import annotations

import sys
from pathlib import Path

import streamlit as st

DASHBOARD = Path(__file__).resolve().parent
RAIZ = DASHBOARD.parent
MODULOS = {p.stem for p in DASHBOARD.glob("*.py")} - {"app", "renovacion"} | {"vistas"}


def firma() -> tuple:
    """Fecha y tamaño de los archivos que el dashboard deja en memoria (código propio y datos)."""
    archivos = [*DASHBOARD.glob("*.py"), *(DASHBOARD / "vistas").glob("*.py"), *(RAIZ / "datos_procesados").glob("*.csv"),
                *(RAIZ / "salidas").rglob("*.*"), RAIZ / "articulo_typst" / "generado" / "cifras.typ",
                *(RAIZ / "pruebas").glob("test_*.py")]
    return tuple(sorted((str(p), p.stat().st_mtime_ns, p.stat().st_size) for p in archivos if p.is_file()))


@st.cache_resource(show_spinner=False)
def _estado() -> dict:
    return {}


def renovar() -> bool:
    """Descarta los módulos propios y los datos en caché si cambió algún archivo. Devuelve si hubo cambios."""
    estado, actual = _estado(), firma()
    if estado.get("firma") == actual:
        return False
    for nombre in [n for n in sys.modules if n.split(".")[0] in MODULOS]:
        del sys.modules[nombre]
    st.cache_data.clear()
    estado["firma"] = actual
    return True
