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

        // Set default date to today
        const recordDate = document.getElementById('recordDate');
        if (recordDate) {
            recordDate.value = new Date().toISOString().split('T')[0];
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
            // Validate data
            const errors = validateRecord(data);
            if (errors.length > 0) {
                throw new Error(errors.join('\n'));
            }

            // Add record
            const newRecord = dataManager.addRecord({
                id: data.recordId ? parseInt(data.recordId) : null,
                name: data.recordName,
                date: data.recordDate,
                status: data.recordStatus,
                amount: parseFloat(data.recordAmount) || 0
            });

            // Refresh table
            this.loadExistingRecords();
            
            UIComponents.showNotification('Record added successfully!', 'success');
            
        } catch (error) {
            throw error;
        }
    }

    handleFileSelect(file) {
        console.log('File selected:', file.name);
        // You can add file validation here
        if (!file.name.match(/\.(csv|xlsx|xls)$/i)) {
            UIComponents.showNotification('Please select a CSV or Excel file', 'error');
            return false;
        }
        return true;
    }

    async uploadFile(file) {
        try {
            UIComponents.showLoading('Processing file...');

            // Simulate file processing
            await new Promise(resolve => setTimeout(resolve, 2000));

            // For demo purposes, we'll add some sample data
            const sampleData = [
                {
                    name: "Imported User 1",
                    status: "Active",
                    amount: 150.00,
                    date: new Date().toISOString().split('T')[0]
                },
                {
                    name: "Imported User 2", 
                    status: "Pending",
                    amount: 200.00,
                    date: new Date().toISOString().split('T')[0]
                }
            ];

            const importedCount = dataManager.importData(sampleData);
            
            // Refresh table
            this.loadExistingRecords();
            
            // Reset file input
            const fileInput = document.getElementById('fileInput');
            const fileInfo = document.getElementById('fileInfo');
            const uploadBtn = document.getElementById('uploadBtn');
            
            if (fileInput) fileInput.value = '';
            if (fileInfo) fileInfo.textContent = 'Ningún archivo seleccionado';
            if (uploadBtn) uploadBtn.disabled = true;

            UIComponents.hideLoading();
            UIComponents.showNotification(`Successfully imported ${importedCount} records!`, 'success');

        } catch (error) {
            UIComponents.hideLoading();
            UIComponents.showNotification('Error processing file: ' + error.message, 'error');
        }
    }

    loadExistingRecords() {
        try {
            const data = dataManager.getAllRecords();
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
                <td colspan="7" style="text-align: center; padding: 2rem; color: var(--gray-500);">
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
                <td>${record.name}</td>
                <td>${formatDate(record.date)}</td>
                <td>
                    <span class="status-badge status-${record.status.toLowerCase()}">
                        ${record.status}
                    </span>
                </td>
                <td>${formatCurrency(record.amount)}</td>
                <td>
                    <button class="btn btn-small btn-warning" onclick="modifyPage.editRecord(${record.id})">
                        Edit
                    </button>
                    <button class="btn btn-small btn-danger" onclick="modifyPage.deleteRecord(${record.id})">
                        Delete
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
                dataManager.deleteRecords(this.selectedRecords);
                this.loadExistingRecords();
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

    editRecord(id) {
        const record = dataManager.getRecordById(id);
        if (!record) return;

        this.currentEditId = id;

        // Populate edit form
        document.getElementById('editName').value = record.name;
        document.getElementById('editDate').value = record.date;
        document.getElementById('editStatus').value = record.status;
        document.getElementById('editAmount').value = record.amount;

        // Show modal
        document.getElementById('editModal').classList.add('active');
        document.body.style.overflow = 'hidden';
    }

    async deleteRecord(id) {
        const confirmed = await UIComponents.confirm('Are you sure you want to delete this record?');
        
        if (confirmed) {
            try {
                dataManager.deleteRecord(id);
                this.loadExistingRecords();
                UIComponents.showNotification('Record deleted successfully!', 'success');
            } catch (error) {
                UIComponents.showNotification('Error deleting record', 'error');
            }
        }
    }

    saveEdit() {
        if (!this.currentEditId) return;

        try {
            const data = {
                name: document.getElementById('editName').value,
                date: document.getElementById('editDate').value,
                status: document.getElementById('editStatus').value,
                amount: document.getElementById('editAmount').value
            };

            // Validate
            const errors = validateRecord(data);
            if (errors.length > 0) {
                UIComponents.showNotification(errors.join('\n'), 'error');
                return;
            }

            // Update record
            dataManager.updateRecord(this.currentEditId, data);
            
            // Close modal
            document.getElementById('editModal').classList.remove('active');
            document.body.style.overflow = '';
            
            // Refresh table
            this.loadExistingRecords();
            
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
