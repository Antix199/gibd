/**
 * UI Components Module
 * Reusable UI components and utilities
 */

class UIComponents {
    /**
     * Show loading overlay
     */
    static showLoading(message = 'Loading...') {
        const overlay = document.getElementById('loadingOverlay');
        if (overlay) {
            const text = overlay.querySelector('p');
            if (text) text.textContent = message;
            overlay.classList.add('active');
        }
    }

    /**
     * Hide loading overlay
     */
    static hideLoading() {
        const overlay = document.getElementById('loadingOverlay');
        if (overlay) {
            overlay.classList.remove('active');
        }
    }

    /**
     * Show notification (simple alert for now, can be enhanced)
     */
    static showNotification(message, type = 'info') {
        // For now, using alert. In a real app, you'd use a toast notification
        const icons = {
            success: '✅',
            error: '❌',
            warning: '⚠️',
            info: 'ℹ️'
        };
        
        alert(`${icons[type] || icons.info} ${message}`);
    }

    /**
     * Confirm dialog
     */
    static async confirm(message) {
        return new Promise((resolve) => {
            const result = window.confirm(message);
            resolve(result);
        });
    }

    /**
     * Create status badge element
     */
    static createStatusBadge(status) {
        const badge = document.createElement('span');
        badge.className = `status-badge status-${status.toLowerCase()}`;
        badge.textContent = status;
        return badge;
    }

    /**
     * Create action button
     */
    static createActionButton(text, className, onClick) {
        const button = document.createElement('button');
        button.className = `btn ${className}`;
        button.textContent = text;
        button.addEventListener('click', onClick);
        return button;
    }

    /**
     * Create table row
     */
    static createTableRow(data, columns, actions = []) {
        const row = document.createElement('tr');
        
        columns.forEach(column => {
            const cell = document.createElement('td');
            
            if (column === 'status') {
                cell.appendChild(this.createStatusBadge(data[column]));
            } else if (column === 'amount') {
                cell.textContent = formatCurrency(data[column]);
            } else if (column === 'date') {
                cell.textContent = formatDate(data[column]);
            } else {
                cell.textContent = data[column] || '';
            }
            
            row.appendChild(cell);
        });

        // Add actions column if provided
        if (actions.length > 0) {
            const actionsCell = document.createElement('td');
            const actionsContainer = document.createElement('div');
            actionsContainer.className = 'table-actions';
            
            actions.forEach(action => {
                const button = this.createActionButton(
                    action.text, 
                    action.className, 
                    () => action.onClick(data)
                );
                actionsContainer.appendChild(button);
            });
            
            actionsCell.appendChild(actionsContainer);
            row.appendChild(actionsCell);
        }

        return row;
    }

    /**
     * Populate table with data
     */
    static populateTable(tableId, data, columns, actions = []) {
        const tbody = document.querySelector(`#${tableId} tbody`);
        if (!tbody) return;

        // Clear existing rows
        tbody.innerHTML = '';

        // Add new rows
        data.forEach(item => {
            const row = this.createTableRow(item, columns, actions);
            tbody.appendChild(row);
        });

        // Add fade-in animation
        tbody.classList.add('fade-in');
    }

    /**
     * Handle form submission with validation
     */
    static handleFormSubmit(formId, onSubmit, onValidationError) {
        const form = document.getElementById(formId);
        if (!form) return;

        form.addEventListener('submit', async (e) => {
            e.preventDefault();
            
            const formData = new FormData(form);
            const data = Object.fromEntries(formData.entries());
            
            // Basic validation
            const errors = validateRecord(data);
            if (errors.length > 0) {
                if (onValidationError) {
                    onValidationError(errors);
                } else {
                    this.showNotification(errors.join('\n'), 'error');
                }
                return;
            }

            try {
                this.showLoading('Processing...');
                await onSubmit(data);
                form.reset();
            } catch (error) {
                this.showNotification('An error occurred: ' + error.message, 'error');
            } finally {
                this.hideLoading();
            }
        });
    }

    /**
     * Setup file upload handling
     */
    static setupFileUpload(inputId, onFileSelect, onUpload) {
        const fileInput = document.getElementById(inputId);
        const selectBtn = document.getElementById('selectFileBtn');
        const uploadBtn = document.getElementById('uploadBtn');
        const fileInfo = document.getElementById('fileInfo');

        if (!fileInput || !selectBtn) return;

        selectBtn.addEventListener('click', () => {
            fileInput.click();
        });

        fileInput.addEventListener('change', (e) => {
            const file = e.target.files[0];
            if (file) {
                fileInfo.textContent = `Archivo: ${file.name}`;
                if (uploadBtn) uploadBtn.disabled = false;
                if (onFileSelect) onFileSelect(file);
            } else {
                fileInfo.textContent = 'Ningún archivo seleccionado';
                if (uploadBtn) uploadBtn.disabled = true;
            }
        });

        if (uploadBtn && onUpload) {
            uploadBtn.addEventListener('click', () => {
                const file = fileInput.files[0];
                if (file) {
                    onUpload(file);
                }
            });
        }
    }

    /**
     * Setup modal functionality
     */
    static setupModal(modalId, openTriggers = [], closeTriggers = []) {
        const modal = document.getElementById(modalId);
        if (!modal) return;

        // Open modal
        openTriggers.forEach(triggerId => {
            const trigger = document.getElementById(triggerId);
            if (trigger) {
                trigger.addEventListener('click', () => {
                    modal.classList.add('active');
                    document.body.style.overflow = 'hidden';
                });
            }
        });

        // Close modal
        closeTriggers.forEach(triggerId => {
            const trigger = document.getElementById(triggerId);
            if (trigger) {
                trigger.addEventListener('click', () => {
                    modal.classList.remove('active');
                    document.body.style.overflow = '';
                });
            }
        });

        // Close on overlay click
        modal.addEventListener('click', (e) => {
            if (e.target === modal) {
                modal.classList.remove('active');
                document.body.style.overflow = '';
            }
        });

        // Close on Escape key
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape' && modal.classList.contains('active')) {
                modal.classList.remove('active');
                document.body.style.overflow = '';
            }
        });
    }

    /**
     * Setup checkbox selection
     */
    static setupCheckboxSelection(tableId, onSelectionChange) {
        const table = document.getElementById(tableId);
        if (!table) return;

        const selectAllCheckbox = table.querySelector('#selectAll');
        
        // Handle select all
        if (selectAllCheckbox) {
            selectAllCheckbox.addEventListener('change', (e) => {
                const checkboxes = table.querySelectorAll('tbody input[type="checkbox"]');
                checkboxes.forEach(checkbox => {
                    checkbox.checked = e.target.checked;
                });
                
                if (onSelectionChange) {
                    const selectedIds = Array.from(checkboxes)
                        .filter(cb => cb.checked)
                        .map(cb => cb.value);
                    onSelectionChange(selectedIds);
                }
            });
        }

        // Handle individual checkboxes
        table.addEventListener('change', (e) => {
            if (e.target.type === 'checkbox' && e.target !== selectAllCheckbox) {
                const checkboxes = table.querySelectorAll('tbody input[type="checkbox"]');
                const checkedBoxes = table.querySelectorAll('tbody input[type="checkbox"]:checked');
                
                // Update select all checkbox
                if (selectAllCheckbox) {
                    selectAllCheckbox.checked = checkboxes.length === checkedBoxes.length;
                    selectAllCheckbox.indeterminate = checkedBoxes.length > 0 && checkedBoxes.length < checkboxes.length;
                }
                
                if (onSelectionChange) {
                    const selectedIds = Array.from(checkedBoxes).map(cb => cb.value);
                    onSelectionChange(selectedIds);
                }
            }
        });
    }

    /**
     * Debounce function for search inputs
     */
    static debounce(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    }

    /**
     * Setup search functionality
     */
    static setupSearch(inputId, onSearch, debounceMs = 300) {
        const input = document.getElementById(inputId);
        if (!input) return;

        const debouncedSearch = this.debounce(onSearch, debounceMs);
        
        input.addEventListener('input', (e) => {
            debouncedSearch(e.target.value);
        });
    }
}

// Make UIComponents globally available
window.UIComponents = UIComponents;
