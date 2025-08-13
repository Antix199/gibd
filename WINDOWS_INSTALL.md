# 🪟 GIBD para Windows

## 📦 Instalación

### Requisitos del Sistema
- **Windows 10** o superior (64-bit)
- **4 GB RAM** mínimo (8 GB recomendado)
- **500 MB** de espacio libre en disco
- **Conexión a Internet** (para funcionalidades web)

### Pasos de Instalación

1. **Descargar el Ejecutable**
   - Ve a la página de [Releases](https://github.com/tu-usuario/glaciaring/releases)
   - Descarga `GIBD-windows.zip`

2. **Extraer el Archivo**
   - Haz clic derecho en `GIBD-windows.zip`
   - Selecciona "Extraer todo..."
   - Elige una carpeta de destino (ej: `C:\GIBD\`)

3. **Ejecutar la Aplicación**
   - Navega a la carpeta extraída
   - Doble clic en `GIBD.exe`

## 🛡️ Seguridad de Windows

### Windows Defender
Si Windows Defender bloquea la aplicación:

1. **Permitir en Windows Defender**:
   - Clic en "Más información"
   - Clic en "Ejecutar de todas formas"

2. **Agregar Excepción** (recomendado):
   - Abrir Windows Security
   - Ir a "Protección contra virus y amenazas"
   - Clic en "Administrar configuración" bajo "Configuración de protección contra virus y amenazas"
   - Clic en "Agregar o quitar exclusiones"
   - Agregar la carpeta de GIBD

### SmartScreen
Si aparece SmartScreen:
1. Clic en "Más información"
2. Clic en "Ejecutar de todas formas"

## 🚀 Uso

### Primera Ejecución
1. **Ejecutar como Administrador** (recomendado):
   - Clic derecho en `GIBD.exe`
   - Seleccionar "Ejecutar como administrador"

2. **Configuración Inicial**:
   - La aplicación se abrirá en tu navegador predeterminado
   - URL: `http://localhost:5000`

### Uso Normal
- Doble clic en `GIBD.exe`
- Esperar a que aparezca la ventana del navegador
- ¡Listo para usar!

## 🔧 Solución de Problemas

### Problema: "No se puede ejecutar"
**Solución**:
- Verificar que tienes permisos de administrador
- Desactivar temporalmente el antivirus
- Ejecutar desde una carpeta sin espacios en el nombre

### Problema: "Puerto 5000 ocupado"
**Solución**:
- Cerrar otras aplicaciones que usen el puerto 5000
- Reiniciar el equipo
- Ejecutar `netstat -ano | findstr :5000` para ver qué proceso usa el puerto

### Problema: "No abre el navegador"
**Solución**:
- Abrir manualmente: `http://localhost:5000`
- Verificar que el firewall no bloquee la aplicación
- Probar con otro navegador

### Problema: "Error de base de datos"
**Solución**:
- Verificar permisos de escritura en la carpeta
- Ejecutar como administrador
- Verificar que no hay archivos bloqueados

## 📁 Estructura de Archivos

```
GIBD/
├── GIBD.exe                # Ejecutable principal
├── _internal/              # Archivos internos de Python
├── assets/                 # Recursos web (CSS, JS, imágenes)
├── models/                 # Modelos de datos
├── controllers/            # Lógica de negocio
├── templates/              # Plantillas HTML
└── database/               # Base de datos SQLite
```

## 🔄 Actualización

### Método Manual
1. Descargar nueva versión
2. Cerrar GIBD actual
3. Reemplazar archivos
4. Ejecutar nueva versión

### Respaldo de Datos
**Importante**: Antes de actualizar, respalda:
- `database/proyectos.db` - Base de datos principal
- Cualquier archivo CSV personalizado

## 🆘 Soporte

### Logs de Error
Los logs se guardan en:
- **Consola**: Visible al ejecutar desde cmd
- **Archivos**: En la carpeta de la aplicación

### Reportar Problemas
1. **Información del Sistema**:
   - Versión de Windows
   - Versión de GlaciarIng
   - Mensaje de error completo

   - Versión de GIBD
   - Mensaje de error completo

2. **Pasos para Reproducir**:
   - Qué estabas haciendo
   - Qué esperabas que pasara
   - Qué pasó en realidad

3. **Enviar Reporte**:
   - GitHub Issues
   - Email de soporte
   - Incluir logs si es posible

## 💡 Consejos

### Rendimiento
- **Cerrar otras aplicaciones** pesadas mientras usas GIBD
- **Usar SSD** para mejor rendimiento de base de datos
- **8 GB RAM** o más para proyectos grandes

### Seguridad
- **Respaldar datos** regularmente
- **No ejecutar** desde carpetas temporales
- **Mantener Windows actualizado**

### Productividad
- **Crear acceso directo** en el escritorio
- **Anclar a la barra de tareas**
- **Usar navegador moderno** (Chrome, Firefox, Edge)

## 🎉 ¡Listo!

GIBD está ahora instalado y listo para usar en Windows.

**¿Necesitas ayuda?** Consulta la documentación completa o contacta soporte.
