# Diego Sebastián Aliaga Damián
# 2024200481M
# Tema 96: Fintech y financiamiento participativo (crowdfunding) en el Perú: oferta y condiciones
# Fecha de búsqueda: 2026-11-07
"""Búsqueda bibliográfica reproducible en OpenAlex (herramienta complementaria, no forma parte de /codigo).

Guarda las respuestas crudas (JSON) y una tabla de candidatos deduplicada por DOI.
Uso:  python 01_buscar_openalex.py <carpeta_salida>
"""
import csv
import json
import sys
import time
from pathlib import Path

import requests

# --- Parámetros congelados de la búsqueda (protocolo) ---
ANIO_INICIO, ANIO_FIN = 2022, 2026          # 2022 se marca aparte por si el docente fija la ventana 2023-2026
POR_CONSULTA = 15
UA = {"User-Agent": "UNCP-Finanzas1-Investigacion/0.1 (busqueda bibliografica academica)"}
CONSULTAS = [
    ("a", "peer-to-peer lending banks substitutes complements", True),
    ("a", "marketplace lending bank competition borrowers", True),
    ("b", "fintech lending small business credit access", True),
    ("b", "crowdfunding small and medium enterprises financing", True),
    ("c", "fintech credit emerging markets Latin America", True),
    ("d", "crowdfunding regulation investor protection", True),
    ("e", "peer-to-peer lending interest rates default risk", True),
    ("e", "lending-based crowdfunding loan pricing", True),
    ("e", "real estate crowdfunding", True),
    ("f", "crowdfunding Peru", False),
    ("f", "fintech Peru", False),
]

def buscar(consulta: str, solo_ingles: bool) -> dict:
    """Consulta la API de OpenAlex con filtros de año, tipo e idioma."""
    filtros = [f"publication_year:{ANIO_INICIO}-{ANIO_FIN}", "type:article"]
    if solo_ingles:
        filtros.append("language:en")
    r = requests.get("https://api.openalex.org/works",
                     params={"search": consulta, "filter": ",".join(filtros), "per_page": POR_CONSULTA},
                     headers=UA, timeout=60)
    r.raise_for_status()
    return r.json()

def main(salida: Path) -> None:
    salida.mkdir(parents=True, exist_ok=True)
    candidatos = {}
    for linea, consulta, ingles in CONSULTAS:
        datos = buscar(consulta, ingles)
        (salida / f"openalex_{linea}_{consulta[:30].replace(' ', '_')}.json").write_text(
            json.dumps(datos, ensure_ascii=False), encoding="utf-8")
        print(f"[{linea}] {consulta!r}: total={datos['meta']['count']} recibidos={len(datos['results'])}")
        for w in datos["results"]:
            doi = (w.get("doi") or "").replace("https://doi.org/", "").lower()
            if not doi:
                continue
            fuente = ((w.get("primary_location") or {}).get("source") or {})
            autores = [a["author"]["display_name"] for a in w.get("authorships", [])]
            reg = candidatos.setdefault(doi, {
                "doi": doi, "titulo": w.get("title"), "anio": w.get("publication_year"),
                "revista": fuente.get("display_name"), "issn_l": fuente.get("issn_l"),
                "tipo_fuente": fuente.get("type"), "autores": "; ".join(autores[:6]),
                "n_autores": len(autores), "citas": w.get("cited_by_count"),
                "oa": (w.get("open_access") or {}).get("oa_status"),
                "oa_url": (w.get("open_access") or {}).get("oa_url"),
                "idioma": w.get("language"), "lineas": set(), "relevancia_max": 0.0,
                "openalex_id": w.get("id"),
            })
            reg["lineas"].add(linea)
            reg["relevancia_max"] = max(reg["relevancia_max"], w.get("relevance_score") or 0)
        time.sleep(1.2)

    filas = sorted(candidatos.values(), key=lambda x: (-x["relevancia_max"]))
    with open(salida / "candidatos_openalex.csv", "w", newline="", encoding="utf-8") as f:
        wr = csv.DictWriter(f, fieldnames=list(filas[0].keys()))
        wr.writeheader()
        for x in filas:
            wr.writerow({**x, "lineas": ",".join(sorted(x["lineas"]))})
    print(f"\nCandidatos únicos con DOI: {len(filas)}")
    for x in filas:
        print(f"{x['anio']} | {','.join(sorted(x['lineas']))} | c={x['citas']:>4} | {x['oa'] or '-':7} | "
              f"{(x['revista'] or '-')[:38]:38} | {(x['titulo'] or '')[:85]} | {x['doi']}")

if __name__ == "__main__":
    main(Path(sys.argv[1]))
