# Diego Sebastián Aliaga Damián
# 2024200481M
# Tema 96: Fintech y financiamiento participativo (crowdfunding) en el Perú: oferta y condiciones
# Fecha de extracción: 2026-11-07 (censo) y 2026-11-08 (reanudación)
"""Pruebas del portal de entrega (portal/): sus cifras son las del análisis y no tiene enlaces rotos."""
import json
import re

import pytest

from conftest import RAIZ

PORTAL = RAIZ / "portal"


@pytest.fixture(scope="module")
def datos():
    s = (PORTAL / "datos.js").read_text(encoding="utf-8")
    return json.loads(s[s.index("{"):s.rindex("}") + 1])


def test_cifras_y_huellas_del_portal_son_las_del_analisis(datos):
    s = (RAIZ / "articulo_typst" / "generado" / "cifras.typ").read_text(encoding="utf-8")
    cifras = dict(re.findall(r'^\s*"([^"]+)":\s*"([^"]*)",?\s*$', s, re.M))
    assert all(cifras[k] == v for k, v in datos["cifras"].items())
    res = json.loads((RAIZ / "salidas" / "resultados_04.json").read_text(encoding="utf-8"))
    assert datos["verificacion"]["sha_base"] == res["sha256_base_procesada"]
    assert datos["verificacion"]["sha_empresas"] == res["econometria"]["sha256_base_empresas"]
    assert len(datos["articulos"]) == 20 and {a["cuartil"] for a in datos["articulos"]} <= {"Q1", "Q2"}


def test_el_portal_no_tiene_enlaces_rotos(datos):
    import importlib.util
    spec = importlib.util.spec_from_file_location("generar_portal", RAIZ / "herramientas" / "portal" / "generar_portal.py")
    gp = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(gp)
    # cada descargable sale de un archivo del repositorio (GitHub Actions lo copia al publicar)
    assert all((RAIZ / origen).exists() for _, origen in gp.COPIAS)
    assert {d["url"] for d in datos["descargas"].values()} == {destino for destino, _ in gp.COPIAS}
    # cada imagen que usan la página y los datos existe
    html = (PORTAL / "index.html").read_text(encoding="utf-8") + (PORTAL / "app.js").read_text(encoding="utf-8")
    rutas = set(re.findall(r'(?:src|href)="((?:img/)[^"$]+)"', html))
    rutas |= {a[k] for a in datos["articulos"] for k in ("img", "mini")}
    rutas |= {f"img/articulo/p{i:02d}.webp" for i in range(1, datos["paginas"]["articulo"] + 1)}
    rutas |= {f"img/beamer/d{i:02d}.webp" for i in range(1, datos["paginas"]["beamer"] + 1)}
    faltan = sorted(r for r in rutas if not (PORTAL / r).exists())
    assert not faltan, faltan
    # los artículos de terceros no se publican en el portal
    assert not list(PORTAL.rglob("*_es.pdf")) and not any(re.match(r"\d{2}_[A-Z]", p.name) for p in PORTAL.rglob("*.pdf"))
