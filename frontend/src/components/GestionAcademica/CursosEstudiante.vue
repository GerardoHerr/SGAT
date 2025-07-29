<template>
  <div class="container py-4">
    <div class="header-bar">
      <h2 class="page-title">Mis Registros</h2>
      <button class="add-btn" @click="abrirModalSolicitud()">
        Nueva Solicitud
      </button>
    </div>

    <!-- Modal para solicitar asignaturas -->
    <div v-if="mostrarFormulario" class="modal-overlay" @click="cerrarModal">
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <h2>
            <i class="fas fa-book me-2"></i>Solicitar Asignatura
          </h2>
          <button class="close-btn" @click="cerrarModal">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
              stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>

        <div class="modal-body">
          <div v-if="asignaturas.length" class="asignaturas-list">
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
            })" :key="asignatura.id" class="asignatura-item">
              <div class="asignatura-info">
                <h6>{{ asignatura.nombre }}</h6>
                <small>Código: {{ asignatura.codigo || 'N/A' }}</small>
              </div>
              <button class="btn-solicitar" @click="enviarSolicitud(asignatura.id)">
                <i class="fas fa-paper-plane"></i>
                Solicitar
              </button>
            </div>
          </div>
          <div v-else class="empty-state">
            <i class="fas fa-inbox fa-3x"></i>
            <p>No hay asignaturas disponibles para solicitar.</p>
          </div>
        </div>

        <div class="modal-footer">
          <button class="btn-cancelar" @click="cerrarModal">
            <i class="fas fa-times"></i>
            Cancelar
          </button>
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

// Reemplazar todos los estilos del modal con estos:

.header-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid $border-color;

  .page-title {
    flex: 1;
    text-align: center;
    margin: 0;
    color: $text-primary;
    font-size: 1.8rem;
    font-weight: 600;
    position: relative;
    padding-bottom: 0.5rem;
    
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
    background: darken($color-primary, 10%);
    transform: translateY(-1px);
  }
}

/* Modal Styles */
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
  z-index: 1050;
  backdrop-filter: blur(4px);
}

.modal-content {
  background: white;
  border-radius: 16px;
  max-width: 600px;
  width: 90%;
  max-height: 80vh;
  overflow: hidden;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.15);
  border: 1px solid $border-color;
  animation: modalSlideIn 0.3s ease-out;
}

@keyframes modalSlideIn {
  from {
    opacity: 0;
    transform: translateY(-50px) scale(0.95);
  }
  to {
    opacity: 1;
    transform: translateY(0) scale(1);
  }
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.5rem;
  border-bottom: 1px solid $border-color;
  background: $bg-lighter;
  
  h2 {
    font-size: 1.4rem;
    font-weight: 600;
    color: $text-primary;
    margin: 0;
    display: flex;
    align-items: center;
    gap: 0.5rem;
    
    i {
      color: $color-primary;
    }
  }
}

.close-btn {
  background: none;
  border: none;
  padding: 0.5rem;
  cursor: pointer;
  color: $text-secondary;
  border-radius: 6px;
  transition: all 0.2s;
  
  &:hover {
    background: rgba($color-primary, 0.1);
    color: $color-primary;
  }
  
  svg {
    width: 20px;
    height: 20px;
  }
}

.modal-body {
  padding: 1.5rem;
  max-height: 50vh;
  overflow-y: auto;
  
  &::-webkit-scrollbar {
    width: 6px;
  }
  
  &::-webkit-scrollbar-track {
    background: $bg-lighter;
    border-radius: 3px;
  }
  
  &::-webkit-scrollbar-thumb {
    background: $color-primary;
    border-radius: 3px;
    
    &:hover {
      background: darken($color-primary, 10%);
    }
  }
}

.asignaturas-list {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.asignatura-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem;
  border: 1px solid $border-color;
  border-radius: 8px;
  transition: all 0.2s ease;
  background: white;
  
  &:hover {
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
    border-color: $color-primary;
    transform: translateY(-1px);
  }
}

.asignatura-info {
  flex: 1;
  
  h6 {
    font-weight: 600;
    margin: 0 0 0.25rem 0;
    color: $text-primary;
    font-size: 1rem;
  }
  
  small {
    color: $text-secondary;
    font-size: 0.85rem;
  }
}

.btn-solicitar {
  background: $color-primary;
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 6px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.9rem;
  
  &:hover {
    background: darken($color-primary, 10%);
    transform: translateY(-1px);
    box-shadow: 0 4px 8px rgba($color-primary, 0.3);
  }
  
  i {
    font-size: 0.8rem;
  }
}

.empty-state {
  text-align: center;
  padding: 3rem 1rem;
  color: $text-secondary;
  
  i {
    //color: $text-muted;
    margin-bottom: 1rem;
    opacity: 0.5;
  }
  
  p {
    margin: 0;
    font-size: 1.1rem;
  }
}

.modal-footer {
  padding: 1rem 1.5rem;
  border-top: 1px solid $border-color;
  background: $bg-lighter;
  display: flex;
  justify-content: flex-end;
}

.btn-cancelar {
  background: transparent;
  color: $text-secondary;
  border: 1px solid $border-color;
  padding: 0.5rem 1rem;
  border-radius: 6px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  
  &:hover {
    //background: rgba($color-danger, 0.1);
    //border-color: $color-danger;
    //color: $color-danger;
  }
  
  i {
    font-size: 0.8rem;
  }
}

// Mantener los demás estilos del card existentes...
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

/* Responsive */
@media (max-width: 767.98px) {
  .modal-content {
    width: 95%;
    margin: 1rem;
  }
  
  .asignatura-item {
    flex-direction: column;
    align-items: flex-start;
    gap: 0.75rem;
  }
  
  .btn-solicitar {
    align-self: flex-end;
  }
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