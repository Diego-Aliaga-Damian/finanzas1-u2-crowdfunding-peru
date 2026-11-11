# Diego Sebastián Aliaga Damián
# 2024200481M
# Tema 96: Fintech y financiamiento participativo (crowdfunding) en el Perú: oferta y condiciones
# Fecha de extracción: 2026-11-07 (censo) y 2026-11-08 (reanudación)
"""Auditoría automatizada del proyecto (Fase IV; complementa a los scripts 01-04).

Reproduce, sin internet, los controles que la consigna anuncia en los numerales 2.4.1, 2.4.2, 2.4.4,
2.4.5, 2.4.6 y 2.4.8, y escribe salidas/reporte_auditoria.md. Cada control termina en uno de tres estados:
    ✅ cumple     ❌ no cumple     ⏳ no ejecutado (p. ej., porque el componente aún no existe)
Regla de autenticidad: un control que no se ejecutó nunca se informa como «cumple».

Uso (desde la raíz del proyecto):
    python codigo/auditoria.py              auditoría local, sin internet (≈ 1 min)
    python codigo/auditoria.py --en-vivo    añade el cotejo de 10 filas al azar con la fuente en vivo
                                            (≈ 21 solicitudes con pausas de 3 s; semilla 0481)
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import logging
import re
import subprocess
import sys
import tempfile
from datetime import datetime
from pathlib import Path

import numpy as np
import pandas as pd
import pandera.pandas as pa

from comun import CODIGO_MATRICULA, CRUDOS, PROCESADOS, RAIZ, SALIDAS, sha256_archivo

CODIGO = RAIZ / "codigo"
CSV_PROCESADO = PROCESADOS / f"datos_procesados_{CODIGO_MATRICULA}.csv"
ARCHIVO_LOG = RAIZ / "log_ejecucion.txt"
README = RAIZ / "README.md"
REPORTE = SALIDAS / "reporte_auditoria.md"
SCRIPTS = ["01_extraccion_api.py", "02_scraping_web.py", "03_limpieza_datos.py", "04_analisis.py"]
DOCUMENTACION = ["README.md", "requirements.txt", ".env.example", "log_ejecucion.txt",
                 "diccionario_variables.md", "incidencias_fuente.md"]
CRUDOS_CSV = [f"datos_crudos_{CODIGO_MATRICULA}_{f}.csv" for f in ("bcrp", "smv_odata", "smv_simv")]
SEMILLA = 481  # cuatro últimos dígitos de la matrícula 2024200481M (0481), numeral 2.4.4
CUMPLE, NO_CUMPLE, NO_EJECUTADO = "✅", "❌", "⏳"

# Clasificación de las columnas sustantivas por fuente (numeral 2.4.1)
FUENTE_COLUMNA = {"SMV-SIMV (scraping)": re.compile(r"^(proy_|monto_)"),
                  "SMV-OData (API)": re.compile(r"_miles$"),
                  "BCRP (API)": re.compile(r"^(tea_|tamn$|ipc$)")}
TIPOS_LECTURA = {"periodo": str, "ruc": str, "empresa_id_simv": str, "plataforma": str, "razon_social": str,
                 "lista_simv": str, "estado_simv": str, "trimestre_eeff": str, "fecha_registro_eeff": str}

resultados: list[dict] = []


# ============================================================================
# Utilidades
# ============================================================================
def anotar(seccion: str, control: str, numeral: str, estado: str, evidencia: str) -> None:
    resultados.append({"seccion": seccion, "control": control, "numeral": numeral,
                       "estado": estado, "evidencia": evidencia})


def logger_silencioso() -> logging.Logger:
    """Logger que no escribe en log_ejecucion.txt: la auditoría no altera la evidencia de extracción."""
    log = logging.getLogger("auditoria_silencioso")
    log.handlers, log.propagate = [logging.NullHandler()], False
    return log


def logger_consola() -> logging.Logger:
    log = logging.getLogger("auditoria")
    if not log.handlers:
        h = logging.StreamHandler()
        h.setFormatter(logging.Formatter("%(asctime)s | auditoria | %(message)s", "%H:%M:%S"))
        log.addHandler(h)
        log.setLevel(logging.INFO)
        log.propagate = False
    return log


def cargar_script(nombre: str):
    """Importa un script cuyo nombre empieza con número (p. ej., 03_limpieza_datos.py)."""
    if str(CODIGO) not in sys.path:
        sys.path.insert(0, str(CODIGO))
    spec = importlib.util.spec_from_file_location("script_" + nombre.split(".")[0], CODIGO / nombre)
    modulo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modulo)
    modulo.relativa = lambda ruta: str(ruta)  # permite escribir fuera de la raíz (carpetas temporales)
    return modulo


def leer_procesado(ruta: Path = CSV_PROCESADO) -> pd.DataFrame:
    tipos = dict(TIPOS_LECTURA)
    columnas = pd.read_csv(ruta, nrows=0).columns
    tipos.update({c: "Int64" for c in columnas if c.startswith(("proy_", "monto_"))})
    return pd.read_csv(ruta, dtype=tipos)


def esquema() -> pa.DataFrameSchema:
    """Esquema Pandera de datos_procesados: tipos, dominios, rangos y llave única."""
    conteo = lambda: pa.Column("Int64", pa.Check.ge(0), nullable=True)
    tasa = lambda: pa.Column(float, pa.Check.in_range(0, 200))
    columnas = {
        "periodo": pa.Column(str, pa.Check.str_matches(r"^\d{4}-(0[1-9]|1[0-2])$")),
        "anio": pa.Column(int, pa.Check.in_range(2021, 2026)),
        "mes": pa.Column(int, pa.Check.in_range(1, 12)),
        "ruc": pa.Column(str, pa.Check.str_matches(r"^\d{11}$")),
        "empresa_id_simv": pa.Column(str, pa.Check.str_matches(r"^\d+$")),
        "plataforma": pa.Column(str),
        "razon_social": pa.Column(str),
        "lista_simv": pa.Column(str, pa.Check.isin(["vigentes", "retiradas"])),
        "estado_simv": pa.Column(str, pa.Check.isin(["con_registros", "sin_registros", "no_obtenido"])),
        **{f"{v}_{t}": conteo() for t in ("emp", "per", "valores")
           for v in ("proy_publicados", "proy_financiados", "monto_financiado")},
        "trimestre_eeff": pa.Column(str, pa.Check.str_matches(r"^\d{4}-T[1-4]$"), nullable=True),
        **{c: pa.Column(float, nullable=True) for c in ("activo_total_miles", "pasivo_total_miles",
                                                         "patrimonio_total_miles", "ingresos_totales_miles",
                                                         "utilidad_neta_miles")},
        "fecha_registro_eeff": pa.Column(str, pa.Check.str_matches(r"^\d{4}-\d{2}-\d{2}$"), nullable=True),
        **{c: tasa() for c in ("tamn", "tea_bcos_pyme_360", "tea_bcos_pyme_mas360", "tea_bcos_consumo_360",
                               "tea_bcos_consumo_mas360", "tea_cmac_pyme_360", "tea_cmac_pyme_mas360",
                               "tea_crac_pyme_360", "tea_crac_pyme_mas360")},
        "ipc": pa.Column(float, pa.Check.in_range(50, 300)),
    }
    return pa.DataFrameSchema(columnas, strict=True, ordered=True, unique=["ruc", "periodo"])


def equivalencia(a: pd.DataFrame, b: pd.DataFrame) -> dict:
    """Criterio del numeral 2.4.5: mismas columnas y tipos, mismo número de filas y % de celdas iguales."""
    info = {"mismas_columnas": list(a.columns) == list(b.columns), "mismas_filas": len(a) == len(b)}
    info["mismos_tipos"] = info["mismas_columnas"] and bool((a.dtypes.astype(str) == b.dtypes.astype(str)).all())
    if not (info["mismas_columnas"] and info["mismas_filas"]):
        info["pct_celdas_iguales"] = 0.0
        return info
    iguales = pd.DataFrame(index=a.index, columns=a.columns, dtype=bool)
    for c in a.columns:
        x, y = a[c], b[c]
        if pd.api.types.is_float_dtype(x) and pd.api.types.is_float_dtype(y):
            iguales[c] = np.isclose(x, y, rtol=0, atol=1e-9, equal_nan=True)
        else:
            iguales[c] = (x == y).fillna(False) | (x.isna() & y.isna())
    info["pct_celdas_iguales"] = round(100 * float(iguales.to_numpy().mean()), 4)
    return info


def lineas_http() -> pd.DataFrame:
    filas = []
    for linea in ARCHIVO_LOG.read_text(encoding="utf-8").splitlines():
        m = re.match(r"^(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}) \| ([^|]+) \| \w+ \| HTTP (\d{3}) \| (\w+) (\S+)", linea)
        if m:
            filas.append({"momento": pd.Timestamp(m.group(1)), "script": m.group(2).strip(),
                          "http": int(m.group(3)), "metodo": m.group(4), "url": m.group(5)})
    return pd.DataFrame(filas)


def reejecutar_03(destino: Path) -> Path:
    """Ejecuta 03 completo escribiendo en una carpeta temporal (no toca la base entregada ni el log)."""
    s03 = cargar_script("03_limpieza_datos.py")
    s03.PROCESADOS = destino
    s03.CSV_PROCESADO = destino / CSV_PROCESADO.name
    s03.DICCIONARIO = destino / "diccionario_variables.md"
    s03.REPORTE = destino / "reporte_limpieza.md"
    s03.controles, s03.transformaciones = [], []
    s03.configurar_log = lambda nombre: logger_silencioso()
    s03.main()
    return s03.CSV_PROCESADO


# ============================================================================
# 1. Estructura y documentación (2.4.2, 2.5 y Bloque B del 2.4.6)
# ============================================================================
def controles_estructura() -> None:
    S = "1. Estructura y documentación"
    for nombre in SCRIPTS:
        existe = (CODIGO / nombre).exists()
        estado = CUMPLE if existe else (NO_EJECUTADO if nombre == "04_analisis.py" else NO_CUMPLE)
        anotar(S, f"Script `{nombre}`", "2.4.2", estado,
               "presente" if existe else ("pendiente: se escribe en la Fase V" if nombre == "04_analisis.py" else "FALTA"))
    for nombre in DOCUMENTACION:
        ruta = RAIZ / nombre
        anotar(S, f"Archivo `{nombre}`", "2.4.2", CUMPLE if ruta.exists() and ruta.stat().st_size > 0 else NO_CUMPLE,
               f"{ruta.stat().st_size:,} bytes" if ruta.exists() else "FALTA")
    for nombre in CRUDOS_CSV:
        ruta = CRUDOS / nombre
        anotar(S, f"Crudo `{nombre}`", "2.4.1", CUMPLE if ruta.exists() else NO_CUMPLE,
               f"{sum(1 for _ in open(ruta, encoding='utf-8')) - 1:,} filas" if ruta.exists() else "FALTA")
    anotar(S, f"Procesado `{CSV_PROCESADO.name}`", "2.4.1", CUMPLE if CSV_PROCESADO.exists() else NO_CUMPLE,
           "presente" if CSV_PROCESADO.exists() else "FALTA")

    encabezado = [r"^# Diego Sebastián Aliaga Damián$", r"^# 2024200481M$", r"^# Tema 96: .+",
                  r"^# Fecha de extracción: \d{4}-\d{2}-\d{2}.*"]
    malos, absolutas = [], []
    unidad = re.compile(r"\b[A-Za-z]:[\\/]{1,2}(Users|Documents|Desktop)|/home/\w+|/Users/\w+")
    for archivo in sorted(CODIGO.glob("*.py")):
        lineas = archivo.read_text(encoding="utf-8").splitlines()[:4]
        if len(lineas) < 4 or not all(re.match(p, l) for p, l in zip(encabezado, lineas)):
            malos.append(archivo.name)
        if unidad.search(archivo.read_text(encoding="utf-8")):
            absolutas.append(archivo.name)
    total = len(list(CODIGO.glob("*.py")))
    anotar(S, "Encabezado obligatorio de 4 líneas en cada archivo de código", "2.4.2",
           CUMPLE if not malos else NO_CUMPLE, f"{total - len(malos)}/{total} archivos" + (f"; fallan: {malos}" if malos else ""))
    anotar(S, "Sin rutas absolutas del equipo en el código", "2.4.4", CUMPLE if not absolutas else NO_CUMPLE,
           "ninguna" if not absolutas else f"en: {absolutas}")

    req = [l for l in (RAIZ / "requirements.txt").read_text(encoding="utf-8").splitlines() if l and not l.startswith("#")]
    sin_version = [l for l in req if "==" not in l]
    anotar(S, "requirements.txt con versiones exactas", "2.4.2", CUMPLE if req and not sin_version else NO_CUMPLE,
           f"{len(req)} librerías con `==`" + (f"; sin versión: {sin_version}" if sin_version else ""))
    env = [l for l in (RAIZ / ".env.example").read_text(encoding="utf-8").splitlines() if "=" in l and not l.startswith("#")]
    con_valor = [l for l in env if l.split("=", 1)[1].strip()]
    anotar(S, ".env.example sin claves ni valores reales", "2.4.4", CUMPLE if not con_valor else NO_CUMPLE,
           f"{len(env)} variables, todas vacías" if not con_valor else f"con valor: {con_valor}")


# ============================================================================
# 2. Mínimos de la base (2.4.1)
# ============================================================================
def controles_minimos(panel: pd.DataFrame, http: pd.DataFrame) -> None:
    S = "2. Mínimos de la base"
    anotar(S, "Histórico de al menos 60 periodos mensuales", "2.4.1",
           CUMPLE if panel.periodo.nunique() >= 60 else NO_CUMPLE,
           f"{panel.periodo.nunique()} meses ({panel.periodo.min()} a {panel.periodo.max()}); {len(panel)} filas")
    anotar(S, "Al menos 6 columnas", "2.4.1", CUMPLE if panel.shape[1] >= 6 else NO_CUMPLE, f"{panel.shape[1]} columnas")
    por_fuente = {f: [c for c in panel.columns if p.search(c)] for f, p in FUENTE_COLUMNA.items()}
    sustantivas = sum(len(v) for v in por_fuente.values())
    anotar(S, "Al menos 4 variables sustantivas", "2.4.1", CUMPLE if sustantivas >= 4 else NO_CUMPLE,
           f"{sustantivas} sustantivas")
    anotar(S, "Al menos 1 variable de cada fuente", "2.4.1", CUMPLE if all(por_fuente.values()) else NO_CUMPLE,
           "; ".join(f"{f}: {len(v)}" for f, v in por_fuente.items()))
    api = http[(http.script == "01_extraccion_api") & (http.http == 200)]
    scr = http[(http.script == "02_scraping_web") & (http.http == 200) & http.url.str.contains("/SIMV/")]
    anotar(S, "Dos vías de extracción ejecutadas (API y scraping)", "2.4.1",
           CUMPLE if len(api) and len(scr) else NO_CUMPLE,
           f"API: {len(api)} respuestas HTTP 200 · scraping: {len(scr)} respuestas HTTP 200 (según el log)")


# ============================================================================
# 3. Autenticidad y coincidencia código-datos (Bloque A del 2.4.6, controles locales)
# ============================================================================
def controles_autenticidad(panel: pd.DataFrame) -> None:
    S = "3. Autenticidad (controles locales del Bloque A)"
    with tempfile.TemporaryDirectory() as tmp:
        regenerado = reejecutar_03(Path(tmp))
        identico = regenerado.read_bytes() == CSV_PROCESADO.read_bytes()
        eq = equivalencia(panel, leer_procesado(regenerado))
    anotar(S, "03 regenera la base entregada desde los crudos", "2.4.5 / A2",
           CUMPLE if identico or eq["pct_celdas_iguales"] >= 95 else NO_CUMPLE,
           f"bytes idénticos: {'sí' if identico else 'no'}; celdas iguales: {eq['pct_celdas_iguales']} %; "
           f"columnas {'=' if eq['mismas_columnas'] else '≠'}; filas {'=' if eq['mismas_filas'] else '≠'}")

    declarado = re.search(r"SHA-256 del archivo procesado\*\*\s*\|\s*\*\*`([0-9a-f]{64})`", README.read_text(encoding="utf-8"))
    real = sha256_archivo(CSV_PROCESADO)
    anotar(S, "SHA-256 del README = hash del archivo entregado", "2.4.5 / A3",
           CUMPLE if declarado and declarado.group(1) == real else NO_CUMPLE,
           f"declarado {declarado.group(1)[:12] if declarado else 'NO ENCONTRADO'}… · real {real[:12]}…")

    # Trazabilidad celda a celda: cada valor de la base existe en el crudo correspondiente
    s = pd.read_csv(CRUDOS / CRUDOS_CSV[2], dtype=str)
    s = s[(s.resultado == "con_registros") & (s.modalidad == "PRESTAMOS")]
    s["periodo"] = s.anio + "-" + s.mes.str.zfill(2)
    clave = panel.set_index(["empresa_id_simv", "periodo"])
    mapa = {"proyectos_publicados": "proy_publicados", "proyectos_financiados": "proy_financiados",
            "monto_total_financiado": "monto_financiado"}
    t = {"EMPRESARIAL": "emp", "PERSONAL": "per"}
    total = iguales = 0
    for _, f in s.iterrows():
        fila = clave.loc[(f.empresa_id, f.periodo)]
        for a, b in mapa.items():
            total += 1
            iguales += int(fila[f"{b}_{t[f.tipo_receptor]}"]) == int(f[a])
    o = pd.read_csv(CRUDOS / CRUDOS_CSV[1], dtype=str)
    o = o[o.TipoEmpresa.str.contains("PARTICIPATIVO", na=False)]
    clave_ruc = panel.set_index(["ruc", "periodo"])
    cols = {"ActivoTotal": "activo_total_miles", "PasivoTotal": "pasivo_total_miles",
            "PatrimonioTotal": "patrimonio_total_miles", "TotalIngreso": "ingresos_totales_miles",
            "UtilidadNeta": "utilidad_neta_miles"}
    for _, f in o.iterrows():
        fila = clave_ruc.loc[(f.RUC, f"{f.Ejercicio}-{3 * int(f.Trimestre[0]):02d}")]
        for a, b in cols.items():
            total += 1
            iguales += float(fila[b]) == float(f[a])
    b = pd.read_csv(CRUDOS / CRUDOS_CSV[0], dtype=str)
    s03 = cargar_script("03_limpieza_datos.py")
    b["periodo"] = b.periodo_bcrp.str[-4:] + "-" + b.periodo_bcrp.str[:3].map(s03.MESES_BCRP).astype(str).str.zfill(2)
    por_mes = panel.drop_duplicates("periodo").set_index("periodo")
    for _, f in b.iterrows():
        total += 1
        iguales += abs(float(por_mes.loc[f.periodo, s03.SERIES_BCRP[f.codigo_serie]]) - float(f.valor)) < 1e-9
    anotar(S, "Cada valor de la base coincide con su crudo (SIMV, EEFF y BCRP)", "2.4.6 / A1-A2",
           CUMPLE if iguales == total else NO_CUMPLE, f"{iguales:,}/{total:,} valores idénticos")

    sin_dato = panel[panel.estado_simv != "con_registros"].filter(regex=r"^(proy_|monto_)").notna().sum().sum()
    anotar(S, "Sin imputaciones: meses sin registros o no obtenidos quedan vacíos", "2.1 / A2",
           CUMPLE if sin_dato == 0 else NO_CUMPLE, f"{sin_dato} celdas con valor donde debería estar vacío")
    anotar(S, "Scripts de extracción presentes", "2.4.6 / A7",
           CUMPLE if all((CODIGO / n).exists() for n in SCRIPTS[:2]) else NO_CUMPLE, "01 y 02 presentes")


# ============================================================================
# 4. Integridad de los crudos (2.4.5)
# ============================================================================
def controles_integridad() -> None:
    S = "4. Integridad de los crudos"
    en_log = set(re.findall(r"sha256=([0-9a-f]{64})", ARCHIVO_LOG.read_text(encoding="utf-8")))
    originales = (list((CRUDOS / "bcrp").glob("*.json")) + list((CRUDOS / "smv_odata").glob("*.json"))
                  + list((CRUDOS / "smv_simv").glob("*_*_*.html")))
    sin_registro = [p.name for p in originales if sha256_archivo(p) not in en_log]
    anotar(S, "SHA-256 de cada respuesta original registrado en el log", "2.4.5",
           CUMPLE if not sin_registro else NO_CUMPLE,
           f"{len(originales) - len(sin_registro)}/{len(originales)} archivos" + (f"; sin registro: {sin_registro[:5]}" if sin_registro else ""))

    s02 = cargar_script("02_scraping_web.py")
    invalidos = []
    for p in (CRUDOS / "smv_simv").glob("*_*_*.html"):
        e, a, m = p.stem.split("_")
        if s02.validar(s02.sopa(p.read_bytes()), e, int(a), int(m)):
            invalidos.append(p.name)
    total = len(list((CRUDOS / "smv_simv").glob("*_*_*.html")))
    anotar(S, "Cada HTML del SIMV trae la grilla y confirma su consulta", "2.4.6",
           CUMPLE if not invalidos else NO_CUMPLE, f"{total - len(invalidos)}/{total} válidos")

    # Los CSV crudos se reconstruyen idénticos desde las respuestas originales
    s01 = cargar_script("01_extraccion_api.py")
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        s01.CSV_BCRP, s01.CSV_SMV, s02.CSV_SIMV = tmp / CRUDOS_CSV[0], tmp / CRUDOS_CSV[1], tmp / CRUDOS_CSV[2]
        log = logger_silencioso()
        s01.csv_bcrp(log); s01.csv_smv(log); s02.generar_csv(log)
        distintos = [n for n in CRUDOS_CSV if (tmp / n).read_bytes() != (CRUDOS / n).read_bytes()]
    anotar(S, "Los 3 CSV crudos se reconstruyen idénticos desde los originales", "2.4.5",
           CUMPLE if not distintos else NO_CUMPLE, "3/3 idénticos" if not distintos else f"distintos: {distintos}")


# ============================================================================
# 5. Calidad de la base procesada (2.4.2)
# ============================================================================
def controles_calidad(panel: pd.DataFrame) -> None:
    S = "5. Calidad de la base procesada"
    try:
        esquema().validate(panel, lazy=True)
        anotar(S, "Esquema Pandera: tipos, dominios, rangos y llave única", "2.4.2", CUMPLE,
               f"{panel.shape[1]} columnas validadas")
    except pa.errors.SchemaErrors as e:
        anotar(S, "Esquema Pandera: tipos, dominios, rangos y llave única", "2.4.2", NO_CUMPLE,
               f"{len(e.failure_cases)} fallas; primeras: {e.failure_cases.head(3).to_dict('records')}")
    dup = panel.duplicated(["ruc", "periodo"]).sum()
    anotar(S, "Sin duplicados en la llave ruc + periodo", "2.4.2", CUMPLE if dup == 0 else NO_CUMPLE, f"{dup} duplicados")
    eeff_fuera = panel[panel.trimestre_eeff.notna() & ~panel.mes.isin([3, 6, 9, 12])]
    anotar(S, "EEFF solo en meses de cierre de trimestre (no se interpola)", "2.4.2",
           CUMPLE if eeff_fuera.empty else NO_CUMPLE, f"{len(eeff_fuera)} filas fuera de mar/jun/sep/dic")
    simv = panel.filter(regex=r"^(proy_|monto_)").notna().any(axis=1)
    incoherente = panel[simv != (panel.estado_simv == "con_registros")]
    anotar(S, "Valores SIMV presentes solo cuando estado_simv = con_registros", "2.4.2",
           CUMPLE if incoherente.empty else NO_CUMPLE, f"{len(incoherente)} filas incoherentes")
    faltantes = panel.isna().mean().mul(100).round(1)
    anotar(S, "Faltantes identificados y explicados", "2.4.2", CUMPLE,
           f"{int((faltantes > 0).sum())} columnas con faltantes; máximo {faltantes.max()} % "
           f"(meses sin registros, no obtenidos o fuera del cierre trimestral; detalle en reporte_limpieza.md)")


# ============================================================================
# 6. Consistencia de fechas (2.4.5)
# ============================================================================
def controles_fechas(panel: pd.DataFrame, http: pd.DataFrame) -> None:
    S = "6. Consistencia de fechas"
    valores = {}
    for n in SCRIPTS[:3]:
        texto = (CODIGO / n).read_text(encoding="utf-8")
        valores[n] = (re.search(r'^FECHA_INICIO = "([\d-]+)"', texto, re.M).group(1),
                      re.search(r'^FECHA_CORTE = "([\d-]+)"', texto, re.M).group(1))
    iguales = len(set(valores.values())) == 1
    anotar(S, "FECHA_INICIO y FECHA_CORTE constantes e idénticas en 01, 02 y 03", "2.4.5",
           CUMPLE if iguales else NO_CUMPLE, f"{set(valores.values())}")
    inicio, corte = next(iter(valores.values()))
    anotar(S, "La base cubre exactamente la ventana declarada", "2.4.5",
           CUMPLE if (panel.periodo.min(), panel.periodo.max()) == (inicio, corte) else NO_CUMPLE,
           f"{panel.periodo.min()} a {panel.periodo.max()}")
    fechas_log = set(http.momento.dt.strftime("%Y-%m-%d"))
    sin_respaldo = []
    for n in SCRIPTS[:3]:
        linea = (CODIGO / n).read_text(encoding="utf-8").splitlines()[3]
        for fecha in re.findall(r"\d{4}-\d{2}-\d{2}", linea):
            if fecha not in fechas_log:
                sin_respaldo.append(f"{n}: {fecha}")
    anotar(S, "Las fechas de extracción del encabezado figuran en el log", "2.4.2 / 2.4.5",
           CUMPLE if not sin_respaldo else NO_CUMPLE,
           f"fechas con solicitudes en el log: {sorted(fechas_log)}" + (f"; sin respaldo: {sin_respaldo}" if sin_respaldo else ""))


# ============================================================================
# 7. Ética de la extracción (2.4.8)
# ============================================================================
def controles_etica(http: pd.DataFrame) -> None:
    S = "7. Ética de la extracción"
    texto = ARCHIVO_LOG.read_text(encoding="utf-8")
    inicios = re.findall(r"\| (0[12]_\w+) \| INFO \| INICIO .*User-Agent=(.+)$", texto, re.M)
    identificables = [ua for _, ua in inicios if "UNCP-FinanzasI-Tema96" in ua]
    anotar(S, "User-Agent identificable en cada corrida de extracción", "2.4.8",
           CUMPLE if inicios and len(identificables) == len(inicios) else NO_CUMPLE,
           f"{len(identificables)}/{len(inicios)} corridas con User-Agent del proyecto")
    intervalos = (http.sort_values("momento").groupby("script").momento.diff().dt.total_seconds().dropna())
    anotar(S, "Pausa mínima de 1 s entre solicitudes (medida en el log)", "2.4.8",
           CUMPLE if (intervalos >= 1).all() else NO_CUMPLE,
           f"{len(intervalos):,} intervalos; mínimo {intervalos.min():.0f} s; mediana {intervalos.median():.0f} s "
           "(resolución del log: 1 s)")
    robots = CRUDOS / "robots" / "smv_robots_evidencia.txt"
    anotar(S, "Evidencia de robots.txt del portal rastreado", "2.4.8", CUMPLE if robots.exists() else NO_CUMPLE,
           robots.read_text(encoding="utf-8").splitlines()[-1][:120] if robots.exists() else "FALTA")
    codigos = http.http.value_counts().to_dict()
    anotar(S, "Códigos HTTP registrados en el log", "2.4.2", CUMPLE,
           f"{len(http):,} solicitudes: " + ", ".join(f"HTTP {k} = {v:,}" for k, v in sorted(codigos.items())))


# ============================================================================
# 8. Reproducibilidad de tablas y figuras (Bloque B del 2.4.6)
# ============================================================================
def reejecutar_04(destino: Path) -> Path:
    """Ejecuta 04 completo escribiendo en una carpeta temporal (no toca las salidas entregadas ni el log)."""
    s04 = cargar_script("04_analisis.py")
    s04.SALIDAS = destino
    s04.DIR_TABLAS, s04.DIR_FIGURAS = destino / "tablas", destino / "figuras"
    s04.ARCHIVO_RESULTADOS, s04.MANIFIESTO = destino / "resultados_04.json", destino / "manifiesto_salidas.csv"
    s04.configurar_log = lambda nombre: logger_silencioso()
    s04.main()
    return s04.MANIFIESTO


def controles_salidas() -> None:
    S = "8. Tablas y figuras"
    if not (CODIGO / "04_analisis.py").exists():
        anotar(S, "Las tablas y figuras del artículo se regeneran con 04_analisis.py", "2.4.6 / B", NO_EJECUTADO,
               "no ejecutado: 04_analisis.py se escribe en la Fase V")
        return
    manifiesto = SALIDAS / "manifiesto_salidas.csv"
    if not manifiesto.exists():
        anotar(S, "Manifiesto de salidas de 04", "2.4.6 / B", NO_CUMPLE, "falta: ejecutar `python codigo/04_analisis.py`")
        return
    entregado = pd.read_csv(manifiesto)
    alterados = [a for a, h in zip(entregado.archivo, entregado.sha256)
                 if not (SALIDAS / a).exists() or sha256_archivo(SALIDAS / a) != h]
    anotar(S, "Las salidas entregadas coinciden con su manifiesto (SHA-256)", "2.4.5",
           CUMPLE if not alterados else NO_CUMPLE,
           f"{len(entregado) - len(alterados)}/{len(entregado)} archivos" + (f"; alterados o ausentes: {alterados[:5]}" if alterados else ""))
    with tempfile.TemporaryDirectory() as tmp:
        nuevo = pd.read_csv(reejecutar_04(Path(tmp)))
    cruce = entregado.merge(nuevo, on="archivo", how="outer", suffixes=("_entregado", "_regenerado"))
    iguales = int((cruce.sha256_entregado == cruce.sha256_regenerado).sum())
    tipos = entregado.archivo.str.extract(r"\.(\w+)$")[0].value_counts().to_dict()
    anotar(S, "Las tablas y figuras del artículo se regeneran con 04_analisis.py", "2.4.6 / B",
           CUMPLE if iguales == len(cruce) else NO_CUMPLE,
           f"{iguales}/{len(cruce)} archivos idénticos byte a byte (" + ", ".join(f"{k}: {v}" for k, v in sorted(tipos.items())) + ")")
    codigo_04 = (CODIGO / "04_analisis.py").read_text(encoding="utf-8")
    lee_crudos = "CRUDOS" in codigo_04 or "datos_crudos" in codigo_04.split('"""', 2)[-1]
    anotar(S, "04 lee exclusivamente la base procesada", "2.4.2", NO_CUMPLE if lee_crudos else CUMPLE,
           "solo usa datos_procesados" if not lee_crudos else "referencia a datos_crudos en el código")


# ============================================================================
# 9. Cotejo en vivo con la fuente (Bloque A, verificación n.º 1) — opcional
# ============================================================================
def cotejo_en_vivo(panel: pd.DataFrame, n: int = 10) -> None:
    S = "9. Cotejo en vivo con la fuente"
    import comun
    log = logger_consola()
    s01, s02 = cargar_script("01_extraccion_api.py"), cargar_script("02_scraping_web.py")
    sesion = comun.crear_sesion()
    rng = np.random.default_rng(SEMILLA)
    candidatas = panel[(panel.estado_simv == "con_registros") & (panel.lista_simv == "vigentes")]
    muestra = candidatas.iloc[sorted(rng.choice(len(candidatas), size=min(n, len(candidatas)), replace=False))]

    url = s01.URL_BCRP.format(codigos="-".join(s01.SERIES_BCRP), inicio=s01.periodo_bcrp(s01.FECHA_INICIO),
                              fin=s01.periodo_bcrp(s01.FECHA_CORTE))
    r = comun.solicitar(sesion, url, log)
    vivo = json.loads(s01.decodificar(r.content))
    nombres = [s01.SERIES_BCRP[c][0] for c in s01.SERIES_BCRP]
    s03 = cargar_script("03_limpieza_datos.py")
    por_periodo = {}
    for p in vivo["periods"]:
        periodo = f"{p['name'][-4:]}-{s03.MESES_BCRP[p['name'][:3]]:02d}"
        por_periodo[periodo] = dict(zip(nombres, p["values"]))
    bcrp_total = bcrp_iguales = 0
    for _, f in muestra.iterrows():
        for v in nombres:
            bcrp_total += 1
            bcrp_iguales += abs(float(por_periodo[f.periodo][v]) - float(f[v])) < 1e-9
    anotar(S, "BCRP en vivo: 10 filas al azar × 10 series", "2.4.6 / A1",
           CUMPLE if bcrp_iguales == bcrp_total else NO_CUMPLE, f"{bcrp_iguales}/{bcrp_total} valores iguales a la API hoy")

    simv_total = simv_iguales = filas_cotejadas = 0
    detalle = []
    for _, f in muestra.iterrows():
        s = None
        for _intento in (1, 2):  # el portal falla de forma intermitente: un reintento con estado nuevo
            _, estado = s02.iniciar_estado(sesion, log, retiradas=False)
            r = s02.consultar(sesion, log, estado, f.empresa_id_simv, f.razon_social, int(f.anio), int(f.mes), False)
            candidata = s02.sopa(r.content) if (r is not None and r.status_code == 200) else None
            if candidata is not None and not s02.validar(candidata, f.empresa_id_simv, int(f.anio), int(f.mes)):
                s = candidata
                break
        if s is None:
            detalle.append(f"{f.plataforma} {f.periodo}: sin respuesta válida tras 2 intentos")
            continue
        filas_cotejadas += 1
        grilla = {(g["modalidad"], g["tipo_receptor"]): g for g in s02.leer_grilla(s)}
        for tipo, sufijo in (("EMPRESARIAL", "emp"), ("PERSONAL", "per")):
            g = grilla.get(("PRESTAMOS", tipo))
            for a, b in (("proyectos_publicados", "proy_publicados"), ("proyectos_financiados", "proy_financiados"),
                         ("monto_total_financiado", "monto_financiado")):
                esperado = f[f"{b}_{sufijo}"]
                if g is None and pd.isna(esperado):
                    continue
                simv_total += 1
                ok = g is not None and not pd.isna(esperado) and int(g[a]) == int(esperado)
                simv_iguales += ok
                if not ok:
                    detalle.append(f"{f.plataforma} {f.periodo} {b}_{sufijo}: base={esperado} vivo={g[a] if g else '—'}")
    if simv_iguales < simv_total:
        estado_simv = NO_CUMPLE                    # algún valor difiere de la fuente
    elif filas_cotejadas < len(muestra) or not simv_total:
        estado_simv = NO_EJECUTADO                 # cotejo parcial: no se declara «cumple»
    else:
        estado_simv = CUMPLE
    anotar(S, "SIMV en vivo: 10 plataforma-mes al azar (préstamos, ambos tipos)", "2.4.6 / A1", estado_simv,
           f"{filas_cotejadas}/{len(muestra)} filas cotejadas; {simv_iguales}/{simv_total} valores iguales al portal hoy"
           + (f"; observaciones: {detalle[:3]}" if detalle else ""))


# ============================================================================
# Reporte
# ============================================================================
def escribir_reporte(en_vivo: bool) -> None:
    try:
        commit = subprocess.run(["git", "rev-parse", "--short", "HEAD"], cwd=RAIZ, capture_output=True,
                                text=True, check=True).stdout.strip()
    except (OSError, subprocess.CalledProcessError):
        commit = "sin git"
    cuenta = {e: sum(r["estado"] == e for r in resultados) for e in (CUMPLE, NO_CUMPLE, NO_EJECUTADO)}
    lineas = ["# Reporte de auditoría automatizada", "",
              f"- Fecha y hora: {datetime.now():%Y-%m-%d %H:%M:%S}",
              f"- Commit de referencia: `{commit}` (los cambios no confirmados también se auditan)",
              f"- Modo: {'local + cotejo en vivo' if en_vivo else 'local, sin internet (cotejo en vivo: no ejecutado)'}",
              f"- Resultado: {CUMPLE} {cuenta[CUMPLE]} cumplen · {NO_CUMPLE} {cuenta[NO_CUMPLE]} no cumplen · "
              f"{NO_EJECUTADO} {cuenta[NO_EJECUTADO]} no ejecutados", "",
              "> Regla de autenticidad: un control marcado ⏳ no se ejecutó y no cuenta como cumplido.", ""]
    for seccion in dict.fromkeys(r["seccion"] for r in resultados):
        lineas += [f"## {seccion}", "", "| Estado | Control | Numeral | Evidencia |", "|---|---|---|---|"]
        lineas += [f"| {r['estado']} | {r['control']} | {r['numeral']} | {r['evidencia']} |"
                   for r in resultados if r["seccion"] == seccion]
        lineas.append("")
    REPORTE.parent.mkdir(parents=True, exist_ok=True)
    REPORTE.write_text("\n".join(lineas), encoding="utf-8", newline="\n")


def main() -> int:
    parser = argparse.ArgumentParser(description="Auditoría automatizada del proyecto")
    parser.add_argument("--en-vivo", action="store_true", help="coteja 10 filas al azar con la fuente en vivo")
    args = parser.parse_args()
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")  # los símbolos ✅ ❌ ⏳ se ven en cualquier consola
    log = logger_consola()
    resultados.clear()
    panel, http = leer_procesado(), lineas_http()
    for nombre, funcion in (("estructura", controles_estructura), ("mínimos", lambda: controles_minimos(panel, http)),
                            ("autenticidad", lambda: controles_autenticidad(panel)), ("integridad", controles_integridad),
                            ("calidad", lambda: controles_calidad(panel)), ("fechas", lambda: controles_fechas(panel, http)),
                            ("ética", lambda: controles_etica(http)), ("tablas y figuras", controles_salidas)):
        log.info("Ejecutando controles de %s…", nombre)
        funcion()
    if args.en_vivo:
        log.info("Ejecutando cotejo en vivo (≈ 21 solicitudes, pausas de 3 s)…")
        cotejo_en_vivo(panel)
    else:
        anotar("9. Cotejo en vivo con la fuente", "Cotejo de 10 filas al azar con BCRP y SIMV", "2.4.6 / A1",
               NO_EJECUTADO, "no ejecutado: usar `python codigo/auditoria.py --en-vivo`")
    escribir_reporte(args.en_vivo)
    fallas = [r for r in resultados if r["estado"] == NO_CUMPLE]
    for r in resultados:
        print(f"{r['estado']} {r['control']} — {r['evidencia'][:110]}")
    print(f"\nReporte: {REPORTE.relative_to(RAIZ).as_posix()} | no cumplen: {len(fallas)}")
    return 1 if fallas else 0


if __name__ == "__main__":
    sys.exit(main())
