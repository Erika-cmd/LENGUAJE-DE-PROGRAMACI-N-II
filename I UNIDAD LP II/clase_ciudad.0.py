import tkinter as tk, math
from tkinter import messagebox as mb

def calcular():
    try:
        ciudades = [e.get().split(",") for e in entradas]
        distancias = []
        for i in range(len(ciudades)):
            for j in range(i+1, len(ciudades)):
                x1, y1 = map(float, ciudades[i][1:])
                x2, y2 = map(float, ciudades[j][1:])
                d = math.hypot(x2 - x1, y2 - y1)
                distancias.append((ciudades[i][0], ciudades[j][0], d))
        
        res = "\n".join([f"Distancia entre {ci1} y {ci2}: {d:.2f}" for ci1, ci2, d in distancias])
        mb.showinfo("Resultados", res)
    except:
        mb.showerror("Error", "Entrada inválida, ingrese correctamente las ciudades y coordenadas.")

v = tk.Tk()
tk.Label(v, text="Ingrese ciudades y coordenadas (nombre,x,y) separadas por comas:").grid(row=0, column=0, columnspan=2)
entradas = []
for i in range(5):  # Ajusta el número de ciudades (aquí es 5 como ejemplo)
    tk.Label(v, text=f"Ciudad {i+1}").grid(row=i+1, column=0)
    e = tk.Entry(v)
    e.grid(row=i+1, column=1)
    entradas.append(e)

tk.Button(v, text="Calcular Distancias", command=calcular).grid(row=6, column=0, columnspan=2, pady=10)
v.mainloop()

