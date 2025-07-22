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
                    monto: parseFloat(recordData.monto) || 0
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

            // Mapear a la estructura correcta
            const proyectos = validData.map(record => ({
                id: record.id || null,
                contrato: record.contrato,
                cliente: record.cliente,
                fecha_inicio: record.fecha_inicio || null, // No asignar fecha por defecto aquí
                fecha_termino: record.fecha_termino || null,
                region: record.region,
                ciudad: record.ciudad,
                estado: record.estado || 'Activo',
                monto: parseFloat(record.monto) || 0
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

    // Normalizar nombres de campos
    const contrato = record.contrato || record.recordContrato;
    const cliente = record.cliente || record.recordCliente;
    const fecha_inicio = record.fecha_inicio || record.recordFechaInicio;
    const region = record.region || record.recordRegion;
    const ciudad = record.ciudad || record.recordCiudad;
    const estado = record.estado || record.recordEstado;
    const monto = record.monto || record.recordMonto;

    // Validar contrato
    if (!contrato || contrato.trim().length < 2) {
        errors.push('El contrato debe tener al menos 2 caracteres');
    }

    // Validar cliente
    if (!cliente || cliente.trim().length < 2) {
        errors.push('El cliente debe tener al menos 2 caracteres');
    }

    // Validar región
    if (!region || region.trim().length < 2) {
        errors.push('La región debe tener al menos 2 caracteres');
    }

    // Validar ciudad
    if (!ciudad || ciudad.trim().length < 2) {
        errors.push('La ciudad debe tener al menos 2 caracteres');
    }

    // Validar estado
    if (!estado || !['Activo', 'Completado', 'Pendiente'].includes(estado)) {
        errors.push('Por favor selecciona un estado válido');
    }

    // Validar monto (opcional, pero si se proporciona debe ser válido)
    if (monto !== undefined && monto !== '' && (isNaN(monto) || parseFloat(monto) < 0)) {
        errors.push('El monto debe ser un número positivo');
    }

    // Validar fecha de inicio
    if (!fecha_inicio || fecha_inicio.trim() === '') {
        errors.push('La fecha de inicio es requerida');
    }

    return errors;
};
