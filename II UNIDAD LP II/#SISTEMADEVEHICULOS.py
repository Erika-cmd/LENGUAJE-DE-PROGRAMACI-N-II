class Vehiculo:
    def __init__(self, nombre, marca, modelo, anio):
        self.__nombre = nombre
        self.__marca = marca
        self.__modelo = modelo
        self.__anio = anio

    def get_nombre(self):
        return self.__nombre

    def get_marca(self):
        return self.__marca

    def get_modelo(self):
        return self.__modelo

    def get_anio(self):
        return self.__anio

    def consumo_por_km(self):
        raise NotImplementedError

    def coste_por_km(self, precio_combustible):
        return self.consumo_por_km() * precio_combustible

    def mostrar_informacion(self, precio_combustible):
        print(f"\nTipo        : {self.get_nombre()}")
        print(f"Marca       : {self.get_marca()}")
        print(f"Modelo      : {self.get_modelo()}")
        print(f"Año         : {self.get_anio()}")
        print(f"Consumo/km  : {self.consumo_por_km():.3f} litros o kWh")
        print(f"Coste/km    : S/. {self.coste_por_km(precio_combustible):.2f}")
        print("-" * 40)

# Subclase: Auto
class Auto(Vehiculo):
    def __init__(self, marca, modelo, anio, consumo_l100):
        super().__init__("Auto", marca, modelo, anio)
        self.__consumo = consumo_l100 / 100

    def consumo_por_km(self):
        return self.__consumo

# Subclase: Camion
class Camion(Vehiculo):
    def __init__(self, marca, modelo, anio, consumo_l100):
        super().__init__("Camión", marca, modelo, anio)
        self.__consumo = consumo_l100 / 100

    def consumo_por_km(self):
        return self.__consumo

# Subclase: Motocicleta
class Motocicleta(Vehiculo):
    def __init__(self, marca, modelo, anio, consumo_l100):
        super().__init__("Motocicleta", marca, modelo, anio)
        self.__consumo = consumo_l100 / 100

    def consumo_por_km(self):
        return self.__consumo

# Subclase: Autobus
class Autobus(Vehiculo):
    def __init__(self, marca, modelo, anio, consumo_l100):
        super().__init__("Autobús", marca, modelo, anio)
        self.__consumo = consumo_l100 / 100

    def consumo_por_km(self):
        return self.__consumo

# Subclase: Bicicleta
class Bicicleta(Vehiculo):
    def __init__(self, marca, modelo, anio):
        super().__init__("Bicicleta", marca, modelo, anio)

    def consumo_por_km(self):
        return 0.0

def main():
    vehiculos = []
    while True:
        print("\n****** SISTEMA DE VEHÍCULOS ******")
        print("1. Registrar Auto")
        print("2. Registrar Camión")
        print("3. Registrar Motocicleta")
        print("4. Registrar Autobús")
        print("5. Registrar Bicicleta")
        print("6. Mostrar todos los vehículos")
        print("7. Salir")

        opcion = input("Opción: ").strip()
        try:
            if opcion in ["1", "2", "3", "4"]:
                marca = input("Marca: ")
                modelo = input("Modelo: ")
                anio = int(input("Año: "))
                consumo = float(input("Consumo (litros o kWh por 100 km): "))
                if opcion == "1":
                    vehiculos.append(Auto(marca, modelo, anio, consumo))
                elif opcion == "2":
                    vehiculos.append(Camion(marca, modelo, anio, consumo))
                elif opcion == "3":
                    vehiculos.append(Motocicleta(marca, modelo, anio, consumo))
                elif opcion == "4":
                    vehiculos.append(Autobus(marca, modelo, anio, consumo))
                print("✔ Vehículo registrado correctamente.")
            elif opcion == "5":
                marca = input("Marca: ")
                modelo = input("Modelo: ")
                anio = int(input("Año: "))
                vehiculos.append(Bicicleta(marca, modelo, anio))
                print("✔ Bicicleta registrada correctamente.")
            elif opcion == "6":
                if not vehiculos:
                    print("✖ No hay vehículos registrados.")
                else:
                    precio = float(input("Precio del combustible por litro/kWh: S/. "))
                    for v in vehiculos:
                        v.mostrar_informacion(precio)
            elif opcion == "7":
                print("Saliendo del sistema...")
                break
            else:
                print("✖ Opción inválida.")
        except ValueError:
            print("✖ Entrada no válida. Intente de nuevo.")

if __name__ == "__main__":
    main()
