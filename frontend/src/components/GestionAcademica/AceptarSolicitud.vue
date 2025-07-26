<template>
  <div class="container mt-5">
    <h2>Solicitudes de Asignaturas</h2>
    <table class="table table-bordered">
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
          <td>{{ solicitud.estado }}</td>
          <td>
            <button
              class="btn btn-success"
              v-if="solicitud.estado === 'pendiente'"
              @click="aceptarSolicitud(solicitud.id)"
            >
              Aceptar
            </button>
          </td>
        </tr>
      </tbody>
    </table>
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
        await axios.patch(`http://localhost:8000/api/solicitudAsignatura/${id}/`, {
          estado: 'aceptado',
        }, {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        })
        this.cargarSolicitudes() // recargar lista
      } catch (error) {
        console.error('Error al aceptar solicitud:', error)
      }
    },
  },
  mounted() {
    this.cargarSolicitudes()
  },
}
</script>

<style scoped>
.container {
  max-width: 800px;
}
</style>
