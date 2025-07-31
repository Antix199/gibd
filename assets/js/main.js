/**
 * Main Page JavaScript - Sistema de Gestión de Proyectos GlaciarIng
 * Funcionalidades completas de filtrado y visualización
 */

class MainPage {
    constructor() {
        this.allProjects = [];
        this.filteredProjects = [];
        this.currentPage = 1;
        this.projectsPerPage = 50;
        
        this.currentFilters = {
            search: '',
            id: '',
            contrato: '',
            cliente: '',
            estado: '',
            region: '',
            ciudad: '',
            fechaInicioDesde: '',
            fechaInicioHasta: '',
            fechaTerminoDesde: '',
            fechaTerminoHasta: '',
            montoDesde: '',
            montoHasta: ''
        };
        
        this.init();
    }

    async init() {
        console.log('🏗️ Inicializando MainPage...');
        this.setupEventListeners();
        await this.loadAllProjects();
        this.applyFiltersAndDisplay();
        console.log('✅ MainPage inicializada correctamente');
    }

    setupEventListeners() {
        // Toggle filters visibility
        const toggleFilters = document.getElementById('toggleFilters');
        if (toggleFilters) {
            toggleFilters.addEventListener('click', () => {
                const filtersContainer = document.getElementById('filtersContainer');
                if (filtersContainer) {
                    filtersContainer.classList.toggle('hidden');
                }
            });
        }

        // Apply filters button
        const applyFiltersBtn = document.getElementById('applyFiltersBtn');
        if (applyFiltersBtn) {
            applyFiltersBtn.addEventListener('click', () => {
                this.collectFiltersAndApply();
            });
        }

        // Clear filters button
        const clearFiltersBtn = document.getElementById('clearFiltersBtn');
        if (clearFiltersBtn) {
            clearFiltersBtn.addEventListener('click', () => {
                this.clearAllFilters();
            });
        }

        // Export filtered button
        const exportFilteredBtn = document.getElementById('exportFilteredBtn');
        if (exportFilteredBtn) {
            exportFilteredBtn.addEventListener('click', () => {
                this.exportFilteredData();
            });
        }

        // Real-time search on main search box
        const searchInput = document.getElementById('searchInput');
        if (searchInput) {
            searchInput.addEventListener('input', (e) => {
                this.currentFilters.search = e.target.value.trim();
                this.applyFiltersAndDisplay();
            });
        }

        // Enter key on filter inputs for quick apply
        const filterInputs = [
            'idFilter', 'contratoFilter', 'clienteFilter', 'regionFilter', 'ciudadFilter',
            'fechaInicioDesde', 'fechaInicioHasta', 'fechaTerminoDesde', 'fechaTerminoHasta',
            'montoDesde', 'montoHasta'
        ];

        filterInputs.forEach(inputId => {
            const input = document.getElementById(inputId);
            if (input) {
                input.addEventListener('keypress', (e) => {
                    if (e.key === 'Enter') {
                        this.collectFiltersAndApply();
                    }
                });
            }
        });

        // Auto-apply on select change
        const estadoFilter = document.getElementById('estadoFilter');
        if (estadoFilter) {
            estadoFilter.addEventListener('change', () => {
                this.collectFiltersAndApply();
            });
        }
    }

    async loadAllProjects() {
        try {
            console.log('📡 Cargando todos los proyectos...');
            UIComponents.showLoading('Cargando proyectos...');

            const response = await fetch('/api/proyectos');
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const result = await response.json();
            this.allProjects = result.data || [];
            
            console.log('✅ Proyectos cargados:', this.allProjects.length);
            UIComponents.hideLoading();

        } catch (error) {
            console.error('❌ Error cargando proyectos:', error);
            UIComponents.showNotification('Error cargando proyectos', 'error');
            UIComponents.hideLoading();
        }
    }

    collectFiltersAndApply() {
        // Recopilar todos los valores de filtros
        this.currentFilters.id = document.getElementById('idFilter')?.value.trim() || '';
        this.currentFilters.contrato = document.getElementById('contratoFilter')?.value.trim() || '';
        this.currentFilters.cliente = document.getElementById('clienteFilter')?.value.trim() || '';
        this.currentFilters.estado = document.getElementById('estadoFilter')?.value || '';
        this.currentFilters.region = document.getElementById('regionFilter')?.value.trim() || '';
        this.currentFilters.ciudad = document.getElementById('ciudadFilter')?.value.trim() || '';
        this.currentFilters.fechaInicioDesde = document.getElementById('fechaInicioDesde')?.value || '';
        this.currentFilters.fechaInicioHasta = document.getElementById('fechaInicioHasta')?.value || '';
        this.currentFilters.fechaTerminoDesde = document.getElementById('fechaTerminoDesde')?.value || '';
        this.currentFilters.fechaTerminoHasta = document.getElementById('fechaTerminoHasta')?.value || '';
        this.currentFilters.montoDesde = document.getElementById('montoDesde')?.value || '';
        this.currentFilters.montoHasta = document.getElementById('montoHasta')?.value || '';

        console.log('🔍 Filtros aplicados:', this.currentFilters);
        this.applyFiltersAndDisplay();
        UIComponents.showNotification('Filtros aplicados exitosamente', 'success');
    }

    applyFiltersAndDisplay() {
        this.filteredProjects = this.allProjects.filter(project => {
            return this.matchesAllFilters(project);
        });

        console.log('📊 Proyectos filtrados:', this.filteredProjects.length, 'de', this.allProjects.length);
        this.displayProjects();
        this.updateStatistics();
    }

    matchesAllFilters(project) {
        // Búsqueda general (ID, contrato, cliente)
        if (this.currentFilters.search) {
            const searchTerm = this.currentFilters.search.toLowerCase();
            const searchMatch = 
                (project.id && project.id.toString().toLowerCase().includes(searchTerm)) ||
                (project.contrato && project.contrato.toLowerCase().includes(searchTerm)) ||
                (project.cliente && project.cliente.toLowerCase().includes(searchTerm));
            
            if (!searchMatch) return false;
        }

        // Filtro por ID específico
        if (this.currentFilters.id && project.id) {
            if (!project.id.toString().toLowerCase().includes(this.currentFilters.id.toLowerCase())) {
                return false;
            }
        }

        // Filtro por contrato
        if (this.currentFilters.contrato && project.contrato) {
            if (!project.contrato.toLowerCase().includes(this.currentFilters.contrato.toLowerCase())) {
                return false;
            }
        }

        // Filtro por cliente
        if (this.currentFilters.cliente && project.cliente) {
            if (!project.cliente.toLowerCase().includes(this.currentFilters.cliente.toLowerCase())) {
                return false;
            }
        }

        // Filtro por estado
        if (this.currentFilters.estado && project.estado !== this.currentFilters.estado) {
            return false;
        }

        // Filtro por región
        if (this.currentFilters.region && project.region) {
            if (!project.region.toLowerCase().includes(this.currentFilters.region.toLowerCase())) {
                return false;
            }
        }

        // Filtro por ciudad
        if (this.currentFilters.ciudad && project.ciudad) {
            if (!project.ciudad.toLowerCase().includes(this.currentFilters.ciudad.toLowerCase())) {
                return false;
            }
        }

        // Filtros de fecha de inicio
        if (this.currentFilters.fechaInicioDesde || this.currentFilters.fechaInicioHasta) {
            const fechaInicio = project.fecha_inicio ? new Date(project.fecha_inicio) : null;
            
            if (this.currentFilters.fechaInicioDesde) {
                const fechaDesde = new Date(this.currentFilters.fechaInicioDesde);
                if (!fechaInicio || fechaInicio < fechaDesde) {
                    return false;
                }
            }
            
            if (this.currentFilters.fechaInicioHasta) {
                const fechaHasta = new Date(this.currentFilters.fechaInicioHasta);
                if (!fechaInicio || fechaInicio > fechaHasta) {
                    return false;
                }
            }
        }

        // Filtros de fecha de término
        if (this.currentFilters.fechaTerminoDesde || this.currentFilters.fechaTerminoHasta) {
            const fechaTermino = project.fecha_termino ? new Date(project.fecha_termino) : null;
            
            if (this.currentFilters.fechaTerminoDesde) {
                const fechaDesde = new Date(this.currentFilters.fechaTerminoDesde);
                if (!fechaTermino || fechaTermino < fechaDesde) {
                    return false;
                }
            }
            
            if (this.currentFilters.fechaTerminoHasta) {
                const fechaHasta = new Date(this.currentFilters.fechaTerminoHasta);
                if (!fechaTermino || fechaTermino > fechaHasta) {
                    return false;
                }
            }
        }

        // Filtros de monto
        if (this.currentFilters.montoDesde || this.currentFilters.montoHasta) {
            const monto = parseFloat(project.monto) || 0;
            
            if (this.currentFilters.montoDesde) {
                const montoDesde = parseFloat(this.currentFilters.montoDesde);
                if (monto < montoDesde) {
                    return false;
                }
            }
            
            if (this.currentFilters.montoHasta) {
                const montoHasta = parseFloat(this.currentFilters.montoHasta);
                if (monto > montoHasta) {
                    return false;
                }
            }
        }

        return true;
    }

    displayProjects() {
        const tableBody = document.getElementById('tableBody');
        if (!tableBody) {
            console.error('❌ Elemento tableBody no encontrado');
            return;
        }

        tableBody.innerHTML = '';

        if (this.filteredProjects.length === 0) {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td colspan="30" class="text-center" style="padding: 2rem; color: #666;">
                    <i class="fas fa-search" style="font-size: 2rem; margin-bottom: 1rem; display: block;"></i>
                    No se encontraron proyectos con los filtros aplicados
                </td>
            `;
            tableBody.appendChild(row);
            return;
        }

        // Mostrar todos los proyectos filtrados (sin paginación)
        this.filteredProjects.forEach(project => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${project.id || 'N/A'}</td>
                <td class="long-text">${project.contrato || 'N/A'}</td>
                <td class="long-text">${project.cliente || 'N/A'}</td>
                <td>${this.formatDate(project.fecha_inicio)}</td>
                <td>${this.formatDate(project.fecha_termino)}</td>
                <td>${project.region || 'N/A'}</td>
                <td>${project.ciudad || 'N/A'}</td>
                <td><span class="status-badge status-${(project.estado || 'pendiente').toLowerCase()}">${project.estado || 'Pendiente'}</span></td>
                <td class="text-right">$${this.formatNumber(project.monto || 0)}</td>
                <td>${project.rut_cliente || 'N/A'}</td>
                <td>${project.tipo_cliente || 'N/A'}</td>
                <td>${project.persona_contacto || 'N/A'}</td>
                <td>${project.telefono_contacto || 'N/A'}</td>
                <td>${project.correo_contacto || 'N/A'}</td>
                <td>${project.superficie_terreno ? project.superficie_terreno.toLocaleString() + ' m²' : 'N/A'}</td>
                <td>${project.superficie_construida ? project.superficie_construida.toLocaleString() + ' m²' : 'N/A'}</td>
                <td>${project.tipo_obra_lista || 'N/A'}</td>
                <td>${project.ems ? '✓' : '✗'}</td>
                <td>${project.estudio_sismico ? '✓' : '✗'}</td>
                <td>${project.estudio_geoelectrico ? '✓' : '✗'}</td>
                <td>${project.topografia ? '✓' : '✗'}</td>
                <td>${project.sondaje ? '✓' : '✗'}</td>
                <td>${project.hidraulica_hidrologia ? '✓' : '✗'}</td>
                <td class="description-cell">${project.descripcion || 'N/A'}</td>
                <td>${project.certificado_experiencia ? '✓' : '✗'}</td>
                <td>${project.orden_compra ? '✓' : '✗'}</td>
                <td>${project.contrato_doc ? '✓' : '✗'}</td>
                <td>${project.factura ? '✓' : '✗'}</td>
                <td>${project.numero_factura || 'N/A'}</td>
                <td>${project.numero_orden_compra || 'N/A'}</td>
            `;
            tableBody.appendChild(row);
        });

        // Ya no necesitamos paginación, pero mantenemos las estadísticas
        this.hidePagination();
    }

    updateStatistics() {
        // Actualizar contadores
        const totalProjects = document.getElementById('totalProjects');
        const filteredCount = document.getElementById('filteredCount');

        if (totalProjects) {
            totalProjects.textContent = this.allProjects.length.toLocaleString();
        }

        if (filteredCount) {
            filteredCount.textContent = this.filteredProjects.length.toLocaleString();
        }

        // Calcular estadísticas adicionales
        const totalMonto = this.filteredProjects.reduce((sum, project) => sum + (parseFloat(project.monto) || 0), 0);
        const totalMontoElement = document.getElementById('totalMonto');
        if (totalMontoElement) {
            totalMontoElement.textContent = '$' + this.formatNumber(totalMonto);
        }

        // Estadísticas por estado
        const estadisticas = this.filteredProjects.reduce((acc, project) => {
            const estado = project.estado || 'Sin Estado';
            acc[estado] = (acc[estado] || 0) + 1;
            return acc;
        }, {});

        console.log('📈 Estadísticas:', estadisticas);
    }

    updatePagination() {
        const totalPages = Math.ceil(this.filteredProjects.length / this.projectsPerPage);
        const paginationContainer = document.getElementById('pagination');

        if (!paginationContainer) return;

        if (totalPages <= 1) {
            paginationContainer.innerHTML = '';
            return;
        }

        let paginationHTML = '';

        // Botón anterior
        if (this.currentPage > 1) {
            paginationHTML += `<button class="btn btn-secondary" onclick="mainPage.goToPage(${this.currentPage - 1})">Anterior</button>`;
        }

        // Números de página
        const startPage = Math.max(1, this.currentPage - 2);
        const endPage = Math.min(totalPages, this.currentPage + 2);

        for (let i = startPage; i <= endPage; i++) {
            const activeClass = i === this.currentPage ? 'btn-primary' : 'btn-secondary';
            paginationHTML += `<button class="btn ${activeClass}" onclick="mainPage.goToPage(${i})">${i}</button>`;
        }

        // Botón siguiente
        if (this.currentPage < totalPages) {
            paginationHTML += `<button class="btn btn-secondary" onclick="mainPage.goToPage(${this.currentPage + 1})">Siguiente</button>`;
        }

        paginationContainer.innerHTML = paginationHTML;
    }

    hidePagination() {
        const paginationContainer = document.getElementById('pagination');
        if (paginationContainer) {
            paginationContainer.innerHTML = '';
        }
    }

    goToPage(page) {
        this.currentPage = page;
        this.displayProjects();
    }

    clearAllFilters() {
        // Limpiar todos los campos de filtro
        const filterInputs = [
            'searchInput', 'idFilter', 'contratoFilter', 'clienteFilter', 'estadoFilter',
            'regionFilter', 'ciudadFilter', 'fechaInicioDesde', 'fechaInicioHasta',
            'fechaTerminoDesde', 'fechaTerminoHasta', 'montoDesde', 'montoHasta'
        ];

        filterInputs.forEach(inputId => {
            const input = document.getElementById(inputId);
            if (input) {
                input.value = '';
            }
        });

        // Resetear filtros internos
        Object.keys(this.currentFilters).forEach(key => {
            this.currentFilters[key] = '';
        });

        this.currentPage = 1;
        this.applyFiltersAndDisplay();
        UIComponents.showNotification('Filtros limpiados', 'info');
    }

    async exportFilteredData() {
        try {
            if (this.filteredProjects.length === 0) {
                UIComponents.showNotification('No hay datos para exportar con los filtros actuales', 'warning');
                return;
            }

            // Crear CSV
            const headers = ['ID', 'Contrato', 'Cliente', 'Fecha Inicio', 'Fecha Término', 'Región', 'Ciudad', 'Estado', 'Monto'];
            const csvContent = [
                headers.join(','),
                ...this.filteredProjects.map(project => [
                    project.id || '',
                    `"${(project.contrato || '').replace(/"/g, '""')}"`,
                    `"${(project.cliente || '').replace(/"/g, '""')}"`,
                    project.fecha_inicio || '',
                    project.fecha_termino || '',
                    `"${(project.region || '').replace(/"/g, '""')}"`,
                    `"${(project.ciudad || '').replace(/"/g, '""')}"`,
                    project.estado || '',
                    project.monto || 0
                ].join(','))
            ].join('\n');

            // Descargar archivo
            const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
            const link = document.createElement('a');
            const url = URL.createObjectURL(blob);
            link.setAttribute('href', url);
            link.setAttribute('download', `proyectos_filtrados_${new Date().toISOString().split('T')[0]}.csv`);
            link.style.visibility = 'hidden';
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);

            UIComponents.showNotification(`${this.filteredProjects.length} proyectos exportados exitosamente`, 'success');
        } catch (error) {
            console.error('Error al exportar datos:', error);
            UIComponents.showNotification('Error al exportar datos', 'error');
        }
    }

    // Métodos utilitarios
    truncateText(text, maxLength) {
        if (!text || text.length <= maxLength) return text;
        return text.substring(0, maxLength) + '...';
    }

    formatDate(dateString) {
        if (!dateString) return 'N/A';
        try {
            const date = new Date(dateString);
            // Usar formato DD/MM/YYYY para consistencia con modify-database
            const day = date.getDate().toString().padStart(2, '0');
            const month = (date.getMonth() + 1).toString().padStart(2, '0');
            const year = date.getFullYear();
            return `${day}/${month}/${year}`;
        } catch (error) {
            return 'N/A';
        }
    }

    formatNumber(number) {
        if (!number) return '0';
        return Number(number).toLocaleString('es-CL');
    }
}

// Inicializar cuando el DOM esté listo
document.addEventListener('DOMContentLoaded', () => {
    console.log('🚀 DOM cargado, inicializando MainPage...');
    window.mainPage = new MainPage();
});
