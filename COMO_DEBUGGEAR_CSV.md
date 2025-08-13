# 🔍 Cómo Debuggear la Importación CSV

## 😭 No te preocupes, vamos a solucionarlo paso a paso

### 🛠️ Scripts de Debugging Creados

He creado varios scripts para encontrar exactamente dónde está el problema:

#### 1. **`debug_complete_flow.py`** - ⭐ EMPEZAR AQUÍ
```bash
python debug_complete_flow.py
```
**Qué hace:**
- Simula TODO el proceso (frontend + backend)
- Te dice exactamente en qué paso falla
- Guarda los datos procesados para inspección

#### 2. **`test_mapeo.py`** - Verificar Mapeo
```bash
python test_mapeo.py
```
**Qué hace:**
- Verifica que todos los 33 campos estén mapeados
- Prueba caracteres especiales (acentos, /)
- Te dice si falta algún campo

#### 3. **`test_import_direct.py`** - Prueba Directa
```bash
python test_import_direct.py
```
**Qué hace:**
- Envía datos directamente al servidor
- Prueba con un registro simple primero
- Luego prueba con el CSV completo

#### 4. **`debug_frontend_csv.py`** - Simular Frontend
```bash
python debug_frontend_csv.py
```
**Qué hace:**
- Simula cómo el frontend procesa el CSV
- Compara diferentes métodos de lectura
- Guarda datos procesados en JSON

## 🚀 Plan de Debugging

### Paso 1: Verificar que el servidor esté ejecutándose
```bash
# En una terminal
python api_server.py
```

### Paso 2: Ejecutar el debug completo
```bash
# En otra terminal
python debug_complete_flow.py
```

### Paso 3: Revisar los resultados

El script te dirá exactamente dónde está el problema:

#### ✅ **Si funciona:**
```
🎉 ¡FLUJO COMPLETO EXITOSO!
```

#### ❌ **Si falla en Paso 1 (Lectura CSV):**
- Problema con el archivo `test_data.csv`
- Encoding incorrecto
- Formato CSV malformado

#### ❌ **Si falla en Paso 2 (Procesamiento):**
- Problema con el mapeo de campos
- Campos faltantes o mal nombrados
- Validación muy estricta

#### ❌ **Si falla en Paso 3 (Servidor):**
- Servidor no ejecutándose
- Error en el backend
- Problema de mapeo en el servidor

## 🔍 Archivos de Debug Generados

Después de ejecutar los scripts, tendrás estos archivos para inspeccionar:

1. **`debug_proyectos_procesados.json`** - Datos como los ve el frontend
2. **`frontend_processed_data.json`** - Datos procesados por simulación frontend
3. **Logs del servidor** - En la consola donde ejecutas `api_server.py`

## 🧪 Casos de Prueba

### Caso 1: Registro Simple
```python
# Un registro mínimo para probar
{
    'Id': '9999',
    'Contrato': 'Proyecto Test',
    'Cliente': 'Cliente Test',
    'Región': 'Metropolitana',
    'Ciudad': 'Santiago',
    'Estado': 'Activo'
}
```

### Caso 2: CSV Completo
- Usa el archivo `test_data.csv` con todos los 33 campos

## 🔧 Posibles Problemas y Soluciones

### Problema 1: "0 proyectos importados"
**Posibles causas:**
- Mapeo de campos incorrecto
- Validación muy estricta
- Campos requeridos vacíos

**Solución:**
```bash
python debug_complete_flow.py
# Revisa qué proyectos se rechazan y por qué
```

### Problema 2: Error de conexión
**Causa:** Servidor no ejecutándose
**Solución:**
```bash
python api_server.py
```

### Problema 3: Error de encoding
**Causa:** Archivo CSV con encoding incorrecto
**Solución:**
- Guardar CSV como UTF-8
- Verificar caracteres especiales

### Problema 4: Campos faltantes
**Causa:** Nombres de columnas no coinciden
**Solución:**
```bash
python test_mapeo.py
# Te dice exactamente qué campos faltan
```

## 📋 Checklist de Debugging

- [ ] ✅ Servidor ejecutándose (`python api_server.py`)
- [ ] ✅ Archivo `test_data.csv` existe
- [ ] ✅ CSV tiene 33 columnas exactas
- [ ] ✅ Ejecutar `python debug_complete_flow.py`
- [ ] ✅ Revisar logs del servidor
- [ ] ✅ Revisar archivos JSON generados
- [ ] ✅ Identificar en qué paso falla

## 🆘 Si Nada Funciona

1. **Copia y pega** los logs completos del servidor
2. **Copia y pega** la salida de `debug_complete_flow.py`
3. **Comparte** el archivo `debug_proyectos_procesados.json`

Con esa información podremos identificar exactamente el problema.

## 🎯 Objetivo

Al final de este proceso sabremos:
- ✅ Si el CSV se lee correctamente
- ✅ Si el mapeo de campos funciona
- ✅ Si el servidor recibe los datos
- ✅ Si el servidor procesa los datos
- ✅ Dónde exactamente está el problema

**¡No te rindas! Vamos a solucionarlo juntos! 💪**
