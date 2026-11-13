# Diego Sebastián Aliaga Damián
# 2024200481M
# Tema 96: Fintech y financiamiento participativo (crowdfunding) en el Perú: oferta y condiciones
# Fecha: 2026-11-13
"""Identidad visual FinCrowd Perú: paleta, CSS, plantilla de Plotly y componentes HTML reutilizables.

Los componentes solo dan forma: reciben cifras ya calculadas (datos.py o salidas del análisis) y nunca las alteran.
Íconos: Material Symbols Rounded, la misma fuente que trae Streamlit para los íconos :material/...:.
"""
from __future__ import annotations

import html
from typing import Iterable

import pandas as pd
import plotly.graph_objects as go
import plotly.io as pio
import streamlit as st

import datos as D

# ----------------------------------------------------------------------------- paleta
AZUL, TURQUESA, ESMERALDA, CORAL, AMARILLO, VIOLETA = "#2563EB", "#06B6D4", "#10B981", "#FB7185", "#FBBF24", "#8B5CF6"
FONDO, TINTA, TINTA_2, TINTA_3, BORDE, GRILLA = "#FAFBFF", "#0F172A", "#475569", "#64748B", "#E2E8F0", "#EDF1F7"
PALETA = [AZUL, ESMERALDA, CORAL, AMARILLO, VIOLETA, TURQUESA]
# Tono suave (fondo) y tono oscuro (texto legible) de cada acento
SUAVE = {AZUL: "#EFF6FF", TURQUESA: "#ECFEFF", ESMERALDA: "#ECFDF5", CORAL: "#FFF1F2", AMARILLO: "#FFFBEB", VIOLETA: "#F5F3FF"}
OSCURO = {AZUL: "#1D4ED8", TURQUESA: "#0E7490", ESMERALDA: "#047857", CORAL: "#BE123C", AMARILLO: "#B45309", VIOLETA: "#6D28D9"}
# El color sigue a la entidad en todas las páginas
COLOR_PLATAFORMA = {"Inversiones.io": AZUL, "Afluenta": ESMERALDA, "Prestopolis": CORAL,
                    "Inversiones Neurona": AMARILLO, "Proyecto Crowd": VIOLETA, "Securite": TURQUESA}
COLOR_SERIE = {"tea_bcos_pyme_360": AZUL, "tea_cmac_pyme_360": ESMERALDA, "tea_crac_pyme_360": VIOLETA,
               "tea_bcos_consumo_360": AMARILLO, "tea_bcos_pyme_mas360": "#93C5FD", "tea_cmac_pyme_mas360": "#6EE7B7",
               "tea_crac_pyme_mas360": "#C4B5FD", "tea_bcos_consumo_mas360": "#FCD34D", "tamn": TURQUESA}
COLOR_ESTADO = {"con_registros": ESMERALDA, "sin_registros": "#CBD5E1", "no_obtenido": CORAL}
FUENTE = "Plus Jakarta Sans, Segoe UI, system-ui, -apple-system, sans-serif"

# Insignias que distinguen la naturaleza de cada cifra
INSIGNIAS = {
    "observado": ("Observado", "visibility", ESMERALDA, "Dato publicado por la fuente oficial (BCRP o SMV)."),
    "articulo": ("Resultado del artículo", "verified", AZUL, "Cifra fija de las salidas de 04_analisis.py; no depende de los filtros."),
    "filtros": ("Responde a los filtros", "filter_alt", VIOLETA, "Se recalcula con el periodo y las plataformas elegidos."),
    "cota": ("Cota inferior", "south", AMARILLO, "Los meses no obtenidos del portal no se imputan: el valor real puede ser algo mayor."),
    "hipotetico": ("Hipotético", "science", CORAL, "Supuesto definido por el usuario: no es un dato observado."),
    "referencia": ("Referencia", "info", TURQUESA, "Indicador de contexto; no es un precio del financiamiento participativo."),
}


# ----------------------------------------------------------------------------- Plotly
def registrar_plantilla() -> None:
    if "fincrowd" in pio.templates:
        return
    pio.templates["fincrowd"] = go.layout.Template(layout=dict(
        font=dict(family=FUENTE, size=12.5, color=TINTA_2), colorway=PALETA,
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        title=dict(font=dict(size=14, color=TINTA, family=FUENTE), x=0, xanchor="left"),
        hoverlabel=dict(bgcolor="white", bordercolor=BORDE, font=dict(family=FUENTE, size=12.5, color=TINTA)),
        xaxis=dict(showgrid=False, linecolor=BORDE, tickcolor=BORDE, ticks="outside", zeroline=False, title_standoff=8),
        yaxis=dict(gridcolor=GRILLA, zeroline=False, linecolor="rgba(0,0,0,0)", title_standoff=8),
        legend=dict(orientation="h", yanchor="bottom", y=1.01, xanchor="left", x=0, bgcolor="rgba(0,0,0,0)",
                    font=dict(size=12), title_text=""),
        margin=dict(l=6, r=6, t=34, b=6), bargap=0.18,
    ))
    pio.templates.default = "plotly_white+fincrowd"


def figura(fig: go.Figure, nombre: str, alto: int = 380, datos: pd.DataFrame | None = None,
           etiqueta_csv: str = "Datos del gráfico (CSV)") -> None:
    """Muestra un gráfico con el estilo FinCrowd, descarga en PNG desde la barra del gráfico y, si se pasan
    datos, un botón para bajarlos en CSV."""
    fig.update_layout(height=alto)
    config = {"displaylogo": False, "modeBarButtonsToRemove": ["lasso2d", "select2d", "autoScale2d"],
              "toImageButtonOptions": {"format": "png", "filename": nombre, "scale": 2}}
    st.plotly_chart(fig, theme=None, config=config, key=f"fig_{nombre}")
    if datos is not None:
        st.download_button(etiqueta_csv, datos.to_csv(index=True).encode("utf-8-sig"), file_name=f"{nombre}.csv",
                           mime="text/csv", icon=":material/download:", key=f"csv_{nombre}", type="tertiary")


def eje_meses(fig: go.Figure, periodos: list[str], cada: int = 6, eje: str = "x") -> list[str]:
    """Eje de categorías con meses en castellano ('ene 2024'); marca solo enero y julio para no saturar.
    Devuelve las etiquetas para usarlas como x."""
    etiquetas = [D.etiqueta_mes(p) for p in periodos]
    marcas = [l for p, l in zip(periodos, etiquetas) if (int(p[5:7]) - 1) % cada == 0]
    fig.update_layout({f"{eje}axis": dict(type="category", tickmode="array", tickvals=marcas,
                                          ticktext=[m.replace(" ", "<br>") for m in marcas], tickangle=0)})
    return etiquetas


def marcar_mes(fig: go.Figure, fecha, texto: str, color: str = TINTA_3, lado: str = "right") -> None:
    """Línea vertical con rótulo (fecha: etiqueta de la categoría, p. ej. 'dic 2025')."""
    fig.add_shape(type="line", x0=fecha, x1=fecha, y0=0, y1=1, yref="paper", line=dict(color=color, width=1.4, dash="dot"))
    fig.add_annotation(x=fecha, y=1, yref="paper", text=texto, showarrow=False, xanchor="left" if lado == "right" else "right",
                       yanchor="top", xshift=4 if lado == "right" else -4, font=dict(size=11, color=color),
                       bgcolor="rgba(255,255,255,0.85)")


# ----------------------------------------------------------------------------- CSS
CSS = f"""
<style>
:root {{
  --fc-azul:{AZUL}; --fc-turquesa:{TURQUESA}; --fc-esmeralda:{ESMERALDA}; --fc-coral:{CORAL};
  --fc-amarillo:{AMARILLO}; --fc-violeta:{VIOLETA}; --fc-tinta:{TINTA}; --fc-tinta2:{TINTA_2}; --fc-tinta3:{TINTA_3};
  --fc-borde:{BORDE}; --fc-sombra:0 1px 2px rgba(15,23,42,.04), 0 6px 18px rgba(37,99,235,.06);
  --fc-sombra-hover:0 2px 6px rgba(15,23,42,.06), 0 14px 32px rgba(37,99,235,.14);
}}
.stApp {{
  background:
    radial-gradient(1100px 420px at 100% -10%, rgba(139,92,246,.07), transparent 60%),
    radial-gradient(900px 380px at -5% -8%, rgba(6,182,212,.08), transparent 55%), {FONDO};
}}
[data-testid="stHeader"] {{ background: transparent; }}
[data-testid="stMainBlockContainer"] {{ padding-top: 2.4rem; padding-bottom: 3rem; max-width: 1380px; }}
h1, h2, h3 {{ letter-spacing: -.02em; }}
[data-testid="stCaptionContainer"], .stCaption {{ color: {TINTA_3}; }}

/* ---------- barra lateral */
[data-testid="stSidebar"] {{
  background: linear-gradient(185deg, #FFFFFF 0%, #F6F7FF 48%, #EEF4FF 100%);
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
  background: linear-gradient(120deg, #FFFFFF 0%, #F5F8FF 55%, #F2FBFF 100%); border:1px solid {BORDE};
  box-shadow: var(--fc-sombra); overflow:hidden; margin-bottom: 6px; }}
.fc-hero::before {{ content:""; position:absolute; left:0; top:0; bottom:0; width:5px;
  background: linear-gradient(180deg, {AZUL}, {VIOLETA}, {TURQUESA}); }}
.fc-hero::after {{ content:""; position:absolute; right:-60px; top:-70px; width:240px; height:240px; border-radius:50%;
  background: radial-gradient(circle, rgba(139,92,246,.13), transparent 70%); }}
.fc-hero-logos {{ display:flex; gap:10px; align-items:center; flex-shrink:0; }}
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
  font-weight:600; color:{TINTA_2}; background:#FFFFFF; border:1px solid {BORDE}; }}
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
  background: linear-gradient(150deg, var(--s) 0%, #FFFFFF 78%); border:1px solid var(--bd);
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
.fc-kpi-sub {{ font-size:.73rem; color:{TINTA_3}; margin-top:3px; }}

/* ---------- tarjetas (contenedores con key que empieza por "tarjeta") */
[class*="st-key-tarjeta"] {{ background:#FFFFFF; border:1px solid {BORDE}; border-radius:18px; padding:16px 18px 8px;
  box-shadow: var(--fc-sombra); transition: box-shadow .18s ease; }}
[class*="st-key-tarjeta"]:hover {{ box-shadow: var(--fc-sombra-hover); }}
.fc-sec {{ display:flex; align-items:center; gap:8px; margin: 2px 0 2px; }}
.fc-sec .fc-ic {{ color: var(--a); font-size:21px; }}
.fc-sec-t {{ font-size:1.02rem; font-weight:800; color:{TINTA}; letter-spacing:-.01em; }}
.fc-sec-s {{ font-size:.8rem; color:{TINTA_3}; margin: 0 0 6px 29px; }}

/* ---------- hallazgos */
.fc-grid {{ display:grid; grid-template-columns: repeat(auto-fit, minmax(255px, 1fr)); gap:14px; margin: 4px 0 6px; }}
.fc-hall {{ position:relative; background:#FFFFFF; border:1px solid {BORDE}; border-radius:18px; padding:16px 16px 14px;
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
.fc-barra {{ height:8px; border-radius:99px; background:#EEF2F7; overflow:hidden; margin-top:6px; }}
.fc-barra > div {{ height:100%; border-radius:99px; background: linear-gradient(90deg, {ESMERALDA}, {TURQUESA}); }}

/* ---------- recuadros de aviso */
.fc-aviso {{ display:flex; gap:12px; align-items:flex-start; padding:12px 16px; border-radius:14px; margin: 6px 0 12px;
  background: var(--s); border:1px solid var(--bd); color:{TINTA_2}; font-size:.86rem; line-height:1.5; }}
.fc-aviso .fc-ic {{ color: var(--o); font-size:22px; margin-top:1px; }}
.fc-aviso b {{ color:{TINTA}; }}

/* ---------- accesos directos (page_link dentro de tarjetas) */
[class*="st-key-tarjeta-acceso"] {{ background: linear-gradient(150deg, var(--fc-s, #F5F8FF), #FFFFFF 70%); }}
[class*="st-key-tarjeta-acceso"]:hover {{ transform: translateY(-3px); }}
[data-testid="stPageLink"] a {{ border-radius: 10px; font-weight: 700; }}

/* ---------- widgets */
[data-testid="stDownloadButton"] button[kind="tertiary"], [data-testid="stBaseButton-tertiary"] {{ color: {OSCURO[AZUL]}; }}
[data-testid="stExpander"] details {{ border-radius: 14px; background:#FFFFFF; }}
[data-testid="stDataFrame"] {{ border-radius: 12px; }}
[data-testid="stTabs"] button[role="tab"] {{ font-weight: 700; }}

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
    registrar_plantilla()
    st.html(CSS)


# ----------------------------------------------------------------------------- componentes
def e(texto) -> str:
    return html.escape(str(texto), quote=True)


def icono(nombre: str, tam: int | None = None, color: str | None = None) -> str:
    estilo = ";".join(x for x in (f"font-size:{tam}px" if tam else "", f"color:{color}" if color else "") if x)
    return f'<span class="fc-ic" style="{estilo}">{nombre}</span>'


def insignia(tipo: str, texto: str | None = None) -> str:
    etiqueta, ic, color, ayuda = INSIGNIAS[tipo]
    return (f'<span class="fc-badge" title="{e(ayuda)}" style="background:{SUAVE[color]};color:{OSCURO[color]};'
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
    b = color_b or {AZUL: VIOLETA, VIOLETA: AZUL, ESMERALDA: TURQUESA, TURQUESA: AZUL, CORAL: AMARILLO,
                    AMARILLO: CORAL}.get(color, AZUL)
    st.html(f"""
<div class="fc-ph" style="--a:{color};--b:{b};--o:{OSCURO.get(color, color)}">
  <div class="fc-chipic">{icono(ic)}</div>
  <div><div class="fc-ph-eye">{e(modulo)}</div><div class="fc-ph-t">{e(titulo)}</div><div class="fc-ph-s">{e(subtitulo)}</div></div>
</div>""")


def seccion(titulo: str, ic: str, color: str = AZUL, subtitulo: str | None = None, extra: str = "") -> None:
    sub = f'<div class="fc-sec-s">{e(subtitulo)}</div>' if subtitulo else ""
    st.html(f'<div class="fc-sec" style="--a:{color}">{icono(ic)}<span class="fc-sec-t">{e(titulo)}</span>{extra}</div>{sub}')


def kpis(items: list[dict]) -> None:
    """items: etiqueta, valor, icono, color y opcionalmente delta (float), delta_txt, sentido ('normal', 'inverso',
    'neutro'), sub, ayuda, insignia."""
    tarjetas = []
    for k in items:
        c = k.get("color", AZUL)
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
        ins = insignia(k["insignia"]) if k.get("insignia") else ""
        tarjetas.append(f"""
<div class="fc-kpi" title="{e(k.get('ayuda', ''))}" style="--a:{c};--s:{SUAVE.get(c, '#F8FAFC')};--bd:{c}2E">
  <div class="fc-kpi-top"><span class="fc-kpi-ic">{icono(k.get('icono', 'insights'), 21)}</span>{ins}</div>
  <div class="fc-kpi-et">{e(k['etiqueta'])}</div>
  <div class="fc-kpi-va">{e(k['valor'])}</div>{de}{sub}
</div>""")
    n = min(len(items), 6)
    st.html(f'<div class="fc-kpis n{n}" style="--n:{n}">' + "".join(tarjetas) + "</div>")


def hallazgos(items: list[dict]) -> None:
    """items: titulo, texto (HTML permitido: viene de cifras calculadas, no del usuario), icono, color, insignia."""
    tarjetas = "".join(f"""
<div class="fc-hall" style="--a:{h['color']};--s:{SUAVE[h['color']]};--o:{OSCURO[h['color']]}">
  <div class="fc-hall-top"><span class="fc-hall-ic">{icono(h['icono'])}</span>{insignia(h.get('insignia', 'articulo'))}</div>
  <div class="fc-hall-t">{e(h['titulo'])}</div><div class="fc-hall-x">{h['texto']}</div>
</div>""" for h in items)
    st.html(f'<div class="fc-grid">{tarjetas}</div>')


def estado(items: list[dict]) -> None:
    """items: titulo, texto, valor, nivel ('ok', 'aviso', 'info', 'error'), icono, barra (0-100, opcional)."""
    niveles = {"ok": ESMERALDA, "aviso": AMARILLO, "info": AZUL, "error": CORAL}
    filas = []
    for it in items:
        c = niveles[it.get("nivel", "info")]
        barra = (f'<div class="fc-barra"><div style="width:{it["barra"]:.1f}%"></div></div>'
                 if it.get("barra") is not None else "")
        filas.append(f"""
<div class="fc-est" style="--s:{SUAVE[c]};--o:{OSCURO[c]}">
  <span class="fc-est-ic">{icono(it.get('icono', 'check_circle'))}</span>
  <div style="flex:1;min-width:0"><div class="fc-est-t">{e(it['titulo'])}</div><div class="fc-est-x">{it['texto']}</div>{barra}</div>
  <div class="fc-est-v">{e(it.get('valor', ''))}</div>
</div>""")
    st.html('<div class="fc-estado">' + "".join(filas) + "</div>")


def aviso(texto: str, ic: str = "info", color: str = AZUL) -> None:
    """Recuadro informativo (HTML permitido: texto propio del dashboard)."""
    st.html(f'<div class="fc-aviso" style="--s:{SUAVE[color]};--bd:{color}40;--o:{OSCURO[color]}">{icono(ic)}<div>{texto}</div></div>')


def nota(texto: str) -> None:
    st.caption(texto)


def chips_filtros(desde: str, hasta: str, plataformas: list[str], total: int, extra: list[tuple[str, str]] | None = None) -> None:
    n = len(plataformas)
    txt_pl = "Todas las plataformas" if n == total else (plataformas[0] if n == 1 else f"{n} de {total} plataformas")
    items = [("calendar_month", f"{desde} a {hasta}"), ("apps", txt_pl)] + (extra or [])
    st.html(chips(items).replace('<div class="fc-chips">', f'<div class="fc-chips">{insignia("filtros")}', 1))
