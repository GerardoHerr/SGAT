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
                class="btn btn-success"
                @click="aceptarSolicitud(solicitud.id)"
                :disabled="loading"
              >
                <i class="fas fa-check"></i> 
                {{ loading ? 'Procesando...' : 'Aceptar' }}
              </button>
              <button
                v-if="solicitud.estado === 'pendiente'"
                class="btn btn-success-outline ml-2"
                @click="rechazarSolicitud(solicitud.id)"
                :disabled="loading"
              >
                <i class="fas fa-times"></i>
                {{ loading ? 'Procesando...' : 'Rechazar' }}
              </button>
            </td>
          </tr>
        </tbody>
      </table>
      <div v-if="solicitudes.length === 0" class="empty-state">
        <p>No hay solicitudes disponibles</p>
      </div>
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
      loading: false,
      error: null
    }
  },
  methods: {
    getEstadoClass(estado) {
      const estados = {
        'pendiente': 'badge-warning',
        'aceptada': 'badge-success',
        'rechazada': 'badge-danger'
      }
      return estados[estado] || 'badge-secondary'
    },
    
    async cargarSolicitudes() {
      try {
        this.loading = true
        this.error = null
        
        const token = localStorage.getItem('access_token')
        if (!token) {
          throw new Error('No se encontró token de autenticación')
        }
        
        const response = await axios.get('http://localhost:8000/api/solicitudAsignatura/', {
          headers: {
            Authorization: `Bearer ${token}`,
            'Content-Type': 'application/json'
          },
        })
        
        this.solicitudes = response.data || []
      } catch (error) {
        console.error('Error al cargar solicitudes:', error)
        this.error = 'Error al cargar las solicitudes'
        
        if (error.response?.status === 401) {
          // Token expirado o inválido
          localStorage.removeItem('access_token')
          this.$router.push('/login')
        }
      } finally {
        this.loading = false
      }
    },
    
    async aceptarSolicitud(id) {
      if (!confirm('¿Está seguro de que desea aceptar esta solicitud?')) {
        return
      }
      
      try {
        this.loading = true
        const token = localStorage.getItem('access_token')
        
        if (!token) {
          throw new Error('No se encontró token de autenticación')
        }
        
        await axios.patch(
          `http://localhost:8000/api/solicitudAsignatura/${id}/`, 
          { estado: 'aceptada' },
          {
            headers: {
              'Authorization': `Bearer ${token}`,
              'Content-Type': 'application/json'
            }
          }
        )
        
        // Actualizar el estado local sin recargar toda la lista
        const solicitudIndex = this.solicitudes.findIndex(s => s.id === id)
        if (solicitudIndex !== -1) {
          this.solicitudes[solicitudIndex].estado = 'aceptada'
        }
        
        this.$toast?.success?.('Solicitud aceptada correctamente') || 
        alert('Solicitud aceptada correctamente')
        
      } catch (error) {
        console.error('Error al aceptar solicitud:', error)
        
        if (error.response) {
          console.error('Detalles del error:', error.response.data)
          const errorMsg = error.response.data?.message || 'Error al aceptar la solicitud'
          this.$toast?.error?.(errorMsg) || alert(errorMsg)
        } else {
          this.$toast?.error?.('Error de conexión') || alert('Error de conexión')
        }
      } finally {
        this.loading = false
      }
    },
    
    async rechazarSolicitud(id) {
      if (!confirm('¿Está seguro de que desea rechazar esta solicitud?')) {
        return
      }
      
      try {
        this.loading = true
        const token = localStorage.getItem('access_token')
        
        if (!token) {
          throw new Error('No se encontró token de autenticación')
        }
        
        await axios.patch(
          `http://localhost:8000/api/solicitudAsignatura/${id}/`, 
          { estado: 'rechazada' },
          {
            headers: {
              'Authorization': `Bearer ${token}`,
              'Content-Type': 'application/json'
            }
          }
        )
        
        // Actualizar el estado local
        const solicitudIndex = this.solicitudes.findIndex(s => s.id === id)
        if (solicitudIndex !== -1) {
          this.solicitudes[solicitudIndex].estado = 'rechazada'
        }
        
        this.$toast?.success?.('Solicitud rechazada correctamente') || 
        alert('Solicitud rechazada correctamente')
        
      } catch (error) {
        console.error('Error al rechazar solicitud:', error)
        
        if (error.response) {
          const errorMsg = error.response.data?.message || 'Error al rechazar la solicitud'
          this.$toast?.error?.(errorMsg) || alert(errorMsg)
        } else {
          this.$toast?.error?.('Error de conexión') || alert('Error de conexión')
        }
      } finally {
        this.loading = false
      }
    }
  },
  
  async mounted() {
    await this.cargarSolicitudes()
  }
}
</script>

<style scoped lang="scss">
@import '@/assets/styles/variables';
@import '@/assets/styles/base';


.container {
  padding: 20px;
  max-width: 100vw;
  box-sizing: border-box;
}

// Contenedor con scroll horizontal siempre visible si es necesario
.table-container {
  width: 100%;
  overflow-x: auto;
  margin-top: 24px;
  background: #fff;
  border-radius: 12px;
  box-shadow: 0 2px 12px rgba(0,0,0,0.06);
  padding: 12px 0;
  max-width: 100vw;
  box-sizing: border-box;
}

table {
  width: 100%;
  min-width: 520px;
  border-collapse: collapse;
  table-layout: auto;
}

th, td {
  padding: 12px 16px;
  text-align: left;
  white-space: nowrap;
}

th {
  background: #f8f9fa;
  font-weight: 700;
  color: #002147;
  border-bottom: 2px solid #e0e0e0;
}

td {
  border-bottom: 1px solid #f0f0f0;
}

th:last-child,
td:last-child {
  text-align: center;
}

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
}

.badge-success {
  color: #155724;
  background-color: #d4edda;
}

.badge-warning {
  color: #856404;
  background-color: #fff3cd;
}

.badge-danger {
  color: #721c24;
  background-color: #f8d7da;
}

.badge-secondary {
  color: #6c757d;
  background-color: #e2e3e5;
}

.btn {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  padding: 8px 16px;
  border: none;
  border-radius: 6px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
  text-decoration: none;
  
  &:disabled {
    opacity: 0.6;
    cursor: not-allowed;
  }
}

.btn-success {
  background-color: #27ae60;
  color: #fff;
  &:hover:not(:disabled) {
    background-color: #219150;
    transform: translateY(-1px);
  }
}

.btn-success-outline {
  background-color: #fff;
  color: #27ae60;
  border: 2px solid #27ae60;
  &:hover:not(:disabled) {
    background-color: #eafbe7;
    color: #219150;
    border-color: #219150;
    transform: translateY(-1px);
  }
}

.ml-2 {
  margin-left: 8px;
}

.empty-state {
  text-align: center;
  padding: 40px 20px;
  color: #6c757d;
  
  p {
    font-size: 16px;
    margin: 0;
  }
}

@media (max-width: 900px) {
  .container {
    padding: 8px;
  }
  .table-container {
    padding: 0;
    border-radius: 0;
    box-shadow: none;
    max-width: 100vw;
  }
  table {
    min-width: 400px;
    font-size: 0.93em;
  }
  th, td {
    padding: 7px 6px;
  }
  th:last-child,
  td:last-child {
    text-align: center;
  }
  .btn {
    padding: 6px 10px;
    font-size: 12px;
  }
  .ml-2 {
    margin-left: 4px;
    margin-top: 4px;
  }
}
</style>