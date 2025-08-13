#!/usr/bin/env python3
"""
Script especializado para construir ejecutable de Windows con mejor experiencia de usuario
"""

import os
import sys
import subprocess
import shutil

def build_windows_executable():
    """Construye ejecutable optimizado para Windows"""
    
    print("GIBD - Constructor para Windows")
    print("=" * 40)
    
    # Limpiar directorios anteriores
    dist_dir = "dist/windows"
    build_dir = "build/windows"
    
    if os.path.exists(dist_dir):
        shutil.rmtree(dist_dir)
    if os.path.exists(build_dir):
        shutil.rmtree(build_dir)
    
    print("Instalando dependencias...")
    subprocess.run([sys.executable, '-m', 'pip', 'install', 'pyinstaller', 'pillow'], check=True)
    
    # Crear icono ICO
    icon_path = 'assets/images/gibd.png'
    ico_path = 'assets/images/gibd.ico'
    
    try:
        from PIL import Image
        img = Image.open(icon_path)
        sizes = [(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)]
        img.save(ico_path, format='ICO', sizes=sizes)
        print("Icono ICO creado")
        icon_to_use = ico_path
    except Exception as e:
        print(f"Usando icono PNG: {e}")
        icon_to_use = icon_path
    
    # Configurar argumentos de PyInstaller para Windows
    args = [
        'pyinstaller',
        '--onefile',
        '--name=GIBD',
        f'--icon={icon_to_use}',
        f'--distpath={dist_dir}',
        f'--workpath={build_dir}',
        '--noconsole',  # Sin ventana de consola
        '--hidden-import=werkzeug.security',
        '--hidden-import=flask',
        '--hidden-import=sqlite3',
        '--hidden-import=webbrowser',
        '--hidden-import=threading',
        'api_server.py'
    ]
    
    # Agregar archivos y directorios
    data_items = [
        ('assets', 'assets'),
        ('models', 'models'),
        ('controllers', 'controllers'),
        ('db', 'db'),
        ('index.html', '.'),
        ('login.html', '.'),
        ('reader.html', '.'),
        ('modify-database.html', '.')
    ]
    
    for src, dst in data_items:
        if os.path.exists(src):
            args.append(f'--add-data={src};{dst}')
            print(f"Agregando: {src}")
    
    print("Construyendo ejecutable...")
    print("Esto puede tomar varios minutos...")
    
    try:
        result = subprocess.run(args, check=True, capture_output=True, text=True)
        print("Construccion exitosa!")
        
        # Verificar ejecutable
        executable_path = os.path.join(dist_dir, 'GIBD.exe')
        if os.path.exists(executable_path):
            size = os.path.getsize(executable_path)
            print(f"Ejecutable creado: {executable_path} ({size // 1024 // 1024} MB)")
            
            # Crear archivo ZIP
            import zipfile
            archive_name = "GIBD-windows.zip"
            with zipfile.ZipFile(archive_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
                zipf.write(executable_path, 'GIBD.exe')
            
            print(f"Archivo ZIP creado: {archive_name}")
            
            # Crear archivo de instrucciones
            with open('INSTRUCCIONES_WINDOWS.txt', 'w', encoding='utf-8') as f:
                f.write("""GIBD - Instrucciones para Windows

1. EJECUTAR:
   - Doble clic en GIBD.exe
   - El programa se abrirá automáticamente en tu navegador

2. ACCESO:
   - URL: http://localhost:5003
   - Si no se abre automáticamente, copia la URL en tu navegador

3. SEGURIDAD:
   - Si Windows Defender pregunta, hacer clic en "Más información" → "Ejecutar de todas formas"
   - Si aparece SmartScreen, hacer clic en "Ejecutar de todas formas"

4. SOLUCIÓN DE PROBLEMAS:
   - Si no funciona, ejecutar como Administrador (clic derecho → "Ejecutar como administrador")
   - Verificar que el puerto 5003 no esté ocupado
   - Desactivar temporalmente el antivirus si es necesario

5. CERRAR:
   - Cerrar la ventana del navegador
   - Presionar Ctrl+C en la consola (si aparece)
   - O cerrar desde el Administrador de tareas

¡Disfruta usando GIBD!
""")
            
            print("Instrucciones creadas: INSTRUCCIONES_WINDOWS.txt")
            
            return True
        else:
            print("Error: Ejecutable no encontrado")
            return False
            
    except subprocess.CalledProcessError as e:
        print(f"Error en la construccion: {e}")
        if e.stderr:
            print("STDERR:", e.stderr)
        return False

if __name__ == "__main__":
    success = build_windows_executable()
    if success:
        print("\n¡Ejecutable de Windows creado exitosamente!")
        print("Archivos generados:")
        print("- GIBD.exe (en dist/windows/)")
        print("- GIBD-windows.zip")
        print("- INSTRUCCIONES_WINDOWS.txt")
    else:
        print("\nError al crear el ejecutable")
        sys.exit(1)
