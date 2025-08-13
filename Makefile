.PHONY: build-mac build-linux build clean install prepare-mac-icon

# Construir para Mac
build-mac:
    @echo "🍎 Preparando construcción para macOS..."
    python build_executable.py
    @echo "✅ Ejecutable para Mac: dist/mac/GlaciarIng"

# Construir para Linux  
build-linux:
    @echo "🐧 Preparando construcción para Linux..."
    python build_executable.py
    @echo "✅ Ejecutable para Linux: dist/linux/GlaciarIng"

# Construir para el sistema actual
build:
    python build_executable.py

# Preparar icono para Mac manualmente
prepare-mac-icon:
    @echo "🎨 Convirtiendo icono para macOS..."
    mkdir -p icon.iconset
    sips -z 16 16 assets/images/gibd.png --out icon.iconset/icon_16x16.png
    sips -z 32 32 assets/images/gibd.png --out icon.iconset/icon_32x32.png
    sips -z 128 128 assets/images/gibd.png --out icon.iconset/icon_128x128.png
    sips -z 256 256 assets/images/gibd.png --out icon.iconset/icon_256x256.png
    sips -z 512 512 assets/images/gibd.png --out icon.iconset/icon_512x512.png
    iconutil -c icns icon.iconset
    mv icon.icns assets/images/gibd.icns
    rm -rf icon.iconset
    @echo "✅ Icono ICNS creado: assets/images/gibd.icns"

# Limpiar archivos de construcción
clean:
    rm -rf build/ dist/ specs/ *.spec
    rm -f assets/images/gibd.icns

# Instalar dependencias
install:
    pip install -r requirements.txt pyinstaller

# Verificar que el icono existe
check-icon:
    @if [ -f "assets/images/gibd.png" ]; then \
        echo "✅ Icono encontrado: assets/images/gibd.png"; \
    else \
        echo "❌ Icono no encontrado: assets/images/gibd.png"; \
    fi