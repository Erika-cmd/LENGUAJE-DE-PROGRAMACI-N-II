class Rectangulo:
    def __init__(self, base, altura, color):
        if base <= 0 or altura <= 0:
            raise ValueError("La base y la altura deben ser mayores que 0.")
        self.base = base
        self.altura = altura
        self._color = color

    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, color):
        if not isinstance(color, str):
            raise ValueError("El color debe ser una cadena de texto.")
        self._color = color

    def calcular_area(self):
        return self.base * self.altura

    def calcular_perimetro(self):
        return 2 * (self.base + self.altura)

    def redimensionar(self, factor):
        if factor <= 0:
            raise ValueError("El factor de redimensionamiento debe ser mayor que 0.")
        self.base *= factor
        self.altura *= factor

# Ejemplo de uso
try:
    rect1 = Rectangulo(5, 10, 'rojo')
    print(f"Área rectángulo 1: {rect1.calcular_area()}")
    print(f"Perímetro rectángulo 1: {rect1.calcular_perimetro()}")
    rect1.redimensionar(2)
    print(f"Nuevo área del rectángulo 1 después de redimensionar: {rect1.calcular_area()}")
    rect1.color = "azul"
    print(f"Nuevo color del rectángulo 1: {rect1.color}")

except ValueError as e:
    print(f"Error: {e}")
