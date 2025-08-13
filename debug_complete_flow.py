#!/usr/bin/env python3
"""
Script para debuggear el flujo completo de importación CSV
"""

import csv
import json
import requests
from datetime import datetime

def step1_read_csv():
    """Paso 1: Leer el CSV como lo hace el frontend"""
    print("📋 PASO 1: LEYENDO CSV")
    print("-" * 30)
    
    try:
        with open('test_data.csv', 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            csv_data = list(reader)
        
        print(f"✅ CSV leído: {len(csv_data)} registros")
        print(f"📋 Columnas detectadas: {len(reader.fieldnames)}")
        
        # Mostrar las primeras columnas
        print("🏷️ Primeras 10 columnas:")
        for i, col in enumerate(reader.fieldnames[:10], 1):
            print(f"  {i:2d}. '{col}'")
        
        if len(reader.fieldnames) > 10:
            print(f"  ... y {len(reader.fieldnames) - 10} más")
        
        # Mostrar primer registro
        if csv_data:
            print(f"\n📄 Primer registro (primeros 5 campos):")
            first_record = csv_data[0]
            for i, (key, value) in enumerate(list(first_record.items())[:5]):
                print(f"  '{key}': '{value}'")
            print("  ...")
        
        return csv_data, reader.fieldnames
        
    except Exception as e:
        print(f"❌ Error leyendo CSV: {e}")
        return None, None

def step2_simulate_frontend_processing(csv_data):
    """Paso 2: Simular el procesamiento del frontend"""
    print(f"\n🎭 PASO 2: SIMULANDO FRONTEND")
    print("-" * 30)
    
    def getCSVValue(row, possibleKeys):
        """Simula la función getCSVValue del frontend"""
        for key in possibleKeys:
            if key in row and row[key] is not None and str(row[key]).strip() != '':
                value = str(row[key]).strip()
                if value.lower() != 'null':
                    return value
        return ''
    
    def parseBoolean(value):
        """Simula parseBoolean del frontend"""
        if not value:
            return False
        return str(value).lower() in ['true', '1', 'sí', 'si', 'yes', 'verdadero']
    
    def parseNumeric(value):
        """Simula parseNumeric del frontend"""
        if not value or str(value).strip() == '' or str(value).lower() == 'null':
            return None
        try:
            return int(value) if '.' not in str(value) else float(value)
        except:
            return None
    
    proyectos = []
    
    for i, row in enumerate(csv_data):
        try:
            # Mapear exactamente como el frontend
            idValue = getCSVValue(row, ['id', 'ID', 'Id'])
            
            proyecto = {
                'id': int(idValue) if idValue else None,
                'contrato': getCSVValue(row, ['contrato', 'Contrato']),
                'cliente': getCSVValue(row, ['cliente', 'Cliente']),
                'fecha_inicio': getCSVValue(row, ['fecha_inicio']),
                'fecha_termino': getCSVValue(row, ['fecha_termino', 'fecha_término']),
                'duracion': parseNumeric(getCSVValue(row, ['duracion', 'duración'])),
                'region': getCSVValue(row, ['region', 'Region', 'región', 'Región']),
                'ciudad': getCSVValue(row, ['ciudad', 'Ciudad']),
                'estado': getCSVValue(row, ['estado', 'Estado']),
                'monto': parseNumeric(getCSVValue(row, ['monto', 'Monto'])),
                'rut_cliente': getCSVValue(row, ['RUT_cliente', 'rut_cliente']),
                'tipo_cliente': getCSVValue(row, ['Tipo_cliente', 'tipo_cliente']),
                'persona_contacto': getCSVValue(row, ['Persona_contacto', 'persona_contacto']),
                'telefono_contacto': getCSVValue(row, ['Telefono_contacto', 'telefono_contacto']),
                'correo_contacto': getCSVValue(row, ['Correo_contacto', 'correo_contacto']),
                'superficie_terreno': parseNumeric(getCSVValue(row, ['Superficie_terreno', 'superficie_terreno'])),
                'superficie_construida': parseNumeric(getCSVValue(row, ['Superficie_construida', 'superficie_construida'])),
                'tipo_obra_lista': getCSVValue(row, ['Tipo_obra_lista', 'tipo_obra_lista']),
                'ems': parseBoolean(getCSVValue(row, ['EMS', 'ems'])),
                'estudio_sismico': parseBoolean(getCSVValue(row, ['Estudio_sismico', 'estudio_sismico'])),
                'estudio_geoelectrico': parseBoolean(getCSVValue(row, ['Estudio_Geoeléctrico', 'estudio_geoelectrico'])),
                'topografia': parseBoolean(getCSVValue(row, ['Topografía', 'topografia'])),
                'sondaje': parseBoolean(getCSVValue(row, ['Sondaje', 'sondaje'])),
                'hidraulica_hidrologia': parseBoolean(getCSVValue(row, ['Hidráulica/Hidrología', 'hidraulica_hidrologia'])),
                'descripcion': getCSVValue(row, ['Descripción', 'descripcion']),
                'certificado_experiencia': parseBoolean(getCSVValue(row, ['Certificado_experiencia', 'certificado_experiencia'])),
                'orden_compra': parseBoolean(getCSVValue(row, ['Orden_compra', 'orden_compra'])),
                'contrato_doc': parseBoolean(getCSVValue(row, ['Contrato_existe', 'contrato_existe'])),
                'factura': parseBoolean(getCSVValue(row, ['Factura', 'factura'])),
                'fecha_factura': getCSVValue(row, ['fecha_factura']),
                'numero_factura': getCSVValue(row, ['Numero_factura', 'numero_factura']),
                'numero_orden_compra': getCSVValue(row, ['Numero_orden_compra', 'numero_orden_compra']),
                'link_documentos': getCSVValue(row, ['Link_documentos', 'link_documentos'])
            }
            
            # Validar campos críticos
            if proyecto['contrato'] and proyecto['contrato'].strip():
                proyectos.append(proyecto)
                if i == 0:  # Mostrar primer proyecto procesado
                    print(f"✅ Primer proyecto procesado:")
                    print(f"  ID: {proyecto['id']}")
                    print(f"  Contrato: {proyecto['contrato']}")
                    print(f"  Cliente: {proyecto['cliente']}")
                    print(f"  Región: {proyecto['region']}")
                    print(f"  Duración: {proyecto['duracion']}")
                    print(f"  Fecha Factura: {proyecto['fecha_factura']}")
            else:
                print(f"❌ Proyecto {i+1} rechazado: contrato vacío")
                
        except Exception as e:
            print(f"❌ Error procesando proyecto {i+1}: {e}")
    
    print(f"📊 Proyectos válidos procesados: {len(proyectos)}/{len(csv_data)}")
    return proyectos

def step3_send_to_server(proyectos):
    """Paso 3: Enviar al servidor"""
    print(f"\n📤 PASO 3: ENVIANDO AL SERVIDOR")
    print("-" * 30)
    
    payload = {'proyectos': proyectos}
    
    print(f"📦 Enviando {len(proyectos)} proyectos...")
    
    try:
        url = 'http://localhost:5000/api/proyectos/bulk-import'
        headers = {'Content-Type': 'application/json'}
        
        response = requests.post(url, json=payload, headers=headers, timeout=30)
        
        print(f"📡 Respuesta del servidor:")
        print(f"  Status Code: {response.status_code}")
        print(f"  Response: {response.text}")
        
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
        print("❌ No se puede conectar al servidor")
        print("💡 ¿Está ejecutándose en localhost:5000?")
        return False
    except Exception as e:
        print(f"❌ Error en request: {e}")
        return False

def main():
    """Función principal"""
    print("🔍 DEBUG COMPLETO DEL FLUJO DE IMPORTACIÓN CSV")
    print("=" * 60)
    
    # Paso 1: Leer CSV
    csv_data, headers = step1_read_csv()
    if not csv_data:
        return
    
    # Paso 2: Procesar como frontend
    proyectos = step2_simulate_frontend_processing(csv_data)
    if not proyectos:
        print("❌ No se procesaron proyectos válidos")
        return
    
    # Guardar datos procesados para inspección
    with open('debug_proyectos_procesados.json', 'w', encoding='utf-8') as f:
        json.dump(proyectos, f, indent=2, ensure_ascii=False, default=str)
    print(f"💾 Proyectos guardados en: debug_proyectos_procesados.json")
    
    # Paso 3: Enviar al servidor
    success = step3_send_to_server(proyectos)
    
    print("\n" + "=" * 60)
    if success:
        print("🎉 ¡FLUJO COMPLETO EXITOSO!")
    else:
        print("❌ FLUJO FALLÓ")
        print("💡 Revisa los logs del servidor para más detalles")
    print("=" * 60)

if __name__ == "__main__":
    main()
