/**
 * Main Page JavaScript
 * Handles the Data Filtering and Display page functionality
 */

class MainPage {
    constructor() {
        this.currentFilters = {
            cliente: '',
            estado: ''
        };
        
        this.init();
    }

    init() {
        this.setupEventListeners();
        this.loadData();
        this.setupSearch();
    }

    setupEventListeners() {
        // Navigation
        const modifyDbBtn = document.getElementById('modifyDbBtn');
        if (modifyDbBtn) {
            modifyDbBtn.addEventListener('click', () => {
                window.location.href = 'modify-database.html';
            });
        }

        // Filter buttons
        const applyFiltersBtn = document.getElementById('applyFiltersBtn');
        const clearFiltersBtn = document.getElementById('clearFiltersBtn');

        if (applyFiltersBtn) {
            applyFiltersBtn.addEventListener('click', () => this.applyFilters());
        }

        if (clearFiltersBtn) {
            clearFiltersBtn.addEventListener('click', () => this.clearFilters());
        }

        // Generate PDF button
        const generatePdfBtn = document.getElementById('generatePdfBtn');
        if (generatePdfBtn) {
            generatePdfBtn.addEventListener('click', () => this.generatePDF());
        }

        // Enter key on filter inputs
        const clienteFilter = document.getElementById('clienteFilter');
        const estadoFilter = document.getElementById('estadoFilter');

        if (clienteFilter) {
            clienteFilter.addEventListener('keypress', (e) => {
                if (e.key === 'Enter') {
                    this.applyFilters();
                }
            });
        }

        if (estadoFilter) {
            estadoFilter.addEventListener('change', () => {
                this.applyFilters();
            });
        }
    }

    setupSearch() {
        // Setup real-time search on the main search box
        UIComponents.setupSearch('searchInput', (query) => {
            this.currentFilters.cliente = query;
            this.loadData();
        });
    }

    async loadData() {
        try {
            UIComponents.showLoading('Loading data...');

            const data = await dataManager.getFilteredRecords(
                this.currentFilters.cliente,
                this.currentFilters.estado
            );

            this.populateTable(data);
            this.updateStatistics(data);
            UIComponents.hideLoading();

        } catch (error) {
            console.error('Error loading data:', error);
            UIComponents.showNotification('Error loading data', 'error');
            UIComponents.hideLoading();
        }
    }

    populateTable(data) {
        const tableBody = document.getElementById('tableBody');
        if (!tableBody) return;

        // Clear existing rows
        tableBody.innerHTML = '';

        if (data.length === 0) {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td colspan="9" style="text-align: center; padding: 2rem; color: var(--gray-500);">
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
                <td>${record.id}</td>
                <td>${record.contrato}</td>
                <td>${record.cliente}</td>
                <td>${formatDate(record.fecha_inicio)}</td>
                <td>${record.fecha_termino ? formatDate(record.fecha_termino) : '-'}</td>
                <td>${record.region}</td>
                <td>${record.ciudad}</td>
                <td>
                    <span class="status-badge status-${record.estado.toLowerCase()}">
                        ${record.estado}
                    </span>
                </td>
                <td>${formatCurrency(record.monto)}</td>
            `;

            tableBody.appendChild(row);
        });
    }

    updateStatistics(data) {
        // Update any statistics display if needed
        const stats = {
            total: data.length,
            totalAmount: data.reduce((sum, record) => sum + record.amount, 0)
        };

        // You can add statistics display here if needed
        console.log('Current view statistics:', stats);
    }

    applyFilters() {
        const clienteFilter = document.getElementById('clienteFilter');
        const estadoFilter = document.getElementById('estadoFilter');

        if (clienteFilter) {
            this.currentFilters.cliente = clienteFilter.value.trim();
        }

        if (estadoFilter) {
            const estadoValue = estadoFilter.value;
            this.currentFilters.estado = estadoValue === 'Seleccionar Estado' ? '' : estadoValue;
        }

        this.loadData();
        
        // Show feedback
        UIComponents.showNotification('Filters applied successfully', 'success');
    }

    clearFilters() {
        // Reset filter inputs
        const clienteFilter = document.getElementById('clienteFilter');
        const estadoFilter = document.getElementById('estadoFilter');
        const searchInput = document.getElementById('searchInput');

        if (clienteFilter) {
            clienteFilter.value = '';
        }

        if (estadoFilter) {
            estadoFilter.value = '';
        }

        if (searchInput) {
            searchInput.value = '';
        }

        // Reset current filters
        this.currentFilters = {
            cliente: '',
            estado: ''
        };

        this.loadData();
        
        // Show feedback
        UIComponents.showNotification('Filters cleared', 'info');
    }

    async generatePDF() {
        try {
            UIComponents.showLoading('Generating export...');

            // Get current filtered data
            const data = await dataManager.getFilteredRecords(
                this.currentFilters.cliente,
                this.currentFilters.estado
            );

            if (data.length === 0) {
                UIComponents.hideLoading();
                UIComponents.showNotification('No data to export', 'warning');
                return;
            }

            // Create CSV content
            const headers = ['ID', 'Contrato', 'Cliente', 'Fecha_Inicio', 'Fecha_Termino', 'Region', 'Ciudad', 'Estado', 'Monto'];
            const csvContent = [
                headers.join(','),
                ...data.map(record => [
                    record.id,
                    `"${record.contrato}"`,
                    `"${record.cliente}"`,
                    formatDate(record.fecha_inicio),
                    record.fecha_termino ? formatDate(record.fecha_termino) : '',
                    `"${record.region}"`,
                    `"${record.ciudad}"`,
                    record.estado,
                    record.monto
                ].join(','))
            ].join('\n');

            // Create and download file
            const blob = new Blob([csvContent], { type: 'text/csv' });
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `glaciaring_data_${new Date().toISOString().split('T')[0]}.csv`;
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            window.URL.revokeObjectURL(url);

            UIComponents.hideLoading();
            UIComponents.showNotification('Data exported successfully!', 'success');

        } catch (error) {
            console.error('Error generating export:', error);
            UIComponents.showNotification('Error generating export', 'error');
            UIComponents.hideLoading();
        }
    }
}

// Initialize the page when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new MainPage();
});

// Handle page visibility changes
document.addEventListener('visibilitychange', () => {
    if (!document.hidden) {
        // Refresh data when page becomes visible (in case data was modified in another tab)
        if (window.mainPage) {
            window.mainPage.loadData();
        }
    }
});
