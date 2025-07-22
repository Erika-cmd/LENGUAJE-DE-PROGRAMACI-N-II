from abc import ABC, abstractmethod

class Vehiculo(ABC):
    def __init__(self, marca, modelo, anio):
        if anio < 1980 or anio > 2025:
            raise Exception("Año inválido")
        self.marca = marca
        self.modelo = modelo
        self.anio = anio

    @abstractmethod
    def calcular_impuesto(self):
        pass

    def mostrar_info(self):
        print(f"Marca: {self.marca} | Modelo: {self.modelo} | Año: {self.anio}")
