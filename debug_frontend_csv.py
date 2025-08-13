#!/usr/bin/env python3
"""
Script que simula exactamente lo que hace el frontend al procesar CSV
"""

import csv
import json

def simulate_frontend_csv_processing():
    """Simula el procesamiento del frontend"""
    
    print("🎭 SIMULANDO PROCESAMIENTO DEL FRONTEND")
    print("=" * 50)
    
    # Leer CSV como lo haría el frontend
    try:
        with open('test_data.csv', 'r', encoding='utf-8') as file:
            content = file.read()
            print(f"📄 Contenido CSV leído ({len(content)} caracteres)")
            print(f"📋 Primeras 200 caracteres: {content[:200]}...")
            
        # Procesar como CSV
        lines = content.strip().split('\n')
        headers = lines[0].split(',')
        
        print(f"\n📊 Headers detectados ({len(headers)}):")
        for i, header in enumerate(headers, 1):
            print(f"  {i:2d}. '{header}'")
        
        # Procesar cada línea
        csv_data = []
        for i, line in enumerate(lines[1:], 1):
            values = line.split(',')
            
            # Crear objeto como lo haría JavaScript
            record = {}
            for j, value in enumerate(values):
                if j < len(headers):
                    # Limpiar comillas si las hay
                    clean_value = value.strip('"').strip()
                    record[headers[j]] = clean_value
            
            csv_data.append(record)
            
            if i <= 2:  # Mostrar solo los primeros 2 registros
                print(f"\n📋 Registro {i}:")
                for key, value in record.items():
                    print(f"  '{key}': '{value}'")
        
        print(f"\n📊 Total registros procesados: {len(csv_data)}")
        
        # Verificar campos críticos
        print(f"\n🔍 VERIFICACIÓN DE CAMPOS CRÍTICOS:")
        if csv_data:
            first_record = csv_data[0]
            critical_fields = ['Id', 'Contrato', 'Cliente', 'fecha_inicio', 'fecha_término', 'Región', 'Ciudad', 'Estado']
            
            for field in critical_fields:
                value = first_record.get(field, 'MISSING')
                status = "✅" if value != 'MISSING' and value.strip() != '' else "❌"
                print(f"  {field}: '{value}' {status}")
        
        # Guardar datos procesados para inspección
        with open('frontend_processed_data.json', 'w', encoding='utf-8') as f:
            json.dump(csv_data, f, indent=2, ensure_ascii=False)
        
        print(f"\n💾 Datos guardados en: frontend_processed_data.json")
        
        return csv_data
        
    except Exception as e:
        print(f"❌ Error procesando CSV: {e}")
        return None

def check_csv_format():
    """Verifica el formato del CSV"""
    
    print("\n🔍 VERIFICACIÓN DE FORMATO CSV")
    print("-" * 40)
    
    try:
        with open('test_data.csv', 'r', encoding='utf-8') as file:
            # Usar el parser CSV de Python
            reader = csv.DictReader(file)
            headers = reader.fieldnames
            rows = list(reader)
        
        print(f"📋 Headers según csv.DictReader ({len(headers)}):")
        for i, header in enumerate(headers, 1):
            print(f"  {i:2d}. '{header}'")
        
        print(f"\n📊 Registros leídos: {len(rows)}")
        
        if rows:
            print(f"\n📄 Primer registro según csv.DictReader:")
            for key, value in rows[0].items():
                print(f"  '{key}': '{value}'")
        
        return headers, rows
        
    except Exception as e:
        print(f"❌ Error con csv.DictReader: {e}")
        return None, None

def compare_processing_methods():
    """Compara diferentes métodos de procesamiento"""
    
    print("\n⚖️ COMPARACIÓN DE MÉTODOS")
    print("-" * 40)
    
    # Método 1: Simulación frontend
    frontend_data = simulate_frontend_csv_processing()
    
    # Método 2: csv.DictReader
    headers, csv_reader_data = check_csv_format()
    
    if frontend_data and csv_reader_data:
        print(f"\n📊 Comparación:")
        print(f"Frontend simulation: {len(frontend_data)} registros")
        print(f"csv.DictReader: {len(csv_reader_data)} registros")
        
        if len(frontend_data) == len(csv_reader_data):
            print("✅ Mismo número de registros")
        else:
            print("❌ Diferente número de registros")
        
        # Comparar primer registro
        if frontend_data and csv_reader_data:
            frontend_keys = set(frontend_data[0].keys())
            csv_keys = set(csv_reader_data[0].keys())
            
            if frontend_keys == csv_keys:
                print("✅ Mismas columnas")
            else:
                print("❌ Diferentes columnas")
                print(f"Solo en frontend: {frontend_keys - csv_keys}")
                print(f"Solo en csv.DictReader: {csv_keys - frontend_keys}")

if __name__ == "__main__":
    print("🔍 DEBUGGING COMPLETO DEL PROCESAMIENTO CSV")
    print("=" * 60)
    
    try:
        compare_processing_methods()
        
        print("\n" + "=" * 60)
        print("💡 SIGUIENTE PASO:")
        print("1. Revisa frontend_processed_data.json")
        print("2. Ejecuta test_import_direct.py")
        print("3. Revisa los logs del servidor")
        print("=" * 60)
        
    except Exception as e:
        print(f"❌ Error general: {e}")
        import traceback
        traceback.print_exc()
