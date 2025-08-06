#!/usr/bin/env python3
"""
Script de prueba para verificar que el campo link_documentos funciona correctamente
"""

import sys
import os
from datetime import datetime

# Agregar el directorio raíz al path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from db.conexion import get_collection
from models.proyecto import Proyecto

def test_link_documentos():
    """Prueba el campo link_documentos"""
    
    try:
        # Obtener la colección
        collection = get_collection('proyectos')
        
        print("🧪 Creando proyecto de prueba con link_documentos...")
        
        # Crear un proyecto de prueba simple
        proyecto_test = Proyecto(
            id=9999,
            contrato="PROYECTO DE PRUEBA - Link Documentos",
            cliente="Cliente de Prueba",
            fecha_inicio=datetime(2024, 1, 1),
            fecha_termino=datetime(2024, 12, 31),
            region="Metropolitana",
            ciudad="Santiago",
            estado="En Progreso",
            monto=1000000,
            rut_cliente="12.345.678-9",
            tipo_cliente="Privado",
            persona_contacto="Juan Pérez",
            telefono_contacto="123456789",
            correo_contacto="juan@test.com",
            superficie_terreno=500,
            superficie_construida=300,
            tipo_obra_lista="OTROS",
            ems=True,
            estudio_sismico=False,
            estudio_geoelectrico=False,
            topografia=True,
            sondaje=False,
            hidraulica_hidrologia=False,
            descripcion="Proyecto de prueba para verificar link_documentos",
            certificado_experiencia=True,
            orden_compra=True,
            contrato_doc=True,
            factura=False,
            numero_factura="",
            numero_orden_compra="OC-2024-001",
            link_documentos="https://drive.google.com/drive/folders/TEST123456789"
        )
        
        # Validar datos
        is_valid, errors = proyecto_test.validate()
        if not is_valid:
            print(f"❌ Error validando proyecto: {errors}")
            return False
        
        # Verificar si ya existe
        existing = collection.find_one({'id': 9999})
        if existing:
            print("⚠️  Proyecto de prueba ya existe, actualizando...")
            collection.update_one(
                {'id': 9999},
                {'$set': proyecto_test.to_dict()}
            )
        else:
            print("✅ Insertando proyecto de prueba...")
            collection.insert_one(proyecto_test.to_dict())
        
        # Verificar que se guardó correctamente
        saved_project = collection.find_one({'id': 9999})
        if saved_project:
            print(f"✅ Proyecto guardado correctamente!")
            print(f"📋 ID: {saved_project['id']}")
            print(f"📋 Contrato: {saved_project['contrato']}")
            print(f"🔗 Link Documentos: {saved_project.get('link_documentos', 'NO ENCONTRADO')}")
            
            if saved_project.get('link_documentos'):
                print("🎉 ¡El campo link_documentos se guardó correctamente!")
            else:
                print("❌ El campo link_documentos NO se guardó")
                
        else:
            print("❌ No se pudo encontrar el proyecto guardado")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Error en la prueba: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Iniciando prueba de link_documentos...")
    success = test_link_documentos()
    if success:
        print("✅ Prueba completada exitosamente!")
        print("💡 Ahora puedes verificar en la interfaz web que el link aparece correctamente.")
    else:
        print("❌ Prueba falló!")
        sys.exit(1)
