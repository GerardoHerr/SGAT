<template>
  <div class="container">
    <h2><i class="fas fa-plus-circle me-2"></i>Crear Nuevo Curso</h2>
    
    <div class="card">
      <div class="card-body">
        <form @submit.prevent="crearCurso" class="needs-validation" novalidate>
          <div class="form-group mb-4">
            <label for="asignatura" class="form-label">Asignatura</label>
            <select 
              id="asignatura" 
              v-model="curso.asignatura" 
              class="form-select" 
              required 
              @change="asignarDocente"
            >
              <option value="" disabled selected>Seleccione una asignatura</option>
              <option v-for="asig in asignaturas" :key="asig.id" :value="asig.id">
                {{ asig.nombre }}
              </option>
            </select>
            <div class="invalid-feedback">
              Por favor seleccione una asignatura
            </div>
          </div>
          
          <div class="form-group mb-4">
            <label for="periodo" class="form-label">Periodo Académico</label>
            <input 
              type="text" 
              id="periodo" 
              v-model="curso.periodo" 
              class="form-control" 
              placeholder="Ej: 2023-2"
              required 
            />
            <div class="form-text">Formato: AAAA-P (ej: 2023-2 para el segundo semestre del 2023)</div>
            <div class="invalid-feedback">
              Por favor ingrese el período académico
            </div>
          </div>
          <div class="form-actions">
            <button type="submit" class="btn btn-primary">
              <i class="fas fa-save me-2"></i>Crear Curso
            </button>
          </div>
        </form>
        
        <div v-if="mensaje" class="alert mt-4" :class="mensaje.tipo === 'error' ? 'alert-danger' : 'alert-success'">
          <i :class="mensaje.tipo === 'error' ? 'fas fa-exclamation-circle' : 'fas fa-check-circle'" class="me-2"></i>
          {{ mensaje.texto }}
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import api from '@/services/api';
import { authService } from '@/services/authService';

export default {
  name: 'CrearCurso',
  data() {
    return {
      asignaturas: [],
      docentes: [],
      curso: {
        asignatura: '',
        docente: '',
        periodo: ''
      },
      mensaje: null,
      currentUser: null,
      userEmail: ''
    };
  },
  async mounted() {
    this.currentUser = authService.getCurrentUser();
    if (this.currentUser) {
      this.userEmail = this.currentUser.email;
      console.log('Usuario actual:', this.currentUser);
    } else {
      console.warn('No se pudo obtener el usuario actual');
      this.$router.push('/login');
      return;
    }
    await this.cargarAsignaturas();
  },
  methods: {
    async cargarAsignaturas() {
      try {
        const response = await api.get('asignaturas/');
        this.asignaturas = response.data;
      } catch (error) {
        console.error('Error al cargar datos:', error);
        this.mostrarMensaje('Error al cargar los datos necesarios', 'error');
      }
    },
    
    async obtenerNombreDocente(email) {
      if (!email) return 'No asignado';
      try {
        const response = await api.get(`usuarios/by-email/?email=${encodeURIComponent(email)}`);
        if (response.data) {
          return `${response.data.nombres || ''} ${response.data.apellidos || ''}`.trim() || email;
        }
        return email;
      } catch (error) {
        console.error('Error al obtener docente:', error);
        return email; // Devolver el email si hay un error
      }
    },
    
    mostrarMensaje(texto, tipo = 'success') {
      this.mensaje = { texto, tipo };
      setTimeout(() => {
        this.mensaje = null;
      }, 5000);
    },
    async asignarDocente() {
      if (!this.curso.asignatura) return;
      
      try {
        const response = await api.get(`asignaturas/${this.curso.asignatura}/`);
        if (response.data && response.data.docente_responsable) {
          // Guardamos directamente el email del docente
          this.curso.docente = response.data.docente_responsable;
          
          // Si necesitas mostrar el nombre del docente, usa obtenerNombreDocente
          const nombreDocente = await this.obtenerNombreDocente(response.data.docente_responsable);
          console.log('Docente asignado:', nombreDocente);
        } else {
          console.warn('La asignatura no tiene docente responsable');
          this.mostrarMensaje('La asignatura seleccionada no tiene un docente asignado', 'advertencia');
        }
      } catch (error) {
        console.error('Error al obtener la asignatura:', error);
        this.mostrarMensaje('Error al cargar la información de la asignatura', 'error');
      }
    },
    async crearCurso() {
      try {
        // Verificar que se haya seleccionado una asignatura
        if (!this.curso.asignatura) {
          this.mostrarMensaje('Por favor selecciona una asignatura', 'error');
          return;
        }

        // Verificar que se haya seleccionado un docente
        if (!this.curso.docente) {
          this.mostrarMensaje('Por favor selecciona un docente', 'error');
          return;
        }

        // Verificar que se haya ingresado un período
        if (!this.curso.periodo) {
          this.mostrarMensaje('Por favor ingresa el período académico', 'error');
          return;
        }

        // Agregar el creador del curso (el administrador)
        const cursoData = {
          ...this.curso,
          creado_por: this.userEmail // Guardamos quién creó el curso (el admin)
        };

        const response = await api.post('cursos/', cursoData);
        console.log('Curso creado:', response.data);
        
        this.mostrarMensaje('Curso creado exitosamente');
        
        // Limpiar el formulario
        this.curso = { asignatura: '', docente: '', periodo: '' };
        
        // Resetear validación del formulario
        this.$nextTick(() => {
          const form = document.querySelector('.needs-validation');
          if (form) form.classList.remove('was-validated');
        });
      } catch (error) {
        console.error('Error al crear curso:', error);
        let mensaje = 'Error al crear el curso';
        
        if (error.response) {
          // Manejar errores específicos de la API
          if (error.response.status === 400) {
            mensaje = error.response.data.detail || 'Datos inválidos';
          } else if (error.response.status === 401) {
            this.$router.push('/login');
            return;
          } else if (error.response.status === 403) {
            mensaje = 'No tienes permiso para realizar esta acción';
          }
        }
        
        this.mostrarMensaje(mensaje, 'error');
      }
    }
  }
}
</script>

<style scoped lang="scss">
@import '@/assets/styles/variables';
@import '@/assets/styles/base';

.form-actions {
  display: flex;
  justify-content: flex-end;
  margin-top: 2rem;
  padding-top: 1rem;
  border-top: 1px solid $border-color;
}

.needs-validation .form-label {
  font-weight: 500;
  margin-bottom: 0.5rem;
}

.invalid-feedback {
  display: none;
  width: 100%;
  margin-top: 0.25rem;
  font-size: 0.875em;
  color: #dc3545;
}

.was-validated .form-control:invalid ~ .invalid-feedback,
.was-validated .form-select:invalid ~ .invalid-feedback {
  display: block;
}

.was-validated .form-control:invalid,
.was-validated .form-select:invalid {
  border-color: #dc3545;
  padding-right: calc(1.5em + 0.75rem);
  background-image: url("data:image/svg+xml,%3csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 12 12' width='12' height='12' fill='none' stroke='%23dc3545'%3e%3ccircle cx='6' cy='6' r='4.5'/%3e%3cpath stroke-linejoin='round' d='M5.8 3.6h.4L6 6.5z'/%3e%3ccircle cx='6' cy='8.2' r='.6' fill='%23dc3545' stroke='none'/%3e%3c/svg%3e");
  background-repeat: no-repeat;
  background-position: right calc(0.375em + 0.1875rem) center;
  background-size: calc(0.75em + 0.375rem) calc(0.75em + 0.375rem);
}

/* Estilos para el select personalizado */
.form-select {
  background-image: url("data:image/svg+xml,%3csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 16 16'%3e%3cpath fill='none' stroke='%23343a40' stroke-linecap='round' stroke-linejoin='round' stroke-width='2' d='m2 5 6 6 6-6'/%3e%3c/svg%3e");
  background-repeat: no-repeat;
  background-position: right 0.75rem center;
  background-size: 16px 12px;
  -webkit-appearance: none;
  -moz-appearance: none;
  appearance: none;
  padding-right: 2.25rem;
}

/* Ajustes responsivos */
@media (max-width: 768px) {
  .card {
    padding: 1rem;
  }
  
  .form-actions {
    .btn {
      width: 100%;
    }
  }
}
</style>