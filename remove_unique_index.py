#!/usr/bin/env python3
"""
Script para eliminar el índice único del campo 'id' en MongoDB
y recrear un índice no único.
"""

import logging
from db.conexion import get_collection

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def remove_unique_index():
    """Elimina el índice único del campo 'id' y crea uno no único"""
    try:
        collection = get_collection("proyectos")
        
        # Listar índices existentes
        indexes = list(collection.list_indexes())
        logger.info("📋 Índices existentes:")
        for idx in indexes:
            logger.info(f"  - {idx['name']}: {idx.get('key', {})}")
        
        # Eliminar el índice único del campo 'id' si existe
        try:
            collection.drop_index("id_1")
            logger.info("✅ Índice único 'id_1' eliminado")
        except Exception as e:
            logger.warning(f"⚠️ No se pudo eliminar el índice 'id_1': {e}")
        
        # Crear nuevo índice no único
        try:
            collection.create_index("id")
            logger.info("✅ Nuevo índice no único en 'id' creado")
        except Exception as e:
            logger.warning(f"⚠️ Error creando índice no único: {e}")
        
        # Listar índices después del cambio
        indexes_after = list(collection.list_indexes())
        logger.info("📋 Índices después del cambio:")
        for idx in indexes_after:
            logger.info(f"  - {idx['name']}: {idx.get('key', {})}")
        
        logger.info("🎉 Proceso completado. Ahora los IDs pueden estar repetidos.")
        return True
        
    except Exception as e:
        logger.error(f"❌ Error en el proceso: {e}")
        return False

if __name__ == "__main__":
    remove_unique_index()
