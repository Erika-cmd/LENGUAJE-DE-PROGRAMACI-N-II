import math
import sys

class TrianguloRectangulo:
    def __init__(self, base, altura):
        self.base = base       # Atributo base
        self.altura = altura   # Atributo altura
        self.hipotenusa = None # Inicializa el atributo hipotenusa

    def calcular_area(self):  # Método: área = (base * altura) / 2
        return (self.base * self.altura) / 2

    def calcular_perimetro(self):  # Método: perímetro = base + altura + hipotenusa
        self.hipotenusa = math.sqrt(self.base**2 + self.altura**2)
        return self.base + self.altura + self.hipotenusa

# Crear una instancia del triángulo
triangulo = TrianguloRectangulo(3, 4)

# Usar métodos
print(f"Área: {triangulo.calcular_area()}")
print(f"Perímetro: {triangulo.calcular_perimetro()}")

# Tamaños en memoria
print("\nTamaños en memoria (bytes):")
tam_objeto = sys.getsizeof(triangulo)                      # Objeto completo
tam_base = sys.getsizeof(triangulo.base)                   # Atributo base
tam_altura = sys.getsizeof(triangulo.altura)               # Atributo altura
tam_hipotenusa = sys.getsizeof(triangulo.hipotenusa)       # Atributo hipotenusa
tam_area = sys.getsizeof(triangulo.calcular_area)          # Método área
tam_perimetro = sys.getsizeof(triangulo.calcular_perimetro)  # Método perímetro
tam_clase = sys.getsizeof(TrianguloRectangulo)             # Clase en sí

# Mostrar tamaños
print(f"Objeto triangulo             : {tam_objeto} bytes")
print(f"Atributo base                : {tam_base} bytes")
print(f"Atributo altura              : {tam_altura} bytes")
print(f"Atributo hipotenusa          : {tam_hipotenusa} bytes")
print(f"Método calcular_area         : {tam_area} bytes")
print(f"Método calcular_perimetro    : {tam_perimetro} bytes")
print(f"Clase TrianguloRectangulo    : {tam_clase} bytes")

# Suma total de memoria usada (una sola línea)
print(f"\nSuma total de memoria usada: {tam_objeto + tam_base + tam_altura + tam_hipotenusa + tam_area + tam_perimetro + tam_clase} bytes")
