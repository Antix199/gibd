/**
 * Data Management Module
 * Handles all data operations via API
 */

class DataManager {
    constructor() {
        this.apiBaseUrl = '/api';
        this.cache = new Map();
        this.cacheTimeout = 5 * 60 * 1000; // 5 minutos
    }

    /**
     * Make API request
     */
    async apiRequest(endpoint, options = {}) {
        try {
            const url = `${this.apiBaseUrl}${endpoint}`;
            const defaultOptions = {
                headers: {
                    'Content-Type': 'application/json',
                },
            };

            const response = await fetch(url, { ...defaultOptions, ...options });
            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.error || `HTTP error! status: ${response.status}`);
            }

            return data;
        } catch (error) {
            console.error('API request failed:', error);
            throw error;
        }
    }

    /**
     * Check API health
     */
    async checkHealth() {
        try {
            const response = await this.apiRequest('/health');
            return response;
        } catch (error) {
            console.error('Health check failed:', error);
            return { status: 'error', message: error.message };
        }
    }

    /**
     * Get all records
     */
    async getAllRecords() {
        try {
            const response = await this.apiRequest('/proyectos');
            return response.data || [];
        } catch (error) {
            console.error('Error getting all records:', error);
            return [];
        }
    }

    /**
     * Get filtered records
     */
    async getFilteredRecords(clienteFilter = '', estadoFilter = '') {
        try {
            const params = new URLSearchParams();
            if (clienteFilter) params.append('cliente', clienteFilter);
            if (estadoFilter) params.append('estado', estadoFilter);

            const endpoint = `/proyectos${params.toString() ? '?' + params.toString() : ''}`;
            const response = await this.apiRequest(endpoint);
            return response.data || [];
        } catch (error) {
            console.error('Error getting filtered records:', error);
            return [];
        }
    }

    /**
     * Get records with advanced filtering
     */
    async getAdvancedFilteredRecords(filters = {}) {
        try {
            const data = await this.getAllRecords();

            return data.filter(record => {
                // Búsqueda general (ID, contrato, cliente)
                if (filters.search) {
                    const searchTerm = filters.search.toLowerCase();
                    const searchMatch =
                        (record.id && record.id.toString().toLowerCase().includes(searchTerm)) ||
                        (record.contrato && record.contrato.toLowerCase().includes(searchTerm)) ||
                        (record.cliente && record.cliente.toLowerCase().includes(searchTerm));

                    if (!searchMatch) return false;
                }

                // Filtro por ID específico
                if (filters.id && record.id) {
                    if (!record.id.toString().toLowerCase().includes(filters.id.toLowerCase())) {
                        return false;
                    }
                }

                // Filtro por contrato
                if (filters.contrato && record.contrato) {
                    if (!record.contrato.toLowerCase().includes(filters.contrato.toLowerCase())) {
                        return false;
                    }
                }

                // Filtro por cliente
                if (filters.cliente && record.cliente) {
                    if (!record.cliente.toLowerCase().includes(filters.cliente.toLowerCase())) {
                        return false;
                    }
                }

                // Filtro por estado
                if (filters.estado && record.estado !== filters.estado) {
                    return false;
                }

                // Filtro por región
                if (filters.region && record.region) {
                    if (!record.region.toLowerCase().includes(filters.region.toLowerCase())) {
                        return false;
                    }
                }

                // Filtro por ciudad
                if (filters.ciudad && record.ciudad) {
                    if (!record.ciudad.toLowerCase().includes(filters.ciudad.toLowerCase())) {
                        return false;
                    }
                }

                // Filtros de fecha de inicio
                if (filters.fechaInicioDesde || filters.fechaInicioHasta) {
                    const fechaInicio = record.fecha_inicio ? new Date(record.fecha_inicio) : null;

                    if (filters.fechaInicioDesde) {
                        const fechaDesde = new Date(filters.fechaInicioDesde);
                        if (!fechaInicio || fechaInicio < fechaDesde) {
                            return false;
                        }
                    }

                    if (filters.fechaInicioHasta) {
                        const fechaHasta = new Date(filters.fechaInicioHasta);
                        if (!fechaInicio || fechaInicio > fechaHasta) {
                            return false;
                        }
                    }
                }

                // Filtros de fecha de término
                if (filters.fechaTerminoDesde || filters.fechaTerminoHasta) {
                    const fechaTermino = record.fecha_termino ? new Date(record.fecha_termino) : null;

                    if (filters.fechaTerminoDesde) {
                        const fechaDesde = new Date(filters.fechaTerminoDesde);
                        if (!fechaTermino || fechaTermino < fechaDesde) {
                            return false;
                        }
                    }

                    if (filters.fechaTerminoHasta) {
                        const fechaHasta = new Date(filters.fechaTerminoHasta);
                        if (!fechaTermino || fechaTermino > fechaHasta) {
                            return false;
                        }
                    }
                }

                // Filtros de monto
                if (filters.montoDesde || filters.montoHasta) {
                    const monto = parseFloat(record.monto) || 0;

                    if (filters.montoDesde) {
                        const montoDesde = parseFloat(filters.montoDesde);
                        if (monto < montoDesde) {
                            return false;
                        }
                    }

                    if (filters.montoHasta) {
                        const montoHasta = parseFloat(filters.montoHasta);
                        if (monto > montoHasta) {
                            return false;
                        }
                    }
                }

                return true;
            });
        } catch (error) {
            console.error('Error filtering records with advanced filters:', error);
            throw error;
        }
    }

    /**
     * Get record by ID
     */
    async getRecordById(id) {
        try {
            const response = await this.apiRequest(`/proyectos/${id}`);
            return response.data;
        } catch (error) {
            console.error('Error getting record by ID:', error);
            return null;
        }
    }

    /**
     * Add new record
     */
    async addRecord(recordData) {
        try {
            const response = await this.apiRequest('/proyectos', {
                method: 'POST',
                body: JSON.stringify({
                    id: recordData.id || null,
                    contrato: recordData.contrato,
                    cliente: recordData.cliente,
                    fecha_inicio: recordData.fecha_inicio,
                    fecha_termino: recordData.fecha_termino,
                    region: recordData.region,
                    ciudad: recordData.ciudad,
                    estado: recordData.estado,
                    monto: parseFloat(recordData.monto) || 0
                })
            });
            return response.data;
        } catch (error) {
            console.error('Error adding record:', error);
            throw error;
        }
    }

    /**
     * Update existing record
     */
    async updateRecord(id, recordData) {
        try {
            const response = await this.apiRequest(`/proyectos/${id}`, {
                method: 'PUT',
                body: JSON.stringify({
                    contrato: recordData.contrato,
                    cliente: recordData.cliente,
                    fecha_inicio: recordData.fecha_inicio,
                    fecha_termino: recordData.fecha_termino,
                    region: recordData.region,
                    ciudad: recordData.ciudad,
                    estado: recordData.estado,
                    monto: parseFloat(recordData.monto) || 0,
                    // Información del cliente
                    rut_cliente: recordData.rut_cliente || '',
                    tipo_cliente: recordData.tipo_cliente || '',
                    persona_contacto: recordData.persona_contacto || '',
                    telefono_contacto: recordData.telefono_contacto || '',
                    correo_contacto: recordData.correo_contacto || '',
                    // Información técnica
                    superficie_terreno: recordData.superficie_terreno ? parseFloat(recordData.superficie_terreno) : null,
                    superficie_construida: recordData.superficie_construida ? parseFloat(recordData.superficie_construida) : null,
                    tipo_obra_lista: recordData.tipo_obra_lista || '',
                    // Estudios y servicios
                    ems: recordData.ems || false,
                    estudio_sismico: recordData.estudio_sismico || false,
                    estudio_geoelectrico: recordData.estudio_geoelectrico || false,
                    topografia: recordData.topografia || false,
                    sondaje: recordData.sondaje || false,
                    hidraulica_hidrologia: recordData.hidraulica_hidrologia || false,
                    descripcion: recordData.descripcion || '',
                    certificado_experiencia: recordData.certificado_experiencia || false,
                    orden_compra: recordData.orden_compra || false,
                    contrato_doc: recordData.contrato_doc || false,
                    factura: recordData.factura || false,
                    numero_factura: recordData.numero_factura || '',
                    numero_orden_compra: recordData.numero_orden_compra || ''
                })
            });
            return response.data;
        } catch (error) {
            console.error('Error updating record:', error);
            throw error;
        }
    }

    /**
     * Delete record by ID
     */
    async deleteRecord(id) {
        try {
            await this.apiRequest(`/proyectos/${id}`, {
                method: 'DELETE'
            });
            return true;
        } catch (error) {
            console.error('Error deleting record:', error);
            return false;
        }
    }

    /**
     * Delete multiple records by IDs
     */
    async deleteRecords(ids) {
        try {
            await this.apiRequest('/proyectos/bulk-delete', {
                method: 'POST',
                body: JSON.stringify({ ids })
            });
            return true;
        } catch (error) {
            console.error('Error deleting records:', error);
            return false;
        }
    }

    /**
     * Import data from array
     */
    async importData(newData) {
        try {
            // Filtrar datos válidos con los nuevos campos (solo requiere contrato)
            const validData = newData.filter(record =>
                record.contrato && record.contrato.trim() !== ''
            );

            // Mapear a la estructura correcta con todos los campos
            const proyectos = validData.map(record => ({
                id: record.id || null,
                contrato: record.contrato,
                cliente: record.cliente,
                fecha_inicio: record.fecha_inicio || null,
                fecha_termino: record.fecha_termino || null,
                region: record.region,
                ciudad: record.ciudad,
                estado: record.estado || 'Activo',
                monto: parseFloat(record.monto) || 0,
                // Información del cliente
                rut_cliente: record.rut_cliente || '',
                tipo_cliente: record.tipo_cliente || '',
                persona_contacto: record.persona_contacto || '',
                telefono_contacto: record.telefono_contacto || '',
                correo_contacto: record.correo_contacto || '',
                // Información técnica
                superficie_terreno: record.superficie_terreno ? parseFloat(record.superficie_terreno) : null,
                superficie_construida: record.superficie_construida ? parseFloat(record.superficie_construida) : null,
                tipo_obra_lista: record.tipo_obra_lista || '',
                // Estudios y servicios
                ems: record.ems || false,
                estudio_sismico: record.estudio_sismico || false,
                estudio_geoelectrico: record.estudio_geoelectrico || false,
                topografia: record.topografia || false,
                sondaje: record.sondaje || false,
                hidraulica_hidrologia: record.hidraulica_hidrologia || false,
                descripcion: record.descripcion || '',
                certificado_experiencia: record.certificado_experiencia || false,
                orden_compra: record.orden_compra || false,
                contrato_doc: record.contrato_doc || false,
                factura: record.factura || false,
                numero_factura: record.numero_factura || '',
                numero_orden_compra: record.numero_orden_compra || ''
            }));

            console.log('=== DATOS ENVIADOS AL SERVIDOR ===');
            proyectos.forEach((proyecto, index) => {
                console.log(`Proyecto ${index + 1}:`, {
                    id: proyecto.id,
                    contrato: proyecto.contrato,
                    fecha_inicio: proyecto.fecha_inicio,
                    fecha_termino: proyecto.fecha_termino
                });
            });

            const response = await this.apiRequest('/proyectos/bulk-import', {
                method: 'POST',
                body: JSON.stringify({ proyectos })
            });

            console.log('Respuesta de importación:', response);
            return proyectos.length;
        } catch (error) {
            console.error('Error importing data:', error);
            return 0;
        }
    }

    /**
     * Export data to JSON
     */
    async exportData() {
        try {
            const data = await this.getAllRecords();
            return JSON.stringify(data, null, 2);
        } catch (error) {
            console.error('Error exporting data:', error);
            return '[]';
        }
    }

    /**
     * Get statistics
     */
    async getStatistics() {
        try {
            const response = await this.apiRequest('/statistics');
            return response.data || {};
        } catch (error) {
            console.error('Error getting statistics:', error);
            return {
                total: 0,
                completed: 0,
                pending: 0,
                active: 0,
                totalAmount: 0
            };
        }
    }

    /**
     * Get status options
     */
    async getStatusOptions() {
        try {
            const response = await this.apiRequest('/status-options');
            return response.data || ['Active', 'Completed', 'Pending'];
        } catch (error) {
            console.error('Error getting status options:', error);
            return ['Active', 'Completed', 'Pending'];
        }
    }
}

// Create global instance
window.dataManager = new DataManager();

// Utility functions
window.formatCurrency = function(amount) {
    return new Intl.NumberFormat('es-CL', {
        style: 'currency',
        currency: 'CLP',
        minimumFractionDigits: 0,
        maximumFractionDigits: 0
    }).format(amount);
};

window.formatDate = function(dateString) {
    if (!dateString) return '';
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US');
};

window.validateRecord = function(record) {
    const errors = [];

    // Normalizar nombres de campos (solo campos obligatorios)
    const id = record.id || record.recordId;
    const contrato = record.contrato || record.recordContrato;
    const cliente = record.cliente || record.recordCliente;
    const region = record.region || record.recordRegion;
    const ciudad = record.ciudad || record.recordCiudad;
    const estado = record.estado || record.recordEstado;
    const monto = record.monto || record.recordMonto;

    // Validar ID (obligatorio)
    if (!id || id === '' || isNaN(id) || parseInt(id) <= 0) {
        errors.push('El ID es obligatorio y debe ser un número positivo');
    }

    // Validar contrato (obligatorio)
    if (!contrato || contrato.trim().length < 2) {
        errors.push('El contrato es obligatorio y debe tener al menos 2 caracteres');
    }

    // Validar cliente (obligatorio)
    if (!cliente || cliente.trim().length < 2) {
        errors.push('El cliente es obligatorio y debe tener al menos 2 caracteres');
    }

    // Validar región (obligatorio)
    if (!region || region.trim().length < 2) {
        errors.push('La región es obligatoria');
    }

    // Validar ciudad (obligatorio)
    if (!ciudad || ciudad.trim().length < 2) {
        errors.push('La ciudad es obligatoria y debe tener al menos 2 caracteres');
    }

    // Validar estado (obligatorio)
    if (!estado || !['Activo', 'Completado', 'Pendiente'].includes(estado)) {
        errors.push('El estado es obligatorio. Selecciona: Activo, Completado o Pendiente');
    }

    // Validar monto (obligatorio)
    if (monto === undefined || monto === '' || isNaN(monto) || parseFloat(monto) < 0) {
        errors.push('El monto es obligatorio y debe ser un número positivo');
    }

    return errors;
};
