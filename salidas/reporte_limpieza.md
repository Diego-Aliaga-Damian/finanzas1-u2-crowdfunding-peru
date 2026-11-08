# Reporte de limpieza e integración (03_limpieza_datos.py)

Archivo generado: `datos_procesados/datos_procesados_2024200481M.csv` · filas: 414 · columnas: 35

## Controles

- ✅ EEFF: identidad activo = pasivo + patrimonio se cumple (±1 mil S/) en 52/52 trimestres
- ✅ EEFF: 52 trimestres de 6 sociedades administradoras (2022-T2 a 2026-T3)
- ✅ Catálogo del SIMV: 6 plataformas (3 vigentes, 3 retiradas)
- ✅ Llave RUC: 6/6 plataformas del SIMV cruzadas uno a uno con la API OData por razón social idéntica
- ✅ SIMV: TOTAL = suma de tipos de receptor en 107/107 consultas con registros
- ✅ SIMV: modalidad VALORES en 10 consultas; monto financiado total = S/ 0
- ✅ BCRP: 10 series × 69 meses (2021-01 a 2026-09); valores faltantes = 0
- ✅ Panel: 414 filas = 6 plataformas × 69 meses; llave ruc + periodo única
- ✅ estado_simv: sin_registros=267, con_registros=107, no_obtenido=40
- ✅ EEFF integrados: 52/52 trimestres
- ✅ Atípicos (Tukey, 3·RIC): 27 identificados; se conservan (datos oficiales)

## Transformaciones aplicadas

1. EEFF (SMV OData): solo sociedades administradoras de plataformas de FPF; moneda única (soles); montos en miles de S/; cada trimestre se asigna a su mes de cierre (mar, jun, sep, dic); los demás meses quedan vacíos (no se interpola).
2. SIMV: conteos y montos convertidos de texto a entero; el monto está en soles corrientes (S/).
3. SIMV: préstamos en columnas por tipo de receptor (_emp, _per); valores en columnas _valores (suma de tipos); la fila TOTAL se usa solo como control.
4. BCRP: periodo 'Ene.2021' -> '2021-01'; 'n.d.' -> vacío; tasas en % (TEA) e IPC (dic. 2021 = 100) como decimales; el valor de cada mes se repite para todas las plataformas.
5. Integración: panel balanceado plataforma × mes (llave ruc + periodo). SIMV por empresa_id_simv y periodo; EEFF por ruc y periodo; BCRP por periodo. estado_simv = con_registros | sin_registros | no_obtenido.

## Valores faltantes por variable

| Variable | Faltantes | % |
|---|---|---|
| `proy_publicados_emp` | 346 | 83.6 |
| `proy_financiados_emp` | 346 | 83.6 |
| `monto_financiado_emp` | 346 | 83.6 |
| `proy_publicados_per` | 330 | 79.7 |
| `proy_financiados_per` | 330 | 79.7 |
| `monto_financiado_per` | 330 | 79.7 |
| `proy_publicados_valores` | 404 | 97.6 |
| `proy_financiados_valores` | 404 | 97.6 |
| `monto_financiado_valores` | 404 | 97.6 |
| `trimestre_eeff` | 362 | 87.4 |
| `activo_total_miles` | 362 | 87.4 |
| `pasivo_total_miles` | 362 | 87.4 |
| `patrimonio_total_miles` | 362 | 87.4 |
| `ingresos_totales_miles` | 362 | 87.4 |
| `utilidad_neta_miles` | 362 | 87.4 |
| `fecha_registro_eeff` | 362 | 87.4 |

Los faltantes de SIMV corresponden a meses sin registros o no obtenidos (`estado_simv`); los de EEFF, a meses que no son de cierre de trimestre o a trimestres en que la empresa no presentó información.

## Atípicos identificados (regla de Tukey, 3·RIC; se conservan)

- Prestopolis 2026-04: monto por proyecto empresarial = S/ 750,000
- Prestopolis 2026-07: monto por proyecto empresarial = S/ 1,190,350
- tamn 2021-03: cambio mensual de -0.75 puntos porcentuales
- tea_bcos_pyme_360 2024-10: cambio mensual de -3.51 puntos porcentuales
- tea_bcos_pyme_360 2024-11: cambio mensual de -7.92 puntos porcentuales
- tea_bcos_pyme_360 2025-01: cambio mensual de +3.93 puntos porcentuales
- tea_bcos_pyme_360 2025-03: cambio mensual de +19.25 puntos porcentuales
- tea_bcos_pyme_mas360 2024-10: cambio mensual de -0.85 puntos porcentuales
- tea_bcos_pyme_mas360 2024-11: cambio mensual de -3.23 puntos porcentuales
- tea_bcos_consumo_360 2021-10: cambio mensual de -4.05 puntos porcentuales
- tea_bcos_consumo_mas360 2025-07: cambio mensual de +0.71 puntos porcentuales
- tea_bcos_consumo_mas360 2026-08: cambio mensual de +0.70 puntos porcentuales
- tea_cmac_pyme_360 2021-11: cambio mensual de -1.22 puntos porcentuales
- tea_cmac_pyme_360 2022-07: cambio mensual de -1.60 puntos porcentuales
- tea_cmac_pyme_360 2022-08: cambio mensual de +1.84 puntos porcentuales
- tea_cmac_pyme_360 2024-01: cambio mensual de +8.99 puntos porcentuales
- tea_cmac_pyme_360 2024-02: cambio mensual de -8.60 puntos porcentuales
- tea_cmac_pyme_360 2024-04: cambio mensual de +1.24 puntos porcentuales
- tea_cmac_pyme_mas360 2022-07: cambio mensual de -0.94 puntos porcentuales
- tea_cmac_pyme_mas360 2022-08: cambio mensual de +1.25 puntos porcentuales
- tea_cmac_pyme_mas360 2024-08: cambio mensual de +0.83 puntos porcentuales
- tea_cmac_pyme_mas360 2024-09: cambio mensual de -0.77 puntos porcentuales
- tea_crac_pyme_360 2023-08: cambio mensual de +4.35 puntos porcentuales
- tea_crac_pyme_mas360 2023-08: cambio mensual de +6.05 puntos porcentuales
- tea_crac_pyme_mas360 2023-09: cambio mensual de +2.39 puntos porcentuales
- tea_crac_pyme_mas360 2023-10: cambio mensual de +3.51 puntos porcentuales
- tea_crac_pyme_mas360 2024-02: cambio mensual de -1.25 puntos porcentuales
