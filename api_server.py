100#!/usr/bin/env python3
"""
GlaciarIng API Server
API REST para conectar el frontend con MongoDB Atlas
"""

from flask import Flask, request, jsonify, send_from_directory, session, redirect, url_for
from flask_cors import CORS
import logging
import sys
import os
import platform
from datetime import datetime
import json
import secrets
from functools import wraps

# Agregar el directorio raíz al path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from controllers.controller import proyecto_controller
from models.proyecto import Proyecto, STATUS_OPTIONS
from db.conexion import test_mongodb_connection

# Configurar logging
if getattr(sys, 'frozen', False):
    # Ejecutable: logging más simple sin colores
    logging.basicConfig(
        level=logging.INFO,
        format='%(levelname)s: %(message)s'
    )
    # Desactivar logs de werkzeug en ejecutables
    logging.getLogger('werkzeug').setLevel(logging.WARNING)
else:
    # Desarrollo: logging completo
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

logger = logging.getLogger(__name__)

# Crear aplicación Flask
app = Flask(__name__, static_folder='assets', static_url_path='/assets')
CORS(app)  # Permitir CORS para el frontend

# Configuración
app.config['JSON_SORT_KEYS'] = False

# Configuración de sesiones (usando sesiones nativas de Flask)
app.config['SECRET_KEY'] = secrets.token_hex(16)

class CustomJSONEncoder(json.JSONEncoder):
    """Encoder personalizado para manejar datetime y ObjectId"""
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        return super().default(obj)

app.json.encoder = CustomJSONEncoder

# ===== SISTEMA DE AUTENTICACIÓN =====

# Credenciales válidas para login de la aplicación
VALID_CREDENTIALS = {
    'Admin': {'password': 'Admin123', 'type': 'admin'},
    'Lector': {'password': 'Lector123', 'type': 'reader'}
}

def login_required(f):
    """Decorador para requerir autenticación"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return jsonify({
                'success': False,
                'error': 'Autenticación requerida'
            }), 401
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    """Decorador para requerir permisos de administrador"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return jsonify({
                'success': False,
                'error': 'Autenticación requerida'
            }), 401
        if session.get('user_type') != 'admin':
            return jsonify({
                'success': False,
                'error': 'Permisos de administrador requeridos'
            }), 403
        return f(*args, **kwargs)
    return decorated_function

# ===== RUTAS PARA SERVIR EL FRONTEND =====

@app.route('/')
def serve_index():
    """Sirve la página principal (solo para administradores autenticados)"""
    if 'user_id' not in session:
        return redirect('/login')
    if session.get('user_type') != 'admin':
        return redirect('/reader')
    return send_from_directory('.', 'index.html')

@app.route('/login')
def serve_login():
    """Sirve la página de login"""
    return send_from_directory('.', 'login.html')

@app.route('/reader')
def serve_reader():
    """Sirve la página para usuarios lectores"""
    if 'user_id' not in session:
        return redirect('/login')
    if session.get('user_type') != 'reader':
        return redirect('/')
    return send_from_directory('.', 'reader.html')

@app.route('/modify-database.html')
def serve_modify():
    """Sirve la página de modificación (solo administradores)"""
    if 'user_id' not in session:
        return redirect('/login')
    if session.get('user_type') != 'admin':
        return jsonify({'error': 'Acceso denegado'}), 403
    return send_from_directory('.', 'modify-database.html')

@app.route('/<path:filename>')
def serve_static(filename):
    """Sirve archivos estáticos"""
    return send_from_directory('.', filename)

# ===== ENDPOINTS DE AUTENTICACIÓN =====

@app.route('/api/login', methods=['POST'])
def login():
    """Endpoint para autenticación de usuarios"""
    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            return jsonify({
                'success': False,
                'error': 'Usuario y contraseña son requeridos'
            }), 400

        # Verificar credenciales
        if username in VALID_CREDENTIALS:
            user_data = VALID_CREDENTIALS[username]
            if user_data['password'] == password:
                # Crear sesión
                session['user_id'] = username
                session['user_type'] = user_data['type']

                logger.info(f"✅ Login exitoso para usuario: {username} (tipo: {user_data['type']})")

                return jsonify({
                    'success': True,
                    'user_type': user_data['type'],
                    'message': 'Login exitoso'
                })

        logger.warning(f"❌ Intento de login fallido para usuario: {username}")
        return jsonify({
            'success': False,
            'error': 'Credenciales inválidas'
        }), 401

    except Exception as e:
        logger.error(f"Error en login: {e}")
        return jsonify({
            'success': False,
            'error': 'Error interno del servidor'
        }), 500

@app.route('/api/logout', methods=['POST'])
def logout():
    """Endpoint para cerrar sesión"""
    try:
        user_id = session.get('user_id')
        session.clear()
        logger.info(f"✅ Logout exitoso para usuario: {user_id}")

        return jsonify({
            'success': True,
            'message': 'Logout exitoso'
        })

    except Exception as e:
        logger.error(f"Error en logout: {e}")
        return jsonify({
            'success': False,
            'error': 'Error interno del servidor'
        }), 500

@app.route('/api/check-session', methods=['GET'])
def check_session():
    """Endpoint para verificar el estado de la sesión"""
    try:
        if 'user_id' in session:
            return jsonify({
                'authenticated': True,
                'user_id': session['user_id'],
                'user_type': session.get('user_type')
            })
        else:
            return jsonify({
                'authenticated': False
            })

    except Exception as e:
        logger.error(f"Error verificando sesión: {e}")
        return jsonify({
            'authenticated': False,
            'error': str(e)
        }), 500

# ===== API ENDPOINTS =====

@app.route('/api/health', methods=['GET'])
def health_check():
    """Endpoint de salud de la API"""
    try:
        connection_info = test_mongodb_connection()
        return jsonify({
            'status': 'healthy',
            'timestamp': datetime.now().isoformat(),
            'database': connection_info
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e),
            'timestamp': datetime.now().isoformat()
        }), 500

@app.route('/api/proyectos', methods=['GET'])
@login_required
def get_proyectos():
    """Obtiene todos los proyectos o proyectos filtrados"""
    try:
        # Obtener tipo de usuario de la sesión
        user_type = session.get('user_type', 'admin')

        # Obtener parámetros de filtro
        cliente_filter = request.args.get('cliente', '')
        estado_filter = request.args.get('estado', '')

        if cliente_filter or estado_filter:
            proyectos = proyecto_controller.search_proyectos(cliente_filter, estado_filter, user_type)
        else:
            proyectos = proyecto_controller.get_all_proyectos(user_type)
        
        # Convertir a formato JSON serializable
        proyectos_json = []
        for proyecto in proyectos:
            proyecto_dict = proyecto.to_json_serializable()
            proyectos_json.append(proyecto_dict)
        
        return jsonify({
            'success': True,
            'data': proyectos_json,
            'count': len(proyectos_json)
        })
        
    except Exception as e:
        logger.error(f"Error obteniendo proyectos: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/proyectos/<int:proyecto_id>', methods=['GET'])
@login_required
def get_proyecto(proyecto_id):
    """Obtiene un proyecto específico por ID"""
    try:
        # Obtener tipo de usuario de la sesión
        user_type = session.get('user_type', 'admin')
        proyecto = proyecto_controller.get_proyecto_by_id(proyecto_id, user_type)
        
        if proyecto:
            return jsonify({
                'success': True,
                'data': proyecto.to_json_serializable()
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Proyecto no encontrado'
            }), 404
            
    except Exception as e:
        logger.error(f"Error obteniendo proyecto {proyecto_id}: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/proyectos', methods=['POST'])
@admin_required
def create_proyecto():
    """Crea un nuevo proyecto"""
    try:
        data = request.get_json()
        logger.info(f"📝 Datos recibidos para crear proyecto: {data}")

        if not data:
            logger.error("❌ No se proporcionaron datos")
            return jsonify({
                'success': False,
                'error': 'No se proporcionaron datos'
            }), 400
        
        # Crear objeto Proyecto
        try:
            fecha_inicio_value = datetime.fromisoformat(data.get('fecha_inicio')) if data.get('fecha_inicio') else None
        except ValueError as e:
            logger.error(f"❌ Error parseando fecha_inicio: {e}")
            fecha_inicio_value = None

        try:
            fecha_termino_value = datetime.fromisoformat(data.get('fecha_termino')) if data.get('fecha_termino') else None
        except ValueError as e:
            logger.error(f"❌ Error parseando fecha_termino: {e}")
            fecha_termino_value = None

        # Parsear fecha_factura
        fecha_factura_value = None
        if data.get('fecha_factura') and str(data.get('fecha_factura')).strip() and str(data.get('fecha_factura')).lower() != 'null':
            try:
                fecha_factura_value = datetime.fromisoformat(data.get('fecha_factura'))
            except ValueError as e:
                logger.error(f"❌ Error parseando fecha_factura: {e}")
                fecha_factura_value = None

        # Parsear duración
        duracion_value = None
        if data.get('duracion') and str(data.get('duracion')).strip() and str(data.get('duracion')).lower() != 'null':
            try:
                duracion_value = int(data.get('duracion'))
            except (ValueError, TypeError) as e:
                logger.error(f"❌ Error parseando duracion: {e}")
                duracion_value = None

        proyecto = Proyecto(
            id=data.get('id'),
            contrato=data.get('contrato', ''),
            cliente=data.get('cliente', ''),
            fecha_inicio=fecha_inicio_value,
            fecha_termino=fecha_termino_value,
            duracion=duracion_value,
            region=data.get('region', ''),
            ciudad=data.get('ciudad', ''),
            estado=data.get('estado', 'Activo'),
            monto=float(data.get('monto', 0)),
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
            fecha_factura=fecha_factura_value,
            numero_factura=data.get('numero_factura', ''),
            numero_orden_compra=data.get('numero_orden_compra', ''),
            link_documentos=data.get('link_documentos', '')
        )

        logger.info(f"📋 Proyecto creado: {proyecto}")

        # Validar datos
        is_valid, errors = proyecto.validate()
        if not is_valid:
            logger.error(f"❌ Validación fallida: {errors}")
            return jsonify({
                'success': False,
                'error': 'Datos inválidos',
                'details': errors
            }), 400

        # Crear proyecto
        logger.info("💾 Intentando guardar proyecto en MongoDB...")
        if proyecto_controller.create_proyecto(proyecto):
            logger.info(f"✅ Proyecto creado exitosamente con ID: {proyecto.id}")
            return jsonify({
                'success': True,
                'data': proyecto.to_json_serializable(),
                'message': 'Proyecto creado exitosamente'
            }), 201
        else:
            logger.error("❌ Error al crear el proyecto en la base de datos")
            return jsonify({
                'success': False,
                'error': 'Error al crear el proyecto'
            }), 500
            
    except Exception as e:
        logger.error(f"Error creando proyecto: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/proyectos/<int:proyecto_id>', methods=['PUT'])
@admin_required
def update_proyecto(proyecto_id):
    """Actualiza un proyecto existente"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'error': 'No se proporcionaron datos'
            }), 400
        
        # Obtener proyecto existente
        proyecto = proyecto_controller.get_proyecto_by_id(proyecto_id)
        if not proyecto:
            return jsonify({
                'success': False,
                'error': 'Proyecto no encontrado'
            }), 404
        
        # Actualizar campos básicos
        proyecto.contrato = data.get('contrato', proyecto.contrato)
        proyecto.cliente = data.get('cliente', proyecto.cliente)
        proyecto.region = data.get('region', proyecto.region)
        proyecto.ciudad = data.get('ciudad', proyecto.ciudad)
        proyecto.estado = data.get('estado', proyecto.estado)
        proyecto.monto = float(data.get('monto', proyecto.monto))

        # Actualizar información del cliente
        proyecto.rut_cliente = data.get('rut_cliente', proyecto.rut_cliente)
        proyecto.tipo_cliente = data.get('tipo_cliente', proyecto.tipo_cliente)
        proyecto.persona_contacto = data.get('persona_contacto', proyecto.persona_contacto)
        proyecto.telefono_contacto = data.get('telefono_contacto', proyecto.telefono_contacto)
        proyecto.correo_contacto = data.get('correo_contacto', proyecto.correo_contacto)

        # Actualizar información técnica
        if 'superficie_terreno' in data:
            proyecto.superficie_terreno = float(data['superficie_terreno']) if data['superficie_terreno'] else None
        if 'superficie_construida' in data:
            proyecto.superficie_construida = float(data['superficie_construida']) if data['superficie_construida'] else None
        proyecto.tipo_obra_lista = data.get('tipo_obra_lista', proyecto.tipo_obra_lista)

        # Actualizar estudios y servicios
        proyecto.ems = data.get('ems', proyecto.ems)
        proyecto.estudio_sismico = data.get('estudio_sismico', proyecto.estudio_sismico)
        proyecto.estudio_geoelectrico = data.get('estudio_geoelectrico', proyecto.estudio_geoelectrico)
        proyecto.topografia = data.get('topografia', proyecto.topografia)
        proyecto.sondaje = data.get('sondaje', proyecto.sondaje)
        proyecto.hidraulica_hidrologia = data.get('hidraulica_hidrologia', proyecto.hidraulica_hidrologia)
        proyecto.descripcion = data.get('descripcion', proyecto.descripcion)
        proyecto.certificado_experiencia = data.get('certificado_experiencia', proyecto.certificado_experiencia)
        proyecto.orden_compra = data.get('orden_compra', proyecto.orden_compra)
        proyecto.contrato_doc = data.get('contrato_doc', proyecto.contrato_doc)
        proyecto.factura = data.get('factura', proyecto.factura)
        proyecto.numero_factura = data.get('numero_factura', proyecto.numero_factura)
        proyecto.numero_orden_compra = data.get('numero_orden_compra', proyecto.numero_orden_compra)
        proyecto.link_documentos = data.get('link_documentos', proyecto.link_documentos)

        # Actualizar fechas
        if data.get('fecha_inicio'):
            try:
                proyecto.fecha_inicio = datetime.fromisoformat(data.get('fecha_inicio'))
            except ValueError:
                pass

        if data.get('fecha_termino'):
            try:
                proyecto.fecha_termino = datetime.fromisoformat(data.get('fecha_termino'))
            except ValueError:
                pass
        
        # Para actualizaciones, no validamos campos obligatorios ya que estamos editando un registro existente
        # Solo validamos que los datos proporcionados sean del tipo correcto
        # La validación estricta solo se aplica en la creación
        
        # Actualizar proyecto
        if proyecto_controller.update_proyecto(proyecto):
            return jsonify({
                'success': True,
                'data': proyecto.to_json_serializable(),
                'message': 'Proyecto actualizado exitosamente'
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Error al actualizar el proyecto'
            }), 500
            
    except Exception as e:
        logger.error(f"Error actualizando proyecto {proyecto_id}: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/proyectos/<int:proyecto_id>', methods=['DELETE'])
@admin_required
def delete_proyecto(proyecto_id):
    """Elimina un proyecto"""
    try:
        if proyecto_controller.delete_proyecto(proyecto_id):
            return jsonify({
                'success': True,
                'message': 'Proyecto eliminado exitosamente'
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Proyecto no encontrado'
            }), 404

    except Exception as e:
        logger.error(f"Error eliminando proyecto {proyecto_id}: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/proyectos/bulk-delete', methods=['POST'])
@admin_required
def bulk_delete_proyectos():
    """Elimina múltiples proyectos"""
    try:
        data = request.get_json()
        ids = data.get('ids', [])

        if not ids:
            return jsonify({
                'success': False,
                'error': 'No se proporcionaron IDs'
            }), 400

        # Convertir a enteros
        ids = [int(id) for id in ids]

        if proyecto_controller.delete_records(ids):
            return jsonify({
                'success': True,
                'message': f'Eliminados {len(ids)} proyectos exitosamente'
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Error al eliminar proyectos'
            }), 500

    except Exception as e:
        logger.error(f"Error en eliminación masiva: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

def parse_boolean_value(value):
    """Convierte valores CSV a booleanos"""
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        return value.lower().strip() in ['true', '1', 'sí', 'si', 'yes', 'verdadero']
    return False

def parse_numeric_value(value, default=None):
    """Convierte valores CSV a números"""
    if not value or str(value).strip() == '' or str(value).lower() == 'null':
        return default
    try:
        if '.' in str(value):
            return float(value)
        else:
            return int(value)
    except (ValueError, TypeError):
        return default

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
        'link_documentos': 'link_documentos',

        # Variaciones alternativas (por si acaso)
        'fecha_termino': 'fecha_termino',
        'duracion': 'duracion',
        'region': 'region',
        'estudio_geoelectrico': 'estudio_geoelectrico',
        'topografia': 'topografia',
        'hidraulica_hidrologia': 'hidraulica_hidrologia',
        'descripcion': 'descripcion',
        'contrato_doc': 'contrato_doc'
    }

    # Normalizar el nombre de la columna
    normalized = column_name.lower().strip()
    return column_mapping.get(normalized, normalized)

@app.route('/api/proyectos/bulk-import', methods=['POST'])
@admin_required
def bulk_import_proyectos():
    """Importa múltiples proyectos"""
    try:
        logger.info("🚀 INICIANDO IMPORTACIÓN CSV")

        # Verificar que lleguen datos
        if not request.is_json:
            logger.error("❌ Request no es JSON")
            return jsonify({'success': False, 'error': 'Request debe ser JSON'}), 400

        data = request.get_json()
        if not data:
            logger.error("❌ No hay datos en el request")
            return jsonify({'success': False, 'error': 'No hay datos'}), 400

        proyectos_data = data.get('proyectos', [])
        logger.info(f"📥 Recibidos {len(proyectos_data)} proyectos para importar")

        if len(proyectos_data) == 0:
            logger.error("❌ Array de proyectos está vacío")
            return jsonify({'success': False, 'error': 'No hay proyectos para importar'}), 400

        # Log de columnas originales y primer registro
        if proyectos_data:
            original_columns = list(proyectos_data[0].keys())
            logger.info(f"📋 Columnas originales CSV ({len(original_columns)}): {original_columns}")
            logger.info(f"📄 Primer registro completo: {proyectos_data[0]}")

        # Normalizar nombres de columnas en cada registro
        normalized_data = []
        for item in proyectos_data:
            normalized_item = {}
            for key, value in item.items():
                normalized_key = normalize_column_name(key)
                normalized_item[normalized_key] = value
            normalized_data.append(normalized_item)

        logger.info(f"📋 Ejemplo de datos normalizados: {normalized_data[0] if normalized_data else 'N/A'}")

        if not normalized_data:
            return jsonify({
                'success': False,
                'error': 'No se proporcionaron datos de proyectos'
            }), 400

        # Crear objetos Proyecto
        proyectos = []
        for i, item in enumerate(normalized_data):
            logger.info(f"📋 Procesando proyecto {i+1}: {item}")

            # Función para parsear fechas con múltiples formatos
            def parse_date(date_str):
                if not date_str or str(date_str).strip() == '' or str(date_str).lower() == 'null':
                    return None

                date_formats = [
                    '%Y-%m-%d',      # 2014-06-10
                    '%d/%m/%Y',      # 10/06/2014
                    '%d-%m-%Y',      # 10-06-2014
                    '%m/%d/%Y',      # 06/10/2014
                    '%Y/%m/%d'       # 2014/06/10
                ]

                for fmt in date_formats:
                    try:
                        return datetime.strptime(str(date_str).strip(), fmt)
                    except ValueError:
                        continue

                logger.warning(f"⚠️ No se pudo parsear fecha: {date_str}")
                return None

            # Parsear fechas
            fecha_inicio = parse_date(item.get('fecha_inicio'))
            fecha_termino = parse_date(item.get('fecha_termino'))
            fecha_factura = parse_date(item.get('fecha_factura'))

            proyecto = Proyecto(
                id=item.get('id'),
                contrato=item.get('contrato', ''),
                cliente=item.get('cliente', ''),
                fecha_inicio=fecha_inicio,
                fecha_termino=fecha_termino,
                duracion=int(item.get('duracion')) if item.get('duracion') else None,
                region=item.get('region', ''),
                ciudad=item.get('ciudad', ''),
                estado=item.get('estado', 'Activo'),
                monto=parse_numeric_value(item.get('monto'), 0),
                # Información del cliente
                rut_cliente=item.get('rut_cliente', ''),
                tipo_cliente=item.get('tipo_cliente', ''),
                persona_contacto=item.get('persona_contacto', ''),
                telefono_contacto=item.get('telefono_contacto', ''),
                correo_contacto=item.get('correo_contacto', ''),
                # Información técnica
                superficie_terreno=parse_numeric_value(item.get('superficie_terreno')),
                superficie_construida=parse_numeric_value(item.get('superficie_construida')),
                tipo_obra_lista=item.get('tipo_obra_lista', ''),
                # Estudios y servicios
                ems=parse_boolean_value(item.get('ems', False)),
                estudio_sismico=parse_boolean_value(item.get('estudio_sismico', False)),
                estudio_geoelectrico=parse_boolean_value(item.get('estudio_geoelectrico', False)),
                topografia=parse_boolean_value(item.get('topografia', False)),
                sondaje=parse_boolean_value(item.get('sondaje', False)),
                hidraulica_hidrologia=parse_boolean_value(item.get('hidraulica_hidrologia', False)),
                descripcion=item.get('descripcion', ''),
                certificado_experiencia=parse_boolean_value(item.get('certificado_experiencia', False)),
                orden_compra=parse_boolean_value(item.get('orden_compra', False)),
                contrato_doc=parse_boolean_value(item.get('contrato_doc', False)),
                factura=parse_boolean_value(item.get('factura', False)),
                fecha_factura=fecha_factura,
                numero_factura=item.get('numero_factura', ''),
                numero_orden_compra=item.get('numero_orden_compra', ''),
                link_documentos=item.get('link_documentos', '')
            )
            logger.info(f"✅ Proyecto creado: ID={proyecto.id}, Contrato={proyecto.contrato}")
            proyectos.append(proyecto)

        # Importar proyectos
        if proyecto_controller.bulk_insert_proyectos(proyectos):
            return jsonify({
                'success': True,
                'message': f'Importados {len(proyectos)} proyectos exitosamente'
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Error al importar proyectos'
            }), 500

    except Exception as e:
        logger.error(f"Error en importación masiva: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/statistics', methods=['GET'])
@login_required
def get_statistics():
    """Obtiene estadísticas de los proyectos"""
    try:
        # Obtener tipo de usuario de la sesión
        user_type = session.get('user_type', 'admin')
        stats = proyecto_controller.get_statistics(user_type)
        return jsonify({
            'success': True,
            'data': stats
        })

    except Exception as e:
        logger.error(f"Error obteniendo estadísticas: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/status-options', methods=['GET'])
def get_status_options():
    """Obtiene las opciones de estado disponibles"""
    return jsonify({
        'success': True,
        'data': STATUS_OPTIONS
    })



# ===== MANEJO DE ERRORES =====

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'success': False,
        'error': 'Endpoint no encontrado'
    }), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        'success': False,
        'error': 'Error interno del servidor'
    }), 500

# ===== FUNCIÓN PRINCIPAL =====

def main():
    """Función principal para ejecutar el servidor"""
    try:
        logger.info("🚀 Iniciando GlaciarIng API Server...")

        # Verificar conexión a MongoDB
        connection_info = test_mongodb_connection()
        if connection_info.get("status") == "connected":
            logger.info("✅ Conexión a MongoDB Atlas verificada")
        else:
            logger.warning("⚠️ Problema con la conexión a MongoDB Atlas")

        # Iniciar servidor
        logger.info("🌐 Servidor disponible en:")
        logger.info("   📱 Frontend: http://localhost:5003")
        logger.info("   🔧 API: http://localhost:5003/api/")
        logger.info("   📊 Health Check: http://localhost:5003/api/health")

        # Abrir navegador automáticamente en ejecutables
        if getattr(sys, 'frozen', False):
            # Estamos ejecutando desde un ejecutable
            import threading
            import webbrowser
            import time

            def open_browser():
                time.sleep(2)  # Esperar a que el servidor inicie
                try:
                    webbrowser.open('http://localhost:5003')
                    logger.info("🌐 Navegador abierto automáticamente")
                except Exception as e:
                    logger.warning(f"No se pudo abrir el navegador: {e}")

            # Abrir navegador en hilo separado
            threading.Thread(target=open_browser, daemon=True).start()

        app.run(
            host='0.0.0.0',
            port=5003,
            debug=False if getattr(sys, 'frozen', False) else True,  # Sin debug en ejecutables
            use_reloader=False  # Evitar problemas con imports
        )

    except Exception as e:
        logger.error(f"❌ Error iniciando servidor: {e}")

if __name__ == "__main__":
    main()
