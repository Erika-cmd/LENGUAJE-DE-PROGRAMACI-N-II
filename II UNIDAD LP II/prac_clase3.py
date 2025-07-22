import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from datetime import datetime
import random # Para simular fallos
import time   # Para simular retrasos

# --- Clases Base y Subclases de Pago ---

# Clase base (interfaz de pago)
class Pago:
    # Ahora procesar_pago acepta 'de_quien'
    def procesar_pago(self, monto, de_quien, a_quien, output_widget):
        output_widget.insert(tk.END, "No se puede procesar un pago genérico.\n")
        output_widget.see(tk.END)
        return {"estado": "Fallida", "error": "Método de pago no válido"}

# Subclase: Pago con tarjeta de crédito
class PagoTarjetaCredito(Pago):
    def __init__(self, numero_tarjeta, titular, cvv):
        self.numero_tarjeta = numero_tarjeta
        self.titular = titular
        self.cvv = cvv

    def _validar_datos(self):
        # Validación de formato y longitud
        if not self.numero_tarjeta.isdigit() or len(self.numero_tarjeta) not in [13, 15, 16]:
            return False, "Número de tarjeta inválido (debe ser numérico, 13, 15 o 16 dígitos)."
        if not self.titular.replace(" ", "").isalpha():
            return False, "Nombre del titular inválido (solo letras y espacios)."
        if not self.cvv.isdigit() or len(self.cvv) not in [3, 4]:
            return False, "CVV inválido (3 o 4 dígitos numéricos)."
        # Simulación de Algoritmo de Luhn (muy básico, solo para demostración)
        if not self._luhn_check(self.numero_tarjeta):
             return False, "Número de tarjeta no pasa la verificación de Luhn."
        return True, ""

    def _luhn_check(self, card_no):
        """Implementación simplificada del Algoritmo de Luhn."""
        digits = [int(d) for d in card_no]
        checksum = 0
        for i, digit in enumerate(reversed(digits)):
            if i % 2 == 1: # Doblar cada segundo dígito
                digit *= 2
                if digit > 9:
                    digit -= 9
            checksum += digit
        return checksum % 10 == 0


    def procesar_pago(self, monto, de_quien, a_quien, output_widget):
        valido, error_msg = self._validar_datos()
        if not valido:
            output_widget.insert(tk.END, f"Error de validación: {error_msg}\n\n")
            output_widget.see(tk.END)
            return {"estado": "Fallida", "error": error_msg}

        fecha_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Simular procesamiento externo con posible fallo
        time.sleep(1) # Simular retraso de red/procesamiento
        if random.random() < 0.15: # 15% de probabilidad de fallo simulado
            error = "Transacción rechazada por el banco (simulado)."
            output_widget.insert(tk.END, f"[{fecha_hora}] FALLO: Pago de ${monto:.2f} de {de_quien} a {a_quien}.\nError: {error}\n\n")
            output_widget.see(tk.END)
            return {"fecha_hora": fecha_hora, "metodo": "Tarjeta de Crédito",
                    "monto": monto, "de_quien": de_quien, "a_quien": a_quien,
                    "detalles": f"Tarjeta ****{self.numero_tarjeta[-4:]}",
                    "estado": "Fallida", "error": error}
        
        mensaje = (f"[{fecha_hora}] Procesando pago de ${monto:.2f} de {de_quien} a {a_quien} con tarjeta de crédito.\n"
                   f"Tarjeta: **** **** **** {self.numero_tarjeta[-4:]}\n"
                   f"Titular: {self.titular}\n"
                   f"Pago realizado exitosamente.\n\n")
        output_widget.insert(tk.END, mensaje)
        output_widget.see(tk.END)
        
        return {
            "fecha_hora": fecha_hora,
            "metodo": "Tarjeta de Crédito",
            "monto": monto,
            "de_quien": de_quien,
            "a_quien": a_quien,
            "detalles": f"Tarjeta ****{self.numero_tarjeta[-4:]}, Titular: {self.titular}",
            "estado": "Exitosa"
        }

# Subclase: Pago con PayPal
class PagoPayPal(Pago):
    def __init__(self, correo):
        self.correo = correo

    def _validar_datos(self):
        # Validación de formato de correo (básica)
        if "@" not in self.correo or "." not in self.correo or len(self.correo) < 5:
            return False, "Formato de correo electrónico inválido."
        return True, ""

    def procesar_pago(self, monto, de_quien, a_quien, output_widget):
        valido, error_msg = self._validar_datos()
        if not valido:
            output_widget.insert(tk.END, f"Error de validación: {error_msg}\n\n")
            output_widget.see(tk.END)
            return {"estado": "Fallida", "error": error_msg}

        fecha_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Simular procesamiento externo con posible fallo
        time.sleep(0.8) # Simular retraso
        if random.random() < 0.10: # 10% de probabilidad de fallo simulado
            error = "Error de conexión con PayPal (simulado)."
            output_widget.insert(tk.END, f"[{fecha_hora}] FALLO: Pago de ${monto:.2f} de {de_quien} a {a_quien}.\nError: {error}\n\n")
            output_widget.see(tk.END)
            return {"fecha_hora": fecha_hora, "metodo": "PayPal",
                    "monto": monto, "de_quien": de_quien, "a_quien": a_quien,
                    "detalles": f"Cuenta: {self.correo}",
                    "estado": "Fallida", "error": error}

        mensaje = (f"[{fecha_hora}] Procesando pago de ${monto:.2f} de {de_quien} a {a_quien} mediante PayPal.\n"
                   f"Cuenta PayPal: {self.correo}\n"
                   f"Pago realizado exitosamente.\n\n")
        output_widget.insert(tk.END, mensaje)
        output_widget.see(tk.END)
        
        return {
            "fecha_hora": fecha_hora,
            "metodo": "PayPal",
            "monto": monto,
            "de_quien": de_quien,
            "a_quien": a_quien,
            "detalles": f"Cuenta: {self.correo}",
            "estado": "Exitosa"
        }

# Subclase: Pago con criptomoneda
class PagoCriptomoneda(Pago):
    def __init__(self, direccion_wallet, tipo_moneda):
        self.direccion_wallet = direccion_wallet
        self.tipo_moneda = tipo_moneda.upper() # Asegurar mayúsculas

    def _validar_datos(self):
        if not self.direccion_wallet:
            return False, "Dirección de wallet no puede estar vacía."
        if not self.tipo_moneda or self.tipo_moneda not in ["BTC", "ETH", "USDT"]: # Ejemplo de monedas soportadas
            return False, "Tipo de moneda no soportado o inválido (BTC, ETH, USDT)."
        # Validación de formato de dirección de wallet (muy básica, depende de la moneda)
        if self.tipo_moneda == "ETH" and (not self.direccion_wallet.startswith("0x") or len(self.direccion_wallet) != 42 or not all(c in "0123456789abcdefABCDEF" for c in self.direccion_wallet[2:])):
             return False, "Formato de dirección ETH inválido (debe empezar con 0x y tener 42 caracteres hexadecimales)."
        # BTC y USDT pueden tener otros formatos, aquí solo una validación muy básica
        if self.tipo_moneda == "BTC" and not (self.direccion_wallet.startswith("1") or self.direccion_wallet.startswith("3") or self.direccion_wallet.startswith("bc1")):
            return False, "Formato de dirección BTC inválido (debe empezar con 1, 3 o bc1)."
        return True, ""


    def procesar_pago(self, monto, de_quien, a_quien, output_widget):
        valido, error_msg = self._validar_datos()
        if not valido:
            output_widget.insert(tk.END, f"Error de validación: {error_msg}\n\n")
            output_widget.see(tk.END)
            return {"estado": "Fallida", "error": error_msg}

        fecha_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Simular procesamiento externo con posible fallo
        time.sleep(2) # Simular retraso mayor para cripto
        if random.random() < 0.20: # 20% de probabilidad de fallo simulado (red congestionada)
            error = "Fallo en la red de criptomonedas (simulado)."
            output_widget.insert(tk.END, f"[{fecha_hora}] FALLO: Pago de {monto:.4f} {self.tipo_moneda} de {de_quien} a {a_quien}.\nError: {error}\n\n")
            output_widget.see(tk.END)
            return {"fecha_hora": fecha_hora, "metodo": "Criptomoneda",
                    "monto": monto, "de_quien": de_quien, "a_quien": a_quien,
                    "detalles": f"Wallet: {self.direccion_wallet}, Tipo: {self.tipo_moneda}",
                    "estado": "Fallida", "error": error}


        mensaje = (f"[{fecha_hora}] Procesando pago de {monto:.4f} {self.tipo_moneda} de {de_quien} a {a_quien} con criptomoneda.\n"
                   f"Wallet: {self.direccion_wallet}\n"
                   f"Pago realizado exitosamente.\n\n")
        output_widget.insert(tk.END, mensaje)
        output_widget.see(tk.END)
        
        return {
            "fecha_hora": fecha_hora,
            "metodo": "Criptomoneda",
            "monto": f"{monto:.4f} {self.tipo_moneda}", # Monto y tipo de moneda juntos
            "de_quien": de_quien,
            "a_quien": a_quien,
            "detalles": f"Wallet: {self.direccion_wallet}, Tipo: {self.tipo_moneda}",
            "estado": "Exitosa"
        }

# --- Clase Principal de la Aplicación Tkinter ---

class PaymentApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Pagos Polimórfico Avanzado")

        self.transactions_history = [] # Lista para almacenar los pagos
        self.total_processed_amount = 0.0 # Para el resumen del movimiento

        self.create_widgets()

    def create_widgets(self):
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Configurar el grid para que se expanda
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1) # Columna de entradas y combobox
        main_frame.rowconfigure(9, weight=1) # Log se expande
        main_frame.rowconfigure(12, weight=2) # Historial se expande más

        # Cantidad
        ttk.Label(main_frame, text="Monto a Pagar:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.amount_entry = ttk.Entry(main_frame)
        self.amount_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), pady=5)
        self.amount_entry.insert(0, "100.00") # Valor por defecto

        # De Quién Viene
        ttk.Label(main_frame, text="De Quién Viene:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.from_whom_entry = ttk.Entry(main_frame)
        self.from_whom_entry.grid(row=1, column=1, sticky=(tk.W, tk.E), pady=5)
        self.from_whom_entry.insert(0, "Cliente X") # Valor por defecto

        # Pagar a
        ttk.Label(main_frame, text="Pagar a:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.pay_to_entry = ttk.Entry(main_frame)
        self.pay_to_entry.grid(row=2, column=1, sticky=(tk.W, tk.E), pady=5)
        self.pay_to_entry.insert(0, "Comercio Electrónico") # Valor por defecto

        # Selección de método de pago
        ttk.Label(main_frame, text="Método de Pago:").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.payment_method_var = tk.StringVar()
        self.payment_method_combobox = ttk.Combobox(main_frame,
                                                    textvariable=self.payment_method_var,
                                                    values=["Tarjeta de Crédito", "PayPal", "Criptomoneda"])
        self.payment_method_combobox.grid(row=3, column=1, sticky=(tk.W, tk.E), pady=5)
        self.payment_method_combobox.set("Tarjeta de Crédito") # Valor por defecto
        self.payment_method_combobox.bind("<<ComboboxSelected>>", self.show_payment_details)

        # Frame para detalles de pago (cambiará dinámicamente)
        self.details_frame = ttk.LabelFrame(main_frame, text="Detalles del Pago", padding="10")
        self.details_frame.grid(row=4, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=10)
        self.details_frame.columnconfigure(1, weight=1) # Para que las entradas se expandan

        self.show_payment_details() # Mostrar los detalles iniciales

        # Botón Procesar Pago
        process_button = ttk.Button(main_frame, text="Procesar Pago", command=self.process_payment)
        process_button.grid(row=5, column=0, columnspan=2, pady=10)

        # Resumen de movimiento total
        self.total_movement_label = ttk.Label(main_frame, text="Movimiento Total Procesado: $0.00")
        self.total_movement_label.grid(row=6, column=0, columnspan=2, sticky=tk.W, pady=5)


        # Separador
        ttk.Separator(main_frame, orient="horizontal").grid(row=7, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=10)

        # Área de mensajes de salida (Log de pagos)
        ttk.Label(main_frame, text="Log de Pagos:").grid(row=8, column=0, sticky=tk.W, pady=5)
        self.output_text = scrolledtext.ScrolledText(main_frame, width=60, height=8, wrap=tk.WORD)
        self.output_text.grid(row=9, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)
        self.output_text.config(state=tk.DISABLED, background="#e0e0e0") # Deshabilitado y con color para diferenciarlo


        # Separador para historial
        ttk.Separator(main_frame, orient="horizontal").grid(row=10, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=10)

        # Historial de Pagos (Treeview)
        ttk.Label(main_frame, text="Historial de Transacciones:").grid(row=11, column=0, sticky=tk.W, pady=5)
        
        self.history_treeview = ttk.Treeview(main_frame, columns=("Fecha/Hora", "De Quién", "A Quién", "Método", "Monto", "Estado", "Detalles"), show="headings")
        self.history_treeview.grid(row=12, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)

        # Definir encabezados
        self.history_treeview.heading("Fecha/Hora", text="Fecha/Hora")
        self.history_treeview.heading("De Quién", text="De Quién") # Nuevo encabezado
        self.history_treeview.heading("A Quién", text="A Quién")
        self.history_treeview.heading("Método", text="Método")
        self.history_treeview.heading("Monto", text="Monto")
        self.history_treeview.heading("Estado", text="Estado")
        self.history_treeview.heading("Detalles", text="Detalles")

        # Configurar el ancho de las columnas (ajusta según sea necesario)
        self.history_treeview.column("Fecha/Hora", width=120, anchor=tk.CENTER)
        self.history_treeview.column("De Quién", width=100, anchor=tk.W) # Ancho y alineación para "De Quién"
        self.history_treeview.column("A Quién", width=100, anchor=tk.W)
        self.history_treeview.column("Método", width=80, anchor=tk.CENTER)
        self.history_treeview.column("Monto", width=70, anchor=tk.E) # Alinear a la derecha para números
        self.history_treeview.column("Estado", width=70, anchor=tk.CENTER)
        self.history_treeview.column("Detalles", width=180, anchor=tk.W)

        # Agregar scrollbar al Treeview
        tree_scrollbar_y = ttk.Scrollbar(main_frame, orient="vertical", command=self.history_treeview.yview)
        tree_scrollbar_y.grid(row=12, column=2, sticky=(tk.N, tk.S))
        self.history_treeview.configure(yscrollcommand=tree_scrollbar_y.set)

        # Botón para Reembolsar (debajo del historial)
        refund_button = ttk.Button(main_frame, text="Reembolsar Transacción Seleccionada", command=self.process_refund)
        refund_button.grid(row=13, column=0, columnspan=2, pady=10)


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
            self.payment_details['numero_tarjeta'].insert(0, "4111222233334444") # Ejemplo válido Luhn

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
            self.payment_details['direccion_wallet'].insert(0, "0xAbc123dEf4567890123456789012345678901234") # Ejemplo de ETH

            ttk.Label(self.details_frame, text="Tipo de Moneda:").grid(row=1, column=0, sticky=tk.W, pady=2)
            self.payment_details['tipo_moneda'] = ttk.Combobox(self.details_frame, 
                                                                values=["BTC", "ETH", "USDT"], 
                                                                width=8)
            self.payment_details['tipo_moneda'].grid(row=1, column=1, sticky=tk.W, pady=2)
            self.payment_details['tipo_moneda'].set("ETH") # Valor por defecto


    def process_payment(self):
        try:
            amount = float(self.amount_entry.get())
            if amount <= 0:
                messagebox.showerror("Error de Monto", "El monto a pagar debe ser mayor que cero.")
                return
        except ValueError:
            messagebox.showerror("Error de Monto", "Por favor, introduce un monto válido.")
            return

        de_quien = self.from_whom_entry.get().strip()
        if not de_quien:
            messagebox.showerror("Error", "Por favor, especifica de quién viene el pago.")
            return

        a_quien = self.pay_to_entry.get().strip()
        if not a_quien:
            messagebox.showerror("Error", "Por favor, especifica a quién se realiza el pago.")
            return

        method = self.payment_method_var.get()
        current_payment = None
        transaction_data = None 

        # Habilitar el widget de texto para poder insertar
        self.output_text.config(state=tk.NORMAL)
        self.output_text.delete("1.0", tk.END) # Limpiar el contenido anterior del log
        self.output_text.insert(tk.END, f"Iniciando procesamiento de pago de {de_quien} para {method} a {a_quien}...\n")


        if method == "Tarjeta de Crédito":
            numero_tarjeta = self.payment_details['numero_tarjeta'].get()
            titular = self.payment_details['titular'].get()
            cvv = self.payment_details['cvv'].get()
            current_payment = PagoTarjetaCredito(numero_tarjeta, titular, cvv)
        elif method == "PayPal":
            correo = self.payment_details['correo'].get()
            current_payment = PagoPayPal(correo)
        elif method == "Criptomoneda":
            direccion_wallet = self.payment_details['direccion_wallet'].get()
            tipo_moneda = self.payment_details['tipo_moneda'].get()
            current_payment = PagoCriptomoneda(direccion_wallet, tipo_moneda)

        if current_payment:
            # Procesar el pago y obtener los datos de la transacción
            # Se pasa 'de_quien' a procesar_pago
            transaction_data = current_payment.procesar_pago(amount, de_quien, a_quien, self.output_text)
            
            if transaction_data["estado"] == "Exitosa":
                self.transactions_history.append(transaction_data)
                self.update_total_movement(amount)
            elif transaction_data["estado"] == "Fallida":
                messagebox.showwarning("Pago Fallido", f"El pago no pudo ser procesado: {transaction_data.get('error', 'Error desconocido')}")
            
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
        for idx, transaction in enumerate(self.transactions_history):
            # Formatear el monto si es un número, de lo contrario usar el string original (para cripto)
            display_monto = f"${transaction['monto']:.2f}" if isinstance(transaction['monto'], (int, float)) else transaction['monto']
            
            self.history_treeview.insert("", tk.END, iid=idx, values=(
                transaction["fecha_hora"],
                transaction["de_quien"], # Nuevo: Quién envía
                transaction["a_quien"],
                transaction["metodo"],
                display_monto,
                transaction["estado"], 
                transaction["detalles"]
            ), tags=(transaction["estado"].lower(),)) # Para aplicar estilos

        # Definir tags para colores de estado (si no están ya definidos)
        # Esto se hace una vez, pero es seguro llamarlo de nuevo.
        self.history_treeview.tag_configure("exitosa", background="#d4edda", foreground="#155724") # Verde claro
        self.history_treeview.tag_configure("fallida", background="#f8d7da", foreground="#721c24") # Rojo claro
        self.history_treeview.tag_configure("reembolsada", background="#fff3cd", foreground="#856404") # Amarillo claro

    def update_total_movement(self, amount):
        # Solo sumar/restar montos de pagos exitosos en moneda fiat (o equivalente)
        # Para cripto, si se necesita un total en USD, se requeriría una conversión de tasa.
        if isinstance(amount, (int, float)):
            self.total_processed_amount += amount
        
        self.total_movement_label.config(text=f"Movimiento Total Procesado: ${self.total_processed_amount:.2f}")

    def process_refund(self):
        selected_item = self.history_treeview.selection()
        if not selected_item:
            messagebox.showwarning("Reembolso", "Por favor, seleccione una transacción para reembolsar.")
            return

        transaction_index = int(selected_item[0]) 
        
        if 0 <= transaction_index < len(self.transactions_history):
            transaction = self.transactions_history[transaction_index]

            if transaction["estado"] == "Exitosa":
                confirm = messagebox.askyesno("Confirmar Reembolso", 
                                              f"¿Está seguro de que desea reembolsar el pago de {transaction['monto']} de {transaction['de_quien']} a {transaction['a_quien']} ({transaction['metodo']})?")
                if confirm:
                    self.output_text.config(state=tk.NORMAL)
                    self.output_text.insert(tk.END, f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Iniciando reembolso para transacción de {transaction['de_quien']} a {transaction['a_quien']}...\n")
                    self.output_text.see(tk.END)
                    time.sleep(1.5) # Simular tiempo de reembolso

                    # Actualizar el estado de la transacción
                    transaction["estado"] = "Reembolsada"
                    transaction["detalles"] += " (Reembolsado)" 

                    # Restar el monto reembolsado del total, si es numérico
                    if isinstance(transaction['monto'], (int, float)):
                        self.update_total_movement(-transaction['monto'])
                    else: 
                        # Para cripto, el total USD no se ajusta automáticamente aquí
                        self.output_text.insert(tk.END, "Nota: Reembolso de cripto no ajusta el total procesado en USD automáticamente.\n")

                    self.update_history_treeview() # Actualizar la vista del historial
                    self.output_text.insert(tk.END, f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Reembolso de {transaction['monto']} completado exitosamente.\n\n")
                    self.output_text.config(state=tk.DISABLED)
                    messagebox.showinfo("Reembolso", "Reembolso procesado exitosamente.")
                else:
                    self.output_text.insert(tk.END, "Reembolso cancelado por el usuario.\n\n")
                    self.output_text.config(state=tk.DISABLED)
            elif transaction["estado"] == "Reembolsada":
                messagebox.showwarning("Reembolso", "Esta transacción ya ha sido reembolsada.")
            elif transaction["estado"] == "Fallida":
                messagebox.showwarning("Reembolso", "No se puede reembolsar una transacción fallida.")
        else:
            messagebox.showerror("Error de Reembolso", "Transacción seleccionada no válida en el historial.")

if __name__ == "__main__":
    root = tk.Tk()
    app = PaymentApp(root)
    root.mainloop()