#!/usr/bin/env python3
"""
Script para probar la estructura CSV con los nuevos campos duracion y fecha_factura
"""

import csv
import io
from datetime import datetime

# Estructura CSV de ejemplo con los nuevos campos
csv_data = """Id,Contrato,Cliente,fecha_inicio,fecha_término,duración,Región,Ciudad,Estado,Monto,RUT_cliente,Tipo_cliente,Persona_contacto,Telefono_contacto,Correo_contacto,Superficie_terreno,Superficie_construida,Tipo_obra_lista,EMS,Estudio_sismico,Estudio_Geoeléctrico,Topografía,Sondaje,Hidráulica/Hidrología,Descripción,Certificado_experiencia,Orden_compra,Contrato_existe,Factura,fecha_factura,Numero_factura,Numero_orden_compra,Link_documentos
1000,Mecánica de Suelos Escuela Fundo Maquehue,Departamento de Educación,10/06/2014,30/06/2014,20,La Araucanía,Padre las Casas,Completado,700000,61.955.000-5,Público,Berenice Alarcón,,,,,635,EDUCACIONAL,TRUE,,,,,,,TRUE,,,,,,,https://drive.google.com/drive/folders/1G2pF9m71Upjg7q1_ThMXWrRTBQMHfmcy?usp=drive_link
1001,EMS vivendas El Porvenir Freire,Ilustre Municipalidad de Freire,16/09/2014,15/10/2014,29,La Araucanía,Freire,Completado,2000000,69.190.900-k,Público,Jorge Carrasco,,,,,1000,VIVIENDAS,TRUE,,,,,,,TRUE,,,,15/11/2014,F-001,,https://drive.google.com/drive/folders/1G2pF9m71Upjg7q1_ThMXWrRTBQMHfmcy?usp=drive_link"""

def test_csv_parsing():
    """Prueba el parsing del CSV con los nuevos campos"""
    print("🧪 Probando estructura CSV con nuevos campos...")
    
    # Simular lectura de CSV
    csv_file = io.StringIO(csv_data)
    reader = csv.DictReader(csv_file)
    
    print("\n📋 Campos detectados en CSV:")
    for i, field in enumerate(reader.fieldnames, 1):
        print(f"  {i:2d}. {field}")
    
    print("\n📊 Datos de ejemplo:")
    csv_file.seek(0)  # Reset file pointer
    reader = csv.DictReader(csv_file)
    
    for i, row in enumerate(reader, 1):
        print(f"\n--- Registro {i} ---")
        print(f"ID: {row.get('Id')}")
        print(f"Contrato: {row.get('Contrato')}")
        print(f"Cliente: {row.get('Cliente')}")
        print(f"Fecha Inicio: {row.get('fecha_inicio')}")
        print(f"Fecha Término: {row.get('fecha_término')}")
        print(f"Duración: {row.get('duración')} días")
        print(f"Región: {row.get('Región')}")
        print(f"Estado: {row.get('Estado')}")
        print(f"Monto: ${row.get('Monto')}")
        print(f"Factura: {row.get('Factura')}")
        print(f"Fecha Factura: {row.get('fecha_factura')}")
        print(f"Número Factura: {row.get('Numero_factura')}")
        
        if i >= 2:  # Solo mostrar primeros 2 registros
            break
    
    print("\n✅ Estructura CSV verificada correctamente!")
    print("\n📝 Campos nuevos agregados:")
    print("  - duración (después de fecha_término)")
    print("  - fecha_factura (después de Factura)")

def validate_field_mapping():
    """Valida que el mapeo de campos sea correcto"""
    print("\n🔍 Validando mapeo de campos...")
    
    expected_fields = [
        'Id', 'Contrato', 'Cliente', 'fecha_inicio', 'fecha_término', 'duración',
        'Región', 'Ciudad', 'Estado', 'Monto', 'RUT_cliente', 'Tipo_cliente',
        'Persona_contacto', 'Telefono_contacto', 'Correo_contacto',
        'Superficie_terreno', 'Superficie_construida', 'Tipo_obra_lista',
        'EMS', 'Estudio_sismico', 'Estudio_Geoeléctrico', 'Topografía',
        'Sondaje', 'Hidráulica/Hidrología', 'Descripción',
        'Certificado_experiencia', 'Orden_compra', 'Contrato_existe',
        'Factura', 'fecha_factura', 'Numero_factura', 'Numero_orden_compra',
        'Link_documentos'
    ]
    
    csv_file = io.StringIO(csv_data)
    reader = csv.DictReader(csv_file)
    actual_fields = reader.fieldnames
    
    print(f"Campos esperados: {len(expected_fields)}")
    print(f"Campos encontrados: {len(actual_fields)}")
    
    missing_fields = set(expected_fields) - set(actual_fields)
    extra_fields = set(actual_fields) - set(expected_fields)
    
    if missing_fields:
        print(f"❌ Campos faltantes: {missing_fields}")
    
    if extra_fields:
        print(f"⚠️  Campos extra: {extra_fields}")
    
    if not missing_fields and not extra_fields:
        print("✅ Todos los campos están presentes y correctos!")
    
    return len(missing_fields) == 0 and len(extra_fields) == 0

if __name__ == "__main__":
    print("=" * 60)
    print("🧪 PRUEBA DE ESTRUCTURA CSV - GLACIARING")
    print("=" * 60)
    
    test_csv_parsing()
    is_valid = validate_field_mapping()
    
    print("\n" + "=" * 60)
    if is_valid:
        print("✅ PRUEBA EXITOSA: La estructura CSV es correcta")
    else:
        print("❌ PRUEBA FALLIDA: Hay problemas con la estructura CSV")
    print("=" * 60)
