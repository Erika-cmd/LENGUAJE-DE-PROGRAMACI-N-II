# Clase base Evento
class Evento:
    # Constructor (inicializa los atributos de la clase)
    def __init__(self, nombre, fecha):
        # Atributos privados (encapsulamiento): los datos son accesibles solo a través de métodos
        self.__nombre = nombre
        self.__fecha = fecha

    # Métodos getter (para obtener los valores de los atributos privados)
    def get_nombre(self):
        return self.__nombre

    def get_fecha(self):
        return self.__fecha

    # Método especial __str__ para representar el objeto como un string
    def __str__(self):
        return f"{self.__nombre} - {self.__fecha}"

# Clase EventoPersonal que hereda de la clase Evento
# Herencia: EventoPersonal es una subclase de Evento
class EventoPersonal(Evento):
    # Constructor de la clase EventoPersonal (llama al constructor de la clase base)
    def __init__(self, nombre, fecha, descripcion):
        # Heredamos los atributos de la clase base Evento usando super()
        super().__init__(nombre, fecha)
        self.__descripcion = descripcion  # Atributo privado adicional

    # Método getter para obtener la descripción del evento
    def get_descripcion(self):
        return self.__descripcion

    # Sobrescribimos el método __str__ para incluir la descripción en el string
    def __str__(self):
        return f"{super().__str__()} - {self.__descripcion}"

# Clase EventoLaboral que hereda de la clase Evento
# Herencia: EventoLaboral también es una subclase de Evento
class EventoLaboral(Evento):
    # Constructor de la clase EventoLaboral (llama al constructor de la clase base)
    def __init__(self, nombre, fecha, hora):
        # Heredamos los atributos de la clase base Evento usando super()
        super().__init__(nombre, fecha)
        self.__hora = hora  # Atributo privado adicional para la hora del evento

    # Método getter para obtener la hora del evento
    def get_hora(self):
        return self.__hora

    # Sobrescribimos el método __str__ para incluir la hora en el string
    def __str__(self):
        return f"{super().__str__()} - {self.__hora}"

# Clase Agenda para gestionar eventos
class Agenda:
    # Constructor de la clase Agenda
    def __init__(self):
        self.__eventos = []  # Lista privada (encapsulamiento) para almacenar los eventos

    # Método para agregar un evento a la agenda
    def agregar_evento(self, evento):
        self.__eventos.append(evento)  # Se agrega el evento a la lista
        print(f"Evento '{evento.get_nombre()}' agregado")

    # Método para mostrar todos los eventos de la agenda
    def mostrar_eventos(self):
        print("\nEventos:")
        for i, evento in enumerate(self.__eventos, start=1):
            print(f"{i}. {evento}")  # Muestra la representación de cada evento usando __str__

    # Método para eliminar un evento por índice
    def eliminar_evento(self, indice):
        if indice >= 0 and indice < len(self.__eventos):  # Verificación de índice válido
            del self.__eventos[indice]  # Se elimina el evento de la lista
            print("Evento eliminado")
        else:
            print("Índice inválido")

    # Método para obtener la lista de eventos (referencia a la lista)
    def get_eventos(self):
        return self.__eventos

    # Destructor de la clase Agenda (se ejecuta cuando el objeto se elimina)
    def __del__(self):
        print("Agenda eliminada")

# Función principal que permite al usuario interactuar con la agenda
def main():
    agenda = Agenda()  # Instanciación de un objeto Agenda
    print("=====================================")
    print(" ✨ Bienvenido a tu Agenda Personal, Erika ✨ ")
    print("=====================================")

    while True:
        # Opciones del menú para interactuar con la agenda
        print("\nOpciones:")
        print("1. Agregar evento personal")
        print("2. Agregar evento laboral")
        print("3. Mostrar eventos")
        print("4. Eliminar evento")
        print("5. Salir")
        opcion = input("Ingrese su opción: ")

        # Opción para agregar evento personal
        if opcion == "1":
            nombre = input("Ingrese nombre del evento: ")
            fecha = input("Ingrese fecha del evento: ")
            descripcion = input("Ingrese descripción del evento: ")
            evento = EventoPersonal(nombre, fecha, descripcion)  # Crear un evento personal
            agenda.agregar_evento(evento)  # Agregar el evento a la agenda
        # Opción para agregar evento laboral
        elif opcion == "2":
            nombre = input("Ingrese nombre del evento: ")
            fecha = input("Ingrese fecha del evento: ")
            hora = input("Ingrese hora del evento: ")
            evento = EventoLaboral(nombre, fecha, hora)  # Crear un evento laboral
            agenda.agregar_evento(evento)  # Agregar el evento a la agenda
        # Opción para mostrar los eventos
        elif opcion == "3":
            agenda.mostrar_eventos()  # Mostrar todos los eventos
        # Opción para eliminar evento
        elif opcion == "4":
            agenda.mostrar_eventos()  # Mostrar los eventos antes de eliminar
            indice = int(input("Ingrese el número del evento a eliminar: ")) - 1
            agenda.eliminar_evento(indice)  # Eliminar el evento por índice
        # Opción para salir
        elif opcion == "5":
            print("¡Hasta luego!")
            del agenda  # Eliminar la agenda y llamar al destructor
            break
        else:
            print("Opción inválida")  # Si la opción ingresada es inválida

# Verificamos si el script está siendo ejecutado directamente
if __name__ == "__main__":
    main()  # Ejecutar la función principal
