<template>
  <div class="asignar-tarea">
    <div class="asignar-tarea-container">
      <div class="asignar-tarea-card">
        <h2 class="asignar-tarea-title"><i class="fas fa-tasks"></i> Asignar Nueva Tarea</h2>
        <form @submit.prevent="crearTarea" class="asignar-tarea-form">
          <div class="asignar-tarea-row">
            <div class="asignar-tarea-group">
              <label for="titulo">Título de la Tarea</label>
              <input id="titulo" v-model="tarea.titulo" type="text" required />
            </div>
            <div class="asignar-tarea-group">
              <label for="tipo_tarea">Tipo de Tarea</label>
              <select id="tipo_tarea" v-model="tarea.tipo_tarea" required>
                <option value="">Seleccionar tipo</option>
                <option value="ACD">ACD - Construcción del Conocimiento</option>
                <option value="AA">AA - Aplicación</option>
                <option value="APE">APE - Prácticas de Experimentación</option>
              </select>
            </div>
          </div>
          <div class="asignar-tarea-row">
            <div class="asignar-tarea-group" style="flex:2">
              <label for="descripcion">Descripción</label>
              <textarea id="descripcion" v-model="tarea.descripcion" rows="4" required></textarea>
            </div>
            <div class="asignar-tarea-group">
              <label for="fecha_entrega">Fecha de Entrega</label>
              <input id="fecha_entrega" v-model="tarea.fecha_entrega" type="datetime-local" required />
            </div>
          </div>
          <div class="asignar-tarea-row">
            <div class="asignar-tarea-group">
              <label for="curso">Curso</label>
              <select id="curso" v-model="tarea.curso" required @change="cargarEstudiantesYGrupos" :disabled="!!cursoSoloQuery">
                <option value="">Seleccionar curso</option>
                <option v-for="curso in cursos" :key="curso.id" :value="curso.id" :disabled="cursoSoloQuery && String(curso.id) !== String(cursoSoloQuery)">
                  {{ curso.asignatura_nombre }} - {{ curso.periodo }}
                </option>
              </select>
            </div>
            <div class="asignar-tarea-group">
              <label for="archivo_explicacion">Archivo PDF de explicación (opcional)</label>
              <input id="archivo_explicacion" type="file" accept="application/pdf" @change="onArchivoExplicacionChange" />
            </div>
          </div>
          <div class="asignar-tarea-row">
            <div class="asignar-tarea-group">
              <label class="asignar-tarea-checkbox">
                <input type="checkbox" v-model="tarea.es_grupal" @change="limpiarAsignaciones" /> Tarea Grupal
              </label>
            </div>
          </div>
          <div v-if="tarea.es_grupal && grupos.length > 0" class="asignar-tarea-group">
            <label>Asignar a Grupos</label>
            <div class="asignar-tarea-checkbox-group">
              <label v-for="grupo in grupos" :key="grupo.id" class="asignar-tarea-checkbox-item">
                <input type="checkbox" :value="grupo.id" v-model="gruposSeleccionados" />
                {{ grupo.nombre }} ({{ grupo.cantidad_estudiantes }} estudiantes)
              </label>
            </div>
          </div>
          <div class="asignar-tarea-actions">
            <button type="submit" :disabled="loading" class="asignar-tarea-btn-primary">
              <i class="fas fa-plus-circle"></i> {{ loading ? 'Creando...' : 'Crear Tarea' }}
            </button>
            <router-link to="/docente/entregas" class="asignar-tarea-btn-secondary">
              <i class="fas fa-times"></i> Cancelar
            </router-link>
          </div>
        </form>
        <div v-if="mensaje" class="asignar-tarea-mensaje" :class="{ 'error': esError }">
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
  background: #23272f;
  display: flex;
  align-items: flex-start;
  justify-content: center;
  padding: 40px 0;
}
.asignar-tarea-container {
  width: 100%;
  max-width: 900px;
  margin: 0 auto;
  padding: 0 16px;
}
.asignar-tarea-card {
  background: #fff;
  border-radius: 18px;
  box-shadow: 0 8px 32px rgba(52,152,219,0.10);
  padding: 38px 32px 28px 32px;
  margin-bottom: 32px;
}
.asignar-tarea-title {
  text-align: center;
  color: $color-primary-dark;
  font-size: 2em;
  font-weight: 700;
  margin-bottom: 32px;
  letter-spacing: 0.5px;
  display: flex;
  align-items: center;
  gap: 12px;
  justify-content: center;
}
.asignar-tarea-form {
  display: flex;
  flex-direction: column;
  gap: 24px;
}
.asignar-tarea-row {
  display: flex;
  gap: 24px;
  margin-bottom: 0;
  flex-wrap: wrap;
}
.asignar-tarea-group {
  flex: 1 1 220px;
  display: flex;
  flex-direction: column;
  gap: 8px;
  margin-bottom: 0;
}
.asignar-tarea-group label {
  color: $text-primary;
  font-weight: 500;
  margin-bottom: 4px;
}
.asignar-tarea-group input,
.asignar-tarea-group select,
.asignar-tarea-group textarea {
  padding: 12px 16px;
  border: 2px solid $border-color;
  border-radius: 8px;
  font-size: 1em;
  background: #f9f9f9;
  transition: border-color 0.2s;
}
.asignar-tarea-group input:focus,
.asignar-tarea-group select:focus,
.asignar-tarea-group textarea:focus {
  outline: none;
  border-color: $color-primary;
  box-shadow: 0 0 0 2px rgba(52,152,219,0.08);
}
.asignar-tarea-group textarea {
  resize: vertical;
  min-height: 90px;
}
.asignar-tarea-checkbox {
  display: flex;
  align-items: center;
  gap: 8px;
  font-weight: 500;
  color: $text-primary;
}
.asignar-tarea-checkbox input[type="checkbox"] {
  accent-color: $color-primary;
  width: 18px;
  height: 18px;
}
.asignar-tarea-checkbox-group {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 10px;
  max-height: 180px;
  overflow-y: auto;
  padding: 10px;
  border: 1px solid $border-color;
  border-radius: 8px;
  background: #f9f9f9;
}
.asignar-tarea-checkbox-item {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 7px 8px;
  border-radius: 4px;
  transition: background 0.2s;
}
.asignar-tarea-checkbox-item:hover {
  background: $color-primary-bg;
}
.asignar-tarea-actions {
  display: flex;
  gap: 18px;
  justify-content: center;
  margin-top: 18px;
}
.asignar-tarea-btn-primary,
.asignar-tarea-btn-secondary {
  padding: 12px 32px;
  border: none;
  border-radius: 8px;
  font-size: 1em;
  font-weight: 600;
  text-decoration: none;
  display: inline-flex;
  align-items: center;
  gap: 8px;
  text-align: center;
  cursor: pointer;
  transition: all 0.2s;
}
.asignar-tarea-btn-primary {
  background: linear-gradient(90deg, #43e97b 0%, #38f9d7 100%);
  color: #fff;
  box-shadow: 0 2px 8px rgba(67, 233, 123, 0.10);
}
.asignar-tarea-btn-primary:disabled {
  background: #b2dfdb;
  color: #eee;
  cursor: not-allowed;
  box-shadow: none;
}
.asignar-tarea-btn-primary:hover:not(:disabled),
.asignar-tarea-btn-primary:focus:not(:disabled) {
  background: linear-gradient(90deg, #38f9d7 0%, #43e97b 100%);
  box-shadow: 0 4px 16px rgba(67, 233, 123, 0.18);
  transform: translateY(-2px) scale(1.03);
}
.asignar-tarea-btn-secondary {
  background: #6c757d;
  color: #fff;
}
.asignar-tarea-btn-secondary:hover {
  background: #5a6268;
  transform: translateY(-2px);
}
.asignar-tarea-mensaje {
  margin-top: 24px;
  padding: 15px;
  border-radius: 8px;
  text-align: center;
  font-weight: 500;
  font-size: 1.08em;
}
.asignar-tarea-mensaje:not(.error) {
  background-color: #27ae60;
  color: #fff;
}
.asignar-tarea-mensaje.error {
  background-color: #e74c3c;
  color: #fff;
}
@media (max-width: 900px) {
  .asignar-tarea-card {
    padding: 18px 4px;
  }
  .asignar-tarea-row {
    flex-direction: column;
    gap: 12px;
  }
}
</style>
