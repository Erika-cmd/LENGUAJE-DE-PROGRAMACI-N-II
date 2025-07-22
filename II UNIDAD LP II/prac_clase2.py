import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from datetime import datetime

# Clase base (interfaz de pago)
class Pago:
    def procesar_pago(self, monto, a_quien, output_widget):
        # Este método ahora también recibe el widget de salida y 'a_quien'
        output_widget.insert(tk.END, "No se puede procesar un pago genérico.\n")
        output_widget.see(tk.END)
        return None # Retorna None si no es un pago válido

# Subclase: Pago con tarjeta de crédito
class PagoTarjetaCredito(Pago):
    def __init__(self, numero_tarjeta, titular, cvv):
        self.numero_tarjeta = numero_tarjeta
        self.titular = titular
        self.cvv = cvv

    def procesar_pago(self, monto, a_quien, output_widget):
        fecha_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        mensaje = (f"[{fecha_hora}] Procesando pago de ${monto:.2f} con tarjeta de crédito a {a_quien}.\n"
                   f"Tarjeta: **** **** **** {self.numero_tarjeta[-4:]}\n"
                   f"Titular: {self.titular}\n"
                   f"Pago realizado exitosamente.\n\n")
        output_widget.insert(tk.END, mensaje)
        output_widget.see(tk.END)
        
        # Retornar los datos de la transacción para el historial
        return {
            "fecha_hora": fecha_hora,
            "metodo": "Tarjeta de Crédito",
            "monto": monto,
            "a_quien": a_quien,
            "detalles": f"Tarjeta terminada en {self.numero_tarjeta[-4:]}, Titular: {self.titular}"
        }

# Subclase: Pago con PayPal
class PagoPayPal(Pago):
    def __init__(self, correo):
        self.correo = correo

    def procesar_pago(self, monto, a_quien, output_widget):
        fecha_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        mensaje = (f"[{fecha_hora}] Procesando pago de ${monto:.2f} mediante PayPal a {a_quien}.\n"
                   f"Cuenta PayPal: {self.correo}\n"
                   f"Pago realizado exitosamente.\n\n")
        output_widget.insert(tk.END, mensaje)
        output_widget.see(tk.END)
        
        return {
            "fecha_hora": fecha_hora,
            "metodo": "PayPal",
            "monto": monto,
            "a_quien": a_quien,
            "detalles": f"Cuenta: {self.correo}"
        }

# Subclase: Pago con criptomoneda
class PagoCriptomoneda(Pago):
    def __init__(self, direccion_wallet, tipo_moneda):
        self.direccion_wallet = direccion_wallet
        self.tipo_moneda = tipo_moneda

    def procesar_pago(self, monto, a_quien, output_widget):
        fecha_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        mensaje = (f"[{fecha_hora}] Procesando pago de {monto:.4f} {self.tipo_moneda} con criptomoneda a {a_quien}.\n"
                   f"Wallet: {self.direccion_wallet}\n"
                   f"Pago realizado exitosamente.\n\n")
        output_widget.insert(tk.END, mensaje)
        output_widget.see(tk.END)
        
        return {
            "fecha_hora": fecha_hora,
            "metodo": "Criptomoneda",
            "monto": f"{monto:.4f} {self.tipo_moneda}", # Formato especial para cripto
            "a_quien": a_quien,
            "detalles": f"Wallet: {self.direccion_wallet}, Tipo: {self.tipo_moneda}"
        }

class PaymentApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Pagos Polimórfico y Historial")

        self.transactions_history = [] # Lista para almacenar los pagos
        self.create_widgets()

    def create_widgets(self):
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Configurar el grid para que se expanda
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1) # Columna de entradas y combobox

        # Cantidad
        ttk.Label(main_frame, text="Monto a Pagar:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.amount_entry = ttk.Entry(main_frame)
        self.amount_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), pady=5)
        self.amount_entry.insert(0, "100.00") # Valor por defecto

        # Pagar a
        ttk.Label(main_frame, text="Pagar a:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.pay_to_entry = ttk.Entry(main_frame)
        self.pay_to_entry.grid(row=1, column=1, sticky=(tk.W, tk.E), pady=5)
        self.pay_to_entry.insert(0, "Proveedor Ejemplo") # Valor por defecto

        # Selección de método de pago
        ttk.Label(main_frame, text="Método de Pago:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.payment_method_var = tk.StringVar()
        self.payment_method_combobox = ttk.Combobox(main_frame,
                                                    textvariable=self.payment_method_var,
                                                    values=["Tarjeta de Crédito", "PayPal", "Criptomoneda"])
        self.payment_method_combobox.grid(row=2, column=1, sticky=(tk.W, tk.E), pady=5)
        self.payment_method_combobox.set("Tarjeta de Crédito") # Valor por defecto
        self.payment_method_combobox.bind("<<ComboboxSelected>>", self.show_payment_details)

        # Frame para detalles de pago (cambiará dinámicamente)
        self.details_frame = ttk.LabelFrame(main_frame, text="Detalles del Pago", padding="10")
        self.details_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=10)
        self.details_frame.columnconfigure(1, weight=1) # Para que las entradas se expandan

        self.show_payment_details() # Mostrar los detalles iniciales

        # Botón Procesar Pago
        process_button = ttk.Button(main_frame, text="Procesar Pago", command=self.process_payment)
        process_button.grid(row=4, column=0, columnspan=2, pady=10)

        # Separador
        ttk.Separator(main_frame, orient="horizontal").grid(row=6, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=10)

        # Área de mensajes de salida (Log de pagos)
        ttk.Label(main_frame, text="Log de Pagos:").grid(row=7, column=0, sticky=tk.W, pady=5)
        self.output_text = scrolledtext.ScrolledText(main_frame, width=60, height=8, wrap=tk.WORD)
        self.output_text.grid(row=8, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)
        self.output_text.config(state=tk.DISABLED, background="#e0e0e0") # Deshabilitado y con color para diferenciarlo
        main_frame.rowconfigure(8, weight=1) # Para que el log se expanda

        # Separador para historial
        ttk.Separator(main_frame, orient="horizontal").grid(row=9, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=10)

        # Historial de Pagos (Treeview)
        ttk.Label(main_frame, text="Historial de Transacciones:").grid(row=10, column=0, sticky=tk.W, pady=5)
        
        self.history_treeview = ttk.Treeview(main_frame, columns=("Fecha/Hora", "Método", "Monto", "A Quién", "Detalles"), show="headings")
        self.history_treeview.grid(row=11, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)

        # Definir encabezados
        self.history_treeview.heading("Fecha/Hora", text="Fecha/Hora")
        self.history_treeview.heading("Método", text="Método")
        self.history_treeview.heading("Monto", text="Monto")
        self.history_treeview.heading("A Quién", text="A Quién")
        self.history_treeview.heading("Detalles", text="Detalles")

        # Configurar el ancho de las columnas (ajusta según sea necesario)
        self.history_treeview.column("Fecha/Hora", width=150, anchor=tk.CENTER)
        self.history_treeview.column("Método", width=100, anchor=tk.CENTER)
        self.history_treeview.column("Monto", width=80, anchor=tk.E) # Alinear a la derecha para números
        self.history_treeview.column("A Quién", width=150, anchor=tk.W)
        self.history_treeview.column("Detalles", width=250, anchor=tk.W)

        # Agregar scrollbar al Treeview
        tree_scrollbar_y = ttk.Scrollbar(main_frame, orient="vertical", command=self.history_treeview.yview)
        tree_scrollbar_y.grid(row=11, column=2, sticky=(tk.N, tk.S))
        self.history_treeview.configure(yscrollcommand=tree_scrollbar_y.set)
        
        main_frame.rowconfigure(11, weight=2) # Para que el historial se expanda más que el log


    def clear_details_frame(self):
        for widget in self.details_frame.winfo_children():
            widget.destroy()
        self.payment_details = {} # Reset payment details

    def show_payment_details(self, event=None):
        self.clear_details_frame()
        method = self.payment_method_var.get()

        if method == "Tarjeta de Crédito":
            ttk.Label(self.details_frame, text="Número de Tarjeta:").grid(row=0, column=0, sticky=tk.W, pady=2)
            self.payment_details['numero_tarjeta'] = ttk.Entry(self.details_frame)
            self.payment_details['numero_tarjeta'].grid(row=0, column=1, sticky=(tk.W, tk.E), pady=2)
            self.payment_details['numero_tarjeta'].insert(0, "1234567812345678")

            ttk.Label(self.details_frame, text="Titular:").grid(row=1, column=0, sticky=tk.W, pady=2)
            self.payment_details['titular'] = ttk.Entry(self.details_frame)
            self.payment_details['titular'].grid(row=1, column=1, sticky=(tk.W, tk.E), pady=2)
            self.payment_details['titular'].insert(0, "ERIKA VALENCIA")

            ttk.Label(self.details_frame, text="CVV:").grid(row=2, column=0, sticky=tk.W, pady=2)
            self.payment_details['cvv'] = ttk.Entry(self.details_frame, width=5)
            self.payment_details['cvv'].grid(row=2, column=1, sticky=tk.W, pady=2)
            self.payment_details['cvv'].insert(0, "123")

        elif method == "PayPal":
            ttk.Label(self.details_frame, text="Correo Electrónico:").grid(row=0, column=0, sticky=tk.W, pady=2)
            self.payment_details['correo'] = ttk.Entry(self.details_frame)
            self.payment_details['correo'].grid(row=0, column=1, sticky=(tk.W, tk.E), pady=2)
            self.payment_details['correo'].insert(0, "erika@example.com")

        elif method == "Criptomoneda":
            ttk.Label(self.details_frame, text="Dirección de Wallet:").grid(row=0, column=0, sticky=tk.W, pady=2)
            self.payment_details['direccion_wallet'] = ttk.Entry(self.details_frame)
            self.payment_details['direccion_wallet'].grid(row=0, column=1, sticky=(tk.W, tk.E), pady=2)
            self.payment_details['direccion_wallet'].insert(0, "0xabc123def456")

            ttk.Label(self.details_frame, text="Tipo de Moneda:").grid(row=1, column=0, sticky=tk.W, pady=2)
            self.payment_details['tipo_moneda'] = ttk.Entry(self.details_frame, width=10)
            self.payment_details['tipo_moneda'].grid(row=1, column=1, sticky=tk.W, pady=2)
            self.payment_details['tipo_moneda'].insert(0, "ETH")

    def process_payment(self):
        try:
            amount = float(self.amount_entry.get())
            if amount <= 0:
                messagebox.showerror("Error de Monto", "El monto a pagar debe ser mayor que cero.")
                return
        except ValueError:
            messagebox.showerror("Error de Monto", "Por favor, introduce un monto válido.")
            return

        a_quien = self.pay_to_entry.get().strip()
        if not a_quien:
            messagebox.showerror("Error", "Por favor, especifica a quién se realiza el pago.")
            return

        method = self.payment_method_var.get()
        current_payment = None
        transaction_data = None # Para almacenar los datos de la transacción

        # Habilitar el widget de texto para poder insertar
        self.output_text.config(state=tk.NORMAL)
        self.output_text.delete("1.0", tk.END) # Limpiar el contenido anterior del log

        if method == "Tarjeta de Crédito":
            numero_tarjeta = self.payment_details['numero_tarjeta'].get()
            titular = self.payment_details['titular'].get()
            cvv = self.payment_details['cvv'].get()
            if not all([numero_tarjeta, titular, cvv]):
                messagebox.showerror("Error de Datos", "Por favor, complete todos los campos de la tarjeta de crédito.")
                self.output_text.config(state=tk.DISABLED)
                return
            current_payment = PagoTarjetaCredito(numero_tarjeta, titular, cvv)
        elif method == "PayPal":
            correo = self.payment_details['correo'].get()
            if not correo:
                messagebox.showerror("Error de Datos", "Por favor, ingrese el correo electrónico de PayPal.")
                self.output_text.config(state=tk.DISABLED)
                return
            current_payment = PagoPayPal(correo)
        elif method == "Criptomoneda":
            direccion_wallet = self.payment_details['direccion_wallet'].get()
            tipo_moneda = self.payment_details['tipo_moneda'].get()
            if not all([direccion_wallet, tipo_moneda]):
                messagebox.showerror("Error de Datos", "Por favor, complete todos los campos de la criptomoneda.")
                self.output_text.config(state=tk.DISABLED)
                return
            current_payment = PagoCriptomoneda(direccion_wallet, tipo_moneda)

        if current_payment:
            # Pasar el widget de salida y 'a_quien' a la clase de pago
            transaction_data = current_payment.procesar_pago(amount, a_quien, self.output_text)
            if transaction_data: # Si la transacción fue exitosa y retornó datos
                self.transactions_history.append(transaction_data)
                self.update_history_treeview()
        else:
            self.output_text.insert(tk.END, "Error: Método de pago no reconocido.\n\n")

        # Deshabilitar el widget de texto después de insertar
        self.output_text.config(state=tk.DISABLED)

    def update_history_treeview(self):
        # Limpiar el treeview existente
        for item in self.history_treeview.get_children():
            self.history_treeview.delete(item)

        # Insertar los datos del historial
        for transaction in self.transactions_history:
            self.history_treeview.insert("", tk.END, values=(
                transaction["fecha_hora"],
                transaction["metodo"],
                f"${transaction['monto']:.2f}" if isinstance(transaction['monto'], (int, float)) else transaction['monto'], # Formatear el monto
                transaction["a_quien"],
                transaction["detalles"]
            ))


if __name__ == "__main__":
    root = tk.Tk()
    app = PaymentApp(root)
    root.mainloop()