/**
 * Custom Export Manager
 * Handles advanced CSV export functionality with field selection and customization
 */

class CustomExportManager {
    constructor() {
        this.availableFields = this.getAvailableFields();
        this.selectedFields = [];
        this.combinedColumns = [];
        this.currentEditingCombined = null;
        
        this.init();
    }

    init() {
        this.setupEventListeners();
        this.populateAvailableFields();
        this.setupDragAndDrop();
    }

    getAvailableFields() {
        return [
            { key: 'id', label: 'ID del Proyecto', type: 'number' },
            { key: 'contrato', label: 'Contrato', type: 'text' },
            { key: 'cliente', label: 'Cliente', type: 'text' },
            { key: 'fecha_inicio', label: 'Fecha de Inicio', type: 'date' },
            { key: 'fecha_termino', label: 'Fecha de Término', type: 'date' },
            { key: 'duracion', label: 'Duración (días)', type: 'number' },
            { key: 'region', label: 'Región', type: 'text' },
            { key: 'ciudad', label: 'Ciudad', type: 'text' },
            { key: 'estado', label: 'Estado', type: 'text' },
            { key: 'monto', label: 'Monto', type: 'number' },
            { key: 'rut_cliente', label: 'RUT Cliente', type: 'text' },
            { key: 'tipo_cliente', label: 'Tipo de Cliente', type: 'text' },
            { key: 'persona_contacto', label: 'Persona de Contacto', type: 'text' },
            { key: 'telefono_contacto', label: 'Teléfono de Contacto', type: 'text' },
            { key: 'correo_contacto', label: 'Correo de Contacto', type: 'text' },
            { key: 'superficie_terreno', label: 'Superficie de Terreno', type: 'number' },
            { key: 'superficie_construida', label: 'Superficie Construida', type: 'number' },
            { key: 'tipo_obra_lista', label: 'Tipo de Obra', type: 'text' },
            { key: 'ems', label: 'EMS', type: 'boolean' },
            { key: 'estudio_sismico', label: 'Estudio Sísmico', type: 'boolean' },
            { key: 'estudio_geoelectrico', label: 'Estudio Geoeléctrico', type: 'boolean' },
            { key: 'topografia', label: 'Topografía', type: 'boolean' },
            { key: 'sondaje', label: 'Sondaje', type: 'boolean' },
            { key: 'hidraulica_hidrologia', label: 'Hidráulica/Hidrología', type: 'boolean' },
            { key: 'descripcion', label: 'Descripción', type: 'text' },
            { key: 'certificado_experiencia', label: 'Certificado de Experiencia', type: 'boolean' },
            { key: 'orden_compra', label: 'Orden de Compra', type: 'boolean' },
            { key: 'contrato_doc', label: 'Contrato Documento', type: 'boolean' },
            { key: 'factura', label: 'Factura', type: 'boolean' },
            { key: 'fecha_factura', label: 'Fecha de Factura', type: 'date' },
            { key: 'numero_factura', label: 'Número de Factura', type: 'text' },
            { key: 'numero_orden_compra', label: 'Número de Orden de Compra', type: 'text' },
            { key: 'link_documentos', label: 'Link de Documentos', type: 'text' }
        ];
    }

    setupEventListeners() {
        // Main export buttons
        document.getElementById('exportCsvBtn')?.addEventListener('click', () => {
            this.exportDefaultCSV();
        });

        document.getElementById('customExportBtn')?.addEventListener('click', () => {
            this.openCustomExportModal();
        });

        // Modal controls
        document.getElementById('closeCustomExportModal')?.addEventListener('click', () => {
            this.closeCustomExportModal();
        });

        document.getElementById('cancelCustomExport')?.addEventListener('click', () => {
            this.closeCustomExportModal();
        });

        document.getElementById('executeCustomExport')?.addEventListener('click', () => {
            this.executeCustomExport();
        });

        // Field search
        document.getElementById('fieldSearch')?.addEventListener('input', (e) => {
            this.filterAvailableFields(e.target.value);
        });

        // Selected fields actions
        document.getElementById('clearSelectedFields')?.addEventListener('click', () => {
            this.clearSelectedFields();
        });

        document.getElementById('addCombinedColumn')?.addEventListener('click', () => {
            this.openCombinedColumnModal();
        });

        // Combined column modal
        document.getElementById('closeCombinedColumnModal')?.addEventListener('click', () => {
            this.closeCombinedColumnModal();
        });

        document.getElementById('cancelCombinedColumn')?.addEventListener('click', () => {
            this.closeCombinedColumnModal();
        });

        document.getElementById('createCombinedColumn')?.addEventListener('click', () => {
            this.createCombinedColumn();
        });

        // Custom separator toggle
        document.getElementById('combinedColumnSeparator')?.addEventListener('change', (e) => {
            const customGroup = document.getElementById('customSeparatorGroup');
            if (e.target.value === 'custom') {
                customGroup.style.display = 'block';
            } else {
                customGroup.style.display = 'none';
            }
        });

        // Close modals on overlay click
        document.getElementById('customExportModal')?.addEventListener('click', (e) => {
            if (e.target.id === 'customExportModal') {
                this.closeCustomExportModal();
            }
        });

        document.getElementById('combinedColumnModal')?.addEventListener('click', (e) => {
            if (e.target.id === 'combinedColumnModal') {
                this.closeCombinedColumnModal();
            }
        });
    }

    populateAvailableFields() {
        const container = document.getElementById('availableFieldsList');
        if (!container) return;

        container.innerHTML = '';
        
        this.availableFields.forEach(field => {
            const fieldElement = this.createFieldElement(field);
            container.appendChild(fieldElement);
        });
    }

    createFieldElement(field, isSelected = false) {
        const div = document.createElement('div');
        div.className = 'field-item';
        div.draggable = true;
        div.dataset.fieldKey = field.key;

        div.innerHTML = `
            <div>
                <span class="field-name">${field.label}</span>
                <span class="field-label type-${field.type}">${field.type}</span>
            </div>
            ${!isSelected ? `<button class="add-btn" data-field-key="${field.key}">Agregar</button>` : ''}
        `;

        // Add event listener to add button
        const addBtn = div.querySelector('.add-btn');
        if (addBtn) {
            addBtn.addEventListener('click', (e) => {
                e.stopPropagation();
                this.addField(field.key);
            });
        }

        // Drag events
        div.addEventListener('dragstart', (e) => {
            e.dataTransfer.setData('text/plain', field.key);
            div.classList.add('dragging');
        });

        div.addEventListener('dragend', () => {
            div.classList.remove('dragging');
        });

        return div;
    }

    addField(fieldKey) {
        const field = this.availableFields.find(f => f.key === fieldKey);
        if (!field || this.selectedFields.find(f => f.key === fieldKey)) return;

        const newField = {
            ...field,
            id: Date.now() + Math.random(),
            type: 'single'
        };

        this.selectedFields.push(newField);
        this.updateSelectedFieldsList();

        // Add animation to newly added field
        setTimeout(() => {
            const fieldElement = document.querySelector(`[data-field-id="${newField.id}"]`);
            if (fieldElement) {
                fieldElement.classList.add('newly-added');
                setTimeout(() => {
                    fieldElement.classList.remove('newly-added');
                }, 300);
            }
        }, 50);
    }

    removeField(fieldId) {
        this.selectedFields = this.selectedFields.filter(f => f.id !== fieldId);
        this.updateSelectedFieldsList();
    }

    updateSelectedFieldsList() {
        const container = document.getElementById('selectedFieldsList');
        if (!container) return;

        if (this.selectedFields.length === 0) {
            container.innerHTML = `
                <div class="empty-selection">
                    <p>Arrastra campos aquí o haz clic en "Agregar" para seleccionar campos</p>
                </div>
            `;
            return;
        }

        container.innerHTML = '';
        
        this.selectedFields.forEach((field, index) => {
            const fieldElement = this.createSelectedFieldElement(field, index);
            container.appendChild(fieldElement);
        });
    }

    createSelectedFieldElement(field, index) {
        const div = document.createElement('div');
        div.className = `selected-field-item ${field.type === 'combined' ? 'combined-column' : ''}`;
        div.dataset.fieldId = field.id;
        div.draggable = true;

        let fieldDetails = '';
        if (field.type === 'combined') {
            fieldDetails = `Campos: ${field.fields.map(f => f.label).join(', ')} | Separador: "${field.separator}"`;
        } else {
            fieldDetails = `Tipo: ${field.type}`;
        }

        div.innerHTML = `
            <div class="field-info">
                <div class="field-name">${field.label}</div>
                <div class="field-details">${fieldDetails}</div>
            </div>
            <div class="field-actions">
                ${field.type === 'combined' ? `<button class="edit-btn" data-field-id="${field.id}" data-action="edit">Editar</button>` : ''}
                <button class="remove-btn" data-field-id="${field.id}" data-action="remove">Quitar</button>
            </div>
        `;

        // Add event listeners to buttons
        const editBtn = div.querySelector('.edit-btn');
        const removeBtn = div.querySelector('.remove-btn');

        if (editBtn) {
            editBtn.addEventListener('click', (e) => {
                e.stopPropagation();
                this.editCombinedColumn(field.id);
            });
        }

        if (removeBtn) {
            removeBtn.addEventListener('click', (e) => {
                e.stopPropagation();
                this.removeField(field.id);
            });
        }

        return div;
    }

    setupDragAndDrop() {
        // Setup drag and drop for available fields to selected fields
        const availableFieldsList = document.getElementById('availableFieldsList');
        const selectedFieldsList = document.getElementById('selectedFieldsList');

        if (availableFieldsList && selectedFieldsList) {
            // Make selected fields list sortable
            this.selectedSortable = Sortable.create(selectedFieldsList, {
                group: 'fields',
                animation: 200,
                ghostClass: 'sortable-ghost',
                chosenClass: 'sortable-chosen',
                dragClass: 'sortable-drag',
                forceFallback: true,
                fallbackClass: 'sortable-drag',
                fallbackOnBody: true,
                swapThreshold: 0.65,
                onAdd: (evt) => {
                    const fieldKey = evt.item.dataset.fieldKey;
                    if (fieldKey) {
                        this.addField(fieldKey);
                        evt.item.remove(); // Remove the dragged element
                    }
                },
                onUpdate: (evt) => {
                    // Reorder selected fields
                    const newOrder = Array.from(selectedFieldsList.children)
                        .map(item => item.dataset.fieldId)
                        .filter(id => id);

                    this.reorderSelectedFields(newOrder);
                },
                onStart: (evt) => {
                    evt.item.classList.add('dragging');
                    selectedFieldsList.classList.add('drag-active');
                },
                onEnd: (evt) => {
                    evt.item.classList.remove('dragging');
                    selectedFieldsList.classList.remove('drag-active');
                },
                onMove: (evt) => {
                    // Add visual feedback when hovering over drop zone
                    if (evt.to === selectedFieldsList) {
                        selectedFieldsList.classList.add('drag-over');
                    } else {
                        selectedFieldsList.classList.remove('drag-over');
                    }
                }
            });

            // Make available fields draggable to selected list
            Sortable.create(availableFieldsList, {
                group: {
                    name: 'fields',
                    pull: 'clone',
                    put: false
                },
                sort: false,
                animation: 200,
                ghostClass: 'sortable-ghost',
                chosenClass: 'sortable-chosen',
                dragClass: 'sortable-drag',
                forceFallback: true,
                fallbackClass: 'sortable-drag',
                fallbackOnBody: true,
                onStart: (evt) => {
                    evt.item.classList.add('dragging');
                    selectedFieldsList.classList.add('drag-active');
                },
                onEnd: (evt) => {
                    evt.item.classList.remove('dragging');
                    selectedFieldsList.classList.remove('drag-active');
                    selectedFieldsList.classList.remove('drag-over');
                }
            });
        }
    }

    reorderSelectedFields(newOrder) {
        const reorderedFields = [];
        newOrder.forEach(fieldId => {
            const field = this.selectedFields.find(f => f.id == fieldId);
            if (field) {
                reorderedFields.push(field);
            }
        });
        this.selectedFields = reorderedFields;
        this.updateSelectedFieldsList();
    }

    filterAvailableFields(searchTerm) {
        const container = document.getElementById('availableFieldsList');
        const fields = container.querySelectorAll('.field-item');
        
        fields.forEach(field => {
            const fieldName = field.querySelector('.field-name').textContent.toLowerCase();
            const fieldLabel = field.querySelector('.field-label').textContent.toLowerCase();
            
            if (fieldName.includes(searchTerm.toLowerCase()) || fieldLabel.includes(searchTerm.toLowerCase())) {
                field.style.display = 'flex';
            } else {
                field.style.display = 'none';
            }
        });
    }

    clearSelectedFields() {
        this.selectedFields = [];
        this.updateSelectedFieldsList();
    }

    openCustomExportModal() {
        document.getElementById('customExportModal').classList.add('active');
        document.body.style.overflow = 'hidden';
        this.updateSelectedFieldsList();

        // Reinitialize drag and drop after modal is shown
        setTimeout(() => {
            this.setupDragAndDrop();
        }, 100);
    }

    closeCustomExportModal() {
        document.getElementById('customExportModal').classList.remove('active');
        document.body.style.overflow = '';
    }

    openCombinedColumnModal() {
        this.populateCombinedFieldsSelection();
        document.getElementById('combinedColumnModal').classList.add('active');
    }

    closeCombinedColumnModal() {
        document.getElementById('combinedColumnModal').classList.remove('active');
        this.currentEditingCombined = null;
        // Reset form
        document.getElementById('combinedColumnName').value = '';
        document.getElementById('combinedColumnSeparator').value = ' - ';
        document.getElementById('customSeparatorGroup').style.display = 'none';
    }

    populateCombinedFieldsSelection() {
        const container = document.getElementById('combinedFieldsSelection');
        if (!container) return;

        container.innerHTML = '';
        
        this.availableFields.forEach(field => {
            const div = document.createElement('div');
            div.className = 'combined-field-option';
            
            div.innerHTML = `
                <input type="checkbox" id="combined_${field.key}" value="${field.key}">
                <label for="combined_${field.key}">${field.label}</label>
            `;
            
            container.appendChild(div);
        });
    }

    createCombinedColumn() {
        const name = document.getElementById('combinedColumnName').value.trim();
        const separatorSelect = document.getElementById('combinedColumnSeparator').value;
        const customSeparator = document.getElementById('customSeparator').value;
        
        const separator = separatorSelect === 'custom' ? customSeparator : separatorSelect;
        
        if (!name) {
            alert('Por favor ingresa un nombre para la columna');
            return;
        }

        const selectedFieldKeys = Array.from(document.querySelectorAll('#combinedFieldsSelection input:checked'))
            .map(input => input.value);

        if (selectedFieldKeys.length < 2) {
            alert('Selecciona al menos 2 campos para combinar');
            return;
        }

        const selectedFields = selectedFieldKeys.map(key => 
            this.availableFields.find(f => f.key === key)
        );

        const combinedField = {
            id: Date.now() + Math.random(),
            key: `combined_${Date.now()}`,
            label: name,
            type: 'combined',
            fields: selectedFields,
            separator: separator
        };

        if (this.currentEditingCombined) {
            // Edit existing
            const index = this.selectedFields.findIndex(f => f.id === this.currentEditingCombined);
            if (index !== -1) {
                this.selectedFields[index] = { ...combinedField, id: this.currentEditingCombined };
            }
        } else {
            // Add new
            this.selectedFields.push(combinedField);
        }

        this.updateSelectedFieldsList();
        this.closeCombinedColumnModal();
    }

    editCombinedColumn(fieldId) {
        const field = this.selectedFields.find(f => f.id === fieldId);
        if (!field || field.type !== 'combined') return;

        this.currentEditingCombined = fieldId;
        
        // Populate form with existing data
        document.getElementById('combinedColumnName').value = field.label;
        document.getElementById('combinedColumnSeparator').value = field.separator;
        
        this.populateCombinedFieldsSelection();
        
        // Check the fields that are part of this combined column
        field.fields.forEach(f => {
            const checkbox = document.getElementById(`combined_${f.key}`);
            if (checkbox) checkbox.checked = true;
        });

        this.openCombinedColumnModal();
    }

    exportDefaultCSV() {
        if (!window.mainPage || !window.mainPage.filteredProjects) {
            alert('No hay datos para exportar');
            return;
        }

        const projects = window.mainPage.filteredProjects;
        const headers = this.availableFields.map(f => f.label);
        const rows = projects.map(project => 
            this.availableFields.map(field => this.formatFieldValue(project[field.key], field.type))
        );

        this.downloadCSV([headers, ...rows], 'proyectos_filtrados');
    }

    executeCustomExport() {
        if (this.selectedFields.length === 0) {
            alert('Selecciona al menos un campo para exportar');
            return;
        }

        if (!window.mainPage || !window.mainPage.filteredProjects) {
            alert('No hay datos para exportar');
            return;
        }

        // Show loading state
        const modal = document.getElementById('customExportModal');
        modal.classList.add('export-loading');

        // Use setTimeout to allow UI to update
        setTimeout(() => {
            try {
                const projects = window.mainPage.filteredProjects;
                const orientation = document.querySelector('input[name="dataOrientation"]:checked').value;
                const booleanFormat = document.getElementById('booleanFormat').value;
                const dateFormat = document.getElementById('dateFormat').value;
                const fileName = document.getElementById('fileName').value.trim() || 'proyectos_filtrados';

                let csvData;

                if (orientation === 'columns') {
                    csvData = this.generateColumnOrientedCSV(projects, booleanFormat, dateFormat);
                } else {
                    csvData = this.generateRowOrientedCSV(projects, booleanFormat, dateFormat);
                }

                this.downloadCSV(csvData, fileName);

                // Show success message
                this.showExportSuccess(projects.length, this.selectedFields.length);

            } catch (error) {
                console.error('Error during export:', error);
                alert('Error al generar el archivo. Por favor intenta nuevamente.');
            } finally {
                // Remove loading state
                modal.classList.remove('export-loading');
                this.closeCustomExportModal();
            }
        }, 100);
    }

    showExportSuccess(projectCount, fieldCount) {
        // You can integrate this with your existing notification system
        if (window.UIComponents && window.UIComponents.showNotification) {
            window.UIComponents.showNotification(
                `Archivo exportado exitosamente: ${projectCount} proyectos con ${fieldCount} campos`,
                'success'
            );
        } else {
            alert(`Archivo exportado exitosamente: ${projectCount} proyectos con ${fieldCount} campos`);
        }
    }

    generateColumnOrientedCSV(projects, booleanFormat, dateFormat) {
        const headers = this.selectedFields.map(field => field.label);
        const rows = projects.map(project => 
            this.selectedFields.map(field => this.getFieldValue(project, field, booleanFormat, dateFormat))
        );

        return [headers, ...rows];
    }

    generateRowOrientedCSV(projects, booleanFormat, dateFormat) {
        // No headers, just the data rows where each field is a row
        const rows = this.selectedFields.map(field => [
            field.label,
            ...projects.map(project => this.getFieldValue(project, field, booleanFormat, dateFormat))
        ]);

        return rows;
    }

    getFieldValue(project, field, booleanFormat, dateFormat) {
        if (field.type === 'combined') {
            return field.fields
                .map(f => this.formatFieldValue(project[f.key], f.type, booleanFormat, dateFormat))
                .join(field.separator);
        } else {
            return this.formatFieldValue(project[field.key], field.type, booleanFormat, dateFormat);
        }
    }

    formatFieldValue(value, type, booleanFormat = 'si-no', dateFormat = 'dd-mm-yyyy') {
        if (value === null || value === undefined || value === '') {
            return '';
        }

        switch (type) {
            case 'boolean':
                return this.formatBoolean(value, booleanFormat);
            case 'date':
                return this.formatDate(value, dateFormat);
            case 'number':
                return typeof value === 'number' ? value.toString() : value;
            default:
                return value.toString();
        }
    }

    formatBoolean(value, format) {
        const formats = {
            'si-no': value ? 'Sí' : 'No',
            'check-x': value ? '✓' : '✗',
            'true-false': value ? 'true' : 'false',
            '1-0': value ? '1' : '0'
        };
        return formats[format] || (value ? 'Sí' : 'No');
    }

    formatDate(value, format) {
        if (!value) return '';
        
        const date = new Date(value);
        if (isNaN(date.getTime())) return value;

        const day = date.getDate().toString().padStart(2, '0');
        const month = (date.getMonth() + 1).toString().padStart(2, '0');
        const year = date.getFullYear();

        const formats = {
            'dd-mm-yyyy': `${day}-${month}-${year}`,
            'mm-dd-yyyy': `${month}-${day}-${year}`,
            'yyyy-mm-dd': `${year}-${month}-${day}`,
            'dd/mm/yyyy': `${day}/${month}/${year}`,
            'mm/dd/yyyy': `${month}/${day}/${year}`
        };

        return formats[format] || `${day}-${month}-${year}`;
    }

    downloadCSV(data, fileName) {
        const csvContent = data.map(row => 
            row.map(cell => {
                // Escape quotes and wrap in quotes if necessary
                const cellStr = cell.toString();
                if (cellStr.includes(',') || cellStr.includes('"') || cellStr.includes('\n')) {
                    return `"${cellStr.replace(/"/g, '""')}"`;
                }
                return cellStr;
            }).join(',')
        ).join('\n');

        const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
        const link = document.createElement('a');
        
        if (link.download !== undefined) {
            const url = URL.createObjectURL(blob);
            link.setAttribute('href', url);
            
            const today = new Date();
            const dateStr = today.toISOString().split('T')[0].split('-').reverse().join('-');
            link.setAttribute('download', `${fileName}_${dateStr}.csv`);
            
            link.style.visibility = 'hidden';
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
        }
    }
}

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.customExportManager = new CustomExportManager();
});
