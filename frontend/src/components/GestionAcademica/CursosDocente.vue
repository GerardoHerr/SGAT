<template>
  <div class="container">
    <div class="d-flex justify-content-between align-items-center mb-4">
      <h2 class="mb-0"><i class="fas fa-chalkboard-teacher me-2"></i>Mis Cursos</h2>
      <div v-if="cursos.length > 0" class="text-muted">
        {{ cursos.length }} curso{{ cursos.length !== 1 ? 's' : '' }} asignado{{ cursos.length !== 1 ? 's' : '' }}
      </div>
    </div>
    
    <div v-if="loading" class="text-center py-5">
      <div class="spinner-border text-primary" role="status">
        <span class="visually-hidden">Cargando...</span>
      </div>
      <p class="mt-2 text-muted">Cargando tus cursos...</p>
    </div>
    
    <div v-else>
      <div v-if="cursos.length === 0" class="alert alert-light text-center py-4">
        <i class="fas fa-info-circle fa-2x mb-3 text-muted"></i>
        <h5 class="mb-2">No tienes cursos asignados</h5>
        <p class="text-muted mb-0">Ponte en contacto con el administrador para que te asigne cursos.</p>
      </div>
      
      <div v-else class="row g-4">
        <div v-for="curso in cursos" :key="curso.id" class="col-12 col-md-6 col-lg-4">
          <div class="card h-100 border-0 shadow-sm">
            <div class="card-body">
              <div class="d-flex justify-content-between align-items-start mb-3">
                <div>
                  <h5 class="card-title mb-1">{{ curso.asignatura_nombre }}</h5>
                  <span class="badge bg-primary bg-opacity-10 text-primary">
                    {{ curso.periodo }}
                  </span>
                </div>
                <div class="dropdown">
                  <button class="btn btn-sm btn-outline-secondary rounded-circle" type="button" data-bs-toggle="dropdown">
                    <i class="fas fa-ellipsis-v"></i>
                  </button>
                  <ul class="dropdown-menu dropdown-menu-end">
                    <li>
                      <button 
                        class="dropdown-item" 
                        @click="irAgregarTarea(curso.id)"
                        :disabled="curso.cantidad_estudiantes === 0"
                      >
                        <i class="fas fa-plus-circle me-2"></i>Agregar Tarea
                      </button>
                    </li>
                    <li>
                      <button 
                        class="dropdown-item" 
                        @click="irMostrarTareas(curso.id)"
                        :disabled="curso.cantidad_estudiantes === 0"
                      >
                        <i class="fas fa-tasks me-2"></i>Ver Tareas
                      </button>
                    </li>
                    <li><hr class="dropdown-divider"></li>
                    <li>
                      <button class="dropdown-item text-muted" disabled>
                        <i class="fas fa-users me-2"></i>
                        {{ curso.cantidad_estudiantes }} estudiante{{ curso.cantidad_estudiantes !== 1 ? 's' : '' }}
                      </button>
                    </li>
                  </ul>
                </div>
              </div>
              
              <div class="d-flex align-items-center text-muted small mb-3">
                <i class="fas fa-user-tie me-2"></i>
                <span class="text-truncate">{{ curso.docente_nombre || 'Sin docente asignado' }}</span>
              </div>
              
              <div class="d-grid gap-2">
                <button 
                  class="btn btn-outline-primary"
                  @click="irAgregarTarea(curso.id)"
                  :disabled="curso.cantidad_estudiantes === 0"
                >
                  <i class="fas fa-plus-circle me-2"></i>Nueva Tarea
                </button>
                <button 
                  class="btn btn-outline-secondary"
                  @click="irMostrarTareas(curso.id)"
                  :disabled="curso.cantidad_estudiantes === 0"
                >
                  <i class="fas fa-tasks me-2"></i>Ver Tareas
                </button>
              </div>
            </div>
            
            <div class="card-footer bg-transparent border-top-0 pt-0">
              <div class="d-flex justify-content-between align-items-center">
                <span class="badge bg-light text-muted">
                  <i class="fas fa-users me-1"></i>
                  {{ curso.cantidad_estudiantes }} estudiante{{ curso.cantidad_estudiantes !== 1 ? 's' : '' }}
                </span>
                <a href="#" class="small" @click.prevent="">
                  Ver detalles <i class="fas fa-chevron-right small ms-1"></i>
                </a>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'CursosDocente',
  data() {
    return {
      cursos: [],
      loading: true,
      docenteEmail: '',
      currentUser: null
    };
  },
  async mounted() {
    this.currentUser = JSON.parse(localStorage.getItem('currentUser'));
    
    if (!this.currentUser || this.currentUser.rol !== 'DOC') {
      this.$router.push('/login');
      return;
    }
    
    this.docenteEmail = this.currentUser.email;
    await this.cargarCursos();
  },
  methods: {
    async cargarCursos() {
      try {
        // Usar query param docente_email en vez de ruta /docente/<email>/
        const response = await fetch(`http://localhost:8000/api/cursos/?docente_email=${encodeURIComponent(this.currentUser.email)}`, {
          headers: { 'Content-Type': 'application/json' }
        });
        if (!response.ok) {
          throw new Error('Error al cargar los cursos');
        }
        this.cursos = await response.json();
      } catch (error) {
        console.error('Error al cargar los cursos:', error);
        this.cursos = [];
        if (error.response?.status === 401) {
          this.$router.push('/login');
        }
      } finally {
        this.loading = false;
      }
    },
    irAgregarTarea(cursoId) {
      this.$router.push(`/docente/asignar-tareas/${cursoId}`);
    },
    irMostrarTareas(cursoId) {
      this.$router.push(`/docente/mostrar-tareas/${cursoId}`);
    }
  }
}
</script>

<style scoped lang="scss">
@import '@/assets/styles/variables';
@import '@/assets/styles/base';

.card {
  transition: transform 0.2s ease, box-shadow 0.2s ease;
  border: 1px solid $border-color;
  
  &:hover {
    transform: translateY(-4px);
    box-shadow: $shadow-md !important;
  }
  
  .card-title {
    font-weight: 600;
    color: $text-primary;
  }
  
  .badge {
    font-weight: 500;
    padding: 0.35em 0.65em;
  }
  
  .dropdown-toggle::after {
    display: none;
  }
  
  .btn-outline-secondary {
    border-color: $border-color;
    color: $text-secondary;
    
    &:hover {
      background-color: $bg-light;
      border-color: darken($border-color, 10%);
    }
  }
}

/* Estilos para los botones deshabilitados */
.btn:disabled,
.dropdown-item:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

/* Ajustes responsivos */
@media (max-width: 767.98px) {
  .card {
    margin-bottom: 1rem;
  }
  
  .btn {
    padding: 0.375rem 0.5rem;
    font-size: 0.875rem;
  }
}

/* Animación de carga */
@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}

.alert {
  animation: fadeIn 0.3s ease-out;
}

/* Mejoras de accesibilidad */
:focus {
  outline: 2px solid $color-primary;
  outline-offset: 2px;
}

/* Estilos para el menú desplegable */
.dropdown-menu {
  border: 1px solid $border-color;
  box-shadow: $shadow-sm;
  
  .dropdown-item {
    padding: 0.5rem 1rem;
    font-size: 0.9rem;
    
    i {
      width: 1.25rem;
      text-align: center;
      margin-right: 0.5rem;
      color: $text-secondary;
    }
    
    &:hover, &:focus {
      background-color: $color-primary-bg;
      color: $color-primary-dark;
      
      i {
        color: $color-primary;
      }
    }
  }
}

.btn-mostrar-tareas {
  font-size: 15px;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.2s, box-shadow 0.2s;
}

.btn-mostrar-tareas:disabled {
  background: #bfc9d1;
  color: #eee;
  cursor: not-allowed;
}
</style>
