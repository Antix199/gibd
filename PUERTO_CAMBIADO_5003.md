# 🔌 Puerto Cambiado a 5003

## 🎯 Cambio Realizado
Se ha cambiado el puerto de la aplicación del **5000** al **5003** para evitar conflictos con otros servicios.

## ✅ Archivos Modificados

### 1. **`api_server.py`** - Servidor Principal

#### Puerto del Servidor:
```python
# ANTES
app.run(
    host='0.0.0.0',
    port=5000,
    debug=True,
    use_reloader=False
)

# AHORA
app.run(
    host='0.0.0.0',
    port=5003,
    debug=True,
    use_reloader=False
)
```

#### Logs de Inicio:
```python
# ANTES
logger.info("   📱 Frontend: http://localhost:5000")
logger.info("   🔧 API: http://localhost:5000/api/")
logger.info("   📊 Health Check: http://localhost:5000/api/health")

# AHORA
logger.info("   📱 Frontend: http://localhost:5003")
logger.info("   🔧 API: http://localhost:5003/api/")
logger.info("   📊 Health Check: http://localhost:5003/api/health")
```

### 2. **`start_server.bat`** - Script de Windows

#### URLs de Información:
```batch
# ANTES
echo Frontend disponible en: http://localhost:5000
echo API disponible en: http://localhost:5000/api/

# AHORA
echo Frontend disponible en: http://localhost:5003
echo API disponible en: http://localhost:5003/api/
```

### 3. **`PROTOTYPE_README.md`** - Documentación

#### URL de Acceso:
```markdown
# ANTES
# Abrir navegador en: http://localhost:5000

# AHORA
# Abrir navegador en: http://localhost:5003
```

## 🌐 **Nuevas URLs de Acceso**

### ✅ **Frontend (Interfaz Principal):**
- **URL**: `http://localhost:5003`
- **Páginas**:
  - Principal: `http://localhost:5003/`
  - Lectura: `http://localhost:5003/reader.html`
  - Modificar: `http://localhost:5003/modify-database.html`

### ✅ **API (Backend):**
- **Base**: `http://localhost:5003/api/`
- **Endpoints**:
  - Health: `http://localhost:5003/api/health`
  - Proyectos: `http://localhost:5003/api/proyectos`
  - Import: `http://localhost:5003/api/proyectos/bulk-import`

## 🔧 **Impacto del Cambio**

### ✅ **Lo que CAMBIÓ:**
- **Puerto del servidor**: 5000 → 5003
- **URLs de acceso**: Todas ahora usan :5003
- **Logs de inicio**: Muestran puerto 5003
- **Documentación**: Actualizada con nuevo puerto

### ✅ **Lo que NO cambió:**
- **Funcionalidad**: Todo funciona igual
- **JavaScript**: Usa rutas relativas (no afectado)
- **Base de datos**: Sin cambios
- **Archivos estáticos**: Sin cambios

## 🚀 **Cómo Usar**

### **Desarrollo Local:**
```bash
# Ejecutar servidor
python api_server.py

# Abrir navegador en:
http://localhost:5003
```

### **Windows (Ejecutable):**
```cmd
# Ejecutar GIBD.exe
# Se abrirá automáticamente en:
http://localhost:5003
```

### **Mac/Linux (Ejecutable):**
```bash
# Ejecutar GIBD
./GIBD

# Abrir navegador en:
http://localhost:5003
```

## ⚠️ **Consideraciones**

### **Firewall:**
- Asegúrate de que el puerto **5003** esté permitido
- Windows Defender puede preguntar sobre el nuevo puerto

### **Conflictos de Puerto:**
- Si el puerto 5003 está ocupado, verás un error
- Usar `netstat -ano | findstr :5003` (Windows) para verificar

### **Marcadores/Bookmarks:**
- Actualizar marcadores del navegador al nuevo puerto
- Cambiar de `:5000` a `:5003`

## 🧪 **Pruebas**

### **Verificar que Funciona:**
1. **Ejecutar** la aplicación
2. **Abrir** `http://localhost:5003`
3. **Verificar** que carga correctamente
4. **Probar** todas las funcionalidades

### **Verificar APIs:**
```bash
# Health check
curl http://localhost:5003/api/health

# Listar proyectos
curl http://localhost:5003/api/proyectos
```

## 💡 **Razones del Cambio**

### ✅ **Evitar Conflictos:**
- Puerto 5000 es común para otros servicios
- Flask development server por defecto
- Algunos servicios de sistema usan 5000

### ✅ **Mejor Experiencia:**
- Puerto dedicado para GIBD
- Menos probabilidad de conflictos
- Más estable en diferentes entornos

## 🔄 **Migración**

### **Para Usuarios Existentes:**
1. **Cerrar** aplicación actual
2. **Actualizar** a nueva versión
3. **Abrir** nueva URL: `http://localhost:5003`
4. **Actualizar** marcadores si es necesario

### **Para Desarrolladores:**
1. **Pull** últimos cambios
2. **Ejecutar** `python api_server.py`
3. **Verificar** logs muestran puerto 5003
4. **Actualizar** scripts/documentación local

## 🎉 **Resultado Final**

GIBD ahora funciona en el puerto **5003**:

- ✅ **Menos conflictos** con otros servicios
- ✅ **Puerto dedicado** para la aplicación
- ✅ **Misma funcionalidad** en nuevo puerto
- ✅ **Documentación actualizada**

**¡La aplicación ahora usa el puerto 5003 como solicitaste! 🔌✨**
