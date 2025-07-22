import math

class Ciudad:
    def __init__(self, nombre, x, y):
        self.nombre = nombre
        self.x = x
        self.y = y
    
    def distancia(self, otra_ciudad):
        dx = self.x - otra_ciudad.x
        dy = self.y - otra_ciudad.y
        return math.sqrt(dx**2 + dy**2)

ciudad1 = Ciudad("Arequipa", 10, 20)
ciudad2 = Ciudad("Cuzco", 40, 60)

distancia_km = ciudad1.distancia(ciudad2)

print(f"Distancia entre {ciudad1.nombre} y {ciudad2.nombre}: {distancia_km:.2f} unidades")
