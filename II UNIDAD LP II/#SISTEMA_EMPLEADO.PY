# ────────────────────────
# Clase Principal: Empleado
# ────────────────────────
class Empleado:
    def __init__(self, nombre: str, dni: str, salario_base: float):
        self.__nombre = nombre
        self.__dni = dni
        self.__salario_base = salario_base

    # Getters (Encapsulamiento)
    def get_nombre(self):
        return self.__nombre

    def get_dni(self):
        return self.__dni

    def get_salario_base(self):
        return self.__salario_base

    # Polimorfismo
    def calcular_salario(self):
        raise NotImplementedError("Debe implementarse en las subclases")

    # Mostrar información (con polimorfismo)
    def mostrar_informacion(self):
        print("\n--- Información del Empleado ---")
        print(f"Nombre : {self.get_nombre()}")
        print(f"DNI    : {self.get_dni()}")

        if isinstance(self, Operario):
            print(f"Salario Base       : S/ {self.get_salario_base():.2f}")
            print(f"Bono Producción    : S/ {self.get_bono_produccion():.2f}")
            print(f"Salario Final      : S/ {self.calcular_salario():.2f}")
        elif isinstance(self, Administrativo):
            print(f"Salario Base       : S/ {self.get_salario_base():.2f}")
            print(f"Impuesto (10%)     : S/ {self.get_impuesto():.2f}")
            print(f"Salario Final      : S/ {self.calcular_salario():.2f}")
        else:
            print(f"Salario Base       : S/ {self.get_salario_base():.2f}")
            print(f"Salario Final      : S/ {self.calcular_salario():.2f}")

        print("-" * 30)

# ────────────────────────
# Subclase 1: Administrativo
# ────────────────────────
class Administrativo(Empleado):
    def __init__(self, nombre: str, dni: str, salario_base: float):
        super().__init__(nombre, dni, salario_base)

    def calcular_salario(self):
        return self.get_salario_base() * 0.90

    def get_impuesto(self):
        return self.get_salario_base() * 0.10

# ────────────────────────
# Subclase 2: Operario
# ────────────────────────
class Operario(Empleado):
    def __init__(self, nombre: str, dni: str, salario_base: float, bono_produccion: float):
        super().__init__(nombre, dni, salario_base)
        self.__bono_produccion = bono_produccion

    def get_bono_produccion(self):
        return self.__bono_produccion

    def calcular_salario(self):
        return self.get_salario_base() + self.get_bono_produccion()

# ────────────────────────
# Función principal
# ────────────────────────
def main():
    empleados = []

    while True:
        print("\n****** SISTEMA DE GESTIÓN DE EMPLEADOS ******")
        print("1. Registrar Administrativo")
        print("2. Registrar Operario")
        print("3. Mostrar empleados registrados")
        print("4. Salir")

        opcion = input("Selecciona una opción: ").strip()

        try:
            if opcion == "1":
                print("\n--- Registro de Administrativo ---")
                nombre = input("Nombre       : ").strip()
                dni = input("DNI          : ").strip()
                salario = float(input("Salario base : S/ "))

                administrativo = Administrativo(nombre, dni, salario)
                empleados.append(administrativo)
                print("✔ Administrativo registrado correctamente.")

            elif opcion == "2":
                print("\n--- Registro de Operario ---")
                nombre = input("Nombre             : ").strip()
                dni = input("DNI                : ").strip()
                salario = float(input("Salario base       : S/ "))
                bono = float(input("Bono producción    : S/ "))

                operario = Operario(nombre, dni, salario, bono)
                empleados.append(operario)
                print("✔ Operario registrado correctamente.")

            elif opcion == "3":
                if not empleados:
                    print("✖ No hay empleados registrados.")
                else:
                    for emp in empleados:
                        emp.mostrar_informacion()

            elif opcion == "4":
                print("Saliendo del sistema...")
                break
            else:
                print("✖ Opción inválida. Intenta nuevamente.")

        except ValueError:
            print("✖ Error: Debes ingresar valores válidos.")
        except Exception as e:
            print(f"✖ Error inesperado: {e}")

# ────────────────────────
# Punto de entrada
# ────────────────────────
if __name__ == "__main__":
    main()
