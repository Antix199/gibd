# GlaciarIng - Full Stack Application

Una aplicación completa de gestión de proyectos con frontend moderno y backend Python conectado a MongoDB Atlas.

## 🚀 Características

### ✨ **Funcionalidades Principales**
- **Visualización de datos** con filtros avanzados
- **Gestión completa de registros** (CRUD)
- **API REST** con Flask y MongoDB Atlas
- **Importación de archivos** CSV/Excel
- **Exportación de datos** a CSV
- **Interfaz responsive** y moderna
- **Base de datos en la nube** (MongoDB Atlas)

### 🎨 **Diseño**
- **Colores suaves** y profesionales
- **Badges de estado** coloridos para fácil identificación
- **Animaciones suaves** y transiciones
- **Diseño modular** y reutilizable

## 📁 Estructura del Proyecto

```
glaciaring/
├── index.html                 # Pantalla principal (Data Filtering)
├── modify-database.html       # Pantalla de modificación
├── assets/
│   ├── css/
│   │   ├── styles.css         # Estilos base y variables CSS
│   │   └── components.css     # Componentes UI reutilizables
│   └── js/
│       ├── data.js           # Gestión de datos y localStorage
│       ├── components.js     # Componentes UI JavaScript
│       ├── main.js          # Lógica de pantalla principal
│       └── modify-database.js # Lógica de pantalla de modificación
└── PROTOTYPE_README.md
```

## 🛠️ Tecnologías Utilizadas

### **Frontend:**
- **HTML5** - Estructura semántica
- **CSS3** - Estilos modernos con variables CSS
- **JavaScript ES6+** - Funcionalidad interactiva
- **Fetch API** - Comunicación con backend
- **Responsive Design** - Compatible con móviles

### **Backend:**
- **Python 3.12** - Lenguaje de programación
- **Flask** - Framework web
- **PyMongo** - Driver de MongoDB
- **Flask-CORS** - Manejo de CORS

### **Base de Datos:**
- **MongoDB Atlas** - Base de datos en la nube
- **Índices optimizados** - Para búsquedas rápidas
- **Agregaciones** - Para estadísticas

## 🚀 Cómo Ejecutar

### **Requisitos Previos:**
```bash
# 1. Instalar dependencias
.venv\Scripts\python.exe -m pip install -r requirements.txt

# 2. Verificar conexión a MongoDB Atlas
.venv\Scripts\python.exe test_connection.py
```

### **Opción 1: Script de Inicio (Recomendado)**
```bash
# Windows
start_server.bat

# O manualmente
.venv\Scripts\python.exe api_server.py
```

### **Opción 2: Desarrollo**
```bash
# Ejecutar servidor de desarrollo
.venv\Scripts\python.exe api_server.py

# Abrir navegador en: http://localhost:5000
```

## 📱 Pantallas

### 🏠 **Pantalla Principal** (`index.html`)
- **Header** con búsqueda y navegación
- **Filtros** por nombre y estado
- **Tabla de datos** con información de registros
- **Exportación** a CSV
- **Búsqueda en tiempo real**

### ⚙️ **Pantalla de Modificación** (`modify-database.html`)
- **Agregar nuevos registros** con validación
- **Cargar datos desde archivos** (simulado)
- **Gestionar registros existentes**
- **Edición inline** con modal
- **Eliminación múltiple** con confirmación

## 🎯 Funcionalidades Implementadas

### ✅ **Gestión de Datos**
- ✅ Crear registros
- ✅ Leer/Visualizar registros
- ✅ Actualizar registros
- ✅ Eliminar registros
- ✅ Filtrado y búsqueda
- ✅ Importación simulada
- ✅ Exportación real a CSV

### ✅ **Interfaz de Usuario**
- ✅ Diseño responsive
- ✅ Navegación entre pantallas
- ✅ Validación de formularios
- ✅ Notificaciones de usuario
- ✅ Loading states
- ✅ Modales para edición
- ✅ Selección múltiple

### ✅ **Experiencia de Usuario**
- ✅ Animaciones suaves
- ✅ Feedback visual
- ✅ Estados de carga
- ✅ Confirmaciones de acciones
- ✅ Manejo de errores
- ✅ Persistencia de datos

## 🔧 Buenas Prácticas Implementadas

### **Arquitectura**
- ✅ **Separación de responsabilidades** (HTML/CSS/JS)
- ✅ **Modularización** del código
- ✅ **Reutilización** de componentes
- ✅ **Nomenclatura consistente**

### **Código**
- ✅ **ES6+ Features** (clases, arrow functions, async/await)
- ✅ **Error handling** robusto
- ✅ **Validación** de datos
- ✅ **Comentarios** descriptivos

### **UI/UX**
- ✅ **Responsive design**
- ✅ **Accesibilidad** básica
- ✅ **Loading states**
- ✅ **Feedback visual**

## 🚀 Próximos Pasos

Para convertir este prototipo en una aplicación completa:

1. **Backend Integration** - Conectar con API real
2. **Autenticación** - Sistema de login/logout
3. **Base de datos** - Reemplazar localStorage
4. **Testing** - Unit tests y E2E tests
5. **Deployment** - Configurar para producción

---