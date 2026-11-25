# Diego Sebastián Aliaga Damián
# 2024200481M
# Tema 96: Fintech y financiamiento participativo (crowdfunding) en el Perú: oferta y condiciones
# Fecha de extracción: 2026-11-07 (censo) y 2026-11-08 (reanudación)
"""Pruebas del Centro de mando (dashboard/terminal_datos.py): lo que se ve en la terminal 3D coincide con la base, con
las tablas del artículo y con el registro de ejecución, y nada hipotético se rotula como observado. No requieren Streamlit."""
import json
import sys

import numpy as np
import pandas as pd
import pytest

from conftest import RAIZ

DASHBOARD = RAIZ / "dashboard"
SALIDAS = RAIZ / "salidas"


@pytest.fixture(scope="module")
def modulos():
    sys.path.insert(0, str(DASHBOARD))
    try:
        import datos
        import terminal_datos
    finally:
        sys.path.remove(str(DASHBOARD))
    return datos, terminal_datos


@pytest.fixture(scope="module")
def base(modulos):
    return modulos[0].leer_base()


@pytest.fixture(scope="module")
def paquete(modulos, base):
    D, TD = modulos
    return TD.paquete(base, D.leer_resultados(), {p: "#000000" for p in D.PLATAFORMAS}, {s: "#000000" for s in D.SERIES_BCRP})


def test_el_paquete_es_json_valido_y_ligero(paquete):
    texto = json.dumps(paquete, allow_nan=False, ensure_ascii=False)
    assert len(texto) < 250_000
    assert len(paquete["meses"]) == 57 and paquete["meses"][0] == "2022-01" and paquete["meses"][-1] == "2026-09"


def test_monto_anual_del_replay_coincide_con_t2(paquete):
    t2 = pd.read_csv(SALIDAS / "tablas" / "t2_oferta_anual.csv").set_index("anio")
    m = pd.Series(paquete["mensual"]["monto"], index=paquete["meses"], dtype=float)
    anual = m.groupby([p[:4] for p in m.index]).sum()
    for anio in t2.index:
        assert anual[str(anio)] == pytest.approx(t2.loc[anio, "monto_soles"])
    por_plataforma = np.array([p["monto"] for p in paquete["plataformas"]], dtype=float).sum(axis=0)
    assert np.allclose(por_plataforma, m.fillna(0))


def test_la_ciudad_de_montos_no_inventa_meses(paquete, modulos):
    sup = next(s for s in paquete["superficies"] if s["id"] == "monto")
    m = dict(zip(paquete["meses"], paquete["mensual"]["monto"]))
    for j, (_, anio) in enumerate(sup["ejeY"]["marcas"]):
        for i in range(12):
            valor, periodo = sup["z"][j][i], f"{anio}-{i + 1:02d}"
            if periodo not in m or m[periodo] is None:
                assert valor is None, periodo
            else:
                assert valor == pytest.approx(m[periodo] / 1e6, abs=1e-4)
    assert sup["z"][-1][9:] == [None, None, None]          # octubre a diciembre de 2026 aún no existen


def test_las_cintas_son_las_tasas_de_la_base(paquete, modulos, base):
    sup = next(s for s in paquete["superficies"] if s["id"] == "tasas")
    t = modulos[0].tasas_bcrp(base)
    assert sorted(sup["series"]) == sorted(t.columns) and sup["meses"] == list(t.index)
    for fila, serie in zip(sup["z"], sup["series"]):
        assert np.allclose(fila, t[serie].round(2))
    assert paquete["desfase_tasas"] == list(t.index).index(paquete["meses"][0])
    assert "FPF" in sup["explica"] and sup["insignia"].startswith("Observado")


def test_la_superficie_de_costo_es_la_formula_del_simulador_y_se_rotula_como_calculo(paquete, modulos):
    D, _ = modulos
    sup = next(s for s in paquete["superficies"] if s["id"] == "costo")
    assert sup["insignia"] == "Cálculo" and "no un dato del FPF" in sup["explica"]
    for j in (0, 12, 29):
        for i in (0, 20, 40):
            tea, n = sup["ejeX"]["valores"][i], sup["ejeY"]["valores"][j]
            assert sup["z"][j][i] == pytest.approx(D.cronograma(100.0, tea, n).interes.sum(), abs=1e-2)
    z = np.array(sup["z"])
    assert (np.diff(z, axis=0) > 0).all() and (np.diff(z, axis=1) > 0).all()   # crece con el plazo y con la tasa
    assert z.max() <= sup["ejeZ"]["max"]


def test_flujos_suman_el_acumulado_de_doce_meses(paquete):
    acumulado = paquete["mensual"]["acumulado_12m"]
    for f, a in zip(paquete["flujos"], acumulado):
        if a is not None:
            assert sum(sum(v) for v in f.values()) == pytest.approx(a, abs=3)


def test_situacion_del_mes_es_descriptiva(paquete, modulos):
    situacion = paquete["mensual"]["situacion"]
    media, desv, monto = (paquete["mensual"][c] for c in ("media_previa", "desv_previa", "monto"))
    for s, m, d, x, p in zip(situacion, media, desv, monto, paquete["meses"]):
        if x is None or x == 0:
            assert s == "sin_actividad"
        elif m is None:
            assert s == "sin_ventana", p                   # sin 12 meses previos no se califica el mes
        elif s == "bajo":
            assert x < m - d
        elif s == "sobre":
            assert x > m + d
    assert situacion[-1] == "maximo"


def test_lider_movil_coincide_con_la_base(paquete, modulos, base):
    D, _ = modulos
    v = D.filtrar(base, "2025-10", "2026-09")
    assert paquete["mensual"]["lider_12m_pct"][-1] == pytest.approx(D.resumen(v)["participacion_lider_pct"], abs=1e-3)
    assert paquete["mensual"]["ihh_12m"][-1] == pytest.approx(D.resumen(v)["hhi"], abs=1e-2)


def test_hitos_salen_de_los_resultados(paquete, modulos):
    r = modulos[0].leer_resultados()
    meses = [h["mes"] for h in paquete["hitos"]]
    assert meses == sorted(meses) and set(meses) <= set(paquete["meses"])
    assert meses[0] == r["inicio_actividad_fpf"]
    salto = next(h for h in paquete["hitos"] if h["mes"] == "2025-03")
    assert f"{r['salto_tea_bcos_pyme_2025_03_pp']:.2f}" in salto["texto"] and "no del FPF" in salto["texto"]


def test_la_consola_repite_lineas_reales_del_log(paquete):
    archivo = (RAIZ / "log_ejecucion.txt").read_text(encoding="utf-8").splitlines()
    log = paquete["log"]
    assert log["total"] == len(archivo) and 0 < len(log["lineas"]) <= 150
    for l in log["lineas"]:
        original = archivo[l["n"] - 1]
        assert original.startswith(f"{l['hora']} | {l['script']} | {l['nivel']}")


def test_el_componente_no_carga_librerias_externas():
    carpeta = DASHBOARD / "terminal"
    assert {"index.html", "terminal.css", "util.js", "superficie.js", "paneles.js", "principal.js"} <= {p.name for p in carpeta.iterdir()}
    for p in carpeta.glob("*.js"):
        texto = p.read_text(encoding="utf-8")
        assert texto.splitlines()[0].endswith("Diego Sebastián Aliaga Damián")
        assert "http://" not in texto and "https://" not in texto, p.name
    assert "<script src=\"http" not in (carpeta / "index.html").read_text(encoding="utf-8")
