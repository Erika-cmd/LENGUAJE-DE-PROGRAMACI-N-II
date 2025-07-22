import winsound  # Solo funciona en Windows

# ────────────────────
# Clase base (superclase): Animal
# ────────────────────
class Animal:
    def __init__(self, nombre: str, edad: int, especie: str) -> None:
        # Encapsulamiento: Atributos privados
        self.__nombre = nombre
        self.__edad = edad
        self.__especie = especie

    # Getters para acceder a los atributos encapsulados
    def get_nombre(self) -> str:
        return self.__nombre

    def get_edad(self) -> int:
        return self.__edad

    def get_especie(self) -> str:
        return self.__especie

    # Método polimórfico: debe ser implementado por las subclases
    def get_tipo_animal(self) -> str:
        raise NotImplementedError("El método get_tipo_animal debe ser implementado por las subclases.")

    def get_detalles_especificos(self) -> str:
        return ""  # Por defecto, sin detalles específicos

    def mostrar_informacion(self) -> None:
        print(f"\n--- Información del Animal ---")
        print(f"Tipo    : {self.get_tipo_animal()}")
        print(f"Nombre  : {self.get_nombre()}")
        print(f"Edad    : {self.get_edad()} años")
        print(f"Especie : {self.get_especie()}")
        detalles = self.get_detalles_especificos()
        if detalles:
            print(f"Detalles: {detalles}")
        print("-" * 30)

# ────────────────────
# Subclase: Felino
# ────────────────────
class Felino(Animal):
    def __init__(self, nombre: str, edad: int, especie: str, colorpelaje: str) -> None:
        super().__init__(nombre, edad, especie)
        self.__colorpelaje = colorpelaje

    def get_colorpelaje(self) -> str:
        return self.__colorpelaje

    def get_tipo_animal(self) -> str:
        return "Felino"

    def get_detalles_especificos(self) -> str:
        return f"Color de Pelaje: {self.__colorpelaje}"

# ────────────────────
# Subclase: Ave
# ────────────────────
class Ave(Animal):
    def __init__(self, nombre: str, edad: int, especie: str, tipo_pico: str) -> None:
        super().__init__(nombre, edad, especie)
        self.__tipo_pico = tipo_pico

    def get_tipo_pico(self) -> str:
        return self.__tipo_pico

    def get_tipo_animal(self) -> str:
        return "Ave"

    def get_detalles_especificos(self) -> str:
        return f"Tipo de Pico: {self.__tipo_pico}"

# ────────────────────
# Función principal
# ────────────────────
def main():
    animales = []

    while True:
        print("\n****** SISTEMA DE GESTIÓN DE ANIMALES ******")
        print("1. Registrar Felino")
        print("2. Registrar Ave")
        print("3. Mostrar todos los animales")
        print("4. Salir")

        opcion = input("Selecciona una opción: ").strip()

        try:
            if opcion == "1":
                print("\n--- Registrar Nuevo Felino ---")
                nombre = input("Nombre del felino: ").strip()
                edad_str = input("Edad del felino: ").strip()
                especie = input("Especie del felino: ").strip()
                colorpelaje = input("Color de pelaje: ").strip()

                if not nombre or not edad_str or not especie or not colorpelaje:
                    print("✖ Error: Todos los campos son obligatorios.")
                    continue

                edad = int(edad_str)
                if edad < 0 or edad > 200:
                    raise ValueError("Edad inválida. Debe ser un número positivo y razonable.")

                felino = Felino(nombre, edad, especie, colorpelaje)
                animales.append(felino)
                print(f"✔ Felino '{nombre}' registrado correctamente.")
                winsound.Beep(700, 300)  # Sonido de confirmación

            elif opcion == "2":
                print("\n--- Registrar Nueva Ave ---")
                nombre = input("Nombre del ave: ").strip()
                edad_str = input("Edad del ave: ").strip()
                especie = input("Especie del ave: ").strip()
                tipo_pico = input("Tipo de pico: ").strip()

                if not nombre or not edad_str or not especie or not tipo_pico:
                    print("✖ Error: Todos los campos son obligatorios.")
                    continue

                edad = int(edad_str)
                if edad < 0 or edad > 200:
                    raise ValueError("Edad inválida. Debe ser un número positivo y razonable.")

                ave = Ave(nombre, edad, especie, tipo_pico)
                animales.append(ave)
                print(f"✔ Ave '{nombre}' registrada correctamente.")
                winsound.Beep(700, 300)  # Sonido de confirmación

            elif opcion == "3":
                if not animales:
                    print("\n✖ No hay animales registrados.")
                else:
                    print("\n--- Lista de Animales Registrados ---")
                    for animal in animales:
                        animal.mostrar_informacion()

            elif opcion == "4":
                print("Saliendo del sistema...")
                winsound.Beep(400, 500)  # Sonido al salir
                break

            else:
                print("✖ Opción inválida. Por favor, selecciona una opción del 1 al 4.")

        except ValueError as e:
            print(f"✖ Error de entrada: {e}. Intenta de nuevo.")
        except Exception as e:
            print(f"✖ Ocurrió un error inesperado: {e}")

# ────────────────────
# Punto de entrada
# ────────────────────
if __name__ == "__main__":
    main()
