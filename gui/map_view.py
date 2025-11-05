import tkinter as tk
import folium
import os
import tempfile
import webbrowser # 👈 Usaremos la biblioteca estándar de Python

class MapView(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.temp_file = None

        # 1. Crear el archivo del mapa al iniciar
        try:
            self._create_map_file()
            
            # 2. Crear un botón grande y claro para abrir el mapa
            launch_button = tk.Button(
                self, 
                text="🗺️ Abrir Mapa de Coquimbo", 
                command=self._open_map_in_browser,
                bg="#4285F4",  # Un color similar al de Google
                fg="white",
                font=("Arial", 14, "bold"),
                relief=tk.FLAT,
                padx=20,
                pady=15
            )
            launch_button.pack(expand=True, padx=50, pady=50)

        except Exception as e:
            self._display_error_message(f"Error fatal al crear el archivo del mapa: {e}")
            return

    def _create_map_file(self):
        """Crea el archivo HTML del mapa y lo guarda en una carpeta temporal."""
        # --- CAMBIOS AQUÍ ---
        # Coordenadas de Coquimbo
        map_center = [-29.9533, -71.3436]
        
        m = folium.Map(location=map_center, zoom_start=14, tiles='OpenStreetMap')
        
        title_html = '<h3 align="center" style="font-size:20px"><b>BuScanGo - Mapa de Coquimbo</b></h3>'
        m.get_root().html.add_child(folium.Element(title_html))

        # Marcadores de ejemplo para Coquimbo
        folium.Marker(
            [-29.9654, -71.3508], 
            popup='Cruz del Tercer Milenio',
            icon=folium.Icon(color='blue', icon='plus')
        ).add_to(m)
        
        folium.Marker(
            [-29.9545, -71.3440], 
            popup='Plaza de Armas de Coquimbo',
            icon=folium.Icon(color='green', icon='info-sign')
        ).add_to(m)

        folium.Marker(
            [-29.9366, -71.3364], 
            popup='Fuerte Lambert',
            icon=folium.Icon(color='red', icon='shield')
        ).add_to(m)
        # --- FIN DE LOS CAMBIOS ---

        # Guardar el archivo
        self.temp_file = os.path.join(tempfile.gettempdir(), "buscango_map.html")
        m.save(self.temp_file)

    def _open_map_in_browser(self):
        """Abre el archivo del mapa en el navegador web predeterminado."""
        if self.temp_file and os.path.exists(self.temp_file):
            webbrowser.open(f'file:///{self.temp_file}')
        else:
            self._display_error_message("Error: No se pudo encontrar el archivo del mapa para abrir.")
    
    def _display_error_message(self, message):
        """Muestra un mensaje de error si algo sale mal."""
        for widget in self.winfo_children():
            widget.destroy()
        error_label = tk.Label(self, text=message, fg="red", font=("Arial", 12))
        error_label.pack(expand=True)

    def __del__(self):
        """Limpia el archivo temporal al cerrar la aplicación."""
        try:
            if hasattr(self, 'temp_file') and self.temp_file and os.path.exists(self.temp_file):
                os.remove(self.temp_file)
        except Exception:
            pass