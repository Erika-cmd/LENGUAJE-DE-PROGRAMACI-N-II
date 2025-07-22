from abc import ABC, abstractmethod

# ⚠️ Excepción personalizada por año inválido
class AnioInvalidoError(Exception):
    def __init__(self, anio):
        super().__init__(f"❌ Año inválido: {anio}. Debe estar entre 1980 y 2025.")

# 🚗 Clase base abstracta
class Vehiculo(ABC):
    def __init__(self, marca, modelo, anio):
        if anio < 1980 or anio > 2025:
            raise AnioInvalidoError(anio)
        self.marca = marca
        self.modelo = modelo
        self.anio = anio

    @abstractmethod
    def calcular_impuesto(self):
        pass

    def mostrar_info(self):
        print(f"\n🔹 Marca : {self.marca}")
        print(f"🔹 Modelo: {self.modelo}")
        print(f"🔹 Año   : {self.anio}")

# 🚘 Clase Auto
class Auto(Vehiculo):
    def calcular_impuesto(self):
        return round(0.05 * (2025 - self.anio), 2)

# 🏍️ Clase Motocicleta
class Motocicleta(Vehiculo):
    def calcular_impuesto(self):
        return round(0.03 * (2025 - self.anio), 2)

# 🚙 Clase Camioneta (extra)
class Camioneta(Vehiculo):
    def calcular_impuesto(self):
        try:
            return 500 if int(self.modelo) > 2015 else 300
        except:
            return 0

# 🔧 Creador de vehículos con manejo de errores
def crear_vehiculo(tipo, marca, modelo, anio):
    try:
        if tipo == "auto":
            return Auto(marca, modelo, anio)
        elif tipo == "moto":
            return Motocicleta(marca, modelo, anio)
        elif tipo == "camioneta":
            return Camioneta(marca, modelo, anio)
    except AnioInvalidoError as e:
        print(e)

# 🧾 Muestra toda la información con polimorfismo
def mostrar_vehiculos(lista):
    for v in lista:
        if v:
            v.mostrar_info()
            print(f"💰 Impuesto: S/ {v.calcular_impuesto():.2f}")

# ▶️ Programa principal
vehiculos = [
    crear_vehiculo("auto", "Toyota", "Corolla", 2010),
    crear_vehiculo("moto", "Yamaha", "FZ", 2020),
    crear_vehiculo("camioneta", "Chevrolet", "2016", 2018),
    crear_vehiculo("auto", "Hyundai", "Elantra", 1985),
    crear_vehiculo("moto", "Honda", "CBR", 1975),
    crear_vehiculo("camioneta", "Mazda", "2012", 2014)
]

mostrar_vehiculos(vehiculos)
