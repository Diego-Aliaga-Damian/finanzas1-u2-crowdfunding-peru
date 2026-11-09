# Diego Sebastián Aliaga Damián
# 2024200481M
# Tema 96: Fintech y financiamiento participativo (crowdfunding) en el Perú: oferta y condiciones
# Fecha de extracción: 2026-11-07 (censo) y 2026-11-08 (reanudación)
"""Pruebas de 01_extraccion_api.py con respuestas simuladas (sin conexión a internet)."""
import json

from conftest import RespuestaSimulada


def test_periodo_bcrp_formato_api(s01):
    assert s01.periodo_bcrp("2021-01") == "2021-1"
    assert s01.periodo_bcrp("2026-09") == "2026-9"


def test_trimestres_de_la_ventana(s01):
    pares = s01.trimestres_consulta()
    assert len(pares) == 23 and pares[0] == (2021, 1) and pares[-1] == (2026, 3)


def test_validar_bcrp_acepta_respuesta_real(s01, fixture_bytes):
    assert s01.validar_bcrp(json.loads(fixture_bytes("bcrp_respuesta.json"))) == []


def test_validar_bcrp_detecta_serie_equivocada(s01, fixture_bytes):
    datos = json.loads(fixture_bytes("bcrp_respuesta.json"))
    datos["config"]["series"][1]["name"] = "Serie cualquiera"
    problemas = s01.validar_bcrp(datos)
    assert any("PN07843NM" in p for p in problemas)


def test_validar_bcrp_detecta_valores_incompletos(s01, fixture_bytes):
    datos = json.loads(fixture_bytes("bcrp_respuesta.json"))
    datos["periods"][0]["values"] = datos["periods"][0]["values"][:3]
    assert any("número de valores" in p for p in s01.validar_bcrp(datos))


def test_extraer_bcrp_guarda_el_crudo_sin_modificarlo(s01, fixture_bytes, log, tmp_path, monkeypatch):
    contenido = fixture_bytes("bcrp_respuesta.json")
    monkeypatch.setattr(s01, "solicitar", lambda *a, **k: RespuestaSimulada(contenido))
    monkeypatch.setattr(s01, "CRUDO_BCRP", tmp_path / "bcrp.json")
    assert s01.extraer_bcrp(None, log) is True
    assert (tmp_path / "bcrp.json").read_bytes() == contenido


def test_extraer_bcrp_no_sobrescribe_con_pagina_antibot(s01, log, tmp_path, monkeypatch):
    crudo = tmp_path / "bcrp.json"
    crudo.write_bytes(b"CRUDO VALIDO ANTERIOR")
    pagina = b"<html><title>Pardon Our Interruption</title></html>"
    monkeypatch.setattr(s01, "solicitar", lambda *a, **k: RespuestaSimulada(pagina))
    monkeypatch.setattr(s01, "CRUDO_BCRP", crudo)
    assert s01.extraer_bcrp(None, log) is False
    assert crudo.read_bytes() == b"CRUDO VALIDO ANTERIOR"


def test_extraer_bcrp_error_http_conserva_el_crudo(s01, log, tmp_path, monkeypatch):
    crudo = tmp_path / "bcrp.json"
    crudo.write_bytes(b"CRUDO VALIDO ANTERIOR")
    monkeypatch.setattr(s01, "solicitar", lambda *a, **k: RespuestaSimulada(b"error", status_code=503))
    monkeypatch.setattr(s01, "CRUDO_BCRP", crudo)
    assert s01.extraer_bcrp(None, log) is False
    assert crudo.read_bytes() == b"CRUDO VALIDO ANTERIOR"


def test_validar_smv(s01, fixture_bytes):
    datos = json.loads(fixture_bytes("smv_odata_respuesta.json"))
    assert s01.validar_smv(datos) == []
    assert s01.validar_smv({"ResponseCode": "ERROR", "data": []})
    sin_columna = {"ResponseCode": "OK", "data": [{k: v for k, v in datos["data"][0].items() if k != "RUC"}]}
    assert any("RUC" in p for p in s01.validar_smv(sin_columna))


def test_respuesta_vacia_de_la_smv_no_reemplaza_un_crudo_con_datos(s01, log, tmp_path, monkeypatch):
    monkeypatch.setattr(s01, "DIR_SMV", tmp_path)
    monkeypatch.setattr(s01, "trimestres_consulta", lambda: [(2025, 4)])
    crudo = tmp_path / "principalcuenta_2025_T4.json"
    crudo.write_bytes(b'{"ResponseCode":"OK","data":[{"RUC":"1"}]}')
    vacia = json.dumps({"ResponseCode": "OK", "Message": "ConsultaGenerada", "data": []}).encode()
    monkeypatch.setattr(s01, "solicitar", lambda *a, **k: RespuestaSimulada(vacia))
    s01.extraer_smv(None, log)
    assert crudo.read_bytes() == b'{"ResponseCode":"OK","data":[{"RUC":"1"}]}'
