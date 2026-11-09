# Diego Sebastián Aliaga Damián
# 2024200481M
# Tema 96: Fintech y financiamiento participativo (crowdfunding) en el Perú: oferta y condiciones
# Fecha de extracción: 2026-11-07 (censo) y 2026-11-08 (reanudación)
"""Pruebas de 03_limpieza_datos.py y de la base procesada entregada (esquema, reproducibilidad, integridad)."""
import re

import pandas as pd

import auditoria
from comun import sha256_archivo


def test_03_reproduce_byte_a_byte_la_base_entregada(tmp_path):
    regenerado = auditoria.reejecutar_03(tmp_path)
    assert regenerado.read_bytes() == auditoria.CSV_PROCESADO.read_bytes()
    assert (tmp_path / "diccionario_variables.md").read_bytes() == (auditoria.RAIZ / "diccionario_variables.md").read_bytes()


def test_esquema_pandera_de_la_base():
    auditoria.esquema().validate(auditoria.leer_procesado(), lazy=True)


def test_panel_balanceado_y_ventana():
    panel = auditoria.leer_procesado()
    assert panel.shape == (414, 35)
    assert panel.groupby("ruc").periodo.nunique().eq(69).all()
    assert (panel.periodo.min(), panel.periodo.max()) == ("2021-01", "2026-09")


def test_sin_imputacion_en_meses_sin_datos_del_simv():
    panel = auditoria.leer_procesado()
    sin_datos = panel[panel.estado_simv != "con_registros"]
    assert sin_datos.filter(regex=r"^(proy_|monto_)").isna().all().all()


def test_hash_declarado_en_el_readme_coincide():
    texto = auditoria.README.read_text(encoding="utf-8")
    declarado = re.search(r"SHA-256 del archivo procesado\*\*\s*\|\s*\*\*`([0-9a-f]{64})`", texto).group(1)
    assert declarado == sha256_archivo(auditoria.CSV_PROCESADO)


def test_equivalencia_detecta_diferencias():
    a = pd.DataFrame({"x": [1.0, 2.0, 3.0, 4.0], "y": ["a", "b", "c", "d"]})
    b = a.copy()
    assert auditoria.equivalencia(a, b)["pct_celdas_iguales"] == 100.0
    b.loc[0, "x"] = 9.0
    assert auditoria.equivalencia(a, b)["pct_celdas_iguales"] == 87.5


def test_encabezado_de_4_lineas_en_todo_el_codigo():
    patrones = [r"^# Diego Sebastián Aliaga Damián$", r"^# 2024200481M$", r"^# Tema 96: .+", r"^# Fecha de extracción: \d{4}-\d{2}-\d{2}"]
    for archivo in list((auditoria.RAIZ / "codigo").glob("*.py")) + list((auditoria.RAIZ / "pruebas").glob("*.py")):
        lineas = archivo.read_text(encoding="utf-8").splitlines()[:4]
        assert all(re.match(p, l) for p, l in zip(patrones, lineas)), archivo.name


def test_fechas_congeladas_identicas_en_01_02_03():
    valores = set()
    for nombre in ("01_extraccion_api.py", "02_scraping_web.py", "03_limpieza_datos.py"):
        texto = (auditoria.CODIGO / nombre).read_text(encoding="utf-8")
        valores.add((re.search(r'^FECHA_INICIO = "(.+)"', texto, re.M).group(1),
                     re.search(r'^FECHA_CORTE = "(.+)"', texto, re.M).group(1)))
    assert valores == {("2021-01", "2026-09")}
