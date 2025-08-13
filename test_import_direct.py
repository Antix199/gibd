#!/usr/bin/env python3
"""
Script para probar la importación CSV directamente
"""

import requests
import json
import csv

def test_csv_import():
    """Prueba la importación CSV directamente"""
    
    print("🧪 PRUEBA DIRECTA DE IMPORTACIÓN CSV")
    print("=" * 50)
    
    # Leer CSV
    try:
        with open('test_data.csv', 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            csv_data = list(reader)
        
        print(f"📁 CSV leído: {len(csv_data)} registros")
        print(f"📋 Columnas: {list(csv_data[0].keys()) if csv_data else 'N/A'}")
        
    except FileNotFoundError:
        print("❌ Archivo test_data.csv no encontrado")
        return False
    except Exception as e:
        print(f"❌ Error leyendo CSV: {e}")
        return False
    
    # Preparar datos para envío
    payload = {
        'proyectos': csv_data
    }
    
    print(f"\n📤 Enviando {len(csv_data)} proyectos al servidor...")
    print(f"📄 Primer registro: {csv_data[0] if csv_data else 'N/A'}")
    
    # Enviar al servidor
    try:
        url = 'http://localhost:5000/api/proyectos/bulk-import'
        headers = {'Content-Type': 'application/json'}
        
        response = requests.post(url, json=payload, headers=headers)
        
        print(f"\n📡 Respuesta del servidor:")
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            result = response.json()
            if result.get('success'):
                print("✅ ¡Importación exitosa!")
                return True
            else:
                print(f"❌ Error en importación: {result.get('error')}")
                return False
        else:
            print(f"❌ Error HTTP: {response.status_code}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ No se puede conectar al servidor. ¿Está ejecutándose en localhost:5000?")
        return False
    except Exception as e:
        print(f"❌ Error en request: {e}")
        return False

def test_single_record():
    """Prueba con un solo registro para debugging"""
    
    print("\n🔍 PRUEBA CON UN SOLO REGISTRO")
    print("-" * 30)
    
    # Registro de prueba simple
    single_record = {
        'Id': '9999',
        'Contrato': 'Proyecto de Prueba',
        'Cliente': 'Cliente de Prueba',
        'fecha_inicio': '01/01/2024',
        'fecha_término': '31/01/2024',
        'duración': 'NULL',
        'Región': 'Metropolitana',
        'Ciudad': 'Santiago',
        'Estado': 'Activo',
        'Monto': '1000000',
        'RUT_cliente': '12345678-9',
        'Tipo_cliente': 'Privado',
        'Persona_contacto': 'Juan Pérez',
        'Telefono_contacto': '123456789',
        'Correo_contacto': 'juan@test.com',
        'Superficie_terreno': '100',
        'Superficie_construida': '80',
        'Tipo_obra_lista': 'RESIDENCIAL',
        'EMS': 'TRUE',
        'Estudio_sismico': 'FALSE',
        'Estudio_Geoeléctrico': 'FALSE',
        'Topografía': 'FALSE',
        'Sondaje': 'FALSE',
        'Hidráulica/Hidrología': 'FALSE',
        'Descripción': 'Proyecto de prueba',
        'Certificado_experiencia': 'TRUE',
        'Orden_compra': 'FALSE',
        'Contrato_existe': 'TRUE',
        'Factura': 'FALSE',
        'fecha_factura': 'NULL',
        'Numero_factura': '',
        'Numero_orden_compra': '',
        'Link_documentos': 'https://test.com'
    }
    
    payload = {
        'proyectos': [single_record]
    }
    
    print(f"📤 Enviando registro de prueba...")
    
    try:
        url = 'http://localhost:5000/api/proyectos/bulk-import'
        headers = {'Content-Type': 'application/json'}
        
        response = requests.post(url, json=payload, headers=headers)
        
        print(f"📡 Respuesta:")
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text}")
        
        return response.status_code == 200
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def check_server():
    """Verifica si el servidor está ejecutándose"""
    try:
        response = requests.get('http://localhost:5000/')
        return response.status_code in [200, 404]  # 404 es OK, significa que el servidor responde
    except:
        return False

if __name__ == "__main__":
    print("🔍 DIAGNÓSTICO DE IMPORTACIÓN CSV")
    print("=" * 60)
    
    # Verificar servidor
    if not check_server():
        print("❌ El servidor no está ejecutándose en localhost:5000")
        print("💡 Ejecuta: python api_server.py")
        exit(1)
    
    print("✅ Servidor detectado en localhost:5000")
    
    # Prueba con un registro simple
    print("\n1️⃣ Probando con registro simple...")
    if test_single_record():
        print("✅ Registro simple funcionó")
    else:
        print("❌ Registro simple falló")
    
    # Prueba con CSV completo
    print("\n2️⃣ Probando con CSV completo...")
    if test_csv_import():
        print("✅ CSV completo funcionó")
    else:
        print("❌ CSV completo falló")
    
    print("\n" + "=" * 60)
    print("💡 Revisa los logs del servidor para más detalles")
