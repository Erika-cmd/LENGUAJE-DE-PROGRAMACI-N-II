import tkinter as tk
from tkinter import messagebox
from tkcalendar import Calendar
from datetime import datetime, timedelta

class AgendaApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Agenda Personal")
        self.root.geometry("800x600")
        self.root.configure(bg="white")

        self.eventos = []

        self.crear_portada()

    def crear_portada(self):
        self.portada = tk.Label(
            self.root,
            text="Bienvenida a tu agenda, Erika 🌟📒",
            font=("Segoe UI", 24, "bold"),
            fg="black",
            bg="white",
            pady=20
        )
        self.portada.pack(pady=20)

        self.instrucciones = tk.Label(
            self.root,
            text="Organiza tu día con facilidad, visualiza tus eventos y más...",
            font=("Segoe UI", 14),
            fg="#0277BD",
            bg="white"
        )
        self.instrucciones.pack(pady=10)

        self.eventos_frame = tk.Frame(self.root, bg="#F8BBD0", width=600, height=600)
        self.eventos_frame.pack(side="right", fill="both", expand=True)
        
        self.eventos_label = tk.Label(
            self.eventos_frame,
            text="Eventos Pendientes:",
            font=("Segoe UI", 18, "bold"),
            fg="black",
            bg="#F8BBD0"
        )
        self.eventos_label.pack(pady=20)

        self.eventos_listbox = tk.Listbox(
            self.eventos_frame,
            font=("Segoe UI", 12),
            fg="black",
            bg="#FFFFFF",
            selectmode="single",
            height=10,
            width=60
        )
        self.eventos_listbox.pack(padx=20, pady=20, fill="both", expand=True)

        self.sidebar = tk.Frame(self.root, bg="white", width=200, height=600)
        self.sidebar.pack(side="left", fill="y")

        self.notificaciones_btn = tk.Button(
            self.sidebar, text="Notificaciones", bg="white", fg="black", width=20, pady=10, command=self.mostrar_notificaciones)
        self.notificaciones_btn.pack(pady=10)

        self.importantes_btn = tk.Button(
            self.sidebar, text="Importantes ❗", bg="white", fg="black", width=20, pady=10, command=self.mostrar_importantes)
        self.importantes_btn.pack(pady=10)

        self.guardar_btn = tk.Button(
            self.sidebar, text="Guardar 💾", bg="white", fg="black", width=20, pady=10, command=self.guardar_evento)
        self.guardar_btn.pack(pady=10)

        self.agregar_btn = tk.Button(
            self.sidebar, text="Agregar Evento", bg="white", fg="black", width=20, pady=10, command=self.mostrar_formulario_evento)
        self.agregar_btn.pack(pady=10)

        self.eliminar_btn = tk.Button(
            self.sidebar, text="Eliminar Evento 🗑️", bg="white", fg="black", width=20, pady=10, command=self.eliminar_evento)
        self.eliminar_btn.pack(pady=10)

    def mostrar_notificaciones(self):
        if self.eventos:
            proximo_evento = min(self.eventos, key=lambda x: datetime.strptime(x["fecha"], "%d/%m/%Y"))
            fecha_evento = datetime.strptime(proximo_evento["fecha"], "%d/%m/%Y")
            if fecha_evento - datetime.now() <= timedelta(days=1):
                mensaje = f"¡Próximo evento!\n{proximo_evento['descripcion']} el {proximo_evento['fecha']} a las {proximo_evento['hora']}"
            else:
                mensaje = "No hay eventos próximos dentro de 24 horas."
            self.notificacion_popup(mensaje)
        else:
            self.notificacion_popup("No hay eventos programados.")

    def notificacion_popup(self, mensaje):
        popup = tk.Toplevel(self.root)
        popup.title("¡Notificación!")
        popup.geometry("400x200")
        popup.configure(bg="#FFEB3B")
        popup_label = tk.Label(
            popup,
            text=mensaje,
            font=("Segoe UI", 16, "bold"),
            fg="black",
            bg="#FFEB3B"
        )
        popup_label.pack(pady=30)
        popup_btn = tk.Button(
            popup,
            text="Cerrar",
            font=("Segoe UI", 12),
            bg="#F8BBD0",
            fg="black",
            command=popup.destroy
        )
        popup_btn.pack(pady=10)

    def mostrar_importantes(self):
        importantes = [evento for evento in self.eventos if evento["importante"]]
        if importantes:
            mensaje = "Importantes:\n" + "\n".join([f"{evento['descripcion']} - {evento['fecha']} {evento['hora']}" for evento in importantes])
            messagebox.showinfo("Eventos Importantes", mensaje)
        else:
            messagebox.showinfo("Eventos Importantes", "No tienes eventos importantes aún.")

    def guardar_evento(self):
        messagebox.showinfo("Guardar", "El evento ha sido guardado exitosamente.")

    def agregar_evento(self):
        descripcion = self.descripcion_entry.get()
        hora = self.hora_entry.get()
        importante = self.importante_var.get()

        self.selected_date = self.cal.get_date()

        if self.selected_date and descripcion and hora:
            evento = {
                "fecha": self.selected_date,
                "descripcion": descripcion,
                "hora": hora,
                "importante": bool(importante)
            }
            self.eventos.append(evento)
            self.eventos.sort(key=lambda x: datetime.strptime(x["fecha"], "%d/%m/%Y"))
            self.actualizar_eventos()
            messagebox.showinfo("Evento Agregado", "Evento agregado correctamente.")
            self.form_frame.pack_forget()
        else:
            messagebox.showwarning("Error", "Debes completar todos los campos.")

    def mostrar_formulario_evento(self):
        self.form_frame = tk.Frame(self.root, bg="white", pady=20)
        self.form_frame.pack(pady=10)

        self.fecha_label = tk.Label(self.form_frame, text="Selecciona la Fecha:", font=("Segoe UI", 12), fg="black", bg="white")
        self.fecha_label.grid(row=0, column=0, padx=10, pady=5)
        self.cal = Calendar(self.form_frame, selectmode='day', date_pattern='dd/mm/yyyy')
        self.cal.grid(row=0, column=1, padx=10, pady=5)

        self.descripcion_label = tk.Label(self.form_frame, text="Descripción del Evento:", font=("Segoe UI", 12), fg="black", bg="white")
        self.descripcion_label.grid(row=1, column=0, padx=10, pady=5)
        self.descripcion_entry = tk.Entry(self.form_frame, font=("Segoe UI", 12), fg="black")
        self.descripcion_entry.grid(row=1, column=1, padx=10, pady=5)

        self.hora_label = tk.Label(self.form_frame, text="Hora (HH:MM):", font=("Segoe UI", 12), fg="black", bg="white")
        self.hora_label.grid(row=2, column=0, padx=10, pady=5)
        self.hora_entry = tk.Entry(self.form_frame, font=("Segoe UI", 12), fg="black")
        self.hora_entry.grid(row=2, column=1, padx=10, pady=5)

        self.importante_var = tk.IntVar()
        self.importante_check = tk.Checkbutton(self.form_frame, text="Marcar como importante ❗", font=("Segoe UI", 12), variable=self.importante_var, bg="white")
        self.importante_check.grid(row=3, columnspan=2, pady=5)

        self.agregar_evento_btn = tk.Button(self.form_frame, text="Agregar Evento", bg="#F8BBD0", fg="black", font=("Segoe UI", 12, "bold"), command=self.agregar_evento)
        self.agregar_evento_btn.grid(row=4, columnspan=2, pady=10)

    def eliminar_evento(self):
        try:
            selected_event = self.eventos_listbox.curselection()
            if selected_event:
                index = selected_event[0]
                del self.eventos[index]
                self.actualizar_eventos()
                messagebox.showinfo("Evento Eliminado", "Evento eliminado correctamente.")
            else:
                messagebox.showwarning("Error", "Debes seleccionar un evento para eliminar.")
        except Exception as e:
            messagebox.showerror("Error", f"Hubo un problema al eliminar el evento: {e}")

    def actualizar_eventos(self):
        self.eventos_listbox.delete(0, tk.END)
        for evento in self.eventos:
            icono = "❗" if evento["importante"] else ""
            evento_texto = f"{evento['descripcion']:<20} {evento['fecha']} {evento['hora']} {icono}"
            self.eventos_listbox.insert(tk.END, evento_texto)

if __name__ == "__main__":
    root = tk.Tk()
    app = AgendaApp(root)
    root.mainloop()
