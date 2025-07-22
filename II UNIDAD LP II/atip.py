import tkinter as tk
from tkinter import messagebox, ttk
import os
import random
from playsound import playsound, PlaysoundException

class CandySurvivalGame:
    # --- CONSTANTES DE CONFIGURACIÓN DEL JUEGO ---
    INITIAL_INVENTORY_EASY = {'limon': 10, 'huevo': 10, 'pera': 9, 'chupetin': 0}
    INITIAL_INVENTORY_NORMAL = {'limon': 7, 'huevo': 7, 'pera': 6, 'chupetin': 0}
    INITIAL_INVENTORY_HARD = {'limon': 5, 'huevo': 5, 'pera': 4, 'chupetin': 0}

    TARGET_LOLLYPOPS_EASY = 7
    TARGET_LOLLYPOPS_NORMAL = 10
    TARGET_LOLLYPOPS_HARD = 12

    CANDY_RECIPE_COST = {'limon': 2, 'huevo': 2, 'pera': 2}
    CREATE_REWARD_AMOUNT = 2 # Caramelos extra al crear chupetin
    EXCHANGE_REWARD_AMOUNT = 6 # Caramelos al canjear chupetin

    # --- Configuración de Sonidos (rutas relativas) ---
    SOUND_FOLDER = "sounds" # ¡NUEVA CONSTANTE PARA LA CARPETA DE SONIDOS!
    
    SOUND_CREATE_SUCCESS = os.path.join(SOUND_FOLDER, "success.wav")
    SOUND_GAIN_CANDY = os.path.join(SOUND_FOLDER, "ding.wav")
    SOUND_ERROR = os.path.join(SOUND_FOLDER, "error.wav")
    SOUND_GAME_OVER = os.path.join(SOUND_FOLDER, "lose.wav")
    SOUND_BUTTON_CLICK = os.path.join(SOUND_FOLDER, "click.wav") 

    def __init__(self, master):
        self.master = master
        master.title("Supervivencia: El Desafío de los Caramelos")
        master.geometry("1000x700")
        master.resizable(True, True)
        master.state('zoomed') # Inicia maximizado

        self.emojis = {
            'limon': '🍋',
            'huevo': '🥚',
            'pera': '🍐',
            'chupetin': '🍭'
        }
        
        self.inventario = {}
        self.objetivo_chupetines = 0 # Se establecerá según la dificultad
        self.game_over = False
        self.game_mode = "solo"
        self.current_player = 1
        self.difficulty = "normal" # Dificultad por defecto

        self.reward_type = None
        self.total_reward_amount = 0
        self.callback_function = None
        self.message_timer = None # Para manejar la duración de los mensajes

        # --- Crear los dos frames principales: para la pantalla de inicio y para el juego ---
        self.start_frame = tk.Frame(self.master, bg="#2196F3")
        self.game_frame = tk.Frame(self.master, bg="#F0F0F0")

        # Crear los widgets de la pantalla de inicio dentro de self.start_frame
        self.create_start_screen_widgets()
        # Crear los widgets del juego dentro de self.game_frame (una vez)
        self.create_game_widgets(self.game_frame) 
        
        # Mostrar solo la pantalla de inicio al principio
        self.start_frame.pack(fill="both", expand=True)
        self.game_frame.pack_forget()

    def play_sound(self, sound_file):
        """Intenta reproducir un archivo de sonido dado su nombre."""
        try:
            # Comprobar si el archivo existe antes de intentar reproducirlo
            if os.path.exists(sound_file):
                playsound(sound_file, block=False) # block=False para no detener el programa
            else:
                print(f"Advertencia: Archivo de sonido no encontrado: {sound_file}")
        except PlaysoundException as e:
            print(f"Error al reproducir sonido {sound_file}: {e}")
        except Exception as e:
            print(f"Un error inesperado ocurrió al reproducir {sound_file}: {e}")

    def create_start_screen_widgets(self):
        """Crea los widgets de la pantalla de inicio dentro de self.start_frame."""
        tk.Label(self.start_frame, text="SUPERVIVENCIA", font=("Helvetica Neue", 48, "bold"), fg="white", bg="#2196F3").pack(pady=20)
        tk.Label(self.start_frame, text="¡El Desafío de los Caramelos!", font=("Helvetica Neue", 24), fg="white", bg="#2196F3").pack(pady=10)
        
        # Opciones de dificultad
        tk.Label(self.start_frame, text="Elige la dificultad:", font=("Helvetica Neue", 16), fg="white", bg="#2196F3").pack(pady=10)
        self.difficulty_var = tk.StringVar(value="normal") # Valor por defecto
        tk.Radiobutton(self.start_frame, text="Fácil", variable=self.difficulty_var, value="easy",
                       font=("Helvetica Neue", 14), bg="#2196F3", fg="white", selectcolor="#4CAF50").pack()
        tk.Radiobutton(self.start_frame, text="Normal", variable=self.difficulty_var, value="normal",
                       font=("Helvetica Neue", 14), bg="#2196F3", fg="white", selectcolor="#FFC107").pack()
        tk.Radiobutton(self.start_frame, text="Difícil", variable=self.difficulty_var, value="hard",
                       font=("Helvetica Neue", 14), bg="#2196F3", fg="white", selectcolor="#EF5350").pack()

        tk.Label(self.start_frame, text="Elige tu modo de juego:", font=("Helvetica Neue", 18), fg="white", bg="#2196F3").pack(pady=20)

        tk.Button(self.start_frame, text="JUGAR SOLO", command=lambda: self.start_game_mode("solo"),
                  font=("Helvetica Neue", 16, "bold"), bg="#4CAF50", fg="white",
                  width=25, height=2, relief="raised", bd=5).pack(pady=10)
        
        tk.Button(self.start_frame, text="JUGAR CON ALGUIEN MÁS\n(2 Jugadores - Colaborativo)", command=lambda: self.start_game_mode("coop2"),
                  font=("Helvetica Neue", 16, "bold"), bg="#FFC107", fg="black",
                  width=25, height=3, relief="raised", bd=5).pack(pady=10)
        
        tk.Label(self.start_frame, text="Modo por Grupos: ¡Próximamente!\n(Más complejo, dos inventarios separados y objetivos)", 
                 font=("Helvetica Neue", 12), fg="white", bg="#2196F3").pack(pady=15)
        
    def start_game_mode(self, mode):
        """Prepara y muestra el frame del juego para el modo seleccionado."""
        self.play_sound(self.SOUND_BUTTON_CLICK) # Sonido al iniciar
        self.game_mode = mode
        self.difficulty = self.difficulty_var.get() # Obtener la dificultad seleccionada
        
        # Establecer inventario inicial y objetivo según la dificultad
        if self.difficulty == "easy":
            self.inventario = self.INITIAL_INVENTORY_EASY.copy()
            self.objetivo_chupetines = self.TARGET_LOLLYPOPS_EASY
        elif self.difficulty == "normal":
            self.inventario = self.INITIAL_INVENTORY_NORMAL.copy()
            self.objetivo_chupetines = self.TARGET_LOLLYPOPS_NORMAL
        elif self.difficulty == "hard":
            self.inventario = self.INITIAL_INVENTORY_HARD.copy()
            self.objetivo_chupetines = self.TARGET_LOLLYPOPS_HARD

        self.chupetin_progressbar.config(maximum=self.objetivo_chupetines) # Actualizar el máximo de la barra

        self.start_frame.pack_forget()
        self.game_frame.pack(fill="both", expand=True)

        self.reset_game_state() # Reinicia el estado interno del juego
        self.update_display() # Actualiza la pantalla con el nuevo estado

    def create_game_widgets(self, parent_frame):
        """Crea todos los widgets de la interfaz principal del juego."""
        parent_frame.columnconfigure(0, weight=2)
        parent_frame.columnconfigure(1, weight=1)
        parent_frame.rowconfigure(0, weight=0)
        parent_frame.rowconfigure(1, weight=1)

        title_frame = tk.Frame(parent_frame, bg="#4CAF50", padx=10, pady=10)
        title_frame.grid(row=0, column=0, columnspan=2, sticky="new")
        tk.Label(title_frame, text="SUPERVIVENCIA", font=("Helvetica Neue", 36, "bold"), fg="white", bg="#4CAF50").pack(pady=5)
        tk.Label(title_frame, text="¡El Desafío de los Caramelos!", font=("Helvetica Neue", 20), fg="white", bg="#4CAF50").pack()

        main_content_frame = tk.Frame(parent_frame, bg="#F0F0F0") 
        main_content_frame.grid(row=1, column=0, columnspan=2, sticky="nsew", padx=20, pady=20)
        main_content_frame.columnconfigure(0, weight=2)
        main_content_frame.columnconfigure(1, weight=1)
        main_content_frame.rowconfigure(0, weight=1)

        # --- Panel Izquierdo (Inventario, Mensajes, Consejos/Reglas) ---
        left_panel_frame = tk.Frame(main_content_frame, bg="#F0F0F0")
        left_panel_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        left_panel_frame.rowconfigure(0, weight=2)
        left_panel_frame.rowconfigure(1, weight=1)

        inventory_frame = tk.Frame(left_panel_frame, bg="#E0F2F7", bd=2, relief="groove")
        inventory_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        inventory_frame.columnconfigure(0, weight=0)
        inventory_frame.columnconfigure(1, weight=1)

        tk.Label(inventory_frame, text="--- TU INVENTARIO ---", font=("Helvetica Neue", 18, "bold"), bg="#E0F2F7", pady=10).grid(row=0, columnspan=2, pady=(0,10))

        self.candy_labels = {} # Almacenar las referencias a las etiquetas para poder cambiarlas de color
        self.candy_labels_vars = {}
        row_idx = 1
        candy_types = ['limon', 'huevo', 'pera']

        for candy_type in candy_types:
            candy_row_frame = tk.Frame(inventory_frame, bg="#E0F2F7")
            candy_row_frame.grid(row=row_idx, column=0, columnspan=2, sticky="ew", padx=10, pady=5)
            tk.Label(candy_row_frame, text=self.emojis.get(candy_type, ''), font=("Arial Unicode MS", 30), bg="#E0F2F7").pack(side=tk.LEFT, padx=5)
            label_text_var = tk.StringVar()
            self.candy_labels_vars[candy_type] = label_text_var
            # Guardamos la referencia de la etiqueta
            self.candy_labels[candy_type] = tk.Label(candy_row_frame, textvariable=label_text_var, font=("Helvetica Neue", 16), bg="#E0F2F7", anchor="w")
            self.candy_labels[candy_type].pack(side=tk.LEFT, fill=tk.X, expand=True)
            row_idx += 1

        chupetin_row_frame = tk.Frame(inventory_frame, bg="#E0F2F7")
        chupetin_row_frame.grid(row=row_idx, column=0, columnspan=2, sticky="ew", padx=10, pady=15)
        tk.Label(chupetin_row_frame, text=self.emojis.get('chupetin', ''), font=("Arial Unicode MS", 30), bg="#E0F2F7").pack(side=tk.LEFT, padx=5)
        self.chupetin_label_var = tk.StringVar()
        # Guardamos la referencia de la etiqueta del chupetin
        self.chupetin_label = tk.Label(chupetin_row_frame, textvariable=self.chupetin_label_var, font=("Helvetica Neue", 18, "bold"), bg="#E0F2F7", anchor="w")
        self.chupetin_label.pack(side=tk.LEFT, fill=tk.X, expand=True)

        self.message_label_var = tk.StringVar()
        self.message_label = tk.Label(inventory_frame, textvariable=self.message_label_var, font=("Helvetica Neue", 14), bg="#E0F2F7", fg="blue", wraplength=400)
        self.message_label.grid(row=row_idx+1, columnspan=2, pady=10)

        # Barra de progreso para chupetines
        progress_frame = tk.Frame(inventory_frame, bg="#E0F2F7")
        progress_frame.grid(row=row_idx+2, columnspan=2, pady=10, sticky="ew", padx=10)
        tk.Label(progress_frame, text="Progreso de Chupetines:", font=("Helvetica Neue", 12), bg="#E0F2F7").pack(side=tk.LEFT)
        self.chupetin_progressbar = ttk.Progressbar(progress_frame, orient="horizontal", length=200, mode="determinate")
        self.chupetin_progressbar.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        # El valor máximo se establece en start_game_mode

        # Indicador de turno
        self.turn_label_var = tk.StringVar()
        self.turn_label = tk.Label(inventory_frame, textvariable=self.turn_label_var, font=("Helvetica Neue", 16, "bold"), bg="#E0F2F7", fg="#FF5722")
        self.turn_label.grid(row=row_idx+3, columnspan=2, pady=10)

        # Historial de mensajes (simulado)
        tk.Label(inventory_frame, text="Últimos Mensajes:", font=("Helvetica Neue", 10, "underline"), bg="#E0F2F7").grid(row=row_idx+4, columnspan=2, pady=(10,0))
        self.message_history_var = tk.StringVar(value="")
        tk.Label(inventory_frame, textvariable=self.message_history_var, font=("Helvetica Neue", 10), bg="#E0F2F7", fg="#555", wraplength=400, justify=tk.LEFT).grid(row=row_idx+5, columnspan=2, pady=(0,5), sticky="w")


        # Panel de Consejos y Reglas
        info_panel_frame = tk.Frame(left_panel_frame, bg="#FFF3E0", bd=2, relief="groove")
        info_panel_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
        info_panel_frame.grid_columnconfigure(0, weight=1)

        self.info_mode_var = tk.StringVar(value="tips")
        mode_toggle_frame = tk.Frame(info_panel_frame, bg="#FFF3E0")
        mode_toggle_frame.grid(row=0, column=0, sticky="ew", pady=(5,0))
        tk.Radiobutton(mode_toggle_frame, text="Consejos", variable=self.info_mode_var, value="tips", 
                       command=self.display_info_content, bg="#FFF3E0", font=("Helvetica Neue", 10, "bold")).pack(side=tk.LEFT, padx=10)
        tk.Radiobutton(mode_toggle_frame, text="Reglas", variable=self.info_mode_var, value="rules", 
                       command=self.display_info_content, bg="#FFF3E0", font=("Helvetica Neue", 10, "bold")).pack(side=tk.LEFT, padx=10)

        self.info_text_widget = tk.Text(info_panel_frame, wrap="word", font=("Helvetica Neue", 12), bg="#FFF3E0", height=8, state="disabled")
        self.info_text_widget.grid(row=1, column=0, padx=10, pady=(5,10), sticky="nsew")


        # --- Panel Derecho (Acciones y Selección de Recompensa) ---
        actions_frame = tk.Frame(main_content_frame, bg="#FFF8E1", bd=2, relief="groove")
        actions_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        actions_frame.grid_columnconfigure(0, weight=1)
        tk.Label(actions_frame, text="--- ACCIONES ---", font=("Helvetica Neue", 18, "bold"), bg="#FFF8E1", pady=10).grid(row=0, column=0, pady=(0,10))

        self.create_button_balanced = tk.Button(actions_frame, 
                                                text=f"Crear 1 Chupetín\n(Usar: 2{self.emojis['limon']}, 2{self.emojis['huevo']}, 2{self.emojis['pera']})", 
                                                command=self.initiate_create_balanced_flow,
                                                font=("Helvetica Neue", 13, "bold"), bg="#81C784", fg="white", width=28, height=3, relief="raised", bd=3)
        self.create_button_balanced.grid(row=1, column=0, pady=10, padx=20)

        self.exchange_button = tk.Button(actions_frame, 
                                        text=f"Canjear 1 Chupetín\n(Obtener 6 caramelos)", 
                                        command=self.initiate_exchange_flow, 
                                        font=("Helvetica Neue", 14, "bold"), bg="#EF5350", fg="white", width=28, height=3, relief="raised", bd=3)
        self.exchange_button.grid(row=2, column=0, pady=10, padx=20) 

        self.reward_selection_frame = tk.Frame(actions_frame, bg="#E0F7FA", bd=2, relief="sunken")
        self.reward_selection_frame.grid_columnconfigure(0, weight=1)
        self.reward_selection_frame.grid_columnconfigure(1, weight=1)
        self.reward_selection_frame.grid_columnconfigure(2, weight=1)

        self.reward_message_label = tk.Label(self.reward_selection_frame, text="", font=("Helvetica", 11), wraplength=250, bg="#E0F7FA")
        self.reward_message_label.grid(row=0, column=0, columnspan=3, pady=(10,5))

        self.reward_vars = {
            'limon': tk.IntVar(value=0),
            'huevo': tk.IntVar(value=0),
            'pera': tk.IntVar(value=0)
        }
        self.reward_spinboxes = {}

        for i, candy_type in enumerate(['limon', 'huevo', 'pera']):
            tk.Label(self.reward_selection_frame, text=f"{self.emojis[candy_type]} {candy_type.capitalize()}:", font=("Helvetica", 10), bg="#E0F7FA").grid(row=i+1, column=0, padx=5, pady=2, sticky="w")
            spinbox = ttk.Spinbox(self.reward_selection_frame, from_=0, to=self.objetivo_chupetines, # Max to chupetines for simplicity
                                  textvariable=self.reward_vars[candy_type], 
                                  width=5, font=("Helvetica", 10), command=self._validate_reward_sum)
            spinbox.grid(row=i+1, column=1, padx=5, pady=2, sticky="ew")
            self.reward_spinboxes[candy_type] = spinbox
        
        self.reward_error_label = tk.Label(self.reward_selection_frame, text="", fg="red", font=("Helvetica", 9), bg="#E0F7FA")
        self.reward_error_label.grid(row=4, column=0, columnspan=3, pady=5)

        confirm_reward_button = tk.Button(self.reward_selection_frame, text="Confirmar Recompensa", 
                                  command=self._confirm_reward_selection,
                                  font=("Helvetica", 10, "bold"), bg="#4CAF50", fg="white")
        confirm_reward_button.grid(row=5, column=0, columnspan=3, pady=10)

        # Botón para reiniciar (si el juego ya está en marcha)
        self.restart_game_button = tk.Button(actions_frame, text="Reiniciar Juego", command=self._confirm_restart_game,
                                            font=("Helvetica Neue", 12), bg="#03A9F4", fg="white", width=20, relief="raised", bd=2)
        self.restart_game_button.grid(row=8, column=0, pady=10, padx=20) 


        back_to_start_button = tk.Button(actions_frame, text="Volver a Inicio", command=self._confirm_go_to_start_screen,
                                  font=("Helvetica Neue", 12), bg="#607D8B", fg="white", width=20, relief="raised", bd=2)
        back_to_start_button.grid(row=9, column=0, pady=20, padx=20) 

        exit_button = tk.Button(actions_frame, text="Salir del Juego", command=self._confirm_exit_game, 
                                font=("Helvetica Neue", 12), bg="#757575", fg="white", width=20, relief="raised", bd=2)
        exit_button.grid(row=10, column=0, pady=10, padx=20)

    def _confirm_restart_game(self):
        """Pide confirmación antes de reiniciar el juego."""
        self.play_sound(self.SOUND_BUTTON_CLICK)
        if messagebox.askyesno("Reiniciar Juego", "¿Estás seguro de que quieres reiniciar el juego?"):
            self.reset_game_state()
            self.update_display("¡El juego ha sido reiniciado!")

    def _confirm_go_to_start_screen(self):
        """Pide confirmación antes de volver a la pantalla de inicio."""
        self.play_sound(self.SOUND_BUTTON_CLICK)
        if messagebox.askyesno("Volver a Inicio", "¿Estás seguro de que quieres volver a la pantalla de inicio?\nPerderás tu progreso actual."):
            self.go_to_start_screen()

    def _confirm_exit_game(self):
        """Pide confirmación antes de salir del juego."""
        self.play_sound(self.SOUND_BUTTON_CLICK)
        if messagebox.askyesno("Salir del Juego", "¿Estás seguro de que quieres salir?"):
            self.master.quit()

    def go_to_start_screen(self):
        """Oculta el frame del juego y muestra la pantalla de inicio."""
        if self.message_timer:
            self.master.after_cancel(self.message_timer)
            self.message_timer = None
        self.game_frame.pack_forget()
        self.start_frame.pack(fill="both", expand=True)

    def reset_game_state(self):
        """Reinicia el estado del juego a los valores iniciales y actualiza el turno."""
        # Se asegura que el inventario se copie DE LAS CONSTANTES, no del estado anterior del juego
        if self.difficulty == "easy":
            self.inventario = self.INITIAL_INVENTORY_EASY.copy()
            self.objetivo_chupetines = self.TARGET_LOLLYPOPS_EASY
        elif self.difficulty == "normal":
            self.inventario = self.INITIAL_INVENTORY_NORMAL.copy()
            self.objetivo_chupetines = self.TARGET_LOLLYPOPS_NORMAL
        elif self.difficulty == "hard":
            self.inventario = self.INITIAL_INVENTORY_HARD.copy()
            self.objetivo_chupetines = self.TARGET_LOLLYPOPS_HARD

        self.game_over = False
        self.current_player = 1 
        self.enable_all_main_buttons() 
        self.hide_reward_selection_frame()
        
        if self.message_timer: # Cancela cualquier timer de mensaje previo
            self.master.after_cancel(self.message_timer)
            self.message_timer = None
        
        self.message_label_var.set("¡El juego ha comenzado! A reunir chupetines para los Sobrevivientes.")
        self.message_history_var.set("") # Limpiar historial
        
        self.update_turn_display()
        self.chupetin_progressbar.config(maximum=self.objetivo_chupetines) # Asegurar que el max sea correcto

    def update_turn_display(self):
        """Actualiza la etiqueta que muestra de quién es el turno."""
        if self.game_mode == "coop2":
            self.turn_label_var.set(f"▶️ Turno del Jugador {self.current_player}")
        else:
            self.turn_label_var.set("") 

    def switch_player_turn(self):
        """Cambia el turno al siguiente jugador en modo cooperativo y desencadena un evento aleatorio."""
        if self.game_mode == "coop2":
            self.current_player = 1 if self.current_player == 2 else 2
            self.update_turn_display()
        
        # Después de cada turno (o acción principal), intentar un evento aleatorio
        self._trigger_random_event()


    def update_display(self, message=None, flash_items=None):
        """
        Actualiza todas las etiquetas con el estado actual del inventario y los mensajes.
        flash_items: dict de {item_type: color} para animar el cambio.
        """
        # 1. Actualizar la cantidad de cada caramelo
        for candy_type, var in self.candy_labels_vars.items():
            var.set(f"{self.emojis[candy_type]} {candy_type.capitalize()}: {self.inventario[candy_type]}")
            # Resetear color si no está en flash_items
            if flash_items is None or candy_type not in flash_items:
                self.candy_labels[candy_type].config(fg="black", bg="#E0F2F7") # Color normal

        # 2. Actualizar la variable del chupetín directamente
        self.chupetin_label_var.set(f"{self.emojis['chupetin']} Chupetines: {self.inventario['chupetin']} / {self.objetivo_chupetines}")
        if flash_items is None or 'chupetin' not in flash_items:
             self.chupetin_label.config(fg="black", bg="#E0F2F7") # Color normal

        # 3. Actualizar la barra de progreso
        self.chupetin_progressbar.config(value=self.inventario['chupetin']) 
        
        # 4. Actualizar y gestionar el mensaje
        if self.message_timer: # Cancela el timer anterior si existe
            self.master.after_cancel(self.message_timer)
            self.message_timer = None

        if message is not None:
            # Actualizar historial de mensajes
            current_history = self.message_history_var.get()
            new_history_line = f"- {message.split('!')[0].strip()}." # Solo la primera parte del mensaje
            updated_history = (new_history_line + "\n" + current_history).strip()
            # Limitar a las últimas 3-4 líneas para no sobrecargar
            self.message_history_var.set("\n".join(updated_history.split('\n')[:4]))

            self.message_label_var.set(message)
            # Configurar el color y fuente del mensaje según su contenido
            if "VICTORIA" in message or "✅" in message:
                self.message_label.config(fg="green", font=("Helvetica Neue", 16, "bold"))
                self.message_timer = self.master.after(5000, lambda: self.message_label_var.set("")) # Mensaje de victoria/éxito dura más
            elif "DERROTA" in message or "❌" in message or "Faltan" in message or "No tienes" in message or "Error" in message:
                self.message_label.config(fg="red", font=("Helvetica Neue", 14))
                self.message_timer = self.master.after(5000, lambda: self.message_label_var.set("")) # Mensaje de error dura más
            else:
                self.message_label.config(fg="blue", font=("Helvetica Neue", 14))
                self.message_timer = self.master.after(3000, lambda: self.message_label_var.set("")) # Mensajes normales duran menos
        
        # 5. Aplicar animación de flash si se especificó
        if flash_items:
            for item, color in flash_items.items():
                if item == 'chupetin':
                    self.chupetin_label.config(fg=color, bg="#ADD8E6") # Azul claro para chupetin
                    self.master.after(500, lambda: self.chupetin_label.config(fg="black", bg="#E0F2F7"))
                elif item in self.candy_labels:
                    self.candy_labels[item].config(fg=color, bg="#ADD8E6") # Azul claro para caramelos
                    self.master.after(500, lambda l=self.candy_labels[item]: l.config(fg="black", bg="#E0F2F7")) # Reset después de 0.5s

        # 6. Forzar la actualización visual de Tkinter
        self.master.update_idletasks()
        self.master.update()           

        # 7. SOLO DESPUÉS DE ACTUALIZAR LA INTERFAZ, VERIFICAR EL ESTADO DEL JUEGO
        self.check_game_status() 
        
        # 8. Actualizar consejos/reglas
        self.display_info_content() 

    def check_game_status(self):
        """Verifica si el juego ha terminado (victoria o derrota)."""
        if self.game_over: 
            return

        # Condición de Victoria
        if self.inventario['chupetin'] >= self.objetivo_chupetines:
            self.game_over = True
            self.play_sound(self.SOUND_CREATE_SUCCESS) # Sonido de victoria
            self.update_display(f"🎉 ¡VICTORIA! ¡Has alcanzado {self.inventario['chupetin']} de {self.objetivo_chupetines} chupetines! ¡Todos los Sobrevivientes están a salvo!")
            self.disable_all_main_buttons()
            return

        # Condición de Derrota
        can_create = (self.inventario['limon'] >= self.CANDY_RECIPE_COST['limon'] and 
                      self.inventario['huevo'] >= self.CANDY_RECIPE_COST['huevo'] and 
                      self.inventario['pera'] >= self.CANDY_RECIPE_COST['pera'])
        can_exchange = (self.inventario['chupetin'] >= 1)

        if not can_create and not can_exchange:
            self.game_over = True
            self.play_sound(self.SOUND_GAME_OVER) # Sonido de derrota
            messagebox.showerror("¡DERROTA!", f"No hay más movimientos posibles y no alcanzaste la meta de {self.objetivo_chupetines} chupetines.\n¡Los Sobrevivientes están en peligro!")
            self.update_display("💀 ¡DERROTA! No hay más movimientos posibles y no alcanzaste la meta.")
            self.disable_all_main_buttons()
            return

        # Si el juego no ha terminado, habilitar/deshabilitar botones según la posibilidad
        if self.reward_selection_frame.winfo_ismapped(): # Si estamos en selección de recompensa, no tocar botones principales
            self.disable_all_main_buttons()
        else:
            self.create_button_balanced.config(state=tk.NORMAL if can_create else tk.DISABLED)
            self.exchange_button.config(state=tk.NORMAL if can_exchange else tk.DISABLED)


    def disable_all_main_buttons(self):
        """Deshabilita los botones de acción principales."""
        self.create_button_balanced.config(state=tk.DISABLED)
        self.exchange_button.config(state=tk.DISABLED)

    def enable_all_main_buttons(self):
        """Habilita los botones de acción principales."""
        # Se llama antes de check_game_status, que luego puede deshabilitarlos selectivamente
        self.create_button_balanced.config(state=tk.NORMAL)
        self.exchange_button.config(state=tk.NORMAL)


    def show_reward_selection_frame(self, total_amount, callback, message_text, reward_type_name):
        """Muestra el frame para que el usuario elija la distribución de caramelos de recompensa."""
        if self.reward_selection_frame.winfo_ismapped():
            return

        self.disable_all_main_buttons()
        self.reward_selection_frame.grid(row=3, column=0, columnspan=1, sticky="ew", pady=10, padx=10) 

        self.total_reward_amount = total_amount
        self.callback_function = callback
        self.reward_type = reward_type_name
        
        self.reward_message_label.config(text=message_text)

        for candy_type in ['limon', 'huevo', 'pera']:
            self.reward_vars[candy_type].set(0)
            # Asegurar que el spinbox no permita valores negativos o más de lo que se puede dar
            self.reward_spinboxes[candy_type].config(from_=0, to=total_amount) 
        
        self._validate_reward_sum()

    def hide_reward_selection_frame(self):
        """Oculta el frame de selección de recompensa."""
        self.reward_selection_frame.grid_forget()
        self.enable_all_main_buttons() # Se re-habilitan los botones principales
        self.total_reward_amount = 0
        self.callback_function = None
        self.reward_type = None

    def _validate_reward_sum(self):
        """Valida que la suma de los caramelos elegidos sea la correcta."""
        current_sum = sum(v.get() for v in self.reward_vars.values())
        expected_sum = self.total_reward_amount

        if current_sum != expected_sum:
            self.reward_error_label.config(text=f"La suma DEBE ser {expected_sum}. Actual: {current_sum}")
            return False
        else:
            self.reward_error_label.config(text="")
            return True

    def _confirm_reward_selection(self):
        """Confirma la elección de recompensa y llama a la función de callback."""
        self.play_sound(self.SOUND_BUTTON_CLICK)
        if not self._validate_reward_sum():
            return
        
        self.callback_function(chosen_rewards={ct: var.get() for ct, var in self.reward_vars.items()})
        
        self.hide_reward_selection_frame()
        self.switch_player_turn() # Esto también activa el evento aleatorio


    def initiate_create_balanced_flow(self):
        """Inicia el flujo de la 'Creación Balanceada' (2 de cada + 2 a elegir)."""
        self.play_sound(self.SOUND_BUTTON_CLICK)
        if self.game_over: return
        
        required_limon = self.CANDY_RECIPE_COST['limon']
        required_huevo = self.CANDY_RECIPE_COST['huevo']
        required_pera = self.CANDY_RECIPE_COST['pera']

        if not (self.inventario['limon'] >= required_limon and 
                self.inventario['huevo'] >= required_huevo and 
                self.inventario['pera'] >= required_pera):
            self.play_sound(self.SOUND_ERROR)
            self.update_display(f"❌ ¡Faltan caramelos! Necesitas {required_limon}{self.emojis['limon']}, {required_huevo}{self.emojis['huevo']}, {required_pera}{self.emojis['pera']} para esta creación.")
            return
        
        # Guardar valores antes del descuento para el "flash" visual
        old_inventario = self.inventario.copy()

        # Descuento los caramelos aquí, ANTES de mostrar la selección de recompensa
        self.inventario['limon'] -= required_limon
        self.inventario['huevo'] -= required_huevo
        self.inventario['pera'] -= required_pera
        
        # Prepara los ítems para el flash visual (los que se descontaron)
        flash_items = {
            'limon': 'red' if old_inventario['limon'] > self.inventario['limon'] else None,
            'huevo': 'red' if old_inventario['huevo'] > self.inventario['huevo'] else None,
            'pera': 'red' if old_inventario['pera'] > self.inventario['pera'] else None
        }

        self.update_display("¡Caramelos usados! Ahora elige tu recompensa.", flash_items) 

        self.show_reward_selection_frame(
            total_amount=self.CREATE_REWARD_AMOUNT,
            callback=self._perform_create_balanced_final,
            message_text=f"¡Has usado {required_limon}{self.emojis['limon']}, {required_huevo}{self.emojis['huevo']}, {required_pera}{self.emojis['pera']}!\nElige los {self.CREATE_REWARD_AMOUNT} caramelos adicionales que deseas recibir:",
            reward_type_name='create'
        )

    def _perform_create_balanced_final(self, chosen_rewards):
        """Ejecuta la acción final de crear chupetín (2 de cada) con la recompensa elegida."""
        if self.game_over: return
        
        old_chupetin_count = self.inventario['chupetin']
        self.inventario['chupetin'] += 1
        
        flash_items = {'chupetin': 'green'} # Para el chupetin ganado

        for candy_type, amount in chosen_rewards.items():
            if amount > 0:
                self.inventario[candy_type] += amount
                flash_items[candy_type] = 'green' # Para los caramelos de recompensa
        
        self.play_sound(self.SOUND_CREATE_SUCCESS)
        self.update_display(f"✅ ¡Chupetín creado! Recibiste 1{self.emojis['chupetin']} y tus {self.CREATE_REWARD_AMOUNT} caramelos elegidos.", flash_items)


    def initiate_exchange_flow(self):
        """Inicia el flujo del 'Canje Grande y Flexible' (1 chupetín por 6 a elegir)."""
        self.play_sound(self.SOUND_BUTTON_CLICK)
        if self.game_over: return
        if self.inventario['chupetin'] < 1:
            self.play_sound(self.SOUND_ERROR)
            self.update_display(f"❌ No tienes chupetines para canjear.")
            return

        old_chupetin_count = self.inventario['chupetin']
        self.inventario['chupetin'] -= 1
        
        flash_items = {'chupetin': 'red' if old_chupetin_count > self.inventario['chupetin'] else None}
        self.update_display("¡Chupetín usado! Ahora elige tu recompensa.", flash_items) 

        self.show_reward_selection_frame(
            total_amount=self.EXCHANGE_REWARD_AMOUNT,
            callback=self._perform_exchange_final,
            message_text=f"¡Has usado 1{self.emojis['chupetin']}!\nElige los {self.EXCHANGE_REWARD_AMOUNT} caramelos que deseas recibir:",
            reward_type_name='exchange'
        )

    def _perform_exchange_final(self, chosen_rewards):
        """Ejecuta la acción final de canje con la recompensa elegida."""
        if self.game_over: return

        flash_items = {}
        for candy_type, amount in chosen_rewards.items():
            if amount > 0:
                self.inventario[candy_type] += amount
                flash_items[candy_type] = 'green' # Para los caramelos de recompensa
        
        self.play_sound(self.SOUND_GAIN_CANDY) # Sonido de ganancia general
        self.update_display(f"✅ ¡Canje exitoso! Recibiste tus {self.EXCHANGE_REWARD_AMOUNT} caramelos elegidos.", flash_items)

    def _trigger_random_event(self):
        """Desencadena un evento aleatorio con cierta probabilidad."""
        if self.game_over:
            return

        event_chance = random.randint(1, 100) # 1 a 100
        
        if event_chance <= 15: # 15% de probabilidad de evento
            event_type = random.choice(["gain", "lose"])
            candy_type = random.choice(['limon', 'huevo', 'pera'])
            amount = random.randint(1, 2) # Gana/pierde 1 o 2 caramelos

            if event_type == "gain":
                self.inventario[candy_type] += amount
                self.play_sound(self.SOUND_GAIN_CANDY)
                self.update_display(f"✨ ¡Evento! Aparecieron {amount} {self.emojis[candy_type]} {candy_type.capitalize()} extra.", {candy_type: 'blue'})
            else: # lose
                # Asegurarse de no perder más de lo que se tiene
                actual_loss = min(amount, self.inventario[candy_type])
                self.inventario[candy_type] -= actual_loss
                if actual_loss > 0:
                    self.play_sound(self.SOUND_GAME_OVER) # Sonido de pérdida
                    self.update_display(f"💔 ¡Evento! Perdiste {actual_loss} {self.emojis[candy_type]} {candy_type.capitalize()}.", {candy_type: 'red'})
                else:
                    self.update_display(f"✨ ¡Evento! Un {self.emojis[candy_type]} {candy_type.capitalize()} intentó escapar, pero no tenías. ¡Suerte la tuya!")
        # else: no event, just normal turn switch


    def display_info_content(self):
        """Muestra los consejos o las reglas en el Text widget del panel de información."""
        self.info_text_widget.config(state="normal")
        self.info_text_widget.delete(1.0, tk.END)

        if self.info_mode_var.get() == "tips":
            self.info_text_widget.insert(tk.END, self.get_tips_text())
        else:
            self.info_text_widget.insert(tk.END, self.get_rules_text())
        
        self.info_text_widget.config(state="disabled")

    def get_tips_text(self):
        """Genera y devuelve el texto de sugerencias de estrategia."""
        limon = self.inventario['limon']
        huevo = self.inventario['huevo']
        pera = self.inventario['pera']
        chupetin = self.inventario['chupetin']

        consejo = "Analiza tu inventario antes de cada movimiento."

        current_candies = [limon, huevo, pera]
        if current_candies:
            min_candy_value = min(current_candies)
            candies_with_min = [c for c in ['limon', 'huevo', 'pera'] if self.inventario[c] == min_candy_value]
        else:
            min_candy_value = 0
            candies_with_min = []
        
        can_create = (limon >= self.CANDY_RECIPE_COST['limon'] and 
                      huevo >= self.CANDY_RECIPE_COST['huevo'] and 
                      pera >= self.CANDY_RECIPE_COST['pera'])
        can_exchange = (chupetin >= 1)

        if self.game_over:
            if chupetin >= self.objetivo_chupetines:
                consejo = "¡Juego terminado con VICTORIA! Reinicia para una nueva partida."
            else:
                consejo = "El juego ha terminado en DERROTA. Reinicia para intentarlo de nuevo."
        elif chupetin >= self.objetivo_chupetines: # Esto debería ser manejado por check_game_status antes
            consejo = "¡FELICIDADES! Has alcanzado la meta de chupetines. ¡VICTORIA!"
        elif chupetin == self.objetivo_chupetines - 1 and can_create:
            consejo = f"¡Estás a UN {self.emojis['chupetin']} de la VICTORIA! ¡Concéntrate en crearlo!"
        elif not can_create:
            if can_exchange:
                missing_types = [c for c in ['limon', 'huevo', 'pera'] if self.inventario[c] < self.CANDY_RECIPE_COST[c]]
                if missing_types:
                    # Identificar los que más faltan para la receta (ej. si necesitas 2 y solo tienes 0 o 1)
                    really_missing = [c for c in missing_types if self.inventario[c] < self.CANDY_RECIPE_COST[c]]
                    if really_missing:
                         consejo = f"🚨 No puedes crear chupetines. ¡Canjea un {self.emojis['chupetin']} por {self.EXCHANGE_REWARD_AMOUNT} caramelos! Enfócate en reponer los que más te faltan ({', '.join([self.emojis[t] for t in really_missing])})."
                    else: # Este caso es por si can_create es False por algún motivo menor
                        consejo = f"🚨 No puedes crear chupetines. Usa el {self.emojis['chupetin']} para canjearlo por {self.EXCHANGE_REWARD_AMOUNT} de los caramelos que necesites para crear."
            else:
                consejo = "Parece que no hay movimientos posibles. Te faltan caramelos para crear y chupetines para canjear. Considera reiniciar."
        elif can_create:
            consejo_crear = f"Puedes crear un {self.emojis['chupetin']} usando {self.CANDY_RECIPE_COST['limon']}{self.emojis['limon']}, {self.CANDY_RECIPE_COST['huevo']}{self.emojis['huevo']}, {self.CANDY_RECIPE_COST['pera']}{self.emojis['pera']}. ¡Recuerda que también recibes {self.CREATE_REWARD_AMOUNT} caramelos a elegir!"
            
            if min_candy_value < 4 and len(candies_with_min) == 1: # Si solo un tipo está bajo
                 consejo = f"{consejo_crear} Asegúrate de elegir los {self.CREATE_REWARD_AMOUNT} {self.emojis[candies_with_min[0]]} adicionales para reponer tu inventario más escaso."
            else:
                 consejo = consejo_crear
        
        elif can_exchange:
            consejo = f"Tienes {chupetin}{self.emojis['chupetin']}. Canjéalo por {self.EXCHANGE_REWARD_AMOUNT} caramelos de los tipos que más te ayuden a crear más chupetines."
        else:
            consejo = "Evalúa cuidadosamente tu inventario y las acciones disponibles para avanzar hacia el objetivo de chupetines."
        
        return consejo

    def get_rules_text(self):
        """Devuelve el texto de las reglas del juego."""
        rules_text = f"""
**REGLAS DE SUPERVIVENCIA:**

1.  **Objetivo:** Obtener {self.objetivo_chupetines} Chupetines ({self.emojis['chupetin']}). (Varía por dificultad)

2.  **Inventario Inicial:** Varía según la dificultad elegida.

3.  **Acción para OBTENER Chupetines:**
    * **Crear 1 Chupetín (Balanceado y Flexible):**
        * **Costo:** {self.CANDY_RECIPE_COST['limon']} {self.emojis['limon']}, {self.CANDY_RECIPE_COST['huevo']} {self.emojis['huevo']}, {self.CANDY_RECIPE_COST['pera']} {self.emojis['pera']} (total {sum(self.CANDY_RECIPE_COST.values())} caramelos variados).
        * **Recibes:** 1 {self.emojis['chupetin']} **MÁS** {self.CREATE_REWARD_AMOUNT} caramelos **DEL TIPO Y DISTRIBUCIÓN QUE TÚ ELIJAS**.
            * (Ej: puedes elegir {self.CREATE_REWARD_AMOUNT}{self.emojis['limon']}, o 1{self.emojis['limon']} y 1{self.emojis['huevo']}, etc.).

4.  **Acción para ENTREGAR Chupetines (Canje):**
    * **Canjear 1 Chupetín (Grande y Flexible):**
        * **Costo:** 1 {self.emojis['chupetin']}.
        * **Recibes:** **{self.EXCHANGE_REWARD_AMOUNT} caramelos DEL TIPO Y DISTRIBUCIÓN QUE TÚ ELIJAS**.
            * (Ej: puedes elegir {self.EXCHANGE_REWARD_AMOUNT}{self.emojis['pera']}, o 2{self.emojis['limon']}, 2{self.emojis['huevo']}, 2{self.emojis['pera']}, etc.).

5.  **Fin del Juego:**
    * **VICTORIA:** Si alcanzas o superas {self.objetivo_chupetines} {self.emojis['chupetin']}.
    * **DERROTA:** Si no puedes realizar ninguna acción (no puedes crear chupetines Y no tienes chupetines para canjear).

**Modos de Juego:**
* **Jugar Solo:** Juegas por tu cuenta para alcanzar el objetivo.
* **Jugar con Alguien Más (Colaborativo):** Dos jugadores comparten el mismo inventario y se turnan. ¡Trabajen juntos juntos para ganar!

**Estrategia:**
* La clave es gestionar tu inventario para poder siempre crear más chupetines.
* Usa el canje de 1{self.emojis['chupetin']} por {self.EXCHANGE_REWARD_AMOUNT} caramelos cuando un tipo se te esté agotando críticamente y necesites reponerlo rápidamente.
* Al crear, elige los {self.CREATE_REWARD_AMOUNT} caramelos extra que recibes para equilibrar tu inventario o potenciar el tipo que más te haga falta.
* ¡Presta atención a los eventos aleatorios! Pueden ayudarte o complicarte las cosas.
        """
        return rules_text

# --- Inicio de la Aplicación ---
if __name__ == "__main__":
    root = tk.Tk()
    game = CandySurvivalGame(root)
    root.mainloop()