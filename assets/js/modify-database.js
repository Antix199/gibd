/**
 * Modify Database Page JavaScript
 * Handles the database modification functionality
 */

class ModifyDatabasePage {
    constructor() {
        this.selectedRecords = [];
        this.currentEditId = null;
        
        this.init();
    }

    init() {
        this.setupEventListeners();
        this.setupFileUpload();
        this.setupModal();
        this.setupCheckboxSelection();
        this.loadExistingRecords();
    }

    setupEventListeners() {
        // Navigation
        const backToMainBtn = document.getElementById('backToMainBtn');
        if (backToMainBtn) {
            backToMainBtn.addEventListener('click', () => {
                window.location.href = 'index.html';
            });
        }

        // Add record form
        UIComponents.handleFormSubmit('addRecordForm', 
            (data) => this.addRecord(data),
            (errors) => UIComponents.showNotification(errors.join('\n'), 'error')
        );

        // Action buttons
        const deleteSelectedBtn = document.getElementById('deleteSelectedBtn');
        const editSelectedBtn = document.getElementById('editSelectedBtn');

        if (deleteSelectedBtn) {
            deleteSelectedBtn.addEventListener('click', () => this.deleteSelected());
        }

        if (editSelectedBtn) {
            editSelectedBtn.addEventListener('click', () => this.editSelected());
        }

        // Edit form
        const saveEditBtn = document.getElementById('saveEditBtn');
        if (saveEditBtn) {
            saveEditBtn.addEventListener('click', () => this.saveEdit());
        }



        // Set default date to today (solo para entrada manual)
        const recordFechaInicio = document.getElementById('recordFechaInicio');
        if (recordFechaInicio && !recordFechaInicio.value) {
            recordFechaInicio.value = new Date().toISOString().split('T')[0];
            console.log('Fecha por defecto establecida para entrada manual');
        }
    }

    setupFileUpload() {
        UIComponents.setupFileUpload('fileInput', 
            (file) => this.handleFileSelect(file),
            (file) => this.uploadFile(file)
        );
    }

    setupModal() {
        UIComponents.setupModal('editModal', [], ['closeEditModal', 'cancelEditBtn']);
    }

    setupCheckboxSelection() {
        UIComponents.setupCheckboxSelection('manageTable', (selectedIds) => {
            this.selectedRecords = selectedIds;
            this.updateActionButtons();
        });
    }

    updateActionButtons() {
        const deleteBtn = document.getElementById('deleteSelectedBtn');
        const editBtn = document.getElementById('editSelectedBtn');

        if (deleteBtn) {
            deleteBtn.disabled = this.selectedRecords.length === 0;
        }

        if (editBtn) {
            editBtn.disabled = this.selectedRecords.length !== 1;
        }
    }

    async addRecord(data) {
        try {
            // Debug: mostrar datos recibidos
            console.log('Datos del formulario:', data);

            // Validate data
            const errors = validateRecord(data);
            console.log('Errores de validación:', errors);

            if (errors.length > 0) {
                throw new Error(errors.join('\n'));
            }

            // Add record
            const newRecord = await dataManager.addRecord({
                id: data.recordId ? parseInt(data.recordId) : null,
                contrato: data.recordContrato,
                cliente: data.recordCliente,
                fecha_inicio: data.recordFechaInicio,
                fecha_termino: data.recordFechaTermino || null,
                region: data.recordRegion,
                ciudad: data.recordCiudad,
                estado: data.recordEstado,
                monto: parseFloat(data.recordMonto) || 0
            });

            // Refresh table
            await this.loadExistingRecords();

            UIComponents.showNotification('Record added successfully!', 'success');

        } catch (error) {
            throw error;
        }
    }

    handleFileSelect(file) {
        console.log('Archivo seleccionado:', file.name);

        // Validar que sea un archivo CSV
        if (!file.name.toLowerCase().endsWith('.csv')) {
            UIComponents.showNotification('Por favor selecciona un archivo CSV (.csv)', 'error');
            return false;
        }

        // Validar tamaño del archivo (máximo 5MB)
        if (file.size > 5 * 1024 * 1024) {
            UIComponents.showNotification('El archivo es demasiado grande. Máximo 5MB permitido.', 'error');
            return false;
        }

        console.log(`Archivo CSV válido: ${file.name} (${(file.size / 1024).toFixed(1)} KB)`);
        return true;
    }

    async uploadFile(file) {
        try {
            UIComponents.showLoading('Procesando archivo CSV...');

            // Validar que sea un archivo CSV
            if (!file.name.toLowerCase().endsWith('.csv')) {
                throw new Error('Por favor selecciona un archivo CSV válido');
            }

            // Leer el contenido del archivo
            const fileContent = await this.readFileContent(file);

            // Parsear el CSV
            const csvData = this.parseCSV(fileContent);

            if (csvData.length === 0) {
                throw new Error('El archivo CSV está vacío o no tiene datos válidos');
            }

            // Convertir datos CSV a formato de proyecto
            const proyectos = this.convertCSVToProjects(csvData);

            if (proyectos.length === 0) {
                throw new Error('No se encontraron proyectos válidos en el archivo CSV');
            }

            // Importar los datos
            const importedCount = await dataManager.importData(proyectos);

            // Refresh table
            await this.loadExistingRecords();

            // Reset file input
            const fileInput = document.getElementById('fileInput');
            const fileInfo = document.getElementById('fileInfo');
            const uploadBtn = document.getElementById('uploadBtn');

            if (fileInput) fileInput.value = '';
            if (fileInfo) fileInfo.textContent = 'Ningún archivo seleccionado';
            if (uploadBtn) uploadBtn.disabled = true;

            // Limpiar formulario para evitar interferencias
            this.clearForm();

            UIComponents.hideLoading();
            UIComponents.showNotification(`¡Importados ${importedCount} proyectos exitosamente!`, 'success');

        } catch (error) {
            UIComponents.hideLoading();
            UIComponents.showNotification('Error procesando archivo: ' + error.message, 'error');
        }
    }

    async readFileContent(file) {
        // Lee el contenido del archivo como texto
        return new Promise((resolve, reject) => {
            const reader = new FileReader();
            reader.onload = (e) => resolve(e.target.result);
            reader.onerror = () => reject(new Error('Error leyendo el archivo'));
            reader.readAsText(file, 'UTF-8');
        });
    }

    parseCSV(csvContent) {
        // Parsea el contenido CSV en un array de objetos
        console.log('Contenido CSV a parsear:', csvContent.substring(0, 200) + '...');

        const lines = csvContent.split('\n').filter(line => line.trim() !== '');
        console.log(`Líneas encontradas: ${lines.length}`);

        if (lines.length < 2) {
            throw new Error('El archivo CSV debe tener al menos una línea de encabezados y una línea de datos');
        }

        // Obtener headers (primera línea)
        const headers = lines[0].split(',').map(header => header.trim().replace(/"/g, ''));
        console.log('Headers encontrados:', headers);

        // Parsear datos (resto de líneas)
        const data = [];
        for (let i = 1; i < lines.length; i++) {
            const line = lines[i].trim();
            if (!line) continue; // Saltar líneas vacías

            const values = this.parseCSVLine(line);
            console.log(`Línea ${i}: "${line}" → ${values.length} valores, esperados: ${headers.length}`);

            // Ser más flexible con el número de columnas
            if (values.length >= headers.length - 2) { // Permitir algunas columnas faltantes
                const row = {};
                headers.forEach((header, index) => {
                    row[header] = values[index] || ''; // Usar string vacío si falta el valor
                });
                data.push(row);
                console.log(`Fila ${i} parseada:`, row);
            } else {
                console.warn(`Línea ${i} ignorada - muy pocas columnas: ${values.length} < ${headers.length - 2}`);
            }
        }

        console.log(`Datos parseados: ${data.length} filas`);
        return data;
    }

    parseCSVLine(line) {
        // Parsea una línea CSV manejando comillas y comas dentro de campos
        const result = [];
        let current = '';
        let inQuotes = false;

        for (let i = 0; i < line.length; i++) {
            const char = line[i];

            if (char === '"') {
                inQuotes = !inQuotes;
            } else if (char === ',' && !inQuotes) {
                // Limpiar comillas del inicio y final del campo
                let cleanValue = current.trim();
                if (cleanValue.startsWith('"') && cleanValue.endsWith('"')) {
                    cleanValue = cleanValue.slice(1, -1);
                }
                result.push(cleanValue);
                current = '';
            } else {
                current += char;
            }
        }

        // Procesar el último campo
        let cleanValue = current.trim();
        if (cleanValue.startsWith('"') && cleanValue.endsWith('"')) {
            cleanValue = cleanValue.slice(1, -1);
        }
        result.push(cleanValue);

        console.log('Línea parseada:', line, '→', result);
        return result;
    }

    convertCSVToProjects(csvData) {
        // Convierte los datos CSV al formato de proyecto
        console.log('Datos CSV recibidos:', csvData);
        const proyectos = [];

        for (const row of csvData) {
            try {
                console.log('Procesando fila:', row);

                // Mapear campos CSV a campos de proyecto
                // Soportar diferentes variaciones de nombres de columnas
                const idValue = this.getCSVValue(row, ['id', 'ID', 'Id']);

                // Obtener valores de fecha antes de parsear
                const fechaInicioRaw = this.getCSVValue(row, ['fecha_inicio', 'Fecha_Inicio', 'fecha inicio', 'start_date', 'Start Date']);
                const fechaTerminoRaw = this.getCSVValue(row, ['fecha_termino', 'fecha_término', 'Fecha_Termino', 'Fecha_Término', 'fecha termino', 'end_date', 'End Date']);

                console.log(`Proyecto ID ${idValue}: fecha_inicio raw = "${fechaInicioRaw}", fecha_termino raw = "${fechaTerminoRaw}"`);

                const proyecto = {
                    id: idValue ? parseInt(idValue) : null,
                    contrato: this.getCSVValue(row, ['contrato', 'Contrato', 'contract', 'Contract']),
                    cliente: this.getCSVValue(row, ['cliente', 'Cliente', 'client', 'Client']),
                    fecha_inicio: this.parseDate(fechaInicioRaw),
                    fecha_termino: this.parseDate(fechaTerminoRaw),
                    region: this.getCSVValue(row, ['region', 'Region', 'región', 'Región']),
                    ciudad: this.getCSVValue(row, ['ciudad', 'Ciudad', 'city', 'City']),
                    estado: this.mapEstado(this.getCSVValue(row, ['estado', 'Estado', 'status', 'Status'])),
                    monto: this.parseMonto(this.getCSVValue(row, ['monto', 'Monto', 'amount', 'Amount'])),
                    // Información del cliente
                    rut_cliente: this.getCSVValue(row, ['RUT_cliente', 'rut_cliente', 'RUT Cliente', 'RUT']),
                    tipo_cliente: this.getCSVValue(row, ['Tipo_cliente', 'tipo_cliente', 'Tipo Cliente', 'Tipo']),
                    persona_contacto: this.getCSVValue(row, ['Persona_contacto', 'persona_contacto', 'Persona Contacto', 'Contacto']),
                    telefono_contacto: this.getCSVValue(row, ['Telefono_contacto', 'telefono_contacto', 'Teléfono Contacto', 'Teléfono']),
                    correo_contacto: this.getCSVValue(row, ['Correo_contacto', 'correo_contacto', 'Correo Contacto', 'Email']),
                    // Información técnica
                    superficie_terreno: this.parseFloat(this.getCSVValue(row, ['Superficie_terreno', 'superficie_terreno', 'Superficie Terreno'])),
                    superficie_construida: this.parseFloat(this.getCSVValue(row, ['Superficie_construida', 'superficie_construida', 'Superficie Construida'])),
                    tipo_obra_lista: this.getCSVValue(row, ['Tipo_obra_lista', 'tipo_obra_lista', 'Tipo Obra Lista', 'Tipo Obra']),
                    // Estudios y servicios
                    ems: this.parseBoolean(this.getCSVValue(row, ['EMS', 'ems'])),
                    estudio_sismico: this.parseBoolean(this.getCSVValue(row, ['Estudio_sismico', 'estudio_sismico', 'Estudio Sísmico'])),
                    estudio_geoelectrico: this.parseBoolean(this.getCSVValue(row, ['Estudio_Geoeléctrico', 'estudio_geoelectrico', 'Estudio Geoeléctrico'])),
                    topografia: this.parseBoolean(this.getCSVValue(row, ['Topografía', 'topografia', 'Topografia'])),
                    sondaje: this.parseBoolean(this.getCSVValue(row, ['Sondaje', 'sondaje'])),
                    hidraulica_hidrologia: this.parseBoolean(this.getCSVValue(row, ['Hidráulica/Hidrología', 'hidraulica_hidrologia', 'Hidráulica', 'Hidrología'])),
                    descripcion: this.getCSVValue(row, ['Descripción', 'descripcion', 'Descripcion']),
                    certificado_experiencia: this.parseBoolean(this.getCSVValue(row, ['Certificado_experiencia', 'certificado_experiencia', 'Certificado Experiencia'])),
                    orden_compra: this.parseBoolean(this.getCSVValue(row, ['Orden_compra', 'orden_compra', 'Orden Compra'])),
                    contrato_doc: this.parseBoolean(this.getCSVValue(row, ['Contrato_existe', 'contrato_existe', 'Contrato Existe', 'Contrato'])),
                    factura: this.parseBoolean(this.getCSVValue(row, ['Factura', 'factura'])),
                    numero_factura: this.getCSVValue(row, ['Numero_factura', 'numero_factura', 'Número Factura']),
                    numero_orden_compra: this.getCSVValue(row, ['Numero_orden_compra', 'numero_orden_compra', 'Número Orden Compra'])
                };

                console.log(`Proyecto ID ${idValue}: fecha_inicio parseada = "${proyecto.fecha_inicio}", fecha_termino parseada = "${proyecto.fecha_termino}"`);

                console.log('Proyecto mapeado:', proyecto);

                // Validar que al menos el contrato esté presente (ser más flexible)
                if (proyecto.contrato && proyecto.contrato.trim() !== '') {
                    // Asignar valores por defecto para campos vacíos (excepto fecha_inicio)
                    if (!proyecto.cliente) proyecto.cliente = 'Cliente no especificado';
                    if (!proyecto.region) proyecto.region = 'Región no especificada';
                    if (!proyecto.ciudad) proyecto.ciudad = 'Ciudad no especificada';
                    if (!proyecto.estado) proyecto.estado = 'Activo';
                    // NO asignar fecha por defecto aquí - dejar que el servidor lo maneje

                    proyectos.push(proyecto);
                    console.log('Proyecto válido agregado:', proyecto);
                } else {
                    console.warn('Proyecto inválido - falta contrato:', proyecto);
                }
            } catch (error) {
                console.warn('Error procesando fila CSV:', row, error);
            }
        }

        console.log(`Proyectos válidos encontrados: ${proyectos.length}`);
        return proyectos;
    }

    clearForm() {
        // Limpiar todos los campos del formulario
        const form = document.getElementById('addRecordForm');
        if (form) {
            form.reset();
            console.log('Formulario limpiado después de importación CSV');
        }
    }

    getCSVValue(row, possibleKeys) {
        // Busca un valor en el objeto row usando diferentes posibles nombres de clave
        console.log('Buscando valor para claves:', possibleKeys, 'en fila:', Object.keys(row));

        for (const key of possibleKeys) {
            if (row[key] !== undefined && row[key] !== null && row[key] !== '') {
                const value = row[key].toString().trim();

                // Manejar valores NULL explícitos
                if (value.toLowerCase() === 'null' || value === '') {
                    continue;
                }

                console.log(`Encontrado ${key}: "${value}"`);
                return value;
            }
        }

        console.log('No se encontró valor para ninguna clave');
        return '';
    }

    parseDate(dateString) {
        // Parsea diferentes formatos de fecha
        if (!dateString ||
            dateString.toLowerCase() === 'null' ||
            dateString.trim() === '' ||
            dateString === '""' ||
            dateString === "''" ||
            dateString.length === 0) {
            console.log('Fecha vacía o NULL:', `"${dateString}"`);
            return null;
        }

        try {
            console.log('Parseando fecha:', `"${dateString}"`);

            const cleanDate = dateString.toString().trim();

            // Detectar formato DD-MM-YYYY específicamente
            const ddmmyyyyPattern = /^(\d{1,2})-(\d{1,2})-(\d{4})$/;
            const ddmmyyyyMatch = cleanDate.match(ddmmyyyyPattern);

            if (ddmmyyyyMatch) {
                const [, day, month, year] = ddmmyyyyMatch;
                const date = new Date(parseInt(year), parseInt(month) - 1, parseInt(day));

                if (!isNaN(date.getTime())) {
                    const result = date.toISOString().split('T')[0];
                    console.log(`✅ Fecha DD-MM-YYYY parseada: ${cleanDate} → ${result}`);
                    return result;
                }
            }

            // Detectar formato YYYY-MM-DD
            const yyyymmddPattern = /^(\d{4})-(\d{1,2})-(\d{1,2})$/;
            const yyyymmddMatch = cleanDate.match(yyyymmddPattern);

            if (yyyymmddMatch) {
                const date = new Date(cleanDate);
                if (!isNaN(date.getTime())) {
                    const result = date.toISOString().split('T')[0];
                    console.log(`✅ Fecha YYYY-MM-DD parseada: ${cleanDate} → ${result}`);
                    return result;
                }
            }

            // Detectar formato DD/MM/YYYY
            const ddmmyyyySlashPattern = /^(\d{1,2})\/(\d{1,2})\/(\d{4})$/;
            const ddmmyyyySlashMatch = cleanDate.match(ddmmyyyySlashPattern);

            if (ddmmyyyySlashMatch) {
                const [, day, month, year] = ddmmyyyySlashMatch;
                const date = new Date(parseInt(year), parseInt(month) - 1, parseInt(day));

                if (!isNaN(date.getTime())) {
                    const result = date.toISOString().split('T')[0];
                    console.log(`✅ Fecha DD/MM/YYYY parseada: ${cleanDate} → ${result}`);
                    return result;
                }
            }

            console.warn(`❌ Formato de fecha no reconocido: "${cleanDate}"`);

        } catch (error) {
            console.warn('❌ Error parseando fecha:', dateString, error);
        }

        console.log('❌ No se pudo parsear la fecha:', dateString);
        return null;
    }

    mapEstado(estadoString) {
        // Mapea diferentes variaciones de estado a los valores estándar
        if (!estadoString) return 'Activo';

        const estado = estadoString.toLowerCase().trim();

        if (estado.includes('activ') || estado.includes('active')) return 'Activo';
        if (estado.includes('complet') || estado.includes('finish') || estado.includes('done')) return 'Completado';
        if (estado.includes('pend') || estado.includes('wait')) return 'Pendiente';

        // Si no coincide, usar el valor original si es válido
        const validStates = ['Activo', 'Completado', 'Pendiente'];
        const capitalizedState = estadoString.charAt(0).toUpperCase() + estadoString.slice(1).toLowerCase();

        return validStates.includes(capitalizedState) ? capitalizedState : 'Activo';
    }

    parseMonto(montoString) {
        // Parsea diferentes formatos de monto
        if (!montoString) return 0;

        try {
            // Remover símbolos de moneda y espacios
            const cleanMonto = montoString.toString()
                .replace(/[$\s]/g, '')
                .replace(/[.,](\d{3})/g, '$1') // Remover separadores de miles
                .replace(/,/g, '.'); // Convertir coma decimal a punto

            const parsed = parseFloat(cleanMonto);
            return isNaN(parsed) ? 0 : Math.abs(parsed);
        } catch (error) {
            console.warn('Error parseando monto:', montoString, error);
            return 0;
        }
    }

    parseBoolean(value) {
        // Parsea valores booleanos desde CSV
        if (typeof value === 'boolean') return value;
        if (!value || value === '') return false;

        const lowerValue = value.toString().toLowerCase().trim();
        return lowerValue === 'true' || lowerValue === 'sí' || lowerValue === 'si' ||
               lowerValue === '1' || lowerValue === 'yes' || lowerValue === 'y';
    }

    parseFloat(value) {
        // Parsea valores flotantes desde CSV
        if (!value || value === '' || value === 'NULL' || value === 'null') return null;

        try {
            // Limpiar el valor (remover espacios, comas como separadores de miles)
            const cleanValue = value.toString()
                .replace(/\s/g, '')
                .replace(/,/g, ''); // Asumir que las comas son separadores de miles

            const parsed = parseFloat(cleanValue);
            return isNaN(parsed) ? null : parsed;
        } catch (error) {
            console.warn('Error parseando float:', value, error);
            return null;
        }
    }

    async loadExistingRecords() {
        try {
            const data = await dataManager.getAllRecords();
            this.populateManageTable(data);
        } catch (error) {
            console.error('Error loading records:', error);
            UIComponents.showNotification('Error loading records', 'error');
        }
    }

    populateManageTable(data) {
        const tableBody = document.getElementById('manageTableBody');
        if (!tableBody) return;

        // Clear existing rows
        tableBody.innerHTML = '';

        if (data.length === 0) {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td colspan="32" style="text-align: center; padding: 2rem; color: var(--gray-500);">
                    No records found
                </td>
            `;
            tableBody.appendChild(row);
            return;
        }

        // Create rows
        data.forEach(record => {
            const row = document.createElement('tr');
            row.className = 'fade-in';
            
            row.innerHTML = `
                <td>
                    <input type="checkbox" class="checkbox" value="${record.id}">
                </td>
                <td>${record.id}</td>
                <td>${record.contrato}</td>
                <td>${record.cliente}</td>
                <td>${record.fecha_inicio ? formatDate(record.fecha_inicio) : '-'}</td>
                <td>${record.fecha_termino ? formatDate(record.fecha_termino) : '-'}</td>
                <td>${record.region}</td>
                <td>${record.ciudad}</td>
                <td>
                    <span class="status-badge status-${record.estado.toLowerCase()}">
                        ${record.estado}
                    </span>
                </td>
                <td>${formatCurrency(record.monto)}</td>
                <td>${record.rut_cliente || 'N/A'}</td>
                <td>${record.tipo_cliente || 'N/A'}</td>
                <td>${record.persona_contacto || 'N/A'}</td>
                <td>${record.telefono_contacto || 'N/A'}</td>
                <td>${record.correo_contacto || 'N/A'}</td>
                <td>${record.superficie_terreno ? record.superficie_terreno.toLocaleString() + ' m²' : 'N/A'}</td>
                <td>${record.superficie_construida ? record.superficie_construida.toLocaleString() + ' m²' : 'N/A'}</td>
                <td>${record.tipo_obra_lista || 'N/A'}</td>
                <td>${record.ems ? '✓' : '✗'}</td>
                <td>${record.estudio_sismico ? '✓' : '✗'}</td>
                <td>${record.estudio_geoelectrico ? '✓' : '✗'}</td>
                <td>${record.topografia ? '✓' : '✗'}</td>
                <td>${record.sondaje ? '✓' : '✗'}</td>
                <td>${record.hidraulica_hidrologia ? '✓' : '✗'}</td>
                <td>${record.descripcion || 'N/A'}</td>
                <td>${record.certificado_experiencia ? '✓' : '✗'}</td>
                <td>${record.orden_compra ? '✓' : '✗'}</td>
                <td>${record.contrato_doc ? '✓' : '✗'}</td>
                <td>${record.factura ? '✓' : '✗'}</td>
                <td>${record.numero_factura || 'N/A'}</td>
                <td>${record.numero_orden_compra || 'N/A'}</td>
                <td>
                    <button class="btn btn-small btn-warning" onclick="modifyPage.editRecord(${record.id})">
                        Editar
                    </button>
                    <button class="btn btn-small btn-danger" onclick="modifyPage.deleteRecord(${record.id})">
                        Eliminar
                    </button>
                </td>
            `;

            tableBody.appendChild(row);
        });

        // Reset selection
        this.selectedRecords = [];
        this.updateActionButtons();
    }

    async deleteSelected() {
        if (this.selectedRecords.length === 0) return;

        const confirmed = await UIComponents.confirm(
            `Are you sure you want to delete ${this.selectedRecords.length} record(s)?`
        );

        if (confirmed) {
            try {
                await dataManager.deleteRecords(this.selectedRecords);
                await this.loadExistingRecords();
                UIComponents.showNotification('Records deleted successfully!', 'success');
            } catch (error) {
                UIComponents.showNotification('Error deleting records', 'error');
            }
        }
    }

    editSelected() {
        if (this.selectedRecords.length !== 1) return;
        this.editRecord(parseInt(this.selectedRecords[0]));
    }

    async editRecord(id) {
        try {
            const record = await dataManager.getRecordById(id);
            if (!record) return;

            this.currentEditId = id;

            // Populate edit form - Información básica
            document.getElementById('editContrato').value = record.contrato || '';
            document.getElementById('editCliente').value = record.cliente || '';
            document.getElementById('editFechaInicio').value = record.fecha_inicio ? formatDate(record.fecha_inicio) : '';
            document.getElementById('editFechaTermino').value = record.fecha_termino ? formatDate(record.fecha_termino) : '';
            document.getElementById('editRegion').value = record.region || '';
            document.getElementById('editCiudad').value = record.ciudad || '';
            document.getElementById('editEstado').value = record.estado || 'Activo';
            document.getElementById('editMonto').value = record.monto || 0;

            // Información del cliente
            document.getElementById('editRutCliente').value = record.rut_cliente || '';
            document.getElementById('editTipoCliente').value = record.tipo_cliente || '';
            document.getElementById('editPersonaContacto').value = record.persona_contacto || '';
            document.getElementById('editTelefonoContacto').value = record.telefono_contacto || '';
            document.getElementById('editCorreoContacto').value = record.correo_contacto || '';

            // Información técnica
            document.getElementById('editSuperficieTerreno').value = record.superficie_terreno || '';
            document.getElementById('editSuperficieConstruida').value = record.superficie_construida || '';
            document.getElementById('editTipoObraLista').value = record.tipo_obra_lista || '';

            // Estudios y servicios (checkboxes)
            document.getElementById('editEms').checked = record.ems || false;
            document.getElementById('editEstudioSismico').checked = record.estudio_sismico || false;
            document.getElementById('editEstudioGeoelectrico').checked = record.estudio_geoelectrico || false;
            document.getElementById('editTopografia').checked = record.topografia || false;
            document.getElementById('editSondaje').checked = record.sondaje || false;
            document.getElementById('editHidraulicaHidrologia').checked = record.hidraulica_hidrologia || false;
            document.getElementById('editCertificadoExperiencia').checked = record.certificado_experiencia || false;

            // Documentos (checkboxes)
            document.getElementById('editOrdenCompra').checked = record.orden_compra || false;
            document.getElementById('editContratoDoc').checked = record.contrato_doc || false;
            document.getElementById('editFactura').checked = record.factura || false;

            // Números de documentos
            document.getElementById('editNumeroOrdenCompra').value = record.numero_orden_compra || '';
            document.getElementById('editNumeroFactura').value = record.numero_factura || '';

            // Descripción
            document.getElementById('editDescripcion').value = record.descripcion || '';

            // Show modal
            document.getElementById('editModal').classList.add('active');
            document.body.style.overflow = 'hidden';
        } catch (error) {
            UIComponents.showNotification('Error loading record for editing', 'error');
        }
    }

    async deleteRecord(id) {
        const confirmed = await UIComponents.confirm('Are you sure you want to delete this record?');

        if (confirmed) {
            try {
                await dataManager.deleteRecord(id);
                await this.loadExistingRecords();
                UIComponents.showNotification('Record deleted successfully!', 'success');
            } catch (error) {
                UIComponents.showNotification('Error deleting record', 'error');
            }
        }
    }

    async saveEdit() {
        if (!this.currentEditId) return;

        try {
            const data = {
                // Información básica
                contrato: document.getElementById('editContrato').value,
                cliente: document.getElementById('editCliente').value,
                fecha_inicio: document.getElementById('editFechaInicio').value,
                fecha_termino: document.getElementById('editFechaTermino').value,
                region: document.getElementById('editRegion').value,
                ciudad: document.getElementById('editCiudad').value,
                estado: document.getElementById('editEstado').value,
                monto: document.getElementById('editMonto').value,

                // Información del cliente
                rut_cliente: document.getElementById('editRutCliente').value,
                tipo_cliente: document.getElementById('editTipoCliente').value,
                persona_contacto: document.getElementById('editPersonaContacto').value,
                telefono_contacto: document.getElementById('editTelefonoContacto').value,
                correo_contacto: document.getElementById('editCorreoContacto').value,

                // Información técnica
                superficie_terreno: document.getElementById('editSuperficieTerreno').value,
                superficie_construida: document.getElementById('editSuperficieConstruida').value,
                tipo_obra_lista: document.getElementById('editTipoObraLista').value,

                // Estudios y servicios (checkboxes)
                ems: document.getElementById('editEms').checked,
                estudio_sismico: document.getElementById('editEstudioSismico').checked,
                estudio_geoelectrico: document.getElementById('editEstudioGeoelectrico').checked,
                topografia: document.getElementById('editTopografia').checked,
                sondaje: document.getElementById('editSondaje').checked,
                hidraulica_hidrologia: document.getElementById('editHidraulicaHidrologia').checked,
                certificado_experiencia: document.getElementById('editCertificadoExperiencia').checked,

                // Documentos (checkboxes)
                orden_compra: document.getElementById('editOrdenCompra').checked,
                contrato_doc: document.getElementById('editContratoDoc').checked,
                factura: document.getElementById('editFactura').checked,

                // Números de documentos
                numero_orden_compra: document.getElementById('editNumeroOrdenCompra').value,
                numero_factura: document.getElementById('editNumeroFactura').value,

                // Descripción
                descripcion: document.getElementById('editDescripcion').value
            };

            // Validate
            const errors = validateRecord(data);
            if (errors.length > 0) {
                UIComponents.showNotification(errors.join('\n'), 'error');
                return;
            }

            // Update record
            await dataManager.updateRecord(this.currentEditId, data);

            // Close modal
            document.getElementById('editModal').classList.remove('active');
            document.body.style.overflow = '';

            // Refresh table
            await this.loadExistingRecords();

            UIComponents.showNotification('Record updated successfully!', 'success');

        } catch (error) {
            UIComponents.showNotification('Error updating record', 'error');
        }
    }


}

// Initialize the page when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.modifyPage = new ModifyDatabasePage();
});
