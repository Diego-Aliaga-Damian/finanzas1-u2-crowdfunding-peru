# Diego Sebastián Aliaga Damián
# 2024200481M
# Tema 96: Fintech y financiamiento participativo (crowdfunding) en el Perú: oferta y condiciones
# Fecha de extracción: 2026-11-07 (censo) y 2026-11-08 (reanudación)
"""Pruebas del dashboard (dashboard/datos.py): sin filtros, sus cálculos reproducen las salidas del artículo,
los filtros se comportan como se espera y la matemática del simulador es correcta. No requieren Streamlit."""
import importlib.util
import json

import numpy as np
import pandas as pd
import pytest

from conftest import RAIZ

SALIDAS = RAIZ / "salidas"


@pytest.fixture(scope="module")
def D():
    spec = importlib.util.spec_from_file_location("dashboard_datos", RAIZ / "dashboard" / "datos.py")
    modulo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modulo)
    return modulo


@pytest.fixture(scope="module")
def base(D):
    return D.leer_base()


@pytest.fixture(scope="module")
def r():
    return json.loads((SALIDAS / "resultados_04.json").read_text(encoding="utf-8"))


def test_dashboard_no_modifica_la_base(D, r):
    assert D.sha256_base() == r["sha256_base_procesada"]


def test_resumen_anual_sin_filtros_coincide_con_t2(D, base):
    a = D.por_anio(D.filtrar(base, "2022-01")).set_index("anio")
    t2 = pd.read_csv(SALIDAS / "tablas" / "t2_oferta_anual.csv").set_index("anio")
    pares = {"monto": "monto_soles", "publicados": "proyectos_publicados", "financiados": "proyectos_financiados",
             "colocacion_pct": "tasa_colocacion_pct", "monto_medio": "monto_promedio_proyecto_soles",
             "empresarial_pct": "participacion_empresarial_pct", "hhi": "hhi",
             "participacion_lider_pct": "participacion_lider_pct", "plataformas_activas": "plataformas_activas"}
    for propio, articulo in pares.items():
        assert np.allclose(a[propio].astype(float), t2[articulo].astype(float)), propio


def test_resumen_total_coincide_con_el_lider_del_articulo(D, base, r):
    k = D.resumen(base)
    assert k["lider"] == r["plataforma_lider"]
    assert round(k["participacion_lider_pct"], 2) == pytest.approx(r["participacion_lider_periodo_pct"])
    assert k["plataformas_activas"] == r["plataformas_con_financiamiento"]


def test_colocacion_por_tipo_coincide_con_t4(D, base, r):
    t4 = pd.read_csv(SALIDAS / "tablas" / "t4_condiciones_por_receptor.csv")
    ini = r["inicio_actividad_fpf"]
    ventanas = {"Todo el periodo": (ini, None), "Antes de la reforma": (ini, D.desplazar(D.REFORMA, -1)),
                "Después de la reforma": (D.REFORMA, None)}
    for nombre, (desde, hasta) in ventanas.items():
        c = D.colocacion_por_tipo(D.filtrar(base, desde, hasta))
        ref = t4[t4.periodo == nombre].reset_index(drop=True)
        assert np.allclose(c.publicados, ref.proyectos_publicados), nombre
        assert np.allclose(c.financiados, ref.proyectos_financiados), nombre
        assert np.allclose(c.colocacion_pct, ref.tasa_colocacion_pct, equal_nan=True), nombre


def test_series_mensuales_coinciden_con_f1_y_f2(D, base, r):
    ini = r["inicio_actividad_fpf"]
    f1 = pd.read_csv(SALIDAS / "figuras" / "f1_monto_mensual_por_plataforma_datos.csv").set_index("periodo")
    m = D.mensual_por_plataforma(base, ini) / 1e6
    assert m.index.equals(f1.index)
    assert all(np.allclose(m[c], f1[c]) for c in f1.columns)
    f2 = pd.read_csv(SALIDAS / "figuras" / "f2_publicados_financiados_colocacion_datos.csv").set_index("periodo")
    s = D.mensual_sistema(base, ini)
    assert s.index.equals(f2.index)
    assert all(np.allclose(s[c], f2[c], equal_nan=True) for c in f2.columns)


def test_monto_real_anual_coincide_con_t2(D, base):
    t2 = pd.read_csv(SALIDAS / "tablas" / "t2_oferta_anual.csv").set_index("anio")
    real = D.mensual_por_plataforma(D.filtrar(base, "2022-01"), real=True).sum(axis=1)
    por_anio = real.groupby(real.index.str[:4].astype(int)).sum()
    assert np.allclose(por_anio, t2.monto_real_soles_dic2021)


def test_filtros_de_periodo_y_plataforma(D, base):
    v = D.filtrar(base, "2025-01", "2025-12", ["Afluenta"])
    assert set(v.plataforma) == {"Afluenta"} and v.periodo.min() == "2025-01" and v.periodo.max() == "2025-12"
    # Las partes suman el total: filtrar por plataforma no pierde ni duplica montos
    total = D.resumen(D.filtrar(base, "2025-01", "2025-12"))["monto"]
    partes = sum(D.resumen(D.filtrar(base, "2025-01", "2025-12", [p]))["monto"] for p in D.PLATAFORMAS)
    assert partes == pytest.approx(total)
    # Una sola plataforma con monto concentra todo: IHH 10 000
    lider = D.resumen(D.filtrar(base, "2024-01", "2024-12", ["Inversiones.io"]))
    assert lider["hhi"] == pytest.approx(10_000)


def test_ventanas_de_comparacion(D, base):
    ps = D.periodos(base)
    assert D.periodo_comparacion("2025-01", "2025-12", "interanual", ps) == ("2024-01", "2024-12")
    assert D.periodo_comparacion("2026-01", "2026-09", "interanual", ps) == ("2025-01", "2025-09")
    assert D.periodo_comparacion("2025-01", "2025-12", "anterior", ps) == ("2024-01", "2024-12")
    assert D.periodo_comparacion("2022-01", "2026-09", "interanual", ps) is None  # se solaparían
    assert D.periodo_comparacion("2021-01", "2021-12", "anterior", ps) is None    # fuera de los datos


def test_variacion_interanual_2026_coincide_con_t2(D, base):
    t2 = pd.read_csv(SALIDAS / "tablas" / "t2_oferta_anual.csv").set_index("anio")
    a = D.resumen(D.filtrar(base, "2026-01", "2026-09"))["monto"]
    b = D.resumen(D.filtrar(base, "2025-01", "2025-09"))["monto"]
    assert D.variacion(a, b) == pytest.approx(t2.loc[2026, "var_interanual_monto_pct"])


def test_matematica_del_simulador(D):
    assert D.cuota_francesa(1000, 0.01, 12) == pytest.approx(88.8488, abs=1e-4)
    assert D.tem_desde_tea(12.6825) == pytest.approx(0.01, abs=1e-6)
    assert D.tcea(50_000, 30.0, 12, 0.0) == pytest.approx(30.0, abs=1e-6)       # sin comisión, TCEA = TEA
    assert D.tcea(50_000, 30.0, 12, 2.0) > 30.0                                    # la comisión encarece
    eq = D.tea_equilibrio(50_000, 12, 2.0, 30.0)
    assert D.tcea(50_000, eq, 12, 2.0) == pytest.approx(30.0, abs=1e-6)
    assert np.isnan(D.tea_equilibrio(50_000, 3, 15.0, 10.0))                      # la comisión sola ya supera el objetivo
    c = D.cronograma(10_000, 25.0, 18)
    assert c.amortizacion.sum() == pytest.approx(10_000) and c.saldo.iloc[-1] == pytest.approx(0, abs=1e-6)
