# Diego Sebastián Aliaga Damián
# 2024200481M
# Tema 96: Fintech y financiamiento participativo (crowdfunding) en el Perú: oferta y condiciones
# Fecha: 2026-11-24
"""Identidad visual FinCrowd Perú: paleta, CSS, plantilla de Plotly y componentes HTML reutilizables.

Los componentes solo dan forma: reciben cifras ya calculadas (datos.py o salidas del análisis) y nunca las alteran.
Íconos: Material Symbols Rounded, la misma fuente que trae Streamlit para los íconos :material/...:.
"""
from __future__ import annotations

import html
from urllib.parse import quote
from typing import Iterable

import pandas as pd
import plotly.graph_objects as go
import plotly.io as pio
import streamlit as st

import datos as D

# ----------------------------------------------------------------------------- paleta por modo (noche y día)
FUENTE = "Plus Jakarta Sans, Segoe UI, system-ui, -apple-system, sans-serif"


def _paleta(azul, turquesa, esmeralda, coral, amarillo, violeta, suave, oscuro, claros, **tonos) -> dict:
    acentos = (azul, turquesa, esmeralda, coral, amarillo, violeta)
    p = dict(AZUL=azul, TURQUESA=turquesa, ESMERALDA=esmeralda, CORAL=coral, AMARILLO=amarillo, VIOLETA=violeta, **tonos)
    p["PALETA"] = [azul, esmeralda, coral, amarillo, violeta, turquesa]
    # Tono de fondo y tono de texto legible de cada acento
    p["SUAVE"], p["OSCURO"] = dict(zip(acentos, suave)), dict(zip(acentos, oscuro))
    # El color sigue a la entidad en todas las páginas
    p["COLOR_PLATAFORMA"] = {"Inversiones.io": azul, "Afluenta": esmeralda, "Prestopolis": coral,
                             "Inversiones Neurona": amarillo, "Proyecto Crowd": violeta, "Securite": turquesa}
    p["COLOR_SERIE"] = {"tea_bcos_pyme_360": azul, "tea_cmac_pyme_360": esmeralda, "tea_crac_pyme_360": violeta,
                        "tea_bcos_consumo_360": amarillo, **dict(zip(
                            ("tea_bcos_pyme_mas360", "tea_cmac_pyme_mas360", "tea_crac_pyme_mas360", "tea_bcos_consumo_mas360"),
                            claros)), "tamn": turquesa}
    p["COLOR_ESTADO"] = {"con_registros": esmeralda, "sin_registros": p["NEUTRO"], "no_obtenido": coral}
    # Insignias que distinguen la naturaleza de cada cifra
    p["INSIGNIAS"] = {
        "observado": ("Observado", "visibility", esmeralda, "Dato publicado por la fuente oficial (BCRP o SMV)."),
        "articulo": ("Resultado del artículo", "verified", azul, "Cifra fija de las salidas de 04_analisis.py; no depende de los filtros."),
        "filtros": ("Responde a los filtros", "filter_alt", violeta, "Se recalcula con el periodo y las plataformas elegidos."),
        "cota": ("Cota inferior", "south", amarillo, "Los meses no obtenidos del portal no se imputan: el valor real puede ser algo mayor."),
        "hipotetico": ("Hipotético", "science", coral, "Supuesto definido por el usuario: no es un dato observado."),
        "referencia": ("Referencia", "info", turquesa, "Indicador de contexto; no es un precio del financiamiento participativo."),
    }
    return p


PALETAS = {
    "light": _paleta(
        "#2563EB", "#06B6D4", "#10B981", "#FB7185", "#FBBF24", "#8B5CF6",
        ("#EFF6FF", "#ECFEFF", "#ECFDF5", "#FFF1F2", "#FFFBEB", "#F5F3FF"),
        ("#1D4ED8", "#0E7490", "#047857", "#BE123C", "#B45309", "#6D28D9"),
        ("#93C5FD", "#6EE7B7", "#C4B5FD", "#FCD34D"),
        FONDO="#FAFBFF", TINTA="#0F172A", TINTA_2="#475569", TINTA_3="#64748B", BORDE="#E2E8F0", GRILLA="#EDF1F7",
        PAPEL="#FFFFFF", PAPEL_2="#F5F8FF", NEUTRO="#CBD5E1", VELO="rgba(255,255,255,0.85)", CARRIL="#EEF2F7"),
    "dark": _paleta(
        "#4F8CFF", "#22D3EE", "#34D399", "#FB7185", "#FBBF24", "#A78BFA",
        ("#122044", "#0B2B38", "#0C2C28", "#33172A", "#30260F", "#221C45"),
        ("#9CC0FF", "#7DE7F7", "#7BE8C0", "#FFA9B7", "#FCD77A", "#CDBBFF"),
        ("#8FB8FF", "#A7F3D0", "#D6C8FF", "#FDE68A"),
        FONDO="#070B17", TINTA="#E8EEFC", TINTA_2="#B4C0DA", TINTA_3="#8C9ABA", BORDE="#1E2A49", GRILLA="#18223D",
        PAPEL="#0D1429", PAPEL_2="#111A35", NEUTRO="#3B4A6B", VELO="rgba(13,20,41,0.88)", CARRIL="#1A2442"),
}
# Colores fijos de la terminal 3D (siempre oscura)
NEON_PLATAFORMA, NEON_SERIE = PALETAS["dark"]["COLOR_PLATAFORMA"], PALETAS["dark"]["COLOR_SERIE"]


def modo() -> str:
    """Tema activo del visitante ('dark' o 'light'); noche si Streamlit aún no lo informa."""
    try:
        return "light" if st.context.theme.type == "light" else "dark"
    except Exception:  # fuera de una sesión de Streamlit (pruebas)
        return "dark"


def __getattr__(nombre: str):
    """T.AZUL, T.TINTA, T.SUAVE… se resuelven al usarlos, según el tema de cada visitante."""
    if nombre in PALETAS["dark"]:
        return PALETAS[modo()][nombre]
    raise AttributeError(nombre)


class _Paleta:
    def __getattr__(self, nombre: str):
        return PALETAS[modo()][nombre]


P = _Paleta()


# En HTML y CSS el color lo elige el navegador con light-dark(), según el tema activo (cambia al instante, sin recargar)
def ld(dia: str, noche: str) -> str:
    return f"light-dark({dia}, {noche})"


def _par(clave: str, acento: str) -> str:
    """Tono SUAVE u OSCURO de un acento (de cualquiera de los dos modos) para los dos temas."""
    for p in PALETAS.values():
        for nombre in ("AZUL", "TURQUESA", "ESMERALDA", "CORAL", "AMARILLO", "VIOLETA"):
            if p[nombre] == acento:
                return ld(*(q[clave][q[nombre]] for q in PALETAS.values()))
    return ld("#F5F8FF", "#111A35") if clave == "SUAVE" else acento


def suave(acento: str) -> str:
    return _par("SUAVE", acento)


def oscuro(acento: str) -> str:
    return _par("OSCURO", acento)


# ----------------------------------------------------------------------------- Plotly
def registrar_plantillas() -> None:
    for m, p in PALETAS.items():
        if f"fincrowd_{m}" in pio.templates:
            continue
        pio.templates[f"fincrowd_{m}"] = go.layout.Template(layout=dict(
            font=dict(family=FUENTE, size=12.5, color=p["TINTA_2"]), colorway=p["PALETA"],
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            title=dict(font=dict(size=14, color=p["TINTA"], family=FUENTE), x=0, xanchor="left"),
            hoverlabel=dict(bgcolor=p["PAPEL_2"], bordercolor=p["BORDE"], font=dict(family=FUENTE, size=12.5, color=p["TINTA"])),
            xaxis=dict(showgrid=False, linecolor=p["BORDE"], tickcolor=p["BORDE"], ticks="outside", zeroline=False, title_standoff=8),
            yaxis=dict(gridcolor=p["GRILLA"], zeroline=False, linecolor="rgba(0,0,0,0)", title_standoff=8),
            legend=dict(orientation="h", yanchor="bottom", y=1.01, xanchor="left", x=0, bgcolor="rgba(0,0,0,0)",
                        font=dict(size=12), title_text=""),
            margin=dict(l=6, r=6, t=34, b=6), bargap=0.18,
        ))


def plantilla() -> str:
    return f"plotly_{'dark' if modo() == 'dark' else 'white'}+fincrowd_{modo()}"


def figura(fig: go.Figure, nombre: str, alto: int = 380, datos: pd.DataFrame | None = None,
           etiqueta_csv: str = "Datos del gráfico (CSV)", leer: str | None = None) -> None:
    """Muestra un gráfico con el estilo FinCrowd, descarga en PNG desde la barra del gráfico, un botón para bajar
    los datos en CSV (si se pasan) y una explicación desplegable de cómo leerlo (si se pasa `leer`)."""
    fig.update_layout(height=alto, template=plantilla())
    config = {"displaylogo": False, "modeBarButtonsToRemove": ["lasso2d", "select2d", "autoScale2d"],
              "toImageButtonOptions": {"format": "png", "filename": nombre, "scale": 2}}
    st.plotly_chart(fig, theme=None, config=config, key=f"fig_{nombre}")
    if leer:
        como_leer(leer)
    if datos is not None:
        st.download_button(etiqueta_csv, datos.to_csv(index=True).encode("utf-8-sig"), file_name=f"{nombre}.csv",
                           mime="text/csv", icon=":material/download:", key=f"csv_{nombre}", type="tertiary")


def como_leer(texto: str, titulo: str = "¿Cómo leer este gráfico?") -> None:
    """Explicación en lenguaje simple, plegada para no recargar la página."""
    with st.expander(titulo, icon=":material/help:"):
        st.markdown(texto)


def eje_meses(fig: go.Figure, periodos: list[str], cada: int = 6, eje: str = "x") -> list[str]:
    """Eje de categorías con meses en castellano ('ene 2024'); marca solo enero y julio para no saturar.
    Devuelve las etiquetas para usarlas como x."""
    etiquetas = [D.etiqueta_mes(p) for p in periodos]
    marcas = [l for p, l in zip(periodos, etiquetas) if (int(p[5:7]) - 1) % cada == 0]
    fig.update_layout({f"{eje}axis": dict(type="category", tickmode="array", tickvals=marcas,
                                          ticktext=[m.replace(" ", "<br>") for m in marcas], tickangle=0)})
    return etiquetas


def marcar_mes(fig: go.Figure, fecha, texto: str, color: str | None = None, lado: str = "right") -> None:
    """Línea vertical con rótulo (fecha: etiqueta de la categoría, p. ej. 'dic 2025')."""
    color = color or P.TINTA_3
    fig.add_shape(type="line", x0=fecha, x1=fecha, y0=0, y1=1, yref="paper", line=dict(color=color, width=1.4, dash="dot"))
    fig.add_annotation(x=fecha, y=1, yref="paper", text=texto, showarrow=False, xanchor="left" if lado == "right" else "right",
                       yanchor="top", xshift=4 if lado == "right" else -4, font=dict(size=11, color=color),
                       bgcolor=P.VELO)


# ----------------------------------------------------------------------------- CSS
def _css() -> str:
    dia, noche = PALETAS["light"], PALETAS["dark"]
    AZUL, TURQUESA, ESMERALDA, CORAL, AMARILLO, VIOLETA = (ld(dia[k], noche[k]) for k in (
        "AZUL", "TURQUESA", "ESMERALDA", "CORAL", "AMARILLO", "VIOLETA"))
    FONDO, TINTA, TINTA_2, TINTA_3, BORDE, GRILLA = (ld(dia[k], noche[k]) for k in (
        "FONDO", "TINTA", "TINTA_2", "TINTA_3", "BORDE", "GRILLA"))
    PAPEL, PAPEL_2, CARRIL = (ld(dia[k], noche[k]) for k in ("PAPEL", "PAPEL_2", "CARRIL"))
    SUAVE = {ld(dia[k], noche[k]): suave(dia[k]) for k in ("AZUL", "TURQUESA", "ESMERALDA", "CORAL", "AMARILLO", "VIOLETA")}
    OSCURO = {ld(dia[k], noche[k]): oscuro(dia[k]) for k in ("AZUL", "TURQUESA", "ESMERALDA", "CORAL", "AMARILLO", "VIOLETA")}
    S1, S2, S3, S4 = (ld("rgba(15,23,42,.04)", "rgba(0,0,0,.35)"), ld("rgba(37,99,235,.06)", "rgba(0,0,0,.28)"),
                      ld("rgba(15,23,42,.06)", "rgba(0,0,0,.45)"), ld("rgba(37,99,235,.14)", "rgba(34,211,238,.10)"))
    SOMBRA, SOMBRA_H = f"0 1px 2px {S1}, 0 8px 22px {S2}", f"0 2px 7px {S3}, 0 15px 36px {S4}"
    HALO_V, HALO_T = ld("rgba(139,92,246,.07)", "rgba(139,92,246,.13)"), ld("rgba(6,182,212,.08)", "rgba(6,182,212,.13)")
    LOGOS = ld("transparent", "#FFFFFF")
    return f"""
<style>
:root, .stApp {{
  --fc-azul:{AZUL}; --fc-turquesa:{TURQUESA}; --fc-esmeralda:{ESMERALDA}; --fc-coral:{CORAL};
  --fc-amarillo:{AMARILLO}; --fc-violeta:{VIOLETA}; --fc-tinta:{TINTA}; --fc-tinta2:{TINTA_2}; --fc-tinta3:{TINTA_3};
  --fc-borde:{BORDE}; --fc-sombra:{SOMBRA};
  --fc-sombra-hover:{SOMBRA_H};
}}
.stApp {{
  background:
    radial-gradient(1100px 420px at 100% -10%, {HALO_V}, transparent 60%),
    radial-gradient(900px 380px at -5% -8%, {HALO_T}, transparent 55%), {FONDO};
}}
[data-testid="stHeader"] {{ background: transparent; }}
[data-testid="stMainBlockContainer"] {{ padding-top: 2.4rem; padding-bottom: 3rem; max-width: 1380px; }}
h1, h2, h3 {{ letter-spacing: -.02em; }}
[data-testid="stCaptionContainer"], [data-testid="stCaptionContainer"] p, .stCaption {{ color: {TINTA_3}; opacity:1 !important; }}

/* ---------- barra lateral */
[data-testid="stSidebar"] {{
  background: linear-gradient(185deg, {PAPEL} 0%, {PAPEL_2} 60%, {FONDO} 100%);
  border-right: 1px solid {BORDE};
}}
[data-testid="stSidebar"]::before {{
  content: ""; position: absolute; inset: 0 0 auto 0; height: 4px; z-index: 2;
  background: linear-gradient(90deg, {AZUL}, {TURQUESA}, {ESMERALDA}, {AMARILLO}, {CORAL}, {VIOLETA});
}}
[data-testid="stSidebarNavLink"] {{ border-radius: 10px; margin: 1px 0; transition: background .15s ease, transform .15s ease; }}
[data-testid="stSidebarNavLink"]:hover {{ background: rgba(37,99,235,.07); transform: translateX(2px); }}
[data-testid="stSidebarNavLink"][aria-current="page"] {{
  background: linear-gradient(90deg, rgba(37,99,235,.13), rgba(6,182,212,.06)); box-shadow: inset 3px 0 0 {AZUL};
}}
[data-testid="stSidebarNavLink"][aria-current="page"] span {{ color: {OSCURO[AZUL]}; font-weight: 700; }}
[data-testid="stSidebarNavLink"] [data-testid="stIconMaterial"] {{ color: {AZUL}; }}
[data-testid="stSidebarNavLink"][href$="/datos"] [data-testid="stIconMaterial"] {{ color: {TURQUESA}; }}
[data-testid="stSidebarNavLink"][href$="/oferta"] [data-testid="stIconMaterial"] {{ color: {AZUL}; }}
[data-testid="stSidebarNavLink"][href$="/plataformas"] [data-testid="stIconMaterial"] {{ color: {VIOLETA}; }}
[data-testid="stSidebarNavLink"][href$="/acceso"] [data-testid="stIconMaterial"] {{ color: {ESMERALDA}; }}
[data-testid="stSidebarNavLink"][href$="/credito-tradicional"] [data-testid="stIconMaterial"] {{ color: {AMARILLO}; }}
[data-testid="stSidebarNavLink"][href$="/simulador"] [data-testid="stIconMaterial"] {{ color: {CORAL}; }}
[data-testid="stSidebarNavLink"][href$="/sensibilidad"] [data-testid="stIconMaterial"] {{ color: {VIOLETA}; }}
[data-testid="stSidebarNavLink"][href$="/productos"] [data-testid="stIconMaterial"] {{ color: {CORAL}; }}
[data-testid="stSidebarNavLink"][href$="/reproducibilidad"] [data-testid="stIconMaterial"] {{ color: {ESMERALDA}; }}
[data-testid="stNavSectionHeader"] {{ text-transform: uppercase; letter-spacing: .09em; font-size: .68rem !important;
  font-weight: 700; color: {TINTA_3}; }}
.fc-side-tit {{ display:flex; align-items:center; gap:6px; font-size:.7rem; font-weight:800; letter-spacing:.09em;
  text-transform:uppercase; color:{TINTA_3}; margin: 4px 0 2px; }}
.fc-side-pie {{ font-size:.74rem; color:{TINTA_3}; line-height:1.45; border-top:1px dashed {BORDE}; padding-top:10px; }}
.fc-side-pie b {{ color:{TINTA_2}; }}

/* ---------- íconos */
.fc-ic {{ font-family: 'Material Symbols Rounded'; font-weight: normal; font-style: normal; font-size: 20px; line-height: 1;
  letter-spacing: normal; text-transform: none; display: inline-block; white-space: nowrap; direction: ltr;
  font-feature-settings: 'liga'; -webkit-font-feature-settings: 'liga'; -webkit-font-smoothing: antialiased;
  font-variation-settings: 'FILL' 1, 'wght' 500, 'GRAD' 0, 'opsz' 24; vertical-align: middle; }}

/* ---------- cabecera compacta (inicio) */
.fc-hero {{ position:relative; display:flex; align-items:center; gap:18px; padding:16px 22px; border-radius:20px;
  background: linear-gradient(120deg, {PAPEL} 0%, {PAPEL_2} 100%); border:1px solid {BORDE};
  box-shadow: var(--fc-sombra); overflow:hidden; margin-bottom: 6px; }}
.fc-hero::before {{ content:""; position:absolute; left:0; top:0; bottom:0; width:5px;
  background: linear-gradient(180deg, {AZUL}, {VIOLETA}, {TURQUESA}); }}
.fc-hero::after {{ content:""; position:absolute; right:-60px; top:-70px; width:240px; height:240px; border-radius:50%;
  background: radial-gradient(circle, rgba(139,92,246,.13), transparent 70%); }}
.fc-hero-logos {{ background:{LOGOS}; border-radius:12px; padding:6px 10px; display:flex; gap:10px; align-items:center; flex-shrink:0; }}
.fc-hero-logos img {{ height:50px; width:auto; object-fit:contain; }}
.fc-hero-txt {{ flex:1; min-width:0; z-index:1; }}
.fc-eyebrow {{ font-size:.68rem; font-weight:800; letter-spacing:.12em; color:{OSCURO[VIOLETA]}; text-transform:uppercase; }}
.fc-brand {{ font-size:1.55rem; font-weight:800; letter-spacing:-.03em; color:{TINTA}; line-height:1.15; }}
.fc-brand span {{ background: linear-gradient(90deg, {AZUL}, {VIOLETA} 60%, {TURQUESA}); -webkit-background-clip:text;
  background-clip:text; color:transparent; }}
.fc-hero-sub {{ font-size:.92rem; font-weight:600; color:{TINTA_2}; margin-top:2px; }}
.fc-hero-meta {{ font-size:.78rem; color:{TINTA_3}; margin-top:3px; }}
.fc-hero-chips {{ display:flex; flex-direction:column; gap:6px; align-items:flex-end; z-index:1; flex-shrink:0; }}

/* ---------- cabecera de página */
.fc-ph {{ display:flex; align-items:center; gap:14px; margin: 0 0 6px; }}
.fc-ph .fc-chipic {{ width:46px; height:46px; border-radius:14px; display:flex; align-items:center; justify-content:center;
  background: linear-gradient(135deg, var(--a), var(--b)); color:#fff; box-shadow: 0 8px 18px -8px var(--a); flex-shrink:0; }}
.fc-ph .fc-chipic .fc-ic {{ font-size:26px; }}
.fc-ph-eye {{ font-size:.68rem; font-weight:800; letter-spacing:.12em; text-transform:uppercase; color:var(--o); }}
.fc-ph-t {{ font-size:1.5rem; font-weight:800; letter-spacing:-.025em; color:{TINTA}; line-height:1.2; }}
.fc-ph-s {{ font-size:.9rem; color:{TINTA_2}; margin-top:2px; }}

/* ---------- chips de filtros e insignias */
.fc-chips {{ display:flex; flex-wrap:wrap; gap:6px; margin: 4px 0 10px; }}
.fc-chip {{ display:inline-flex; align-items:center; gap:5px; padding:4px 10px; border-radius:999px; font-size:.76rem;
  font-weight:600; color:{TINTA_2}; background:{PAPEL}; border:1px solid {BORDE}; }}
.fc-chip .fc-ic {{ font-size:15px; color:{TINTA_3}; }}
.fc-badge {{ display:inline-flex; align-items:center; gap:4px; padding:2px 9px 2px 7px; border-radius:999px;
  font-size:.69rem; font-weight:700; letter-spacing:.01em; white-space:nowrap; cursor:help; }}
.fc-badge .fc-ic {{ font-size:14px; }}

/* ---------- tarjetas KPI */
.fc-kpis {{ display:grid; grid-template-columns: repeat(var(--n, 4), minmax(0, 1fr)); gap:14px; margin: 4px 0 12px; }}
@media (max-width: 1540px) {{ .fc-kpis.n5, .fc-kpis.n6 {{ grid-template-columns: repeat(3, minmax(0, 1fr)); }} }}
@media (max-width: 1050px) {{ .fc-kpis {{ grid-template-columns: repeat(2, minmax(0, 1fr)) !important; }} }}
@media (max-width: 520px) {{ .fc-kpis {{ grid-template-columns: minmax(0, 1fr) !important; }} }}
.fc-kpi {{ position:relative; overflow:hidden; border-radius:18px; padding:14px 16px 13px; cursor:default;
  background: linear-gradient(150deg, var(--s) 0%, {PAPEL} 78%); border:1px solid var(--bd);
  box-shadow: var(--fc-sombra); transition: transform .18s ease, box-shadow .18s ease; }}
.fc-kpi::after {{ content:""; position:absolute; right:-30px; top:-30px; width:96px; height:96px; border-radius:50%;
  background: var(--a); opacity:.10; transition: transform .25s ease; }}
.fc-kpi:hover {{ transform: translateY(-3px); box-shadow: var(--fc-sombra-hover); }}
.fc-kpi:hover::after {{ transform: scale(1.25); }}
.fc-kpi-top {{ display:flex; justify-content:space-between; align-items:flex-start; gap:6px; }}
.fc-kpi-ic {{ width:36px; height:36px; border-radius:11px; display:inline-flex; align-items:center; justify-content:center;
  background: var(--a); color:#fff; box-shadow: 0 6px 14px -6px var(--a); }}
.fc-kpi-et {{ font-size:.78rem; font-weight:600; color:{TINTA_2}; margin-top:10px; line-height:1.25; }}
.fc-kpi-va {{ font-size:1.5rem; font-weight:800; color:{TINTA}; letter-spacing:-.025em; line-height:1.2; margin-top:2px; }}
.fc-kpi-de {{ display:flex; align-items:center; gap:3px; font-size:.75rem; font-weight:700; margin-top:5px; }}
.fc-kpi-de .fc-ic {{ font-size:16px; }}
.fc-kpi-de.sube {{ color:{OSCURO[ESMERALDA]}; }} .fc-kpi-de.baja {{ color:{OSCURO[CORAL]}; }} .fc-kpi-de.neutro {{ color:{TINTA_3}; }}
.fc-kpi-ref {{ font-size:.68rem; color:{TINTA_3}; margin-top:1px; }}
.fc-kpi-sp {{ height:36px; margin:8px -16px -13px; background-size:100% 100%; background-repeat:no-repeat; }}
.st-key-abrir-centro [data-testid="stPageLink"] a {{ background: linear-gradient(90deg, #F59E0B, #FBBF24); border-radius:12px; padding:9px 18px; width:max-content; }}
.st-key-abrir-centro [data-testid="stPageLink"] a * {{ color:#1A1203 !important; font-weight:800; }}
.st-key-abrir-centro [data-testid="stPageLink"] a:hover {{ filter:brightness(1.07); }}
/* ---------- invitación al Centro de mando (siempre de noche, como la terminal) */
.fc-cen {{ position:relative; overflow:hidden; border-radius:20px; min-height:148px; padding:22px 26px; margin:4px 0 8px; color:#E8EEFC;
  background: radial-gradient(520px 200px at 82% 108%, rgba(34,211,238,.30), transparent 70%),
    radial-gradient(420px 220px at 12% -20%, rgba(79,140,255,.34), transparent 70%), #070B17; border:1px solid #1E2A49; }}
.fc-cen-piso {{ position:absolute; left:-30%; right:-30%; bottom:-64%; height:170%; transform: perspective(320px) rotateX(62deg); opacity:.55;
  background: repeating-linear-gradient(90deg, rgba(79,140,255,.45) 0 1px, transparent 1px 46px), repeating-linear-gradient(0deg, rgba(34,211,238,.4) 0 1px, transparent 1px 46px);
  -webkit-mask-image: linear-gradient(transparent 30%, #000); mask-image: linear-gradient(transparent 30%, #000); animation: fc-avanza 3.2s linear infinite; }}
@keyframes fc-avanza {{ to {{ background-position: 0 0, 0 46px; }} }}
.fc-cen-bar {{ position:absolute; right:28px; bottom:0; width:38%; height:84%; display:flex; align-items:flex-end; gap:4px; }}
.fc-cen-bar i {{ flex:1; height:var(--h); border-radius:3px 3px 0 0; background: linear-gradient(180deg, #FBBF24, #10B981 45%, #2563EB); opacity:.85;
  transform-origin: bottom; animation: fc-sube 1.1s cubic-bezier(.2,.9,.3,1) var(--d) both; }}
@keyframes fc-sube {{ from {{ transform: scaleY(0); }} }}
.fc-cen-txt {{ position:relative; max-width:56%; }}
.fc-cen-eye {{ font-size:.68rem; font-weight:800; letter-spacing:.12em; text-transform:uppercase; color:#22D3EE; }}
.fc-cen-t {{ font-size:1.45rem; font-weight:800; letter-spacing:-.025em; line-height:1.2; margin:3px 0 4px; color:#E8EEFC; }}
.fc-cen-s {{ font-size:.86rem; color:#B4C0DA; line-height:1.5; }}
@media (max-width: 760px) {{ .fc-cen-txt {{ max-width:100%; }} .fc-cen-bar {{ opacity:.22; width:70%; }} }}
@media (prefers-reduced-motion: reduce) {{ .fc-cen-piso, .fc-cen-bar i {{ animation:none; }} }}
.fc-kpi-sub {{ font-size:.73rem; color:{TINTA_3}; margin-top:3px; }}

/* ---------- tarjetas (contenedores con key que empieza por "tarjeta") */
[class*="st-key-tarjeta"] {{ background:{PAPEL}; border:1px solid {BORDE}; border-radius:18px; padding:16px 18px 8px;
  box-shadow: var(--fc-sombra); transition: box-shadow .18s ease; }}
[class*="st-key-tarjeta"]:hover {{ box-shadow: var(--fc-sombra-hover); }}
.fc-sec {{ display:flex; align-items:center; gap:8px; margin: 2px 0 2px; }}
.fc-sec .fc-ic {{ color: var(--a); font-size:21px; }}
.fc-sec-t {{ font-size:1.02rem; font-weight:800; color:{TINTA}; letter-spacing:-.01em; }}
.fc-sec-s {{ font-size:.8rem; color:{TINTA_3}; margin: 0 0 6px 29px; }}

/* ---------- hallazgos */
.fc-grid {{ display:grid; grid-template-columns: repeat(auto-fit, minmax(255px, 1fr)); gap:14px; margin: 4px 0 6px; }}
.fc-hall {{ position:relative; background:{PAPEL}; border:1px solid {BORDE}; border-radius:18px; padding:16px 16px 14px;
  box-shadow: var(--fc-sombra); transition: transform .18s ease, box-shadow .18s ease; overflow:hidden; }}
.fc-hall::before {{ content:""; position:absolute; left:0; right:0; top:0; height:4px; background: var(--a); }}
.fc-hall:hover {{ transform: translateY(-3px); box-shadow: var(--fc-sombra-hover); }}
.fc-hall-top {{ display:flex; align-items:center; justify-content:space-between; gap:8px; margin-bottom:8px; }}
.fc-hall-ic {{ width:34px; height:34px; border-radius:10px; display:inline-flex; align-items:center; justify-content:center;
  background: var(--s); color: var(--o); }}
.fc-hall-t {{ font-size:.95rem; font-weight:800; color:{TINTA}; line-height:1.3; margin-bottom:4px; }}
.fc-hall-x {{ font-size:.83rem; color:{TINTA_2}; line-height:1.5; }}
.fc-hall-x b {{ color:{TINTA}; }}

/* ---------- estado y procedencia */
.fc-estado {{ display:flex; flex-direction:column; gap:2px; }}
.fc-est {{ display:flex; align-items:flex-start; gap:10px; padding:9px 4px; border-bottom:1px dashed {BORDE}; }}
.fc-est:last-child {{ border-bottom:none; }}
.fc-est-ic {{ width:28px; height:28px; border-radius:9px; display:inline-flex; align-items:center; justify-content:center;
  background: var(--s); color: var(--o); flex-shrink:0; }}
.fc-est-ic .fc-ic {{ font-size:17px; }}
.fc-est-t {{ font-size:.84rem; font-weight:700; color:{TINTA}; }}
.fc-est-x {{ font-size:.76rem; color:{TINTA_3}; line-height:1.4; }}
.fc-est-v {{ margin-left:auto; text-align:right; font-size:.84rem; font-weight:800; color:var(--o); white-space:nowrap; }}
.fc-barra {{ height:8px; border-radius:99px; background:{CARRIL}; overflow:hidden; margin-top:6px; }}
.fc-barra > div {{ height:100%; border-radius:99px; background: linear-gradient(90deg, {ESMERALDA}, {TURQUESA}); }}

/* ---------- «En pocas palabras»: la conclusión del módulo antes de los gráficos */
.fc-resp {{ display:flex; gap:14px; align-items:flex-start; padding:14px 18px; border-radius:16px; margin: 4px 0 14px;
  background: linear-gradient(110deg, {SUAVE[AZUL]} 0%, {SUAVE[VIOLETA]} 60%, {SUAVE[TURQUESA]} 100%); border:1px solid {BORDE}; }}
.fc-resp-ic {{ width:38px; height:38px; border-radius:12px; flex-shrink:0; display:flex; align-items:center; justify-content:center;
  background: linear-gradient(135deg, {AZUL}, {VIOLETA}); color:#fff; box-shadow: 0 6px 14px -6px {AZUL}; }}
.fc-resp-t {{ font-size:.7rem; font-weight:800; letter-spacing:.1em; text-transform:uppercase; color:{OSCURO[VIOLETA]}; }}
.fc-resp-x {{ font-size:.98rem; font-weight:600; color:{TINTA}; line-height:1.5; margin-top:2px; }}
.fc-resp-x b {{ color:{OSCURO[AZUL]}; }}

/* ---------- guía de pasos y leyenda de etiquetas (inicio) */
.fc-pasos {{ display:grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap:12px; margin: 2px 0 12px; }}
.fc-paso {{ display:flex; gap:12px; align-items:flex-start; padding:12px 14px; border-radius:14px; background:{PAPEL};
  border:1px solid {BORDE}; }}
.fc-paso-n {{ width:30px; height:30px; border-radius:50%; flex-shrink:0; display:flex; align-items:center; justify-content:center;
  font-weight:800; font-size:.9rem; color:#fff; background: var(--a); }}
.fc-paso-t {{ font-size:.86rem; font-weight:800; color:{TINTA}; }}
.fc-paso-x {{ font-size:.78rem; color:{TINTA_2}; line-height:1.45; margin-top:1px; }}
.fc-leyenda {{ display:grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap:8px 16px; }}
.fc-leyenda div {{ font-size:.8rem; color:{TINTA_2}; line-height:1.45; }}
.fc-kpi-ex {{ font-size:.72rem; color:{TINTA_3}; line-height:1.35; margin-top:2px; }}

/* ---------- recuadros de aviso */
.fc-aviso {{ display:flex; gap:12px; align-items:flex-start; padding:12px 16px; border-radius:14px; margin: 6px 0 12px;
  background: var(--s); border:1px solid var(--bd); color:{TINTA_2}; font-size:.86rem; line-height:1.5; }}
.fc-aviso .fc-ic {{ color: var(--o); font-size:22px; margin-top:1px; }}
.fc-aviso b {{ color:{TINTA}; }}

/* ---------- accesos directos (page_link dentro de tarjetas) */
[class*="st-key-tarjeta-acceso"] {{ background: linear-gradient(150deg, var(--fc-s, {PAPEL_2}), {PAPEL} 70%); }}
[class*="st-key-tarjeta-acceso"]:hover {{ transform: translateY(-3px); }}
[data-testid="stPageLink"] a {{ border-radius: 10px; font-weight: 700; }}

/* ---------- widgets */
[data-testid="stDownloadButton"] button[kind="tertiary"], [data-testid="stBaseButton-tertiary"] {{ color: {OSCURO[AZUL]}; }}
[data-testid="stExpander"] details {{ border-radius: 14px; background:{PAPEL}; }}
[data-testid="stDataFrame"] {{ border-radius: 12px; }}
[data-testid="stTabs"] button[role="tab"] {{ font-weight: 700; }}

/* ---------- gráficos: el texto y la rejilla siguen al tema del visitante sin esperar a que se redibujen */
.js-plotly-plot .xtick text, .js-plotly-plot .ytick text, .js-plotly-plot .legendtext, .js-plotly-plot .xtitle, .js-plotly-plot .ytitle,
.js-plotly-plot .y2title, .js-plotly-plot .y2tick text {{ fill: {TINTA_2} !important; }}
.js-plotly-plot .gridlayer path {{ stroke: {GRILLA} !important; }}
.js-plotly-plot .hoverlayer .hovertext path, .js-plotly-plot .hoverlayer .legend .bg {{ fill: {PAPEL_2} !important; stroke: {BORDE} !important; }}
.js-plotly-plot .hoverlayer text {{ fill: {TINTA} !important; }}
.js-plotly-plot .annotation-text-g .bg {{ fill: {PAPEL} !important; }}
.js-plotly-plot .bartext-outside {{ fill: {TINTA_2} !important; }}

@media (max-width: 760px) {{
  .fc-hero {{ flex-wrap: wrap; padding: 14px 16px; }}
  .fc-hero-chips {{ align-items:flex-start; flex-direction:row; flex-wrap:wrap; }}
  .fc-brand {{ font-size: 1.3rem; }}
  .fc-kpi-va {{ font-size: 1.3rem; }}
  [data-testid="stMainBlockContainer"] {{ padding-top: 1.6rem; }}
}}
</style>
"""


def aplicar_tema() -> None:
    registrar_plantillas()
    st.html(_css())


# ----------------------------------------------------------------------------- componentes
def e(texto) -> str:
    return html.escape(str(texto), quote=True)


def icono(nombre: str, tam: int | None = None, color: str | None = None) -> str:
    estilo = ";".join(x for x in (f"font-size:{tam}px" if tam else "", f"color:{color}" if color else "") if x)
    return f'<span class="fc-ic" style="{estilo}">{nombre}</span>'


def insignia(tipo: str, texto: str | None = None) -> str:
    etiqueta, ic, color, ayuda = P.INSIGNIAS[tipo]
    return (f'<span class="fc-badge" title="{e(ayuda)}" style="background:{suave(color)};color:{oscuro(color)};'
            f'border:1px solid {color}33">{icono(ic)}{e(texto or etiqueta)}</span>')


def chips(items: Iterable[tuple[str, str]]) -> str:
    return '<div class="fc-chips">' + "".join(f'<span class="fc-chip">{icono(i)}{e(t)}</span>' for i, t in items) + "</div>"


def encabezado_inicio(logo_uncp: str, logo_facultad: str, actualizado: str) -> None:
    logos = "".join(f'<img src="{src}" alt="{alt}">' for src, alt in ((logo_uncp, "Logo de la UNCP"),
                                                                       (logo_facultad, "Logo de la Facultad de Economía")) if src)
    st.html(f"""
<div class="fc-hero">
  <div class="fc-hero-logos">{logos}</div>
  <div class="fc-hero-txt">
    <div class="fc-eyebrow">Finanzas I · Unidad II · Tema N.º 96 · UNCP</div>
    <div class="fc-brand">FinCrowd <span>Perú</span></div>
    <div class="fc-hero-sub">Fintech y financiamiento participativo (crowdfunding) en el Perú: oferta y condiciones, 2022-2026</div>
    <div class="fc-hero-meta">Diego Sebastián Aliaga Damián (2024200481M) · Facultad de Economía · Docente: Dr. Ciro Iván Machacuay Meza</div>
  </div>
  <div class="fc-hero-chips">
    <span class="fc-chip">{icono('event_available')}Datos hasta {e(actualizado)}</span>
    <span class="fc-chip">{icono('database')}BCRP · SMV</span>
  </div>
</div>""")


def encabezado_pagina(titulo: str, subtitulo: str, ic: str, color: str, modulo: str, color_b: str | None = None) -> None:
    b = color_b or {P.AZUL: P.VIOLETA, P.VIOLETA: P.AZUL, P.ESMERALDA: P.TURQUESA, P.TURQUESA: P.AZUL, P.CORAL: P.AMARILLO,
                    P.AMARILLO: P.CORAL}.get(color, P.AZUL)
    st.html(f"""
<div class="fc-ph" style="--a:{color};--b:{b};--o:{oscuro(color)}">
  <div class="fc-chipic">{icono(ic)}</div>
  <div><div class="fc-ph-eye">{e(modulo)}</div><div class="fc-ph-t">{e(titulo)}</div><div class="fc-ph-s">{e(subtitulo)}</div></div>
</div>""")


def seccion(titulo: str, ic: str, color: str | None = None, subtitulo: str | None = None, extra: str = "") -> None:
    color = color or P.AZUL
    sub = f'<div class="fc-sec-s">{e(subtitulo)}</div>' if subtitulo else ""
    st.html(f'<div class="fc-sec" style="--a:{color}">{icono(ic)}<span class="fc-sec-t">{e(titulo)}</span>{extra}</div>{sub}')


def minigrafico(serie: list, color: str) -> str:
    """Línea pequeña con la evolución mensual de la cifra (sin escala: solo la forma). Los vacíos cortan la línea."""
    v = [float(x) if x is not None and not pd.isna(x) else None for x in serie]
    reales = [x for x in v if x is not None]
    if len(reales) < 3:
        return ""
    lo, hi = min(reales), max(reales)
    rango = (hi - lo) or 1.0
    tramos, actual = [], []
    for i, x in enumerate(v):
        if x is None:
            tramos, actual = (tramos + [actual] if len(actual) > 1 else tramos), []
        else:
            actual.append((100 * i / (len(v) - 1), 29 - 26 * (x - lo) / rango))
    if len(actual) > 1:
        tramos.append(actual)
    trazos = ""
    for t in tramos:
        puntos = " ".join(f"{a:.1f},{b:.1f}" for a, b in t)
        trazos += (f'<polygon points="{t[0][0]:.1f},32 {puntos} {t[-1][0]:.1f},32" fill="{color}" fill-opacity=".14"></polygon>'
                   f'<polyline points="{puntos}" fill="none" stroke="{color}" stroke-width="1.8" stroke-linejoin="round" '
                   'vector-effect="non-scaling-stroke"></polyline>')
    svg = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 32" preserveAspectRatio="none">{trazos}</svg>'
    # Como imagen de fondo: st.html elimina las etiquetas <svg> al limpiar el HTML
    return (f'<div class="fc-kpi-sp" role="img" aria-label="Evolución mensual en tu selección" '
            f'style="background-image:url(&quot;data:image/svg+xml,{quote(svg)}&quot;)"></div>')


def portada_centro(meses: int, trimestres: pd.Series) -> None:
    """Invitación animada al Centro de mando 3D (solo CSS). Las barras son el monto financiado por trimestre (base real)."""
    tope = float(trimestres.max())
    barras = "".join(f'<i title="{e(k)}: S/ {v / 1e6:.2f} M" style="--h:{max(1.0, 100 * v / tope):.1f}%;--d:{i * .07:.2f}s"></i>'
                     for i, (k, v) in enumerate(trimestres.items()))
    st.html(f"""
<div class="fc-cen"><div class="fc-cen-piso"></div><div class="fc-cen-bar" aria-hidden="true">{barras}</div>
  <div class="fc-cen-txt"><div class="fc-cen-eye">Nuevo · Centro de mando 3D</div>
  <div class="fc-cen-t">Mira {meses} meses de crowdfunding en movimiento</div>
  <div class="fc-cen-s">Superficie 3D de costos, ciudad de montos, flujo del dinero y el registro real de la extracción, todo con los datos del estudio.</div></div>
</div>""")


def kpis(items: list[dict]) -> None:
    """items: etiqueta, valor, icono, color y opcionalmente delta (float), delta_txt, sentido ('normal', 'inverso',
    'neutro'), sub, ayuda, insignia."""
    tarjetas = []
    for k in items:
        c = k.get("color", P.AZUL)
        de = ""
        if "delta_txt" in k:
            d = k.get("delta")
            if d is None or pd.isna(d):
                clase, flecha = "neutro", "remove"
            else:
                sentido = k.get("sentido", "normal")
                flecha = "trending_up" if d > 0 else "trending_down" if d < 0 else "trending_flat"
                clase = "neutro" if sentido == "neutro" or d == 0 else (
                    "sube" if (d > 0) == (sentido == "normal") else "baja")
            ref = f'<div class="fc-kpi-ref">{e(k["delta_ref"])}</div>' if k.get("delta_ref") else ""
            de = f'<div class="fc-kpi-de {clase}">{icono(flecha)}{e(k["delta_txt"])}</div>{ref}'
        sub = f'<div class="fc-kpi-sub">{e(k["sub"])}</div>' if k.get("sub") else ""
        spark = minigrafico(k["serie"], c) if k.get("serie") else ""
        ins = insignia(k["insignia"]) if k.get("insignia") else ""
        explica = f'<div class="fc-kpi-ex">{e(k["explica"])}</div>' if k.get("explica") else ""
        tarjetas.append(f"""
<div class="fc-kpi" title="{e(k.get('ayuda', ''))}" style="--a:{c};--s:{suave(c)};--bd:{c}2E">
  <div class="fc-kpi-top"><span class="fc-kpi-ic">{icono(k.get('icono', 'insights'), 21)}</span>{ins}</div>
  <div class="fc-kpi-et">{e(k['etiqueta'])}</div>{explica}
  <div class="fc-kpi-va">{e(k['valor'])}</div>{de}{sub}{spark}
</div>""")
    n = min(len(items), 6)
    st.html(f'<div class="fc-kpis n{n}" style="--n:{n}">' + "".join(tarjetas) + "</div>")


def hallazgos(items: list[dict]) -> None:
    """items: titulo, texto (HTML permitido: viene de cifras calculadas, no del usuario), icono, color, insignia."""
    tarjetas = "".join(f"""
<div class="fc-hall" style="--a:{h['color']};--s:{suave(h['color'])};--o:{oscuro(h['color'])}">
  <div class="fc-hall-top"><span class="fc-hall-ic">{icono(h['icono'])}</span>{insignia(h.get('insignia', 'articulo'))}</div>
  <div class="fc-hall-t">{e(h['titulo'])}</div><div class="fc-hall-x">{h['texto']}</div>
</div>""" for h in items)
    st.html(f'<div class="fc-grid">{tarjetas}</div>')


def estado(items: list[dict]) -> None:
    """items: titulo, texto, valor, nivel ('ok', 'aviso', 'info', 'error'), icono, barra (0-100, opcional)."""
    niveles = {"ok": P.ESMERALDA, "aviso": P.AMARILLO, "info": P.AZUL, "error": P.CORAL}
    filas = []
    for it in items:
        c = niveles[it.get("nivel", "info")]
        barra = (f'<div class="fc-barra"><div style="width:{it["barra"]:.1f}%"></div></div>'
                 if it.get("barra") is not None else "")
        filas.append(f"""
<div class="fc-est" style="--s:{suave(c)};--o:{oscuro(c)}">
  <span class="fc-est-ic">{icono(it.get('icono', 'check_circle'))}</span>
  <div style="flex:1;min-width:0"><div class="fc-est-t">{e(it['titulo'])}</div><div class="fc-est-x">{it['texto']}</div>{barra}</div>
  <div class="fc-est-v">{e(it.get('valor', ''))}</div>
</div>""")
    st.html('<div class="fc-estado">' + "".join(filas) + "</div>")


def aviso(texto: str, ic: str = "info", color: str | None = None) -> None:
    """Recuadro informativo (HTML permitido: texto propio del dashboard)."""
    color = color or P.AZUL
    st.html(f'<div class="fc-aviso" style="--s:{suave(color)};--bd:{color}40;--o:{oscuro(color)}">{icono(ic)}<div>{texto}</div></div>')


def nota(texto: str) -> None:
    st.caption(texto)


def respuesta(texto: str, titulo: str = "En pocas palabras") -> None:
    """La conclusión del módulo en lenguaje simple, arriba de todo (HTML permitido: texto propio con cifras)."""
    st.html(f'<div class="fc-resp"><span class="fc-resp-ic">{icono("tips_and_updates", 22)}</span>'
            f'<div><div class="fc-resp-t">{e(titulo)}</div><div class="fc-resp-x">{texto}</div></div></div>')


def guia_pasos(pasos: list[tuple[str, str]]) -> None:
    colores = [P.AZUL, P.VIOLETA, P.ESMERALDA, P.CORAL]
    tarjetas = "".join(f'<div class="fc-paso" style="--a:{colores[i % 4]}"><span class="fc-paso-n">{i + 1}</span>'
                       f'<div><div class="fc-paso-t">{e(t)}</div><div class="fc-paso-x">{x}</div></div></div>'
                       for i, (t, x) in enumerate(pasos))
    st.html(f'<div class="fc-pasos">{tarjetas}</div>')


def leyenda_insignias() -> None:
    filas = "".join(f"<div>{insignia(k)}<br>{e(v[3])}</div>" for k, v in P.INSIGNIAS.items())
    st.html(f'<div class="fc-leyenda">{filas}</div>')


def chips_filtros(desde: str, hasta: str, plataformas: list[str], total: int, extra: list[tuple[str, str]] | None = None) -> None:
    n = len(plataformas)
    txt_pl = "Todas las plataformas" if n == total else (plataformas[0] if n == 1 else f"{n} de {total} plataformas")
    items = [("calendar_month", f"{desde} a {hasta}"), ("apps", txt_pl)] + (extra or [])
    st.html(chips(items).replace('<div class="fc-chips">', f'<div class="fc-chips">{insignia("filtros")}', 1))
