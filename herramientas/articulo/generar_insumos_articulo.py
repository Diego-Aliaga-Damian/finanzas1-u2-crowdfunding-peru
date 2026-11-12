# Diego Sebastián Aliaga Damián
# 2024200481M
# Tema 96: Fintech y financiamiento participativo (crowdfunding) en el Perú: oferta y condiciones
# Fecha de extracción: 2026-11-07 (censo) y 2026-11-08 (reanudación)
"""Genera los insumos del artículo LaTeX a partir de archivos del proyecto (nada se transcribe a mano).

Salidas en articulo/generado/:
    cifras.tex                macros \\cifra{clave} con las cifras citadas en el texto (de salidas/resultados_04.json,
                              datos_procesados y log_ejecucion.txt)
    anexo_endpoints.tex       fuentes, endpoints y parámetros (constantes de los scripts 01 y 02)
    anexo_diccionario.tex     diccionario de variables (de diccionario_variables.md)
    anexo_reproducibilidad.tex  repositorio, commit, fechas, SHA-256 y versiones

Uso (desde la raíz del proyecto):  python herramientas/articulo/generar_insumos_articulo.py
"""
from __future__ import annotations

import importlib.util
import json
import re
import subprocess
import sys
from pathlib import Path

import pandas as pd

RAIZ = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(RAIZ / "codigo"))
from comun import CODIGO_MATRICULA, PROCESADOS, SALIDAS, sha256_archivo  # noqa: E402

DESTINO = RAIZ / "articulo" / "generado"
CSV_PROCESADO = PROCESADOS / f"datos_procesados_{CODIGO_MATRICULA}.csv"
REPOSITORIO = "https://github.com/Diego-Aliaga-Damian/finanzas1-u2-crowdfunding-peru"
MESES = {1: "enero", 2: "febrero", 3: "marzo", 4: "abril", 5: "mayo", 6: "junio", 7: "julio", 8: "agosto",
         9: "septiembre", 10: "octubre", 11: "noviembre", 12: "diciembre"}
# Corridas de extracción que construyeron los crudos (encabezado de los scripts). Se fijan para que la cifra de
# solicitudes no cambie cuando la demostración en clase o un diagnóstico escriban nuevas líneas en el log.
SCRIPTS_EXTRACCION = ("01_extraccion_api", "02_scraping_web")
FECHAS_EXTRACCION = ("2026-11-07", "2026-11-08")


def cargar(nombre: str):
    spec = importlib.util.spec_from_file_location("s_" + nombre[:2], RAIZ / "codigo" / nombre)
    modulo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modulo)
    return modulo


def esc(texto) -> str:
    """Escapa caracteres especiales de LaTeX."""
    return (str(texto).replace("\\", "\\textbackslash{}").replace("&", "\\&").replace("%", "\\%")
            .replace("_", "\\_").replace("#", "\\#").replace("$", "\\$").replace("{", "\\{").replace("}", "\\}"))


def num(x: float, dec: int = 0) -> str:
    """Punto decimal, espacio fino de miles (recomendación de la RAE) y signo menos tipográfico (U+2212)."""
    return f"{x:,.{dec}f}".replace(",", "\\,").replace("-", "−")


def col(*anchos: float) -> str:
    """Especificación de columnas alineadas a la izquierda (sin huecos de justificación)."""
    return "@{}" + "".join(f">{{\\RaggedRight\\arraybackslash}}p{{{a}cm}}" for a in anchos) + "@{}"


def mes_texto(aaaa_mm: str) -> str:
    return f"{MESES[int(aaaa_mm[5:7])]} de {aaaa_mm[:4]}"


def p_texto(p: float) -> str:
    return "< 0.001" if p < 0.001 else num(p, 3)


def escribir(nombre: str, lineas: list[str]) -> None:
    DESTINO.mkdir(parents=True, exist_ok=True)
    encabezado = ["% Generado por herramientas/articulo/generar_insumos_articulo.py; no editar a mano."]
    (DESTINO / nombre).write_text("\n".join(encabezado + lineas) + "\n", encoding="utf-8", newline="\n")
    print(f"generado: articulo/generado/{nombre}")


def cifras() -> dict[str, str]:
    r = json.loads((SALIDAS / "resultados_04.json").read_text(encoding="utf-8"))
    panel = pd.read_csv(CSV_PROCESADO, dtype={"ruc": str})
    s01 = cargar("01_extraccion_api.py")
    c = {"inicioFPF": mes_texto(r["inicio_actividad_fpf"]), "fechaInicio": mes_texto(s01.FECHA_INICIO),
         "fechaCorte": mes_texto(s01.FECHA_CORTE), "lider": r["plataforma_lider"],
         "participacionLider": num(r["participacion_lider_periodo_pct"], 1),
         "plataformasAutorizadas": str(panel.ruc.nunique()),
         "plataformasVigentes": str(panel[panel.lista_simv == "vigentes"].ruc.nunique()),
         "plataformasConFinanciamiento": str(r["plataformas_con_financiamiento"]),
         "filasPanel": num(len(panel)), "columnasPanel": str(panel.shape[1]),
         "mesesObtenidos": num((panel.estado_simv != "no_obtenido").sum()),
         "noObtenidos": num((panel.estado_simv == "no_obtenido").sum()),
         "coberturaPct": num(100 * (panel.estado_simv != "no_obtenido").mean(), 1),
         "eeffEscala": str(len(r["eeff_escala_corregida"]) + len(r["eeff_escala_excluida"])),
         "eeffEscalaCorregida": str(len(r["eeff_escala_corregida"])), "eeffEscalaExcluida": str(len(r["eeff_escala_excluida"])),
         "saltoTEA": num(r["salto_tea_bcos_pyme_2025_03_pp"], 1),
         "semilla": "0481", "bootstrap": num(10_000)}
    total_fin = total_monto = 0
    for anio, v in r["anual"].items():
        c[f"proyFin{anio}"] = num(v["proyectos_financiados"])
        c[f"monto{anio}"] = num(v["monto_soles"] / 1e6, 2)
        c[f"montoMedio{anio}"] = num(v["monto_promedio_proyecto_soles"] / 1e3, 1)
        c[f"colocacion{anio}"] = num(v["tasa_colocacion_pct"], 1)
        c[f"hhi{anio}"] = num(v["hhi"])
        if v["var_interanual_monto_pct"] is not None:
            c[f"varMonto{anio}"] = num(v["var_interanual_monto_pct"], 1)
        total_fin += v["proyectos_financiados"]
        total_monto += v["monto_soles"]
    c["proyFinTotal"], c["montoTotal"] = num(total_fin), num(total_monto / 1e6, 2)
    h1 = r["h1"]
    c.update({"hUnoMedianaAntes": num(h1["mediana_antes_soles"] / 1e6, 2), "hUnoMedianaDespues": num(h1["mediana_despues_soles"] / 1e6, 2),
              "hUnoU": num(h1["U"]), "hUnoP": p_texto(h1["p_valor_unilateral"]), "hUnoNAntes": str(h1["n_antes"]),
              "hUnoNDespues": str(h1["n_despues"]), "hUnoICinf": num(h1["ic95_diferencia_medianas_soles"][0] / 1e6, 2),
              "hUnoICsup": num(h1["ic95_diferencia_medianas_soles"][1] / 1e6, 2)})
    c["mesesActividadFPF"] = str(h1["n_antes"] + h1["n_despues"])
    sens = r["h1_sensibilidad"]
    c["hUnoPSinLider"] = p_texto(next(v for k, v in sens.items() if k.startswith("H1: sin"))["p_valor_unilateral"])
    c["hUnoPCota"] = p_texto(next(v for k, v in sens.items() if k.startswith("H1: cota"))["p_valor_unilateral"])
    ht = r["h1_tendencia"]
    c.update({"placeboN": str(len(ht["cortes_placebo"])), "placeboPMax": p_texto(ht["p_placebo_max"]),
              "crecMensualPrevio": num(ht["crecimiento_mensual_previo_pct"], 1), "rDosTendencia": num(ht["r2_tendencia_previa"], 2),
              "acfPrevia": num(ht["autocorrelacion_log_monto_previa"], 2),
              "mesesSobreTendencia": str(ht["meses_despues_sobre_tendencia"]), "mesesDespues": str(ht["meses_despues"]),
              "interanualAntes": num(ht["interanual_mediana_antes_pct"]), "interanualDespues": num(ht["interanual_mediana_despues_pct"]),
              "interanualP": p_texto(ht["interanual_p"])})
    cota = r["cota_no_obtenidos"]
    c.update({"noObtenidosVentana": str(cota["meses_no_obtenidos_en_ventana"]),
              "cotaMaxAnual": num(max(cota["por_anio_soles"].values()) / 1e6, 2),
              "cotaPctMax": num(max(cota["por_anio_pct_del_monto"].values()), 1),
              "cotaPctMaxDesde2024": num(max(v for a, v in cota["por_anio_pct_del_monto"].items() if a >= "2024"), 1)})
    h2 = r["h2"]
    dl = h2["dentro_lider"]
    c.update({"colocacionEmp": num(h2["colocacion_empresarial_pct"], 1), "colocacionPer": num(h2["colocacion_personal_pct"], 1),
              "hDosZ": num(h2["z"], 2), "hDosP": p_texto(h2["p_valor"]),
              "principalPersonal": h2["plataforma_principal_personal"], "pctPersonalPrincipal": num(h2["pct_personal_en_principal"], 1),
              "pctEmpresarialPrincipal": num(h2["pct_empresarial_en_principal"], 1),
              "hDosFisherOR": num(dl["odds_ratio"], 2), "hDosFisherP": p_texto(dl["p_valor_fisher"]),
              "perLiderFin": str(dl["financiados_per"]), "perLiderPub": str(dl["publicados_per"])})
    rhos = [v["rho"] for v in r["e1"].values()]
    ps = [v["p_valor"] for v in r["e1"].values()]
    c.update({"eUnoRhoMin": num(min(rhos), 2), "eUnoRhoMax": num(max(rhos), 2), "eUnoPMin": p_texto(min(ps)),
              "eUnoN": str(len(rhos))})
    ci = r["costo_intermediacion_lider"]
    c.update({"costoMediana": num(ci["mediana_trimestral_pct"], 2), "costoAcumulada": num(ci["mediana_trimestral_lectura_acumulada_pct"], 2),
              "costoTrimestres": str(ci["trimestres"])})
    lineas_http = re.findall(r"^(\d{4}-\d{2}-\d{2}) [\d:]+ \| (\S+) \| \w+ \| HTTP (\d{3}) \|",
                             (Path(RAIZ) / "log_ejecucion.txt").read_text(encoding="utf-8"), re.M)
    extraccion = [h for f, s, h in lineas_http if s in SCRIPTS_EXTRACCION and f in FECHAS_EXTRACCION]
    c["solicitudesHTTP"] = num(len(extraccion))
    c["solicitudesHTTPok"] = num(sum(x == "200" for x in extraccion))
    c["solicitudesDiagnostico"] = num(sum(1 for f, s, _ in lineas_http if s not in SCRIPTS_EXTRACCION and f in FECHAS_EXTRACCION))
    c.update(cifras_tablas(r))
    # Versión de cada valor p con su relación, para escribir $p\cifra{xRel}$: «< 0.001» o «= 0.127»
    for k in [k for k in c if k.endswith("P") or k.endswith("PMin") or k.endswith("PMax") or k.startswith("hUnoP")]:
        c[f"{k}Rel"] = c[k] if c[k].startswith("<") else f"= {c[k]}"
    return c


def cifras_tablas(r: dict) -> dict[str, str]:
    """Cifras que el texto de Resultados cita de las tablas de 04 (se leen de los CSV, sin redondeos manuales)."""
    tablas, c = SALIDAS / "tablas", {}
    lider = r["plataforma_lider"]
    # T1: plataformas, ordenadas por monto financiado
    t1 = pd.read_csv(tablas / "t1_plataformas.csv").sort_values("monto_financiado_soles", ascending=False)
    c["plataformasRetiradas"] = str(int((t1.lista_simv == "retiradas").sum()))
    for orden, f in zip(("Lider", "Segunda", "Tercera"), t1[t1.proyectos_financiados > 0].itertuples()):
        c[f"nombre{orden}"] = f.plataforma
        c[f"proyFin{orden}"] = num(f.proyectos_financiados)
        c[f"monto{orden}"] = num(f.monto_financiado_soles / 1e6, 2)
        c[f"inicio{orden}"] = mes_texto(f.primer_mes_financiamiento)
        c[f"fin{orden}"] = mes_texto(f.ultimo_mes_financiamiento)
        c[f"mesesFin{orden}"] = str(f.meses_con_financiamiento)
    # T2: oferta anual
    t2 = pd.read_csv(tablas / "t2_oferta_anual.csv")
    for f in t2.itertuples():
        c[f"publicados{f.anio}"] = num(f.proyectos_publicados)
        c[f"partEmp{f.anio}"] = num(f.participacion_empresarial_pct, 1)
        c[f"montoReal{f.anio}"] = num(f.monto_real_soles_dic2021 / 1e6, 2)
    # T3: situación financiera de las sociedades administradoras
    t3 = pd.read_csv(tablas / "t3_plataformas_financieros.csv")
    tl = t3[t3.plataforma == lider]
    for f in tl.itertuples():
        c[f"roaLider{f.anio}"] = num(f.roa_pct, 1)
        c[f"ingresosLider{f.anio}"] = num(f.ingresos_miles)
        c[f"utilidadLider{f.anio}"] = num(f.utilidad_miles)
        c[f"activoLider{f.anio}"] = num(f.activo_cierre_miles)
        c[f"patrimonioLider{f.anio}"] = num(f.patrimonio_cierre_miles)
    c["primerAnioUtilidadLider"] = str(int(tl[tl.utilidad_miles > 0].anio.min()))
    c["costoAnualLiderMin"] = num(tl.costo_intermediacion_pct.min(), 1)
    c["costoAnualLiderMax"] = num(tl.costo_intermediacion_pct.max(), 1)
    otras = t3[(t3.plataforma != lider) & t3.roa_pct.notna()]
    c["aniosOtras"] = str(len(otras))
    c["aniosOtrasPerdida"] = str(int((otras.utilidad_miles < 0).sum()))
    # T4: condiciones por tipo de receptor
    t4 = pd.read_csv(tablas / "t4_condiciones_por_receptor.csv").set_index(["periodo", "tipo_receptor"])
    for periodo, sufijo in (("Todo el periodo", ""), ("Antes de la reforma", "Antes"), ("Después de la reforma", "Despues")):
        for tipo, t in (("Empresarial", "Emp"), ("Personal", "Per")):
            f = t4.loc[(periodo, tipo)]
            c[f"publicados{t}{sufijo}"] = num(f.proyectos_publicados)
            if f.proyectos_publicados > 0:
                c[f"colocacion{t}{sufijo}"] = num(f.tasa_colocacion_pct, 1)
                c[f"montoMedio{t}{sufijo}"] = num(f.monto_promedio_proyecto_soles / 1e3, 1)
                c[f"ic{t}{sufijo}Inf"] = num(f.ic95_inferior, 1)
                c[f"ic{t}{sufijo}Sup"] = num(f.ic95_superior, 1)
    # T7: tasas medias por periodo (2025 dividido por el quiebre de marzo)
    t7 = pd.read_csv(tablas / "t7_comparacion_segmentos.csv")
    claves = {"tamn": "Tamn", "tea_bcos_pyme_360": "BcosPyme", "tea_cmac_pyme_360": "CmacPyme",
              "tea_crac_pyme_360": "CracPyme", "tea_bcos_consumo_360": "BcosConsumo"}
    for f in t7.to_dict("records"):
        etiqueta = f["periodo"][:4] + ("a" if "(ene-feb)" in f["periodo"] else "b" if "(mar-dic)" in f["periodo"] else "")
        for col, nombre in claves.items():
            c[f"tea{nombre}{etiqueta}"] = num(f[f"{col}_media"], 1)
    for col, nombre in claves.items():
        c[f"tea{nombre}Min"] = num(t7[f"{col}_media"].min(), 1)
        c[f"tea{nombre}Max"] = num(t7[f"{col}_media"].max(), 1)
    c["fpfEmpPrimero"] = num(t7.fpf_empresarial_monto_medio_soles.iloc[0] / 1e3, 1)
    c["fpfEmpUltimo"] = num(t7.fpf_empresarial_monto_medio_soles.iloc[-1] / 1e3, 1)
    # F1: monto mensual del sistema (datos de la figura)
    f1 = pd.read_csv(SALIDAS / "figuras" / "f1_monto_mensual_por_plataforma_datos.csv", index_col=0).sum(axis=1)
    for anio, mediana in f1.groupby(f1.index.str[:4]).median().items():
        c[f"medianaMensual{anio}"] = num(mediana, 2)
    c["maxMensual"], c["mesMaxMensual"] = num(f1.max(), 2), mes_texto(f1.idxmax())
    return c


def anexo_endpoints() -> list[str]:
    s01, s02 = cargar("01_extraccion_api.py"), cargar("02_scraping_web.py")
    filas = [("API", "BCRP, BCRPData", s01.URL_BCRP, f"10 series mensuales; {s01.periodo_bcrp(s01.FECHA_INICIO)} a {s01.periodo_bcrp(s01.FECHA_CORTE)}"),
             ("API", "SMV, OData PrincipalCuentaSMV", s01.URL_SMV, "sEjercicio=2021-2026; sPeriodo=1-4; sTipoInf=I (23 trimestres)"),
             ("Scraping", "SMV, SIMV «Información de Proyectos»", s02.URL_SIMV,
              f"POST ASP.NET por plataforma, año y mes; pausa de {s02.PAUSA_SIMV:.0f} s; 6 plataformas × 69 meses")]
    # Anchos: suma de columnas + separaciones <= 15.92 cm (ancho de texto en A4 con márgenes de 2.54 cm)
    lineas = [f"\\begin{{longtable}}{{{col(1.6, 2.8, 5.8, 3.9)}}}", "\\toprule",
              "Vía & Fuente & Endpoint o URL & Parámetros \\\\", "\\midrule", "\\endhead"]
    lineas += [f"{esc(v)} & {esc(f)} & \\url{{{u}}} & {esc(p)} \\\\" for v, f, u, p in filas]
    return lineas + ["\\bottomrule", "\\end{longtable}"]


def anexo_diccionario() -> list[str]:
    texto = (RAIZ / "diccionario_variables.md").read_text(encoding="utf-8").splitlines()
    filas = [l for l in texto if re.match(r"^\| \d+ \|", l)]
    lineas = ["{\\scriptsize\\setlength{\\tabcolsep}{4pt}", f"\\begin{{longtable}}{{{col(3.8, 5.0, 2.2, 1.7, 1.9)}}}", "\\toprule",
              "Variable & Definición & Unidad & Frecuencia & Fuente \\\\", "\\midrule", "\\endhead"]
    for f in filas:
        partes = [x.strip() for x in f.strip("|").split("|")]
        _, variable, definicion, unidad, frecuencia, fuente = partes[:6]
        corta = ("SIMV" if "SIMV" in fuente else "SMV-OData" if "OData" in fuente else
                 re.search(r"serie (PN\w+)", fuente).group(1) if "BCRP" in fuente else "Derivada")
        nombre = esc(variable.strip("`")).replace("\\_", "\\_\\allowbreak{}")  # permite cortar en cada guion bajo
        lineas.append(f"\\texttt{{{nombre}}} & {esc(definicion)} & {esc(unidad)} & {esc(frecuencia)} & {esc(corta)} \\\\")
    return lineas + ["\\bottomrule", "\\end{longtable}", "}"]


def anexo_reproducibilidad() -> list[str]:
    try:
        commit = subprocess.run(["git", "rev-parse", "--short", "HEAD"], cwd=RAIZ, capture_output=True, text=True, check=True).stdout.strip()
    except (OSError, subprocess.CalledProcessError):
        commit = "sin git"
    log = (RAIZ / "log_ejecucion.txt").read_text(encoding="utf-8")
    fechas = sorted(set(re.findall(r"^(\d{4}-\d{2}-\d{2}) [\d:]+ \| \S+ \| INFO \| HTTP", log, re.M)))
    req = {l.split("==")[0]: l.split("==")[1] for l in (RAIZ / "requirements.txt").read_text(encoding="utf-8").splitlines() if "==" in l}
    versiones = ", ".join(f"{k} {req[k]}" for k in ("requests", "beautifulsoup4", "pandas", "numpy", "scipy", "matplotlib", "pandera", "pytest") if k in req)
    panel = pd.read_csv(CSV_PROCESADO)
    s01 = cargar("01_extraccion_api.py")
    filas = [("Repositorio", f"\\url{{{REPOSITORIO}}}"), ("Commit de referencia", f"\\texttt{{{commit}}}"),
             ("Periodo consultado", f"{s01.FECHA_INICIO} a {s01.FECHA_CORTE} (constantes FECHA\\_INICIO y FECHA\\_CORTE)"),
             ("Fechas de extracción", ", ".join(fechas) + " (según log\\_ejecucion.txt)"),
             ("Archivo procesado", f"\\texttt{{datos\\_procesados/{CSV_PROCESADO.name.replace('_', chr(92) + '_')}}}: {len(panel)} filas, {panel.shape[1]} columnas"),
             ("SHA-256 del archivo procesado", "\\texttt{{{}}}\\newline\\texttt{{{}}}".format(*(lambda h: (h[:32], h[32:]))(sha256_archivo(CSV_PROCESADO)))),
             ("Orden de ejecución", "\\texttt{01\\_extraccion\\_api.py} $\\rightarrow$ \\texttt{02\\_scraping\\_web.py} $\\rightarrow$ "
                                    "\\texttt{03\\_limpieza\\_datos.py} $\\rightarrow$ \\texttt{04\\_analisis.py}"),
             ("Verificación", "\\texttt{python -m pytest} y \\texttt{python codigo/auditoria.py} (con \\texttt{-{}-en-vivo} para cotejar con las fuentes)"),
             ("Entorno", f"Python 3.14.7; {esc(versiones)}")]
    lineas = [f"\\begin{{longtable}}{{{col(3.8, 11.3)}}}", "\\toprule", "Elemento & Detalle \\\\", "\\midrule", "\\endhead"]
    lineas += [f"{a} & {b} \\\\" for a, b in filas]
    return lineas + ["\\bottomrule", "\\end{longtable}"]


def main() -> int:
    c = cifras()
    lineas = ["\\newcommand{\\cifra}[1]{\\ifcsname cifra@#1\\endcsname\\csname cifra@#1\\endcsname\\else\\textbf{??#1??}\\fi}"]
    lineas += [f"\\expandafter\\def\\csname cifra@{k}\\endcsname{{{v}}}" for k, v in sorted(c.items())]
    escribir("cifras.tex", lineas)
    escribir("anexo_endpoints.tex", anexo_endpoints())
    escribir("anexo_diccionario.tex", anexo_diccionario())
    escribir("anexo_reproducibilidad.tex", anexo_reproducibilidad())
    print(f"cifras disponibles: {len(c)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
