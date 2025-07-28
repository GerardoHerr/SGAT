<template>
  <div class="asignar-tarea">
    <div class="container">
      <div class="card">
        <h2>Asignar Nueva Tarea</h2>
        
        <form @submit.prevent="crearTarea" class="form">
          <div class="form-group">
            <label for="titulo">Título de la Tarea</label>
            <input
              id="titulo"
              v-model="tarea.titulo"
              type="text"
              class="form-input"
              required
            />
          </div>

          <div class="form-group">
            <label for="descripcion">Descripción</label>
            <textarea
              id="descripcion"
              v-model="tarea.descripcion"
              class="form-textarea"
              rows="4"
              required
            ></textarea>
          </div>

          <div class="form-row">
            <div class="form-group">
              <label for="tipo_tarea">Tipo de Tarea</label>
              <select
                id="tipo_tarea"
                v-model="tarea.tipo_tarea"
                class="form-select"
                required
              >
                <option value="">Seleccionar tipo</option>
                <option value="ACD">ACD - Actividades de Construcción del Conocimiento</option>
                <option value="AA">AA - Actividades de Aplicación</option>
                <option value="APE">APE - Actividades Prácticas de Experimentación</option>
              </select>
            </div>

            <div class="form-group">
              <label for="fecha_entrega">Fecha de Entrega</label>
              <input
                id="fecha_entrega"
                v-model="tarea.fecha_entrega"
                type="datetime-local"
                class="form-input"
                required
              />
            </div>
          </div>

          <div class="form-group">
            <label for="curso">Curso</label>
            <select
              id="curso"
              v-model="tarea.curso"
              class="form-select"
              required
              @change="cargarEstudiantesYGrupos"
              :disabled="!!cursoSoloQuery"
            >
              <option value="">Seleccionar curso</option>
              <option
                v-for="curso in cursos"
                :key="curso.id"
                :value="curso.id"
                :disabled="cursoSoloQuery && String(curso.id) !== String(cursoSoloQuery)"
              >
                {{ curso.asignatura_nombre }} - {{ curso.periodo }}
              </option>
            </select>
          </div>
          <div class="form-group">
            <label for="archivo_explicacion">Archivo PDF de explicación (opcional)</label>
            <input
              id="archivo_explicacion"
              type="file"
              accept="application/pdf"
              @change="onArchivoExplicacionChange"
              class="form-input"
            />
          </div>

          <div class="form-group">
            <label>
              <input
                type="checkbox"
                v-model="tarea.es_grupal"
                @change="limpiarAsignaciones"
              />
              Tarea Grupal
            </label>
          </div>

          <!-- El select de estudiantes está oculto, la selección es automática -->
          <input v-if="false" id="estudiantes-select" />

          <div v-if="tarea.es_grupal && grupos.length > 0" class="form-group">
            <label>Asignar a Grupos</label>
            <div class="checkbox-group">
              <label
                v-for="grupo in grupos"
                :key="grupo.id"
                class="checkbox-item"
              >
                <input
                  type="checkbox"
                  :value="grupo.id"
                  v-model="gruposSeleccionados"
                />
                {{ grupo.nombre }} ({{ grupo.cantidad_estudiantes }} estudiantes)
              </label>
            </div>
          </div>

          <div class="form-actions">
            <button type="submit" class="btn-primary" :disabled="loading">
              {{ loading ? 'Creando...' : 'Crear Tarea' }}
            </button>
            <router-link to="/docente/entregas" class="btn-secondary">
              Cancelar
            </router-link>
          </div>
        </form>

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
  name: 'AsignarTarea',
  data() {
    return {
      tarea: {
        titulo: '',
        descripcion: '',
        tipo_tarea: '',
        fecha_entrega: '',
        curso: '',
        es_grupal: false,
        docente: null
      },
      archivoExplicacion: null,
      cursos: [],
      estudiantes: [],
      grupos: [],
      estudiantesSeleccionados: [],
      gruposSeleccionados: [],
      loading: false,
      mensaje: '',
      esError: false,
      docenteEmail: '',
      cursoSoloQuery: null
    }
  },
  
  async mounted() {
    this.obtenerUsuarioActual()
    await this.cargarCursos()
    // Permitir recibir el id del curso por params o query
    let cursoId = this.$route.params.cursoId || this.$route.query.curso
    if (cursoId && this.cursos.length > 0) {
      // Verifica que el curso exista en la lista
      const existe = this.cursos.some(c => String(c.id) === String(cursoId))
      if (existe) {
        this.tarea.curso = String(cursoId)
        this.cursoSoloQuery = String(cursoId)
        await this.cargarEstudiantesYGrupos()
      } else {
        this.mostrarMensaje('El curso especificado no existe o no tienes acceso', true)
      }
    }
  },

  watch: {
    '$route.params.cursoId': {
      immediate: false,
      handler(newVal) {
        if (newVal && this.cursos.length > 0) {
          const existe = this.cursos.some(c => String(c.id) === String(newVal))
          if (existe) {
            this.tarea.curso = String(newVal)
            this.cursoSoloQuery = String(newVal)
            this.cargarEstudiantesYGrupos()
          } else {
            this.mostrarMensaje('El curso especificado no existe o no tienes acceso', true)
          }
        }
      }
    },
    cursos: {
      immediate: false,
      handler(newCursos) {
        // Si los cursos se cargan después de tener el param, fijar el curso
        let cursoId = this.$route.params.cursoId || this.$route.query.curso
        if (cursoId && newCursos.length > 0) {
          const existe = newCursos.some(c => String(c.id) === String(cursoId))
          if (existe) {
            this.tarea.curso = String(cursoId)
            this.cursoSoloQuery = String(cursoId)
            this.cargarEstudiantesYGrupos()
          }
        }
      }
    }
  },
  
  methods: {
    // MÉTODO MOVIDO AQUÍ DESDE data()
    onArchivoExplicacionChange(e) {
      const file = e.target.files[0]
      if (file && file.type === 'application/pdf') {
        this.archivoExplicacion = file
        console.log('[DEBUG] Archivo PDF seleccionado:', file.name, 'Tamaño:', file.size)
      } else {
        this.archivoExplicacion = null
        if (file) {
          this.mostrarMensaje('Por favor seleccione un archivo PDF válido', true)
        }
      }
    },

    obtenerUsuarioActual() {
      const currentUser = JSON.parse(localStorage.getItem('currentUser'))
      if (currentUser && currentUser.rol === 'DOC') {
        this.tarea.docente = currentUser.email
        this.docenteEmail = currentUser.email
      } else {
        this.$router.push('/login')
      }
    },
    
    async cargarCursos() {
      try {
        const response = await axios.get(`http://localhost:8000/api/cursos/?docente_email=${this.docenteEmail}`)
        this.cursos = response.data
      } catch (error) {
        console.error('Error al cargar cursos del docente:', error)
        this.mostrarMensaje('Error al cargar sus cursos', true)
      }
    },

    async cargarEstudiantesYGrupos() {
      if (!this.tarea.curso) return
      try {
        const estudiantesResponse = await axios.get(`http://localhost:8000/api/cursos/${this.tarea.curso}/estudiantes/`)
        this.estudiantes = estudiantesResponse.data
        this.estudiantesSeleccionados = this.estudiantes.map(e => e.id)
        
        const gruposResponse = await axios.get(`http://localhost:8000/api/grupos/?curso_id=${this.tarea.curso}`)
        this.grupos = gruposResponse.data
      } catch (error) {
        console.error('Error al cargar estudiantes y grupos:', error)
        this.mostrarMensaje('Error al cargar estudiantes y grupos', true)
      }
    },

    limpiarAsignaciones() {
      this.estudiantesSeleccionados = []
      this.gruposSeleccionados = []
    },

    async crearTarea() {
      console.log('[DEBUG] Creando tarea...')
      console.log('[DEBUG] Archivo seleccionado:', this.archivoExplicacion)
      
      if (!this.tarea.curso) {
        this.mostrarMensaje('Debe seleccionar un curso', true)
        return
      }

      if (this.tarea.es_grupal) {
        if (this.gruposSeleccionados.length === 0) {
          this.mostrarMensaje('Debe seleccionar al menos un grupo para tareas grupales', true)
          return
        }
      } else {
        if (this.estudiantes.length > 0 && this.estudiantesSeleccionados.length === 0) {
          this.estudiantesSeleccionados = this.estudiantes.map(e => e.id)
        }
        if (this.estudiantesSeleccionados.length === 0) {
          this.mostrarMensaje('Debe seleccionar al menos un estudiante para tareas individuales', true)
          return
        }
      }

      this.loading = true
      try {
        const formData = new FormData()
        formData.append('titulo', this.tarea.titulo)
        formData.append('descripcion', this.tarea.descripcion)
        formData.append('tipo_tarea', this.tarea.tipo_tarea)
        formData.append('fecha_entrega', this.tarea.fecha_entrega)
        formData.append('curso', this.tarea.curso)
        formData.append('es_grupal', this.tarea.es_grupal)
        formData.append('docente', this.tarea.docente)
        formData.append('activa', true)
        
        // VERIFICAR QUE EL ARCHIVO SE AGREGUE AL FORMDATA
        if (this.archivoExplicacion) {
          formData.append('archivo_explicacion', this.archivoExplicacion)
          console.log('[DEBUG] Archivo agregado al FormData:', this.archivoExplicacion.name)
        } else {
          console.log('[DEBUG] No hay archivo para agregar')
        }

        // Debug: Ver contenido del FormData
        for (let pair of formData.entries()) {
          console.log('[DEBUG] FormData:', pair[0], pair[1])
        }

        const response = await axios.post('http://localhost:8000/api/asignaciones/', formData, {
          headers: { 
            'Content-Type': 'multipart/form-data'
          }
        })
        
        const tareaCreada = response.data
        console.log('[DEBUG] Tarea creada:', tareaCreada)

        let estudiantesIds = []
        let gruposIds = []
        if (this.tarea.es_grupal) {
          gruposIds = this.gruposSeleccionados
        } else {
          estudiantesIds = this.estudiantesSeleccionados
        }

        await axios.post(
          `http://localhost:8000/api/asignaciones/${tareaCreada.id}/asignar_estudiantes_grupos/`,
          {
            tarea_id: tareaCreada.id,
            estudiantes_ids: estudiantesIds,
            grupos_ids: gruposIds
          }
        )
        
        this.mostrarMensaje('Tarea creada y entregas generadas correctamente', false)
        this.limpiarFormulario()
      } catch (error) {
        console.error('Error al crear tarea:', error)
        let msg = 'Error al crear la tarea'
        if (error.response && error.response.data && typeof error.response.data === 'object') {
          msg += ': ' + JSON.stringify(error.response.data)
        }
        this.mostrarMensaje(msg, true)
      } finally {
        this.loading = false
      }
    },

    limpiarFormulario() {
      this.tarea = {
        titulo: '',
        descripcion: '',
        tipo_tarea: '',
        fecha_entrega: '',
        curso: '',
        es_grupal: false,
        docente: this.tarea.docente
      }
      this.archivoExplicacion = null
      const input = document.getElementById('archivo_explicacion')
      if (input) input.value = ''
      this.estudiantesSeleccionados = []
      this.gruposSeleccionados = []
      this.estudiantes = []
      this.grupos = []
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



<style scoped lang="scss">
@import '@/assets/styles/variables';
@import '@/assets/styles/base';

.asignar-tarea {
  min-height: 100vh;
  background: #323232;
  padding: 20px 0;
  display: flex;
  align-items: center;
}

.container {
  max-width: 800px;
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

.form {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
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

.form-input,
.form-select,
.form-textarea {
  padding: 12px 16px;
  border: 2px solid rgba(50, 50, 50, 0.2);
  border-radius: 8px;
  font-size: 16px;
  transition: border-color 0.3s ease;
  background: white;
}

.form-input:focus,
.form-select:focus,
.form-textarea:focus {
  outline: none;
  border-color: #3498db;
  box-shadow: 0 0 0 3px rgba(52, 152, 219, 0.1);
}

.form-textarea {
  resize: vertical;
  min-height: 100px;
}

.checkbox-group {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 10px;
  max-height: 200px;
  overflow-y: auto;
  padding: 10px;
  border: 1px solid rgba(50, 50, 50, 0.2);
  border-radius: 8px;
  background: white;
}

.checkbox-item {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px;
  border-radius: 4px;
  transition: background-color 0.2s ease;
}

.checkbox-item:hover {
  background-color: rgba(52, 152, 219, 0.1);
}

.form-actions {
  display: flex;
  gap: 15px;
  justify-content: center;
  margin-top: 30px;
}

.btn-primary,
.btn-secondary {
  padding: 12px 30px;
  border: none;
  border-radius: 8px;
  font-size: 16px;
  font-weight: 600;
  text-decoration: none;
  display: inline-block;
  text-align: center;
  cursor: pointer;
  transition: all 0.3s ease;
}

.btn-primary {
  background: #3498db;
  color: white;
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

.btn-secondary {
  background: #6c757d;
  color: white;
}

.btn-secondary:hover {
  background: #5a6268;
  transform: translateY(-2px);
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
  
  .checkbox-group {
    grid-template-columns: 1fr;
  }
  
  .form-actions {
    flex-direction: column;
  }
}
</style>
