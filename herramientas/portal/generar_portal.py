# Diego Sebastián Aliaga Damián
# 2024200481M
# Tema 96: Fintech y financiamiento participativo (crowdfunding) en el Perú: oferta y condiciones
# Fecha: 2026-11-26
"""Portal de entrega (sitio estático para GitHub Pages, carpeta portal/).

El portal reúne los productos, la base de datos y el código del proyecto. Todas las cifras salen de los archivos que
genera el análisis; nada se escribe a mano.

Uso (desde la raíz del proyecto):
    python herramientas/portal/generar_portal.py             # datos, vistas previas y archivos (requiere pymupdf y Pillow)
    python herramientas/portal/generar_portal.py --archivos  # solo copia los descargables (GitHub Actions; biblioteca estándar)

Los artículos de terceros (los 20 PDF y sus traducciones) no se publican: solo su referencia, su DOI y su cuartil.
"""
from __future__ import annotations

import csv
import hashlib
import io
import json
import re
import shutil
import subprocess
import sys
import zipfile
from datetime import date
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
PORTAL = RAIZ / "portal"
IMG = PORTAL / "img"
ARCHIVOS = PORTAL / "archivos"          # se genera; no va al repositorio (.gitignore)
REPOSITORIO = "https://github.com/Diego-Aliaga-Damian/finanzas1-u2-crowdfunding-peru"
DASHBOARD = "https://fincrowd-peru-diego-aliaga.streamlit.app/"
DESCARGAS = RAIZ / "dashboard" / "descargas"
ENTREGA = RAIZ / "entregas" / "DIEGO_SEBASTIAN_ALIAGA_DAMIAN"
ZIP_ENTREGA = RAIZ / "entregas" / "ALIAGA_DAMIAN_DIEGO_SEBASTIAN_UNIDAD-II.zip"

# Orden del estado del arte (el mismo de la carpeta N.º 1: 01_Braggion_2025.pdf, ..., 20_Ma_2023.pdf)
ARTICULOS = ["braggion2025", "hau2024", "kim2026", "serfes2025", "chu2024", "vives2025", "eid2024", "beaumont2026",
             "bennaceur2026", "onorato2024", "pampurini2024", "fasano2026", "ran2025", "lazos2025", "danisewicz2023",
             "fareed2025", "morello2025", "alvarezfranco2026", "miglo2025", "ma2023"]
# Cuartil SJR verificado a mano por el estudiante el 2026-11-26 (LEEME de la carpeta de artículos)
CUARTIL = {k: "Q1" for k in ARTICULOS} | {"alvarezfranco2026": "Q2"}

# Archivo descargable: (ruta en el portal, origen en el repositorio)
COPIAS = [
    ("archivos/Aliaga_Damian_articulo_FPF_Peru.pdf", "dashboard/descargas/Aliaga_Damian_articulo_FPF_Peru.pdf"),
    ("archivos/Aliaga_Damian_articulo_FPF_Peru_typst.pdf", "dashboard/descargas/Aliaga_Damian_articulo_FPF_Peru_typst.pdf"),
    ("archivos/Aliaga_Damian_beamer.pdf", "dashboard/descargas/Aliaga_Damian_beamer.pdf"),
    ("archivos/Aliaga_Damian_beamer_para_imprimir.pdf", "dashboard/descargas/Aliaga_Damian_beamer_para_imprimir.pdf"),
    ("archivos/Aliaga_Damian_poster_articulo.pdf", "dashboard/descargas/Aliaga_Damian_poster_articulo.pdf"),
    ("archivos/Aliaga_Damian_posteres_20_articulos.zip", "dashboard/descargas/Aliaga_Damian_posteres_20_articulos.zip"),
    ("archivos/Guia_completa_del_proyecto.pdf", "docs/guia/Guia_completa_del_proyecto.pdf"),
    ("archivos/datos_procesados_2024200481M.csv", "datos_procesados/datos_procesados_2024200481M.csv"),
    ("archivos/datos_procesados_2024200481M_empresas.csv", "datos_procesados/datos_procesados_2024200481M_empresas.csv"),
]


# ----------------------------------------------------------------------------- archivos descargables (sin dependencias)
def copiar_archivos() -> None:
    if ARCHIVOS.exists():
        shutil.rmtree(ARCHIVOS)
    (ARCHIVOS / "posteres").mkdir(parents=True)
    for destino, origen in COPIAS:
        shutil.copy2(RAIZ / origen, PORTAL / destino)
    with zipfile.ZipFile(DESCARGAS / "Aliaga_Damian_posteres_20_articulos.zip") as z:
        for nombre in z.namelist():
            if re.fullmatch(r"poster_[a-z0-9]+\.pdf", nombre):
                (ARCHIVOS / "posteres" / nombre).write_bytes(z.read(nombre))
    (PORTAL / ".nojekyll").write_text("", encoding="utf-8")
    print(f"archivos copiados en {ARCHIVOS.relative_to(RAIZ).as_posix()}")


# ----------------------------------------------------------------------------- datos del portal
def cifras() -> dict[str, str]:
    s = (RAIZ / "articulo_typst" / "generado" / "cifras.typ").read_text(encoding="utf-8")
    return dict(re.findall(r'^\s*"([^"]+)":\s*"([^"]*)",?\s*$', s, re.M))


def bib() -> dict[str, dict]:
    s = (RAIZ / "articulo" / "referencias.bib").read_text(encoding="utf-8")
    out = {}
    for m in re.finditer(r"@\w+\{([^,]+),(.*?)\n\}", s, re.S):
        cuerpo = m.group(2)

        def campo(n: str) -> str:
            mm = re.search(rf"\b{n}\s*=\s*\{{(.*?)\}},?\s*\n", cuerpo, re.S | re.I)
            return re.sub(r"\s+", " ", mm.group(1)).replace("{", "").replace("}", "").replace("\\&", "&").strip() if mm else ""
        autores = [a.split(",")[0].strip() for a in re.split(r"\s+and\s+", campo("author"))]
        corto = autores[0] if len(autores) == 1 else f"{autores[0]} y {autores[1]}" if len(autores) == 2 else f"{autores[0]} et al."
        out[m.group(1).strip()] = {"titulo": campo("title"), "autores": corto, "revista": campo("journal"),
                                   "anio": campo("year"), "doi": campo("DOI").lower()}
    return out


def versiones() -> dict[str, tuple[int, str]]:
    """N.º -> (páginas, versión) según el LEEME de la carpeta de artículos (local; no está en el repositorio)."""
    f = RAIZ / "entregas" / "Carpeta_1_articulos" / "LEEME_articulos.md"
    if not f.exists():
        return {}
    filas = re.findall(r"^\| (\d{2}) \| \d{2}_[^|]+\.pdf \| (\d+) \| ([^|]+) \|$", f.read_text(encoding="utf-8"), re.M)
    return {n: (int(p), re.sub(r"\s*\(.*", "", v).strip()) for n, p, v in filas}


def poster_tex(clave: str) -> dict[str, str]:
    s = (RAIZ / "productos" / "posteres_articulos" / "articulos" / f"{clave}.tex").read_text(encoding="utf-8")
    g = lambda n: (re.search(rf"\\def\\{n}\{{(.*?)\}}\s*$", s, re.M) or [None, ""])[1]
    return {"titulo_es": g("TituloEs"), "ambito": g("Ambito"), "enfoque": g("Enfoque")}


def arbol(carpeta: Path) -> dict:
    hijos = sorted(carpeta.iterdir(), key=lambda p: (p.is_file(), p.name.lower()))
    nodo = {"n": carpeta.name, "h": [arbol(p) if p.is_dir() else {"n": p.name, "s": p.stat().st_size} for p in hijos]}
    nodo["s"] = sum(h["s"] for h in nodo["h"])
    nodo["c"] = sum(h.get("c", 1) for h in nodo["h"])
    return nodo


def contar_pruebas() -> int:
    py = RAIZ / ".venv" / "Scripts" / "python.exe"
    r = subprocess.run([str(py if py.exists() else sys.executable), "-m", "pytest", "--collect-only", "-q"], cwd=RAIZ,
                       capture_output=True, text=True, encoding="utf-8", errors="replace")
    m = re.search(r"(\d+) tests? collected", r.stdout)
    if m:
        return int(m.group(1))
    return sum(int(x) for x in re.findall(r"^\S+\.py: (\d+)$", r.stdout, re.M))   # salida «archivo: n» de pytest


def serie_mensual() -> list[dict]:
    f = RAIZ / "salidas" / "figuras" / "f1_monto_mensual_por_plataforma_datos.csv"
    with f.open(encoding="utf-8") as fh:
        filas = list(csv.DictReader(fh))
    periodo = next(c for c in filas[0] if "periodo" in c.lower() or c == "")
    out = []
    for r in filas:
        total = sum(float(v) for k, v in r.items() if k != periodo and v not in ("", None))
        out.append({"p": r[periodo], "m": round(total, 3)})
    return out


def lineas(ruta: str) -> int:
    return sum(1 for _ in (RAIZ / ruta).open(encoding="utf-8"))


def mb(ruta: Path) -> float:
    return round(ruta.stat().st_size / 1e6, 1)


def datos_portal(paginas: dict[str, int]) -> dict:
    c, b, v = cifras(), bib(), versiones()
    res = json.loads((RAIZ / "salidas" / "resultados_04.json").read_text(encoding="utf-8"))
    aud = (RAIZ / "salidas" / "reporte_auditoria.md").read_text(encoding="utf-8")
    controles = int(re.search(r"(\d+) cumplen", aud).group(1))
    articulos = []
    for i, k in enumerate(ARTICULOS, 1):
        n = f"{i:02d}"
        pag, ver = v.get(n, (None, ""))
        articulos.append({"n": n, "clave": k, **b[k], **poster_tex(k), "cuartil": CUARTIL[k], "paginas": pag,
                          "version": ver, "poster": f"archivos/posteres/poster_{k}.pdf",
                          "img": f"img/posteres/{k}.webp", "mini": f"img/posteres/{k}_m.webp"})
    descargas = {Path(d).stem: {"url": d, "mb": mb(RAIZ / o), "nombre": Path(d).name} for d, o in COPIAS}
    scripts = [
        ("codigo/01_extraccion_api.py", "Extracción por API", "BCRPData (10 series) y SMV OData (estados financieros)."),
        ("codigo/02_scraping_web.py", "Scraping del portal SIMV", "Proyectos y montos por plataforma y mes, con pausas y validación de eco."),
        ("codigo/03_limpieza_datos.py", "Limpieza e integración", "Tipifica, controla totales y arma el panel balanceado y la base de empresas."),
        ("codigo/04_analisis.py", "Análisis", "Indicadores, contrastes y las 15 tablas y 5 figuras del artículo."),
        ("codigo/econometria.py", "Pruebas econométricas", "Raíz unitaria, cointegración, corto plazo HAC, reforma, logit y panel."),
        ("codigo/auditoria.py", "Auditoría", "Controles de integridad y cotejo en vivo con las fuentes oficiales."),
        ("codigo/comun.py", "Funciones comunes", "Constantes del periodo, registro de ejecución y utilidades compartidas."),
    ]
    entrega = arbol(ENTREGA) if ENTREGA.exists() else None
    crudos = sum(1 for p in (RAIZ / "datos_crudos").rglob("*") if p.is_file())
    tablas = sum(1 for p in (RAIZ / "salidas" / "tablas").glob("*.csv") if re.match(r"t\d+_", p.name))
    figuras = len(list((RAIZ / "salidas" / "figuras").glob("*.pdf")))
    return {
        "generado": date.today().isoformat(),
        "repositorio": REPOSITORIO, "dashboard": DASHBOARD,
        "cifras": {k: c[k] for k in ("filasPanel", "columnasPanel", "plataformasAutorizadas", "plataformasConFinanciamiento",
                                     "monto2022", "monto2025", "monto2026", "participacionLider", "nombreLider", "logN",
                                     "empRoaN", "solicitudesHTTP", "coberturaPct", "fechaInicio", "fechaCorte",
                                     "mesesActividadFPF", "hhi2025", "cpConWaldP", "logUnoOr", "logTresOr",
                                     "refPlacebos", "refPlacebosN", "empRoaP", "muSeriesObs", "teaBcosPyme2022",
                                     "teaBcosPyme2026")},
        "verificacion": {"pruebas": contar_pruebas(), "controles": controles,
                         "sha_base": res["sha256_base_procesada"], "sha_empresas": res["econometria"]["sha256_base_empresas"],
                         "crudos": crudos, "tablas": tablas, "figuras": figuras},
        "paginas": paginas, "descargas": descargas, "articulos": articulos,
        "scripts": [{"ruta": r, "titulo": t, "texto": x, "lineas": lineas(r)} for r, t, x in scripts],
        "serie": serie_mensual(),
        "entrega": entrega,
        "zip": {"nombre": ZIP_ENTREGA.name, "mb": mb(ZIP_ENTREGA)} if ZIP_ENTREGA.exists() else None,
    }


# ----------------------------------------------------------------------------- vistas previas (pymupdf y Pillow)
def vistas_previas() -> dict[str, int]:
    import pymupdf
    from PIL import Image

    def guardar(pix, destino: Path, ancho: int, calidad: int = 72) -> None:
        im = Image.open(io.BytesIO(pix.tobytes("png"))).convert("RGB")
        if im.width > ancho:
            im = im.resize((ancho, round(im.height * ancho / im.width)), Image.LANCZOS)
        destino.parent.mkdir(parents=True, exist_ok=True)
        im.save(destino, "WEBP", quality=calidad, method=6)

    def paginas(pdf: Path, carpeta: str, prefijo: str, ancho: int, dpi: int, calidad: int, solo: int = 0) -> int:
        d = pymupdf.open(pdf)
        for i, p in enumerate(d, 1):
            if solo and i > solo:
                break
            guardar(p.get_pixmap(dpi=dpi), IMG / carpeta / f"{prefijo}{i:02d}.webp", ancho, calidad)
        return len(d)

    if IMG.exists():
        shutil.rmtree(IMG)
    n = {"articulo": paginas(DESCARGAS / "Aliaga_Damian_articulo_FPF_Peru.pdf", "articulo", "p", 900, 120, 62),
         "typst": paginas(DESCARGAS / "Aliaga_Damian_articulo_FPF_Peru_typst.pdf", "typst", "p", 900, 120, 62, solo=1),
         "beamer": paginas(DESCARGAS / "Aliaga_Damian_beamer.pdf", "beamer", "d", 1280, 150, 66)}
    d = pymupdf.open(DESCARGAS / "Aliaga_Damian_poster_articulo.pdf")
    guardar(d[0].get_pixmap(dpi=55), IMG / "poster_articulo.webp", 1600, 74)
    guardar(d[0].get_pixmap(dpi=22), IMG / "poster_articulo_m.webp", 640, 66)
    for k in ARTICULOS:
        d = pymupdf.open(RAIZ / "productos" / "posteres_articulos" / "pdf" / f"poster_{k}.pdf")
        guardar(d[0].get_pixmap(dpi=42), IMG / "posteres" / f"{k}.webp", 960, 64)
        guardar(d[0].get_pixmap(dpi=18), IMG / "posteres" / f"{k}_m.webp", 420, 64)
    for nombre in ("logo_uncp.png", "logo_facultad.png"):
        im = Image.open(RAIZ / "productos" / "posteres_articulos" / "img" / nombre).convert("RGBA")
        im.thumbnail((220, 220))
        im.save(IMG / nombre.replace(".png", ".webp"), "WEBP", quality=88)
    for nombre in ("fincrowd.svg", "fincrowd_icono.svg"):
        shutil.copy2(RAIZ / "dashboard" / "img" / nombre, IMG / nombre)
    return n


def main() -> int:
    if "--archivos" not in sys.argv:
        n = vistas_previas()
        datos = datos_portal(n)
        (PORTAL / "datos.js").write_text("// Generado por herramientas/portal/generar_portal.py; no editar a mano.\n"
                                         f"window.PORTAL = {json.dumps(datos, ensure_ascii=False, separators=(',', ':'))};\n",
                                         encoding="utf-8")
        peso = sum(p.stat().st_size for p in IMG.rglob("*") if p.is_file()) / 1e6
        print(f"datos.js y {sum(1 for p in IMG.rglob('*') if p.is_file())} imágenes ({peso:.1f} MB)")
    copiar_archivos()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
