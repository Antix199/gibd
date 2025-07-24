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

        proyecto = Proyecto(
            id=data.get('id'),
            contrato=data.get('contrato', ''),
            cliente=data.get('cliente', ''),
            fecha_inicio=fecha_inicio_value,
            fecha_termino=fecha_termino_value,
            region=data.get('region', ''),
            ciudad=data.get('ciudad', ''),
            estado=data.get('estado', 'Activo'),
            monto=float(data.get('monto', 0))
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
        
        # Actualizar campos
        proyecto.contrato = data.get('contrato', proyecto.contrato)
        proyecto.cliente = data.get('cliente', proyecto.cliente)
        proyecto.region = data.get('region', proyecto.region)
        proyecto.ciudad = data.get('ciudad', proyecto.ciudad)
        proyecto.estado = data.get('estado', proyecto.estado)
        proyecto.monto = float(data.get('monto', proyecto.monto))

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
        
        # Validar datos
        is_valid, errors = proyecto.validate()
        if not is_valid:
            return jsonify({
                'success': False,
                'error': 'Datos inválidos',
                'details': errors
            }), 400
        
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

@app.route('/api/proyectos/bulk-import', methods=['POST'])
@admin_required
def bulk_import_proyectos():
    """Importa múltiples proyectos"""
    try:
        data = request.get_json()
        proyectos_data = data.get('proyectos', [])

        logger.info(f"📥 Recibidos {len(proyectos_data)} proyectos para importar")

        if not proyectos_data:
            return jsonify({
                'success': False,
                'error': 'No se proporcionaron datos de proyectos'
            }), 400

        # Crear objetos Proyecto
        proyectos = []
        for i, item in enumerate(proyectos_data):
            logger.info(f"📋 Procesando proyecto {i+1}: {item}")

            # Parsear fecha de inicio
            fecha_inicio_str = item.get('fecha_inicio')
            if fecha_inicio_str and fecha_inicio_str.strip() and fecha_inicio_str.lower() != 'null':
                try:
                    fecha_inicio = datetime.fromisoformat(fecha_inicio_str)
                    logger.info(f"✅ Fecha inicio parseada: {fecha_inicio_str} → {fecha_inicio}")
                except ValueError as e:
                    logger.warning(f"⚠️ Error parseando fecha_inicio '{fecha_inicio_str}': {e}, usando None")
                    fecha_inicio = None
            else:
                fecha_inicio = None

            # Parsear fecha de término
            fecha_termino_str = item.get('fecha_termino')
            if fecha_termino_str:
                try:
                    fecha_termino = datetime.fromisoformat(fecha_termino_str)
                    logger.info(f"✅ Fecha término parseada: {fecha_termino_str} → {fecha_termino}")
                except ValueError as e:
                    logger.warning(f"⚠️ Error parseando fecha_termino '{fecha_termino_str}': {e}, usando None")
                    fecha_termino = None
            else:
                fecha_termino = None

            proyecto = Proyecto(
                id=item.get('id'),
                contrato=item.get('contrato', ''),
                cliente=item.get('cliente', ''),
                fecha_inicio=fecha_inicio,
                fecha_termino=fecha_termino,
                region=item.get('region', ''),
                ciudad=item.get('ciudad', ''),
                estado=item.get('estado', 'Activo'),
                monto=float(item.get('monto', 0))
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
        logger.info("   📱 Frontend: http://localhost:5000")
        logger.info("   🔧 API: http://localhost:5000/api/")
        logger.info("   📊 Health Check: http://localhost:5000/api/health")

        app.run(
            host='0.0.0.0',
            port=5000,
            debug=True,
            use_reloader=False  # Evitar problemas con imports
        )

    except Exception as e:
        logger.error(f"❌ Error iniciando servidor: {e}")

if __name__ == "__main__":
    main()
