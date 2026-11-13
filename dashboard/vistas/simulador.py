# Diego Sebastián Aliaga Damián
# 2024200481M
# Tema 96: Fintech y financiamiento participativo (crowdfunding) en el Perú: oferta y condiciones
# Fecha: 2026-11-13
"""Simulador: cuota y costo de un préstamo con una TEA hipotética del FPF frente a la TEA observada del crédito
tradicional (BCRP). La tasa del FPF nunca se presenta como observada: la SMV no la publica."""
from __future__ import annotations

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

import compartido as C
import datos as D
import tema as T


def _soles(x: float, dec: int = 2) -> str:
    return f"S/{C.NBSP}{C.num(x, dec)}" if pd.notna(x) else "—"


def pagina() -> None:
    r = C.resultados()
    T.encabezado_pagina("Simulador de financiamiento",
                        "Cuota y costo de un préstamo con una tasa supuesta del FPF frente a la TEA observada de un segmento del crédito tradicional.",
                        "calculate", T.CORAL, "Herramienta · Simulador")
    T.aviso("<b>La tasa del FPF es un supuesto tuyo, no un dato.</b> La SMV no publica la tasa de interés de las operaciones "
            "de financiamiento participativo, así que aquí no hay una tasa observada del FPF. La TEA de referencia sí es "
            "observada (BCRP), pero es el promedio de un segmento del crédito tradicional, no la oferta de una entidad concreta.",
            "science", T.CORAL)
    bcrp = D.tasas_bcrp(C.base())
    ps = list(bcrp.index)

    entradas, salidas = st.columns([1, 2.15], gap="medium")
    with entradas, st.container(key="tarjeta-sim-entradas"):
        T.seccion("Préstamo", "payments", T.AZUL)
        monto = st.number_input("Monto (S/)", min_value=1_000, max_value=2_000_000, value=50_000, step=1_000, key="w_sim_monto")
        plazo = st.slider("Plazo (meses)", 3, 60, 12, key="w_sim_plazo")
        T.seccion("Referencia", "account_balance", T.ESMERALDA, extra=T.insignia("observado", "Observada · BCRP"))
        series = [s for s in D.SERIES_BCRP if s != "tamn"]
        serie = st.selectbox("Segmento del crédito tradicional", series, index=0, format_func=D.SERIES_BCRP.get, key="w_sim_serie")
        mes = st.select_slider("Mes de la TEA", options=ps, value=ps[-1], format_func=D.etiqueta_mes, key="w_sim_mes")
        tea_ref = float(bcrp.loc[mes, serie])
        if (plazo <= 12) != serie.endswith("_360"):
            st.caption(f":orange[Un plazo de {plazo} meses corresponde al tramo "
                       f"{'≤360' if plazo <= 12 else '>360'} días; considera cambiar el segmento.]")
        T.seccion("FPF", "science", T.CORAL, extra=T.insignia("hipotetico", "Hipotético · tu supuesto"))
        igual = st.toggle("Igual a la TEA de referencia", value=True, key="w_sim_igual",
                          help="Desactívalo para suponer otra TEA para el FPF.")
        if igual or "w_sim_tea" not in st.session_state:
            st.session_state["w_sim_tea"] = round(tea_ref, 2)
        tea_elegida = st.slider("TEA hipotética del FPF (%)", 0.0, 120.0, step=0.01, format="%.2f", key="w_sim_tea",
                                disabled=igual, help="Valor que tú supones; no es un dato observado.")
        tea_fpf = tea_ref if igual else tea_elegida
        comision = st.number_input("Comisión inicial hipotética (% del monto)", 0.0, 20.0, 0.0, step=0.25, key="w_sim_com",
                                   help="Se descuenta del desembolso. El crédito tradicional se simula sin comisiones, porque la TEA "
                                        "del BCRP no las incluye.")
        ci = r["costo_intermediacion_lider"]
        st.caption(f"Referencia del artículo: los ingresos de {ci['plataforma']} equivalen a una mediana de "
                   f"{C.num(ci['mediana_trimestral_pct'], 2)} % del monto financiado por trimestre. Es un cociente de ingresos "
                   "de la plataforma, no una comisión ni una tasa observada; si lo usas como comisión, es solo un escenario.")

    tem_f, tem_r = D.tem_desde_tea(tea_fpf), D.tem_desde_tea(tea_ref)
    cuota_f, cuota_r = D.cuota_francesa(monto, tem_f, plazo), D.cuota_francesa(monto, tem_r, plazo)
    costo_f = cuota_f * plazo - monto + monto * comision / 100
    costo_r = cuota_r * plazo - monto
    tcea_f = D.tcea(monto, tea_fpf, plazo, comision)
    equilibrio = D.tea_equilibrio(monto, plazo, comision, tea_ref)
    with salidas:
        T.kpis([
            {"etiqueta": "Cuota mensual con la TEA hipotética del FPF", "valor": _soles(cuota_f), "icono": "science",
             "color": T.CORAL, "insignia": "hipotetico", "sub": f"TEA {C.num(tea_fpf, 2)} % · TEM {C.num(100 * tem_f, 3)} %"},
            {"etiqueta": "Cuota mensual con la TEA observada", "valor": _soles(cuota_r), "icono": "account_balance",
             "color": T.ESMERALDA, "insignia": "observado",
             "sub": f"TEA {C.num(tea_ref, 2)} % · {D.SERIES_BCRP[serie]} · {D.etiqueta_mes(mes)}"},
            {"etiqueta": "Costo total del FPF (intereses + comisión)", "valor": _soles(costo_f, 0), "icono": "receipt_long",
             "color": T.VIOLETA, "insignia": "hipotetico", "delta": costo_f - costo_r,
             "delta_txt": f"{'+' if costo_f - costo_r > 0 else ''}{_soles(costo_f - costo_r, 0)}", "sentido": "inverso",
             "delta_ref": f"frente a {_soles(costo_r, 0)} con la referencia"},
            {"etiqueta": "Costo efectivo anual del FPF (con comisión)", "valor": f"{C.num(tcea_f, 2)} %", "icono": "percent",
             "color": T.AMARILLO, "insignia": "hipotetico", "sub": "igual a la TEA si la comisión es cero"},
            {"etiqueta": "TEA del FPF que iguala a la referencia", "icono": "balance", "color": T.AZUL, "insignia": "hipotetico",
             "valor": f"{C.num(equilibrio, 2)} %" if pd.notna(equilibrio) else "No existe",
             "sub": "con tu comisión, el costo efectivo iguala la TEA observada" if pd.notna(equilibrio)
             else "la comisión sola ya supera el costo de la referencia"},
            {"etiqueta": "Total pagado al final", "valor": _soles(cuota_f * plazo, 0), "icono": "summarize", "color": T.TURQUESA,
             "insignia": "hipotetico", "sub": f"{plazo} cuotas; recibes {_soles(monto * (1 - comision / 100), 0)}"},
        ])

        crono_f, crono_r = D.cronograma(monto, tea_fpf, plazo), D.cronograma(monto, tea_ref, plazo)
        c1, c2 = st.columns(2, gap="medium")
        with c1, st.container(key="tarjeta-sim-saldo"):
            T.seccion("Saldo pendiente", "trending_down", T.AZUL)
            fig = go.Figure()
            fig.add_scatter(x=crono_r.mes, y=crono_r.saldo, name="TEA observada", line=dict(color=T.ESMERALDA, width=2.4),
                            hovertemplate="Mes %{x}: S/ %{y:,.0f}<extra>Observada</extra>")
            fig.add_scatter(x=crono_f.mes, y=crono_f.saldo, name="TEA hipotética del FPF",
                            line=dict(color=T.CORAL, width=2.4, dash="dash"),
                            hovertemplate="Mes %{x}: S/ %{y:,.0f}<extra>Hipotética</extra>")
            fig.update_layout(xaxis_title="Mes", yaxis_title="S/", hovermode="x unified")
            T.figura(fig, "fincrowd_sim_saldo", 300)
        with c2, st.container(key="tarjeta-sim-sens"):
            T.seccion("Costo total según la TEA supuesta", "insights", T.VIOLETA)
            teas = np.linspace(0, max(80.0, tea_fpf, tea_ref) * 1.05, 120)
            costos = [D.cuota_francesa(monto, D.tem_desde_tea(x), plazo) * plazo - monto + monto * comision / 100 for x in teas]
            fig = go.Figure()
            fig.add_scatter(x=teas, y=costos, name="FPF (hipotético)", line=dict(color=T.VIOLETA, width=2.4),
                            hovertemplate="TEA %{x:.1f} %: S/ %{y:,.0f}<extra></extra>")
            fig.add_hline(y=costo_r, line=dict(color=T.ESMERALDA, dash="dot", width=1.6),
                          annotation_text="costo con la TEA observada", annotation_position="top left",
                          annotation_font=dict(color=T.OSCURO[T.ESMERALDA], size=11))
            fig.add_scatter(x=[tea_fpf], y=[costo_f], mode="markers", name="Tu supuesto",
                            marker=dict(size=12, color=T.CORAL, line=dict(color="white", width=2)),
                            hovertemplate="Tu supuesto: S/ %{y:,.0f}<extra></extra>")
            fig.update_layout(xaxis_title="TEA hipotética del FPF (%)", yaxis_title="S/", showlegend=False)
            T.figura(fig, "fincrowd_sim_sensibilidad", 300)

        with st.expander("Cronograma de pagos", icon=":material/table_rows:"):
            tabla = pd.DataFrame({"Mes": crono_f.mes, "Cuota FPF (hipotética)": crono_f.cuota.round(2),
                                  "Interés FPF": crono_f.interes.round(2), "Saldo FPF": crono_f.saldo.round(2),
                                  "Cuota con TEA observada": crono_r.cuota.round(2), "Interés observada": crono_r.interes.round(2),
                                  "Saldo observada": crono_r.saldo.round(2)})
            st.dataframe(tabla, hide_index=True, height=320)
            st.download_button("Descargar cronograma (CSV)", tabla.to_csv(index=False).encode("utf-8-sig"),
                               "fincrowd_cronograma.csv", "text/csv", icon=":material/download:", type="tertiary")
    T.nota("Supuestos del cálculo: cuota constante (sistema francés); TEM = (1 + TEA)^(1/12) − 1; la comisión se descuenta del "
           "desembolso; el costo efectivo anual es la TIR mensual de los flujos llevada a 12 meses. No incluye seguros, "
           "impuestos ni otros cargos. La TEA del BCRP es un promedio del segmento y no incluye comisiones, por lo que el costo "
           "efectivo de un crédito tradicional concreto puede ser mayor. Fuente de la TEA: BCRP (BCRPData).")
