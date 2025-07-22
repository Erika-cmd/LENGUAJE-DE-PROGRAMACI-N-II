# 1. Clase base o interfaz
class Figura:
    def dibujar(self):
        print("No se puede dibujar una figura genérica")

# 2. Clases con comportamientos diferentes
class Cuadrado(Figura):
    def __init__(self, lado):
        self.lado = lado

    def dibujar(self):
        print("Figura: Cuadrado")
        for _ in range(self.lado):
            print(" ■ " * self.lado)

class Triangulo(Figura):
    def __init__(self, altura):
        self.altura = altura

    def dibujar(self):
        print("Figura: Triángulo")
        for i in range(1, self.altura + 1):
            print(" ▲ " * i)

class Circulo(Figura):
    def __init__(self, radio):
        self.radio = radio

    def dibujar(self):
        print("Figura: Círculo")
        r = self.radio
        for y in range(-r, r + 1):
            fila = ""
            for x in range(-r, r + 1):
                if x*x + y*y <= r*r:
                    fila += " ●"
                else:
                    fila += "  "
            print(fila)

# 3. Uso polimórfico
figuras = [Cuadrado(3), Triangulo(4), Circulo(5)]

# Dibujar todas las figuras
for figura in figuras:
    figura.dibujar()
    print()  

