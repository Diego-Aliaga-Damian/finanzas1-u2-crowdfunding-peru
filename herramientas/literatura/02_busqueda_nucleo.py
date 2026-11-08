# Diego Sebastián Aliaga Damián
# 2024200481M
# Tema 96: Fintech y financiamiento participativo (crowdfunding) en el Perú: oferta y condiciones
# Fecha de búsqueda: 2026-11-07
"""Segunda pasada: misma búsqueda restringida a revistas del núcleo científico (OpenAlex is_core)
y métricas de cada revista (h-index, citación media a 2 años) como criterio de priorización.
El cuartil SJR/JCR NO se obtiene aquí: se verifica manualmente (Scimago restringe el acceso automatizado).
Uso:  python 02_busqueda_nucleo.py <carpeta_salida>
"""
import csv
import json
import sys
import time
from pathlib import Path

import requests

ANIO_INICIO, ANIO_FIN = 2022, 2026
POR_CONSULTA = 25
UA = {"User-Agent": "UNCP-Finanzas1-Investigacion/0.1 (busqueda bibliografica academica)"}
CONSULTAS = [
    ("a", "peer-to-peer lending banks"),
    ("a", "marketplace lending"),
    ("a", "fintech lending bank competition"),
    ("b", "fintech small business lending"),
    ("b", "crowdfunding small business finance"),
    ("b", "debt crowdfunding"),
    ("c", "fintech Latin America"),
    ("c", "fintech credit emerging markets"),
    ("d", "crowdfunding regulation"),
    ("e", "peer-to-peer lending interest rate"),
    ("e", "crowdfunding platform"),
    ("e", "real estate crowdfunding"),
]

def get(url, params):
    r = requests.get(url, params=params, headers=UA, timeout=60)
    if r.status_code != 200:
        print("  ERROR", r.status_code, r.text[:300])
    r.raise_for_status()
    time.sleep(1.2)
    return r.json()

def main(salida: Path) -> None:
    salida.mkdir(parents=True, exist_ok=True)
    cand, fuentes_ids = {}, set()
    for linea, q in CONSULTAS:
        filtro = f"publication_year:{ANIO_INICIO}-{ANIO_FIN},type:article,language:en,primary_location.source.is_core:true"
        d = get("https://api.openalex.org/works", {"search": q, "filter": filtro, "per_page": POR_CONSULTA})
        (salida / f"nucleo_{linea}_{q.replace(' ', '_')}.json").write_text(json.dumps(d, ensure_ascii=False), encoding="utf-8")
        print(f"[{linea}] {q!r}: total={d['meta']['count']}")
        for w in d["results"]:
            doi = (w.get("doi") or "").replace("https://doi.org/", "").lower()
            src = (w.get("primary_location") or {}).get("source") or {}
            if not doi or not src.get("id"):
                continue
            fuentes_ids.add(src["id"].split("/")[-1])
            c = cand.setdefault(doi, {"doi": doi, "anio": w.get("publication_year"), "titulo": w.get("title"),
                                      "revista": src.get("display_name"), "fuente_id": src["id"].split("/")[-1],
                                      "citas": w.get("cited_by_count"), "oa": (w.get("open_access") or {}).get("oa_status"),
                                      "oa_url": (w.get("open_access") or {}).get("oa_url"),
                                      "primer_autor": (w.get("authorships") or [{}])[0].get("author", {}).get("display_name"),
                                      "openalex_id": w["id"].split("/")[-1], "lineas": set(), "rel": 0.0})
            c["lineas"].add(linea); c["rel"] = max(c["rel"], w.get("relevance_score") or 0)

    # Métricas de revistas (lotes de 50 ids)
    met, ids = {}, sorted(fuentes_ids)
    for k in range(0, len(ids), 50):
        d = get("https://api.openalex.org/sources", {"filter": "openalex_id:" + "|".join(ids[k:k+50]), "per_page": 50})
        for s in d["results"]:
            st = s.get("summary_stats") or {}
            met[s["id"].split("/")[-1]] = {"issn_l": s.get("issn_l"), "issn": ";".join(s.get("issn") or []),
                                           "h": st.get("h_index"), "c2": round(st.get("2yr_mean_citedness") or 0, 2),
                                           "editorial": s.get("host_organization_name")}
    filas = []
    for c in cand.values():
        filas.append({**c, **met.get(c["fuente_id"], {}), "lineas": ",".join(sorted(c["lineas"]))})
    filas.sort(key=lambda x: (x["lineas"], -x["rel"]))
    with open(salida / "candidatos_nucleo.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(filas[0].keys())); w.writeheader(); w.writerows(filas)
    print(f"\nCandidatos únicos: {len(filas)} | revistas: {len(met)}")
    for x in filas:
        print(f"{x['lineas']:5}|{x['anio']}|c={x['citas']:>4}|h={x.get('h') or 0:>3}|c2={x.get('c2') or 0:>5}|"
              f"{(x['revista'] or '')[:30]:30}|{(x['titulo'] or '')[:78]}|{x['doi']}")

if __name__ == "__main__":
    main(Path(sys.argv[1]))
