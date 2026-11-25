# Diego Sebastián Aliaga Damián
# 2024200481M
# Tema 96: Fintech y financiamiento participativo (crowdfunding) en el Perú: oferta y condiciones
# Fecha de extracción: 2026-11-07 (censo) y 2026-11-08 (reanudación)
"""Pruebas econométricas del artículo. Este módulo solo calcula; 04_analisis.py lo llama, guarda las tablas T9-T15 y
la figura F5 y registra los resultados.

Estrategia (la misma secuencia de la Unidad I, adaptada a este tema):
    0. Verificación del tamaño de muestra por variable: al menos 1 000 observaciones o 60 periodos mensuales.
    1. Raíz unitaria: ADF (H0: raíz unitaria), KPSS (H0: estacionaria) y Zivot-Andrews (raíz unitaria con un quiebre).
    2. Largo plazo: cointegración de Engle-Granger y de Johansen (traza) entre el monto del FPF y cada TEA; Granger.
    3. Corto plazo: modelo dinámico en diferencias con errores HAC (Newey-West) y pruebas de diagnóstico.
    4. Reforma de noviembre de 2025 (H1): regresión segmentada (serie de tiempo interrumpida), con cortes ficticios.
    5. Colocación (H2): logit sobre los proyectos publicados.
    6. Rentabilidad de las administradoras (OE2): panel de empresas supervisadas por la SMV, con efectos de trimestre.

Decisiones fijadas antes de estimar, para no elegir la especificación por su resultado:
    - El monto mensual del sistema va en soles de diciembre de 2021 y con seno hiperbólico inverso, asinh(S/ millones),
      que se comporta como el logaritmo y admite los 17 meses sin proyectos (así cada serie conserva 69 periodos).
    - Comparadores: las cuatro TEA de hasta 360 días de la Figura de tasas. La TAMN no entra en los modelos porque
      promedia todo el crédito bancario y contiene a las demás; solo se prueba su raíz unitaria.
    - Rezagos: ADF por AIC; Johansen por BIC con un mínimo de 1; HAC con floor(4(T/100)^(2/9)) rezagos.
    - Impulsos: un mes con un salto de tasa que se revierte o no tiene explicación publicada lleva su propia variable
      ficticia (ene-2024 y feb-2024 en cajas municipales; mar-2025 en bancos). Se muestran las dos versiones.
    - Se informa siempre la sensibilidad con los 52 meses de actividad, aunque queda por debajo de 60 periodos.
Ninguna estimación tiene interpretación causal.
"""
from __future__ import annotations

import warnings

import numpy as np
import pandas as pd
import statsmodels.api as sm
from statsmodels.stats.diagnostic import acorr_breusch_godfrey, breaks_cusumolsresid, het_breuschpagan, linear_reset
from statsmodels.stats.stattools import durbin_watson, jarque_bera
from statsmodels.tsa.stattools import adfuller, coint, grangercausalitytests, kpss, zivot_andrews
from statsmodels.tsa.vector_ar.vecm import coint_johansen, select_order

MIN_OBSERVACIONES, MIN_PERIODOS = 1_000, 60    # criterio del curso: por cada variable
ALFA = 0.05
TASAS = {"tea_bcos_pyme_360": "Bancos, pyme ≤360 d", "tea_cmac_pyme_360": "Cajas municipales, pyme ≤360 d",
         "tea_crac_pyme_360": "Cajas rurales, pyme ≤360 d", "tea_bcos_consumo_360": "Bancos, consumo ≤360 d"}
IMPULSOS = ("2024-01", "2024-02", "2025-03")
COMPARABLES = ("SOCIEDADES AGENTES DE BOLSA", "SOCIEDADES ADMINISTRADORAS DE FONDOS MUTUOS Y FONDOS DE INVERSION",
               "SOCIEDADES ADMINISTRADORAS DE FONDOS DE INVERSION", "SOCIEDADES TITULIZADORAS",
               "EMPRESAS ADMINISTRADORAS DE FONDOS COLECTIVOS")
CUENTAS = ["activo_total_miles", "pasivo_total_miles", "patrimonio_total_miles", "ingresos_totales_miles", "utilidad_neta_miles"]


# ============================================================================
# 0. Series y verificación del tamaño de muestra
# ============================================================================
def series_mensuales(m: pd.DataFrame) -> pd.DataFrame:
    """69 meses. Un mes sin ningún registro vale cero (S2 de 04): el portal respondió que no había proyectos."""
    s = pd.DataFrame(index=m.index)
    s["monto_real"] = m.monto_financiado_total.fillna(0.0) / m.ipc * 100 / 1e6   # S/ millones de dic-2021
    s["fpf"] = np.arcsinh(s.monto_real)
    for c in TASAS:
        s[c] = m[c]
    s["tamn"], s["ln_ipc"] = m.tamn, np.log(m.ipc)
    s["inflacion"] = 100 * s.ln_ipc.diff()
    s["activo"] = m.en_ventana_fpf.astype(bool)
    return s


def ajustar_escala_fpf(e: pd.DataFrame, umbral: float) -> pd.DataFrame:
    """Aplica a las plataformas de FPF la misma regla S5 de 04 (registros hechos en soles y no en miles)."""
    e = e.copy()
    escala = e.es_fpf.eq(1) & (e.activo_total_miles > umbral)
    con_referencia = e.es_fpf.eq(1) & e.rpj.isin(e.loc[e.es_fpf.eq(1) & ~escala, "rpj"].unique())
    e.loc[escala & con_referencia, CUENTAS] = e.loc[escala & con_referencia, CUENTAS] / 1000
    return e[~(escala & ~con_referencia)]


def verificacion_muestra(d: pd.DataFrame, s: pd.DataFrame, proyectos: pd.DataFrame, empresas: pd.DataFrame) -> pd.DataFrame:
    """Observaciones válidas por variable en cada bloque y si cumplen el mínimo (1 000 o 60 periodos por variable)."""
    largo = pd.concat([d[["periodo", "plataforma", "proy_publicados_" + t, "proy_financiados_" + t, "monto_financiado_" + t]]
                       .set_axis(["periodo", "plataforma", "publicados", "financiados", "monto"], axis=1).assign(receptor=t)
                       for t in ("emp", "per", "valores")])
    mensual = s[["fpf", *TASAS, "tamn", "ln_ipc"]]
    comparables = empresas[empresas.tipo_empresa.isin(COMPARABLES) | empresas.es_fpf.eq(1)]
    plataformas = d[CUENTAS]
    filas = [("Series mensuales del sistema (pruebas de series de tiempo)", "mes", mensual.shape[1], int(mensual.notna().sum().min()), "periodos"),
             ("Celdas del portal SIMV (plataforma-mes-receptor)", "celda", 3, int(largo[["publicados", "financiados", "monto"]].notna().sum().min()), "observaciones"),
             ("Proyectos publicados (logit de colocación)", "proyecto", 4, len(proyectos), "observaciones"),
             ("Estados financieros de todas las empresas supervisadas", "empresa-trimestre", 5, int(empresas[CUENTAS].notna().sum().min()), "observaciones"),
             ("Estados financieros de intermediarios comparables", "empresa-trimestre", 5, int(comparables[CUENTAS].notna().sum().min()), "observaciones"),
             ("Estados financieros solo de las plataformas de FPF", "plataforma-trimestre", 5, int(plataformas.notna().sum().min()), "observaciones")]
    t = pd.DataFrame(filas, columns=["bloque", "unidad", "variables", "datos_por_variable", "criterio"])
    t["minimo_por_variable"] = np.where(t.criterio == "periodos", MIN_PERIODOS, MIN_OBSERVACIONES)
    t["datos_totales"] = t.variables * t.datos_por_variable
    t["minimo_total"] = t.variables * t.minimo_por_variable
    t["cumple"] = t.datos_por_variable >= t.minimo_por_variable
    return t


# ============================================================================
# 1. Raíz unitaria
# ============================================================================
def _kpss(x: pd.Series) -> tuple[float, float]:
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")           # statsmodels avisa que el valor p está acotado a [0.01; 0.10]
        e, p, *_ = kpss(x, regression="c", nlags="auto")
    return float(e), float(p)


def raiz_unitaria(s: pd.DataFrame) -> pd.DataFrame:
    nombres = {"fpf": "Monto del FPF (asinh, S/ reales)", **{k: "TEA " + v for k, v in TASAS.items()}, "tamn": "TAMN", "ln_ipc": "IPC (logaritmo)"}
    filas = []
    for c, nombre in nombres.items():
        x = s[c].dropna()
        n, dx = adfuller(x, regression="c", autolag="AIC", result_object=False), adfuller(x.diff().dropna(), regression="c", autolag="AIC", result_object=False)
        (kn, pkn), (kd, pkd) = _kpss(x), _kpss(x.diff().dropna())
        z = zivot_andrews(x.to_numpy(), regression="c", autolag="AIC")
        quiebre = x.index[min(z[4] + 1, len(x) - 1)]  # primer mes del nuevo nivel
        if n[1] < ALFA:
            conclusion = "I(0)"
        elif dx[1] < ALFA:
            conclusion = "I(1)" if pkd >= ALFA else "I(1), con reserva"
        else:
            conclusion = "No concluyente"
        if z[1] < ALFA and conclusion != "I(0)":
            conclusion += "; I(0) con quiebre"
        a52 = adfuller(x[s.activo], regression="c", autolag="AIC", result_object=False)
        filas.append({"variable": c, "nombre": nombre, "n": len(x), "adf_nivel": n[0], "adf_nivel_p": n[1], "adf_nivel_rezagos": n[2],
                      "adf_dif": dx[0], "adf_dif_p": dx[1], "adf_dif_rezagos": dx[2], "kpss_nivel": kn, "kpss_nivel_p": pkn,
                      "kpss_dif": kd, "kpss_dif_p": pkd, "za": z[0], "za_p": z[1], "za_quiebre": quiebre,
                      "adf_nivel_p_52": a52[1], "conclusion": conclusion})
    return pd.DataFrame(filas)


# ============================================================================
# 2. Largo plazo: cointegración y causalidad de Granger
# ============================================================================
def _rezagos(x: np.ndarray) -> int:
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        return max(1, int(select_order(x, maxlags=6, deterministic="co").bic))


def _johansen(x: np.ndarray) -> tuple[int, float, float, int]:
    k = _rezagos(x)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")           # parte imaginaria nula por redondeo (traza verificada en las pruebas)
        j = coint_johansen(x, 0, k)
    rango = next((r for r in range(x.shape[1]) if j.lr1[r] <= j.cvt[r, 1]), x.shape[1])
    return k, float(j.lr1[0]), float(j.cvt[0, 1]), rango


def _granger(causa: pd.Series, efecto: pd.Series, rezagos: int = 1) -> float:
    g = pd.DataFrame({"y": efecto.diff(), "x": causa.diff()}).dropna()
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        r = grangercausalitytests(g.to_numpy(), maxlag=[rezagos])
    return float(r[rezagos][0]["ssr_ftest"][1])


def cointegracion(s: pd.DataFrame) -> tuple[pd.DataFrame, dict]:
    activos = s[s.activo]
    filas = []
    for c, nombre in TASAS.items():
        eg = coint(s.fpf, s[c], trend="c", autolag="aic")
        eg52 = coint(activos.fpf, activos[c], trend="c", autolag="aic")
        k, traza, vc, rango = _johansen(s[["fpf", c]].to_numpy())
        filas.append({"relacion": f"FPF y TEA {nombre}", "engle_granger": eg[0], "engle_granger_p": eg[1], "engle_granger_p_52": eg52[1],
                      "johansen_rezagos": k, "johansen_traza": traza, "johansen_vc5": vc, "johansen_rango": rango,
                      "granger_tasa_a_fpf_p": _granger(s[c], s.fpf), "granger_fpf_a_tasa_p": _granger(s.fpf, s[c])})
    cols = ["fpf", *TASAS]
    eg = coint(s.fpf, s[list(TASAS)], trend="c", autolag="aic")
    eg52 = coint(activos.fpf, activos[list(TASAS)], trend="c", autolag="aic")
    k, traza, vc, rango = _johansen(s[cols].to_numpy())
    filas.append({"relacion": "FPF y las cuatro TEA (sistema)", "engle_granger": eg[0], "engle_granger_p": eg[1], "engle_granger_p_52": eg52[1],
                  "johansen_rezagos": k, "johansen_traza": traza, "johansen_vc5": vc, "johansen_rango": rango,
                  "granger_tasa_a_fpf_p": np.nan, "granger_fpf_a_tasa_p": np.nan})
    t = pd.DataFrame(filas)
    eg_si, jo_si = t.engle_granger_p < ALFA, t.johansen_traza > t.johansen_vc5
    t["conclusion"] = np.select([eg_si & jo_si, eg_si | jo_si], ["Cointegración", "Evidencia mixta"], "Sin cointegración")
    # Sensibilidad: con la TAMN (que contiene a las demás tasas) aparece una relación, ¿incluye al FPF o es entre tasas?
    con, sin = _johansen(s[cols + ["tamn"]].to_numpy()), _johansen(s[list(TASAS) + ["tamn"]].to_numpy())
    extra = {"rango_con_tamn_y_fpf": con[3], "rango_con_tamn_sin_fpf": sin[3],
             "granger_min_p": float(t[["granger_tasa_a_fpf_p", "granger_fpf_a_tasa_p"]].min().min())}
    return t, extra


# ============================================================================
# 3. Corto plazo: modelo dinámico en diferencias con errores HAC
# ============================================================================
def rezagos_hac(n: int) -> int:
    return int(np.floor(4 * (n / 100) ** (2 / 9)))


def corto_plazo(s: pd.DataFrame, reforma: str) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Δfpf_t = α + φ Δfpf_(t−1) + Σ β_k ΔTEA_k,t + λ inflación_t + δ reforma_t + impulsos + ε_t."""
    d = pd.DataFrame({"d_fpf": s.fpf.diff(), "d_fpf_1": s.fpf.diff().shift(1), **{"d_" + c: s[c].diff() for c in TASAS},
                      "inflacion": s.inflacion, "reforma": (s.index >= reforma).astype(float)})
    for p in IMPULSOS:
        d["i_" + p] = (d.index == p).astype(float)
    base = ["d_fpf_1", *["d_" + c for c in TASAS], "inflacion", "reforma"]
    impulsos = ["i_" + p for p in IMPULSOS]
    muestras = {1: (d.dropna(), base), 2: (d.dropna(), base + impulsos), 3: (d[s.activo & s.activo.shift(1, fill_value=False)].dropna(), base + impulsos)}
    nombres = {"const": "Constante", "d_fpf_1": "Δ FPF del mes anterior", **{"d_" + c: "Δ TEA " + v for c, v in TASAS.items()},
               "inflacion": "Inflación mensual (%)", "reforma": "Reforma (dic-2025 en adelante)", **{"i_" + p: f"Impulso {p}" for p in IMPULSOS}}
    coefs, diag = [], []
    for k, (x, cols) in muestras.items():
        X = sm.add_constant(x[cols])
        mco = sm.OLS(x.d_fpf, X).fit()
        hac = sm.OLS(x.d_fpf, X).fit(cov_type="HAC", cov_kwds={"maxlags": rezagos_hac(len(x)), "use_correction": True}, use_t=True)
        for v in X.columns:
            coefs.append({"modelo": k, "variable": v, "nombre": nombres[v], "coef": hac.params[v], "ee": hac.bse[v], "p": hac.pvalues[v], "p_mco": mco.pvalues[v]})
        w = hac.wald_test(", ".join(f"d_{c} = 0" for c in TASAS), use_f=True, scalar=True)
        bg, bp = acorr_breusch_godfrey(mco, 4, result_object=False), het_breuschpagan(mco.resid, X.to_numpy())
        jb, cu = jarque_bera(mco.resid), breaks_cusumolsresid(mco.resid, X.shape[1])
        diag.append({"modelo": k, "n": int(hac.nobs), "r2": mco.rsquared, "r2_ajustado": mco.rsquared_adj, "durbin_watson": durbin_watson(mco.resid),
                     "wald_tasas_p": float(w.pvalue), "breusch_godfrey_p": float(bg[1]), "breusch_pagan_p": float(bp[1]), "jarque_bera_p": float(jb[1]),
                     "reset_p": float(linear_reset(mco, 2, use_f=True).pvalue), "cusum_p": float(cu[1]), "rezagos_hac": rezagos_hac(len(x))})
    return pd.DataFrame(coefs), pd.DataFrame(diag)


# ============================================================================
# 4. Reforma: regresión segmentada (H1)
# ============================================================================
def _segmentos(indice: pd.Index, inicio: str, corte: str) -> pd.DataFrame:
    t, ti, tc = np.arange(len(indice)), list(indice).index(inicio), list(indice).index(corte)
    return sm.add_constant(pd.DataFrame({"tendencia": np.maximum(0, t - ti + 1), "nivel": (t >= tc) * 1.0,
                                         "pendiente": np.where(t >= tc, t - tc, 0)}, index=indice).astype(float))


def reforma_segmentada(s: pd.DataFrame, reforma: str, placebos: tuple[str, ...]) -> tuple[pd.DataFrame, pd.DataFrame, dict, pd.DataFrame]:
    inicio = s.index[s.activo][0]
    X = _segmentos(s.index, inicio, reforma)
    hac = lambda y, X: sm.OLS(y, X).fit(cov_type="HAC", cov_kwds={"maxlags": rezagos_hac(len(X)), "use_correction": True}, use_t=True)
    modelos = {1: ("asinh, HAC", hac(s.fpf, X)), 2: ("asinh, MCG AR(1)", sm.GLSAR(s.fpf, X, rho=1).iterative_fit(50)),
               3: ("S/ millones reales, HAC", hac(s.monto_real, X))}
    nombres = {"const": "Constante", "tendencia": "Tendencia mensual desde el inicio", "nivel": "Cambio de nivel tras la reforma",
               "pendiente": "Cambio de pendiente tras la reforma"}
    coefs, diag = [], []
    for k, (titulo, r) in modelos.items():
        for v in X.columns:
            coefs.append({"modelo": k, "titulo": titulo, "variable": v, "nombre": nombres[v], "coef": r.params[v], "ee": r.bse[v], "p": r.pvalues[v]})
        w = r.wald_test("nivel = 0, pendiente = 0", use_f=True, scalar=True)
        diag.append({"modelo": k, "titulo": titulo, "n": len(s), "r2": r.rsquared, "wald_reforma_p": float(w.pvalue), "durbin_watson": durbin_watson(r.resid)})
    previos = s[s.index < reforma]
    p_placebo = [float(hac(previos.fpf, _segmentos(previos.index, inicio, c)).wald_test("nivel = 0, pendiente = 0", use_f=True, scalar=True).pvalue) for c in placebos]
    sin = X.assign(nivel=0.0, pendiente=0.0)
    ajuste = pd.DataFrame({"monto_real": s.monto_real, "ajuste_asinh": np.sinh(modelos[1][1].predict(X)), "sin_reforma_asinh": np.sinh(modelos[1][1].predict(sin)),
                           "ajuste_lineal": modelos[3][1].predict(X), "sin_reforma_lineal": modelos[3][1].predict(sin)})
    extra = {"placebos": list(placebos), "placebo_p": p_placebo, "placebos_significativos": int(sum(p < ALFA for p in p_placebo)),
             "rho_ar1": float(np.ravel(modelos[2][1].model.rho)[0])}
    return pd.DataFrame(coefs), pd.DataFrame(diag), extra, ajuste


# ============================================================================
# 5. Colocación: logit sobre proyectos publicados (H2)
# ============================================================================
def proyectos_publicados(d: pd.DataFrame, lider: str) -> pd.DataFrame:
    """Un registro por proyecto publicado. El portal da totales por plataforma, tipo de receptor y mes; se agregan por
    año porque un proyecto puede financiarse en un mes posterior (S3). Con datos agrupados, la verosimilitud del logit
    es la misma que con un registro por proyecto. Los de valores no tienen tipo de receptor y no entran."""
    con = d[d.estado_simv == "con_registros"]
    filas = []
    for (pl, anio), g in con.groupby(["plataforma", "anio"]):
        for t in ("emp", "per"):
            pub, fin = int(g[f"proy_publicados_{t}"].sum()), int(g[f"proy_financiados_{t}"].sum())
            if fin > pub:
                raise ValueError(f"más financiados que publicados en {pl} {anio} {t}")
            filas += [{"financiado": int(i < fin), "empresarial": int(t == "emp"), "lider": int(pl == lider), "anio": int(anio) - 2022} for i in range(pub)]
    return pd.DataFrame(filas)


def logit_colocacion(x: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    nombres = {"const": "Constante", "empresarial": "Proyecto empresarial", "lider": "Plataforma líder", "anio": "Año (desde 2022)"}
    coefs, diag = [], []
    for k, cols in {1: ["empresarial"], 2: ["empresarial", "lider"], 3: ["empresarial", "lider", "anio"]}.items():
        r = sm.Logit(x.financiado, sm.add_constant(x[cols].astype(float))).fit(disp=0)
        ic = np.exp(r.conf_int())
        for v in r.params.index:
            coefs.append({"modelo": k, "variable": v, "nombre": nombres[v], "coef": r.params[v], "ee": r.bse[v], "p": r.pvalues[v],
                          "razon": np.exp(r.params[v]), "razon_inf": ic.loc[v, 0], "razon_sup": ic.loc[v, 1]})
        me = r.get_margeff(at="overall").summary_frame().loc["empresarial"]
        p = r.predict()
        rangos = pd.Series(p).rank().to_numpy()
        n1, n0 = int(x.financiado.sum()), int((1 - x.financiado).sum())
        auc = (rangos[x.financiado.to_numpy() == 1].sum() - n1 * (n1 + 1) / 2) / (n1 * n0)
        diag.append({"modelo": k, "n": int(r.nobs), "pseudo_r2": r.prsquared, "lr_p": r.llr_pvalue, "auc": auc,
                     "efecto_marginal_pp": 100 * me.iloc[0], "efecto_inf_pp": 100 * me.iloc[4], "efecto_sup_pp": 100 * me.iloc[5]})
    return pd.DataFrame(coefs), pd.DataFrame(diag)


# ============================================================================
# 6. Rentabilidad: plataformas frente a empresas supervisadas (OE2)
# ============================================================================
def rentabilidad_empresas(e: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Razón_it = α + β FPF_i + γ ln(activo_it) + efectos de trimestre + ε_it; errores agrupados por empresa. Las razones no
    dependen de la moneda; se acotan a los percentiles 1 y 99 de cada muestra."""
    e = e[e.activo_total_miles > 0].copy()
    e["roa"] = 100 * e.utilidad_neta_miles / e.activo_total_miles
    e["capital"] = 100 * e.patrimonio_total_miles / e.activo_total_miles
    e["ln_activo"] = np.log(e.activo_total_miles)
    comparables = e[e.tipo_empresa.isin(COMPARABLES) | e.es_fpf.eq(1)]
    casos = {1: ("ROA trimestral, intermediarios", comparables, "roa"), 2: ("ROA trimestral, todas", e, "roa"),
             3: ("Patrimonio/activo, intermediarios", comparables, "capital")}
    coefs, diag = [], []
    for k, (titulo, x, var) in casos.items():
        y = x[var].clip(*x[var].quantile([0.01, 0.99]))
        T = pd.get_dummies(x.trimestre, drop_first=True, dtype=float)
        X = sm.add_constant(pd.concat([x[["es_fpf", "ln_activo"]].astype(float), T], axis=1))
        r = sm.OLS(y, X).fit(cov_type="cluster", cov_kwds={"groups": x.rpj.astype("category").cat.codes.to_numpy()}, use_t=True)
        for v, nombre in (("es_fpf", "Plataforma de FPF"), ("ln_activo", "Tamaño (logaritmo del activo)")):
            coefs.append({"modelo": k, "titulo": titulo, "variable": v, "nombre": nombre, "coef": r.params[v], "ee": r.bse[v], "p": r.pvalues[v]})
        diag.append({"modelo": k, "titulo": titulo, "n": int(r.nobs), "empresas": int(x.rpj.nunique()), "empresas_fpf": int(x[x.es_fpf == 1].rpj.nunique()),
                     "n_fpf": int(x.es_fpf.sum()), "r2": r.rsquared, "mediana_fpf": float(x.loc[x.es_fpf == 1, var].median()),
                     "mediana_resto": float(x.loc[x.es_fpf == 0, var].median())})
    return pd.DataFrame(coefs), pd.DataFrame(diag)
