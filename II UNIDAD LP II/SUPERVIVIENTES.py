import tkinter as tk
from tkinter import messagebox

def calcular_chupetines():
    try:
        limon = int(entry_limon.get())
        pera = int(entry_pera.get())
        huevo = int(entry_huevo.get())

        # Calcular cuántos chupetines se pueden formar
        chupetines = min(limon // 2, pera // 2, huevo // 2)

        # Calcular caramelos sobrantes
        sobrante_limon = limon - chupetines * 2
        sobrante_pera = pera - chupetines * 2
        sobrante_huevo = huevo - chupetines * 2

        resultado.set(f"Chupetines posibles: {chupetines}\n"
                      f"Sobrantes → Limón: {sobrante_limon}, Pera: {sobrante_pera}, Huevo: {sobrante_huevo}")
    except ValueError:
        messagebox.showerror("Error", "Por favor ingresa números enteros válidos.")

# Crear ventana
ventana = tk.Tk()
ventana.title("Juego de los Sobrevivientes 🍬")

# Etiquetas
tk.Label(ventana, text="Caramelos de Limón:").grid(row=0, column=0, sticky="w")
tk.Label(ventana, text="Caramelos de Pera:").grid(row=1, column=0, sticky="w")
tk.Label(ventana, text="Caramelos de Huevo:").grid(row=2, column=0, sticky="w")

# Entradas
entry_limon = tk.Entry(ventana)
entry_pera = tk.Entry(ventana)
entry_huevo = tk.Entry(ventana)
entry_limon.grid(row=0, column=1)
entry_pera.grid(row=1, column=1)
entry_huevo.grid(row=2, column=1)

# Botón
tk.Button(ventana, text="Calcular Chupetines", command=calcular_chupetines).grid(row=3, column=0, columnspan=2, pady=10)

# Resultado
resultado = tk.StringVar()
tk.Label(ventana, textvariable=resultado, fg="blue", font=("Arial", 11)).grid(row=4, column=0, columnspan=2)

ventana.mainloop()
