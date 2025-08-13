#!/usr/bin/env python3
"""
Script para debuggear la importación CSV
"""

import csv
import json
from datetime import datetime

def normalize_column_name(column_name):
    """Normaliza nombres de columnas CSV para mapeo consistente"""
    if not column_name:
        return ''
    
    # Mapeo de nombres de columnas CSV a nombres de campos internos
    column_mapping = {
        'id': 'id',
        'contrato': 'contrato',
        'cliente': 'cliente',
        'fecha_inicio': 'fecha_inicio',
        'fecha_término': 'fecha_termino',
        'fecha_termino': 'fecha_termino',
        'duración': 'duracion',
        'duracion': 'duracion',
        'región': 'region',
        'region': 'region',
        'ciudad': 'ciudad',
        'estado': 'estado',
        'monto': 'monto',
        'rut_cliente': 'rut_cliente',
        'tipo_cliente': 'tipo_cliente',
        'persona_contacto': 'persona_contacto',
        'telefono_contacto': 'telefono_contacto',
        'correo_contacto': 'correo_contacto',
        'superficie_terreno': 'superficie_terreno',
        'superficie_construida': 'superficie_construida',
        'tipo_obra_lista': 'tipo_obra_lista',
        'ems': 'ems',
        'estudio_sismico': 'estudio_sismico',
        'estudio_geoeléctrico': 'estudio_geoelectrico',
        'estudio_geoelectrico': 'estudio_geoelectrico',
        'topografía': 'topografia',
        'topografia': 'topografia',
        'sondaje': 'sondaje',
        'hidráulica/hidrología': 'hidraulica_hidrologia',
        'hidraulica_hidrologia': 'hidraulica_hidrologia',
        'descripción': 'descripcion',
        'descripcion': 'descripcion',
        'certificado_experiencia': 'certificado_experiencia',
        'orden_compra': 'orden_compra',
        'contrato_existe': 'contrato_doc',
        'contrato_doc': 'contrato_doc',
        'factura': 'factura',
        'fecha_factura': 'fecha_factura',
        'numero_factura': 'numero_factura',
        'numero_orden_compra': 'numero_orden_compra',
        'link_documentos': 'link_documentos'
    }
    
    # Normalizar el nombre de la columna
    normalized = column_name.lower().strip()
    return column_mapping.get(normalized, normalized)

def parse_boolean_value(value):
    """Convierte valores CSV a booleanos"""
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        return value.lower().strip() in ['true', '1', 'sí', 'si', 'yes', 'verdadero']
    return False

def parse_numeric_value(value, default=None):
    """Convierte valores CSV a números"""
    if not value or str(value).strip() == '' or str(value).lower() == 'null':
        return default
    try:
        if '.' in str(value):
            return float(value)
        else:
            return int(value)
    except (ValueError, TypeError):
        return default

def parse_date(date_str):
    """Parsea fechas con múltiples formatos"""
    if not date_str or str(date_str).strip() == '' or str(date_str).lower() == 'null':
        return None
    
    date_formats = [
        '%Y-%m-%d',      # 2014-06-10
        '%d/%m/%Y',      # 10/06/2014
        '%d-%m-%Y',      # 10-06-2014
        '%m/%d/%Y',      # 06/10/2014
        '%Y/%m/%d'       # 2014/06/10
    ]
    
    for fmt in date_formats:
        try:
            return datetime.strptime(str(date_str).strip(), fmt)
        except ValueError:
            continue
    
    print(f"⚠️ No se pudo parsear fecha: {date_str}")
    return None

def debug_csv_import(csv_file_path):
    """Debug completo de importación CSV"""
    print("🔍 DEBUGGING IMPORTACIÓN CSV")
    print("=" * 50)
    
    # Leer CSV
    with open(csv_file_path, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        raw_data = list(reader)
    
    print(f"📁 Archivo: {csv_file_path}")
    print(f"📊 Registros encontrados: {len(raw_data)}")
    print(f"📋 Columnas originales: {len(reader.fieldnames)}")
    
    # Mostrar columnas originales
    print("\n🏷️ COLUMNAS ORIGINALES:")
    for i, col in enumerate(reader.fieldnames, 1):
        normalized = normalize_column_name(col)
        print(f"  {i:2d}. '{col}' → '{normalized}'")
    
    # Normalizar datos
    normalized_data = []
    for item in raw_data:
        normalized_item = {}
        for key, value in item.items():
            normalized_key = normalize_column_name(key)
            normalized_item[normalized_key] = value
        normalized_data.append(normalized_item)
    
    # Procesar primer registro como ejemplo
    if normalized_data:
        print("\n🧪 PROCESANDO PRIMER REGISTRO:")
        item = normalized_data[0]
        
        print(f"  ID: {item.get('id')}")
        print(f"  Contrato: {item.get('contrato')}")
        print(f"  Cliente: {item.get('cliente')}")
        
        # Fechas
        fecha_inicio = parse_date(item.get('fecha_inicio'))
        fecha_termino = parse_date(item.get('fecha_termino'))
        fecha_factura = parse_date(item.get('fecha_factura'))
        
        print(f"  Fecha Inicio: '{item.get('fecha_inicio')}' → {fecha_inicio}")
        print(f"  Fecha Término: '{item.get('fecha_termino')}' → {fecha_termino}")
        print(f"  Fecha Factura: '{item.get('fecha_factura')}' → {fecha_factura}")
        
        # Duración
        duracion = parse_numeric_value(item.get('duracion'))
        print(f"  Duración: '{item.get('duracion')}' → {duracion}")
        
        # Monto
        monto = parse_numeric_value(item.get('monto'), 0)
        print(f"  Monto: '{item.get('monto')}' → {monto}")
        
        # Booleanos
        ems = parse_boolean_value(item.get('ems'))
        factura = parse_boolean_value(item.get('factura'))
        print(f"  EMS: '{item.get('ems')}' → {ems}")
        print(f"  Factura: '{item.get('factura')}' → {factura}")
    
    # Verificar campos críticos
    print("\n✅ VERIFICACIÓN DE CAMPOS CRÍTICOS:")
    critical_fields = ['id', 'contrato', 'cliente', 'region', 'ciudad', 'estado']
    
    for field in critical_fields:
        values = [item.get(field, '') for item in normalized_data]
        empty_count = sum(1 for v in values if not v or str(v).strip() == '')
        print(f"  {field}: {len(values) - empty_count}/{len(values)} con datos")
    
    # Verificar nuevos campos
    print("\n🆕 VERIFICACIÓN DE NUEVOS CAMPOS:")
    new_fields = ['duracion', 'fecha_factura']
    
    for field in new_fields:
        values = [item.get(field, '') for item in normalized_data]
        empty_count = sum(1 for v in values if not v or str(v).strip() == '')
        print(f"  {field}: {len(values) - empty_count}/{len(values)} con datos")
    
    return normalized_data

if __name__ == "__main__":
    try:
        result = debug_csv_import('test_data.csv')
        print(f"\n🎉 DEBUG COMPLETADO - {len(result)} registros procesados")
    except FileNotFoundError:
        print("❌ Archivo test_data.csv no encontrado")
    except Exception as e:
        print(f"❌ Error: {e}")
