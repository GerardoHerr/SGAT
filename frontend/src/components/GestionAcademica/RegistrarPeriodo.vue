<template>
  <div class="periodos-container">
    <!-- Header Bar -->
      <div class="header-bar">
      <h2 class="page-title">Gestión de Periodos Académicos </h2>
      <button class="add-btn" @click="mostrarModal = true">
        Agregar Periodo
      </button>
    </div>

    <!-- Tabla de Periodos -->
    <div class="table-container">
      <div>
        <table class="periodos-table">
          <thead>
            <tr>
              <th>#</th>
              <th>Nombre del Periodo</th>
              <th>Fecha de Inicio</th>
              <th>Fecha de Fin</th>
              <th>Estado</th>
              <th>Opciones</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(periodo, index) in periodos" :key="periodo.id" 
                :class="{ 'row-even': index % 2 === 0 }">
              <td>{{ index + 1 }}</td>
              <td>{{ periodo.nombre }}</td>
              <td>{{ formatearFecha(periodo.fecha_inicio) }}</td>
              <td>{{ formatearFecha(periodo.fecha_fin) }}</td>
              <td>
                <span class="status-badge" :class="obtenerEstadoPeriodo(periodo)">
                  {{ obtenerTextoEstado(periodo) }}
                </span>
              </td>
              <td class="actions-cell">
                <button class="action-btn edit-btn" @click="editarPeriodo(periodo)" title="Editar">
                  <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" d="m16.862 4.487 1.687-1.688a1.875 1.875 0 1 1 2.652 2.652L10.582 16.07a4.5 4.5 0 0 1-1.897 1.13L6 18l.8-2.685a4.5 4.5 0 0 1 1.13-1.897l8.932-8.931Zm0 0L19.5 7.125M18 14v4.75A2.25 2.25 0 0 1 15.75 21H5.25A2.25 2.25 0 0 1 3 18.75V8.25A2.25 2.25 0 0 1 5.25 6H10" />
                  </svg>
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
      
      <div v-if="periodos.length === 0" class="empty-state">
        <p>No se encontraron periodos académicos</p>
      </div>
    </div>

    <!-- Modal para Agregar/Editar Periodo -->
    <div v-if="mostrarModal" class="modal-overlay" @click="cerrarModal">
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <h2>{{ editando ? 'Editar Periodo Académico' : 'Registro de Periodo Académico' }}</h2>
          <button class="close-btn" @click="cerrarModal">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>
        
        <form @submit.prevent="guardarPeriodo" class="form-content">
          <div class="input-wrapper">
            <label for="fechaInicio">Fecha de Inicio (*) </label>
            <input 
              id="fechaInicio"
              v-model="form.fechaInicio" 
              type="date" 
              :class="{ 'error': errors.fechaInicio }"
              required 
              :disabled="loading"
              @change="generarNombre"
            >
            <span v-if="errors.fechaInicio" class="error-msg">{{ errors.fechaInicio }}</span>
          </div>

          <div class="input-wrapper">
            <label for="fechaFin">Fecha de Fin (*)</label>
            <input 
              id="fechaFin"
              v-model="form.fechaFin" 
              type="date" 
              :class="{ 'error': errors.fechaFin }"
              required 
              :disabled="loading"
              :min="form.fechaInicio"
              @change="generarNombre"
            >
            <span v-if="errors.fechaFin" class="error-msg">{{ errors.fechaFin }}</span>
          </div>
        
          <div class="input-wrapper">
            <label for="fechaFin">Estado (*)</label>
            <select v-model="form.activa" :class="{ 'error': errors.activa }" :disabled="loading">
              <option value="" disabled>Seleccione estado</option>
              <option :value="true">Activo</option>
              <option :value="false">Inactivo</option>
            </select>
            <span v-if="errors.activa" class="error-msg">{{ errors.activa }}</span>
          </div>

          <div class="input-wrapper">
            <label for="nombre">Nombre del Periodo</label>
            <input 
              id="nombre"
              v-model="form.nombre" 
              type="text" 
              placeholder="Se generará automáticamente"
              readonly
              :disabled="loading"
              class="readonly-field"
            >
          </div>

          <button type="submit" class="add-btn" :disabled="loading || !form.nombre">
            <span v-if="loading">{{ editando ? 'Actualizando...' : 'Registrando...' }}</span>
            <span v-else>{{ editando ? 'Actualizar Periodo' : 'Registrar Periodo' }}</span>
          </button>
        </form>
        
        <div v-if="mensaje" class="mensaje-wrapper">
          <div class="mensaje" :class="tipoMensaje">
            {{ mensaje }}
          </div>
        </div>
      </div>
    </div>

    <!-- Modal de éxito -->
    <div v-if="mostrarModalExito" class="modal-overlay" @click="cerrarModalExito">
      <div class="confirmation-modal" @click.stop>
        <h2 class="modal-exito-titulo">{{ mensajeExito }}</h2>
        <button class="cancel-btn" @click="cerrarModalExito">Aceptar</button>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'GestionPeriodos',
  data() {
    return {
      periodos: [],
      form: {
        fechaInicio: '',
        fechaFin: '',
        nombre: ''
      },
      errors: {},
      loading: false,
      mensaje: '',
      tipoMensaje: '',
      editando: false,
      mostrarModal: false,
      mostrarModalExito: false,
      mensajeExito: '',
      periodoOriginal: null
    }
  },
  async mounted() {
    await this.cargarPeriodos()
  },
  methods: {
    obtenerUsuarioActual() {
      const currentUser = authService.getCurrentUser();
      if (currentUser && currentUser.email) {
        this.usuarioEmail = currentUser.email;
      } else {
        this.mensaje = 'Error: No se pudo obtener el usuario autenticado';
        this.tipoMensaje = 'error';
        this.$router.push('/login');
      }
    },

    async cargarPeriodos() {
      try {
        const response = await axios.get('http://localhost:8000/api/periodos/')
        this.periodos = response.data.results || response.data || []
      } catch (error) {
        console.error('Error al cargar periodos:', error)
        this.mostrarMensaje('Error al cargar periodos', 'error')
      }
    },

    editarPeriodo(periodo) {
      this.editando = true
      this.periodoOriginal = periodo
      this.form = {
        fechaInicio: periodo.fecha_inicio,
        fechaFin: periodo.fecha_fin,
        nombre: periodo.nombre
      }
      this.mostrarModal = true
      this.limpiarErrores()
    },

    generarNombre() {
      if (this.form.fechaInicio && this.form.fechaFin) {
        const fechaInicio = new Date(this.form.fechaInicio);
        const fechaFin = new Date(this.form.fechaFin);
        
        // Validar que la fecha de fin sea posterior a la de inicio
        if (fechaFin <= fechaInicio) {
          this.errors.fechaFin = 'La fecha de fin debe ser posterior a la fecha de inicio';
          this.form.nombre = '';
          return;
        }
        
        // Validar que haya al menos 3 meses de diferencia
        const diferenciaMeses = this.calcularDiferenciaMeses(fechaInicio, fechaFin);
        if (diferenciaMeses < 3) {
          this.errors.fechaFin = 'La fecha de fin debe ser al menos 3 meses posterior a la fecha de inicio';
          this.form.nombre = '';
          return;
        }
        
        // Limpiar errores si las validaciones pasan
        delete this.errors.fechaFin;
        
        const meses = [
          'Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio',
          'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre'
        ];
        
        const mesInicio = meses[fechaInicio.getMonth()];
        const añoInicio = fechaInicio.getFullYear();
        const mesFin = meses[fechaFin.getMonth()];
        const añoFin = fechaFin.getFullYear();
        
        // Generar nombre en formato: Marzo2025-Agosto2025
        this.form.nombre = `${mesInicio}${añoInicio}-${mesFin}${añoFin}`;
      } else {
        this.form.nombre = '';
      }
    },

    calcularDiferenciaMeses(fechaInicio, fechaFin) {
      const diffTime = Math.abs(fechaFin - fechaInicio);
      const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
      return Math.floor(diffDays / 30); // Aproximación de meses
    },

    validar() {
      this.errors = {}

      if (!this.form.fechaInicio) {
        this.errors.fechaInicio = 'La fecha de inicio es obligatoria'
      }

      if (!this.form.fechaFin) {
        this.errors.fechaFin = 'La fecha de fin es obligatoria'
      }

      if (this.form.fechaInicio && this.form.fechaFin) {
        const fechaInicio = new Date(this.form.fechaInicio);
        const fechaFin = new Date(this.form.fechaFin);
        
        if (fechaFin <= fechaInicio) {
          this.errors.fechaFin = 'La fecha de fin debe ser posterior a la fecha de inicio';
        } else {
          const diferenciaMeses = this.calcularDiferenciaMeses(fechaInicio, fechaFin);
          if (diferenciaMeses < 3) {
            this.errors.fechaFin = 'La fecha de fin debe ser al menos 3 meses posterior a la fecha de inicio';
          }
        }
      }

      if (!this.form.nombre) {
        this.errors.nombre = 'El nombre del periodo es obligatorio'
      }

      return Object.keys(this.errors).length === 0
    },

    async guardarPeriodo() {
      if (!this.validar()) {
        this.mensaje = ''
        return
      }

      this.loading = true
      try {
        if (this.editando) {
          // Actualizar periodo
          const updateData = {
            nombre: this.form.nombre,
            fecha_inicio: this.form.fechaInicio,
            fecha_fin: this.form.fechaFin,
          }
          
          const response = await axios.put(`http://localhost:8000/api/periodos/${this.periodoOriginal.id}/`, updateData)
          
          // Actualizar en la lista local
          const index = this.periodos.findIndex(p => p.id === this.periodoOriginal.id)
          if (index !== -1) {
            this.periodos[index] = { ...this.periodos[index], ...response.data }
          }
          
          this.mostrarModalGuardado('guardar')
        } else {
          // Crear nuevo periodo
          const response = await axios.post('http://localhost:8000/api/periodos/', {
            nombre: this.form.nombre,
            fecha_inicio: this.form.fechaInicio,
            fecha_fin: this.form.fechaFin
          })
          
          // Agregar a la lista local
          this.periodos.push(response.data)
          
          this.mostrarModalGuardado('guardar')
        }
        
        this.cerrarModal()
      } catch (error) {
        console.error('Error:', error)
        
        // Manejar errores de validación
        if (error.response && error.response.data) {
          const result = error.response.data
          if (result.error) {
            this.mensaje = result.error
          } else if (result.detail) {
            this.mensaje = result.detail
          } else {
            this.mensaje = this.editando ? 'Error al actualizar el periodo' : 'Error al registrar el periodo'
          }
        } else {
          this.mensaje = 'Error de conexión con el servidor'
        }
        this.tipoMensaje = 'error'
      } finally {
        this.loading = false
      }
    },

    mostrarModalGuardado(tipo) {
      if (tipo === 'guardar') {
        this.mensajeExito = this.editando ? 'Periodo actualizado correctamente.' : 'Periodo creado correctamente.';
      }
      this.mostrarModalExito = true;
    },

    cerrarModalExito() {
      this.mostrarModalExito = false;
    },

    cerrarModal() {
      this.mostrarModal = false
      this.editando = false
      this.periodoOriginal = null
      this.limpiarFormulario()
      this.limpiarErrores()
    },

    limpiarFormulario() {
      this.form = {
        fechaInicio: '',
        fechaFin: '',
        nombre: ''
      };
    },

    limpiarErrores() {
      this.errors = {}
      this.mensaje = ''
    },

    mostrarMensaje(texto, tipo) {
      this.mensaje = texto
      this.tipoMensaje = tipo
      setTimeout(() => {
        this.mensaje = ''
      }, 5000)
    },

    formatearFecha(fecha) {
      if (!fecha) return '';
      const date = new Date(fecha);
      return date.toLocaleDateString('es-ES', {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
      });
    },

    obtenerEstadoPeriodo(periodo) {
      const hoy = new Date();
      const fechaInicio = new Date(periodo.fecha_inicio);
      const fechaFin = new Date(periodo.fecha_fin);
      
      if (hoy < fechaInicio) {
        return 'pendiente';
      } else if (hoy >= fechaInicio && hoy <= fechaFin) {
        return 'active';
      } else {
        return 'inactive';
      }
    },

    obtenerTextoEstado(periodo) {
      const estado = this.obtenerEstadoPeriodo(periodo);
      const estados = {
        'pendiente': 'Pendiente',
        'active': 'Activo',
        'inactive': 'Finalizado'
      };
      return estados[estado] || 'Desconocido';
    }
  }
}
</script>

<style scoped lang="scss">
@import '@/assets/styles/variables';
@import '@/assets/styles/base';

/* Contenedor principal */
.periodos-container {
  width: 100%;
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem 1.5rem;
  min-height: 80vh;
  box-sizing: border-box;
  background: #fff;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

/* Header Bar */
.header-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
}

.page-title {
  flex: 1;
  text-align: center;
  margin: 0;
  color: #1e293b;
  font-size: 1.8rem;
  font-weight: 600;
  
  &::after {
    content: '';
    position: absolute;
    bottom: 0;
    left: 50%;
    transform: translateX(-50%);
    width: 50px;
    height: 3px;
    background: $color-primary;
    border-radius: 2px;
  }
}

.add-btn {
  @extend .btn;
  @extend .btn-primary;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-weight: 500;
  padding: 0.75rem 1.5rem;
  
  &:hover {
    background: #0f172a;
    transform: translateY(-1px);
  }
}

/* Tabla */
.table-container {
  background: white;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  
  > div {
    overflow: auto;
    
    &::-webkit-scrollbar {
      width: 8px;
      height: 8px;
    }
    
    &::-webkit-scrollbar-track {
      background: #f1f1f1;
      border-radius: 4px;
    }
    
    &::-webkit-scrollbar-thumb {
      background: #c1c1c1;
      border-radius: 4px;
      
      &:hover {
        background: #a8a8a8;
      }
    }
  }
}

.periodos-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 0.9rem;
  
  thead {
    position: sticky;
    top: 0;
    z-index: 10;
    background: #fff;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
  }
  
  th {
    background: $bg-lighter;
    padding: 1rem;
    text-align: left;
    font-weight: 600;
    color: $text-secondary;
    border-bottom: 1px solid #e5e7eb;
    font-size: 0.9rem;
  }
  
  td {
    padding: 1rem;
    border-bottom: 1px solid #f3f4f6;
    font-size: 0.9rem;
    color: $text-primary;
  }
  
  tr:hover {
    background: rgba($color-primary, 0.03);
  }
}

.row-even {
  background: $bg-lighter;
}

.actions-cell {
  text-align: center;
}

.action-btn {
  background: none;
  border: none;
  padding: 0.5rem;
  border-radius: 4px;
  cursor: pointer;
  margin: 0 0.25rem;
  transition: all 0.2s;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  
  svg {
    width: 16px;
    height: 16px;
  }
  
  &.edit-btn {
    color: #2563eb;
    background: rgba(37, 99, 235, 0.1);
    
    &:hover {
      background: rgba(37, 99, 235, 0.2);
    }
  }
}

/* Status badges */
.status-badge {
  padding: 0.25rem 0.75rem;
  border-radius: 9999px;
  font-size: 0.8rem;
  font-weight: 600;
  
  &.active {
    background: rgba(34, 197, 94, 0.1);
    color: #16a34a;
  }
  
  &.inactive {
    background: rgba(239, 68, 68, 0.1);
    color: #dc2626;
  }
  
  &.pendiente {
    background: rgba(249, 115, 22, 0.1);
    color: #ea580c;
  }
}

/* Estado vacío */
.empty-state {
  text-align: center;
  padding: 3rem;
  color: #64748b;
}

/* Modal overlay */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  backdrop-filter: blur(4px);
}

/* Modal content */
.modal-content {
  background: white;
  border-radius: 16px;
  max-width: 500px;
  width: 100%;
  max-height: 90vh;
  overflow-y: auto;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.15);
  border: 1px solid #e5e7eb;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.5rem;
  border-bottom: 1px solid #e5e7eb;
  
  h2 {
    font-size: 1.5rem;
    font-weight: 700;
    color: #1e293b;
    margin: 0;
  }
}

.close-btn {
  background: none;
  border: none;
  padding: 0.5rem;
  cursor: pointer;
  color: #64748b;
  border-radius: 4px;
  transition: all 0.2s;
  
  &:hover {
    background: #f1f5f9;
    color: #374151;
  }
  
  svg {
    width: 20px;
    height: 20px;
  }
}

/* Estilos del formulario en modal */
.form-content {
  padding: 1.5rem;
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
}

.input-wrapper {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  
  label {
    display: block;
    margin-bottom: 0.5rem;
    color: $text-primary;
    font-weight: 500;
    font-size: 0.9rem;
  }
}

.form-content input,
.form-content select {
  padding: 0.875rem 1rem;
  font-size: 0.95rem;
  border: 2px solid #e2e8f0;
  border-radius: 8px;
  outline: none;
  transition: all 0.3s ease;
  background: white;
  font-weight: 500;
  width: 100%;
  box-sizing: border-box;
  color: #374151;
  
  &:focus {
    border-color: #2563eb;
    box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.1);
  }
  
  &.error {
    border-color: #ef4444;
    box-shadow: 0 0 0 3px rgba(239, 68, 68, 0.1);
  }
  
  &:disabled {
    background: #f8fafc;
    color: #64748b;
    cursor: not-allowed;
  }
  
  /* Date picker styles */
  &[type="date"] {
    &::-webkit-calendar-picker-indicator {
      color: $color-primary;
      cursor: pointer;
      padding: 0.2rem;
      border-radius: 4px;
      
      &:hover {
        background: rgba($color-primary, 0.1);
      }
    }
  }
}

.readonly-field {
  background: $bg-lighter !important;
  color: $text-secondary !important;
  cursor: not-allowed;
  font-style: italic;
}

.submit-btn {
  padding: 0.875rem 1.5rem;
  font-size: 1rem;
  background: #2563eb;
  color: white;
  font-weight: 600;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s ease;
  margin-top: 0.5rem;
  box-shadow: 0 4px 12px rgba(37, 99, 235, 0.3);
  
  &:hover:not(:disabled) {
    background: #1d4ed8;
    transform: translateY(-2px);
    box-shadow: 0 6px 16px rgba(37, 99, 235, 0.4);
  }
  
  &:disabled {
    background: #94a3b8;
    cursor: not-allowed;
    transform: none;
    box-shadow: none;
  }
}

.error-msg {
  color: #ef4444;
  font-size: 0.8rem;
  font-weight: 600;
}

.mensaje-wrapper {
  padding: 0 1.5rem 1.5rem;
}

.mensaje {
  padding: 0.875rem 1rem;
  border-radius: 8px;
  font-weight: 500;
  font-size: 0.9rem;
  
  &.success {
    background: rgba(34, 197, 94, 0.1);
    color: #16a34a;
    border: 1px solid rgba(34, 197, 94, 0.3);
  }
  
  &.error {
    background: rgba(239, 68, 68, 0.1);
    color: #dc2626;
    border: 1px solid rgba(239, 68, 68, 0.3);
  }
}

/* Confirmation Modal */
.confirmation-modal {
  background: #fff;
  border-radius: 8px;
  padding: 2rem;
  text-align: center;
  max-width: 400px;
  width: 90%;
  margin: 0 auto;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
  border: 1px solid #e0e0e0;
}

.modal-exito-titulo {
  color: #4CAF50;
  margin-bottom: 1.5rem;
  font-size: 1.5rem;
  font-weight: 600;
  text-align: center;
}

.cancel-btn {
  min-width: 100px;
  padding: 0.75rem 1.5rem;
  background: transparent;
  border: 1px solid #757575;
  color: #616161;
  border-radius: 4px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
  
  &:hover {
    background: #f5f5f5;
    border-color: #9e9e9e;
  }
}

/* Responsive */
@media (max-width: 768px) {
  .periodos-container {
    padding: 1rem;
  }
  
  .periodos-table {
    font-size: 0.8rem;
    
    th, td {
      padding: 0.75rem 0.5rem;
    }
  }
  
  .page-title {
    font-size: 1.5rem;
  }
}
</style>