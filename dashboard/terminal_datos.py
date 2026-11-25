# Diego Sebastián Aliaga Damián
# 2024200481M
# Tema 96: Fintech y financiamiento participativo (crowdfunding) en el Perú: oferta y condiciones
# Fecha: 2026-11-24
"""Datos del Centro de mando (terminal 3D), sin dependencias de Streamlit (se prueban con pytest).

Todo sale de la base procesada, de las salidas de 04_analisis.py y de log_ejecucion.txt; no se consulta internet, no
se estima ningún faltante y no hay datos simulados. Lo único que no es un dato observado es la superficie de costo,
que es la fórmula de la cuota (sistema francés) evaluada en una malla de tasas y plazos, y se rotula como cálculo.
Las bandas del replay son descriptivas: media y desviación de los 12 meses anteriores; no son señales ni pronósticos.
"""
from __future__ import annotations

import math
import re
from pathlib import Path

import numpy as np
import pandas as pd

import datos as D

LOG = D.RAIZ / "log_ejecucion.txt"
INICIO = "2022-01"           # el replay empieza el año de la primera actividad (los meses previos no tienen proyectos)
TIPOS = (("emp", "Empresas"), ("per", "Personas"), ("valores", "Valores"))
TRAMO_CORTO, TRAMO_LARGO = (3, 12), (13, 60)   # plazos, en meses, de los tramos ≤360 y >360 días del BCRP


def _n(x, dec: int = 2):
    """Número apto para JSON: None si es NaN o infinito."""
    if x is None or (isinstance(x, float) and not math.isfinite(x)) or pd.isna(x):
        return None
    return round(float(x), dec)


def _lista(s, dec: int = 2) -> list:
    return [_n(x, dec) for x in s]


# ----------------------------------------------------------------------------- replay mensual
def mensual(base: pd.DataFrame) -> pd.DataFrame:
    """Una fila por mes del replay. Ventanas móviles solo con meses desde el inicio de la actividad."""
    m = D.mensual_sistema(base, INICIO)[["proy_publicados_total", "proy_financiados_total", "monto_financiado_total",
                                         "colocacion_12m_pct", "no_obtenidas"]].copy()
    m.columns = ["publicados", "financiados", "monto", "colocacion_12m_pct", "no_obtenidas"]
    m["interanual_pct"] = 100 * (m.monto / m.monto.shift(12) - 1)
    m["acumulado_12m"] = m.monto.rolling(12).sum()
    # Banda descriptiva: media y desviación estándar muestral de los 12 meses ANTERIORES al mes que se muestra
    m["media_previa"] = m.monto.shift(1).rolling(12).mean()
    m["desv_previa"] = m.monto.shift(1).rolling(12).std()
    maximo_previo = m.monto.cummax().shift(1)
    m["situacion"] = [_situacion(*x) for x in zip(m.monto, m.media_previa, m.desv_previa, maximo_previo)]
    p = D.mensual_por_plataforma(base, INICIO)
    suma = p.rolling(12).sum()
    part = suma.div(suma.sum(axis=1).replace(0, np.nan), axis=0)
    completo = m.acumulado_12m.notna()
    m["lider_12m_pct"] = (100 * part.max(axis=1)).where(completo)
    m["ihh_12m"] = ((100 * part) ** 2).sum(axis=1).where(completo)
    return m


def _situacion(monto, media, desv, maximo) -> str:
    if pd.isna(monto) or monto == 0:
        return "sin_actividad"
    if pd.isna(media) or pd.isna(desv):
        return "sin_ventana"          # con menos de 12 meses previos no se califica el mes
    if pd.notna(maximo) and monto > maximo:
        return "maximo"
    if monto > media + desv:
        return "sobre"
    return "bajo" if monto < media - desv else "dentro"


def flujos_12m(base: pd.DataFrame, meses: list[str]) -> list[dict]:
    """Por cada mes, el monto de los últimos 12 meses (o los que haya) de cada plataforma a cada tipo de receptor."""
    con = base[base.estado_simv == "con_registros"]
    salida = []
    for p in meses:
        v = con[(con.periodo > D.desplazar(p, -12)) & (con.periodo <= p)]
        g = v.groupby("plataforma")[[f"monto_financiado_{t}" for t, _ in TIPOS]].sum()
        salida.append({pl: [_n(x, 0) for x in g.loc[pl]] for pl in g.index if g.loc[pl].sum() > 0})
    return salida


# ----------------------------------------------------------------------------- superficies
def superficie_costo() -> dict:
    """Costo total por cada S/ 100 (intereses) según TEA y plazo: cuota francesa, la misma fórmula del simulador."""
    teas = [round(x, 2) for x in np.linspace(5, 80, 41)]
    plazos = [3, 4, 5, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30, 32, 34, 36, 38, 40, 42, 44, 46, 48, 50, 52, 54, 57, 60]
    z = [[_n(D.cuota_francesa(100.0, D.tem_desde_tea(t), n) * n - 100.0, 3) for t in teas] for n in plazos]
    return {"id": "costo", "tipo": "malla", "boton": "Costo del crédito", "insignia": "Cálculo",
            "titulo": "Costo total por cada S/ 100 prestados", "formula": "costo(TEA, plazo) = cuota × n − 100",
            "ejeX": {"titulo": "TEA (%)", "valores": teas, "marcas": [[t, f"{t} %"] for t in (10, 20, 30, 40, 50, 60, 70, 80)]},
            "ejeY": {"titulo": "PLAZO (MESES)", "valores": plazos, "marcas": [[n, str(n)] for n in (6, 12, 24, 36, 48, 60)]},
            "ejeZ": {"titulo": "S/", "max": 220, "marcas": [[v, f"S/ {v}"] for v in (0, 50, 100, 150, 200)]}, "z": z,
            "explica": "Es una cuenta, no un dato del FPF: para cada tasa y plazo, cuánto interés pagas por cada S/ 100. "
                       "Las líneas de colores sí son observadas: la TEA promedio de bancos y cajas (BCRP) en el mes del "
                       "replay, dibujada solo en los plazos de su tramo. Pasa el cursor para leer cualquier punto."}


def superficie_tasas(base: pd.DataFrame) -> dict:
    """TEA observada por segmento y mes (BCRP). Las cintas no se unen: los segmentos son categorías."""
    t = D.tasas_bcrp(base)
    orden = list(t.mean().sort_values().index)
    meses = list(t.index)
    anios = [(i, m[:4]) for i, m in enumerate(meses) if m.endswith("-01")]
    return {"id": "tasas", "tipo": "cintas", "boton": "Tasas de bancos y cajas", "insignia": "Observado · BCRP",
            "titulo": "TEA observada del crédito tradicional", "formula": "9 series del BCRP × 69 meses",
            "ejeX": {"titulo": "MES", "valores": list(range(len(meses))), "marcas": [[i, a] for i, a in anios]},
            "ejeY": {"titulo": "", "valores": list(range(len(orden))), "marcas": [[i, "TAMN" if s == "tamn" else D.SERIES_BCRP[s]] for i, s in enumerate(orden)]},
            "ejeZ": {"titulo": "TEA %", "max": 70, "marcas": [[v, f"{v} %"] for v in (0, 10, 20, 30, 40, 50, 60, 70)]},
            "z": [_lista(t[s]) for s in orden], "series": orden, "meses": meses,
            "explica": "Cada cinta es una tasa promedio publicada por el BCRP y avanza con el replay. Son precios de bancos y "
                       "cajas: la SMV no publica la tasa de las operaciones del FPF, así que no hay una cinta del crowdfunding."}


def superficie_monto(base: pd.DataFrame) -> dict:
    """Monto financiado por mes y año (S/ millones): una columna por mes observado."""
    s = D.mensual_sistema(base, INICIO).monto_financiado_total / 1e6
    anios = sorted({p[:4] for p in s.index})
    z = [[_n(s.get(f"{a}-{k:02d}"), 4) for k in range(1, 13)] for a in anios]
    indice = [[list(s.index).index(f"{a}-{k:02d}") if f"{a}-{k:02d}" in s.index else None for k in range(1, 13)] for a in anios]
    return {"id": "monto", "tipo": "barras", "boton": "Monto del crowdfunding", "insignia": "Observado · SMV",
            "titulo": "Monto financiado por mes y año", "formula": "S/ millones corrientes · cota inferior",
            "ejeX": {"titulo": "MES DEL AÑO", "valores": list(range(12)), "marcas": [[i, n] for i, n in enumerate(D.MESES)]},
            "ejeY": {"titulo": "", "valores": list(range(len(anios))), "marcas": [[i, a] for i, a in enumerate(anios)]},
            "ejeZ": {"titulo": "S/ M", "max": 16, "marcas": [[v, f"{v}"] for v in (0, 4, 8, 12, 16)]},
            "z": z, "indice": indice,
            "explica": "Cada columna es lo que se financió en un mes en todo el FPF. La ciudad crece con el replay: de casi "
                       "nada en 2022 a más de S/ 10 millones por mes. Donde no hay columna, no hubo proyectos o el mes aún no existe."}


# ----------------------------------------------------------------------------- consola: líneas reales del log
_URL = re.compile(r"https?://([^/\s]+)\S*")


def lineas_log(ruta: Path = LOG, maximo: int = 150) -> dict:
    """Muestra del registro real de extracción: toda la primera corrida de las API y una línea de cada k del scraping.
    Conserva el número de línea del archivo para poder verificarla."""
    if not ruta.exists():
        return {"total": 0, "http200": 0, "lineas": []}
    todas = ruta.read_text(encoding="utf-8").splitlines()
    partes = [(i, x.split(" | ")) for i, x in enumerate(todas, 1)]
    validas = [(i, p) for i, p in partes if len(p) >= 4]
    api = [x for x in validas if x[1][1] == "01_extraccion_api"][:40]
    otras = [x for x in validas if x[1][1] == "02_scraping_web"]
    k = max(1, len(otras) // max(1, maximo - len(api)))
    elegidas = api + otras[::k][: maximo - len(api)]
    salida = []
    for i, p in elegidas:
        texto = " · ".join(p[3:])
        texto = _URL.sub(lambda m: m.group(1), texto)
        texto = re.sub(r"sha256=([0-9a-f]{10})[0-9a-f]+", r"sha256=\1…", texto)
        salida.append({"n": i, "hora": p[0], "script": p[1], "nivel": p[2], "texto": texto if len(texto) <= 150 else texto[:149] + "…"})
    return {"total": len(todas), "http200": sum(" | HTTP 200 | " in x for x in todas), "lineas": salida}


# ----------------------------------------------------------------------------- cinta, hitos y relato
def cinta(base: pd.DataFrame, m: pd.DataFrame) -> list[dict]:
    """Último valor de cada serie y su cambio frente al mes anterior."""
    t = D.tasas_bcrp(base)
    ult = D.etiqueta_mes(t.index[-1])
    items = [{"t": f"FPF monto {ult}", "v": f"S/ {m.monto.iloc[-1] / 1e6:.2f} M",
              "d": _n(100 * (m.monto.iloc[-1] / m.monto.iloc[-2] - 1), 1), "u": "% mensual"},
             {"t": "FPF acumulado 12 m", "v": f"S/ {m.acumulado_12m.iloc[-1] / 1e6:.1f} M",
              "d": _n(100 * (m.acumulado_12m.iloc[-1] / m.acumulado_12m.iloc[-13] - 1), 1), "u": "% interanual"},
             {"t": "FPF colocación 12 m", "v": f"{m.colocacion_12m_pct.iloc[-1]:.1f} %",
              "d": _n(m.colocacion_12m_pct.iloc[-1] - m.colocacion_12m_pct.iloc[-13], 1), "u": "p. p. interanual"},
             {"t": "FPF IHH 12 m", "v": f"{m.ihh_12m.iloc[-1]:,.0f}".replace(",", " "), "d": None, "u": ""}]
    for s, nombre in D.SERIES_BCRP.items():
        items.append({"t": "TEA " + nombre if s != "tamn" else "TAMN", "v": f"{t[s].iloc[-1]:.2f} %",
                      "d": _n(t[s].iloc[-1] - t[s].iloc[-2], 2), "u": "p. p. mensual"})
    return items


def hitos(m: pd.DataFrame, r: dict) -> list[dict]:
    """Momentos del replay, calculados de los datos (no escritos a mano)."""
    mill = lambda x: f"S/ {x / 1e6:.2f} M"
    lista: list[dict] = []
    ini = r["inicio_actividad_fpf"]
    lista.append({"mes": ini, "sup": "monto", "titulo": "Empieza la actividad",
                  "texto": f"Primer mes con proyectos financiados en la base: {int(m.financiados[ini])} proyectos por "
                           f"S/ {m.monto[ini] / 1e3:.1f} mil."})
    for umbral in (5e6, 10e6):
        pasa = m.index[m.monto > umbral]
        if len(pasa):
            p = pasa[0]
            lista.append({"mes": p, "sup": "monto", "titulo": f"Supera S/ {umbral / 1e6:.0f} millones en un mes",
                          "texto": f"{mill(m.monto[p])} con {int(m.financiados[p])} proyectos financiados."})
    lista.append({"mes": D.QUIEBRE_TEA, "sup": "tasas", "titulo": "Salta la TEA bancaria pyme ≤360 d",
                  "texto": f"Sube {r['salto_tea_bcos_pyme_2025_03_pp']:.2f} puntos porcentuales en un mes, sin un "
                           "movimiento parecido en las cajas. Es un precio de bancos, no del FPF."})
    h1 = r["h1"]
    lista.append({"mes": D.REFORMA, "sup": "monto", "titulo": "Primer mes completo con la reforma",
                  "texto": f"La mediana mensual pasa de {mill(h1['mediana_antes_soles'])} a {mill(h1['mediana_despues_soles'])}, pero los "
                           f"{len(r['h1_tendencia']['cortes_placebo'])} cortes ficticios anteriores también salen significativos: "
                           "ya venía creciendo."})
    ult = m.index[-1]
    extra = " Es el mes más alto de la base." if m.monto[ult] == m.monto.max() else ""
    lista.append({"mes": ult, "sup": "costo", "titulo": "Último mes de la base",
                  "texto": f"{mill(m.monto[ult])} y {mill(m.acumulado_12m[ult])} en 12 meses.{extra}"})
    lista.sort(key=lambda h: h["mes"])
    return lista


# ----------------------------------------------------------------------------- paquete completo para el componente
def paquete(base: pd.DataFrame, r: dict, colores_plataforma: dict[str, str], colores_serie: dict[str, str]) -> dict:
    m = mensual(base)
    meses = list(m.index)
    p = D.mensual_por_plataforma(base, INICIO)
    con_monto = [x for x in D.PLATAFORMAS if x in p.columns and p[x].sum() > 0]
    t = D.tasas_bcrp(base).reindex(meses)
    return {
        "meses": meses, "etiquetas": [D.etiqueta_mes(x) for x in meses],
        "reforma": meses.index(D.REFORMA), "lider": r["plataforma_lider"], "sha": r["sha256_base_procesada"],
        "plataformas": [{"nombre": x, "color": colores_plataforma[x], "monto": _lista(p[x], 0)} for x in con_monto],
        "mensual": {c: (_lista(m[c], 4) if c != "situacion" else list(m[c])) for c in m.columns},
        "tasas": [{"id": s, "nombre": n, "color": colores_serie[s], "v": _lista(t[s]),
                   "tramo": None if s == "tamn" else list(TRAMO_CORTO if s.endswith("_360") else TRAMO_LARGO)}
                  for s, n in D.SERIES_BCRP.items()],
        "flujos": flujos_12m(base, meses), "tipos": [n for _, n in TIPOS],
        "superficies": [superficie_costo(), superficie_monto(base), superficie_tasas(base)],
        "desfase_tasas": list(D.tasas_bcrp(base).index).index(meses[0]),
        "cinta": cinta(base, m), "hitos": hitos(m, r), "log": lineas_log(),
    }
