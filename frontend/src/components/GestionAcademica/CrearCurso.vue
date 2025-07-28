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
          
          <div v-if="curso.docente" class="alert alert-info mb-4">
            <i class="fas fa-info-circle me-2"></i>
            Docente asignado: {{ obtenerNombreDocente(curso.docente) }}
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
import axios from 'axios'

export default {
  name: 'CrearCurso',
  data() {
    return {
      curso: {
        asignatura: '',
        docente: '',
        periodo: ''
      },
      asignaturas: [],
      docentes: [],
      mensaje: null
    }
  },
  async mounted() {
    await this.cargarAsignaturas();
  },
  methods: {
    async cargarAsignaturas() {
      try {
        const token = localStorage.getItem('access_token');
        const [asignaturasRes, docentesRes] = await Promise.all([
          axios.get('http://localhost:8000/api/asignaturas/', {
            headers: { 'Authorization': `Bearer ${token}` }
          }),
          axios.get('http://localhost:8000/api/usuarios/docentes/', {
            headers: { 'Authorization': `Bearer ${token}` }
          })
        ]);
        
        this.asignaturas = asignaturasRes.data;
        this.docentes = docentesRes.data;
      } catch (error) {
        console.error('Error al cargar datos:', error);
        this.mostrarMensaje('Error al cargar los datos necesarios', 'error');
      }
    },
    
    obtenerNombreDocente(id) {
      const docente = this.docentes.find(d => d.id === id);
      return docente ? `${docente.nombres} ${docente.apellidos}` : 'No asignado';
    },
    
    mostrarMensaje(texto, tipo = 'success') {
      this.mensaje = { texto, tipo };
      setTimeout(() => {
        this.mensaje = null;
      }, 5000);
    },
    asignarDocente() {
      // Busca la asignatura seleccionada y asigna el docente responsable
      const asig = this.asignaturas.find(a => a.id === this.curso.asignatura);
      this.curso.docente = asig ? asig.docente_responsable : '';
    },
    async crearCurso() {
      try {
        const token = localStorage.getItem('access_token');
        await axios.post('http://localhost:8000/api/cursos/', this.curso, {
          headers: { 'Authorization': `Bearer ${token}` }
        });
        
        this.mostrarMensaje('Curso creado exitosamente');
        this.curso = { asignatura: '', docente: '', periodo: '' };
        this.$nextTick(() => {
          const form = document.querySelector('.needs-validation');
          form.classList.remove('was-validated');
        });
      } catch (error) {
        console.error('Error al crear curso:', error);
        const mensaje = error.response?.data?.detail || 'Error al crear el curso';
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