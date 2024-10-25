import tkinter as tk
from tkinter import ttk, simpledialog, messagebox
import pandas as pd
from hashlib import sha256
import logging

# Configuración de logging
logging.basicConfig(filename='app.log', level=logging.INFO, format='%(asctime)s - %(message)s')

class DataSecurityApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Data Security Application")
        self.root.geometry("800x600")
        self.root.configure(bg='#003366')  # Fondo azul marino
        self.df = pd.read_csv('archivos/combined_dataset.csv')
        self.login_window()

    def login_window(self):
        self.customer_id = simpledialog.askstring("Login", "Enter your Customer ID", parent=self.root)
        self.password = simpledialog.askstring("Login", "Enter your password", parent=self.root, show='*')
        self.verify_login(self.customer_id, self.password)

    def verify_login(self, customer_id, password):
        # Placeholder para verificación de contraseña
        if password == "12345":
            user_data = self.df[self.df['CustomerID'] == customer_id]
            if not user_data.empty:
                self.user_data = user_data
                messagebox.showinfo("Login Successful", "Login Successful")
                self.transaction_window()
            else:
                messagebox.showerror("Login Failed", "Invalid Customer ID")
                self.root.destroy()
        else:
            messagebox.showerror("Login Failed", "Invalid Password")
            self.root.destroy()

    def transaction_window(self):
        ttk.Label(self.root, text="Enter Transaction ID:", foreground='white', background='#003366').pack(pady=10)
        self.transaction_id_entry = ttk.Entry(self.root)
        self.transaction_id_entry.pack(pady=10)
        ttk.Button(self.root, text="Verify Transaction", command=self.verify_transaction).pack(pady=20)
        ttk.Button(self.root, text="Encrypt Emails", command=self.encrypt_emails).pack(pady=10)
        ttk.Button(self.root, text="Decrypt Emails", command=self.decrypt_emails).pack(pady=10)
        ttk.Button(self.root, text="Hash Data", command=self.hash_data).pack(pady=10)
        ttk.Button(self.root, text="Log Activity", command=self.log_activity).pack(pady=10)

    def verify_transaction(self):
        transaction_id = self.transaction_id_entry.get()
        if self.user_data[self.user_data['TransactionID'] == transaction_id].empty:
            messagebox.showerror("Access Denied", "No tiene acceso a ver esta información")
        else:
            selected_transaction = self.user_data[self.user_data['TransactionID'] == transaction_id].iloc[0]
            info = (f"Welcome {selected_transaction['Nombre']} {selected_transaction['Apellido']}\n"
                    f"Email: {selected_transaction['Correo']}\n"
                    f"Phone: {selected_transaction['Telefono']}\n"
                    f"Civil Status: {selected_transaction['Estado Civil']}\n"
                    f"Customer ID: {selected_transaction['CustomerID']}\n"
                    f"Gender: {selected_transaction['CustGender']}\n"
                    f"Location: {selected_transaction['CustLocation']}\n"
                    f"Account Balance: {selected_transaction['CustAccountBalance']}\n"
                    f"Transaction Amount: {selected_transaction['TransactionAmount (INR)']}\n"
                    f"Transaction Date: {selected_transaction['TransactionDate']}\n"
                    f"Transaction Time: {selected_transaction['TransactionTime']}")
            messagebox.showinfo("Transaction Details", info)

    def encrypt_emails(self):
        self.user_data['Correo'] = self.user_data['Correo'].apply(lambda x: sha256(x.encode()).hexdigest())
        messagebox.showinfo("Success", "Emails encrypted successfully.")

    def decrypt_emails(self):
        self.user_data['Correo'] = self.user_data['Correo'].apply(lambda x: sha256)
        messagebox.showinfo("Notice", "Decryption not applicable after hashing.")

    def hash_data(self):
        self.user_data['Correo'] = self.user_data['Correo'].apply(lambda x: sha256(x.encode()).hexdigest())
        messagebox.showinfo("Success", "Data hashed successfully.")

    def log_activity(self):
        logging.info("User logged activity.")
        messagebox.showinfo("Log", "Activity logged successfully.")

if __name__ == '__main__':
    root = tk.Tk()
    app = DataSecurityApp(root)
    root.mainloop()
