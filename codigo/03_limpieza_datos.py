# Diego Sebastián Aliaga Damián
# 2024200481M
# Tema 96: Fintech y financiamiento participativo (crowdfunding) en el Perú: oferta y condiciones
# Fecha de extracción: 2026-11-07 (censo) y 2026-11-08 (reanudación)
"""03 — Limpieza, tipificación e integración de las fuentes (numeral 2.4.2).

Entradas (solo datos_crudos/; este script no se conecta a internet):
    datos_crudos_2024200481M_smv_simv.csv       (02) proyectos por plataforma y mes
    smv_simv/lista_vigentes.html, lista_retiradas.html   (02) catálogo de plataformas del SIMV
    datos_crudos_2024200481M_smv_odata.csv      (01) estados financieros trimestrales
    datos_crudos_2024200481M_bcrp.csv           (01) tasas activas mensuales e IPC

Salidas:
    datos_procesados/datos_procesados_2024200481M.csv   panel plataforma × mes (6 × 69 = 414 filas)
    diccionario_variables.md                             generado desde este mismo código
    salidas/reporte_limpieza.md                          controles, faltantes, atípicos y transformaciones

Unidad de análisis: plataforma-mes. Llave común: ruc + periodo (AAAA-MM).

Transformaciones (todas se registran en el reporte):
    1. Nombres de variables normalizados (minúsculas, sin tildes, con guion bajo).
    2. Tipos: conteos y montos del SIMV -> entero; EEFF -> decimal (miles de S/); tasas e IPC -> decimal.
    3. SIMV: de «una fila por modalidad y tipo» a columnas por tipo de receptor. La fila TOTAL del portal
       solo se usa como control (TOTAL = suma de tipos).
    4. Faltantes: los meses «sin registros» y los «no obtenidos» quedan vacíos; nunca se imputan.
    5. Frecuencia: los EEFF trimestrales se asignan al mes de cierre del trimestre; no se interpola.
    6. BCRP: 'Ene.2021' -> '2021-01'; el valor del mes se repite para cada plataforma.
    7. Atípicos: se identifican y se reportan; no se eliminan, porque son datos oficiales.

Ejecución (desde la raíz del proyecto):  python codigo/03_limpieza_datos.py
"""
from __future__ import annotations

import sys

import numpy as np
import pandas as pd
from bs4 import BeautifulSoup

from comun import CODIGO_MATRICULA, CRUDOS, PROCESADOS, RAIZ, SALIDAS, configurar_log, relativa, sha256_archivo

# ============================================================================
# PARÁMETROS (deben coincidir con 01 y 02)
# ============================================================================
FECHA_INICIO = "2021-01"
FECHA_CORTE = "2026-09"

CSV_SIMV = CRUDOS / f"datos_crudos_{CODIGO_MATRICULA}_smv_simv.csv"
CSV_ODATA = CRUDOS / f"datos_crudos_{CODIGO_MATRICULA}_smv_odata.csv"
CSV_BCRP = CRUDOS / f"datos_crudos_{CODIGO_MATRICULA}_bcrp.csv"
LISTAS_SIMV = {"vigentes": CRUDOS / "smv_simv" / "lista_vigentes.html",
               "retiradas": CRUDOS / "smv_simv" / "lista_retiradas.html"}
CSV_PROCESADO = PROCESADOS / f"datos_procesados_{CODIGO_MATRICULA}.csv"
DICCIONARIO = RAIZ / "diccionario_variables.md"
REPORTE = SALIDAS / "reporte_limpieza.md"

URL_SIMV = "https://www.smv.gob.pe/SIMV/Frm_ProyectosFPF?data=785FE29A0201FCD759A08F94A0F74DBB4FD1B4D805"
URL_ODATA = ("https://mvnet.smv.gob.pe/SMV.OData.Api/api/InfFinanciera/PrincipalCuentaSMV"
             "?sEjercicio={AAAA}&sPeriodo={1-4}&sTipoInf=I")
URL_BCRP = "https://estadisticas.bcrp.gob.pe/estadisticas/series/api/{código}/json/2021-1/2026-9"

MESES_BCRP = {"Ene": 1, "Feb": 2, "Mar": 3, "Abr": 4, "May": 5, "Jun": 6,
              "Jul": 7, "Ago": 8, "Sep": 9, "Oct": 10, "Nov": 11, "Dic": 12}

# Código BCRP -> nombre de variable (los mismos de 01_extraccion_api.py)
SERIES_BCRP = {"PN07807NM": "tamn", "PN07843NM": "tea_bcos_pyme_360", "PN07844NM": "tea_bcos_pyme_mas360",
               "PN07846NM": "tea_bcos_consumo_360", "PN07847NM": "tea_bcos_consumo_mas360",
               "PN07861NM": "tea_cmac_pyme_360", "PN07862NM": "tea_cmac_pyme_mas360",
               "PN07879NM": "tea_crac_pyme_360", "PN07880NM": "tea_crac_pyme_mas360", "PN38705PM": "ipc"}

# Nombre corto de cada sociedad administradora (etiqueta para tablas y figuras; la razón social completa se conserva)
NOMBRE_CORTO = {"20605667351": "Inversiones.io", "20566550939": "Afluenta", "20610079394": "Inversiones Neurona",
                "20610205501": "Proyecto Crowd", "20612782513": "Prestopolis", "20614384213": "Securite"}

TIPOS = {"EMPRESARIAL": "emp", "PERSONAL": "per"}
VARIABLES_SIMV = {"proyectos_publicados": "proy_publicados", "proyectos_financiados": "proy_financiados",
                  "monto_total_financiado": "monto_financiado"}
VARIABLES_EEFF = {"ActivoTotal": "activo_total_miles", "PasivoTotal": "pasivo_total_miles",
                  "PatrimonioTotal": "patrimonio_total_miles", "TotalIngreso": "ingresos_totales_miles",
                  "UtilidadNeta": "utilidad_neta_miles"}

controles: list[str] = []          # líneas del reporte de limpieza
transformaciones: list[str] = []


def registrar(log, texto: str, nivel: str = "info") -> None:
    getattr(log, nivel)("CONTROL | " + texto)
    controles.append(("⚠️ " if nivel != "info" else "✅ ") + texto)


def periodos() -> list[str]:
    inicio, fin = pd.Period(FECHA_INICIO, "M"), pd.Period(FECHA_CORTE, "M")
    return [str(p) for p in pd.period_range(inicio, fin, freq="M")]


# ============================================================================
# BLOQUE 1 — Catálogo de plataformas y llave RUC
# ============================================================================
def leer_catalogo(log) -> pd.DataFrame:
    """Lee las listas del SIMV (tal como llegaron) y obtiene id, razón social y lista."""
    filas = []
    for lista, ruta in LISTAS_SIMV.items():
        selector = BeautifulSoup(ruta.read_bytes(), "html.parser").select_one(
            'select[name="ctl00$MainContent$cboDenominacionSocial"]')
        for opcion in selector.select("option"):
            if opcion.get("value") != "-1":
                filas.append({"empresa_id_simv": opcion.get("value"),
                              "razon_social": opcion.get_text(strip=True), "lista_simv": lista})
    catalogo = pd.DataFrame(filas)
    registrar(log, f"Catálogo del SIMV: {len(catalogo)} plataformas "
                   f"({(catalogo.lista_simv == 'vigentes').sum()} vigentes, {(catalogo.lista_simv == 'retiradas').sum()} retiradas)")
    return catalogo


def asignar_ruc(catalogo: pd.DataFrame, eeff: pd.DataFrame, log) -> pd.DataFrame:
    """Une el catálogo del SIMV con el RUC de la API OData por razón social idéntica (ambas son de la SMV)."""
    nombres = eeff.drop_duplicates("ruc").set_index("razon_social")["ruc"]
    catalogo = catalogo.assign(ruc=catalogo.razon_social.map(nombres))
    faltan = catalogo[catalogo.ruc.isna()]
    if not faltan.empty:
        raise ValueError(f"Plataformas del SIMV sin RUC en la API OData: {faltan.razon_social.tolist()}")
    if catalogo.ruc.duplicated().any() or set(catalogo.ruc) != set(eeff.ruc):
        raise ValueError("El cruce SIMV-OData no es uno a uno; revisar razones sociales")
    catalogo["plataforma"] = catalogo.ruc.map(NOMBRE_CORTO)
    registrar(log, f"Llave RUC: {len(catalogo)}/{len(catalogo)} plataformas del SIMV cruzadas uno a uno con la API OData "
                   "por razón social idéntica")
    return catalogo


# ============================================================================
# BLOQUE 2 — SIMV: proyectos por plataforma y mes
# ============================================================================
def preparar_simv(log) -> pd.DataFrame:
    s = pd.read_csv(CSV_SIMV, dtype=str)
    s["periodo"] = s.anio + "-" + s.mes.str.zfill(2)
    con = s[s.resultado == "con_registros"].copy()
    for col in VARIABLES_SIMV:
        con[col] = pd.to_numeric(con[col], errors="raise").astype("int64")
    transformaciones.append("SIMV: conteos y montos convertidos de texto a entero; el monto está en soles corrientes (S/).")

    # Control: en cada consulta con registros, TOTAL = suma de todas las filas de detalle
    detalle = con[con.modalidad != "TOTAL"].groupby(["empresa_id", "periodo"])[list(VARIABLES_SIMV)].sum()
    total = con[con.modalidad == "TOTAL"].set_index(["empresa_id", "periodo"])[list(VARIABLES_SIMV)]
    diferencias = (detalle.reindex(total.index) - total).abs().sum(axis=1)
    if (diferencias != 0).any():
        raise ValueError(f"TOTAL distinto de la suma de tipos en {int((diferencias != 0).sum())} consultas")
    registrar(log, f"SIMV: TOTAL = suma de tipos de receptor en {len(total)}/{len(total)} consultas con registros")

    # Préstamos: columnas por tipo de receptor
    prestamos = con[con.modalidad == "PRESTAMOS"].copy()
    prestamos["tipo"] = prestamos.tipo_receptor.map(TIPOS)
    ancho = prestamos.pivot_table(index=["empresa_id", "periodo"], columns="tipo",
                                  values=list(VARIABLES_SIMV), aggfunc="sum")
    ancho.columns = [f"{VARIABLES_SIMV[v]}_{t}" for v, t in ancho.columns]

    # Valores: se suman ambos tipos en columnas propias (en el periodo solo aparece con ceros)
    valores = (con[con.modalidad == "VALORES"].groupby(["empresa_id", "periodo"])[list(VARIABLES_SIMV)].sum()
               .rename(columns={k: f"{v}_valores" for k, v in VARIABLES_SIMV.items()}))
    registrar(log, f"SIMV: modalidad VALORES en {len(valores)} consultas; monto financiado total = "
                   f"S/ {int(valores.filter(like='monto').sum().sum()):,}")
    otras = set(con.modalidad) - {"PRESTAMOS", "VALORES", "TOTAL"}
    if otras:
        raise ValueError(f"Modalidades no previstas en el SIMV: {otras}")
    transformaciones.append("SIMV: préstamos en columnas por tipo de receptor (_emp, _per); valores en columnas "
                            "_valores (suma de tipos); la fila TOTAL se usa solo como control.")

    estado = s.drop_duplicates(["empresa_id", "periodo"]).set_index(["empresa_id", "periodo"])["resultado"]
    simv = ancho.join(valores, how="outer").join(estado.rename("estado_simv"), how="outer").reset_index()
    return simv.rename(columns={"empresa_id": "empresa_id_simv"})


# ============================================================================
# BLOQUE 3 — SMV OData: estados financieros trimestrales de las sociedades administradoras
# ============================================================================
def preparar_eeff(log) -> pd.DataFrame:
    o = pd.read_csv(CSV_ODATA, dtype=str)
    o = o[o.TipoEmpresa.str.contains("PARTICIPATIVO", na=False)].copy()
    if o.duplicated(["RUC", "Ejercicio", "Trimestre"]).any():
        raise ValueError("EEFF duplicados para un mismo RUC y trimestre")
    if set(o.Moneda) != {"Soles"}:
        raise ValueError(f"Monedas no previstas en los EEFF: {set(o.Moneda)}")
    trimestre = o.Trimestre.str[0].astype(int)  # '1er Trimestre' -> 1
    o["trimestre_eeff"] = o.Ejercicio + "-T" + trimestre.astype(str)
    o["periodo"] = o.Ejercicio + "-" + (3 * trimestre).astype(str).str.zfill(2)  # mes de cierre del trimestre
    for origen, destino in VARIABLES_EEFF.items():
        o[destino] = pd.to_numeric(o[origen], errors="raise").astype(float)
    o["fecha_registro_eeff"] = pd.to_datetime(o.FechaRegistro, format="%d/%m/%Y").dt.strftime("%Y-%m-%d")
    transformaciones.append("EEFF (SMV OData): solo sociedades administradoras de plataformas de FPF; moneda única "
                            "(soles); montos en miles de S/; cada trimestre se asigna a su mes de cierre "
                            "(mar, jun, sep, dic); los demás meses quedan vacíos (no se interpola).")
    # Control contable: activo = pasivo + patrimonio (tolerancia de 1 mil por redondeo)
    brecha = (o.activo_total_miles - o.pasivo_total_miles - o.patrimonio_total_miles).abs()
    registrar(log, f"EEFF: identidad activo = pasivo + patrimonio se cumple (±1 mil S/) en "
                   f"{int((brecha <= 1).sum())}/{len(o)} trimestres",
              "info" if (brecha <= 1).all() else "warning")
    registrar(log, f"EEFF: {len(o)} trimestres de {o.RUC.nunique()} sociedades administradoras "
                   f"({o.trimestre_eeff.min()} a {o.trimestre_eeff.max()})")
    columnas = ["RUC", "NombreEmpresa", "periodo", "trimestre_eeff", *VARIABLES_EEFF.values(), "fecha_registro_eeff"]
    return o[columnas].rename(columns={"RUC": "ruc", "NombreEmpresa": "razon_social"})


# ============================================================================
# BLOQUE 4 — BCRP: tasas activas e IPC
# ============================================================================
def preparar_bcrp(log) -> pd.DataFrame:
    b = pd.read_csv(CSV_BCRP, dtype=str)
    if set(b.codigo_serie) != set(SERIES_BCRP):
        raise ValueError(f"Series del BCRP distintas de las previstas: {set(b.codigo_serie) ^ set(SERIES_BCRP)}")
    mes = b.periodo_bcrp.str[:3].map(MESES_BCRP)
    if mes.isna().any():
        raise ValueError(f"Meses del BCRP no reconocidos: {b.periodo_bcrp[mes.isna()].unique()}")
    b["periodo"] = b.periodo_bcrp.str[-4:] + "-" + mes.astype(int).astype(str).str.zfill(2)
    b["valor"] = pd.to_numeric(b.valor.replace("n.d.", np.nan), errors="raise")
    ancho = b.pivot(index="periodo", columns="codigo_serie", values="valor").rename(columns=SERIES_BCRP)
    ancho = ancho[list(SERIES_BCRP.values())].reset_index()
    transformaciones.append("BCRP: periodo 'Ene.2021' -> '2021-01'; 'n.d.' -> vacío; tasas en % (TEA) e IPC "
                            "(dic. 2021 = 100) como decimales; el valor de cada mes se repite para todas las plataformas.")
    registrar(log, f"BCRP: {ancho.shape[1] - 1} series × {len(ancho)} meses ({ancho.periodo.min()} a {ancho.periodo.max()}); "
                   f"valores faltantes = {int(ancho.isna().sum().sum())}")
    return ancho


# ============================================================================
# BLOQUE 5 — Integración por la llave común y controles
# ============================================================================
def integrar(catalogo, simv, eeff, bcrp, log) -> pd.DataFrame:
    meses = periodos()
    if sorted(bcrp.periodo) != meses:
        raise ValueError("Los meses del BCRP no coinciden con FECHA_INICIO-FECHA_CORTE")
    base = catalogo.merge(pd.DataFrame({"periodo": meses}), how="cross")  # panel balanceado
    panel = (base.merge(simv, on=["empresa_id_simv", "periodo"], how="left", validate="one_to_one")
                 .merge(eeff.drop(columns="razon_social"), on=["ruc", "periodo"], how="left", validate="one_to_one")
                 .merge(bcrp, on="periodo", how="left", validate="many_to_one"))
    fuera = set(zip(eeff.ruc, eeff.periodo)) - set(zip(panel.ruc, panel.periodo))
    if fuera:
        raise ValueError(f"EEFF fuera del panel (RUC y periodo sin fila): {sorted(fuera)[:5]}")
    panel["estado_simv"] = panel.estado_simv.fillna("no_obtenido")
    panel["anio"] = panel.periodo.str[:4].astype(int)
    panel["mes"] = panel.periodo.str[5:].astype(int)
    transformaciones.append("Integración: panel balanceado plataforma × mes (llave ruc + periodo). SIMV por "
                            "empresa_id_simv y periodo; EEFF por ruc y periodo; BCRP por periodo. "
                            "estado_simv = con_registros | sin_registros | no_obtenido.")
    # Controles de la llave
    if panel.duplicated(["ruc", "periodo"]).any():
        raise ValueError("Llave ruc + periodo duplicada en el panel")
    if len(panel) != len(catalogo) * len(meses):
        raise ValueError("El panel no está balanceado")
    registrar(log, f"Panel: {len(panel)} filas = {len(catalogo)} plataformas × {len(meses)} meses; llave ruc + periodo única")
    registrar(log, "estado_simv: " + ", ".join(f"{k}={v}" for k, v in panel.estado_simv.value_counts().items()))
    registrar(log, f"EEFF integrados: {panel.trimestre_eeff.notna().sum()}/{len(eeff)} trimestres")
    columnas = (["periodo", "anio", "mes", "ruc", "empresa_id_simv", "plataforma", "razon_social", "lista_simv",
                 "estado_simv"]
                + [f"{v}_{t}" for t in ("emp", "per") for v in VARIABLES_SIMV.values()]
                + [f"{v}_valores" for v in VARIABLES_SIMV.values()]
                + ["trimestre_eeff", *VARIABLES_EEFF.values(), "fecha_registro_eeff"]
                + list(SERIES_BCRP.values()))
    for c in columnas:  # columnas que no aparecieron (p. ej., ningún dato de un tipo) se crean vacías
        if c not in panel:
            panel[c] = np.nan
    enteros = [c for c in columnas if c.startswith(("proy_", "monto_"))]
    panel[enteros] = panel[enteros].astype("Int64")  # entero que admite vacío
    return panel[columnas].sort_values(["ruc", "periodo"]).reset_index(drop=True)


def detectar_atipicos(panel: pd.DataFrame, log) -> list[str]:
    """Regla de Tukey (fuera de Q1 - 3·RIC y Q3 + 3·RIC). Solo se reporta; no se elimina ningún dato."""
    hallazgos = []
    activos = panel[panel.proy_financiados_emp.fillna(0) > 0]
    monto_proyecto = (activos.monto_financiado_emp / activos.proy_financiados_emp).astype(float)
    q1, q3 = monto_proyecto.quantile([0.25, 0.75])
    fuera = activos[(monto_proyecto < q1 - 3 * (q3 - q1)) | (monto_proyecto > q3 + 3 * (q3 - q1))]
    for _, f in fuera.iterrows():
        hallazgos.append(f"{f.plataforma} {f.periodo}: monto por proyecto empresarial = "
                         f"S/ {f.monto_financiado_emp / f.proy_financiados_emp:,.0f}")
    bcrp = panel.drop_duplicates("periodo").set_index("periodo")[[v for v in SERIES_BCRP.values() if v != "ipc"]]
    cambios = bcrp.diff()
    for serie in cambios:
        c = cambios[serie].dropna()
        q1, q3 = c.quantile([0.25, 0.75])
        for periodo, valor in c[(c < q1 - 3 * (q3 - q1)) | (c > q3 + 3 * (q3 - q1))].items():
            hallazgos.append(f"{serie} {periodo}: cambio mensual de {valor:+.2f} puntos porcentuales")
    registrar(log, f"Atípicos (Tukey, 3·RIC): {len(hallazgos)} identificados; se conservan (datos oficiales)")
    return hallazgos


# ============================================================================
# BLOQUE 6 — Diccionario de variables y reporte
# ============================================================================
def diccionario() -> list[dict]:
    e_simv = f"SMV, SIMV «Información de Proyectos» ({URL_SIMV})"
    e_eeff = f"SMV, API OData PrincipalCuentaSMV ({URL_ODATA})"
    filas = [
        ("periodo", "Mes de referencia (AAAA-MM). Llave común", "—", "Mensual", "Construida a partir de cada fuente"),
        ("anio", "Año del periodo", "—", "Mensual", "Derivada de periodo"),
        ("mes", "Mes del periodo (1-12)", "—", "Mensual", "Derivada de periodo"),
        ("ruc", "RUC de la sociedad administradora. Llave común", "—", "—", e_eeff + ", campo RUC"),
        ("empresa_id_simv", "Código de la empresa en el formulario del SIMV", "—", "—", e_simv),
        ("plataforma", "Nombre corto de la plataforma (etiqueta asignada por el autor)", "—", "—", "Derivada de razon_social"),
        ("razon_social", "Razón social de la sociedad administradora", "—", "—", e_simv + "; idéntica en " + e_eeff),
        ("lista_simv", "Lista del SIMV en que figura: vigentes o retiradas", "—", "—", e_simv),
        ("estado_simv", "Resultado de la consulta: con_registros, sin_registros (el portal no reporta datos) o "
                        "no_obtenido (sin respuesta válida; ver incidencias_fuente.md)", "—", "Mensual", e_simv),
    ]
    for t, nombre in (("emp", "empresariales"), ("per", "personales")):
        filas += [
            (f"proy_publicados_{t}", f"Proyectos de préstamo {nombre} publicados en la plataforma en el mes", "proyectos", "Mensual", e_simv),
            (f"proy_financiados_{t}", f"Proyectos de préstamo {nombre} publicados que fueron financiados", "proyectos", "Mensual", e_simv),
            (f"monto_financiado_{t}", f"Monto total financiado de proyectos de préstamo {nombre}", "soles corrientes (S/)", "Mensual", e_simv),
        ]
    filas += [
        ("proy_publicados_valores", "Proyectos publicados en la modalidad valores (todos los receptores)", "proyectos", "Mensual", e_simv),
        ("proy_financiados_valores", "Proyectos financiados en la modalidad valores", "proyectos", "Mensual", e_simv),
        ("monto_financiado_valores", "Monto financiado en la modalidad valores", "soles corrientes (S/)", "Mensual", e_simv),
        ("trimestre_eeff", "Trimestre del estado financiero (AAAA-Tn), asignado a su mes de cierre", "—", "Trimestral", e_eeff),
        ("activo_total_miles", "Activo total de la sociedad administradora", "miles de S/", "Trimestral", e_eeff + ", campo ActivoTotal"),
        ("pasivo_total_miles", "Pasivo total", "miles de S/", "Trimestral", e_eeff + ", campo PasivoTotal"),
        ("patrimonio_total_miles", "Patrimonio total", "miles de S/", "Trimestral", e_eeff + ", campo PatrimonioTotal"),
        ("ingresos_totales_miles", "Ingresos totales del periodo informado", "miles de S/", "Trimestral", e_eeff + ", campo TotalIngreso"),
        ("utilidad_neta_miles", "Utilidad neta del periodo informado", "miles de S/", "Trimestral", e_eeff + ", campo UtilidadNeta"),
        ("fecha_registro_eeff", "Fecha en que la empresa registró el estado financiero en la SMV", "fecha (AAAA-MM-DD)", "Trimestral", e_eeff + ", campo FechaRegistro"),
    ]
    etiquetas = {"tamn": "Tasa activa promedio en moneda nacional (TAMN), empresas bancarias",
                 "tea_bcos_pyme_360": "TEA de préstamos a pequeña y microempresa hasta 360 días, empresas bancarias, MN",
                 "tea_bcos_pyme_mas360": "TEA de préstamos a pequeña y microempresa a más de 360 días, empresas bancarias, MN",
                 "tea_bcos_consumo_360": "TEA de préstamos de consumo hasta 360 días, empresas bancarias, MN",
                 "tea_bcos_consumo_mas360": "TEA de préstamos de consumo a más de 360 días, empresas bancarias, MN",
                 "tea_cmac_pyme_360": "TEA de préstamos a pequeña y microempresa hasta 360 días, cajas municipales, MN",
                 "tea_cmac_pyme_mas360": "TEA de préstamos a pequeña y microempresa a más de 360 días, cajas municipales, MN",
                 "tea_crac_pyme_360": "TEA de préstamos a pequeña y microempresa hasta 360 días, cajas rurales, MN",
                 "tea_crac_pyme_mas360": "TEA de préstamos a pequeña y microempresa a más de 360 días, cajas rurales, MN",
                 "ipc": "Índice de precios al consumidor de Lima Metropolitana (dic. 2021 = 100)"}
    for codigo, nombre in SERIES_BCRP.items():
        unidad = "índice" if nombre == "ipc" else "% (tasa efectiva anual)"
        filas.append((nombre, etiquetas[nombre], unidad, "Mensual",
                      f"BCRP, BCRPData, serie {codigo} ({URL_BCRP.replace('{código}', codigo)})"))
    return [dict(zip(["variable", "definicion", "unidad", "frecuencia", "fuente"], f)) for f in filas]


def escribir_diccionario(panel: pd.DataFrame, log) -> None:
    dic = diccionario()
    faltan = set(panel.columns) - {d["variable"] for d in dic}
    sobran = {d["variable"] for d in dic} - set(panel.columns)
    if faltan or sobran:
        raise ValueError(f"Diccionario y datos no coinciden. Faltan: {faltan}; sobran: {sobran}")
    lineas = ["# Diccionario de variables — datos_procesados_2024200481M.csv", "",
              "Generado automáticamente por `codigo/03_limpieza_datos.py`. Unidad de análisis: plataforma-mes. "
              "Llave común: `ruc` + `periodo`. Celda vacía = dato no disponible (no se imputa).", "",
              "| N.º | Variable | Definición | Unidad de medida | Frecuencia | Fuente exacta y URL o endpoint |",
              "|---|---|---|---|---|---|"]
    lineas += [f"| {i} | `{d['variable']}` | {d['definicion']} | {d['unidad']} | {d['frecuencia']} | {d['fuente']} |"
               for i, d in enumerate(dic, 1)]
    DICCIONARIO.write_text("\n".join(lineas) + "\n", encoding="utf-8", newline="\n")
    log.info("DICCIONARIO | variables=%d | archivo=%s", len(dic), relativa(DICCIONARIO))


def escribir_reporte(panel: pd.DataFrame, atipicos: list[str], log) -> None:
    faltantes = panel.isna().sum()
    lineas = ["# Reporte de limpieza e integración (03_limpieza_datos.py)", "",
              f"Archivo generado: `{relativa(CSV_PROCESADO)}` · filas: {len(panel)} · columnas: {panel.shape[1]}", "",
              "## Controles", "", *[f"- {c}" for c in controles], "",
              "## Transformaciones aplicadas", "", *[f"{i}. {t}" for i, t in enumerate(transformaciones, 1)], "",
              "## Valores faltantes por variable", "", "| Variable | Faltantes | % |", "|---|---|---|",
              *[f"| `{c}` | {n} | {100 * n / len(panel):.1f} |" for c, n in faltantes.items() if n > 0], "",
              "Los faltantes de SIMV corresponden a meses sin registros o no obtenidos (`estado_simv`); los de EEFF, a "
              "meses que no son de cierre de trimestre o a trimestres en que la empresa no presentó información.", "",
              "## Atípicos identificados (regla de Tukey, 3·RIC; se conservan)", "",
              *([f"- {a}" for a in atipicos] or ["- Ninguno"]), ""]
    REPORTE.parent.mkdir(parents=True, exist_ok=True)
    REPORTE.write_text("\n".join(lineas), encoding="utf-8", newline="\n")
    log.info("REPORTE | archivo=%s", relativa(REPORTE))


# ============================================================================
# EJECUCIÓN
# ============================================================================
def main() -> int:
    log = configurar_log("03_limpieza_datos")
    log.info("INICIO | entradas: %s", ", ".join(relativa(p) for p in (CSV_SIMV, CSV_ODATA, CSV_BCRP)))
    eeff = preparar_eeff(log)
    catalogo = asignar_ruc(leer_catalogo(log), eeff, log)
    simv = preparar_simv(log)
    bcrp = preparar_bcrp(log)
    panel = integrar(catalogo, simv, eeff, bcrp, log)
    atipicos = detectar_atipicos(panel, log)
    PROCESADOS.mkdir(parents=True, exist_ok=True)
    panel.to_csv(CSV_PROCESADO, index=False, encoding="utf-8", lineterminator="\n")
    log.info("PROCESADO | filas=%d | columnas=%d | archivo=%s | sha256=%s", len(panel), panel.shape[1],
             relativa(CSV_PROCESADO), sha256_archivo(CSV_PROCESADO))
    escribir_diccionario(panel, log)
    escribir_reporte(panel, atipicos, log)
    log.info("FIN | 03 completado")
    return 0


if __name__ == "__main__":
    sys.exit(main())
