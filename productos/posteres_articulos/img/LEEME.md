# Imágenes institucionales de los pósteres

Coloca aquí estos archivos con **exactamente** estos nombres. La plantilla (`../plantilla_poster.tex`) los detecta sola al compilar:

| Archivo | Qué es | Si falta |
|---|---|---|
| `logo_uncp.png` | Logo de la Universidad Nacional del Centro del Perú (PNG, fondo transparente, 600 px de ancho o más) | Aparece un recuadro gris «LOGO UNCP» |
| `logo_facultad.png` | Logo de la Facultad de Economía (opcional) | No se muestra |
| `foto_autor.jpg` | Tu foto, vertical, tipo carné (opcional) | No se muestra |

Después de copiarlos, vuelve a compilar desde la raíz del proyecto:

```
python herramientas/posteres/generar_posteres.py
```

Usa los logos oficiales que publica la universidad (por ejemplo, los del ADESA o del portal institucional) y no los modifiques.
