# Biblioteca de estudio — Python, Samsung Innovation Campus

Dos presentaciones para repasar **las Clases 1 y 2 del Capítulo 2**.

## Comenzar: sin instalar nada

1. Descomprime el archivo ZIP.
2. Abre `index.html` en Chrome, Safari, Edge o Firefox.
3. Elige Clase 1 o Clase 2. Las presentaciones incluidas funcionan sin conexión.
4. Navega con **← / →**, Espacio y los botones. Usa **Índice** para saltar de tema, **F** para pantalla completa, **Copiar código** para llevar un ejemplo a Colab, y **Mostrar solución** en los ejercicios.

## Quarto — fuente editable

Los archivos `clase_1.qmd` y `clase_2.qmd` son fuentes **Quarto** (`revealjs`); están preparados para renderizarse como diapositivas editables desde Markdown. El estilo de ese renderizado está en `assets/quarto.css`.

1. Instala Quarto desde https://quarto.org/docs/get-started/ .
2. Abre una terminal dentro de la carpeta `Python_Samsung_Quarto`.
3. Ejecuta:

```bash
quarto render clase_1.qmd --to revealjs
quarto render clase_2.qmd --to revealjs
```

**Aviso importante:** En este entorno no estaba instalado el ejecutable Quarto. Por ello, además de los `.qmd` listos para renderizar, incluí **versiones HTML independientes** generadas a partir del mismo contenido, que puedes abrir y estudiar ahora. Estas páginas HTML utilizan un visor de diapositivas local; no deben confundirse con una exportación efectuada por la CLI de Quarto.

## Procedencia de los contenidos

- **Clase 1:** `cuadernos_originales/Clase_1_capitulo_2_Python.ipynb` (primeros 106 bloques).
- **Clase 2:** celdas a partir de «Clase 2: Capítulo 2» de `cuadernos_originales/Clase_1_y_2_capitulo_2_Python.ipynb`.
- El segundo cuaderno también incluye el contenido de la Clase 1; se separó para no duplicar diapositivas.
- Se mantuvo el orden de contenidos del curso. Las explicaciones y ejercicios de consolidación se redactaron como refuerzo, y las discrepancias importantes con comentarios originales se señalan como **Aclaración del Colab**.
- **No ejecuta Python dentro del navegador**: los ejemplos son de lectura y copia, y las soluciones de práctica se pueden desplegar. Ejecuta/modifica código en Colab o Jupyter.

## Cómo añadir la clase siguiente

Duplica `clase_2.qmd` con otro nombre, reemplaza los bloques por lo estudiado en clase y ejecuta `quarto render`.

## Inventario

- Clase 1: 50 diapositivas.
- Clase 2: 39 diapositivas.
- Archivos originales: 2 notebooks (`.ipynb`).
- Páginas: `index.html`, `clase_1.html`, `clase_2.html`.
- Edición: `clase_1.qmd`, `clase_2.qmd`, `assets/quarto.css`.

## Publicarlo en GitHub Pages (opcional)

1. Crea un repositorio en GitHub.
2. Sube **el contenido** de esta carpeta (no el ZIP): `index.html`, `clase_1.html`, `clase_2.html`, los `.qmd` y `assets/`.
3. En **Settings → Pages**, publica desde la rama principal y la carpeta raíz (`/root`).
4. GitHub Pages servirá `index.html` como portada y podrás acceder a ambas clases desde tu enlace.

También puedes publicar los HTML sin reconstruirlos con Quarto; están empaquetados sin bibliotecas externas.


## Modo interactivo

Las diapositivas permiten **editar y ejecutar Python directamente**. Cada celda tiene un botón Ejecutar, el resultado real y la salida esperada desplegable. El intérprete Pyodide se descarga de Internet en el primer uso. Los cambios de código se guardan localmente en el navegador. Para generar presentaciones editables desde los archivos `.qmd`, ejecuta `quarto add r-wasm/quarto-live` y después `quarto render clase_1.qmd` o `quarto render clase_2.qmd`.
