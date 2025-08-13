from datetime import datetime
from typing import Optional, Dict, Any
from bson import ObjectId
import logging

logger = logging.getLogger(__name__)

class Proyecto:
    """Modelo para representar un proyecto/registro en MongoDB Atlas"""

    def __init__(self,
                 id: int = None,
                 contrato: str = "",
                 cliente: str = "",
                 fecha_inicio: Optional[datetime] = None,
                 fecha_termino: Optional[datetime] = None,
                 region: str = "",
                 ciudad: str = "",
                 estado: str = "Activo",
                 monto: float = 0.0,
                 # Información del cliente
                 rut_cliente: str = "",
                 tipo_cliente: str = "",
                 persona_contacto: str = "",
                 telefono_contacto: str = "",
                 correo_contacto: str = "",
                 # Información técnica
                 superficie_terreno: Optional[float] = None,
                 superficie_construida: Optional[float] = None,
                 tipo_obra_lista: str = "",
                 # Estudios y servicios
                 ems: bool = False,
                 estudio_sismico: bool = False,
                 estudio_geoelectrico: bool = False,
                 topografia: bool = False,
                 sondaje: bool = False,
                 hidraulica_hidrologia: bool = False,
                 descripcion: str = "",
                 certificado_experiencia: bool = False,
                 orden_compra: bool = False,
                 contrato_doc: bool = False,
                 factura: bool = False,
                 numero_factura: str = "",
                 numero_orden_compra: str = "",
                 link_documentos: str = "",
                 _id: Optional[ObjectId] = None,
                 created_at: Optional[datetime] = None,
                 updated_at: Optional[datetime] = None):
        self.id = id
        self.contrato = contrato
        self.cliente = cliente
        self.fecha_inicio = fecha_inicio
        self.fecha_termino = fecha_termino
        self.region = region
        self.ciudad = ciudad
        self.estado = estado
        self.monto = monto
        # Información del cliente
        self.rut_cliente = rut_cliente
        self.tipo_cliente = tipo_cliente
        self.persona_contacto = persona_contacto
        self.telefono_contacto = telefono_contacto
        self.correo_contacto = correo_contacto
        # Información técnica
        self.superficie_terreno = superficie_terreno
        self.superficie_construida = superficie_construida
        self.tipo_obra_lista = tipo_obra_lista
        # Estudios y servicios
        self.ems = ems
        self.estudio_sismico = estudio_sismico
        self.estudio_geoelectrico = estudio_geoelectrico
        self.topografia = topografia
        self.sondaje = sondaje
        self.hidraulica_hidrologia = hidraulica_hidrologia
        self.descripcion = descripcion
        self.certificado_experiencia = certificado_experiencia
        self.orden_compra = orden_compra
        self.contrato_doc = contrato_doc
        self.factura = factura
        self.numero_factura = numero_factura
        self.numero_orden_compra = numero_orden_compra
        self.link_documentos = link_documentos
        self._id = _id  # MongoDB ObjectId
        self.created_at = created_at if created_at else datetime.now()
        self.updated_at = updated_at if updated_at else datetime.now()

    def to_dict(self) -> Dict[str, Any]:
        """Convierte el objeto a diccionario para MongoDB"""
        data = {
            'id': self.id,
            'contrato': self.contrato,
            'cliente': self.cliente,
            'fecha_inicio': self.fecha_inicio,
            'fecha_termino': self.fecha_termino,
            'region': self.region,
            'ciudad': self.ciudad,
            'estado': self.estado,
            'monto': self.monto,
            # Información del cliente
            'rut_cliente': self.rut_cliente,
            'tipo_cliente': self.tipo_cliente,
            'persona_contacto': self.persona_contacto,
            'telefono_contacto': self.telefono_contacto,
            'correo_contacto': self.correo_contacto,
            # Información técnica
            'superficie_terreno': self.superficie_terreno,
            'superficie_construida': self.superficie_construida,
            'tipo_obra_lista': self.tipo_obra_lista,
            # Estudios y servicios
            'ems': self.ems,
            'estudio_sismico': self.estudio_sismico,
            'estudio_geoelectrico': self.estudio_geoelectrico,
            'topografia': self.topografia,
            'sondaje': self.sondaje,
            'hidraulica_hidrologia': self.hidraulica_hidrologia,
            'descripcion': self.descripcion,
            'certificado_experiencia': self.certificado_experiencia,
            'orden_compra': self.orden_compra,
            'contrato_doc': self.contrato_doc,
            'factura': self.factura,
            'numero_factura': self.numero_factura,
            'numero_orden_compra': self.numero_orden_compra,
            'link_documentos': self.link_documentos,
            'created_at': self.created_at,
            'updated_at': datetime.now()  # Siempre actualizar timestamp
        }

        # Solo incluir _id si existe
        if self._id:
            data['_id'] = self._id

        return data

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Proyecto':
        """Crea un objeto Proyecto desde un diccionario de MongoDB"""
        return cls(
            id=data.get('id'),
            contrato=data.get('contrato', ''),
            cliente=data.get('cliente', ''),
            fecha_inicio=data.get('fecha_inicio'),
            fecha_termino=data.get('fecha_termino'),
            region=data.get('region', ''),
            ciudad=data.get('ciudad', ''),
            estado=data.get('estado', 'Activo'),
            monto=data.get('monto', 0.0),
            # Información del cliente
            rut_cliente=data.get('rut_cliente', ''),
            tipo_cliente=data.get('tipo_cliente', ''),
            persona_contacto=data.get('persona_contacto', ''),
            telefono_contacto=data.get('telefono_contacto', ''),
            correo_contacto=data.get('correo_contacto', ''),
            # Información técnica
            superficie_terreno=data.get('superficie_terreno'),
            superficie_construida=data.get('superficie_construida'),
            tipo_obra_lista=data.get('tipo_obra_lista', ''),
            # Estudios y servicios
            ems=data.get('ems', False),
            estudio_sismico=data.get('estudio_sismico', False),
            estudio_geoelectrico=data.get('estudio_geoelectrico', False),
            topografia=data.get('topografia', False),
            sondaje=data.get('sondaje', False),
            hidraulica_hidrologia=data.get('hidraulica_hidrologia', False),
            descripcion=data.get('descripcion', ''),
            certificado_experiencia=data.get('certificado_experiencia', False),
            orden_compra=data.get('orden_compra', False),
            contrato_doc=data.get('contrato_doc', False),
            factura=data.get('factura', False),
            numero_factura=data.get('numero_factura', ''),
            numero_orden_compra=data.get('numero_orden_compra', ''),
            link_documentos=data.get('link_documentos', ''),
            _id=data.get('_id'),
            created_at=data.get('created_at'),
            updated_at=data.get('updated_at')
        )

    def update_fields(self, **kwargs):
        """Actualiza campos específicos del proyecto"""
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.updated_at = datetime.now()

    def validate(self) -> tuple[bool, list[str]]:
        """Valida los datos del proyecto"""
        errors = []

        # Validar contrato
        if not self.contrato or len(self.contrato.strip()) < 2:
            errors.append("El contrato debe tener al menos 2 caracteres")

        # Validar cliente
        if not self.cliente or len(self.cliente.strip()) < 2:
            errors.append("El cliente debe tener al menos 2 caracteres")

        # Validar región
        if not self.region or len(self.region.strip()) < 2:
            errors.append("La región debe tener al menos 2 caracteres")

        # Validar ciudad
        if not self.ciudad or len(self.ciudad.strip()) < 2:
            errors.append("La ciudad debe tener al menos 2 caracteres")

        # Validar estado
        if self.estado not in STATUS_OPTIONS:
            errors.append(f"Estado inválido. Opciones válidas: {', '.join(STATUS_OPTIONS)}")

        # Validar monto
        if self.monto < 0:
            errors.append("El monto no puede ser negativo")

        if self.monto > 999999999.99:
            errors.append("El monto es demasiado grande")

        # Validar fechas
        if self.fecha_inicio and self.fecha_inicio > datetime.now():
            errors.append("La fecha de inicio no puede ser futura")

        if self.fecha_termino and self.fecha_inicio and self.fecha_termino < self.fecha_inicio:
            errors.append("La fecha de término no puede ser anterior a la fecha de inicio")

        return len(errors) == 0, errors

    def to_json_serializable(self) -> Dict[str, Any]:
        """Convierte el objeto a formato serializable JSON"""
        data = self.to_dict()

        # Convertir ObjectId a string
        if data.get('_id'):
            data['_id'] = str(data['_id'])

        # Convertir datetime a string ISO
        for field in ['date', 'created_at', 'updated_at']:
            if data.get(field) and isinstance(data[field], datetime):
                data[field] = data[field].isoformat()

        return data

    def __str__(self):
        return f"Proyecto(id={self.id}, contrato='{self.contrato}', cliente='{self.cliente}', estado='{self.estado}', monto={self.monto})"

    def __repr__(self):
        return self.__str__()

# Constantes para los estados disponibles
STATUS_OPTIONS = [
    "Activo",
    "Completado",
    "Pendiente"
]

# Mapeo de colores para estados (para uso en frontend)
STATUS_COLORS = {
    "Activo": "#3498db",      # Azul
    "Completado": "#27ae60",   # Verde
    "Pendiente": "#f39c12"      # Naranja
}

# Función para validar el estado
def validate_status(status: str) -> bool:
    """Valida si el estado es válido"""
    return status in STATUS_OPTIONS

# Función para formatear fecha
def format_date(date: datetime) -> str:
    """Formatea la fecha para mostrar en la interfaz"""
    if isinstance(date, datetime):
        return date.strftime("%Y-%m-%d")
    elif isinstance(date, str):
        try:
            # Intentar parsear si es string ISO
            parsed_date = datetime.fromisoformat(date.replace('Z', '+00:00'))
            return parsed_date.strftime("%Y-%m-%d")
        except:
            return date
    return str(date) if date else ""

# Función para formatear cantidad
def format_amount(amount: float) -> str:
    """Formatea la cantidad como moneda chilena"""
    return f"${amount:,.0f} CLP"

# Función para crear índices en MongoDB
def create_indexes(collection):
    """Crea índices optimizados para la colección de proyectos"""
    try:
        # Índice en el campo 'id' (no único)
        collection.create_index("id")

        # Índice compuesto para búsquedas frecuentes
        collection.create_index([("estado", 1), ("fecha_inicio", -1)])

        # Índice de texto para búsqueda por cliente y contrato
        collection.create_index([("cliente", "text"), ("contrato", "text")])

        # Índice en created_at para ordenamiento
        collection.create_index("created_at")

        logger.info("✅ Índices creados exitosamente")
        return True

    except Exception as e:
        logger.error(f"❌ Error creando índices: {e}")
        return False

# Función para obtener estadísticas de la colección
def get_collection_stats(collection) -> Dict[str, Any]:
    """Obtiene estadísticas de la colección de proyectos"""
    try:
        # Contar documentos por estado
        pipeline = [
            {
                "$group": {
                    "_id": "$status",
                    "count": {"$sum": 1},
                    "total_amount": {"$sum": "$amount"}
                }
            }
        ]

        status_stats = list(collection.aggregate(pipeline))

        # Estadísticas generales
        total_count = collection.count_documents({})
        total_amount = collection.aggregate([
            {"$group": {"_id": None, "total": {"$sum": "$amount"}}}
        ])
        total_amount = list(total_amount)
        total_amount = total_amount[0]["total"] if total_amount else 0

        return {
            "total_projects": total_count,
            "total_amount": total_amount,
            "status_breakdown": {stat["_id"]: stat for stat in status_stats},
            "average_amount": total_amount / total_count if total_count > 0 else 0
        }

    except Exception as e:
        logger.error(f"❌ Error obteniendo estadísticas: {e}")
        return {}