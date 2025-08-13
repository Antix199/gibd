from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError
import logging
import os
import sys
import ssl
import platform
from urllib.parse import quote_plus

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_ssl_context():
    """Configura el contexto SSL para ejecutables"""
    if getattr(sys, 'frozen', False):
        # Estamos en un ejecutable
        if platform.system() == 'Darwin':  # macOS
            # En macOS, usar contexto SSL sin verificación de certificados
            context = ssl.create_default_context()
            context.check_hostname = False
            context.verify_mode = ssl.CERT_NONE
            logger.info("🔒 Configuración SSL para ejecutable macOS: verificación deshabilitada")
            return context
        elif platform.system() == 'Windows':
            # En Windows, intentar usar certificados del sistema
            try:
                context = ssl.create_default_context()
                logger.info("🔒 Configuración SSL para ejecutable Windows: certificados del sistema")
                return context
            except Exception as e:
                logger.warning(f"⚠️ Error configurando SSL en Windows: {e}")
                context = ssl.create_default_context()
                context.check_hostname = False
                context.verify_mode = ssl.CERT_NONE
                return context

    # Desarrollo: usar configuración por defecto
    return None

class DatabaseConnection:
    """Clase para manejar la conexión a MongoDB Atlas :)"""

    def __init__(self, username=None, password=None):
        # Credenciales de MongoDB Atlas - usar las proporcionadas o las por defecto
        self.username = username or "Admin"
        self.password = password or "Admin123"
        self.cluster_url = "proyectosdb.v5zsbpp.mongodb.net"
        self.database_name = "glaciaring_db"

        # Construir URI de conexión
        self.connection_string = self._build_connection_string()

        self.client = None
        self.db = None

    def _build_connection_string(self):
        """Construye la cadena de conexión de MongoDB Atlas completita"""
        # Escapar caracteres especiales en la contraseña
        escaped_password = quote_plus(self.password)

        connection_string = (
            f"mongodb+srv://{self.username}:{escaped_password}@{self.cluster_url}/"
            f"{self.database_name}?retryWrites=true&w=majority&appName=glaciaring"
        )

        return connection_string

    def update_credentials(self, username, password):
        """Actualiza las credenciales y reconstruye la cadena de conexión"""
        self.username = username
        self.password = password
        self.connection_string = self._build_connection_string()

        # Cerrar conexión existente si existe
        if self.client:
            self.client.close()
            self.client = None
            self.db = None

        logger.info(f"🔄 Credenciales actualizadas para usuario: {username}")

    def connect(self):
        """Establece la conexión con MongoDB Atlas"""
        try:
            logger.info("Intentando conectar a MongoDB Atlas...")

            # Crear cliente con configuración optimizada
            ssl_context = get_ssl_context()

            client_kwargs = {
                'serverSelectionTimeoutMS': 5000,  # 5 segundos timeout
                'connectTimeoutMS': 10000,         # 10 segundos para conectar
                'socketTimeoutMS': 20000,          # 20 segundos para operaciones
                'maxPoolSize': 50,                 # Máximo 50 conexiones
                'retryWrites': True
            }

            # Agregar configuración SSL si es necesaria
            if ssl_context:
                client_kwargs['ssl_context'] = ssl_context
                logger.info("🔒 Usando configuración SSL personalizada")

            self.client = MongoClient(self.connection_string, **client_kwargs)

            # Verificar la conexión
            self.client.admin.command('ping')

            # Obtener la base de datos
            self.db = self.client[self.database_name]

            logger.info(f"✅ Conexión exitosa a MongoDB Atlas - Base de datos: {self.database_name}")
            return True

        except ServerSelectionTimeoutError as e:
            logger.error(f"❌ Error de timeout al conectar con MongoDB Atlas: {e}")

            # Intentar conexión alternativa para ejecutables con problemas SSL
            if getattr(sys, 'frozen', False) and 'SSL' in str(e):
                logger.info("🔄 Intentando conexión alternativa sin SSL...")
                return self._try_alternative_connection()

            return False
        except ConnectionFailure as e:
            logger.error(f"❌ Error de conexión con MongoDB Atlas: {e}")

            # Intentar conexión alternativa para ejecutables con problemas SSL
            if getattr(sys, 'frozen', False) and 'SSL' in str(e):
                logger.info("🔄 Intentando conexión alternativa sin SSL...")
                return self._try_alternative_connection()

            return False
        except Exception as e:
            logger.error(f"❌ Error inesperado al conectar: {e}")
            return False

    def _try_alternative_connection(self):
        """Intenta conexión alternativa para ejecutables con problemas SSL"""
        try:
            logger.info("🔄 Intentando conexión con SSL deshabilitado...")

            # Crear contexto SSL completamente permisivo
            context = ssl.create_default_context()
            context.check_hostname = False
            context.verify_mode = ssl.CERT_NONE

            # Configuración alternativa más permisiva
            alternative_kwargs = {
                'serverSelectionTimeoutMS': 10000,  # Más tiempo
                'connectTimeoutMS': 20000,
                'socketTimeoutMS': 30000,
                'ssl_context': context,
                'retryWrites': True,
                'w': 'majority'
            }

            self.client = MongoClient(self.connection_string, **alternative_kwargs)

            # Verificar la conexión
            self.client.admin.command('ping')

            # Obtener la base de datos
            self.db = self.client[self.database_name]

            logger.info("✅ Conexión alternativa exitosa (SSL deshabilitado)")
            return True

        except Exception as e:
            logger.error(f"❌ Conexión alternativa también falló: {e}")
            return False

    def get_database(self):
        """Retorna la instancia de la base de datos"""
        if self.db is None:
            if not self.connect():
                raise Exception("No se pudo establecer conexión con MongoDB Atlas")
        return self.db

    def get_collection(self, collection_name):
        """Retorna una colección específica"""
        db = self.get_database()
        return db[collection_name]

    def test_connection(self):
        """Prueba la conexión y retorna información del servidor"""
        try:
            if not self.client:
                self.connect()

            # Obtener información del servidor
            server_info = self.client.server_info()
            db_stats = self.db.command("dbstats")

            connection_info = {
                "status": "connected",
                "server_version": server_info.get("version"),
                "database": self.database_name,
                "collections_count": len(self.db.list_collection_names()),
                "db_size_mb": round(db_stats.get("dataSize", 0) / (1024 * 1024), 2)
            }

            logger.info(f"📊 Información de conexión: {connection_info}")
            return connection_info

        except Exception as e:
            logger.error(f"❌ Error al probar conexión: {e}")
            return {"status": "error", "message": str(e)}

    def close_connection(self):
        """Cierra la conexión con MongoDB"""
        if self.client:
            self.client.close()
            logger.info("🔌 Conexión cerrada")

# Mapeo de tipos de usuario a credenciales de MongoDB
# Nota: Ambos tipos de usuario usan las mismas credenciales de MongoDB Atlas
# La diferenciación de permisos se maneja a nivel de aplicación
USER_CREDENTIALS = {
    'admin': {'username': 'Admin', 'password': 'Admin123'},
    'reader': {'username': 'Admin', 'password': 'Admin123'}  # Usar las mismas credenciales válidas
}

# Instancia global de la conexión
db_connection = DatabaseConnection()

def get_db_for_user(user_type='admin'):
    """Función helper para obtener la base de datos con credenciales específicas del usuario"""
    if user_type in USER_CREDENTIALS:
        credentials = USER_CREDENTIALS[user_type]
        db_connection.update_credentials(credentials['username'], credentials['password'])
    return db_connection.get_database()

def get_collection_for_user(collection_name, user_type='admin'):
    """Función helper para obtener una colección con credenciales específicas del usuario"""
    if user_type in USER_CREDENTIALS:
        credentials = USER_CREDENTIALS[user_type]
        db_connection.update_credentials(credentials['username'], credentials['password'])
    return db_connection.get_collection(collection_name)

def get_db():
    """Función helper para obtener la base de datos (mantiene compatibilidad)"""
    return db_connection.get_database()

def get_collection(collection_name):
    """Función helper para obtener una colección (mantiene compatibilidad)"""
    return db_connection.get_collection(collection_name)

def test_mongodb_connection():
    """Función para probar la conexión desde otros módulos"""
    return db_connection.test_connection()