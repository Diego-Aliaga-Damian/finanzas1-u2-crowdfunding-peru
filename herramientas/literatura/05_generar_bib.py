# Diego Sebastián Aliaga Damián
# 2024200481M
# Tema 96: Fintech y financiamiento participativo (crowdfunding) en el Perú: oferta y condiciones
# Fecha de consulta: 2026-11-11
"""Genera articulo/referencias.bib desde Crossref (BibTeX por DOI) + articulo/referencias_manuales.bib.

Ninguna referencia académica se teclea a mano: se descarga el registro BibTeX que publica Crossref para cada DOI
verificado en la Fase II-B, y solo se normaliza (clave, idioma, entidades HTML, nombres propios protegidos para
que biblatex-apa aplique el tipo oración sin alterar siglas ni gentilicios).
Uso (desde la raíz del proyecto):  python herramientas/literatura/05_generar_bib.py
"""
import re
import sys
import time
import unicodedata
from pathlib import Path

import requests

RAIZ = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(RAIZ / "codigo"))
from comun import user_agent  # noqa: E402

DOIS = {  # núcleo del estado del arte (2023-2026) + contexto peruano
    "nucleo": ["10.1016/j.jfineco.2025.104113", "10.1016/j.jbvi.2024.e00508", "10.1016/j.jeconbus.2026.106307",
               "10.1016/j.jbankfin.2024.107338", "10.1017/s0022109023000698", "10.1016/j.jfineco.2025.104040",
               "10.1016/j.bar.2024.101448", "10.1093/rfs/hhaf080", "10.1111/jifm.12242", "10.1016/j.ribaf.2023.102185",
               "10.1016/j.frl.2024.105519", "10.1016/j.jeconbus.2026.106343", "10.1287/mnsc.2023.01538",
               "10.1016/j.techfore.2025.124119", "10.1016/j.jbankfin.2023.106986", "10.1016/j.frl.2024.106642",
               "10.1080/08276331.2024.2389505", "10.1108/jefas-09-2024-0280", "10.1108/jes-03-2024-0194",
               "10.1016/j.gfj.2023.100884"],
    "peru": ["10.18601/16923960.v25n2.09", "10.18178/ijtef.2023.14.4.759"],
}
IDIOMA = {"10.18601/16923960.v25n2.09": "spanish"}
# Apellidos compuestos que Crossref parte mal (verificado en la ficha del FMI del documento de trabajo previo:
# "Sami Ben Naceur"). Las llaves evitan que biblatex tome "Ben" como nombre de pila.
AUTOR_CORREGIDO = {"10.1111/jifm.12242": ("Naceur, Sami Ben", "{Ben Naceur}, Sami")}
PROTEGER = ["Latin America", "Caribbean", "Peruvian", "Peru", "FinTech", "FinTechs", "Fintech", "P2P", "U.S.", "Italian",
            "LendingClub", "SMEs", "ESG", "UK", "EU"]
SALIDA = RAIZ / "articulo" / "referencias.bib"
MANUALES = RAIZ / "articulo" / "referencias_manuales.bib"


def clave(bib: str, usadas: set) -> str:
    autor = re.search(r"author\s*=\s*\{([^,}]+)", bib)
    anio = re.search(r"year\s*=\s*\{?(\d{4})", bib)
    base = unicodedata.normalize("NFKD", autor.group(1) if autor else "anon").encode("ascii", "ignore").decode()
    base = re.sub(r"[^a-z]", "", base.lower()) + (anio.group(1) if anio else "")
    k, letra = base, "a"
    while k in usadas:
        k, letra = base + letra, chr(ord(letra) + 1)
    usadas.add(k)
    return k


def corregir_autor_y_anio(bib: str, anio_final: int | None) -> str:
    """Quita autores vacíos que Crossref deja al inicio y fija el año de la versión final (APA 7)."""
    bib = re.sub(r"(author\s*=\s*\{)\s*and\s+", r"\1", bib)
    if anio_final:
        bib = re.sub(r"year\s*=\s*\{?\d{4}\}?", f"year ={{{anio_final}}}", bib)
    return re.sub(r",\s*month\s*=\s*[^,\n]+", "", bib)


def anio_version_final(sesion, doi: str) -> int | None:
    """Año de la versión impresa (published-print); si no existe, el de la versión en línea."""
    r = sesion.get(f"https://api.crossref.org/works/{doi}", timeout=60)
    time.sleep(1.0)
    m = r.json()["message"] if r.ok else {}
    for campo in ("published-print", "published-online", "issued"):
        partes = (m.get(campo) or {}).get("date-parts", [[None]])[0]
        if partes and partes[0]:
            return int(partes[0])
    return None


def limpiar(bib: str, doi: str, k: str) -> str:
    bib = re.sub(r"^@(\w+)\{[^,]+,", lambda m: f"@{m.group(1).lower()}{{{k},", bib.strip(), count=1)
    bib = bib.replace("&amp;", "\\&").replace("{\\&}amp;", "\\&")
    titulo = re.search(r"title\s*=\s*\{(.+?)\},\s*\w+\s*=", bib, re.S)
    if titulo:
        t = titulo.group(1)
        for palabra in sorted(PROTEGER, key=len, reverse=True):
            t = re.sub(rf"(?<![{{\w]){re.escape(palabra)}(?![\w}}])", "{" + palabra + "}", t)
        bib = bib.replace(titulo.group(1), t, 1)
    bib = re.sub(r",\s*url\s*=\s*\{[^}]*\}", "", bib)  # biblatex-apa construye el enlace desde el DOI
    # Crossref registra a veces al editor de la revista; en APA 7 un artículo de revista no lleva editor
    bib = re.sub(r",\s*editor\s*=\s*\{[^}]*\}", "", bib)
    bib = bib.rstrip("}").rstrip().rstrip(",") + f",\n  langid = {{{IDIOMA.get(doi, 'english')}}}\n}}"
    return re.sub(r",\s+(\w+)\s*=", r",\n  \1 =", bib)


def main() -> int:
    sesion = requests.Session()
    sesion.headers.update({"User-Agent": user_agent()})
    entradas, usadas = [], set()
    for grupo, dois in DOIS.items():
        for doi in dois:
            r = sesion.get(f"https://api.crossref.org/works/{doi}/transform/application/x-bibtex", timeout=60)
            time.sleep(1.0)
            if r.status_code != 200 or not r.text.lstrip().startswith("@"):
                print(f"ERROR {r.status_code} {doi}")
                return 1
            texto = corregir_autor_y_anio(r.text, anio_version_final(sesion, doi))
            if doi in AUTOR_CORREGIDO:
                texto = texto.replace(*AUTOR_CORREGIDO[doi])
            k = clave(texto, usadas)
            entradas.append(f"% {grupo} · doi:{doi}\n" + limpiar(texto, doi, k))
            print(f"OK {k:22s} {doi}")
    manual = MANUALES.read_text(encoding="utf-8") if MANUALES.exists() else ""
    encabezado = ("% Generado por herramientas/literatura/05_generar_bib.py desde Crossref; no editar a mano.\n"
                  "% Las entradas manuales (normas y fuentes de datos) están en referencias_manuales.bib.\n\n")
    SALIDA.write_text(encabezado + "\n\n".join(entradas) + "\n\n" + manual, encoding="utf-8", newline="\n")
    print(f"\n{len(entradas)} entradas de Crossref + entradas manuales -> {SALIDA.relative_to(RAIZ).as_posix()}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
