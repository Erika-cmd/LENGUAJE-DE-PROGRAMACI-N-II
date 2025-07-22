import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import tkinter.font as tkFont
import sys
from datetime import datetime, timedelta

# Clases originales
class Libro:        
    def __init__(self, titulo, autor, isbn, editorial="", anio_publicacion=""):          
        self.__titulo, self.__autor, self.__isbn, self.__disponible = titulo, autor, isbn, True          
        self.__editorial = editorial # Nuevo: Editorial
        self.__anio_publicacion = anio_publicacion # Nuevo: Año de publicación
    
    def __del__(self):    
        print(f"[DEL] Libro '{self.__titulo}' eliminado.")          
    
    def reservar(self):    
        self.__disponible = False if self.__disponible else self.__disponible
        return self.__disponible          
    
    def cancelar(self):    
        self.__disponible = True          
    
    def disponible(self):    
        return self.__disponible          
    
    def mostrar(self):    
        print(f"{self.__titulo} | {self.__autor} | ISBN: {self.__isbn} | {'Disponible' if self.__disponible else 'Reservado'}")          
    
    def get_isbn(self):    
        return self.__isbn    
    
    def get_titulo(self):
        return self.__titulo
    
    def get_autor(self):
        return self.__autor
    
    def get_estado(self):
        return 'Disponible' if self.__disponible else 'Reservado'

    def get_editorial(self): # Nuevo: Getter para editorial
        return self.__editorial

    def get_anio_publicacion(self): # Nuevo: Getter para año de publicación
        return self.__anio_publicacion

class Usuario:        
    def __init__(self, nombre, dni, direccion="", telefono=""):    
        self.__nombre, self.__dni = nombre, dni    
        self.__historial = [] # Historial de acciones del usuario
        self.__direccion = direccion # Nuevo: Dirección
        self.__telefono = telefono # Nuevo: Teléfono
    
    def __del__(self):    
        print(f"[DEL] Usuario '{self.__nombre}' eliminado.")          
    
    def mostrar(self):    
        print(f"{self.__nombre} | DNI: {self.__dni}")          
    
    def get_dni(self):    
        return self.__dni    
    
    def get_nombre(self):
        return self.__nombre

    def get_direccion(self): # Nuevo: Getter para dirección
        return self.__direccion
    
    def get_telefono(self): # Nuevo: Getter para teléfono
        return self.__telefono

    # Métodos para historial
    def registrar_historial(self, accion, timestamp):
        self.__historial.append(f"{timestamp}: {accion}")

    def get_historial(self):
        return self.__historial

class Reserva:        
    def __init__(self, libro, usuario, fecha_reserva):    
        self.__libro = libro
        self.__usuario = usuario
        self.__fecha_reserva = fecha_reserva
        self.__fecha_vencimiento = fecha_reserva + timedelta(days=7) # Por ejemplo, 7 días de reserva
    
    def __del__(self):    
        print("[DEL] Reserva eliminada.")          
    
    def mostrar(self):    
        print("== Reserva ==")
        self.__usuario.mostrar()
        self.__libro.mostrar()          
    
    def get_libro(self):    
        return self.__libro
    
    def get_usuario(self):
        return self.__usuario

    def get_fecha_reserva(self): # Nuevo: Getter para fecha de reserva
        return self.__fecha_reserva

    def get_fecha_vencimiento(self): # Nuevo: Getter para fecha de vencimiento
        return self.__fecha_vencimiento

class Biblioteca:        
    def __init__(self):    
        self.__libros, self.__usuarios, self.__reservas = [], [], []            
        self.multa_por_dia = 0.50 # Nuevo: Multa por día de retraso

    def agregar_libro(self, titulo, autor, isbn, editorial="", anio_publicacion=""):            
        l = Libro(titulo, autor, isbn, editorial, anio_publicacion)            
        self.__libros.append(l)
        return l

    def agregar_usuario(self, nombre, dni, direccion="", telefono=""):            
        u = Usuario(nombre, dni, direccion, telefono)            
        self.__usuarios.append(u)
        return u

    def buscar(self, coleccion, clave, metodo):    
        return next((x for x in coleccion if metodo(x) == clave), None)          

    def buscar_usuario_por_dni(self, dni):
        return self.buscar(self.__usuarios, dni, lambda u: u.get_dni())

    def buscar_libro_por_isbn(self, isbn): # Nuevo: Método para buscar libro por ISBN
        return self.buscar(self.__libros, isbn, lambda l: l.get_isbn())

    def reservar_libro(self, isbn, dni):            
        libro = self.buscar_libro_por_isbn(isbn)            
        usuario = self.buscar_usuario_por_dni(dni)            
        if libro and usuario:                  
            if libro.disponible():    
                libro.reservar()
                fecha_actual = datetime.now()
                reserva = Reserva(libro, usuario, fecha_actual)
                self.__reservas.append(reserva)
                timestamp = fecha_actual.strftime("%Y-%m-%d %H:%M:%S")
                usuario.registrar_historial(f"Reservó el libro '{libro.get_titulo()}' (ISBN: {libro.get_isbn()}) - Vence: {reserva.get_fecha_vencimiento().strftime('%Y-%m-%d %H:%M:%S')}", timestamp)
                return True, "[OK] Reservado."                  
            else:    
                return False, "[X] Ya reservado."            
        else:    
            return False, "[!] Libro o usuario no encontrado."          

    def cancelar_reserva(self, isbn):            
        r = next((r for r in self.__reservas if r.get_libro().get_isbn() == isbn), None)            
        if r:    
            # Calcular multa antes de cancelar
            multa = self.calcular_multa(r)
            if multa > 0:
                mensaje_multa = f"Se ha generado una multa de S/. {multa:.2f} por retraso."
                # Aquí podrías agregar lógica para "cobrar" la multa o registrarla
            else:
                mensaje_multa = ""

            r.get_libro().cancelar()
            self.__reservas.remove(r)
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            accion_historial = f"Canceló la reserva del libro '{r.get_libro().get_titulo()}' (ISBN: {r.get_libro().get_isbn()})"
            if mensaje_multa:
                accion_historial += f" - {mensaje_multa}"
            r.get_usuario().registrar_historial(accion_historial, timestamp)
            
            return True, f"[OK] Reserva cancelada. {mensaje_multa}".strip()            
        else:    
            return False, "[X] No se encontró reserva."          

    def calcular_multa(self, reserva): # Nuevo: Método para calcular multa
        fecha_actual = datetime.now()
        fecha_vencimiento = reserva.get_fecha_vencimiento()
        if fecha_actual > fecha_vencimiento:
            dias_retraso = (fecha_actual - fecha_vencimiento).days
            return dias_retraso * self.multa_por_dia
        return 0

    def eliminar_libro(self, isbn): # Nuevo: Método para eliminar libro
        libro = self.buscar_libro_por_isbn(isbn)
        if libro:
            if not libro.disponible():
                return False, "No se puede eliminar un libro reservado. Cancele la reserva primero."
            self.__libros.remove(libro)
            return True, "Libro eliminado correctamente."
        return False, "Libro no encontrado."

    def eliminar_usuario(self, dni): # Nuevo: Método para eliminar usuario
        usuario = self.buscar_usuario_por_dni(dni)
        if usuario:
            # Comprobar si el usuario tiene reservas activas
            reservas_activas = [r for r in self.__reservas if r.get_usuario().get_dni() == dni]
            if reservas_activas:
                return False, "No se puede eliminar un usuario con reservas activas. Cancele sus reservas primero."
            self.__usuarios.remove(usuario)
            return True, "Usuario eliminado correctamente."
        return False, "Usuario no encontrado."

    def get_libros(self, filtro=None):
        if filtro is None:
            return self.__libros
        else:
            return [l for l in self.__libros if filtro(l)]
            
    def get_usuarios(self):
        return self.__usuarios
        
    def get_reservas(self):
        return self.__reservas
    
    def mostrar_libros(self, filtro=None):            
        print("== Lista de libros ==")            
        for l in self.__libros:                  
            if filtro is None or filtro(l):    
                l.mostrar()          

    def menu(self):            
        """Implementación original del menú de consola"""
        opciones = {                  
            "1": lambda: self.agregar_libro(input("Título: "), input("Autor: "), input("ISBN: ")),
            "2": lambda: self.agregar_usuario(input("Nombre: "), input("DNI: ")),
            "3": lambda: self.reservar_libro(input("ISBN: "), input("DNI: ")),
            "4": lambda: self.cancelar_reserva(input("ISBN del libro: ")),
            "5": lambda: self.mostrar_libros(),                  
            "6": lambda: self.mostrar_libros(lambda l: l.disponible()),                  
            "7": lambda: self.mostrar_libros(lambda l: not l.disponible())            
        }          
        while True:                  
            print("\n--- MENÚ ---\n1. Registrar libro\n2. Registrar usuario\n3. Hacer reserva\n4. Cancelar reserva\n5. Ver todos\n6. Libros disponibles\n7. Libros reservados\n0. Salir")                  
            op = input("Opción: ")                  
            if op == "0":    
                print("Adiós.")
                break                  
            opciones.get(op, lambda: print("Opción inválida"))()
            
            # Pausa para que el usuario pueda leer el resultado
            input("\nPresione Enter para continuar...")

# Interfaz gráfica con Tkinter
class BibliotecaApp(tk.Tk):
    def __init__(self):
        super().__init__()
        
        self.biblioteca = Biblioteca()
        self.setup_ui()
        
        # Datos de prueba
        self.cargar_datos_prueba()
        
    def cargar_datos_prueba(self):
        """Carga algunos datos de prueba para demostración"""
        # Libros
        self.biblioteca.agregar_libro("Don Quijote de la Mancha", "Miguel de Cervantes", "9788420412146", "Alfaguara", "1605")
        self.biblioteca.agregar_libro("Cien años de soledad", "Gabriel García Márquez", "9780307474728", "Sudamericana", "1967")
        self.biblioteca.agregar_libro("La sombra del viento", "Carlos Ruiz Zafón", "9788408163381", "Planeta", "2001")
        self.biblioteca.agregar_libro("El señor de los anillos", "J.R.R. Tolkien", "9788445071720", "Minotauro", "1954")
        
        # Usuarios
        ana = self.biblioteca.agregar_usuario("Ana García", "12345678A", "Calle Falsa 123", "555-1111")
        juan = self.biblioteca.agregar_usuario("Juan Pérez", "87654321B", "Avenida Siempre Viva 45", "555-2222")
        maria = self.biblioteca.agregar_usuario("Maria Lopez", "11223344C", "Plaza Mayor 5", "555-3333")
        
        # Registrar algunas acciones para el historial
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ana.registrar_historial("Se registró en el sistema", timestamp)
        juan.registrar_historial("Se registró en el sistema", timestamp)
        maria.registrar_historial("Se registró en el sistema", timestamp)

        # Actualizar vistas
        self.actualizar_vista_libros()
        self.actualizar_vista_usuarios()
        self.actualizar_combobox_usuarios() # Asegurar que el combobox de historial se carga
    
    def setup_ui(self):
        """Configura la interfaz de usuario"""
        self.title("Sistema de Gestión de Biblioteca")
        self.geometry("1000x700") # Aumentar tamaño para nuevas columnas
        self.minsize(1000, 700)
        
        # Fuentes
        self.title_font = tkFont.Font(family="Helvetica", size=14, weight="bold")
        self.subtitle_font = tkFont.Font(family="Helvetica", size=12, weight="bold")
        
        # Notebook (pestañas)
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)
        
        # ******************************************************************
        # CORRECCIÓN DE ERROR: Inicializar status_bar antes de crear las pestañas
        # para que esté disponible cuando se usen métodos que lo actualicen.
        # ******************************************************************
        self.status_bar = tk.Label(self, text="Sistema de Gestión de Biblioteca - Listo", bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Crear pestañas
        self.tab_libros = ttk.Frame(self.notebook)
        self.tab_usuarios = ttk.Frame(self.notebook)
        self.tab_reservas = ttk.Frame(self.notebook)
        self.tab_historial = ttk.Frame(self.notebook)
        
        self.notebook.add(self.tab_libros, text="Libros")
        self.notebook.add(self.tab_usuarios, text="Usuarios")
        self.notebook.add(self.tab_reservas, text="Reservas")
        self.notebook.add(self.tab_historial, text="Historial de Usuarios")
        
        # Configurar pestañas
        self.setup_tab_libros()
        self.setup_tab_usuarios()
        self.setup_tab_reservas()
        self.setup_tab_historial()
        
    def setup_tab_libros(self):
        """Configura la pestaña de Libros"""
        main_frame = ttk.Frame(self.tab_libros)
        main_frame.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)
        
        left_frame = ttk.LabelFrame(main_frame, text="Catálogo de Libros")
        left_frame.pack(side=tk.LEFT, expand=True, fill=tk.BOTH, padx=5, pady=5)
        
        columns = ("titulo", "autor", "isbn", "editorial", "anio_publicacion", "estado") # Nuevas columnas
        self.libros_tree = ttk.Treeview(left_frame, columns=columns, show="headings")
        
        self.libros_tree.heading("titulo", text="Título")
        self.libros_tree.heading("autor", text="Autor")
        self.libros_tree.heading("isbn", text="ISBN")
        self.libros_tree.heading("editorial", text="Editorial") # Nueva heading
        self.libros_tree.heading("anio_publicacion", text="Año") # Nueva heading
        self.libros_tree.heading("estado", text="Estado")
        
        self.libros_tree.column("titulo", width=200)
        self.libros_tree.column("autor", width=150)
        self.libros_tree.column("isbn", width=120)
        self.libros_tree.column("editorial", width=100) # Ancho para nueva columna
        self.libros_tree.column("anio_publicacion", width=60, anchor=tk.CENTER) # Ancho para nueva columna
        self.libros_tree.column("estado", width=80)
        
        scrollbar = ttk.Scrollbar(left_frame, orient=tk.VERTICAL, command=self.libros_tree.yview)
        self.libros_tree.configure(yscrollcommand=scrollbar.set)
        
        self.libros_tree.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        right_frame = ttk.Frame(main_frame)
        right_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=5, pady=5)
        
        ttk.Label(right_frame, text="Gestión de Libros", font=self.title_font).pack(pady=10)
        
        filter_frame = ttk.LabelFrame(right_frame, text="Filtrar Libros")
        filter_frame.pack(fill=tk.X, pady=5)
        
        ttk.Button(filter_frame, text="Todos", command=lambda: self.actualizar_vista_libros()).pack(fill=tk.X, padx=5, pady=2)
        ttk.Button(filter_frame, text="Disponibles", command=lambda: self.actualizar_vista_libros(lambda l: l.disponible())).pack(fill=tk.X, padx=5, pady=2)
        ttk.Button(filter_frame, text="Reservados", command=lambda: self.actualizar_vista_libros(lambda l: not l.disponible())).pack(fill=tk.X, padx=5, pady=2)
        
        # Búsqueda de libros
        search_book_frame = ttk.LabelFrame(right_frame, text="Buscar Libro")
        search_book_frame.pack(fill=tk.X, pady=5)
        self.search_book_entry = ttk.Entry(search_book_frame, width=30)
        self.search_book_entry.pack(side=tk.LEFT, padx=5, pady=2, expand=True, fill=tk.X)
        ttk.Button(search_book_frame, text="Buscar", command=self.buscar_libro_gui).pack(side=tk.LEFT, padx=5, pady=2)

        actions_frame = ttk.LabelFrame(right_frame, text="Acciones de Libros")
        actions_frame.pack(fill=tk.X, pady=10)
        
        ttk.Button(actions_frame, text="Añadir Libro", command=self.mostrar_dialogo_nuevo_libro).pack(fill=tk.X, padx=5, pady=2)
        ttk.Button(actions_frame, text="Eliminar Libro", command=self.eliminar_libro_seleccionado).pack(fill=tk.X, padx=5, pady=2)
        ttk.Button(actions_frame, text="Reservar Libro", command=self.mostrar_dialogo_reservar_libro).pack(fill=tk.X, padx=5, pady=2)
        ttk.Button(actions_frame, text="Cancelar Reserva", command=self.mostrar_dialogo_cancelar_reserva).pack(fill=tk.X, padx=5, pady=2)
    
    def setup_tab_usuarios(self):
        """Configura la pestaña de Usuarios"""
        main_frame = ttk.Frame(self.tab_usuarios)
        main_frame.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)
        
        left_frame = ttk.LabelFrame(main_frame, text="Lista de Usuarios")
        left_frame.pack(side=tk.LEFT, expand=True, fill=tk.BOTH, padx=5, pady=5)
        
        columns = ("nombre", "dni", "direccion", "telefono") # Nuevas columnas
        self.usuarios_tree = ttk.Treeview(left_frame, columns=columns, show="headings")
        
        self.usuarios_tree.heading("nombre", text="Nombre")
        self.usuarios_tree.heading("dni", text="DNI")
        self.usuarios_tree.heading("direccion", text="Dirección") # Nueva heading
        self.usuarios_tree.heading("telefono", text="Teléfono") # Nueva heading
        
        self.usuarios_tree.column("nombre", width=200)
        self.usuarios_tree.column("dni", width=100)
        self.usuarios_tree.column("direccion", width=200) # Ancho para nueva columna
        self.usuarios_tree.column("telefono", width=100) # Ancho para nueva columna
        
        scrollbar = ttk.Scrollbar(left_frame, orient=tk.VERTICAL, command=self.usuarios_tree.yview)
        self.usuarios_tree.configure(yscrollcommand=scrollbar.set)
        
        self.usuarios_tree.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        right_frame = ttk.Frame(main_frame)
        right_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=5, pady=5)
        
        ttk.Label(right_frame, text="Gestión de Usuarios", font=self.title_font).pack(pady=10)

        # Búsqueda de usuarios
        search_user_frame = ttk.LabelFrame(right_frame, text="Buscar Usuario")
        search_user_frame.pack(fill=tk.X, pady=5)
        self.search_user_entry = ttk.Entry(search_user_frame, width=30)
        self.search_user_entry.pack(side=tk.LEFT, padx=5, pady=2, expand=True, fill=tk.X)
        ttk.Button(search_user_frame, text="Buscar", command=self.buscar_usuario_gui).pack(side=tk.LEFT, padx=5, pady=2)
        
        actions_frame = ttk.LabelFrame(right_frame, text="Acciones de Usuarios")
        actions_frame.pack(fill=tk.X, pady=10)
        
        ttk.Button(actions_frame, text="Añadir Usuario", command=self.mostrar_dialogo_nuevo_usuario).pack(fill=tk.X, padx=5, pady=2)
        ttk.Button(actions_frame, text="Eliminar Usuario", command=self.eliminar_usuario_seleccionado).pack(fill=tk.X, padx=5, pady=2)
    
    def setup_tab_reservas(self):
        """Configura la pestaña de Reservas"""
        main_frame = ttk.Frame(self.tab_reservas)
        main_frame.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)
        
        ttk.Label(main_frame, text="Gestión de Reservas", font=self.title_font).pack(pady=10)
        
        columns = ("titulo", "isbn", "usuario", "dni", "fecha_reserva", "fecha_vencimiento", "multa_estimada") # Nuevas columnas para fechas y multa
        self.reservas_tree = ttk.Treeview(main_frame, columns=columns, show="headings")
        
        self.reservas_tree.heading("titulo", text="Título del Libro")
        self.reservas_tree.heading("isbn", text="ISBN")
        self.reservas_tree.heading("usuario", text="Usuario")
        self.reservas_tree.heading("dni", text="DNI")
        self.reservas_tree.heading("fecha_reserva", text="Fecha Reserva") # Nueva heading
        self.reservas_tree.heading("fecha_vencimiento", text="Fecha Vencimiento") # Nueva heading
        self.reservas_tree.heading("multa_estimada", text="Multa Estimada") # Nueva heading (mostramos S/.0.00 si no hay multa)
        
        self.reservas_tree.column("titulo", width=180)
        self.reservas_tree.column("isbn", width=100)
        self.reservas_tree.column("usuario", width=120)
        self.reservas_tree.column("dni", width=90)
        self.reservas_tree.column("fecha_reserva", width=130, anchor=tk.CENTER) # Ancho para nueva columna
        self.reservas_tree.column("fecha_vencimiento", width=140, anchor=tk.CENTER) # Ancho para nueva columna
        self.reservas_tree.column("multa_estimada", width=100, anchor=tk.CENTER) # Ancho para nueva columna
        
        scrollbar = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=self.reservas_tree.yview)
        self.reservas_tree.configure(yscrollcommand=scrollbar.set)
        
        self.reservas_tree.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        actions_frame = ttk.Frame(main_frame)
        actions_frame.pack(fill=tk.X, pady=10)
        
        ttk.Button(actions_frame, text="Actualizar Reservas", command=self.actualizar_vista_reservas).pack(side=tk.LEFT, padx=5)
        ttk.Button(actions_frame, text="Cancelar Reserva Seleccionada", command=self.cancelar_reserva_seleccionada).pack(side=tk.LEFT, padx=5)
        ttk.Button(actions_frame, text="Ver Multas Pendientes", command=self.mostrar_multas_pendientes).pack(side=tk.LEFT, padx=5) # Nuevo botón
    
    def setup_tab_historial(self):
        """Configura la pestaña de Historial de Usuarios"""
        main_frame = ttk.Frame(self.tab_historial)
        main_frame.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)

        ttk.Label(main_frame, text="Historial de Actividad de Usuarios", font=self.title_font).pack(pady=10)

        user_select_frame = ttk.LabelFrame(main_frame, text="Seleccionar Usuario")
        user_select_frame.pack(fill=tk.X, pady=5)

        self.selected_user_dni = tk.StringVar()
        self.user_combobox = ttk.Combobox(user_select_frame, textvariable=self.selected_user_dni, state="readonly")
        self.user_combobox.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=5, pady=5)
        self.user_combobox.bind("<<ComboboxSelected>>", self.on_user_selected_for_history)

        ttk.Button(user_select_frame, text="Mostrar Historial", command=self.mostrar_historial_usuario).pack(side=tk.LEFT, padx=5)

        columns = ("historial_entry",)
        self.historial_tree = ttk.Treeview(main_frame, columns=columns, show="headings")
        self.historial_tree.heading("historial_entry", text="Actividad")
        self.historial_tree.column("historial_entry", width=600)
        
        scrollbar = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=self.historial_tree.yview)
        self.historial_tree.configure(yscrollcommand=scrollbar.set)

        self.historial_tree.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.actualizar_combobox_usuarios()

    def actualizar_combobox_usuarios(self):
        """Actualiza el combobox de usuarios para el historial"""
        usuarios = self.biblioteca.get_usuarios()
        self.user_combobox['values'] = [f"{u.get_nombre()} ({u.get_dni()})" for u in usuarios]
        if usuarios:
            self.user_combobox.set(self.user_combobox['values'][0])
            self.on_user_selected_for_history(None)
        else:
            self.user_combobox.set("")
            self.user_combobox['values'] = []
            self.actualizar_vista_historial(None) # Limpiar historial si no hay usuarios

    # Métodos para actualizar vistas
    def actualizar_vista_libros(self, filtro=None):
        """Actualiza la vista de libros"""
        for i in self.libros_tree.get_children():
            self.libros_tree.delete(i)
        
        libros = self.biblioteca.get_libros(filtro)
        
        for libro in libros:
            self.libros_tree.insert('', tk.END, values=(
                libro.get_titulo(),
                libro.get_autor(),
                libro.get_isbn(),
                libro.get_editorial(), # Nuevo
                libro.get_anio_publicacion(), # Nuevo
                libro.get_estado()
            ))
        
        self.status_bar.config(text=f"Mostrando {len(libros)} libros")
    
    def actualizar_vista_usuarios(self):
        """Actualiza la vista de usuarios"""
        for i in self.usuarios_tree.get_children():
            self.usuarios_tree.delete(i)
        
        usuarios = self.biblioteca.get_usuarios()
        
        for usuario in usuarios:
            self.usuarios_tree.insert('', tk.END, values=(
                usuario.get_nombre(),
                usuario.get_dni(),
                usuario.get_direccion(), # Nuevo
                usuario.get_telefono() # Nuevo
            ))
        
        self.status_bar.config(text=f"Mostrando {len(usuarios)} usuarios")
        self.actualizar_combobox_usuarios()
    
    def actualizar_vista_reservas(self):
        """Actualiza la vista de reservas"""
        for i in self.reservas_tree.get_children():
            self.reservas_tree.delete(i)
        
        reservas = self.biblioteca.get_reservas()
        
        for reserva in reservas:
            libro = reserva.get_libro()
            usuario = reserva.get_usuario()
            multa = self.biblioteca.calcular_multa(reserva)
            
            self.reservas_tree.insert('', tk.END, values=(
                libro.get_titulo(),
                libro.get_isbn(),
                usuario.get_nombre(),
                usuario.get_dni(),
                reserva.get_fecha_reserva().strftime("%Y-%m-%d %H:%M:%S"), # Formatear fecha
                reserva.get_fecha_vencimiento().strftime("%Y-%m-%d %H:%M:%S"), # Formatear fecha
                f"S/. {multa:.2f}" if multa > 0 else "S/. 0.00" # Mostrar multa
            ))
        
        self.status_bar.config(text=f"Mostrando {len(reservas)} reservas")

    def actualizar_vista_historial(self, usuario):
        """Actualiza la vista del historial para un usuario dado"""
        for i in self.historial_tree.get_children():
            self.historial_tree.delete(i)

        if usuario:
            for entrada in usuario.get_historial():
                self.historial_tree.insert('', tk.END, values=(entrada,))
            self.status_bar.config(text=f"Mostrando historial para {usuario.get_nombre()}")
        else:
            self.status_bar.config(text="No se ha seleccionado un usuario para el historial o no hay historial")

    def on_user_selected_for_history(self, event):
        """Cuando un usuario es seleccionado en el combobox del historial"""
        self.mostrar_historial_usuario()

    def mostrar_historial_usuario(self):
        """Muestra el historial del usuario seleccionado en la pestaña de historial"""
        selected_text = self.selected_user_dni.get()
        if not selected_text:
            self.actualizar_vista_historial(None)
            return

        dni_start = selected_text.rfind('(') + 1
        dni_end = selected_text.rfind(')')
        selected_dni = selected_text[dni_start:dni_end]

        usuario = self.biblioteca.buscar_usuario_por_dni(selected_dni)
        if usuario:
            self.actualizar_vista_historial(usuario)
        else:
            messagebox.showerror("Error", "Usuario no encontrado para el historial.")
            self.actualizar_vista_historial(None)
    
    # Diálogos y acciones
    def mostrar_dialogo_nuevo_libro(self):
        dialogo = DialogoNuevoLibro(self)
        if dialogo.result:
            titulo, autor, isbn, editorial, anio_publicacion = dialogo.result
            libro = self.biblioteca.agregar_libro(titulo, autor, isbn, editorial, anio_publicacion)
            if libro:
                messagebox.showinfo("Éxito", "Libro registrado correctamente")
                self.actualizar_vista_libros()
            else:
                messagebox.showerror("Error", "No se pudo registrar el libro")
    
    def eliminar_libro_seleccionado(self): # Nuevo método
        seleccion = self.libros_tree.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "No hay libro seleccionado para eliminar.")
            return
        
        item = self.libros_tree.item(seleccion[0])
        isbn = item['values'][2] # ISBN está en la posición 2
        
        if messagebox.askyesno("Confirmar Eliminación", f"¿Está seguro de que desea eliminar el libro con ISBN: {isbn}?"):
            exito, mensaje = self.biblioteca.eliminar_libro(isbn)
            if exito:
                messagebox.showinfo("Éxito", mensaje)
                self.actualizar_vista_libros()
                self.actualizar_vista_reservas() # Por si la eliminación afecta reservas (aunque ya se comprueba)
            else:
                messagebox.showerror("Error", mensaje)

    def buscar_libro_gui(self): # Nuevo método
        query = self.search_book_entry.get().strip().lower()
        if not query:
            self.actualizar_vista_libros() # Mostrar todos si la búsqueda está vacía
            return

        def filtro_busqueda(libro):
            return (query in libro.get_titulo().lower() or
                    query in libro.get_autor().lower() or
                    query in libro.get_isbn().lower() or
                    query in libro.get_editorial().lower())

        self.actualizar_vista_libros(filtro_busqueda)
        if not self.libros_tree.get_children():
            self.status_bar.config(text=f"No se encontraron libros para '{query}'")
        else:
            self.status_bar.config(text=f"Mostrando resultados de búsqueda para '{query}'")

    def mostrar_dialogo_nuevo_usuario(self):
        dialogo = DialogoNuevoUsuario(self)
        if dialogo.result:
            nombre, dni, direccion, telefono = dialogo.result
            usuario = self.biblioteca.agregar_usuario(nombre, dni, direccion, telefono)
            if usuario:
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                usuario.registrar_historial("Se registró en el sistema", timestamp)
                messagebox.showinfo("Éxito", "Usuario registrado correctamente")
                self.actualizar_vista_usuarios()
            else:
                messagebox.showerror("Error", "No se pudo registrar el usuario")

    def eliminar_usuario_seleccionado(self): # Nuevo método
        seleccion = self.usuarios_tree.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "No hay usuario seleccionado para eliminar.")
            return
        
        item = self.usuarios_tree.item(seleccion[0])
        dni = item['values'][1] # DNI está en la posición 1
        nombre = item['values'][0]

        if messagebox.askyesno("Confirmar Eliminación", f"¿Está seguro de que desea eliminar al usuario {nombre} (DNI: {dni})?"):
            exito, mensaje = self.biblioteca.eliminar_usuario(dni)
            if exito:
                messagebox.showinfo("Éxito", mensaje)
                self.actualizar_vista_usuarios()
                self.actualizar_vista_reservas() # Por si la eliminación afecta reservas (aunque ya se comprueba)
            else:
                messagebox.showerror("Error", mensaje)

    def buscar_usuario_gui(self): # Nuevo método
        query = self.search_user_entry.get().strip().lower()
        if not query:
            self.actualizar_vista_usuarios()
            return
        
        # Filtrar la lista de usuarios para mostrar solo los que coinciden con la búsqueda
        # Limpiar vista actual
        for i in self.usuarios_tree.get_children():
            self.usuarios_tree.delete(i)
        
        usuarios_filtrados = [u for u in self.biblioteca.get_usuarios() if 
                              query in u.get_nombre().lower() or 
                              query in u.get_dni().lower() or
                              query in u.get_direccion().lower() or
                              query in u.get_telefono().lower()]
        
        for usuario in usuarios_filtrados:
            self.usuarios_tree.insert('', tk.END, values=(
                usuario.get_nombre(),
                usuario.get_dni(),
                usuario.get_direccion(),
                usuario.get_telefono()
            ))

        if not self.usuarios_tree.get_children():
            self.status_bar.config(text=f"No se encontraron usuarios para '{query}'")
        else:
            self.status_bar.config(text=f"Mostrando resultados de búsqueda para '{query}'")

    def mostrar_dialogo_reservar_libro(self):
        dialogo = DialogoReservarLibro(self)
        if dialogo.result:
            isbn, dni = dialogo.result
            exito, mensaje = self.biblioteca.reservar_libro(isbn, dni)
            if exito:
                messagebox.showinfo("Éxito", mensaje)
                self.actualizar_vista_libros()
                self.actualizar_vista_reservas()
                # Asegurarse de que el historial del usuario se actualice en la vista
                usuario_afectado = self.biblioteca.buscar_usuario_por_dni(dni)
                if self.selected_user_dni.get() and usuario_afectado and usuario_afectado.get_dni() in self.selected_user_dni.get():
                     self.actualizar_vista_historial(usuario_afectado)
            else:
                messagebox.showerror("Error", mensaje)
    
    def mostrar_dialogo_cancelar_reserva(self):
        isbn = simpledialog.askstring("Cancelar Reserva", "ISBN del libro a cancelar:")
        if isbn:
            reserva_a_cancelar = next((r for r in self.biblioteca.get_reservas() if r.get_libro().get_isbn() == isbn), None)
            usuario_dni = reserva_a_cancelar.get_usuario().get_dni() if reserva_a_cancelar else None

            exito, mensaje = self.biblioteca.cancelar_reserva(isbn)
            if exito:
                messagebox.showinfo("Éxito", mensaje)
                self.actualizar_vista_libros()
                self.actualizar_vista_reservas()
                if usuario_dni:
                    usuario_afectado = self.biblioteca.buscar_usuario_por_dni(usuario_dni)
                    if self.selected_user_dni.get() and usuario_afectado and usuario_afectado.get_dni() in self.selected_user_dni.get():
                        self.actualizar_vista_historial(usuario_afectado)
            else:
                messagebox.showerror("Error", mensaje)
    
    def cancelar_reserva_seleccionada(self):
        seleccion = self.reservas_tree.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "No hay reserva seleccionada")
            return
        
        item = self.reservas_tree.item(seleccion[0])
        isbn = item['values'][1]
        dni_usuario = item['values'][3]
        
        exito, mensaje = self.biblioteca.cancelar_reserva(isbn)
        if exito:
            messagebox.showinfo("Éxito", mensaje)
            self.actualizar_vista_libros()
            self.actualizar_vista_reservas()
            usuario_afectado = self.biblioteca.buscar_usuario_por_dni(dni_usuario)
            if self.selected_user_dni.get() and usuario_afectado and usuario_afectado.get_dni() in self.selected_user_dni.get():
                self.actualizar_vista_historial(usuario_afectado)
        else:
            messagebox.showerror("Error", mensaje)

    def mostrar_multas_pendientes(self): # Nuevo método
        multas_info = []
        total_multas = 0
        for reserva in self.biblioteca.get_reservas():
            multa = self.biblioteca.calcular_multa(reserva)
            if multa > 0:
                multas_info.append(f"Libro: '{reserva.get_libro().get_titulo()}' (ISBN: {reserva.get_libro().get_isbn()})\n"
                                   f"Usuario: {reserva.get_usuario().get_nombre()} (DNI: {reserva.get_usuario().get_dni()})\n"
                                   f"Fecha Vencimiento: {reserva.get_fecha_vencimiento().strftime('%Y-%m-%d %H:%M:%S')}\n"
                                   f"Multa: S/. {multa:.2f}\n"
                                   "--------------------")
                total_multas += multa
        
        if multas_info:
            messagebox.showwarning("Multas Pendientes", "\n".join(multas_info) + f"\nTotal de Multas: S/. {total_multas:.2f}")
        else:
            messagebox.showinfo("Multas Pendientes", "No hay multas pendientes en este momento.")

# Diálogos personalizados
class DialogoNuevoLibro(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        
        self.parent = parent
        self.result = None
        
        self.title("Nuevo Libro")
        self.geometry("350x250") # Aumentar tamaño
        self.resizable(False, False)
        self.transient(parent)
        self.grab_set()
        
        # Campos
        ttk.Label(self, text="Título:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.titulo_entry = ttk.Entry(self, width=35)
        self.titulo_entry.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(self, text="Autor:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        self.autor_entry = ttk.Entry(self, width=35)
        self.autor_entry.grid(row=1, column=1, padx=5, pady=5)
        
        ttk.Label(self, text="ISBN:").grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
        self.isbn_entry = ttk.Entry(self, width=35)
        self.isbn_entry.grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(self, text="Editorial:").grid(row=3, column=0, padx=5, pady=5, sticky=tk.W)
        self.editorial_entry = ttk.Entry(self, width=35)
        self.editorial_entry.grid(row=3, column=1, padx=5, pady=5)

        ttk.Label(self, text="Año Publicación:").grid(row=4, column=0, padx=5, pady=5, sticky=tk.W)
        self.anio_publicacion_entry = ttk.Entry(self, width=35)
        self.anio_publicacion_entry.grid(row=4, column=1, padx=5, pady=5)
        
        # Botones
        btn_frame = ttk.Frame(self)
        btn_frame.grid(row=5, column=0, columnspan=2, pady=10)
        
        ttk.Button(btn_frame, text="Guardar", command=self.guardar).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Cancelar", command=self.cancelar).pack(side=tk.LEFT, padx=5)
        
        self.center_window()
        self.wait_window()
    
    def guardar(self):
        titulo = self.titulo_entry.get().strip()
        autor = self.autor_entry.get().strip()
        isbn = self.isbn_entry.get().strip()
        editorial = self.editorial_entry.get().strip()
        anio_publicacion = self.anio_publicacion_entry.get().strip()
        
        if not titulo or not autor or not isbn:
            messagebox.showerror("Error", "Los campos Título, Autor e ISBN son obligatorios")
            return
        
        self.result = (titulo, autor, isbn, editorial, anio_publicacion)
        self.destroy()
    
    def cancelar(self):
        self.destroy()
    
    def center_window(self):
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.parent.winfo_width() // 2) - (width // 2) + self.parent.winfo_x()
        y = (self.parent.winfo_height() // 2) - (height // 2) + self.parent.winfo_y()
        self.geometry(f'{width}x{height}+{x}+{y}')

class DialogoNuevoUsuario(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        
        self.parent = parent
        self.result = None
        
        self.title("Nuevo Usuario")
        self.geometry("350x250") # Aumentar tamaño
        self.resizable(False, False)
        self.transient(parent)
        self.grab_set()
        
        # Campos
        ttk.Label(self, text="Nombre:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.nombre_entry = ttk.Entry(self, width=35)
        self.nombre_entry.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(self, text="DNI:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        self.dni_entry = ttk.Entry(self, width=35)
        self.dni_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(self, text="Dirección:").grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
        self.direccion_entry = ttk.Entry(self, width=35)
        self.direccion_entry.grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(self, text="Teléfono:").grid(row=3, column=0, padx=5, pady=5, sticky=tk.W)
        self.telefono_entry = ttk.Entry(self, width=35)
        self.telefono_entry.grid(row=3, column=1, padx=5, pady=5)
        
        # Botones
        btn_frame = ttk.Frame(self)
        btn_frame.grid(row=4, column=0, columnspan=2, pady=10)
        
        ttk.Button(btn_frame, text="Guardar", command=self.guardar).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Cancelar", command=self.cancelar).pack(side=tk.LEFT, padx=5)
        
        self.center_window()
        self.wait_window()
    
    def guardar(self):
        nombre = self.nombre_entry.get().strip()
        dni = self.dni_entry.get().strip()
        direccion = self.direccion_entry.get().strip()
        telefono = self.telefono_entry.get().strip()
        
        if not nombre or not dni:
            messagebox.showerror("Error", "Los campos Nombre y DNI son obligatorios")
            return
        
        self.result = (nombre, dni, direccion, telefono)
        self.destroy()
    
    def cancelar(self):
        self.destroy()
    
    def center_window(self):
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.parent.winfo_width() // 2) - (width // 2) + self.parent.winfo_x()
        y = (self.parent.winfo_height() // 2) - (height // 2) + self.parent.winfo_y()
        self.geometry(f'{width}x{height}+{x}+{y}')

class DialogoReservarLibro(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        
        self.parent = parent
        self.result = None
        
        self.title("Reservar Libro")
        self.geometry("300x150")
        self.resizable(False, False)
        self.transient(parent)
        self.grab_set()
        
        # Campos
        ttk.Label(self, text="ISBN:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.isbn_entry = ttk.Entry(self, width=30)
        self.isbn_entry.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(self, text="DNI del Usuario:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        self.dni_entry = ttk.Entry(self, width=30)
        self.dni_entry.grid(row=1, column=1, padx=5, pady=5)
        
        # Botones
        btn_frame = ttk.Frame(self)
        btn_frame.grid(row=2, column=0, columnspan=2, pady=10)
        
        ttk.Button(btn_frame, text="Reservar", command=self.reservar).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Cancelar", command=self.cancelar).pack(side=tk.LEFT, padx=5)
        
        self.center_window()
        self.wait_window()
    
    def reservar(self):
        isbn = self.isbn_entry.get().strip()
        dni = self.dni_entry.get().strip()
        
        if not isbn or not dni:
            messagebox.showerror("Error", "Todos los campos son obligatorios")
            return
        
        self.result = (isbn, dni)
        self.destroy()
    
    def cancelar(self):
        self.destroy()
    
    def center_window(self):
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.parent.winfo_width() // 2) - (width // 2) + self.parent.winfo_x()
        y = (self.parent.winfo_height() // 2) - (height // 2) + self.parent.winfo_y()
        self.geometry(f'{width}x{height}+{x}+{y}')

# === MAIN ===
if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--console":
        Biblioteca().menu()
    else:
        app = BibliotecaApp()
        style = ttk.Style()
        style.theme_use('clam')
        
        # Colores más sutiles y decentes
        # Fondo general de la aplicación y pestañas
        style.configure('.', background='#e0e0e0', foreground='#333333') # Gris claro
        style.configure('TFrame', background='#e0e0e0')
        style.configure('TLabel', background='#e0e0e0', foreground='#333333')
        style.configure('TLabelframe', background='#e0e0e0', foreground='#333333')
        style.configure('TLabelframe.Label', background='#e0e0e0', foreground='#333333')

        # Botones
        style.configure('TButton', 
                        background='#607D8B', # Azul grisáceo
                        foreground='white',
                        font=('Helvetica', 10, 'bold'),
                        borderwith=1,
                        relief='raised')
        style.map('TButton',  
                  background=[('active', '#78909C'), ('pressed', '#455A64')], # Tonalidades más oscuras al interactuar
                  foreground=[('active', 'white'), ('pressed', 'white')])

        # Notebook (pestañas)
        style.configure('TNotebook', background='#c0c0c0') # Gris medio para el fondo de las pestañas
        style.configure('TNotebook.Tab', 
                        background='#90A4AE', # Azul grisáceo claro para pestañas inactivas
                        foreground='#333333',
                        font=('Helvetica', 10, 'bold'))
        style.map('TNotebook.Tab', 
                  background=[('selected', '#607D8B')], # Azul grisáceo para pestaña activa
                  foreground=[('selected', 'white')])

        # Treeview (para listas de datos)
        style.configure("Treeview",
                        background="#FFFFFF", # Blanco para el fondo de las filas
                        foreground="#333333",
                        rowheight=25,
                        fieldbackground="#FFFFFF")
        style.map('Treeview',
                  background=[('selected', '#A7D9EF')]) # Azul claro al seleccionar

        style.configure("Treeview.Heading",
                        background="#B0BEC5", # Gris azulado para los encabezados
                        foreground="#333333",
                        font=('Helvetica', 10, 'bold'))
        style.map("Treeview.Heading",
                  background=[('active','#90A4AE')])

        app.mainloop()