# Diego Sebastián Aliaga Damián
# 2024200481M
# Tema 96: Fintech y financiamiento participativo (crowdfunding) en el Perú: oferta y condiciones
# Fecha: 2026-11-13
"""Carga en caché, filtros globales y formatos compartidos por todas las páginas del dashboard."""
from __future__ import annotations

import base64
import re
from pathlib import Path

import pandas as pd
import streamlit as st

import datos as D

RAIZ = D.RAIZ
DESCARGAS = RAIZ / "dashboard" / "descargas"
IMG_UNCP = RAIZ / "productos" / "posteres_articulos" / "img" / "logo_uncp.png"
IMG_FACULTAD = RAIZ / "productos" / "posteres_articulos" / "img" / "logo_facultad.png"
IMG_MARCA = RAIZ / "dashboard" / "img" / "fincrowd.svg"
IMG_ICONO = RAIZ / "dashboard" / "img" / "fincrowd_icono.svg"
REPOSITORIO = "https://github.com/Diego-Aliaga-Damian/finanzas1-u2-crowdfunding-peru"
PAGINAS: dict = {}  # app.py registra aquí los objetos st.Page para los accesos directos

ATAJOS = {"Todo": None, "2024": ("2024-01", "2024-12"), "2025": ("2025-01", "2025-12"), "2026": ("2026-01", None),
          "Últimos 12 m": "ult12", "Tras la reforma": (D.REFORMA, None)}


# ----------------------------------------------------------------------------- carga (una vez por sesión del servidor)
@st.cache_data(show_spinner=False)
def base() -> pd.DataFrame:
    return D.leer_base()


@st.cache_data(show_spinner=False)
def resultados() -> dict:
    return D.leer_resultados()


@st.cache_data(show_spinner=False)
def tablas() -> dict[str, pd.DataFrame]:
    return D.leer_tablas()


@st.cache_data(show_spinner=False)
def figuras() -> dict[str, pd.DataFrame]:
    return D.leer_figuras()


@st.cache_data(show_spinner=False)
def cifras() -> dict[str, str]:
    return D.leer_cifras()


@st.cache_data(show_spinner=False)
def integridad() -> tuple[bool, str]:
    """Recalcula el SHA-256 de la base y lo compara con el que registró 04_analisis.py."""
    h = D.sha256_base()
    return h == resultados()["sha256_base_procesada"], h


@st.cache_data(show_spinner=False)
def auditoria() -> dict:
    ruta = RAIZ / "salidas" / "reporte_auditoria.md"
    if not ruta.exists():
        return {}
    texto = ruta.read_text(encoding="utf-8")
    fecha = re.search(r"Fecha y hora:\s*([0-9-]+ [0-9:]+)", texto)
    res = re.search(r"(\d+) cumplen\D+(\d+) no cumplen\D+(\d+) no ejecutados", texto)
    return {"texto": texto, "fecha": fecha.group(1) if fecha else "—",
            "cumplen": int(res.group(1)) if res else None, "no_cumplen": int(res.group(2)) if res else None,
            "no_ejecutados": int(res.group(3)) if res else None}


@st.cache_data(show_spinner=False)
def pruebas_definidas() -> int:
    return sum(len(re.findall(r"^def test_", p.read_text(encoding="utf-8"), re.M)) for p in (RAIZ / "pruebas").glob("test_*.py"))


@st.cache_data(show_spinner=False)
def imagen_b64(ruta: str) -> str:
    p = Path(ruta)
    if not p.exists():
        return ""
    tipo = "image/svg+xml" if p.suffix == ".svg" else "image/png"
    return f"data:{tipo};base64,{base64.b64encode(p.read_bytes()).decode()}"


# ----------------------------------------------------------------------------- filtros globales
def todos_los_periodos() -> list[str]:
    return D.periodos(base())


def iniciar_filtros() -> None:
    """Estado canónico de los filtros (g_*). Los widgets usan claves versionadas (g_ver): cuando un atajo cambia
    el filtro, la versión sube y los widgets se recrean con el valor nuevo, sin escribir sobre su estado."""
    ps = todos_los_periodos()
    st.session_state.setdefault("g_periodo", ("2022-01", ps[-1]))
    st.session_state.setdefault("g_plataformas", list(D.PLATAFORMAS))
    st.session_state.setdefault("g_atajo", "Todo")
    st.session_state.setdefault("g_comparar", "Año anterior")
    st.session_state.setdefault("g_ver", 0)


def clave(nombre: str) -> str:
    return f"{nombre}_{st.session_state.get('g_ver', 0)}"


def _nueva_version() -> None:
    st.session_state["g_ver"] = st.session_state.get("g_ver", 0) + 1


def aplicar_atajo(k: str) -> None:
    ps = todos_los_periodos()
    nombre = st.session_state.get(k) or "Todo"
    eleccion = ATAJOS[nombre]
    if eleccion is None:
        rango = ("2022-01", ps[-1])
    elif eleccion == "ult12":
        rango = (D.desplazar(ps[-1], -11), ps[-1])
    else:
        rango = (eleccion[0], eleccion[1] or ps[-1])
    st.session_state["g_periodo"] = rango
    st.session_state["g_atajo"] = nombre
    _nueva_version()


def periodo_a_mano(k: str) -> None:
    """El periodo se movió en la barra lateral: ningún atajo queda marcado."""
    valor = st.session_state.get(k)
    if valor and len(valor) == 2:
        st.session_state["g_periodo"] = (valor[0], valor[1])
    st.session_state["g_atajo"] = "Personalizado"
    _nueva_version()


def plataformas_a_mano(k: str) -> None:
    st.session_state["g_plataformas"] = list(st.session_state.get(k) or [])
    _nueva_version()


def activas() -> list[str]:
    con = participacion_total()
    return [p for p in D.PLATAFORMAS if p in set(con[con.monto > 0].plataforma)]


def grupo_actual() -> str | None:
    pl = set(filtros()[2])
    if pl == set(D.PLATAFORMAS):
        return "Todas"
    if pl == set(activas()):
        return "Activas"
    if pl == {resultados()["plataforma_lider"]}:
        return "Líder"
    return None


def aplicar_grupo_plataformas(k: str) -> None:
    grupo = st.session_state.get(k)
    if grupo == "Todas":
        st.session_state["g_plataformas"] = list(D.PLATAFORMAS)
    elif grupo == "Activas":
        st.session_state["g_plataformas"] = activas()
    elif grupo == "Líder":
        st.session_state["g_plataformas"] = [resultados()["plataforma_lider"]]
    _nueva_version()


def guardar_comparacion() -> None:
    st.session_state["g_comparar"] = st.session_state.get("w_comparar") or "Sin comparación"


def restablecer() -> None:
    st.session_state["g_periodo"] = ("2022-01", todos_los_periodos()[-1])
    st.session_state["g_plataformas"] = list(D.PLATAFORMAS)
    st.session_state["g_atajo"] = "Todo"
    _nueva_version()


def filtros() -> tuple[str, str, list[str]]:
    desde, hasta = st.session_state.get("g_periodo", ("2022-01", todos_los_periodos()[-1]))
    return desde, hasta, list(st.session_state.get("g_plataformas", list(D.PLATAFORMAS)))


def sin_filtro_plataforma() -> bool:
    return set(filtros()[2]) == set(D.PLATAFORMAS)


@st.cache_data(show_spinner=False)
def participacion_total() -> pd.DataFrame:
    return D.participacion(base())


def vista_filtrada() -> pd.DataFrame:
    desde, hasta, plataformas = filtros()
    return D.filtrar(base(), desde, hasta, plataformas)


# ----------------------------------------------------------------------------- formatos (como en el artículo)
NBSP = " "


def num(x, dec: int = 0) -> str:
    """Punto decimal y espacio de miles, como en el artículo; signo menos tipográfico."""
    if x is None or pd.isna(x):
        return "—"
    return f"{x:,.{dec}f}".replace(",", NBSP).replace("-", "−")


def soles_m(x, dec: int = 2) -> str:
    """Millones de soles; por debajo de S/ 1 M, en miles (para no mostrar «0.00 M»)."""
    if x is None or pd.isna(x):
        return "—"
    if 0 < abs(x) < 1e6:
        return f"S/{NBSP}{num(x / 1e3, 1)}{NBSP}mil"
    return f"S/{NBSP}{num(x / 1e6, dec)}{NBSP}M"


def pct(x, dec: int = 1) -> str:
    return f"{num(x, dec)}{NBSP}%" if pd.notna(x) else "—"


def p_txt(p: float) -> str:
    return "< 0.001" if p < 0.001 else f"= {p:.3f}"


def mes_txt(periodo: str) -> str:
    return D.etiqueta_mes(periodo)
