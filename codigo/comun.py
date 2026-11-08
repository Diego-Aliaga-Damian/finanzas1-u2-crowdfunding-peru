# Diego Sebastián Aliaga Damián
# 2024200481M
# Tema 96: Fintech y financiamiento participativo (crowdfunding) en el Perú: oferta y condiciones
# Fecha de extracción: 2026-11-07
"""Funciones comunes a los scripts 01-04.

Reúne en un solo lugar lo que exige la consigna para toda extracción:
rutas relativas (2.4.4), User-Agent identificable y pausa mínima de 1 s (2.4.8),
log con fecha, hora y código HTTP (2.4.2), crudos que no se sobrescriben si la
descarga falla (2.4.5) y hash SHA-256 (2.4.6).
"""
from __future__ import annotations

import hashlib
import logging
import os
import time
from pathlib import Path

import requests
from dotenv import load_dotenv

# --- 1. Rutas relativas a la raíz del proyecto (nunca rutas absolutas del equipo) ---
RAIZ = Path(__file__).resolve().parent.parent
CRUDOS = RAIZ / "datos_crudos"
PROCESADOS = RAIZ / "datos_procesados"
SALIDAS = RAIZ / "salidas"
ARCHIVO_LOG = RAIZ / "log_ejecucion.txt"
CODIGO_MATRICULA = "2024200481M"

# Lee el archivo .env si existe (es opcional: ninguna fuente exige clave de API).
load_dotenv(RAIZ / ".env")

PAUSA_MINIMA = 1.0  # segundos; la consigna exige al menos 1 s entre solicitudes


# --- 2. Log de ejecución: consola + log_ejecucion.txt (se acumula, no se borra) ---
def configurar_log(nombre_script: str) -> logging.Logger:
    """Devuelve un logger que escribe fecha, hora, script, nivel y mensaje."""
    log = logging.getLogger(nombre_script)
    if log.handlers:  # evita duplicar líneas si se llama dos veces
        return log
    log.setLevel(logging.INFO)
    formato = logging.Formatter("%(asctime)s | %(name)s | %(levelname)s | %(message)s",
                                datefmt="%Y-%m-%d %H:%M:%S")
    for manejador in (logging.FileHandler(ARCHIVO_LOG, mode="a", encoding="utf-8"),
                      logging.StreamHandler()):
        manejador.setFormatter(formato)
        log.addHandler(manejador)
    return log


# --- 3. Sesión HTTP con User-Agent identificable ---
def user_agent() -> str:
    """Identifica el proyecto ante el servidor; el contacto se toma de .env si se definió."""
    base = "UNCP-FinanzasI-Tema96/1.0 (investigacion academica; Universidad Nacional del Centro del Peru"
    contacto = os.getenv("CONTACTO_UA", "").strip()
    return f"{base}; contacto: {contacto})" if contacto else f"{base})"


def crear_sesion() -> requests.Session:
    sesion = requests.Session()
    sesion.headers.update({"User-Agent": user_agent()})
    return sesion


def pausa_configurada(pausa: float) -> float:
    """Nunca menos de 1 s; si .env define PAUSA_SEGUNDOS mayor, se respeta."""
    try:
        extra = float(os.getenv("PAUSA_SEGUNDOS") or 0)
    except ValueError:
        extra = 0.0
    return max(pausa, extra, PAUSA_MINIMA)


# --- 4. Solicitud con pausa previa, reintentos acotados y registro del código HTTP ---
def solicitar(sesion: requests.Session, url: str, log: logging.Logger, *, metodo: str = "GET",
              pausa: float = 1.5, intentos: int = 3, timeout: int = 60, **kwargs) -> requests.Response | None:
    """Hace la solicitud y registra HTTP, URL y bytes.

    - La pausa se aplica ANTES de cada solicitud: así nunca hay dos seguidas sin espera.
    - Reintenta solo ante errores de conexión, 429 o 5xx (con espera creciente).
    - Ante 4xx (salvo 429) no reintenta: devuelve la respuesta para que el script decida.
    """
    espera = pausa_configurada(pausa)
    for intento in range(1, intentos + 1):
        time.sleep(espera)
        try:
            r = sesion.request(metodo, url, timeout=timeout, **kwargs)
        except requests.RequestException as error:
            log.warning("ERROR_CONEXION | intento=%d | %s | %s", intento, url, type(error).__name__)
            time.sleep(espera * intento)
            continue
        log.info("HTTP %d | %s %s | bytes=%d | intento=%d", r.status_code, metodo, r.url, len(r.content), intento)
        if r.status_code == 429 or r.status_code >= 500:
            time.sleep(espera * 2 * intento)
            continue
        return r
    log.error("SIN_RESPUESTA_VALIDA | %s | intentos=%d", url, intentos)
    return None


# --- 5. Guardado atómico e integridad ---
def sha256_bytes(contenido: bytes) -> str:
    return hashlib.sha256(contenido).hexdigest()


def sha256_archivo(ruta: Path) -> str:
    h = hashlib.sha256()
    with open(ruta, "rb") as f:
        for bloque in iter(lambda: f.read(1 << 20), b""):
            h.update(bloque)
    return h.hexdigest()


def guardar_atomico(ruta: Path, contenido: bytes) -> str:
    """Escribe en un temporal y lo renombra: si algo falla, el crudo anterior queda intacto."""
    ruta.parent.mkdir(parents=True, exist_ok=True)
    temporal = ruta.with_name(ruta.name + ".tmp")
    temporal.write_bytes(contenido)
    os.replace(temporal, ruta)
    return sha256_bytes(contenido)


def relativa(ruta: Path) -> str:
    """Ruta relativa a la raíz, para que el log no exponga rutas del equipo."""
    return ruta.resolve().relative_to(RAIZ).as_posix()
