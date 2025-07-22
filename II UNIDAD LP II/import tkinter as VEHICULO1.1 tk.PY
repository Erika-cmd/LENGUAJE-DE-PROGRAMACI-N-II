import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

# ────────────────────
# Clase base (superclase)
# ────────────────────
class Vehiculo:
    def __init__(self, nombre: str, marca: str, modelo: str, anio: int) -> None:
        # Encapsulamiento: Atributos privados
        self.__nombre = nombre
        self.__marca = marca
        self.__modelo = modelo
        self.__anio = anio

    # Getters para acceder a los atributos encapsulados
    def get_nombre(self) -> str:
        return self.__nombre

    def get_marca(self) -> str:
        return self.__marca

    def get_modelo(self) -> str:
        return self.__modelo

    def get_anio(self) -> int:
        return self.__anio

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
        # Formato para el Treeview
        return (
            self.get_nombre(),
            self.get_marca(),
            self.get_modelo(),
            self.get_anio(),
            f"{self.consumo_por_km():.3f}",
            f"S/. {self.coste_por_km(precio_combustible):.2f}"
        )
    
    def draw_graph(self, ax: plt.Axes, precio_combustible: float):
        """
        Método abstracto para dibujar un gráfico relacionado con el vehículo en un objeto Axes de Matplotlib.
        Debe ser implementado por las subclases.
        """
        raise NotImplementedError("El método draw_graph debe ser implementado por las subclases.")


# ────────────────────
# Subclase: Auto
# ────────────────────
class Auto(Vehiculo):
    def __init__(self, marca: str, modelo: str, anio: int, consumo_l100: float) -> None:
        super().__init__("Auto", marca, modelo, anio)
        # Convertir consumo de L/100km a L/km
        self.__consumo = consumo_l100 / 100

    # Polimorfismo: Implementación específica del consumo
    def consumo_por_km(self) -> float:
        return self.__consumo

    def draw_graph(self, ax: plt.Axes, precio_combustible: float):
        consumo = self.consumo_por_km()
        coste = self.coste_por_km(precio_combustible)
        
        labels = ['Consumo (L/km)', 'Coste (S/./km)']
        values = [consumo, coste]
        colors = ['#4CAF50', '#FFC107'] # Verde para consumo, Naranja para coste

        ax.bar(labels, values, color=colors)
        ax.set_title(f"Detalles de {self.get_nombre()}: {self.get_marca()} {self.get_modelo()}")
        ax.set_ylabel("Valor")
        ax.set_ylim(0, max(values) * 1.2 if max(values) > 0 else 0.1) # Ajustar límite Y
        ax.grid(axis='y', linestyle='--', alpha=0.7)
        for i, v in enumerate(values):
            ax.text(i, v + (max(values) * 0.05 if max(values) > 0 else 0.01), f"{v:.3f}", ha='center', va='bottom')


# ────────────────────
# Subclase: Camion
# ────────────────────
class Camion(Vehiculo):
    def __init__(self, marca: str, modelo: str, anio: int, consumo_l100: float) -> None:
        super().__init__("Camión", marca, modelo, anio)
        self.__consumo = consumo_l100 / 100

    # Polimorfismo: Implementación específica del consumo
    def consumo_por_km(self) -> float:
        return self.__consumo

    def draw_graph(self, ax: plt.Axes, precio_combustible: float):
        consumo = self.consumo_por_km()
        coste = self.coste_por_km(precio_combustible)
        
        labels = ['Consumo (L/km)', 'Coste (S/./km)']
        values = [consumo, coste]
        colors = ['#2196F3', '#FF5722'] # Azul para consumo, Rojo para coste

        ax.bar(labels, values, color=colors)
        ax.set_title(f"Detalles de {self.get_nombre()}: {self.get_marca()} {self.get_modelo()}")
        ax.set_ylabel("Valor")
        ax.set_ylim(0, max(values) * 1.2 if max(values) > 0 else 0.1)
        ax.grid(axis='y', linestyle='--', alpha=0.7)
        for i, v in enumerate(values):
            ax.text(i, v + (max(values) * 0.05 if max(values) > 0 else 0.01), f"{v:.3f}", ha='center', va='bottom')

# ────────────────────
# Subclase: Motocicleta
# ────────────────────
class Motocicleta(Vehiculo):
    def __init__(self, marca: str, modelo: str, anio: int, consumo_l100: float) -> None:
        super().__init__("Motocicleta", marca, modelo, anio)
        self.__consumo = consumo_l100 / 100

    # Polimorfismo: Implementación específica del consumo
    def consumo_por_km(self) -> float:
        return self.__consumo

    def draw_graph(self, ax: plt.Axes, precio_combustible: float):
        consumo = self.consumo_por_km()
        coste = self.coste_por_km(precio_combustible)
        
        labels = ['Consumo (L/km)', 'Coste (S/./km)']
        values = [consumo, coste]
        colors = ['#9C27B0', '#FFEB3B'] # Morado para consumo, Amarillo para coste

        ax.bar(labels, values, color=colors)
        ax.set_title(f"Detalles de {self.get_nombre()}: {self.get_marca()} {self.get_modelo()}")
        ax.set_ylabel("Valor")
        ax.set_ylim(0, max(values) * 1.2 if max(values) > 0 else 0.1)
        ax.grid(axis='y', linestyle='--', alpha=0.7)
        for i, v in enumerate(values):
            ax.text(i, v + (max(values) * 0.05 if max(values) > 0 else 0.01), f"{v:.3f}", ha='center', va='bottom')

# ────────────────────
# Subclase: Autobus
# ────────────────────
class Autobus(Vehiculo):
    def __init__(self, marca: str, modelo: str, anio: int, consumo_l100: float) -> None:
        super().__init__("Autobús", marca, modelo, anio)
        self.__consumo = consumo_l100 / 100

    # Polimorfismo: Implementación específica del consumo
    def consumo_por_km(self) -> float:
        return self.__consumo

    def draw_graph(self, ax: plt.Axes, precio_combustible: float):
        consumo = self.consumo_por_km()
        coste = self.coste_por_km(precio_combustible)
        
        labels = ['Consumo (L/km)', 'Coste (S/./km)']
        values = [consumo, coste]
        colors = ['#00BCD4', '#FF9800'] # Cian para consumo, Naranja oscuro para coste

        ax.bar(labels, values, color=colors)
        ax.set_title(f"Detalles de {self.get_nombre()}: {self.get_marca()} {self.get_modelo()}")
        ax.set_ylabel("Valor")
        ax.set_ylim(0, max(values) * 1.2 if max(values) > 0 else 0.1)
        ax.grid(axis='y', linestyle='--', alpha=0.7)
        for i, v in enumerate(values):
            ax.text(i, v + (max(values) * 0.05 if max(values) > 0 else 0.01), f"{v:.3f}", ha='center', va='bottom')

# ────────────────────
# Subclase: Bicicleta
# ────────────────────
class Bicicleta(Vehiculo):
    def __init__(self, marca: str, modelo: str, anio: int) -> None:
        super().__init__("Bicicleta", marca, modelo, anio)

    # Polimorfismo: Consumo de 0 para bicicleta
    def consumo_por_km(self) -> float:
        return 0.0

    def draw_graph(self, ax: plt.Axes, precio_combustible: float):
        # Para bicicleta, el consumo es 0, así que el gráfico será diferente o indicará esto.
        # Podríamos mostrar un mensaje o un gráfico simbólico.
        ax.text(0.5, 0.5, "¡No consume combustible!\n(Consumo: 0 L/km, Coste: S/. 0.00/km)",
                horizontalalignment='center', verticalalignment='center',
                transform=ax.transAxes, fontsize=12, color='green')
        ax.set_title(f"Detalles de {self.get_nombre()}: {self.get_marca()} {self.get_modelo()}")
        ax.set_xticks([]) # Ocultar ticks del eje x
        ax.set_yticks([]) # Ocultar ticks del eje y
        ax.set_frame_on(False) # Ocultar el marco del gráfico

# ────────────────────
# Aplicación Tkinter
# ────────────────────
class VehiculosApp:
    def __init__(self, master: tk.Tk) -> None:
        self.master = master
        master.title("Sistema de Gestión de Vehículos")
        master.geometry("1400x800") # Aumentar tamaño para incluir el gráfico
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
        main_frame.grid_columnconfigure(0, weight=1) # Columna para el notebook
        main_frame.grid_columnconfigure(1, weight=1) # Columna para el gráfico
        main_frame.grid_rowconfigure(1, weight=1) # Fila para el Treeview
        main_frame.grid_rowconfigure(2, weight=1) # Fila para el Treeview (si se extiende)

        # --- Notebook para las pestañas de registro de vehículos ---
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        
        # Crear pestañas para cada tipo de vehículo
        self._create_vehicle_tab("Auto", self._create_auto_inputs)
        self._create_vehicle_tab("Camión", self._create_camion_inputs)
        self._create_vehicle_tab("Motocicleta", self._create_motocicleta_inputs)
        self._create_vehicle_tab("Autobús", self._create_autobus_inputs)
        self._create_vehicle_tab("Bicicleta", self._create_bicicleta_inputs)

        # --- Frame de Gráfica de Matplotlib ---
        self.plot_frame = ttk.LabelFrame(main_frame, text="Gráfica del Vehículo", padding="10 10 10 10")
        self.plot_frame.grid(row=0, column=1, rowspan=2, padx=10, pady=10, sticky="nsew") # Ocupa 2 filas
        self.plot_frame.grid_columnconfigure(0, weight=1)
        self.plot_frame.grid_rowconfigure(0, weight=1)

        # Configurar la figura y los ejes de Matplotlib
        self.fig, self.ax = plt.subplots(figsize=(5, 4), dpi=100)
        self.canvas_matplotlib = FigureCanvasTkAgg(self.fig, master=self.plot_frame)
        self.canvas_matplotlib_widget = self.canvas_matplotlib.get_tk_widget()
        self.canvas_matplotlib_widget.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # Barra de herramientas de Matplotlib (opcional, pero útil para zoom/pan)
        self.toolbar = NavigationToolbar2Tk(self.canvas_matplotlib, self.plot_frame)
        self.toolbar.update()
        self.canvas_matplotlib_widget.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # --- Frame de Visualización de Vehículos (Treeview) ---
        display_frame = ttk.LabelFrame(main_frame, text="Vehículos Registrados", padding="10 10 10 10")
        display_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew") # Ahora en row 1, column 0
        display_frame.grid_columnconfigure(0, weight=1)
        display_frame.grid_rowconfigure(0, weight=1)

        # Treeview para mostrar los vehículos
        self.vehicles_tree = ttk.Treeview(display_frame, 
                                          columns=("Tipo", "Marca", "Modelo", "Año", "Consumo/km", "Coste/km"), 
                                          show="headings")
        self.vehicles_tree.heading("Tipo", text="Tipo")
        self.vehicles_tree.heading("Marca", text="Marca")
        self.vehicles_tree.heading("Modelo", text="Modelo")
        self.vehicles_tree.heading("Año", text="Año")
        self.vehicles_tree.heading("Consumo/km", text="Consumo/km (L/kWh)")
        self.vehicles_tree.heading("Coste/km", text="Coste/km (S/.)")

        self.vehicles_tree.column("Tipo", width=90, anchor="center")
        self.vehicles_tree.column("Marca", width=90, anchor="w")
        self.vehicles_tree.column("Modelo", width=100, anchor="w")
        self.vehicles_tree.column("Año", width=60, anchor="center")
        self.vehicles_tree.column("Consumo/km", width=120, anchor="center")
        self.vehicles_tree.column("Coste/km", width=120, anchor="center")

        self.vehicles_tree.grid(row=0, column=0, sticky="nsew")

        # Scrollbar para el Treeview
        scrollbar = ttk.Scrollbar(display_frame, orient=tk.VERTICAL, command=self.vehicles_tree.yview)
        self.vehicles_tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.grid(row=0, column=1, sticky="ns")

        # Vincular la selección del Treeview a la función de dibujo
        self.vehicles_tree.bind("<<TreeviewSelect>>", self.on_vehicle_select)


        # --- Frame de Control Inferior (Precio Combustible y Salir) ---
        control_bottom_frame = ttk.Frame(main_frame, padding="10 0 0 0")
        control_bottom_frame.grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky="ew") # Ahora en row 2, columnspan 2
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
        self.clear_plot() # Limpiar el plot al inicio

    def _create_vehicle_tab(self, tab_name: str, create_inputs_func):
        """Crea una pestaña en el Notebook para un tipo de vehículo."""
        tab = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(tab, text=tab_name)
        create_inputs_func(tab)
        tab.grid_columnconfigure(1, weight=1) # Permitir que las entradas se expandan

    # --- Métodos para crear inputs en las pestañas ---
    def _create_common_inputs(self, parent_frame: ttk.Frame, start_row: int) -> dict:
        """Crea los campos de entrada comunes a la mayoría de los vehículos."""
        inputs = {}
        ttk.Label(parent_frame, text="Marca:").grid(row=start_row, column=0, padx=5, pady=5, sticky="w")
        inputs['marca'] = ttk.Entry(parent_frame, width=30)
        inputs['marca'].grid(row=start_row, column=1, padx=5, pady=5, sticky="ew")

        ttk.Label(parent_frame, text="Modelo:").grid(row=start_row + 1, column=0, padx=5, pady=5, sticky="w")
        inputs['modelo'] = ttk.Entry(parent_frame, width=30)
        inputs['modelo'].grid(row=start_row + 1, column=1, padx=5, pady=5, sticky="ew")

        ttk.Label(parent_frame, text="Año:").grid(row=start_row + 2, column=0, padx=5, pady=5, sticky="w")
        inputs['anio'] = ttk.Entry(parent_frame, width=30)
        inputs['anio'].grid(row=start_row + 2, column=1, padx=5, pady=5, sticky="ew")
        return inputs

    def _create_consumo_input(self, parent_frame: ttk.Frame, row: int) -> ttk.Entry:
        """Crea el campo de entrada para el consumo."""
        ttk.Label(parent_frame, text="Consumo (L/kWh por 100 km):").grid(row=row, column=0, padx=5, pady=5, sticky="w")
        consumo_entry = ttk.Entry(parent_frame, width=30)
        consumo_entry.grid(row=row, column=1, padx=5, pady=5, sticky="ew")
        return consumo_entry

    def _create_auto_inputs(self, parent_frame: ttk.Frame) -> None:
        self.auto_inputs = self._create_common_inputs(parent_frame, 0)
        self.auto_inputs['consumo'] = self._create_consumo_input(parent_frame, 3)
        ttk.Button(parent_frame, text="Registrar Auto", command=self.add_auto).grid(row=4, column=0, columnspan=2, pady=10)

    def _create_camion_inputs(self, parent_frame: ttk.Frame) -> None:
        self.camion_inputs = self._create_common_inputs(parent_frame, 0)
        self.camion_inputs['consumo'] = self._create_consumo_input(parent_frame, 3)
        ttk.Button(parent_frame, text="Registrar Camión", command=self.add_camion).grid(row=4, column=0, columnspan=2, pady=10)

    def _create_motocicleta_inputs(self, parent_frame: ttk.Frame) -> None:
        self.moto_inputs = self._create_common_inputs(parent_frame, 0)
        self.moto_inputs['consumo'] = self._create_consumo_input(parent_frame, 3)
        ttk.Button(parent_frame, text="Registrar Motocicleta", command=self.add_motocicleta).grid(row=4, column=0, columnspan=2, pady=10)

    def _create_autobus_inputs(self, parent_frame: ttk.Frame) -> None:
        self.autobus_inputs = self._create_common_inputs(parent_frame, 0)
        self.autobus_inputs['consumo'] = self._create_consumo_input(parent_frame, 3)
        ttk.Button(parent_frame, text="Registrar Autobús", command=self.add_autobus).grid(row=4, column=0, columnspan=2, pady=10)

    def _create_bicicleta_inputs(self, parent_frame: ttk.Frame) -> None:
        self.bici_inputs = self._create_common_inputs(parent_frame, 0)
        # Bicicleta no tiene consumo de combustible, no se añade campo de consumo
        ttk.Button(parent_frame, text="Registrar Bicicleta", command=self.add_bicicleta).grid(row=3, column=0, columnspan=2, pady=10)


    def _show_status_message(self, message: str, is_error: bool = False) -> None:
        """Muestra un mensaje en la barra de estado."""
        self.status_label.config(text=message, foreground="red" if is_error else "blue")
        self.master.after(3000, lambda: self.status_label.config(text="")) # Limpiar después de 3s

    def _get_common_vehicle_data(self, inputs: dict, has_consumo: bool = True) -> tuple:
        """Helper para obtener y validar datos comunes de vehículo."""
        marca = inputs['marca'].get().strip()
        modelo = inputs['modelo'].get().strip()
        anio_str = inputs['anio'].get().strip()
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
        
        return marca, modelo, anio, consumo

    def add_auto(self) -> None:
        try:
            marca, modelo, anio, consumo = self._get_common_vehicle_data(self.auto_inputs)
            self.vehiculos_list.append(Auto(marca, modelo, anio, consumo))
            self.update_vehicles_display()
            self._show_status_message("✔ Auto registrado correctamente.")
            self._clear_inputs(self.auto_inputs)
        except ValueError as e:
            self._show_status_message(f"✖ Error al registrar auto: {e}", is_error=True)

    def add_camion(self) -> None:
        try:
            marca, modelo, anio, consumo = self._get_common_vehicle_data(self.camion_inputs)
            self.vehiculos_list.append(Camion(marca, modelo, anio, consumo))
            self.update_vehicles_display()
            self._show_status_message("✔ Camión registrado correctamente.")
            self._clear_inputs(self.camion_inputs)
        except ValueError as e:
            self._show_status_message(f"✖ Error al registrar camión: {e}", is_error=True)

    def add_motocicleta(self) -> None:
        try:
            marca, modelo, anio, consumo = self._get_common_vehicle_data(self.moto_inputs)
            self.vehiculos_list.append(Motocicleta(marca, modelo, anio, consumo))
            self.update_vehicles_display()
            self._show_status_message("✔ Motocicleta registrada correctamente.")
            self._clear_inputs(self.moto_inputs)
        except ValueError as e:
            self._show_status_message(f"✖ Error al registrar motocicleta: {e}", is_error=True)

    def add_autobus(self) -> None:
        try:
            marca, modelo, anio, consumo = self._get_common_vehicle_data(self.autobus_inputs)
            self.vehiculos_list.append(Autobus(marca, modelo, anio, consumo))
            self.update_vehicles_display()
            self._show_status_message("✔ Autobús registrado correctamente.")
            self._clear_inputs(self.autobus_inputs)
        except ValueError as e:
            self._show_status_message(f"✖ Error al registrar autobús: {e}", is_error=True)

    def add_bicicleta(self) -> None:
        try:
            marca, modelo, anio, _ = self._get_common_vehicle_data(self.bici_inputs, has_consumo=False)
            self.vehiculos_list.append(Bicicleta(marca, modelo, anio))
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
            # Después de actualizar el precio, si hay un vehículo seleccionado, actualiza su gráfica
            self.on_vehicle_select(None) 
        except ValueError as e:
            self._show_status_message(f"✖ Error en el precio del combustible: {e}", is_error=True)

    def update_vehicles_display(self) -> None:
        """Actualiza el Treeview con la lista actual de vehículos."""
        # Limpiar el Treeview existente
        for item in self.vehicles_tree.get_children():
            self.vehicles_tree.delete(item)

        if not self.vehiculos_list:
            self.vehicles_tree.insert("", tk.END, values=("No hay vehículos registrados", "", "", "", "", ""))
            return

        # Insertar los vehículos actualizados
        for vehiculo in self.vehiculos_list:
            self.vehicles_tree.insert("", tk.END, values=vehiculo.get_info_for_display(self.precio_combustible))
        
        # Si hay vehículos, seleccionar el primero por defecto para mostrar su gráfica
        if self.vehiculos_list:
            first_item_id = self.vehicles_tree.get_children()[0]
            self.vehicles_tree.selection_set(first_item_id)
            self.vehicles_tree.focus(first_item_id)
            self.on_vehicle_select(None) # Forzar la actualización de la gráfica

    def on_vehicle_select(self, event):
        """Maneja la selección de un vehículo en el Treeview para mostrar su gráfica."""
        selected_item = self.vehicles_tree.focus()
        if not selected_item:
            self.clear_plot()
            return

        # Obtener el índice del vehículo seleccionado en la lista
        item_index = self.vehicles_tree.index(selected_item)
        if item_index < 0 or item_index >= len(self.vehiculos_list):
            self.clear_plot()
            return

        selected_vehicle = self.vehiculos_list[item_index]
        self.draw_vehicle_plot(selected_vehicle)

    def clear_plot(self):
        """Limpia los ejes de Matplotlib y redibuja."""
        self.ax.clear()
        self.ax.set_title("Selecciona un vehículo para ver su gráfica")
        self.ax.set_xticks([]) # Ocultar ticks del eje x por defecto
        self.ax.set_yticks([]) # Ocultar ticks del eje y por defecto
        self.ax.grid(True)
        self.canvas_matplotlib.draw_idle()

    def draw_vehicle_plot(self, vehicle: Vehiculo):
        """Dibuja el gráfico del vehículo dado en los ejes de Matplotlib."""
        self.ax.clear() # Limpiar el plot anterior
        try:
            # Pasa el precio del combustible para que el gráfico pueda calcular el coste
            vehicle.draw_graph(self.ax, self.precio_combustible) 
        except NotImplementedError:
            self.ax.text(0.5, 0.5, "Gráfica no disponible para este vehículo.",
                         horizontalalignment='center', verticalalignment='center',
                         transform=self.ax.transAxes, fontsize=12, color='gray')
            self.ax.set_title(f"Gráfica de {vehicle.get_nombre()}")
        except Exception as e:
            self.ax.text(0.5, 0.5, f"Error al dibujar: {e}",
                         horizontalalignment='center', verticalalignment='center',
                         transform=self.ax.transAxes, fontsize=10, color='red')
            self.ax.set_title(f"Error en gráfica de {vehicle.get_nombre()}")
        
        self.canvas_matplotlib.draw_idle() # Redibujar el canvas

# ────────────────────
# Punto de entrada de la aplicación
# ────────────────────
if __name__ == "__main__":
    root = tk.Tk()
    app = VehiculosApp(root)
    root.mainloop()
