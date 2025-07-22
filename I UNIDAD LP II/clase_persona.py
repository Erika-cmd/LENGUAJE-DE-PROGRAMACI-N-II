import sys
class Persona:
    def __init__(self, nombre):
        self.nombre = nombre 
p1 = Persona("patricia")

tamaño = sys.getsizeof (p1)
print (f"El objeto p1 ocupa {tamaño} bytes en memoria")
        