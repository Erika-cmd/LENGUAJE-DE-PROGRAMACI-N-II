import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class CalculadoraNumerica:
    def _init_(self, root):
        self.root = root
        self.root.title("Calculadora Numérica")
        self.root.geometry("800x600")
        self.root.configure(bg='#2C3E50')  # Color de fondo azul oscuro

        style = ttk.Style()
        style.configure('Custom.TButton',
                        background='#3498DB',  # Azul
                        foreground='white',
                        padding=10,
                        font=('Arial', 10, 'bold'))

        # Frame principal
        main_frame = tk.Frame(root, bg='#2C3E50', padx=20, pady=20)
        main_frame.pack(expand=True, fill='both')

        # Título
        title = tk.Label(main_frame,
                         text="Calculadora Numérica",
                         font=('Arial', 20, 'bold'),
                         bg='#2C3E50',
                         fg='white')
        title.pack(pady=20)

        buttons_frame = tk.Frame(main_frame, bg='#2C3E50')
        buttons_frame.pack(fill='x', pady=10)

        methods = [
            ("Interpolación - Método de Lagrange", self.lagrange_window),
            ("Diferencias Finitas", self.diferencias_finitas_window),
            ("Diferencias Divididas - Newton", self.diferencias_divididas_window),
            ("Integración - Método del Trapecio", self.trapecio_window),
            ("Integración - Método de Simpson", self.simpson_window),
            ("ED - Método de Euler", self.euler_window),
            ("ED - Método de Taylor", self.taylor_window),
            ("ED - Método de Runge-Kutta", self.runge_kutta_window)
        ]

        for i, (text, command) in enumerate(methods):
            btn = tk.Button(buttons_frame,
                            text=text,
                            command=command,
                            bg='#3498DB',
                            fg='white',
                            font=('Arial', 10),
                            pady=10,
                            relief='raised')
            btn.grid(row=i // 2, column=i % 2, padx=5, pady=5, sticky='ew')

        buttons_frame.grid_columnconfigure(0, weight=1)
        buttons_frame.grid_columnconfigure(1, weight=1)

    def create_method_window(self, title):
        window = tk.Toplevel(self.root)
        window.title(title)
        window.geometry("600x400")
        window.configure(bg='#34495E')
        return window

    def lagrange_window(self):
        window = self.create_method_window("Interpolación de Lagrange")

        # Frame para entradas
        input_frame = tk.Frame(window, bg='#34495E')
        input_frame.pack(pady=20)

        # Número de puntos
        tk.Label(input_frame,
                 text="Número de puntos:",
                 bg='#34495E',
                 fg='white').grid(row=0, column=0, pady=5)
        n_points = tk.Entry(input_frame)
        n_points.grid(row=0, column=1, pady=5)

        # Frame para los puntos
        points_frame = tk.Frame(window, bg='#34495E')
        points_frame.pack(pady=10)

        def create_point_inputs():
            for widget in points_frame.winfo_children():
                widget.destroy()

            try:
                n = int(n_points.get())
                self.x_entries = []
                self.y_entries = []

                tk.Label(points_frame,
                         text="X",
                         bg='#34495E',
                         fg='white').grid(row=0, column=1)
                tk.Label(points_frame,
                         text="Y",
                         bg='#34495E',
                         fg='white').grid(row=0, column=2)

                for i in range(n):
                    tk.Label(points_frame,
                             text=f"Punto {i+1}:",
                             bg='#34495E',
                             fg='white').grid(row=i+1, column=0)
                    x_entry = tk.Entry(points_frame)
                    y_entry = tk.Entry(points_frame)
                    x_entry.grid(row=i+1, column=1)
                    y_entry.grid(row=i+1, column=2)
                    self.x_entries.append(x_entry)
                    self.y_entries.append(y_entry)

            except ValueError:
                messagebox.showerror("Error", "Por favor ingrese un número válido")

        # Botón para crear entradas de puntos
        tk.Button(input_frame,
                  text="Crear puntos",
                  command=create_point_inputs,
                  bg='#E74C3C',
                  fg='white').grid(row=0, column=2, pady=5, padx=5)

        # Valor a interpolar
        tk.Label(window,
                 text="Valor a interpolar:",
                 bg='#34495E',
                 fg='white').pack(pady=5)
        x_interpolate = tk.Entry(window)
        x_interpolate.pack(pady=5)

        # Resultado
        result_label = tk.Label(window,
                                text="",
                                bg='#34495E',
                                fg='white')
        result_label.pack(pady=20)

        def calculate():
            try:
                x_points = [float(entry.get()) for entry in self.x_entries]
                y_points = [float(entry.get()) for entry in self.y_entries]
                x_to_interpolate = float(x_interpolate.get())

                result = 0
                n = len(x_points)
                for i in range(n):
                    term = y_points[i]
                    for j in range(n):
                        if i != j:
                            term *= (x_to_interpolate - x_points[j]) / (x_points[i] - x_points[j])
                    result += term

                result_label.config(text=f"Resultado: {result:.4f}")

                # Crear gráfica
                fig, ax = plt.subplots(figsize=(6, 4))

                # Plotear puntos originales
                ax.scatter(x_points, y_points, color='blue', label='Puntos dados')

                # Plotear punto interpolado
                ax.scatter(x_to_interpolate, result, color='red', label='Punto interpolado')

                # Generar curva suave de interpolación
                x_smooth = np.linspace(min(x_points), max(x_points), 200)
                y_smooth = []
                for x in x_smooth:
                    y = 0
                    for i in range(n):
                        term = y_points[i]
                        for j in range(n):
                            if i != j:
                                term *= (x - x_points[j]) / (x_points[i] - x_points[j])
                        y += term
                    y_smooth.append(y)

                ax.plot(x_smooth, y_smooth, 'g-', label='Polinomio de Lagrange')

                ax.grid(True)
                ax.legend()
                ax.set_xlabel('X')
                ax.set_ylabel('Y')
                ax.set_title('Interpolación de Lagrange')

                # Si ya existe un canvas, eliminarlo
                for widget in window.winfo_children():
                    if isinstance(widget, FigureCanvasTkAgg):
                        widget.get_tk_widget().destroy()

                # Agregar el nuevo canvas
                canvas = FigureCanvasTkAgg(fig, master=window)
                canvas.draw()
                canvas.get_tk_widget().pack(pady=10)

            except Exception as e:
                messagebox.showerror("Error", f"Por favor verifique los datos ingresados.\n{str(e)}")

        # Botón calcular
        tk.Button(window,
                  text="Calcular",
                  command=calculate,
                  bg='#2ECC71',
                  fg='white').pack(pady=10)

    def diferencias_finitas_window(self):
        window = self.create_method_window("Diferencias Finitas")

        # Frame para entradas
        input_frame = tk.Frame(window, bg='#34495E')
        input_frame.pack(pady=20)

        # Número de puntos
        tk.Label(input_frame,
                 text="Número de puntos:",
                 bg='#34495E',
                 fg='white').grid(row=0, column=0, pady=5)
        n_points = tk.Entry(input_frame)
        n_points.grid(row=0, column=1, pady=5)

        # Frame para los puntos
        points_frame = tk.Frame(window, bg='#34495E')
        points_frame.pack(pady=10)

        def create_point_inputs():
            for widget in points_frame.winfo_children():
                widget.destroy()

            try:
                n = int(n_points.get())
                self.x_entries = []
                self.y_entries = []

                tk.Label(points_frame,
                         text="X",
                         bg='#34495E',
                         fg='white').grid(row=0, column=1)
                tk.Label(points_frame,
                         text="Y",
                         bg='#34495E',
                         fg='white').grid(row=0, column=2)

                for i in range(n):
                    tk.Label(points_frame,
                             text=f"Punto {i+1}:",
                             bg='#34495E',
                             fg='white').grid(row=i+1, column=0)
                    x_entry = tk.Entry(points_frame)
                    y_entry = tk.Entry(points_frame)
                    x_entry.grid(row=i+1, column=1)
                    y_entry.grid(row=i+1, column=2)
                    self.x_entries.append(x_entry)
                    self.y_entries.append(y_entry)

            except ValueError:
                messagebox.showerror("Error", "Por favor ingrese un número válido")

        # Botón para crear entradas de puntos
        tk.Button(input_frame,
                  text="Crear puntos",
                  command=create_point_inputs,
                  bg='#E74C3C',
                  fg='white').grid(row=0, column=2, pady=5, padx=5)

        # Valor a interpolar
        tk.Label(window,
                 text="Valor a interpolar:",
                 bg='#34495E',
                 fg='white').pack(pady=5)
        x_interpolate = tk.Entry(window)
        x_interpolate.pack(pady=5)

        # Resultado
        result_label = tk.Label(window,
                                text="",
                                bg='#34495E',
                                fg='white')
        result_label.pack(pady=20)

        def calculate():
            try:
                x_points = [float(entry.get()) for entry in self.x_entries]
                y_points = [float(entry.get()) for entry in self.y_entries]
                x_to_interpolate = float(x_interpolate.get())

                # Implementar el método de diferencias finitas aquí
                result = np.polyfit(x_points, y_points, len(x_points) - 1)
                result = np.polyval(result, x_to_interpolate)

                result_label.config(text=f"Resultado: {result:.4f}")

                # Crear gráfica
                fig, ax = plt.subplots(figsize=(6, 4))

                # Plotear puntos originales
                ax.scatter(x_points, y_points, color='blue', label='Puntos dados')

                # Plotear punto interpolado
                ax.scatter(x_to_interpolate, result, color='red', label='Punto interpolado')

                # Generar curva suave de interpolación
                x_smooth = np.linspace(min(x_points), max(x_points), 200)
                y_smooth = np.polyval(result, x_smooth)

                ax.plot(x_smooth, y_smooth, 'g-', label='Interpolación')

                ax.grid(True)
                ax.legend()
                ax.set_xlabel('X')
                ax.set_ylabel('Y')
                ax.set_title('Diferencias Finitas')

                # Si ya existe un canvas, eliminarlo
                for widget in window.winfo_children():
                    if isinstance(widget, FigureCanvasTkAgg):
                        widget.get_tk_widget().destroy()

                # Agregar el nuevo canvas
                canvas = FigureCanvasTkAgg(fig, master=window)
                canvas.draw()
                canvas.get_tk_widget().pack(pady=10)

            except Exception as e:
                messagebox.showerror("Error", f"Por favor verifique los datos ingresados.\n{str(e)}")

        # Botón calcular
        tk.Button(window,
                  text="Calcular",
                  command=calculate,
                  bg='#2ECC71',
                  fg='white').pack(pady=10)

    def diferencias_divididas_window(self):
        window = self.create_method_window("Diferencias Divididas")

        # Frame para entradas
        input_frame = tk.Frame(window, bg='#34495E')
        input_frame.pack(pady=20)

        # Número de puntos
        tk.Label(input_frame,
                 text="Número de puntos:",
                 bg='#34495E',
                 fg='white').grid(row=0, column=0, pady=5)
        n_points = tk.Entry(input_frame)
        n_points.grid(row=0, column=1, pady=5)

        # Frame para los puntos
        points_frame = tk.Frame(window, bg='#34495E')
        points_frame.pack(pady=10)

        def create_point_inputs():
            for widget in points_frame.winfo_children():
                widget.destroy()

            try:
                n = int(n_points.get())
                self.x_entries = []
                self.y_entries = []

                tk.Label(points_frame,
                         text="X",
                         bg='#34495E',
                         fg='white').grid(row=0, column=1)
                tk.Label(points_frame,
                         text="Y",
                         bg='#34495E',
                         fg='white').grid(row=0, column=2)

                for i in range(n):
                    tk.Label(points_frame,
                             text=f"Punto {i+1}:",
                             bg='#34495E',
                             fg='white').grid(row=i+1, column=0)
                    x_entry = tk.Entry(points_frame)
                    y_entry = tk.Entry(points_frame)
                    x_entry.grid(row=i+1, column=1)
                    y_entry.grid(row=i+1, column=2)
                    self.x_entries.append(x_entry)
                    self.y_entries.append(y_entry)

            except ValueError:
                messagebox.showerror("Error", "Por favor ingrese un número válido")

        # Botón para crear entradas de puntos
        tk.Button(input_frame,
                  text="Crear puntos",
                  command=create_point_inputs,
                  bg='#E74C3C',
                  fg='white').grid(row=0, column=2, pady=5, padx=5)

        # Valor a interpolar
        tk.Label(window,
                 text="Valor a interpolar:",
                 bg='#34495E',
                 fg='white').pack(pady=5)
        x_interpolate = tk.Entry(window)
        x_interpolate.pack(pady=5)

        # Resultado
        result_label = tk.Label(window,
                                text="",
                                bg='#34495E',
                                fg='white')
        result_label.pack(pady=20)

        def calculate():
            try:
                x_points = [float(entry.get()) for entry in self.x_entries]
                y_points = [float(entry.get()) for entry in self.y_entries]
                x_to_interpolate = float(x_interpolate.get())

                # Implementar el método de diferencias divididas de Newton aquí
                def divided_diff(x, y):
                    n = len(y)
                    coef = np.zeros([n, n])
                    coef[:, 0] = y
                    for j in range(1, n):
                        for i in range(n - j):
                            coef[i][j] = (coef[i + 1][j - 1] - coef[i][j - 1]) / (x[i + j] - x[i])
                    return coef[0, :]

                coef = divided_diff(x_points, y_points)

                def newton_poly(coef, x_data, x):
                    n = len(coef) - 1
                    p = coef[n]
                    for k in range(1, n + 1):
                        p = coef[n - k] + (x - x_data[n - k]) * p
                    return p

                result = newton_poly(coef, x_points, x_to_interpolate)

                result_label.config(text=f"Resultado: {result:.4f}")

                # Crear gráfica
                fig, ax = plt.subplots(figsize=(6, 4))

                # Plotear puntos originales
                ax.scatter(x_points, y_points, color='blue', label='Puntos dados')

                # Plotear punto interpolado
                ax.scatter(x_to_interpolate, result, color='red', label='Punto interpolado')

                # Generar curva suave de interpolación
                x_smooth = np.linspace(min(x_points), max(x_points), 200)
                y_smooth = [newton_poly(coef, x_points, x) for x in x_smooth]

                ax.plot(x_smooth, y_smooth, 'g-', label='Interpolación')

                ax.grid(True)
                ax.legend()
                ax.set_xlabel('X')
                ax.set_ylabel('Y')
                ax.set_title('Diferencias Divididas de Newton')

                # Si ya existe un canvas, eliminarlo
                for widget in window.winfo_children():
                    if isinstance(widget, FigureCanvasTkAgg):
                        widget.get_tk_widget().destroy()

                # Agregar el nuevo canvas
                canvas = FigureCanvasTkAgg(fig, master=window)
                canvas.draw()
                canvas.get_tk_widget().pack(pady=10)

            except Exception as e:
                messagebox.showerror("Error", f"Por favor verifique los datos ingresados.\n{str(e)}")

        # Botón calcular
        tk.Button(window,
                  text="Calcular",
                  command=calculate,
                  bg='#2ECC71',
                  fg='white').pack(pady=10)

    def trapecio_window(self):
        window = self.create_method_window("Método del Trapecio")

        # Frame para entradas
        input_frame = tk.Frame(window, bg='#34495E')
        input_frame.pack(pady=20)

        # Función
        tk.Label(input_frame,
                 text="Función (en términos de x):",
                 bg='#34495E',
                 fg='white').grid(row=0, column=0, pady=5)
        function_entry = tk.Entry(input_frame)
        function_entry.grid(row=0, column=1, pady=5)

        # Límites de integración
        tk.Label(input_frame,
                 text="Límite inferior:",
                 bg='#34495E',
                 fg='white').grid(row=1, column=0, pady=5)
        lower_limit = tk.Entry(input_frame)
        lower_limit.grid(row=1, column=1, pady=5)

        tk.Label(input_frame,
                 text="Límite superior:",
                 bg='#34495E',
                 fg='white').grid(row=2, column=0, pady=5)
        upper_limit = tk.Entry(input_frame)
        upper_limit.grid(row=2, column=1, pady=5)

        # Número de intervalos
        tk.Label(input_frame,
                 text="Número de intervalos:",
                 bg='#34495E',
                 fg='white').grid(row=3, column=0, pady=5)
        n_intervals = tk.Entry(input_frame)
        n_intervals.grid(row=3, column=1, pady=5)

        # Resultado
        result_label = tk.Label(window,
                                text="",
                                bg='#34495E',
                                fg='white')
        result_label.pack(pady=20)

        def calculate():
            try:
                func = lambda x: eval(function_entry.get())
                a = float(lower_limit.get())
                b = float(upper_limit.get())
                n = int(n_intervals.get())

                h = (b - a) / n
                result = 0.5 * (func(a) + func(b))
                for i in range(1, n):
                    result += func(a + i * h)
                result *= h

                result_label.config(text=f"Resultado: {result:.4f}")

            except Exception as e:
                messagebox.showerror("Error", f"Por favor verifique los datos ingresados.\n{str(e)}")

        # Botón calcular
        tk.Button(window,
                  text="Calcular",
                  command=calculate,
                  bg='#2ECC71',
                  fg='white').pack(pady=10)

    def simpson_window(self):
        window = self.create_method_window("Método de Simpson")

        # Frame para entradas
        input_frame = tk.Frame(window, bg='#34495E')
        input_frame.pack(pady=20)

        # Función
        tk.Label(input_frame,
                 text="Función (en términos de x):",
                 bg='#34495E',
                 fg='white').grid(row=0, column=0, pady=5)
        function_entry = tk.Entry(input_frame)
        function_entry.grid(row=0, column=1, pady=5)

        # Límites de integración
        tk.Label(input_frame,
                 text="Límite inferior:",
                 bg='#34495E',
                 fg='white').grid(row=1, column=0, pady=5)
        lower_limit = tk.Entry(input_frame)
        lower_limit.grid(row=1, column=1, pady=5)

        tk.Label(input_frame,
                 text="Límite superior:",
                 bg='#34495E',
                 fg='white').grid(row=2, column=0, pady=5)
        upper_limit = tk.Entry(input_frame)
        upper_limit.grid(row=2, column=1, pady=5)

        # Número de intervalos
        tk.Label(input_frame,
                 text="Número de intervalos:",
                 bg='#34495E',
                 fg='white').grid(row=3, column=0, pady=5)
        n_intervals = tk.Entry(input_frame)
        n_intervals.grid(row=3, column=1, pady=5)

        # Resultado
        result_label = tk.Label(window,
                                text="",
                                bg='#34495E',
                                fg='white')
        result_label.pack(pady=20)

        def calculate():
            try:
                func = lambda x: eval(function_entry.get())
                a = float(lower_limit.get())
                b = float(upper_limit.get())
                n = int(n_intervals.get())

                if n % 2 != 0:
                    raise ValueError("El número de intervalos debe ser par")

                h = (b - a) / n
                result = func(a) + func(b)
                for i in range(1, n, 2):
                    result += 4 * func(a + i * h)
                for i in range(2, n - 1, 2):
                    result += 2 * func(a + i * h)
                result *= h / 3

                result_label.config(text=f"Resultado: {result:.4f}")

            except Exception as e:
                messagebox.showerror("Error", f"Por favor verifique los datos ingresados.\n{str(e)}")

        # Botón calcular
        tk.Button(window,
                  text="Calcular",
                  command=calculate,
                  bg='#2ECC71',
                  fg='white').pack(pady=10)

    def euler_window(self):
        window = self.create_method_window("Método de Euler")

        # Frame para entradas
        input_frame = tk.Frame(window, bg='#34495E')
        input_frame.pack(pady=20)

        # Función
        tk.Label(input_frame,
                 text="Función (dy/dx):",
                 bg='#34495E',
                 fg='white').grid(row=0, column=0, pady=5)
        function_entry = tk.Entry(input_frame)
        function_entry.grid(row=0, column=1, pady=5)

        # Condiciones iniciales
        tk.Label(input_frame,
                 text="Valor inicial de x:",
                 bg='#34495E',
                 fg='white').grid(row=1, column=0, pady=5)
        x0 = tk.Entry(input_frame)
        x0.grid(row=1, column=1, pady=5)

        tk.Label(input_frame,
                 text="Valor inicial de y:",
                 bg='#34495E',
                 fg='white').grid(row=2, column=0, pady=5)
        y0 = tk.Entry(input_frame)
        y0.grid(row=2, column=1, pady=5)

        # Paso
        tk.Label(input_frame,
                 text="Paso (h):",
                 bg='#34495E',
                 fg='white').grid(row=3, column=0, pady=5)
        h = tk.Entry(input_frame)
        h.grid(row=3, column=1, pady=5)

        # Número de pasos
        tk.Label(input_frame,
                 text="Número de pasos:",
                 bg='#34495E',
                 fg='white').grid(row=4, column=0, pady=5)
        n_steps = tk.Entry(input_frame)
        n_steps.grid(row=4, column=1, pady=5)

        # Resultado
        result_label = tk.Label(window,
                                text="",
                                bg='#34495E',
                                fg='white')
        result_label.pack(pady=20)

        def calculate():
            try:
                func = lambda x, y: eval(function_entry.get())
                x0_val = float(x0.get())
                y0_val = float(y0.get())
                h_val = float(h.get())
                n_steps_val = int(n_steps.get())

                x_vals = [x0_val]
                y_vals = [y0_val]

                for _ in range(n_steps_val):
                    y0_val += h_val * func(x0_val, y0_val)
                    x0_val += h_val
                    x_vals.append(x0_val)
                    y_vals.append(y0_val)

                result_label.config(text=f"Resultado: y({x0_val:.4f}) = {y0_val:.4f}")

                # Crear gráfica
                fig, ax = plt.subplots(figsize=(6, 4))
                ax.plot(x_vals, y_vals, 'g-', label='Solución de Euler')
                ax.grid(True)
                ax.legend()
                ax.set_xlabel('X')
                ax.set_ylabel('Y')
                ax.set_title('Método de Euler')

                # Si ya existe un canvas, eliminarlo
                for widget in window.winfo_children():
                    if isinstance(widget, FigureCanvasTkAgg):
                        widget.get_tk_widget().destroy()

                # Agregar el nuevo canvas
                canvas = FigureCanvasTkAgg(fig, master=window)
                canvas.draw()
                canvas.get_tk_widget().pack(pady=10)

            except Exception as e:
                messagebox.showerror("Error", f"Por favor verifique los datos ingresados.\n{str(e)}")

        # Botón calcular
        tk.Button(window,
                  text="Calcular",
                  command=calculate,
                  bg='#2ECC71',
                  fg='white').pack(pady=10)

    def taylor_window(self):
        window = self.create_method_window("Método de Taylor")

        # Frame para entradas
        input_frame = tk.Frame(window, bg='#34495E')
        input_frame.pack(pady=20)

        # Función
        tk.Label(input_frame,
                 text="Función (dy/dx):",
                 bg='#34495E',
                 fg='white').grid(row=0, column=0, pady=5)
        function_entry = tk.Entry(input_frame)
        function_entry.grid(row=0, column=1, pady=5)

        # Condiciones iniciales
        tk.Label(input_frame,
                 text="Valor inicial de x:",
                 bg='#34495E',
                 fg='white').grid(row=1, column=0, pady=5)
        x0 = tk.Entry(input_frame)
        x0.grid(row=1, column=1, pady=5)

        tk.Label(input_frame,
                 text="Valor inicial de y:",
                 bg='#34495E',
                 fg='white').grid(row=2, column=0, pady=5)
        y0 = tk.Entry(input_frame)
        y0.grid(row=2, column=1, pady=5)

        # Paso
        tk.Label(input_frame,
                 text="Paso (h):",
                 bg='#34495E',
                 fg='white').grid(row=3, column=0, pady=5)
        h = tk.Entry(input_frame)
        h.grid(row=3, column=1, pady=5)

        # Número de pasos
        tk.Label(input_frame,
                 text="Número de pasos:",
                 bg='#34495E',
                 fg='white').grid(row=4, column=0, pady=5)
        n_steps = tk.Entry(input_frame)
        n_steps.grid(row=4, column=1, pady=5)

        # Resultado
        result_label = tk.Label(window,
                                text="",
                                bg='#34495E',
                                fg='white')
        result_label.pack(pady=20)

        def calculate():
            try:
                func = lambda x, y: eval(function_entry.get())
                x0_val = float(x0.get())
                y0_val = float(y0.get())
                h_val = float(h.get())
                n_steps_val = int(n_steps.get())

                x_vals = [x0_val]
                y_vals = [y0_val]

                for _ in range(n_steps_val):
                    y0_val += h_val * func(x0_val, y0_val)
                    x0_val += h_val
                    x_vals.append(x0_val)
                    y_vals.append(y0_val)

                result_label.config(text=f"Resultado: y({x0_val:.4f}) = {y0_val:.4f}")

                # Crear gráfica
                fig, ax = plt.subplots(figsize=(6, 4))
                ax.plot(x_vals, y_vals, 'g-', label='Solución de Taylor')
                ax.grid(True)
                ax.legend()
                ax.set_xlabel('X')
                ax.set_ylabel('Y')
                ax.set_title('Método de Taylor')

                # Si ya existe un canvas, eliminarlo
                for widget in window.winfo_children():
                    if isinstance(widget, FigureCanvasTkAgg):
                        widget.get_tk_widget().destroy()

                # Agregar el nuevo canvas
                canvas = FigureCanvasTkAgg(fig, master=window)
                canvas.draw()
                canvas.get_tk_widget().pack(pady=10)

            except Exception as e:
                messagebox.showerror("Error", f"Por favor verifique los datos ingresados.\n{str(e)}")

        # Botón calcular
        tk.Button(window,
                  text="Calcular",
                  command=calculate,
                  bg='#2ECC71',
                  fg='white').pack(pady=10)

    def runge_kutta_window(self):
        window = self.create_method_window("Método de Runge-Kutta")

        # Frame para entradas
        input_frame = tk.Frame(window, bg='#34495E')
        input_frame.pack(pady=20)

        # Función
        tk.Label(input_frame,
                 text="Función (dy/dx):",
                 bg='#34495E',
                 fg='white').grid(row=0, column=0, pady=5)
        function_entry = tk.Entry(input_frame)
        function_entry.grid(row=0, column=1, pady=5)

        # Condiciones iniciales
        tk.Label(input_frame,
                 text="Valor inicial de x:",
                 bg='#34495E',
                 fg='white').grid(row=1, column=0, pady=5)
        x0 = tk.Entry(input_frame)
        x0.grid(row=1, column=1, pady=5)

        tk.Label(input_frame,
                 text="Valor inicial de y:",
                 bg='#34495E',
                 fg='white').grid(row=2, column=0, pady=5)
        y0 = tk.Entry(input_frame)
        y0.grid(row=2, column=1, pady=5)

        # Paso
        tk.Label(input_frame,
                 text="Paso (h):",
                 bg='#34495E',
                 fg='white').grid(row=3, column=0, pady=5)
        h = tk.Entry(input_frame)
        h.grid(row=3, column=1, pady=5)

        # Número de pasos
        tk.Label(input_frame,
                 text="Número de pasos:",
                 bg='#34495E',
                 fg='white').grid(row=4, column=0, pady=5)
        n_steps = tk.Entry(input_frame)
        n_steps.grid(row=4, column=1, pady=5)

        # Resultado
        result_label = tk.Label(window,
                                text="",
                                bg='#34495E',
                                fg='white')
        result_label.pack(pady=20)

        def calculate():
            try:
                func = lambda x, y: eval(function_entry.get())
                x0_val = float(x0.get())
                y0_val = float(y0.get())
                h_val = float(h.get())
                n_steps_val = int(n_steps.get())

                x_vals = [x0_val]
                y_vals = [y0_val]

                for _ in range(n_steps_val):
                    k1 = h_val * func(x0_val, y0_val)
                    k2 = h_val * func(x0_val + 0.5 * h_val, y0_val + 0.5 * k1)
                    k3 = h_val * func(x0_val + 0.5 * h_val, y0_val + 0.5 * k2)
                    k4 = h_val * func(x0_val + h_val, y0_val + k3)
                    y0_val += (k1 + 2 * k2 + 2 * k3 + k4) / 6
                    x0_val += h_val
                    x_vals.append(x0_val)
                    y_vals.append(y0_val)

                result_label.config(text=f"Resultado: y({x0_val:.4f}) = {y0_val:.4f}")

                # Crear gráfica
                fig, ax = plt.subplots(figsize=(6, 4))
                ax.plot(x_vals, y_vals, 'g-', label='Solución de Runge-Kutta')
                ax.grid(True)
                ax.legend()
                ax.set_xlabel('X')
                ax.set_ylabel('Y')
                ax.set_title('Método de Runge-Kutta')

                # Si ya existe un canvas, eliminarlo
                for widget in window.winfo_children():
                    if isinstance(widget, FigureCanvasTkAgg):
                        widget.get_tk_widget().destroy()

                # Agregar el nuevo canvas
                canvas = FigureCanvasTkAgg(fig, master=window)
                canvas.draw()
                canvas.get_tk_widget().pack(pady=10)

            except Exception as e:
                messagebox.showerror("Error", f"Por favor verifique los datos ingresados.\n{str(e)}")

        # Botón calcular
        tk.Button(window,
                  text="Calcular",
                  command=calculate,
                  bg='#2ECC71',
                  fg='white').pack(pady=10)

if __name__ == "__main__":
    root = tk.Tk()
    app = CalculadoraNumerica(root)
    root.mainloop()