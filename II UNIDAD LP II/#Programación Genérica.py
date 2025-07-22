from typing import TypeVar, Generic
import math

T = TypeVar("T", int, float)

class OperacionMatematica(Generic[T]):
    def calcular(self, a: T, b: T) -> T:
        raise NotImplementedError("Método calcular() no implementado")

class Suma(OperacionMatematica[T]):
    def calcular(self, a: T, b: T) -> T:
        return a + b

class Hipotenusa(OperacionMatematica[T]):
    def calcular(self, a: T, b: T) -> T:
        return math.sqrt(a**2 + b**2)

class Factorial(OperacionMatematica[int]):
    def calcular(self, a: int, b: int = 0) -> int:
        if a < 0:
            raise ValueError("No se puede calcular el factorial de un número negativo.")
        return math.factorial(a)

def main():
    suma = Suma()
    num1 = 5
    num2 = 7
    resultado_suma = suma.calcular(num1, num2)
    print(f"La suma de {num1} + {num2} es {resultado_suma}")

    hipo = Hipotenusa()
    cateto1 = 4
    cateto2 = 5
    resultado_hipo = hipo.calcular(cateto1, cateto2)
    print(f"La hipotenusa de lados {cateto1} y {cateto2} es {resultado_hipo:.2f}")

    factorial = Factorial()
    numero = 5
    resultado_fact = factorial.calcular(numero)
    print(f"El factorial de {numero} es {resultado_fact}")

if __name__ == "__main__":
    main()

