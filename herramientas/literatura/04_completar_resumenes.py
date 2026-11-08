# Diego Sebastián Aliaga Damián
# 2024200481M
# Tema 96: Fintech y financiamiento participativo (crowdfunding) en el Perú: oferta y condiciones
# Fecha de consulta: 2026-11-07
"""Completa resúmenes ausentes (Semantic Scholar) y el estado de acceso abierto (OpenAlex)
para los artículos verificados en Crossref. Uso: python 04_completar_resumenes.py <carpeta_crudos>"""
import csv
import json
import sys
import time
from pathlib import Path

import requests

UA = {"User-Agent": "UNCP-Finanzas1-Investigacion/0.1 (verificacion bibliografica academica)"}

def main(carpeta: Path) -> None:
    filas = list(csv.DictReader(open(carpeta / "verificacion_crossref.csv", encoding="utf-8")))
    for f in filas:
        # Estado de acceso abierto según OpenAlex
        r = requests.get(f"https://api.openalex.org/works/doi:{f['doi']}", headers=UA, timeout=60)
        oa = r.json().get("open_access", {}) if r.ok else {}
        f["oa_estado"], f["oa_url"] = oa.get("oa_status"), oa.get("oa_url")
        time.sleep(1.0)
        f["fuente_resumen"] = "OpenAlex" if f["resumen"] else ""
        if not f["resumen"]:
            r = requests.get(f"https://api.semanticscholar.org/graph/v1/paper/DOI:{f['doi']}",
                             params={"fields": "abstract,tldr"}, headers=UA, timeout=60)
            if r.ok:
                j = r.json()
                txt = j.get("abstract") or ((j.get("tldr") or {}).get("text"))
                if txt:
                    f["resumen"] = txt
                    f["fuente_resumen"] = "SemanticScholar" + ("" if j.get("abstract") else "-TLDR")
            print(f"  S2 {f['doi']}: HTTP {r.status_code} -> {f['fuente_resumen'] or 'sin resumen'}")
            time.sleep(3.0)
    with open(carpeta / "verificacion_completa.csv", "w", newline="", encoding="utf-8") as fo:
        w = csv.DictWriter(fo, fieldnames=list(filas[0].keys())); w.writeheader(); w.writerows(filas)
    for f in filas:
        if f["fuente_resumen"].startswith("Semantic"):
            print(f"\n{f['doi']} [{f['fuente_resumen']}]\n  {f['resumen'][:600]}")
    print("\nAcceso abierto:", {k: sum(1 for f in filas if f['oa_estado'] == k) for k in {f['oa_estado'] for f in filas}})

if __name__ == "__main__":
    main(Path(sys.argv[1]))
