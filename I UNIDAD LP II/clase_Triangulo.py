import math
import sys

class Triangulo:
    def __init__(self, lado1, lado2, lado3):
        self.__lado1 = lado1
        self.__lado2 = lado2
        self.__lado3 = lado3

    def validar(self):
        # Verifica si los lados cumplen con la desigualdad triangular
        if (
            self.__lado1 + self.__lado2 > self.__lado3 and
            self.__lado1 + self.__lado3 > self.__lado2 and
            self.__lado2 + self.__lado3 > self.__lado1
        ):
            return True
        return False

    def calcular_perimetro(self):
        if self.validar():
            return self.__lado1 + self.__lado2 + self.__lado3
        else:
            return "No es un triángulo válido"

    def calcular_area(self):
        if self.validar():
            s = self.calcular_perimetro() / 2  # semiperímetro
            area = math.sqrt(
                s * (s - self.__lado1) * (s - self.__lado2) * (s - self.__lado3)
            )
            return area
        else:
            return "No es un triángulo válido"

# Crear instancia y usar métodos
triangulo = Triangulo(3, 4, 5)
if triangulo.validar():
    print("Es un triángulo válido")
else:
    print("No es un triángulo válido")

print("Perímetro:", triangulo.calcular_perimetro())
print("Área:", triangulo.calcular_area())

# Tamaños en memoria
print("\nTamaños en memoria (bytes):")
tam_objeto = sys.getsizeof(triangulo)                      # Objeto completo
tam_lado1 = sys.getsizeof(triangulo._Triangulo__lado1)      # Atributo lado1
tam_lado2 = sys.getsizeof(triangulo._Triangulo__lado2)      # Atributo lado2
tam_lado3 = sys.getsizeof(triangulo._Triangulo__lado3)      # Atributo lado3
tam_area = sys.getsizeof(triangulo.calcular_area)           # Método calcular_area
tam_perimetro = sys.getsizeof(triangulo.calcular_perimetro) # Método calcular_perimetro
tam_validar = sys.getsizeof(triangulo.validar)              # Método validar
tam_clase = sys.getsizeof(Triangulo)                        # Clase en sí

# Mostrar tamaños
print(f"Objeto triangulo             : {tam_objeto} bytes")
print(f"Atributo lado1               : {tam_lado1} bytes")
print(f"Atributo lado2               : {tam_lado2} bytes")
print(f"Atributo lado3               : {tam_lado3} bytes")
print(f"Método calcular_area         : {tam_area} bytes")
print(f"Método calcular_perimetro    : {tam_perimetro} bytes")
print(f"Método validar               : {tam_validar} bytes")
print(f"Clase Triangulo              : {tam_clase} bytes")

# Suma total de memoria usada (en una sola línea)
print(f"\nSuma total de memoria usada: {tam_objeto + tam_lado1 + tam_lado2 + tam_lado3 + tam_area + tam_perimetro + tam_validar + tam_clase} bytes")
