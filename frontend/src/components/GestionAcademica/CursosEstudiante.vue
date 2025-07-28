<template>
  <div class="container py-4">
    <div class="d-flex justify-content-between align-items-center mb-4">
      <h2 class="mb-0"><i class="fas fa-graduation-cap me-2"></i>Mis Registros</h2>
      <button class="btn btn-primary" @click="abrirModalSolicitud">
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
              <div v-for="asignatura in asignaturas.filter(a => {
                // Excluir si hay solicitud pendiente o aceptada para esta asignatura
                const id = a.id;
                const nombre = a.nombre?.trim().toLowerCase();
                const codigoNombre = (a.codigo ? a.codigo + ' - ' : '') + a.nombre;
                const codigoNombreNorm = codigoNombre.trim().toLowerCase();
                return !((solicitudesPendientes && solicitudesPendientes.some(s => {
                  if (typeof s.asignatura === 'number' || !isNaN(Number(s.asignatura))) return Number(s.asignatura) === id;
                  if (typeof s.asignatura === 'string') {
                    const sNorm = s.asignatura.trim().toLowerCase();
                    return sNorm === nombre || sNorm === codigoNombreNorm;
                  }
                  return false;
                })) || (solicitudesAceptadas && solicitudesAceptadas.some(s => {
                  if (typeof s.asignatura === 'number' || !isNaN(Number(s.asignatura))) return Number(s.asignatura) === id;
                  if (typeof s.asignatura === 'string') {
                    const sNorm = s.asignatura.trim().toLowerCase();
                    return sNorm === nombre || sNorm === codigoNombreNorm;
                  }
                  return false;
                })));
              })" :key="asignatura.id"
                   class="list-group-item d-flex justify-content-between align-items-center">
                <div>
                  <h6 class="mb-1">{{ asignatura.nombre }}</h6>
                  <small class="text-muted">Código: {{ asignatura.codigo || 'N/A' }}</small>
                </div>
                <button class="btn btn-sm btn-outline-primary" 
                        @click="enviarSolicitud(asignatura.id)">
                  <i class="fas fa-paper-plane me-1"></i>
                  Solicitar
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
    <div v-else class="text-center py-5"></div>
    <!-- Tabla de otras solicitudes del estudiante logeado -->
    <div v-if="solicitudes && solicitudes.length" class="mt-4">
      <h4 class="mb-3"><i class="fas fa-list-alt text-primary me-2"></i>Otras Solicitudes de Asignatura</h4>
      <table class="table table-bordered table-striped">
        <thead>
          <tr>
            <th>Asignatura</th>
            <th>Estado</th>
            <th>Fecha Solicitud</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="sol in solicitudes.filter(s => s && s.estado !== 'aceptada')" :key="'otra-'+sol.id">
            <td>{{ sol.asignatura }}</td>
            <td>
              <span v-if="sol.estado === 'pendiente'" class="badge bg-warning text-dark">Pendiente</span>
              <span v-else-if="sol.estado === 'rechazada'" class="badge bg-danger">Rechazada</span>
              <span v-else class="badge bg-secondary">{{ sol.estado }}</span>
            </td>
            <td>{{ sol.fecha_solicitud ? sol.fecha_solicitud.replace('T', ' ').slice(0, 16) : '-' }}</td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Tabla de solicitudes aceptadas del estudiante logeado -->
    <div v-if="solicitudesAceptadas.length" class="mt-5">
      <h4 class="mb-3"><i class="fas fa-check-circle text-success me-2"></i>Solicitudes de Asignatura Aceptadas</h4>
      <table class="table table-bordered table-striped">
        <thead>
          <tr>
            <th>Asignatura</th>
            <th>Estado</th>
            <th>Fecha Solicitud</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="sol in solicitudesAceptadas" :key="sol.id">
            <td>{{ sol.asignatura }}</td>
            <td><span class="badge bg-success">Aceptada</span></td>
            <td>{{ sol.fecha_solicitud ? sol.fecha_solicitud.replace('T', ' ').slice(0, 16) : '-' }}</td>
          </tr>
        </tbody>
      </table>
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
      solicitudesAceptadas: [],
      mostrarFormulario: false,
      loading: false,
      error: null,
      estudianteId: null,
      currentUser: null
    };
  },
  methods: {
    abrirModalSolicitud() {
      this.mostrarFormulario = true;
      this.cargarDatosModal();
    },
    async cargarSolicitudes() {
      try {
        const token = localStorage.getItem('access_token');
        const response = await axios.get('http://localhost:8000/api/solicitudAsignatura/', {
          headers: { Authorization: `Bearer ${token}` }
        });
        this.solicitudes = response.data; // Guardar todas las solicitudes
        console.log('Solicitudes cargadas:', this.solicitudes);
        this.solicitudesPendientes = response.data.filter(s => s.estado === 'pendiente');
        this.solicitudesAceptadas = response.data.filter(s => s.estado === 'aceptada');
        console.log('Solicitudes aceptadas:', this.solicitudesAceptadas);
        console.log('Solicitudes pendientes:', this.solicitudesPendientes);
      } catch (error) {
        console.error('Error al cargar solicitudes:', error);
      }
    },
    async cargarCursos() {
      try {
        const currentUser = JSON.parse(localStorage.getItem('currentUser'));
        const email = currentUser?.email;
        const cursosResp = await axios.get(`http://localhost:8000/api/cursos/?estudiante_email=${email}`);
        console.log('Cursos cargados solo acep:', cursosResp.data);
        let cursos = cursosResp.data;
        // Filtrar cursos para mostrar solo los aceptados
        await this.cargarSolicitudes();
        // Filtrar solicitudes aceptadas solo del estudiante logeado
        const estudianteId = this.currentUser?.id;
        const solicitudesAceptadas = (this.solicitudes || []).filter(s => s.estado === 'aceptado' && s.estudiante === estudianteId);
        // Normalizar ids y nombres de asignaturas aceptadas
        const aceptadasIds = [];
        const aceptadasNombres = [];
        solicitudesAceptadas.forEach(s => {
          if (typeof s.asignatura === 'number' || !isNaN(Number(s.asignatura))) {
            aceptadasIds.push(Number(s.asignatura));
          } else if (typeof s.asignatura === 'string') {
            aceptadasNombres.push(s.asignatura.trim().toLowerCase());
          }
        });
        // Mostrar cursos que correspondan a esas asignaturas aceptadas
        this.cursos = cursos.filter(curso => {
          // Validar que el curso pertenezca al estudiante actual (por email o id si está disponible)
          if (curso.estudiante_email && curso.estudiante_email !== email) return false;
          if (curso.estudiante && this.currentUser && curso.estudiante !== this.currentUser.id) return false;

          // Comparar por id
          if (aceptadasIds.includes(curso.asignatura)) return true;
          // Comparar por nombre
          const nombreNormalizado = (curso.asignatura_nombre || '').trim().toLowerCase();
          if (aceptadasNombres.includes(nombreNormalizado)) return true;
          // Comparar por "codigo - nombre"
          const nombreCompuesto = (curso.asignatura_codigo ? curso.asignatura_codigo + ' - ' : '') + (curso.asignatura_nombre || '');
          const nombreCompuestoNormalizado = nombreCompuesto.trim().toLowerCase();
          if (aceptadasNombres.includes(nombreCompuestoNormalizado)) return true;
          return false;
        });
        console.log('Cursos aceptados cargados:', this.cursos);
      } catch (error) {
        this.cursos = [];
        console.error('Error al cargar cursos:', error);
      }
    },
    revisarCurso(cursoId) {
      this.$router.push({ name: 'ListarTareasEstudiante', params: { id: cursoId } });
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
      // Cargar solicitudes primero
      await this.cargarSolicitudes();
      // Luego cargar todas las asignaturas y filtrar las que ya tienen solicitud pendiente o aceptada
      try {
        const response = await axios.get('http://localhost:8000/api/asignaturas/');
        console.log('Asignaturas cargadas:', response.data);
        console.log('Solicitudes pendientes:', this.solicitudesPendientes);
        // Obtener IDs de asignaturas con solicitud pendiente o aceptada
        // Excluir asignaturas con solicitud pendiente o aceptada, comparando por id o nombre
        const excluidasIds = [];
        const excluidasNombres = [];
        (this.solicitudes || [])
          .filter(s => s.estado === 'pendiente' || s.estado === 'aceptado')
          .forEach(s => {
            if (typeof s.asignatura === 'number' || !isNaN(Number(s.asignatura))) {
              excluidasIds.push(Number(s.asignatura));
              console.log(`Excluyendo asignatura por ID: ${s.asignatura}`);
            } else if (typeof s.asignatura === 'string') {
              excluidasNombres.push(s.asignatura.trim());
            }
          });
        // Filtrar asignaturas que no tienen solicitud pendiente ni aceptada
        this.asignaturas = response.data.filter(a => {
          // Excluir si el id está en excluidasIds
          if (excluidasIds.includes(a.id)) return false;
          // Excluir si el nombre o el string "codigo - nombre" está en excluidasNombres (ignorando mayúsculas/minúsculas y espacios)
          const nombreNormalizado = a.nombre.trim().toLowerCase();
          const nombreCompuesto = (a.codigo ? a.codigo + ' - ' : '') + a.nombre;
          const nombreCompuestoNormalizado = nombreCompuesto.trim().toLowerCase();
          return !excluidasNombres.some(n => {
            const nNorm = n.trim().toLowerCase();
            return nNorm === nombreNormalizado || nNorm === nombreCompuestoNormalizado;
          });
        });
      } catch (error) {
        this.asignaturas = [];
        console.error('Error al cargar asignaturas:', error);
      }
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
