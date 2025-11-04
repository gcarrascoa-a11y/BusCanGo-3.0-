import tkinter as tk
import folium
from folium.plugins import MiniMap, Fullscreen
import os
from config import MAP_CENTER, MAP_ZOOM
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
        # Coordenadas (usar configuración si está disponible)
        try:
            center = MAP_CENTER
            zoom = MAP_ZOOM
        except Exception:
            center = [-29.9533, -71.3436]
            zoom = 13

        # Crear mapa base sin tiles para poder añadir varias capas
        m = folium.Map(location=center, zoom_start=zoom, control_scale=True)

        # Capas de tiles alternativas
        folium.TileLayer('OpenStreetMap', name='OpenStreetMap').add_to(m)
        folium.TileLayer('Stamen Terrain', name='Stamen Terrain').add_to(m)
        folium.TileLayer('Stamen Toner', name='Stamen Toner').add_to(m)

        # Título en el mapa (se define antes de la comprobación de Google para poder añadir avisos)
        title_html = '<h3 align="center" style="font-size:20px"><b>BuScanGo - Mapa de Coquimbo</b></h3>'

        # Opción: capa de Google Maps (requiere API Key y uso bajo términos de Google)
        use_google = os.getenv('USE_GOOGLE_MAPS', '').lower() in ('1', 'true', 'yes')
        google_key = os.getenv('GOOGLE_MAPS_API_KEY')
        if use_google:
            if google_key:
                # Atención: el uso de tiles de Google está sujeto a los términos de Google Maps.
                # Asegúrate de tener habilitado el API y facturación si corresponde.
                google_tiles = f"https://mt1.google.com/vt/lyrs=m&x={{x}}&y={{y}}&z={{z}}&key={google_key}"
                folium.TileLayer(tiles=google_tiles, attr='Google', name='Google Maps', overlay=False, control=True).add_to(m)
            else:
                # Si no hay API key, no añadimos la capa y dejamos la advertencia en el mapa (título)
                title_html += '<br><small style="color:orange">(USE_GOOGLE_MAPS activo pero falta GOOGLE_MAPS_API_KEY)</small>'

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
        # Controles y plugins adicionales
        MiniMap(toggle_display=True, position='bottomright').add_to(m)
        Fullscreen(position='topright').add_to(m)
        folium.LayerControl(collapsed=False).add_to(m)
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