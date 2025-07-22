import tkinter as tk
from tkinter import ttk

# ──────────── CLASES POO ────────────
class Empleado:
    def __init__(self, nombre: str, dni: str, salario_base: float):
        self.__nombre = nombre
        self.__dni = dni
        self.__salario_base = salario_base

    def get_nombre(self): return self.__nombre
    def get_dni(self): return self.__dni
    def get_salario_base(self): return self.__salario_base

    def calcular_salario(self):
        raise NotImplementedError()

    def mostrar_informacion(self):
        info = f"Nombre : {self.get_nombre()}\nDNI    : {self.get_dni()}\n"
        if isinstance(self, Operario):
            info += (f"Salario Base    : S/ {self.get_salario_base():.2f}\n"
                     f"Bono Producción : S/ {self.get_bono_produccion():.2f}\n"
                     f"Salario Final   : S/ {self.calcular_salario():.2f}")
        elif isinstance(self, Administrativo):
            info += (f"Salario Base    : S/ {self.get_salario_base():.2f}\n"
                     f"Impuesto (10%)  : S/ {self.get_impuesto():.2f}\n"
                     f"Salario Final   : S/ {self.calcular_salario():.2f}")
        return info

class Administrativo(Empleado):
    def calcular_salario(self): return self.get_salario_base() * 0.90
    def get_impuesto(self): return self.get_salario_base() * 0.10

class Operario(Empleado):
    def __init__(self, nombre, dni, salario_base, bono_produccion):
        super().__init__(nombre, dni, salario_base)
        self.__bono_produccion = bono_produccion

    def get_bono_produccion(self): return self.__bono_produccion
    def calcular_salario(self): return self.get_salario_base() + self.get_bono_produccion()

# ──────────── INTERFAZ CON TKINTER ────────────
class App:
    def __init__(self, root):
        self.empleados = []
        self.root = root
        self.root.title("Sistema de Gestión de Empleados")
        self.root.geometry("720x500")
        self.root.configure(bg="#f0f8ff")

        tk.Label(root, text="SISTEMA DE EMPLEADOS", font=("Helvetica", 20, "bold"),
                 bg="#4682b4", fg="white", pady=12).pack(fill=tk.X)

        self.status_label = tk.Label(root, text="", bg="#f0f8ff", fg="#007700", font=("Arial", 10, "italic"))
        self.status_label.pack(pady=(0, 5))

        self.tabs = ttk.Notebook(root)
        self.tabs.pack(fill="both", expand=True, padx=10, pady=10)

        self.tab_admin = ttk.Frame(self.tabs)
        self.tab_ope = ttk.Frame(self.tabs)
        self.tab_lista = ttk.Frame(self.tabs)

        self.tabs.add(self.tab_admin, text="Registrar Administrativo")
        self.tabs.add(self.tab_ope, text="Registrar Operario")
        self.tabs.add(self.tab_lista, text="Lista de Empleados")

        self.crear_tab_admin()
        self.crear_tab_operario()
        self.crear_tab_lista()

    def crear_tab_admin(self):
        self.admin_inputs = self._crear_formulario(self.tab_admin,
            ["Nombre", "DNI", "Salario Base"],
            self.registrar_admin)

    def crear_tab_operario(self):
        self.ope_inputs = self._crear_formulario(self.tab_ope,
            ["Nombre", "DNI", "Salario Base", "Bono Producción"],
            self.registrar_operario)

    def crear_tab_lista(self):
        self.text_area = tk.Text(self.tab_lista, bg="#fffafa", fg="#333", font=("Courier New", 10),
                                 width=85, height=25)
        self.text_area.pack(padx=10, pady=10)

        tk.Button(self.tab_lista, text="Mostrar Empleados", bg="#4682b4", fg="white",
                  font=("Arial", 10, "bold"), command=self.mostrar_empleados).pack()

    def registrar_admin(self):
        try:
            nombre = self.admin_inputs[0].get()
            dni = self.admin_inputs[1].get()
            salario = float(self.admin_inputs[2].get())

            empleado = Administrativo(nombre, dni, salario)
            self.empleados.append(empleado)

            self._mostrar_mensaje("✔ Administrativo registrado.")
            self._limpiar(self.admin_inputs)
        except:
            self._mostrar_mensaje("✖ Error: datos inválidos.", color="#bb0000")

    def registrar_operario(self):
        try:
            nombre = self.ope_inputs[0].get()
            dni = self.ope_inputs[1].get()
            salario = float(self.ope_inputs[2].get())
            bono = float(self.ope_inputs[3].get())

            empleado = Operario(nombre, dni, salario, bono)
            self.empleados.append(empleado)

            self._mostrar_mensaje("✔ Operario registrado.")
            self._limpiar(self.ope_inputs)
        except:
            self._mostrar_mensaje("✖ Error: datos inválidos.", color="#bb0000")

    def mostrar_empleados(self):
        self.text_area.delete(1.0, tk.END)
        if not self.empleados:
            self.text_area.insert(tk.END, "⚠ No hay empleados registrados.")
        else:
            for emp in self.empleados:
                self.text_area.insert(tk.END, emp.mostrar_informacion() + "\n\n")

    def _crear_formulario(self, frame, campos, comando):
        entries = []
        for i, label in enumerate(campos):
            tk.Label(frame, text=label + ":", font=("Arial", 10)).grid(row=i, column=0, padx=10, pady=5, sticky="e")
            ent = tk.Entry(frame, font=("Arial", 10), width=30)
            ent.grid(row=i, column=1, padx=10, pady=5)
            entries.append(ent)

        btn = tk.Button(frame, text="Registrar", bg="#20b2aa", fg="white",
                        font=("Arial", 10, "bold"), width=25, command=comando)
        btn.grid(row=len(campos), column=0, columnspan=2, pady=10)
        return entries

    def _limpiar(self, entradas):
        for e in entradas:
            e.delete(0, tk.END)

    def _mostrar_mensaje(self, texto, color="#007700"):
        self.status_label.config(text=texto, fg=color)

# ──────────── EJECUTAR APLICACIÓN ────────────
if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
