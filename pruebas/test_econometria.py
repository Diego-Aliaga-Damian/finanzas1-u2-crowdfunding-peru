# Diego Sebastián Aliaga Damián
# 2024200481M
# Tema 96: Fintech y financiamiento participativo (crowdfunding) en el Perú: oferta y condiciones
# Fecha de extracción: 2026-11-07 (censo) y 2026-11-08 (reanudación)
"""Pruebas de codigo/econometria.py: tamaño de muestra por variable, cálculos comprobados por otra vía y coherencia entre
las tablas T9-T15 y resultados_04.json."""
import json

import numpy as np
import pandas as pd
import pytest
from scipy.linalg import eigh

import auditoria
import econometria as EC

TABLAS = auditoria.SALIDAS / "tablas"


@pytest.fixture(scope="module")
def s04():
    return auditoria.cargar_script("04_analisis.py")


@pytest.fixture(scope="module")
def datos(s04):
    d = s04.leer_base()
    m = s04.serie_mensual(d)
    return d, m, EC.series_mensuales(m)


@pytest.fixture(scope="module")
def ec():
    return json.loads((auditoria.SALIDAS / "resultados_04.json").read_text(encoding="utf-8"))["econometria"]


def test_cada_variable_de_los_modelos_cumple_el_minimo():
    """Criterio del curso: 1 000 observaciones o 60 periodos por cada variable (no por base)."""
    t = pd.read_csv(TABLAS / "t9_verificacion_muestra.csv")
    modelos, solo_fpf = t[~t.bloque.str.contains("solo de las plataformas")], t[t.bloque.str.contains("solo de las plataformas")]
    assert modelos.cumple.all() and not solo_fpf.cumple.any()         # las plataformas solas no alcanzan: solo describen
    assert (t.datos_totales == t.variables * t.datos_por_variable).all()
    assert set(modelos.loc[modelos.criterio == "periodos", "datos_por_variable"]) == {69}
    assert (modelos.loc[modelos.criterio == "observaciones", "datos_por_variable"] >= 1000).all()


def test_series_mensuales_completas(datos):
    s = datos[2]
    assert len(s) == 69 and s[["fpf", *EC.TASAS, "tamn", "ln_ipc"]].notna().all().all()
    assert int(s.activo.sum()) == 52 and (s.loc[~s.activo, "monto_real"] == 0).all()


def test_base_de_empresas_es_el_crudo_sin_editar():
    e = pd.read_csv(auditoria.CSV_EMPRESAS, dtype={"rpj": str, "ruc": str})
    crudo = pd.read_csv(auditoria.CRUDOS / f"datos_crudos_{auditoria.CODIGO_MATRICULA}_smv_odata.csv")
    assert len(e) == len(crudo) == 6001 and not e.duplicated(["rpj", "trimestre"]).any()
    assert e.utilidad_neta_miles.sum() == pytest.approx(crudo.UtilidadNeta.sum())
    assert e.activo_total_miles.sum() == pytest.approx(crudo.ActivoTotal.sum())


def test_raiz_unitaria_distingue_casos_conocidos():
    rng = np.random.default_rng(481)
    ruido, paseo = rng.normal(size=300), rng.normal(size=300).cumsum()
    from statsmodels.tsa.stattools import adfuller
    assert adfuller(ruido, autolag="AIC", result_object=False)[1] < 0.05 < adfuller(paseo, autolag="AIC", result_object=False)[1]
    assert EC._kpss(pd.Series(ruido))[1] >= 0.05 > EC._kpss(pd.Series(paseo))[1]


def test_traza_de_johansen_con_un_calculo_independiente(datos):
    """Misma traza con autovalores generalizados de matrices simétricas (sin la parte compleja de statsmodels)."""
    s = datos[2]

    def traza(x, k):
        dx = np.diff(x, axis=0)
        T = len(dx)
        z0, z1 = dx[k:], x[:-1][k:]
        z2 = np.column_stack([dx[k - j - 1:T - j - 1] for j in range(k)] + [np.ones(T - k)])
        residuo = lambda y: y - z2 @ np.linalg.lstsq(z2, y, rcond=None)[0]
        r0, r1 = residuo(z0), residuo(z1)
        n = len(r0)
        s00, s11, s01 = r0.T @ r0 / n, r1.T @ r1 / n, r0.T @ r1 / n
        lam = eigh(s01.T @ np.linalg.solve(s00, s01), s11, eigvals_only=True)
        return -n * np.log(1 - lam).sum()

    t = pd.read_csv(TABLAS / "t11_cointegracion.csv")
    for cols, fila in zip([["fpf", c] for c in EC.TASAS] + [["fpf", *EC.TASAS]], t.itertuples()):
        assert traza(s[cols].to_numpy(), fila.johansen_rezagos) == pytest.approx(fila.johansen_traza, rel=1e-6)


def test_logit_simple_es_la_razon_de_productos_cruzados(ec):
    """Con una sola variable binaria, la razón de momios del logit es la de la tabla 2 × 2."""
    t4 = pd.read_csv(TABLAS / "t4_condiciones_por_receptor.csv")
    g = t4[t4.periodo == "Todo el periodo"].set_index("tipo_receptor")
    a, b = g.loc["Empresarial", ["proyectos_financiados", "proyectos_publicados"]]
    c, d = g.loc["Personal", ["proyectos_financiados", "proyectos_publicados"]]
    assert ec["logit"]["1"]["coef"]["empresarial"]["razon"] == pytest.approx((a / (b - a)) / (c / (d - c)), rel=1e-4)
    assert ec["logit"]["1"]["n"] == int(b + d) >= 1000


def test_regresion_segmentada_recupera_un_salto_conocido():
    indice = pd.Index([f"{a}-{k:02d}" for a in range(2021, 2027) for k in range(1, 13)][:69])
    rng = np.random.default_rng(481)
    X = EC._segmentos(indice, "2022-06", "2025-12")
    s = pd.DataFrame({"monto_real": (X @ [1.0, 0.2, 3.0, -0.1] + rng.normal(0, 0.05, 69)).to_numpy()}, index=indice)
    s["fpf"], s["activo"] = s.monto_real, indice >= "2022-06"
    c = EC.reforma_segmentada(s, "2025-12", ("2024-06",))[0]
    c = c[c.modelo == 3].set_index("variable").coef
    assert c["nivel"] == pytest.approx(3.0, abs=0.15) and c["pendiente"] == pytest.approx(-0.1, abs=0.03)


def test_corto_plazo_observaciones_y_rezagos(datos, ec):
    assert [int(ec["corto_plazo"][k]["n"]) for k in "123"] == [67, 67, 51]
    assert EC.rezagos_hac(67) == 3
    # Los impulsos absorben su mes: el residuo es cero y la tasa de ese mes no mueve el coeficiente
    coefs, _ = EC.corto_plazo(datos[2], "2025-12")
    assert set(coefs[coefs.modelo == 2].variable) >= {"i_2024-01", "i_2024-02", "i_2025-03"}


def test_regla_de_escala_solo_toca_a_las_plataformas():
    e = pd.DataFrame({"rpj": ["A", "A", "B", "C"], "es_fpf": [1, 1, 1, 0], "tipo_empresa": "x", "trimestre": "2024-T1",
                      **{c: [900_000.0, 900.0, 400_000.0, 900_000.0] for c in EC.CUENTAS}})
    r = EC.ajustar_escala_fpf(e, 50_000)
    assert list(r.rpj) == ["A", "A", "C"] and r.activo_total_miles.tolist() == [900.0, 900.0, 900_000.0]


def test_cifras_del_json_coinciden_con_las_tablas(ec):
    t10 = pd.read_csv(TABLAS / "t10_raiz_unitaria.csv").set_index("variable")
    assert ec["raiz_unitaria"]["fpf"]["adf_nivel_p"] == pytest.approx(t10.loc["fpf", "adf_nivel_p"], rel=1e-4)
    t15 = pd.read_csv(TABLAS / "t15_rentabilidad_empresas.csv")
    f = t15[(t15.modelo == 1) & (t15.variable == "es_fpf")].iloc[0]
    assert ec["empresas"]["1"]["coef"]["es_fpf"]["p"] == pytest.approx(f.p, rel=1e-4) and f.n >= 1000
    assert ec["sha256_base_empresas"] == auditoria.sha256_archivo(auditoria.CSV_EMPRESAS)
