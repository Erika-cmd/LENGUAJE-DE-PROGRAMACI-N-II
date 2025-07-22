class Suma:
    def __init__(self, a, b):
        self.__a = a
        self.__b = b

    def resultado(self):
        return self.__a + self.__b

    def get_a(self):
        return self.__a
    
    def get_b(self):
        return self.__b
    
    def set_a(self, nuevo_a):
        self.__a = nuevo_a

    def set_b(self, nuevo_b):
        self.__b = nuevo_b

# Uso de la clase
operacion = Suma(7, 3)
print("La suma es:", operacion.resultado())

operacion.set_a(10)  # cambiamos el valor de a
print("La nueva suma es:", operacion.resultado())



    