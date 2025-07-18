/**
 * Data Management Module
 * Handles all data operations and storage
 */

class DataManager {
    constructor() {
        this.storageKey = 'glaciaring_data';
        this.data = this.loadData();
        this.nextId = this.getNextId();
    }

    /**
     * Load data from localStorage or return default data
     */
    loadData() {
        const stored = localStorage.getItem(this.storageKey);
        if (stored) {
            try {
                return JSON.parse(stored);
            } catch (e) {
                console.error('Error parsing stored data:', e);
            }
        }
        
        // Default sample data
        return [
            {
                id: 1001,
                name: "Alice Smith",
                date: "2023-01-15",
                status: "Completed",
                amount: 120.00
            },
            {
                id: 1002,
                name: "Bob Johnson",
                date: "2023-01-18",
                status: "Pending",
                amount: 75.50
            },
            {
                id: 1003,
                name: "Charlie Brown",
                date: "2023-01-20",
                status: "Active",
                amount: 200.00
            },
            {
                id: 1004,
                name: "Diana Prince",
                date: "2023-01-22",
                status: "Completed",
                amount: 99.99
            },
            {
                id: 1005,
                name: "Eve Adams",
                date: "2023-01-25",
                status: "Pending",
                amount: 50.00
            }
        ];
    }

    /**
     * Save data to localStorage
     */
    saveData() {
        try {
            localStorage.setItem(this.storageKey, JSON.stringify(this.data));
            return true;
        } catch (e) {
            console.error('Error saving data:', e);
            return false;
        }
    }

    /**
     * Get next available ID
     */
    getNextId() {
        if (this.data.length === 0) return 1001;
        return Math.max(...this.data.map(item => item.id)) + 1;
    }

    /**
     * Get all records
     */
    getAllRecords() {
        return [...this.data];
    }

    /**
     * Get filtered records
     */
    getFilteredRecords(nameFilter = '', statusFilter = '') {
        return this.data.filter(record => {
            const nameMatch = !nameFilter || 
                record.name.toLowerCase().includes(nameFilter.toLowerCase());
            const statusMatch = !statusFilter || record.status === statusFilter;
            return nameMatch && statusMatch;
        });
    }

    /**
     * Get record by ID
     */
    getRecordById(id) {
        return this.data.find(record => record.id === parseInt(id));
    }

    /**
     * Add new record
     */
    addRecord(recordData) {
        const newRecord = {
            id: recordData.id || this.nextId++,
            name: recordData.name,
            date: recordData.date,
            status: recordData.status,
            amount: parseFloat(recordData.amount) || 0
        };

        this.data.push(newRecord);
        this.saveData();
        return newRecord;
    }

    /**
     * Update existing record
     */
    updateRecord(id, recordData) {
        const index = this.data.findIndex(record => record.id === parseInt(id));
        if (index === -1) return false;

        this.data[index] = {
            ...this.data[index],
            name: recordData.name,
            date: recordData.date,
            status: recordData.status,
            amount: parseFloat(recordData.amount) || 0
        };

        this.saveData();
        return this.data[index];
    }

    /**
     * Delete record by ID
     */
    deleteRecord(id) {
        const index = this.data.findIndex(record => record.id === parseInt(id));
        if (index === -1) return false;

        this.data.splice(index, 1);
        this.saveData();
        return true;
    }

    /**
     * Delete multiple records by IDs
     */
    deleteRecords(ids) {
        const numericIds = ids.map(id => parseInt(id));
        this.data = this.data.filter(record => !numericIds.includes(record.id));
        this.saveData();
        return true;
    }

    /**
     * Import data from array
     */
    importData(newData) {
        try {
            const validData = newData.filter(record => 
                record.name && record.status && typeof record.amount === 'number'
            );

            validData.forEach(record => {
                record.id = record.id || this.nextId++;
                record.date = record.date || new Date().toISOString().split('T')[0];
                record.amount = parseFloat(record.amount) || 0;
            });

            this.data.push(...validData);
            this.saveData();
            return validData.length;
        } catch (e) {
            console.error('Error importing data:', e);
            return 0;
        }
    }

    /**
     * Export data to JSON
     */
    exportData() {
        return JSON.stringify(this.data, null, 2);
    }

    /**
     * Clear all data
     */
    clearData() {
        this.data = [];
        this.nextId = 1001;
        this.saveData();
    }

    /**
     * Get statistics
     */
    getStatistics() {
        const total = this.data.length;
        const completed = this.data.filter(r => r.status === 'Completed').length;
        const pending = this.data.filter(r => r.status === 'Pending').length;
        const active = this.data.filter(r => r.status === 'Active').length;
        const totalAmount = this.data.reduce((sum, r) => sum + r.amount, 0);

        return {
            total,
            completed,
            pending,
            active,
            totalAmount
        };
    }
}

// Create global instance
window.dataManager = new DataManager();

// Utility functions
window.formatCurrency = function(amount) {
    return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD'
    }).format(amount);
};

window.formatDate = function(dateString) {
    if (!dateString) return '';
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US');
};

window.validateRecord = function(record) {
    const errors = [];
    
    if (!record.name || record.name.trim().length < 2) {
        errors.push('Name must be at least 2 characters long');
    }
    
    if (!record.status || !['Active', 'Completed', 'Pending'].includes(record.status)) {
        errors.push('Please select a valid status');
    }
    
    if (record.amount && (isNaN(record.amount) || record.amount < 0)) {
        errors.push('Amount must be a positive number');
    }
    
    if (!record.date) {
        errors.push('Date is required');
    }
    
    return errors;
};
