# Diego Sebastián Aliaga Damián
# 2024200481M
# Tema 96: Fintech y financiamiento participativo (crowdfunding) en el Perú: oferta y condiciones
# Fecha de extracción: 2026-11-07 (censo) y 2026-11-08 (reanudación)
"""Pruebas de 04_analisis.py: regeneración idéntica de tablas y figuras y coherencia de las cifras clave."""
import json

import numpy as np
import pandas as pd
import pytest

import auditoria


@pytest.fixture(scope="module")
def s04():
    return auditoria.cargar_script("04_analisis.py")


def test_04_regenera_todas_las_salidas_identicas(tmp_path):
    nuevo = pd.read_csv(auditoria.reejecutar_04(tmp_path))
    entregado = pd.read_csv(auditoria.SALIDAS / "manifiesto_salidas.csv")
    cruce = entregado.merge(nuevo, on="archivo", how="outer", suffixes=("_e", "_n"))
    assert len(cruce) == len(entregado) == len(nuevo)
    assert (cruce.sha256_e == cruce.sha256_n).all(), cruce[cruce.sha256_e != cruce.sha256_n].archivo.tolist()


def test_cifras_clave_coinciden_con_las_tablas():
    r = json.loads((auditoria.SALIDAS / "resultados_04.json").read_text(encoding="utf-8"))
    t2 = pd.read_csv(auditoria.SALIDAS / "tablas" / "t2_oferta_anual.csv").set_index("anio")
    for anio, v in r["anual"].items():
        assert v["proyectos_financiados"] == int(t2.loc[int(anio), "proyectos_financiados"])
        assert v["monto_soles"] == int(t2.loc[int(anio), "monto_soles"])
    assert r["sha256_base_procesada"] == auditoria.sha256_archivo(auditoria.CSV_PROCESADO)


def test_totales_de_2024_y_2025_cercanos_a_la_smv():
    """Contraste externo: cifras de la SMV citadas en prensa (2024: 253 proyectos, S/ 54,5 M; 2025: 432, S/ 120,3 M)."""
    r = json.loads((auditoria.SALIDAS / "resultados_04.json").read_text(encoding="utf-8"))["anual"]
    assert abs(r["2025"]["proyectos_financiados"] - 432) <= 1 and abs(r["2025"]["monto_soles"] / 1e6 - 120.3) < 0.5
    assert abs(r["2024"]["proyectos_financiados"] - 253) <= 2 and abs(r["2024"]["monto_soles"] / 1e6 - 54.5) < 1.0


def test_intervalo_de_wilson(s04):
    inferior, superior = s04.wilson(50, 100)
    assert round(inferior, 1) == 40.4 and round(superior, 1) == 59.6


def test_indice_de_herfindahl(s04):
    assert s04.hhi(pd.Series([1.0])) == 10_000
    assert s04.hhi(pd.Series([0.5, 0.5])) == 5_000


def test_sin_lider_no_imputa_meses_no_obtenidos(s04):
    """S2: un mes sin registros en las demás plataformas vale cero solo si ninguna quedó no obtenida."""
    d = pd.DataFrame({"plataforma": ["L", "A", "B"] * 3,
                      "periodo": ["2024-01"] * 3 + ["2024-02"] * 3 + ["2024-03"] * 3,
                      "estado_simv": ["con_registros", "sin_registros", "sin_registros",
                                      "con_registros", "no_obtenido", "sin_registros",
                                      "con_registros", "con_registros", "no_obtenido"],
                      "monto_financiado_total": [10.0, 0.0, 0.0, 10.0, np.nan, 0.0, 10.0, 5.0, np.nan]})
    s = s04.serie_sin_lider(d, pd.Index(["2024-01", "2024-02", "2024-03"]), "L")
    assert s["2024-01"] == 0 and pd.isna(s["2024-02"]) and s["2024-03"] == 5


def test_escala_eeff_con_y_sin_referencia_interna(s04):
    """S5a: con trimestres propios bajo el umbral se divide entre 1 000; S5b: sin referencia, los saldos no se usan."""
    d = pd.DataFrame({"plataforma": ["A", "A", "B"], "trimestre_eeff": ["2022-T4", "2023-T1", "2023-T3"],
                      "activo_total_miles": [966_653.0, 1_098.0, 361_538.0], "pasivo_total_miles": [686_562.0, 533.0, 708.0],
                      "patrimonio_total_miles": [280_091.0, 565.0, 360_830.0], "ingresos_totales_miles": [113_930.0, 99.0, 0.0],
                      "utilidad_neta_miles": [-100_278.0, -112.0, 0.0]})
    a = s04.ajustar_escala_eeff(d)
    assert a.loc[0, "activo_total_miles"] == pytest.approx(966.653) and a.loc[0, "ingresos_totales_miles"] == pytest.approx(113.93)
    assert a.loc[1, "activo_total_miles"] == 1_098
    assert pd.isna(a.loc[2, "activo_total_miles"]) and a.loc[2, "ingresos_totales_miles"] == 0


def test_04_no_lee_datos_crudos():
    codigo = (auditoria.CODIGO / "04_analisis.py").read_text(encoding="utf-8")
    assert "CRUDOS" not in codigo and "datos_crudos" not in codigo.split('"""', 2)[-1]
