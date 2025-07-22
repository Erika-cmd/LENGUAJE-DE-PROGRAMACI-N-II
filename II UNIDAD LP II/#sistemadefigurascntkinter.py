import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import pandas as pd # Necesario para leer CSV
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import numpy as np # Para simulación de datos
from lifelines import KaplanMeierFitter, CoxPHFitter # Para Kaplan-Meier y Cox

class SurvivalAnalysisApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Software Educativo - Análisis de Supervivencia")
        self.geometry("1400x850") # Tamaño más grande para acomodar todo
        self.minsize(1000, 700) # Tamaño mínimo
        self.configure(bg="#EBF5FB") # Fondo principal

        self._configure_styles()
        self._create_widgets()

        # Atributos para la simulación
        self.sim_fig = None
        self.sim_ax = None
        self.sim_canvas_widget = None
        self.sim_toolbar = None

        # Atributos para la carga de CSV y análisis
        self.csv_data_frame = None # Para almacenar el DataFrame del CSV cargado
        self.analysis_fig = None
        self.analysis_ax = None
        self.analysis_canvas_widget = None
        self.analysis_toolbar = None

        # Atributos para la Regresión de Cox
        self.cox_fig = None
        self.cox_ax = None # Aunque Cox no siempre tiene un plot directo, se puede reservar
        self.cox_canvas_widget = None
        self.cox_toolbar = None


    def _configure_styles(self):
        """Configura los estilos para los widgets ttk."""
        style = ttk.Style(self)
        style.theme_use('clam') # Un tema moderno y limpio

        style.configure("TFrame", background="#EBF5FB")
        style.configure("TLabel", background="#EBF5FB", foreground="#2C3E50")

        # Estilos para el encabezado
        style.configure("Header.TFrame", background="#4A90E2", borderwidth=0, relief="flat")
        style.configure("HeaderTitle.TLabel", background="#4A90E2", foreground="white",
                        font=("Helvetica Neue", 28, "bold"))
        style.configure("HeaderSubtitle.TLabel", background="#4A90E2", foreground="white",
                         font=("Helvetica Neue", 20))

        # Estilos para los botones de navegación (ahora serán pestañas)
        style.configure("TNotebook", background="#EBF5FB", borderwidth=0)
        style.configure("TNotebook.Tab", background="#ADD8E6", foreground="#2C3E50",
                        font=("Helvetica Neue", 12, "bold"), padding=[15, 8]) # Más padding para tabs
        style.map("TNotebook.Tab",
                  background=[('selected', '#4A90E2'), ('active', '#85C1E9')],
                  foreground=[('selected', 'white'), ('active', '#2C3E50')])
        
        # Estilo para los botones dentro de las pestañas
        style.configure("Tab.TButton",
                        font=("Helvetica Neue", 11, "bold"),
                        padding=12, # Más padding para botones
                        background="#5DADE2",
                        foreground="white",
                        relief="flat",
                        borderwidth=0)
        style.map("Tab.TButton",
                  background=[('active', '#85C1E9')],
                  foreground=[('active', 'white')])

        # Estilo para el pie de página
        style.configure("Footer.TLabel", background="#EBF5FB", foreground="#7F8C8D", font=("Helvetica Neue", 10))

        # Estilo para Treeview (para mostrar CSV)
        style.configure("Treeview.Heading", font=("Helvetica Neue", 10, "bold"), background="#ADD8E6", foreground="#333", padding=5)
        style.configure("Treeview", font=("Helvetica Neue", 9), rowheight=22, background="white", fieldbackground="white")
        style.map("Treeview", background=[('selected', '#87CEEB')])

        # Estilo para LabelFrames de secciones
        style.configure("Section.TLabelframe", background="#F0F8FF", borderwidth=1, relief="solid", padding=10)
        style.configure("Section.TLabelframe.Label", background="#F0F8FF", foreground="#2C3E50", font=("Helvetica Neue", 13, "bold"))


    def _create_widgets(self):
        """Crea y posiciona todos los widgets de la aplicación."""

        # --- Sección de Título y Subtítulo ---
        header_frame = ttk.Frame(self, style="Header.TFrame")
        header_frame.pack(fill="x", pady=(0, 10))

        titulo = ttk.Label(header_frame, text="SOFTWARE EDUCATIVO", style="HeaderTitle.TLabel")
        titulo.pack(pady=(15, 0), padx=20)

        subtitulo = ttk.Label(header_frame, text="ANÁLISIS DE SUPERVIVENCIA", style="HeaderSubtitle.TLabel")
        subtitulo.pack(pady=(0, 15), padx=20)

        # --- Notebook (Pestañas) para el Contenido Principal ---
        self.notebook = ttk.Notebook(self, style="TNotebook")
        self.notebook.pack(pady=10, fill="both", expand=True, padx=20)

        # Crear las pestañas
        self._create_teoria_tab()
        self._create_simulacion_tab()
        self._create_csv_tab()
        self._create_analisis_tab() # Pestaña de Kaplan-Meier
        self._create_cox_tab() # Nueva pestaña de Regresión de Cox

        # --- Pie de página ---
        footer = ttk.Label(self, text="Desarrollado por: Zenaida Erika Valencia Condori - FIEI 2025",
                           style="Footer.TLabel")
        footer.pack(side="bottom", pady=10)

    def _create_teoria_tab(self):
        """Crea la pestaña de Teoría Interactiva."""
        teoria_tab = ttk.Frame(self.notebook, style="TFrame")
        self.notebook.add(teoria_tab, text="📘 Teoría Interactiva")

        teoria_tab.grid_rowconfigure(0, weight=1)
        teoria_tab.grid_columnconfigure(0, weight=1)

        # Usar un Text widget para contenido largo y scrollable
        teoria_text_widget = tk.Text(teoria_tab, wrap="word", font=("Helvetica Neue", 11),
                                     bg="white", fg="#333", padx=15, pady=15, relief="flat", bd=0)
        teoria_text_widget.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        # Scrollbar para el Text widget
        scrollbar = ttk.Scrollbar(teoria_tab, command=teoria_text_widget.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")
        teoria_text_widget.config(yscrollcommand=scrollbar.set)

        teoria_content = """
        ¡Bienvenido a la sección de Teoría Interactiva sobre Análisis de Supervivencia!

        El Análisis de Supervivencia, también conocido como análisis de tiempo hasta el evento, es una rama de la estadística que se ocupa del análisis del tiempo transcurrido hasta que ocurre un evento de interés. Este evento puede ser la muerte, la falla de un componente, la recaída de una enfermedad, la graduación de un estudiante, etc.

        Conceptos Clave:
        ------------------
        1.  Tiempo hasta el Evento: Es la variable principal de interés. Es el tiempo desde un punto de inicio definido hasta la ocurrencia del evento.

        2.  Censura: Es una característica fundamental en el análisis de supervivencia. Ocurre cuando no se observa el tiempo exacto hasta el evento para algunos individuos. Las razones comunes incluyen:
            * Censura por la Derecha: El evento no ha ocurrido al final del estudio o el individuo se pierde de seguimiento. Se sabe que el tiempo hasta el evento es al menos el tiempo observado.
            * Censura por la Izquierda: El evento ocurrió antes del inicio del seguimiento.
            * Censura por Intervalo: Se sabe que el evento ocurrió en un intervalo de tiempo.
            En este software nos enfocaremos principalmente en la censura por la derecha.

        3.  Función de Supervivencia S(t):
            * Define la probabilidad de que un individuo sobreviva más allá de un tiempo t.
            * S(t) = P(T > t), donde T es el tiempo hasta el evento.
            * Siempre S(0) = 1 (probabilidad de sobrevivir al inicio es 1) y S(t) tiende a 0 a medida que t aumenta.

        4.  Función de Riesgo h(t):
            * Representa la tasa instantánea de ocurrencia del evento en el tiempo t, dado que el individuo ha sobrevivido hasta ese momento.
            * Es una medida de la "peligrosidad" en un momento dado.
            * h(t) = f(t) / S(t), donde f(t) es la función de densidad de probabilidad del tiempo hasta el evento.

        Métodos Comunes:
        ------------------
        1.  Estimador de Kaplan-Meier (No Paramétrico):
            * Es el método más utilizado para estimar la función de supervivencia a partir de datos censurados.
            * No asume una distribución específica para los tiempos de supervivencia.
            * Se calcula como un producto de probabilidades condicionales de supervivencia en cada tiempo de evento observado.

        2.  Modelos Paramétricos (Ej. Exponencial, Weibull):
            * Asumen que los tiempos de supervivencia siguen una distribución de probabilidad específica (ej. exponencial, Weibull, log-normal).
            * Permiten hacer inferencias y predicciones más allá de los datos observados si la suposición de distribución es correcta.

        3.  Regresión de Cox (Modelo de Riesgos Proporcionales):
            * Es un modelo semi-paramétrico muy popular.
            * No asume una distribución específica para la función de riesgo base, pero asume que los efectos de las covariables son proporcionales a la función de riesgo base.
            * Permite evaluar cómo diferentes factores (covariables) influyen en el tiempo hasta el evento.

        ¡Explora las otras secciones para simular datos y cargar tus propios archivos CSV!
        """
        teoria_text_widget.insert(tk.END, teoria_content)
        teoria_text_widget.config(state="disabled") # Hacer el texto de solo lectura

    def _create_simulacion_tab(self):
        """Crea la pestaña de Simulación de Datos."""
        simulacion_tab = ttk.Frame(self.notebook, style="TFrame")
        self.notebook.add(simulacion_tab, text="📊 Simulación de Datos")

        simulacion_tab.grid_columnconfigure(0, weight=1)
        simulacion_tab.grid_columnconfigure(1, weight=2) # Columna para el gráfico más grande
        simulacion_tab.grid_rowconfigure(0, weight=1) # Fila para inputs
        simulacion_tab.grid_rowconfigure(1, weight=1) # Fila para el gráfico

        # --- Frame de Controles de Simulación ---
        control_frame = ttk.LabelFrame(simulacion_tab, text="Parámetros de Simulación", padding="10", style="Section.TLabelframe")
        control_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        control_frame.grid_columnconfigure(1, weight=1) # Para que las entradas se expandan

        ttk.Label(control_frame, text="Tamaño de Muestra:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.sample_size_entry = ttk.Entry(control_frame, width=15)
        self.sample_size_entry.insert(0, "100")
        self.sample_size_entry.grid(row=0, column=1, sticky="ew", padx=5, pady=5)

        ttk.Label(control_frame, text="Tasa de Evento (lambda):").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.event_rate_entry = ttk.Entry(control_frame, width=15)
        self.event_rate_entry.insert(0, "0.05")
        self.event_rate_entry.grid(row=1, column=1, sticky="ew", padx=5, pady=5)

        ttk.Label(control_frame, text="Proporción de Censura:").grid(row=2, column=0, sticky="w", padx=5, pady=5)
        self.censoring_prop_entry = ttk.Entry(control_frame, width=15)
        self.censoring_prop_entry.insert(0, "0.2")
        self.censoring_prop_entry.grid(row=2, column=1, sticky="ew", padx=5, pady=5)

        ttk.Button(control_frame, text="Generar Simulación", command=self._run_simulation, style="Tab.TButton").grid(row=3, column=0, columnspan=2, pady=15)

        self.sim_status_label = ttk.Label(control_frame, text="", foreground="blue")
        self.sim_status_label.grid(row=4, column=0, columnspan=2, pady=5)

        # --- Frame para el Gráfico de Simulación ---
        plot_frame = ttk.LabelFrame(simulacion_tab, text="Gráfico de Supervivencia (Kaplan-Meier)", padding="10", style="Section.TLabelframe")
        plot_frame.grid(row=0, column=1, rowspan=2, padx=10, pady=10, sticky="nsew") # Ocupa 2 filas
        plot_frame.grid_columnconfigure(0, weight=1)
        plot_frame.grid_rowconfigure(0, weight=1)

        # Configurar la figura de Matplotlib para la simulación
        self.sim_fig, self.sim_ax = plt.subplots(figsize=(6, 5), dpi=100)
        self.sim_canvas_matplotlib = FigureCanvasTkAgg(self.sim_fig, master=plot_frame)
        self.sim_canvas_widget = self.sim_canvas_matplotlib.get_tk_widget()
        self.sim_canvas_widget.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.sim_toolbar = NavigationToolbar2Tk(self.sim_canvas_matplotlib, plot_frame)
        self.sim_toolbar.update()
        self.sim_canvas_widget.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self._clear_sim_plot() # Limpiar el plot al inicio

    def _clear_sim_plot(self):
        """Limpia el gráfico de simulación."""
        self.sim_ax.clear()
        self.sim_ax.set_title("Gráfico de Supervivencia (Kaplan-Meier)")
        self.sim_ax.set_xlabel("Tiempo")
        self.sim_ax.set_ylabel("Probabilidad de Supervivencia")
        self.sim_ax.set_ylim(0, 1)
        self.sim_ax.grid(True)
        self.sim_canvas_matplotlib.draw_idle()

    def _run_simulation(self):
        """Genera y visualiza datos de supervivencia simulados."""
        try:
            sample_size = int(self.sample_size_entry.get())
            event_rate = float(self.event_rate_entry.get())
            censoring_prop = float(self.censoring_prop_entry.get())

            if sample_size <= 0 or event_rate <= 0 or not (0 <= censoring_prop <= 1): # Censura puede ser 1
                raise ValueError("Parámetros inválidos. Asegúrate de que sean positivos y la proporción de censura esté entre 0 y 1.")

            # Simulación de tiempos de evento (distribución exponencial para simplicidad)
            event_times = np.random.exponential(1 / event_rate, size=sample_size)
            
            # Simulación de tiempos de censura (uniforme hasta un cierto punto)
            # Para lograr la proporción de censura, ajustamos el límite superior del tiempo de censura
            # Esto es una simplificación, en la realidad es más complejo.
            # Asegurarse de que max_time no sea 0 si event_times son todos muy pequeños
            if len(event_times) > 0:
                max_event_time = np.max(event_times)
                if max_event_time == 0: # Evitar división por cero o max_time muy pequeño
                    max_time = 1.0 # Valor por defecto seguro
                else:
                    max_time = np.percentile(event_times, (1 - censoring_prop) * 100)
                    if max_time == 0: max_time = max_event_time # Fallback si el percentil es 0
            else:
                max_time = 1.0 # Si no hay eventos, tiempo máximo por defecto

            censoring_times = np.random.uniform(0, max_time * 1.5, size=sample_size)

            # Determinar el tiempo observado y el estado del evento
            T = np.minimum(event_times, censoring_times)
            E = (event_times <= censoring_times).astype(int) # 1 si evento, 0 si censurado

            # Crear y ajustar el modelo Kaplan-Meier
            kmf = KaplanMeierFitter()
            kmf.fit(T, event_observed=E)

            # Dibujar el gráfico
            self.sim_ax.clear()
            kmf.plot_survival_function(ax=self.sim_ax)
            self.sim_ax.set_title(f"Curva de Kaplan-Meier (N={sample_size}, Tasa Evento={event_rate}, Censura={censoring_prop*100:.1f}%)")
            self.sim_ax.set_xlabel("Tiempo")
            self.sim_ax.set_ylabel("Probabilidad de Supervivencia")
            self.sim_ax.set_ylim(0, 1)
            self.sim_ax.grid(True)
            self.sim_canvas_matplotlib.draw_idle()
            
            self.sim_status_label.config(text="Simulación generada exitosamente.", foreground="blue")

        except ValueError as e:
            self.sim_status_label.config(text=f"Error en parámetros: {e}", foreground="red")
            self._clear_sim_plot()
        except Exception as e:
            self.sim_status_label.config(text=f"Error inesperado en simulación: {e}", foreground="red")
            self._clear_sim_plot()

    def _create_csv_tab(self):
        """Crea la pestaña de Cargar Archivo CSV."""
        csv_tab = ttk.Frame(self.notebook, style="TFrame")
        self.notebook.add(csv_tab, text="📁 Cargar Archivo CSV")

        csv_tab.grid_columnconfigure(0, weight=1)
        csv_tab.grid_rowconfigure(2, weight=1) # Fila para el Treeview

        ttk.Label(csv_tab, text="Carga tus datos de supervivencia desde un archivo CSV.",
                  font=("Helvetica Neue", 12), background="#EBF5FB").grid(row=0, column=0, pady=10, padx=10, sticky="w")

        button_frame = ttk.Frame(csv_tab, style="TFrame")
        button_frame.grid(row=1, column=0, pady=5, padx=10, sticky="ew")
        button_frame.grid_columnconfigure(0, weight=1) # Para que la ruta se expanda

        self.csv_file_path_var = tk.StringVar()
        ttk.Label(button_frame, textvariable=self.csv_file_path_var, wraplength=500,
                  background="#EBF5FB", font=("Helvetica Neue", 10, "italic")).grid(row=0, column=0, sticky="w")
        
        ttk.Button(button_frame, text="Buscar Archivo CSV...", command=self._browse_csv_file, style="Tab.TButton").grid(row=0, column=1, padx=10)

        # Treeview para mostrar el contenido del CSV
        self.csv_tree = ttk.Treeview(csv_tab, show="headings")
        self.csv_tree.grid(row=2, column=0, sticky="nsew", padx=10, pady=10)

        # Scrollbars para el Treeview
        csv_vsb = ttk.Scrollbar(csv_tab, orient="vertical", command=self.csv_tree.yview)
        csv_hsb = ttk.Scrollbar(csv_tab, orient="horizontal", command=self.csv_tree.xview)
        self.csv_tree.configure(yscrollcommand=csv_vsb.set, xscrollcommand=csv_hsb.set)
        csv_vsb.grid(row=2, column=1, sticky="ns")
        csv_hsb.grid(row=3, column=0, sticky="ew")

        self.csv_status_label = ttk.Label(csv_tab, text="", foreground="blue")
        self.csv_status_label.grid(row=4, column=0, columnspan=2, pady=5)

    def _browse_csv_file(self):
        """Abre un diálogo para seleccionar un archivo CSV y carga su contenido."""
        file_path = filedialog.askopenfilename(
            title="Seleccionar Archivo CSV",
            filetypes=[("Archivos CSV", "*.csv"), ("Todos los archivos", "*.*")]
        )
        if file_path:
            self.csv_file_path_var.set(f"Archivo seleccionado: {file_path.split('/')[-1]}")
            self.csv_status_label.config(text="Cargando datos...", foreground="blue")
            try:
                # Cargar el CSV usando pandas
                self.csv_data_frame = pd.read_csv(file_path)
                self._display_csv_data()
                self.csv_status_label.config(text=f"Archivo '{file_path.split('/')[-1]}' cargado exitosamente. Filas: {len(self.csv_data_frame)}", foreground="green")
                
                # Actualizar comboboxes en las pestañas de análisis
                self._update_analysis_comboboxes()

            except Exception as e:
                self.csv_status_label.config(text=f"Error al cargar CSV: {e}", foreground="red")
                self.csv_data_frame = None
                self._clear_csv_display()
                self._update_analysis_comboboxes() # Limpiar también en análisis
        else:
            self.csv_file_path_var.set("Ningún archivo seleccionado.")
            self.csv_status_label.config(text="Carga de archivo cancelada.", foreground="gray")
            self.csv_data_frame = None
            self._clear_csv_display()
            self._update_analysis_comboboxes() # Limpiar también en análisis

    def _display_csv_data(self):
        """Muestra los datos del DataFrame cargado en el Treeview."""
        self._clear_csv_display() # Limpiar Treeview antes de cargar nuevos datos

        if self.csv_data_frame is not None:
            # Configurar columnas del Treeview
            self.csv_tree["columns"] = list(self.csv_data_frame.columns)
            self.csv_tree["show"] = "headings"

            for col in self.csv_data_frame.columns:
                self.csv_tree.heading(col, text=col)
                self.csv_tree.column(col, width=100, anchor="center") # Ancho por defecto

            # Insertar filas
            for index, row in self.csv_data_frame.iterrows():
                self.csv_tree.insert("", "end", values=list(row))
        else:
            self.csv_status_label.config(text="No hay datos CSV para mostrar.", foreground="gray")

    def _clear_csv_display(self):
        """Limpia el Treeview de la sección CSV."""
        self.csv_tree.delete(*self.csv_tree.get_children())
        self.csv_tree["columns"] = () # Borrar columnas
        self.csv_tree["show"] = "" # Ocultar encabezados si no hay columnas

    def _create_analisis_tab(self):
        """Crea la pestaña de Análisis de Datos (Kaplan-Meier)."""
        analisis_tab = ttk.Frame(self.notebook, style="TFrame")
        self.notebook.add(analisis_tab, text="📈 Análisis de Datos")

        analisis_tab.grid_columnconfigure(0, weight=1) # Controles
        analisis_tab.grid_columnconfigure(1, weight=2) # Gráfico
        analisis_tab.grid_rowconfigure(0, weight=1) # Controles y gráfico

        # --- Frame de Controles de Análisis ---
        control_frame = ttk.LabelFrame(analisis_tab, text="Parámetros de Análisis (Kaplan-Meier)", padding="10", style="Section.TLabelframe")
        control_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        control_frame.grid_columnconfigure(1, weight=1)

        ttk.Label(control_frame, text="Columna de Tiempo:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.km_time_col_combobox = ttk.Combobox(control_frame, state="readonly", width=25)
        self.km_time_col_combobox.grid(row=0, column=1, sticky="ew", padx=5, pady=5)

        ttk.Label(control_frame, text="Columna de Evento (1=Evento, 0=Censura):").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.km_event_col_combobox = ttk.Combobox(control_frame, state="readonly", width=25)
        self.km_event_col_combobox.grid(row=1, column=1, sticky="ew", padx=5, pady=5)

        ttk.Label(control_frame, text="Columna de Grupo (Opcional):").grid(row=2, column=0, sticky="w", padx=5, pady=5)
        self.km_group_col_combobox = ttk.Combobox(control_frame, state="readonly", width=25)
        self.km_group_col_combobox.grid(row=2, column=1, sticky="ew", padx=5, pady=5)
        self.km_group_col_combobox.bind("<<ComboboxSelected>>", self._on_km_group_selected) # Para limpiar si se deselecciona

        ttk.Button(control_frame, text="Realizar Análisis KM", command=self._perform_km_analysis, style="Tab.TButton").grid(row=3, column=0, columnspan=2, pady=15)

        self.km_analysis_status_label = ttk.Label(control_frame, text="", foreground="blue")
        self.km_analysis_status_label.grid(row=4, column=0, columnspan=2, pady=5)

        # --- Frame para el Gráfico de Análisis ---
        plot_frame = ttk.LabelFrame(analisis_tab, text="Curva de Supervivencia (Kaplan-Meier)", padding="10", style="Section.TLabelframe")
        plot_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        plot_frame.grid_columnconfigure(0, weight=1)
        plot_frame.grid_rowconfigure(0, weight=1)

        self.analysis_fig, self.analysis_ax = plt.subplots(figsize=(7, 6), dpi=100)
        self.analysis_canvas_matplotlib = FigureCanvasTkAgg(self.analysis_fig, master=plot_frame)
        self.analysis_canvas_widget = self.analysis_canvas_matplotlib.get_tk_widget()
        self.analysis_canvas_widget.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.analysis_toolbar = NavigationToolbar2Tk(self.analysis_canvas_matplotlib, plot_frame)
        self.analysis_toolbar.update()
        self.analysis_canvas_widget.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self._clear_analysis_plot() # Limpiar el plot al inicio

    def _on_km_group_selected(self, event):
        """Maneja la selección del combobox de grupo de KM para permitir deseleccionar."""
        if self.km_group_col_combobox.get() == "Ninguno":
            self.km_group_col_combobox.set("") # Limpiar la selección
        self._clear_analysis_plot() # Limpiar el gráfico al cambiar la selección

    def _clear_analysis_plot(self):
        """Limpia el gráfico de análisis."""
        self.analysis_ax.clear()
        self.analysis_ax.set_title("Curva de Supervivencia (Kaplan-Meier)")
        self.analysis_ax.set_xlabel("Tiempo")
        self.analysis_ax.set_ylabel("Probabilidad de Supervivencia")
        self.analysis_ax.set_ylim(0, 1)
        self.analysis_ax.grid(True)
        self.analysis_canvas_matplotlib.draw_idle()

    def _update_analysis_comboboxes(self):
        """Actualiza las opciones de los comboboxes de tiempo, evento y grupo en ambas pestañas de análisis."""
        if self.csv_data_frame is not None:
            columns = self.csv_data_frame.columns.tolist()
            
            # Para Kaplan-Meier
            self.km_time_col_combobox['values'] = columns
            self.km_event_col_combobox['values'] = columns
            # Añadir opción "Ninguno" para la columna de grupo
            self.km_group_col_combobox['values'] = ["Ninguno"] + columns 

            # Intentar seleccionar automáticamente
            if 'time' in columns: self.km_time_col_combobox.set('time')
            elif 'Time' in columns: self.km_time_col_combobox.set('Time')
            if 'event' in columns: self.km_event_col_combobox.set('event')
            elif 'Event' in columns: self.km_event_col_combobox.set('Event')

            # Para Cox Regression
            self.cox_time_col_combobox['values'] = columns
            self.cox_event_col_combobox['values'] = columns
            self.cox_covariates_listbox.delete(0, tk.END) # Limpiar antes de poblar
            for col in columns:
                self.cox_covariates_listbox.insert(tk.END, col)
            
            # Intentar seleccionar automáticamente para Cox
            if 'time' in columns: self.cox_time_col_combobox.set('time')
            elif 'Time' in columns: self.cox_time_col_combobox.set('Time')
            if 'event' in columns: self.cox_event_col_combobox.set('event')
            elif 'Event' in columns: self.cox_event_col_combobox.set('Event')

        else:
            # Limpiar todos los comboboxes si no hay datos
            self.km_time_col_combobox['values'] = []
            self.km_event_col_combobox['values'] = []
            self.km_group_col_combobox['values'] = []
            self.km_time_col_combobox.set('')
            self.km_event_col_combobox.set('')
            self.km_group_col_combobox.set('')

            self.cox_time_col_combobox['values'] = []
            self.cox_event_col_combobox['values'] = []
            self.cox_covariates_listbox.delete(0, tk.END)
            self.cox_time_col_combobox.set('')
            self.cox_event_col_combobox.set('')

        self._clear_analysis_plot() # Limpiar gráfico KM
        self._clear_cox_output() # Limpiar salida Cox

    def _perform_km_analysis(self):
        """Realiza el análisis de Kaplan-Meier con los datos cargados."""
        if self.csv_data_frame is None:
            self.km_analysis_status_label.config(text="Por favor, carga un archivo CSV primero.", foreground="red")
            self._clear_analysis_plot()
            return

        time_col = self.km_time_col_combobox.get()
        event_col = self.km_event_col_combobox.get()
        group_col = self.km_group_col_combobox.get() if self.km_group_col_combobox.get() != "Ninguno" else None

        if not time_col or not event_col:
            self.km_analysis_status_label.config(text="Selecciona las columnas de Tiempo y Evento.", foreground="red")
            self._clear_analysis_plot()
            return
        
        if time_col not in self.csv_data_frame.columns or event_col not in self.csv_data_frame.columns:
            self.km_analysis_status_label.config(text="Columnas seleccionadas no encontradas en el CSV.", foreground="red")
            self._clear_analysis_plot()
            return

        try:
            T = self.csv_data_frame[time_col].astype(float)
            E = self.csv_data_frame[event_col].astype(int) # Evento debe ser 0 o 1

            if not all(x in [0, 1] for x in E.unique()):
                messagebox.showwarning("Advertencia de Datos", "La columna de Evento debe contener solo valores 0 (censurado) y 1 (evento).", parent=self)
                # return # Podríamos detener la ejecución o intentar continuar
            
            self.analysis_ax.clear() # Limpiar el plot antes de dibujar nuevas curvas
            kmf = KaplanMeierFitter()

            if group_col and group_col in self.csv_data_frame.columns:
                # Análisis por grupos
                for name, grouped_df in self.csv_data_frame.groupby(group_col):
                    kmf.fit(grouped_df[time_col], event_observed=grouped_df[event_col], label=str(name))
                    kmf.plot_survival_function(ax=self.analysis_ax)
                self.analysis_ax.legend(title=group_col) # Añadir leyenda
            else:
                # Análisis general sin grupos
                kmf.fit(T, event_observed=E)
                kmf.plot_survival_function(ax=self.analysis_ax)

            self.analysis_ax.set_title(f"Curva de Kaplan-Meier\n(Tiempo: '{time_col}', Evento: '{event_col}')")
            self.analysis_ax.set_xlabel("Tiempo")
            self.analysis_ax.set_ylabel("Probabilidad de Supervivencia")
            self.analysis_ax.set_ylim(0, 1)
            self.analysis_ax.grid(True)
            self.analysis_canvas_matplotlib.draw_idle()

            self.km_analysis_status_label.config(text="Análisis de Kaplan-Meier realizado exitosamente.", foreground="blue")

        except ValueError as e:
            self.km_analysis_status_label.config(text=f"Error en el tipo de datos de las columnas: {e}. Asegúrate de que sean numéricas.", foreground="red")
            self._clear_analysis_plot()
        except Exception as e:
            self.km_analysis_status_label.config(text=f"Error al realizar el análisis: {e}", foreground="red")
            self._clear_analysis_plot()

    def _create_cox_tab(self):
        """Crea la nueva pestaña de Regresión de Cox."""
        cox_tab = ttk.Frame(self.notebook, style="TFrame")
        self.notebook.add(cox_tab, text="🔬 Regresión de Cox")

        cox_tab.grid_columnconfigure(0, weight=1) # Controles
        cox_tab.grid_columnconfigure(1, weight=1) # Salida del modelo
        cox_tab.grid_rowconfigure(0, weight=1) # Controles y salida

        # --- Frame de Controles de Cox ---
        control_frame = ttk.LabelFrame(cox_tab, text="Parámetros de Regresión de Cox", padding="10", style="Section.TLabelframe")
        control_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        control_frame.grid_columnconfigure(1, weight=1)

        ttk.Label(control_frame, text="Columna de Tiempo:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.cox_time_col_combobox = ttk.Combobox(control_frame, state="readonly", width=25)
        self.cox_time_col_combobox.grid(row=0, column=1, sticky="ew", padx=5, pady=5)

        ttk.Label(control_frame, text="Columna de Evento (1=Evento, 0=Censura):").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.cox_event_col_combobox = ttk.Combobox(control_frame, state="readonly", width=25)
        self.cox_event_col_combobox.grid(row=1, column=1, sticky="ew", padx=5, pady=5)

        ttk.Label(control_frame, text="Covariables (Selecciona Múltiples):").grid(row=2, column=0, sticky="nw", padx=5, pady=5)
        
        # Listbox para covariables con multi-selección
        self.cox_covariates_listbox = tk.Listbox(control_frame, selectmode=tk.MULTIPLE, height=8, width=30,
                                                 font=("Helvetica Neue", 10), bg="white", fg="#333", relief="solid", bd=1)
        self.cox_covariates_listbox.grid(row=2, column=1, sticky="nsew", padx=5, pady=5)
        
        # Scrollbar para el Listbox
        cov_vsb = ttk.Scrollbar(control_frame, orient="vertical", command=self.cox_covariates_listbox.yview)
        cov_vsb.grid(row=2, column=2, sticky="ns")
        self.cox_covariates_listbox.config(yscrollcommand=cov_vsb.set)

        ttk.Button(control_frame, text="Realizar Regresión de Cox", command=self._perform_cox_regression, style="Tab.TButton").grid(row=3, column=0, columnspan=3, pady=15)

        self.cox_status_label = ttk.Label(control_frame, text="", foreground="blue")
        self.cox_status_label.grid(row=4, column=0, columnspan=3, pady=5)


        # --- Frame para la Salida del Modelo de Cox ---
        output_frame = ttk.LabelFrame(cox_tab, text="Resultados del Modelo de Cox", padding="10", style="Section.TLabelframe")
        output_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        output_frame.grid_columnconfigure(0, weight=1)
        output_frame.grid_rowconfigure(0, weight=1)

        self.cox_output_text = tk.Text(output_frame, wrap="word", font=("Consolas", 10),
                                       bg="white", fg="#333", padx=10, pady=10, relief="flat", bd=0)
        self.cox_output_text.grid(row=0, column=0, sticky="nsew")

        # Scrollbar para el Text widget
        cox_output_vsb = ttk.Scrollbar(output_frame, orient="vertical", command=self.cox_output_text.yview)
        cox_output_vsb.grid(row=0, column=1, sticky="ns")
        self.cox_output_text.config(yscrollcommand=cox_output_vsb.set)

        self._clear_cox_output() # Limpiar la salida al inicio

    def _clear_cox_output(self):
        """Limpia el área de texto de salida del modelo de Cox."""
        self.cox_output_text.config(state="normal")
        self.cox_output_text.delete(1.0, tk.END)
        self.cox_output_text.insert(tk.END, "Aquí se mostrarán los resultados de la Regresión de Cox.\n\n"
                                          "Asegúrate de cargar un CSV en la pestaña 'Cargar Archivo CSV' "
                                          "y seleccionar las columnas de Tiempo, Evento y Covariables.")
        self.cox_output_text.config(state="disabled")

    def _perform_cox_regression(self):
        """Realiza la regresión de riesgos proporcionales de Cox."""
        self._clear_cox_output() # Limpiar salida anterior
        if self.csv_data_frame is None:
            self.cox_status_label.config(text="Por favor, carga un archivo CSV primero.", foreground="red")
            return

        time_col = self.cox_time_col_combobox.get()
        event_col = self.cox_event_col_combobox.get()
        
        selected_indices = self.cox_covariates_listbox.curselection()
        covariates = [self.cox_covariates_listbox.get(i) for i in selected_indices]

        if not time_col or not event_col:
            self.cox_status_label.config(text="Selecciona las columnas de Tiempo y Evento.", foreground="red")
            return
        
        if not covariates:
            self.cox_status_label.config(text="Selecciona al menos una covariable.", foreground="red")
            return

        # Validar que las columnas existan
        required_cols = [time_col, event_col] + covariates
        if not all(col in self.csv_data_frame.columns for col in required_cols):
            self.cox_status_label.config(text="Una o más columnas seleccionadas no se encontraron en el CSV.", foreground="red")
            return

        try:
            # Preparar los datos para lifelines
            df_cox = self.csv_data_frame[[time_col, event_col] + covariates].copy()
            df_cox[time_col] = df_cox[time_col].astype(float)
            df_cox[event_col] = df_cox[event_col].astype(int)

            # Convertir covariables a tipo numérico o dummy si son categóricas
            for col in covariates:
                if df_cox[col].dtype == 'object' or df_cox[col].dtype == 'category':
                    # Convertir a variables dummy (one-hot encoding)
                    df_cox = pd.get_dummies(df_cox, columns=[col], prefix=col, drop_first=True)
                    # Actualizar la lista de covariables con los nuevos nombres de columnas dummy
                    covariates.remove(col)
                    covariates.extend([c for c in df_cox.columns if c.startswith(f"{col}_")])
                else:
                    df_cox[col] = df_cox[col].astype(float) # Asegurar que sean numéricas

            # Eliminar filas con valores NaN en las columnas relevantes
            df_cox.dropna(subset=[time_col, event_col] + covariates, inplace=True)

            if df_cox.empty:
                self.cox_status_label.config(text="No hay datos válidos después de la limpieza para el análisis.", foreground="red")
                return

            # Ajustar el modelo de Cox
            cph = CoxPHFitter()
            cph.fit(df_cox, duration_col=time_col, event_col=event_col, formula="+".join(covariates))

            # Mostrar el resumen en el Text widget
            self.cox_output_text.config(state="normal")
            self.cox_output_text.delete(1.0, tk.END)
            self.cox_output_text.insert(tk.END, cph.summary.to_string()) # Convertir el summary a string
            self.cox_output_text.config(state="disabled")

            self.cox_status_label.config(text="Regresión de Cox realizada exitosamente.", foreground="blue")

        except ValueError as e:
            self.cox_status_label.config(text=f"Error en el tipo de datos o formato: {e}. Revisa tus columnas.", foreground="red")
            self._clear_cox_output()
        except Exception as e:
            self.cox_status_label.config(text=f"Error inesperado al realizar la regresión de Cox: {e}", foreground="red")
            self._clear_cox_output()


# --- Punto de entrada de la aplicación ---
if __name__ == "__main__":
    app = SurvivalAnalysisApp()
    app.mainloop()