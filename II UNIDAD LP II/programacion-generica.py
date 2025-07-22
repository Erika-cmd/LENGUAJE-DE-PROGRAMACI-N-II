from typing import TypeVar, Generic 
import math

T = TypeVar("T", int, float)

class Pitagoras(Generic[T]):
    def __init__(self, cateto1: T, cateto2: T):
        self.a = cateto1
        self.b = cateto2

    def calcular_hipotenusa(self) -> float:
        return math.sqrt(self.a ** 2 + self.b ** 2)

    def calcular_promedio(self) -> T:
        promedio = (self.a + self.b) / 2
        if isinstance(self.a, int) and isinstance(self.b, int):
            return int(promedio)
        else:
            return float(promedio)

pitagoras_enteros = Pitagoras[int](8, 12)
pitagoras_decimal = Pitagoras[float](5.5, 7.3)

print("Teorema de Pitágoras con enteros:")
print(f"Catetos: {pitagoras_enteros.a} y {pitagoras_enteros.b}")
print(f"Hipotenusa: {pitagoras_enteros.calcular_hipotenusa():.2f}")
print(f"Promedio: {pitagoras_enteros.calcular_promedio()}")

print("Teorema de Pitágoras con decimales:")
print(f"Catetos: {pitagoras_decimal.a} y {pitagoras_decimal.b}")
print(f"Hipotenusa: {pitagoras_decimal.calcular_hipotenusa():.2f}")
print(f"Promedio: {pitagoras_decimal.calcular_promedio():.2f}")
