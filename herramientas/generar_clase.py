#!/usr/bin/env python3
"""Genera clase_N.html y clase_N.qmd a partir de herramientas/clases/clase_N.py.

Usa clase_2.html como plantilla (estilos, navegación e índice) y obtiene cada
«Salida esperada» ejecutando el código con Python, así nunca queda desfasada.

Uso:  python3 herramientas/generar_clase.py 3 4
Requiere: pygments (pip install pygments)
"""
import html
import importlib.util
import pathlib
import re
import subprocess
import sys
import tempfile

from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import PythonLexer

RAIZ = pathlib.Path(__file__).resolve().parent.parent
PLANTILLA_HTML = RAIZ / 'clase_2.html'
PLANTILLA_QMD = RAIZ / 'clase_2.qmd'
INICIO_DECK = '<main class="deck-wrap"><div class="deck">'
FIN_DECK = '</div></main>'


def inline(texto):
    """Escapa HTML y convierte `código` y **negrita**."""
    t = html.escape(texto, quote=True)
    t = re.sub(r'`([^`]+)`', r'<code class="inline">\1</code>', t)
    return re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', t)


def plano(texto):
    return texto.replace('`', '').replace('**', '')


def ejecutar(codigo):
    with tempfile.TemporaryDirectory() as carpeta:
        archivo = pathlib.Path(carpeta) / 'celda.py'
        archivo.write_text(codigo, encoding='utf-8')
        r = subprocess.run([sys.executable, '-I', str(archivo)], capture_output=True,
                           text=True, cwd=carpeta, timeout=30)
    if r.returncode != 0 or r.stderr:
        raise SystemExit(f'Falló una celda:\n{codigo}\n---\n{r.stderr}')
    return r.stdout.rstrip('\n')


def caja_codigo(codigo):
    resaltado = highlight(codigo, PythonLexer(), HtmlFormatter()).rstrip('\n')
    return ('<div class="code-box"><div class="code-bar"><span class="lang-dot"></span><span>PYTHON</span>'
            '<button class="copy-btn" aria-label="Copiar código">Copiar código</button></div>'
            + resaltado + '</div>')


def caja_salida(salida):
    return ('<div class="output-box"><div class="output-label"><span class="output-mark">↳</span> '
            'SALIDA ESPERADA</div><pre>' + html.escape(salida) + '</pre></div>')


def salida_de(d):
    real = ejecutar(d['codigo'])
    return d.get('salida', real)


def encabezado(d):
    partes = [f'<div class="overline">{html.escape(d["tema"].upper())} <span class="overline-dot">●</span> GUÍA DE REPASO</div>',
              f'<h2>{inline(d["titulo"])}</h2>']
    if d.get('lead'):
        partes.append(f'<p class="lead">{inline(d["lead"])}</p>')
    return ''.join(partes)


def pie(d, etiqueta='◆ IDEA CLAVE'):
    partes = []
    if d.get('idea'):
        partes.append(f'<div class="takeaway"><span>{etiqueta}</span><p>{inline(d["idea"])}</p></div>')
    if d.get('nota'):
        partes.append(f'<div class="source-note"><span>↪ ACLARACIÓN DEL COLAB</span> {inline(d["nota"])}</div>')
    return ''.join(partes)


def bloque_qmd(codigo, salida):
    texto = f'```{{pyodide}}\n{codigo.rstrip()}\n```\n\n'
    if salida is not None:
        texto += f'**Salida esperada**\n\n```text\n{salida}\n```\n\n'
    return texto


def pie_qmd(d, titulo='Idea clave'):
    texto = ''
    if d.get('idea'):
        texto += f'::: {{.callout-tip title="{titulo}"}}\n{d["idea"]}\n:::\n\n'
    if d.get('nota'):
        texto += f'::: {{.callout-note title="Aclaración del Colab"}}\n{d["nota"]}\n:::\n\n'
    return texto


def render(d, semana, numero):
    """Devuelve (clase CSS extra, html interno, texto qmd) de una diapositiva."""
    tipo = d['tipo']
    if tipo == 'portada':
        lista = ''.join(f'<span>{inline(x)}</span>' for x in d['lista'])
        cuerpo = (f'<div class="hero-radial"></div><div class="overline">SAMSUNG INNOVATION CAMPUS · PYTHON</div>'
                  f'<div class="hero-count">SEMANA {semana} · CLASE {numero}</div><h1>{inline(d["titulo"])}</h1>'
                  f'<p class="hero-sub">{inline(d["sub"])}</p><div class="hero-list">{lista}</div>'
                  f'<p class="hero-foot">{inline(d["pie"])}</p>')
        return ' cover', cuerpo, ''
    if tipo == 'capitulo':
        cuerpo = ('<div class="chapter-art"><span class="arc arc-1"></span><span class="arc arc-2"></span></div>'
                  f'<div class="chapter-content"><div class="overline">SIGUIENTE BLOQUE</div><h1>{inline(d["titulo"])}</h1>'
                  f'<p>{inline(d["texto"])}</p></div>')
        return ' chapter', cuerpo, f'# {d["titulo"]}\n\n{d["texto"]}\n\n'
    qmd = f'## {d["titulo"]} {{.scrollable}}\n\n<span class="study-topic">{d["tema"]}</span>\n\n'
    if d.get('lead'):
        qmd += d['lead'] + '\n\n'
    if tipo == 'tema':
        puntos = ''.join(f'<li>{inline(p)}</li>' for p in d['puntos'])
        teoria = f'<div class="theory-panel"><div class="panel-kicker">EN POCAS PALABRAS</div><ul>{puntos}</ul></div>'
        qmd += ''.join(f'- {p}\n' for p in d['puntos']) + '\n'
        if d.get('codigo'):
            salida = salida_de(d)
            ejemplo = f'<div class="example-panel">{caja_codigo(d["codigo"])}{caja_salida(salida)}</div>'
            grid = f'<div class="slide-grid ">{teoria}{ejemplo}</div>'
            qmd += bloque_qmd(d['codigo'], salida)
        else:
            grid = f'<div class="slide-grid no-code">{teoria}</div>'
        return '', encabezado(d) + grid + pie(d), qmd + pie_qmd(d)
    if tipo == 'practica':
        salida = salida_de({'codigo': d['solucion'], **({'salida': d['salida']} if 'salida' in d else {})})
        cuerpo = (encabezado(d) +
                  f'<div class="exercise-box"><div class="exercise-tag">✦ DESAFÍO · INTÉNTALO SIN MIRAR</div><p>{inline(d["reto"])}</p></div>'
                  '<button class="solution-toggle" aria-expanded="false">Mostrar solución <span>⌄</span></button>'
                  f'<div class="solution-content" hidden>{caja_codigo(d["solucion"])}{caja_salida(salida)}</div>'
                  + pie(d, 'PISTA / IDEA CLAVE'))
        qmd += (f'**Ponte a prueba**\n\n{d["reto"]}\n\n**Solución (ábrela cuando hayas intentado resolverlo):**\n\n'
                f'<details>\n<summary>Mostrar solución</summary>\n\n{bloque_qmd(d["solucion"], salida)}</details>\n\n')
        return '', cuerpo, qmd + pie_qmd(d)
    raise SystemExit(f'Tipo de diapositiva desconocido: {tipo}')


def cargar_spec(numero):
    ruta = RAIZ / 'herramientas' / 'clases' / f'clase_{numero}.py'
    spec = importlib.util.spec_from_file_location(f'clase_{numero}', ruta)
    modulo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modulo)
    return modulo


def generar(numero):
    m = cargar_spec(numero)
    plantilla = PLANTILLA_HTML.read_text(encoding='utf-8')
    cabeza = plantilla[:plantilla.index(INICIO_DECK) + len(INICIO_DECK)]
    cola = plantilla[plantilla.index(FIN_DECK):]

    cabeza = re.sub(r'<title>[^<]*</title>', f'<title>Clase {numero} | Python · Samsung Innovation Campus</title>', cabeza, count=1)
    cabeza = re.sub(r'<span class="nav-pill">[^<]*</span>', f'<span class="nav-pill">SEMANA {m.SEMANA} · CLASE {numero:02d}</span>', cabeza, count=1)
    cabeza = cabeza.replace('href="index.html#semana-1"', f'href="index.html#semana-{m.SEMANA}"', 1)

    secciones, items, qmd = [], [], []
    for i, d in enumerate(m.DIAPOSITIVAS):
        extra, cuerpo, texto = render(d, m.SEMANA, numero)
        etiqueta = html.escape(plano(d['titulo']), quote=True)
        secciones.append(f'<section class="slide{extra}" data-index="{i}" aria-label="Diapositiva {i + 1}: {etiqueta}">{cuerpo}</section>')
        items.append(f'<button class="item" data-slide="{i}"><span class="num">{i + 1:02d}</span>{html.escape(plano(d["titulo"]))}</button>')
        qmd.append(texto)
    total = len(secciones)

    cola = re.sub(r'<span id="counter" class="slide-counter">[^<]*</span>', f'<span id="counter" class="slide-counter">01 / {total:02d}</span>', cola, count=1)
    cola = re.sub(r'<h3>Contenido de Clase \d+</h3>.*?</aside>',
                  lambda _: f'<h3>Contenido de Clase {numero}</h3>' + ''.join(items) + '</aside>', cola, count=1, flags=re.S)
    (RAIZ / f'clase_{numero}.html').write_text(cabeza + ''.join(secciones) + cola, encoding='utf-8')

    frente = PLANTILLA_QMD.read_text(encoding='utf-8').split('---', 2)[1]
    frente = re.sub(r'title: ".*"', f'title: "Clase {numero} — {m.TITULO}"', frente, count=1)
    frente = re.sub(r'subtitle: ".*"', f'subtitle: "Samsung Innovation Campus · Capítulo {m.CAPITULO}"', frente, count=1)
    (RAIZ / f'clase_{numero}.qmd').write_text('---' + frente + '---\n\n' + ''.join(qmd).rstrip() + '\n', encoding='utf-8')
    print(f'clase_{numero}: {total} diapositivas')
    return total


if __name__ == '__main__':
    for n in sys.argv[1:] or ['3', '4']:
        generar(int(n))
