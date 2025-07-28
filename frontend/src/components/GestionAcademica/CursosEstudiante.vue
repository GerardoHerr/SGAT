<template>
  <div class="container py-4">
    <div class="d-flex justify-content-between align-items-center mb-4">
      <h2 class="mb-0"><i class="fas fa-graduation-cap me-2"></i>Mis Cursos</h2>
      <button class="btn btn-primary" @click="mostrarFormulario = true">
        <i class="fas fa-plus-circle me-2"></i>Nueva Solicitud
      </button>
    </div>

    <!-- Modal para solicitar asignaturas -->
    <div v-if="mostrarFormulario" class="modal" tabindex="-1" style="display: block; background-color: rgba(0,0,0,0.5);">
      <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">
              <i class="fas fa-book me-2"></i>Solicitar Asignatura
            </h5>
            <button type="button" class="btn-close" @click="cerrarModal" aria-label="Cerrar"></button>
          </div>
          <div class="modal-body">
            <div v-if="asignaturas.length" class="list-group">
              <div v-for="asignatura in asignaturas" :key="asignatura.id" 
                   class="list-group-item d-flex justify-content-between align-items-center">
                <div>
                  <h6 class="mb-1">{{ asignatura.nombre }}</h6>
                  <small class="text-muted">Código: {{ asignatura.codigo || 'N/A' }}</small>
                </div>
                <button class="btn btn-sm btn-outline-primary" 
                        @click="enviarSolicitud(asignatura.id)"
                        :disabled="solicitudesPendientes.some(s => s.asignatura === asignatura.id)">
                  <i class="fas fa-paper-plane me-1"></i>
                  {{ solicitudesPendientes.some(s => s.asignatura === asignatura.id) ? 'Solicitado' : 'Solicitar' }}
                </button>
              </div>
            </div>
            <div v-else class="text-center py-4">
              <i class="fas fa-inbox fa-3x text-muted mb-3"></i>
              <p class="mb-0">No hay asignaturas disponibles para solicitar.</p>
            </div>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-outline-secondary" @click="cerrarModal">
              <i class="fas fa-times me-1"></i>Cancelar
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Lista de cursos del estudiante -->
    <div v-if="cursos.length" class="row g-4 mt-2">
      <div v-for="curso in cursos" :key="curso.id" class="col-12 col-md-6 col-lg-4">
        <div class="card h-100 border-0 shadow-sm">
          <div class="card-body">
            <div class="d-flex justify-content-between align-items-start mb-3">
              <div>
                <h5 class="card-title mb-1">{{ curso.asignatura_nombre || curso.asignatura }}</h5>
                <span class="badge bg-primary bg-opacity-10 text-primary">
                  {{ curso.periodo || 'Sin período' }}
                </span>
              </div>
              <i class="fas fa-book text-muted fa-2x opacity-25"></i>
            </div>
            
            <div class="d-flex justify-content-between align-items-center mt-4">
              <span class="text-muted small">
                <i class="fas fa-tasks me-1"></i>
                {{ curso.tareas_pendientes || 0 }} tareas pendientes
              </span>
              <button class="btn btn-outline-primary btn-sm" @click="revisarCurso(curso.id)">
                <i class="fas fa-eye me-1"></i>Ver curso
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
    <div v-else class="text-center py-5">
      <i class="fas fa-book-open fa-3x text-muted mb-3"></i>
      <p class="text-muted">No tienes cursos asignados aún.</p>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import MostarTareasEstudiante from '../GestionTarea/MostarTareasEstudiante.vue';

export default {
  components: {
    MostarTareasEstudiante
  },
  data() {
    return {
      cursos: [],
      asignaturas: [],
      solicitudesPendientes: [],
      mostrarFormulario: false,
      loading: false,
      error: null,
      estudianteId: null,
      currentUser: null
    };
  },
  methods: {
    async cargarSolicitudes() {
      try {
        const token = localStorage.getItem('access_token');
        const response = await axios.get('http://localhost:8000/api/solicitudAsignatura/', {
          headers: { Authorization: `Bearer ${token}` }
        });
        this.solicitudesPendientes = response.data.filter(s => s.estado === 'pendiente');
      } catch (error) {
        console.error('Error al cargar solicitudes:', error);
      }
    },
    async cargarCursos() {
      try {
        const currentUser = JSON.parse(localStorage.getItem('currentUser'));
        if (!currentUser || currentUser.rol !== 'EST') return;

        // 1. Trae todas las solicitudes aceptadas del estudiante
        const solicitudesResp = await axios.get(`http://localhost:8000/api/solicitudAsignatura/?estudiante=${currentUser.email}`);
        const solicitudesAceptadas = solicitudesResp.data.filter(s => s.estado === 'aceptado');

        // 2. Obtén los IDs de asignaturas aceptadas
        const asignaturasAceptadasIds = solicitudesAceptadas.map(s => s.asignatura.id || s.asignatura);

        // 3. Trae todos los cursos y filtra solo los que correspondan a esas asignaturas
        const cursosResp = await axios.get('http://localhost:8000/api/cursos/');
        this.cursos = cursosResp.data.filter(curso =>
          asignaturasAceptadasIds.includes(curso.asignatura)
          || asignaturasAceptadasIds.includes(curso.asignatura_id)
          || asignaturasAceptadasIds.includes(curso.asignatura?.id)
        );
      } catch (error) {
        this.cursos = [];
        console.error('Error al cargar cursos:', error);
      }
    },
    revisarCurso(cursoId) {
      this.$router.push({ path: '/estudiante/listar-tareas', query: { curso: cursoId } });
    },
    async cargarAsignaturas() {
      try {
        const response = await axios.get('http://localhost:8000/api/asignaturas/');
           
        // Obtener IDs de asignaturas que ya están aceptadas
        const aceptadasIds = this.solicitudesPendientes
          .filter(s => {
            return s.estado === 'aceptado';
          })
          .map(s => {
            // Buscar la asignatura que contenga el nombre en el string
            const asignaturaEncontrada = response.data.find(asig => {
              const coincide = s.asignatura.includes(asig.nombre);
              return coincide;
            });
            
            if (asignaturaEncontrada) {
              return asignaturaEncontrada.id;
            }
            
            console.log(`No se encontró asignatura para: ${s.asignatura}`);
            return null;
          })
          .filter(id => id !== null); // Filtrar los nulls
        
        // Filtrar asignaturas que no están aceptadas
        this.asignaturas = response.data.filter(a => {
          const incluida = aceptadasIds.includes(a.id);
          return !incluida;
        });
      } catch (error) {
        console.error('Error al cargar asignaturas:', error);
      }
    },
    async cargarDatosModal() {
      // Primero cargar solicitudes, luego asignaturas para que el filtro funcione
      await this.cargarSolicitudes();
      await this.cargarAsignaturas();
    },
    async enviarSolicitud(asignaturaId) {
      try {
        const token = localStorage.getItem('access_token');
        await axios.post('http://localhost:8000/api/solicitudAsignatura/', { asignatura: asignaturaId }, {
          headers: { Authorization: `Bearer ${token}` }
        });
        alert(`Solicitud enviada para asignatura ID: ${asignaturaId}`);
        this.cerrarModal();
        await this.cargarSolicitudes(); // actualizar solicitudes
      } catch (error) {
        console.error('Error al enviar solicitud:', error);
        alert('Hubo un error al enviar la solicitud');
      }
    },
    cerrarModal() {
      this.mostrarFormulario = false;
    }
  },
  mounted() {
    this.currentUser = JSON.parse(localStorage.getItem('currentUser'));
    if (!this.currentUser || this.currentUser.rol !== 'EST') {
      this.$router.push('/login');
      return;
    }
    
    if (this.currentUser.id) {
      this.estudianteId = this.currentUser.id;
      this.cargarCursos();
    } else {
      this.error = 'No se pudo cargar la información del usuario';
    }
  }
};
</script>

<style scoped lang="scss">
@import '@/assets/styles/variables';
@import '@/assets/styles/base';

.modal {
  z-index: 1050;
  
  .modal-content {
    border: none;
    border-radius: $border-radius;
    box-shadow: $shadow-lg;
  }
  
  .modal-header {
    border-bottom: 1px solid $border-color;
    padding: 1.25rem 1.5rem;
    
    .modal-title {
      font-weight: 600;
      color: $text-primary;
    }
  }
  
  .modal-body {
    padding: 1.5rem;
    
    .list-group-item {
      border-left: none;
      border-right: none;
      padding: 1rem 1.25rem;
      
      &:first-child {
        border-top: none;
      }
      
      &:last-child {
        border-bottom: none;
      }
      
      h6 {
        font-weight: 500;
        margin-bottom: 0.25rem;
      }
    }
  }
  
  .modal-footer {
    border-top: 1px solid $border-color;
    padding: 1rem 1.5rem;
  }
}

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
    margin-bottom: 0.5rem;
  }
  
  .badge {
    font-weight: 500;
    padding: 0.35em 0.65em;
  }
  
  .btn-outline-primary {
    &:hover {
      background-color: $color-primary;
      border-color: $color-primary;
    }
  }
}

/* Ajustes responsivos */
@media (max-width: 767.98px) {
  .card {
    margin-bottom: 1rem;
  }
  
  .modal-dialog {
    margin: 0.5rem;
  }
}
.modal-contenido {
  background-color: #fff;
  padding: 25px 30px;
  border-radius: 15px;
  width: 420px;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.3);
}

/* Animación de entrada */
.animate-entrada {
  animation: fadeInScale 0.3s ease-in-out;
}

@keyframes fadeInScale {
  0% {
    opacity: 0;
    transform: scale(0.9);
  }
  100% {
    opacity: 1;
    transform: scale(1);
  }
}

/* Campos del formulario */
label {
  display: block;
  margin-bottom: 6px;
  font-weight: bold;
}
select {
  width: 100%;
  padding: 10px;
  border-radius: 6px;
  border: 1px solid #ccc;
  margin-bottom: 20px;
}

/* Botones dentro del modal */
.botones {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}
.btn-enviar {
  background-color: #28a745;
  color: white;
  border: none;
  padding: 10px 16px;
  border-radius: 6px;
  cursor: pointer;
  transition: background-color 0.3s;
}
.btn-enviar:hover {
  background-color: #218838;
}
.btn-cancelar {
  background-color: #dc3545;
  color: white;
  border: none;
  padding: 10px 16px;
  border-radius: 6px;
  cursor: pointer;
  transition: background-color 0.3s;
}
.btn-cancelar:hover {
  background-color: #c82333;
}
.asignatura-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 0;
  border-bottom: 1px solid #eee;
}

.asignatura-item:last-child {
  border-bottom: none;
}
</style>
