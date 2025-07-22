from typing import List, Optional, Dict, Any
from datetime import datetime
import logging
from bson import ObjectId
from pymongo.errors import PyMongoError

from db.conexion import get_collection, test_mongodb_connection
from models.proyecto import Proyecto, STATUS_OPTIONS, create_indexes, get_collection_stats

logger = logging.getLogger(__name__)

class ProyectoController:
    """Controlador para manejar operaciones CRUD de proyectos en MongoDB Atlas con CSV almacenado en BD"""

    def __init__(self):
        self.collection_name = "proyectos"
        self._collection = None
        self._initialize_collection()

    def _initialize_collection(self):
        """Inicializa la colección y crea índices si es necesario"""
        try:
            self._collection = get_collection(self.collection_name)

            # Crear índices si la colección está vacía (primera vez)
            if self._collection.count_documents({}) == 0:
                create_indexes(self._collection)
                logger.info("🔧 Colección inicializada con índices")

        except Exception as e:
            logger.error(f"❌ Error inicializando colección: {e}")



    def get_collection(self):
        """Obtiene la colección de proyectos"""
        if self._collection is None:
            self._initialize_collection()
        return self._collection



    def create_proyecto(self, proyecto: Proyecto) -> bool:
        """Crea un nuevo proyecto en MongoDB Atlas"""
        try:
            collection = self.get_collection()

            # Validar datos antes de insertar
            is_valid, errors = proyecto.validate()
            if not is_valid:
                logger.error(f"❌ Datos inválidos: {errors}")
                return False

            # Generar ID único si no existe
            if not proyecto.id:
                proyecto.id = self._generate_next_id()

            # Preparar datos para inserción
            data = proyecto.to_dict()
            data.pop('_id', None)  # Dejar que MongoDB genere el _id

            # Insertar documento en MongoDB
            result = collection.insert_one(data)
            proyecto._id = result.inserted_id

            logger.info(f"✅ Proyecto creado con ID: {proyecto.id}, MongoDB _id: {result.inserted_id}")
            return True


        except PyMongoError as e:
            logger.error(f"❌ Error de MongoDB al crear proyecto: {e}")
            return False
        except Exception as e:
            logger.error(f"❌ Error inesperado al crear proyecto: {e}")
            return False

    def get_all_proyectos(self) -> List[Proyecto]:
        """Obtiene todos los proyectos de MongoDB Atlas"""
        try:
            collection = self.get_collection()

            # Obtener documentos ordenados por ID
            cursor = collection.find().sort("id", 1)

            proyectos = []
            for doc in cursor:
                proyecto = Proyecto.from_dict(doc)
                proyectos.append(proyecto)

            logger.info(f"📊 Obtenidos {len(proyectos)} proyectos")
            return proyectos

        except PyMongoError as e:
            logger.error(f"❌ Error de MongoDB al obtener proyectos: {e}")
            return []
        except Exception as e:
            logger.error(f"❌ Error inesperado al obtener proyectos: {e}")
            return []

    def get_proyecto_by_id(self, proyecto_id: int) -> Optional[Proyecto]:
        """Obtiene un proyecto por su ID"""
        try:
            collection = self.get_collection()
            doc = collection.find_one({"id": proyecto_id})

            if doc:
                proyecto = Proyecto.from_dict(doc)
                logger.info(f"📋 Proyecto encontrado: {proyecto_id}")
                return proyecto
            else:
                logger.warning(f"⚠️ Proyecto no encontrado: {proyecto_id}")
                return None

        except PyMongoError as e:
            logger.error(f"❌ Error de MongoDB al obtener proyecto {proyecto_id}: {e}")
            return None
        except Exception as e:
            logger.error(f"❌ Error inesperado al obtener proyecto {proyecto_id}: {e}")
            return None

    def update_proyecto(self, proyecto: Proyecto) -> bool:
        """Actualiza un proyecto existente"""
        try:
            collection = self.get_collection()

            # Validar datos antes de actualizar
            is_valid, errors = proyecto.validate()
            if not is_valid:
                logger.error(f"❌ Datos inválidos para actualización: {errors}")
                return False

            # Preparar datos para actualización
            data = proyecto.to_dict()
            data.pop('_id', None)  # No actualizar el _id
            data['updated_at'] = datetime.now()

            # Actualizar documento
            result = collection.update_one(
                {"id": proyecto.id},
                {"$set": data}
            )

            if result.modified_count > 0:
                logger.info(f"✅ Proyecto {proyecto.id} actualizado")
                return True
            elif result.matched_count > 0:
                logger.info(f"ℹ️ Proyecto {proyecto.id} encontrado pero sin cambios")
                return True
            else:
                logger.warning(f"⚠️ No se encontró proyecto con ID {proyecto.id}")
                return False

        except PyMongoError as e:
            logger.error(f"❌ Error de MongoDB al actualizar proyecto {proyecto.id}: {e}")
            return False
        except Exception as e:
            logger.error(f"❌ Error inesperado al actualizar proyecto {proyecto.id}: {e}")
            return False

    def delete_proyecto(self, proyecto_id: int) -> bool:
        """Elimina un proyecto por su ID"""
        try:
            collection = self.get_collection()

            result = collection.delete_one({"id": proyecto_id})

            if result.deleted_count > 0:
                logger.info(f"🗑️ Proyecto {proyecto_id} eliminado")
                return True
            else:
                logger.warning(f"⚠️ No se encontró proyecto con ID {proyecto_id}")
                return False

        except PyMongoError as e:
            logger.error(f"❌ Error de MongoDB al eliminar proyecto {proyecto_id}: {e}")
            return False
        except Exception as e:
            logger.error(f"❌ Error inesperado al eliminar proyecto {proyecto_id}: {e}")
            return False

    def search_proyectos(self, cliente_filter: str = "", estado_filter: str = "") -> List[Proyecto]:
        """Busca proyectos por cliente y/o estado usando índices de MongoDB"""
        try:
            collection = self.get_collection()
            query = {}

            # Filtro por cliente usando índice de texto
            if cliente_filter:
                query["$text"] = {"$search": cliente_filter}

            # Filtro por estado
            if estado_filter and estado_filter not in ["Select Status", ""]:
                query["estado"] = estado_filter

            # Ejecutar consulta con ordenamiento
            cursor = collection.find(query).sort("id", 1)

            proyectos = []
            for doc in cursor:
                proyecto = Proyecto.from_dict(doc)
                proyectos.append(proyecto)

            logger.info(f"🔍 Búsqueda completada: {len(proyectos)} resultados")
            return proyectos

        except PyMongoError as e:
            logger.error(f"❌ Error de MongoDB en búsqueda: {e}")
            return []
        except Exception as e:
            logger.error(f"❌ Error inesperado en búsqueda: {e}")
            return []

    def _generate_next_id(self) -> int:
        """Genera el siguiente ID disponible usando agregación de MongoDB"""
        try:
            collection = self.get_collection()

            # Usar agregación para obtener el ID máximo
            pipeline = [
                {"$group": {"_id": None, "max_id": {"$max": "$id"}}}
            ]

            result = list(collection.aggregate(pipeline))

            if result and result[0]["max_id"]:
                next_id = result[0]["max_id"] + 1
            else:
                next_id = 1001  # ID inicial

            logger.info(f"🔢 Siguiente ID generado: {next_id}")
            return next_id

        except PyMongoError as e:
            logger.error(f"❌ Error de MongoDB al generar ID: {e}")
            return 1001
        except Exception as e:
            logger.error(f"❌ Error inesperado al generar ID: {e}")
            return 1001

    def bulk_insert_proyectos(self, proyectos: List[Proyecto]) -> bool:
        """Inserta múltiples proyectos de una vez usando operación bulk"""
        try:
            if not proyectos:
                logger.warning("⚠️ Lista de proyectos vacía")
                return False

            collection = self.get_collection()
            documents = []

            for proyecto in proyectos:
                # Validar cada proyecto
                is_valid, errors = proyecto.validate()
                if not is_valid:
                    logger.warning(f"⚠️ Proyecto inválido omitido: {errors}")
                    continue

                # Generar ID solo si no existe
                if not proyecto.id:
                    proyecto.id = self._generate_next_id()

                # Preparar documento
                data = proyecto.to_dict()
                data.pop('_id', None)
                documents.append(data)

            if documents:
                result = collection.insert_many(documents, ordered=False)
                logger.info(f"📦 Insertados {len(result.inserted_ids)} proyectos en lote")
                return True
            else:
                logger.warning("⚠️ No hay documentos válidos para insertar")
                return False

        except PyMongoError as e:
            logger.error(f"❌ Error de MongoDB en inserción masiva: {e}")
            return False
        except Exception as e:
            logger.error(f"❌ Error inesperado en inserción masiva: {e}")
            return False

    def get_statistics(self) -> Dict[str, Any]:
        """Obtiene estadísticas de la colección"""
        try:
            collection = self.get_collection()
            return get_collection_stats(collection)
        except Exception as e:
            logger.error(f"❌ Error obteniendo estadísticas: {e}")
            return {}

    def delete_records(self, ids: List[int]) -> bool:
        """Elimina múltiples registros por sus IDs"""
        try:
            collection = self.get_collection()

            result = collection.delete_many({"id": {"$in": ids}})

            if result.deleted_count > 0:
                logger.info(f"🗑️ Eliminados {result.deleted_count} proyectos")
                return True
            else:
                logger.warning(f"⚠️ No se encontraron proyectos con los IDs proporcionados")
                return False

        except PyMongoError as e:
            logger.error(f"❌ Error de MongoDB al eliminar proyectos: {e}")
            return False
        except Exception as e:
            logger.error(f"❌ Error inesperado al eliminar proyectos: {e}")
            return False

    def test_connection(self) -> bool:
        """Prueba la conexión a MongoDB Atlas"""
        try:
            connection_info = test_mongodb_connection()
            return connection_info.get("status") == "connected"
        except Exception as e:
            logger.error(f"❌ Error probando conexión: {e}")
            return False

# Instancia global del controlador
proyecto_controller = ProyectoController()