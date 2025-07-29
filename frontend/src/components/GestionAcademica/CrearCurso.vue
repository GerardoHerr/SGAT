<template>
  <div class="cursos-container">
    <!-- Header Bar -->
    <div class="header-bar">
      <h2 class="page-title">Gestión de Cursos</h2>
      <button class="add-btn" @click="mostrarModal = true">
        Agregar Curso
      </button>
    </div>



    <!-- Tabla de Cursos -->
    <div class="tabla-section">
      <div class="card-tabla">
        <h3>Cursos Registrados</h3>

        <div class="tabla-container">
          <table class="tabla-cursos">
            <thead>
              <tr>
                <th>#</th>
                <th>Asignatura</th>
                <th>Docente Responsable</th>
                <th>Período Académico</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(curso, index) in cursos" :key="curso.id">
                <td>{{ index + 1 }}</td>
                <td>{{ curso.asignatura_nombre || 'N/A' }}</td>
                <td>
                  <span v-if="curso.docente_nombre">
                    {{ curso.docente_nombre }}
                  </span>
                  <span v-else class="sin-docente">Sin asignar</span>
                </td>
                <td>{{ curso.periodo }}</td>
              </tr>
            </tbody>
          </table>

          <div v-if="cursos.length === 0" class="empty-state">
            <p>No se encontraron cursos registrados</p>
          </div>
        </div>
      </div>
    </div>

    <!-- Modal para Agregar Curso -->
    <div v-if="mostrarModal" class="modal-overlay" @click="cerrarModal">
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <h2>Crear Nuevo Curso</h2>
          <button class="close-btn" @click="cerrarModal">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
              stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>

        <form @submit.prevent="crearCurso" class="form-content">
          <div class="input-wrapper">
            <label for="asignatura">Asignatura (*)</label>
            <select id="asignatura" v-model="curso.asignatura" :class="{ 'error': errors.asignatura }" required
              @change="asignarDocente" :disabled="loading">
              <option value="" disabled>Seleccione una asignatura</option>
              <option v-for="asig in asignaturas" :key="asig.codigo" :value="asig.id">
                {{ asig.codigo }} - {{ asig.nombre }}
              </option>
            </select>
            <span v-if="errors.asignatura" class="error-msg">{{ errors.asignatura }}</span>
          </div>

          <div class="input-wrapper">
            <label for="docente">Docente Responsable</label>
            <input id="docente" v-model="docenteNombre" type="text" placeholder="Se asignará automáticamente" readonly
              :disabled="loading" class="readonly-field">
            <span v-if="errors.docente" class="error-msg">{{ errors.docente }}</span>
          </div>

          <div class="input-wrapper">
            <label for="periodo">Período Académico (*)</label>
            <input id="periodo" v-model="curso.periodo" type="text" placeholder="Ej: 2024-1"
              :class="{ 'error': errors.periodo }" required :disabled="loading">
            <div class="form-text">Formato: AAAA-P (ej: 2024-1 para el primer semestre del 2024)</div>
            <span v-if="errors.periodo" class="error-msg">{{ errors.periodo }}</span>
          </div>

          <button type="submit" class="submit-btn" :disabled="loading || !curso.asignatura || !curso.periodo">
            <span v-if="loading">Creando...</span>
            <span v-else>Crear Curso</span>
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
import api from '@/services/api';
import { authService } from '@/services/authService';

export default {
  name: 'GestionCursos',
  data() {
    return {
      cursos: [],
      asignaturas: [],
      curso: {
        asignatura: '',
        docente: '',
        periodo: ''
      },
      docenteNombre: '',
      errors: {},
      loading: false,
      mensaje: '',
      tipoMensaje: '',
      mostrarModal: false,
      mostrarModalExito: false,
      mensajeExito: '',
      currentUser: null,
      userEmail: ''
    };
  },
  async mounted() {
    this.currentUser = authService.getCurrentUser();
    if (this.currentUser) {
      this.userEmail = this.currentUser.email;
    } else {
      console.warn('No se pudo obtener el usuario actual');
      this.$router.push('/login');
      return;
    }
    await this.cargarDatos();
  },
  methods: {
    async cargarDatos() {
      try {
        await Promise.all([
          this.cargarAsignaturas(),
          this.cargarCursos()
        ]);
      } catch (error) {
        console.error('Error al cargar datos:', error);
        this.mostrarMensaje('Error al cargar los datos necesarios', 'error');
      }
    },

    async cargarAsignaturas() {
      try {
        const response = await api.get('asignaturas/');
        this.asignaturas = response.data;
      } catch (error) {
        console.error('Error al cargar asignaturas:', error);
        throw error;
      }
    },

    async cargarCursos() {
      try {
        const response = await api.get('cursos/');
        this.cursos = await Promise.all(
          response.data.map(async (curso) => {
            // Obtener nombre de la asignatura
            let asignaturaNombre = 'N/A';
            if (curso.asignatura) {
              const asignatura = this.asignaturas.find(a => a.id === curso.asignatura);
              asignaturaNombre = asignatura ? asignatura.nombre : curso.asignatura;
            }

            // Obtener nombre del docente
            let docenteNombre = 'Sin asignar';
            if (curso.docente) {
              try {
                const docenteResponse = await api.get(`usuarios/by-email/?email=${encodeURIComponent(curso.docente)}`);
                if (docenteResponse.data) {
                  docenteNombre = `${docenteResponse.data.nombre || ''} ${docenteResponse.data.apellido || ''}`.trim() || curso.docente;
                }
              } catch (error) {
                console.error('Error al obtener docente:', error);
                docenteNombre = curso.docente;
              }
            }

            return {
              ...curso,
              asignatura_nombre: asignaturaNombre,
              docente_nombre: docenteNombre
            };
          })
        );
      } catch (error) {
        console.error('Error al cargar cursos:', error);
        this.cursos = [];
      }
    },

    async asignarDocente() {
      if (!this.curso.asignatura) {
        this.docenteNombre = '';
        this.curso.docente = '';
        return;
      }

      try {
        const asignatura = this.asignaturas.find(a => a.id === this.curso.asignatura);
        if (!asignatura) {
          this.docenteNombre = '';
          this.curso.docente = '';
          this.errors.docente = 'No se encontró la asignatura seleccionada';
          return;
        }
        const response = await api.get(`asignaturas/${this.curso.asignatura}/`);
        if (response.data && response.data.docente_responsable) {
          this.curso.docente = response.data.docente_responsable;
          
          // Obtener el nombre del docente para mostrarlo
          const docenteResponse = await api.get(`usuarios/by-email/?email=${encodeURIComponent(response.data.docente_responsable)}`);
          if (docenteResponse.data) {
            this.docenteNombre = `${docenteResponse.data.nombre || ''} ${docenteResponse.data.apellido || ''}`.trim() || response.data.docente_responsable;
          } else {
            this.docenteNombre = response.data.docente_responsable;
          }
        } else {
          this.docenteNombre = 'Sin asignar';
          this.curso.docente = '';
          this.errors.docente = 'La asignatura seleccionada no tiene un docente asignado';
        }
      } catch (error) {
        console.error('Error al obtener la asignatura:', error);
        this.docenteNombre = 'Error al cargar';
        this.curso.docente = '';
        this.errors.docente = 'Error al cargar la información de la asignatura';
      }
    },

    validar() {
      this.errors = {};

      if (!this.curso.asignatura) {
        this.errors.asignatura = 'Por favor selecciona una asignatura';
      }

      if (!this.curso.docente) {
        this.errors.docente = 'La asignatura debe tener un docente asignado';
      }

      if (!this.curso.periodo) {
        this.errors.periodo = 'Por favor ingresa el período académico';
      } else {
        // Validar formato del período (AAAA-P)
        const formatoValido = /^\d{4}-[1-2]$/.test(this.curso.periodo);
        if (!formatoValido) {
          this.errors.periodo = 'El formato debe ser AAAA-P (ej: 2024-1)';
        }
      }

      // Validar duplicados
      if (this.curso.asignatura && this.curso.periodo) {
        const yaExiste = this.cursos.some(c => 
          c.asignatura === this.curso.asignatura && c.periodo === this.curso.periodo
        );
        if (yaExiste) {
          this.errors.periodo = 'Ya existe un curso para esta asignatura y período académico';
        }
      }

      return Object.keys(this.errors).length === 0;
    },

    async crearCurso() {
      if (!this.validar()) {
        this.mensaje = '';
        return;
      }

      this.loading = true;
      try {
        const cursoData = {
          ...this.curso
        };

        const response = await api.post('cursos/', cursoData);

        // Resolver nombres de asignatura y docente para el nuevo curso
        let asignaturaNombre = 'N/A';
        let docenteNombre = 'Sin asignar';
        const asignatura = this.asignaturas.find(a => a.id === response.data.asignatura);
        if (asignatura) {
          asignaturaNombre = asignatura.nombre;
        }
        if (response.data.docente) {
          try {
            const docenteResponse = await api.get(`usuarios/by-email/?email=${encodeURIComponent(response.data.docente)}`);
            if (docenteResponse.data) {
              docenteNombre = `${docenteResponse.data.nombre || ''} ${docenteResponse.data.apellido || ''}`.trim() || response.data.docente;  
            }
          } catch (error) {
            docenteNombre = response.data.docente;
          }
        }
        const nuevoCurso = {
          ...response.data,
          asignatura_nombre: asignaturaNombre,
          docente_nombre: docenteNombre
        };
        this.cursos = [nuevoCurso, ...this.cursos];

        this.mostrarModalGuardado();
        this.cerrarModal();
      } catch (error) {
        console.error('Error al crear curso:', error);
        let mensaje = 'Error al crear el curso';

        if (error.response) {
          if (error.response.status === 400) {
            mensaje = error.response.data.detail || 'Datos inválidos';
          } else if (error.response.status === 401) {
            this.$router.push('/login');
            return;
          } else if (error.response.status === 403) {
            mensaje = 'No tienes permiso para realizar esta acción';
          }
        }

        this.mensaje = mensaje;
        this.tipoMensaje = 'error';
      } finally {
        this.loading = false;
      }
    },

    mostrarModalGuardado() {
      this.mensajeExito = 'Curso creado correctamente.';
      this.mostrarModalExito = true;
    },

    cerrarModalExito() {
      this.mostrarModalExito = false;
    },

    cerrarModal() {
      this.mostrarModal = false;
      this.limpiarFormulario();
      this.limpiarErrores();
    },

    limpiarFormulario() {
      this.curso = {
        asignatura: '',
        docente: '',
        periodo: ''
      };
      this.docenteNombre = '';
    },

    limpiarErrores() {
      this.errors = {};
      this.mensaje = '';
    },

    mostrarMensaje(texto, tipo) {
      this.mensaje = texto;
      this.tipoMensaje = tipo;
      setTimeout(() => {
        this.mensaje = '';
      }, 5000);
    }
  }
}
</script>

<style scoped lang="scss">
@import '@/assets/styles/variables';
@import '@/assets/styles/base';

/* Contenedor principal */
.cursos-container {
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

/* Tabla Section - Estilos del AsignarDocente */
.tabla-section {
  margin-top: 2rem;
}

.card-tabla {
  background: white;
  border-radius: 12px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
  border: 1px solid $border-color;
  overflow: hidden;
  
  h3 {
    background: $bg-lighter;
    margin: 0;
    padding: 1rem 1.5rem;
    color: $text-primary;
    font-size: 1.2rem;
    font-weight: 600;
    border-bottom: 1px solid $border-color;
  }
}

.tabla-container {
  overflow-x: auto;
  
  &::-webkit-scrollbar {
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

.tabla-cursos {
  width: 100%;
  border-collapse: collapse;
  font-size: 0.9rem;
  
  thead tr {
    background: $bg-lighter;
  }
  
  th {
    padding: 1rem;
    text-align: left;
    font-weight: 600;
    color: $text-secondary;
    border-bottom: 2px solid $border-color;
    font-size: 0.85rem;
    text-transform: uppercase;
    letter-spacing: 0.5px;
  }
  
  td {
    padding: 1rem;
    border-bottom: 1px solid rgba($border-color, 0.5);
    color: $text-primary;
    vertical-align: middle;
  }
  
  tbody tr {
    transition: background-color 0.2s ease;
    
    &:hover {
      background: rgba($color-primary, 0.02);
    }
    
    &:nth-child(even) {
      background: rgba($bg-lighter, 0.3);
      
      &:hover {
        background: rgba($color-primary, 0.04);
      }
    }
  }
}

.sin-docente {
  //color: $text-muted;
  font-style: italic;
  font-size: 0.85rem;
}

.empty-state {
  text-align: center;
  padding: 3rem;
  //color: $text-muted;
  font-size: 1.1rem;
  
  p {
    margin: 0;
    padding: 1rem 2rem;
    background: $bg-lighter;
    border-radius: 6px;
    display: inline-block;
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

.readonly-field {
  background: $bg-lighter !important;
  color: $text-secondary !important;
  cursor: not-allowed;
  font-style: italic;
}

.form-text {
  font-size: 0.8rem;
  //color: $text-muted;
  margin-top: 0.25rem;
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
  .cursos-container {
    padding: 1rem;
  }
  
  .tabla-cursos {
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