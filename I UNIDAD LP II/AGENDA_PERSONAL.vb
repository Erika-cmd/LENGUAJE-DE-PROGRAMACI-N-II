Imports System.Windows.Forms
Imports System.Data.SQLite ' Necesario instalar el paquete NuGet System.Data.SQLite

Public Class AgendaForm
    Inherits Form

    Private WithEvents ListaTareas As New ListBox()
    Private WithEvents BotonAgregar As New Button()
    Private WithEvents CajaTarea As New TextBox()
    Private conexionBD As SQLiteConnection

    Public Sub New()
        ' Inicialización de la interfaz de usuario
        ConfigurarGUI()

        ' Inicialización de la base de datos
        conexionBD = New SQLiteConnection("Data Source=agenda.db;Version=3;")
        conexionBD.Open()
        CrearTablaSiNoExiste()
        CargarTareas()
    End Sub

    Private Sub ConfigurarGUI()
        ' Configuración de los controles de la GUI
        BotonAgregar.Text = "Agregar Tarea"
        CajaTarea.Width = 200

        ' Diseño de la interfaz
        Me.Controls.Add(ListaTareas)
        Me.Controls.Add(BotonAgregar)
        Me.Controls.Add(CajaTarea)
    End Sub

    Private Sub CrearTablaSiNoExiste()
        Dim comando As New SQLiteCommand("CREATE TABLE IF NOT EXISTS tareas (id INTEGER PRIMARY KEY, descripcion TEXT)", conexionBD)
        comando.ExecuteNonQuery()
    End Sub

    Private Sub CargarTareas()
        ListaTareas.Items.Clear()
        Dim comando As New SQLiteCommand("SELECT descripcion FROM tareas", conexionBD)
        Dim lector As SQLiteDataReader = comando.ExecuteReader()

        While lector.Read()
            ListaTareas.Items.Add(lector("descripcion"))
        End While

        lector.Close()
    End Sub

    Private Sub BotonAgregar_Click(sender As Object, e As EventArgs) Handles BotonAgregar.Click
        ' Agregar tarea a la base de datos
        Dim descripcion As String = CajaTarea.Text
        Dim comando As New SQLiteCommand("INSERT INTO tareas (descripcion) VALUES (@descripcion)", conexionBD)
        comando.Parameters.AddWithValue("@descripcion", descripcion)
        comando.ExecuteNonQuery()

        ' Actualizar la lista de tareas en la GUI
        CargarTareas()

        ' Limpiar la caja de texto
        CajaTarea.Clear()
    End Sub

    Private Sub AgendaForm_FormClosing(sender As Object, e As FormClosingEventArgs) Handles Me.FormClosing
        ' Cerrar la conexión a la base de datos al cerrar el formulario
        If conexionBD IsNot Nothing Then
            conexionBD.Close()
        End If
    End Sub
End Class