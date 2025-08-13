#!/usr/bin/env python3
"""
Script para probar la importación CSV con los nuevos campos
"""

import json
import requests
from datetime import datetime

# Datos de prueba CSV simulando la estructura real
test_csv_data = [
    {
        "Id": "1000",
        "Contrato": "Mecánica de Suelos Escuela Fundo Maquehue",
        "Cliente": "Departamento de Educación",
        "fecha_inicio": "10/06/2014",
        "fecha_término": "30/06/2014",
        "duración": "20",
        "Región": "La Araucanía",
        "Ciudad": "Padre las Casas",
        "Estado": "Completado",
        "Monto": "700000",
        "RUT_cliente": "61.955.000-5",
        "Tipo_cliente": "Público",
        "Persona_contacto": "Berenice Alarcón",
        "Telefono_contacto": "",
        "Correo_contacto": "",
        "Superficie_terreno": "",
        "Superficie_construida": "635",
        "Tipo_obra_lista": "EDUCACIONAL",
        "EMS": "TRUE",
        "Estudio_sismico": "",
        "Estudio_Geoeléctrico": "",
        "Topografía": "",
        "Sondaje": "",
        "Hidráulica/Hidrología": "",
        "Descripción": "",
        "Certificado_experiencia": "TRUE",
        "Orden_compra": "",
        "Contrato_existe": "",
        "Factura": "",
        "fecha_factura": "",
        "Numero_factura": "",
        "Numero_orden_compra": "",
        "Link_documentos": "https://drive.google.com/drive/folders/1G2pF9m71Upjg7q1_ThMXWrRTBQMHfmcy?usp=drive_link"
    },
    {
        "Id": "1001",
        "Contrato": "EMS vivendas El Porvenir Freire",
        "Cliente": "Ilustre Municipalidad de Freire",
        "fecha_inicio": "16/09/2014",
        "fecha_término": "15/10/2014",
        "duración": "29",
        "Región": "La Araucanía",
        "Ciudad": "Freire",
        "Estado": "Completado",
        "Monto": "2000000",
        "RUT_cliente": "69.190.900-k",
        "Tipo_cliente": "Público",
        "Persona_contacto": "Jorge Carrasco",
        "Telefono_contacto": "",
        "Correo_contacto": "",
        "Superficie_terreno": "",
        "Superficie_construida": "1000",
        "Tipo_obra_lista": "VIVIENDAS",
        "EMS": "TRUE",
        "Estudio_sismico": "",
        "Estudio_Geoeléctrico": "",
        "Topografía": "",
        "Sondaje": "",
        "Hidráulica/Hidrología": "",
        "Descripción": "",
        "Certificado_experiencia": "TRUE",
        "Orden_compra": "",
        "Contrato_existe": "",
        "Factura": "TRUE",
        "fecha_factura": "15/11/2014",
        "Numero_factura": "F-001",
        "Numero_orden_compra": "",
        "Link_documentos": "https://drive.google.com/drive/folders/1G2pF9m71Upjg7q1_ThMXWrRTBQMHfmcy?usp=drive_link"
    }
]

def test_column_mapping():
    """Prueba el mapeo de columnas"""
    print("🧪 Probando mapeo de columnas CSV...")
    
    # Simular la función normalize_column_name
    def normalize_column_name(column_name):
        if not column_name:
            return ''
        
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
        
        normalized = column_name.lower().strip()
        return column_mapping.get(normalized, normalized)
    
    # Normalizar datos de prueba
    normalized_data = []
    for item in test_csv_data:
        normalized_item = {}
        for key, value in item.items():
            normalized_key = normalize_column_name(key)
            normalized_item[normalized_key] = value
        normalized_data.append(normalized_item)
    
    print("\n📋 Datos originales vs normalizados:")
    for i, (original, normalized) in enumerate(zip(test_csv_data, normalized_data)):
        print(f"\n--- Registro {i+1} ---")
        print("Original keys:", list(original.keys())[:5], "...")
        print("Normalized keys:", list(normalized.keys())[:5], "...")
        print(f"ID: {original.get('Id')} → {normalized.get('id')}")
        print(f"Duración: {original.get('duración')} → {normalized.get('duracion')}")
        print(f"Fecha Factura: {original.get('fecha_factura')} → {normalized.get('fecha_factura')}")
    
    return normalized_data

def test_data_parsing():
    """Prueba el parsing de datos"""
    print("\n🔧 Probando parsing de datos...")
    
    def parse_boolean_value(value):
        if isinstance(value, bool):
            return value
        if isinstance(value, str):
            return value.lower().strip() in ['true', '1', 'sí', 'si', 'yes', 'verdadero']
        return False
    
    def parse_numeric_value(value, default=None):
        if not value or str(value).strip() == '' or str(value).lower() == 'null':
            return default
        try:
            if '.' in str(value):
                return float(value)
            else:
                return int(value)
        except (ValueError, TypeError):
            return default
    
    # Probar parsing
    test_values = {
        'boolean_true': 'TRUE',
        'boolean_false': '',
        'number_int': '20',
        'number_float': '635.5',
        'number_empty': '',
        'number_null': 'NULL'
    }
    
    print("\n📊 Resultados de parsing:")
    for key, value in test_values.items():
        if 'boolean' in key:
            result = parse_boolean_value(value)
            print(f"{key}: '{value}' → {result} ({type(result).__name__})")
        elif 'number' in key:
            result = parse_numeric_value(value)
            print(f"{key}: '{value}' → {result} ({type(result).__name__})")

if __name__ == "__main__":
    print("=" * 60)
    print("🧪 PRUEBA DE IMPORTACIÓN CSV - GLACIARING")
    print("=" * 60)
    
    normalized_data = test_column_mapping()
    test_data_parsing()
    
    print("\n" + "=" * 60)
    print("✅ PRUEBA COMPLETADA")
    print("📝 Los datos están listos para importación")
    print("=" * 60)
    
    # Guardar datos normalizados para prueba
    with open('test_normalized_data.json', 'w', encoding='utf-8') as f:
        json.dump(normalized_data, f, indent=2, ensure_ascii=False)
    
    print("💾 Datos normalizados guardados en: test_normalized_data.json")
