# Clase 3 · Funciones — primera parte del Colab del Capítulo 3 (01/09/25 – 04/09/25).
SEMANA = 2
CAPITULO = 3
TITULO = 'Funciones'
TEMA = 'Funciones'


def c(codigo):
    return codigo.strip('\n') + '\n'


DIAPOSITIVAS = [
    {'tipo': 'portada', 'titulo': 'Funciones',
     'sub': 'Capítulo 3 · Definir, llamar y reutilizar código',
     'lista': ['Partes de una función', 'Parámetros y argumentos', 'return, None y closures'],
     'pie': 'Basado en la primera parte del Colab del Capítulo 3 (clases del 01/09/25 al 04/09/25).'},

    {'tipo': 'tema', 'tema': 'Inicio', 'titulo': 'Ruta de la clase',
     'lead': 'Cinco bloques, del concepto básico a las funciones que recuerdan datos.',
     'puntos': ['01 · Anatomía: `def`, nombre, parámetros, cuerpo y `return`.',
                '02 · Tipos de parámetros: obligatorios, por palabra clave y por defecto.',
                '03 · `return` y el valor especial `None`.',
                '04 · Closures: funciones dentro de funciones.',
                '05 · Reto final con todo lo anterior.'],
     'idea': 'Una función es una receta con nombre: la escribes una vez y la usas cuantas veces quieras.'},

    # ---------- 01 · Anatomía
    {'tipo': 'capitulo', 'titulo': '01 / Anatomía de una función', 'texto': 'Definir una vez, usar muchas veces.'},

    {'tipo': 'tema', 'tema': 'Anatomía', 'titulo': 'Las cinco partes de una función',
     'lead': 'Cada función tiene la misma estructura, por pequeña que sea.',
     'puntos': ['`def` anuncia que vas a definir una función.',
                'El **nombre** (`saludar`) es con lo que luego la llamas.',
                'Los **parámetros** van entre paréntesis: `nombre`.',
                'El **cuerpo** va indentado; `return` entrega el resultado.'],
     'codigo': c('''
def saludar(nombre):  # 'nombre' es un parámetro
    """Esta función saluda a la persona con el nombre dado."""
    return f"Hola, {nombre}!"  # valor de retorno

mensaje = saludar("Ana")  # "Ana" es el argumento
print(mensaje)
'''),
     'idea': 'Definir la función no la ejecuta: solo se ejecuta cuando la llamas con `saludar(...)`.'},

    {'tipo': 'tema', 'tema': 'Anatomía', 'titulo': 'Definir no es ejecutar',
     'lead': 'Python lee la definición y la guarda; el cuerpo corre en cada llamada.',
     'puntos': ['Al definir, Python solo recuerda la receta.',
                'Cada llamada `nombre()` vuelve a ejecutar el cuerpo completo.',
                'Por eso puedes llamar la misma función muchas veces.'],
     'codigo': c('''
def anunciar():
    print("¡Llegó el café!")

print("Antes de llamar")
anunciar()
anunciar()
print("Después de llamar")
'''),
     'idea': 'Predice la salida antes de ejecutar: ¿cuántas veces aparece el anuncio?'},

    {'tipo': 'tema', 'tema': 'Anatomía', 'titulo': 'Parámetros frente a argumentos',
     'lead': 'Son dos caras de lo mismo: el hueco y el valor que lo llena.',
     'puntos': ['**Parámetro**: el nombre en la definición (`base`, `altura`).',
                '**Argumento**: el valor real en la llamada (`10`, `5`).',
                'El parámetro solo existe dentro de la función.'],
     'codigo': c('''
# DEFINICIÓN: 'base' y 'altura' son los PARÁMETROS
def calcular_area_triangulo(base, altura):
    area = 0.5 * base * altura
    return area

# LLAMADA: 10 y 5 son los ARGUMENTOS
area_del_triangulo = calcular_area_triangulo(10, 5)
print(area_del_triangulo)
'''),
     'idea': 'Truco para recordarlo: el **p**arámetro está en la **p**lantilla; el **a**rgumento es lo que **a**portas al llamar.'},

    {'tipo': 'tema', 'tema': 'Anatomía', 'titulo': 'Ejemplo · Preparar un café ☕',
     'lead': 'Eres barista: la receta es la función y el pedido del cliente son los argumentos.',
     'puntos': ['Nombre: `preparar_cafe`.',
                'Parámetros: `tipo_cafe` y `cantidad_leche`.',
                'Cuerpo: los pasos; aquí, un `print`.',
                'Retorno: el café listo que entregas.'],
     'codigo': c('''
def preparar_cafe(tipo_cafe, cantidad_leche):
    print(f"Preparando un {tipo_cafe} con {cantidad_leche}.")
    return "¡Aquí está tu café!"

cafe_listo = preparar_cafe("capuchino", "mucha leche")
print(cafe_listo)
'''),
     'nota': 'En el Colab la salida guardada dice «Preparando un espresso…», pero el código llama con `"capuchino"`: esa salida es de una ejecución anterior. La salida real es la de aquí.'},

    {'tipo': 'tema', 'tema': 'Anatomía', 'titulo': 'Ejemplo · Área de un terreno',
     'lead': 'Ahora eres ingeniero: la fórmula es la función y las medidas reales son los argumentos.',
     'puntos': ['Parámetros: `largo` y `ancho`.',
                'Cuerpo: multiplicar `largo * ancho`.',
                'El resultado se guarda en una variable para usarlo después.'],
     'codigo': c('''
def calcular_area_rectangulo(largo, ancho):
    """Calcula el área de un rectángulo."""
    area = largo * ancho
    return area

area_terreno = calcular_area_rectangulo(40, 20)
print(f"El área del terreno es de {area_terreno} metros cuadrados.")
'''),
     'nota': 'El comentario del Colab dice «20 y 15 son los argumentos», pero la llamada usa `40` y `20`; por eso el resultado es 800.'},

    {'tipo': 'tema', 'tema': 'Anatomía', 'titulo': 'Repaso · La máquina de hacer jugo 🍹',
     'lead': 'El mismo esquema en otro contexto: ingredientes, pasos y producto final.',
     'puntos': ['`fruta` y `azucar_cucharadas` son los parámetros.',
                '`"naranja"` y `2` son los argumentos.',
                'El `print` ocurre dentro; el `return` sale de la función.'],
     'codigo': c('''
def hacer_jugo(fruta, azucar_cucharadas):
    print(f"Mezclando {fruta} con {azucar_cucharadas} cucharadas de azúcar.")
    return f"Aquí está tu jugo de {fruta}."

jugo_listo = hacer_jugo("naranja", 2)
print(jugo_listo)
'''),
     'idea': 'Cambia los argumentos (por ejemplo `"mango", 0`) y vuelve a ejecutar.'},

    {'tipo': 'tema', 'tema': 'Anatomía', 'titulo': 'Docstring: documenta tu función',
     'lead': 'El texto entre triples comillas justo debajo de `def` explica qué hace la función.',
     'puntos': ['Se llama **docstring** y es opcional, pero muy recomendable.',
                'Python lo guarda en `función.__doc__`.',
                '`help(función)` lo muestra.'],
     'codigo': c('''
def calcular_area_rectangulo(largo, ancho):
    """Calcula el área de un rectángulo."""
    return largo * ancho

print(calcular_area_rectangulo.__doc__)
'''),
     'idea': 'Una buena docstring responde: ¿qué recibe y qué devuelve?'},

    {'tipo': 'practica', 'tema': 'Anatomía', 'titulo': 'Práctica 01 · Tu primera función',
     'lead': 'Aplica las cinco partes en una función nueva.',
     'reto': 'Escribe `celsius_a_fahrenheit(c)` que devuelva `c * 9 / 5 + 32`. Imprime el resultado para 0 °C y para 37 °C.',
     'solucion': c('''
def celsius_a_fahrenheit(c):
    """Convierte grados Celsius a Fahrenheit."""
    return c * 9 / 5 + 32

print(celsius_a_fahrenheit(0))
print(celsius_a_fahrenheit(37))
'''),
     'idea': 'Usa `return`, no `print`, dentro de la función: así el resultado se puede reutilizar.'},

    # ---------- 02 · Parámetros y argumentos
    {'tipo': 'capitulo', 'titulo': '02 / Parámetros y argumentos', 'texto': 'Cómo llegan los datos a una función.'},

    {'tipo': 'tema', 'tema': 'Parámetros', 'titulo': 'Parámetros posicionales obligatorios',
     'lead': 'Python asigna los argumentos por su posición: el primero al primer parámetro, y así sucesivamente.',
     'puntos': ['El orden importa: `restar(5, 15)` no es `restar(15, 5)`.',
                'Si falta un argumento, Python lanza `TypeError`.'],
     'codigo': c('''
def restar(a, b):
    return a - b

print(restar(5, 15))   # a=5, b=15
try:
    restar(10)         # falta b
except TypeError as error:
    print("Error:", error)
'''),
     'nota': 'En el Colab el comentario dice «a=10, b=6», pero la llamada es `restar(5, 15)`: `a` vale 5, `b` vale 15 y el resultado es -10.'},

    {'tipo': 'tema', 'tema': 'Parámetros', 'titulo': 'Argumentos por palabra clave',
     'lead': 'Escribes el nombre del parámetro al llamar, y el orden deja de importar.',
     'puntos': ['`restar(b=19, a=26)` asigna por nombre, no por posición.',
                'Hace las llamadas más claras cuando hay muchos parámetros.'],
     'codigo': c('''
def restar(a, b):
    return a - b

print(restar(b=19, a=26))
print(restar(a=26, b=19))
'''),
     'idea': 'Las dos llamadas dan lo mismo: lo que manda es el nombre, no el lugar.'},

    {'tipo': 'tema', 'tema': 'Parámetros', 'titulo': 'Parámetros con valor por defecto',
     'lead': 'Si no envías ese argumento, la función usa el valor que trae de fábrica.',
     'puntos': ['`mensaje="Hola"` define el valor por defecto.',
                'Si lo envías, se sobrescribe.',
                'Los parámetros con valor por defecto van al final.'],
     'codigo': c('''
def saludar(nombre, mensaje="Hola"):
    return f"{mensaje}, {nombre}!"

print(saludar("Ana"))
print(saludar("Juan", mensaje="Hola de nuevo"))
print(saludar("Pedro", mensaje="Buenos días"))
'''),
     'nota': 'En el Colab solo se ve `\'Hola de nuevo, Pedro!\'` porque una celda muestra únicamente el valor de su última línea. Para ver todas las llamadas, usa `print`. Además, un comentario dice «Hola de nuevo, Ana!» para la llamada con «Juan».'},

    {'tipo': 'tema', 'tema': 'Parámetros', 'titulo': 'El orden de los nombres manda',
     'lead': 'Lo que cuenta es cómo se llaman los parámetros en la definición, no cómo se llamen tus variables.',
     'puntos': ['Por posición: el primer valor va al primer parámetro.',
                'Por palabra clave: cada valor va al parámetro con ese nombre.',
                'Un nombre engañoso (`restar` que hace `b - a`) confunde: nombra según lo que hace.'],
     'codigo': c('''
def restar(a, b):
    return a - b

print(restar(10, 4))      # a=10, b=4
print(restar(4, 10))      # a=4,  b=10
print(restar(b=4, a=10))  # por nombre
'''),
     'nota': 'El Colab define una versión `restar(b, a)` con el comentario «\'10\' es a, \'5\' es b» (no coincide con el código) y otra `restar(a, b)` que devuelve `b - a`. Aquí se usa una sola versión coherente.'},

    {'tipo': 'tema', 'tema': 'Parámetros', 'titulo': 'Valor por defecto con decisión',
     'lead': 'Un parámetro por defecto puede cambiar el comportamiento de la función.',
     'puntos': ['Sin `idioma`, la función usa `"es"`.',
                'Con `idioma="en"`, responde en inglés.',
                'El `if` dentro del cuerpo decide qué devolver.'],
     'codigo': c('''
def saludar_con_idioma(nombre, idioma="es"):
    if idioma == "es":
        return f"Hola, {nombre}!"
    else:
        return f"Hello, {nombre}!"

print(saludar_con_idioma("María"))
print(saludar_con_idioma("John", idioma="en"))
'''),
     'idea': 'Los valores por defecto hacen que la llamada más común sea también la más corta.'},

    {'tipo': 'tema', 'tema': 'Parámetros', 'titulo': 'Devolver varios valores',
     'lead': 'Una función puede procesar datos y entregar varios resultados a la vez.',
     'puntos': ['El parámetro `calificaciones` espera una lista.',
                '`return promedio, maxima, minima` devuelve una tupla.',
                'Al llamar, la desempaquetas en tres variables.'],
     'codigo': c('''
def analizar_calificaciones(calificaciones):
    """Calcula el promedio, la nota más alta y la más baja."""
    promedio = sum(calificaciones) / len(calificaciones)
    maxima = max(calificaciones)
    minima = min(calificaciones)
    return promedio, maxima, minima

notas_curso = [85, 90, 78, 92, 88]
prom, alta, baja = analizar_calificaciones(notas_curso)
print(f"Promedio: {prom}")
print(f"Nota máxima: {alta}")
print(f"Nota mínima: {baja}")
'''),
     'idea': 'Parámetro: `calificaciones` (lo que espera). Argumento: `notas_curso` (la lista real que entregas).'},

    {'tipo': 'tema', 'tema': 'Parámetros', 'titulo': 'Reglas para no equivocarte',
     'lead': 'Tres reglas que evitan la mayoría de errores al llamar funciones.',
     'puntos': ['Primero van los argumentos posicionales y después los de palabra clave: `saludar("Ana", mensaje="Hola")`.',
                'En la definición, los parámetros con valor por defecto van después de los obligatorios.',
                'No envíes el mismo parámetro dos veces: `restar(5, a=3)` da `TypeError`.',
                'Si una llamada falla, lee el mensaje: Python te dice qué argumento falta o sobra.'],
     'idea': 'Ante la duda, usa palabras clave: la llamada se lee sola.'},

    {'tipo': 'practica', 'tema': 'Parámetros', 'titulo': 'Práctica 02 · Precio con descuento',
     'lead': 'Combina un parámetro obligatorio con uno por defecto.',
     'reto': 'Escribe `precio_final(precio, descuento=0.1)` que devuelva el precio con el descuento aplicado. Imprime `precio_final(100)`, `precio_final(100, 0.25)` y `precio_final(descuento=0.5, precio=80)`.',
     'solucion': c('''
def precio_final(precio, descuento=0.1):
    return precio * (1 - descuento)

print(precio_final(100))
print(precio_final(100, 0.25))
print(precio_final(descuento=0.5, precio=80))
'''),
     'idea': 'La tercera llamada usa palabras clave en otro orden y sigue funcionando.'},

    # ---------- 03 · return y None
    {'tipo': 'capitulo', 'titulo': '03 / return y None', 'texto': 'Lo que la función te entrega al terminar.'},

    {'tipo': 'tema', 'tema': 'return', 'titulo': '`return` termina la función',
     'lead': 'Cuando Python llega a `return`, sale de la función de inmediato.',
     'puntos': ['El valor después de `return` vuelve al lugar de la llamada.',
                'El código escrito después de `return` nunca se ejecuta.'],
     'codigo': c('''
def mi_funcion():
    print("¡Hola!")
    return "Adiós"
    print("Este mensaje no se imprimirá.")  # código inalcanzable

valor = mi_funcion()
print(valor)
'''),
     'idea': 'Piensa en `return` como la puerta de salida: lo que lleves en la mano es lo que entregas.'},

    {'tipo': 'tema', 'tema': 'return', 'titulo': 'Varios valores = una tupla',
     'lead': 'Si devuelves varios valores separados por comas, Python los empaqueta en una tupla.',
     'puntos': ['`datos` recibe la tupla completa.',
                'También puedes desempaquetarla en variables separadas.'],
     'codigo': c('''
def get_datos_personales():
    nombre = "Ana"
    edad = 30
    ciudad = "Madrid"
    return nombre, edad, ciudad

datos = get_datos_personales()
print(datos)
nombre, edad, ciudad = get_datos_personales()
print(nombre, "vive en", ciudad)
'''),
     'idea': 'Es la misma tupla de la Clase 1, solo que creada por una función.'},

    {'tipo': 'tema', 'tema': 'return', 'titulo': 'Sin `return`, la función devuelve `None`',
     'lead': 'Aunque no escribas `return`, Python siempre devuelve algo: el valor especial `None`.',
     'puntos': ['`None` significa «nada» o «ausencia de valor».',
                'Una función que solo imprime hace algo visible, pero no entrega nada.',
                'Guardar su resultado en una variable da `None`.'],
     'codigo': c('''
def mostrar_alerta(mensaje):
    """Muestra un mensaje de advertencia en la pantalla."""
    print(f"[ALERTA]: {mensaje}")

resultado = mostrar_alerta("Batería baja")
print(resultado)
'''),
     'idea': '`return` sin valor también devuelve `None`.'},

    {'tipo': 'tema', 'tema': 'return', 'titulo': '`print` frente a `return`',
     'lead': 'Es la confusión más común: mostrar un valor no es lo mismo que devolverlo.',
     'puntos': ['`print` muestra en pantalla y la función devuelve `None`.',
                '`return` entrega el valor para que lo uses después.',
                'Solo con `return` puedes hacer `doble(5) + 1`.'],
     'codigo': c('''
def doble_con_print(x):
    print(x * 2)

def doble_con_return(x):
    return x * 2

a = doble_con_print(5)
b = doble_con_return(5)
print(a, b)
print(b + 1)
'''),
     'nota': 'En el Colab hay una celda con `return` escrito fuera de una función, junto a la analogía del trabajador. Al ejecutarla, Python da `SyntaxError: \'return\' outside function`: `return` solo puede ir dentro de una función.'},

    {'tipo': 'practica', 'tema': 'return', 'titulo': 'Práctica 03 · ¿Qué imprime?',
     'lead': 'Predice la salida antes de abrir la solución.',
     'reto': 'Dada `def clasificar(x):` con `if x > 0: return "positivo"` y después `print("no positivo")`, ¿qué muestran `print(clasificar(3))` y `print(clasificar(-1))`?',
     'solucion': c('''
def clasificar(x):
    if x > 0:
        return "positivo"
    print("no positivo")

print(clasificar(3))
print(clasificar(-1))
'''),
     'idea': 'Con -1 no se llega al `return`: se imprime el mensaje y la función devuelve `None`.'},

    # ---------- 04 · Closures
    {'tipo': 'capitulo', 'titulo': '04 / Closures', 'texto': 'Funciones que recuerdan de dónde vienen.'},

    {'tipo': 'tema', 'tema': 'Closures', 'titulo': '¿Qué es un closure?',
     'lead': 'Una función anidada que recuerda las variables de la función que la creó, incluso cuando esa función ya terminó.',
     'puntos': ['**Mensajero privado**: la oficina (función exterior) cierra, pero el mensajero (función interior) se lleva el documento que necesita.',
                '**Fotógrafo de bodas**: la dirección de los novios queda apuntada en el cuaderno del asistente aunque la oficina ya no opere.',
                'Ese «paquete de memoria» que viaja con la función interior es el closure.'],
     'idea': 'Tres ingredientes: una función dentro de otra, que usa una variable de afuera y que se devuelve sin ejecutarla.'},

    {'tipo': 'tema', 'tema': 'Closures', 'titulo': 'Una fábrica de multiplicadores',
     'lead': 'La función exterior recibe `a` y devuelve una función que multiplica por ese `a`.',
     'puntos': ['`crear_multiplicador(2)` devuelve una función, no un número.',
                '`doble` recuerda que `a = 2`; `triple` recuerda que `a = 3`.',
                'Se devuelve `mult` sin paréntesis: la función misma, sin ejecutarla.'],
     'codigo': c('''
def crear_multiplicador(a):
    def mult(x):
        return a * x
    return mult

doble = crear_multiplicador(2)
triple = crear_multiplicador(3)
print(doble(10), doble(5), doble(3))
print(triple(10))
'''),
     'nota': 'En el Colab la función se define como `cierre_calculo`, pero se llama `cierre_calc()`: ejecutada tal cual, la celda da `NameError`. La salida «20 10 6» que se ve guardada viene de una ejecución anterior. Además, la línea `a = 2` dentro de la función anulaba el parámetro. Aquí se corrigen ambos detalles.'},

    {'tipo': 'tema', 'tema': 'Closures', 'titulo': 'El fotógrafo que recuerda tu nombre 📸',
     'lead': 'Cada closure guarda su propio dato: un fotógrafo para Laura y otro para Luis.',
     'puntos': ['`contratar_fotografo` es la función exterior.',
                '`tomar_foto` es el closure: usa `nombre_cliente`.',
                'Cada llamada a la fábrica crea un closure con su propia memoria.'],
     'codigo': c('''
def contratar_fotografo(nombre_cliente):
    def tomar_foto(evento):
        return f"Foto de {evento} tomada para {nombre_cliente}."
    return tomar_foto

fotografo_para_laura = contratar_fotografo("Laura")
fotografo_para_luis = contratar_fotografo("Luis")
print(fotografo_para_laura("la boda"))
print(fotografo_para_luis("la graduación"))
'''),
     'idea': '`contratar_fotografo` ya terminó, pero cada fotógrafo sigue sabiendo para quién trabaja.'},

    {'tipo': 'tema', 'tema': 'Closures', 'titulo': '¿Para qué sirven los closures?',
     'lead': 'Son la base de herramientas más avanzadas de Python.',
     'puntos': ['**Encapsular datos**: el dato queda guardado dentro de la función, sin variables globales.',
                '**Funciones a medida**: creas versiones especializadas (un fotógrafo por cliente).',
                '**Decoradores**: modifican otras funciones y se construyen con closures.'],
     'idea': 'Si necesitas muchas funciones casi iguales, piensa en una fábrica con closures.'},

    {'tipo': 'practica', 'tema': 'Closures', 'titulo': 'Práctica 04 · Calculadora de impuestos',
     'lead': 'Construye tu propia fábrica de funciones.',
     'reto': 'Escribe `crear_impuesto(tasa)` que devuelva una función que reciba un precio y le sume el impuesto. Crea `iva = crear_impuesto(0.19)` y `reducido = crear_impuesto(0.05)` e imprime ambos para un precio de 100.',
     'solucion': c('''
def crear_impuesto(tasa):
    def aplicar(precio):
        return round(precio * (1 + tasa), 2)
    return aplicar

iva = crear_impuesto(0.19)
reducido = crear_impuesto(0.05)
print(iva(100))
print(reducido(100))
'''),
     'idea': 'La función interior usa `tasa`, que pertenece a la función exterior: eso es el closure.'},

    # ---------- 05 · Reto
    {'tipo': 'capitulo', 'titulo': '05 / Reto final', 'texto': 'Todo junto en un solo programa.'},

    {'tipo': 'practica', 'tema': 'Reto final', 'titulo': 'Reto · Boletín de notas',
     'lead': 'Usa parámetros por defecto, varios valores de retorno y una función auxiliar.',
     'reto': 'Escribe `boletin(nombre, notas, minimo=60)` que devuelva el promedio y el estado (`"Aprobado"` o `"Reprobado"`). Imprime el boletín de Ana `[85, 90, 78]` y de Luis `[50, 62, 58]` con el formato `Ana: 84.3 → Aprobado`.',
     'solucion': c('''
def promedio(valores):
    return sum(valores) / len(valores)

def boletin(nombre, notas, minimo=60):
    prom = promedio(notas)
    estado = "Aprobado" if prom >= minimo else "Reprobado"
    return prom, estado

for nombre, notas in [("Ana", [85, 90, 78]), ("Luis", [50, 62, 58])]:
    prom, estado = boletin(nombre, notas)
    print(f"{nombre}: {prom:.1f} → {estado}")
'''),
     'idea': 'Divide el problema: una función calcula el promedio y otra decide el estado.'},

    # ---------- Cierre
    {'tipo': 'tema', 'tema': 'Cierre', 'titulo': 'Errores y detalles detectados en el Colab',
     'lead': 'Revisar el código con salidas reales evita aprender algo equivocado.',
     'puntos': ['La salida guardada del café dice «espresso», pero el código pide un capuchino: es de una ejecución anterior.',
                'Comentarios que no coinciden con el código: «20 y 15» (son 40 y 20) y «a=10, b=6» (son 5 y 15).',
                '`return` fuera de una función da `SyntaxError`.',
                '`cierre_calc()` no existe (la función es `cierre_calculo`): la celda da `NameError`, y `a = 2` anulaba el parámetro.',
                'Una celda solo muestra su última línea: usa `print` para ver todo.'],
     'idea': 'La fuente de verdad es lo que el programa hace al ejecutarlo, no el comentario.'},

    {'tipo': 'tema', 'tema': 'Cierre', 'titulo': 'Ficha de repaso · Clase 3',
     'lead': 'Intenta responder sin mirar las diapositivas.',
     'puntos': ['¿Cuál es la diferencia entre un parámetro y un argumento?',
                '¿Qué pasa si llamas a una función con un argumento de menos?',
                '¿Qué devuelve una función que no tiene `return`?',
                '¿Por qué `doble_con_print(5) + 1` da error y `doble_con_return(5) + 1` no?',
                '¿Qué recuerda un closure y cuándo lo usarías?'],
     'idea': 'Próximo paso: Clase 4, donde las funciones viven dentro de las clases como métodos.'},
]
