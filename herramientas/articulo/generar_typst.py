# Diego Sebastián Aliaga Damián
# 2024200481M
# Tema 96: Fintech y financiamiento participativo (crowdfunding) en el Perú: oferta y condiciones
# Fecha: 2026-11-13
"""Genera la versión Typst del artículo a partir de las mismas fuentes que la versión LaTeX.

Produce en articulo_typst/:
    generado/cifras.typ        las mismas cifras que articulo/generado/cifras.tex (#cifra("clave"))
    generado/tablas.typ        T1-T8 de salidas/tablas/*.tex convertidas a tablas de Typst
    generado/anexo.typ         repositorio, endpoints y diccionario de variables
    generado/referencias.bib   articulo/referencias.bib sin comandos de LaTeX (Typst no los interpreta)
    secciones/*.typ            traducción automática de articulo/secciones/*.tex
La plantilla APA 7 está en articulo_typst/articulo.typ (no se genera). Para compilar:
    python herramientas/articulo/generar_typst.py
    typst compile articulo_typst/articulo.typ --root .
Si se edita una sección en LaTeX, basta con volver a ejecutar este script.
"""
from __future__ import annotations

import importlib.util
import re
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
DESTINO = RAIZ / "articulo_typst"
GENERADO = DESTINO / "generado"
sys.path.insert(0, str(RAIZ / "codigo"))


def cargar(ruta: Path, nombre: str):
    spec = importlib.util.spec_from_file_location(nombre, ruta)
    modulo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modulo)
    return modulo


LATEX = cargar(RAIZ / "herramientas" / "articulo" / "generar_insumos_articulo.py", "insumos_latex")


# ----------------------------------------------------------------------------- utilidades
def texto_plano(s: str) -> str:
    """Quita el escapado de LaTeX de un texto corto (celdas y cifras)."""
    for a, b in ((r"\textbackslash{}", "\\"), (r"\,", "\u2009"), (r"\%", "%"), (r"\_", "_"), (r"\&", "&"),
                 (r"\#", "#"), (r"\$", "$"), (r"\{", "{"), (r"\}", "}"), ("~", "\u00a0")):
        s = s.replace(a, b)
    return s.strip()


def cadena(s: str) -> str:
    """Literal de cadena de Typst."""
    return '"' + s.replace("\\", "\\\\").replace('"', '\\"') + '"'


def escribir(ruta: Path, texto: str) -> None:
    ruta.parent.mkdir(parents=True, exist_ok=True)
    ruta.write_text(texto, encoding="utf-8", newline="\n")
    print(f"generado: {ruta.relative_to(RAIZ).as_posix()}")


# ----------------------------------------------------------------------------- cifras
def cifras_typ() -> str:
    c = LATEX.cifras()
    lineas = ["// Generado por herramientas/articulo/generar_typst.py; no editar a mano.",
              "#let cifras = ("]
    lineas += [f"  {cadena(k)}: {cadena(texto_plano(v))}," for k, v in sorted(c.items())]
    lineas += [")", '#let cifra(clave) = cifras.at(clave, default: text(fill: red, weight: "bold")[??#clave??])']
    return "\n".join(lineas) + "\n"


# ----------------------------------------------------------------------------- tablas de 04
ALINEA = {"RaggedRight": "left", "RaggedLeft": "right", "Centering": "center"}


def tabla_desde_latex(ruta: Path) -> str:
    texto = ruta.read_text(encoding="utf-8")
    spec = re.findall(r"\\hsize=([\d.]+)\\hsize\\(RaggedRight|RaggedLeft|Centering)", texto)
    columnas = ", ".join(f"{float(p):.3f}fr" for p, _ in spec)
    alinea = ", ".join(ALINEA[a] for _, a in spec)
    filas = [l.strip()[:-2].strip() for l in texto.splitlines() if l.strip().endswith(r"\\")]
    celdas = [[texto_plano(c) for c in re.split(r"(?<!\\)&", f)] for f in filas]
    encabezado, cuerpo = celdas[0], celdas[1:]
    nombre = ruta.stem
    partes = [f"#let {nombre.replace('-', '_')} = table(",
              f"  columns: ({columnas}),", f"  align: ({alinea}),",
              "  stroke: none, inset: (x: 3pt, y: 2.6pt),",
              "  table.hline(stroke: 0.8pt),",
              "  table.header(" + ", ".join(cadena(c) for c in encabezado) + "),",
              "  table.hline(stroke: 0.5pt),"]
    partes += ["  " + ", ".join(cadena(c) for c in fila) + "," for fila in cuerpo]
    partes += ["  table.hline(stroke: 0.8pt),", ")"]
    return "\n".join(partes)


def tablas_typ() -> str:
    tablas = sorted((RAIZ / "salidas" / "tablas").glob("t*.tex"))
    return "// Generado por herramientas/articulo/generar_typst.py desde salidas/tablas/*.tex; no editar a mano.\n\n" + \
        "\n\n".join(tabla_desde_latex(t) for t in tablas) + "\n"


# ----------------------------------------------------------------------------- anexo
def tabla_simple(nombre: str, columnas: str, encabezado: list[str], filas: list[list[str]]) -> str:
    partes = [f"#let {nombre} = table(", f"  columns: ({columnas}),", "  align: left,",
              "  stroke: none, inset: (x: 3pt, y: 2.4pt),", "  table.hline(stroke: 0.8pt),",
              "  table.header(" + ", ".join(cadena(c) for c in encabezado) + "),", "  table.hline(stroke: 0.5pt),"]
    partes += ["  " + ", ".join(c if c.startswith(("raw(", "link(")) else cadena(c) for c in f) + "," for f in filas]
    partes += ["  table.hline(stroke: 0.8pt),", ")"]
    return "\n".join(partes)


def anexo_typ() -> str:
    import subprocess
    s01 = LATEX.cargar("01_extraccion_api.py")
    s02 = LATEX.cargar("02_scraping_web.py")
    try:
        commit = subprocess.run(["git", "rev-parse", "--short", "HEAD"], cwd=RAIZ, capture_output=True, text=True, check=True).stdout.strip()
    except (OSError, subprocess.CalledProcessError):
        commit = "sin git"
    log = (RAIZ / "log_ejecucion.txt").read_text(encoding="utf-8")
    fechas = sorted(set(re.findall(r"^(\d{4}-\d{2}-\d{2}) [\d:]+ \| \S+ \| INFO \| HTTP", log, re.M)))
    req = {l.split("==")[0]: l.split("==")[1] for l in (RAIZ / "requirements.txt").read_text(encoding="utf-8").splitlines() if "==" in l}
    versiones = ", ".join(f"{k} {req[k]}" for k in ("requests", "beautifulsoup4", "pandas", "numpy", "scipy", "matplotlib", "pandera", "pytest") if k in req)
    csv = LATEX.CSV_PROCESADO
    import pandas as pd
    panel = pd.read_csv(csv)
    h = LATEX.sha256_archivo(csv)
    repro = [["Repositorio", f'link({cadena(LATEX.REPOSITORIO)})'], ["Commit de referencia", f"raw({cadena(commit)})"],
             ["Periodo consultado", f"{s01.FECHA_INICIO} a {s01.FECHA_CORTE} (constantes FECHA_INICIO y FECHA_CORTE)"],
             ["Fechas de extracción", ", ".join(fechas) + " (según log_ejecucion.txt)"],
             ["Archivo procesado", f"datos_procesados/{csv.name}: {len(panel)} filas, {panel.shape[1]} columnas"],
             ["SHA-256 del archivo procesado", f"raw({cadena(h[:32] + ' ' + h[32:])})"],
             ["Orden de ejecución", "01_extraccion_api.py → 02_scraping_web.py → 03_limpieza_datos.py → 04_analisis.py"],
             ["Verificación", "python -m pytest y python codigo/auditoria.py (con --en-vivo para cotejar con las fuentes)"],
             ["Entorno", f"Python 3.14.7; {versiones}"]]
    endpoints = [["API", "BCRP, BCRPData", f"link({cadena(s01.URL_BCRP)})",
                  f"10 series mensuales; {s01.periodo_bcrp(s01.FECHA_INICIO)} a {s01.periodo_bcrp(s01.FECHA_CORTE)}"],
                 ["API", "SMV, OData PrincipalCuentaSMV", f"link({cadena(s01.URL_SMV)})", "sEjercicio=2021-2026; sPeriodo=1-4; sTipoInf=I (23 trimestres)"],
                 ["Scraping", "SMV, SIMV «Información de Proyectos»", f"link({cadena(s02.URL_SIMV)})",
                  f"POST ASP.NET por plataforma, año y mes; pausa de {s02.PAUSA_SIMV:.0f} s; 6 plataformas × 69 meses"]]
    dicc = []
    for f in (RAIZ / "diccionario_variables.md").read_text(encoding="utf-8").splitlines():
        if re.match(r"^\| \d+ \|", f):
            _, variable, definicion, unidad, frecuencia, fuente = [x.strip() for x in f.strip("|").split("|")][:6]
            corta = ("SIMV" if "SIMV" in fuente else "SMV-OData" if "OData" in fuente else
                     re.search(r"serie (PN\w+)", fuente).group(1) if "BCRP" in fuente else "Derivada")
            dicc.append([f"raw({cadena(variable.strip('`'))})", definicion.replace("`", ""), unidad, frecuencia, corta])
    partes = ["// Generado por herramientas/articulo/generar_typst.py; no editar a mano.",
              tabla_simple("anexo_reproducibilidad", "3.8fr, 11.3fr", ["Elemento", "Detalle"], repro),
              tabla_simple("anexo_endpoints", "1.6fr, 2.8fr, 5.8fr, 3.9fr", ["Vía", "Fuente", "Endpoint o URL", "Parámetros"], endpoints),
              tabla_simple("anexo_diccionario", "3.8fr, 5fr, 2.2fr, 1.7fr, 1.9fr",
                           ["Variable", "Definición", "Unidad", "Frecuencia", "Fuente"], dicc)]
    return "\n\n".join(partes) + "\n"


# ----------------------------------------------------------------------------- bibliografía
def bib_typ() -> str:
    texto = (RAIZ / "articulo" / "referencias.bib").read_text(encoding="utf-8")
    for a, b in ((r"N.\textsuperscript{o}", "N.º"), (r"{\&}", "&"), (r"\&", "&")):
        texto = texto.replace(a, b)
    # Typst (hayagriva) trata @dataset como software y como página web deja «(2026,)». Como libro el año sale bien;
    # la descripción y la fecha de consulta (numeral 2.4.8) se agregan al título entre corchetes.
    meses = LATEX.MESES

    def conjunto_de_datos(m: re.Match) -> str:
        bloque = m.group(0).replace("@dataset{", "@book{")
        fecha = re.search(r"urldate = \{(\d{4})-(\d{2})-(\d{2})\}", bloque)
        consulta = f"{int(fecha.group(3))} de {meses[int(fecha.group(2))]} de {fecha.group(1)}" if fecha else ""
        return re.sub(r"(title = \{.*)\},\n", lambda t: f"{t.group(1)} [conjunto de datos consultado el {consulta}]}},\n", bloque, count=1)

    return re.sub(r"@dataset\{.*?\n\}", conjunto_de_datos, texto, flags=re.S)


# ----------------------------------------------------------------------------- secciones LaTeX -> Typst
def argumento(s: str, i: int) -> tuple[str, int]:
    """Lee {…} balanceado desde s[i] == '{'; devuelve (contenido, índice tras la llave de cierre)."""
    assert s[i] == "{", s[i:i + 30]
    nivel, j = 0, i
    while True:
        if s[j] == "{" and s[j - 1] != "\\":
            nivel += 1
        elif s[j] == "}" and s[j - 1] != "\\":
            nivel -= 1
            if nivel == 0:
                return s[i + 1:j], j + 1
        j += 1


def opcional(s: str, i: int) -> tuple[str | None, int]:
    if i < len(s) and s[i] == "[":
        j = s.index("]", i)
        return s[i + 1:j], j + 1
    return None, i


MATEMATICA = [(r"\mathit{IHH}", ' "IHH"'), (r"\mathit{ROA}", ' "ROA"'), (r"\mathit{OR}", ' "OR"'), (r"_{\min}", "_min "),
              (r"\sum", " sum"), (r"\cdot", " dot "), (r"\big/", " slash "), (r"\min", " min "), (r"\,", " thin "),
              (r"_{it}", "_(i t)"), (r"\bar{A}", " overline(A) "), (r"\frac{4}{n}", " 4/n ")]


def matematica(m: str) -> str:
    m = re.sub(r"\\cifra\{(\w+)\}", lambda x: f' #cifra("{x.group(1)}") ', m)
    for a, b in MATEMATICA:
        m = m.replace(a, b)
    m = m.replace("=", " = ")
    return "$" + re.sub(r"\s+", " ", m).strip() + "$"


def convertir(s: str, tablas_usadas: set) -> str:
    """Traduce el subconjunto de LaTeX que usan las secciones del artículo."""
    s = re.sub(r"(?m)^\s*%.*$\n?", "", s)                # comentarios de línea completa
    s = re.sub(r"(?<!\\)%.*$", "", s, flags=re.M)        # comentarios al final de línea
    # Typst antepone «Tabla»/«Figura» a la referencia: «Tabla~\ref{x}» pasa a ser solo «@x»
    s = re.sub(r"(Tabla|Figura)~\\ref\{", r"\\ref{", s)
    salida, i = [], 0
    while i < len(s):
        c = s[i]
        if c == "$":
            j = s.index("$", i + 1)
            salida.append(matematica(s[i + 1:j]))
            i = j + 1
            continue
        if c == "~":
            salida.append("~")
            i += 1
            continue
        if c != "\\":
            salida.append(c)
            i += 1
            continue
        m = re.match(r"\\([A-Za-z]+)\*?", s[i:])
        if not m:  # símbolo escapado: \% \, \& \_ \\
            sig = s[i + 1]
            salida.append({"%": "%", ",": "\u2009", "&": "&", "_": "\\_", "#": "\\#", "\\": "\\\n"}.get(sig, sig))
            i += 2
            continue
        cmd, i = m.group(1), i + len(m.group(0))
        if cmd in ("section", "subsection", "subsubsection"):
            titulo, i = argumento(s, i)
            nivel = {"section": "=", "subsection": "==", "subsubsection": "==="}[cmd]
            salida.append(f"\n{nivel} {convertir(titulo, tablas_usadas).strip()}\n")
        elif cmd == "cifra":
            clave, i = argumento(s, i)
            salida.append(f'#cifra("{clave}")')
        elif cmd == "parencite":
            claves, i = argumento(s, i)
            salida.append(" ".join(f"@{k.strip()}" for k in claves.split(",")))
        elif cmd == "textcite":
            clave, i = argumento(s, i)
            salida.append(f'#cite(<{clave.strip()}>, form: "prose")')
        elif cmd in ("textit", "emph"):
            t, i = argumento(s, i)
            salida.append(f"_{convertir(t, tablas_usadas)}_")
        elif cmd == "textbf":
            t, i = argumento(s, i)
            salida.append(f"*{convertir(t, tablas_usadas)}*")
        elif cmd == "texttt":
            t, i = argumento(s, i)
            salida.append(f"`{texto_plano(t)}`")
        elif cmd == "textsuperscript":
            t, i = argumento(s, i)
            salida.append(f"#super[{t}]")
        elif cmd == "url":
            t, i = argumento(s, i)
            salida.append(f'#link("{t}")')
        elif cmd == "ref":
            t, i = argumento(s, i)
            salida.append(f"@{t.replace(':', '-')}")
        elif cmd in ("noindent", "FloatBarrier", "small", "footnotesize", "centering", "par", "medskip", "smallskip"):
            pass
        elif cmd == "clearpage":
            salida.append("\n#pagebreak()\n")
        elif cmd == "pendiente":
            _, i = argumento(s, i)
        elif cmd == "begin":
            entorno, i = argumento(s, i)
            fin = s.index(r"\end{" + entorno + "}", i)
            cuerpo, i = s[i:fin], fin + len(r"\end{" + entorno + "}")
            salida.append(entorno_typst(entorno, cuerpo, tablas_usadas))
        else:
            raise ValueError(f"comando sin traducción: \\{cmd} cerca de: {s[i - 20:i + 40]!r}")
    return "".join(salida)


def entorno_typst(entorno: str, cuerpo: str, tablas_usadas: set) -> str:
    if entorno in ("itemize", "enumerate"):
        marca = "-" if entorno == "itemize" else "+"
        items = [x.strip() for x in cuerpo.split(r"\item")[1:]]
        return "\n" + "\n".join(f"{marca} {convertir(x, tablas_usadas).strip()}" for x in items) + "\n"
    if entorno in ("table", "figure"):
        cuerpo = re.sub(r"^\[[^\]]*\]", "", cuerpo.lstrip())  # opción de ubicación [!htbp]
        titulo = etiqueta = nota = contenido = None
        k = cuerpo.index(r"\caption")
        titulo, _ = argumento(cuerpo, k + len(r"\caption"))
        if r"\label" in cuerpo:
            etiqueta, _ = argumento(cuerpo, cuerpo.index(r"\label") + len(r"\label"))
        if r"\notaapa" in cuerpo:
            nota, _ = argumento(cuerpo, cuerpo.index(r"\notaapa") + len(r"\notaapa"))
        if r"\input{\tablas/" in cuerpo:
            nombre = re.search(r"\\input\{\\tablas/(\w+)\.tex\}", cuerpo).group(1)
            tablas_usadas.add(nombre)
            contenido = nombre
        else:
            ancho, archivo = re.search(r"\\includegraphics\[width=([\d.]*)\\linewidth\]\{(\w+)\.pdf\}", cuerpo).groups()
            contenido = f'image("/salidas/figuras/{archivo}.png", width: {float(ancho or 1) * 100:.0f}%)'
        funcion = "tabla_apa" if entorno == "table" else "figura_apa"
        partes = [f"\n#{funcion}({contenido},", f"  titulo: [{convertir(titulo, tablas_usadas).strip()}],"]
        if nota:
            partes.append(f"  nota: [{convertir(nota, tablas_usadas).strip()}],")
        partes.append(")" + (f" <{etiqueta.replace(':', '-')}>" if etiqueta else "") + "\n")
        return "\n".join(partes)
    raise ValueError(f"entorno sin traducción: {entorno}")


def secciones() -> None:
    tablas_usadas: set = set()
    for f in sorted((RAIZ / "articulo" / "secciones").glob("0[0-8]_*.tex")):
        if f.stem == "00_portada":
            continue  # la portada se arma en la plantilla Typst
        texto = convertir(f.read_text(encoding="utf-8"), tablas_usadas)
        texto = re.sub(r"\n{3,}", "\n\n", texto).strip() + "\n"
        encabezado = (f"// Traducido automáticamente de articulo/secciones/{f.name} por herramientas/articulo/generar_typst.py.\n"
                      "// Para cambiar el texto, edita el .tex y vuelve a ejecutar el script (o edita aquí y deja de regenerar).\n"
                      '#import "../generado/cifras.typ": cifra\n#import "../generado/tablas.typ": *\n#import "../estilo.typ": *\n\n')
        escribir(DESTINO / "secciones" / f"{f.stem}.typ", encabezado + texto)


def main() -> int:
    LATEX.main()  # asegura que las cifras de LaTeX estén al día
    escribir(GENERADO / "cifras.typ", cifras_typ())
    escribir(GENERADO / "tablas.typ", tablas_typ())
    escribir(GENERADO / "anexo.typ", anexo_typ())
    escribir(GENERADO / "referencias.bib", bib_typ())
    secciones()
    return 0


if __name__ == "__main__":
    sys.exit(main())
