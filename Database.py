# Base de datos de usuarios con SQLite y Python | User database with SQLite and Python

# Importamos las librerias necesarias | Import the necessary libraries
import sqlite3
from tkinter import *
from tkinter import ttk
from tkinter import messagebox

# URL de la base de datos | Database URL
url = "Users.db"

#--------------------------------------------------------------


#----------------

# Funcion para insertar datos | Function to insert data
def insert():
    
    # Desactivar el boton de insertar | Disable the insert button
    button_insert.config(state="disabled")

    # Nueva ventana de Insertar datos | New window to insert data
    window_insert = Toplevel(window)
    window_insert.title("Insertar datos")
    window_insert.geometry("350x200")

    # Etiquetas de texto | Text labels
    Label(window_insert, text="Usuario", font=("Arial", 12)).grid(row=1, column=0)
    Label(window_insert, text="Email", font=("Arial", 12)).grid(row=2, column=0)
    Label(window_insert, text="Nombre", font=("Arial", 12)).grid(row=3, column=0)
    Label(window_insert, text="Apellido", font=("Arial", 12)).grid(row=4, column=0)
    Label(window_insert, text="Fecha de Nacimiento", font=("Arial", 12)).grid(row=5, column=0)

    # Entradas de texto | Text entries
    usuario_entry = Entry(window_insert, font=("Arial", 12))
    usuario_entry.grid(row=1, column=1)
    email_entry = Entry(window_insert, font=("Arial", 12))
    email_entry.grid(row=2, column=1)
    name_entry = Entry(window_insert, font=("Arial", 12))
    name_entry.grid(row=3, column=1)
    lastname_entry = Entry(window_insert, font=("Arial", 12))
    lastname_entry.grid(row=4, column=1)
    date_entry = Entry(window_insert, font=("Arial", 12))
    date_entry.grid(row=5, column=1)

    # Crear un botón para enviar los datos | Create a button to send the data
    Button(
        window_insert,
        text="Enviar",
        font=("Arial", 12),
        command=lambda: send_data(
            usuario_entry.get(),
            email_entry.get(),
            name_entry.get(),
            lastname_entry.get(),
            date_entry.get(),
        ),
    ).grid(row=6, column=0, columnspan=2)

    # Cerrar la ventana de insertar datos | Close the window to insert data
    window_insert.protocol("WM_DELETE_WINDOW", lambda: close_window_insert(window_insert))

#----------------


#----------------

# Función para cerrar la ventana de insertar datos y activar el boton de insertar | Function to close the window to insert data and activate the insert button
def close_window_insert(window_insert):
    
    window_insert.destroy()
    button_insert.config(state="normal")

#----------------


#----------------

# Función para enviar los datos a la base de datos en SQLite | Function to send the data to the SQLite database
def send_data(username, email, name, lastname, date):
    
    # Comprobar que los campos no esten vacios | Check that the fields are not emptyq
    if username == "" or email == "" or name == "" or lastname == "" or date == "":
        
        # Mostrar mensaje de error en ventana emergente | Show error message in popup window
        messagebox.showinfo("Error", "Por favor, Rellene todos los campos")
        return

    # Crear la conexión | Create the connection
    connection = sqlite3.connect(url)
    cursor = connection.cursor()

    # Crear la consulta SQL | Create the SQL query
    query = "INSERT INTO Username (username, email, name, last_name, date) VALUES (?, ?, ?, ?, ?)"

    # Ejecutar la consulta | Execute the query
    cursor.execute(query, (username, email, name, lastname, date))

    # Confirmar los cambios | Confirm the changes
    connection.commit()

    # Cerrar la conexión | Close the connection
    connection.close()

    # Mostrar los datos | Show the data
    update_data()

#----------------


#----------------

# Función para eliminar los datos de la base de datos | Function to delete the data from the database
def remove():
    
    # Obtiene los elementos seleccionados | Get the selected items
    selected_items = data.selection()

    # Comprueba que haya elementos seleccionados | Check that there are selected items
    for selected_item in selected_items:
        
        # Obtiene el elemento | Get the item
        item = data.item(selected_item)
        # Obtiene el ID del elemento | Get the ID of the item
        id = item["values"][0]
        # Elimina el elemento del Treeview | Delete the item from the Treeview
        data.delete(selected_item)

    # Crear la conexión | Create the connection
    connection = sqlite3.connect(url)
    cursor = connection.cursor()

    # Crear la consulta SQL | Create the SQL query
    query = "DELETE FROM Username WHERE id = ?"

    # Ejecutar la consulta | Execute the query
    cursor.execute(query, (id,))

    # Confirmar los cambios | Confirm the changes
    connection.commit()

    # Cerrar la conexión | Close the connection
    connection.close()

    # Mostrar los datos | Show the data
    update_data()

#----------------


#----------------

# Actualizar los datos en la tabla | Update the data in the table
def update_data():
    
    # Eliminar los elementos existentes | Delete existing items
    for row in data.get_children():
        
        data.delete(row)

    # Crear la conexión | Create the connection
    connection = sqlite3.connect(url)
    cursor = connection.cursor()

    # Realizar la consulta SQL | Make the SQL query
    cursor.execute("SELECT * FROM Username")

    # Guardar la consulta en una variable | Save the query in a variable
    results = cursor.fetchall()

    # Cerrar la conexión | Close the connection
    connection.close()

    # Insertar los nuevos datos | Insert the new data
    for row in results:
        
        data.insert("", "end", values=row)

#----------------


#--------------------------------------------------------------

# Crear la ventana principal | Create the main window
window = Tk()
window.title("Base de datos de suarios")

# Boton para insertar | Button to insert
button_insert = Button(
    window, text="Insertar", font=("Arial", 10), command=lambda: insert()
)
button_insert.grid(row=0, column=0)

# Boton para eliminar | Button to remove
button_remove = Button(
    window, text="Eliminar", font=("Arial", 10), command=lambda: remove()
)
button_remove.grid(row=0, column=3)

# Crear el Treeview | Create the Treeview
data = ttk.Treeview(window, show="headings")
data.grid(row=1, column=0, columnspan=4, padx=5, pady=5)

# Definir las columnas | Define the columns
data["columns"] = (
    "ID",
    "Usuario",
    "Email",
    "Nombre",
    "Apellido",
    "Fecha de Nacimiento",
)

# Formato de las columnas | Columns format
data.column("ID", width=100, anchor=CENTER)
data.column("Usuario", width=100, anchor=CENTER)
data.column("Email", width=200, anchor=CENTER)
data.column("Nombre", width=100, anchor=CENTER)
data.column("Apellido", width=100, anchor=CENTER)
data.column("Fecha de Nacimiento", width=120, anchor=CENTER)

# Nombre de las columnas | Columns name
data.heading("ID", text="ID")
data.heading("Usuario", text="Usuario")
data.heading("Email", text="Email")
data.heading("Nombre", text="Nombre")
data.heading("Apellido", text="Apellido")
data.heading("Fecha de Nacimiento", text="Fecha de Nacimiento")

# Mostrar los datos | Show the data
update_data()

# Loop para que funcione la aplicacion | Loop for the application to work
window.mainloop()
#--------------------------------------------------------------