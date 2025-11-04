import tkinter as tk
from tkinter import ttk, messagebox

class LoginWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("BuScanGo - Inicio de Sesión")
        self.geometry("320x240")
        self.resizable(False, False)
        self.transient(parent)
        self.grab_set()
        
        # Centrar la ventana
        screen_width = parent.winfo_screenwidth()
        screen_height = parent.winfo_screenheight()
        x = (screen_width - 320) // 2
        y = (screen_height - 240) // 2
        self.geometry(f"320x240+{x}+{y}")
        
        self._init_components()
        self.authenticated = False
        
    def _init_components(self):
        main_frame = ttk.Frame(self, padding="20")
        main_frame.pack(fill="both", expand=True)
        
        # Título
        title_label = ttk.Label(main_frame, 
                             text="BuScanGo",
                             font=("Arial", 16, "bold"),
                             foreground="#2196F3")
        title_label.pack(pady=(0, 20))
        
        # Frame para inputs
        input_frame = ttk.Frame(main_frame)
        input_frame.pack(fill="x", pady=10)
        
        # Usuario
        ttk.Label(input_frame, text="Usuario:").pack(anchor="w")
        self.username_var = tk.StringVar()
        self.username_entry = ttk.Entry(input_frame, textvariable=self.username_var)
        self.username_entry.pack(fill="x", pady=(0, 10))
        
        # Contraseña
        ttk.Label(input_frame, text="Contraseña:").pack(anchor="w")
        self.password_var = tk.StringVar()
        self.password_entry = ttk.Entry(input_frame, textvariable=self.password_var, show="*")
        self.password_entry.pack(fill="x", pady=(0, 10))
        
        # Botón de inicio
        ttk.Button(main_frame, 
                 text="Iniciar Sesión",
                 command=self._login).pack(pady=10)
        
        # Vincular Enter a login
        self.bind('<Return>', lambda e: self._login())
        
        # Focus en usuario
        self.username_entry.focus()
    
    def _login(self):
        username = self.username_var.get().strip()
        password = self.password_var.get().strip()
        
        if not username or not password:
            messagebox.showerror("Error", "Por favor complete todos los campos")
            return
        
        if username == "admin" and password == "1234":
            self.authenticated = True
            self.destroy()
        else:
            messagebox.showerror("Error", "Usuario o contraseña incorrectos")
            self.username_var.set("")
            self.password_var.set("")
            self.username_entry.focus()