import tkinter as tk
from dotenv import load_dotenv
import os
import sys
from tkinter import messagebox

from gui import MainWindow
from database import DatabaseManager
from services import DataManager
from utils import setup_logger
from config import WINDOW_TITLE, WINDOW_SIZE

def main():
    try:
        # Cargar variables de entorno
        load_dotenv()
        
        # Configurar logger
        logger = setup_logger()
        logger.info("Iniciando aplicación")
        
        # Iniciar interfaz gráfica
        root = tk.Tk()
        root.withdraw()  # Ocultar ventana principal hasta login
        
        # Mostrar ventana de login
        from auth.login import LoginWindow
        login = LoginWindow(root)
        root.wait_window(login)
        
        if not hasattr(login, 'authenticated') or not login.authenticated:
            logger.info("Login cancelado")
            sys.exit(0)
            
        # Mostrar ventana principal
        root.deiconify()
        root.title(WINDOW_TITLE)
        root.geometry(WINDOW_SIZE)
        
        # Inicializar servicios
        db = DatabaseManager()
        data_manager = DataManager("data.json")
        
        # Crear ventana principal
        app = MainWindow(root, data_manager)
        app.pack(expand=True, fill="both")
        
        root.mainloop()
        
    except Exception as e:
        logger.error(f"Error al iniciar la aplicación: {str(e)}")
        messagebox.showerror("Error", f"Error al iniciar la aplicación: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()