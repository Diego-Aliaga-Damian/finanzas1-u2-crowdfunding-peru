# Diego Sebastián Aliaga Damián
# 2024200481M
# Tema 96: Fintech y financiamiento participativo (crowdfunding) en el Perú: oferta y condiciones
# Fecha de extracción: 2026-11-07
"""02 — Scraping del portal SIMV de la SMV (vía 2 obligatoria de la Unidad II, numeral 2.4.1).

Página: «Información de Proyectos» de Financiamiento Participativo Financiero (FPF)
URL:    https://www.smv.gob.pe/SIMV/Frm_ProyectosFPF?data=785FE29A0201FCD759A08F94A0F74DBB4FD1B4D805

Cómo funciona la página (ASP.NET Web Forms):
  1. GET: devuelve el formulario con campos ocultos (__VIEWSTATE, __EVENTVALIDATION, ...).
  2. Para listar las plataformas retiradas se marca la casilla «cbxRetiradas» (postback que recarga la lista).
  3. POST con plataforma + año + mes + botón «Buscar»: devuelve la grilla con los resultados.

Selectores usados:
  - Plataformas: select[name="ctl00$MainContent$cboDenominacionSocial"] > option
  - Grilla:      table#MainContent_grdTodos  (si no hay datos: «No se encontraron registros…»)
  - Modalidad:   span[id^="MainContent_grdTodos_lblCabDato3_"]
  - Filas:       table[id^="MainContent_grdTodos_grdDetalle_"] tr > td  (tipo, publicados, financiados, monto)
Paginación: la grilla no pagina (una tabla por modalidad, una fila por tipo de receptor). El recorrido
  completo equivale a consultar cada plataforma en cada mes del periodo.

Ética (2.4.8): User-Agent identificable, pausa de 3 s entre solicitudes, robots.txt verificado y guardado,
  y detención automática si el portal responde con varios fallos seguidos (posible bloqueo).

Salidas (datos_crudos/, evidencia primaria que no se edita):
  smv_simv/{id}_{AAAA}_{MM}.html               respuesta original de cada consulta
  smv_simv/lista_vigentes.html, lista_retiradas.html   listas de plataformas tal como llegaron
  robots/smv_robots_*.txt                       evidencia de la consulta a robots.txt
  datos_crudos_2024200481M_smv_simv.csv         lectura literal de cada grilla (valores como texto)

Uso (desde la raíz del proyecto):
  python codigo/02_scraping_web.py              censo completo: 6 plataformas × 69 meses (≈ 35 min)
  python codigo/02_scraping_web.py --reanudar   omite las consultas ya guardadas y válidas
  python codigo/02_scraping_web.py --demo       demostración en vivo: 3 solicitudes (≈ 15 s), no toca los crudos
"""
from __future__ import annotations

import argparse
import sys
from urllib.robotparser import RobotFileParser

import pandas as pd
from bs4 import BeautifulSoup

from comun import (CODIGO_MATRICULA, CRUDOS, SALIDAS, configurar_log, crear_sesion, guardar_atomico,
                   relativa, sha256_archivo, solicitar, user_agent)

# ============================================================================
# PARÁMETROS CONGELADOS DE LA CONSULTA (numeral 2.4.5)
# ============================================================================
FECHA_INICIO = "2021-01"
FECHA_CORTE = "2026-09"

URL_SIMV = "https://www.smv.gob.pe/SIMV/Frm_ProyectosFPF?data=785FE29A0201FCD759A08F94A0F74DBB4FD1B4D805"
URL_ROBOTS = "https://www.smv.gob.pe/robots.txt"
PAUSA_SIMV = 3.0            # segundos entre solicitudes (la consigna exige al menos 1 s)
MAX_FALLOS_SEGUIDOS = 5     # si el portal falla 5 veces seguidas, se detiene el rastreo
MESES_PRUEBA_RETIRADAS = 2  # plataforma retirada sin grilla en sus 2 primeras consultas: incidencia y se omite
MAX_INTENTOS_RETIRADAS = 3  # intentos por mes para retiradas, cada uno con estado recién cargado

# Nombres de los campos del formulario ASP.NET (selectores del formulario)
CAMPO_EMPRESA = "ctl00$MainContent$cboDenominacionSocial"
CAMPO_TEXTO_EMPRESA = "ctl00$MainContent$TextBox1"
CAMPO_ANIO = "ctl00$MainContent$lisAnio"
CAMPO_MES = "ctl00$MainContent$lisMes"
CAMPO_RETIRADAS = "ctl00$MainContent$cbxRetiradas"
BOTON_BUSCAR = "ctl00$MainContent$cbBuscar"
ID_GRILLA = "MainContent_grdTodos"

# Consulta fija de la demostración en vivo: Inversiones.io, último mes del periodo
DEMO_EMPRESA_ID = "177663"
DEMO_ANIO, DEMO_MES = 2026, 9

DIR_SIMV = CRUDOS / "smv_simv"
DIR_ROBOTS = CRUDOS / "robots"
DIR_DEMO = SALIDAS / "demo"
CSV_SIMV = CRUDOS / f"datos_crudos_{CODIGO_MATRICULA}_smv_simv.csv"
COLUMNAS_CSV = ["empresa_id", "empresa", "lista", "anio", "mes", "resultado", "modalidad", "tipo_receptor",
                "proyectos_publicados", "proyectos_financiados", "monto_total_financiado", "archivo_crudo"]


# ============================================================================
# BLOQUE 1 — Utilidades del formulario ASP.NET
# ============================================================================
def sopa(contenido: bytes) -> BeautifulSoup:
    return BeautifulSoup(contenido, "html.parser")


def campos_ocultos(s: BeautifulSoup) -> dict:
    """__VIEWSTATE, __EVENTVALIDATION y demás campos ocultos que ASP.NET exige devolver en cada POST."""
    return {i["name"]: i.get("value", "") for i in s.find_all("input")
            if i.get("name", "").startswith("__")}


def opciones_empresas(s: BeautifulSoup) -> dict[str, str]:
    """{id: razón social} de la lista desplegable de plataformas (sin la opción vacía «-1»)."""
    lista = s.select_one(f'select[name="{CAMPO_EMPRESA}"]')
    if lista is None:
        return {}
    return {o.get("value"): o.get_text(strip=True) for o in lista.select("option") if o.get("value") != "-1"}


def valor_seleccionado(s: BeautifulSoup, campo: str) -> str | None:
    opcion = s.select_one(f'select[name="{campo}"] option[selected]')
    return opcion.get("value") if opcion else None


def meses_periodo() -> list[tuple[int, int]]:
    """[(2021, 1), (2021, 2), …, (2026, 9)] según FECHA_INICIO y FECHA_CORTE."""
    a, m = map(int, FECHA_INICIO.split("-"))
    a1, m1 = map(int, FECHA_CORTE.split("-"))
    meses = []
    while (a, m) <= (a1, m1):
        meses.append((a, m))
        a, m = (a + 1, 1) if m == 12 else (a, m + 1)
    return meses


# ============================================================================
# BLOQUE 2 — robots.txt (2.4.8): se consulta, se guarda la evidencia y se respeta
# ============================================================================
def revisar_robots(sesion, log, destino=DIR_ROBOTS) -> bool:
    r = solicitar(sesion, URL_ROBOTS, log, pausa=PAUSA_SIMV)
    if r is None:
        log.warning("ROBOTS | sin respuesta; se continúa con política conservadora (pausa 3 s)")
        return True
    tipo = r.headers.get("content-type", "")
    evidencia = (f"consulta: {URL_ROBOTS}\nurl_final: {r.url}\nhttp: {r.status_code}\n"
                 f"content-type: {tipo}\nredirecciones: {[h.status_code for h in r.history]}\n")
    es_robots = r.status_code == 200 and "text/plain" in tipo and r.url.rstrip("/").endswith("robots.txt")
    if es_robots:
        guardar_atomico(destino / "smv_robots_contenido.txt", r.content)
        reglas = RobotFileParser()
        reglas.parse(r.text.splitlines())
        permitido = reglas.can_fetch(user_agent(), URL_SIMV)
        evidencia += f"robots.txt válido; can_fetch(URL_SIMV) = {permitido}\n"
    else:
        permitido = True
        evidencia += ("www.smv.gob.pe no publica un robots.txt propio (la ruta redirige a otra página); "
                      "no hay reglas que prohíban la ruta /SIMV/. Se aplica política conservadora.\n")
    guardar_atomico(destino / "smv_robots_evidencia.txt", evidencia.encode("utf-8"))
    log.info("ROBOTS | http=%s | url_final=%s | robots_valido=%s | permitido=%s",
             r.status_code, r.url, es_robots, permitido)
    return permitido


# ============================================================================
# BLOQUE 3 — Consultas al formulario
# ============================================================================
def iniciar_estado(sesion, log, retiradas: bool):
    """GET de la página; si se piden las retiradas, marca la casilla (postback). Devuelve (respuesta, sopa)."""
    r = solicitar(sesion, URL_SIMV, log, pausa=PAUSA_SIMV)
    if r is None or r.status_code != 200:
        return None, None
    s = sopa(r.content)
    if not retiradas:
        return r, s
    datos = campos_ocultos(s)
    datos.update({"__EVENTTARGET": CAMPO_RETIRADAS, CAMPO_RETIRADAS: "on", CAMPO_EMPRESA: "-1",
                  CAMPO_ANIO: "-1", CAMPO_MES: "-1", CAMPO_TEXTO_EMPRESA: ""})
    r = solicitar(sesion, URL_SIMV, log, metodo="POST", data=datos, pausa=PAUSA_SIMV)
    if r is None or r.status_code != 200:
        return None, None
    return r, sopa(r.content)


def consultar(sesion, log, estado: BeautifulSoup, empresa_id: str, empresa: str, anio: int, mes: int,
              retiradas: bool):
    """POST «Buscar» para una plataforma y un mes, reutilizando el ViewState de la respuesta anterior."""
    datos = campos_ocultos(estado)
    datos.update({"__EVENTTARGET": "", "__EVENTARGUMENT": "", CAMPO_EMPRESA: empresa_id,
                  CAMPO_TEXTO_EMPRESA: empresa, CAMPO_ANIO: str(anio), CAMPO_MES: str(mes),
                  BOTON_BUSCAR: "Buscar"})
    if retiradas:
        datos[CAMPO_RETIRADAS] = "on"
    return solicitar(sesion, URL_SIMV, log, metodo="POST", data=datos, pausa=PAUSA_SIMV)


def validar(s: BeautifulSoup, empresa_id: str, anio: int, mes: int) -> list[str]:
    """La respuesta solo se guarda si trae la grilla y si el formulario devuelto confirma la consulta pedida."""
    problemas = []
    if s.find(id=ID_GRILLA) is None:
        problemas.append("no contiene la grilla de resultados (posible error o bloqueo)")
    eco = {"empresa": (valor_seleccionado(s, CAMPO_EMPRESA), empresa_id),
           "año": (valor_seleccionado(s, CAMPO_ANIO), str(anio)),
           "mes": (valor_seleccionado(s, CAMPO_MES), str(mes))}
    for campo, (devuelto, pedido) in eco.items():
        if devuelto != pedido:
            problemas.append(f"el formulario devuelto indica {campo}={devuelto} y se pidió {pedido}")
    return problemas


def leer_grilla(s: BeautifulSoup) -> list[dict]:
    """Lee la grilla tal como se muestra. Lista vacía = «No se encontraron registros»."""
    grilla = s.find(id=ID_GRILLA)
    filas = []
    for bloque in grilla.select("tr.item-grid2"):
        etiqueta = bloque.select_one('span[id^="MainContent_grdTodos_lblCabDato3_"]')
        modalidad = etiqueta.get_text(strip=True) if etiqueta else ""
        for tr in bloque.select('table[id^="MainContent_grdTodos_grdDetalle_"] tr'):
            celdas = [td.get_text(strip=True) for td in tr.find_all("td")]
            if len(celdas) == 4:
                filas.append({"modalidad": modalidad, "tipo_receptor": celdas[0],
                              "proyectos_publicados": celdas[1], "proyectos_financiados": celdas[2],
                              "monto_total_financiado": celdas[3]})
    return filas


# ============================================================================
# BLOQUE 4 — Censo completo: plataformas × meses
# ============================================================================
def archivo_consulta(empresa_id: str, anio: int, mes: int):
    return DIR_SIMV / f"{empresa_id}_{anio}_{mes:02d}.html"


def crudo_valido(ruta, empresa_id, anio, mes) -> bool:
    return ruta.exists() and not validar(sopa(ruta.read_bytes()), empresa_id, anio, mes)


def solo_falta_grilla(problemas: list[str]) -> bool:
    """True si el portal confirmó la consulta (eco correcto) pero no mostró la grilla: es un
    comportamiento del portal, no un bloqueo (las respuestas de bloqueo no traen el formulario)."""
    return len(problemas) == 1 and problemas[0].startswith("no contiene la grilla")


def censo(sesion, log, reanudar: bool) -> tuple[bool, list[str]]:
    """Recorre plataformas × meses. Devuelve (sin_errores, lista_de_incidencias_documentadas)."""
    todo_ok, fallos_seguidos, incidencias = True, 0, []
    for retiradas, nombre_lista in ((False, "vigentes"), (True, "retiradas")):
        r, estado = iniciar_estado(sesion, log, retiradas)
        if estado is None:
            log.error("SIMV | no se pudo cargar la lista de %s", nombre_lista)
            return False, incidencias
        guardar_atomico(DIR_SIMV / f"lista_{nombre_lista}.html", r.content)
        empresas = opciones_empresas(estado)
        log.info("SIMV | lista %s | plataformas=%d | %s", nombre_lista, len(empresas),
                 "; ".join(f"{k}={v[:40]}" for k, v in empresas.items()))
        for empresa_id, empresa in empresas.items():
            if not retiradas:
                r, estado = iniciar_estado(sesion, log, retiradas)  # estado limpio para cada plataforma
            guardadas = sin_grilla = 0
            for anio, mes in meses_periodo():
                destino = archivo_consulta(empresa_id, anio, mes)
                if reanudar and crudo_valido(destino, empresa_id, anio, mes):
                    guardadas += 1
                    continue
                intentos = MAX_INTENTOS_RETIRADAS if retiradas else 2
                for intento in range(1, intentos + 1):
                    if retiradas:
                        # Las retiradas solo responden de forma fiable con un estado recién cargado
                        # (GET + casilla): reutilizar el estado anterior acertó ~10 % de las veces y el
                        # estado nuevo ~50 % en el censo del 2026-11-07 (ver incidencias_fuente.md).
                        _, nuevo = iniciar_estado(sesion, log, True)
                        estado = nuevo if nuevo is not None else estado
                    r = consultar(sesion, log, estado, empresa_id, empresa, anio, mes, retiradas)
                    s = sopa(r.content) if (r is not None and r.status_code == 200) else None
                    problemas = validar(s, empresa_id, anio, mes) if s is not None else ["sin respuesta HTTP 200"]
                    if not problemas:
                        break
                    log.warning("SIMV | %s %d-%02d | intento %d no válido: %s", empresa_id, anio, mes,
                                intento, "; ".join(problemas))
                    if not retiradas:  # vigentes: reintento con estado nuevo
                        _, nuevo = iniciar_estado(sesion, log, retiradas)
                        estado = nuevo if nuevo is not None else estado
                if problemas:
                    if s is not None:  # la respuesta inválida se guarda como evidencia, aparte de la base
                        guardar_atomico(DIR_SIMV / "incidencias" / f"{empresa_id}_{anio}_{mes:02d}_no_valida.html",
                                        r.content)
                    if retiradas and solo_falta_grilla(problemas):
                        sin_grilla += 1
                        if guardadas == 0 and sin_grilla >= MESES_PRUEBA_RETIRADAS:
                            texto = (f"{empresa_id} ({empresa[:50]}): el portal confirma la consulta pero no muestra "
                                     f"la grilla en {sin_grilla} meses seguidos; se omite la plataforma")
                            log.warning("SIMV | INCIDENCIA | %s", texto)
                            incidencias.append(texto)
                            break
                        continue
                    todo_ok, fallos_seguidos = False, fallos_seguidos + 1
                    log.error("SIMV | %s %d-%02d | NO GUARDADO (se conserva el crudo anterior)", empresa_id, anio, mes)
                    if fallos_seguidos >= MAX_FALLOS_SEGUIDOS:
                        log.error("SIMV | %d fallos seguidos: posible bloqueo; se detiene el rastreo", fallos_seguidos)
                        return False, incidencias
                    continue
                fallos_seguidos = 0
                estado = s
                huella = guardar_atomico(destino, r.content)
                guardadas += 1
                filas = leer_grilla(s)
                log.info("SIMV | %s %d-%02d | OK | resultado=%s | filas=%d | archivo=%s | sha256=%s",
                         empresa_id, anio, mes, "con_registros" if filas else "sin_registros", len(filas),
                         relativa(destino), huella)
    return todo_ok, incidencias


def generar_csv(log) -> None:
    """Relee los HTML guardados y escribe la lectura literal de cada grilla (incluye las consultas sin registros)."""
    catalogo = {}
    for nombre_lista in ("vigentes", "retiradas"):
        lista = DIR_SIMV / f"lista_{nombre_lista}.html"
        if lista.exists():
            for k, v in opciones_empresas(sopa(lista.read_bytes())).items():
                catalogo[k] = (v, nombre_lista)
    filas = []
    for archivo in sorted(DIR_SIMV.glob("*_*_*.html")):
        empresa_id, anio, mes = archivo.stem.split("_")
        empresa, lista = catalogo.get(empresa_id, ("", ""))
        base = {"empresa_id": empresa_id, "empresa": empresa, "lista": lista, "anio": anio, "mes": str(int(mes)),
                "archivo_crudo": archivo.name}
        grilla = leer_grilla(sopa(archivo.read_bytes()))
        if grilla:
            filas += [{**base, "resultado": "con_registros", **f} for f in grilla]
        else:
            filas.append({**base, "resultado": "sin_registros"})
    pd.DataFrame(filas, columns=COLUMNAS_CSV).to_csv(CSV_SIMV, index=False, encoding="utf-8", lineterminator="\n")
    log.info("SIMV | CSV crudo | filas=%d | consultas=%d | archivo=%s | sha256=%s", len(filas),
             len(list(DIR_SIMV.glob("*_*_*.html"))), relativa(CSV_SIMV), sha256_archivo(CSV_SIMV))


# ============================================================================
# BLOQUE 5 — Demostración en vivo (3 solicitudes; escribe en salidas/demo, nunca en datos_crudos)
# ============================================================================
def demo(sesion, log) -> bool:
    log.info("DEMO | consulta en vivo: empresa=%s periodo=%d-%02d", DEMO_EMPRESA_ID, DEMO_ANIO, DEMO_MES)
    revisar_robots(sesion, log, destino=DIR_DEMO)
    _, estado = iniciar_estado(sesion, log, retiradas=False)
    empresa = opciones_empresas(estado).get(DEMO_EMPRESA_ID, "") if estado is not None else ""
    r = consultar(sesion, log, estado, DEMO_EMPRESA_ID, empresa, DEMO_ANIO, DEMO_MES, False) if estado else None
    s = sopa(r.content) if (r is not None and r.status_code == 200) else None
    problemas = validar(s, DEMO_EMPRESA_ID, DEMO_ANIO, DEMO_MES) if s is not None else ["sin respuesta HTTP 200"]
    if problemas:
        log.error("DEMO | respuesta no válida: %s", "; ".join(problemas))
        return False
    guardar_atomico(DIR_DEMO / f"{DEMO_EMPRESA_ID}_{DEMO_ANIO}_{DEMO_MES:02d}.html", r.content)
    vivo = leer_grilla(s)
    print(f"\nEn vivo desde la SMV: {empresa[:60]} · {DEMO_ANIO}-{DEMO_MES:02d}")
    print(pd.DataFrame(vivo).to_string(index=False) if vivo else "  (sin registros)")
    # Comparación con la base entregada (CSV crudo generado por el censo)
    if not CSV_SIMV.exists():
        print("\nAún no existe la base entregada para comparar.")
        return True
    base = pd.read_csv(CSV_SIMV, dtype=str)
    entregado = base[(base.empresa_id == DEMO_EMPRESA_ID) & (base.anio == str(DEMO_ANIO)) & (base.mes == str(DEMO_MES))]
    campos = ["proyectos_publicados", "proyectos_financiados", "monto_total_financiado"]
    total = coinciden = 0
    for f in vivo:
        fila = entregado[(entregado.modalidad == f["modalidad"]) & (entregado.tipo_receptor == f["tipo_receptor"])]
        for c in campos:
            total += 1
            coinciden += (not fila.empty) and fila.iloc[0][c] == f[c]
    print(f"\nComparación con datos_crudos entregados: {coinciden}/{total} valores coinciden")
    log.info("DEMO | comparación con la base entregada: %d/%d valores coinciden", coinciden, total)
    return True


# ============================================================================
# EJECUCIÓN
# ============================================================================
def main() -> int:
    parser = argparse.ArgumentParser(description="Scraping del SIMV-SMV: Información de Proyectos FPF")
    parser.add_argument("--demo", action="store_true", help="demostración en vivo (3 solicitudes)")
    parser.add_argument("--reanudar", action="store_true", help="omite consultas ya guardadas y válidas")
    args = parser.parse_args()

    log = configurar_log("02_scraping_web")
    sesion = crear_sesion()
    if args.demo:
        return 0 if demo(sesion, log) else 1

    log.info("INICIO | FECHA_INICIO=%s | FECHA_CORTE=%s | pausa=%.1fs | User-Agent=%s",
             FECHA_INICIO, FECHA_CORTE, PAUSA_SIMV, user_agent())
    if not revisar_robots(sesion, log):
        log.error("ROBOTS | la ruta está prohibida: no se rastrea (aplicar sustitución de fuente, 2.4.3)")
        return 1
    ok, incidencias = censo(sesion, log, args.reanudar)
    if any(DIR_SIMV.glob("*_*_*.html")):
        generar_csv(log)
    log.info("FIN | SIMV=%s | incidencias_documentadas=%d", "OK" if ok else "CON ERRORES", len(incidencias))
    for texto in incidencias:
        log.info("FIN | incidencia: %s (ver incidencias_fuente.md)", texto)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
