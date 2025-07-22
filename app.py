#!/usr/bin/env python3
"""
GlaciarIng - Aplicación de gestión de proyectos
Archivo principal que lanza la aplicación con MongoDB Atlas
"""

import tkinter as tk
from tkinter import messagebox
import logging
import sys
import os

# Agregar el directorio raíz al path para importar módulos
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from views.interfaz import MainWindow
from db.conexion import db_connection, test_mongodb_connection

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('glaciaring.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

def check_database_connection():
    """Verifica la conexión a MongoDB Atlas"""
    try:
        logger.info("🔄 Verificando conexión a MongoDB Atlas...")

        connection_info = test_mongodb_connection()

        if connection_info.get("status") == "connected":
            logger.info("✅ Conexión a MongoDB Atlas establecida correctamente")
            logger.info(f"📊 Servidor: {connection_info.get('server_version')}")
            logger.info(f"🗄️ Base de datos: {connection_info.get('database')}")
            logger.info(f"📁 Colecciones: {connection_info.get('collections_count')}")
            return True
        else:
            logger.error("❌ No se pudo conectar a MongoDB Atlas")
            logger.error(f"Error: {connection_info.get('message')}")
            return False

    except Exception as e:
        logger.error(f"❌ Error al verificar conexión: {e}")
        return False

def create_sample_data():
    """Crea datos de ejemplo si la base de datos está vacía"""
    try:
        from controllers.controller import proyecto_controller
        from models.proyecto import Proyecto
        from datetime import datetime

        # Verificar si ya hay datos
        proyectos = proyecto_controller.get_all_proyectos()
        if proyectos:
            logger.info(f"📊 Base de datos ya contiene {len(proyectos)} registros")
            return

        logger.info("📦 Creando datos de ejemplo...")

        # Crear datos de ejemplo
        sample_data = [
            Proyecto(id=1001, name="Alice Smith", date=datetime(2023, 1, 15), status="Completed", amount=120.00),
            Proyecto(id=1002, name="Bob Johnson", date=datetime(2023, 1, 18), status="Pending", amount=75.50),
            Proyecto(id=1003, name="Charlie Brown", date=datetime(2023, 1, 20), status="Active", amount=200.00),
            Proyecto(id=1004, name="Diana Prince", date=datetime(2023, 1, 22), status="Completed", amount=99.99),
            Proyecto(id=1005, name="Eve Adams", date=datetime(2023, 1, 25), status="Pending", amount=50.00),
        ]

        # Insertar datos de ejemplo
        success_count = 0
        for proyecto in sample_data:
            if proyecto_controller.create_proyecto(proyecto):
                success_count += 1

        logger.info(f"✅ Se crearon {success_count} registros de ejemplo")

    except Exception as e:
        logger.error(f"❌ Error al crear datos de ejemplo: {e}")

def show_connection_error():
    """Muestra un diálogo de error de conexión más detallado"""
    error_message = """
❌ No se pudo conectar a MongoDB Atlas

Posibles causas:
• Credenciales incorrectas
• Problemas de red/firewall
• MongoDB Atlas no disponible
• IP no autorizada en Atlas

Soluciones:
1. Verificar credenciales en db/conexion.py
2. Verificar conexión a internet
3. Autorizar IP en MongoDB Atlas
4. Ejecutar: python test_connection.py

¿Deseas continuar sin base de datos?
(Los datos se guardarán solo en memoria)
    """

    return messagebox.askyesno(
        "Error de Conexión - MongoDB Atlas",
        error_message
    )

def main():
    """Función principal de la aplicación"""
    try:
        logger.info("🚀 Iniciando GlaciarIng con MongoDB Atlas...")

        # Verificar conexión a la base de datos
        db_connected = check_database_connection()

        if not db_connected:
            # Mostrar diálogo de error más informativo
            continue_without_db = show_connection_error()

            if not continue_without_db:
                logger.info("👋 Aplicación cancelada por el usuario")
                return
            else:
                logger.warning("⚠️ Continuando sin conexión a base de datos")
        else:
            # Crear datos de ejemplo si es necesario
            create_sample_data()

        # Crear ventana principal
        root = tk.Tk()

        # Configurar la ventana principal
        root.title("GlaciarIng - Sistema de Gestión de Proyectos (MongoDB Atlas)")

        # Maximizar ventana según el sistema operativo
        try:
            root.state('zoomed')  # Windows
        except:
            try:
                root.attributes('-zoomed', True)  # Linux
            except:
                root.geometry("1200x800")  # Fallback

        # Crear la aplicación
        app = MainWindow(root)

        # Manejar el cierre de la aplicación
        def on_closing():
            try:
                logger.info("🔌 Cerrando conexión a base de datos...")
                db_connection.close_connection()
                logger.info("👋 Aplicación cerrada correctamente")
                root.destroy()
            except Exception as e:
                logger.error(f"❌ Error al cerrar aplicación: {e}")
                root.destroy()

        root.protocol("WM_DELETE_WINDOW", on_closing)

        # Mostrar estado de conexión en el título
        if db_connected:
            root.title(root.title() + " - ✅ Conectado")
        else:
            root.title(root.title() + " - ⚠️ Sin BD")

        # Iniciar el loop principal
        logger.info("✅ Aplicación iniciada correctamente")
        root.mainloop()

    except Exception as e:
        logger.error(f"❌ Error crítico en la aplicación: {e}")
        messagebox.showerror(
            "Error Crítico",
            f"Error inesperado: {str(e)}\n\nRevisa el archivo glaciaring.log para más detalles."
        )
    finally:
        # Asegurar que la conexión se cierre
        try:
            db_connection.close_connection()
        except:
            pass

if __name__ == "__main__":
    main()