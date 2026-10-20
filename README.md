# Samsung Innovation Campus — Biblioteca de Python

Biblioteca de repaso del Capítulo 2: presentaciones HTML interactivas con Python ejecutable de las Clases 1 y 2, fuentes editables Quarto (`.qmd`) y cuadernos de Google Colab originales.

**Inicio:** abre [index.html](index.html) en un navegador o, una vez activado GitHub Pages, visita la página de este repositorio.

- [Clase 1: Estructuras de datos](clase_1.html)
- [Clase 2: Aplicaciones prácticas](clase_2.html)
- [Guía de uso y edición](LEEME.md)

## Publicar con GitHub Pages

En el repositorio: **Settings → Pages → Build and deployment → Deploy from a branch → main → /(root) → Save**.

Dirección esperada después de la publicación: https://carlos09or.github.io/Samsung-Innovation-Campus/

## Python interactivo en el navegador

- Abre la presentación HTML desde `index.html` y entra en una diapositiva con código.
- Edita la celda y pulsa **▶ Ejecutar** o **Ctrl/Cmd + Enter**. La **SALIDA REAL** aparecerá debajo.
- Puedes comparar con la salida original pulsando **Comparar con la salida esperada**.
- Los cambios se guardan automáticamente en el almacenamiento local **de este navegador**, no en GitHub ni entre dispositivos.
- La primera ejecución **requiere acceso a Internet** para descargar Pyodide (Python basado en WebAssembly). Después, el código se ejecuta en tu navegador, no en un servidor externo.
- El botón **Detener Python** cancela las ejecuciones bloqueadas y reinicia la sesión de Python.
- Algunas librerías externas necesitan configuración adicional. Los ejemplos de este capítulo usan la biblioteca estándar.

## Regenerar presentaciones desde Quarto Live

Los archivos `.qmd` ahora usan el formato `live-revealjs` y bloques `{pyodide}`. Instala [Quarto](https://quarto.org/) y desde esta carpeta ejecuta:

```bash
quarto add r-wasm/quarto-live
quarto render clase_1.qmd
quarto render clase_2.qmd
```

Quarto Live genera su propio estilo RevealJS a partir de los `.qmd`. Los archivos `clase_1.html` y `clase_2.html` incluidos conservan el diseño visual personalizado de las presentaciones anteriores y ejecutan Python mediante `assets/live-python.js`. Para preservar ese diseño personalizado al editar teoría de forma avanzada, es necesario adaptar también el HTML generado o el generador de diseño.


> Repositorio personal de apuntes. Material de refuerzo derivado de los Colab originales, no material oficial de Samsung.
