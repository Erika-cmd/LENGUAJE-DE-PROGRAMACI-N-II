import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import tkinter.font as tkFont
import sys
from datetime import datetime # Importar datetime para fecha y hora

# Clases originales
class Libro:        
    def __init__(self, titulo, autor, isbn):          
        self.__titulo, self.__autor, self.__isbn, self.__disponible = titulo, autor, isbn, True          
    
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

class Usuario:        
    def __init__(self, nombre, dni):    
        self.__nombre, self.__dni = nombre, dni    
        self.__historial = [] # Nuevo: historial de acciones del usuario
    
    def __del__(self):    
        print(f"[DEL] Usuario '{self.__nombre}' eliminado.")          
    
    def mostrar(self):    
        print(f"{self.__nombre} | DNI: {self.__dni}")          
    
    def get_dni(self):    
        return self.__dni    
    
    def get_nombre(self):
        return self.__nombre

    # Nuevo: Métodos para historial
    def registrar_historial(self, accion, timestamp):
        self.__historial.append(f"{timestamp}: {accion}")

    def get_historial(self):
        return self.__historial

class Reserva:        
    def __init__(self, libro, usuario):    
        self.__libro, self.__usuario = libro, usuario    
    
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

class Biblioteca:        
    def __init__(self):    
        self.__libros, self.__usuarios, self.__reservas = [], [], []            

    def agregar_libro(self, titulo, autor, isbn):            
        l = Libro(titulo, autor, isbn)            
        self.__libros.append(l)
        return l

    def agregar_usuario(self, nombre, dni):            
        u = Usuario(nombre, dni)            
        self.__usuarios.append(u)
        return u

    def buscar(self, coleccion, clave, metodo):    
        return next((x for x in coleccion if metodo(x) == clave), None)          

    def buscar_usuario_por_dni(self, dni):
        return self.buscar(self.__usuarios, dni, lambda u: u.get_dni())

    def reservar_libro(self, isbn, dni):            
        libro = self.buscar(self.__libros, isbn, lambda l: l.get_isbn())            
        usuario = self.buscar_usuario_por_dni(dni) # Usar el nuevo método            
        if libro and usuario:                  
            if libro.disponible():    
                libro.reservar()
                reserva = Reserva(libro, usuario)
                self.__reservas.append(reserva)
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                usuario.registrar_historial(f"Reservó el libro '{libro.get_titulo()}' (ISBN: {libro.get_isbn()})", timestamp)
                return True, "[OK] Reservado."                  
            else:    
                return False, "[X] Ya reservado."            
        else:    
            return False, "[!] Libro o usuario no encontrado."          

    def cancelar_reserva(self, isbn):            
        r = next((r for r in self.__reservas if r.get_libro().get_isbn() == isbn), None)            
        if r:    
            r.get_libro().cancelar()
            self.__reservas.remove(r)
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            r.get_usuario().registrar_historial(f"Canceló la reserva del libro '{r.get_libro().get_titulo()}' (ISBN: {r.get_libro().get_isbn()})", timestamp)
            return True, "[OK] Reserva cancelada."            
        else:    
            return False, "[X] No se encontró reserva."          

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
        self.biblioteca.agregar_libro("Don Quijote", "Miguel de Cervantes", "9788420412146")
        self.biblioteca.agregar_libro("Cien años de soledad", "Gabriel García Márquez", "9780307474728")
        self.biblioteca.agregar_libro("La sombra del viento", "Carlos Ruiz Zafón", "9788408163381")
        
        # Usuarios
        ana = self.biblioteca.agregar_usuario("Ana García", "12345678A")
        juan = self.biblioteca.agregar_usuario("Juan Pérez", "87654321B")
        
        # Registrar algunas acciones para el historial
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ana.registrar_historial("Se registró en el sistema", timestamp)
        juan.registrar_historial("Se registró en el sistema", timestamp)

        # Actualizar vistas
        self.actualizar_vista_libros()
        self.actualizar_vista_usuarios()
    
    def setup_ui(self):
        """Configura la interfaz de usuario"""
        self.title("Biblioteca Virtual")
        self.geometry("900x600")
        self.minsize(900, 600)
        
        # Fuentes
        self.title_font = tkFont.Font(family="Helvetica", size=14, weight="bold")
        self.subtitle_font = tkFont.Font(family="Helvetica", size=12, weight="bold")
        
        # Notebook (pestañas)
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)
        
        # Crear pestañas
        self.tab_libros = ttk.Frame(self.notebook)
        self.tab_usuarios = ttk.Frame(self.notebook)
        self.tab_reservas = ttk.Frame(self.notebook)
        self.tab_historial = ttk.Frame(self.notebook) # Nueva pestaña para historial
        
        self.notebook.add(self.tab_libros, text="Libros")
        self.notebook.add(self.tab_usuarios, text="Usuarios")
        self.notebook.add(self.tab_reservas, text="Reservas")
        self.notebook.add(self.tab_historial, text="Historial de Usuarios") # Añadir nueva pestaña
        
        # Configurar pestañas
        self.setup_tab_libros()
        self.setup_tab_usuarios()
        self.setup_tab_reservas()
        self.setup_tab_historial() # Configurar la nueva pestaña
        
        # Barra de estado
        self.status_bar = tk.Label(self, text="Biblioteca Virtual - Lista para usar", bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
    
    def setup_tab_libros(self):
        """Configura la pestaña de Libros"""
        # Frame principal con dos columnas
        main_frame = ttk.Frame(self.tab_libros)
        main_frame.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)
        
        # Frame izquierdo (lista de libros)
        left_frame = ttk.LabelFrame(main_frame, text="Catálogo de Libros")
        left_frame.pack(side=tk.LEFT, expand=True, fill=tk.BOTH, padx=5, pady=5)
        
        # Treeview para mostrar libros
        columns = ("titulo", "autor", "isbn", "estado")
        self.libros_tree = ttk.Treeview(left_frame, columns=columns, show="headings")
        
        # Configurar columnas
        self.libros_tree.heading("titulo", text="Título")
        self.libros_tree.heading("autor", text="Autor")
        self.libros_tree.heading("isbn", text="ISBN")
        self.libros_tree.heading("estado", text="Estado")
        
        self.libros_tree.column("titulo", width=200)
        self.libros_tree.column("autor", width=150)
        self.libros_tree.column("isbn", width=120)
        self.libros_tree.column("estado", width=80)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(left_frame, orient=tk.VERTICAL, command=self.libros_tree.yview)
        self.libros_tree.configure(yscrollcommand=scrollbar.set)
        
        # Empaquetado
        self.libros_tree.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Frame derecho (acciones)
        right_frame = ttk.Frame(main_frame)
        right_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=5, pady=5)
        
        # Título
        ttk.Label(right_frame, text="Gestión de Libros", font=self.title_font).pack(pady=10)
        
        # Filtros
        filter_frame = ttk.LabelFrame(right_frame, text="Filtrar libros")
        filter_frame.pack(fill=tk.X, pady=5)
        
        ttk.Button(filter_frame, text="Todos", command=lambda: self.actualizar_vista_libros()).pack(fill=tk.X, padx=5, pady=2)
        ttk.Button(filter_frame, text="Disponibles", command=lambda: self.actualizar_vista_libros(lambda l: l.disponible())).pack(fill=tk.X, padx=5, pady=2)
        ttk.Button(filter_frame, text="Reservados", command=lambda: self.actualizar_vista_libros(lambda l: not l.disponible())).pack(fill=tk.X, padx=5, pady=2)
        
        # Acciones
        actions_frame = ttk.LabelFrame(right_frame, text="Acciones")
        actions_frame.pack(fill=tk.X, pady=10)
        
        ttk.Button(actions_frame, text="Añadir Libro", command=self.mostrar_dialogo_nuevo_libro).pack(fill=tk.X, padx=5, pady=2)
        ttk.Button(actions_frame, text="Reservar Libro", command=self.mostrar_dialogo_reservar_libro).pack(fill=tk.X, padx=5, pady=2)
        ttk.Button(actions_frame, text="Cancelar Reserva", command=self.mostrar_dialogo_cancelar_reserva).pack(fill=tk.X, padx=5, pady=2)
    
    def setup_tab_usuarios(self):
        """Configura la pestaña de Usuarios"""
        # Frame principal con dos columnas
        main_frame = ttk.Frame(self.tab_usuarios)
        main_frame.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)
        
        # Frame izquierdo (lista de usuarios)
        left_frame = ttk.LabelFrame(main_frame, text="Lista de Usuarios")
        left_frame.pack(side=tk.LEFT, expand=True, fill=tk.BOTH, padx=5, pady=5)
        
        # Treeview para mostrar usuarios
        columns = ("nombre", "dni")
        self.usuarios_tree = ttk.Treeview(left_frame, columns=columns, show="headings")
        
        # Configurar columnas
        self.usuarios_tree.heading("nombre", text="Nombre")
        self.usuarios_tree.heading("dni", text="DNI")
        
        self.usuarios_tree.column("nombre", width=200)
        self.usuarios_tree.column("dni", width=100)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(left_frame, orient=tk.VERTICAL, command=self.usuarios_tree.yview)
        self.usuarios_tree.configure(yscrollcommand=scrollbar.set)
        
        # Empaquetado
        self.usuarios_tree.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Frame derecho (acciones)
        right_frame = ttk.Frame(main_frame)
        right_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=5, pady=5)
        
        # Título
        ttk.Label(right_frame, text="Gestión de Usuarios", font=self.title_font).pack(pady=10)
        
        # Acciones
        actions_frame = ttk.LabelFrame(right_frame, text="Acciones")
        actions_frame.pack(fill=tk.X, pady=10)
        
        ttk.Button(actions_frame, text="Añadir Usuario", command=self.mostrar_dialogo_nuevo_usuario).pack(fill=tk.X, padx=5, pady=2)
    
    def setup_tab_reservas(self):
        """Configura la pestaña de Reservas"""
        # Frame principal
        main_frame = ttk.Frame(self.tab_reservas)
        main_frame.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)
        
        # Título
        ttk.Label(main_frame, text="Gestión de Reservas", font=self.title_font).pack(pady=10)
        
        # Treeview para mostrar reservas
        columns = ("titulo", "isbn", "usuario", "dni")
        self.reservas_tree = ttk.Treeview(main_frame, columns=columns, show="headings")
        
        # Configurar columnas
        self.reservas_tree.heading("titulo", text="Título del Libro")
        self.reservas_tree.heading("isbn", text="ISBN")
        self.reservas_tree.heading("usuario", text="Usuario")
        self.reservas_tree.heading("dni", text="DNI")
        
        self.reservas_tree.column("titulo", width=200)
        self.reservas_tree.column("isbn", width=120)
        self.reservas_tree.column("usuario", width=150)
        self.reservas_tree.column("dni", width=100)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=self.reservas_tree.yview)
        self.reservas_tree.configure(yscrollcommand=scrollbar.set)
        
        # Empaquetado
        self.reservas_tree.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Frame de acciones
        actions_frame = ttk.Frame(main_frame)
        actions_frame.pack(fill=tk.X, pady=10)
        
        ttk.Button(actions_frame, text="Actualizar", command=self.actualizar_vista_reservas).pack(side=tk.LEFT, padx=5)
        ttk.Button(actions_frame, text="Cancelar Reserva Seleccionada", command=self.cancelar_reserva_seleccionada).pack(side=tk.LEFT, padx=5)

    def setup_tab_historial(self):
        """Configura la pestaña de Historial de Usuarios"""
        main_frame = ttk.Frame(self.tab_historial)
        main_frame.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)

        # Título
        ttk.Label(main_frame, text="Historial de Actividad de Usuarios", font=self.title_font).pack(pady=10)

        # Selector de usuario
        user_select_frame = ttk.LabelFrame(main_frame, text="Seleccionar Usuario")
        user_select_frame.pack(fill=tk.X, pady=5)

        self.selected_user_dni = tk.StringVar()
        self.user_combobox = ttk.Combobox(user_select_frame, textvariable=self.selected_user_dni, state="readonly")
        self.user_combobox.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=5, pady=5)
        self.user_combobox.bind("<<ComboboxSelected>>", self.on_user_selected_for_history)

        ttk.Button(user_select_frame, text="Mostrar Historial", command=self.mostrar_historial_usuario).pack(side=tk.LEFT, padx=5)

        # Treeview para mostrar historial
        columns = ("historial_entry",)
        self.historial_tree = ttk.Treeview(main_frame, columns=columns, show="headings")
        self.historial_tree.heading("historial_entry", text="Actividad")
        self.historial_tree.column("historial_entry", width=600)
        
        scrollbar = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=self.historial_tree.yview)
        self.historial_tree.configure(yscrollcommand=scrollbar.set)

        self.historial_tree.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.actualizar_combobox_usuarios() # Cargar usuarios al iniciar

    def actualizar_combobox_usuarios(self):
        """Actualiza el combobox de usuarios para el historial"""
        usuarios = self.biblioteca.get_usuarios()
        self.user_combobox['values'] = [f"{u.get_nombre()} ({u.get_dni()})" for u in usuarios]
        if usuarios:
            self.user_combobox.set(self.user_combobox['values'][0])
            self.on_user_selected_for_history(None) # Cargar historial del primer usuario por defecto

    def on_user_selected_for_history(self, event):
        """Cuando un usuario es seleccionado en el combobox del historial"""
        self.mostrar_historial_usuario()

    def mostrar_historial_usuario(self):
        """Muestra el historial del usuario seleccionado en la pestaña de historial"""
        selected_text = self.selected_user_dni.get()
        if not selected_text:
            return

        # Extraer DNI del texto del combobox
        dni_start = selected_text.rfind('(') + 1
        dni_end = selected_text.rfind(')')
        selected_dni = selected_text[dni_start:dni_end]

        usuario = self.biblioteca.buscar_usuario_por_dni(selected_dni)
        if usuario:
            self.actualizar_vista_historial(usuario)
        else:
            messagebox.showerror("Error", "Usuario no encontrado para el historial.")
            self.actualizar_vista_historial(None) # Limpiar el treeview

    # Métodos para actualizar vistas
    def actualizar_vista_libros(self, filtro=None):
        """Actualiza la vista de libros"""
        # Limpiar vista actual
        for i in self.libros_tree.get_children():
            self.libros_tree.delete(i)
        
        # Obtener libros filtrados
        libros = self.biblioteca.get_libros(filtro)
        
        # Agregar a la vista
        for libro in libros:
            self.libros_tree.insert('', tk.END, values=(
                libro.get_titulo(),
                libro.get_autor(),
                libro.get_isbn(),
                libro.get_estado()
            ))
        
        # Actualizar barra de estado
        self.status_bar.config(text=f"Mostrando {len(libros)} libros")
    
    def actualizar_vista_usuarios(self):
        """Actualiza la vista de usuarios"""
        # Limpiar vista actual
        for i in self.usuarios_tree.get_children():
            self.usuarios_tree.delete(i)
        
        # Obtener usuarios
        usuarios = self.biblioteca.get_usuarios()
        
        # Agregar a la vista
        for usuario in usuarios:
            self.usuarios_tree.insert('', tk.END, values=(
                usuario.get_nombre(),
                usuario.get_dni()
            ))
        
        # Actualizar barra de estado
        self.status_bar.config(text=f"Mostrando {len(usuarios)} usuarios")
        self.actualizar_combobox_usuarios() # También actualizar el combobox de historial
    
    def actualizar_vista_reservas(self):
        """Actualiza la vista de reservas"""
        # Limpiar vista actual
        for i in self.reservas_tree.get_children():
            self.reservas_tree.delete(i)
        
        # Obtener reservas
        reservas = self.biblioteca.get_reservas()
        
        # Agregar a la vista
        for reserva in reservas:
            libro = reserva.get_libro()
            usuario = reserva.get_usuario()
            
            self.reservas_tree.insert('', tk.END, values=(
                libro.get_titulo(),
                libro.get_isbn(),
                usuario.get_nombre(),
                usuario.get_dni()
            ))
        
        # Actualizar barra de estado
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
            self.status_bar.config(text="No se ha seleccionado un usuario para el historial")
    
    # Diálogos
    def mostrar_dialogo_nuevo_libro(self):
        """Muestra un diálogo para agregar un nuevo libro"""
        dialogo = DialogoNuevoLibro(self)
        if dialogo.result:
            titulo, autor, isbn = dialogo.result
            libro = self.biblioteca.agregar_libro(titulo, autor, isbn)
            if libro:
                messagebox.showinfo("Éxito", "Libro registrado correctamente")
                self.actualizar_vista_libros()
                # Opcional: registrar acción para el usuario que añadió el libro si tuviéramos un sistema de login
                # self.biblioteca.buscar_usuario_por_dni(dni_usuario_activo).registrar_historial(...)
            else:
                messagebox.showerror("Error", "No se pudo registrar el libro")
    
    def mostrar_dialogo_nuevo_usuario(self):
        """Muestra un diálogo para agregar un nuevo usuario"""
        dialogo = DialogoNuevoUsuario(self)
        if dialogo.result:
            nombre, dni = dialogo.result
            usuario = self.biblioteca.agregar_usuario(nombre, dni)
            if usuario:
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                usuario.registrar_historial("Se registró en el sistema", timestamp)
                messagebox.showinfo("Éxito", "Usuario registrado correctamente")
                self.actualizar_vista_usuarios()
                self.actualizar_combobox_usuarios() # Para que aparezca en el selector de historial
            else:
                messagebox.showerror("Error", "No se pudo registrar el usuario")
    
    def mostrar_dialogo_reservar_libro(self):
        """Muestra un diálogo para reservar un libro"""
        dialogo = DialogoReservarLibro(self)
        if dialogo.result:
            isbn, dni = dialogo.result
            exito, mensaje = self.biblioteca.reservar_libro(isbn, dni)
            if exito:
                messagebox.showinfo("Éxito", mensaje)
                self.actualizar_vista_libros()
                self.actualizar_vista_reservas()
                self.actualizar_vista_historial(self.biblioteca.buscar_usuario_por_dni(dni)) # Actualizar historial del usuario
            else:
                messagebox.showerror("Error", mensaje)
    
    def mostrar_dialogo_cancelar_reserva(self):
        """Muestra un diálogo para cancelar una reserva"""
        isbn = simpledialog.askstring("Cancelar Reserva", "ISBN del libro:")
        if isbn:
            # Necesitamos encontrar la reserva para obtener el DNI del usuario antes de cancelarla
            reserva_a_cancelar = next((r for r in self.biblioteca.get_reservas() if r.get_libro().get_isbn() == isbn), None)
            usuario_dni = reserva_a_cancelar.get_usuario().get_dni() if reserva_a_cancelar else None

            exito, mensaje = self.biblioteca.cancelar_reserva(isbn)
            if exito:
                messagebox.showinfo("Éxito", mensaje)
                self.actualizar_vista_libros()
                self.actualizar_vista_reservas()
                if usuario_dni: # Actualizar historial del usuario que canceló
                    self.actualizar_vista_historial(self.biblioteca.buscar_usuario_por_dni(usuario_dni))
            else:
                messagebox.showerror("Error", mensaje)
    
    def cancelar_reserva_seleccionada(self):
        """Cancela la reserva seleccionada en la vista de reservas"""
        seleccion = self.reservas_tree.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "No hay reserva seleccionada")
            return
        
        item = self.reservas_tree.item(seleccion[0])
        isbn = item['values'][1]  # ISBN está en la posición 1
        dni_usuario = item['values'][3] # DNI del usuario está en la posición 3
        
        exito, mensaje = self.biblioteca.cancelar_reserva(isbn)
        if exito:
            messagebox.showinfo("Éxito", mensaje)
            self.actualizar_vista_libros()
            self.actualizar_vista_reservas()
            self.actualizar_vista_historial(self.biblioteca.buscar_usuario_por_dni(dni_usuario)) # Actualizar historial
        else:
            messagebox.showerror("Error", mensaje)

# Diálogos personalizados (sin cambios, excepto que son llamados por el nuevo código)
class DialogoNuevoLibro(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        
        self.parent = parent
        self.result = None
        
        self.title("Nuevo Libro")
        self.geometry("300x200")
        self.resizable(False, False)
        self.transient(parent)
        self.grab_set()
        
        # Campos
        ttk.Label(self, text="Título:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.titulo_entry = ttk.Entry(self, width=30)
        self.titulo_entry.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(self, text="Autor:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        self.autor_entry = ttk.Entry(self, width=30)
        self.autor_entry.grid(row=1, column=1, padx=5, pady=5)
        
        ttk.Label(self, text="ISBN:").grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
        self.isbn_entry = ttk.Entry(self, width=30)
        self.isbn_entry.grid(row=2, column=1, padx=5, pady=5)
        
        # Botones
        btn_frame = ttk.Frame(self)
        btn_frame.grid(row=3, column=0, columnspan=2, pady=10)
        
        ttk.Button(btn_frame, text="Guardar", command=self.guardar).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Cancelar", command=self.cancelar).pack(side=tk.LEFT, padx=5)
        
        # Centrar
        self.center_window()
        
        # Esperar a que el diálogo se cierre
        self.wait_window()
    
    def guardar(self):
        titulo = self.titulo_entry.get().strip()
        autor = self.autor_entry.get().strip()
        isbn = self.isbn_entry.get().strip()
        
        if not titulo or not autor or not isbn:
            messagebox.showerror("Error", "Todos los campos son obligatorios")
            return
        
        self.result = (titulo, autor, isbn)
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
        self.geometry("300x150")
        self.resizable(False, False)
        self.transient(parent)
        self.grab_set()
        
        # Campos
        ttk.Label(self, text="Nombre:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.nombre_entry = ttk.Entry(self, width=30)
        self.nombre_entry.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(self, text="DNI:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        self.dni_entry = ttk.Entry(self, width=30)
        self.dni_entry.grid(row=1, column=1, padx=5, pady=5)
        
        # Botones
        btn_frame = ttk.Frame(self)
        btn_frame.grid(row=2, column=0, columnspan=2, pady=10)
        
        ttk.Button(btn_frame, text="Guardar", command=self.guardar).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Cancelar", command=self.cancelar).pack(side=tk.LEFT, padx=5)
        
        # Centrar
        self.center_window()
        
        # Esperar a que el diálogo se cierre
        self.wait_window()
    
    def guardar(self):
        nombre = self.nombre_entry.get().strip()
        dni = self.dni_entry.get().strip()
        
        if not nombre or not dni:
            messagebox.showerror("Error", "Todos los campos son obligatorios")
            return
        
        self.result = (nombre, dni)
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
        
        # Centrar
        self.center_window()
        
        # Esperar a que el diálogo se cierre
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
    # Mantener la opción de menú de consola original
    if len(sys.argv) > 1 and sys.argv[1] == "--console":
        Biblioteca().menu()
    else:
        # Versión gráfica
        app = BibliotecaApp()
        # Configurar tema
        style = ttk.Style()
        style.theme_use('clam')  # Otros temas: 'alt', 'default', 'classic'
        
        # Personalizar colores
        style.configure('TButton', background='#4a7abc', foreground='black')
        style.map('TButton',  
                  background=[('active', '#3c5e94'), ('pressed', '#2c456e')],
                  foreground=[('active', 'white'), ('pressed', 'white')])
        
        # Iniciar aplicación
        app.mainloop()