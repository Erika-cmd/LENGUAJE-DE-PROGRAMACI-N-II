import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import simpledialog

# Clase Producto
class Producto:
    def __init__(self, nombre, precio, stock, unidad, marca):
        self.nombre = nombre
        self.precio = precio
        self.stock = stock
        self.unidad = unidad
        self.marca = marca

    def mostrar_informacion(self):
        return f"{self.nombre} ({self.marca}) - {self.precio} por {self.unidad} - {self.stock} {self.unidad}"

    def actualizar_precio(self, nuevo_precio):
        self.precio = nuevo_precio

    def actualizar_stock(self, nuevo_stock):
        self.stock = nuevo_stock

    def aplicar_descuento(self, porcentaje):
        self.precio *= (1 - porcentaje / 100)

# Productos iniciales
productos = [
    Producto("Arroz", 3.50, 100, "kg", "La Abuela"),
    Producto("Azúcar", 4.50, 50, "kg", "Dulzura"),
    Producto("Aceite", 8.00, 80, "litros", "Aceituna Dorada"),
    Producto("Leche", 4.50, 60, "litros", "Alpina"),
    Producto("Cereal", 5.00, 30, "cajas", "Cornflakes"),
    Producto("Galletas", 2.50, 90, "paquetes", "Delicias")
]

# Funciones
def actualizar_producto():
    try:
        print("Actualizando producto...")
        precio = float(entrada_precio.get())
        stock = int(entrada_stock.get())
        if precio < 0 or stock < 0:
            raise ValueError("Precio y stock deben ser positivos.")
        producto = productos[combo_producto.current()]
        producto.actualizar_precio(precio)
        producto.actualizar_stock(stock)
        etiqueta_estado.config(text=f"{producto.nombre} actualizado correctamente.", fg="green")
        actualizar_tabla()
    except ValueError as e:
        etiqueta_estado.config(text=f"Error: {e}", fg="red")
        print(f"Error: {e}")

def aplicar_descuento():
    try:
        print("Aplicando descuento...")
        porcentaje = float(entrada_descuento.get())
        if porcentaje < 0 or porcentaje > 100:
            raise ValueError("El descuento debe estar entre 0 y 100.")
        producto = productos[combo_producto.current()]
        producto.aplicar_descuento(porcentaje)
        etiqueta_estado.config(text=f"Descuento del {porcentaje}% aplicado a {producto.nombre}.", fg="blue")
        actualizar_tabla()
    except ValueError as e:
        etiqueta_estado.config(text=f"Error: {e}", fg="red")
        print(f"Error: {e}")

def realizar_venta():
    try:
        print("Realizando venta...")
        cantidad = int(entrada_cantidad.get())
        if cantidad <= 0:
            raise ValueError("La cantidad debe ser mayor a 0.")
        producto = productos[combo_producto.current()]
        if producto.stock < cantidad:
            raise ValueError("Stock insuficiente.")
        producto.stock -= cantidad
        total = round(producto.precio * cantidad, 2)
        etiqueta_estado.config(text=f"Venta realizada: {cantidad} x {producto.nombre} = ${total}", fg="purple")
        actualizar_tabla()
    except ValueError as e:
        etiqueta_estado.config(text=f"Error: {e}", fg="red")
        print(f"Error: {e}")

def actualizar_tabla():
    print("Actualizando tabla...")
    for row in tabla_productos.get_children():
        tabla_productos.delete(row)
    for prod in productos:
        tabla_productos.insert("", "end", values=(prod.nombre, prod.marca, f"${prod.precio:.2f}", f"{prod.stock} {prod.unidad}"))

def limpiar_campos():
    entrada_precio.delete(0, tk.END)
    entrada_stock.delete(0, tk.END)
    entrada_descuento.delete(0, tk.END)
    entrada_cantidad.delete(0, tk.END)

# Interfaz
ventana = tk.Tk()
ventana.title("Sistema de Gestión de Minimarket")
ventana.geometry("700x600")
ventana.configure(bg="#f0f8ff")

# Título
tk.Label(ventana, text="Gestión de Productos - Minimarket", font=("Helvetica", 18, "bold"),
         bg="#00BFFF", fg="white", pady=15).pack(fill="x")

# Frame de entrada
frame_entrada = tk.Frame(ventana, bg="#f0f8ff")
frame_entrada.pack(pady=10)

tk.Label(frame_entrada, text="Producto:", bg="#f0f8ff", font=("Arial", 12)).grid(row=0, column=0, padx=5, pady=5)
combo_producto = ttk.Combobox(frame_entrada, values=[p.nombre for p in productos], state="readonly", font=("Arial", 12))
combo_producto.current(0)
combo_producto.grid(row=0, column=1, padx=5, pady=5)

tk.Label(frame_entrada, text="Nuevo Precio:", bg="#f0f8ff", font=("Arial", 12)).grid(row=1, column=0, padx=5, pady=5)
entrada_precio = tk.Entry(frame_entrada, font=("Arial", 12))
entrada_precio.grid(row=1, column=1, padx=5, pady=5)

tk.Label(frame_entrada, text="Nuevo Stock:", bg="#f0f8ff", font=("Arial", 12)).grid(row=2, column=0, padx=5, pady=5)
entrada_stock = tk.Entry(frame_entrada, font=("Arial", 12))
entrada_stock.grid(row=2, column=1, padx=5, pady=5)

tk.Label(frame_entrada, text="Descuento (%):", bg="#f0f8ff", font=("Arial", 12)).grid(row=3, column=0, padx=5, pady=5)
entrada_descuento = tk.Entry(frame_entrada, font=("Arial", 12))
entrada_descuento.grid(row=3, column=1, padx=5, pady=5)

tk.Label(frame_entrada, text="Cantidad a vender:", bg="#f0f8ff", font=("Arial", 12)).grid(row=4, column=0, padx=5, pady=5)
entrada_cantidad = tk.Entry(frame_entrada, font=("Arial", 12))
entrada_cantidad.grid(row=4, column=1, padx=5, pady=5)

# Botones
frame_botones = tk.Frame(ventana, bg="#f0f8ff")
frame_botones.pack(pady=10)

tk.Button(frame_botones, text="Actualizar Producto", bg="#4CAF50", fg="white", font=("Arial", 11),
          command=actualizar_producto).grid(row=0, column=0, padx=10)

tk.Button(frame_botones, text="Aplicar Descuento", bg="#FFA500", fg="white", font=("Arial", 11),
          command=aplicar_descuento).grid(row=0, column=1, padx=10)

tk.Button(frame_botones, text="Realizar Venta", bg="#8A2BE2", fg="white", font=("Arial", 11),
          command=realizar_venta).grid(row=0, column=2, padx=10)

# Estado
etiqueta_estado = tk.Label(ventana, text="", font=("Arial", 12, "italic"), bg="#f0f8ff")
etiqueta_estado.pack(pady=10)

# Tabla de productos
tabla_productos = ttk.Treeview(ventana, columns=("Nombre", "Marca", "Precio", "Stock"), show="headings", height=10)
tabla_productos.heading("Nombre", text="Nombre")
tabla_productos.heading("Marca", text="Marca")
tabla_productos.heading("Precio", text="Precio")
tabla_productos.heading("Stock", text="Stock")
tabla_productos.pack(padx=20, pady=10, fill="x")

# Actualizar la tabla al inicio
actualizar_tabla()

# Iniciar la interfaz
print("Iniciando la interfaz...")
ventana.mainloop()

