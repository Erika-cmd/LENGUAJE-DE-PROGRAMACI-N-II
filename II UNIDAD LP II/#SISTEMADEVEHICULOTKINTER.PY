import tkinter as tk
from tkinter import ttk, messagebox

# ────────────────────
# Clase base (superclase)
# ────────────────────
class Vehiculo:
    def __init__(self, nombre: str, marca: str, modelo: str, anio: int, 
                 registrador: str = "N/A", notario: str = "N/A") -> None:
        # Encapsulamiento: Atributos privados
        self.__nombre = nombre
        self.__marca = marca
        self.__modelo = modelo
        self.__anio = anio
        self.__registrador = registrador # Nuevo atributo para el registrador
        self.__notario = notario       # Nuevo atributo para el notario

    # Getters para acceder a los atributos encapsulados
    def get_nombre(self) -> str:
        return self.__nombre

    def get_marca(self) -> str:
        return self.__marca

    def get_modelo(self) -> str:
        return self.__modelo

    def get_anio(self) -> int:
        return self.__anio
    
    def get_registrador(self) -> str:
        return self.__registrador

    def get_notario(self) -> str:
        return self.__notario

    # Método polimórfico: debe ser implementado por las subclases
    def consumo_por_km(self) -> float:
        """Calcula y retorna el consumo de combustible/energía por kilómetro."""
        raise NotImplementedError("El método consumo_por_km debe ser implementado por las subclases.")

    # Método común para todas las subclases
    def coste_por_km(self, precio_combustible: float) -> float:
        """Calcula el coste por kilómetro basado en el consumo y el precio del combustible."""
        return self.consumo_por_km() * precio_combustible

    def get_info_for_display(self, precio_combustible: float) -> tuple:
        """
        Retorna una tupla con la información del vehículo para ser mostrada en la GUI.
        Polimorfismo: Cada subclase puede añadir sus propios detalles si es necesario.
        """
        # Formato para el Treeview, incluyendo registrador y notario
        return (
            self.get_nombre(),
            self.get_marca(),
            self.get_modelo(),
            self.get_anio(),
            f"{self.consumo_por_km():.3f}",
            f"S/. {self.coste_por_km(precio_combustible):.2f}",
            self.get_registrador(), # Nuevo
            self.get_notario()     # Nuevo
        )

# ────────────────────
# Subclase: Auto
# ────────────────────
class Auto(Vehiculo):
    def __init__(self, marca: str, modelo: str, anio: int, consumo_l100: float,
                 registrador: str = "N/A", notario: str = "N/A") -> None:
        super().__init__("Auto", marca, modelo, anio, registrador, notario)
        # Convertir consumo de L/100km a L/km
        self.__consumo = consumo_l100 / 100

    # Polimorfismo: Implementación específica del consumo
    def consumo_por_km(self) -> float:
        return self.__consumo

# ────────────────────
# Subclase: Camion
# ────────────────────
class Camion(Vehiculo):
    def __init__(self, marca: str, modelo: str, anio: int, consumo_l100: float,
                 registrador: str = "N/A", notario: str = "N/A") -> None:
        super().__init__("Camión", marca, modelo, anio, registrador, notario)
        self.__consumo = consumo_l100 / 100

    # Polimorfismo: Implementación específica del consumo
    def consumo_por_km(self) -> float:
        return self.__consumo

# ────────────────────
# Subclase: Motocicleta
# ────────────────────
class Motocicleta(Vehiculo):
    def __init__(self, marca: str, modelo: str, anio: int, consumo_l100: float,
                 registrador: str = "N/A", notario: str = "N/A") -> None:
        super().__init__("Motocicleta", marca, modelo, anio, registrador, notario)
        self.__consumo = consumo_l100 / 100

    # Polimorfismo: Implementación específica del consumo
    def consumo_por_km(self) -> float:
        return self.__consumo

# ────────────────────
# Subclase: Autobus
# ────────────────────
class Autobus(Vehiculo):
    def __init__(self, marca: str, modelo: str, anio: int, consumo_l100: float,
                 registrador: str = "N/A", notario: str = "N/A") -> None:
        super().__init__("Autobús", marca, modelo, anio, registrador, notario)
        self.__consumo = consumo_l100 / 100

    # Polimorfismo: Implementación específica del consumo
    def consumo_por_km(self) -> float:
        return self.__consumo

# ────────────────────
# Subclase: Bicicleta
# ────────────────────
class Bicicleta(Vehiculo):
    def __init__(self, marca: str, modelo: str, anio: int,
                 registrador: str = "N/A", notario: str = "N/A") -> None:
        super().__init__("Bicicleta", marca, modelo, anio, registrador, notario)

    # Polimorfismo: Consumo de 0 para bicicleta
    def consumo_por_km(self) -> float:
        return 0.0

# ────────────────────
# Aplicación Tkinter
# ────────────────────
class VehiculosApp:
    def __init__(self, master: tk.Tk) -> None:
        self.master = master
        master.title("Sistema de Gestión de Vehículos")
        master.geometry("1200x750") # Aumentar el tamaño para las nuevas columnas
        master.resizable(True, True)

        self.vehiculos_list: list[Vehiculo] = [] # Lista para almacenar objetos Vehiculo
        self.precio_combustible = 0.0 # Precio por defecto

        # Configuración de estilos para ttk
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("TFrame", background="#E0F7FA")
        style.configure("TLabel", background="#E0F7FA", font=("Arial", 10))
        style.configure("TButton", font=("Arial", 10, "bold"), padding=6)
        style.configure("Treeview.Heading", font=("Arial", 10, "bold"))
        style.configure("Treeview", font=("Arial", 10))
        style.map("TButton", background=[('active', '#B0E0E6')])

        # --- Frame Principal ---
        main_frame = ttk.Frame(master, padding="10 10 10 10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Configurar columnas y filas para expandir
        main_frame.grid_columnconfigure(0, weight=1)
        main_frame.grid_rowconfigure(1, weight=1)

        # --- Notebook para las pestañas de registro de vehículos ---
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        
        # Crear pestañas para cada tipo de vehículo
        self._create_vehicle_tab("Auto", self._create_auto_inputs)
        self._create_vehicle_tab("Camión", self._create_camion_inputs)
        self._create_vehicle_tab("Motocicleta", self._create_motocicleta_inputs)
        self._create_vehicle_tab("Autobús", self._create_autobus_inputs)
        self._create_vehicle_tab("Bicicleta", self._create_bicicleta_inputs)

        # --- Frame de Visualización de Vehículos (Treeview) ---
        display_frame = ttk.LabelFrame(main_frame, text="Vehículos Registrados", padding="10 10 10 10")
        display_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
        display_frame.grid_columnconfigure(0, weight=1)
        display_frame.grid_rowconfigure(0, weight=1)

        # Treeview para mostrar los vehículos, con nuevas columnas
        self.vehicles_tree = ttk.Treeview(display_frame, 
                                          columns=("Tipo", "Marca", "Modelo", "Año", "Consumo/km", "Coste/km", "Registrador", "Notario"), 
                                          show="headings")
        self.vehicles_tree.heading("Tipo", text="Tipo")
        self.vehicles_tree.heading("Marca", text="Marca")
        self.vehicles_tree.heading("Modelo", text="Modelo")
        self.vehicles_tree.heading("Año", text="Año")
        self.vehicles_tree.heading("Consumo/km", text="Consumo/km (L/kWh)")
        self.vehicles_tree.heading("Coste/km", text="Coste/km (S/.)")
        self.vehicles_tree.heading("Registrador", text="Registrador") # Nueva columna
        self.vehicles_tree.heading("Notario", text="Notario")       # Nueva columna

        self.vehicles_tree.column("Tipo", width=90, anchor="center")
        self.vehicles_tree.column("Marca", width=90, anchor="w")
        self.vehicles_tree.column("Modelo", width=100, anchor="w")
        self.vehicles_tree.column("Año", width=60, anchor="center")
        self.vehicles_tree.column("Consumo/km", width=120, anchor="center")
        self.vehicles_tree.column("Coste/km", width=120, anchor="center")
        self.vehicles_tree.column("Registrador", width=120, anchor="w") # Ancho para la nueva columna
        self.vehicles_tree.column("Notario", width=120, anchor="w")     # Ancho para la nueva columna

        self.vehicles_tree.grid(row=0, column=0, sticky="nsew")

        # Scrollbar para el Treeview
        scrollbar = ttk.Scrollbar(display_frame, orient=tk.VERTICAL, command=self.vehicles_tree.yview)
        self.vehicles_tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.grid(row=0, column=1, sticky="ns")

        # --- Frame de Control Inferior (Precio Combustible y Salir) ---
        control_bottom_frame = ttk.Frame(main_frame, padding="10 0 0 0")
        control_bottom_frame.grid(row=2, column=0, padx=10, pady=10, sticky="ew")
        control_bottom_frame.grid_columnconfigure(0, weight=1) # Para centrar elementos

        # Entrada para el precio del combustible
        price_frame = ttk.Frame(control_bottom_frame)
        price_frame.pack(pady=5)
        ttk.Label(price_frame, text="Precio Combustible por L/kWh (S/.):").pack(side=tk.LEFT, padx=5)
        self.precio_combustible_entry = ttk.Entry(price_frame, width=15)
        self.precio_combustible_entry.insert(0, "0.0") # Valor inicial
        self.precio_combustible_entry.pack(side=tk.LEFT, padx=5)
        self.update_price_button = ttk.Button(price_frame, text="Actualizar Costes", command=self.update_price_and_display)
        self.update_price_button.pack(side=tk.LEFT, padx=5)

        self.status_label = ttk.Label(control_bottom_frame, text="Listo para registrar vehículos.", font=("Arial", 10, "italic"), foreground="blue")
        self.status_label.pack(pady=5)
        
        self.exit_button = ttk.Button(control_bottom_frame, text="Salir del Sistema", command=self.master.quit)
        self.exit_button.pack(pady=5)

        # Inicializar la visualización de vehículos
        self.update_vehicles_display()

    def _create_vehicle_tab(self, tab_name: str, create_inputs_func):
        """Crea una pestaña en el Notebook para un tipo de vehículo."""
        tab = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(tab, text=tab_name)
        create_inputs_func(tab)
        tab.grid_columnconfigure(1, weight=1) # Permitir que las entradas se expandan

    # --- Métodos para crear inputs en las pestañas ---
    def _create_common_inputs(self, parent_frame: ttk.Frame, start_row: int) -> dict:
        """Crea los campos de entrada comunes a la mayoría de los vehículos, incluyendo registrador y notario."""
        inputs = {}
        # Campos existentes
        ttk.Label(parent_frame, text="Marca:").grid(row=start_row, column=0, padx=5, pady=5, sticky="w")
        inputs['marca'] = ttk.Entry(parent_frame, width=30)
        inputs['marca'].grid(row=start_row, column=1, padx=5, pady=5, sticky="ew")

        ttk.Label(parent_frame, text="Modelo:").grid(row=start_row + 1, column=0, padx=5, pady=5, sticky="w")
        inputs['modelo'] = ttk.Entry(parent_frame, width=30)
        inputs['modelo'].grid(row=start_row + 1, column=1, padx=5, pady=5, sticky="ew")

        ttk.Label(parent_frame, text="Año:").grid(row=start_row + 2, column=0, padx=5, pady=5, sticky="w")
        inputs['anio'] = ttk.Entry(parent_frame, width=30)
        inputs['anio'].grid(row=start_row + 2, column=1, padx=5, pady=5, sticky="ew")

        # Nuevos campos para Registrador y Notario
        ttk.Label(parent_frame, text="Nombre del Registrador:").grid(row=start_row + 3, column=0, padx=5, pady=5, sticky="w")
        inputs['registrador'] = ttk.Entry(parent_frame, width=30)
        inputs['registrador'].grid(row=start_row + 3, column=1, padx=5, pady=5, sticky="ew")

        ttk.Label(parent_frame, text="Nombre del Notario (Opcional):").grid(row=start_row + 4, column=0, padx=5, pady=5, sticky="w")
        inputs['notario'] = ttk.Entry(parent_frame, width=30)
        inputs['notario'].grid(row=start_row + 4, column=1, padx=5, pady=5, sticky="ew")

        return inputs

    def _create_consumo_input(self, parent_frame: ttk.Frame, row: int) -> ttk.Entry:
        """Crea el campo de entrada para el consumo."""
        ttk.Label(parent_frame, text="Consumo (L/kWh por 100 km):").grid(row=row, column=0, padx=5, pady=5, sticky="w")
        consumo_entry = ttk.Entry(parent_frame, width=30)
        consumo_entry.grid(row=row, column=1, padx=5, pady=5, sticky="ew")
        return consumo_entry

    def _create_auto_inputs(self, parent_frame: ttk.Frame) -> None:
        self.auto_inputs = self._create_common_inputs(parent_frame, 0)
        # El campo de consumo se añade después de los comunes
        self.auto_inputs['consumo'] = self._create_consumo_input(parent_frame, 5) # Ajustar la fila
        ttk.Button(parent_frame, text="Registrar Auto", command=self.add_auto).grid(row=6, column=0, columnspan=2, pady=10) # Ajustar la fila del botón

    def _create_camion_inputs(self, parent_frame: ttk.Frame) -> None:
        self.camion_inputs = self._create_common_inputs(parent_frame, 0)
        self.camion_inputs['consumo'] = self._create_consumo_input(parent_frame, 5) # Ajustar la fila
        ttk.Button(parent_frame, text="Registrar Camión", command=self.add_camion).grid(row=6, column=0, columnspan=2, pady=10) # Ajustar la fila del botón

    def _create_motocicleta_inputs(self, parent_frame: ttk.Frame) -> None:
        self.moto_inputs = self._create_common_inputs(parent_frame, 0)
        self.moto_inputs['consumo'] = self._create_consumo_input(parent_frame, 5) # Ajustar la fila
        ttk.Button(parent_frame, text="Registrar Motocicleta", command=self.add_motocicleta).grid(row=6, column=0, columnspan=2, pady=10) # Ajustar la fila del botón

    def _create_autobus_inputs(self, parent_frame: ttk.Frame) -> None:
        self.autobus_inputs = self._create_common_inputs(parent_frame, 0)
        self.autobus_inputs['consumo'] = self._create_consumo_input(parent_frame, 5) # Ajustar la fila
        ttk.Button(parent_frame, text="Registrar Autobús", command=self.add_autobus).grid(row=6, column=0, columnspan=2, pady=10) # Ajustar la fila del botón

    def _create_bicicleta_inputs(self, parent_frame: ttk.Frame) -> None:
        self.bici_inputs = self._create_common_inputs(parent_frame, 0)
        # Bicicleta no tiene consumo de combustible, el botón va en una fila anterior
        ttk.Button(parent_frame, text="Registrar Bicicleta", command=self.add_bicicleta).grid(row=5, column=0, columnspan=2, pady=10) # Ajustar la fila del botón


    def _show_status_message(self, message: str, is_error: bool = False) -> None:
        """Muestra un mensaje en la barra de estado."""
        self.status_label.config(text=message, foreground="red" if is_error else "blue")
        self.master.after(3000, lambda: self.status_label.config(text="")) # Limpiar después de 3s

    def _get_common_vehicle_data(self, inputs: dict, has_consumo: bool = True) -> tuple:
        """Helper para obtener y validar datos comunes de vehículo, incluyendo registrador y notario."""
        marca = inputs['marca'].get().strip()
        modelo = inputs['modelo'].get().strip()
        anio_str = inputs['anio'].get().strip()
        
        # Nuevos campos
        registrador = inputs['registrador'].get().strip()
        notario = inputs['notario'].get().strip()

        consumo_str = inputs['consumo'].get().strip() if has_consumo else "0.0" # Default para bici

        if not marca or not modelo or not anio_str:
            raise ValueError("Marca, Modelo y Año no pueden estar vacíos.")
        
        try:
            anio = int(anio_str)
            if anio <= 1900 or anio > 2100: # Rango razonable
                raise ValueError("Año inválido.")
        except ValueError:
            raise ValueError("Año debe ser un número entero válido.")
        
        consumo = 0.0
        if has_consumo:
            try:
                consumo = float(consumo_str)
                if consumo < 0:
                    raise ValueError("Consumo no puede ser negativo.")
            except ValueError:
                raise ValueError("Consumo debe ser un número válido.")
        
        # Retornar todos los datos, incluyendo registrador y notario
        return marca, modelo, anio, consumo, registrador if registrador else "N/A", notario if notario else "N/A"

    def add_auto(self) -> None:
        try:
            marca, modelo, anio, consumo, registrador, notario = self._get_common_vehicle_data(self.auto_inputs)
            self.vehiculos_list.append(Auto(marca, modelo, anio, consumo, registrador, notario))
            self.update_vehicles_display()
            self._show_status_message("✔ Auto registrado correctamente.")
            self._clear_inputs(self.auto_inputs)
        except ValueError as e:
            self._show_status_message(f"✖ Error al registrar auto: {e}", is_error=True)

    def add_camion(self) -> None:
        try:
            marca, modelo, anio, consumo, registrador, notario = self._get_common_vehicle_data(self.camion_inputs)
            self.vehiculos_list.append(Camion(marca, modelo, anio, consumo, registrador, notario))
            self.update_vehicles_display()
            self._show_status_message("✔ Camión registrado correctamente.")
            self._clear_inputs(self.camion_inputs)
        except ValueError as e:
            self._show_status_message(f"✖ Error al registrar camión: {e}", is_error=True)

    def add_motocicleta(self) -> None:
        try:
            marca, modelo, anio, consumo, registrador, notario = self._get_common_vehicle_data(self.moto_inputs)
            self.vehiculos_list.append(Motocicleta(marca, modelo, anio, consumo, registrador, notario))
            self.update_vehicles_display()
            self._show_status_message("✔ Motocicleta registrada correctamente.")
            self._clear_inputs(self.moto_inputs)
        except ValueError as e:
            self._show_status_message(f"✖ Error al registrar motocicleta: {e}", is_error=True)

    def add_autobus(self) -> None:
        try:
            marca, modelo, anio, consumo, registrador, notario = self._get_common_vehicle_data(self.autobus_inputs)
            self.vehiculos_list.append(Autobus(marca, modelo, anio, consumo, registrador, notario))
            self.update_vehicles_display()
            self._show_status_message("✔ Autobús registrado correctamente.")
            self._clear_inputs(self.autobus_inputs)
        except ValueError as e:
            self._show_status_message(f"✖ Error al registrar autobús: {e}", is_error=True)

    def add_bicicleta(self) -> None:
        try:
            marca, modelo, anio, _, registrador, notario = self._get_common_vehicle_data(self.bici_inputs, has_consumo=False)
            self.vehiculos_list.append(Bicicleta(marca, modelo, anio, registrador, notario))
            self.update_vehicles_display()
            self._show_status_message("✔ Bicicleta registrada correctamente.")
            self._clear_inputs(self.bici_inputs)
        except ValueError as e:
            self._show_status_message(f"✖ Error al registrar bicicleta: {e}", is_error=True)

    def _clear_inputs(self, inputs: dict) -> None:
        """Limpia los campos de entrada de un conjunto de widgets."""
        for entry in inputs.values():
            if isinstance(entry, ttk.Entry):
                entry.delete(0, tk.END)

    def update_price_and_display(self) -> None:
        """Actualiza el precio del combustible y refresca la visualización de vehículos."""
        try:
            new_price_str = self.precio_combustible_entry.get().strip()
            if not new_price_str:
                raise ValueError("El precio del combustible no puede estar vacío.")
            new_price = float(new_price_str)
            if new_price < 0:
                raise ValueError("El precio del combustible no puede ser negativo.")
            self.precio_combustible = new_price
            self.update_vehicles_display()
            self._show_status_message(f"Precio del combustible actualizado a S/. {self.precio_combustible:.2f}.")
        except ValueError as e:
            self._show_status_message(f"✖ Error en el precio del combustible: {e}", is_error=True)

    def update_vehicles_display(self) -> None:
        """Actualiza el Treeview con la lista actual de vehículos."""
        # Limpiar el Treeview existente
        for item in self.vehicles_tree.get_children():
            self.vehicles_tree.delete(item)

        if not self.vehiculos_list:
            # Asegurarse de que el número de valores coincida con el número de columnas
            self.vehicles_tree.insert("", tk.END, values=("No hay vehículos registrados", "", "", "", "", "", "", ""))
            return

        # Insertar los vehículos actualizados
        for vehiculo in self.vehiculos_list:
            self.vehicles_tree.insert("", tk.END, values=vehiculo.get_info_for_display(self.precio_combustible))

# ────────────────────
# Punto de entrada de la aplicación
# ────────────────────
if __name__ == "__main__":
    root = tk.Tk()
    app = VehiculosApp(root)
    root.mainloop()