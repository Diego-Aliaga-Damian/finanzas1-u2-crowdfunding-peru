# Diego Sebastián Aliaga Damián
# 2024200481M
# Tema 96: Fintech y financiamiento participativo (crowdfunding) en el Perú: oferta y condiciones
# Fecha: 2026-11-12
"""Agrega a cada póster la ficha del estudio (ámbito y enfoque, según el resumen oficial) y la figura propia
que acompaña la sección «Relevancia para el financiamiento participativo en el Perú».

Figura: 1 = monto mensual por plataforma (F1), 2 = publicados, financiados y colocación (F2),
        3 = tasas del crédito tradicional (F3), 4 = ingresos de la plataforma líder sobre el monto (F4).
Uso (desde la raíz del proyecto): python herramientas/posteres/ficha_articulos.py
Es idempotente: si el archivo ya tiene la ficha, la reemplaza.
"""
import re
import sys
from pathlib import Path

CARPETA = Path(__file__).resolve().parents[2] / "productos" / "posteres_articulos" / "articulos"
FICHA = {  # clave: (ámbito, enfoque, figura)
    "alvarezfranco2026": ("15 países de América Latina y el Caribe (Global Findex 2021)", "Empírico: índice de inclusión y modelo probit", 2),
    "beaumont2026": ("Francia (datos administrativos)", "Empírico: emparejamiento por puntaje de propensión e instrumento \\textit{shift-share}", 2),
    "bennaceur2026": ("57 países, más de 10\\,000 instituciones financieras", "Empírico", 3),
    "braggion2025": ("Plataforma de crowdfunding de deuda en línea", "Modelo estructural estimado con datos nuevos", 4),
    "chu2024": ("Teórico", "Modelo de competencia (resultados analíticos y numéricos)", 2),
    "danisewicz2023": ("Estados Unidos (Connecticut y Nueva York)", "Experimento natural: fallo judicial sobre préstamos por encima de la usura", 2),
    "eid2024": ("Préstamos entre pares en distintas regiones", "Empírico: variables instrumentales", 1),
    "fareed2025": ("Países en desarrollo", "Empírico, con técnicas para tratar la endogeneidad", 2),
    "fasano2026": ("Italia (plataforma de préstamos inmobiliarios)", "Aprendizaje automático (\\textit{Gradient Boosting} y SHAP)", 1),
    "hau2024": ("China (vendedores de la plataforma de Alibaba)", "Empírico: regresión discontinua", 2),
    "kim2026": ("Estados Unidos (LendingClub, 2009-2017)", "Modelo teórico y entrada escalonada de la plataforma", 3),
    "larioshernandez2025": ("América Latina", "Cualitativo exploratorio (método de Gioia invertido)", 1),
    "lazos2025": ("Reino Unido (crowdfunding de capital)", "Empírico: efecto de un tope de inversión", 1),
    "ma2023": ("China (plataforma de préstamos en línea)", "Empírico con datos detallados de prestatarios", 3),
    "miglo2025": ("Teórico", "Modelo de información asimétrica (crowdfunding de recompensa)", 1),
    "onorato2024": ("Italia, 2021 (fintech de crédito y bancos)", "Análisis envolvente de datos estocástico (SDEA)", 4),
    "pampurini2024": ("Italia, 2020-2022 (fintech de crédito)", "Análisis envolvente de datos estocástico (SDEA)", 4),
    "ran2025": ("Muestra global de países", "Empírico: diferencias en diferencias", 1),
    "serfes2025": ("Teórico", "Modelo de competencia con evaluación crediticia y garantías", 3),
    "vives2025": ("Teórico", "Modelo espacial de competencia entre bancos y fintech", 1),
}
INICIO, FIN = "% --- Ficha del estudio (herramientas/posteres/ficha_articulos.py) ---", "% --- fin de la ficha ---"


def main() -> int:
    faltan = []
    for archivo in sorted(CARPETA.glob("*.tex")):
        clave = archivo.stem
        if clave not in FICHA:
            faltan.append(clave)
            continue
        ambito, enfoque, figura = FICHA[clave]
        bloque = f"{INICIO}\n\\def\\Ambito{{{ambito}}}\n\\def\\Enfoque{{{enfoque}}}\n\\def\\FiguraPeru{{{figura}}}\n{FIN}\n"
        texto = archivo.read_text(encoding="utf-8")
        texto = re.sub(re.escape(INICIO) + r".*?" + re.escape(FIN) + r"\n", "", texto, flags=re.S)
        archivo.write_text(texto.rstrip("\n") + "\n" + bloque, encoding="utf-8", newline="\n")
    print(f"fichas escritas: {len(FICHA) - len(faltan)}; sin ficha: {faltan or 'ninguno'}")
    return 1 if faltan else 0


if __name__ == "__main__":
    sys.exit(main())
