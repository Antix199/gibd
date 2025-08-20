from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError
import logging
import platform
from urllib.parse import quote_plus
import certifi

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DatabaseConnection:
    """Clase para manejar la conexión a MongoDB Atlas de forma multiplataforma"""

    def __init__(self, username=None, password=None):
        self.username = username or "Admin"
        self.password = password or "Admin123"
        self.cluster_url = "proyectosdb.v5zsbpp.mongodb.net"
        self.database_name = "glaciaring_db"

        # Construir URI de conexión
        self.connection_string = self._build_connection_string()

        self.client = None
        self.db = None

    def _build_connection_string(self):
        """Construye la cadena de conexión de MongoDB Atlas"""
        escaped_password = quote_plus(self.password)
        return (
            f"mongodb+srv://{self.username}:{escaped_password}@{self.cluster_url}/"
            f"{self.database_name}?retryWrites=true&w=majority&appName=glaciaring"
        )

    def update_credentials(self, username, password):
        """Actualiza credenciales y reconstruye la conexión"""
        self.username = username
        self.password = password
        self.connection_string = self._build_connection_string()
        if self.client:
            self.client.close()
            self.client = None
            self.db = None
        logger.info(f"🔄 Credenciales actualizadas para usuario: {username}")

    def connect(self):
        """Establece conexión segura con MongoDB Atlas usando certifi"""
        try:
            logger.info("Intentando conectar a MongoDB Atlas...")
            self.client = MongoClient(
                self.connection_string,
                tls=True,
                tlsCAFile=certifi.where(),
                serverSelectionTimeoutMS=5000,  # timeout para selección de servidor
                connectTimeoutMS=10000,
                socketTimeoutMS=20000,
                maxPoolSize=50
            )

            # Probar conexión
            self.client.admin.command('ping')

            # Obtener la base de datos
            self.db = self.client[self.database_name]
            logger.info(f"✅ Conexión exitosa a MongoDB Atlas - Base: {self.database_name}")
            return True

        except ServerSelectionTimeoutError as e:
            logger.error(f"❌ Timeout al conectar MongoDB Atlas: {e}")
            return False
        except ConnectionFailure as e:
            logger.error(f"❌ Falló la conexión con MongoDB Atlas: {e}")
            return False
        except Exception as e:
            logger.error(f"❌ Error inesperado al conectar: {e}")
            return False

    def get_database(self):
        """Retorna la base de datos"""
        if self.db is None:
            if not self.connect():
                raise Exception("No se pudo establecer conexión con MongoDB Atlas")
        return self.db

    def get_collection(self, collection_name):
        """Retorna una colección específica"""
        db = self.get_database()
        return db[collection_name]

    def test_connection(self):
        """Prueba la conexión y retorna info"""
        try:
            if not self.client:
                self.connect()
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

# Credenciales por tipo de usuario
USER_CREDENTIALS = {
    'admin': {'username': 'Admin', 'password': 'Admin123'},
    'reader': {'username': 'Admin', 'password': 'Admin123'}
}

# Instancia global
db_connection = DatabaseConnection()

def get_db_for_user(user_type='admin'):
    if user_type in USER_CREDENTIALS:
        creds = USER_CREDENTIALS[user_type]
        db_connection.update_credentials(creds['username'], creds['password'])
    return db_connection.get_database()

def get_collection_for_user(collection_name, user_type='admin'):
    if user_type in USER_CREDENTIALS:
        creds = USER_CREDENTIALS[user_type]
        db_connection.update_credentials(creds['username'], creds['password'])
    return db_connection.get_collection(collection_name)

def get_db():
    return db_connection.get_database()

def get_collection(collection_name):
    return db_connection.get_collection(collection_name)

def test_mongodb_connection():
    return db_connection.test_connection()
