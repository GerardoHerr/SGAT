<template>
  <div class="asignar-tarea">
    <div class="asignar-tarea-container">
      <div class="asignar-tarea-card">
        <!-- Header Section -->
        <div class="asignar-tarea-header">
          <div class="asignar-tarea-icon">
            <i class="fas fa-tasks"></i>
          </div>
          <h2 class="asignar-tarea-title">Asignar Nueva Tarea</h2>
          <p class="asignar-tarea-subtitle">Complete la información para crear una nueva tarea</p>
        </div>

        <form @submit.prevent="crearTarea" class="asignar-tarea-form">
          <!-- Información Básica -->
          <div class="asignar-tarea-section">
            <h3 class="asignar-tarea-section-title">
              <i class="fas fa-info-circle"></i>
              Información Básica
            </h3>
            <div class="asignar-tarea-section-content">
              <div class="asignar-tarea-row">
                <div class="asignar-tarea-group">
                  <label for="titulo">
                    <i class="fas fa-heading"></i>
                    Título de la Tarea
                  </label>
                  <input 
                    id="titulo" 
                    v-model="tarea.titulo" 
                    type="text" 
                    required 
                    placeholder="Ingrese el título de la tarea"
                  />
                </div>
                <div class="asignar-tarea-group">
                  <label for="tipo_tarea">
                    <i class="fas fa-tag"></i>
                    Tipo de Tarea
                  </label>
                  <select id="tipo_tarea" v-model="tarea.tipo_tarea" required>
                    <option value="">Seleccionar tipo</option>
                    <option value="ACD">ACD - Contacto con el Docente</option>
                    <option value="AA">AA - Aprendizaje Autónomo</option>
                    <option value="APE">APE - Prácticas de Experimentación</option>
                  </select>
                </div>
              </div>
              
              <div class="asignar-tarea-row">
                <div class="asignar-tarea-group asignar-tarea-group-full">
                  <label for="descripcion">
                    <i class="fas fa-align-left"></i>
                    Descripción
                  </label>
                  <textarea 
                    id="descripcion" 
                    v-model="tarea.descripcion" 
                    rows="4" 
                    required
                    placeholder="Describe detalladamente la tarea a realizar..."
                  ></textarea>
                </div>
              </div>
            </div>
          </div>

          <!-- Configuración -->
          <div class="asignar-tarea-section">
            <h3 class="asignar-tarea-section-title">
              <i class="fas fa-cog"></i>
              Configuración
            </h3>
            <div class="asignar-tarea-section-content">
              <div class="asignar-tarea-row">
                <div class="asignar-tarea-group">
                  <label for="curso">
                    <i class="fas fa-book"></i>
                    Curso
                  </label>
                  <select 
                    id="curso" 
                    v-model="tarea.curso" 
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
                <div class="asignar-tarea-group">
                  <label for="fecha_entrega">
                    <i class="fas fa-calendar-alt"></i>
                    Fecha de Entrega
                  </label>
                  <input 
                    id="fecha_entrega" 
                    v-model="tarea.fecha_entrega" 
                    type="datetime-local" 
                    required 
                  />
                </div>
              </div>

              <div class="asignar-tarea-row">
                <div class="asignar-tarea-group">
                  <label for="archivo_explicacion">
                    <i class="fas fa-file-pdf"></i>
                    Archivo PDF de explicación (opcional)
                  </label>
                  <div class="asignar-tarea-file-wrapper">
                    <input 
                      id="archivo_explicacion" 
                      type="file" 
                      accept="application/pdf" 
                      @change="onArchivoExplicacionChange" 
                    />
                    <div class="asignar-tarea-file-info">
                      <i class="fas fa-cloud-upload-alt"></i>
                      <span>Seleccionar archivo PDF</span>
                    </div>
                  </div>
                  <div v-if="archivoExplicacion" class="asignar-tarea-file-nombre">
                    <i class="fas fa-file"></i>
                    <span>{{ archivoExplicacion.name }}</span>
                  </div>
                </div>

                <div class="asignar-tarea-group">
                  <div class="asignar-tarea-checkbox-container">
                    <label class="asignar-tarea-checkbox-toggle">
                      <input 
                        type="checkbox" 
                        v-model="tarea.es_grupal" 
                        @change="limpiarAsignaciones" 
                      />
                      <span class="asignar-tarea-checkbox-slider"></span>
                      <span class="asignar-tarea-checkbox-label">
                        <i class="fas fa-users"></i>
                        Tarea Grupal
                      </span>
                    </label>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Asignación de Grupos -->
          <div v-if="tarea.es_grupal && grupos.length > 0" class="asignar-tarea-section">
            <h3 class="asignar-tarea-section-title">
              <i class="fas fa-users"></i>
              Asignar a Grupos
            </h3>
            <div class="asignar-tarea-section-content">
              <div class="asignar-tarea-checkbox-grid">
                <label 
                  v-for="grupo in grupos" 
                  :key="grupo.id" 
                  class="asignar-tarea-checkbox-card"
                >
                  <input 
                    type="checkbox" 
                    :value="grupo.id" 
                    v-model="gruposSeleccionados" 
                  />
                  <div class="asignar-tarea-checkbox-content">
                    <div class="asignar-tarea-checkbox-header">
                      <i class="fas fa-user-friends"></i>
                      <span class="asignar-tarea-checkbox-name">{{ grupo.nombre }}</span>
                    </div>
                    <div class="asignar-tarea-checkbox-info">
                      {{ grupo.cantidad_estudiantes }} estudiantes
                    </div>
                  </div>
                  <div class="asignar-tarea-checkbox-check">
                    <i class="fas fa-check"></i>
                  </div>
                </label>
              </div>
            </div>
          </div>

          <!-- Acciones -->
          <div class="asignar-tarea-actions">
            <button type="submit" :disabled="loading" class="asignar-tarea-btn-primary">
              <i class="fas fa-plus-circle"></i>
              <span>{{ loading ? 'Creando...' : 'Crear Tarea' }}</span>
              <div v-if="loading" class="asignar-tarea-spinner"></div>
            </button>
            <router-link to="/docente/entregas" class="asignar-tarea-btn-secondary">
              <i class="fas fa-times"></i>
              <span>Cancelar</span>
            </router-link>
          </div>
        </form>

        <!-- Mensaje -->
        <div class="asignar-tarea-mensaje-wrapper">
          <div v-if="mensaje" class="asignar-tarea-mensaje" :class="{ 'error': esError }">
            <i :class="esError ? 'fas fa-exclamation-triangle' : 'fas fa-check-circle'"></i>
            {{ mensaje }}
          </div>
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
    'tarea.fecha_entrega'(nuevaFecha) {
      if (!nuevaFecha) return;
      const fechaEntrega = new Date(nuevaFecha);
      const ahora = new Date();
      if (fechaEntrega < ahora) {
        this.mostrarMensaje('No se puede seleccionar una fecha de entrega anterior al momento actual', true);
        this.tarea.fecha_entrega = '';
      }
    },
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

      // Validar fecha de entrega
      if (!this.tarea.fecha_entrega) {
        this.mostrarMensaje('Debe ingresar una fecha de entrega', true)
        return
      }
      const fechaEntrega = new Date(this.tarea.fecha_entrega)
      const ahora = new Date()
      if (fechaEntrega < ahora) {
        this.mostrarMensaje('La fecha de entrega no puede ser anterior al momento actual', true)
        return
      }

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
        
        // Solo agregar archivo_explicacion si el usuario seleccionó uno
        if (this.archivoExplicacion) {
          formData.append('archivo_explicacion', this.archivoExplicacion)
          console.log('[DEBUG] Archivo agregado al FormData:', this.archivoExplicacion.name)
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
  background: #f5f6fa;
  display: flex;
  align-items: flex-start;
  justify-content: center;
  padding: 20px 0;
  width: 95%;  
}
/* Nombre del archivo PDF seleccionado */
.asignar-tarea-file-nombre {
  margin-top: 8px;
  color: #2c3e50;
  font-size: 0.98em;
  display: flex;
  align-items: center;
  gap: 8px;
  word-break: break-all;
}

.asignar-tarea-container {
  width: 100%;
  max-width: 2400px;
  margin: 0 auto;
  padding: 0 16px;
}

.asignar-tarea-card {
  background: #fff;
  border-radius: 24px;
  box-shadow: 0 20px 60px rgba(52,152,219,0.15);
  overflow: hidden;
  margin-bottom: 32px;
  max-width: 1800px;
  margin-left: auto;
  margin-right: auto;
}

/* Header */
.asignar-tarea-header {
  background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);
  color: white;
  text-align: center;
  padding: 40px 32px;
  position: relative;
  overflow: hidden;
}

.asignar-tarea-header::before {
  content: '';
  position: absolute;
  top: -50%;
  left: -50%;
  width: 200%;
  height: 200%;
  background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><circle cx="50" cy="50" r="2" fill="rgba(255,255,255,0.1)"/></svg>') repeat;
  animation: float 20s linear infinite;
}

@keyframes float {
  0% { transform: translate(-50%, -50%) rotate(0deg); }
  100% { transform: translate(-50%, -50%) rotate(360deg); }
}

.asignar-tarea-icon {
  display: inline-block;
  width: 80px;
  height: 80px;
  background: rgba(255, 255, 255, 0.2);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 20px;
  position: relative;
  z-index: 1;
}

.asignar-tarea-icon i {
  font-size: 36px;
}

.asignar-tarea-title {
  font-size: 2.5em;
  font-weight: 700;
  margin-bottom: 8px;
  position: relative;
  z-index: 1;
}

.asignar-tarea-subtitle {
  font-size: 1.1em;
  opacity: 0.9;
  font-weight: 400;
  margin: 0;
  position: relative;
  z-index: 1;
}

/* Form */
.asignar-tarea-form {
  padding: 40px 32px;
}

/* Sections */
.asignar-tarea-section {
  margin-bottom: 40px;
  background: #f8f9fa;
  border-radius: 16px;
  overflow: hidden;
  border: 1px solid #e9ecef;
}

.asignar-tarea-section-title {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  margin: 0;
  padding: 20px 24px;
  font-size: 1.3em;
  font-weight: 600;
  display: flex;
  align-items: center;
  gap: 12px;
}

.asignar-tarea-section-content {
  padding: 32px 24px;
}

/* Form Elements */
.asignar-tarea-row {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 24px;
  margin-bottom: 24px;
}

.asignar-tarea-row:last-child {
  margin-bottom: 0;
}

.asignar-tarea-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.asignar-tarea-group-full {
  grid-column: 1 / -1;
}

.asignar-tarea-group label {
  color: #2c3e50;
  font-weight: 600;
  font-size: 0.95em;
  display: flex;
  align-items: center;
  gap: 8px;
}

.asignar-tarea-group label i {
  color: #667eea;
  width: 16px;
}

.asignar-tarea-group input,
.asignar-tarea-group select,
.asignar-tarea-group textarea {
  padding: 16px 20px;
  border: 2px solid #e1e5e9;
  border-radius: 12px;
  font-size: 1em;
  background: #fff;
  transition: all 0.3s ease;
  font-family: inherit;
}

.asignar-tarea-group input:focus,
.asignar-tarea-group select:focus,
.asignar-tarea-group textarea:focus {
  outline: none;
  border-color: #43e97b;
  box-shadow: 0 0 0 4px rgba(67, 233, 123, 0.1);
  transform: translateY(-2px);
}

.asignar-tarea-group input::placeholder,
.asignar-tarea-group textarea::placeholder {
  color: #9ca3af;
  font-style: italic;
}

.asignar-tarea-group textarea {
  resize: vertical;
  min-height: 120px;
  line-height: 1.6;
}

/* File Upload */
.asignar-tarea-file-wrapper {
  position: relative;
  overflow: hidden;
  border: 2px dashed #e1e5e9;
  border-radius: 12px;
  background: #fff;
  transition: all 0.3s ease;
  cursor: pointer;
}

.asignar-tarea-file-wrapper:hover {
  border-color: #43e97b;
  background: #f0fdf4;
}

.asignar-tarea-file-wrapper input[type="file"] {
  position: absolute;
  opacity: 0;
  width: 100%;
  height: 100%;
  cursor: pointer;
  border: none;
  padding: 0;
}

.asignar-tarea-file-info {
  padding: 20px;
  text-align: center;
  color: #6b7280;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
}

.asignar-tarea-file-info i {
  font-size: 24px;
  color: #43e97b;
}

/* Toggle Switch */
.asignar-tarea-checkbox-container {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 100%;
}

.asignar-tarea-checkbox-toggle {
  display: flex;
  align-items: center;
  gap: 16px;
  cursor: pointer;
  padding: 20px;
  background: #fff;
  border: 2px solid #e1e5e9;
  border-radius: 12px;
  transition: all 0.3s ease;
}

.asignar-tarea-checkbox-toggle:hover {
  border-color: #43e97b;
  background: #f0fdf4;
}

.asignar-tarea-checkbox-toggle input[type="checkbox"] {
  display: none;
}

.asignar-tarea-checkbox-slider {
  width: 60px;
  height: 30px;
  background: #e5e7eb;
  border-radius: 15px;
  position: relative;
  transition: all 0.3s ease;
}

.asignar-tarea-checkbox-slider::before {
  content: '';
  position: absolute;
  top: 3px;
  left: 3px;
  width: 24px;
  height: 24px;
  background: white;
  border-radius: 50%;
  transition: all 0.3s ease;
  box-shadow: 0 2px 4px rgba(0,0,0,0.2);
}

.asignar-tarea-checkbox-toggle input:checked + .asignar-tarea-checkbox-slider {
  background: #43e97b;
}

.asignar-tarea-checkbox-toggle input:checked + .asignar-tarea-checkbox-slider::before {
  transform: translateX(30px);
}

.asignar-tarea-checkbox-label {
  font-weight: 600;
  color: #2c3e50;
  display: flex;
  align-items: center;
  gap: 8px;
}

/* Checkbox Grid */
.asignar-tarea-checkbox-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 16px;
}

.asignar-tarea-checkbox-card {
  display: flex;
  align-items: center;
  padding: 20px;
  background: white;
  border: 2px solid #e1e5e9;
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
}

.asignar-tarea-checkbox-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(135deg, #43e97b, #38f9d7);
  opacity: 0;
  transition: opacity 0.3s ease;
}

.asignar-tarea-checkbox-card:hover {
  border-color: #43e97b;
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(67, 233, 123, 0.15);
}

.asignar-tarea-checkbox-card input[type="checkbox"] {
  display: none;
}

.asignar-tarea-checkbox-card input:checked + .asignar-tarea-checkbox-content + .asignar-tarea-checkbox-check {
  opacity: 1;
  transform: scale(1);
}

.asignar-tarea-checkbox-card input:checked {
  & ~ * {
    color: white;
    position: relative;
    z-index: 2;
  }
}

.asignar-tarea-checkbox-card input:checked::before {
  opacity: 1;
}

.asignar-tarea-checkbox-content {
  flex: 1;
  position: relative;
  z-index: 2;
}

.asignar-tarea-checkbox-header {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 8px;
}

.asignar-tarea-checkbox-header i {
  color: #43e97b;
  font-size: 18px;
}

.asignar-tarea-checkbox-name {
  font-weight: 600;
  font-size: 1.1em;
  color: #2c3e50;
}

.asignar-tarea-checkbox-info {
  color: #6b7280;
  font-size: 0.9em;
  margin-left: 30px;
}

.asignar-tarea-checkbox-check {
  width: 24px;
  height: 24px;
  border-radius: 50%;
  background: #43e97b;
  display: flex;
  align-items: center;
  justify-content: center;
  opacity: 0;
  transform: scale(0);
  transition: all 0.3s ease;
  position: relative;
  z-index: 2;
}

.asignar-tarea-checkbox-check i {
  color: white;
  font-size: 12px;
}

/* Actions */
.asignar-tarea-actions {
  display: flex;
  gap: 20px;
  justify-content: center;
  margin-top: 40px;
  padding: 0 32px;
}

.asignar-tarea-btn-primary,
.asignar-tarea-btn-secondary {
  padding: 16px 32px;
  border: none;
  border-radius: 12px;
  font-size: 1.1em;
  font-weight: 600;
  text-decoration: none;
  display: inline-flex;
  align-items: center;
  gap: 12px;
  text-align: center;
  cursor: pointer;
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
  min-width: 160px;
  justify-content: center;
}

.asignar-tarea-btn-primary {
  background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);
  color: #fff;
  box-shadow: 0 8px 25px rgba(67, 233, 123, 0.3);
}

.asignar-tarea-btn-primary::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255,255,255,0.3), transparent);
  transition: left 0.5s;
}

.asignar-tarea-btn-primary:hover::before {
  left: 100%;
}

.asignar-tarea-btn-primary:disabled {
  background: linear-gradient(135deg, #b2dfdb 0%, #b2dfdb 100%);
  color: #fff;
  cursor: not-allowed;
  box-shadow: none;
  transform: none;
}

.asignar-tarea-btn-primary:hover:not(:disabled) {
  transform: translateY(-3px) scale(1.02);
  box-shadow: 0 12px 35px rgba(67, 233, 123, 0.4);
}

.asignar-tarea-btn-secondary {
  background: linear-gradient(135deg, #6c757d 0%, #5a6268 100%);
  color: #fff;
  box-shadow: 0 8px 25px rgba(108, 117, 125, 0.3);
}

.asignar-tarea-btn-secondary:hover {
  transform: translateY(-3px) scale(1.02);
  box-shadow: 0 12px 35px rgba(108, 117, 125, 0.4);
}

/* Spinner */
.asignar-tarea-spinner {
  width: 18px;
  height: 18px;
  border: 2px solid rgba(255,255,255,0.3);
  border-top: 2px solid white;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

/* Messages */

.asignar-tarea-mensaje-wrapper {
  min-height: 64px;
  margin: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.asignar-tarea-mensaje {
  width: 100%;
  padding: 20px 24px;
  border-radius: 12px;
  text-align: center;
  font-weight: 500;
  font-size: 1.1em;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 12px;
  animation: slideIn 0.3s ease;
}

@keyframes slideIn {
  from {
    opacity: 0;
    transform: translateY(-20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.asignar-tarea-mensaje:not(.error) {
  background: linear-gradient(135deg, #27ae60 0%, #2ecc71 100%);
  color: #fff;
  box-shadow: 0 8px 25px rgba(39, 174, 96, 0.3);
}

.asignar-tarea-mensaje.error {
  background: linear-gradient(135deg, #e74c3c 0%, #c0392b 100%);
  color: #fff;
  box-shadow: 0 8px 25px rgba(231, 76, 60, 0.3);
}

.asignar-tarea-mensaje i {
  font-size: 20px;
}

/* Responsive Design */
@media (max-width: 768px) {
  .asignar-tarea-container {
    padding: 0 12px;
  }
  
  .asignar-tarea-card {
    border-radius: 16px;
  }
  
  .asignar-tarea-header {
    padding: 30px 20px;
  }
  
  .asignar-tarea-title {
    font-size: 2em;
  }
  
  .asignar-tarea-form {
    padding: 24px 20px;
  }
  
  .asignar-tarea-section-content {
    padding: 24px 16px;
  }
  
  .asignar-tarea-row {
    grid-template-columns: 1fr;
    gap: 16px;
  }
  
  .asignar-tarea-checkbox-grid {
    grid-template-columns: 1fr;
  }
  
  .asignar-tarea-actions {
    flex-direction: column;
    padding: 0 20px;
  }
  
  .asignar-tarea-btn-primary,
  .asignar-tarea-btn-secondary {
    width: 100%;
  }
  
  .asignar-tarea-mensaje-wrapper {
    margin: 24px 16px;
    min-height: 48px;
  }
  .asignar-tarea-mensaje {
    padding: 16px 20px;
    font-size: 1em;
  }
}

@media (max-width: 480px) {
  .asignar-tarea-header {
    padding: 24px 16px;
  }
  
  .asignar-tarea-icon {
    width: 60px;
    height: 60px;
    margin-bottom: 16px;
  }
  
  .asignar-tarea-icon i {
    font-size: 28px;
  }
  
  .asignar-tarea-title {
    font-size: 1.8em;
  }
  
  .asignar-tarea-subtitle {
    font-size: 1em;
  }
  
  .asignar-tarea-section-title {
    padding: 16px 20px;
    font-size: 1.2em;
  }
  
  .asignar-tarea-checkbox-card {
    padding: 16px;
  }
  
  .asignar-tarea-checkbox-name {
    font-size: 1em;
  }
}

</style>