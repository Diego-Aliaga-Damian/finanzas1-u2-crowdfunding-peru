# Diego Sebastián Aliaga Damián
# 2024200481M
# Tema 96: Fintech y financiamiento participativo (crowdfunding) en el Perú: oferta y condiciones
# Fecha: 2026-11-12
"""Compila los pósteres en español de los artículos del estado del arte (Carpeta N.º 1, Unidad II).

Cada artículo tiene su contenido en productos/posteres_articulos/articulos/<clave>.tex y todos usan la misma
plantilla (plantilla_poster.tex). La clave coincide con la de articulo/referencias.bib, de modo que la referencia
APA del póster sale de la misma bibliografía del artículo.
Uso (desde la raíz del proyecto):
    python herramientas/posteres/generar_posteres.py            # todos
    python herramientas/posteres/generar_posteres.py ran2025    # uno o varios
Los PDF quedan en productos/posteres_articulos/pdf/.
"""
import os
import shutil
import subprocess
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
CARPETA = RAIZ / "productos" / "posteres_articulos"
SALIDA = CARPETA / "pdf"
TEMPORALES = (".aux", ".log", ".bbl", ".bcf", ".blg", ".run.xml", ".out")


def ejecutable(nombre: str) -> str:
    """pdflatex/biber del PATH o, en Windows, de la instalación de MiKTeX por usuario."""
    encontrado = shutil.which(nombre)
    if encontrado:
        return encontrado
    miktex = Path(os.environ.get("LOCALAPPDATA", "")) / "Programs" / "MiKTeX" / "miktex" / "bin" / "x64" / f"{nombre}.exe"
    if miktex.exists():
        return str(miktex)
    raise FileNotFoundError(f"No se encontró {nombre}: instala MiKTeX o TeX Live")


def compilar(clave: str) -> bool:
    trabajo = f"poster_{clave}"
    entrada = rf"\def\articulo{{{clave}}}\input{{plantilla_poster}}"
    pdflatex = [ejecutable("pdflatex"), "-interaction=nonstopmode", "-halt-on-error", f"-jobname={trabajo}", entrada]
    pasos = [pdflatex, [ejecutable("biber"), trabajo], pdflatex, pdflatex]
    for paso in pasos:
        r = subprocess.run(paso, cwd=CARPETA, capture_output=True)
        if r.returncode != 0:
            print(f"ERROR {clave}: falló {Path(paso[0]).stem} (revisar {trabajo}.log)")
            return False
    SALIDA.mkdir(exist_ok=True)
    shutil.move(CARPETA / f"{trabajo}.pdf", SALIDA / f"{trabajo}.pdf")
    for ext in TEMPORALES:
        (CARPETA / f"{trabajo}{ext}").unlink(missing_ok=True)
    print(f"OK {clave} -> {(SALIDA / f'{trabajo}.pdf').relative_to(RAIZ).as_posix()}")
    return True


def main() -> int:
    claves = sys.argv[1:] or sorted(p.stem for p in (CARPETA / "articulos").glob("*.tex"))
    fallas = [c for c in claves if not compilar(c)]
    print(f"\n{len(claves) - len(fallas)} de {len(claves)} pósteres compilados")
    return 1 if fallas else 0


if __name__ == "__main__":
    sys.exit(main())
