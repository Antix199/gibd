#!/usr/bin/env python3
import platform
import PyInstaller.__main__
import os
import sys
import subprocess

def convert_icon_for_mac():
    """Convierte PNG a ICNS para Mac"""
    try:
        # Crear iconset
        os.makedirs('icon.iconset', exist_ok=True)
        
        # Generar diferentes tamaños
        sizes = [16, 32, 128, 256, 512]
        for size in sizes:
            subprocess.run([
                'sips', '-z', str(size), str(size), 
                'assets/images/gibd.png', 
                '--out', f'icon.iconset/icon_{size}x{size}.png'
            ], check=True)
        
        # Crear ICNS
        subprocess.run(['iconutil', '-c', 'icns', 'icon.iconset'], check=True)
        
        # Mover a assets
        os.rename('icon.icns', 'assets/images/gibd.icns')
        
        # Limpiar
        subprocess.run(['rm', '-rf', 'icon.iconset'], check=True)
        
        return 'assets/images/gibd.icns'
    except Exception as e:
        print(f"⚠️  No se pudo convertir icono para Mac: {e}")
        return 'assets/images/gibd.png'

def build_executable():
    system = platform.system().lower()
    
    # Configuración base
    args = [
        'api_server.py',
        '--onefile',
        '--name=GlaciarIng',
        '--add-data=assets:assets',
        '--add-data=*.html:.',
        '--hidden-import=pymongo',
        '--hidden-import=flask',
        '--hidden-import=flask_cors',
        '--hidden-import=controllers.controller',
        '--hidden-import=models.proyecto',
        '--hidden-import=db.conexion',
    ]
    
    # Configuración específica por sistema
    if system == 'darwin':  # Mac
        icon_path = convert_icon_for_mac()
        args.extend([
            '--windowed',
            f'--icon={icon_path}',
            '--distpath=dist/mac',
            '--workpath=build/mac'
        ])
        print("🍎 Construyendo para macOS...")
        
    elif system == 'linux':
        args.extend([
            '--icon=assets/images/gibd.png',
            '--distpath=dist/linux',
            '--workpath=build/linux'
        ])
        print("🐧 Construyendo para Linux...")
        
    else:
        print(f"❌ Sistema {system} no soportado")
        return
    
    print(f"🚀 Iniciando construcción...")
    PyInstaller.__main__.run(args)
    print(f"✅ Ejecutable creado en dist/{system}/GlaciarIng")

if __name__ == "__main__":
    build_executable()