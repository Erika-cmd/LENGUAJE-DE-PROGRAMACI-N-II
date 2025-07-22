from datetime import datetime

class Persona:
    def __init__(self, nombre): self._nombre = nombre
    def get_nombre(self): return self._nombre
    def set_nombre(self, nombre): self._nombre = nombre
    def __del__(self): print(f"[INFO] Persona eliminada: {self._nombre}")

class Evento:
    def __init__(self, desc, fecha, hora, imp=False):
        self._desc = desc
        self._fecha = datetime.strptime(f"{fecha} {hora}", "%d/%m/%Y %H:%M")
        self._imp = imp
    def es_importante(self): return self._imp
    def obtener_fecha(self): return self._fecha
    def __str__(self): return f"{self._desc} - {self._fecha.strftime('%d/%m/%Y %H:%M')} {'❗' if self._imp else ''}"
    def __del__(self): print(f"[INFO] Evento eliminado: {self._desc}")

class Agenda(Persona):
    def __init__(self, nombre):
        super().__init__(nombre)
        self._eventos = []

    def agregar_evento(self, desc, fecha, hora, imp=False):
        self._eventos.append(Evento(desc, fecha, hora, imp))
        self._eventos.sort(key=lambda e: e.obtener_fecha())

    def eliminar_evento(self, idx):
        if 0 <= idx < len(self._eventos): del self._eventos[idx]

    def mostrar_eventos(self): return [str(e) for e in self._eventos]
    def mostrar_importantes(self): return [str(e) for e in self._eventos if e.es_importante()]

    def notificacion(self):
        ahora = datetime.now()
        for e in self._eventos:
            if 0 <= (e.obtener_fecha() - ahora).total_seconds() <= 86400:
                return f"🔔 ¡Próximo evento!\n{e}"
        return "🔕 No hay eventos próximos en 24h."

if __name__ == "__main__":
    agenda = Agenda(input("Ingrese su nombre: "))
    while True:
        print("\n1. Agregar\n2. Ver\n3. Importantes\n4. Eliminar\n5. Notificación\n6. Salir")
        op = input("Opción: ")

        if op == "1":
            d = input("Descripción: ")
            f = input("Fecha (dd/mm/yyyy): ")
            h = input("Hora (HH:MM): ")
            i = input("¿Importante? (s/n): ").lower() == "s"
            agenda.agregar_evento(d, f, h, i)
        elif op == "2":
            print("\n📅 Eventos:")
            for i, e in enumerate(agenda.mostrar_eventos(), 1): print(f"{i}. {e}")
        elif op == "3":
            print("\n❗ Importantes:")
            for e in agenda.mostrar_importantes(): print(e)
        elif op == "4":
            idx = int(input("Índice a eliminar (1...): ")) - 1
            agenda.eliminar_evento(idx)
        elif op == "5":
            print(agenda.notificacion())
        elif op == "6":
            print("👋 ¡Hasta luego!")
            break
        else:
            print("❌ Opción inválida.")
