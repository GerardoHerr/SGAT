<template>
  <div class="container py-4">
    <div class="card border-0 shadow-sm">
      <div class="card-body">
        <h2 class="mb-4">
          <i class="fas fa-file-alt text-primary me-2"></i>Generación de Reportes
        </h2>
        
        <h4>Por favor, seleccione el curso y tipo de reporte para continuar:</h4>
        <div v-if="cargandoCursos" class="text-center py-4">
          <div class="spinner-border text-primary" role="status">
            <span class="visually-hidden">Cargando...</span>
          </div>
          <p class="mt-2 text-muted">Cargando cursos disponibles...</p>
        </div>
        
        <div v-else>
          <div class="row g-3">
            <div class="col-md-6">
              <div class="mb-3">
                <label for="curso" class="form-label">
                  <i class="fas fa-chalkboard-teacher me-1 text-muted"></i>Curso: 
                </label>
                <select 
                  v-model="cursoSeleccionado" 
                  id="curso" 
                  class="form-select"
                  :disabled="cargando"
                  @change="fetchTareas"
                >
                  <option disabled value="">Seleccione un curso</option>
                  <option v-for="curso in cursos" :key="curso.id" :value="curso.id">
                    {{ curso.asignatura_nombre }} - {{ curso.periodo }}
                  </option>
                </select>
              </div>
            </div>
            
            <div class="col-md-6">
              <div class="mb-3">
                <label for="tipo" class="form-label">
                  <i class="fas fa-file-alt me-1 text-muted"></i>Tipo de reporte: 
                </label>
                <select 
                  v-model="tipoReporte" 
                  id="tipo" 
                  class="form-select"
                  :disabled="!cursoSeleccionado || cargando"
                  @change="fetchTareas"
                >
                  <option disabled value="">Seleccione tipo</option>
                  <option value="entregas">Entregas de tareas</option>
                  <option value="tareas">Tareas del curso</option>
                </select>
              </div>
            </div>
          </div>
          
          <div class="d-flex justify-content-end mt-4">
            <button 
              class="btn btn-primary" 
              :disabled="!cursoSeleccionado || !tipoReporte || cargando" 
              @click="generarReporte"
            >
              <template v-if="cargando">
                <span class="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>
                Generando...
              </template>
              <template v-else>
                <i class="fas fa-file-export me-2"></i>Generar Reporte
              </template>
            </button>
          </div>
          
          <div v-if="error" class="alert alert-danger mt-3 mb-0" role="alert">
            <i class="fas fa-exclamation-circle me-2"></i>{{ error }}
          </div>
          
          <div v-if="reporteUrl" class="mt-4 pt-3 border-top">
            <div class="alert alert-success d-flex align-items-center" role="alert">
              <i class="fas fa-check-circle me-2"></i>
              <div>
                Reporte generado correctamente
              </div>
            </div>
            <a :href="reporteUrl" class="btn btn-outline-primary" target="_blank" download>
              <i class="fas fa-download me-2"></i>Descargar reporte
            </a>
          </div>
          
          <div v-if="reporteHtml" class="mt-4 border rounded p-3">
            <h5 class="mb-3">Vista previa del reporte</h5>
            <div class="reporte-preview" v-html="reporteHtml"></div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { getCursosDocente, generarReporteDocente, getTareasPorCurso, getEntregasPorCurso } from '@/services/reporteService';

export default {
  name: 'GeneracionReportes',
  data() {
    return {
      cursos: [],
      cursoSeleccionado: '',
      tipoReporte: '',
      tareas: [],
      entregas: [],
      cargando: false,
      cargandoCursos: true,
      error: null,
      reporteUrl: null,
      reporteHtml: '',
      currentUser: null
    };
  },
  methods: {
    async fetchTareas() {
      this.tareas = [];
      this.entregas = [];
      
      if (this.tipoReporte === 'entregas' && this.cursoSeleccionado) {
        try {
          // Primero obtenemos las tareas del curso seleccionado
          const tareasCurso = await getTareasPorCurso(this.cursoSeleccionado);
          const tareaIds = tareasCurso.map(t => t.id);
          // Luego traemos todas las entregas y filtramos solo las que correspondan a esas tareas
          const allEntregas = await getEntregasPorCurso(this.cursoSeleccionado);
          console.log('Entregas obtenidas:', allEntregas);
          this.entregas = allEntregas.filter(e => tareaIds.includes(e.tarea));
          console.log('Entregas filtradas:', this.entregas);
        } catch (e) {
          console.error('Error al cargar entregas:', e);
          this.entregas = [];
        }
      } else if (this.tipoReporte === 'tareas' && this.cursoSeleccionado) {
        try {
          this.tareas = await getTareasPorCurso(this.cursoSeleccionado);
          console.log('Tareas obtenidas:', this.tareas);
        } catch (e) {
          console.error('Error al cargar tareas:', e);
          this.tareas = [];
        }
      }
    },
    
    async generarReporte() {
      this.cargando = true;
      this.error = null;
      this.reporteUrl = null;
      this.reporteHtml = '';
      
      try {
        const res = await generarReporteDocente(this.cursoSeleccionado, this.tipoReporte);
        if (res.url) {
          this.reporteUrl = res.url;
        } else if (res.html) {
          this.reporteHtml = res.html;
        } else {
          this.error = 'No se pudo generar el reporte.';
        }
      } catch (e) {
        console.error('Error al generar reporte:', e);
        this.error = 'Error al generar el reporte. Por favor, intente nuevamente.';
      } finally {
        this.cargando = false;
      }
    },
    
    async cargarCursos() {
      this.cargandoCursos = true;
      this.error = null;
      
      try {
        let url = '';
        if (this.currentUser.rol === 'DOC') {
          url = `http://localhost:8000/api/cursos/?docente_email=${encodeURIComponent(this.currentUser.email)}`;
        } else if (this.currentUser.rol === 'EST') {
          url = `http://localhost:8000/api/cursos/?estudiante_email=${encodeURIComponent(this.currentUser.email)}`;
        } else {
          throw new Error('Rol de usuario no soportado');
        }
        const response = await fetch(url, {
          headers: { 'Content-Type': 'application/json' }
        });
        if (!response.ok) {
          throw new Error('Error al cargar los cursos');
        }
        this.cursos = await response.json();
      } catch (error) {
        console.error('Error al cargar cursos:', error);
        this.error = 'No se pudieron cargar los cursos. Por favor, intente más tarde.';
      } finally {
        this.cargandoCursos = false;
      }
    }
  },
  
  async mounted() {
    this.currentUser = JSON.parse(localStorage.getItem('currentUser'));
    
    if (!this.currentUser) {
      this.$router.push('/login');
      return;
    }
    
    await this.cargarCursos();
  }
};
</script>

<style scoped lang="scss">
@import '@/assets/styles/variables';
@import '@/assets/styles/base';

.reporte-container {
  max-width: 500px;
  margin: 40px auto;
  background: #fff;
  border-radius: 16px;
  box-shadow: 0 8px 24px rgba(0,0,0,0.10);
  padding: 32px 28px 24px 28px;
}
.reporte-container h2 {
  text-align: center;
  margin-bottom: 28px;
  color: #002147;
  font-size: 1.7rem;
  font-weight: 600;
}
.fade-enter-active, .fade-leave-active {
  transition: opacity 0.3s;
}
.fade-enter-from, .fade-leave-to {
  opacity: 0;
}
.reporte-form {
  display: flex;
  flex-direction: column;
  gap: 18px;
}
.form-group {
  display: flex;
  flex-direction: column;
  gap: 6px;
  margin-bottom: 10px;
}
.input-icon-group {
  position: relative;
  display: flex;
  align-items: center;
}
.input-icon-group i {
  position: absolute;
  left: 12px;
  color: #888;
  font-size: 1.1rem;
  z-index: 1;
}
.input-icon-group select {
  padding-left: 36px;
  width: 100%;
}
.btn-generar {
  width: 100%;
  padding: 15px;
  background: linear-gradient(90deg, #002147 60%, #005fa3 100%);
  color: #fff;
  font-size: 1.1rem;
  font-weight: 600;
  border: none;
  border-radius: 10px;
  cursor: pointer;
  margin-top: 18px;
  box-shadow: 0 2px 8px rgba(0,33,71,0.08);
  transition: background 0.2s, transform 0.2s;
}
.btn-generar:disabled {
  background: #a0aec0;
  cursor: not-allowed;
}
.centrado-tareas {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-top: 10px;
}
.titulo-tareas {
  margin-bottom: 10px;
  color: #002147;
  font-size: 1.1rem;
  font-weight: 600;
  text-align: center;
  letter-spacing: 0.5px;
}
.centrado-tareas ul {
  list-style: none;
  padding: 0;
  margin: 0;
  width: 100%;
  display: flex;
  flex-direction: column;
  gap: 10px;
}
.tarea-card {
  background: #f7fafc;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0,33,71,0.04);
  padding: 12px 18px;
  display: flex;
  align-items: center;
  gap: 12px;
  transition: box-shadow 0.2s;
}
.tarea-card i {
  color: #005fa3;
  font-size: 1.2rem;
}
.tarea-info {
  flex: 1;
  text-align: left;
}
.tarea-titulo {
  font-weight: 600;
  color: #222;
  font-size: 1rem;
}
.no-tareas {
  text-align: center;
  color: #888;
  margin: 12px 0 0 0;
  font-size: 1rem;
  display: flex;
  align-items: center;
  gap: 8px;
  justify-content: center;
}

select, button {
  padding: 12px;
  border-radius: 8px;
  border: 1px solid #d1d5db;
  font-size: 1rem;
}
button {
  background: #002147;
  color: #fff;
  font-weight: 600;
  border: none;
  cursor: pointer;
  transition: background 0.2s;
}
button:disabled {
  background: #a0aec0;
  cursor: not-allowed;
}
.error {
  margin-top: 18px;
  color: #c33;
  background: #fee;
  border: 1px solid #fcc;
  border-radius: 8px;
  padding: 10px;
  text-align: center;
}
.reporte-descarga {
  margin-top: 24px;
  text-align: center;
}
.reporte-descarga a {
  color: #002147;
  font-size: 1.1rem;
  font-weight: 600;
  text-decoration: none;
  display: inline-flex;
  align-items: center;
  gap: 8px;
}
.reporte-descarga a:hover {
  text-decoration: underline;
}
.reporte-preview {
  margin-top: 24px;
  background: #f7fafc;
  border-radius: 8px;
  padding: 18px;
  font-size: 0.98rem;
  color: #222;
}
.centrado-tareas {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-top: 10px;
}
.titulo-tareas {
  margin-bottom: 10px;
  color: #002147;
  font-size: 1.1rem;
  font-weight: 600;
  text-align: center;
}
.centrado-tareas ul {
  list-style: none;
  padding: 0;
  margin: 0;
  width: 100%;
}
.centrado-tareas li {
  text-align: center;
  margin-bottom: 6px;
}
</style>
