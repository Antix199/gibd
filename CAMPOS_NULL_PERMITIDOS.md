# ✅ Campos NULL Permitidos - Duración y Fecha Factura

## 🎯 Cambio Realizado
Se ha configurado el sistema para permitir que los campos `duracion` y `fecha_factura` sean **NULL** (opcionales) en toda la aplicación.

## ✅ Modificaciones Implementadas

### 1. **Servidor API** (`api_server.py`)

#### Parsing Mejorado:
```python
# Parsear duración - permite NULL
duracion_value = None
if data.get('duracion') and str(data.get('duracion')).strip() and str(data.get('duracion')).lower() != 'null':
    try:
        duracion_value = int(data.get('duracion'))
    except (ValueError, TypeError):
        duracion_value = None

# Parsear fecha_factura - permite NULL
fecha_factura_value = None
if data.get('fecha_factura') and str(data.get('fecha_factura')).strip() and str(data.get('fecha_factura')).lower() != 'null':
    try:
        fecha_factura_value = datetime.fromisoformat(data.get('fecha_factura'))
    except ValueError:
        fecha_factura_value = None
```

### 2. **Formularios HTML** (`modify-database.html`)

#### Etiquetas Actualizadas:
- ✅ **Duración**: "Duración (meses) *(opcional)*"
- ✅ **Fecha Factura**: "Fecha de Factura *(opcional)*"
- ✅ **Placeholders**: "Duración en meses (opcional)"

#### Formularios Afectados:
- ✅ Formulario de agregar proyecto
- ✅ Formulario de editar proyecto
- ✅ Documentación CSV actualizada

### 3. **JavaScript** (`modify-database.js`)

#### Validación Mejorada:
```javascript
// Agregar proyecto - permite NULL
duracion: (data.recordDuracion && data.recordDuracion.trim() !== '') ? parseInt(data.recordDuracion) : null,
fecha_factura: (data.recordFechaFactura && data.recordFechaFactura.trim() !== '') ? data.recordFechaFactura : null,

// Editar proyecto - permite NULL
duracion: document.getElementById('editDuracion').value ? parseInt(document.getElementById('editDuracion').value) : null,
fecha_factura: document.getElementById('editFechaFactura').value || null,
```

#### Función `parseNumeric` Mejorada:
```javascript
parseNumeric(numericString) {
    if (!numericString || 
        numericString.toString().trim() === '' || 
        numericString.toString().toLowerCase() === 'null' ||
        numericString.toString().toLowerCase() === 'undefined') {
        return null;
    }
    // ... resto de la lógica
}
```

### 4. **Visualización** (`main.js` y `modify-database.js`)

#### Mostrar Valores NULL:
```javascript
// En lugar de 'N/A', mostrar '-' para valores NULL
${project.duracion !== null && project.duracion !== undefined ? project.duracion : '-'}
${record.fecha_factura ? formatDate(record.fecha_factura) : '-'}
```

## 📊 **Comportamiento Actualizado**

### ✅ **Valores Aceptados como NULL:**
- Campo vacío: `""`
- Valor NULL: `"null"` (case-insensitive)
- Valor undefined: `"undefined"`
- Solo espacios: `"   "`

### ✅ **Visualización:**
- **Valores NULL**: Se muestran como `-`
- **Valores válidos**: Se muestran normalmente
- **Formularios**: Campos vacíos son válidos

### ✅ **CSV Import:**
- **Campos vacíos**: Se interpretan como NULL
- **"NULL"**: Se interpreta como NULL
- **Valores válidos**: Se procesan normalmente

## 🧪 **Ejemplos de Uso**

### CSV Válido con NULLs:
```csv
Id,Contrato,Cliente,fecha_inicio,fecha_término,duración,Región,Ciudad,Estado,Monto,Factura,fecha_factura,Numero_factura
1000,Proyecto A,Cliente A,10/06/2014,30/06/2014,,La Araucanía,Temuco,Completado,700000,FALSE,,
1001,Proyecto B,Cliente B,16/09/2014,15/10/2014,2,Coquimbo,Coquimbo,Completado,2000000,TRUE,15/11/2014,F-001
```

### Formulario:
- **Duración**: Campo vacío = NULL ✅
- **Fecha Factura**: Sin seleccionar = NULL ✅
- **Ambos con valores**: Funciona normal ✅

## 🔍 **Validaciones**

### ✅ **Backend (Python):**
- Acepta `None` para ambos campos
- Valida tipos cuando hay valores
- Maneja errores de parsing gracefully

### ✅ **Frontend (JavaScript):**
- Campos opcionales en formularios
- Validación flexible de entrada
- Visualización consistente de NULLs

### ✅ **Base de Datos:**
- Campos definidos como `Optional[int]` y `Optional[datetime]`
- Permite almacenar NULL sin errores

## 🎉 **Resultado Final**

Los campos `duracion` y `fecha_factura` ahora son completamente opcionales:

- ✅ **Formularios**: No requieren valores
- ✅ **CSV**: Acepta campos vacíos
- ✅ **API**: Maneja NULL correctamente
- ✅ **Visualización**: Muestra `-` para valores NULL
- ✅ **Filtros**: Funcionan con valores NULL
- ✅ **Exportación**: Incluye valores NULL apropiadamente

**Los usuarios pueden dejar estos campos vacíos sin problemas.**
