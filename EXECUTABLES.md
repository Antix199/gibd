# 🚀 GIBD - Ejecutables

## 📦 Ejecutables Disponibles

GIBD está disponible como ejecutable standalone para las siguientes plataformas:

### 🐧 Linux
- **Archivo**: `GIBD-linux.tar.gz`
- **Contenido**: `GIBD` (ejecutable)
- **Requisitos**: Ubuntu 20.04+ o distribución equivalente
- **Instalación**:
  ```bash
  tar -xzf GIBD-linux.tar.gz
  chmod +x GIBD
  ./GIBD
  ```

### 🍎 macOS
- **Archivo**: `GIBD-mac.tar.gz`
- **Contenido**: `GIBD` (ejecutable)
- **Requisitos**: macOS 10.14 o superior
- **Instalación**:
  ```bash
  tar -xzf GIBD-mac.tar.gz
  chmod +x GIBD
  ./GIBD
  ```
- **Nota**: Puede requerir permitir la aplicación en Configuración de Seguridad

### 🪟 Windows
- **Archivo**: `GIBD-windows.zip`
- **Contenido**: `GIBD.exe` (ejecutable)
- **Requisitos**: Windows 10 o superior
- **Instalación**:
  1. Descomprimir el archivo ZIP
  2. Ejecutar `GIBD.exe`
  3. Permitir en Windows Defender si es necesario

## 🌐 Acceso a la Aplicación

Una vez ejecutado, GIBD estará disponible en:
- **URL**: `http://localhost:5003`
- **Frontend**: Interfaz web completa
- **API**: `http://localhost:5003/api/`

## 🔧 Construcción Local

### Requisitos
- Python 3.11+
- Dependencias del proyecto

### Construir para tu plataforma
```bash
# Instalar dependencias
pip install -r requirements.txt
pip install pyinstaller pillow

# Construir ejecutable
python build_executable.py

# El ejecutable estará en dist/{platform}/
```

### Construir para plataforma específica
```bash
# Para Linux
python build_executable.py linux

# Para macOS
python build_executable.py mac

# Para Windows
python build_executable.py windows
```

## 📋 Características de los Ejecutables

### ✅ **Incluido en cada ejecutable:**
- Servidor web Flask
- Base de datos SQLite
- Interfaz web completa
- Todos los assets (CSS, JS, imágenes)
- Dependencias de Python

### ✅ **No requiere:**
- Instalación de Python
- Instalación de dependencias
- Configuración adicional
- Conexión a internet (excepto para funcionalidades específicas)

## 🔄 Proceso de Release

### Automático (GitHub Actions)
1. **Push a main** o **crear release** en GitHub
2. **GitHub Actions** construye automáticamente para las 3 plataformas
3. **Artifacts** disponibles para descarga
4. **Release** automático con los 3 ejecutables

### Manual
```bash
# Construir para todas las plataformas (requiere acceso a cada OS)
python build_executable.py linux
python build_executable.py mac
python build_executable.py windows
```

## 📁 Estructura de Archivos

```
releases/
├── GIBD-linux.tar.gz     # Ejecutable para Linux
├── GIBD-mac.tar.gz       # Ejecutable para macOS
└── GIBD-windows.zip      # Ejecutable para Windows
```

## 🛠️ Solución de Problemas

### Linux
- **Error de permisos**: `chmod +x GIBD`
- **Librerías faltantes**: Instalar dependencias del sistema

### macOS
- **"No se puede abrir"**: Ir a Configuración → Seguridad → Permitir
- **Quarantine**: `xattr -d com.apple.quarantine GIBD`

### Windows
- **Windows Defender**: Permitir aplicación
- **SmartScreen**: Hacer clic en "Más información" → "Ejecutar de todas formas"

## 📊 Información Técnica

### Tamaño Aproximado
- **Linux**: ~50-80 MB
- **macOS**: ~50-80 MB  
- **Windows**: ~40-70 MB

### Tecnologías
- **PyInstaller**: Para crear ejecutables
- **Flask**: Servidor web
- **SQLite**: Base de datos
- **Python 3.11**: Runtime incluido

## 🎯 Próximos Pasos

1. **Descargar** el ejecutable para tu plataforma
2. **Ejecutar** el archivo
3. **Abrir** `http://localhost:5003` en tu navegador
4. **¡Usar GIBD!**

---

**¿Necesitas ayuda?** Consulta la documentación completa o reporta issues en GitHub.
