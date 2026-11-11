# Diego Sebastián Aliaga Damián
# 2024200481M
# Tema 96: Fintech y financiamiento participativo (crowdfunding) en el Perú: oferta y condiciones
# Fecha de extracción: 2026-11-07 (censo) y 2026-11-08 (reanudación)
"""04 — Análisis financiero y estadístico: tablas y figuras del artículo (numeral 2.4.2).

Lee EXCLUSIVAMENTE datos_procesados/datos_procesados_2024200481M.csv y escribe en salidas/:
    tablas/   T1-T8 en CSV (valores sin redondear) y en LaTeX (para \\input en el artículo)
    figuras/  F1-F4 en PNG (300 ppp) y PDF (vectorial); cada figura tiene su tabla de datos en CSV
    resultados_04.json      cifras clave citadas en el texto del artículo
    manifiesto_salidas.csv  SHA-256 de cada salida (la auditoría verifica que se regeneren iguales)

Objetivos (diseño de la Fase II): OE1 oferta · OE2 plataformas · OE3 acceso y reforma (H1, H2)
· OE4 comparación con el crédito tradicional (E1, exploratoria) · sensibilidad.

Supuestos declarados (se discuten en el artículo):
    S1. `ingresos_totales_miles` es el ingreso del trimestre, no el acumulado del año: el diccionario de la
        SMV no lo precisa y los valores bajan dentro de un mismo año. T8 prueba la lectura acumulada.
    S2. Los meses `no_obtenido` del SIMV no se imputan: los agregados del FPF son una cota inferior.
    S3. La tasa de colocación se calcula sobre sumas anuales o del periodo, no mes a mes: un proyecto
        puede financiarse en un mes posterior al de su publicación.
    S4. Asociaciones no implican causalidad: H1 y E1 son evidencia descriptiva.
    S5. Algunas sociedades registraron sus EEFF en soles y no en miles (activo de cientos de miles de «miles»).
        Para el análisis se dividen entre 1 000 los registros con activo > 50 000 «miles»; se listan en resultados_04.json.
Semilla de los procedimientos aleatorios (bootstrap): 0481, de la matrícula 2024200481M (numeral 2.4.4).

Ejecución (desde la raíz del proyecto):  python codigo/04_analisis.py
"""
from __future__ import annotations

import json
import sys

import matplotlib

matplotlib.use("Agg")  # sin ventana: las figuras solo se guardan
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import stats

from comun import CODIGO_MATRICULA, PROCESADOS, SALIDAS, configurar_log, relativa, sha256_archivo

# ============================================================================
# PARÁMETROS
# ============================================================================
CSV_PROCESADO = PROCESADOS / f"datos_procesados_{CODIGO_MATRICULA}.csv"
DIR_TABLAS = SALIDAS / "tablas"
DIR_FIGURAS = SALIDAS / "figuras"
ARCHIVO_RESULTADOS = SALIDAS / "resultados_04.json"
MANIFIESTO = SALIDAS / "manifiesto_salidas.csv"

SEMILLA = 481                  # cuatro últimos dígitos de la matrícula (0481)
B_BOOTSTRAP = 10_000           # réplicas del bootstrap de medianas (H1)
B_BLOQUES, LARGO_BLOQUE = 5_000, 3   # bootstrap por bloques móviles (E1)
REFORMA = "2025-12"            # primer mes completo tras la Res. SMV N.º 019-2025-SMV/01 (14-11-2025)
REFORMA_ALTERNATIVA = "2025-11"
UMBRAL_ESCALA_EEFF = 50_000    # miles de S/: por encima, el registro se hizo en soles (supuesto S5)
MONTO_MINIMO_COCIENTE = 1_000_000  # S/ financiados en el año para calcular ingresos / monto
Z95 = stats.norm.ppf(0.975)

# Paleta categórica validada (guía de visualización), en orden fijo: el color sigue a la entidad.
COLOR_PLATAFORMA = {"Inversiones.io": "#2a78d6", "Prestopolis": "#eb6834", "Afluenta": "#1baf7a",
                    "Inversiones Neurona": "#eda100", "Proyecto Crowd": "#e87ba4", "Securite": "#008300"}
COLOR_SEGMENTO = {"tea_bcos_pyme_360": "#2a78d6", "tea_cmac_pyme_360": "#eb6834",
                  "tea_crac_pyme_360": "#1baf7a", "tea_bcos_consumo_360": "#eda100"}
TINTA, TINTA_2, TINTA_SUAVE, GRILLA, EJE = "#0b0b0b", "#52514e", "#898781", "#e1e0d9", "#c3c2b7"
NOMBRE_SEGMENTO = {"tea_bcos_pyme_360": "Bancos · pyme ≤360 d", "tea_cmac_pyme_360": "Cajas municipales · pyme ≤360 d",
                   "tea_crac_pyme_360": "Cajas rurales · pyme ≤360 d", "tea_bcos_consumo_360": "Bancos · consumo ≤360 d"}

salidas_generadas: list = []
resultados: dict = {}


# ============================================================================
# BLOQUE 1 — Lectura y agregados derivados (no se guardan en datos_procesados)
# ============================================================================
def leer_base() -> pd.DataFrame:
    tipos = {"periodo": str, "ruc": str, "empresa_id_simv": str}
    d = pd.read_csv(CSV_PROCESADO, dtype=tipos)
    flujo = [c for c in d.columns if c.startswith(("proy_", "monto_"))]
    d[flujo] = d[flujo].astype(float)
    # En meses con registros, un tipo de receptor no reportado equivale a cero proyectos (no a dato faltante)
    con = d.estado_simv == "con_registros"
    d.loc[con, flujo] = d.loc[con, flujo].fillna(0.0)
    for v in ("proy_publicados", "proy_financiados", "monto_financiado"):
        d[f"{v}_total"] = d[[f"{v}_emp", f"{v}_per", f"{v}_valores"]].sum(axis=1, min_count=1)
    d["monto_real_total"] = d.monto_financiado_total / d.ipc * 100  # soles de diciembre de 2021
    # S5. Escala de los EEFF: registros con activo > 50 000 «miles» se interpretan como hechos en soles y se
    # dividen entre 1 000 SOLO para el análisis (datos_procesados conserva el valor de la fuente).
    eeff = ["activo_total_miles", "pasivo_total_miles", "patrimonio_total_miles", "ingresos_totales_miles", "utilidad_neta_miles"]
    escala = d.activo_total_miles > UMBRAL_ESCALA_EEFF
    d.loc[escala, eeff] = d.loc[escala, eeff] / 1000
    resultados["eeff_escala_corregida"] = sorted(f"{p} {t}" for p, t in zip(d.loc[escala, "plataforma"], d.loc[escala, "trimestre_eeff"]))
    return d


def serie_mensual(d: pd.DataFrame) -> pd.DataFrame:
    """Agregado del sistema FPF por mes (suma de plataformas con registros) + tasas tradicionales."""
    con = d[d.estado_simv == "con_registros"]
    cols = [c for c in con.columns if c.startswith(("proy_", "monto_"))]
    m = con.groupby("periodo")[cols].sum()
    m["plataformas_con_registros"] = con.groupby("periodo").size()
    m["plataformas_activas"] = con[con.proy_financiados_total > 0].groupby("periodo").size()
    m["plataformas_no_obtenidas"] = d[d.estado_simv == "no_obtenido"].groupby("periodo").size()
    tasas = d.drop_duplicates("periodo").set_index("periodo")[["tamn", *COLOR_SEGMENTO, "tea_bcos_pyme_mas360",
                                                               "tea_cmac_pyme_mas360", "tea_crac_pyme_mas360", "ipc"]]
    m = tasas.join(m).fillna({"plataformas_activas": 0, "plataformas_no_obtenidas": 0, "plataformas_con_registros": 0})
    inicio = m[m.monto_financiado_total > 0].index.min()
    m["en_ventana_fpf"] = m.index >= inicio
    resultados["inicio_actividad_fpf"] = inicio
    return m


# ============================================================================
# BLOQUE 2 — Utilidades de salida (CSV, LaTeX, figuras) y registro en el manifiesto
# ============================================================================
def num(x, dec: int = 0) -> str:
    """Número con punto decimal y espacio fino de miles (recomendación de la RAE); vacío -> '—'."""
    if x is None or (isinstance(x, float) and np.isnan(x)) or pd.isna(x):
        return "—"
    return f"{x:,.{dec}f}".replace(",", "\u2009")


def guardar_tabla(raw: pd.DataFrame, formateada: pd.DataFrame, nombre: str, log, alineacion: str | None = None) -> None:
    DIR_TABLAS.mkdir(parents=True, exist_ok=True)
    csv = DIR_TABLAS / f"{nombre}.csv"
    raw.to_csv(csv, index=False, encoding="utf-8", lineterminator="\n")
    esc = lambda s: (str(s).replace("\\", "\\textbackslash{}").replace("&", "\\&").replace("%", "\\%")
                     .replace("_", "\\_").replace("#", "\\#").replace("$", "\\$").replace("\u2009", "\\,"))
    al = alineacion or ("l" + "r" * (formateada.shape[1] - 1))
    lineas = [f"% Generado por codigo/04_analisis.py; no editar a mano.", f"\\begin{{tabular}}{{{al}}}", "\\toprule",
              " & ".join(esc(c) for c in formateada.columns) + " \\\\", "\\midrule"]
    lineas += [" & ".join(esc(v) for v in fila) + " \\\\" for fila in formateada.itertuples(index=False)]
    lineas += ["\\bottomrule", "\\end{tabular}", ""]
    tex = DIR_TABLAS / f"{nombre}.tex"
    tex.write_text("\n".join(lineas), encoding="utf-8", newline="\n")
    salidas_generadas.extend([csv, tex])
    log.info("TABLA | %s | filas=%d", nombre, len(raw))


def estilo() -> None:
    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 8.5, "axes.edgecolor": EJE,
                         "axes.labelcolor": TINTA_2, "xtick.color": TINTA_2, "ytick.color": TINTA_2,
                         "axes.grid": True, "grid.color": GRILLA, "grid.linewidth": 0.6, "grid.linestyle": "-",
                         "axes.axisbelow": True, "axes.spines.top": False, "axes.spines.right": False,
                         "legend.frameon": False, "figure.dpi": 100, "savefig.dpi": 300,
                         "pdf.fonttype": 42, "axes.titlesize": 9, "axes.titleweight": "bold",
                         "axes.titlecolor": TINTA, "axes.titlelocation": "left"})


def guardar_figura(fig, nombre: str, datos: pd.DataFrame, log) -> None:
    DIR_FIGURAS.mkdir(parents=True, exist_ok=True)
    png, pdf, csv = (DIR_FIGURAS / f"{nombre}.png", DIR_FIGURAS / f"{nombre}.pdf", DIR_FIGURAS / f"{nombre}_datos.csv")
    fig.savefig(png, bbox_inches="tight", metadata={"Software": None})
    fig.savefig(pdf, bbox_inches="tight", metadata={"CreationDate": None, "Creator": None, "Producer": None})
    plt.close(fig)
    datos.to_csv(csv, index=True, encoding="utf-8", lineterminator="\n")  # vista en tabla de la figura
    salidas_generadas.extend([png, pdf, csv])
    log.info("FIGURA | %s", nombre)


def etiquetas_meses(ax, periodos: list[str], cada: int = 6) -> None:
    pos = [i for i, p in enumerate(periodos) if int(p[5:]) in (1, 7)][:: max(1, cada // 6)]
    meses = {"01": "ene", "07": "jul"}
    ax.set_xticks(pos, [f"{meses[periodos[i][5:]]}\n{periodos[i][:4]}" for i in pos])


def marcar_reforma(ax, periodos: list[str], y_texto: float | None = None, lado: str = "izquierda") -> None:
    """Línea de referencia en el mes de la reforma; el rótulo se coloca donde no tapa datos."""
    x = periodos.index(REFORMA) - 0.5
    ax.axvline(x, color=TINTA_2, linewidth=0.8)
    if y_texto is not None:
        dx, alineacion = (-0.4, "right") if lado == "izquierda" else (0.4, "left")
        ax.text(x + dx, y_texto, "Reforma del\nreglamento\n(nov-2025)", color=TINTA_2, fontsize=7, va="top", ha=alineacion)


# Títulos de las figuras: en APA 7 van en el pie de figura del artículo, no dentro de la imagen
TITULOS_FIGURAS = {
    "f1_monto_mensual_por_plataforma": "Monto financiado mensual mediante plataformas de financiamiento participativo financiero, por plataforma (S/ millones corrientes)",
    "f2_publicados_financiados_colocacion": "Proyectos publicados y financiados por mes y tasa de colocación móvil de 12 meses",
    "f3_tasas_credito_tradicional": "Tasas activas promedio del crédito tradicional en moneda nacional por segmento",
    "f4_costo_intermediacion_implicito": "Ingresos trimestrales de la plataforma líder como porcentaje del monto financiado en el trimestre"}


# ============================================================================
# BLOQUE 3 — OE1: evolución y estructura de la oferta
# ============================================================================
def t1_plataformas(d: pd.DataFrame, log) -> None:
    filas = []
    for (ruc, plataforma, lista), g in d.groupby(["ruc", "plataforma", "lista_simv"]):
        activos = g[g.proy_financiados_total > 0]
        eeff = g[g.trimestre_eeff.notna()]
        filas.append({"plataforma": plataforma, "ruc": ruc, "lista_simv": lista,
                      "meses_obtenidos_simv": int((g.estado_simv != "no_obtenido").sum()), "meses_periodo": len(g),
                      "meses_con_financiamiento": len(activos),
                      "primer_mes_financiamiento": activos.periodo.min() if len(activos) else None,
                      "ultimo_mes_financiamiento": activos.periodo.max() if len(activos) else None,
                      "proyectos_financiados": activos.proy_financiados_total.sum(),
                      "monto_financiado_soles": activos.monto_financiado_total.sum(),
                      "trimestres_eeff": len(eeff), "primer_eeff": eeff.trimestre_eeff.min() if len(eeff) else None,
                      "ultimo_eeff": eeff.trimestre_eeff.max() if len(eeff) else None})
    t = pd.DataFrame(filas).sort_values("monto_financiado_soles", ascending=False)
    total = t.monto_financiado_soles.sum()
    t["participacion_monto_pct"] = 100 * t.monto_financiado_soles / total
    f = pd.DataFrame({
        "Plataforma": t.plataforma, "Lista SIMV": t.lista_simv.str.capitalize(),
        "Meses obtenidos": [f"{a}/{b}" for a, b in zip(t.meses_obtenidos_simv, t.meses_periodo)],
        "Meses con financiamiento": t.meses_con_financiamiento,
        "Periodo de actividad": [f"{a} a {b}" if a else "—" for a, b in zip(t.primer_mes_financiamiento, t.ultimo_mes_financiamiento)],
        "Proyectos financiados": t.proyectos_financiados.map(num),
        "Monto (S/ millones)": (t.monto_financiado_soles / 1e6).map(lambda x: num(x, 2)),
        "Participación (%)": t.participacion_monto_pct.map(lambda x: num(x, 1)),
        "EEFF (trimestres)": [f"{n} ({a} a {b})" if n else "0" for n, a, b in zip(t.trimestres_eeff, t.primer_eeff, t.ultimo_eeff)]})
    guardar_tabla(t, f, "t1_plataformas", log, "lllrlrrrl")
    resultados["plataformas_con_financiamiento"] = int((t.meses_con_financiamiento > 0).sum())
    resultados["participacion_lider_periodo_pct"] = round(float(t.participacion_monto_pct.iloc[0]), 2)
    resultados["plataforma_lider"] = t.plataforma.iloc[0]


def hhi(participaciones: pd.Series) -> float:
    return float(((100 * participaciones) ** 2).sum())


def t2_anual(d: pd.DataFrame, m: pd.DataFrame, log) -> pd.DataFrame:
    con = d[d.estado_simv == "con_registros"].copy()
    filas = []
    for anio in range(2022, int(d.anio.max()) + 1):
        g = con[con.anio == anio]
        mm = m[m.index.str.startswith(str(anio))]
        monto = g.monto_financiado_total.sum()
        por_plataforma = g.groupby("plataforma").monto_financiado_total.sum()
        part = por_plataforma / monto if monto else por_plataforma * np.nan
        financiados = g.proy_financiados_total.sum()
        filas.append({"anio": anio, "meses": len(mm),
                      "plataformas_activas": int((g.groupby("plataforma").proy_financiados_total.sum() > 0).sum()),
                      "proyectos_publicados": g.proy_publicados_total.sum(), "proyectos_financiados": financiados,
                      "tasa_colocacion_pct": 100 * financiados / g.proy_publicados_total.sum(),
                      "monto_soles": monto, "monto_real_soles_dic2021": g.monto_real_total.sum(),
                      "monto_promedio_proyecto_soles": monto / financiados if financiados else np.nan,
                      "participacion_empresarial_pct": 100 * g.monto_financiado_emp.sum() / monto if monto else np.nan,
                      "hhi": hhi(part.dropna()), "participacion_lider_pct": 100 * float(part.max()),
                      "meses_plataforma_no_obtenidos": int(mm.plataformas_no_obtenidas.sum())})
    t = pd.DataFrame(filas)
    # Variación interanual comparable: misma cantidad de meses (2026 tiene ene-sep)
    ultimo = int(d.anio.max())
    meses_ultimo = int(t.loc[t.anio == ultimo, "meses"].iloc[0])
    t["var_interanual_monto_pct"] = 100 * t.monto_soles.pct_change()
    comparable = con[(con.anio == ultimo - 1) & (con.periodo.str[5:].astype(int) <= meses_ultimo)].monto_financiado_total.sum()
    t.loc[t.anio == ultimo, "var_interanual_monto_pct"] = 100 * (t.loc[t.anio == ultimo, "monto_soles"].iloc[0] / comparable - 1)
    etiqueta = lambda a: f"{a} (ene-sep)" if a == ultimo and meses_ultimo < 12 else str(a)
    f = pd.DataFrame({
        "Año": t.anio.map(etiqueta), "Plataformas activas": t.plataformas_activas,
        "Proyectos publicados": t.proyectos_publicados.map(num), "Proyectos financiados": t.proyectos_financiados.map(num),
        "Tasa de colocación (%)": t.tasa_colocacion_pct.map(lambda x: num(x, 1)),
        "Monto (S/ millones)": (t.monto_soles / 1e6).map(lambda x: num(x, 2)),
        "Var. interanual (%)": t.var_interanual_monto_pct.map(lambda x: num(x, 1)),
        "Monto medio por proyecto (S/ miles)": (t.monto_promedio_proyecto_soles / 1e3).map(lambda x: num(x, 1)),
        "Empresarial (% del monto)": t.participacion_empresarial_pct.map(lambda x: num(x, 1)),
        "IHH": t.hhi.map(num)})
    guardar_tabla(t, f, "t2_oferta_anual", log)
    resultados["anual"] = {str(r.anio): {"proyectos_financiados": int(r.proyectos_financiados), "monto_soles": int(r.monto_soles),
                                         "monto_promedio_proyecto_soles": round(float(r.monto_promedio_proyecto_soles), 0),
                                         "tasa_colocacion_pct": round(float(r.tasa_colocacion_pct), 1), "hhi": round(r.hhi, 0),
                                         "var_interanual_monto_pct": None if pd.isna(r.var_interanual_monto_pct) else round(float(r.var_interanual_monto_pct), 1)}
                           for r in t.itertuples()}
    return t


def f1_monto_mensual(d: pd.DataFrame, m: pd.DataFrame, log) -> None:
    ventana = m[m.en_ventana_fpf].index.tolist()
    con = d[(d.estado_simv == "con_registros") & d.periodo.isin(ventana)]
    tabla = con.pivot_table(index="periodo", columns="plataforma", values="monto_financiado_total", aggfunc="sum").reindex(ventana)
    activas = [p for p in COLOR_PLATAFORMA if p in tabla.columns and tabla[p].sum() > 0]
    tabla = (tabla[activas] / 1e6).fillna(0)
    fig, ax = plt.subplots(figsize=(6.3, 3.0))
    base = np.zeros(len(tabla))
    for p in activas:
        ax.bar(range(len(tabla)), tabla[p], bottom=base, width=0.8, color=COLOR_PLATAFORMA[p],
               edgecolor="white", linewidth=0.5, label=p)
        base += tabla[p].to_numpy()
    ax.set_ylabel("S/ millones (corrientes)")
    etiquetas_meses(ax, ventana)
    marcar_reforma(ax, ventana, base.max() * 0.98, lado="izquierda")
    ax.legend(loc="upper left")  # una columna: queda sobre los meses de menor monto
    ax.set_xlim(-0.8, len(tabla) - 0.2)
    guardar_figura(fig, "f1_monto_mensual_por_plataforma", tabla, log)


def f2_publicados_financiados(m: pd.DataFrame, log) -> None:
    v = m[m.en_ventana_fpf].copy()
    v["colocacion_12m_pct"] = 100 * v.proy_financiados_total.rolling(12).sum() / v.proy_publicados_total.rolling(12).sum()
    periodos = v.index.tolist()
    fig, (a1, a2) = plt.subplots(2, 1, figsize=(6.3, 4.6), sharex=True, gridspec_kw={"height_ratios": [1.4, 1]})
    for col, nombre, color in (("proy_publicados_total", "Publicados", COLOR_PLATAFORMA["Inversiones.io"]),
                               ("proy_financiados_total", "Financiados", COLOR_PLATAFORMA["Prestopolis"])):
        a1.plot(range(len(v)), v[col], color=color, linewidth=1.6, label=nombre)
    a1.set_ylabel("Proyectos por mes")
    a1.set_title("A. Proyectos publicados y financiados (todas las plataformas)")
    a1.legend(loc="upper left")
    a2.plot(range(len(v)), v.colocacion_12m_pct, color=COLOR_PLATAFORMA["Afluenta"], linewidth=1.6)
    a2.set_ylabel("%")
    a2.set_title("B. Tasa de colocación móvil de 12 meses (financiados / publicados)")
    etiquetas_meses(a2, periodos)
    marcar_reforma(a1, periodos)
    marcar_reforma(a2, periodos, a2.get_ylim()[0] + 0.32 * (a2.get_ylim()[1] - a2.get_ylim()[0]), lado="derecha")
    guardar_figura(fig, "f2_publicados_financiados_colocacion",
                   v[["proy_publicados_total", "proy_financiados_total", "colocacion_12m_pct"]], log)


# ============================================================================
# BLOQUE 4 — OE2: situación financiera de las sociedades administradoras
# ============================================================================
def ingresos_alternativos(g: pd.DataFrame) -> pd.Series:
    """Lectura acumulada (sensibilidad de S1): ingreso del trimestre = diferencia con el trimestre previo del año."""
    acumulado = g.ingresos_totales_miles
    previo = acumulado.groupby(g.anio).shift(1)
    return acumulado - previo.fillna(0)


def t3_y_f4_plataformas(d: pd.DataFrame, log) -> None:
    filas_q = []
    for plataforma, g in d.groupby("plataforma"):
        g = g.sort_values("periodo").copy()
        g["trimestre"] = g.anio.astype(str) + "-T" + ((g.mes - 1) // 3 + 1).astype(str)
        monto_q = g.groupby("trimestre").monto_financiado_total.sum(min_count=1)
        meses_ok = g.groupby("trimestre").estado_simv.apply(lambda s: (s != "no_obtenido").sum())
        e = g[g.trimestre_eeff.notna()].copy()
        e["ingresos_alt_miles"] = ingresos_alternativos(e)
        for _, r in e.iterrows():
            filas_q.append({"plataforma": plataforma, "trimestre": r.trimestre_eeff, "anio": r.anio,
                            "activo_miles": r.activo_total_miles, "pasivo_miles": r.pasivo_total_miles,
                            "patrimonio_miles": r.patrimonio_total_miles, "ingresos_miles": r.ingresos_totales_miles,
                            "ingresos_alt_miles": r.ingresos_alt_miles, "utilidad_miles": r.utilidad_neta_miles,
                            "monto_trimestre_soles": monto_q.get(r.trimestre, np.nan),
                            "meses_simv_obtenidos": int(meses_ok.get(r.trimestre, 0))})
    q = pd.DataFrame(filas_q)
    valido = (q.monto_trimestre_soles > 0) & (q.meses_simv_obtenidos == 3)
    q["costo_intermediacion_pct"] = np.where(valido, 100 * q.ingresos_miles * 1e3 / q.monto_trimestre_soles, np.nan)
    q["costo_intermediacion_alt_pct"] = np.where(valido, 100 * q.ingresos_alt_miles * 1e3 / q.monto_trimestre_soles, np.nan)
    q["no_monotono_en_el_anio"] = q.groupby(["plataforma", "anio"]).ingresos_miles.transform(lambda s: bool((s.diff() < 0).any()))
    q["trimestre_completo_simv"] = q.meses_simv_obtenidos == 3
    anual = q.groupby(["plataforma", "anio"]).agg(
        trimestres=("trimestre", "size"), activo_cierre_miles=("activo_miles", "last"),
        patrimonio_cierre_miles=("patrimonio_miles", "last"), activo_medio_miles=("activo_miles", "mean"),
        ingresos_miles=("ingresos_miles", "sum"), utilidad_miles=("utilidad_miles", "sum"),
        monto_financiado_soles=("monto_trimestre_soles", "sum"),
        simv_completo=("trimestre_completo_simv", "all")).reset_index()
    anual["roa_pct"] = 100 * anual.utilidad_miles / anual.activo_medio_miles
    anual["apalancamiento"] = (anual.activo_cierre_miles - anual.patrimonio_cierre_miles) / anual.patrimonio_cierre_miles
    # El cociente solo tiene sentido con todos los meses del SIMV obtenidos y un volumen financiado relevante
    calculable = anual.simv_completo & (anual.monto_financiado_soles >= MONTO_MINIMO_COCIENTE)
    anual["costo_intermediacion_pct"] = np.where(calculable, 100 * anual.ingresos_miles * 1e3 / anual.monto_financiado_soles, np.nan)
    f = pd.DataFrame({
        "Plataforma": anual.plataforma, "Año": anual.anio, "Trimestres": anual.trimestres,
        "Activo al cierre (S/ miles)": anual.activo_cierre_miles.map(num),
        "Patrimonio al cierre (S/ miles)": anual.patrimonio_cierre_miles.map(num),
        "Ingresos (S/ miles)": anual.ingresos_miles.map(num), "Utilidad neta (S/ miles)": anual.utilidad_miles.map(num),
        "ROA (%)": anual.roa_pct.map(lambda x: num(x, 1)),
        "Ingresos / monto financiado (%)": anual.costo_intermediacion_pct.map(lambda x: num(x, 1))})
    guardar_tabla(anual, f, "t3_plataformas_financieros", log, "lrrrrrrrr")
    q.to_csv(DIR_TABLAS / "t3b_plataformas_trimestral.csv", index=False, encoding="utf-8", lineterminator="\n")
    salidas_generadas.append(DIR_TABLAS / "t3b_plataformas_trimestral.csv")

    lider = resultados["plataforma_lider"]
    s = q[(q.plataforma == lider) & q.costo_intermediacion_pct.notna()].set_index("trimestre")
    fig, ax = plt.subplots(figsize=(6.3, 2.6))
    ax.plot(range(len(s)), s.costo_intermediacion_pct, color=COLOR_PLATAFORMA[lider], linewidth=1.6, marker="o", markersize=3.5)
    ax.set_xticks(range(len(s)), [t.replace("-", "\n") for t in s.index], fontsize=7)
    ax.set_ylabel(f"Ingresos de {lider} / monto financiado (%)")
    ax.text(len(s) - 1, s.costo_intermediacion_pct.iloc[-1], f"  {num(s.costo_intermediacion_pct.iloc[-1], 1)} %",
            color=TINTA_2, fontsize=7, va="center")
    guardar_figura(fig, "f4_costo_intermediacion_implicito", s[["ingresos_miles", "monto_trimestre_soles", "costo_intermediacion_pct"]], log)
    resultados["costo_intermediacion_lider"] = {
        "plataforma": lider, "mediana_trimestral_pct": round(float(s.costo_intermediacion_pct.median()), 2),
        "mediana_trimestral_lectura_acumulada_pct": round(float(s.costo_intermediacion_alt_pct.median()), 2),
        "trimestres": int(len(s))}
    resultados["ingresos_no_monotonos"] = {
        "plataforma_anios_con_caida": int(q.groupby(["plataforma", "anio"]).no_monotono_en_el_anio.first().sum()),
        "plataforma_anios_con_2_o_mas_trimestres": int((q.groupby(["plataforma", "anio"]).size() >= 2).sum())}


# ============================================================================
# BLOQUE 5 — OE3: condiciones de acceso y de monto; H1 y H2
# ============================================================================
def wilson(k: float, n: float) -> tuple[float, float]:
    if n <= 0:
        return np.nan, np.nan
    p = k / n
    den = 1 + Z95 ** 2 / n
    centro = (p + Z95 ** 2 / (2 * n)) / den
    margen = Z95 * np.sqrt(p * (1 - p) / n + Z95 ** 2 / (4 * n ** 2)) / den
    return 100 * (centro - margen), 100 * (centro + margen)


def t4_t5_condiciones_y_contrastes(d: pd.DataFrame, m: pd.DataFrame, log) -> None:
    con = d[d.estado_simv == "con_registros"]
    filas = []
    for periodo_nombre, filtro in (("Todo el periodo", con.periodo >= resultados["inicio_actividad_fpf"]),
                                   ("Antes de la reforma", (con.periodo >= resultados["inicio_actividad_fpf"]) & (con.periodo < REFORMA)),
                                   ("Después de la reforma", con.periodo >= REFORMA)):
        g = con[filtro]
        for tipo, sufijo in (("Empresarial", "emp"), ("Personal", "per")):
            pub, fin, monto = g[f"proy_publicados_{sufijo}"].sum(), g[f"proy_financiados_{sufijo}"].sum(), g[f"monto_financiado_{sufijo}"].sum()
            li, ls = wilson(fin, pub) if fin <= pub else (np.nan, np.nan)
            filas.append({"periodo": periodo_nombre, "tipo_receptor": tipo, "proyectos_publicados": pub, "proyectos_financiados": fin,
                          "tasa_colocacion_pct": 100 * fin / pub if pub else np.nan, "ic95_inferior": li, "ic95_superior": ls,
                          "monto_soles": monto, "monto_promedio_proyecto_soles": monto / fin if fin else np.nan})
    t4 = pd.DataFrame(filas)
    f = pd.DataFrame({"Periodo": t4.periodo, "Receptor": t4.tipo_receptor, "Publicados": t4.proyectos_publicados.map(num),
                      "Financiados": t4.proyectos_financiados.map(num),
                      "Colocación (%) [IC 95 %]": [f"{num(c, 1)} [{num(a, 1)}; {num(b, 1)}]" for c, a, b in zip(t4.tasa_colocacion_pct, t4.ic95_inferior, t4.ic95_superior)],
                      "Monto (S/ millones)": (t4.monto_soles / 1e6).map(lambda x: num(x, 2)),
                      "Monto medio (S/ miles)": (t4.monto_promedio_proyecto_soles / 1e3).map(lambda x: num(x, 1))})
    guardar_tabla(t4, f, "t4_condiciones_por_receptor", log, "llrrrrr")

    # H2: diferencia de tasas de colocación empresarial vs personal (todo el periodo), prueba z de dos proporciones
    tot = t4[t4.periodo == "Todo el periodo"].set_index("tipo_receptor")
    k1, n1 = tot.loc["Empresarial", ["proyectos_financiados", "proyectos_publicados"]]
    k2, n2 = tot.loc["Personal", ["proyectos_financiados", "proyectos_publicados"]]
    p = (k1 + k2) / (n1 + n2)
    z = (k1 / n1 - k2 / n2) / np.sqrt(p * (1 - p) * (1 / n1 + 1 / n2))
    p_h2 = 2 * stats.norm.sf(abs(z))

    contrastes = [{"contraste": "H2: colocación empresarial = personal", "estadistico": "z", "valor": z, "p_valor": p_h2,
                   "detalle": f"empresarial {100 * k1 / n1:.1f} % ({int(k1)}/{int(n1)}); personal {100 * k2 / n2:.1f} % ({int(k2)}/{int(n2)})"}]
    contrastes += contraste_h1(m, REFORMA, "monto_financiado_total", "H1: monto mensual mayor tras la reforma (corte dic-2025)")
    t5 = pd.DataFrame(contrastes)
    f = pd.DataFrame({"Contraste": t5.contraste, "Estadístico": t5.estadistico, "Valor": t5.valor.map(lambda x: num(x, 2)),
                      "p": t5.p_valor.map(lambda x: "< 0.001" if x < 0.001 else num(x, 3)), "Detalle": t5.detalle})
    guardar_tabla(t5, f, "t5_contrastes_h1_h2", log, "lcrrl")
    resultados["h2"] = {"z": round(float(z), 3), "p_valor": float(p_h2), "colocacion_empresarial_pct": round(100 * k1 / n1, 1),
                        "colocacion_personal_pct": round(100 * k2 / n2, 1)}


def contraste_h1(m: pd.DataFrame, corte: str, variable: str, nombre: str, excluir_ruc: str | None = None,
                 serie: pd.Series | None = None) -> list[dict]:
    """U de Mann-Whitney (unilateral: después > antes) e IC bootstrap de la diferencia de medianas."""
    s = serie if serie is not None else m.loc[m.en_ventana_fpf, variable]
    s = s.dropna()  # meses sin registros publicados no entran al contraste (no se imputan)
    antes, despues = s[s.index < corte].to_numpy(), s[s.index >= corte].to_numpy()
    u, p_uni = stats.mannwhitneyu(despues, antes, alternative="greater")
    rng = np.random.default_rng(SEMILLA)
    dif = np.median(rng.choice(despues, (B_BOOTSTRAP, len(despues))), axis=1) - np.median(rng.choice(antes, (B_BOOTSTRAP, len(antes))), axis=1)
    li, ls = np.percentile(dif, [2.5, 97.5])
    escala = 1e6
    res = {"contraste": nombre, "estadistico": "U", "valor": u, "p_valor": p_uni,
           "detalle": f"mediana antes {np.median(antes) / escala:.2f} M (n={len(antes)}); después {np.median(despues) / escala:.2f} M "
                      f"(n={len(despues)}); diferencia {(np.median(despues) - np.median(antes)) / escala:.2f} M, "
                      f"IC 95 % bootstrap [{li / escala:.2f}; {ls / escala:.2f}]"}
    clave = "h1" if corte == REFORMA and serie is None and variable == "monto_financiado_total" else None
    if clave:
        resultados["h1"] = {"U": float(u), "p_valor_unilateral": float(p_uni), "n_antes": len(antes), "n_despues": len(despues),
                            "mediana_antes_soles": float(np.median(antes)), "mediana_despues_soles": float(np.median(despues)),
                            "ic95_diferencia_medianas_soles": [float(li), float(ls)]}
    return [res]


# ============================================================================
# BLOQUE 6 — OE4: comparación con el crédito tradicional; E1 exploratoria
# ============================================================================
def f3_tasas_tradicionales(m: pd.DataFrame, log) -> None:
    periodos = m.index.tolist()
    fig, ax = plt.subplots(figsize=(6.3, 3.2))
    for col, color in COLOR_SEGMENTO.items():
        ax.plot(range(len(m)), m[col], color=color, linewidth=1.6, label=NOMBRE_SEGMENTO[col])
        ax.text(len(m) - 0.4, m[col].iloc[-1], f" {num(m[col].iloc[-1], 1)}", color=TINTA_2, fontsize=7, va="center")
    ax.set_ylabel("TEA (%)")
    etiquetas_meses(ax, periodos)
    quiebre = periodos.index("2025-03")
    salto = m.loc["2025-03", "tea_bcos_pyme_360"] - m.loc["2025-02", "tea_bcos_pyme_360"]
    ax.annotate(f"Bancos pyme: +{num(salto, 1)} p. p.\nen mar-2025", xy=(quiebre, m.loc["2025-03", "tea_bcos_pyme_360"] - 8),
                xytext=(quiebre + 3, 40), fontsize=7, color=TINTA_2,
                arrowprops={"arrowstyle": "-", "color": TINTA_2, "linewidth": 0.6})
    ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.2), ncols=2)  # fuera del área de datos
    ax.set_xlim(-1, len(m) + 4)
    guardar_figura(fig, "f3_tasas_credito_tradicional", m[list(COLOR_SEGMENTO)], log)
    resultados["salto_tea_bcos_pyme_2025_03_pp"] = round(float(m.loc["2025-03", "tea_bcos_pyme_360"] - m.loc["2025-02", "tea_bcos_pyme_360"]), 2)


def t6_comparabilidad(log) -> None:
    filas = [("Moneda", "Soles (SIMV)", "Moneda nacional", "Sí"),
             ("Plazo", "No publicado por operación", "Tramos ≤360 d y >360 d", "Parcial (supuesto declarado)"),
             ("Precio (tasa)", "No observado", "TEA promedio", "No: escenarios del simulador"),
             ("Costos adicionales", "Ingresos de la plataforma / monto (aprox.)", "Comisiones fuera de la TEA", "Parcial; sin TCEA"),
             ("Riesgo del receptor", "No observado (selección de la plataforma)", "Promedio de toda la cartera", "No"),
             ("Garantías", "No observadas", "No observadas", "No"),
             ("Regulador", "SMV", "SBS", "Diferencia institucional")]
    t = pd.DataFrame(filas, columns=["Dimensión", "Financiamiento participativo", "Crédito tradicional (BCRP)", "¿Comparable?"])
    guardar_tabla(t, t, "t6_comparabilidad", log, "llll")


def t7_comparacion_segmentos(d: pd.DataFrame, m: pd.DataFrame, log) -> None:
    con = d[d.estado_simv == "con_registros"]
    filas = []
    for anio in range(2022, int(d.anio.max()) + 1):
        g, mm = con[con.anio == anio], m[m.index.str.startswith(str(anio))]
        fila = {"anio": anio}
        for sufijo, nombre in (("emp", "empresarial"), ("per", "personal")):
            fin, monto = g[f"proy_financiados_{sufijo}"].sum(), g[f"monto_financiado_{sufijo}"].sum()
            fila[f"fpf_{nombre}_monto_medio_soles"] = monto / fin if fin else np.nan
        for col in COLOR_SEGMENTO:
            fila[f"{col}_media"] = mm[col].mean()
        filas.append(fila)
    t = pd.DataFrame(filas)
    f = pd.DataFrame({"Año": t.anio,
                      "FPF empresarial: monto medio (S/ miles)": (t.fpf_empresarial_monto_medio_soles / 1e3).map(lambda x: num(x, 1)),
                      "FPF personal: monto medio (S/ miles)": (t.fpf_personal_monto_medio_soles / 1e3).map(lambda x: num(x, 1)),
                      **{f"{NOMBRE_SEGMENTO[c]} (TEA %)": t[f"{c}_media"].map(lambda x: num(x, 1)) for c in COLOR_SEGMENTO}})
    guardar_tabla(t, f, "t7_comparacion_segmentos", log)


def bootstrap_bloques_spearman(x: np.ndarray, y: np.ndarray) -> tuple[float, float]:
    rng = np.random.default_rng(SEMILLA)
    n = len(x)
    inicios_posibles = n - LARGO_BLOQUE + 1
    bloques = int(np.ceil(n / LARGO_BLOQUE))
    rhos = []
    for _ in range(B_BLOQUES):
        idx = np.concatenate([np.arange(i, i + LARGO_BLOQUE) for i in rng.integers(0, inicios_posibles, bloques)])[:n]
        rhos.append(stats.spearmanr(x[idx], y[idx]).statistic)
    return tuple(np.nanpercentile(rhos, [2.5, 97.5]))


def e1(m: pd.DataFrame, tasa: str) -> dict:
    v = m[m.en_ventana_fpf]
    pares = pd.DataFrame({"dx": v.monto_financiado_total.diff(), "dy": v[tasa].diff()}).dropna()  # mismos meses
    dx, dy = pares.dx, pares.dy
    rho = stats.spearmanr(dx, dy)
    li, ls = bootstrap_bloques_spearman(dx.to_numpy(), dy.to_numpy())
    return {"contraste": f"E1: Δ monto FPF vs Δ {tasa}", "estadistico": "rho de Spearman", "valor": rho.statistic,
            "p_valor": rho.pvalue, "detalle": f"n={len(dx)} cambios mensuales; IC 95 % bootstrap por bloques [{li:.2f}; {ls:.2f}]"}


# ============================================================================
# BLOQUE 7 — Sensibilidad (T8)
# ============================================================================
def t8_sensibilidad(d: pd.DataFrame, m: pd.DataFrame, log) -> None:
    filas = []
    filas += contraste_h1(m, REFORMA, "monto_financiado_total", "H1 base: corte dic-2025, soles corrientes")
    filas += contraste_h1(m, REFORMA_ALTERNATIVA, "monto_financiado_total", "H1: corte nov-2025")
    filas += contraste_h1(m, REFORMA, "monto_real_total", "H1: soles reales de dic-2021 (IPC)")
    lider = resultados["plataforma_lider"]
    serie_lider = d[(d.plataforma == lider) & d.periodo.isin(m[m.en_ventana_fpf].index)].set_index("periodo").monto_financiado_total
    filas += contraste_h1(m, REFORMA, "", f"H1: solo {lider}", serie=serie_lider)
    otras = d[(d.plataforma != lider) & (d.estado_simv == "con_registros") & d.periodo.isin(m[m.en_ventana_fpf].index)]
    serie_otras = otras.groupby("periodo").monto_financiado_total.sum().reindex(m[m.en_ventana_fpf].index).fillna(0)
    filas += contraste_h1(m, REFORMA, "", f"H1: sin {lider}", serie=serie_otras)
    for tasa in ("tea_bcos_pyme_360", "tea_cmac_pyme_360", "tea_crac_pyme_360", "tea_bcos_pyme_mas360",
                 "tea_cmac_pyme_mas360", "tea_crac_pyme_mas360"):
        filas.append(e1(m, tasa))
    t = pd.DataFrame(filas)
    c = resultados["costo_intermediacion_lider"]
    t = pd.concat([t, pd.DataFrame([{"contraste": f"S1: ingresos/monto de {lider} (mediana trimestral)", "estadistico": "%",
                                     "valor": c["mediana_trimestral_pct"], "p_valor": np.nan,
                                     "detalle": f"lectura acumulada de los ingresos: {c['mediana_trimestral_lectura_acumulada_pct']:.2f} %"}])],
                  ignore_index=True)
    f = pd.DataFrame({"Análisis": t.contraste, "Estadístico": t.estadistico, "Valor": t.valor.map(lambda x: num(x, 2)),
                      "p": t.p_valor.map(lambda x: "—" if pd.isna(x) else ("< 0.001" if x < 0.001 else num(x, 3))),
                      "Detalle": t.detalle})
    guardar_tabla(t, f, "t8_sensibilidad", log, "lcrrl")
    resultados["e1"] = {r.contraste: {"rho": round(float(r.valor), 3), "p_valor": float(r.p_valor)}
                        for r in t.itertuples() if str(r.contraste).startswith("E1")}
    resultados["h1_sensibilidad"] = {r.contraste: {"U": float(r.valor), "p_valor_unilateral": float(r.p_valor)}
                                     for r in t.itertuples() if str(r.contraste).startswith("H1")}


# ============================================================================
# BLOQUE 8 — Resultados, manifiesto y ejecución
# ============================================================================
def escribir_resultados_y_manifiesto(log) -> None:
    ARCHIVO_RESULTADOS.write_text(json.dumps(resultados, ensure_ascii=False, indent=2, default=str), encoding="utf-8", newline="\n")
    salidas_generadas.append(ARCHIVO_RESULTADOS)
    filas = [{"archivo": p.relative_to(SALIDAS).as_posix(), "bytes": p.stat().st_size, "sha256": sha256_archivo(p)}
             for p in sorted(set(salidas_generadas))]
    pd.DataFrame(filas).to_csv(MANIFIESTO, index=False, encoding="utf-8", lineterminator="\n")
    log.info("MANIFIESTO | salidas=%d | archivo=%s", len(filas), relativa(MANIFIESTO))


def main() -> int:
    log = configurar_log("04_analisis")
    log.info("INICIO | entrada: %s | sha256=%s", relativa(CSV_PROCESADO), sha256_archivo(CSV_PROCESADO))
    salidas_generadas.clear()
    resultados.clear()
    resultados["sha256_base_procesada"] = sha256_archivo(CSV_PROCESADO)
    resultados["titulos_figuras"] = TITULOS_FIGURAS
    estilo()
    d = leer_base()
    m = serie_mensual(d)
    t1_plataformas(d, log)
    t2_anual(d, m, log)
    f1_monto_mensual(d, m, log)
    f2_publicados_financiados(m, log)
    t3_y_f4_plataformas(d, log)
    t4_t5_condiciones_y_contrastes(d, m, log)
    f3_tasas_tradicionales(m, log)
    t6_comparabilidad(log)
    t7_comparacion_segmentos(d, m, log)
    t8_sensibilidad(d, m, log)
    escribir_resultados_y_manifiesto(log)
    log.info("FIN | 04 completado | salidas=%d", len(set(salidas_generadas)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
