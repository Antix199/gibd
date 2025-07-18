/**
 * Main Page JavaScript
 * Handles the Data Filtering and Display page functionality
 */

class MainPage {
    constructor() {
        this.currentFilters = {
            name: '',
            status: ''
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
        const nameFilter = document.getElementById('nameFilter');
        const statusFilter = document.getElementById('statusFilter');

        if (nameFilter) {
            nameFilter.addEventListener('keypress', (e) => {
                if (e.key === 'Enter') {
                    this.applyFilters();
                }
            });
        }

        if (statusFilter) {
            statusFilter.addEventListener('change', () => {
                this.applyFilters();
            });
        }
    }

    setupSearch() {
        // Setup real-time search on the main search box
        UIComponents.setupSearch('searchInput', (query) => {
            this.currentFilters.name = query;
            this.loadData();
        });
    }

    loadData() {
        try {
            UIComponents.showLoading('Loading data...');
            
            // Simulate loading delay for better UX
            setTimeout(() => {
                const data = dataManager.getFilteredRecords(
                    this.currentFilters.name,
                    this.currentFilters.status
                );

                this.populateTable(data);
                this.updateStatistics(data);
                UIComponents.hideLoading();
            }, 300);
            
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
                <td colspan="5" style="text-align: center; padding: 2rem; color: var(--gray-500);">
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
                <td>${record.name}</td>
                <td>${formatDate(record.date)}</td>
                <td>
                    <span class="status-badge status-${record.status.toLowerCase()}">
                        ${record.status}
                    </span>
                </td>
                <td>${formatCurrency(record.amount)}</td>
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
        const nameFilter = document.getElementById('nameFilter');
        const statusFilter = document.getElementById('statusFilter');

        if (nameFilter) {
            let nameValue = nameFilter.value.trim();
            // Clear placeholder text
            if (nameValue === 'dd-mm-aaaa') {
                nameValue = '';
            }
            this.currentFilters.name = nameValue;
        }

        if (statusFilter) {
            const statusValue = statusFilter.value;
            this.currentFilters.status = statusValue === 'Select Status' ? '' : statusValue;
        }

        this.loadData();
        
        // Show feedback
        UIComponents.showNotification('Filters applied successfully', 'success');
    }

    clearFilters() {
        // Reset filter inputs
        const nameFilter = document.getElementById('nameFilter');
        const statusFilter = document.getElementById('statusFilter');
        const searchInput = document.getElementById('searchInput');

        if (nameFilter) {
            nameFilter.value = '';
        }

        if (statusFilter) {
            statusFilter.value = '';
        }

        if (searchInput) {
            searchInput.value = '';
        }

        // Reset current filters
        this.currentFilters = {
            name: '',
            status: ''
        };

        this.loadData();
        
        // Show feedback
        UIComponents.showNotification('Filters cleared', 'info');
    }

    generatePDF() {
        try {
            UIComponents.showLoading('Generating export...');
            
            // Get current filtered data
            const data = dataManager.getFilteredRecords(
                this.currentFilters.name,
                this.currentFilters.status
            );

            if (data.length === 0) {
                UIComponents.hideLoading();
                UIComponents.showNotification('No data to export', 'warning');
                return;
            }

            // Simulate export process
            setTimeout(() => {
                // Create CSV content
                const headers = ['ID', 'Name', 'Date', 'Status', 'Amount'];
                const csvContent = [
                    headers.join(','),
                    ...data.map(record => [
                        record.id,
                        `"${record.name}"`,
                        record.date,
                        record.status,
                        record.amount
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
            }, 1000);

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
