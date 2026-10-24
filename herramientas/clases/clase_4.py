# Clase 4 · Programación orientada a objetos — segunda parte del Colab del Capítulo 3 (01/09/25 – 04/09/25).
SEMANA = 2
CAPITULO = 3
TITULO = 'Programación orientada a objetos'


def c(codigo):
    return codigo.strip('\n') + '\n'


DIAPOSITIVAS = [
    {'tipo': 'portada', 'titulo': 'Programación orientada a objetos',
     'sub': 'Capítulo 3 · Clases, objetos, herencia y métodos dunder',
     'lista': ['Clases y objetos', 'Encapsulamiento y herencia', 'Métodos dunder'],
     'pie': 'Basado en la segunda parte del Colab del Capítulo 3 (clases del 01/09/25 al 04/09/25).'},

    {'tipo': 'tema', 'tema': 'Inicio', 'titulo': 'Ruta de la clase',
     'lead': 'De la plantilla al objeto, y del objeto a uno que se comporta como un tipo de Python.',
     'puntos': ['01 · Clases y objetos: `class`, `__init__`, `self` y métodos.',
                '02 · Encapsulamiento y herencia.',
                '03 · Métodos dunder: `__str__`, `__repr__`, `__len__`, `__eq__` y `__add__`.',
                '04 · Reto final: una playlist.'],
     'idea': 'Un método es una función que vive dentro de una clase: todo lo de la Clase 3 sigue valiendo.'},

    # ---------- 01 · Clases y objetos
    {'tipo': 'capitulo', 'titulo': '01 / Clases y objetos', 'texto': 'El plano y lo que construyes con él.'},

    {'tipo': 'tema', 'tema': 'Clases y objetos', 'titulo': 'Clase = plano, objeto = instancia',
     'lead': 'La POO se basa en dos ideas: la plantilla y las cosas concretas creadas con ella.',
     'puntos': ['**Clase**: el plano. Define atributos (datos) y métodos (acciones).',
                '**Objeto**: una instancia concreta del plano, con sus propios datos.',
                'Analogía: la receta de galletas es la clase; cada galleta horneada es un objeto.',
                'Plano de un coche: tiene marca y modelo y puede conducir. Tu Tesla rojo es un objeto.'],
     'idea': 'Una clase, muchos objetos: todos comparten la estructura, pero cada uno guarda sus valores.'},

    {'tipo': 'tema', 'tema': 'Clases y objetos', 'titulo': 'Tu primera clase: `Coche`',
     'lead': 'Defines la clase una vez y creas objetos llamándola como si fuera una función.',
     'puntos': ['`class Coche:` define la plantilla.',
                '`__init__` guarda `marca` y `modelo` en el objeto.',
                '`conducir` es un método: una función de la clase.',
                '`mi_coche = Coche("Tesla", "Model 3")` crea el objeto.'],
     'codigo': c('''
class Coche:
    def __init__(self, marca, modelo):
        self.marca = marca
        self.modelo = modelo

    def conducir(self, distancia):
        print(f"El {self.marca} {self.modelo} ha recorrido {distancia} km.")

mi_coche = Coche("Tesla", "Model 3")
mi_coche.conducir(100)
'''),
     'idea': 'Los métodos se llaman con punto: `objeto.metodo(argumentos)`.'},

    {'tipo': 'tema', 'tema': 'Clases y objetos', 'titulo': '`__init__`: el constructor',
     'lead': 'Se ejecuta solo, cada vez que creas un objeto, para darle sus valores iniciales.',
     'puntos': ['No lo llamas directamente: `Coche(...)` lo invoca por ti.',
                '`self.marca = marca` guarda el argumento como atributo del objeto.',
                'Luego lees los atributos con `objeto.atributo`.'],
     'codigo': c('''
class Coche:
    def __init__(self, marca, modelo):
        self.marca = marca
        self.modelo = modelo

mi_coche = Coche("Tesla", "Model 3")
print(mi_coche.marca)
print(mi_coche.modelo)
'''),
     'idea': 'Los parámetros de `__init__` (sin contar `self`) son los argumentos que pasas al crear el objeto.'},

    {'tipo': 'tema', 'tema': 'Clases y objetos', 'titulo': '`self`: el objeto que está trabajando',
     'lead': 'Dentro de un método, `self` es el objeto concreto que recibió la llamada.',
     'puntos': ['`mi_coche.conducir(50)` equivale a `Coche.conducir(mi_coche, 50)`.',
                'Con `self.km` cada coche lleva su propio kilometraje.',
                'Un método puede leer y modificar los atributos de su objeto.'],
     'codigo': c('''
class Coche:
    def __init__(self, marca):
        self.marca = marca
        self.km = 0

    def conducir(self, distancia):
        self.km += distancia

tesla = Coche("Tesla")
ford = Coche("Ford")
tesla.conducir(100)
tesla.conducir(50)
ford.conducir(20)
print(tesla.marca, tesla.km)
print(ford.marca, ford.km)
'''),
     'idea': 'Dos objetos de la misma clase no comparten sus atributos: cada uno tiene los suyos.'},

    {'tipo': 'practica', 'tema': 'Clases y objetos', 'titulo': 'Práctica 01 · Clase `Mascota`',
     'lead': 'Crea una clase con constructor y un método.',
     'reto': 'Define `Mascota` con los atributos `nombre` y `especie`, y un método `presentarse()` que devuelva `"Soy Luna, un gato"`. Crea dos mascotas e imprime su presentación.',
     'solucion': c('''
class Mascota:
    def __init__(self, nombre, especie):
        self.nombre = nombre
        self.especie = especie

    def presentarse(self):
        return f"Soy {self.nombre}, un {self.especie}"

luna = Mascota("Luna", "gato")
rocky = Mascota("Rocky", "perro")
print(luna.presentarse())
print(rocky.presentarse())
'''),
     'idea': 'No olvides `self` como primer parámetro de cada método.'},

    # ---------- 02 · Encapsulamiento y herencia
    {'tipo': 'capitulo', 'titulo': '02 / Encapsulamiento y herencia', 'texto': 'Proteger los datos y reutilizar código.'},

    {'tipo': 'tema', 'tema': 'Encapsulamiento', 'titulo': 'Encapsulamiento',
     'lead': 'Agrupar datos y métodos en una clase, y que el resto del programa use los métodos en lugar de tocar los datos.',
     'puntos': ['Analogía: un control remoto. Usas los botones (métodos) sin tocar los circuitos (datos).',
                'En Python, un guion bajo (`_saldo`) indica «uso interno, no lo toques desde afuera».',
                'Los métodos pueden validar: aquí no se permite retirar más de lo que hay.'],
     'codigo': c('''
class CuentaBancaria:
    def __init__(self, titular, saldo=0):
        self.titular = titular
        self._saldo = saldo

    def depositar(self, monto):
        self._saldo += monto

    def retirar(self, monto):
        if monto > self._saldo:
            return "Fondos insuficientes"
        self._saldo -= monto
        return "Retiro exitoso"

    def ver_saldo(self):
        return self._saldo

cuenta = CuentaBancaria("Ana", 100)
cuenta.depositar(50)
print(cuenta.retirar(500))
print(cuenta.retirar(30))
print(cuenta.ver_saldo())
'''),
     'idea': 'El Colab explica el encapsulamiento solo con teoría; este ejemplo es un refuerzo para verlo en código.'},

    {'tipo': 'tema', 'tema': 'Herencia', 'titulo': 'Herencia: `Perro` hereda de `Animal`',
     'lead': 'Una clase hija recibe los atributos y métodos de la clase padre y puede añadir los suyos.',
     'puntos': ['`class Perro(Animal):` indica que `Perro` hereda de `Animal`.',
                '`respirar` viene heredado; `ladrar` es propio de `Perro`.',
                'Analogía: un perro respira como todo animal, pero además ladra.'],
     'codigo': c('''
class Animal:
    def respirar(self):
        print("Estoy respirando.")

class Perro(Animal):  # Perro hereda de Animal
    def ladrar(self):
        print("¡Guau!")

mi_perro = Perro()
mi_perro.respirar()  # método heredado
mi_perro.ladrar()    # método propio
'''),
     'idea': 'La herencia evita repetir código: lo común va en la clase padre.'},

    {'tipo': 'tema', 'tema': 'Herencia', 'titulo': 'Sobrescribir métodos y `super()`',
     'lead': 'La clase hija puede reemplazar un método del padre y reutilizar su constructor con `super()`.',
     'puntos': ['`super().__init__(nombre)` ejecuta el constructor de `Animal`.',
                '`Perro` y `Gato` redefinen `hablar` a su manera.',
                'El mismo llamado `animal.hablar()` responde distinto según el objeto.',
                '`isinstance(luna, Animal)` es `True`: un gato también es un animal.'],
     'codigo': c('''
class Animal:
    def __init__(self, nombre):
        self.nombre = nombre

    def hablar(self):
        return "..."

class Perro(Animal):
    def __init__(self, nombre, raza):
        super().__init__(nombre)
        self.raza = raza

    def hablar(self):
        return "¡Guau!"

class Gato(Animal):
    def hablar(self):
        return "¡Miau!"

rocky = Perro("Rocky", "labrador")
luna = Gato("Luna")
for animal in [rocky, luna, Animal("Genérico")]:
    print(animal.nombre, "dice", animal.hablar())
print(rocky.raza, isinstance(luna, Animal))
'''),
     'idea': 'Refuerzo: el Colab presenta la herencia básica; `super()` y la sobrescritura son el paso siguiente.'},

    {'tipo': 'practica', 'tema': 'Herencia', 'titulo': 'Práctica 02 · Vehículos',
     'lead': 'Crea una clase padre y una hija que reutilice su constructor.',
     'reto': 'Define `Vehiculo(marca, ruedas)` con un método `describir()` que devuelva `"Yamaha con 2 ruedas"`. Crea `Moto(Vehiculo)` cuyo constructor reciba solo `marca` y llame a `super().__init__(marca, 2)`.',
     'solucion': c('''
class Vehiculo:
    def __init__(self, marca, ruedas):
        self.marca = marca
        self.ruedas = ruedas

    def describir(self):
        return f"{self.marca} con {self.ruedas} ruedas"

class Moto(Vehiculo):
    def __init__(self, marca):
        super().__init__(marca, 2)

print(Vehiculo("Toyota", 4).describir())
print(Moto("Yamaha").describir())
'''),
     'idea': '`Moto` no define `describir`: lo hereda tal cual de `Vehiculo`.'},

    # ---------- 03 · Métodos dunder
    {'tipo': 'capitulo', 'titulo': '03 / Métodos dunder', 'texto': 'Superpoderes para tus objetos.'},

    {'tipo': 'tema', 'tema': 'Métodos dunder', 'titulo': 'POO y métodos dunder',
     'lead': '«Dunder» viene de *double underscore*: métodos con doble guion bajo a cada lado.',
     'puntos': ['La POO es el plano general: atributos y métodos.',
                'Los dunder definen cómo reacciona tu objeto ante Python: `print()`, `len()`, `==`, `+`.',
                'Nunca los llamas directamente: Python los invoca por ti.',
                '`__init__` ya es un dunder: lo dispara `Clase(...)`.'],
     'idea': 'Si quieres que tu objeto se imprima bonito, se compare o se sume, hay un dunder para eso.'},

    {'tipo': 'tema', 'tema': 'Métodos dunder', 'titulo': '`__str__`: cómo se imprime tu objeto',
     'lead': 'Define el texto legible que aparece al usar `print()` o `str()`.',
     'puntos': ['Debe devolver (`return`) una cadena, no imprimirla.',
                'Es pensado para el usuario final: claro y amigable.'],
     'codigo': c('''
class Persona:
    def __init__(self, nombre, edad):
        self.nombre = nombre
        self.edad = edad

    def __str__(self):
        return f"Persona: {self.nombre}, {self.edad} años"

persona1 = Persona("Ana", 30)
print(persona1)
print(str(persona1).upper())
'''),
     'idea': 'Sin `__str__`, `print` no sabe qué mostrar de tu objeto.'},

    {'tipo': 'tema', 'tema': 'Métodos dunder', 'titulo': 'Sin `__str__`: el mensaje raro',
     'lead': 'Si la clase no define cómo mostrarse, Python imprime su tipo y su dirección en memoria.',
     'puntos': ['Verás algo como `<__main__.Coche object at 0x…>`.',
                'La dirección cambia en cada ejecución.',
                'La solución es añadir `__str__` (o `__repr__`).'],
     'codigo': c('''
class Coche:
    def __init__(self, marca, modelo):
        self.marca = marca
        self.modelo = modelo

mi_coche = Coche("Ford", "Focus")
print(mi_coche)
'''),
     'salida': '<__main__.Coche object at 0x…>   (la dirección cambia en cada ejecución)',
     'nota': 'El comentario del Colab dice «Salida: Coche: Ford Focus», pero esa clase no tiene `__str__`, así que se imprime la dirección del objeto, como muestra la salida real del Colab.'},

    {'tipo': 'tema', 'tema': 'Métodos dunder', 'titulo': '`__repr__`: la versión para programadores',
     'lead': 'Una representación inequívoca, idealmente la forma de volver a crear el objeto.',
     'puntos': ['La usan `repr()`, la consola y las listas al mostrarse.',
                'Si no hay `__str__`, `print` usa `__repr__`.',
                '`__str__` es para personas; `__repr__`, para depurar.'],
     'codigo': c('''
class Punto:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return f"Punto(x={self.x}, y={self.y})"

p = Punto(6, 4)
print(repr(p))
print(p)
print([p, Punto(0, 0)])
'''),
     'nota': 'El comentario del Colab dice «Punto(x=3, y=4)», pero el objeto se crea con `Punto(6, 4)`.'},

    {'tipo': 'tema', 'tema': 'Métodos dunder', 'titulo': '`__len__`: que `len()` funcione',
     'lead': 'Ideal para clases que guardan una colección, como una pila.',
     'puntos': ['`len(pila)` llama a `pila.__len__()`.',
                'Debe devolver un entero.',
                'Aquí la pila delega en la lista interna `self.items`.'],
     'codigo': c('''
class Pila:
    def __init__(self):
        self.items = []

    def __len__(self):
        return len(self.items)

    def _push(self, item):
        self.items.append(item)

pila = Pila()
for valor in [10, 20, 30, 60, 40]:
    pila._push(valor)
print(len(pila))
'''),
     'nota': 'El comentario del Colab dice «Salida: 2», pero se apilan cinco valores, así que `len(pila)` es 5. Además, el guion bajo de `_push` indica uso interno; para un método pensado para usarse desde afuera, sería más claro llamarlo `push` o `apilar`.'},

    {'tipo': 'tema', 'tema': 'Métodos dunder', 'titulo': '`__eq__`: comparar con `==`',
     'lead': 'Decide cuándo dos objetos de tu clase cuentan como iguales.',
     'puntos': ['Sin `__eq__`, `==` solo es `True` si es exactamente el mismo objeto.',
                'Aquí, dos coches son iguales si coinciden marca y modelo.',
                'Debe devolver `True` o `False`.'],
     'codigo': c('''
class Coche:
    def __init__(self, marca, modelo):
        self.marca = marca
        self.modelo = modelo

    def __eq__(self, otro):
        return self.marca == otro.marca and self.modelo == otro.modelo

coche1 = Coche("Bmw", "Model 5")
coche2 = Coche("Bmw", "Model 5")
coche3 = Coche("Rolls Royce", "Model 1")
print(coche1 == coche2)
print(coche1 == coche3)
'''),
     'idea': 'Prueba a borrar `__eq__` y vuelve a ejecutar: `coche1 == coche2` pasará a ser `False`.'},

    {'tipo': 'tema', 'tema': 'Métodos dunder', 'titulo': '`__add__`: sumar objetos con `+`',
     'lead': 'Define qué significa `objeto1 + objeto2` para tu clase.',
     'puntos': ['`v1 + v2` llama a `v1.__add__(v2)`.',
                'Devuelve un objeto **nuevo**; no modifica los originales.',
                'Como el resultado también es un `Vector`, puedes encadenar sumas.'],
     'codigo': c('''
class Vector:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def __add__(self, otro):
        return Vector(self.x + otro.x, self.y + otro.y, self.z + otro.z)

    def __str__(self):
        return f"({self.x}, {self.y}, {self.z})"

v1 = Vector(2, 3, 1)
v2 = Vector(6, 5, 2)
v3 = v1 + v2
v4 = v1 + v2 + v3
v5 = v1 + v2 + v3 + v4
print(v3)
print(v5)
'''),
     'idea': 'En el Colab la tercera componente se llama `L`; aquí se usa `z`, el nombre habitual en 3D. El resultado es el mismo.'},

    {'tipo': 'tema', 'tema': 'Métodos dunder', 'titulo': 'Tabla mental · ¿Qué dispara cada dunder?',
     'lead': 'Asocia cada método con la operación de Python que lo activa.',
     'puntos': ['`Clase(...)` → `__init__`',
                '`print(obj)` o `str(obj)` → `__str__`',
                '`repr(obj)` o mostrar una lista → `__repr__`',
                '`len(obj)` → `__len__`',
                '`a == b` → `__eq__` · `a + b` → `__add__`'],
     'idea': 'Hay muchos más: `__lt__` para `<`, `__getitem__` para `obj[i]`, `__contains__` para `in`…'},

    {'tipo': 'practica', 'tema': 'Métodos dunder', 'titulo': 'Práctica 03 · Clase `Dinero`',
     'lead': 'Combina tres métodos dunder en una sola clase.',
     'reto': 'Crea `Dinero(cantidad, moneda)` con `__str__` (que muestre `"15.5 USD"`), `__add__` (que sume dos cantidades de la misma moneda) y `__eq__`. Suma 10 USD + 5.5 USD, imprime el resultado y compáralo con `Dinero(15.5, "USD")`.',
     'solucion': c('''
class Dinero:
    def __init__(self, cantidad, moneda):
        self.cantidad = cantidad
        self.moneda = moneda

    def __add__(self, otro):
        return Dinero(self.cantidad + otro.cantidad, self.moneda)

    def __eq__(self, otro):
        return self.cantidad == otro.cantidad and self.moneda == otro.moneda

    def __str__(self):
        return f"{self.cantidad} {self.moneda}"

total = Dinero(10, "USD") + Dinero(5.5, "USD")
print(total)
print(total == Dinero(15.5, "USD"))
'''),
     'idea': 'Extra: en `__add__`, lanza un error si las monedas son distintas.'},

    # ---------- 04 · Reto
    {'tipo': 'capitulo', 'titulo': '04 / Reto final', 'texto': 'Una clase que contiene objetos de otra clase.'},

    {'tipo': 'practica', 'tema': 'Reto final', 'titulo': 'Reto · Mi playlist',
     'lead': 'Dos clases que trabajan juntas, con métodos normales y dunder.',
     'reto': 'Crea `Cancion(titulo, segundos)` con `__str__`. Crea `Playlist(nombre)` que guarde una lista de canciones, con `agregar(cancion)`, `__len__` y `duracion_total()` en minutos. Agrega tres canciones e imprime cuántas hay, la duración total y cada canción.',
     'solucion': c('''
class Cancion:
    def __init__(self, titulo, segundos):
        self.titulo = titulo
        self.segundos = segundos

    def __str__(self):
        minutos, seg = divmod(self.segundos, 60)
        return f"{self.titulo} ({minutos}:{seg:02d})"

class Playlist:
    def __init__(self, nombre):
        self.nombre = nombre
        self.canciones = []

    def agregar(self, cancion):
        self.canciones.append(cancion)

    def __len__(self):
        return len(self.canciones)

    def duracion_total(self):
        return round(sum(c.segundos for c in self.canciones) / 60, 1)

mix = Playlist("Para estudiar")
mix.agregar(Cancion("Lo-fi 1", 185))
mix.agregar(Cancion("Piano", 240))
mix.agregar(Cancion("Lluvia", 302))
print(f"{mix.nombre}: {len(mix)} canciones, {mix.duracion_total()} min")
for cancion in mix.canciones:
    print("-", cancion)
'''),
     'idea': 'Una `Playlist` contiene objetos `Cancion`: así se modelan relaciones reales entre objetos.'},

    # ---------- Cierre
    {'tipo': 'tema', 'tema': 'Cierre', 'titulo': 'Errores y detalles detectados en el Colab',
     'lead': 'Varios comentarios del Colab no coinciden con lo que el código imprime.',
     'puntos': ['Sin `__str__`, `print(mi_coche)` muestra la dirección del objeto, no «Coche: Ford Focus».',
                '`Punto(6, 4)` se representa como `Punto(x=6, y=4)`, no `x=3, y=4`.',
                'La pila tiene 5 elementos, no 2; y `_push` sugiere un método interno.',
                'La analogía se titula «receta de galletas», pero el texto habla de un pastel: la idea es la misma.'],
     'idea': 'Ejecuta siempre y compara: la salida real manda sobre el comentario.'},

    {'tipo': 'tema', 'tema': 'Cierre', 'titulo': 'Ficha de repaso · Clase 4',
     'lead': 'Intenta responder sin mirar las diapositivas.',
     'puntos': ['¿Qué diferencia hay entre una clase y un objeto?',
                '¿Para qué sirve `self` y por qué es el primer parámetro?',
                '¿Qué hereda una clase hija y qué hace `super()`?',
                '¿Cuándo se ejecuta `__str__`? ¿Y `__eq__`?',
                '¿Qué imprime `print(obj)` si la clase no tiene `__str__` ni `__repr__`?'],
     'idea': 'Próximo paso: reescribe el reto de la Clase 3 (boletín) como una clase `Estudiante`.'},
]
