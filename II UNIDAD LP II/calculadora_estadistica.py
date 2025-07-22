from typing import TypeVar, Generic, List
import math

T = TypeVar("T", int, float)

class CalculadoraEstadistica(Generic[T]):
    def __init__(self, datos: List[T]):
        self.datos = datos

    def promedio(self) -> float:
        return sum(self.datos) / len(self.datos)

    def minimo(self) -> T:
        return min(self.datos)

    def maximo(self) -> T:
        return max(self.datos)

    def varianza(self) -> float:
        media = self.promedio()
        return sum((x - media) ** 2 for x in self.datos) / len(self.datos)

    def desviacion_estandar(self) -> float:
        return math.sqrt(self.varianza())

datos_enteros = [10, 20, 15, 25, 30]
datos_decimales = [10.5, 19.8, 14.2, 25.7, 29.9]


print(" Estadísticas para enteros:")
calc_int = CalculadoraEstadistica[int](datos_enteros)
print(f"Promedio: {calc_int.promedio():.2f}")
print(f"Mínimo: {calc_int.minimo()}")
print(f"Máximo: {calc_int.maximo()}")
print(f"Varianza: {calc_int.varianza():.2f}")
print(f"Desviación estándar: {calc_int.desviacion_estandar():.2f}")

print("\n Estadísticas para decimales:")
calc_float = CalculadoraEstadistica[float](datos_decimales)
print(f"Promedio: {calc_float.promedio():.2f}")
print(f"Mínimo: {calc_float.minimo()}")
print(f"Máximo: {calc_float.maximo()}")
print(f"Varianza: {calc_float.varianza():.2f}")
print(f"Desviación estándar: {calc_float.desviacion_estandar():.2f}")

