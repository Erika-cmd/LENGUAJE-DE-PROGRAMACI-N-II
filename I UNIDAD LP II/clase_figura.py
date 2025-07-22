import math

# Clase padre
class Figura:
    def __init__(self, color):
        self.color = color

# Clase hija que hereda de Figura
class Circulo(Figura):
    def __init__(self, color, radio):
        super().__init__(color)  # Llama al constructor de la clase padre
        self.radio = radio

    def calcular_area(self):
        return math.pi * self.radio ** 2

    def calcular_perimetro(self):
        return 2 * math.pi * self.radio

# Ejemplo de uso
c = Circulo("Rojo", 7)

print("=== Información del Círculo ===")
print(f"Color: {c.color}")
print(f"Radio: {c.radio}")
print(f"Área: {c.calcular_area():.2f}")
print(f"Perímetro: {c.calcular_perimetro():.2f}")
