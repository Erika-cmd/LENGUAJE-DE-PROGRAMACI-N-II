# -----------------------------------------------
# EXAMEN: Sistema de gestión de vehículos
# -----------------------------------------------

from abc import ABC, abstractmethod

# -----------------------------------------------
# PARTE 4: Excepción personalizada para año inválido
# -----------------------------------------------
class AnioInvalidoError(Exception):
    def __init__(self, anio):
        super().__init__(f"Error: Año inválido ({anio}). Debe estar entre 1980 y 2025.")

# -----------------------------------------------
# PARTE 1: Clase abstracta base: Vehiculo
# -----------------------------------------------
class Vehiculo(ABC):
    def __init__(self, marca, modelo, anio):
        if anio < 1980 or anio > 2025:
            raise AnioInvalidoError(anio)
        self.marca = marca
        self.modelo = modelo
        self.anio = anio

    @abstractmethod
    def calcular_impuesto(self):
        """Este método será implementado por cada clase hija"""
        pass

    def mostrar_info(self):
        print("\n🚗 Información del Vehículo:")
        print(f"- Marca : {self.marca}")
        print(f"- Modelo: {self.modelo}")
        print(f"- Año   : {self.anio}")

# -----------------------------------------------
# PARTE 2: Clases hijas Auto y Motocicleta
# -----------------------------------------------
class Auto(Vehiculo):
    def calcular_impuesto(self):
        return round(0.05 * (2025 - self.anio), 2)

class Motocicleta(Vehiculo):
    def calcular_impuesto(self):
        return round(0.03 * (2025 - self.anio), 2)

# -----------------------------------------------
# PREGUNTA EXTRA: Clase Camioneta
# -----------------------------------------------
class Camioneta(Vehiculo):
    def calcular_impuesto(self):
        try:
            if int(self.modelo) > 2015:
                return 500
            else:
                return 300
        except:
            print("⚠️ Error: El modelo debe ser numérico para calcular el impuesto.")
            return 0

# -----------------------------------------------
# Función para crear vehículos con validación
# -----------------------------------------------
def crear_vehiculo(tipo, marca, modelo, anio):
    try:
        if tipo == "auto":
            return Auto(marca, modelo, anio)
        elif tipo == "moto":
            return Motocicleta(marca, modelo, anio)
        elif tipo == "camioneta":
            return Camioneta(marca, modelo, anio)
        else:
            print(f"⚠️ Tipo desconocido: {tipo}")
            return None
    except AnioInvalidoError as e:
        print(e)
        return None

# -----------------------------------------------
# PARTE 3: Mostrar todos los vehículos (polimorfismo)
# -----------------------------------------------
def mostrar_vehiculos(lista_vehiculos):
    for v in lista_vehiculos:
        if v:
            v.mostrar_info()
            impuesto = v.calcular_impuesto()
            print(f"💰 Impuesto calculado: S/ {impuesto:.2f}")

# -----------------------------------------------
# PRUEBA GENERAL DEL SISTEMA (Ejecución del examen)
# -----------------------------------------------
if __name__ == "__main__":
    # Lista de vehículos de prueba
    vehiculos = [
        crear_vehiculo("auto", "Toyota", "Corolla", 2010),
        crear_vehiculo("moto", "Yamaha", "FZ", 2020),
        crear_vehiculo("camioneta", "Chevrolet", "2016", 2018),
        crear_vehiculo("auto", "Hyundai", "Elantra", 1985),
        crear_vehiculo("moto", "Honda", "CBR", 1975),  # Año inválido
        crear_vehiculo("camioneta", "Mazda", "2012", 2014)
    ]

    # Mostrar los vehículos correctamente creados
    mostrar_vehiculos(vehiculos)
