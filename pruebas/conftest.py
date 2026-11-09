# Diego Sebastián Aliaga Damián
# 2024200481M
# Tema 96: Fintech y financiamiento participativo (crowdfunding) en el Perú: oferta y condiciones
# Fecha de extracción: 2026-11-07 (censo) y 2026-11-08 (reanudación)
"""Configuración común de las pruebas (pytest).

- Carga los scripts 01-03 y auditoria.py como módulos (sus nombres empiezan con número).
- Ofrece respuestas HTTP simuladas a partir de recortes de respuestas reales (pruebas/fixtures/),
  para que las pruebas no dependan de los servidores del BCRP ni de la SMV.
- Usa un logger silencioso: ninguna prueba escribe en log_ejecucion.txt ni en datos_crudos/.
"""
from __future__ import annotations

import json
import logging
import sys
from pathlib import Path

import pytest

RAIZ = Path(__file__).resolve().parent.parent
FIXTURES = RAIZ / "pruebas" / "fixtures"
sys.path.insert(0, str(RAIZ / "codigo"))

import auditoria  # noqa: E402  (el módulo necesita la ruta de codigo/ en sys.path)


class RespuestaSimulada:
    """Imita lo que usan los scripts de requests.Response: status_code, content, text, json, url, headers."""

    def __init__(self, contenido: bytes, status_code: int = 200, url: str = "https://ejemplo.pe",
                 headers: dict | None = None):
        self.content, self.status_code, self.url = contenido, status_code, url
        self.headers = headers or {"content-type": "text/html; charset=utf-8"}
        self.history = []

    @property
    def text(self) -> str:
        return self.content.decode("utf-8", errors="replace")

    def json(self):
        return json.loads(self.content)


@pytest.fixture(scope="session")
def s01():
    return auditoria.cargar_script("01_extraccion_api.py")


@pytest.fixture(scope="session")
def s02():
    return auditoria.cargar_script("02_scraping_web.py")


@pytest.fixture
def log():
    return auditoria.logger_silencioso()


@pytest.fixture
def fixture_bytes():
    def leer(nombre: str) -> bytes:
        coincidencias = sorted(FIXTURES.glob(nombre))
        assert coincidencias, f"falta el fixture {nombre}"
        return coincidencias[0].read_bytes()
    return leer
