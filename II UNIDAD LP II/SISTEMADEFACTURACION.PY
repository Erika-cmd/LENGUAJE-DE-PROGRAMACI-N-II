from abc import ABC, abstractmethod
from typing import List

# -------------------- PRINCIPIO D: Dependency Inversion --------------------
class IImprimible(ABC):  # Abstracción de impresoras
    @abstractmethod
    def imprimir(self, factura):
        pass

# -------------------- PRINCIPIO S: Single Responsibility --------------------
class Producto:
    def __init__(self, nombre: str, precio: float):
        self.nombre = nombre
        self.precio = precio

class Cliente:
    def __init__(self, nombre: str, dni: str):
        self.nombre = nombre
        self.dni = dni

# -------------------- PRINCIPIO L: Liskov Substitution --------------------
class ItemFactura:
    def __init__(self, producto: Producto, cantidad: int):
        self.producto = producto
        self.cantidad = cantidad

    def subtotal(self):
        return self.producto.precio * self.cantidad

# -------------------- PRINCIPIO O: Open/Closed Principle --------------------
class Factura:
    def __init__(self, cliente: Cliente):
        self.cliente = cliente
        self.items: List[ItemFactura] = []

    def agregar_item(self, item: ItemFactura):
        self.items.append(item)

    def calcular_total(self):
        return sum(item.subtotal() for item in self.items)

# -------------------- PRINCIPIO I: Interface Segregation (con impresora) --------------------
class ImpresoraSimple(IImprimible):
    def imprimir(self, factura: Factura):
        print("======== FACTURA ========")
        print(f"Cliente: {factura.cliente.nombre} | DNI: {factura.cliente.dni}")
        for item in factura.items:
            print(f"- {item.producto.nombre} x {item.cantidad} = S/ {item.subtotal():.2f}")
        print(f"TOTAL: S/ {factura.calcular_total():.2f}")
        print("=========================")

# -------------------- USO DEL SISTEMA --------------------
if __name__ == "__main__":
    # Crear productos
    arroz = Producto("Arroz", 3.50)
    aceite = Producto("Aceite", 10.00)

    # Crear cliente
    cliente = Cliente("Erika Valencia", "73820258")

    # Crear factura
    factura = Factura(cliente)
    factura.agregar_item(ItemFactura(arroz, 2))
    factura.agregar_item(ItemFactura(aceite, 1))

    # Imprimir con impresora
    impresora = ImpresoraSimple()
    impresora.imprimir(factura)
