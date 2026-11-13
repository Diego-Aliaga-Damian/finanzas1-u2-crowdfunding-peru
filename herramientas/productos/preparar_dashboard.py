# Diego Sebastián Aliaga Damián
# 2024200481M
# Tema 96: Fintech y financiamiento participativo (crowdfunding) en el Perú: oferta y condiciones
# Fecha: 2026-11-13
"""Copia los productos compilados a dashboard/descargas/ para que el dashboard los ofrezca como descarga.

Requiere haber compilado antes: articulo/articulo.pdf (LaTeX), articulo_typst/articulo.pdf (Typst),
productos/beamer/*.pdf, productos/poster_articulo/poster_articulo.pdf y productos/posteres_articulos/pdf/*.pdf.
Uso (desde la raíz del proyecto): python herramientas/productos/preparar_dashboard.py
"""
import shutil
import sys
import zipfile
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
DESTINO = RAIZ / "dashboard" / "descargas"
COPIAS = {"articulo/articulo.pdf": "Aliaga_Damian_articulo_FPF_Peru.pdf",
          "articulo_typst/articulo.pdf": "Aliaga_Damian_articulo_FPF_Peru_typst.pdf",
          "productos/beamer/beamer.pdf": "Aliaga_Damian_beamer.pdf",
          "productos/beamer/beamer_impresion.pdf": "Aliaga_Damian_beamer_para_imprimir.pdf",
          "productos/poster_articulo/poster_articulo.pdf": "Aliaga_Damian_poster_articulo.pdf"}


def main() -> int:
    DESTINO.mkdir(parents=True, exist_ok=True)
    faltan = []
    for origen, nombre in COPIAS.items():
        ruta = RAIZ / origen
        if ruta.exists():
            shutil.copy2(ruta, DESTINO / nombre)
            print(f"OK {nombre}")
        else:
            faltan.append(origen)
    posteres = sorted((RAIZ / "productos" / "posteres_articulos" / "pdf").glob("poster_*.pdf"))
    with zipfile.ZipFile(DESTINO / "Aliaga_Damian_posteres_20_articulos.zip", "w", zipfile.ZIP_DEFLATED) as z:
        for p in posteres:
            z.write(p, p.name)
    print(f"OK Aliaga_Damian_posteres_20_articulos.zip ({len(posteres)} pósteres)")
    if faltan:
        print("FALTAN (compílalos antes):", ", ".join(faltan))
    return 1 if faltan or len(posteres) != 20 else 0


if __name__ == "__main__":
    sys.exit(main())
