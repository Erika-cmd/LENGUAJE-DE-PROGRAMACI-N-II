class Calculadora:
    def __init__(self, numero1, numero2):
        self.__numero1 = numero1
        self.__numero2 = numero2

    def establecer_numeros(self, n1, n2):
        self.__numero1 = n1
        self.__numero2 = n2

    def obtener_suma(self):
        return self.__numero1 + self.__numero2

# Crear el objeto con 5 y 8 y mostrar la suma
calc = Calculadora(5, 8)
print("La suma de 5 + 8 es:", calc.obtener_suma())

# Actualizar los números a 10 y 5 y mostrar la nueva suma
calc.establecer_numeros(10, 5)
print("La suma de 10 + 5 es:", calc.obtener_suma())

