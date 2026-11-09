# Diego Sebastián Aliaga Damián
# 2024200481M
# Tema 96: Fintech y financiamiento participativo (crowdfunding) en el Perú: oferta y condiciones
# Fecha de extracción: 2026-11-07 (censo) y 2026-11-08 (reanudación)
"""Pruebas de 02_scraping_web.py con páginas reales guardadas (sin conexión a internet)."""
from conftest import RespuestaSimulada


def test_meses_del_periodo(s02):
    meses = s02.meses_periodo()
    assert len(meses) == 69 and meses[0] == (2021, 1) and meses[-1] == (2026, 9)


def test_lista_de_plataformas_vigentes(s02, fixture_bytes):
    empresas = s02.opciones_empresas(s02.sopa(fixture_bytes("simv_lista_vigentes.html")))
    assert set(empresas) == {"177663", "186982", "190130"}
    assert "INVERSIONES.IO" in empresas["177663"]


def test_campos_ocultos_de_aspnet(s02, fixture_bytes):
    campos = s02.campos_ocultos(s02.sopa(fixture_bytes("simv_lista_vigentes.html")))
    assert "__VIEWSTATE" in campos and "__EVENTVALIDATION" in campos


def test_leer_grilla_con_registros(s02, fixture_bytes):
    filas = s02.leer_grilla(s02.sopa(fixture_bytes("simv_con_grilla_*.html")))
    empresarial = next(f for f in filas if f["tipo_receptor"] == "EMPRESARIAL")
    assert empresarial == {"modalidad": "PRESTAMOS", "tipo_receptor": "EMPRESARIAL", "proyectos_publicados": "44",
                           "proyectos_financiados": "43", "monto_total_financiado": "13658108"}
    assert any(f["modalidad"] == "TOTAL" for f in filas)


def test_validar_acepta_la_consulta_pedida(s02, fixture_bytes):
    assert s02.validar(s02.sopa(fixture_bytes("simv_con_grilla_*.html")), "177663", 2026, 9) == []


def test_validar_detecta_que_la_respuesta_es_de_otro_mes(s02, fixture_bytes):
    problemas = s02.validar(s02.sopa(fixture_bytes("simv_con_grilla_*.html")), "177663", 2026, 8)
    assert any("mes" in p for p in problemas)


def test_sin_registros_es_valida_y_sin_filas(s02, fixture_bytes):
    pagina = s02.sopa(fixture_bytes("simv_sin_registros_*.html"))
    assert s02.validar(pagina, "177663", 2021, 1) == []
    assert s02.leer_grilla(pagina) == []


def test_respuesta_sin_grilla_se_reconoce_como_incidencia(s02, fixture_bytes):
    pagina = s02.sopa(fixture_bytes("simv_sin_grilla_*.html"))
    problemas = s02.validar(pagina, "181125", 2021, 1)
    assert problemas and s02.solo_falta_grilla(problemas)


def test_robots_ausente_permite_con_politica_conservadora(s02, log, tmp_path, monkeypatch):
    redireccion = RespuestaSimulada(b"<html>gob.pe</html>", url="https://www.gob.pe/smv")
    monkeypatch.setattr(s02, "solicitar", lambda *a, **k: redireccion)
    assert s02.revisar_robots(None, log, destino=tmp_path) is True
    assert "no publica un robots.txt propio" in (tmp_path / "smv_robots_evidencia.txt").read_text(encoding="utf-8")


def test_robots_que_prohibe_la_ruta_detiene_el_rastreo(s02, log, tmp_path, monkeypatch):
    robots = RespuestaSimulada(b"User-agent: *\nDisallow: /SIMV/\n", url="https://www.smv.gob.pe/robots.txt",
                               headers={"content-type": "text/plain"})
    monkeypatch.setattr(s02, "solicitar", lambda *a, **k: robots)
    assert s02.revisar_robots(None, log, destino=tmp_path) is False


def test_censo_se_detiene_tras_fallos_seguidos_y_no_guarda_respuestas_invalidas(s02, fixture_bytes, log, tmp_path, monkeypatch):
    lista = fixture_bytes("simv_lista_vigentes.html")
    sin_grilla = fixture_bytes("simv_sin_grilla_*.html")
    llamadas = []
    monkeypatch.setattr(s02, "DIR_SIMV", tmp_path)
    monkeypatch.setattr(s02, "iniciar_estado", lambda *a, **k: (RespuestaSimulada(lista), s02.sopa(lista)))

    def consultar(*args, **kwargs):
        llamadas.append(args[3:6])
        return RespuestaSimulada(sin_grilla)

    monkeypatch.setattr(s02, "consultar", consultar)
    ok, incidencias = s02.censo(None, log, reanudar=False)
    assert ok is False and incidencias == []
    assert len(llamadas) == 2 * s02.MAX_FALLOS_SEGUIDOS  # 2 intentos por mes, se detiene al 5.º mes fallido
    assert not list(tmp_path.glob("*_*_*.html"))  # ninguna respuesta inválida entra a la base
    assert len(list((tmp_path / "incidencias").glob("*_no_valida.html"))) == s02.MAX_FALLOS_SEGUIDOS
