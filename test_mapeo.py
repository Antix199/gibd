#!/usr/bin/env python3
"""
Script para probar el mapeo exacto de campos CSV
"""

def normalize_column_name(column_name):
    """Normaliza nombres de columnas CSV para mapeo consistente"""
    if not column_name:
        return ''
    
    # Mapeo EXACTO de nombres de columnas CSV a nombres de campos internos
    column_mapping = {
        # Campos básicos - EXACTOS del CSV
        'id': 'id',
        'contrato': 'contrato', 
        'cliente': 'cliente',
        'fecha_inicio': 'fecha_inicio',
        'fecha_término': 'fecha_termino',  # Con acento como en CSV
        'duración': 'duracion',           # Con acento como en CSV
        'región': 'region',               # Con acento como en CSV
        'ciudad': 'ciudad',
        'estado': 'estado',
        'monto': 'monto',
        
        # Información del cliente - EXACTOS del CSV
        'rut_cliente': 'rut_cliente',
        'tipo_cliente': 'tipo_cliente',
        'persona_contacto': 'persona_contacto',
        'telefono_contacto': 'telefono_contacto',
        'correo_contacto': 'correo_contacto',
        
        # Información técnica - EXACTOS del CSV
        'superficie_terreno': 'superficie_terreno',
        'superficie_construida': 'superficie_construida',
        'tipo_obra_lista': 'tipo_obra_lista',
        
        # Estudios y servicios - EXACTOS del CSV
        'ems': 'ems',
        'estudio_sismico': 'estudio_sismico',
        'estudio_geoeléctrico': 'estudio_geoelectrico',  # Con acento como en CSV
        'topografía': 'topografia',                      # Con acento como en CSV
        'sondaje': 'sondaje',
        'hidráulica/hidrología': 'hidraulica_hidrologia', # Con acentos y / como en CSV
        'descripción': 'descripcion',                     # Con acento como en CSV
        
        # Documentos - EXACTOS del CSV
        'certificado_experiencia': 'certificado_experiencia',
        'orden_compra': 'orden_compra',
        'contrato_existe': 'contrato_doc',
        'factura': 'factura',
        'fecha_factura': 'fecha_factura',
        'numero_factura': 'numero_factura',
        'numero_orden_compra': 'numero_orden_compra',
        'link_documentos': 'link_documentos'
    }
    
    # Normalizar el nombre de la columna
    normalized = column_name.lower().strip()
    return column_mapping.get(normalized, normalized)

def test_mapeo():
    """Prueba el mapeo de todos los campos CSV"""
    
    # Campos exactos del CSV proporcionado
    csv_fields = [
        'Id', 'Contrato', 'Cliente', 'fecha_inicio', 'fecha_término', 'duración', 
        'Región', 'Ciudad', 'Estado', 'Monto', 'RUT_cliente', 'Tipo_cliente', 
        'Persona_contacto', 'Telefono_contacto', 'Correo_contacto', 'Superficie_terreno', 
        'Superficie_construida', 'Tipo_obra_lista', 'EMS', 'Estudio_sismico', 
        'Estudio_Geoeléctrico', 'Topografía', 'Sondaje', 'Hidráulica/Hidrología', 
        'Descripción', 'Certificado_experiencia', 'Orden_compra', 'Contrato_existe', 
        'Factura', 'fecha_factura', 'Numero_factura', 'Numero_orden_compra', 'Link_documentos'
    ]
    
    print("🔍 PRUEBA DE MAPEO DE CAMPOS CSV")
    print("=" * 60)
    print(f"📊 Total campos a mapear: {len(csv_fields)}")
    print()
    
    mapped_count = 0
    unmapped_fields = []
    
    print("📋 MAPEO CAMPO POR CAMPO:")
    for i, field in enumerate(csv_fields, 1):
        mapped_field = normalize_column_name(field)
        
        # Verificar si se mapeó correctamente (no devolvió el mismo campo)
        if mapped_field != field.lower().strip():
            status = "✅"
            mapped_count += 1
        else:
            # Verificar si es un campo que no necesita mapeo (ya está en minúsculas sin acentos)
            if field.lower() in ['id', 'contrato', 'cliente', 'fecha_inicio', 'ciudad', 'estado', 'monto', 'ems', 'sondaje', 'factura', 'fecha_factura']:
                status = "✅"
                mapped_count += 1
            else:
                status = "❌"
                unmapped_fields.append(field)
        
        print(f"  {i:2d}. '{field}' → '{mapped_field}' {status}")
    
    print()
    print("📊 RESUMEN:")
    print(f"✅ Campos mapeados correctamente: {mapped_count}/{len(csv_fields)}")
    print(f"❌ Campos sin mapear: {len(unmapped_fields)}")
    
    if unmapped_fields:
        print(f"🚨 Campos problemáticos: {unmapped_fields}")
        return False
    else:
        print("🎉 ¡Todos los campos están mapeados correctamente!")
        return True

def test_caracteres_especiales():
    """Prueba específica para campos con caracteres especiales"""
    print("\n🔤 PRUEBA DE CARACTERES ESPECIALES:")
    print("-" * 40)
    
    special_fields = {
        'fecha_término': 'fecha_termino',
        'duración': 'duracion', 
        'Región': 'region',
        'Estudio_Geoeléctrico': 'estudio_geoelectrico',
        'Topografía': 'topografia',
        'Hidráulica/Hidrología': 'hidraulica_hidrologia',
        'Descripción': 'descripcion'
    }
    
    all_correct = True
    for original, expected in special_fields.items():
        mapped = normalize_column_name(original)
        if mapped == expected:
            print(f"✅ '{original}' → '{mapped}'")
        else:
            print(f"❌ '{original}' → '{mapped}' (esperado: '{expected}')")
            all_correct = False
    
    return all_correct

if __name__ == "__main__":
    print("🧪 PRUEBA COMPLETA DE MAPEO CSV")
    print("=" * 60)
    
    # Prueba general
    mapeo_ok = test_mapeo()
    
    # Prueba de caracteres especiales
    especiales_ok = test_caracteres_especiales()
    
    print("\n" + "=" * 60)
    if mapeo_ok and especiales_ok:
        print("🎉 ¡TODAS LAS PRUEBAS PASARON!")
        print("✅ El mapeo está listo para importar CSV")
    else:
        print("❌ HAY PROBLEMAS EN EL MAPEO")
        print("🔧 Revisa los campos marcados con ❌")
    print("=" * 60)
