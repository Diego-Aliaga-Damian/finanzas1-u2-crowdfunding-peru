# Diego Sebastián Aliaga Damián
# 2024200481M
# Tema 96: Fintech y financiamiento participativo (crowdfunding) en el Perú: oferta y condiciones
# Fecha de verificación: 2026-11-07
"""Verifica cada DOI preseleccionado contra Crossref (fuente de registro del DOI) y recupera el resumen
desde OpenAlex para evaluar pertinencia. Marca discrepancias de título o año entre ambas fuentes.
Uso:  python 03_verificar_crossref.py <carpeta_salida>
"""
import csv
import json
import re
import sys
import time
from difflib import SequenceMatcher
from pathlib import Path

import requests

UA = {"User-Agent": "UNCP-Finanzas1-Investigacion/0.1 (verificacion bibliografica academica)"}
PRESELECCION = [  # (línea temática, DOI) — elegidos por título entre los candidatos de OpenAlex
    ("a", "10.1016/j.jbankfin.2024.107124"), ("a", "10.1016/j.jbankfin.2024.107338"),
    ("a", "10.1017/s0022109023000698"), ("a", "10.1016/j.jfineco.2025.104040"),
    ("a", "10.1016/j.jbankfin.2023.106986"), ("a", "10.1016/j.gfj.2023.100884"),
    ("a", "10.1016/j.bar.2024.101448"), ("a", "10.1016/j.chieco.2023.101944"),
    ("a", "10.1016/j.jfi.2024.101101"), ("a", "10.1002/sej.1470"),
    ("a", "10.1111/jofi.70003"), ("a", "10.1016/j.ribaf.2023.102185"),
    ("a", "10.1016/j.frl.2024.105519"), ("a", "10.1016/j.irfa.2022.102116"),
    ("a", "10.1111/jifm.12242"),
    ("b", "10.1016/j.jfineco.2025.104113"), ("b", "10.1016/j.jfs.2024.101290"),
    ("b", "10.1016/j.jfs.2026.101541"), ("b", "10.1016/j.bar.2025.101583"),
    ("b", "10.1016/j.jbvi.2024.e00508"), ("b", "10.1016/j.intfin.2023.101882"),
    ("b", "10.1080/00036846.2023.2200230"), ("b", "10.1093/rfs/hhaf080"),
    ("b", "10.1007/s11187-022-00622-9"), ("b", "10.1016/j.frl.2024.106642"),
    ("b", "10.1016/j.resglo.2024.100238"), ("b", "10.1108/jes-03-2024-0194"),
    ("b", "10.1111/jofi.13384"), ("b", "10.1287/mnsc.2023.01538"),
    ("b", "10.1016/j.jik.2022.100278"),
    ("c", "10.1080/08276331.2024.2389505"), ("c", "10.1108/jefas-09-2024-0280"),
    ("c", "10.1108/ijoem-04-2024-0678"), ("c", "10.1016/j.latcb.2022.100061"),
    ("c", "10.3390/jrfm15020062"), ("c", "10.1007/s43621-025-01597-9"),
    ("d", "10.1016/j.techfore.2025.124119"), ("d", "10.54648/cola2025039"),
    ("d", "10.1016/j.irfa.2026.105101"), ("d", "10.1287/isre.2022.1154"),
    ("e", "10.1016/j.jeconbus.2026.106343"), ("e", "10.1016/j.jeconbus.2026.106307"),
    ("f", "10.15381/quipu.v30i63.24043"), ("f", "10.18601/16923960.v25n2.09"),
    ("f", "10.18178/ijtef.2023.14.4.759"),
]

def resumen_openalex(doi: str):
    r = requests.get(f"https://api.openalex.org/works/doi:{doi}", headers=UA, timeout=60)
    if r.status_code != 200:
        return None, None
    w = r.json()
    inv = w.get("abstract_inverted_index") or {}
    pos = sorted((p, t) for t, ps in inv.items() for p in ps)
    return w.get("title"), " ".join(t for _, t in pos)

def main(salida: Path) -> None:
    salida.mkdir(parents=True, exist_ok=True)
    filas, crudos = [], {}
    for linea, doi in PRESELECCION:
        r = requests.get(f"https://api.crossref.org/works/{doi}", headers=UA, timeout=60)
        time.sleep(1.0)
        t_oa, abstract = resumen_openalex(doi)
        time.sleep(1.0)
        if r.status_code != 200:
            filas.append({"linea": linea, "doi": doi, "crossref_http": r.status_code, "estado": "DOI NO RESUELVE EN CROSSREF"})
            print(f"[{linea}] {doi}: Crossref HTTP {r.status_code}")
            continue
        m = r.json()["message"]
        crudos[doi] = m
        titulo = re.sub(r"<[^>]+>", "", (m.get("title") or [""])[0])
        anio = (m.get("published-print") or m.get("published-online") or m.get("issued") or {}).get("date-parts", [[None]])[0][0]
        autores = [f"{a.get('family','')}, {a.get('given','')}".strip(", ") for a in m.get("author", [])]
        sim = SequenceMatcher(None, titulo.lower(), (t_oa or "").lower()).ratio()
        fila = {
            "linea": linea, "doi": doi, "crossref_http": 200, "tipo": m.get("type"),
            "anio_crossref": anio, "revista": (m.get("container-title") or [""])[0],
            "issn": ";".join(m.get("ISSN") or []), "volumen": m.get("volume"), "numero": m.get("issue"),
            "paginas": m.get("page") or m.get("article-number"), "autores": " | ".join(autores),
            "n_autores": len(autores), "titulo": titulo, "similitud_titulo_openalex": round(sim, 2),
            "editorial": m.get("publisher"), "resumen": abstract or "",
        }
        fila["estado"] = "OK" if sim >= 0.85 else "REVISAR TÍTULO"
        filas.append(fila)
        print(f"[{linea}] {anio} | {fila['estado']} | {fila['revista'][:40]} | {autores[0] if autores else '-'} (+{len(autores)-1}) "
              f"| {titulo[:90]}\n      ISSN {fila['issn']} | tipo={fila['tipo']}\n      RESUMEN: {(abstract or 'SIN RESUMEN')[:420]}")
    (salida / "crossref_crudos.json").write_text(json.dumps(crudos, ensure_ascii=False), encoding="utf-8")
    campos = sorted({k for f in filas for k in f}, key=lambda k: list(filas[0].keys()).index(k) if k in filas[0] else 99)
    with open(salida / "verificacion_crossref.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=campos); w.writeheader(); w.writerows(filas)
    print("\nVerificados:", sum(1 for f in filas if f.get("estado") == "OK"), "de", len(filas))

if __name__ == "__main__":
    main(Path(sys.argv[1]))
