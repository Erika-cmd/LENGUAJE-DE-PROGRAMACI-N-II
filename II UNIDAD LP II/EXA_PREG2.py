class Auto(Vehiculo):
    def calcular_impuesto(self):
        return 0.05 * (2025 - self.anio)

class Motocicleta(Vehiculo):
    def calcular_impuesto(self):
        return 0.03 * (2025 - self.anio)
