# Clase base (interfaz de pago)
class Pago:
    def procesar_pago(self, monto):
        print("No se puede procesar un pago genérico.")

# Subclase: Pago con tarjeta de crédito
class PagoTarjetaCredito(Pago):
    def __init__(self, numero_tarjeta, titular, cvv):
        self.numero_tarjeta = numero_tarjeta
        self.titular = titular
        self.cvv = cvv

    def procesar_pago(self, monto):
        print(f"Procesando pago de ${monto:.2f} con tarjeta de crédito.")
        print(f"Tarjeta: **** **** **** {self.numero_tarjeta[-4:]}")
        print(f"Titular: {self.titular}")
        print("Pago realizado exitosamente.\n")

# Subclase: Pago con PayPal
class PagoPayPal(Pago):
    def __init__(self, correo):
        self.correo = correo

    def procesar_pago(self, monto):
        print(f"Procesando pago de ${monto:.2f} mediante PayPal.")
        print(f"Cuenta PayPal: {self.correo}")
        print("Pago realizado exitosamente.\n")

# Subclase: Pago con criptomoneda
class PagoCriptomoneda(Pago):
    def __init__(self, direccion_wallet, tipo_moneda):
        self.direccion_wallet = direccion_wallet
        self.tipo_moneda = tipo_moneda

    def procesar_pago(self, monto):
        print(f"Procesando pago de {monto:.4f} {self.tipo_moneda} con criptomoneda.")
        print(f"Wallet: {self.direccion_wallet}")
        print("Pago realizado exitosamente.\n")

# Uso del polimorfismo
pagos = [
    PagoTarjetaCredito("1234567812345678", "ERIKA VALENCIA", "123"),
    PagoPayPal("erika@example.com"),
    PagoCriptomoneda("0xabc123def456", "ETH")
]

# Procesar cada pago con polimorfismo
for pago in pagos:
    pago.procesar_pago(100)
