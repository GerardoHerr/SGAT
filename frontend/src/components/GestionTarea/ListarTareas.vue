<template>
  <div class="listar-tareas">
    <div class="container">
      <div class="card">
        <div class="header">
          <h2>Mis Tareas Asignadas</h2>
          <router-link to="/docente/asignar-tareas" class="btn-primary">
            Nueva Tarea
          </router-link>
        </div>

        <!-- Filtros -->
        <div class="filtros">
          <div class="form-group">
            <label for="filtro-asignatura">Filtrar por Asignatura</label>
            <select
              id="filtro-asignatura"
              v-model="filtros.asignatura"
              class="form-select"
              @change="aplicarFiltros"
            >
              <option value="">Todas las asignaturas</option>
              <option
                v-for="asignatura in asignaturas"
                :key="asignatura.id"
                :value="asignatura.id"
              >
                {{ asignatura.nombre }}
              </option>
            </select>
          </div>

          <div class="form-group">
            <label for="filtro-tipo">Filtrar por Tipo</label>
            <select
              id="filtro-tipo"
              v-model="filtros.tipo_tarea"
              class="form-select"
              @change="aplicarFiltros"
            >
              <option value="">Todos los tipos</option>
              <option value="ACD">ACD</option>
              <option value="AA">AA</option>
              <option value="APE">APE</option>
            </select>
          </div>
        </div>

        <!-- Lista de Tareas -->
        <div v-if="loading" class="loading">
          Cargando tareas...
        </div>

        <div v-else-if="tareas.length === 0" class="sin-tareas">
          <p>No hay tareas asignadas</p>
          <router-link to="/docente/asignar-tareas" class="btn-primary">
            Crear Primera Tarea
          </router-link>
        </div>

        <div v-else class="tareas-grid">
          <div
            v-for="tarea in tareas"
            :key="tarea.id"
            class="tarea-card"
            :class="{ 'vencida': esTareaVencida(tarea.fecha_entrega) }"
          >
            <div class="tarea-header">
              <h3>{{ tarea.titulo }}</h3>
              <div class="badges">
                <span class="badge tipo" :class="tarea.tipo_tarea.toLowerCase()">
                  {{ tarea.tipo_tarea }}
                </span>
                <span class="badge modalidad">
                  {{ tarea.es_grupal ? 'Grupal' : 'Individual' }}
                </span>
              </div>
            </div>

            <div class="tarea-info">
              <p class="asignatura">
                <strong>Asignatura:</strong> {{ tarea.asignatura_nombre }}
              </p>
              <p class="descripcion">{{ tarea.descripcion }}</p>
              <p class="fecha-entrega">
                <strong>Fecha de entrega:</strong>
                <span :class="{ 'vencida': esTareaVencida(tarea.fecha_entrega) }">
                  {{ formatearFecha(tarea.fecha_entrega) }}
                </span>
              </p>
            </div>

            <div class="asignaciones">
              <div v-if="!tarea.es_grupal && tarea.estudiantes_asignados.length > 0">
                <strong>Estudiantes asignados ({{ tarea.estudiantes_asignados.length }}):</strong>
                <div class="estudiantes-lista">
                  <span
                    v-for="estudiante in tarea.estudiantes_asignados.slice(0, 3)"
                    :key="estudiante.id"
                    class="estudiante-tag"
                  >
                    {{ estudiante.nombre }} {{ estudiante.apellido }}
                  </span>
                  <span
                    v-if="tarea.estudiantes_asignados.length > 3"
                    class="mas-estudiantes"
                  >
                    +{{ tarea.estudiantes_asignados.length - 3 }} más
                  </span>
                </div>
              </div>

              <div v-if="tarea.es_grupal && tarea.grupos_asignados.length > 0">
                <strong>Grupos asignados ({{ tarea.grupos_asignados.length }}):</strong>
                <div class="grupos-lista">
                  <span
                    v-for="grupo in tarea.grupos_asignados"
                    :key="grupo.id"
                    class="grupo-tag"
                  >
                    {{ grupo.nombre }}
                  </span>
                </div>
              </div>
            </div>

            <div class="tarea-actions">
              <button
                @click="verDetalles(tarea)"
                class="btn-ver"
              >
                Ver Detalles
              </button>
              <button
                @click="editarTarea(tarea.id)"
                class="btn-editar"
              >
                Editar
              </button>
              <button
                @click="eliminarTarea(tarea.id)"
                class="btn-eliminar"
              >
                Eliminar
              </button>
            </div>
          </div>
        </div>

        <div v-if="mensaje" class="mensaje" :class="{ 'error': esError }">
          {{ mensaje }}
        </div>
      </div>
    </div>

    <!-- Modal de Detalles -->
    <div v-if="tareaSeleccionada" class="modal-overlay" @click="cerrarModal">
      <div class="modal" @click.stop>
        <div class="modal-header">
          <h3>{{ tareaSeleccionada.titulo }}</h3>
          <button @click="cerrarModal" class="btn-cerrar">×</button>
        </div>
        <div class="modal-content">
          <div class="detalle-grupo">
            <strong>Tipo:</strong> {{ tareaSeleccionada.tipo_tarea }}
          </div>
          <div class="detalle-grupo">
            <strong>Modalidad:</strong> {{ tareaSeleccionada.es_grupal ? 'Grupal' : 'Individual' }}
          </div>
          <div class="detalle-grupo">
            <strong>Asignatura:</strong> {{ tareaSeleccionada.asignatura_nombre }}
          </div>
          <div class="detalle-grupo">
            <strong>Fecha de entrega:</strong> {{ formatearFecha(tareaSeleccionada.fecha_entrega) }}
          </div>
          <div class="detalle-grupo">
            <strong>Descripción:</strong>
            <p>{{ tareaSeleccionada.descripcion }}</p>
          </div>
          
          <div v-if="!tareaSeleccionada.es_grupal" class="detalle-grupo">
            <strong>Estudiantes asignados:</strong>
            <ul>
              <li
                v-for="estudiante in tareaSeleccionada.estudiantes_asignados"
                :key="estudiante.id"
              >
                {{ estudiante.nombre }} {{ estudiante.apellido }}
              </li>
            </ul>
          </div>

          <div v-if="tareaSeleccionada.es_grupal" class="detalle-grupo">
            <strong>Grupos asignados:</strong>
            <ul>
              <li
                v-for="grupo in tareaSeleccionada.grupos_asignados"
                :key="grupo.id"
              >
                {{ grupo.nombre }}
              </li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'ListarTareas',
  data() {
    return {
      tareas: [],
      asignaturas: [],
      filtros: {
        asignatura: '',
        tipo_tarea: ''
      },
      tareaSeleccionada: null,
      loading: false,
      mensaje: '',
      esError: false,
      docenteId: null,
      docenteEmail: '' // Email del docente autenticado
    }
  },
  async mounted() {
    this.obtenerUsuarioActual()
    await this.cargarAsignaturas()
    await this.cargarTareas()
  },
  methods: {
    obtenerUsuarioActual() {
      // Obtener usuario del authService
      const currentUser = JSON.parse(localStorage.getItem('currentUser'))
      if (currentUser && currentUser.rol === 'DOC') {
        this.docenteId = currentUser.id
        this.docenteEmail = currentUser.email
      } else {
        // Redirigir al login si no es docente
        this.$router.push('/login')
      }
    },

    async cargarAsignaturas() {
      try {
        // Filtrar solo las asignaturas del docente autenticado
        const response = await fetch(`http://localhost:8000/api/asignaturas/mis_asignaturas/?email=${this.docenteEmail}`)
        if (response.ok) {
          this.asignaturas = await response.json()
        } else {
          console.error('Error al cargar asignaturas del docente')
        }
      } catch (error) {
        console.error('Error al cargar asignaturas:', error)
      }
    },

    async cargarTareas() {
      try {
        // Filtrar solo las tareas del docente autenticado
        const response = await fetch(`http://localhost:8000/api/asignaciones/?docente_email=${this.docenteEmail}`)
        if (response.ok) {
          this.tareas = await response.json()
        } else {
          console.error('Error al cargar tareas del docente')
        }
      } catch (error) {
        console.error('Error al cargar tareas:', error)
      }
    },

    async aplicarFiltros() {
      await this.cargarTareas()
    },

    async aplicarFiltros() {
      await this.cargarTareas()
    },

    formatearFecha(fecha) {
      return new Date(fecha).toLocaleString('es-ES', {
        year: 'numeric',
        month: 'long',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
      })
    },

    esTareaVencida(fechaEntrega) {
      return new Date(fechaEntrega) < new Date()
    },

    verDetalles(tarea) {
      this.tareaSeleccionada = tarea
    },

    cerrarModal() {
      this.tareaSeleccionada = null
    },

    editarTarea(tareaId) {
      this.$router.push(`/editar-tarea/${tareaId}`)
    },

    async eliminarTarea(tareaId) {
      if (!confirm('¿Está seguro de que desea eliminar esta tarea?')) {
        return
      }
      
      try {
        await axios.delete(`http://localhost:8000/api/asignaciones/${tareaId}/`)
        this.mostrarMensaje('Tarea eliminada correctamente', false)
        await this.cargarTareas()
      } catch (error) {
        console.error('Error al eliminar tarea:', error)
        this.mostrarMensaje('Error al eliminar la tarea', true)
      }
    },

    mostrarMensaje(texto, esError = false) {
      this.mensaje = texto
      this.esError = esError
      setTimeout(() => {
        this.mensaje = ''
      }, 5000)
    }
  }
}
</script>

<style scoped>
.listar-tareas {
  min-height: 100vh;
  background: #323232;
  padding: 20px 0;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
}

.card {
  background: #DDD0C8;
  border-radius: 15px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.1);
  padding: 40px;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 30px;
}

h2 {
  color: #323232;
  font-size: 28px;
  font-weight: 600;
  margin: 0;
}

.filtros {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
  margin-bottom: 30px;
  padding: 20px;
  background: rgba(50, 50, 50, 0.05);
  border-radius: 10px;
}

.form-group {
  display: flex;
  flex-direction: column;
}

.form-group label {
  color: #323232;
  font-weight: 500;
  margin-bottom: 8px;
}

.form-select {
  padding: 10px 12px;
  border: 1px solid rgba(50, 50, 50, 0.2);
  border-radius: 6px;
  font-size: 14px;
  background: white;
}

.loading,
.sin-tareas {
  text-align: center;
  padding: 40px;
  color: #323232;
}

.sin-tareas p {
  font-size: 18px;
  margin-bottom: 20px;
}

.tareas-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
  gap: 25px;
}

.tarea-card {
  background: white;
  border-radius: 12px;
  padding: 25px;
  border: 1px solid rgba(50, 50, 50, 0.1);
  transition: all 0.3s ease;
}

.tarea-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
}

.tarea-card.vencida {
  border-left: 4px solid #e74c3c;
}

.tarea-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 15px;
}

.tarea-header h3 {
  color: #323232;
  font-size: 18px;
  font-weight: 600;
  margin: 0;
  flex: 1;
}

.badges {
  display: flex;
  flex-direction: column;
  gap: 5px;
}

.badge {
  padding: 4px 8px;
  border-radius: 12px;
  font-size: 11px;
  font-weight: 600;
  text-align: center;
  white-space: nowrap;
}

.badge.tipo.acd {
  background: rgba(52, 152, 219, 0.1);
  color: #3498db;
}

.badge.tipo.aa {
  background: rgba(155, 89, 182, 0.1);
  color: #9b59b6;
}

.badge.tipo.ape {
  background: rgba(39, 174, 96, 0.1);
  color: #27ae60;
}

.badge.modalidad {
  background: rgba(52, 152, 219, 0.1);
  color: #3498db;
}

.tarea-info {
  margin-bottom: 20px;
}

.tarea-info p {
  margin: 8px 0;
  color: #323232;
}

.descripcion {
  font-style: italic;
  color: #666;
}

.fecha-entrega .vencida {
  color: #e74c3c;
  font-weight: 600;
}

.asignaciones {
  margin-bottom: 20px;
  padding: 15px;
  background: rgba(50, 50, 50, 0.03);
  border-radius: 8px;
  border: 1px solid rgba(50, 50, 50, 0.1);
}

.estudiantes-lista,
.grupos-lista {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-top: 10px;
}

.estudiante-tag,
.grupo-tag {
  background: #3498db;
  color: white;
  padding: 4px 8px;
  border-radius: 12px;
  font-size: 12px;
  font-weight: 500;
}

.mas-estudiantes {
  background: #6c757d;
  color: white;
  padding: 4px 8px;
  border-radius: 12px;
  font-size: 12px;
}

.tarea-actions {
  display: flex;
  gap: 10px;
  justify-content: flex-end;
}

.btn-primary,
.btn-ver,
.btn-editar,
.btn-eliminar {
  padding: 8px 16px;
  border: none;
  border-radius: 6px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  text-decoration: none;
  display: inline-block;
  text-align: center;
  transition: all 0.2s ease;
}

.btn-primary {
  background: #3498db;
  color: white;
}

.btn-ver {
  background: #17a2b8;
  color: white;
}

.btn-editar {
  background: #27ae60;
  color: white;
}

.btn-eliminar {
  background: #e74c3c;
  color: white;
}

.btn-primary:hover,
.btn-ver:hover,
.btn-editar:hover,
.btn-eliminar:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
}

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
  z-index: 1000;
}

.modal {
  background: #DDD0C8;
  border-radius: 12px;
  max-width: 600px;
  width: 90%;
  max-height: 80vh;
  overflow-y: auto;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px;
  border-bottom: 1px solid rgba(50, 50, 50, 0.1);
}

.modal-header h3 {
  margin: 0;
  color: #323232;
}

.btn-cerrar {
  background: none;
  border: none;
  font-size: 24px;
  cursor: pointer;
  color: #666;
}

.modal-content {
  padding: 20px;
}

.detalle-grupo {
  margin-bottom: 15px;
}

.detalle-grupo strong {
  color: #323232;
}

.detalle-grupo p,
.detalle-grupo ul {
  margin: 5px 0 0 0;
  color: #555;
}

.mensaje {
  margin-top: 20px;
  padding: 15px;
  border-radius: 8px;
  text-align: center;
  font-weight: 500;
}

.mensaje:not(.error) {
  background-color: #27ae60;
  color: white;
}

.mensaje.error {
  background-color: #e74c3c;
  color: white;
}

@media (max-width: 768px) {
  .header {
    flex-direction: column;
    gap: 20px;
    text-align: center;
  }
  
  .filtros {
    grid-template-columns: 1fr;
  }
  
  .tareas-grid {
    grid-template-columns: 1fr;
  }
  
  .tarea-actions {
    flex-wrap: wrap;
    justify-content: center;
  }
}
</style>
