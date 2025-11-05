# BuScanGo - Sistema de Gestión de Buses

Sistema de gestión de buses desarrollado en Python con interfaz gráfica usando Tkinter y mapas interactivos con Folium.

## 🚌 Características

- **Gestión de Buses**: Crear, listar y gestionar buses del sistema
- **Gestión de Rutas**: Crear y administrar rutas con paradas
- **Mapa Interactivo**: Visualización de rutas en mapa de Coquimbo
- **Interfaz Gráfica**: Aplicación de escritorio fácil de usar
- **Persistencia de Datos**: Almacenamiento en archivos JSON

## 🛠️ Tecnologías Utilizadas

- **Python 3.13+**
- **Tkinter** - Interfaz gráfica
- **Folium** - Mapas interactivos
- **TkinterWeb** - Visualización de mapas en Tkinter
- **SQLite** - Base de datos (opcional)
- **ReportLab** - Generación de reportes

## 📋 Requisitos

- Python 3.13 o superior
- Conexión a internet (para cargar mapas)

## 🚀 Instalación

### 1. Clonar el repositorio
```bash
git clone https://github.com/pedrocontreras2007/proyecto-buscango.git
cd buscango
```

### 2. Crear entorno virtual
```bash
python -m venv venv
```

### 3. Activar entorno virtual

**Windows (PowerShell):**
```powershell
.\venv\Scripts\Activate.ps1
```

**Windows (Git Bash):**
```bash
source venv/Scripts/activate
```

**Linux/Mac:**
```bash
source venv/bin/activate
```

### 4. Instalar dependencias
```bash
pip install -r requirements.txt
```

## 🎯 Uso

### Ejecutar la aplicación

**Windows (PowerShell):**
```powershell
cd "ruta\al\proyecto"
.\venv\Scripts\Activate.ps1
python main.py
```

**Windows (Git Bash):**
```bash
cd "/ruta/al/proyecto"
source venv/Scripts/activate
python main.py
```

**Linux/Mac:**
```bash
cd /ruta/al/proyecto
source venv/bin/activate
python main.py
```

### Funcionalidades

1. **Crear Bus**: Archivo → Nuevo Bus
2. **Crear Ruta**: Archivo → Nueva Ruta
3. **Listar Buses**: Gestión → Listar Buses
4. **Listar Rutas**: Gestión → Listar Rutas
5. **Ver Mapa**: Pestaña "Mapa"

## 📁 Estructura del Proyecto

```
buscango/
├── main.py                 # Punto de entrada de la aplicación
├── requirements.txt        # Dependencias del proyecto
├── data.json              # Datos de la aplicación
├── config.py              # Configuración general
├── gui/                   # Interfaz gráfica
│   ├── main_window.py     # Ventana principal
│   ├── map_view.py        # Vista del mapa
│   └── styles.py          # Estilos de la interfaz
├── models/                # Modelos de datos
│   ├── bus.py            # Modelo de bus
│   └── ruta.py           # Modelo de ruta
├── services/              # Servicios de la aplicación
│   ├── data_manager.py   # Gestión de datos
│   ├── simulador.py      # Simulador de buses
│   └── notifier.py       # Notificaciones
├── database/              # Base de datos
│   └── db_manager.py     # Gestión de base de datos
├── utils/                 # Utilidades
│   ├── constants.py      # Constantes
│   └── logger.py         # Sistema de logging
├── auth/                  # Autenticación
│   └── login.py          # Sistema de login
├── reports/               # Reportes
│   └── report_generator.py
└── tests/                 # Pruebas
    └── test_bus.py
```

## 🔧 Configuración

### Variables de Entorno
Crea un archivo `.env` en la raíz del proyecto:
```
# Configuración de la base de datos
DB_NAME=buscango.db

# Configuración del servidor
HOST=localhost
PORT=8000
```

## 🧪 Pruebas

```bash
python -m pytest tests/
```

## 📝 Desarrollo

### Agregar nuevas funcionalidades
1. Crea el código en el módulo correspondiente
2. Actualiza la interfaz gráfica si es necesario
3. Agrega pruebas en `tests/`
4. Actualiza la documentación

### Estructura de commits
- `feat:` Nueva funcionalidad
- `fix:` Corrección de errores
- `docs:` Documentación
- `style:` Formato de código
- `refactor:` Refactorización
- `test:` Pruebas

## 🤝 Contribuciones

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 👥 Autores

- **Pedro Contreras**- *Desarrollo inicial* - [pedrocontreras2007](https://github.com/pedrocontreras2007)

## 🙏 Agradecimientos

- [Folium](https://python-visualization.github.io/folium/) - Mapas interactivos
- [TkinterWeb](https://github.com/Andereoo/TkinterWeb) - Visualización web en Tkinter
- [ReportLab](https://www.reportlab.com/) - Generación de reportes PDF

## Este Cambio se realizo el 04-11-2025 a las 21:14Hrs