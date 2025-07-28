<template>
  <div class="container">
    <h2>Solicitudes de Asignaturas</h2>
    <div class="table-container">
      <table>
        <thead>
          <tr>
            <th>Estudiante</th>
            <th>Asignatura</th>
            <th>Estado</th>
            <th>Acciones</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="solicitud in solicitudes" :key="solicitud.id">
            <td>{{ solicitud.estudiante }}</td>
            <td>{{ solicitud.asignatura }}</td>
            <td>
              <span :class="`badge ${getEstadoClass(solicitud.estado)}`">
                {{ solicitud.estado }}
              </span>
            </td>
            <td>
              <button
                v-if="solicitud.estado === 'pendiente'"
                class="btn btn-primary"
                @click="aceptarSolicitud(solicitud.id)"
              >
                <i class="fas fa-check"></i> Aceptar
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'AceptarSolicitudes',
  data() {
    return {
      solicitudes: [],
    }
  },
  methods: {
    getEstadoClass(estado) {
      const estados = {
        'pendiente': 'badge-warning',
        'aceptada': 'badge-success',
        'rechazada': 'badge-danger'
      };
      return estados[estado] || 'badge-secondary';
    },
    
    async cargarSolicitudes() {
      try {
        const token = localStorage.getItem('access_token')
        const response = await axios.get('http://localhost:8000/api/solicitudAsignatura/', {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        })
        this.solicitudes = response.data
      } catch (error) {
        console.error('Error al cargar solicitudes:', error)
      }
    },
    async aceptarSolicitud(id) {
      try {
        const token = localStorage.getItem('access_token')
        await axios.patch(
          `http://localhost:8000/api/solicitudAsignatura/${id}/`, 
          { estado: 'aceptada' },  // Cambiado de 'aceptado' a 'aceptada'
          {
            headers: {
              'Authorization': `Bearer ${token}`,
              'Content-Type': 'application/json'
            }
          }
        )
        this.cargarSolicitudes() // recargar lista
      } catch (error) {
        console.error('Error al aceptar solicitud:', error)
        if (error.response) {
          console.error('Detalles del error:', error.response.data)
        }
      }
    },
  },
  mounted() {
    this.cargarSolicitudes()
  },
}
</script>

<style scoped lang="scss">
@import '@/assets/styles/variables';
@import '@/assets/styles/base';

.badge {
  display: inline-block;
  padding: 0.35em 0.65em;
  font-size: 0.75em;
  font-weight: 700;
  line-height: 1;
  text-align: center;
  white-space: nowrap;
  vertical-align: baseline;
  border-radius: 0.25rem;
  text-transform: capitalize;

  &-success {
    color: #155724;
    background-color: #d4edda;
  }
  
  &-warning {
    color: #856404;
    background-color: #fff3cd;
  }
  
  &-danger {
    color: #721c24;
    background-color: #f8d7da;
  }
}

table {
  th:last-child,
  td:last-child {
    text-align: right;
  }
}
</style>
