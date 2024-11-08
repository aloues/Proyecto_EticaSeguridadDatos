import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import pandas as pd
from hashlib import sha256
import logging
import re

# Configuración de logging
logging.basicConfig(filename='app.log', level=logging.INFO, format='%(asctime)s - %(message)s')

class DataSecurityApp:
    def __init__(self, root):
        self.root = root
        self.root.title("InstaTransaction")
        self.root.geometry("800x600")
        self.root.configure(bg='#003366')  # Fondo azul marino
        self.df = pd.read_csv('archivos/combined_dataset.csv')
        self.restricted_data = []  # Almacena la configuración de datos restringidos
        self.info_shown = False  # Controla si la información del usuario está visible
        self.show_consent_message()
        self.policy_updated = self.check_policy_update()     # Check for any updates to the privacy policy

    def show_consent_message(self):
        # Mensaje de consentimiento
        self.consent_frame = tk.Frame(self.root, bg='#003366')
        self.consent_frame.pack(fill=tk.BOTH, expand=True)

        consent_label = tk.Label(self.consent_frame, text="Consentimiento de Recolección de Datos", font=("Arial", 16, "bold"), fg="white", bg="#003366")
        consent_label.pack(pady=20)

        # Explicación sobre el uso de datos
        tk.Label(self.consent_frame, text="Esta aplicación recopilará su ID de Cliente y Contraseña para autenticación y verificación de transacciones. No se recopilarán datos innecesarios ni se compartirán con terceros.",
                 font=("Arial", 10), fg="white", bg="#003366", wraplength=600, justify="left").pack(pady=10)

        # Checkbox de aceptación de términos
        self.accept_terms_var = tk.BooleanVar()
        accept_checkbox = ttk.Checkbutton(self.consent_frame, text="He leído y acepto los términos", variable=self.accept_terms_var)
        accept_checkbox.pack(pady=20)

        # Botón de continuar
        ttk.Button(self.consent_frame, text="Aceptar", command=self.check_consent).pack(pady=20)

    def check_consent(self):
        if self.accept_terms_var.get():
            self.consent_frame.pack_forget()  # Oculta el mensaje de consentimiento
            self.create_login_screen()  # Muestra la pantalla de inicio de sesión
        else:
            messagebox.showwarning("Consentimiento Requerido", "Debe aceptar los términos para continuar.")

    def create_login_screen(self):
        # Welcome screen
        title_label = tk.Label(self.root, text="Bienvenido a InstaTransaction", font=("Arial", 20, "bold"), bg='#003366', fg='white')
        title_label.pack(pady=20)
        
        # ID input
        self.customer_id_label = ttk.Label(self.root, text="ID:", foreground='white', background='#003366')
        self.customer_id_label.pack(pady=5)
        self.customer_id_entry = ttk.Entry(self.root)
        self.customer_id_entry.pack(pady=5)
        
        # Password input
        self.password_label = ttk.Label(self.root, text="Contraseña:", foreground='white', background='#003366')
        self.password_label.pack(pady=5)
        self.password_entry = ttk.Entry(self.root, show="*")
        self.password_entry.pack(pady=5)
        
        # Button to toggle password visibility
        self.show_password = False
        self.toggle_password_button = tk.Button(self.root, text="Mostrar", command=self.toggle_password_visibility)
        self.toggle_password_button.pack(pady=5)
        
        # Login button
        self.login_button = ttk.Button(self.root, text="Iniciar sesión", command=self.verify_login)
        self.login_button.pack(pady=20)
        
        # Button to create a new password if not registered
        self.create_password_button = ttk.Button(self.root, text="Crear Nueva Contraseña", command=self.create_new_password)
        self.create_password_button.pack(pady=5)
        
        # Information label
        self.info_label = tk.Label(self.root, text="Iniciando sesión... Sus datos se usan solo para autenticación y verificación de transacciones.", font=("Arial", 8), bg='#003366', fg='yellow', wraplength=400)
        self.info_label.pack(pady=10)

    def toggle_password_visibility(self):
        """Toggle the visibility of the password in the password entry field."""
        if self.show_password:
            self.password_entry.config(show="*")
            self.toggle_password_button.config(text="Mostrar")
        else:
            self.password_entry.config(show="")
            self.toggle_password_button.config(text="Ocultar")
        self.show_password = not self.show_password

    def verify_login(self):
        # Get input from user
        customer_id = self.customer_id_entry.get().strip()
        password = self.password_entry.get().strip()
        
        # Ensure ID column is treated as string in case of mixed data types
        self.df['ID'] = self.df['ID'].astype(str)
        
        # Filter user data by ID and check if any matches
        user_data = self.df[self.df['ID'] == customer_id]
        
        if not user_data.empty:
            # Retrieve stored password
            stored_password = user_data.iloc[0].get('Password', None)
            
            if pd.isna(stored_password):
                self.info_label.config(text="No hay contraseña registrada para este ID. Use 'Crear Nueva Contraseña'.")
                self.show_password_requirements()
            else:
                # Check the hashed password against stored hash
                if sha256(password.encode()).hexdigest() == stored_password:
                    # Store user data and show main window
                    self.user_data = user_data.iloc[0]
                    self.info_label.config(text="Inicio de sesión exitoso.")
                    self.main_window()
                else:
                    self.info_label.config(text="Contraseña incorrecta.")
        else:
            self.info_label.config(text="ID inválido.")

    def show_password_requirements(self):
        """Display password requirements for creating a new password."""
        requirements = """
        Requisitos para la contraseña:
        - Mínimo 8 caracteres
        - Al menos una letra mayúscula
        - Al menos un carácter especial (!@#$%^&*)
        - Al menos un número
        """
        self.info_label.config(text=requirements)

    def create_new_password(self):
        customer_id = self.customer_id_entry.get()
        password = self.password_entry.get()
        user_data = self.df[self.df['ID'] == customer_id]

        if not user_data.empty:
            stored_password = user_data.iloc[0].get('Password', None)
            if pd.isna(stored_password):  # Verifica si no hay una contraseña registrada
                if self.is_valid_password(password):
                    # Guarda la nueva contraseña hasheada en el DataFrame
                    self.df.loc[self.df['ID'] == customer_id, 'Password'] = sha256(password.encode()).hexdigest()
                    self.df.to_csv('archivos/combined_dataset.csv', index=False)
                    self.info_label.config(text="Contraseña creada exitosamente. Ahora puede iniciar sesión.")
                else:
                    self.info_label.config(text="La contraseña no cumple con los requisitos. Intente nuevamente.")
                    self.show_password_requirements()
            else:
                self.info_label.config(text="Ya existe una contraseña registrada. Ingrese la contraseña para iniciar sesión.")
        else:
            self.info_label.config(text="ID inválido. No puede crear una contraseña para un ID que no existe.")

    def is_valid_password(self, password):
        """Check if the password meets the required conditions."""
        # Minimum 8 characters
        if len(password) < 8:
            return False
        # At least one uppercase letter
        if not re.search(r"[A-Z]", password):
            return False
        # At least one lowercase letter
        if not re.search(r"[a-z]", password):
            return False
        # At least one number
        if not re.search(r"[0-9]", password):
            return False
        # At least one special character
        if not re.search(r"[!@#$%^&*]", password):
            return False
        return True
    
    def main_window(self):
        # Limpia la ventana
        for widget in self.root.winfo_children():
            widget.destroy()

        # Botón de información en la esquina superior derecha
        self.info_button = tk.Button(self.root, text="?", font=("Arial", 12, "bold"), bg="white", command=self.toggle_user_info)
        self.info_button.place(x=770, y=10, width=20, height=20)

        # Mensaje de bienvenida
        welcome_label = tk.Label(self.root, text=f"Bienvenido, {self.user_data['Nombre']} {self.user_data['Apellido']}!",
                                 font=("Arial", 18, "bold"), bg='#003366', fg='white')
        welcome_label.pack(pady=10)

        # Marco de contenido dinámico para mostrar la información o las transacciones
        self.content_frame = tk.Frame(self.root, bg='#003366')
        self.content_frame.pack(fill=tk.BOTH, expand=True)

        # Info label to display messages to the user (initialize it here)
        self.info_label = tk.Label(self.root, text="", font=("Arial", 10), bg='#003366', fg='yellow')
        self.info_label.pack(pady=5)

        # Botón para restringir datos en la esquina inferior izquierda
        restrict_button = tk.Button(self.root, text="Restringir Uso de Mis Datos", command=self.restrict_data_usage, bg="orange", fg="black")
        restrict_button.place(x=10, y=560, width=200, height=30)

        # Download data button (Green button)
        download_button = tk.Button(self.root, text="Descargar Mis Datos", command=lambda: self.download_user_data(self.user_data['TransactionID']), bg="green", fg="white")
        download_button.place(x=220, y=560, width=200, height=30)

        # Botones de eliminar cuenta y cerrar sesión en la esquina inferior derecha
        delete_button = tk.Button(self.root, text="Eliminar Mi Cuenta", command=self.delete_account, bg="red", fg="white")
        delete_button.place(x=580, y=560, width=100, height=30)

        logout_button = tk.Button(self.root, text="Cerrar Sesión", command=self.logout, bg="red", fg="white")
        logout_button.place(x=690, y=560, width=100, height=30)

        # Muestra la selección de transacciones por defecto
        self.show_transactions()

    def download_user_data(self, transaction_id):  # Descargar datos del usuario como CSV
        user_data = self.df[self.df['TransactionID'] == transaction_id]
        
        if not user_data.empty:
            # Open a file dialog to choose where to save the file
            file_path = filedialog.asksaveasfilename(defaultextension=".csv", 
                                                    filetypes=[("CSV files", "*.csv")],
                                                    title="Guardar archivo como",
                                                    initialfile=f"{transaction_id}_data.csv")
            if file_path:  # Check if the user provided a path
                user_data.to_csv(file_path, index=False)
                self.info_label.config(text="Su archivo de datos se ha guardado correctamente.")
            else:
                self.info_label.config(text="Guardado cancelado.")
        else:
            self.info_label.config(text="No se encontraron datos para este usuario.")

    def toggle_user_info(self):
        # Alterna entre mostrar la información del usuario y la selección de transacciones
        if self.info_shown:
            self.show_transactions()  # Muestra las transacciones
            self.info_shown = False
        else:
            self.show_user_info()  # Muestra la información del usuario
            self.info_shown = True

    def show_user_info(self):
        # Limpia el marco de contenido y muestra la información del usuario
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        info_label = tk.Label(self.content_frame, text=f"Hola, {self.user_data['Nombre']} {self.user_data['Apellido']}! ¿En qué podemos ayudarte?", 
                              font=("Arial", 14), fg="white", bg="#003366")
        info_label.pack(pady=10)

        # Información detallada
        user_info_text = (f"Nombre: {self.user_data['Nombre']}\n"
                          f"Apellido: {self.user_data['Apellido']}\n"
                          f"Ubicación: {self.user_data['CustLocation']}\n"
                          f"Correo: {self.user_data['Correo']}\n"
                          f"Estado Civil: {self.user_data['Estado Civil']}")
        user_info_label = tk.Label(self.content_frame, text=user_info_text, font=("Arial", 12), fg="white", bg="#003366", justify="left")
        user_info_label.pack(anchor="w", padx=20)

        # Botón de edición a la derecha de la información del usuario
        edit_button = tk.Button(self.content_frame, text="Editar Mi Información", command=self.edit_user_data, bg="blue", fg="white")
        edit_button.pack(anchor="e", padx=20)

        # Display Privacy Policy below user information
        policy_title_label = tk.Label(self.content_frame, text="Política de Privacidad:", font=("Arial", 14, "bold"), fg="white", bg="#003366")
        policy_title_label.pack(pady=10)

        # Privacy policy text
        privacy_policy_text = """
        - Su información se usa exclusivamente para autenticación y verificación de transacciones. 
        - No se recopilan datos innecesarios y no compartimos sus datos con terceros sin su consentimiento.
        - Los datos se protegen mediante métodos de encriptación estándar de la industria.
        - Consentimiento: Al usar esta aplicación, usted acepta estos términos y condiciones.

        Actualización de Política de Privacidad
        - Nos reservamos el derecho de actualizar esta política. Cualquier cambio será notificado.
        """
        policy_label = tk.Label(self.content_frame, text=privacy_policy_text, font=("Arial", 10), fg="white", bg="#003366", wraplength=600, justify="left")
        policy_label.pack(pady=5)

    def check_policy_update(self):
        """
        Check if the privacy policy has been updated. 
        Returns True if updated, False otherwise.
        """
        current_policy_version = "1.1"  # Updated version
        try:
            with open('last_seen_policy_version.txt', 'r') as file:
                last_seen_version = file.read().strip()
        except FileNotFoundError:
            last_seen_version = None

        if last_seen_version != current_policy_version:
            # Update the last seen version
            with open('last_seen_policy_version.txt', 'w') as file:
                file.write(current_policy_version)
            return True  # Indicate that the policy was updated
        return False  # No update

    def show_transactions(self):
        # Limpia el marco de contenido y muestra las transacciones disponibles
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        tk.Label(self.content_frame, text="Seleccione el ID de Transacción para ver detalles:", font=("Arial", 12), fg="white", bg="#003366").pack(pady=10)

        # Desplegable para seleccionar TransactionID
        transaction_ids = self.user_data['TransactionID'].split(",")  # Ajusta esto según la estructura de los datos
        self.transaction_var = tk.StringVar()
        self.transaction_menu = ttk.Combobox(self.content_frame, textvariable=self.transaction_var, values=transaction_ids)
        self.transaction_menu.pack(pady=5)

        # Botón para ver detalles de la transacción seleccionada
        view_button = tk.Button(self.content_frame, text="Ver Detalles", command=self.show_transaction_details)
        view_button.pack(pady=10)

    def show_transaction_details(self):
        # Get the selected transaction ID
        transaction_id = self.transaction_var.get()
        
        # Check if transaction_id is selected
        if transaction_id:
            # Filter for the transaction in the DataFrame
            transaction_data = self.df[self.df['TransactionID'] == transaction_id]
            
            # Check if transaction exists and matches the logged-in customer ID
            if not transaction_data.empty and transaction_data['ID'].values[0] == self.user_data['ID']:
                # Clear content frame for transaction details
                for widget in self.content_frame.winfo_children():
                    widget.destroy()
                
                # Display transaction details
                columns = ["Ubicación", "Saldo en Cuenta", "Monto de Transacción", "Fecha", "Hora"]
                values = [
                    transaction_data['CustLocation'].values[0],
                    transaction_data['CustAccountBalance'].values[0],
                    transaction_data['TransactionAmount (INR)'].values[0],
                    transaction_data['TransactionDate'].values[0],
                    transaction_data['TransactionTime'].values[0]
                ]

                # Treeview to display transaction details
                tree = ttk.Treeview(self.content_frame, columns=columns, show="headings", height=1)
                tree.pack(pady=10)

                for col in columns:
                    tree.heading(col, text=col)
                    tree.column(col, anchor="center")

                tree.insert('', 'end', values=values)
            else:
                # Show message if transaction does not match customer ID
                messagebox.showwarning("Acceso Denegado", "No tiene permiso para ver esta información.")
        else:
            messagebox.showwarning("Transacción No Seleccionada", "Por favor, seleccione un ID de transacción.")



    def edit_user_data(self):
        # Ventana de edición en la misma pantalla
        edit_window = tk.Toplevel(self.root)
        edit_window.title("Editar Información Personal")
        edit_window.geometry("300x250")

        tk.Label(edit_window, text="Editar Correo:").pack(pady=5)
        email_entry = ttk.Entry(edit_window)
        email_entry.insert(0, self.user_data['Correo'])
        email_entry.pack(pady=5)

        tk.Label(edit_window, text="Editar Teléfono:").pack(pady=5)
        phone_entry = ttk.Entry(edit_window)
        phone_entry.insert(0, self.user_data['Telefono'])
        phone_entry.pack(pady=5)

        def save_changes():
            self.df.loc[self.df['ID'] == self.user_data['ID'], 'Correo'] = email_entry.get()
            self.df.loc[self.df['ID'] == self.user_data['ID'], 'Telefono'] = phone_entry.get()
            self.df.to_csv('archivos/combined_dataset.csv', index=False)
            self.user_data = self.df[self.df['ID'] == self.user_data['ID']].iloc[0]
            messagebox.showinfo("Éxito", "Datos actualizados exitosamente.")
            edit_window.destroy()

        ttk.Button(edit_window, text="Guardar Cambios", command=save_changes).pack(pady=20)

    def restrict_data_usage(self):
        # Ventana de restricción de datos
        restrict_window = tk.Toplevel(self.root)
        restrict_window.title("Restringir Uso de Datos")
        restrict_window.geometry("300x250")

        tk.Label(restrict_window, text="Seleccione hasta 2 datos para restringir su uso:").pack(pady=10)

        # Variables de selección para cada opción
        self.restrict_email_var = tk.BooleanVar()
        self.restrict_phone_var = tk.BooleanVar()
        self.restrict_status_var = tk.BooleanVar()
        self.restrict_location_var = tk.BooleanVar()

        # Creación de los checkboxes
        email_check = ttk.Checkbutton(restrict_window, text="Correo", variable=self.restrict_email_var, command=self.limit_restriction)
        phone_check = ttk.Checkbutton(restrict_window, text="Teléfono", variable=self.restrict_phone_var, command=self.limit_restriction)
        status_check = ttk.Checkbutton(restrict_window, text="Estado Civil", variable=self.restrict_status_var, command=self.limit_restriction)
        location_check = ttk.Checkbutton(restrict_window, text="Ubicación", variable=self.restrict_location_var, command=self.limit_restriction)

        # Posicionamiento de los checkboxes
        email_check.pack(pady=5)
        phone_check.pack(pady=5)
        status_check.pack(pady=5)
        location_check.pack(pady=5)

        def apply_restriction():
            # Guardar los datos restringidos seleccionados
            self.restricted_data = [data for data, var in zip(
                ["Correo", "Teléfono", "Estado Civil", "Ubicación"],
                [self.restrict_email_var, self.restrict_phone_var, self.restrict_status_var, self.restrict_location_var]
            ) if var.get()]
            
            if len(self.restricted_data) <= 2:
                messagebox.showinfo("Restricción Aplicada", f"Ha restringido el uso de: {', '.join(self.restricted_data)}.")
                restrict_window.destroy()
            else:
                messagebox.showwarning("Límite de Restricción", "Solo puede seleccionar hasta 2 datos para restringir.")

        # Botón para aplicar la restricción
        ttk.Button(restrict_window, text="Aplicar Restricción", command=apply_restriction).pack(pady=20)

    def limit_restriction(self):
        # Restringir a un máximo de 2 selecciones
        selected_count = sum([self.restrict_email_var.get(), self.restrict_phone_var.get(), 
                              self.restrict_status_var.get(), self.restrict_location_var.get()])
        if selected_count > 2:
            messagebox.showwarning("Límite de Restricción", "Solo puede seleccionar hasta 2 datos para restringir.")
            # Desactivar la última selección realizada para mantener solo 2 seleccionadas
            if self.restrict_email_var.get():
                self.restrict_email_var.set(False)
            elif self.restrict_phone_var.get():
                self.restrict_phone_var.set(False)
            elif self.restrict_status_var.get():
                self.restrict_status_var.set(False)
            elif self.restrict_location_var.get():
                self.restrict_location_var.set(False)

    def delete_account(self):
        response = messagebox.askyesno("Eliminar Cuenta", "¿Está seguro de que desea eliminar su cuenta y todos los datos asociados?")
        if response:
            self.df = self.df[self.df['ID'] != self.user_data['ID']]
            self.df.to_csv('archivos/combined_dataset.csv', index=False)
            messagebox.showinfo("Cuenta Eliminada", "Su cuenta ha sido eliminada exitosamente.")
            self.logout()

    def logout(self):
        # Regresa a la pantalla de login
        for widget in self.root.winfo_children():
            widget.destroy()
        self.show_consent_message()

if __name__ == '__main__':
    root = tk.Tk()
    app = DataSecurityApp(root)
    root.mainloop()
