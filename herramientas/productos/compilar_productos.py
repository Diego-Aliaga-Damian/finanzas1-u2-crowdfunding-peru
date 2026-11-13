# Diego Sebastián Aliaga Damián
# 2024200481M
# Tema 96: Fintech y financiamiento participativo (crowdfunding) en el Perú: oferta y condiciones
# Fecha: 2026-11-12
"""Compila el Beamer (proyección e impresión) y el póster del artículo (Fase X).

Antes de compilar regenera las cifras del artículo (articulo/generado/cifras.tex), que usan los tres productos.
Uso (desde la raíz del proyecto): python herramientas/productos/compilar_productos.py
Salidas: productos/beamer/beamer.pdf, productos/beamer/beamer_impresion.pdf y
         productos/poster_articulo/poster_articulo.pdf
"""
import os
import shutil
import subprocess
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
PRODUCTOS = [  # (carpeta, archivo, usa biber)
    (RAIZ / "productos" / "beamer", "beamer", False),
    (RAIZ / "productos" / "beamer", "beamer_impresion", False),
    (RAIZ / "productos" / "poster_articulo", "poster_articulo", True),
]
TEMPORALES = (".aux", ".log", ".bbl", ".bcf", ".blg", ".run.xml", ".out", ".nav", ".snm", ".toc", ".vrb")


def ejecutable(nombre: str) -> str:
    encontrado = shutil.which(nombre)
    if encontrado:
        return encontrado
    miktex = Path(os.environ.get("LOCALAPPDATA", "")) / "Programs" / "MiKTeX" / "miktex" / "bin" / "x64" / f"{nombre}.exe"
    if miktex.exists():
        return str(miktex)
    raise FileNotFoundError(f"No se encontró {nombre}: instala MiKTeX o TeX Live")


def compilar(carpeta: Path, nombre: str, usa_biber: bool) -> bool:
    pdflatex = [ejecutable("pdflatex"), "-interaction=nonstopmode", "-halt-on-error", f"{nombre}.tex"]
    pasos = [pdflatex] + ([[ejecutable("biber"), nombre]] if usa_biber else []) + [pdflatex, pdflatex]
    for paso in pasos:
        if subprocess.run(paso, cwd=carpeta, capture_output=True).returncode != 0:
            print(f"ERROR {nombre}: falló {Path(paso[0]).stem} (revisar {nombre}.log)")
            return False
    for ext in TEMPORALES:
        (carpeta / f"{nombre}{ext}").unlink(missing_ok=True)
    print(f"OK {(carpeta / f'{nombre}.pdf').relative_to(RAIZ).as_posix()}")
    return True


def main() -> int:
    subprocess.run([sys.executable, str(RAIZ / "herramientas" / "articulo" / "generar_insumos_articulo.py")],
                   cwd=RAIZ, check=True, capture_output=True)
    fallas = [n for c, n, b in PRODUCTOS if not compilar(c, n, b)]
    return 1 if fallas else 0


if __name__ == "__main__":
    sys.exit(main())
