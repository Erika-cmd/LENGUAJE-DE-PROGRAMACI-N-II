from typing import TypeVar, Generic

T = TypeVar("T", int, float)

class Collatz(Generic[T]):
    def __init__(self, numero: T):
        self.n = int(numero)  # Convertimos a entero, porque Collatz solo aplica a enteros

    def mostrar_secuencia(self):
        if self.n <= 0:
            print("La conjetura solo se aplica a números enteros positivos.")
            return

        print(f"Secuencia de Collatz para {self.n}:")
        pasos = 0
        n = self.n
        while n != 1:
            print(n, end=" → ")
            if n % 2 == 0:
                n = n // 2
            else:
                n = 3 * n + 1
            pasos += 1
        print("1")
        print(f"Pasos totales: {pasos}")

# 🔢 Pruebas
collatz_entero = Collatz 
collatz_entero.mostrar_secuencia()

print()

collatz_decimal = Collatz[float](13.0)
collatz_decimal.mostrar_secuencia()
