import math

class OperacionesMatematicas:
    def __init__(self, valor: float):
        self.x = valor

    def potencia(self) -> float:
        return round(math.pow(self.x, 2), 4)

    def raiz_cuadrada(self):
        if self.x < 0:
            return "Raíz cuadrada solo está definida para números no negativos."
        return f"{math.sqrt(self.x):.2f}"

    def logaritmo_natural(self):
        if self.x <= 0:
            return "Logaritmo solo está definido para números positivos."
        return f"{math.log(self.x):.2f}"

    def seno(self) -> float:
        return round(math.sin(math.radians(self.x)), 4)

    def coseno(self) -> float:
        return round(math.cos(math.radians(self.x)), 4)

    def tangente(self) -> float:
        return round(math.tan(math.radians(self.x)), 4)

# 🔢 Ejemplo con valor positivo
print("---- Con x = 45 ----")
op1 = OperacionesMatematicas(45)
print(f"Potencia (x^2): {op1.potencia()}")
print(f"Raíz cuadrada: {op1.raiz_cuadrada()}")
print(f"Logaritmo natural (ln x): {op1.logaritmo_natural()}")
print(f"Seno: {op1.seno()}")
print(f"Coseno: {op1.coseno()}")
print(f"Tangente: {op1.tangente()}")

# 🔴 Ejemplo con valor negativo
print("\n---- Con x = -5 ----")
op2 = OperacionesMatematicas(-5)
print(f"Potencia (x^2): {op2.potencia()}")
print(f"Raíz cuadrada: {op2.raiz_cuadrada()}")
print(f"Logaritmo natural (ln x): {op2.logaritmo_natural()}")
print(f"Seno: {op2.seno()}")
print(f"Coseno: {op2.coseno()}")
print(f"Tangente: {op2.tangente()}")
