class Estudiante:
    def __init__(self, nombre, edad, notas):
        self.nombre = nombre  
        self.edad = edad
        self.notas = notas

    def mostrar_info(self):
        print("Nombre:", self.nombre)
        print("Edad:", self.edad)
        if self.notas: 
            promedio = sum(self.notas) / len(self.notas)
            print("Promedio:", promedio)
        else:
            print("No hay notas registradas.")

    def agregar_nota(self, nota): 
        self.notas.append(nota)

e = Estudiante("Erika", 21, [15, 18, 17])
e.mostrar_info()
e.agregar_nota(20)
print("\nDespués de agregar una nota:")
e.mostrar_info()
