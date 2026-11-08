# Diego Sebastián Aliaga Damián
# 2024200481M
# Tema 96: Fintech y financiamiento participativo (crowdfunding) en el Perú: oferta y condiciones
# Fecha de extracción: 2026-11-07
"""01 — Extracción por API (vía 1 obligatoria de la Unidad II, numeral 2.4.1).

Fuente A — BCRPData (Banco Central de Reserva del Perú), API REST pública, sin clave.
    Endpoint: https://estadisticas.bcrp.gob.pe/estadisticas/series/api/{códigos}/json/{inicio}/{fin}
    Uso: tasas activas del sistema crediticio tradicional (comparador) e IPC.

Fuente B — SMV (Superintendencia del Mercado de Valores), API OData pública, sin clave.
    Endpoint: https://mvnet.smv.gob.pe/SMV.OData.Api/api/InfFinanciera/PrincipalCuentaSMV
              ?sEjercicio={AAAA}&sPeriodo={1-4}&sTipoInf=I
    Uso: estados financieros trimestrales de las sociedades administradoras de plataformas
    de financiamiento participativo (se guardan TODAS las filas; el filtro se hace en 03).

Salidas en datos_crudos/ (evidencia primaria, no se editan):
    bcrp/bcrp_series_mensuales.json                 respuesta original del BCRP
    smv_odata/principalcuenta_{AAAA}_T{n}.json      una respuesta original por trimestre
    datos_crudos_2024200481M_bcrp.csv               aplanado literal del JSON (valores como texto)
    datos_crudos_2024200481M_smv_odata.csv          aplanado literal de todas las filas recibidas

Ejecución (desde la raíz del proyecto):  python codigo/01_extraccion_api.py
"""
from __future__ import annotations

import json
import sys

import pandas as pd

from comun import (CODIGO_MATRICULA, CRUDOS, configurar_log, crear_sesion, guardar_atomico,
                   relativa, sha256_archivo, solicitar, user_agent)

# ============================================================================
# PARÁMETROS CONGELADOS DE LA CONSULTA (numeral 2.4.5: constantes, no fechas dinámicas)
# ============================================================================
FECHA_INICIO = "2021-01"
FECHA_CORTE = "2026-09"

URL_BCRP = "https://estadisticas.bcrp.gob.pe/estadisticas/series/api/{codigos}/json/{inicio}/{fin}"
URL_SMV = "https://mvnet.smv.gob.pe/SMV.OData.Api/api/InfFinanciera/PrincipalCuentaSMV"
TIPO_INFORMACION_SMV = "I"  # "I" = información individual (no consolidada)

# Código BCRP -> (nombre de variable, palabras que deben aparecer en el nombre oficial devuelto).
# La validación por nombre impide usar una serie equivocada si un código cambiara.
SERIES_BCRP = {
    "PN07807NM": ("tamn", ["TAMN"]),
    "PN07843NM": ("tea_bcos_pyme_360", ["empresas bancarias", "Pequeña y Microempresa", "Hasta 360"]),
    "PN07844NM": ("tea_bcos_pyme_mas360", ["empresas bancarias", "Pequeña y Microempresa", "Más 360"]),
    "PN07846NM": ("tea_bcos_consumo_360", ["empresas bancarias", "Consumo", "Hasta 360"]),
    "PN07847NM": ("tea_bcos_consumo_mas360", ["empresas bancarias", "Consumo", "Más 360"]),
    "PN07861NM": ("tea_cmac_pyme_360", ["cajas municipales", "Pequeña y Microempresa", "Hasta 360"]),
    "PN07862NM": ("tea_cmac_pyme_mas360", ["cajas municipales", "Pequeña y Microempresa", "Más 360"]),
    "PN07879NM": ("tea_crac_pyme_360", ["cajas rurales", "Pequeña y Microempresa", "Hasta 360"]),
    "PN07880NM": ("tea_crac_pyme_mas360", ["cajas rurales", "Pequeña y Microempresa", "Más 360"]),
    "PN38705PM": ("ipc", ["precios"]),
}

# Columnas que toda fila de la API SMV debe traer para ser útil al estudio.
COLUMNAS_SMV = {"RUC", "TipoEmpresa", "NombreEmpresa", "Ejercicio", "Trimestre", "Moneda",
                "ActivoTotal", "PasivoTotal", "PatrimonioTotal", "TotalIngreso", "UtilidadNeta"}

DIR_BCRP = CRUDOS / "bcrp"
DIR_SMV = CRUDOS / "smv_odata"
CRUDO_BCRP = DIR_BCRP / "bcrp_series_mensuales.json"
CSV_BCRP = CRUDOS / f"datos_crudos_{CODIGO_MATRICULA}_bcrp.csv"
CSV_SMV = CRUDOS / f"datos_crudos_{CODIGO_MATRICULA}_smv_odata.csv"


# ============================================================================
# BLOQUE A — BCRPData
# ============================================================================
def periodo_bcrp(aaaa_mm: str) -> str:
    """'2021-01' -> '2021-1' (formato que espera la API del BCRP)."""
    anio, mes = aaaa_mm.split("-")
    return f"{anio}-{int(mes)}"


def decodificar(contenido: bytes) -> str:
    """La API del BCRP declara text/html; el cuerpo es JSON en UTF-8 (con respaldo latin-1)."""
    try:
        return contenido.decode("utf-8")
    except UnicodeDecodeError:
        return contenido.decode("latin-1")


def validar_bcrp(datos: dict) -> list[str]:
    """Devuelve la lista de problemas; vacía si la respuesta es válida."""
    problemas = []
    series = datos.get("config", {}).get("series", [])
    periodos = datos.get("periods", [])
    if len(series) != len(SERIES_BCRP):
        problemas.append(f"se esperaban {len(SERIES_BCRP)} series y llegaron {len(series)}")
    if not periodos:
        problemas.append("la respuesta no trae periodos")
    for codigo, serie in zip(SERIES_BCRP, series):
        nombre = serie.get("name", "").lower()
        faltan = [p for p in SERIES_BCRP[codigo][1] if p.lower() not in nombre]
        if faltan:
            problemas.append(f"{codigo}: el nombre oficial no contiene {faltan} -> '{serie.get('name')}'")
    for p in periodos:
        if len(p.get("values", [])) != len(SERIES_BCRP):
            problemas.append(f"periodo {p.get('name')}: número de valores distinto al de series")
            break
    return problemas


def extraer_bcrp(sesion, log) -> bool:
    url = URL_BCRP.format(codigos="-".join(SERIES_BCRP), inicio=periodo_bcrp(FECHA_INICIO),
                          fin=periodo_bcrp(FECHA_CORTE))
    r = solicitar(sesion, url, log)
    if r is None or r.status_code != 200:
        log.error("BCRP | descarga fallida; se conserva el crudo anterior si existe")
        return False
    try:
        datos = json.loads(decodificar(r.content))
    except json.JSONDecodeError:
        log.error("BCRP | la respuesta no es JSON (posible página de error o anti-bot); no se guarda")
        return False
    problemas = validar_bcrp(datos)
    if problemas:
        for p in problemas:
            log.error("BCRP | VALIDACION | %s", p)
        return False
    huella = guardar_atomico(CRUDO_BCRP, r.content)  # se guardan los bytes tal como llegaron
    log.info("BCRP | OK | series=%d | periodos=%d | archivo=%s | sha256=%s",
             len(datos["config"]["series"]), len(datos["periods"]), relativa(CRUDO_BCRP), huella)
    return True


def csv_bcrp(log) -> None:
    """Aplana el JSON guardado sin transformar valores (quedan como texto, incluido 'n.d.')."""
    datos = json.loads(decodificar(CRUDO_BCRP.read_bytes()))
    nombres = [s["name"] for s in datos["config"]["series"]]
    filas = [{"codigo_serie": codigo, "nombre_serie": nombre, "periodo_bcrp": p["name"], "valor": valor}
             for p in datos["periods"]
             for codigo, nombre, valor in zip(SERIES_BCRP, nombres, p["values"])]
    # Fin de línea LF fijo: el archivo (y su SHA-256) es idéntico en Windows, macOS o Linux.
    pd.DataFrame(filas).to_csv(CSV_BCRP, index=False, encoding="utf-8", lineterminator="\n")
    log.info("BCRP | CSV crudo | filas=%d | archivo=%s | sha256=%s",
             len(filas), relativa(CSV_BCRP), sha256_archivo(CSV_BCRP))


# ============================================================================
# BLOQUE B — SMV, API OData de información financiera
# ============================================================================
def trimestres_consulta() -> list[tuple[int, int]]:
    """Pares (ejercicio, trimestre) desde FECHA_INICIO hasta el trimestre de FECHA_CORTE."""
    a0, m0 = map(int, FECHA_INICIO.split("-"))
    a1, m1 = map(int, FECHA_CORTE.split("-"))
    pares = []
    for anio in range(a0, a1 + 1):
        for trimestre in range(1, 5):
            inicio_trim, fin_trim = 3 * trimestre - 2, 3 * trimestre
            if (anio, fin_trim) < (a0, m0) or (anio, inicio_trim) > (a1, m1):
                continue
            pares.append((anio, trimestre))
    return pares


def validar_smv(datos) -> list[str]:
    if not isinstance(datos, dict) or datos.get("ResponseCode") != "OK":
        return [f"ResponseCode distinto de OK: {datos.get('ResponseCode') if isinstance(datos, dict) else type(datos)}"]
    filas = datos.get("data")
    if not isinstance(filas, list):
        return ["el campo 'data' no es una lista"]
    if filas and not COLUMNAS_SMV.issubset(filas[0]):
        return [f"faltan columnas: {sorted(COLUMNAS_SMV - set(filas[0]))}"]
    return []


def extraer_smv(sesion, log) -> bool:
    todo_ok = True
    for anio, trimestre in trimestres_consulta():
        destino = DIR_SMV / f"principalcuenta_{anio}_T{trimestre}.json"
        parametros = {"sEjercicio": anio, "sPeriodo": trimestre, "sTipoInf": TIPO_INFORMACION_SMV}
        r = solicitar(sesion, URL_SMV, log, params=parametros)
        if r is None or r.status_code != 200:
            log.error("SMV | %d-T%d | descarga fallida; se conserva el crudo anterior", anio, trimestre)
            todo_ok = False
            continue
        try:
            datos = r.json()
        except ValueError:
            log.error("SMV | %d-T%d | la respuesta no es JSON; no se guarda", anio, trimestre)
            todo_ok = False
            continue
        problemas = validar_smv(datos)
        if problemas:
            log.error("SMV | %d-T%d | VALIDACION | %s", anio, trimestre, "; ".join(problemas))
            todo_ok = False
            continue
        filas = len(datos["data"])
        if filas == 0 and destino.exists():
            # Una respuesta vacía nunca reemplaza un crudo que ya tenía filas.
            log.warning("SMV | %d-T%d | respuesta vacía; se conserva el crudo previo", anio, trimestre)
            continue
        huella = guardar_atomico(destino, r.content)
        pfp = sum("PARTICIPATIVO" in str(f.get("TipoEmpresa", "")).upper() for f in datos["data"])
        log.info("SMV | %d-T%d | OK | filas=%d | filas_PFP=%d | archivo=%s | sha256=%s",
                 anio, trimestre, filas, pfp, relativa(destino), huella)
    return todo_ok


def csv_smv(log) -> None:
    """Une todas las respuestas guardadas, sin alterar valores; añade solo el nombre del crudo de origen."""
    marcos = []
    for archivo in sorted(DIR_SMV.glob("principalcuenta_*.json")):
        filas = json.loads(archivo.read_bytes()).get("data", [])
        if filas:
            df = pd.DataFrame(filas, dtype=str)
            df["_archivo_crudo"] = archivo.name
            marcos.append(df)
    total = pd.concat(marcos, ignore_index=True)
    total.to_csv(CSV_SMV, index=False, encoding="utf-8", lineterminator="\n")
    log.info("SMV | CSV crudo | filas=%d | columnas=%d | archivo=%s | sha256=%s",
             len(total), total.shape[1], relativa(CSV_SMV), sha256_archivo(CSV_SMV))


# ============================================================================
# EJECUCIÓN
# ============================================================================
def main() -> int:
    log = configurar_log("01_extraccion_api")
    log.info("INICIO | FECHA_INICIO=%s | FECHA_CORTE=%s | User-Agent=%s", FECHA_INICIO, FECHA_CORTE, user_agent())
    sesion = crear_sesion()
    ok_bcrp = extraer_bcrp(sesion, log)
    ok_smv = extraer_smv(sesion, log)
    if CRUDO_BCRP.exists():
        csv_bcrp(log)
    if any(DIR_SMV.glob("principalcuenta_*.json")):
        csv_smv(log)
    log.info("FIN | BCRP=%s | SMV=%s", "OK" if ok_bcrp else "CON ERRORES", "OK" if ok_smv else "CON ERRORES")
    return 0 if (ok_bcrp and ok_smv) else 1


if __name__ == "__main__":
    sys.exit(main())
