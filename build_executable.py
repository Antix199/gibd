#!/usr/bin/env python3
"""
Script para construir ejecutables de GIBD para múltiples plataformas
"""

import os
import sys
import platform
import subprocess
import shutil
from pathlib import Path

def get_platform():
    """Detecta la plataforma actual"""
    system = platform.system().lower()
    if system == 'darwin':
        return 'mac'
    elif system == 'windows':
        return 'windows'
    elif system == 'linux':
        return 'linux'
    else:
        raise ValueError(f"Plataforma no soportada: {system}")

def install_dependencies():
    """Instala las dependencias necesarias"""
    print("📦 Instalando dependencias...")
    
    # Instalar PyInstaller
    subprocess.run([sys.executable, '-m', 'pip', 'install', 'pyinstaller'], check=True)
    
    # Instalar Pillow para iconos (especialmente Windows)
    try:
        subprocess.run([sys.executable, '-m', 'pip', 'install', 'Pillow'], check=True)
        print("✅ Pillow instalado para conversión de iconos")
    except subprocess.CalledProcessError:
        print("⚠️ No se pudo instalar Pillow, usando icono PNG")

def create_icon_for_platform(platform_name):
    """Crea el icono apropiado para cada plataforma"""
    icon_path = 'assets/images/gibd.png'
    
    if platform_name == 'windows':
        try:
            from PIL import Image
            # Convertir PNG a ICO para Windows
            img = Image.open(icon_path)
            ico_path = 'assets/images/gibd.ico'
            sizes = [(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)]
            img.save(ico_path, format='ICO', sizes=sizes)
            print("✅ Icono ICO creado para Windows")
            return ico_path
        except Exception as e:
            print(f"⚠️ No se pudo crear icono ICO: {e}")
            return icon_path
    
    elif platform_name == 'mac':
        try:
            # Crear ICNS para Mac usando sips (solo en Mac)
            if platform.system().lower() == 'darwin':
                icns_path = 'assets/images/gibd.icns'
                subprocess.run([
                    'sips', '-s', 'format', 'icns', 
                    icon_path, '--out', icns_path
                ], check=True)
                print("✅ Icono ICNS creado para Mac")
                return icns_path
        except Exception as e:
            print(f"⚠️ No se pudo crear icono ICNS: {e}")
    
    # Usar PNG por defecto
    return icon_path

def build_executable(target_platform=None):
    """Construye el ejecutable para la plataforma especificada"""
    
    # Determinar plataforma objetivo
    if target_platform:
        platform_name = target_platform.lower()
    else:
        platform_name = get_platform()
    
    print(f"🚀 Construyendo GIBD para {platform_name}...")
    
    # Limpiar directorios anteriores
    dist_dir = f"dist/{platform_name}"
    build_dir = f"build/{platform_name}"
    
    if os.path.exists(dist_dir):
        shutil.rmtree(dist_dir)
    if os.path.exists(build_dir):
        shutil.rmtree(build_dir)
    
    # Crear icono apropiado
    icon_path = create_icon_for_platform(platform_name)
    
    # Configurar argumentos de PyInstaller
    args = [
        'pyinstaller',
        '--onefile',
        '--name=GIBD',
        f'--icon={icon_path}',
        f'--distpath={dist_dir}',
        f'--workpath={build_dir}',
        '--add-data=assets:assets',
        '--add-data=templates:templates',
        '--add-data=static:static',
        '--hidden-import=werkzeug.security',
        '--hidden-import=flask',
        '--hidden-import=sqlite3',
        'api_server.py'
    ]
    
    # Configuración específica por plataforma
    if platform_name == 'windows':
        args.append('--console')  # Mantener consola para logs
    elif platform_name == 'mac':
        args.append('--windowed')  # Sin consola en Mac
    
    print(f"📋 Ejecutando: {' '.join(args)}")
    
    # Ejecutar PyInstaller
    try:
        result = subprocess.run(args, check=True, capture_output=True, text=True)
        print("✅ Construcción exitosa!")
        
        # Verificar que el ejecutable se creó
        if platform_name == 'windows':
            executable_path = os.path.join(dist_dir, 'GIBD.exe')
        else:
            executable_path = os.path.join(dist_dir, 'GIBD')
        
        if os.path.exists(executable_path):
            size = os.path.getsize(executable_path)
            print(f"📁 Ejecutable creado: {executable_path} ({size // 1024 // 1024} MB)")
            
            # Dar permisos de ejecución en Unix
            if platform_name in ['linux', 'mac']:
                os.chmod(executable_path, 0o755)
                print("✅ Permisos de ejecución establecidos")
            
            return executable_path
        else:
            print("❌ El ejecutable no se encontró después de la construcción")
            return None
            
    except subprocess.CalledProcessError as e:
        print(f"❌ Error en la construcción: {e}")
        if e.stdout:
            print("STDOUT:", e.stdout)
        if e.stderr:
            print("STDERR:", e.stderr)
        return None

def create_archive(platform_name, executable_path):
    """Crea un archivo comprimido del ejecutable"""
    if not executable_path or not os.path.exists(executable_path):
        print("❌ No se puede crear archivo: ejecutable no encontrado")
        return None
    
    dist_dir = os.path.dirname(executable_path)
    executable_name = os.path.basename(executable_path)
    
    if platform_name == 'windows':
        # ZIP para Windows
        archive_name = f"GIBD-{platform_name}.zip"
        import zipfile
        with zipfile.ZipFile(archive_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
            zipf.write(executable_path, executable_name)
        print(f"📦 Archivo ZIP creado: {archive_name}")
        return archive_name
    
    else:
        # TAR.GZ para Linux/Mac
        archive_name = f"GIBD-{platform_name}.tar.gz"
        import tarfile
        with tarfile.open(archive_name, 'w:gz') as tar:
            tar.add(executable_path, arcname=executable_name)
        print(f"📦 Archivo TAR.GZ creado: {archive_name}")
        return archive_name

def main():
    """Función principal"""
    print("🔨 GIBD - Constructor de Ejecutables")
    print("=" * 50)
    
    # Obtener plataforma objetivo de argumentos
    target_platform = None
    if len(sys.argv) > 1:
        target_platform = sys.argv[1]
        print(f"🎯 Plataforma objetivo: {target_platform}")
    else:
        target_platform = get_platform()
        print(f"🖥️ Plataforma detectada: {target_platform}")
    
    try:
        # Instalar dependencias
        install_dependencies()
        
        # Construir ejecutable
        executable_path = build_executable(target_platform)
        
        if executable_path:
            # Crear archivo comprimido
            archive_path = create_archive(target_platform, executable_path)
            
            if archive_path:
                print("\n🎉 ¡Construcción completada exitosamente!")
                print(f"📁 Ejecutable: {executable_path}")
                print(f"📦 Archivo: {archive_path}")
            else:
                print("\n⚠️ Ejecutable creado pero no se pudo archivar")
        else:
            print("\n❌ Falló la construcción del ejecutable")
            sys.exit(1)
            
    except Exception as e:
        print(f"\n❌ Error general: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
