# Diego Sebastián Aliaga Damián
# 2024200481M
# Tema 96: Fintech y financiamiento participativo (crowdfunding) en el Perú: oferta y condiciones
# Fecha de extracción: 2026-11-07 (censo) y 2026-11-08 (reanudación)
"""Pruebas de 04_analisis.py: regeneración idéntica de tablas y figuras y coherencia de las cifras clave."""
import json

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


def test_04_no_lee_datos_crudos():
    codigo = (auditoria.CODIGO / "04_analisis.py").read_text(encoding="utf-8")
    assert "CRUDOS" not in codigo and "datos_crudos" not in codigo.split('"""', 2)[-1]
