<template>
  <div class="gestion-grupos">
    <div class="container">
      <div class="card">
        <h2>Gestión de Grupos</h2>
        
        <!-- Selector de Asignatura -->
        <div class="form-group">
          <label for="asignatura">Seleccionar Asignatura</label>
          <select
            id="asignatura"
            v-model="asignaturaSeleccionada"
            class="form-select"
            @change="cargarGrupos"
          >
            <option value="">Seleccionar asignatura</option>
            <option
              v-for="asignatura in asignaturas"
              :key="asignatura.id"
              :value="asignatura.id"
            >
              {{ asignatura.nombre }}
            </option>
          </select>
        </div>

        <!-- Sección de Creación de Grupos Aleatorios -->
        <div v-if="asignaturaSeleccionada" class="seccion-crear-grupos">
          <h3>Crear Grupos Aleatorios</h3>
          <div class="form-row">
            <div class="form-group">
              <label for="cantidad_grupos">Cantidad de Grupos</label>
              <input
                id="cantidad_grupos"
                v-model.number="formGrupos.cantidad_grupos"
                type="number"
                min="1"
                max="20"
                class="form-input"
              />
            </div>
            <div class="form-group">
              <label for="nombre_base">Nombre Base</label>
              <input
                id="nombre_base"
                v-model="formGrupos.nombre_base"
                type="text"
                class="form-input"
                placeholder="Grupo"
              />
            </div>
          </div>
          <button
            @click="crearGruposAleatorios"
            class="btn-primary"
            :disabled="loading"
          >
            {{ loading ? 'Creando...' : 'Crear Grupos Aleatorios' }}
          </button>
        </div>

        <!-- Lista de Grupos Existentes -->
        <div v-if="grupos.length > 0" class="seccion-grupos">
          <h3>Grupos Existentes</h3>
          <div class="grupos-grid">
            <div
              v-for="grupo in grupos"
              :key="grupo.id"
              class="grupo-card"
            >
              <div class="grupo-header">
                <h4>{{ grupo.nombre }}</h4>
                <span class="estudiantes-count">
                  {{ grupo.cantidad_estudiantes }} estudiantes
                </span>
              </div>
              
              <div class="grupo-descripcion">
                {{ grupo.descripcion }}
              </div>
              
              <div class="estudiantes-lista">
                <div
                  v-for="estudiante in grupo.estudiantes"
                  :key="estudiante.id"
                  class="estudiante-item"
                >
                  <span>{{ estudiante.nombre }} {{ estudiante.apellido }}</span>
                  <button
                    @click="removerEstudiante(grupo.id, estudiante.id)"
                    class="btn-remove"
                    title="Remover estudiante"
                  >
                    ×
                  </button>
                </div>
              </div>

              <div class="grupo-actions">
                <select
                  v-model="estudianteParaAgregar[grupo.id]"
                  class="form-select-small"
                >
                  <option value="">Agregar estudiante...</option>
                  <option
                    v-for="estudiante in estudiantesDisponibles"
                    :key="estudiante.id"
                    :value="estudiante.id"
                  >
                    {{ estudiante.nombre }} {{ estudiante.apellido }}
                  </option>
                </select>
                <button
                  @click="agregarEstudiante(grupo.id)"
                  class="btn-add"
                  :disabled="!estudianteParaAgregar[grupo.id]"
                >
                  Agregar
                </button>
              </div>
            </div>
          </div>
        </div>

        <div v-if="mensaje" class="mensaje" :class="{ 'error': esError }">
          {{ mensaje }}
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'GestionGrupos',
  data() {
    return {
      asignaturas: [],
      asignaturaSeleccionada: '',
      grupos: [],
      estudiantesDisponibles: [],
      formGrupos: {
        cantidad_grupos: 4,
        nombre_base: 'Grupo'
      },
      estudianteParaAgregar: {},
      loading: false,
      mensaje: '',
      esError: false
    }
  },
  async mounted() {
    await this.cargarAsignaturas()
  },
  methods: {
    async cargarAsignaturas() {
      try {
        const response = await axios.get('http://localhost:8000/api/asignaturas/')
        this.asignaturas = response.data
      } catch (error) {
        console.error('Error al cargar asignaturas:', error)
        this.mostrarMensaje('Error al cargar asignaturas', true)
      }
    },

    async cargarGrupos() {
      if (!this.asignaturaSeleccionada) {
        this.grupos = []
        return
      }
      
      try {
        const response = await axios.get(`http://localhost:8000/api/grupos/?asignatura_id=${this.asignaturaSeleccionada}`)
        this.grupos = response.data
        await this.cargarEstudiantesDisponibles()
      } catch (error) {
        console.error('Error al cargar grupos:', error)
        this.mostrarMensaje('Error al cargar grupos', true)
      }
    },

    async cargarEstudiantesDisponibles() {
      try {
        // Obtener todos los estudiantes de la asignatura
        const response = await axios.get(`http://localhost:8000/api/usuarios/?rol=EST`)
        const todosEstudiantes = response.data
        
        // Filtrar estudiantes que no están en ningún grupo
        const estudiantesEnGrupos = new Set()
        this.grupos.forEach(grupo => {
          grupo.estudiantes.forEach(estudiante => {
            estudiantesEnGrupos.add(estudiante.id)
          })
        })
        
        this.estudiantesDisponibles = todosEstudiantes.filter(
          estudiante => !estudiantesEnGrupos.has(estudiante.id)
        )
      } catch (error) {
        console.error('Error al cargar estudiantes disponibles:', error)
      }
    },

    async crearGruposAleatorios() {
      if (!this.asignaturaSeleccionada || this.formGrupos.cantidad_grupos < 1) {
        this.mostrarMensaje('Seleccione una asignatura y una cantidad válida de grupos', true)
        return
      }
      
      this.loading = true
      
      try {
        const response = await axios.post('http://localhost:8000/api/grupos/crear_grupos_aleatorios/', {
          asignatura_id: this.asignaturaSeleccionada,
          cantidad_grupos: this.formGrupos.cantidad_grupos,
          nombre_base: this.formGrupos.nombre_base
        })
        
        this.mostrarMensaje(response.data.mensaje, false)
        await this.cargarGrupos()
        
      } catch (error) {
        console.error('Error al crear grupos:', error)
        const mensaje = error.response?.data?.error || 'Error al crear grupos aleatorios'
        this.mostrarMensaje(mensaje, true)
      } finally {
        this.loading = false
      }
    },

    async agregarEstudiante(grupoId) {
      const estudianteId = this.estudianteParaAgregar[grupoId]
      if (!estudianteId) return
      
      try {
        await axios.post(`http://localhost:8000/api/grupos/${grupoId}/agregar_estudiante/`, {
          estudiante_id: estudianteId
        })
        
        this.mostrarMensaje('Estudiante agregado al grupo correctamente', false)
        this.estudianteParaAgregar[grupoId] = ''
        await this.cargarGrupos()
        
      } catch (error) {
        console.error('Error al agregar estudiante:', error)
        const mensaje = error.response?.data?.error || 'Error al agregar estudiante'
        this.mostrarMensaje(mensaje, true)
      }
    },

    async removerEstudiante(grupoId, estudianteId) {
      if (!confirm('¿Está seguro de que desea remover este estudiante del grupo?')) {
        return
      }
      
      try {
        await axios.post(`http://localhost:8000/api/grupos/${grupoId}/remover_estudiante/`, {
          estudiante_id: estudianteId
        })
        
        this.mostrarMensaje('Estudiante removido del grupo correctamente', false)
        await this.cargarGrupos()
        
      } catch (error) {
        console.error('Error al remover estudiante:', error)
        const mensaje = error.response?.data?.error || 'Error al remover estudiante'
        this.mostrarMensaje(mensaje, true)
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
.gestion-grupos {
  min-height: 100vh;
  background: #323232;
  padding: 20px 0;
  display: flex;
  align-items: flex-start;
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

h2 {
  text-align: center;
  color: #323232;
  margin-bottom: 30px;
  font-size: 28px;
  font-weight: 600;
}

h3 {
  color: #323232;
  margin: 30px 0 20px 0;
  font-size: 20px;
  font-weight: 600;
  border-bottom: 2px solid #3498db;
  padding-bottom: 10px;
}

.form-group {
  display: flex;
  flex-direction: column;
  margin-bottom: 20px;
}

.form-group label {
  color: #323232;
  font-weight: 500;
  margin-bottom: 8px;
}

.form-input,
.form-select {
  padding: 12px 16px;
  border: 2px solid rgba(50, 50, 50, 0.2);
  border-radius: 8px;
  font-size: 16px;
  transition: border-color 0.3s ease;
  background: white;
}

.form-input:focus,
.form-select:focus {
  outline: none;
  border-color: #3498db;
  box-shadow: 0 0 0 3px rgba(52, 152, 219, 0.1);
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
}

.seccion-crear-grupos {
  background: rgba(50, 50, 50, 0.05);
  border-radius: 10px;
  padding: 25px;
  margin: 20px 0;
}

.btn-primary {
  background: #3498db;
  color: white;
  border: none;
  padding: 12px 24px;
  border-radius: 8px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.btn-primary:hover:not(:disabled) {
  background: #2980b9;
  transform: translateY(-2px);
  box-shadow: 0 10px 25px rgba(52, 152, 219, 0.3);
}

.btn-primary:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.grupos-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
  gap: 20px;
  margin-top: 20px;
}

.grupo-card {
  background: white;
  border-radius: 10px;
  padding: 20px;
  border: 1px solid rgba(50, 50, 50, 0.1);
  transition: box-shadow 0.3s ease;
}

.grupo-card:hover {
  box-shadow: 0 5px 20px rgba(0, 0, 0, 0.1);
}

.grupo-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
}

.grupo-header h4 {
  color: #323232;
  margin: 0;
  font-size: 18px;
}

.estudiantes-count {
  background: #3498db;
  color: white;
  padding: 4px 12px;
  border-radius: 15px;
  font-size: 12px;
  font-weight: 600;
}

.grupo-descripcion {
  color: #666;
  font-size: 14px;
  margin-bottom: 15px;
  font-style: italic;
}

.estudiantes-lista {
  margin-bottom: 15px;
  max-height: 200px;
  overflow-y: auto;
}

.estudiante-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 8px 12px;
  background: rgba(50, 50, 50, 0.03);
  border-radius: 5px;
  margin-bottom: 5px;
  border: 1px solid rgba(50, 50, 50, 0.1);
}

.btn-remove {
  background: #e74c3c;
  color: white;
  border: none;
  width: 24px;
  height: 24px;
  border-radius: 50%;
  cursor: pointer;
  font-size: 16px;
  line-height: 1;
  display: flex;
  align-items: center;
  justify-content: center;
}

.btn-remove:hover {
  background: #c0392b;
}

.grupo-actions {
  display: flex;
  gap: 10px;
  align-items: center;
}

.form-select-small {
  flex: 1;
  padding: 8px 12px;
  border: 1px solid rgba(50, 50, 50, 0.2);
  border-radius: 5px;
  font-size: 14px;
  background: white;
}

.btn-add {
  background: #27ae60;
  color: white;
  border: none;
  padding: 8px 16px;
  border-radius: 5px;
  font-size: 14px;
  cursor: pointer;
  white-space: nowrap;
}

.btn-add:hover:not(:disabled) {
  background: #229954;
}

.btn-add:disabled {
  opacity: 0.6;
  cursor: not-allowed;
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
  .form-row {
    grid-template-columns: 1fr;
  }
  
  .grupos-grid {
    grid-template-columns: 1fr;
  }
  
  .grupo-actions {
    flex-direction: column;
  }
}
</style>
