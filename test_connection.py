#!/usr/bin/env python3
"""
Script para probar la conexión a MongoDB Atlas
"""

import sys
import os
from datetime import datetime

# Agregar el directorio raíz al path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_mongodb_connection():
    """Prueba la conexión a MongoDB Atlas"""
    print("🔄 Probando conexión a MongoDB Atlas...")
    print("=" * 50)
    
    try:
        # Importar módulos
        from db.conexion import db_connection, test_mongodb_connection
        from controllers.controller import proyecto_controller
        from models.proyecto import Proyecto
        
        # 1. Probar conexión básica
        print("1️⃣ Probando conexión básica...")
        connection_info = test_mongodb_connection()
        
        if connection_info.get("status") == "connected":
            print("✅ Conexión exitosa!")
            print(f"   📊 Versión del servidor: {connection_info.get('server_version')}")
            print(f"   🗄️ Base de datos: {connection_info.get('database')}")
            print(f"   📁 Colecciones: {connection_info.get('collections_count')}")
            print(f"   💾 Tamaño DB: {connection_info.get('db_size_mb')} MB")
        else:
            print("❌ Error de conexión:")
            print(f"   {connection_info.get('message')}")
            return False
        
        print("\n2️⃣ Probando operaciones CRUD...")
        
        # 2. Probar crear proyecto
        print("   📝 Creando proyecto de prueba...")
        test_proyecto = Proyecto(
            name="Proyecto de Prueba MongoDB",
            status="Active",
            amount=150.75,
            date=datetime.now()
        )
        
        if proyecto_controller.create_proyecto(test_proyecto):
            print(f"   ✅ Proyecto creado con ID: {test_proyecto.id}")
        else:
            print("   ❌ Error creando proyecto")
            return False
        
        # 3. Probar leer proyectos
        print("   📖 Leyendo proyectos...")
        proyectos = proyecto_controller.get_all_proyectos()
        print(f"   ✅ Encontrados {len(proyectos)} proyectos")
        
        # 4. Probar búsqueda
        print("   🔍 Probando búsqueda...")
        resultados = proyecto_controller.search_proyectos("Prueba", "Active")
        print(f"   ✅ Búsqueda completada: {len(resultados)} resultados")
        
        # 5. Probar actualización
        print("   ✏️ Actualizando proyecto...")
        test_proyecto.name = "Proyecto Actualizado"
        test_proyecto.amount = 200.00
        
        if proyecto_controller.update_proyecto(test_proyecto):
            print("   ✅ Proyecto actualizado")
        else:
            print("   ❌ Error actualizando proyecto")
        
        # 6. Probar estadísticas
        print("   📊 Obteniendo estadísticas...")
        stats = proyecto_controller.get_statistics()
        if stats:
            print(f"   ✅ Total proyectos: {stats.get('total_projects', 0)}")
            print(f"   ✅ Monto total: ${stats.get('total_amount', 0):.2f}")
        
        # 7. Limpiar - eliminar proyecto de prueba
        print("   🧹 Limpiando proyecto de prueba...")
        if proyecto_controller.delete_proyecto(test_proyecto.id):
            print("   ✅ Proyecto de prueba eliminado")
        
        print("\n🎉 ¡Todas las pruebas completadas exitosamente!")
        print("✅ MongoDB Atlas está funcionando correctamente")
        return True
        
    except ImportError as e:
        print(f"❌ Error de importación: {e}")
        print("💡 Asegúrate de que pymongo esté instalado: pip install pymongo")
        return False
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        return False

def create_sample_data():
    """Crea datos de ejemplo en MongoDB Atlas"""
    print("\n🔄 Creando datos de ejemplo...")
    print("=" * 50)
    
    try:
        from controllers.controller import proyecto_controller
        from models.proyecto import Proyecto
        
        # Verificar si ya hay datos
        proyectos_existentes = proyecto_controller.get_all_proyectos()
        if len(proyectos_existentes) > 0:
            print(f"ℹ️ Ya existen {len(proyectos_existentes)} proyectos en la base de datos")
            respuesta = input("¿Deseas agregar más datos de ejemplo? (s/n): ")
            if respuesta.lower() != 's':
                return True
        
        # Datos de ejemplo
        sample_data = [
            Proyecto(id=1001, name="Alice Smith", date=datetime(2023, 1, 15), status="Completed", amount=120.00),
            Proyecto(id=1002, name="Bob Johnson", date=datetime(2023, 1, 18), status="Pending", amount=75.50),
            Proyecto(id=1003, name="Charlie Brown", date=datetime(2023, 1, 20), status="Active", amount=200.00),
            Proyecto(id=1004, name="Diana Prince", date=datetime(2023, 1, 22), status="Completed", amount=99.99),
            Proyecto(id=1005, name="Eve Adams", date=datetime(2023, 1, 25), status="Pending", amount=50.00),
        ]
        
        # Insertar datos
        print(f"📦 Insertando {len(sample_data)} proyectos de ejemplo...")
        
        success_count = 0
        for proyecto in sample_data:
            if proyecto_controller.create_proyecto(proyecto):
                success_count += 1
                print(f"   ✅ {proyecto.name} - ${proyecto.amount}")
            else:
                print(f"   ⚠️ Error insertando {proyecto.name}")
        
        print(f"\n🎉 Insertados {success_count}/{len(sample_data)} proyectos exitosamente!")
        return True
        
    except Exception as e:
        print(f"❌ Error creando datos de ejemplo: {e}")
        return False

def main():
    """Función principal"""
    print("🚀 GlaciarIng - Prueba de Conexión MongoDB Atlas")
    print("=" * 60)
    
    # Probar conexión
    if not test_mongodb_connection():
        print("\n❌ Las pruebas de conexión fallaron")
        sys.exit(1)
    
    # Preguntar si crear datos de ejemplo
    print("\n" + "=" * 60)
    respuesta = input("¿Deseas crear datos de ejemplo? (s/n): ")
    
    if respuesta.lower() == 's':
        if create_sample_data():
            print("\n✅ Datos de ejemplo creados exitosamente")
        else:
            print("\n❌ Error creando datos de ejemplo")
    
    print("\n🎯 Conexión configurada y lista para usar!")
    print("💡 Ahora puedes ejecutar tu aplicación principal con: python app.py")

if __name__ == "__main__":
    main()
