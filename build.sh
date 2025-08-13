#!/bin/bash

echo "🚀 GlaciarIng - Constructor de Ejecutables"
echo "=========================================="

# Verificar que existe el icono
if [ ! -f "assets/images/gibd.png" ]; then
    echo "❌ Error: No se encuentra el icono assets/images/gibd.png"
    exit 1
fi

# Detectar sistema operativo
OS=$(uname -s)
case $OS in
    Darwin)
        echo "🍎 Detectado: macOS"
        PLATFORM="mac"
        ;;
    Linux)
        echo "🐧 Detectado: Linux"
        PLATFORM="linux"
        ;;
    *)
        echo "❌ Sistema operativo no soportado: $OS"
        exit 1
        ;;
esac

# Instalar dependencias si es necesario
if ! command -v pyinstaller &> /dev/null; then
    echo "📦 Instalando PyInstaller..."
    pip install pyinstaller
fi

# Construir ejecutable
echo "🔨 Construyendo ejecutable para $PLATFORM..."
python build_executable.py

# Verificar resultado
if [ -f "dist/$PLATFORM/GlaciarIng" ]; then
    echo "✅ ¡Ejecutable creado exitosamente!"
    echo "📍 Ubicación: dist/$PLATFORM/GlaciarIng"
    
    # Dar permisos de ejecución
    chmod +x "dist/$PLATFORM/GlaciarIng"
    echo "🔐 Permisos de ejecución otorgados"
    
    # Mostrar información del archivo
    ls -lh "dist/$PLATFORM/GlaciarIng"
else
    echo "❌ Error: No se pudo crear el ejecutable"
    exit 1
fi