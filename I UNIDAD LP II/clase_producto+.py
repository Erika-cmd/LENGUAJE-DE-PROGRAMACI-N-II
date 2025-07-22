class Producto:
    def __init__(self, precio):
        self.precio = precio

    def aplicar_descuento(self, porcentaje):
        self.precio -= self.precio * (porcentaje / 100)

p = Producto(100)
p.aplicar_descuento(10)

print(p.precio)
