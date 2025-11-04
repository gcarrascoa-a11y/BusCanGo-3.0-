import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from .map_view import MapView
from .styles import Styles
from models.bus import Bus

class MainWindow(tk.Frame):
    def __init__(self, parent, data_manager):
        super().__init__(parent)
        self.data_manager = data_manager
        self.parent = parent
        
        # Mostrar mensaje de bienvenida
        self._mostrar_bienvenida()
        
        self._create_menu()
        self._init_ui()
        self.styles = Styles()
        self.styles.apply_style(self)
        
    def _mostrar_bienvenida(self):
        """Muestra un mensaje de bienvenida al iniciar la aplicación"""
        # Crear ventana de bienvenida
        welcome_window = tk.Toplevel(self.parent)
        welcome_window.title("Bienvenido")
        welcome_window.geometry("400x200")
        welcome_window.transient(self.parent)
        welcome_window.overrideredirect(True)  # Quitar bordes de la ventana
        
        # Centrar la ventana
        screen_width = self.parent.winfo_screenwidth()
        screen_height = self.parent.winfo_screenheight()
        x = (screen_width - 400) // 2
        y = (screen_height - 200) // 2
        welcome_window.geometry(f"400x200+{x}+{y}")
        
        # Frame principal con fondo
        main_frame = ttk.Frame(welcome_window, style="Welcome.TFrame")
        main_frame.pack(fill="both", expand=True)
        
        # Título
        title_label = ttk.Label(main_frame, 
                              text="Bienvenido a BuScanGo",
                              font=("Arial", 24, "bold"),
                              foreground="#2196F3")
        title_label.pack(pady=(40, 10))
        
        # Subtítulo
        subtitle_label = ttk.Label(main_frame,
                                 text="Sistema de Gestión y Monitoreo de Rutas de Buses",
                                 font=("Arial", 12),
                                 foreground="#666666")
        subtitle_label.pack(pady=5)
        
        # Configurar estilo
        style = ttk.Style()
        style.configure("Welcome.TFrame", background="white")
        style.configure("Welcome.TLabel", background="white")
        
        # Hacer que la ventana desaparezca después de 3 segundos
        self.parent.after(3000, welcome_window.destroy)
        
    def _create_menu(self):
        menubar = tk.Menu(self.parent)
        
        # Menú Archivo
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Nuevo Bus", command=self._nuevo_bus)
        file_menu.add_command(label="Nueva Ruta", command=self._nueva_ruta)
        file_menu.add_separator()
        file_menu.add_command(label="Salir", command=self.parent.quit)
        menubar.add_cascade(label="Archivo", menu=file_menu)
        
        self.parent.config(menu=menubar)
    
    def _init_ui(self):
        # Notebook principal
        self.notebook = ttk.Notebook(self)
        
        # Pestaña de mapa
        self.map_frame = ttk.Frame(self.notebook)
        self.map_view = MapView(self.map_frame)
        self.map_view.pack(expand=True, fill="both")
        
        # Pestaña de gestión
        self.management_frame = self._create_management_frame()
        
        self.notebook.add(self.map_frame, text="Mapa")
        self.notebook.add(self.management_frame, text="Gestión")
        self.notebook.pack(expand=True, fill="both", padx=5, pady=5)
    
    def _create_management_frame(self):
        """Crea el frame de gestión con botones para manejar rutas.

        Oculta el botón de asignar flota y muestra el menú con acciones de rutas:
        Agregar Ruta, Editar Ruta y Eliminar Ruta.
        """
        frame = ttk.Frame(self.notebook)

        gestion_frame = ttk.LabelFrame(frame, text="Gestión")
        gestion_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Panel de buses
        bus_panel = ttk.LabelFrame(gestion_frame, text="Gestión de Buses")
        bus_panel.pack(fill="x", padx=6, pady=(6, 4))
        ttk.Button(bus_panel, text="Agregar Bus", command=self._nuevo_bus).pack(side="left", padx=6)
        ttk.Button(bus_panel, text="Listar Buses", command=self._listar_buses).pack(side="left", padx=6)

        # Panel de rutas
        route_panel = ttk.LabelFrame(gestion_frame, text="Gestión de Rutas")
        route_panel.pack(fill="x", padx=6, pady=(4, 6))
        ttk.Button(route_panel, text="Agregar Ruta", command=self._nueva_ruta).pack(side="left", padx=6)
        ttk.Button(route_panel, text="Editar Ruta", command=self._editar_ruta_seleccionar).pack(side="left", padx=6)
        ttk.Button(route_panel, text="Eliminar Ruta", command=self._eliminar_ruta_seleccionar).pack(side="left", padx=6)

        return frame
    
    def _nuevo_bus(self):
        """Abre diálogo para crear nuevo bus"""
        dialog = BusDialog(self.parent, self.data_manager)
        self.parent.wait_window(dialog.dialog)
    
    def _nueva_ruta(self):
        """Abre diálogo para crear nueva ruta"""
        dialog = RutaDialog(self.parent, self.data_manager)
        self.parent.wait_window(dialog.dialog)
    
    def _listar_buses(self):
        """Muestra lista de buses"""
        try:
            datos = self.data_manager.cargar_datos()
            buses = datos.get('buses', {})
            
            if not buses:
                messagebox.showinfo("Lista de Buses", "No hay buses registrados")
                return
            
            # Crear ventana de lista
            list_window = tk.Toplevel(self.parent)
            list_window.title("Lista de Buses")
            list_window.geometry("500x400")
            list_window.transient(self.parent)
            
            # Frame principal
            main_frame = ttk.Frame(list_window, padding="10")
            main_frame.pack(fill="both", expand=True)
            # Frame de botones
            button_frame = ttk.Frame(main_frame)
            button_frame.pack(fill="x", pady=(0, 8))

            # Los botones dependen del Treeview, se enlazan por referencia más abajo
            ttk.Button(button_frame, text="Editar Bus", command=lambda: self._editar_bus_on_selection(tree, buses)).pack(side="left", padx=5)
            ttk.Button(button_frame, text="Eliminar Bus", command=lambda: self._eliminar_bus_on_selection(tree)).pack(side="left", padx=5)
            ttk.Button(button_frame, text="Actualizar", command=lambda: self._actualizar_lista_buses(tree, buses)).pack(side="left", padx=5)

            # Treeview para mostrar buses
            columns = ("Número", "Capacidad", "Estado", "Pasajeros")
            tree = ttk.Treeview(main_frame, columns=columns, show="headings", height=15)
            
            # Configurar columnas
            for col in columns:
                tree.heading(col, text=col)
                tree.column(col, width=100)
            
            # Agregar datos
            for numero, bus_data in buses.items():
                tree.insert("", "end", values=(
                    numero,
                    bus_data.get('capacidad', 'N/A'),
                    bus_data.get('estado', 'N/A'),
                    bus_data.get('pasajeros', 0)
                ))
            
            # Scrollbar
            scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=tree.yview)
            tree.configure(yscrollcommand=scrollbar.set)
            
            tree.pack(side="left", fill="both", expand=True)
            scrollbar.pack(side="right", fill="y")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar la lista de buses: {str(e)}")
    
    def _editar_recorrido(self, nombre_ruta, ruta_data):
        """Abre diálogo para editar el recorrido de una ruta"""
        dialog = EditarRecorridoDialog(self.parent, self.data_manager, nombre_ruta, ruta_data)
        self.parent.wait_window(dialog.dialog)
        self._listar_rutas()  # Actualizar la lista después de editar

    def _open_fleet_manager(self):
        """Abre el gestor de flota (diálogo)"""
        dialog = FleetManagerDialog(self.parent, self.data_manager)
        self.parent.wait_window(dialog.dialog)

    def _editar_bus_on_selection(self, tree, buses):
        """Edita el bus seleccionado en el Treeview"""
        selection = tree.selection()
        if not selection:
            messagebox.showinfo("Editar Bus", "Seleccione un bus de la lista")
            return
        item = selection[0]
        numero = tree.item(item)['values'][0]
        bus_data = buses.get(numero)
        if not bus_data:
            messagebox.showerror("Error", "Datos del bus no encontrados")
            return
        dialog = EditBusDialog(self.parent, self.data_manager, numero, bus_data)
        self.parent.wait_window(dialog.dialog)
        # Refrescar
        datos = self.data_manager.cargar_datos()
        self._actualizar_lista_buses(tree, datos.get('buses', {}))

    def _eliminar_bus_on_selection(self, tree):
        """Elimina el bus seleccionado con confirmación"""
        selection = tree.selection()
        if not selection:
            messagebox.showinfo("Eliminar Bus", "Seleccione un bus de la lista")
            return
        item = selection[0]
        numero = tree.item(item)['values'][0]
        if messagebox.askyesno("Confirmar Eliminación", f"¿Está seguro de que desea eliminar el bus '{numero}'?"):
            try:
                datos = self.data_manager.cargar_datos()
                datos.get('buses', {}).pop(numero, None)
                self.data_manager.guardar_datos(datos)
                messagebox.showinfo("Éxito", f"Bus '{numero}' eliminado exitosamente")
                self._actualizar_lista_buses(tree, datos.get('buses', {}))
            except Exception as e:
                messagebox.showerror("Error", f"Error al eliminar el bus: {str(e)}")

    def _actualizar_lista_buses(self, tree, buses):
        # Limpiar
        for it in tree.get_children():
            tree.delete(it)
        for numero, bus_data in buses.items():
            tree.insert("", "end", values=(
                numero,
                bus_data.get('capacidad', 'N/A'),
                bus_data.get('estado', 'N/A'),
                bus_data.get('pasajeros', 0)
            ))

    def _editar_ruta(self, nombre_ruta, ruta_data):
        """Abre diálogo para editar información de una ruta"""
        dialog = EditarRutaDialog(self.parent, self.data_manager, nombre_ruta, ruta_data)
        self.parent.wait_window(dialog.dialog)
        # Refrescar no es posible aquí porque no sabemos el Treeview, el llamado externo lo hará
    
    def _listar_rutas(self):
        """Muestra lista de rutas"""
        try:
            datos = self.data_manager.cargar_datos()
            rutas = datos.get('rutas', {})
            
            if not rutas:
                messagebox.showinfo("Lista de Rutas", "No hay rutas registradas")
                return
            
            # Crear ventana de lista
            list_window = tk.Toplevel(self.parent)
            list_window.title("Lista de Rutas")
            list_window.geometry("600x400")
            list_window.transient(self.parent)
            
            # Frame principal
            main_frame = ttk.Frame(list_window, padding="10")
            main_frame.pack(fill="both", expand=True)
            
            # Frame para botones de acción (arriba del Treeview)
            button_frame = ttk.Frame(main_frame)
            button_frame.pack(fill="x", pady=(0, 8))
            ttk.Button(button_frame, text="Editar Recorrido", command=lambda: self._editar_recorrido_on_selection(tree, rutas)).pack(side="left", padx=5)
            ttk.Button(button_frame, text="Editar Información", command=lambda: self._editar_ruta_on_selection(tree, rutas)).pack(side="left", padx=5)
            ttk.Button(button_frame, text="Eliminar", command=lambda: self._confirmar_eliminar_ruta_on_selection(tree)).pack(side="left", padx=5)
            ttk.Button(button_frame, text="Actualizar", command=lambda: self._actualizar_lista_rutas(tree, rutas)).pack(side="left", padx=5)

            # Treeview para mostrar rutas
            columns = ("Nombre", "Paradas", "Acciones")
            tree = ttk.Treeview(main_frame, columns=columns, show="headings", height=15)
            
            # Configurar columnas
            tree.heading("Nombre", text="Nombre de la Ruta")
            tree.heading("Paradas", text="Número de Paradas")
            tree.heading("Acciones", text="Acciones")
            tree.column("Nombre", width=200)
            tree.column("Paradas", width=100)
            tree.column("Acciones", width=150)
            
            # Frame para botones de acción
            button_frame = ttk.Frame(main_frame)
            # Empaquetar normalmente (no usar before=tree porque tree aún no está empaquetado)
            button_frame.pack(fill="x", pady=(0, 5))
            
            # Agregar datos y botones de acción
            for nombre, ruta_data in rutas.items():
                paradas = ruta_data.get('paradas', [])
                item = tree.insert("", "end", values=(
                    nombre,
                    len(paradas),
                    "Editar | Recorrido"
                ))
                
                # Agregar binding para los botones de acción
                tree.tag_bind(item, '<Double-Button-1>', lambda e, n=nombre, r=ruta_data: self._editar_ruta(n, r))
                
            # Agregar menú contextual
            def popup(event):
                item = tree.identify_row(event.y)
                if item:
                    tree.selection_set(item)
                    nombre = tree.item(item)['values'][0]
                    ruta_data = rutas[nombre]
                    menu = tk.Menu(main_frame, tearoff=0)
                    menu.add_command(label="Editar Información", 
                                   command=lambda: self._editar_ruta(nombre, ruta_data))
                    menu.add_command(label="Editar Recorrido", 
                                   command=lambda: self._editar_recorrido(nombre, ruta_data))
                    menu.post(event.x_root, event.y_root)
            
            tree.bind('<Button-3>', popup)  # Clic derecho
            
            # Scrollbar
            scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=tree.yview)
            tree.configure(yscrollcommand=scrollbar.set)
            
            tree.pack(side="left", fill="both", expand=True)
            scrollbar.pack(side="right", fill="y")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar la lista de rutas: {str(e)}")
            
    def _actualizar_lista_rutas(self, tree, rutas):
        """Actualiza la lista de rutas en el Treeview"""
        # Limpiar lista actual
        for item in tree.get_children():
            tree.delete(item)
            
        # Agregar datos actualizados
        for nombre, ruta_data in rutas.items():
            paradas = ruta_data.get('paradas', [])
            tree.insert("", "end", values=(
                nombre,
                len(paradas),
                "Editar | Recorrido"
            ))
            
    def _editar_ruta_desde_tree(self, event, tree, rutas):
        """Maneja el doble clic en una ruta del Treeview"""
        item = tree.selection()[0]
        nombre = tree.item(item)['values'][0]
        ruta_data = rutas[nombre]
        self._editar_ruta(nombre, ruta_data)
        
    def _confirmar_eliminar_ruta(self, nombre_ruta):
        """Confirma y elimina una ruta"""
        if messagebox.askyesno("Confirmar Eliminación", 
                             f"¿Está seguro de que desea eliminar la ruta '{nombre_ruta}'?"):
            try:
                datos = self.data_manager.cargar_datos()
                datos['rutas'].pop(nombre_ruta, None)
                self.data_manager.guardar_datos(datos)
                messagebox.showinfo("Éxito", f"Ruta '{nombre_ruta}' eliminada exitosamente")
                self._listar_rutas()
            except Exception as e:
                messagebox.showerror("Error", f"Error al eliminar la ruta: {str(e)}")

    def _editar_recorrido_on_selection(self, tree, rutas):
        selection = tree.selection()
        if not selection:
            messagebox.showinfo("Editar Recorrido", "Seleccione una ruta de la lista")
            return
        item = selection[0]
        nombre = tree.item(item)['values'][0]
        ruta_data = rutas.get(nombre)
        if not ruta_data:
            messagebox.showerror("Error", "Datos de la ruta no encontrados")
            return
        self._editar_recorrido(nombre, ruta_data)

    def _confirmar_eliminar_ruta_on_selection(self, tree):
        selection = tree.selection()
        if not selection:
            messagebox.showinfo("Eliminar Ruta", "Seleccione una ruta de la lista")
            return
        item = selection[0]
        nombre = tree.item(item)['values'][0]
        self._confirmar_eliminar_ruta(nombre)

    def _editar_ruta_on_selection(self, tree, rutas):
        selection = tree.selection()
        if not selection:
            messagebox.showinfo("Editar Ruta", "Seleccione una ruta de la lista")
            return
        item = selection[0]
        nombre = tree.item(item)['values'][0]
        ruta_data = rutas.get(nombre)
        if not ruta_data:
            messagebox.showerror("Error", "Datos de la ruta no encontrados")
            return
        # Abrir diálogo de edición simple
        dialog = EditarRutaDialog(self.parent, self.data_manager, nombre, ruta_data)
        self.parent.wait_window(dialog.dialog)
        # Refrescar
        datos = self.data_manager.cargar_datos()
        self._actualizar_lista_rutas(tree, datos.get('rutas', {}))

    def _select_route_dialog(self, title="Seleccionar Ruta"):
        """Muestra un cuadro de diálogo simple para seleccionar una ruta y devuelve su nombre o None."""
        top = tk.Toplevel(self.parent)
        top.title(title)
        top.geometry("320x300")
        top.transient(self.parent)
        top.grab_set()

        frame = ttk.Frame(top, padding=10)
        frame.pack(fill="both", expand=True)

        listbox = tk.Listbox(frame, height=12)
        vsb = ttk.Scrollbar(frame, orient="vertical", command=listbox.yview)
        listbox.configure(yscrollcommand=vsb.set)
        listbox.pack(side="left", fill="both", expand=True)
        vsb.pack(side="right", fill="y")

        try:
            datos = self.data_manager.cargar_datos()
            rutas = list(datos.get('rutas', {}).keys())
        except Exception:
            rutas = []

        for r in rutas:
            listbox.insert(tk.END, r)

        result = {'selected': None}

        def on_ok():
            sel = listbox.curselection()
            if sel:
                result['selected'] = listbox.get(sel[0])
            top.destroy()

        def on_cancel():
            top.destroy()

        btns = ttk.Frame(frame)
        btns.pack(fill="x", pady=(8,0))
        ttk.Button(btns, text="OK", command=on_ok).pack(side="left", padx=6)
        ttk.Button(btns, text="Cancelar", command=on_cancel).pack(side="left", padx=6)

        self.parent.wait_window(top)
        return result['selected']

    def _editar_ruta_seleccionar(self):
        nombre = self._select_route_dialog("Editar Ruta")
        if not nombre:
            return
        datos = self.data_manager.cargar_datos()
        ruta_data = datos.get('rutas', {}).get(nombre)
        if not ruta_data:
            messagebox.showerror("Error", "Ruta no encontrada")
            return
        dialog = EditarRutaDialog(self.parent, self.data_manager, nombre, ruta_data)
        self.parent.wait_window(dialog.dialog)

    def _eliminar_ruta_seleccionar(self):
        nombre = self._select_route_dialog("Eliminar Ruta")
        if not nombre:
            return
        self._confirmar_eliminar_ruta(nombre)


class BusDialog:
    def __init__(self, parent, data_manager):
        self.data_manager = data_manager
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Nuevo Bus")
        self.dialog.geometry("300x200")
        self.dialog.resizable(False, False)
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Centrar la ventana
        self.dialog.geometry("+%d+%d" % (parent.winfo_rootx() + 50, parent.winfo_rooty() + 50))
        
        self._create_widgets()
    
    def _create_widgets(self):
        # Frame principal
        main_frame = ttk.Frame(self.dialog, padding="10")
        main_frame.pack(fill="both", expand=True)
        
        # Número de bus
        ttk.Label(main_frame, text="Número de Bus:").grid(row=0, column=0, sticky="w", pady=5)
        self.numero_var = tk.StringVar()
        ttk.Entry(main_frame, textvariable=self.numero_var, width=20).grid(row=0, column=1, pady=5, padx=(10, 0))
        
        # Capacidad
        ttk.Label(main_frame, text="Capacidad:").grid(row=1, column=0, sticky="w", pady=5)
        self.capacidad_var = tk.StringVar(value="40")
        ttk.Entry(main_frame, textvariable=self.capacidad_var, width=20).grid(row=1, column=1, pady=5, padx=(10, 0))
        
        # Selección de ruta
        ttk.Label(main_frame, text="Asignar Ruta:").grid(row=2, column=0, sticky="w", pady=5)
        self.ruta_var = tk.StringVar()
        # obtener rutas actuales
        rutas = []
        try:
            datos = self.data_manager.cargar_datos()
            rutas = list(datos.get('rutas', {}).keys())
        except Exception:
            rutas = []
        self.ruta_combo = ttk.Combobox(main_frame, textvariable=self.ruta_var, values=rutas, state='readonly')
        self.ruta_combo.grid(row=2, column=1, pady=5, padx=(10, 0))

        # Botones para crear/editar ruta desde el diálogo del bus
        ruta_btn_frame = ttk.Frame(main_frame)
        ruta_btn_frame.grid(row=3, column=0, columnspan=2, pady=(5, 0))
        ttk.Button(ruta_btn_frame, text="Nueva Ruta", command=self._crear_nueva_ruta).pack(side="left", padx=5)
        ttk.Button(ruta_btn_frame, text="Editar Ruta", command=self._editar_ruta_seleccionada).pack(side="left", padx=5)
        
        # Botones
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=2, column=0, columnspan=2, pady=20)
        
        ttk.Button(button_frame, text="Crear", command=self._crear_bus).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Cancelar", command=self.dialog.destroy).pack(side="left", padx=5)
    
    def _crear_bus(self):
        try:
            numero = self.numero_var.get().strip()
            capacidad = int(self.capacidad_var.get())
            
            if not numero:
                messagebox.showerror("Error", "El número de bus es obligatorio")
                return
            
            if capacidad <= 0:
                messagebox.showerror("Error", "La capacidad debe ser mayor a 0")
                return
            
            # Crear el bus y asignar ruta si corresponde
            bus = Bus(numero, capacidad)
            ruta_seleccionada = self.ruta_var.get().strip()
            datos = self.data_manager.cargar_datos()
            if 'buses' not in datos:
                datos['buses'] = {}

            # Guardar como diccionario; almacenar el nombre de la ruta si está seleccionada
            bus_dict = bus.to_dict()
            if ruta_seleccionada:
                bus_dict['ruta'] = ruta_seleccionada
                # intentar asignar objeto ruta en memoria (opcional)
                try:
                    from models.ruta import Ruta
                    rutas = datos.get('rutas', {})
                    if ruta_seleccionada in rutas:
                        ruta_obj = Ruta(ruta_seleccionada, rutas[ruta_seleccionada].get('paradas', []))
                        bus.ruta_actual = ruta_obj
                except Exception:
                    pass

            datos['buses'][numero] = bus_dict
            self.data_manager.guardar_datos(datos)
            
            messagebox.showinfo("Éxito", f"Bus {numero} creado exitosamente")
            self.dialog.destroy()
            
        except ValueError as e:
            messagebox.showerror("Error", f"Error en los datos: {str(e)}")
        except Exception as e:
            messagebox.showerror("Error", f"Error al crear el bus: {str(e)}")

    def _crear_nueva_ruta(self):
        # Abrir el diálogo de nueva ruta y refrescar el combobox
        dialog = RutaDialog(self.dialog, self.data_manager)
        self.dialog.wait_window(dialog.dialog)
        try:
            datos = self.data_manager.cargar_datos()
            rutas = list(datos.get('rutas', {}).keys())
            self.ruta_combo['values'] = rutas
            if rutas:
                self.ruta_var.set(rutas[-1])
        except Exception:
            pass

    def _editar_ruta_seleccionada(self):
        nombre = self.ruta_var.get().strip()
        if not nombre:
            messagebox.showinfo("Editar Ruta", "Seleccione una ruta para editar")
            return
        datos = self.data_manager.cargar_datos()
        ruta_data = datos.get('rutas', {}).get(nombre)
        if not ruta_data:
            messagebox.showerror("Error", "Datos de la ruta no encontrados")
            return
        dialog = EditarRutaDialog(self.dialog, self.data_manager, nombre, ruta_data)
        self.dialog.wait_window(dialog.dialog)
        # refrescar combobox
        try:
            datos = self.data_manager.cargar_datos()
            rutas = list(datos.get('rutas', {}).keys())
            self.ruta_combo['values'] = rutas
        except Exception:
            pass


class EditBusDialog:
    def __init__(self, parent, data_manager, numero, bus_data):
        self.data_manager = data_manager
        self.numero = numero
        self.bus_data = bus_data
        self.dialog = tk.Toplevel(parent)
        self.dialog.title(f"Editar Bus: {numero}")
        # Ventana más espaciosa para mejor UX
        self.dialog.geometry("420x300")
        self.dialog.resizable(False, False)
        self.dialog.transient(parent)
        self.dialog.grab_set()

        # Centrar la ventana
        self.dialog.geometry("+%d+%d" % (parent.winfo_rootx() + 60, parent.winfo_rooty() + 60))

        self._create_widgets()

    def _create_widgets(self):
        main_frame = ttk.Frame(self.dialog, padding="12")
        main_frame.pack(fill="both", expand=True)

        # Layout con grid para mejor alineación
        main_frame.columnconfigure(1, weight=1)

        ttk.Label(main_frame, text="Número de Bus:").grid(row=0, column=0, sticky="w", pady=6)
        ttk.Label(main_frame, text=self.numero, font=(None, 10, 'bold')).grid(row=0, column=1, sticky="w", pady=6)

        ttk.Label(main_frame, text="Capacidad:").grid(row=1, column=0, sticky="w", pady=6)
        self.capacidad_var = tk.StringVar(value=str(self.bus_data.get('capacidad', '40')))
        ttk.Entry(main_frame, textvariable=self.capacidad_var, width=12).grid(row=1, column=1, sticky="w", pady=6)

        from utils.constants import BUS_STATES
        ttk.Label(main_frame, text="Estado:").grid(row=2, column=0, sticky="w", pady=6)
        self.estado_var = tk.StringVar(value=self.bus_data.get('estado', 'AVAILABLE'))
        estado_values = list(BUS_STATES.keys())
        estado_combo = ttk.Combobox(main_frame, textvariable=self.estado_var, values=estado_values, state='readonly', width=14)
        estado_combo.grid(row=2, column=1, sticky="w", pady=6)

        # Selección de ruta (editar asignación) con botones de acción
        ttk.Label(main_frame, text="Asignar Ruta:").grid(row=3, column=0, sticky="w", pady=6)
        self.ruta_var = tk.StringVar()
        self.ruta_combo = ttk.Combobox(main_frame, textvariable=self.ruta_var, state='readonly')
        self.ruta_combo.grid(row=3, column=1, sticky="we", pady=6)

        # Botones para nueva/editar ruta y editar recorrido
        ruta_btn_frame = ttk.Frame(main_frame)
        ruta_btn_frame.grid(row=4, column=1, sticky="w", pady=(0,6))
        ttk.Button(ruta_btn_frame, text="Nueva Ruta", command=self._crear_nueva_ruta).pack(side="left", padx=4)
        ttk.Button(ruta_btn_frame, text="Editar Ruta", command=self._editar_ruta_seleccionada).pack(side="left", padx=4)
        ttk.Button(ruta_btn_frame, text="Editar Recorrido", command=self._editar_recorrido_seleccionada).pack(side="left", padx=4)

        # Mostrar pasajeros (solo lectura)
        ttk.Label(main_frame, text="Pasajeros: ").grid(row=5, column=0, sticky="w", pady=6)
        pasajeros = self.bus_data.get('pasajeros', 0)
        ttk.Label(main_frame, text=str(pasajeros)).grid(row=5, column=1, sticky="w", pady=6)

        # Botones de acción
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=6, column=0, columnspan=2, pady=12)
        ttk.Button(button_frame, text="Guardar", command=self._guardar).pack(side="left", padx=6)
        ttk.Button(button_frame, text="Cancelar", command=self.dialog.destroy).pack(side="left", padx=6)

        # Cargar rutas en el combobox
        self._refresh_routes()

    def _guardar(self):
        try:
            capacidad = int(self.capacidad_var.get())
            if capacidad <= 0:
                messagebox.showerror("Error", "La capacidad debe ser mayor a 0")
                return

            estado = self.estado_var.get()

            datos = self.data_manager.cargar_datos()
            buses = datos.get('buses', {})
            if self.numero not in buses:
                messagebox.showerror("Error", "El bus ya no existe")
                self.dialog.destroy()
                return

            buses[self.numero]['capacidad'] = capacidad
            buses[self.numero]['estado'] = estado
            # asignar ruta si se seleccionó
            ruta_sel = self.ruta_var.get().strip() if hasattr(self, 'ruta_var') else ''
            if ruta_sel:
                buses[self.numero]['ruta'] = ruta_sel
            # No tocar pasajeros ni ruta aquí
            datos['buses'] = buses
            self.data_manager.guardar_datos(datos)

            messagebox.showinfo("Éxito", f"Bus '{self.numero}' actualizado correctamente")
            self.dialog.destroy()
        except ValueError:
            messagebox.showerror("Error", "La capacidad debe ser un número entero")
        except Exception as e:
            messagebox.showerror("Error", f"Error al guardar el bus: {str(e)}")

    def _refresh_routes(self):
        try:
            datos = self.data_manager.cargar_datos()
            rutas = list(datos.get('rutas', {}).keys())
        except Exception:
            rutas = []
        self.ruta_combo['values'] = rutas
        # establecer valor actual si existe
        ruta_actual = self.bus_data.get('ruta')
        if ruta_actual and ruta_actual in rutas:
            self.ruta_var.set(ruta_actual)

    def _crear_nueva_ruta(self):
        dialog = RutaDialog(self.dialog, self.data_manager)
        self.dialog.wait_window(dialog.dialog)
        self._refresh_routes()
        # seleccionar la última ruta si existe
        try:
            datos = self.data_manager.cargar_datos()
            rutas = list(datos.get('rutas', {}).keys())
            if rutas:
                self.ruta_var.set(rutas[-1])
        except Exception:
            pass

    def _editar_ruta_seleccionada(self):
        nombre = self.ruta_var.get().strip()
        if not nombre:
            messagebox.showinfo("Editar Ruta", "Seleccione una ruta para editar")
            return
        datos = self.data_manager.cargar_datos()
        ruta_data = datos.get('rutas', {}).get(nombre)
        if not ruta_data:
            messagebox.showerror("Error", "Datos de la ruta no encontrados")
            return
        dialog = EditarRutaDialog(self.dialog, self.data_manager, nombre, ruta_data)
        self.dialog.wait_window(dialog.dialog)
        self._refresh_routes()

    def _editar_recorrido_seleccionada(self):
        nombre = self.ruta_var.get().strip()
        if not nombre:
            messagebox.showinfo("Editar Recorrido", "Seleccione una ruta para editar su recorrido")
            return
        datos = self.data_manager.cargar_datos()
        ruta_data = datos.get('rutas', {}).get(nombre)
        if not ruta_data:
            messagebox.showerror("Error", "Datos de la ruta no encontrados")
            return
        dialog = EditarRecorridoDialog(self.dialog, self.data_manager, nombre, ruta_data)
        self.dialog.wait_window(dialog.dialog)
        self._refresh_routes()


class FleetManagerDialog:
    """Diálogo para gestionar la flota: añadir/editar/eliminar registros de flota."""
    def __init__(self, parent, data_manager):
        self.data_manager = data_manager
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Gestor de Flota")
        self.dialog.geometry("700x450")
        self.dialog.transient(parent)
        self.dialog.grab_set()

        self._create_widgets()
        self._load_flota()

    def _create_widgets(self):
        main_frame = ttk.Frame(self.dialog, padding=10)
        main_frame.pack(fill="both", expand=True)

        # Botones superiores
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(fill="x", pady=(0,8))
        ttk.Button(btn_frame, text="Agregar", command=self._add).pack(side="left", padx=4)
        ttk.Button(btn_frame, text="Editar", command=self._edit).pack(side="left", padx=4)
        ttk.Button(btn_frame, text="Eliminar", command=self._delete).pack(side="left", padx=4)
        ttk.Button(btn_frame, text="Cerrar", command=self.dialog.destroy).pack(side="right", padx=4)

        # Treeview
        columns = ("Nombre", "Cantidad", "Capacidad", "Ruta")
        self.tree = ttk.Treeview(main_frame, columns=columns, show="headings")
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=150)

        vsb = ttk.Scrollbar(main_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=vsb.set)
        self.tree.pack(side="left", fill="both", expand=True)
        vsb.pack(side="right", fill="y")

    def _load_flota(self):
        datos = self.data_manager.cargar_datos()
        flota = datos.get('flota', {})
        # limpiar
        for it in self.tree.get_children():
            self.tree.delete(it)
        for nombre, info in flota.items():
            self.tree.insert("", "end", values=(nombre, info.get('cantidad', 0), info.get('capacidad', 0), info.get('ruta', '')))

    def _add(self):
        dialog = FleetItemDialog(self.dialog, self.data_manager)
        self.dialog.wait_window(dialog.dialog)
        self._load_flota()

    def _edit(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showinfo("Editar", "Seleccione un elemento de la flota")
            return
        item = sel[0]
        nombre = self.tree.item(item)['values'][0]
        datos = self.data_manager.cargar_datos()
        info = datos.get('flota', {}).get(nombre)
        if not info:
            messagebox.showerror("Error", "Elemento no encontrado")
            return
        dialog = FleetItemDialog(self.dialog, self.data_manager, nombre, info)
        self.dialog.wait_window(dialog.dialog)
        self._load_flota()

    def _delete(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showinfo("Eliminar", "Seleccione un elemento de la flota")
            return
        item = sel[0]
        nombre = self.tree.item(item)['values'][0]
        if messagebox.askyesno("Confirmar", f"Eliminar '{nombre}'?"):
            try:
                datos = self.data_manager.cargar_datos()
                datos.get('flota', {}).pop(nombre, None)
                self.data_manager.guardar_datos(datos)
                self._load_flota()
            except Exception as e:
                messagebox.showerror("Error", f"Error al eliminar: {str(e)}")


class FleetItemDialog:
    """Diálogo para crear/editar un item de flota"""
    def __init__(self, parent, data_manager, nombre=None, info=None):
        self.data_manager = data_manager
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Elemento de Flota")
        self.dialog.geometry("420x300")
        self.dialog.transient(parent)
        self.dialog.grab_set()

        self.nombre_original = nombre
        self.info = info or {}
        self._create_widgets()

    def _create_widgets(self):
        main = ttk.Frame(self.dialog, padding=10)
        main.pack(fill="both", expand=True)

        ttk.Label(main, text="Nombre (identificador):").grid(row=0, column=0, sticky="w", pady=6)
        self.nombre_var = tk.StringVar(value=self.nombre_original or "")
        ttk.Entry(main, textvariable=self.nombre_var, width=30).grid(row=0, column=1, pady=6)

        ttk.Label(main, text="Cantidad disponible:").grid(row=1, column=0, sticky="w", pady=6)
        self.cant_var = tk.StringVar(value=str(self.info.get('cantidad', 1)))
        ttk.Entry(main, textvariable=self.cant_var, width=10).grid(row=1, column=1, sticky="w", pady=6)

        ttk.Label(main, text="Capacidad por bus:").grid(row=2, column=0, sticky="w", pady=6)
        self.cap_var = tk.StringVar(value=str(self.info.get('capacidad', 40)))
        ttk.Entry(main, textvariable=self.cap_var, width=10).grid(row=2, column=1, sticky="w", pady=6)

        ttk.Label(main, text="Asignar Ruta:").grid(row=3, column=0, sticky="w", pady=6)
        try:
            datos = self.data_manager.cargar_datos()
            rutas = list(datos.get('rutas', {}).keys())
        except Exception:
            rutas = []
        self.ruta_var = tk.StringVar(value=self.info.get('ruta', ''))
        self.ruta_combo = ttk.Combobox(main, textvariable=self.ruta_var, values=rutas, state='readonly')
        self.ruta_combo.grid(row=3, column=1, sticky="w", pady=6)

        # Botones
        btns = ttk.Frame(main)
        btns.grid(row=4, column=0, columnspan=2, pady=12)
        ttk.Button(btns, text="Guardar", command=self._guardar).pack(side="left", padx=6)
        ttk.Button(btns, text="Cancelar", command=self.dialog.destroy).pack(side="left", padx=6)

    def _guardar(self):
        nombre = self.nombre_var.get().strip()
        if not nombre:
            messagebox.showerror("Error", "El nombre es obligatorio")
            return
        try:
            cantidad = int(self.cant_var.get())
            capacidad = int(self.cap_var.get())
            if cantidad < 0 or capacidad <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Cantidad y capacidad deben ser números válidos")
            return

        ruta = self.ruta_var.get().strip()

        try:
            datos = self.data_manager.cargar_datos()
            if 'flota' not in datos:
                datos['flota'] = {}
            # si renombró el elemento, eliminar el anterior
            if self.nombre_original and self.nombre_original != nombre:
                datos['flota'].pop(self.nombre_original, None)
            datos['flota'][nombre] = {'cantidad': cantidad, 'capacidad': capacidad, 'ruta': ruta}
            self.data_manager.guardar_datos(datos)
            messagebox.showinfo("Éxito", "Elemento de flota guardado")
            self.dialog.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"Error al guardar: {str(e)}")


class EditarRutaDialog:
    def __init__(self, parent, data_manager, nombre_ruta, ruta_data):
        self.data_manager = data_manager
        self.nombre_original = nombre_ruta
        self.ruta_data = ruta_data
        self.dialog = tk.Toplevel(parent)
        self.dialog.title(f"Editar Ruta: {nombre_ruta}")
        # Ventana más amplia para facilitar la edición desde los diálogos de bus
        self.dialog.geometry("700x520")
        self.dialog.resizable(False, False)
        self.dialog.transient(parent)
        self.dialog.grab_set()

        # Centrar
        self.dialog.geometry("+%d+%d" % (parent.winfo_rootx() + 60, parent.winfo_rooty() + 60))

        self._create_widgets()

    def _create_widgets(self):
        main_frame = ttk.Frame(self.dialog, padding="10")
        main_frame.pack(fill="both", expand=True)
        # Permitir que el área de texto crezca dentro del frame
        main_frame.grid_rowconfigure(1, weight=1)
        main_frame.grid_columnconfigure(1, weight=1)

        ttk.Label(main_frame, text="Nombre de la Ruta:").grid(row=0, column=0, sticky="w", pady=5)
        self.nombre_var = tk.StringVar(value=self.nombre_original)
        ttk.Entry(main_frame, textvariable=self.nombre_var, width=30).grid(row=0, column=1, pady=5, padx=(10,0))

        ttk.Label(main_frame, text="Paradas (una por línea):").grid(row=1, column=0, sticky="nw", pady=5)
        text_frame = ttk.Frame(main_frame)
        text_frame.grid(row=1, column=1, pady=5, padx=(10,0), sticky="nsew")

        # Área de texto ampliada para editar múltiples paradas cómodamente
        self.paradas_text = tk.Text(text_frame, width=40, height=18)
        scrollbar = ttk.Scrollbar(text_frame, orient="vertical", command=self.paradas_text.yview)
        self.paradas_text.configure(yscrollcommand=scrollbar.set)
        self.paradas_text.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        paradas = self.ruta_data.get('paradas', [])
        self.paradas_text.insert("1.0", "\n".join(paradas))

        # Botones
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=2, column=0, columnspan=2, pady=12)
        ttk.Button(button_frame, text="Guardar", command=self._guardar).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Eliminar Ruta", command=self._eliminar).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Cancelar", command=self.dialog.destroy).pack(side="left", padx=5)

    def _guardar(self):
        try:
            nuevo_nombre = self.nombre_var.get().strip()
            paradas_text = self.paradas_text.get("1.0", tk.END).strip()
            if not nuevo_nombre:
                messagebox.showerror("Error", "El nombre de la ruta es obligatorio")
                return
            paradas = [p.strip() for p in paradas_text.split('\n') if p.strip()]
            if not paradas:
                messagebox.showerror("Error", "Debe haber al menos una parada")
                return

            from models.ruta import Ruta
            ruta = Ruta(nuevo_nombre, paradas)

            datos = self.data_manager.cargar_datos()
            if nuevo_nombre != self.nombre_original:
                datos.get('rutas', {}).pop(self.nombre_original, None)
            if 'rutas' not in datos:
                datos['rutas'] = {}
            datos['rutas'][nuevo_nombre] = ruta.to_dict()
            self.data_manager.guardar_datos(datos)
            messagebox.showinfo("Éxito", f"Ruta '{nuevo_nombre}' actualizada")
            self.dialog.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"Error al guardar la ruta: {str(e)}")

    def _eliminar(self):
        if messagebox.askyesno("Confirmar Eliminación", f"¿Eliminar la ruta '{self.nombre_original}'?"):
            try:
                datos = self.data_manager.cargar_datos()
                datos.get('rutas', {}).pop(self.nombre_original, None)
                self.data_manager.guardar_datos(datos)
                messagebox.showinfo("Éxito", f"Ruta '{self.nombre_original}' eliminada")
                self.dialog.destroy()
            except Exception as e:
                messagebox.showerror("Error", f"Error al eliminar la ruta: {str(e)}")


class RutaDialog:
    def __init__(self, parent, data_manager):
        self.data_manager = data_manager
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Nueva Ruta")
        self.dialog.geometry("400x300")
        self.dialog.resizable(False, False)
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Centrar la ventana
        self.dialog.geometry("+%d+%d" % (parent.winfo_rootx() + 50, parent.winfo_rooty() + 50))
        
        self._create_widgets()
    
    def _create_widgets(self):
        # Frame principal
        main_frame = ttk.Frame(self.dialog, padding="10")
        main_frame.pack(fill="both", expand=True)
        
        # Nombre de la ruta
        ttk.Label(main_frame, text="Nombre de la Ruta:").grid(row=0, column=0, sticky="w", pady=5)
        self.nombre_var = tk.StringVar()
        ttk.Entry(main_frame, textvariable=self.nombre_var, width=30).grid(row=0, column=1, pady=5, padx=(10, 0))
        
        # Lista de paradas
        ttk.Label(main_frame, text="Paradas (una por línea):").grid(row=1, column=0, sticky="nw", pady=5)
        
        # Text widget para paradas
        text_frame = ttk.Frame(main_frame)
        text_frame.grid(row=1, column=1, pady=5, padx=(10, 0), sticky="nsew")
        
        self.paradas_text = tk.Text(text_frame, width=30, height=8)
        scrollbar = ttk.Scrollbar(text_frame, orient="vertical", command=self.paradas_text.yview)
        self.paradas_text.configure(yscrollcommand=scrollbar.set)
        
        self.paradas_text.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Botones
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=2, column=0, columnspan=2, pady=20)
        
        ttk.Button(button_frame, text="Crear", command=self._crear_ruta).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Cancelar", command=self.dialog.destroy).pack(side="left", padx=5)
    
    def _crear_ruta(self):
        try:
            nombre = self.nombre_var.get().strip()
            paradas_text = self.paradas_text.get("1.0", tk.END).strip()
            
            if not nombre:
                messagebox.showerror("Error", "El nombre de la ruta es obligatorio")
                return
            
            # Procesar paradas
            paradas = []
            if paradas_text:
                paradas = [p.strip() for p in paradas_text.split('\n') if p.strip()]
            
            # Crear la ruta
            from models.ruta import Ruta
            ruta = Ruta(nombre, paradas)
            
            # Guardar en el data manager
            datos = self.data_manager.cargar_datos()
            if 'rutas' not in datos:
                datos['rutas'] = {}
            
            datos['rutas'][nombre] = ruta.to_dict()
            self.data_manager.guardar_datos(datos)
            
            messagebox.showinfo("Éxito", f"Ruta '{nombre}' creada exitosamente con {len(paradas)} paradas")
            self.dialog.destroy()
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al crear la ruta: {str(e)}")


class EditarRecorridoDialog:
    def __init__(self, parent, data_manager, nombre_ruta, ruta_data):
        self.data_manager = data_manager
        self.nombre_ruta = nombre_ruta
        self.ruta_data = ruta_data
        self.dialog = tk.Toplevel(parent)
        self.dialog.title(f"Editar Recorrido: {nombre_ruta}")
        self.dialog.geometry("800x600")
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Centrar la ventana
        self.dialog.geometry("+%d+%d" % (parent.winfo_rootx() + 50, parent.winfo_rooty() + 50))
        
        self._create_widgets()
    
    def _create_widgets(self):
        # Frame principal con 2 columnas
        main_frame = ttk.Frame(self.dialog, padding="10")
        main_frame.pack(fill="both", expand=True)
        
        # Frame izquierdo para el mapa
        map_frame = ttk.LabelFrame(main_frame, text="Mapa de Recorrido")
        map_frame.pack(side="left", fill="both", expand=True, padx=(0, 5))
        
        # Crear vista del mapa
        self.map_view = MapView(map_frame)
        self.map_view.pack(fill="both", expand=True)
        
        # Frame derecho para la lista de paradas y botones
        control_frame = ttk.Frame(main_frame)
        control_frame.pack(side="right", fill="y", padx=(5, 0))
        
        # Lista de paradas
        paradas_frame = ttk.LabelFrame(control_frame, text="Paradas del Recorrido")
        paradas_frame.pack(fill="both", expand=True)
        
        # Listbox con scrollbar
        self.paradas_listbox = tk.Listbox(paradas_frame, width=30, height=15)
        scrollbar = ttk.Scrollbar(paradas_frame, orient="vertical", command=self.paradas_listbox.yview)
        self.paradas_listbox.configure(yscrollcommand=scrollbar.set)
        
        self.paradas_listbox.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Cargar paradas existentes
        paradas = self.ruta_data.get('paradas', [])
        for parada in paradas:
            self.paradas_listbox.insert(tk.END, parada)
        
        # Frame para botones de control de paradas
        buttons_frame = ttk.Frame(control_frame)
        buttons_frame.pack(fill="x", pady=10)
        
        ttk.Button(buttons_frame, text="Agregar Parada", 
                  command=self._agregar_parada).pack(fill="x", pady=2)
        ttk.Button(buttons_frame, text="Eliminar Parada", 
                  command=self._eliminar_parada).pack(fill="x", pady=2)
        ttk.Button(buttons_frame, text="Mover Arriba", 
                  command=lambda: self._mover_parada(-1)).pack(fill="x", pady=2)
        ttk.Button(buttons_frame, text="Mover Abajo", 
                  command=lambda: self._mover_parada(1)).pack(fill="x", pady=2)
        
        # Frame para botones de acción
        action_frame = ttk.Frame(control_frame)
        action_frame.pack(fill="x", pady=10)
        
        ttk.Button(action_frame, text="Guardar Cambios", 
                  command=self._guardar_cambios).pack(side="left", padx=5)
        ttk.Button(action_frame, text="Cancelar", 
                  command=self.dialog.destroy).pack(side="left", padx=5)
    
    def _agregar_parada(self):
        """Agrega una nueva parada al recorrido"""
        nueva_parada = simpledialog.askstring("Nueva Parada", 
                                            "Ingrese el nombre de la parada:",
                                            parent=self.dialog)
        if nueva_parada:
            self.paradas_listbox.insert(tk.END, nueva_parada.strip())
            self._actualizar_mapa()
    
    def _eliminar_parada(self):
        """Elimina la parada seleccionada"""
        seleccion = self.paradas_listbox.curselection()
        if seleccion:
            self.paradas_listbox.delete(seleccion)
            self._actualizar_mapa()
    
    def _mover_parada(self, direccion):
        """Mueve una parada arriba o abajo en la lista"""
        seleccion = self.paradas_listbox.curselection()
        if not seleccion:
            return
        
        pos = seleccion[0]
        if direccion == -1 and pos > 0:  # Mover arriba
            texto = self.paradas_listbox.get(pos)
            self.paradas_listbox.delete(pos)
            self.paradas_listbox.insert(pos-1, texto)
            self.paradas_listbox.selection_set(pos-1)
            self._actualizar_mapa()
        elif direccion == 1 and pos < self.paradas_listbox.size()-1:  # Mover abajo
            texto = self.paradas_listbox.get(pos)
            self.paradas_listbox.delete(pos)
            self.paradas_listbox.insert(pos+1, texto)
            self.paradas_listbox.selection_set(pos+1)
            self._actualizar_mapa()
    
    def _actualizar_mapa(self):
        """Actualiza el mapa con el recorrido actual"""
        # Obtener lista actual de paradas
        paradas = list(self.paradas_listbox.get(0, tk.END))
        
        # Actualizar el mapa (implementar en MapView la funcionalidad necesaria)
        # self.map_view.actualizar_recorrido(paradas)
        pass
    
    def _guardar_cambios(self):
        """Guarda los cambios en el recorrido"""
        try:
            # Obtener lista actual de paradas
            paradas = list(self.paradas_listbox.get(0, tk.END))
            
            if not paradas:
                messagebox.showerror("Error", "Debe haber al menos una parada")
                return
            
            # Actualizar datos
            datos = self.data_manager.cargar_datos()
            datos['rutas'][self.nombre_ruta]['paradas'] = paradas
            self.data_manager.guardar_datos(datos)
            
            messagebox.showinfo("Éxito", f"Recorrido de la ruta '{self.nombre_ruta}' actualizado exitosamente")
            self.dialog.destroy()
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al guardar el recorrido: {str(e)}")


class EditarRecorridoDialog:
    def __init__(self, parent, data_manager, nombre_ruta, ruta_data):
        self.data_manager = data_manager
        self.nombre_ruta = nombre_ruta
        self.ruta_data = ruta_data
        self.dialog = tk.Toplevel(parent)
        self.dialog.title(f"Editar Recorrido: {nombre_ruta}")
        self.dialog.geometry("800x600")
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Centrar la ventana
        self.dialog.geometry("+%d+%d" % (parent.winfo_rootx() + 50, parent.winfo_rooty() + 50))
        
        self._create_widgets()
        
    def _create_widgets(self):
        # Frame principal con 2 columnas
        main_frame = ttk.Frame(self.dialog, padding="10")
        main_frame.pack(fill="both", expand=True)
        
        # Frame izquierdo para el mapa
        map_frame = ttk.LabelFrame(main_frame, text="Mapa de Recorrido")
        map_frame.pack(side="left", fill="both", expand=True, padx=(0, 5))
        
        # Crear vista del mapa
        self.map_view = MapView(map_frame)
        self.map_view.pack(fill="both", expand=True)
        
        # Frame derecho para la lista de paradas y botones
        control_frame = ttk.Frame(main_frame)
        control_frame.pack(side="right", fill="y", padx=(5, 0))
        
        # Lista de paradas
        paradas_frame = ttk.LabelFrame(control_frame, text="Paradas del Recorrido")
        paradas_frame.pack(fill="both", expand=True)
        
        # Listbox con scrollbar
        self.paradas_listbox = tk.Listbox(paradas_frame, width=30, height=15)
        scrollbar = ttk.Scrollbar(paradas_frame, orient="vertical", command=self.paradas_listbox.yview)
        self.paradas_listbox.configure(yscrollcommand=scrollbar.set)
        
        self.paradas_listbox.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Cargar paradas existentes
        paradas = self.ruta_data.get('paradas', [])
        for parada in paradas:
            self.paradas_listbox.insert(tk.END, parada)
        
        # Frame para botones de control de paradas
        buttons_frame = ttk.Frame(control_frame)
        buttons_frame.pack(fill="x", pady=10)
        
        ttk.Button(buttons_frame, text="Agregar Parada", 
                  command=self._agregar_parada).pack(fill="x", pady=2)
        ttk.Button(buttons_frame, text="Eliminar Parada", 
                  command=self._eliminar_parada).pack(fill="x", pady=2)
        ttk.Button(buttons_frame, text="Mover Arriba", 
                  command=lambda: self._mover_parada(-1)).pack(fill="x", pady=2)
        ttk.Button(buttons_frame, text="Mover Abajo", 
                  command=lambda: self._mover_parada(1)).pack(fill="x", pady=2)
        
        # Frame para botones de acción
        action_frame = ttk.Frame(control_frame)
        action_frame.pack(fill="x", pady=10)
        
        ttk.Button(action_frame, text="Guardar Cambios", 
                  command=self._guardar_cambios).pack(side="left", padx=5)
        ttk.Button(action_frame, text="Cancelar", 
                  command=self.dialog.destroy).pack(side="left", padx=5)
    
    def _agregar_parada(self):
        """Agrega una nueva parada al recorrido"""
        nueva_parada = simpledialog.askstring("Nueva Parada", 
                                            "Ingrese el nombre de la parada:",
                                            parent=self.dialog)
        if nueva_parada:
            self.paradas_listbox.insert(tk.END, nueva_parada.strip())
            self._actualizar_mapa()
    
    def _eliminar_parada(self):
        """Elimina la parada seleccionada"""
        seleccion = self.paradas_listbox.curselection()
        if seleccion:
            self.paradas_listbox.delete(seleccion)
            self._actualizar_mapa()
    
    def _mover_parada(self, direccion):
        """Mueve una parada arriba o abajo en la lista"""
        seleccion = self.paradas_listbox.curselection()
        if not seleccion:
            return
        
        pos = seleccion[0]
        if direccion == -1 and pos > 0:  # Mover arriba
            texto = self.paradas_listbox.get(pos)
            self.paradas_listbox.delete(pos)
            self.paradas_listbox.insert(pos-1, texto)
            self.paradas_listbox.selection_set(pos-1)
            self._actualizar_mapa()
        elif direccion == 1 and pos < self.paradas_listbox.size()-1:  # Mover abajo
            texto = self.paradas_listbox.get(pos)
            self.paradas_listbox.delete(pos)
            self.paradas_listbox.insert(pos+1, texto)
            self.paradas_listbox.selection_set(pos+1)
            self._actualizar_mapa()
    
    def _actualizar_mapa(self):
        """Actualiza el mapa con el recorrido actual"""
        # Obtener lista actual de paradas
        paradas = list(self.paradas_listbox.get(0, tk.END))
        
        # Actualizar el mapa (implementar en MapView la funcionalidad necesaria)
        # self.map_view.actualizar_recorrido(paradas)
        pass
    
    def _guardar_cambios(self):
        """Guarda los cambios en el recorrido"""
        try:
            # Obtener lista actual de paradas
            paradas = list(self.paradas_listbox.get(0, tk.END))
            
            if not paradas:
                messagebox.showerror("Error", "Debe haber al menos una parada")
                return
            
            # Actualizar datos
            datos = self.data_manager.cargar_datos()
            datos['rutas'][self.nombre_ruta]['paradas'] = paradas
            self.data_manager.guardar_datos(datos)
            
            messagebox.showinfo("Éxito", f"Recorrido de la ruta '{self.nombre_ruta}' actualizado exitosamente")
            self.dialog.destroy()
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al guardar el recorrido: {str(e)}")