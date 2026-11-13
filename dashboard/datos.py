# Diego Sebastián Aliaga Damián
# 2024200481M
# Tema 96: Fintech y financiamiento participativo (crowdfunding) en el Perú: oferta y condiciones
# Fecha: 2026-11-13
"""Datos y cálculos del dashboard FinCrowd Perú, sin dependencias de Streamlit (se prueban con pytest).

Solo lee archivos del repositorio y nunca los modifica. Los agregados filtrados siguen las mismas reglas que
codigo/04_analisis.py: solo cuentan los meses `con_registros`; un tipo de receptor no reportado en un mes
observado vale cero (S2); los meses `no_obtenido` no se imputan, por lo que los montos son una cota inferior;
la colocación se calcula sobre sumas del periodo, no mes a mes (S3). Sin filtros, los resultados coinciden con
T2, T4, F1 y F2 del artículo (lo verifica pruebas/test_dashboard.py).
"""
from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

import numpy as np
import pandas as pd

RAIZ = Path(__file__).resolve().parents[1]
CSV_BASE = RAIZ / "datos_procesados" / "datos_procesados_2024200481M.csv"
TABLAS = RAIZ / "salidas" / "tablas"
FIGURAS = RAIZ / "salidas" / "figuras"
RESULTADOS = RAIZ / "salidas" / "resultados_04.json"
CIFRAS_TYPST = RAIZ / "articulo_typst" / "generado" / "cifras.typ"

REFORMA = "2025-12"      # primer mes completo tras la Res. SMV N.º 019-2025-SMV/01 (igual que 04_analisis.py)
QUIEBRE_TEA = "2025-03"  # salto de la TEA bancaria pyme <=360 d documentado en el artículo
PLATAFORMAS = ("Inversiones.io", "Afluenta", "Prestopolis", "Inversiones Neurona", "Proyecto Crowd", "Securite")
SERIES_BCRP = {"tea_bcos_pyme_360": "Bancos · pyme ≤360 d", "tea_cmac_pyme_360": "Cajas municipales · pyme ≤360 d",
               "tea_crac_pyme_360": "Cajas rurales · pyme ≤360 d", "tea_bcos_consumo_360": "Bancos · consumo ≤360 d",
               "tea_bcos_pyme_mas360": "Bancos · pyme >360 d", "tea_cmac_pyme_mas360": "Cajas municipales · pyme >360 d",
               "tea_crac_pyme_mas360": "Cajas rurales · pyme >360 d", "tea_bcos_consumo_mas360": "Bancos · consumo >360 d",
               "tamn": "TAMN (todo el crédito bancario en MN)"}
ESTADOS = {"con_registros": "Con registros", "sin_registros": "Sin registros (cero)", "no_obtenido": "No obtenido"}
_TIPOS = (("emp", "Empresarial"), ("per", "Personal"), ("valores", "Valores"))


# ----------------------------------------------------------------------------- lectura
def leer_base(ruta: Path = CSV_BASE) -> pd.DataFrame:
    """Base procesada con los totales que usa 04_analisis.py (mismas reglas de ceros y vacíos)."""
    d = pd.read_csv(ruta, dtype={"periodo": str, "ruc": str, "empresa_id_simv": str})
    flujo = [c for c in d.columns if c.startswith(("proy_", "monto_"))]
    d[flujo] = d[flujo].astype(float)
    observado = d.estado_simv.isin(["con_registros", "sin_registros"])
    d.loc[observado, flujo] = d.loc[observado, flujo].fillna(0.0)
    for v in ("proy_publicados", "proy_financiados", "monto_financiado"):
        d[f"{v}_total"] = d[[f"{v}_emp", f"{v}_per", f"{v}_valores"]].sum(axis=1, min_count=1)
    d["fecha"] = pd.to_datetime(d.periodo + "-01")
    return d


def leer_resultados() -> dict:
    return json.loads(RESULTADOS.read_text(encoding="utf-8"))


def leer_tablas() -> dict[str, pd.DataFrame]:
    return {p.stem: pd.read_csv(p, encoding="utf-8") for p in sorted(TABLAS.glob("*.csv"))}


def leer_figuras() -> dict[str, pd.DataFrame]:
    return {p.stem.replace("_datos", ""): pd.read_csv(p) for p in sorted(FIGURAS.glob("*_datos.csv"))}


def leer_cifras() -> dict[str, str]:
    """Cifras del artículo tal como se imprimen (generadas por herramientas/articulo/generar_typst.py)."""
    if not CIFRAS_TYPST.exists():
        return {}
    return dict(re.findall(r'^\s*"([^"]+)":\s*"([^"]*)",?\s*$', CIFRAS_TYPST.read_text(encoding="utf-8"), re.M))


def sha256_base(ruta: Path = CSV_BASE) -> str:
    return hashlib.sha256(ruta.read_bytes()).hexdigest()


# ----------------------------------------------------------------------------- periodos
def periodos(d: pd.DataFrame) -> list[str]:
    return sorted(d.periodo.unique())


MESES = ("ene", "feb", "mar", "abr", "may", "jun", "jul", "ago", "sep", "oct", "nov", "dic")


def etiqueta_mes(periodo: str) -> str:
    """'2025-12' -> 'dic 2025' (rótulos en castellano para los ejes)."""
    return f"{MESES[int(periodo[5:7]) - 1]} {periodo[:4]}"


def desplazar(periodo: str, meses: int) -> str:
    return (pd.Period(periodo, "M") + meses).strftime("%Y-%m")


def meses_entre(desde: str, hasta: str) -> int:
    return (pd.Period(hasta, "M") - pd.Period(desde, "M")).n + 1


def periodo_comparacion(desde: str, hasta: str, modo: str, disponibles: list[str]) -> tuple[str, str] | None:
    """Ventana con la que se comparan los KPI. modo: 'anterior' (misma duración, justo antes) o 'interanual'
    (los mismos meses un año antes; solo para ventanas de hasta 12 meses, porque con más se solaparían).
    None si no hay una ventana comparable dentro de los datos."""
    if modo == "anterior":
        n = meses_entre(desde, hasta)
        a, b = desplazar(desde, -n), desplazar(desde, -1)
    elif modo == "interanual":
        if meses_entre(desde, hasta) > 12:
            return None
        a, b = desplazar(desde, -12), desplazar(hasta, -12)
    else:
        return None
    return (a, b) if a >= disponibles[0] else None


def filtrar(d: pd.DataFrame, desde: str | None = None, hasta: str | None = None,
            plataformas: list[str] | tuple[str, ...] | None = None) -> pd.DataFrame:
    v = d
    if desde:
        v = v[v.periodo >= desde]
    if hasta:
        v = v[v.periodo <= hasta]
    if plataformas is not None:
        v = v[v.plataforma.isin(plataformas)]
    return v


# ----------------------------------------------------------------------------- indicadores
def hhi(participaciones: pd.Series) -> float:
    """Índice de Herfindahl-Hirschman con participaciones en proporción (máximo 10 000)."""
    return float(((100 * participaciones) ** 2).sum())


def resumen(v: pd.DataFrame) -> dict:
    """KPI de un subconjunto ya filtrado de la base (cualquier periodo y plataformas)."""
    con = v[v.estado_simv == "con_registros"]
    monto = float(con.monto_financiado_total.sum())
    publicados = float(con.proy_publicados_total.sum())
    financiados = float(con.proy_financiados_total.sum())
    por_plataforma = con.groupby("plataforma").monto_financiado_total.sum().sort_values(ascending=False)
    part = por_plataforma / monto if monto else por_plataforma * np.nan
    activas = con.groupby("plataforma").proy_financiados_total.sum()
    obtenidas = int((v.estado_simv != "no_obtenido").sum())
    return {"monto": monto, "publicados": publicados, "financiados": financiados,
            "colocacion_pct": 100 * financiados / publicados if publicados else np.nan,
            "monto_medio": monto / financiados if financiados else np.nan,
            "plataformas_activas": int((activas > 0).sum()), "plataformas_seleccionadas": int(v.plataforma.nunique()),
            "hhi": hhi(part.dropna()) if monto else np.nan,
            "lider": por_plataforma.index[0] if monto else None,
            "participacion_lider_pct": 100 * float(part.iloc[0]) if monto else np.nan,
            "empresarial_pct": 100 * float(con.monto_financiado_emp.sum()) / monto if monto else np.nan,
            "filas": len(v), "filas_obtenidas": obtenidas,
            "cobertura_pct": 100 * obtenidas / len(v) if len(v) else np.nan,
            "meses": int(v.periodo.nunique())}


def variacion(actual: float, previo: float) -> float:
    """Variación porcentual; NaN si el periodo de comparación no tiene base (sin actividad)."""
    if previo is None or pd.isna(previo) or previo == 0 or pd.isna(actual):
        return np.nan
    return 100 * (actual / previo - 1)


def por_anio(v: pd.DataFrame) -> pd.DataFrame:
    """Resumen anual de un subconjunto filtrado (con todos los filtros, coincide con T2)."""
    filas = [{"anio": int(a), **resumen(g)} for a, g in v.groupby("anio")]
    return pd.DataFrame(filas)


def participacion(v: pd.DataFrame) -> pd.DataFrame:
    con = v[v.estado_simv == "con_registros"]
    t = con.groupby("plataforma").agg(monto=("monto_financiado_total", "sum"), financiados=("proy_financiados_total", "sum"),
                                      publicados=("proy_publicados_total", "sum")).reset_index()
    total = t.monto.sum()
    t["participacion_pct"] = 100 * t.monto / total if total else np.nan
    return t.sort_values("monto", ascending=False)


def mensual_por_plataforma(v: pd.DataFrame, desde: str | None = None, real: bool = False) -> pd.DataFrame:
    """Monto mensual por plataforma (soles), meses sin registros = 0 (como F1). Con real=True, en soles de
    diciembre de 2021 (deflactado con el IPC de la base, como T2)."""
    con = v[v.estado_simv == "con_registros"]
    if real:
        con = con.assign(monto_financiado_total=con.monto_financiado_total / con.ipc * 100)
    meses = sorted(p for p in v.periodo.unique() if desde is None or p >= desde)
    t = con.pivot_table(index="periodo", columns="plataforma", values="monto_financiado_total", aggfunc="sum")
    return t.reindex(meses).fillna(0.0)


def mensual_sistema(v: pd.DataFrame, desde: str | None = None) -> pd.DataFrame:
    """Publicados, financiados, monto y colocación móvil de 12 meses del agregado filtrado (como F2).
    Un mes sin ninguna plataforma con registros queda vacío, igual que en 04_analisis.py."""
    con = v[v.estado_simv == "con_registros"]
    meses = sorted(p for p in v.periodo.unique() if desde is None or p >= desde)
    m = con.groupby("periodo")[["proy_publicados_total", "proy_financiados_total", "monto_financiado_total",
                                "proy_publicados_emp", "proy_financiados_emp", "proy_publicados_per",
                                "proy_financiados_per"]].sum().reindex(meses)
    m["colocacion_12m_pct"] = 100 * m.proy_financiados_total.rolling(12).sum() / m.proy_publicados_total.rolling(12).sum()
    m["no_obtenidas"] = v[v.estado_simv == "no_obtenido"].groupby("periodo").size().reindex(meses).fillna(0).astype(int)
    m.index.name = "periodo"
    return m


def agrupar(t: pd.DataFrame, nivel: str) -> pd.DataFrame:
    """Suma una tabla mensual (índice AAAA-MM) por trimestre o por año. Los periodos incompletos dentro de la
    ventana se rotulan con el número de meses que suman, para no compararlos como si fueran completos."""
    if nivel == "Mensual":
        return t
    trimestral = nivel == "Trimestral"
    clave = [f"{p[:4]}-T{(int(p[5:]) - 1) // 3 + 1}" if trimestral else p[:4] for p in t.index]
    g = t.groupby(clave, sort=True).sum(min_count=1)
    n = pd.Series(1, index=t.index).groupby(clave).sum()
    completo = 3 if trimestral else 12
    g.index = [f"{k} ({n[k]} m)" if n[k] < completo else k for k in g.index]
    return g


def colocacion_por_tipo(v: pd.DataFrame) -> pd.DataFrame:
    """Publicados, financiados y colocación por tipo de receptor (con todos los filtros del periodo, coincide con T4)."""
    con = v[v.estado_simv == "con_registros"]
    filas = []
    for suf, nombre in _TIPOS[:2]:
        pub, fin = con[f"proy_publicados_{suf}"].sum(), con[f"proy_financiados_{suf}"].sum()
        monto = con[f"monto_financiado_{suf}"].sum()
        filas.append({"tipo_receptor": nombre, "publicados": pub, "financiados": fin,
                      "colocacion_pct": 100 * fin / pub if pub else np.nan, "monto": monto,
                      "monto_medio": monto / fin if fin else np.nan})
    return pd.DataFrame(filas)


def cobertura(v: pd.DataFrame) -> pd.DataFrame:
    """Estado de la consulta al portal por plataforma y mes (para el mapa de calidad de datos)."""
    return v.pivot_table(index="plataforma", columns="periodo", values="estado_simv", aggfunc="first")


def tasas_bcrp(d: pd.DataFrame) -> pd.DataFrame:
    """Series mensuales del BCRP (una fila por mes). Son tasas observadas del crédito tradicional, no del FPF."""
    return d.drop_duplicates("periodo").set_index("periodo")[list(SERIES_BCRP)]


def intervalo_detalle(texto: str) -> tuple[float, float]:
    """Extrae el intervalo «[a; b]» del detalle de T8 (tal como lo escribió 04_analisis.py)."""
    m = re.search(r"\[(−?-?[0-9.]+);\s*(−?-?[0-9.]+)\]", str(texto))
    if not m:
        return np.nan, np.nan
    return tuple(float(x.replace("−", "-")) for x in m.groups())


def diferencia_detalle(texto: str) -> float:
    m = re.search(r"diferencia (−?-?[0-9.]+) M", str(texto))
    return float(m.group(1).replace("−", "-")) if m else np.nan


# ----------------------------------------------------------------------------- simulador (matemática financiera)
def tem_desde_tea(tea_pct: float) -> float:
    """Tasa efectiva mensual equivalente: (1 + TEA)^(1/12) − 1."""
    return (1 + tea_pct / 100) ** (1 / 12) - 1


def cuota_francesa(principal: float, tem: float, n: int) -> float:
    """Cuota constante del sistema francés: P · i / (1 − (1 + i)^−n)."""
    if tem == 0:
        return principal / n
    return principal * tem / (1 - (1 + tem) ** -n)


def cronograma(principal: float, tea_pct: float, n: int) -> pd.DataFrame:
    i = tem_desde_tea(tea_pct)
    c = cuota_francesa(principal, i, n)
    filas, saldo = [], principal
    for mes in range(1, n + 1):
        interes = saldo * i
        amort = c - interes
        saldo = max(saldo - amort, 0.0)
        filas.append({"mes": mes, "cuota": c, "interes": interes, "amortizacion": amort, "saldo": saldo})
    return pd.DataFrame(filas)


def _tir_mensual(neto_recibido: float, cuota: float, n: int) -> float:
    """Tasa mensual r que iguala lo recibido con el valor actual de las cuotas (bisección)."""
    va = lambda r: cuota * n if r == 0 else cuota * (1 - (1 + r) ** -n) / r
    if neto_recibido >= va(0.0):
        return 0.0
    lo, hi = 0.0, 1.0
    for _ in range(200):
        mid = (lo + hi) / 2
        lo, hi = (mid, hi) if va(mid) > neto_recibido else (lo, mid)
    return (lo + hi) / 2


def tcea(principal: float, tea_pct: float, n: int, comision_pct: float = 0.0) -> float:
    """Costo efectivo anual (%) de un préstamo a cuota fija con comisión inicial descontada del desembolso.
    Sin comisión es igual a la TEA."""
    c = cuota_francesa(principal, tem_desde_tea(tea_pct), n)
    r = _tir_mensual(principal * (1 - comision_pct / 100), c, n)
    return 100 * ((1 + r) ** 12 - 1)


def tea_equilibrio(principal: float, n: int, comision_pct: float, costo_objetivo_pct: float) -> float:
    """TEA hipotética que, con la comisión dada, iguala el costo efectivo anual objetivo. NaN si no existe
    (la comisión por sí sola ya supera el objetivo)."""
    if tcea(principal, 0.0, n, comision_pct) > costo_objetivo_pct:
        return np.nan
    lo, hi = 0.0, max(costo_objetivo_pct, 1.0)
    for _ in range(200):
        mid = (lo + hi) / 2
        lo, hi = (mid, hi) if tcea(principal, mid, n, comision_pct) < costo_objetivo_pct else (lo, mid)
    return (lo + hi) / 2
