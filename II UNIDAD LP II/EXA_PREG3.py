def mostrar_vehiculos(vehiculos):
    for v in vehiculos:
        v.mostrar_info()
        print(f"Impuesto: {v.calcular_impuesto():.2f}\n")
