# FinCrowd Perú: dashboard del proyecto (entrega por enlace)

Aplicación de Streamlit que reúne los datos, los resultados y todos los productos del trabajo. Lee solo archivos del repositorio: la base procesada, las salidas de `04_analisis.py` y los PDF de `dashboard/descargas/`. No modifica ningún archivo ni consulta las fuentes en vivo.

## Estructura

| Archivo | Qué hace |
|---|---|
| `app.py` | Configuración, navegación (10 páginas) y filtros globales de la barra lateral |
| `datos.py` | Cálculos sin Streamlit: mismos criterios que `04_analisis.py` (S2, S3) y matemática del simulador |
| `compartido.py` | Carga en caché, estado de los filtros y formatos numéricos del artículo |
| `tema.py` | Identidad visual: paleta, CSS, plantilla de Plotly, tarjetas KPI, insignias e íconos |
| `vistas/*.py` | Una página por archivo: inicio, oferta, plataformas, acceso, crédito, sensibilidad, simulador, datos, productos y reproducibilidad |
| `img/` | Logotipo de FinCrowd Perú (SVG) |

Cada cifra lleva una insignia que indica su naturaleza: **Observado** (BCRP o SMV), **Resultado del artículo** (fijo), **Responde a los filtros**, **Cota inferior** (meses no obtenidos sin imputar), **Referencia** (no es un precio) e **Hipotético** (supuesto del usuario en el simulador).

## Pruebas

`pruebas/test_dashboard.py` comprueba que, sin filtros, los cálculos del dashboard reproducen T2, T4, F1 y F2 y la matemática del simulador. `pruebas/test_dashboard_app.py` renderiza cada página con `streamlit.testing` y simula los filtros. Se ejecutan con el resto: `python -m pytest`.

## Probarlo en tu computadora

Desde la raíz del proyecto, con el entorno activado:

```
pip install -r dashboard/requirements.txt
streamlit run dashboard/app.py
```

Se abre en `http://localhost:8501`.

## Publicarlo en Streamlit Community Cloud (gratis)

1. Verifica que el último commit esté en GitHub (`git push`).
2. Entra a <https://share.streamlit.io> e inicia sesión con tu cuenta de GitHub. La primera vez te pedirá autorizar el acceso a tus repositorios.
3. Pulsa **Create app** y luego **Deploy a public app from GitHub**.
4. Completa:
   - **Repository:** `Diego-Aliaga-Damian/finanzas1-u2-crowdfunding-peru`
   - **Branch:** `main`
   - **Main file path:** `dashboard/app.py`
   - **App URL:** el nombre que prefieras, por ejemplo `fpf-peru-aliaga` (queda `https://fpf-peru-aliaga.streamlit.app`)
5. En **Advanced settings**, elige **Python 3.12** (o 3.13) y guarda.
6. Pulsa **Deploy**. La primera vez tarda unos 2 o 3 minutos.
7. Abre el enlace en una ventana privada para confirmar que se ve sin iniciar sesión. Ese es el enlace que entregas.

## Actualizarlo

Cada vez que hagas `git push`, Streamlit Cloud vuelve a desplegar la aplicación sola. Si cambias el artículo, el Beamer o los pósteres, recompílalos y copia los PDF antes del commit:

```
python herramientas/productos/compilar_productos.py
python herramientas/posteres/generar_posteres.py
python herramientas/productos/preparar_dashboard.py
```

## Si la aplicación «se duerme»

Las aplicaciones gratuitas se suspenden tras varios días sin visitas. Al abrir el enlace aparece un botón para reactivarla, que tarda menos de un minuto. Conviene abrirla el día anterior a la revisión del docente.
