#!/usr/bin/env python3
"""
Script para probar la construcción de ejecutables localmente
"""

import os
import sys
import subprocess
import platform

def test_build():
    """Prueba la construcción del ejecutable para la plataforma actual"""
    
    print("🧪 PRUEBA DE CONSTRUCCIÓN DE EJECUTABLE")
    print("=" * 50)
    
    # Detectar plataforma
    system = platform.system().lower()
    if system == 'darwin':
        platform_name = 'mac'
    elif system == 'windows':
        platform_name = 'windows'
    elif system == 'linux':
        platform_name = 'linux'
    else:
        print(f"❌ Plataforma no soportada: {system}")
        return False
    
    print(f"🖥️ Plataforma detectada: {platform_name}")
    
    # Verificar que existe el script de construcción
    if not os.path.exists('build_executable.py'):
        print("❌ No se encontró build_executable.py")
        return False
    
    # Verificar que existe el archivo principal
    if not os.path.exists('api_server.py'):
        print("❌ No se encontró api_server.py")
        return False
    
    # Verificar dependencias
    print("\n📦 Verificando dependencias...")
    try:
        import flask
        print("✅ Flask disponible")
    except ImportError:
        print("❌ Flask no encontrado")
        return False
    
    try:
        import pyinstaller
        print("✅ PyInstaller disponible")
    except ImportError:
        print("⚠️ PyInstaller no encontrado, instalando...")
        subprocess.run([sys.executable, '-m', 'pip', 'install', 'pyinstaller'], check=True)
    
    # Ejecutar construcción
    print(f"\n🚀 Construyendo ejecutable para {platform_name}...")
    try:
        result = subprocess.run([
            sys.executable, 'build_executable.py', platform_name
        ], check=True, capture_output=True, text=True)
        
        print("✅ Construcción exitosa!")
        print("STDOUT:", result.stdout[-500:] if len(result.stdout) > 500 else result.stdout)
        
    except subprocess.CalledProcessError as e:
        print("❌ Error en la construcción:")
        print("STDOUT:", e.stdout)
        print("STDERR:", e.stderr)
        return False
    
    # Verificar archivos generados
    print("\n📁 Verificando archivos generados...")
    
    # Verificar ejecutable
    if platform_name == 'windows':
        executable_path = f"dist/{platform_name}/GIBD.exe"
    else:
        executable_path = f"dist/{platform_name}/GIBD"
    
    if os.path.exists(executable_path):
        size = os.path.getsize(executable_path)
        print(f"✅ Ejecutable encontrado: {executable_path} ({size // 1024 // 1024} MB)")
    else:
        print(f"❌ Ejecutable no encontrado: {executable_path}")
        return False
    
    # Verificar archivo comprimido
    if platform_name == 'windows':
        archive_path = f"GIBD-{platform_name}.zip"
    else:
        archive_path = f"GIBD-{platform_name}.tar.gz"
    
    if os.path.exists(archive_path):
        size = os.path.getsize(archive_path)
        print(f"✅ Archivo comprimido encontrado: {archive_path} ({size // 1024 // 1024} MB)")
    else:
        print(f"❌ Archivo comprimido no encontrado: {archive_path}")
        return False
    
    print("\n🎉 ¡Prueba completada exitosamente!")
    print(f"📁 Ejecutable: {executable_path}")
    print(f"📦 Archivo: {archive_path}")
    
    # Instrucciones de uso
    print(f"\n📋 Para probar el ejecutable:")
    if platform_name == 'windows':
        print(f"   {executable_path}")
    else:
        print(f"   chmod +x {executable_path}")
        print(f"   ./{executable_path}")
    print("   Luego abrir: http://localhost:5003")
    
    return True

def clean_build():
    """Limpia archivos de construcción anteriores"""
    print("🧹 Limpiando archivos de construcción anteriores...")
    
    import shutil
    
    # Directorios a limpiar
    dirs_to_clean = ['dist', 'build', '__pycache__']
    
    for dir_name in dirs_to_clean:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
            print(f"✅ Eliminado: {dir_name}")
    
    # Archivos a limpiar
    files_to_clean = ['GIBD.spec', 'GIBD-linux.tar.gz', 'GIBD-mac.tar.gz', 'GIBD-windows.zip']
    
    for file_name in files_to_clean:
        if os.path.exists(file_name):
            os.remove(file_name)
            print(f"✅ Eliminado: {file_name}")

def main():
    """Función principal"""
    if len(sys.argv) > 1 and sys.argv[1] == 'clean':
        clean_build()
        return
    
    # Limpiar antes de construir
    clean_build()
    
    # Probar construcción
    success = test_build()
    
    if success:
        print("\n🎉 ¡Prueba exitosa! El sistema de construcción funciona correctamente.")
    else:
        print("\n❌ Prueba fallida. Revisa los errores anteriores.")
        sys.exit(1)

if __name__ == "__main__":
    main()
