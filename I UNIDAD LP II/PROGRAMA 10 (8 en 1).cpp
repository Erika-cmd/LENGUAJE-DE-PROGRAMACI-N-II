class NodoCurso:
    def __init__(self, nombre, requisito=None):
        self.nombre = nombre
        self.requisito = requisito
        self.siguiente = None

class ListaCursos:
    def __init__(self):
        self.inicio = None

    def agregar_curso(self, nombre, requisito_nombre=None):
        nuevo = NodoCurso(nombre)
        actual = self.inicio
        while actual:
            if actual.nombre == requisito_nombre:
                nuevo.requisito = actual
                break
            actual = actual.siguiente
        nuevo.siguiente = self.inicio
        self.inicio = nuevo

    def mostrar_cursos(self):
        actual = self.inicio
        while actual:
            if actual.requisito:
                print(f"{actual.nombre} requiere {actual.requisito.nombre}")
            else:
                print(f"{actual.nombre} no tiene requisitos")
            actual = actual.siguiente

lista = ListaCursos()
lista.agregar_curso("Matemática Básica")
lista.agregar_curso("Álgebra", "Matemática Básica")
lista.agregar_curso("Cálculo I", "Álgebra")
lista.agregar_curso("Cálculo II", "Cálculo I")
lista.mostrar_cursos()
