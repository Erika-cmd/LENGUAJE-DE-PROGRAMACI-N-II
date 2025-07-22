class Rectangulo:
    def __init__(self, base, altura, color):
        self.base = base
        self.altura = altura
        self.color = color

    def area(self):
        return self.base * self.altura

    def perimetro(self):
        return 2 * (self.base + self.altura)

    def mostrar_info(self):
        print(f"Rectángulo de base {self.base}, altura {self.altura}, color {self.color}")
        print(f"Área: {self.area()} - Perímetro: {self.perimetro()}")


class Cuadrado(Rectangulo):
    def __init__(self, lado, color):
        super().__init__(lado, lado, color)

    def mostrar_info(self):
        print(f"Cuadrado de lado {self.base}, color {self.color}")
        print(f"Área: {self.area()} - Perímetro: {self.perimetro()}")


# Código principal
r1 = Rectangulo(10, 5, "verde")
c1 = Cuadrado(7, "azul")

r1.mostrar_info()
c1.mostrar_info()
