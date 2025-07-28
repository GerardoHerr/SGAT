<template>
  <div class="container mt-5">
    <h2>Solicitudes de Asignatura</h2>

    <!-- Botón para abrir el modal -->
    <button class="btn-principal" @click="mostrarFormulario = true">
      Nueva Solicitud
    </button>

    <!-- Modal personalizado -->
    <div v-if="mostrarFormulario" class="modal-overlay">
      <div class="modal-contenido animate-entrada">
        <h3>Solicitar Asignatura</h3>
        <div v-if="asignaturas.length">
          <div
            class="asignatura-item"
            v-for="asignatura in asignaturas"
            :key="asignatura.id"
          >
            <span>{{ asignatura.nombre }}</span>
            <button class="btn-enviar" @click="enviarSolicitud(asignatura.id)">
              Solicitar
            </button>
          </div>
        </div>
        <div v-else>
          <p>No hay asignaturas disponibles para solicitar.</p>
        </div>

        <div class="botones mt-3">
          <button class="btn-cancelar" @click="cerrarModal">Cancelar</button>
        </div>
      </div>
    </div>

    <!-- Lista de cursos del estudiante logeado -->
    <div v-if="cursos.length" class="mt-4">
      <h4>Mis Cursos</h4>
      <ul class="list-group">
        <li
          v-for="curso in cursos"
          :key="curso.id"
          class="list-group-item d-flex justify-content-between align-items-center"
        >
          <span>
            {{ curso.asignatura_nombre || 'Sin nombre' }}<br>
            <small>Periodo: {{ curso.periodo || 'Sin periodo' }}</small>
          </span>
          <button class="btn-revisar" @click="revisarCurso(curso.id)">Revisar</button>
        </li>
      </ul>
    </div>
    <div v-else class="mt-3">
      <p>No tienes cursos asignados aún.</p>
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
      mostrarFormulario: false,
      asignaturas: [],
      solicitudes: [],
      cursos: [],
      cursoSeleccionado: null,
      estudianteEmail: '',
    };
  },
  methods: {
    async cargarSolicitudes() {
      try {
        const token = localStorage.getItem('access_token');
        const response = await axios.get('http://localhost:8000/api/solicitudAsignatura/', {
          headers: { Authorization: `Bearer ${token}` }
        });
        this.solicitudes = response.data;
        //this.$router.push({ name: 'MostarTareasEstudiante', params: { cursoId } });
      } catch (error) {
        console.error('Error al cargar solicitudes:', error);
      }
    },
    async cargarCursos() {
      try {
        const currentUser = JSON.parse(localStorage.getItem('currentUser'));
        const email = currentUser?.email;
        const cursosResp = await axios.get(`http://localhost:8000/api/cursos/?estudiante_email=${email}`);
        this.cursos = cursosResp.data;
        console.log('Cursos cargados:', this.cursos);
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
        const aceptadasIds = this.solicitudes
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
  watch: {
    async mostrarFormulario(val) {
      if (val) {
        await this.cargarDatosModal();
      }
    }
  },
  mounted() {
    this.cargarSolicitudes();
    this.cargarCursos();
    const currentUser = JSON.parse(localStorage.getItem('currentUser'));
    if (currentUser && currentUser.email) {
      this.estudianteEmail = currentUser.email;
    }
  }
};
</script>

<style scoped>
.btn-revisar {
  background-color: #3a86ff;
  color: white;
  border: none;
  padding: 8px 16px;
  border-radius: 6px;
  cursor: pointer;
  transition: background-color 0.3s;
}
.btn-revisar:hover {
  background-color: #265ecf;
}
/* Tipografía general */
* {
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

/* Botón principal */
.btn-principal {
  background-color: #3a86ff;
  color: white;
  border: none;
  padding: 12px 20px;
  border-radius: 8px;
  cursor: pointer;
  font-size: 16px;
  transition: background-color 0.3s;
}
.btn-principal:hover {
  background-color: #265ecf;
}

/* Fondo del modal */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 999;
}

/* Contenedor del modal */
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
