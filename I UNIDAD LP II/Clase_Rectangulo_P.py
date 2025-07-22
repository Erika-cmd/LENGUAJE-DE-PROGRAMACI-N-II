class Rectangulo:
    # Constructor
    def __init__(self, longitud, ancho):
        self.longitud = float(longitud)
        self.ancho = float(ancho)
        print(f"Constructor: Rectángulo creado con longitud {self.longitud} y ancho {self.ancho}")

    # Método para calcular y mostrar el área
    def mostrar_area(self):
        area = self.longitud * self.ancho
        print(f"El área del rectángulo es: {area}")

    # Método para calcular y mostrar el perímetro
    def mostrar_perimetro(self):
        perimetro = 2 * (self.longitud + self.ancho)
        print(f"El perímetro del rectángulo es: {perimetro}")

    # Destructor
    def __del__(self):
        print("Destructor: Rectángulo eliminado")


# Programa principal
print("¡Bienvenido! Vamos a calcular el área y perímetro de un rectángulo.\n")
longitud = input("Ingrese la longitud: ")
ancho = input("Ingrese el ancho: ")

rectangulo = Rectangulo(longitud, ancho)
rectangulo.mostrar_area()
rectangulo.mostrar_perimetro()

# Eliminamos el objeto para que se vea el mensaje del destructor
del rectangulo
