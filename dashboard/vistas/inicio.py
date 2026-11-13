# Diego Sebastián Aliaga Damián
# 2024200481M
# Tema 96: Fintech y financiamiento participativo (crowdfunding) en el Perú: oferta y condiciones
# Fecha: 2026-11-13
"""Inicio: cabecera, filtros, KPI con comparación, evolución, concentración, hallazgos, calidad de datos y accesos."""
from __future__ import annotations

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

import compartido as C
import datos as D
import tema as T
from vistas import graficos as G

MODOS = {"Año anterior": "interanual", "Periodo anterior": "anterior", "Sin comparación": None}


def _barra_filtros() -> None:
    with st.container(key="tarjeta-filtros"):
        c1, c2, c3 = st.columns([1.3, 0.8, 1.1], gap="medium")
        atajo = st.session_state.get("g_atajo")
        k_atajo, k_grupo = C.clave("w_atajo"), C.clave("w_grupo")
        c1.pills("Periodo rápido", list(C.ATAJOS), key=k_atajo, on_change=C.aplicar_atajo, args=(k_atajo,),
                 default=atajo if atajo in C.ATAJOS else None,
                 help="Ajusta el periodo global; también puedes moverlo con el control de la barra lateral.")
        c2.segmented_control("Plataformas", ["Todas", "Activas", "Líder"], key=k_grupo, default=C.grupo_actual(),
                             on_change=C.aplicar_grupo_plataformas, args=(k_grupo,),
                             help=f"Activas: las {len(C.activas())} plataformas que financiaron al menos un proyecto. "
                                  f"Líder: {C.resultados()['plataforma_lider']}.")
        c3.segmented_control("Comparar con", list(MODOS), key="w_comparar", default=st.session_state.get("g_comparar"),
                             on_change=C.guardar_comparacion,
                             format_func=lambda m: {"Año anterior": "Año previo", "Periodo anterior": "Periodo previo",
                                                    "Sin comparación": "No"}[m],
                             help="Año previo: los mismos meses un año antes (ventanas de hasta 12 meses). "
                                  "Periodo previo: igual duración, justo antes.")
        desde, hasta, plataformas = C.filtros()
        T.chips_filtros(desde, hasta, plataformas, len(D.PLATAFORMAS))


def _kpis(v: pd.DataFrame, desde: str, hasta: str, plataformas: list[str]) -> dict:
    k = D.resumen(v)
    modo = MODOS.get(st.session_state.get("g_comparar") or "Sin comparación")
    comp = D.periodo_comparacion(desde, hasta, modo, C.todos_los_periodos()) if modo else None
    p = D.resumen(D.filtrar(C.base(), comp[0], comp[1], plataformas)) if comp else None
    ref = f"vs {comp[0]} a {comp[1]}" if comp else ""
    sin = ("sin comparación" if not modo else "usa un periodo de hasta 12 meses"
           if modo == "interanual" and D.meses_entre(desde, hasta) > 12 else "sin periodo previo en los datos")

    def var(clave: str, tipo: str = "pct"):
        if p is None:
            return float("nan"), sin
        if tipo == "pp":
            d = k[clave] - p[clave] if pd.notna(k[clave]) and pd.notna(p[clave]) else float("nan")
            return d, (f"{'+' if d > 0 else ''}{C.num(d, 1)}{C.NBSP}p.{C.NBSP}p." if pd.notna(d) else "sin base previa")
        if tipo == "pts":
            d = k[clave] - p[clave] if pd.notna(k[clave]) and pd.notna(p[clave]) else float("nan")
            return d, (f"{'+' if d > 0 else ''}{C.num(d)}{C.NBSP}puntos" if pd.notna(d) else "sin base previa")
        d = D.variacion(k[clave], p[clave])
        return d, (f"{'+' if d > 0 else ''}{C.pct(d)}" if pd.notna(d) else "sin actividad previa")

    cota = "cota" if (v.estado_simv == "no_obtenido").any() else "filtros"
    items = []
    for clave, etiqueta, valor, ic, color, tipo, sentido, ayuda, ins in (
            ("monto", "Monto financiado", C.soles_m(k["monto"]), "payments", T.AZUL, "pct", "normal",
             "Suma del monto financiado en los meses con registros del portal de la SMV (soles corrientes).", cota),
            ("financiados", "Proyectos financiados", C.num(k["financiados"]), "rocket_launch", T.TURQUESA, "pct", "normal",
             "Proyectos que alcanzaron su financiamiento en el periodo.", None),
            ("colocacion_pct", "Tasa de colocación", C.pct(k["colocacion_pct"]), "target", T.ESMERALDA, "pp", "normal",
             "Financiados entre publicados, con sumas del periodo (un proyecto puede financiarse en un mes posterior).", None),
            ("monto_medio", "Monto medio por proyecto", f"S/{C.NBSP}{C.num(k['monto_medio'] / 1e3, 1)} mil" if pd.notna(k["monto_medio"]) else "—",
             "request_quote", T.VIOLETA, "pct", "normal", "Monto financiado entre proyectos financiados.", None),
            ("hhi", "Concentración (IHH)", C.num(k["hhi"]), "donut_large", T.CORAL, "pts", "neutro",
             "Índice de Herfindahl-Hirschman sobre el monto: 10 000 significa que una sola plataforma lo reúne todo.", None),
            ("participacion_lider_pct", "Participación de la líder", C.pct(k["participacion_lider_pct"]), "workspace_premium",
             T.AMARILLO, "pp", "neutro", "Porcentaje del monto que reúne la plataforma con mayor monto en la selección.", None)):
        d, txt = var(clave, tipo)
        item = {"etiqueta": etiqueta, "valor": valor, "icono": ic, "color": color, "delta": d, "delta_txt": txt,
                "delta_ref": ref if pd.notna(d) else "", "sentido": sentido, "ayuda": ayuda, "insignia": ins}
        if clave == "participacion_lider_pct" and k["lider"]:
            item["sub"] = k["lider"]
        if clave == "hhi":
            item["sub"] = f"{k['plataformas_activas']} de {k['plataformas_seleccionadas']} plataformas con financiamiento"
        items.append(item)
    T.kpis(items)
    return k


def _evolucion(v: pd.DataFrame, desde: str, hasta: str) -> None:
    G.monto_por_plataforma(v, desde, hasta, "inicio")


def _concentracion(v: pd.DataFrame) -> None:
    c1, c2 = st.columns([1, 1.25], gap="medium")
    part = D.participacion(v)
    part = part[part.monto > 0]
    with c1, st.container(key="tarjeta-participacion"):
        T.seccion("Participación en el monto", "pie_chart", T.CORAL, "Reparto del monto financiado en la selección.")
        if part.empty:
            T.aviso("Sin montos en la selección.", "info", T.AZUL)
        else:
            fig = go.Figure(go.Pie(labels=part.plataforma, values=part.monto, hole=0.64, sort=False,
                                   marker=dict(colors=[T.COLOR_PLATAFORMA[p] for p in part.plataforma], line=dict(color="white", width=2)),
                                   textinfo="none", hovertemplate="<b>%{label}</b><br>S/ %{value:,.0f}<br>%{percent}<extra></extra>"))
            lider = part.iloc[0]
            fig.add_annotation(text=f"<b>{C.num(lider.participacion_pct, 1)} %</b><br><span style='font-size:11px'>{lider.plataforma}</span>",
                               showarrow=False, font=dict(size=20, color=T.TINTA))
            fig.update_layout(legend=dict(orientation="h", y=-0.08, yanchor="top"), margin=dict(t=10, b=10))
            T.figura(fig, "fincrowd_participacion", 320, part.set_index("plataforma")[["monto", "participacion_pct"]])
    with c2, st.container(key="tarjeta-ihh"):
        T.seccion("Concentración por año (IHH)", "stacked_bar_chart", T.VIOLETA,
                  "Índice de Herfindahl-Hirschman del monto: máximo 10 000 (una sola plataforma).")
        a = D.por_anio(v)
        a = a[a.monto > 0]
        if a.empty:
            T.aviso("Sin montos en la selección.", "info", T.AZUL)
        else:
            meses = v.groupby("anio").periodo.nunique()
            etiqueta = [f"{x} ({meses[x]} m)" if meses[x] < 12 else str(x) for x in a.anio]
            fig = go.Figure()
            fig.add_bar(x=etiqueta, y=a.hhi, marker=dict(color=a.hhi, colorscale=[[0, "#C4B5FD"], [1, T.VIOLETA]], cmin=0, cmax=10000),
                        text=[C.num(h) for h in a.hhi], textposition="outside", cliponaxis=False, name="IHH",
                        customdata=a[["participacion_lider_pct", "plataformas_activas"]].to_numpy(),
                        hovertemplate="<b>%{x}</b><br>IHH %{y:,.0f}<br>Líder: %{customdata[0]:.1f} %<br>"
                                      "Plataformas activas: %{customdata[1]}<extra></extra>")
            fig.update_layout(yaxis=dict(range=[0, 11000], title="IHH"), showlegend=False)
            fig.add_hline(y=10000, line=dict(color=T.TINTA_3, dash="dot", width=1))
            T.figura(fig, "fincrowd_ihh_anual", 320, a.set_index("anio")[["hhi", "participacion_lider_pct", "plataformas_activas", "monto"]])


def _hallazgos() -> None:
    r, t = C.resultados(), C.tablas()
    an, h1, ht, h2 = r["anual"], r["h1"], r["h1_tendencia"], r["h2"]
    t3 = t["t3_plataformas_financieros"]
    roa = t3[(t3.plataforma == r["plataforma_lider"]) & (t3.anio == 2025)].roa_pct
    e1 = r["e1"]
    T.seccion("Hallazgos principales", "lightbulb", T.AMARILLO, "Resultados del artículo: no cambian con los filtros.")
    T.hallazgos([
        {"titulo": "Crecimiento acelerado", "icono": "trending_up", "color": T.AZUL,
         "texto": f"El monto anual pasó de <b>{C.soles_m(an['2022']['monto_soles'])}</b> en 2022 a "
                  f"<b>{C.soles_m(an['2025']['monto_soles'])}</b> en 2025, aunque el ritmo interanual se desacelera."},
        {"titulo": "Mercado muy concentrado", "icono": "hub", "color": T.CORAL,
         "texto": f"De {len(D.PLATAFORMAS)} sociedades, solo <b>{r['plataformas_con_financiamiento']}</b> financiaron proyectos "
                  f"y {r['plataforma_lider']} reúne el <b>{C.pct(r['participacion_lider_periodo_pct'])}</b> del monto."},
        {"titulo": "Acceso según el modelo de negocio", "icono": "groups", "color": T.ESMERALDA,
         "texto": f"Colocación empresarial <b>{C.pct(h2['colocacion_empresarial_pct'])}</b> y personal "
                  f"<b>{C.pct(h2['colocacion_personal_pct'])}</b> (z = {C.num(h2['z'], 2)}), pero dentro de la líder la "
                  f"diferencia no es significativa (Fisher p {C.p_txt(h2['dentro_lider']['p_valor_fisher'])})."},
        {"titulo": "La reforma no explica el aumento", "icono": "gavel", "color": T.VIOLETA,
         "texto": f"La mediana mensual sube de {C.soles_m(h1['mediana_antes_soles'])} a <b>{C.soles_m(h1['mediana_despues_soles'])}</b>, "
                  f"pero {len(ht['cortes_placebo'])} cortes placebo también son significativos y el crecimiento interanual cae de "
                  f"{C.num(ht['interanual_mediana_antes_pct'])} % a {C.num(ht['interanual_mediana_despues_pct'])} %."},
        {"titulo": "Solo la líder es rentable", "icono": "account_balance", "color": T.TURQUESA,
         "texto": f"ROA anualizado de {r['plataforma_lider']} en 2025: <b>{C.pct(roa.iloc[0]) if len(roa) else '—'}</b>. "
                  f"Sus ingresos equivalen a una mediana de <b>{C.num(r['costo_intermediacion_lider']['mediana_trimestral_pct'], 2)} %</b> "
                  f"del monto financiado por trimestre (no es una tasa de interés)."},
        {"titulo": "Precio no comparable", "icono": "visibility_off", "color": T.AMARILLO,
         "texto": f"La SMV no publica la tasa ni el plazo de cada operación. Con {len(e1)} tasas del BCRP, ninguna "
                  f"correlación con el monto es significativa (menor p = {min(x['p_valor'] for x in e1.values()):.3f})."},
    ])


def _calidad(v: pd.DataFrame) -> None:
    r, cif, aud = C.resultados(), C.cifras(), C.auditoria()
    ok_hash, h = C.integridad()
    k_total = D.resumen(C.base())
    k_sel = D.resumen(v)
    c1, c2 = st.columns([1.25, 1], gap="medium")
    with c1, st.container(key="tarjeta-calidad"):
        T.seccion("Calidad y procedencia de los datos", "verified_user", T.ESMERALDA)
        T.estado([
            {"titulo": "Integridad de la base procesada", "icono": "fingerprint", "nivel": "ok" if ok_hash else "error",
             "texto": f"SHA-256 recalculado al abrir el dashboard: <code>{h[:16]}…</code>",
             "valor": "Coincide" if ok_hash else "No coincide"},
            {"titulo": "Cobertura del portal de la SMV", "icono": "travel_explore", "nivel": "aviso" if k_total["filas_obtenidas"] < k_total["filas"] else "ok",
             "texto": f"{k_total['filas_obtenidas']} de {k_total['filas']} plataforma-mes obtenidos; los faltantes no se imputan "
                      f"(los montos son una cota inferior). En tu selección: {C.pct(k_sel['cobertura_pct'])}.",
             "valor": C.pct(k_total["cobertura_pct"]), "barra": k_total["cobertura_pct"]},
            {"titulo": "Extracción automatizada", "icono": "api", "nivel": "info",
             "texto": "API del BCRP (10 series) y de la SMV (estados financieros) y rastreo del portal de proyectos de la SMV.",
             "valor": f"{cif.get('solicitudesHTTP', '—')} solicitudes"},
            {"titulo": "Auditoría automatizada", "icono": "fact_check",
             "nivel": "ok" if aud.get("no_cumplen") == 0 and aud.get("no_ejecutados") == 0 else "aviso",
             "texto": f"Último reporte: {aud.get('fecha', '—')}. {C.pruebas_definidas()} pruebas automatizadas definidas en el repositorio.",
             "valor": f"{aud.get('cumplen', '—')} controles OK" if aud else "—"},
        ])
    with c2, st.container(key="tarjeta-cobertura"):
        T.seccion("Estado de la consulta por plataforma", "grid_view", T.TURQUESA, "Meses de tu selección según la respuesta del portal.")
        cuenta = v.groupby(["plataforma", "estado_simv"]).size().unstack(fill_value=0).reindex(columns=list(D.ESTADOS), fill_value=0)
        cuenta = cuenta.reindex([p for p in reversed(D.PLATAFORMAS) if p in cuenta.index])
        fig = go.Figure()
        for est, nombre in D.ESTADOS.items():
            fig.add_bar(y=cuenta.index, x=cuenta[est], name=nombre, orientation="h", marker_color=T.COLOR_ESTADO[est],
                        hovertemplate=f"<b>%{{y}}</b><br>{nombre}: %{{x}} meses<extra></extra>")
        fig.update_layout(barmode="stack", xaxis_title="Meses", legend=dict(y=1.02), margin=dict(l=6, t=30))
        T.figura(fig, "fincrowd_estado_consulta", 290)


def _accesos() -> None:
    T.seccion("Explorar más", "explore", T.AZUL)
    destinos = [("simulador", "Simulador de financiamiento", "calculate", T.CORAL,
                 "Compara una tasa hipotética del FPF con la TEA observada del crédito tradicional."),
                ("credito", "Comparación financiera", "account_balance", T.AMARILLO,
                 "Tasas del BCRP por segmento, qué es comparable y la asociación exploratoria E1."),
                ("reproducibilidad", "Reproducibilidad", "sync_alt", T.ESMERALDA,
                 "Cómo regenerar la base, las tablas y el artículo, y el reporte de auditoría.")]
    cols = st.columns(3, gap="medium")
    for col, (clave, titulo, ic, color, texto) in zip(cols, destinos):
        with col, st.container(key=f"tarjeta-acceso-{clave}"):
            st.html(f'<div class="fc-hall-top" style="--s:{T.SUAVE[color]};--o:{T.OSCURO[color]}"><span class="fc-hall-ic">'
                    f'{T.icono(ic)}</span></div><div class="fc-hall-t">{T.e(titulo)}</div><div class="fc-hall-x">{T.e(texto)}</div>')
            if clave in C.PAGINAS:
                st.page_link(C.PAGINAS[clave], label="Abrir", icon=":material/arrow_forward:")


def pagina() -> None:
    r = C.resultados()
    T.encabezado_inicio(C.imagen_b64(str(C.IMG_UNCP)), C.imagen_b64(str(C.IMG_FACULTAD)), C.mes_txt(C.todos_los_periodos()[-1]))
    _barra_filtros()
    desde, hasta, plataformas = C.filtros()
    if not plataformas:
        T.aviso("Elige al menos una plataforma en la barra lateral.", "filter_alt_off", T.CORAL)
        return
    v = C.vista_filtrada()
    _kpis(v, desde, hasta, plataformas)
    _evolucion(v, desde, hasta)
    _concentracion(v)
    _hallazgos()
    _calidad(v)
    _accesos()
    T.nota(f"Fuentes: SMV (SIMV y API OData) y BCRP (BCRPData). Los KPI usan solo meses con registros del portal; el periodo de "
           f"actividad del FPF empieza en {r['inicio_actividad_fpf']}. Sin filtros, las cifras coinciden con las tablas del artículo.")
