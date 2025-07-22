import math

class Figura:
    def __init__(self, nombre):
        self.__nombre = nombre

    def get_nombre(self):
        return self.__nombre

    def calcular_area(self):
        raise NotImplementedError

    def calcular_perimetro(self):
        raise NotImplementedError

    def mostrar_informacion(self):
        print(f"\nFigura     : {self.get_nombre()}")
        print(f"Área       : {self.calcular_area():.2f}")
        print(f"Perímetro  : {self.calcular_perimetro():.2f}")
        print("-" * 30)

# Subclase: Circulo
class Circulo(Figura):
    def __init__(self, radio):
        super().__init__("Círculo")
        self.__radio = radio

    def get_radio(self):
        return self.__radio

    def calcular_area(self):
        return math.pi * self.__radio ** 2

    def calcular_perimetro(self):
        return 2 * math.pi * self.__radio

# Subclase: Rectangulo
class Rectangulo(Figura):
    def __init__(self, base, altura):
        super().__init__("Rectángulo")
        self.__base = base
        self.__altura = altura

    def get_base(self):
        return self.__base

    def get_altura(self):
        return self.__altura

    def calcular_area(self):
        return self.__base * self.__altura

    def calcular_perimetro(self):
        return 2 * (self.__base + self.__altura)

# Subclase: Triangulo
class Triangulo(Figura):
    def __init__(self, base, altura, lado1, lado2):
        super().__init__("Triángulo")
        self.__base = base
        self.__altura = altura
        self.__lado1 = lado1
        self.__lado2 = lado2

    def calcular_area(self):
        return (self.__base * self.__altura) / 2

    def calcular_perimetro(self):
        return self.__base + self.__lado1 + self.__lado2

# Subclase: Rombo
class Rombo(Figura):
    def __init__(self, D, d, lado):
        super().__init__("Rombo")
        self.__D = D
        self.__d = d
        self.__lado = lado

    def calcular_area(self):
        return (self.__D * self.__d) / 2

    def calcular_perimetro(self):
        return 4 * self.__lado

# Subclase: Pentagono
class Pentagono(Figura):
    def __init__(self, lado, apotema):
        super().__init__("Pentágono")
        self.__lado = lado
        self.__apotema = apotema

    def calcular_area(self):
        return (5 * self.__lado * self.__apotema) / 2

    def calcular_perimetro(self):
        return 5 * self.__lado

def main():
    lista_figuras = []

    while True:
        print("\n****** SISTEMA DE FIGURAS ******")
        print("1. Registrar Círculo")
        print("2. Registrar Rectángulo")
        print("3. Registrar Triángulo")
        print("4. Registrar Rombo")
        print("5. Registrar Pentágono")
        print("6. Mostrar todas las figuras")
        print("7. Salir")

        opcion = input("Ingrese una opción: ").strip()

        try:
            if opcion == "1":
                radio = float(input("Radio del círculo: "))
                lista_figuras.append(Circulo(radio))
                print("✔ Círculo registrado.")

            elif opcion == "2":
                base = float(input("Base del rectángulo: "))
                altura = float(input("Altura del rectángulo: "))
                lista_figuras.append(Rectangulo(base, altura))
                print("✔ Rectángulo registrado.")

            elif opcion == "3":
                base = float(input("Base del triángulo: "))
                altura = float(input("Altura del triángulo: "))
                lado1 = float(input("Lado 1 del triángulo: "))
                lado2 = float(input("Lado 2 del triángulo: "))
                lista_figuras.append(Triangulo(base, altura, lado1, lado2))
                print("✔ Triángulo registrado.")

            elif opcion == "4":
                D = float(input("Diagonal mayor del rombo: "))
                d = float(input("Diagonal menor del rombo: "))
                lado = float(input("Lado del rombo: "))
                lista_figuras.append(Rombo(D, d, lado))
                print("✔ Rombo registrado.")

            elif opcion == "5":
                lado = float(input("Lado del pentágono: "))
                apotema = float(input("Apotema del pentágono: "))
                lista_figuras.append(Pentagono(lado, apotema))
                print("✔ Pentágono registrado.")

            elif opcion == "6":
                if not lista_figuras:
                    print("No hay figuras registradas.")
                else:
                    for figura in lista_figuras:
                        figura.mostrar_informacion()

            elif opcion == "7":
                print("Saliendo del sistema…")
                break

            else:
                print("✖ Opción inválida.")

        except ValueError:
            print("✖ Entrada no válida. Use solo números.")

if __name__ == "__main__":
    main()
