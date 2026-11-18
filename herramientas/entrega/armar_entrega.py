# Diego Sebastián Aliaga Damián
# 2024200481M
# Tema 96: Fintech y financiamiento participativo (crowdfunding) en el Perú: oferta y condiciones
# Fecha: 2026-11-15
"""Arma la carpeta de entrega de la Unidad II según el numeral 2.5 de la consigna (y, con --zip, el comprimido).

Carpeta general con los nombres y apellidos completos y tres subcarpetas:
    N1_Productos_...            artículo (LaTeX y Typst), Beamer, póster, 20 pósteres, 20 artículos en inglés,
                                sus traducciones al español y el enlace del dashboard
    N2_Desarrollo_...           templates: journal (LaTeX y Typst), póster, Beamer, 20 pósteres y el código del dashboard
    N3_Base_de_datos_y_codigo_...   /codigo, /datos_crudos, /datos_procesados, /salidas, diccionario, README.md,
                                requirements.txt, .env.example, log_ejecucion.txt, incidencias_fuente.md y enlace de GitHub
Solo copia archivos: no recompila nada ni modifica el proyecto. Se vuelve a ejecutar cada vez que se agregan
artículos o traducciones. Al final imprime la lista de verificación con lo que falta.

Uso (desde la raíz del proyecto):
    python herramientas/entrega/armar_entrega.py          # arma la carpeta en entregas/
    python herramientas/entrega/armar_entrega.py --zip    # además crea APELLIDOS_NOMBRES_UNIDAD-II.zip
"""
from __future__ import annotations

import shutil
import sys
import zipfile
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
ENTREGAS = RAIZ / "entregas"
NOMBRE = "Diego_Sebastian_Aliaga_Damian"
GENERAL = ENTREGAS / "DIEGO_SEBASTIAN_ALIAGA_DAMIAN"            # «NOMBRES Y APELLIDOS completos» (2.5)
ZIP = ENTREGAS / "ALIAGA_DAMIAN_DIEGO_SEBASTIAN_UNIDAD-II.zip"   # «APELLIDOS_NOMBRES_UNIDAD-II.zip» (2.3)
N1 = GENERAL / f"N1_Productos_{NOMBRE}"
N2 = GENERAL / f"N2_Desarrollo_{NOMBRE}"
N3 = GENERAL / f"N3_Base_de_datos_y_codigo_{NOMBRE}"
REPOSITORIO = "https://github.com/Diego-Aliaga-Damian/finanzas1-u2-crowdfunding-peru"
DASHBOARD = "https://fincrowd-peru-diego-aliaga.streamlit.app/"
ARTICULOS = ENTREGAS / "Carpeta_1_articulos"
SOBRAS = shutil.ignore_patterns("__pycache__", "*.pyc", "*.aux", "*.log", "*.bbl", "*.bcf", "*.blg", "*.run.xml",
                                "*.out", "*.toc", "*.nav", "*.snm", "*.fls", "*.fdb_latexmk", "*.synctex.gz", "*.pdf")
faltan: list[str] = []


def copiar(origen: Path, destino: Path, ignorar=None) -> None:
    if not origen.exists():
        faltan.append(f"No existe {origen.relative_to(RAIZ).as_posix()}")
        return
    destino.parent.mkdir(parents=True, exist_ok=True)
    if origen.is_dir():
        shutil.copytree(origen, destino, ignore=ignorar)
    else:
        shutil.copy2(origen, destino)


def enlace(destino: Path, url: str, texto: str) -> None:
    """Acceso directo de Windows (.url) y un .txt legible en cualquier sistema."""
    destino.with_suffix(".url").write_text(f"[InternetShortcut]\nURL={url}\n", encoding="utf-8")
    destino.with_suffix(".txt").write_text(f"{texto}\n{url}\n", encoding="utf-8")


def productos() -> None:
    copiar(RAIZ / "articulo" / "articulo.pdf", N1 / "Aliaga_Damian_articulo_FPF_Peru.pdf")
    copiar(RAIZ / "articulo_typst" / "articulo.pdf", N1 / "Aliaga_Damian_articulo_FPF_Peru_typst.pdf")
    copiar(RAIZ / "productos" / "beamer" / "beamer.pdf", N1 / "Aliaga_Damian_beamer.pdf")
    copiar(RAIZ / "productos" / "beamer" / "beamer_impresion.pdf", N1 / "Aliaga_Damian_beamer_para_imprimir.pdf")
    copiar(RAIZ / "productos" / "poster_articulo" / "poster_articulo.pdf", N1 / "Aliaga_Damian_poster_articulo.pdf")
    copiar(RAIZ / "productos" / "posteres_articulos" / "pdf", N1 / "Posteres_20_articulos_espanol")
    copiar(ARTICULOS / "1_originales_ingles", N1 / "Articulos_20_ingles_Q1_Q2",
           shutil.ignore_patterns("*.md", "desktop.ini"))
    copiar(ARTICULOS / "2_traducciones_espanol", N1 / "Articulos_20_traducidos_espanol",
           shutil.ignore_patterns("*.md", "desktop.ini"))
    enlace(N1 / "Dashboard_FinCrowd_Peru", DASHBOARD,
           "Dashboard interactivo del artículo (FinCrowd Perú), publicado en Streamlit Community Cloud:")


def desarrollo() -> None:
    art = N2 / "1_journal_LaTeX"
    copiar(RAIZ / "articulo" / "articulo.tex", art / "articulo.tex")
    copiar(RAIZ / "articulo" / "referencias.bib", art / "referencias.bib")
    copiar(RAIZ / "articulo" / "secciones", art / "secciones", SOBRAS)
    copiar(RAIZ / "articulo" / "generado", art / "generado", SOBRAS)
    copiar(RAIZ / "productos" / "poster_articulo", N2 / "2_poster_articulo_LaTeX", SOBRAS)
    copiar(RAIZ / "productos" / "beamer", N2 / "3_beamer_LaTeX", SOBRAS)
    copiar(RAIZ / "productos" / "posteres_articulos", N2 / "4_posteres_20_articulos_LaTeX",
           shutil.ignore_patterns("pdf", "__pycache__", "*.aux", "*.log", "*.bbl", "*.bcf", "*.blg", "*.run.xml",
                                  "*.out", "*.fls", "*.fdb_latexmk", "*.synctex.gz", "*.pdf"))
    copiar(RAIZ / "articulo_typst", N2 / "5_journal_Typst", SOBRAS)
    copiar(RAIZ / "dashboard", N2 / "6_dashboard_Streamlit", shutil.ignore_patterns("descargas", "__pycache__", "*.pyc"))
    copiar(RAIZ / ".streamlit" / "config.toml", N2 / "6_dashboard_Streamlit" / ".streamlit" / "config.toml")
    (N2 / "LEEME_desarrollo.txt").write_text(
        "Fuentes (templates) de los productos. Se compilan dentro de la estructura del repositorio, porque leen las\n"
        "tablas, figuras y cifras de /salidas y de articulo/generado:\n"
        f"  {REPOSITORIO}\n\n"
        "1_journal_LaTeX        articulo.tex (pdflatex + biber); secciones/ y generado/\n"
        "2_poster_articulo_LaTeX  poster_articulo.tex\n"
        "3_beamer_LaTeX         beamer.tex (proyectar) y beamer_impresion.tex (una diapositiva por hoja)\n"
        "4_posteres_20_articulos_LaTeX  plantilla_poster.tex y un .tex por artículo (articulos/)\n"
        "5_journal_Typst        articulo.typ: versión Typst del mismo artículo (typst compile articulo.typ --root ..)\n"
        f"6_dashboard_Streamlit  app.py: dashboard interactivo (streamlit run dashboard/app.py), publicado en {DASHBOARD}\n",
        encoding="utf-8")


def codigo_y_datos() -> None:
    for carpeta in ("codigo", "datos_crudos", "datos_procesados", "salidas"):
        copiar(RAIZ / carpeta, N3 / carpeta, shutil.ignore_patterns("__pycache__", "*.pyc"))
    for archivo in ("diccionario_variables.md", "README.md", "requirements.txt", ".env.example", "log_ejecucion.txt",
                    "incidencias_fuente.md"):
        copiar(RAIZ / archivo, N3 / archivo)
    # Adicional: las pruebas automatizadas que el README indica ejecutar (python -m pytest). Las del dashboard se
    # omiten aquí porque el dashboard está en la Carpeta N.º 2 (se ejecutan en el repositorio completo).
    copiar(RAIZ / "pruebas", N3 / "pruebas", shutil.ignore_patterns("__pycache__", "*.pyc", "test_dashboard*.py"))
    copiar(RAIZ / "pytest.ini", N3 / "pytest.ini")
    enlace(N3 / "enlace_repositorio_GitHub", REPOSITORIO, "Repositorio público del proyecto (código, datos y productos):")


def contar(carpeta: Path, patron: str = "*.pdf") -> int:
    return len(list(carpeta.glob(patron))) if carpeta.exists() else 0


def verificacion() -> list[tuple[str, str, bool]]:
    originales = sorted(p.stem for p in (N1 / "Articulos_20_ingles_Q1_Q2").glob("*.pdf"))
    traducidos = {p.stem.removesuffix("_es") for p in (N1 / "Articulos_20_traducidos_espanol").glob("*.pdf")}
    sin_traduccion = [o for o in originales if o not in traducidos]
    filas = [
        ("N1 · Artículo (journal) en LaTeX, en PDF", "sí" if (N1 / "Aliaga_Damian_articulo_FPF_Peru.pdf").exists() else "NO",
         (N1 / "Aliaga_Damian_articulo_FPF_Peru.pdf").exists()),
        ("N1 · Beamer en PDF", "sí" if (N1 / "Aliaga_Damian_beamer.pdf").exists() else "NO",
         (N1 / "Aliaga_Damian_beamer.pdf").exists()),
        ("N1 · Póster del artículo en PDF", "sí" if (N1 / "Aliaga_Damian_poster_articulo.pdf").exists() else "NO",
         (N1 / "Aliaga_Damian_poster_articulo.pdf").exists()),
        ("N1 · 20 pósteres en español", f"{contar(N1 / 'Posteres_20_articulos_espanol')}/20",
         contar(N1 / "Posteres_20_articulos_espanol") == 20),
        ("N1 · 20 artículos en inglés", f"{len(originales)}/20", len(originales) == 20),
        ("N1 · Los mismos artículos traducidos", f"{len(originales) - len(sin_traduccion)}/20",
         len(originales) == 20 and not sin_traduccion),
        ("N1 · Adicional: artículo en Typst y enlace del dashboard",
         "sí" if (N1 / "Aliaga_Damian_articulo_FPF_Peru_typst.pdf").exists() else "NO",
         (N1 / "Aliaga_Damian_articulo_FPF_Peru_typst.pdf").exists()),
        ("N2 · Templates: journal, póster, Beamer", "sí", all((N2 / d).exists() for d in
                                                       ("1_journal_LaTeX", "2_poster_articulo_LaTeX", "3_beamer_LaTeX"))),
        ("N2 · Templates de los 20 pósteres", f"{contar(N2 / '4_posteres_20_articulos_LaTeX' / 'articulos', '*.tex')}/20",
         contar(N2 / "4_posteres_20_articulos_LaTeX" / "articulos", "*.tex") == 20),
        ("N3 · /codigo con los cuatro scripts", f"{sum((N3 / 'codigo' / f'{s}.py').exists() for s in ('01_extraccion_api', '02_scraping_web', '03_limpieza_datos', '04_analisis'))}/4",
         all((N3 / "codigo" / f"{s}.py").exists() for s in ("01_extraccion_api", "02_scraping_web", "03_limpieza_datos", "04_analisis"))),
        ("N3 · /datos_crudos, /datos_procesados, /salidas", "sí",
         all((N3 / d).exists() for d in ("datos_crudos", "datos_procesados", "salidas"))),
        ("N3 · diccionario, README, requirements, .env.example, log, incidencias, enlace", "sí",
         all((N3 / f).exists() for f in ("diccionario_variables.md", "README.md", "requirements.txt", ".env.example",
                                          "log_ejecucion.txt", "incidencias_fuente.md", "enlace_repositorio_GitHub.txt"))),
    ]
    if sin_traduccion and len(sin_traduccion) < len(originales):
        faltan.append("Sin traducción: " + ", ".join(sin_traduccion))
    return filas


def comprimir() -> None:
    if ZIP.exists():
        ZIP.unlink()
    with zipfile.ZipFile(ZIP, "w", zipfile.ZIP_DEFLATED) as z:
        for f in sorted(GENERAL.rglob("*")):
            if f.is_file():
                z.write(f, f.relative_to(ENTREGAS).as_posix())
    print(f"\nZIP: {ZIP.relative_to(RAIZ).as_posix()} ({ZIP.stat().st_size / 1e6:.1f} MB)")


def main() -> int:
    if GENERAL.exists():
        shutil.rmtree(GENERAL)  # solo la carpeta generada por este script
    productos()
    desarrollo()
    codigo_y_datos()
    filas = verificacion()
    (GENERAL / "LEEME.txt").write_text(
        "Finanzas I (055D), Unidad II, tema N.º 96. Diego Sebastián Aliaga Damián (2024200481M).\n"
        "Fintech y financiamiento participativo (crowdfunding) en el Perú: oferta y condiciones, 2022-2026\n\n"
        f"N1_Productos     productos en PDF, los 20 artículos con sus traducciones y el enlace del dashboard\n"
        f"N2_Desarrollo    templates LaTeX y Typst y el código del dashboard\n"
        f"N3_Base_de_datos_y_codigo   código, datos crudos y procesados, salidas y documentación\n\n"
        f"Dashboard: {DASHBOARD}\nRepositorio: {REPOSITORIO}\n", encoding="utf-8")
    print(f"Carpeta: {GENERAL.relative_to(RAIZ).as_posix()}\n")
    for etiqueta, valor, ok in filas:
        print(f"  [{'OK' if ok else '..'}] {etiqueta}: {valor}")
    for f in faltan:
        print(f"  Falta: {f}")
    if "--zip" in sys.argv:
        comprimir()
    return 0


if __name__ == "__main__":
    sys.exit(main())
