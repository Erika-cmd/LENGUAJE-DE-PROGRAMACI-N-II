notas = [float(input(f"Nota {i+1}: ")) for i in range(30)]
prom = sum(notas) / len(notas)
mayores = sum(1 for n in notas if n > prom)
print(f"Promedio: {prom:.2f}")
print(f"Mayores al promedio: {mayores}")
