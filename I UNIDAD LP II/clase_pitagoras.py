import sys
import math

class Pitagoras:
    def __init__(self, cateto1, cateto2):
        self.cateto1 = cateto1
        self.cateto2 = cateto2
    
    def calcular_hipotenusa(self):
        return math.sqrt(self.cateto1**2 + self.cateto2**2)

triangulo = Pitagoras(3, 4)
print(f"Hipotenusa {triangulo.calcular_hipotenusa()}")

print("\nTamaños en memoria (bytes)")
tam_objeto = sys.getsizeof(triangulo)
tam_objeto1 = sys.getsizeof(triangulo.cateto1)
tam_objeto2 = sys.getsizeof(triangulo.cateto2)
tam_metodo = sys.getsizeof(triangulo.calcular_hipotenusa)  # tamaño del método
tam_clase = sys.getsizeof(Pitagoras)  # tamaño de la clase

print(f"Objeto triangulo : {tam_objeto} bytes")
print(f"Objeto1 triangulo : {tam_objeto1} bytes")
print(f"Objeto2 triangulo : {tam_objeto2} bytes")
print(f"Método calcular_hipotenusa : {tam_metodo} bytes")
print(f"Clase Pitagoras : {tam_clase} bytes")

# Suma total del uso de memoria
suma_total = tam_objeto + tam_objeto1 + tam_objeto2 + tam_metodo + tam_clase
print(f"\nSuma total de memoria usada: {suma_total} bytes")
