<template>
  <div class="asignaturas-container">
    <!-- Header Bar -->
    <div class="header-bar">
      <h2 class="page-title">Gestión de Asignaturas</h2>
      <button class="add-btn" @click="mostrarModal = true">
        Agregar Asignatura
      </button>
    </div>

    <!-- Tabla de Asignaturas -->
    <div class="table-container">
      <div>
        <table class="asignaturas-table">
          <thead>
            <tr>
              <th>#</th>
              <th>Código</th>
              <th>Nombre</th>
              <th>Estado</th>
              <th>Opciones</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(asignatura, index) in asignaturas" :key="asignatura.codigo" 
                :class="{ 'row-even': index % 2 === 0 }">
              <td>{{ index + 1 }}</td>
              <td>{{ asignatura.codigo }}</td>
              <td>{{ asignatura.nombre }}</td>
              <td>
                <span class="status-badge" :class="asignatura.activa ? 'active' : 'inactive'">
                  {{ asignatura.activa ? 'Activa' : 'Inactiva' }}
                </span>
              </td>
              <td class="actions-cell">
                <button class="action-btn edit-btn" @click="editarAsignatura(asignatura)" title="Editar">
                  <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" d="m16.862 4.487 1.687-1.688a1.875 1.875 0 1 1 2.652 2.652L10.582 16.07a4.5 4.5 0 0 1-1.897 1.13L6 18l.8-2.685a4.5 4.5 0 0 1 1.13-1.897l8.932-8.931Zm0 0L19.5 7.125M18 14v4.75A2.25 2.25 0 0 1 15.75 21H5.25A2.25 2.25 0 0 1 3 18.75V8.25A2.25 2.25 0 0 1 5.25 6H10" />
                  </svg>
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
      
      <div v-if="asignaturas.length === 0" class="empty-state">
        <p>No se encontraron asignaturas</p>
      </div>
    </div>

    <!-- Modal para Agregar/Editar Asignatura -->
    <div v-if="mostrarModal" class="modal-overlay" @click="cerrarModal">
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <h2>{{ editando ? 'Editar Asignatura' : 'Registro de Asignatura' }}</h2>
          <button class="close-btn" @click="cerrarModal">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>
        
        <form @submit.prevent="guardarAsignatura" class="form-content">
          <div class="input-wrapper">
            <input 
              v-model="form.codigo" 
              type="text" 
              placeholder="Código de Asignatura (*)"
              :class="{ 'error': errors.codigo }"
              required 
              maxlength="10"
              
            >
            <span v-if="errors.codigo" class="error-msg">{{ errors.codigo }}</span>
          </div>

          <div class="input-wrapper">
            <input 
              v-model="form.nombre" 
              type="text" 
              placeholder="Nombre de Asignatura (*)"
              :class="{ 'error': errors.nombre }"
              required 
              maxlength="200"
              :disabled="loading"
            >
            <span v-if="errors.nombre" class="error-msg">{{ errors.nombre }}</span>
          </div>

          <div class="input-wrapper">
            <textarea 
              v-model="form.descripcion"
              placeholder="Descripción de la asignatura (opcional)"
              rows="3"
              :class="{ 'error': errors.descripcion }"
              :disabled="loading"
            ></textarea>
            <span v-if="errors.descripcion" class="error-msg">{{ errors.descripcion }}</span>
          </div>

          <div class="input-wrapper">
            <select v-model="form.activa" :class="{ 'error': errors.activa }" :disabled="loading">
              <option value="" disabled>Seleccione estado (*)</option>
              <option :value="true">Activa</option>
              <option :value="false">Inactiva</option>
            </select>
            <span v-if="errors.activa" class="error-msg">{{ errors.activa }}</span>
          </div>

          <button type="submit" class="add-btn" :disabled="loading">
            <span v-if="loading">{{ editando ? 'Actualizando...' : 'Registrando...' }}</span>
            <span v-else>{{ editando ? 'Actualizar Asignatura' : 'Registrar Asignatura' }} </span>
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
import { authService } from '@/services/authService.js'
import axios from 'axios'

export default {
  name: 'GestionAsignaturas',
  data() {
    return {
      asignaturas: [],
      form: {
        codigo: '',
        nombre: '',
        descripcion: '',
        activa: true
      },
      errors: {},
      loading: false,
      mensaje: '',
      tipoMensaje: '',
      usuarioEmail: null,
      editando: false,
      mostrarModal: false,
      mostrarModalExito: false,
      mensajeExito: '',
      codigoOriginal: ''
    }
  },
  async mounted() {
    this.obtenerUsuarioActual();
    await this.cargarAsignaturas();
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

    async cargarAsignaturas() {
      try {
        const response = await axios.get('http://localhost:8000/api/asignaturas/')
        this.asignaturas = response.data.results || response.data || []
      } catch (error) {
        console.error('Error al cargar asignaturas:', error)
        this.mostrarMensaje('Error al cargar asignaturas', 'error')
      }
    },

    editarAsignatura(asignatura) {
      this.editando = true
      this.codigoOriginal = asignatura.codigo
      this.form = {
        id: asignatura.id,
        codigo: asignatura.codigo,
        nombre: asignatura.nombre,
        descripcion: asignatura.descripcion || '',
        activa: asignatura.activa
      }
      this.mostrarModal = true
      this.limpiarErrores()
    },

    validar() {
      this.errors = {}

      if (!this.form.codigo.trim()) {
        this.errors.codigo = 'El código es obligatorio'
      }

      if (!this.form.nombre.trim()) {
        this.errors.nombre = 'El nombre es obligatorio'
      }

      if (this.form.activa === '') {
        this.errors.activa = 'Debes seleccionar un estado'
      }

      return Object.keys(this.errors).length === 0
    },

    async guardarAsignatura() {
      if (!this.validar()) {
        this.mensaje = ''
        return
      }

      // Verificar que tenemos el email del usuario
      if (!this.usuarioEmail) {
        this.mensaje = 'Error: Usuario no autenticado'
        this.tipoMensaje = 'error'
        return
      }

      this.loading = true
      try {
        if (this.editando) {
          // Actualizar asignatura
          const updateData = {
            codigo: this.form.codigo,
            nombre: this.form.nombre,
            descripcion: this.form.descripcion,
            activa: this.form.activa,
            registrada_por: this.usuarioEmail
          }
          
          const response = await axios.put(`http://localhost:8000/api/asignaturas/${this.form.id}/`, updateData)
          
          // Actualizar en la lista local
          const index = this.asignaturas.findIndex(a => a.codigo === this.codigoOriginal)
          if (index !== -1) {
            this.asignaturas[index] = { ...this.asignaturas[index], ...response.data }
          }
          
          this.mostrarModalGuardado('guardar')
        } else {
          // Crear nueva asignatura
          const response = await axios.post('http://localhost:8000/api/asignaturas/', {
            codigo: this.form.codigo,
            nombre: this.form.nombre,
            descripcion: this.form.descripcion,
            activa: this.form.activa,
            registrada_por: this.usuarioEmail
          })
          
          // Agregar a la lista local
          this.asignaturas.push(response.data)
          
          this.mostrarModalGuardado('guardar')
        }
        
        this.cerrarModal()
      } catch (error) {
        console.error('Error:', error)
        
        // Manejar errores de validación de Django REST Framework
        if (error.response && error.response.data) {
          const result = error.response.data
          if (result.codigo && Array.isArray(result.codigo)) {
            this.mensaje = `Error en código: ${result.codigo[0]}`
          } else if (result.nombre && Array.isArray(result.nombre)) {
            this.mensaje = `Error en nombre: ${result.nombre[0]}`
          } else if (result.registrada_por && Array.isArray(result.registrada_por)) {
            this.mensaje = `Error en usuario: ${result.registrada_por[0]}`
          } else if (result.detail) {
            this.mensaje = result.detail
          } else {
            this.mensaje = this.editando ? 'Error al actualizar la asignatura' : 'Error al registrar la asignatura'
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
        this.mensajeExito = this.editando ? 'Asignatura actualizada correctamente.' : 'Asignatura creada correctamente.';
      }
      this.mostrarModalExito = true;
    },

    cerrarModalExito() {
      this.mostrarModalExito = false;
    },

    cerrarModal() {
      this.mostrarModal = false
      this.editando = false
      this.codigoOriginal = ''
      this.limpiarFormulario()
      this.limpiarErrores()
    },

    limpiarFormulario() {
      this.form = {
        codigo: '',
        nombre: '',
        descripcion: '',
        activa: true
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
    }
  }
}
</script>

<style scoped lang="scss">
@import '@/assets/styles/variables';
@import '@/assets/styles/base';
/* Contenedor principal */
.asignaturas-container {
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
  margin-bottom: 2rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid #e5e7eb;
}

.page-title {
  flex: 1;
  text-align: center;
  margin: 0;
  color: #1e293b;
  font-size: 1.8rem;
  font-weight: 600;
}

.add-btn {
  @extend .btn;
  @extend .btn-primary;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-weight: 500;
  padding: 0.6rem 1.2rem;
  
  svg {
    width: 1.2rem;
    height: 1.2rem;
  }
}

.add-btn:hover {
  background: #0f172a;
  transform: translateY(-1px);
}

/* Tabla */
.table-container {
  width: 100%;
  flex: 1;
  display: flex;
  flex-direction: column;
  border-radius: 8px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  margin-bottom: 2rem;
  background: #fff;
  max-height: calc(100vh - 300px);
  min-height: 300px;
  position: relative;
  overflow: hidden;
  
  > div {
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    overflow: auto;
    padding-right: 8px;
    
    &::-webkit-scrollbar {
      width: 8px;
      height: 8px;
    }
    
    &::-webkit-scrollbar-track {
      background: #f1f1f1;
      border-radius: 4px;
      margin: 4px 0;
    }
    
    &::-webkit-scrollbar-thumb {
      background: #c1c1c1;
      border-radius: 4px;
    }
    
    &::-webkit-scrollbar-thumb:hover {
      background: #a8a8a8;
    }
  }
}

.asignaturas-table {
  width: 100%;
  background: white;
  font-size: 0.9rem;
  table-layout: fixed;
  min-width: 100%;
  margin: 0;
  
  thead {
    position: sticky;
    top: 0;
    z-index: 10;
    background: #fff;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
  }
  
  th, td {
    padding: 0.75rem 1rem;
    text-align: left;
    border-bottom: 1px solid #e0e0e0;
    vertical-align: middle;
  }
  
  /* Anchos específicos de columnas para asignaturas */
  th:nth-child(1), td:nth-child(1) { width: 60px; }  /* # */
  th:nth-child(2), td:nth-child(2) { width: 150px; } /* Código */
  th:nth-child(3), td:nth-child(3) { width: auto; }  /* Nombre */
  th:nth-child(4), td:nth-child(4) { width: 120px; } /* Estado */
  th:nth-child(5), td:nth-child(5) { width: 120px; } /* Opciones */
  
  td {
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
    max-width: 0;
    
    /* Show full text on hover */
    &:hover {
      overflow: visible;
      position: relative;
      z-index: 1;
      background: white;
      box-shadow: 0 0 10px rgba(0,0,0,0.1);
      white-space: normal;
      word-break: break-word;
    }
  }
  
  th {
    background: $bg-lighter;
    color: $text-secondary;
    font-weight: 600;
    font-size: 0.8rem;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    white-space: nowrap;
  }
  
  td {
    color: $text-primary;
    vertical-align: middle;
  }
  
  tr:last-child td {
    border-bottom: none;
  }
  
  tr:hover {
    background: rgba($color-primary, 0.03);
  }
  
  .row-even {
    background: $bg-lighter;
  }
}

.actions-cell {
  text-align: center;
}

.action-btn {
  background: none;
  border: none;
  padding: 0.5rem;
  align-items: center;
  justify-content: center;
  border-radius: 6px;
  transition: all 0.2s ease;
  border: 1px solid transparent;
  cursor: pointer;
  display: inline-flex;
  
  svg {
    width: 1.25rem;
    height: 1.25rem;
  }
  
  &.edit-btn {
    color: #4a6cf7; /* Mismo color azul que usuarios */
    border-color: #4a6cf7;
    
    &:hover {
      background: rgba(74, 108, 247, 0.1);
    }
  }
}

.status-badge {
  display: inline-block;
  padding: 0.25rem 0.75rem;
  border-radius: 50px;
  font-size: 0.8rem;
  font-weight: 500;
  text-align: center;
  min-width: 80px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

/* Status badges */
.status-badge {
  &.active {
    background: rgba($color-primary, 0.1);
    color: $color-primary;
    border: 1px solid rgba($color-primary, 0.2);
  }
  
  &.inactive {
    background: rgba(#f44336, 0.1);
    color: #f44336;
    border: 1px solid rgba(#f44336, 0.2);
  }
  border: 1px solid #9A8F84;
}

/* Estado vacío */
.empty-state {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 100%;
  min-height: 200px;
  color: #757575;
  font-size: 1.1rem;
  background: #fafafa;
  border-radius: 8px;
  margin: 0;
  padding: 2rem;
  
  p {
    margin: 0;
    padding: 1rem 2rem;
    background: white;
    border-radius: 6px;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  }
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
}

.modal-header h2 {
  font-size: 1.5rem;
  font-weight: 700;
  color: #1e293b;
  margin: 0;
}

.close-btn {
  background: none;
  border: none;
  padding: 0.5rem;
  cursor: pointer;
  color: #64748b;
  border-radius: 4px;
  transition: all 0.2s;
}

.close-btn:hover {
  background: #f1f5f9;
  color: #374151;
}

.close-btn svg {
  width: 20px;
  height: 20px;
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
}

.form-content input,
.form-content select,
.form-content textarea {
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
}

.form-content input:focus,
.form-content select:focus,
.form-content textarea:focus {
  border-color: #2563eb;
  box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.1);
}

.form-content input.error,
.form-content select.error,
.form-content textarea.error {
  border-color: #ef4444;
  box-shadow: 0 0 0 3px rgba(239, 68, 68, 0.1);
}

.form-content input:disabled {
  background: #f8fafc;
  color: #64748b;
  cursor: not-allowed;
}

.form-content select {
  cursor: pointer;
  appearance: none;
  background-image: url("data:image/svg+xml,%3csvg xmlns='http://www.w3.org/2000/svg' fill='none' viewBox='0 0 20 20'%3e%3cpath stroke='%232563eb' stroke-linecap='round' stroke-linejoin='round' stroke-width='2' d='m6 8 4 4 4-4'/%3e%3c/svg%3e");
  background-position: right 0.75rem center;
  background-repeat: no-repeat;
  background-size: 1.2em 1.2em;
  padding-right: 2.5rem;
}

.form-content textarea {
  min-height: 80px;
  resize: vertical;
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
}

.submit-btn:hover:not(:disabled) {
  background: #1d4ed8;
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(37, 99, 235, 0.4);
}

.submit-btn:disabled {
  background: #94a3b8;
  cursor: not-allowed;
  transform: none;
  box-shadow: none;
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
}

.mensaje.success {
  background: rgba(34, 197, 94, 0.1);
  color: #16a34a;
  border: 1px solid rgba(34, 197, 94, 0.3);
}

.mensaje.error {
  background: rgba(239, 68, 68, 0.1);
  color: #dc2626;
  border: 1px solid rgba(239, 68, 68, 0.3);
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
}

.cancel-btn:hover {
  background: #f5f5f5;
  border-color: #9e9e9e;
}

/* Responsive */
@media (max-width: 768px) {
  .asignaturas-container {
    padding: 1rem;
    margin: 0.5rem;
  }
  
  .asignaturas-table {
    font-size: 0.8rem;
  }
  
  .asignaturas-table th,
  .asignaturas-table td {
    padding: 0.75rem 0.5rem;
  }
  
  .page-title {
    font-size: 1.5rem;
  }
}
</style>